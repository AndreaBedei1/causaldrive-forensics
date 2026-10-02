"""Graph fusion: identity association, the global event graph, the global trace.

This runs only after every local graph exists and the alignment is known.

1. ``associate_tracks`` decides, for each anonymous local track, whether it can
   be named after another recorder.  Each matched collision of the recorder
   names a partner; the track must be its recorder's only persistent,
   continuous, approaching, speed-consistent track at that contact (the
   clearance at the contact weighs the confidence, it is no veto) and compatible with no
   other partner.  With insufficient, ambiguous or conflicting evidence the
   track keeps an anonymous global name such as ``A:track_001``: nothing is
   guessed.
2. ``fuse_graphs`` places every local node on the global time axis, merges the
   matched collision reports into one node and keeps the provenance (graph,
   local node, local time) of everything, including each observing recorder's
   own perceived state just before the event (local names, never rewritten).
3. ``global_trace`` groups the global nodes by global time for humans.
"""

from __future__ import annotations

import copy
import math
from typing import Any, Dict, List, Optional, Sequence

from .checks import temporal_safety_relations
from .config import FusionConfig
from .local import LocalReconstruction
from .models import (OUTCOME, SAME_TRACK, Alignment, Association, GlobalGraph, GlobalNode,
                     GraphClock, GraphEdge, Observation, display_order, precedes_edges)
from .tracking import LocalTrack

ASSOCIATED = "ASSOCIATED"
ANONYMOUS = "ANONYMOUS"
# Track speed and partner speed are compared over at most this long before contact.
SPEED_WINDOW_S = 3.0
SPEED_STEP_S = 0.1


# A track touches the recorder at a contact when observed this close to it in time.
TOUCH_WINDOW_S = 0.06


def _speed_rmse(track: LocalTrack, clock: GraphClock, partner: LocalReconstruction,
                partner_clock: GraphClock, start: float, end: float) -> Optional[float]:
    """Track speed versus the partner's own speed at the same global instants.

    Speed is a magnitude, so it can be compared although the two recorders
    have unrelated local frames.
    """
    errors = []
    steps = int(math.floor((end - start) / SPEED_STEP_S + 1e-6))
    for step in range(steps + 1):
        t_local = start + step * SPEED_STEP_S
        t_partner = t_local + clock.offset_to_global - partner_clock.offset_to_global
        sample = track.sample_near(t_local)
        if sample is not None and partner.ego.start <= t_partner <= partner.ego.end:
            errors.append(sample.speed_mps - partner.ego.at(t_partner).speed)
    if len(errors) < 3:
        return None
    return math.sqrt(sum(error * error for error in errors) / len(errors))


def _approach(track: LocalTrack, t_contact: float, cfg: FusionConfig) -> Optional[tuple]:
    """(clearance at the start, clearance at the end) of the last ``approach_window_s`` of tracking before the contact.

    The clearance (free distance from the recorder's own footprint to the
    target's near surface) rather than the range from the radar, which sits at
    the centre of the vehicle."""
    end = min(track.last_t, t_contact)
    window = [sample for sample in track.samples if end - cfg.approach_window_s - 1e-6 <= sample.t_local <= end + 1e-6]
    if len(window) < 2:
        return None
    return window[0].clearance_m, window[-1].clearance_m


def _range_factor(range_m: float, cfg: FusionConfig) -> float:
    """Confidence factor of the clearance at the contact: 1 up to ``contact_range_m``, then decaying."""
    excess = max(range_m - cfg.contact_range_m, 0.0)
    return math.exp(-0.5 * (excess / cfg.contact_range_scale_m) ** 2)


class _Evidence:
    """Evidence that one local track is the partner of the matched collision."""

    def __init__(self) -> None:
        self.lines: List[str] = []
        self.blocking: List[str] = []
        self.rmse: Optional[float] = None
        self.range_at_contact: Optional[float] = None
        self.clearance_at_contact: Optional[float] = None  # observed within one sample of the contact

    def check(self, passed: bool, text: str) -> None:
        self.lines.append(text)
        if not passed:
            self.blocking.append(text)


