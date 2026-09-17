"""Unit tests for :mod:`cdf.local.event_graph`.

The event graph is the observational record, so the properties worth asserting
are structural: which relations appear between which events, that the relations
are the *event* vocabulary and never the causal one, that the edge count stays
bounded well below a complete graph, and that two builds of the same input agree
byte for byte.
"""

from __future__ import annotations

from typing import List, Optional

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import ParticipantEvidence
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventEdgeType,
    EventType,
    GraphDocument,
    Provenance,
    TrackSample,
    make_event_id,
    make_track_id,
)
from cdf.local.event_graph import build_event_graph, event_interval, subject_key

PARTICIPANT = "A"
TRACK_1 = make_track_id(PARTICIPANT, 1)
TRACK_2 = make_track_id(PARTICIPANT, 2)

EVENT_EDGE_VALUES = set(e.value for e in EventEdgeType)
CAUSAL_EDGE_VALUES = set(e.value for e in CausalEdgeType)


def make_event(
    t: float,
    event_type: EventType,
    subject: Optional[str] = None,
    duration: float = 0.2,
    confidence: float = 0.9,
    participant_id: str = PARTICIPANT,
) -> Event:
    """A local event with a deterministic id, as the extractor would emit it."""
    return Event(
        event_id=make_event_id("local", participant_id, event_type.value, t, subject),
        event_type=event_type,
        participant_id=participant_id,
        t_start=t,
        t_peak=t,
        t_end=t + duration,
        subject=subject,
        confidence=confidence,
        provenance=Provenance.LOCAL,
    )


def evidence(track_samples: Optional[List[TrackSample]] = None) -> ParticipantEvidence:
    return ParticipantEvidence(
        participant_id=PARTICIPANT, tracks=list(track_samples or [])
    )


def config(**overrides) -> Config:
    """The real threshold registry, optionally with an ``event_graph`` override."""
    cfg = load_run_config()
    if overrides:
        return cfg.with_overrides({"event_graph": overrides})
    return cfg


def edges_of(doc: GraphDocument, edge_type: EventEdgeType):
    return [e for e in doc.edges if e.edge_type == edge_type.value]


def scenario_events() -> List[Event]:
    """A small rear-end-like local trace: one track, one ego reaction, one outcome."""
    return [
        make_event(0.0, EventType.RADAR_TRACK_APPEARED, TRACK_1),
        make_event(1.0, EventType.TARGET_DECELERATION, TRACK_1),
        make_event(2.0, EventType.RAPID_CLOSING, TRACK_1),
        make_event(3.0, EventType.CRITICAL_TTC, TRACK_1),
        make_event(3.2, EventType.HARD_BRAKE),
        make_event(4.5, EventType.COLLISION),
    ]


# ---------------------------------------------------------------------------
# Document identity
# ---------------------------------------------------------------------------


def test_document_identity_and_nodes_are_preserved():
    events = scenario_events()
    doc = build_event_graph(
        events, evidence(), config(), run_id="R1", scenario_id="S01", seed=11
    )

    assert doc.graph_kind == "event"
    assert doc.scope is Provenance.LOCAL
    assert doc.owner == PARTICIPANT
    assert doc.run_id == "R1"
    assert doc.scenario_id == "S01"
    assert doc.seed == 11
    # Nodes are the input events, unchanged and in time order.
    assert sorted(doc.node_ids()) == sorted(e.event_id for e in events)
    assert [n.t_peak for n in doc.nodes] == sorted(e.t_peak for e in events)


def test_event_graph_uses_only_event_edge_types():
    doc = build_event_graph(scenario_events(), evidence(), config())

    assert doc.edges, "a six-event trace must produce edges"
    kinds = set(e.edge_type for e in doc.edges)
    assert kinds <= EVENT_EDGE_VALUES
    assert not (kinds & CAUSAL_EDGE_VALUES)
    # The relations the local layer can actually justify.
    assert EventEdgeType.PRECEDES.value in kinds
    assert EventEdgeType.SAME_TRACK.value in kinds
    # Cross-participant agreement relations belong to fusion, never to a local graph.
    assert EventEdgeType.ALIGNS_WITH.value not in kinds
    assert EventEdgeType.ASSOCIATED_WITH.value not in kinds


