"""The reference a reconstruction is actually judged against.

A structural metric is only meaningful if both graphs are allowed to say the same
things. These tests fix that property, from both directions: the reference may
not assert anything no reconstruction could emit, and it must assert the things a
reconstruction does emit, so that a correct reconstruction can match it.

They also fix the part that keeps the comparison honest. The reference shares its
*definitions* with the inference layer -- what counts as hard deceleration must
mean one thing -- and measures them independently, from exact state. A reference
that shared its detection code would agree by construction and measure nothing.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

import pytest

from cdf.common.config import load_run_config, repo_root
from cdf.common.schemas import CausalEdgeType, EventType, Provenance
from cdf.graph.ontology import (
    COMPARABLE_EDGE_TYPES,
    COMPARABLE_EVENT_TYPES,
    DESIGN_REFERENCE_EVENT_TYPES,
    SENSOR_RELATIVE_EVENT_TYPES,
    comparable_view,
    describe,
    exclusion_reason,
    family,
    is_comparable,
)
from cdf.oracle.observable import (
    ObservableExtractor,
    build_observable_events,
    pairwise_truth,
)
from cdf.oracle.observable_graph import (
    OBSERVABLE_RULES,
    ObservableRule,
    build_observable_causal_graph,
)


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


# ---------------------------------------------------------------------------
# The ontology
# ---------------------------------------------------------------------------


def test_every_event_type_is_classified_exactly_once() -> None:
    """A type with no classification would silently fall out of every metric."""
    declared = {e.value for e in EventType}
    classified = (
        COMPARABLE_EVENT_TYPES | SENSOR_RELATIVE_EVENT_TYPES
        | DESIGN_REFERENCE_EVENT_TYPES
    )
    assert declared == classified, sorted(declared ^ classified)
    assert not (COMPARABLE_EVENT_TYPES & SENSOR_RELATIVE_EVENT_TYPES)
    assert not (COMPARABLE_EVENT_TYPES & DESIGN_REFERENCE_EVENT_TYPES)
    assert not (SENSOR_RELATIVE_EVENT_TYPES & DESIGN_REFERENCE_EVENT_TYPES)


def test_the_privileged_types_are_not_comparable() -> None:
    """These are what made the old comparison unfair; they must stay excluded."""
    for name in ("ORACLE_SCRIPTED_INTERVENTION", "ORACLE_RIGHT_OF_WAY_CONFLICT",
                 "ORACLE_SIGNAL_VIOLATION"):
        assert not is_comparable(name)
        assert "design reference" in exclusion_reason(name)


def test_a_radar_track_event_is_excluded_as_sensor_relative() -> None:
    """The simulator has vehicles, not tracks; there is nothing to compare to."""
    for name in ("RADAR_TRACK_APPEARED", "RADAR_TRACK_LOST"):
        assert not is_comparable(name)
        assert "instrument" in exclusion_reason(name)


def test_every_exclusion_states_a_reason() -> None:
    """A metric that silently drops nodes can be gamed by emitting more of them."""
    for name in sorted(SENSOR_RELATIVE_EVENT_TYPES | DESIGN_REFERENCE_EVENT_TYPES):
        reason = exclusion_reason(name)
        assert reason and len(reason) > 20, name
    for name in sorted(COMPARABLE_EVENT_TYPES):
        assert exclusion_reason(name) is None, name


def test_each_comparable_type_belongs_to_one_family() -> None:
    for name in sorted(COMPARABLE_EVENT_TYPES):
        assert family(name) in {"own_motion", "pairwise", "outcome"}, name
    assert family("RADAR_TRACK_APPEARED") is None


def test_the_causal_relation_vocabulary_is_shared_whole() -> None:
    assert COMPARABLE_EDGE_TYPES == {e.value for e in CausalEdgeType}


def test_the_contract_is_serialisable_for_artifacts_and_tests() -> None:
    import json

    contract = describe()
    json.dumps(contract)
    assert contract["comparable_event_types"]
    assert set(contract["families"]["own_motion"]) <= set(
        contract["comparable_event_types"]
    )


# ---------------------------------------------------------------------------
# comparable_view
# ---------------------------------------------------------------------------


def _graph(nodes, edges, scope=Provenance.FUSED):
    from cdf.common.schemas import GraphDocument

    return GraphDocument(
        graph_kind="causal", scope=scope, owner=None, run_id="R",
        scenario_id="S01", seed=0, nodes=nodes, edges=edges, meta={},
    )


def _node(event_id, event_type, participant="A", t=1.0, subject=None):
    from cdf.common.schemas import Event

    return Event(
        event_id=event_id, event_type=event_type, participant_id=participant,
        t_start=t, t_peak=t, t_end=t + 0.1, subject=subject, values={},
        confidence=1.0, evidence=[], provenance=Provenance.FUSED,
        owners=[participant],
    )


def _edge(source, target):
    from cdf.common.schemas import GraphEdge

    return GraphEdge(
        source=source, target=target, edge_type=CausalEdgeType.TRIGGERS.value,
        confidence=0.9, provenance=Provenance.FUSED, rule="r", detail={},
    )


def test_the_comparable_view_drops_a_node_and_the_edges_that_touched_it() -> None:
    doc = _graph(
        [
            _node("track", EventType.RADAR_TRACK_APPEARED),
            _node("brake", EventType.BRAKE_ONSET),
            _node("decel", EventType.DECELERATION),
        ],
        [_edge("track", "brake"), _edge("brake", "decel")],
    )
    view = comparable_view(doc)
    assert {n.event_id for n in view.nodes} == {"brake", "decel"}
    assert [(e.source, e.target) for e in view.edges] == [("brake", "decel")]
    ontology = view.meta["ontology"]
    assert ontology["n_nodes_dropped"] == 1
    assert ontology["n_edges_dropped"] == 1
    assert "RADAR_TRACK_APPEARED" in ontology["dropped_node_types"]
    assert ontology["reasons"]["RADAR_TRACK_APPEARED"]


def test_the_comparable_view_leaves_a_fully_comparable_graph_alone() -> None:
    doc = _graph(
        [_node("brake", EventType.BRAKE_ONSET), _node("decel", EventType.DECELERATION)],
        [_edge("brake", "decel")],
    )
    view = comparable_view(doc)
    assert len(view.nodes) == 2 and len(view.edges) == 1
    assert view.meta["ontology"]["n_nodes_dropped"] == 0


# ---------------------------------------------------------------------------
# The observable extractor
# ---------------------------------------------------------------------------


REAL_RUN = repo_root() / "artifacts_independent_clocks" / "S01_rear_end" / "seed_000_crash"


@pytest.fixture(scope="module")
def real_trace():
    if not REAL_RUN.is_dir():
        pytest.skip("the reference run is not present in this checkout")
    from cdf.oracle.events import load_oracle_trace

    return load_oracle_trace(REAL_RUN)


@pytest.fixture(scope="module")
def observable(real_trace, cfg):
    return build_observable_events(real_trace, cfg)


def test_the_reference_asserts_only_the_comparable_vocabulary(observable) -> None:
    """The property the whole refactor exists to establish."""
    offenders = sorted({
        e.event_type.value for e in observable if not is_comparable(e.event_type)
    })
    assert offenders == [], offenders


def test_the_reference_contains_no_scripted_intervention(observable) -> None:
    types = {e.event_type.value for e in observable}
    assert EventType.ORACLE_SCRIPTED_INTERVENTION.value not in types
    assert EventType.ORACLE_RIGHT_OF_WAY_CONFLICT.value not in types


def test_the_reference_asserts_what_a_vehicle_would_also_assert(observable) -> None:
    """Not merely "nothing forbidden" -- it has to be rich enough to match."""
    types = {e.event_type.value for e in observable}
    for expected in ("BRAKE_ONSET", "DECELERATION", "HARD_DECELERATION",
                     "RANGE_DECREASING", "CRITICAL_TTC", "COLLISION"):
        assert expected in types, expected


def test_every_reference_event_carries_privileged_evidence(observable) -> None:
    for event in observable:
        assert event.provenance is Provenance.ORACLE
        assert event.evidence, event.event_id
        assert event.confidence == 1.0, (
            "ground truth measures rather than estimates; it is not unsure"
        )


def test_pairwise_events_name_an_observer_and_a_subject(observable) -> None:
    for event in observable:
        if family(event.event_type) == "pairwise":
            assert event.subject, event.event_id
            assert event.subject != event.participant_id
        elif family(event.event_type) == "own_motion":
            assert event.subject is None, event.event_id


def test_extraction_is_deterministic(real_trace, cfg) -> None:
    first = build_observable_events(real_trace, cfg)
    second = build_observable_events(real_trace, cfg)
    assert [e.event_id for e in first] == [e.event_id for e in second]
    assert [e.t_peak for e in first] == [e.t_peak for e in second]


def test_event_ids_are_unique(observable) -> None:
    ids = [e.event_id for e in observable]
    assert len(ids) == len(set(ids))


def test_a_vehicle_struck_twice_still_stops_once(cfg) -> None:
    """S06's chain: B is hit by A and hits C, and comes to rest once."""
    from cdf.oracle.events import load_oracle_trace

    run = (repo_root() / "artifacts_independent_clocks" / "S06_chain_collision"
           / "seed_000_a_front_pushed")
    if not run.is_dir():
        pytest.skip("the S06 reference run is not present")
    events = build_observable_events(
        load_oracle_trace(run), load_run_config(scenario_id="S06")
    )
    stops = [e for e in events if e.event_type is EventType.POST_IMPACT_STOP]
    per_vehicle: Dict[str, int] = {}
    for stop in stops:
        per_vehicle[stop.participant_id] = per_vehicle.get(stop.participant_id, 0) + 1
    assert all(n == 1 for n in per_vehicle.values()), per_vehicle


