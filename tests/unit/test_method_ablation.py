"""The ablation must be able to report that the method did not help.

An ablation that can only show improvement is decoration. These tests fix the
arithmetic, the direction of the deltas, and the reachability ceiling that makes
the strict numbers readable -- including the case where the added stage makes a
score worse, which must come through as a negative number and not be clamped,
hidden, or relabelled.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.evaluation.method_ablation import (
    ARMS,
    INFERENCE_KEY,
    _best_local,
    _deltas,
    _scores,
    reference_reachability,
)


def node(event_id: str, event_type: Any, participant: str, t: float) -> Event:
    return Event(
        event_id=event_id, event_type=event_type, participant_id=participant,
        t_start=t, t_peak=t, t_end=t + 0.2, subject=None, values={},
        confidence=0.9, evidence=[], provenance=Provenance.ORACLE, owners=[participant],
    )


def oracle_graph(nodes, edges) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=Provenance.ORACLE, owner=None, run_id="R",
        scenario_id="S01", seed=0, nodes=nodes, edges=edges, meta={},
    )


def edge(source: str, target: str) -> GraphEdge:
    return GraphEdge(
        source=source, target=target, edge_type=CausalEdgeType.CONTRIBUTES_TO.value,
        confidence=0.9, provenance=Provenance.ORACLE, rule="template", detail={},
    )


# ---------------------------------------------------------------------------
# The arms
# ---------------------------------------------------------------------------


def test_the_arms_are_ordered_by_how_much_reasoning_they_apply() -> None:
    assert ARMS == ("best_local", "simple_fusion", "fusion_global_reasoning")
    assert INFERENCE_KEY == "fusion.post_fusion.enabled", (
        "the last two arms must differ in exactly one documented key"
    )


def test_the_baseline_is_the_strongest_viewpoint_not_the_average() -> None:
    per = {
        "A": {"edge_f1": 0.10, "node_f1": 0.90},
        "B": {"edge_f1": 0.40, "node_f1": 0.10},
        "C": {"edge_f1": 0.40, "node_f1": 0.50},
    }
    assert _best_local({"per_participant": per}) == "C"


def test_the_baseline_choice_is_reproducible_on_a_tie() -> None:
    per = {
        "B": {"edge_f1": 0.5, "node_f1": 0.5},
        "A": {"edge_f1": 0.5, "node_f1": 0.5},
    }
    assert _best_local({"per_participant": per}) == "A"
    assert _best_local({"per_participant": dict(reversed(list(per.items())))}) == "A"


def test_a_participant_that_was_not_scored_does_not_win() -> None:
    per = {"A": {"edge_f1": None, "node_f1": None}, "B": {"edge_f1": 0.0, "node_f1": 0.0}}
    assert _best_local({"per_participant": per}) == "B"


def test_no_local_graph_means_no_baseline_rather_than_a_zero() -> None:
    assert _best_local({"per_participant": {}}) is None


def test_the_metric_block_is_read_in_the_shape_the_metric_module_writes() -> None:
    block = {
        "node_precision": 0.5, "node_recall": 0.4, "node_f1": 0.44,
        "n_nodes_matched": 2, "n_nodes_truth": 5, "n_nodes_pred": 4,
        "edge_precision": 0.25, "edge_recall": 0.2, "edge_f1": 0.22,
        "n_edges_matched": 1, "n_edges_truth": 5, "n_edges_pred": 4,
        "structural_hamming_distance": 7,
    }
    scores = _scores(block)
    assert scores["nodes"]["f1"] == 0.44 and scores["nodes"]["n_matched"] == 2
    assert scores["edges"]["recall"] == 0.2 and scores["edges"]["shd"] == 7
    assert _scores(None) == {"nodes": None, "edges": None}


# ---------------------------------------------------------------------------
# Deltas
# ---------------------------------------------------------------------------


def arm(node_f1: float, edge_f1: float, edge_recall: float = 0.0) -> Dict[str, Any]:
    block = {
        "nodes": {"precision": 0.0, "recall": 0.0, "f1": node_f1},
        "edges": {"precision": 0.0, "recall": edge_recall, "f1": edge_f1},
    }
    return {"strict": block, "canonical": block}


def test_an_improvement_is_a_positive_delta() -> None:
    deltas = _deltas({
        "best_local": arm(0.3, 0.1),
        "simple_fusion": arm(0.4, 0.2),
        "fusion_global_reasoning": arm(0.4, 0.35),
    })
    assert deltas["fusion_over_best_local"]["strict_edges_f1"] == pytest.approx(0.1)
    assert deltas["reasoning_over_simple_fusion"]["strict_edges_f1"] == pytest.approx(0.15)
    assert deltas["reasoning_over_best_local"]["strict_edges_f1"] == pytest.approx(0.25)


def test_a_regression_is_reported_as_a_negative_number_not_hidden() -> None:
    """The stage that made a score worse must say so."""
    deltas = _deltas({
        "best_local": arm(0.3, 0.30),
        "simple_fusion": arm(0.3, 0.20),
        "fusion_global_reasoning": arm(0.3, 0.05),
    })
    assert deltas["fusion_over_best_local"]["strict_edges_f1"] == pytest.approx(-0.10)
    assert deltas["reasoning_over_simple_fusion"]["strict_edges_f1"] == pytest.approx(-0.15)
    assert deltas["reasoning_over_best_local"]["strict_edges_f1"] == pytest.approx(-0.25)


def test_a_missing_arm_yields_no_delta_rather_than_a_zero() -> None:
    deltas = _deltas({"simple_fusion": arm(0.4, 0.2)})
    assert deltas["fusion_over_best_local"]["strict_edges_f1"] is None
    assert deltas["reasoning_over_simple_fusion"]["strict_edges_f1"] is None


def test_both_vocabularies_are_reported_for_every_step() -> None:
    deltas = _deltas({
        "best_local": arm(0.3, 0.1, edge_recall=0.2),
        "simple_fusion": arm(0.4, 0.2, edge_recall=0.5),
        "fusion_global_reasoning": arm(0.4, 0.2, edge_recall=0.9),
    })
    for step in deltas.values():
        for vocabulary in ("strict", "canonical"):
            for measure in ("nodes", "edges"):
                for metric in ("precision", "recall", "f1"):
                    assert "{0}_{1}_{2}".format(vocabulary, measure, metric) in step
    assert deltas["reasoning_over_simple_fusion"]["canonical_edges_recall"] == (
        pytest.approx(0.4)
    )


# ---------------------------------------------------------------------------
# The ceiling
# ---------------------------------------------------------------------------


def test_an_edge_from_a_scripted_action_is_counted_as_strictly_unreachable() -> None:
    """No reconstruction has a node of that type to put at the tail."""
    doc = oracle_graph(
        [
            node("act", EventType.ORACLE_SCRIPTED_INTERVENTION, "B", 4.0),
            node("decel", EventType.HARD_DECELERATION, "B", 4.2),
            node("hit", EventType.COLLISION, "A", 5.6),
        ],
        [edge("act", "decel"), edge("decel", "hit")],
    )
    result = reference_reachability(doc)
    assert result["n_reference_edges"] == 2
    assert result["n_edges_touching_a_scripted_action"] == 1
    assert result["fraction_unreachable_strictly"] == 0.5
    assert result["strict_edge_recall_ceiling"] == 0.5


def test_a_reference_of_ordinary_events_has_no_ceiling_below_one() -> None:
    doc = oracle_graph(
        [
            node("brake", EventType.HARD_BRAKE, "B", 4.0),
            node("hit", EventType.COLLISION, "A", 5.6),
        ],
        [edge("brake", "hit")],
    )
    assert reference_reachability(doc)["strict_edge_recall_ceiling"] == 1.0


def test_an_empty_reference_reports_no_ceiling_rather_than_one() -> None:
    result = reference_reachability(oracle_graph([], []))
    assert result["n_reference_edges"] == 0
    assert result["strict_edge_recall_ceiling"] is None
    assert result["fraction_unreachable_strictly"] is None
