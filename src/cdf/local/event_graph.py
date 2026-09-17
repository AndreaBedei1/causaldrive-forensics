"""Local event graph: what one vehicle observed, and how those observations relate.

The event graph is deliberately *not* a causal model. Its edges record relations
that can be read straight off the evidence without any theory of why things
happen: which event came before which (``PRECEDES``), which derived observation
came from which radar track (``OBSERVED_FROM``), which events concern the same
tracked object (``SAME_TRACK``), and which of our own manoeuvres coincided in
time with an interaction (``INTERACTS_WITH``). Causal claims live in a separate
document built by :mod:`cdf.local.causal_graph`, so that a reviewer can always
tell an observation apart from a hypothesis -- and so that an error in the causal
rule table can never corrupt the observational record.

``ALIGNS_WITH`` and ``ASSOCIATED_WITH`` are the two remaining event relations in
:class:`~cdf.common.schemas.EventEdgeType`. They express agreement *between*
participants and are therefore emitted only by the fusion layer; a local graph
never contains them.

Bounding the edge count
-----------------------
A graph with an edge for every ordered pair of events would be quadratic, would
be unreadable, and would say nothing: "everything precedes everything later" is
not evidence. Each relation is therefore limited to its informative neighbours --
a short forward fan-out in time for ``PRECEDES``, a chain per track for
``SAME_TRACK``, the nearest few overlapping partners for ``INTERACTS_WITH`` --
and the whole document is additionally capped by ``event_graph.max_edges``. Every
limit is configurable and the limits actually used are recorded in the document's
``meta`` block.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence
from ..common.schemas import (
    ORACLE_ONLY_EVENT_TYPES,
    Event,
    EventEdgeType,
    EventType,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from ..common.timeline import Interval, temporal_relation

__all__ = [
    "SELF_SUBJECT_ALIASES",
    "subject_key",
    "is_ego_event",
    "event_interval",
    "sort_events",
    "validated_local_nodes",
    "build_event_graph",
]


#: Subject values that mean "this event is about the observer itself" rather than
#: about a tracked object. The event extractor may leave the field unset or spell
#: it explicitly; both must be understood identically by every consumer.
SELF_SUBJECT_ALIASES: Tuple[str, ...] = ("", "self", "ego")

#: Relative priority of each relation when the global edge budget is exceeded.
#: The structural relations (which track an event belongs to, which observation
#: it came from) carry information that cannot be recovered from the node list,
#: whereas ``PRECEDES`` merely restates the timestamps, so it is dropped first.
_RELATION_PRIORITY: Dict[str, int] = {
    EventEdgeType.OBSERVED_FROM.value: 0,
    EventEdgeType.SAME_TRACK.value: 1,
    EventEdgeType.INTERACTS_WITH.value: 2,
    EventEdgeType.PRECEDES.value: 3,
}


# ---------------------------------------------------------------------------
# Event helpers (shared with the causal builder)
# ---------------------------------------------------------------------------


def subject_key(event: Event) -> Optional[str]:
    """The local radar track an event concerns, or ``None`` for an ego event.

    Normalising here means the rest of the pipeline never has to decide whether
    ``None``, ``""`` and ``"self"`` mean the same thing.
    """
    subject = event.subject
    if subject is None:
        return None
    text = str(subject).strip()
    if text.lower() in SELF_SUBJECT_ALIASES:
        return None
    return text


def is_ego_event(event: Event) -> bool:
    """Whether the event describes the observer itself rather than a track.

    Own-behaviour events (braking, steering, ...) and outcome events (collision,
    post-impact stop) are ego events; every radar/interaction event carries a
    track subject and is not.
    """
    return subject_key(event) is None


def event_interval(event: Event) -> Interval:
    """The closed time interval an event occupies.

    Most events are threshold crossings and have ``t_end is None``, which yields a
    degenerate interval at ``t_peak``; :func:`~cdf.common.timeline.temporal_relation`
    handles those through its tolerance argument. A negative-length interval is a
    malformed event, not something to paper over, so it raises.
    """
    t_start = float(event.t_start)
    t_peak = float(event.t_peak)
    if t_peak < t_start - 1e-6:
        raise ValueError(
            "event {0} has t_peak {1} before t_start {2}".format(
                event.event_id, t_peak, t_start
            )
        )
    if event.t_end is None:
        return Interval(min(t_start, t_peak), t_peak)
    t_end = float(event.t_end)
    if t_end < t_start - 1e-6:
        raise ValueError(
            "event {0} has t_end {1} before t_start {2}".format(
                event.event_id, t_end, t_start
            )
        )
    return Interval(min(t_start, t_peak), max(t_end, t_peak, t_start))


def sort_events(events: Sequence[Event]) -> List[Event]:
    """Events in a deterministic order: peak time, then type, then id.

    Reruns with the same seed must produce byte-identical artifacts, and the
    iteration order of the builders is what fixes the edge order, so the tie
    breakers matter even though they are arbitrary.
    """
    return sorted(
        events,
        key=lambda e: (
            float(e.t_peak),
            float(e.t_start),
            _type_value(e),
            str(e.event_id),
        ),
    )


def _type_value(event: Event) -> str:
    return (
        event.event_type.value
        if isinstance(event.event_type, EventType)
        else str(event.event_type)
    )


def validated_local_nodes(events: Sequence[Event], participant_id: str) -> List[Event]:
    """Sorted copy of ``events`` after the local-layer boundary checks.

    Shared by the event graph and the causal DAG so that both refuse the same
    inputs. The checks are leakage guards: a privileged event type or another
    participant's event reaching a *local* graph means the pipeline is mis-wired,
    and a silent pass there would invalidate every result downstream.
    """
    for event in events:
        if event.event_type in ORACLE_ONLY_EVENT_TYPES:
            raise ValueError(
                "oracle-only event type {0} reached the local event graph of "
                "participant {1!r} (event {2})".format(
                    _type_value(event), participant_id, event.event_id
                )
            )
        if event.provenance is Provenance.ORACLE:
            raise ValueError(
                "event {0} has oracle provenance and cannot enter a local "
                "graph".format(event.event_id)
            )
        if event.participant_id != participant_id:
            raise ValueError(
                "event {0} belongs to participant {1!r} but is being added to the "
                "local graph of {2!r}; every vehicle builds its graph from its own "
                "evidence only".format(
                    event.event_id, event.participant_id, participant_id
                )
            )
    return sort_events(events)


# ---------------------------------------------------------------------------
# Edge builders
# ---------------------------------------------------------------------------


def _event_evidence(event: Event, part: str) -> Evidence:
    """Back-pointer from an edge to one of the events it relates."""
    interval = event_interval(event)
    return Evidence(
        kind="event",
        ref=event.event_id,
        t_start=interval.start,
        t_end=interval.end,
        detail={"part": part, "event_type": _type_value(event)},
    )


def _relation_edge(
    source: Event,
    target: Event,
    edge_type: str,
    owner: str,
    tolerance_s: float,
    confidence: float,
    detail: Dict[str, Any],
) -> GraphEdge:
    """Assemble one event-graph edge with its temporal annotation and evidence."""
    relation = temporal_relation(
        event_interval(source), event_interval(target), tol=tolerance_s
    )
    return GraphEdge(
        source=source.event_id,
        target=target.event_id,
        edge_type=edge_type,
        confidence=float(confidence),
        provenance=Provenance.LOCAL,
        rule=None,
        temporal_relation=relation,
        evidence=[_event_evidence(source, "source"), _event_evidence(target, "target")],
        owners=[owner],
        detail=detail,
    )


def _precedes_edges(
    nodes: List[Event], owner: str, fanout: int, tolerance_s: float
) -> List[GraphEdge]:
    """``PRECEDES`` from each event to the next ``fanout`` events in time.

    Only the local neighbourhood is linked: transitive closure adds no
    information (precedence is transitive by construction) and would make the
    graph quadratic.
    """
    edges: List[GraphEdge] = []
    for i, source in enumerate(nodes):
        for target in nodes[i + 1 : i + 1 + fanout]:
            edges.append(
                _relation_edge(
                    source,
                    target,
                    EventEdgeType.PRECEDES.value,
                    owner,
                    tolerance_s,
                    confidence=1.0,
                    detail={"gap_s": round(float(target.t_peak) - float(source.t_peak), 6)},
                )
            )
    return edges


def _observed_from_edges(
    nodes: List[Event], ev: ParticipantEvidence, owner: str, tolerance_s: float
) -> List[GraphEdge]:
    """``OBSERVED_FROM`` from a radar-derived event to its track's appearance.

    This is the provenance relation of the local pipeline: it says "this claim
    exists because our radar was holding a track at the time", and it is what
    makes a spurious track's downstream events identifiable as such. When a track
    was re-acquired several times the most recent appearance at or before the
    event is used, because that is the acquisition the event actually rests on.
    """
    appearances: Dict[str, List[Event]] = {}
    for node in nodes:
        if node.event_type is EventType.RADAR_TRACK_APPEARED:
            key = subject_key(node)
            if key is not None:
                appearances.setdefault(key, []).append(node)
    for group in appearances.values():
        group.sort(key=lambda e: float(e.t_peak))

    edges: List[GraphEdge] = []
    for node in nodes:
        if node.event_type is EventType.RADAR_TRACK_APPEARED:
            continue
        key = subject_key(node)
        if key is None:
            continue
        group = appearances.get(key)
        if not group:
            continue
        earlier = [a for a in group if float(a.t_peak) <= float(node.t_peak)]
        anchor = earlier[-1] if earlier else group[0]
        if anchor.event_id == node.event_id:
            continue
        span = ev.track_span(key)
        detail: Dict[str, Any] = {"track": key}
        if span is not None:
            detail["track_t_start"] = span[0]
            detail["track_t_end"] = span[1]
        edge = _relation_edge(
            node,
            anchor,
            EventEdgeType.OBSERVED_FROM.value,
            owner,
            tolerance_s,
            confidence=1.0,
            detail=detail,
        )
        if span is not None:
            edge.evidence.append(
                Evidence(kind="track", ref=key, t_start=span[0], t_end=span[1])
            )
        edges.append(edge)
    return edges


def _same_track_edges(
    nodes: List[Event], owner: str, fanout: int, tolerance_s: float
) -> List[GraphEdge]:
    """``SAME_TRACK`` chaining the events of one local track in time order.

    A chain (rather than a clique) already expresses "these events are about one
    object" while staying linear in the number of events; ``fanout`` widens it
    when a denser identity relation is wanted.
    """
    by_subject: Dict[str, List[Event]] = {}
    for node in nodes:
        key = subject_key(node)
        if key is not None:
            by_subject.setdefault(key, []).append(node)

    edges: List[GraphEdge] = []
    for key in sorted(by_subject.keys()):
        group = by_subject[key]
        for i, source in enumerate(group):
            for target in group[i + 1 : i + 1 + fanout]:
                edges.append(
                    _relation_edge(
                        source,
                        target,
                        EventEdgeType.SAME_TRACK.value,
                        owner,
                        tolerance_s,
                        confidence=1.0,
                        detail={"track": key},
                    )
                )
    return edges


def _interacts_with_edges(
    nodes: List[Event],
    owner: str,
    pad_s: float,
    max_per_event: int,
    tolerance_s: float,
) -> List[GraphEdge]:
    """``INTERACTS_WITH`` between an ego event and a temporally overlapping track event.

    Direction is from the ego event to the track event by convention -- the
    relation is symmetric, and emitting it once keeps the document unambiguous.
    Intervals are padded by ``pad_s`` before the overlap test because most events
    are instantaneous threshold crossings that would otherwise never overlap
    anything; the pad is the "simultaneous enough to be worth relating" window.
    """
    ego = [n for n in nodes if is_ego_event(n)]
    tracked = [n for n in nodes if not is_ego_event(n)]
    edges: List[GraphEdge] = []
    for source in ego:
        source_iv = event_interval(source).expanded(pad_s)
        partners: List[Tuple[float, Event]] = []
        for target in tracked:
            if source_iv.intersects(event_interval(target)):
                partners.append(
                    (abs(float(target.t_peak) - float(source.t_peak)), target)
                )
        partners.sort(key=lambda item: (item[0], float(item[1].t_peak), item[1].event_id))
        for gap, target in partners[:max_per_event]:
            # Both nodes are estimates; the weakest one bounds how much the
            # coincidence is worth, so the edge inherits their mean confidence.
            confidence = 0.5 * (float(source.confidence) + float(target.confidence))
            edges.append(
                _relation_edge(
                    source,
                    target,
                    EventEdgeType.INTERACTS_WITH.value,
                    owner,
                    tolerance_s,
                    confidence=max(0.0, min(1.0, confidence)),
                    detail={
                        "track": subject_key(target),
                        "peak_gap_s": round(float(gap), 6),
                        "overlap_pad_s": float(pad_s),
                    },
                )
            )
    return edges


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def build_event_graph(
    events: Sequence[Event],
    ev: ParticipantEvidence,
    cfg: Config,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> GraphDocument:
    """Build one participant's local event graph from its own events.

    Parameters
    ----------
    events:
        The participant's local events. They become the graph's nodes unchanged;
        this function never invents or merges events.
    ev:
        The same participant's evidence bundle. Used for the owner id and for the
        track spans quoted as evidence on ``OBSERVED_FROM`` edges.
    cfg:
        Threshold registry. Keys read: ``event_graph.precedes_fanout``,
        ``event_graph.same_track_fanout``, ``event_graph.interacts_tolerance_s``,
        ``event_graph.interacts_max_per_event``, ``event_graph.max_edges`` and
        ``simulation.fixed_delta_seconds`` (used as the tolerance of the
        qualitative temporal relation: two events within one simulation tick are
        treated as simultaneous).

    Returns
    -------
    GraphDocument
        ``graph_kind="event"``, ``scope=LOCAL``, ``owner=ev.participant_id``.
    """
    nodes = validated_local_nodes(events, ev.participant_id)
    owner = ev.participant_id

    precedes_fanout = _non_negative_int(
        cfg.get("event_graph.precedes_fanout", 3), "event_graph.precedes_fanout"
    )
    same_track_fanout = _non_negative_int(
        cfg.get("event_graph.same_track_fanout", 1), "event_graph.same_track_fanout"
    )
    interacts_max = _non_negative_int(
        cfg.get("event_graph.interacts_max_per_event", 4),
        "event_graph.interacts_max_per_event",
    )
    max_edges = _non_negative_int(
        cfg.get("event_graph.max_edges", 5000), "event_graph.max_edges"
    )
    pad_s = float(cfg.get("event_graph.interacts_tolerance_s", 0.5))
    if pad_s < 0.0:
        raise ValueError(
            "event_graph.interacts_tolerance_s must not be negative, got {0!r}".format(pad_s)
        )
    tolerance_s = float(cfg.get("simulation.fixed_delta_seconds", 0.05))
    if tolerance_s < 0.0:
        raise ValueError(
            "simulation.fixed_delta_seconds must not be negative, got {0!r}".format(
                tolerance_s
            )
        )

    proposed: List[GraphEdge] = []
    proposed.extend(_precedes_edges(nodes, owner, precedes_fanout, tolerance_s))
    proposed.extend(_observed_from_edges(nodes, ev, owner, tolerance_s))
    proposed.extend(_same_track_edges(nodes, owner, same_track_fanout, tolerance_s))
    proposed.extend(
        _interacts_with_edges(nodes, owner, pad_s, interacts_max, tolerance_s)
    )

    kept = _apply_edge_budget(
        proposed, max_edges, {n.event_id: float(n.t_peak) for n in nodes}
    )
    kept.sort(key=_presentation_key)

    counts: Dict[str, int] = {}
    for edge in kept:
        counts[edge.edge_type] = counts.get(edge.edge_type, 0) + 1

    meta: Dict[str, Any] = {
        "note": (
            "event-graph edges are temporal, observational and identity relations; "
            "none of them is a causal claim"
        ),
        "n_nodes": len(nodes),
        "edge_counts": dict(sorted(counts.items())),
        "limits": {
            "precedes_fanout": precedes_fanout,
            "same_track_fanout": same_track_fanout,
            "interacts_max_per_event": interacts_max,
            "interacts_tolerance_s": pad_s,
            "max_edges": max_edges,
        },
        "relation_tolerance_s": tolerance_s,
        "edge_budget": {
            "limit": max_edges,
            "n_proposed": len(proposed),
            "n_kept": len(kept),
            "truncated": len(kept) < len(proposed),
        },
        "tracks": sorted({k for k in (subject_key(n) for n in nodes) if k is not None}),
    }

    return GraphDocument(
        graph_kind="event",
        scope=Provenance.LOCAL,
        owner=owner,
        run_id=run_id,
        scenario_id=scenario_id,
        seed=int(seed),
        nodes=nodes,
        edges=kept,
        meta=meta,
    )


def _apply_edge_budget(
    edges: List[GraphEdge], max_edges: int, t_peak: Dict[str, float]
) -> List[GraphEdge]:
    """Trim the proposal list to ``max_edges``, dropping the least informative first.

    ``max_edges <= 0`` disables the cap. Edges are ranked first by relation
    priority, so a whole class is given up before a more informative one loses a
    single edge, and then by the temporal distance they span.

    The second key is what makes a *partial* truncation survivable. The budget
    usually bites in the middle of a class rather than at its boundary, and
    ranking the remainder by event id would keep a hash-ordered scatter: the
    timeline would end up stitched together in a few places and severed
    everywhere else, which is worse than a uniformly coarser graph. Shortest
    first keeps the immediate-successor chain -- the part of ``PRECEDES`` that
    cannot be recovered by transitivity -- and spends whatever budget is left on
    the wider hops. Ties fall back to the presentation key, so the result is
    still fully deterministic and two runs of the same seed cannot differ.
    """
    if max_edges <= 0 or len(edges) <= max_edges:
        return list(edges)

    def rank(edge: GraphEdge) -> Tuple[Any, ...]:
        source_t = t_peak.get(edge.source)
        target_t = t_peak.get(edge.target)
        span = (
            abs(target_t - source_t)
            if source_t is not None and target_t is not None
            else float("inf")
        )
        return (
            _RELATION_PRIORITY.get(edge.edge_type, 9),
            round(span, 6),
        ) + _presentation_key(edge)

    return sorted(edges, key=rank)[:max_edges]


def _presentation_key(edge: GraphEdge) -> Tuple[str, str, str]:
    return (str(edge.source), str(edge.target), str(edge.edge_type))


def _non_negative_int(value: Any, dotted: str) -> int:
    """Coerce a configuration value to a non-negative int, or fail loudly."""
    try:
        out = int(value)
    except (TypeError, ValueError):
        raise TypeError("{0} must be an integer, got {1!r}".format(dotted, value))
    if out < 0:
        raise ValueError("{0} must not be negative, got {1!r}".format(dotted, value))
    return out