# ---------------------------------------------------------------------------
# Exact pairwise geometry
# ---------------------------------------------------------------------------


def test_the_privileged_pair_geometry_is_physically_consistent(real_trace) -> None:
    rows = pairwise_truth(real_trace, "A", "B")
    assert rows
    for row in rows[:200]:
        assert row["range_m"] >= 0.0
        # Range rate is the line-of-sight component of relative velocity, so it
        # can never exceed the magnitude of that velocity.
        speed = math.hypot(row["relative_vx"], row["relative_vy"])
        assert abs(row["range_rate_mps"]) <= speed + 1e-6
        if row["ttc_s"] is not None:
            assert row["ttc_s"] > 0.0, "a time to collision is only defined while closing"
        assert row["closing_rate_mps"] == pytest.approx(-row["range_rate_mps"])


def test_the_pair_geometry_is_symmetric_in_range(real_trace) -> None:
    ab = {round(r["t"], 4): r["range_m"] for r in pairwise_truth(real_trace, "A", "B")}
    ba = {round(r["t"], 4): r["range_m"] for r in pairwise_truth(real_trace, "B", "A")}
    shared = sorted(set(ab) & set(ba))
    assert shared
    for t in shared[:100]:
        assert ab[t] == pytest.approx(ba[t])


# ---------------------------------------------------------------------------
# The observable causal graph
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def observable_graph(observable, real_trace, cfg):
    return build_observable_causal_graph(
        observable, real_trace, cfg, run_id="R", scenario_id="S01", seed=0
    )


