"""Graph fusion: identity association, the global event graph, the global trace.

This runs only after every local graph exists and the alignment is known.

1. ``associate_tracks`` decides, for each anonymous local track, whether it can
   be named after another recorder.  The matched collision names the partner;
   the track must be its recorder's only persistent, continuous, approaching,
   speed-consistent track at the contact (the range at the contact weighs the
   confidence, it is no veto).  With insufficient or ambiguous evidence the
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
    """(range at the start, range at the end) of the last ``approach_window_s`` of tracking before the contact."""
    end = min(track.last_t, t_contact)
    window = [sample for sample in track.samples if end - cfg.approach_window_s - 1e-6 <= sample.t_local <= end + 1e-6]
    if len(window) < 2:
        return None
    return window[0].range_m, window[-1].range_m


def _range_factor(range_m: float, cfg: FusionConfig) -> float:
    """Confidence factor of the range at the contact: 1 up to ``contact_range_m``, then decaying."""
    excess = max(range_m - cfg.contact_range_m, 0.0)
    return math.exp(-0.5 * (excess / cfg.contact_range_scale_m) ** 2)


class _Evidence:
    """Evidence that one local track is the partner of the matched collision."""

    def __init__(self) -> None:
        self.lines: List[str] = []
        self.blocking: List[str] = []
        self.rmse: Optional[float] = None
        self.range_at_contact: Optional[float] = None

    def check(self, passed: bool, text: str) -> None:
        self.lines.append(text)
        if not passed:
            self.blocking.append(text)


def _evidence(track: LocalTrack, clock: GraphClock, partner: LocalReconstruction, partner_clock: GraphClock,
              cfg: FusionConfig) -> _Evidence:
    """Hierarchical evidence; every check but the range at the contact is required."""
    t_contact = clock.anchor_t_local
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
        evidence.check(last < first, "{0} before the contact: range {1:.1f} m -> {2:.1f} m over the last {3:.1f} s".format(
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

    near = [sample.range_m for sample in track.samples
            if t_contact - cfg.contact_window_s - 1e-6 <= sample.t_local <= t_contact + 1e-6]
    if near:
        evidence.range_at_contact = min(near)
        factor = _range_factor(evidence.range_at_contact, cfg)
        # Evidence, not a veto: radar mount, vehicle geometry and impact angle can keep it high.
        evidence.lines.append("range at the contact {0:.2f} m{1}".format(
            evidence.range_at_contact, "" if factor >= 0.999 else
            " (beyond {0:.2f} m: confidence factor {1:.2f})".format(cfg.contact_range_m, factor)))
    return evidence


def associate_tracks(locals_: Sequence[LocalReconstruction], alignment: Alignment,
                     cfg: FusionConfig) -> List[Association]:
    """One decision per anonymous local track, in a fixed order.

    The matched collision is the primary evidence of who the partner is.  A
    track is that partner when it is the only one of its recorder that is
    persistent, observed up to the contact (no TRACK_LOST before the contact
    window), approaching, and moving at the partner's own speed; the range at
    the contact only weighs the confidence.  Two or more such tracks are an
    ambiguity: they all stay anonymous.  Ground truth is never used.
    """
    by_owner = {local.owner: local for local in locals_}
    reference = next((event for event in alignment.matched_events
                      if event["event_id"] == alignment.reference_event), None)
    associations = []
    for local in sorted(locals_, key=lambda item: item.owner):
        owner = local.owner
        clock = alignment.graphs[owner]
        partner = None
        if clock.status == "ALIGNED" and reference is not None:
            others = [graph for graph in reference["graphs"] if graph != owner]
            partner = by_owner[others[0]] if len(others) == 1 else None
        if clock.status != "ALIGNED" or reference is None or partner is None:
            reason = ("graph {0} is not aligned: {1}".format(owner, clock.reason) if clock.status != "ALIGNED"
                      else "the reference collision has no single partner graph")
            associations.extend(Association(owner, track.track_id, owner + ":" + track.track_id, ANONYMOUS, None,
                                            [reason], [owner], blocking=[reason]) for track in local.tracks)
            continue
        header = "{0} and {1} both reported {2} (peak impulse {3} vs {4} N*s)".format(
            owner, partner.owner, reference["event_id"], reference["peak_impulse"][owner],
            reference["peak_impulse"][partner.owner])
        evidence = {track.track_id: _evidence(track, clock, partner, alignment.graphs[partner.owner], cfg)
                    for track in local.tracks}
        candidates = [track_id for track_id, item in evidence.items() if not item.blocking]
        for track in local.tracks:
            item = evidence[track.track_id]
            lines = [header] + item.lines
            sources = [owner, partner.owner]
            if item.blocking:
                associations.append(Association(owner, track.track_id, owner + ":" + track.track_id, ANONYMOUS, None,
                                                lines, sources, candidate=partner.owner, blocking=item.blocking))
            elif len(candidates) > 1:
                reason = "ambiguous: {0} persistent tracks of {1} are compatible with the contact ({2})".format(
                    len(candidates), owner, ", ".join(candidates))
                associations.append(Association(owner, track.track_id, owner + ":" + track.track_id, ANONYMOUS, None,
                                                lines + [reason], sources, candidate=partner.owner, blocking=[reason]))
            else:
                lines.append("the only track of {0} compatible with the contact".format(owner))
                # Confidence: collision match, reduced by speed disagreement and by a long range at the contact.
                confidence = (reference["confidence"] * math.exp(-0.5 * (item.rmse / cfg.speed_consistency_mps) ** 2)
                              * (_range_factor(item.range_at_contact, cfg) if item.range_at_contact is not None else 1.0))
                associations.append(Association(owner, track.track_id, partner.owner, ASSOCIATED, round(confidence, 2),
                                                lines, sources, candidate=partner.owner))
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
        for item in temporal_safety_relations(local.graph):
            entity, status = names.get((local.owner, item["track"]), (local.owner + ":" + item["track"], ANONYMOUS))
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
