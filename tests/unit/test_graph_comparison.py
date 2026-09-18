"""The comparison that produces the project's primary number.

Everything here is about what must and must not count as a match. A metric that
matched on ids would measure the id scheme; one that ignored participants would
credit a reconstruction for putting the right event on the wrong vehicle; one
that ignored direction would credit it for drawing the cause backwards. Each of
those is a way to look good while being wrong, and each has a test.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pytest

from cdf.common.config import load_run_config
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.evaluation.graph_comparison import compare_graphs, normalise_outcome_pairs


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


def node(
    event_id: str,
    event_type: EventType,
    participant: str,
    t: float,
    subject: Optional[str] = None,
    scope: Provenance = Provenance.FUSED,
) -> Event:
    return Event(
        event_id=event_id, event_type=event_type, participant_id=participant,
        t_start=t, t_peak=t, t_end=t + 0.2, subject=subject, values={},
        confidence=0.9, evidence=[], provenance=scope, owners=[participant],
    )


def edge(
    source: str, target: str,
    edge_type: CausalEdgeType = CausalEdgeType.TRIGGERS,
    scope: Provenance = Provenance.FUSED,
) -> GraphEdge:
    return GraphEdge(
        source=source, target=target, edge_type=edge_type.value, confidence=0.8,
        provenance=scope, rule="r", detail={},
    )


def graph(nodes, edges, scope=Provenance.FUSED) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=scope, owner=None, run_id="R",
        scenario_id="S01", seed=0, nodes=nodes, edges=edges, meta={},
    )


def reference(nodes, edges) -> GraphDocument:
    return graph(
        [n for n in nodes], [e for e in edges], scope=Provenance.ORACLE
    )


# ---------------------------------------------------------------------------
# Node matching
# ---------------------------------------------------------------------------


def test_the_same_physical_event_matches_under_different_ids(cfg) -> None:
    """Two layers name the same fact differently; that is not a disagreement."""
    inferred = graph([node("fused:xyz", EventType.BRAKE_ONSET, "B", 4.00)], [])
    gt = reference([node("oracle_obs:abc", EventType.BRAKE_ONSET, "B", 4.05)], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["n_matched"] == 1
    assert result["nodes"]["f1"] == 1.0
    row = result["node_rows"][0]
    assert row["status"] == "matched"
    assert row["reference_id"] != row["inferred_id"]
    assert row["abs_timing_error_s"] == pytest.approx(0.05)


def test_an_event_outside_the_tolerance_does_not_match(cfg) -> None:
    tolerance = float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5))
    inferred = graph([node("a", EventType.BRAKE_ONSET, "B", 4.0)], [])
    gt = reference([node("b", EventType.BRAKE_ONSET, "B", 4.0 + tolerance + 0.5)], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["n_matched"] == 0
    assert {r["status"] for r in result["node_rows"]} == {"missing", "extra"}


def test_the_right_event_on_the_wrong_vehicle_does_not_match(cfg) -> None:
    """Otherwise a reconstruction is credited for blaming the wrong car."""
    inferred = graph([node("a", EventType.BRAKE_ONSET, "A", 4.0)], [])
    gt = reference([node("b", EventType.BRAKE_ONSET, "B", 4.0)], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["n_matched"] == 0


def test_the_right_relation_about_the_wrong_pair_does_not_match(cfg) -> None:
    inferred = graph([node("a", EventType.CRITICAL_TTC, "A", 5.0, subject="C")], [])
    gt = reference([node("b", EventType.CRITICAL_TTC, "A", 5.0, subject="B")], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["n_matched"] == 0


def test_a_different_event_type_never_matches(cfg) -> None:
    inferred = graph([node("a", EventType.ACCELERATION, "B", 4.0)], [])
    gt = reference([node("b", EventType.DECELERATION, "B", 4.0)], [])
    assert compare_graphs(inferred, gt, cfg)["nodes"]["n_matched"] == 0


def test_a_collision_matches_whichever_vehicle_it_was_filed_under(cfg) -> None:
    """A collision is one physical event and an unordered pair of vehicles."""
    inferred = graph([node("a", EventType.COLLISION, "B", 6.0, subject="A")], [])
    gt = reference([node("b", EventType.COLLISION, "A", 6.0, subject="B")], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["n_matched"] == 1, (
        "COLLISION(A,B) and COLLISION(B,A) are the same crash"
    )


def test_normalising_an_outcome_pair_leaves_one_sided_events_alone() -> None:
    doc = graph([
        node("stop", EventType.POST_IMPACT_STOP, "B", 7.0, subject="A"),
        node("brake", EventType.BRAKE_ONSET, "B", 4.0),
    ], [])
    out = normalise_outcome_pairs(doc)
    stop = next(n for n in out.nodes if n.event_id == "stop")
    assert stop.participant_id == "B", (
        "a post-impact stop is about one vehicle coming to rest"
    )


# ---------------------------------------------------------------------------
# Vocabulary restriction
# ---------------------------------------------------------------------------


def test_a_sensor_event_is_set_aside_rather_than_scored(cfg) -> None:
    """A radar track has no privileged counterpart; counting it is unfair."""
    inferred = graph([
        node("track", EventType.RADAR_TRACK_APPEARED, "A", 1.0, subject="B"),
        node("brake", EventType.BRAKE_ONSET, "B", 4.0),
    ], [])
    gt = reference([node("b", EventType.BRAKE_ONSET, "B", 4.0)], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["precision"] == 1.0, (
        "the radar event must not be counted as a false positive"
    )
    ontology = result["ontology"]["inferred"]
    assert ontology["n_nodes_dropped"] == 1
    assert "RADAR_TRACK_APPEARED" in ontology["dropped_node_types"]


def test_a_reference_node_no_reconstruction_could_emit_is_set_aside(cfg) -> None:
    """The failure the whole refactor exists to remove."""
    inferred = graph([node("a", EventType.BRAKE_ONSET, "B", 4.0)], [])
    gt = reference([
        node("b", EventType.BRAKE_ONSET, "B", 4.0),
        node("scripted", EventType.ORACLE_SCRIPTED_INTERVENTION, "B", 4.0),
    ], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["nodes"]["recall"] == 1.0, (
        "recall must not be capped by a node type no reconstruction can emit"
    )
    assert result["ontology"]["reference"]["n_nodes_dropped"] == 1


# ---------------------------------------------------------------------------
# Edge matching
# ---------------------------------------------------------------------------


def _chain(prefix: str, scope: Provenance):
    nodes = [
        node(prefix + "brake", EventType.BRAKE_ONSET, "B", 4.0, scope=scope),
        node(prefix + "decel", EventType.HARD_DECELERATION, "B", 4.3, scope=scope),
    ]
    return nodes


def test_an_edge_matches_through_the_node_correspondence(cfg) -> None:
    inferred = graph(
        _chain("i_", Provenance.FUSED),
        [edge("i_brake", "i_decel", CausalEdgeType.CONTRIBUTES_TO)],
    )
    gt = reference(
        _chain("o_", Provenance.ORACLE),
        [edge("o_brake", "o_decel", CausalEdgeType.CONTRIBUTES_TO,
              scope=Provenance.ORACLE)],
    )
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["n_matched"] == 1
    assert result["edges"]["f1"] == 1.0
    row = next(r for r in result["edge_rows"] if r["status"] == "true_positive")
    assert row["source_type"] == "BRAKE_ONSET"
    assert row["target_type"] == "HARD_DECELERATION"


def test_an_edge_drawn_backwards_is_not_a_match(cfg) -> None:
    """Getting the direction wrong is getting the causation wrong."""
    inferred = graph(
        _chain("i_", Provenance.FUSED),
        [edge("i_decel", "i_brake", CausalEdgeType.CONTRIBUTES_TO)],
    )
    gt = reference(
        _chain("o_", Provenance.ORACLE),
        [edge("o_brake", "o_decel", CausalEdgeType.CONTRIBUTES_TO,
              scope=Provenance.ORACLE)],
    )
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["n_matched"] == 0
    assert result["edges"]["n_reversed"] >= 1
    assert any(r["status"] == "wrong_direction" for r in result["edge_rows"])


def test_the_wrong_relation_between_the_right_events_is_not_a_match(cfg) -> None:
    inferred = graph(
        _chain("i_", Provenance.FUSED),
        [edge("i_brake", "i_decel", CausalEdgeType.PREVENTS)],
    )
    gt = reference(
        _chain("o_", Provenance.ORACLE),
        [edge("o_brake", "o_decel", CausalEdgeType.CONTRIBUTES_TO,
              scope=Provenance.ORACLE)],
    )
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["n_matched"] == 0


def test_an_invented_edge_lowers_precision(cfg) -> None:
    nodes = _chain("i_", Provenance.FUSED) + [
        node("i_extra", EventType.ACCELERATION, "B", 2.0)
    ]
    inferred = graph(nodes, [
        edge("i_brake", "i_decel", CausalEdgeType.CONTRIBUTES_TO),
        edge("i_extra", "i_decel", CausalEdgeType.CONTRIBUTES_TO),
    ])
    gt = reference(
        _chain("o_", Provenance.ORACLE) + [
            node("o_extra", EventType.ACCELERATION, "B", 2.0,
                 scope=Provenance.ORACLE)
        ],
        [edge("o_brake", "o_decel", CausalEdgeType.CONTRIBUTES_TO,
              scope=Provenance.ORACLE)],
    )
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["n_matched"] == 1
    assert result["edges"]["precision"] == pytest.approx(0.5)
    assert result["edges"]["recall"] == 1.0
    assert result["edges"]["n_extra"] == 1


def test_a_missed_edge_lowers_recall(cfg) -> None:
    inferred = graph(_chain("i_", Provenance.FUSED), [])
    gt = reference(
        _chain("o_", Provenance.ORACLE),
        [edge("o_brake", "o_decel", CausalEdgeType.CONTRIBUTES_TO,
              scope=Provenance.ORACLE)],
    )
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["recall"] == 0.0
    assert result["edges"]["n_missing"] == 1
    assert any(r["status"] == "missing_edge" for r in result["edge_rows"])


def test_an_edge_whose_endpoint_never_matched_is_not_a_true_positive(cfg) -> None:
    """An edge between events the reference does not have cannot be correct."""
    inferred = graph(
        [
            node("i_brake", EventType.BRAKE_ONSET, "B", 4.0),
            node("i_ghost", EventType.LANE_CHANGE_LIKE_MANEUVER, "B", 4.2),
        ],
        [edge("i_ghost", "i_brake", CausalEdgeType.TRIGGERS)],
    )
    gt = reference([node("o_brake", EventType.BRAKE_ONSET, "B", 4.0,
                         scope=Provenance.ORACLE)], [])
    result = compare_graphs(inferred, gt, cfg)
    assert result["edges"]["n_matched"] == 0


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def test_every_reference_and_inferred_node_appears_in_exactly_one_row(cfg) -> None:
    inferred = graph([
        node("i_a", EventType.BRAKE_ONSET, "B", 4.0),
        node("i_b", EventType.ACCELERATION, "A", 2.0),
    ], [])
    gt = reference([
        node("o_a", EventType.BRAKE_ONSET, "B", 4.0, scope=Provenance.ORACLE),
        node("o_c", EventType.THROTTLE_ONSET, "A", 1.0, scope=Provenance.ORACLE),
    ], [])
    result = compare_graphs(inferred, gt, cfg)
    statuses = [r["status"] for r in result["node_rows"]]
    assert statuses.count("matched") == 1
    assert statuses.count("missing") == 1
    assert statuses.count("extra") == 1
    for row in result["node_rows"]:
        assert row["event_type"] and row["participant"]


def test_no_reference_means_no_score_rather_than_a_zero(cfg) -> None:
    result = compare_graphs(graph([], []), None, cfg)
    assert result["scored"] is False
    assert result["reason"]


def test_an_empty_reconstruction_scores_zero_and_lists_what_it_missed(cfg) -> None:
    gt = reference([
        node("o_a", EventType.BRAKE_ONSET, "B", 4.0, scope=Provenance.ORACLE)
    ], [])
    result = compare_graphs(graph([], []), gt, cfg)
    assert result["scored"] is True
    assert result["nodes"]["recall"] == 0.0
    assert [r["status"] for r in result["node_rows"]] == ["missing"]