def test_no_rule_names_a_scenario_or_an_uncomparable_type() -> None:
    for rule in OBSERVABLE_RULES:
        for value in rule.cause_types + rule.effect_types:
            assert value in COMPARABLE_EVENT_TYPES, (rule.name, value)
        assert rule.edge_type.value in COMPARABLE_EDGE_TYPES
        lowered = rule.name.lower()
        for token in ("s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08",
                      "s09", "template", "scripted"):
            assert token not in lowered, rule.name


def test_a_rule_may_not_name_an_uncomparable_type() -> None:
    with pytest.raises(ValueError, match="comparable vocabulary"):
        ObservableRule(
            "bad", (EventType.ORACLE_SCRIPTED_INTERVENTION.value,),
            (EventType.COLLISION.value,), CausalEdgeType.TRIGGERS,
            "same_pair", 1.0, "",
        )


def test_the_reference_graph_recovers_the_mechanism(observable_graph) -> None:
    """S01: B brakes, B slows, the gap closes, TTC goes critical, they collide."""
    nodes = {n.event_id: n for n in observable_graph.nodes}
    pairs = {
        (nodes[e.source].event_type.value, nodes[e.target].event_type.value)
        for e in observable_graph.edges
    }
    assert ("BRAKE_ONSET", "DECELERATION") in pairs or (
        ("HARD_BRAKE", "HARD_DECELERATION") in pairs
    )
    assert any(src.endswith("DECELERATION") and tgt in
               ("RANGE_DECREASING", "RAPID_CLOSING") for src, tgt in pairs)
    assert any(tgt == "COLLISION" for _src, tgt in pairs)