def _evidence(track: LocalTrack, t_contact: float, clock: GraphClock, partner: LocalReconstruction,
              partner_clock: GraphClock, cfg: FusionConfig) -> _Evidence:
    """Hierarchical evidence for one contact; every check but the clearance at the contact is required."""
    evidence = _Evidence()

    seen_for = t_contact - track.first_t
    evidence.check(seen_for >= cfg.min_track_persistence_s,
                   "tracked for {0:.2f} s before the matched collision{1}".format(
                       max(seen_for, 0.0), "" if seen_for >= cfg.min_track_persistence_s
                       else " (needs {0:.2f} s)".format(cfg.min_track_persistence_s)))

    if track.first_t > t_contact:
        evidence.check(False, "first seen {0:.2f} s after the matched collision".format(track.first_t - t_contact))
    else:
        gap = max(t_contact - track.last_t, 0.0)
        evidence.check(gap <= cfg.contact_window_s + 1e-6,
                       "continuous up to the contact: last observed {0:.2f} s before it (window {1:.2f} s)".format(
                           gap, cfg.contact_window_s) if gap <= cfg.contact_window_s + 1e-6 else
                       "lost {0:.2f} s before the matched collision (window {1:.2f} s)".format(gap, cfg.contact_window_s))

    approach = _approach(track, t_contact, cfg)
    if approach is None:
        evidence.check(False, "range trend before the contact not measurable")
    else:
        first, last = approach
        evidence.check(last < first, "{0} before the contact: clearance {1:.1f} m -> {2:.1f} m over the last {3:.1f} s".format(
            "approaching" if last < first else "not approaching", first, last, cfg.approach_window_s))

    start = max(track.first_t, t_contact - SPEED_WINDOW_S)
    end = min(track.last_t, t_contact)
    evidence.rmse = _speed_rmse(track, clock, partner, partner_clock, start, end) if end > start else None
    if evidence.rmse is None:
        evidence.check(False, "speed not comparable with {0}'s own speed before the collision".format(partner.owner))
    else:
        evidence.check(evidence.rmse <= cfg.speed_consistency_mps,
                       "track speed {0} {1}'s own speed: RMSE {2:.2f} m/s over {3:.1f} s{4}".format(
                           "agrees with" if evidence.rmse <= cfg.speed_consistency_mps else "disagrees with",
                           partner.owner, evidence.rmse, end - start,
                           "" if evidence.rmse <= cfg.speed_consistency_mps
                           else " (> {0:.2f})".format(cfg.speed_consistency_mps)))

    at_contact = [sample.clearance_m for sample in track.samples
                  if t_contact - TOUCH_WINDOW_S - 1e-6 <= sample.t_local <= t_contact + 1e-6 and sample.measured]
    evidence.clearance_at_contact = min(at_contact) if at_contact else None
    near = [sample.clearance_m for sample in track.samples
            if t_contact - cfg.contact_window_s - 1e-6 <= sample.t_local <= t_contact + 1e-6]
    if near:
        evidence.range_at_contact = min(near)
        factor = _range_factor(evidence.range_at_contact, cfg)
        # Evidence, not a veto: vehicle geometry, impact angle and a roof radar's view can keep it high.
        evidence.lines.append("clearance at the contact {0:.2f} m{1}".format(
            evidence.range_at_contact, "" if factor >= 0.999 else
            " (beyond {0:.2f} m: confidence factor {1:.2f})".format(cfg.contact_range_m, factor)))
    return evidence


def _touching(event_id: str, rivals: Sequence[str], checks: Dict[Any, "_Evidence"],
              cfg: FusionConfig) -> Optional[str]:
    """The only compatible track touching the recorder at the contact, all rivals clearly apart; else None."""
    def clearance(track_id: str) -> Optional[float]:
        return checks[(event_id, track_id)].clearance_at_contact
    touching = [t for t in rivals if clearance(t) is not None and clearance(t) <= cfg.touching_clearance_m]
    if len(touching) != 1:
        return None
    others = [t for t in rivals if t != touching[0]]
    if all(clearance(t) is not None and clearance(t) >= cfg.rival_clearance_m for t in others):
        return touching[0]
    return None


def _partner(event: Dict[str, Any], owner: str) -> str:
    return next(graph for graph in event["graphs"] if graph != owner)


def recorder_contacts(owner: str, alignment: Alignment) -> List[Dict[str, Any]]:
    """The matched collisions of one recorder whose graphs are all aligned, in its local time order."""
    return sorted((event for event in alignment.matched_events if owner in event["graphs"]
                   and all(alignment.graphs[graph].status == "ALIGNED" for graph in event["graphs"])),
                  key=lambda event: event["t_local"][owner])


