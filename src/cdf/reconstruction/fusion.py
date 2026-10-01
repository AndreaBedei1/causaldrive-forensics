"""Graph fusion: identity association, the global event graph, the global trace.

This runs only after every local graph exists and the alignment is known.

1. ``associate_tracks`` decides, for each anonymous local track, whether it can
   be named after another recorder.  The evidence is taken around the matched
   collision.  With insufficient evidence the track keeps an anonymous global
   name such as ``A:track_001``: nothing is guessed.
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


def _range_at_contact(track: LocalTrack, t_contact: float, cfg: FusionConfig) -> Optional[float]:
    near = [sample.range_m for sample in track.samples
            if t_contact - cfg.contact_window_s - 1e-6 <= sample.t_local <= t_contact + 1e-6]
    return min(near) if near else None


def _decide(local: LocalReconstruction, track: LocalTrack, alignment: Alignment,
            reference: Optional[Dict[str, Any]], partner: Optional[LocalReconstruction],
            tracks_at_contact: List[str], cfg: FusionConfig) -> Association:
    owner = local.owner
    anonymous = owner + ":" + track.track_id
    clock = alignment.graphs[owner]
    if clock.status != "ALIGNED":
        reason = "graph {0} is not aligned: {1}".format(owner, clock.reason)
        return Association(owner, track.track_id, anonymous, ANONYMOUS, None, [reason], [owner],
                           blocking=[reason])
    if reference is None or partner is None:
        reason = "the reference collision has no single partner graph"
        return Association(owner, track.track_id, anonymous, ANONYMOUS, None, [reason], [owner],
                           blocking=[reason])

    t_contact = clock.anchor_t_local
    evidence = ["{0} and {1} both reported {2} (peak impulse {3} vs {4} N*s)".format(
        owner, partner.owner, reference["event_id"],
        reference["peak_impulse"][owner], reference["peak_impulse"][partner.owner])]
    blocking: List[str] = []

    def check(passed: bool, text: str) -> None:
        evidence.append(text)
        if not passed:
            blocking.append(text)

    seen_for = t_contact - track.first_t
    if seen_for >= cfg.min_track_persistence_s:
        check(True, "tracked for {0:.2f} s before the matched collision".format(seen_for))
    else:
        check(False, "tracked only {0:.2f} s before the matched collision (needs {1:.2f} s)".format(
            max(seen_for, 0.0), cfg.min_track_persistence_s))

    range_at_contact = _range_at_contact(track, t_contact, cfg)
    if range_at_contact is None and track.first_t > t_contact:
        check(False, "not at the contact: first seen {0:.2f} s after the matched collision".format(
            track.first_t - t_contact))
    elif range_at_contact is None:
        check(False, "not at the contact: last seen {0:.2f} s before the matched collision "
                     "(window {1:.2f} s)".format(t_contact - track.last_t, cfg.contact_window_s))
    elif range_at_contact <= cfg.contact_range_m:
        check(True, "at the contact: minimum range {0:.2f} m in the last {1:.2f} s before "
                    "the collision".format(range_at_contact, cfg.contact_window_s))
    else:
        check(False, "not at the contact: minimum range {0:.2f} m in the last {1:.2f} s "
                     "(needs <= {2:.2f} m)".format(range_at_contact, cfg.contact_window_s, cfg.contact_range_m))

    if len(tracks_at_contact) > 1:
        check(False, "ambiguous: {0} tracks of {1} were at the contact".format(len(tracks_at_contact), owner))
    elif tracks_at_contact == [track.track_id]:
        check(True, "the only track of {0} at the contact".format(owner))

    start = max(track.first_t, t_contact - SPEED_WINDOW_S)
    end = min(track.last_t, t_contact)
    rmse = None
    if end > start:
        rmse = _speed_rmse(track, clock, partner, alignment.graphs[partner.owner], start, end)
    if rmse is None:
        check(False, "speed not comparable with {0}'s own speed before the collision".format(partner.owner))
    elif rmse <= cfg.speed_consistency_mps:
        check(True, "track speed agrees with {0}'s own speed: RMSE {1:.2f} m/s over {2:.1f} s".format(
            partner.owner, rmse, end - start))
    else:
        check(False, "track speed disagrees with {0}'s own speed: RMSE {1:.2f} m/s (> {2:.2f})".format(
            partner.owner, rmse, cfg.speed_consistency_mps))

    sources = [owner, partner.owner]
    if blocking:
        return Association(owner, track.track_id, anonymous, ANONYMOUS, None, evidence, sources,
                           candidate=partner.owner, blocking=blocking)
    # Confidence: collision-match confidence, reduced by any speed disagreement.
    confidence = reference["confidence"] * math.exp(-0.5 * (rmse / cfg.speed_consistency_mps) ** 2)
    return Association(owner, track.track_id, partner.owner, ASSOCIATED, round(confidence, 2),
                       evidence, sources, candidate=partner.owner)


def associate_tracks(locals_: Sequence[LocalReconstruction], alignment: Alignment,
                     cfg: FusionConfig) -> List[Association]:
    """One decision per anonymous local track, in a fixed order."""
    by_owner = {local.owner: local for local in locals_}
    reference = next((event for event in alignment.matched_events
                      if event["event_id"] == alignment.reference_event), None)
    associations = []
    for local in sorted(locals_, key=lambda item: item.owner):
        clock = alignment.graphs[local.owner]
        partner = None
        at_contact: List[str] = []
        if clock.status == "ALIGNED" and reference is not None:
            others = [graph for graph in reference["graphs"] if graph != local.owner]
            partner = by_owner[others[0]] if len(others) == 1 else None
            for track in local.tracks:
                range_at_contact = _range_at_contact(track, clock.anchor_t_local, cfg)
                if range_at_contact is not None and range_at_contact <= cfg.contact_range_m:
                    at_contact.append(track.track_id)
        for track in local.tracks:
            associations.append(_decide(local, track, alignment, reference, partner, at_contact, cfg))
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


def short_label(node: GlobalNode) -> str:
    """COLLISION(A,B), BRAKE_START(B), CLOSING_START(A,B), TRACK_APPEARED(A,A:track_002)."""
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