def test_the_reference_graph_is_acyclic(observable_graph) -> None:
    import networkx as nx

    g = nx.DiGraph()
    g.add_nodes_from(n.event_id for n in observable_graph.nodes)
    g.add_edges_from((e.source, e.target) for e in observable_graph.edges)
    assert nx.is_directed_acyclic_graph(g)


def test_the_trace_refuses_some_edges_the_rules_proposed(observable_graph) -> None:
    """Verification has to be able to say no, or it is not verification."""
    assert observable_graph.meta["n_edges_refused_by_trace"] > 0
    for refusal in observable_graph.meta["refused"]:
        assert refusal["rule"] and refusal["reason"]


def test_every_verified_edge_carries_the_quantities_that_support_it(
    observable_graph
) -> None:
    verified = [e for e in observable_graph.edges if e.detail.get("verified")]
    assert verified, "at least some rules must be verified against the trace"
    for edge in verified:
        assert edge.detail["support"], edge.rule
        assert edge.detail["relation"]
        assert "lag_s" in edge.detail


def test_the_reference_graph_holds_only_comparable_nodes(observable_graph) -> None:
    assert all(is_comparable(n.event_type) for n in observable_graph.nodes)
    assert all(e.edge_type in COMPARABLE_EDGE_TYPES for e in observable_graph.edges)


def test_building_the_reference_is_deterministic(observable, real_trace, cfg) -> None:
    a = build_observable_causal_graph(observable, real_trace, cfg, scenario_id="S01")
    b = build_observable_causal_graph(observable, real_trace, cfg, scenario_id="S01")
    assert [(e.source, e.target, e.edge_type) for e in a.edges] == [
        (e.source, e.target, e.edge_type) for e in b.edges
    ]


def test_the_reference_is_richer_than_the_template_based_one(
    observable_graph
) -> None:
    """The point of the refactor, stated as a measurement.

    The old reference asserted a handful of template edges, most of them leaving
    a scripted-action node no reconstruction could match. This one asserts the
    physical structure, in a vocabulary a reconstruction shares.
    """
    from cdf.common.schemas import Provenance as P
    from cdf.graph.export import load_graph

    old_path = REAL_RUN / "oracle" / "oracle_causal_graph.json"
    if not old_path.is_file():
        pytest.skip("no legacy reference to compare against")
    old = load_graph(old_path, expect_scope=P.ORACLE)
    assert len(observable_graph.nodes) > len(old.nodes)
    assert len(observable_graph.edges) > len(old.edges)
    scripted = sum(
        1 for n in old.nodes
        if n.event_type is EventType.ORACLE_SCRIPTED_INTERVENTION
    )
    assert scripted > 0, "the legacy reference did contain scripted nodes"