def associate_tracks(locals_: Sequence[LocalReconstruction], alignment: Alignment,
                     cfg: FusionConfig) -> List[Association]:
    """One decision per anonymous local track, in a fixed order.

    Every matched collision of a recorder names a partner: the other recorder
    of that contact.  Per contact, a track is compatible with the partner when
    it is persistent, observed up to the contact (no TRACK_LOST before the
    contact window), approaching, and moving at the partner's own speed; the
    clearance at the contact only weighs the confidence.  A track is named after a
    partner when it is its recorder's only compatible track for a contact with
    that partner and is compatible with no other partner.  Two or more
    compatible tracks for one contact are an ambiguity, unless exactly one of
    them touches the recorder at the contact (observed within one sample of it,
    within ``touching_clearance_m``) while every rival is at least
    ``rival_clearance_m`` away: a body in contact is at the recorder's skin.  One
    track compatible with two partners is a conflict.  Ambiguous and conflicting
    tracks stay anonymous.  Ground truth is never used.
    """
    by_owner = {local.owner: local for local in locals_}
    associations = []
    for local in sorted(locals_, key=lambda item: item.owner):
        owner = local.owner
        clock = alignment.graphs[owner]
        contacts = recorder_contacts(owner, alignment)
        if clock.status != "ALIGNED" or not contacts:
            reason = ("graph {0} is not aligned: {1}".format(owner, clock.reason) if clock.status != "ALIGNED"
                      else "no matched collision of {0} names a partner".format(owner))
            associations.extend(Association(owner, track.track_id, owner + ":" + track.track_id, ANONYMOUS, None,
                                            [reason], [owner], blocking=[reason]) for track in local.tracks)
            continue
        several = len(contacts) > 1
        checks: Dict[Any, _Evidence] = {}
        for event in contacts:
            partner = by_owner[_partner(event, owner)]
            for track in local.tracks:
                checks[(event["event_id"], track.track_id)] = _evidence(
                    track, event["t_local"][owner], clock, partner, alignment.graphs[partner.owner], cfg)
        compatible = {event["event_id"]: [track.track_id for track in local.tracks
                                          if not checks[(event["event_id"], track.track_id)].blocking]
                      for event in contacts}
        touching = {event_id: _touching(event_id, rivals, checks, cfg)
                    for event_id, rivals in compatible.items() if len(rivals) > 1}

        def header(event: Dict[str, Any]) -> str:
            partner = _partner(event, owner)
            return "{0} and {1} both reported {2}{3} (peak impulse {4} vs {5} N*s)".format(
                owner, partner, event["event_id"],
                " at {0:.2f} s".format(event["t_local"][owner]) if several else "",
                event["peak_impulse"][owner], event["peak_impulse"][partner])

        def prefixed(event: Dict[str, Any], reasons: Sequence[str]) -> List[str]:
            if not several:
                return list(reasons)
            return ["{0} with {1}: {2}".format(event["event_id"], _partner(event, owner), reason)
                    for reason in reasons]

        for track in local.tracks:
            fits = [event for event in contacts if track.track_id in compatible[event["event_id"]]]
            partners = sorted({_partner(event, owner) for event in fits})
            unique = [event for event in fits if compatible[event["event_id"]] == [track.track_id]
                      or touching.get(event["event_id"]) == track.track_id]
            # The contact the decision rests on: one where the track is the only compatible
            # one, else a compatible one, else the contact with the fewest failed checks.
            if unique:
                basis = max(unique, key=lambda event: event["confidence"])
            elif fits:
                basis = fits[0]
            else:
                basis = min(contacts, key=lambda event: len(checks[(event["event_id"], track.track_id)].blocking))
            item = checks[(basis["event_id"], track.track_id)]
            lines = [header(basis)] + item.lines
            # The recorder's other contacts, in one line each.
            others = ["{0} with {1} at {2:.2f} s: {3}".format(
                event["event_id"], _partner(event, owner), event["t_local"][owner],
                "also compatible" if not checks[(event["event_id"], track.track_id)].blocking
                else "not compatible (" + "; ".join(checks[(event["event_id"], track.track_id)].blocking) + ")")
                for event in contacts if event is not basis]
            candidate = _partner(basis, owner)
            sources = [owner, candidate]
            anonymous = owner + ":" + track.track_id
            if not fits:
                associations.append(Association(owner, track.track_id, anonymous, ANONYMOUS, None, lines + others,
                                                sources, candidate=candidate, blocking=prefixed(basis, item.blocking),
                                                collision_event=basis["event_id"]))
            elif len(partners) > 1:
                reason = "conflict: compatible with the contacts with {0}".format(" and ".join(
                    "{0} ({1})".format(_partner(event, owner), event["event_id"]) for event in fits))
                associations.append(Association(owner, track.track_id, anonymous, ANONYMOUS, None,
                                                lines + others + [reason], [owner] + partners,
                                                candidate=candidate, blocking=[reason],
                                                collision_event=basis["event_id"]))
            elif not unique:
                rivals = compatible[basis["event_id"]]
                reason = "ambiguous: {0} persistent tracks of {1} are compatible with the contact{2} ({3})".format(
                    len(rivals), owner, " " + basis["event_id"] if several else "", ", ".join(rivals))
                associations.append(Association(owner, track.track_id, anonymous, ANONYMOUS, None,
                                                lines + others + [reason], sources,
                                                candidate=candidate, blocking=[reason],
                                                collision_event=basis["event_id"]))
            else:
                rivals = [t for t in compatible[basis["event_id"]] if t != track.track_id]
                if rivals:
                    lines.append("the only compatible track of {0} touching it at the contact (clearance {1:.2f} m; "
                                 "{2} at {3})".format(owner, item.clearance_at_contact, ", ".join(rivals), ", ".join(
                                     "{0:.2f} m".format(checks[(basis["event_id"], t)].clearance_at_contact)
                                     for t in rivals)))
                else:
                    lines.append("the only track of {0} compatible with the contact".format(owner))
                # Confidence: collision match, reduced by speed disagreement and by a long clearance at the contact.
                confidence = (basis["confidence"] * math.exp(-0.5 * (item.rmse / cfg.speed_consistency_mps) ** 2)
                              * (_range_factor(item.range_at_contact, cfg) if item.range_at_contact is not None
                                 else 1.0))
                associations.append(Association(owner, track.track_id, candidate, ASSOCIATED, round(confidence, 2),
                                                lines + others, sources, candidate=candidate,
                                                collision_event=basis["event_id"]))
    return associations


