"""Scoring the explanation: what the causal metrics do and refuse to do.

The risk these tests guard against is a metric that flatters the method. A
vacuous 1.0 on an empty comparison, a chain score that is really an id-matching
score, a negative control whose silence is averaged in with a crash scenario's
success -- each would make the campaign look better than it is.
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
from cdf.evaluation.causal_metrics import (
    ATTRIBUTION_CLASS_ALIASES,
    evaluate_attribution_sets,
    evaluate_causal_paths,
    prf1,
)


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


def node(
    event_id: str,
    event_type: Any,
    participant: str,
    t: float,
    subject: Optional[str] = None,
    values: Optional[Dict[str, Any]] = None,
) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant,
        t_start=t, t_peak=t, t_end=t + 0.2,
        subject=subject,
        values=dict(values or {}),
        confidence=0.9,
        evidence=[],
        provenance=Provenance.FUSED,
        owners=[participant],
    )


def edge(source: str, target: str, edge_type: str) -> GraphEdge:
    return GraphEdge(
        source=source, target=target, edge_type=edge_type, confidence=0.8,
        provenance=Provenance.FUSED, rule="r", detail={},
    )


def graph(nodes: List[Event], edges: List[GraphEdge], scope=Provenance.FUSED) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=scope, owner=None, run_id="R", scenario_id="S01",
        seed=0, nodes=nodes, edges=edges, meta={},
    )


# ---------------------------------------------------------------------------
# prf1
# ---------------------------------------------------------------------------


def test_a_correct_silence_scores_one_but_is_flagged_as_vacuous() -> None:
    """Naming nobody when there is nobody to name is right, and must be visible."""
    score = prf1(set(), set())
    assert score["f1"] == 1.0
    assert score["vacuous"] is True


def test_naming_somebody_when_there_is_nobody_scores_zero() -> None:
    score = prf1(set(), {"A"})
    assert score["precision"] == 0.0 and score["f1"] == 0.0
    assert score["fp"] == 1 and score["vacuous"] is False


def test_partial_agreement_is_scored_element_wise() -> None:
    score = prf1({"A", "B"}, {"B", "C"})
    assert score["tp"] == 1 and score["fp"] == 1 and score["fn"] == 1
    assert score["precision"] == 0.5 and score["recall"] == 0.5 and score["f1"] == 0.5


def test_missing_everything_scores_zero_not_undefined() -> None:
    score = prf1({"A"}, set())
    assert score["recall"] == 0.0 and score["f1"] == 0.0 and score["vacuous"] is False


# ---------------------------------------------------------------------------
# Causal paths
# ---------------------------------------------------------------------------


def test_the_same_chain_told_in_two_vocabularies_matches(cfg) -> None:
    """The oracle's scripted action and the vehicle's recorded brake are one fact."""
    oracle = graph(
        [
            node("o_act", EventType.ORACLE_SCRIPTED_INTERVENTION, "B", 4.0,
                 values={"kind_is_brake": 1.0}),
            node("o_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("o_act", "o_hit", CausalEdgeType.CONTRIBUTES_TO.value)],
        scope=Provenance.ORACLE,
    )
    fused = graph(
        [
            node("f_brake", EventType.HARD_BRAKE, "B", 4.1),
            node("f_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("f_brake", "f_hit", CausalEdgeType.TRIGGERS.value)],
    )
    result = evaluate_causal_paths(fused, oracle, cfg)
    assert result["path"]["recall"] == 1.0, (
        "HARD_BRAKE--TRIGGERS-->COLLISION must match "
        "SCRIPTED_INTERVENTION(brake)--CONTRIBUTES_TO-->COLLISION"
    )
    assert result["path"]["tp"] == 1


def test_a_chain_through_the_wrong_behaviour_does_not_match(cfg) -> None:
    oracle = graph(
        [
            node("o_act", EventType.ORACLE_SCRIPTED_INTERVENTION, "B", 4.0,
                 values={"kind_is_brake": 1.0}),
            node("o_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("o_act", "o_hit", CausalEdgeType.CONTRIBUTES_TO.value)],
        scope=Provenance.ORACLE,
    )
    fused = graph(
        [
            node("f_lane", EventType.LANE_CHANGE_LIKE_MANEUVER, "B", 4.1),
            node("f_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("f_lane", "f_hit", CausalEdgeType.TRIGGERS.value)],
    )
    result = evaluate_causal_paths(fused, oracle, cfg)
    assert result["path"]["recall"] == 0.0
    assert "lateral_manoeuvre" in result["ancestry"]["extra_families"] or (
        result["ancestry"]["extra_families"]
    )


def test_node_ids_are_not_what_is_being_compared(cfg) -> None:
    """Renaming every node must not change the score."""
    import dataclasses

    oracle = graph(
        [
            node("o_brake", EventType.HARD_BRAKE, "B", 4.0),
            node("o_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("o_brake", "o_hit", CausalEdgeType.TRIGGERS.value)],
        scope=Provenance.ORACLE,
    )
    renamed_nodes = [
        dataclasses.replace(n, event_id="zzz_" + n.event_id) for n in oracle.nodes
    ]
    renamed = graph(
        renamed_nodes,
        [edge("zzz_o_brake", "zzz_o_hit", CausalEdgeType.TRIGGERS.value)],
    )
    result = evaluate_causal_paths(renamed, oracle, cfg)
    assert result["path"]["f1"] == 1.0


def test_an_empty_reconstruction_recalls_nothing(cfg) -> None:
    oracle = graph(
        [
            node("o_brake", EventType.HARD_BRAKE, "B", 4.0),
            node("o_hit", EventType.COLLISION, "A", 5.6, subject="B"),
        ],
        [edge("o_brake", "o_hit", CausalEdgeType.TRIGGERS.value)],
        scope=Provenance.ORACLE,
    )
    empty = graph([], [])
    result = evaluate_causal_paths(empty, oracle, cfg)
    assert result["path"]["recall"] == 0.0
    assert result["ancestry"]["recall"] == 0.0
    assert result["ancestry"]["missing_families"]


def test_no_oracle_graph_means_no_score_not_a_zero(cfg) -> None:
    result = evaluate_causal_paths(graph([], []), None, cfg)
    assert result["scored"] is False and result["reason"]


# ---------------------------------------------------------------------------
# Attribution sets
# ---------------------------------------------------------------------------


INITIATORS = {
    "action_ids": ["B_emergency_brake"],
    "participant_of_action": {"B_emergency_brake": "B"},
    "preventive_action_ids": ["A_late_brake"],
}

TWO = {
    "action_ids": ["B_brake", "C_brake"],
    "participant_of_action": {"B_brake": "B", "C_brake": "C"},
    "preventive_action_ids": [],
}


def attribution(actions: List[str], klass: str) -> Dict[str, Any]:
    return {
        "classification": {
            "attribution_class": klass,
            "necessary_actions": list(actions),
        }
    }


def test_the_named_contributor_is_compared_to_the_designed_one() -> None:
    result = evaluate_attribution_sets(
        attribution(["B_emergency_brake"], "single_initiator"), INITIATORS, True
    )
    assert result["truth_participants"] == ["B"]
    assert result["predicted_participants"] == ["B"]
    assert result["f1"] == 1.0 and result["exact_set_match"] is True
    assert result["class_correct"] is True


def test_naming_the_victim_instead_of_the_initiator_scores_zero() -> None:
    result = evaluate_attribution_sets(
        attribution(["A_late_brake"], "single_initiator"), INITIATORS, True
    )
    assert result["predicted_participants"] == []
    assert result["f1"] == 0.0 and result["exact_set_match"] is False


def test_either_multi_contributor_verdict_is_accepted() -> None:
    """The template says who contributed, never whether one alone sufficed."""
    for klass in ("shared_contribution", "joint_contribution"):
        result = evaluate_attribution_sets(
            attribution(["B_brake", "C_brake"], klass), TWO, True
        )
        assert result["exact_set_match"] is True, klass
        assert result["class_correct"] is True, klass
    wrong = evaluate_attribution_sets(
        attribution(["B_brake", "C_brake"], "single_initiator"), TWO, True
    )
    assert wrong["class_correct"] is False


def test_a_negative_control_is_scored_on_restraint_not_on_f1() -> None:
    silent = evaluate_attribution_sets(
        attribution([], "insufficient_evidence"), INITIATORS, False
    )
    assert silent["truth_participants"] == []
    assert silent["false_attribution"] is False
    assert silent["restraint_correct"] is True
    assert silent["vacuous"] is True, "a vacuous 1.0 must be flagged, not counted blind"

    invented = evaluate_attribution_sets(
        attribution(["B_emergency_brake"], "single_initiator"), INITIATORS, False
    )
    assert invented["false_attribution"] is True
    assert invented["restraint_correct"] is False
    assert invented["precision"] == 0.0


def test_a_minimal_prevention_set_is_read_as_the_named_contributors() -> None:
    payload = {
        "classification": {
            "attribution_class": "joint_contribution",
            "necessary_actions": [],
            "minimal_prevention_sets": [{"actions": ["B_brake", "C_brake"]}],
        }
    }
    result = evaluate_attribution_sets(payload, TWO, True)
    assert result["predicted_participants"] == ["B", "C"]
    assert result["predicted_source"] == "classification.minimal_prevention_sets"
    assert result["exact_set_match"] is True


def test_the_graph_only_hypothesis_is_scored_separately() -> None:
    """What reasoning alone achieved, before the simulator was re-run."""
    hypothesis = {
        "collisions": [
            {"outcome_id": "hit", "contributors": [{"participant_id": "B"}]}
        ]
    }
    result = evaluate_attribution_sets(None, INITIATORS, True, graph_hypothesis=hypothesis)
    assert result["scored"] is False, "no replay artifact was supplied"
    assert result["graph_only"]["f1"] == 1.0
    assert result["graph_only"]["exact_set_match"] is True


def test_no_attribution_artifact_is_recorded_as_unscored() -> None:
    result = evaluate_attribution_sets(None, INITIATORS, True)
    assert result["scored"] is False
    assert result["predicted_participants"] == []


def test_every_class_name_in_use_has_one_canonical_meaning() -> None:
    from cdf.causal.combinations import ATTRIBUTION_CLASSES

    assert set(ATTRIBUTION_CLASS_ALIASES.values()) <= set(ATTRIBUTION_CLASSES)
    for klass in ATTRIBUTION_CLASSES:
        assert ATTRIBUTION_CLASS_ALIASES.get(klass) == klass, (
            "a class must be its own alias so the table cannot silently rename it"
        )