def test_every_edge_carries_provenance_owner_and_evidence():
    doc = build_event_graph(scenario_events(), evidence(), config())
    ids = set(doc.node_ids())

    for edge in doc.edges:
        assert edge.provenance is Provenance.LOCAL
        assert edge.owners == [PARTICIPANT]
        assert edge.source in ids and edge.target in ids
        refs = set(ev.ref for ev in edge.evidence if ev.kind == "event")
        assert {edge.source, edge.target} <= refs
        # An event-graph edge is a relation, not a rule-derived hypothesis.
        assert edge.rule is None


# ---------------------------------------------------------------------------
# PRECEDES
# ---------------------------------------------------------------------------


def test_precedes_links_each_event_to_the_next_few_and_is_annotated():
    events = scenario_events()
    fanout = 2
    doc = build_event_graph(events, evidence(), config(precedes_fanout=fanout))

    by_time = sorted(events, key=lambda e: e.t_peak)
    index = {e.event_id: i for i, e in enumerate(by_time)}
    precedes = edges_of(doc, EventEdgeType.PRECEDES)

    expected = sum(min(fanout, len(by_time) - 1 - i) for i in range(len(by_time)))
    assert len(precedes) == expected

    for edge in precedes:
        step = index[edge.target] - index[edge.source]
        assert 1 <= step <= fanout, "PRECEDES must stay inside the forward fan-out"
        source = by_time[index[edge.source]]
        target = by_time[index[edge.target]]
        assert source.t_peak <= target.t_peak
        # Disjoint intervals in this trace: the annotation must say so.
        if event_interval(source).end < event_interval(target).start:
            assert edge.temporal_relation == "before"
        assert edge.temporal_relation in {
            "before",
            "overlaps",
            "contains",
            "during",
            "equals",
        }


def test_precedes_never_points_backwards_in_time():
    doc = build_event_graph(scenario_events(), evidence(), config())
    t_peak = {n.event_id: n.t_peak for n in doc.nodes}
    for edge in edges_of(doc, EventEdgeType.PRECEDES):
        assert t_peak[edge.source] <= t_peak[edge.target]


# ---------------------------------------------------------------------------
# SAME_TRACK / OBSERVED_FROM
# ---------------------------------------------------------------------------


def test_same_track_edges_join_one_track_and_never_two():
    events = scenario_events() + [
        make_event(1.5, EventType.RADAR_TRACK_APPEARED, TRACK_2),
        make_event(2.5, EventType.LATERAL_CROSSING, TRACK_2),
        make_event(3.5, EventType.PREDICTED_PATH_CONFLICT, TRACK_2),
    ]
    doc = build_event_graph(events, evidence(), config(same_track_fanout=1))
    subject = {n.event_id: subject_key(n) for n in doc.nodes}

    same_track = edges_of(doc, EventEdgeType.SAME_TRACK)
    assert same_track
    for edge in same_track:
        assert subject[edge.source] is not None
        assert subject[edge.source] == subject[edge.target]

    # A chain over n events of one track has exactly n-1 links.
    n_track_1 = sum(1 for n in doc.nodes if subject_key(n) == TRACK_1)
    n_track_2 = sum(1 for n in doc.nodes if subject_key(n) == TRACK_2)
    assert len(same_track) == (n_track_1 - 1) + (n_track_2 - 1)

    # Ego events (HARD_BRAKE, COLLISION) have no track and cannot be chained.
    ego_ids = set(n.event_id for n in doc.nodes if subject_key(n) is None)
    for edge in same_track:
        assert edge.source not in ego_ids and edge.target not in ego_ids