def _global_subject(owner: str, subject: Optional[str], names: Dict[Any, str]) -> Optional[str]:
    if subject is None:
        return None
    return names.get((owner, subject), owner + ":" + subject)


def fuse_graphs(locals_: Sequence[LocalReconstruction], alignment: Alignment,
                associations: Sequence[Association]) -> GlobalGraph:
    """Local graphs + alignment + associations -> one global event graph."""
    names = {(item.local_graph, item.local_track): item.global_entity for item in associations}
    recorders = sorted(local.owner for local in locals_)
    merged_events = [event for event in alignment.matched_events
                     if all(alignment.graphs[graph].status == "ALIGNED" for graph in event["graphs"])]
    merged_node_ids = {node_id for event in merged_events for node_id in event["nodes"].values()}

    drafts: List[GlobalNode] = []
    local_nodes = {(local.owner, node.node_id): node for local in locals_ for node in local.graph.nodes}

    def beliefs(observations: Sequence[Observation]) -> Dict[str, Dict[str, Any]]:
        out = {}
        for obs in observations:
            state = local_nodes[(obs.graph, obs.local_node)].perceived_state_before
            if state is not None:
                out[obs.graph] = copy.deepcopy(state)
        return out

    for local in sorted(locals_, key=lambda item: item.owner):
        clock = alignment.graphs[local.owner]
        for node in local.graph.nodes:
            if node.node_id in merged_node_ids:
                continue
            subject = _global_subject(local.owner, node.subject_id, names)
            participants = [local.owner] + ([subject] if subject in recorders and subject != local.owner else [])
            drafts.append(GlobalNode(
                node_id="", event_type=node.event_type, kind=node.kind, actor_id=local.owner,
                subject_id=subject, participants=participants, t_global=clock.to_global(node.t_local),
                attributes=dict(node.attributes),
                source=node.source, confidence=node.confidence,
                observations=[Observation(local.owner, node.node_id, node.t_local)]))
            drafts[-1].perceived_state_before = beliefs(drafts[-1].observations)
    for event in merged_events:
        graphs = sorted(event["graphs"])
        times = [alignment.graphs[graph].to_global(event["t_local"][graph]) for graph in graphs]
        drafts.append(GlobalNode(
            node_id="", event_type="COLLISION", kind=OUTCOME, actor_id=None, subject_id=None,
            participants=graphs, t_global=round(sum(times) / len(times), 4),
            attributes={"matched_event": event["event_id"],
                        "reference_event": event["event_id"] == alignment.reference_event,
                        "peak_impulse": dict(event["peak_impulse"])},
            source="collision_sensor", confidence=event["confidence"],
            observations=[Observation(graph, event["nodes"][graph], event["t_local"][graph]) for graph in graphs]))
        drafts[-1].perceived_state_before = beliefs(drafts[-1].observations)

    aligned = display_order([node for node in drafts if node.t_global is not None],
                            lambda node: node.t_global, lambda node: node.event_type,
                            lambda node: node.actor_id, lambda node: node.subject_id)
    unaligned = sorted((node for node in drafts if node.t_global is None),
                       key=lambda node: (node.observations[0].graph, node.observations[0].t_local))
    nodes = aligned + unaligned
    for number, node in enumerate(nodes, 1):
        node.node_id = "g{0:02d}".format(number)

    global_id = {obs.local_node: node.node_id for node in nodes for obs in node.observations}
    # Nodes at the same global time are simultaneous at this resolution: no PRECEDES between them.
    edges = precedes_edges(aligned, lambda node: node.t_global, lambda node: node.node_id)
    for local in sorted(locals_, key=lambda item: item.owner):
        for edge in local.graph.edges:
            if edge.relation == SAME_TRACK:
                edges.append(GraphEdge(global_id[edge.from_node], global_id[edge.to_node], SAME_TRACK))

    entities = []
    for owner in recorders:
        aliases = [item.local_graph + ":" + item.local_track for item in associations
                   if item.status == ASSOCIATED and item.global_entity == owner]
        entities.append({"entity_id": owner, "kind": "recorder",
                         "clock": alignment.graphs[owner].status, "observed_as": aliases})
    for item in associations:
        if item.status == ANONYMOUS:
            entities.append({"entity_id": item.global_entity, "kind": "anonymous_track",
                             "observed_by": item.local_graph, "candidate": item.candidate})
    return GlobalGraph(entities=entities, nodes=nodes, edges=edges)