def test_observed_from_points_at_the_appearance_of_its_own_track():
    events = scenario_events() + [
        make_event(1.5, EventType.RADAR_TRACK_APPEARED, TRACK_2),
        make_event(2.5, EventType.LATERAL_CROSSING, TRACK_2),
    ]
    samples = [
        TrackSample(t=0.0, frame=0, participant_id=PARTICIPANT, track_id=TRACK_1),
        TrackSample(t=4.0, frame=80, participant_id=PARTICIPANT, track_id=TRACK_1),
    ]
    doc = build_event_graph(events, evidence(samples), config())

    appearance = {
        subject_key(n): n.event_id
        for n in doc.nodes
        if n.event_type is EventType.RADAR_TRACK_APPEARED
    }
    node_type = {n.event_id: n.event_type for n in doc.nodes}
    subject = {n.event_id: subject_key(n) for n in doc.nodes}

    observed = edges_of(doc, EventEdgeType.OBSERVED_FROM)
    # Every track-scoped event except the appearances themselves must be anchored.
    derived = [
        n
        for n in doc.nodes
        if subject_key(n) is not None and n.event_type is not EventType.RADAR_TRACK_APPEARED
    ]
    assert len(observed) == len(derived)

    for edge in observed:
        assert node_type[edge.target] is EventType.RADAR_TRACK_APPEARED
        assert subject[edge.source] == subject[edge.target]
        assert edge.target == appearance[subject[edge.source]]

    # The track span from the evidence bundle is quoted as supporting evidence.
    track_1_edges = [e for e in observed if subject[e.source] == TRACK_1]
    assert track_1_edges
    spans = [ev for ev in track_1_edges[0].evidence if ev.kind == "track"]
    assert spans and spans[0].ref == TRACK_1
    assert spans[0].t_start == 0.0 and spans[0].t_end == 4.0


def test_observed_from_uses_the_most_recent_reacquisition():
    first = make_event(0.0, EventType.RADAR_TRACK_APPEARED, TRACK_1)
    second = make_event(5.0, EventType.RADAR_TRACK_APPEARED, TRACK_1, duration=0.1)
    late = make_event(6.0, EventType.RAPID_CLOSING, TRACK_1)
    early = make_event(1.0, EventType.RANGE_DECREASING, TRACK_1)

    doc = build_event_graph([first, second, late, early], evidence(), config())
    anchors = {
        e.source: e.target for e in edges_of(doc, EventEdgeType.OBSERVED_FROM)
    }
    assert anchors[late.event_id] == second.event_id
    assert anchors[early.event_id] == first.event_id


# ---------------------------------------------------------------------------
# INTERACTS_WITH
# ---------------------------------------------------------------------------


def test_interacts_with_links_own_behaviour_to_a_simultaneous_track_event():
    brake = make_event(3.2, EventType.HARD_BRAKE)
    critical = make_event(3.0, EventType.CRITICAL_TTC, TRACK_1)
    far_away = make_event(30.0, EventType.RAPID_CLOSING, TRACK_1)

    doc = build_event_graph(
        [brake, critical, far_away], evidence(), config(interacts_tolerance_s=0.5)
    )
    interacts = edges_of(doc, EventEdgeType.INTERACTS_WITH)

    assert [(e.source, e.target) for e in interacts] == [
        (brake.event_id, critical.event_id)
    ]
    # The edge inherits the mean confidence of the two estimates it relates.
    assert interacts[0].confidence == pytest.approx(
        0.5 * (brake.confidence + critical.confidence)
    )
    assert far_away.event_id not in {e.target for e in interacts}


def test_interacts_with_respects_its_per_event_limit():
    brake = make_event(5.0, EventType.HARD_BRAKE)
    track_events = [
        make_event(5.0 + 0.01 * i, EventType.RAPID_CLOSING, make_track_id(PARTICIPANT, i))
        for i in range(8)
    ]
    doc = build_event_graph(
        [brake] + track_events,
        evidence(),
        config(interacts_max_per_event=3, interacts_tolerance_s=1.0),
    )
    interacts = edges_of(doc, EventEdgeType.INTERACTS_WITH)
    assert len(interacts) == 3
    # The three kept partners are the ones closest in time to the brake.
    assert set(e.target for e in interacts) == set(
        e.event_id for e in track_events[:3]
    )


# ---------------------------------------------------------------------------
# Bounded size
# ---------------------------------------------------------------------------


def test_edge_count_stays_far_below_a_complete_graph():
    n = 60
    events = [make_event(0.1 * i, EventType.STEER_ONSET) for i in range(n)]
    fanout = 3
    doc = build_event_graph(events, evidence(), config(precedes_fanout=fanout))

    complete = n * (n - 1) // 2
    expected_precedes = sum(min(fanout, n - 1 - i) for i in range(n))
    assert len(edges_of(doc, EventEdgeType.PRECEDES)) == expected_precedes
    assert len(doc.edges) == expected_precedes
    assert len(doc.edges) < 0.2 * complete


def test_edge_budget_truncates_and_keeps_the_structural_relations():
    events = [make_event(0.0, EventType.RADAR_TRACK_APPEARED, TRACK_1)] + [
        make_event(0.5 * i, EventType.RANGE_DECREASING, TRACK_1) for i in range(1, 12)
    ]
    doc = build_event_graph(events, evidence(), config(max_edges=20))

    assert len(doc.edges) == 20
    assert doc.meta["edge_budget"]["truncated"] is True
    assert doc.meta["edge_budget"]["n_proposed"] > 20
    kinds = set(e.edge_type for e in doc.edges)
    # OBSERVED_FROM (11) + SAME_TRACK (11) already exceed the budget, so the
    # purely temporal PRECEDES edges are what gets dropped.
    assert kinds <= {EventEdgeType.OBSERVED_FROM.value, EventEdgeType.SAME_TRACK.value}
    assert doc.meta["limits"]["max_edges"] == 20


def test_partial_truncation_keeps_the_immediate_successor_chain():
    """When the budget bites inside a relation, the short hops must be what survive.

    Dropping ``PRECEDES`` wholesale is defensible -- it restates the timestamps.
    Dropping an arbitrary *part* of it is not: a hash-ordered scatter stitches the
    timeline together in a few places and severs it everywhere else, which reads
    as evidence of a gap that is really an artifact of the budget. The wide hops
    are the recoverable ones (precedence is transitive), so they are what a
    partial truncation must spend first.
    """
    events = [make_event(0.5 * i, EventType.STEER_ONSET) for i in range(12)]
    doc = build_event_graph(
        events, evidence(), config(precedes_fanout=3, max_edges=8)
    )
    index = {e.event_id: i for i, e in enumerate(events)}

    assert len(doc.edges) == 8
    steps = sorted(index[e.target] - index[e.source] for e in doc.edges)
    assert steps == [1] * 8, "budget kept wide hops while dropping adjacent links"


def test_meta_records_the_limits_actually_applied():
    doc = build_event_graph(scenario_events(), evidence(), config(precedes_fanout=2))
    limits = doc.meta["limits"]
    assert limits["precedes_fanout"] == 2
    assert doc.meta["n_nodes"] == len(doc.nodes)
    assert doc.meta["tracks"] == [TRACK_1]
    counts = doc.meta["edge_counts"]
    assert sum(counts.values()) == len(doc.edges)


# ---------------------------------------------------------------------------
# Boundary guards and determinism
# ---------------------------------------------------------------------------


def test_foreign_participant_event_is_rejected():
    events = scenario_events() + [
        make_event(2.0, EventType.HARD_BRAKE, participant_id="B")
    ]
    with pytest.raises(ValueError) as excinfo:
        build_event_graph(events, evidence(), config())
    assert "own evidence only" in str(excinfo.value)


def test_oracle_event_type_is_rejected():
    events = scenario_events() + [
        make_event(2.0, EventType.ORACLE_RIGHT_OF_WAY_CONFLICT)
    ]
    with pytest.raises(ValueError) as excinfo:
        build_event_graph(events, evidence(), config())
    assert "oracle-only" in str(excinfo.value)


def test_oracle_provenance_is_rejected():
    event = make_event(2.0, EventType.HARD_BRAKE)
    event.provenance = Provenance.ORACLE
    with pytest.raises(ValueError):
        build_event_graph([event], evidence(), config())


def test_empty_event_list_yields_an_empty_but_valid_document():
    doc = build_event_graph([], evidence(), config())
    assert doc.nodes == [] and doc.edges == []
    assert doc.graph_kind == "event" and doc.scope is Provenance.LOCAL


def test_build_is_deterministic():
    events = scenario_events()
    first = build_event_graph(events, evidence(), config())
    second = build_event_graph(list(reversed(events)), evidence(), config())

    def signature(doc: GraphDocument):
        return [
            (e.source, e.target, e.edge_type, round(e.confidence, 9), e.temporal_relation)
            for e in doc.edges
        ]

    assert signature(first) == signature(second)
    assert first.node_ids() == second.node_ids()