def global_temporal_relations(locals_: Sequence[LocalReconstruction], alignment: Alignment,
                              associations: Sequence[Association]) -> List[Dict[str, Any]]:
    """``checks.temporal_safety_relations`` of every local graph, with the track's
    identity decision and global times; temporal properties only, no causality."""
    names = {(item.local_graph, item.local_track): (item.global_entity, item.status) for item in associations}
    out = []
    for local in sorted(locals_, key=lambda item: item.owner):
        clock = alignment.graphs[local.owner]
        # An identified track's collision is the recorder's collision with that entity.
        with_entity: Dict[str, List[float]] = {}
        for event in recorder_contacts(local.owner, alignment):
            with_entity.setdefault(_partner(event, local.owner), []).append(event["t_local"][local.owner])
        partner_collisions = {track: with_entity.get(entity, []) for (owner, track), (entity, status) in names.items()
                              if owner == local.owner and status == ASSOCIATED}
        for item in temporal_safety_relations(local.graph, partner_collisions):
            entity, status = names.get((local.owner, item["track"]), (local.owner + ":" + item["track"], ANONYMOUS))
            if item["track"] in partner_collisions:
                item["collision_with"] = entity
            times = {"cut_in": item["cut_in"]["t_local"] if item["cut_in"] else None,
                     "critical_ttc_start": item["critical_ttc_start"], "ego_path_entry": item["ego_path_entry"],
                     "collision": item["collision"]}
            t_global = {key: clock.to_global(value) for key, value in times.items() if value is not None}
            out.append(dict(item, recorder=local.owner, entity=entity, association=status,
                            t_global={key: value for key, value in t_global.items() if value is not None}))
    return out


def short_label(node: GlobalNode) -> str:
    """COLLISION(A,B), BRAKE_START(B), CLOSING_START(A,B), TRACK_APPEARED_LEFT(A,A:track_002)."""
    if node.actor_id is None:
        return "{0}({1})".format(node.event_type, ",".join(node.participants))
    names = [node.actor_id] + ([node.subject_id] if node.subject_id else [])
    return "{0}({1})".format(node.event_type, ",".join(names))


def global_trace(graph: GlobalGraph) -> List[Dict[str, Any]]:
    """({(event, id, attributes), ...}, t_global) rows; simultaneous events share a row."""
    rows: Dict[float, List[GlobalNode]] = {}
    for node in graph.nodes:
        if node.t_global is not None:
            rows.setdefault(round(node.t_global, 2), []).append(node)
    trace = []
    for t_global in sorted(rows):
        nodes = rows[t_global]
        trace.append({"t_global": t_global,
                      "text": "; ".join(short_label(node) for node in nodes),
                      "events": [{"id": node.node_id, "type": node.event_type, "actor": node.actor_id,
                                  "subject": node.subject_id, "participants": node.participants,
                                  "attributes": node.attributes} for node in nodes]})
    return trace
