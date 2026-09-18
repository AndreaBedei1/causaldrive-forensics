"""Multi-action counterfactuals: what a *set* of removed actions establishes.

Removing one action at a time can only answer "was this one necessary?". The
question a two-vehicle incident actually poses is whether any single change would
have been enough at all, and these tests pin the five answers the vocabulary
allows -- including the two that decline to name anybody.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

import pytest

from cdf.causal.combinations import (
    ATTRIBUTION_CLASSES,
    SetOutcome,
    classify_from_set_outcomes,
    minimal_prevention_sets,
    plan_combinations,
)
from cdf.causal.interventions import InterventionSpec


def outcome(
    actions: Sequence[str],
    prevented: bool,
    severity_reduction: Optional[float] = None,
) -> SetOutcome:
    return SetOutcome(
        actions=frozenset(actions),
        prevented=prevented,
        severity_reduction=severity_reduction,
        intervention_id="__".join(sorted(actions)),
        collision=not prevented,
    )


def classify(outcomes: Sequence[SetOutcome], factual_collision: bool = True) -> str:
    return classify_from_set_outcomes(factual_collision, outcomes, None)[
        "attribution_class"
    ]


# ---------------------------------------------------------------------------
# The five verdicts
# ---------------------------------------------------------------------------


def test_one_removal_prevents_it_and_no_other_does() -> None:
    result = classify_from_set_outcomes(
        True, [outcome(["a"], True), outcome(["b"], False)], None
    )
    assert result["attribution_class"] == "single_initiator"
    assert result["sufficient_single_actions"] == ["a"]
    assert [s["actions"] for s in result["minimal_prevention_sets"]] == [["a"]]


def test_either_removal_would_have_been_enough() -> None:
    """Both sufficient alone: the contribution is shared, not joint."""
    result = classify_from_set_outcomes(
        True, [outcome(["a"], True), outcome(["b"], True)], None
    )
    assert result["attribution_class"] == "shared_contribution"
    assert result["sufficient_single_actions"] == ["a", "b"]
    assert [s["actions"] for s in result["minimal_prevention_sets"]] == [["a"], ["b"]]


def test_neither_removal_is_enough_but_both_together_are() -> None:
    """The case single-action replay cannot see, and the reason this module exists."""
    result = classify_from_set_outcomes(
        True,
        [outcome(["a"], False), outcome(["b"], False), outcome(["a", "b"], True)],
        None,
    )
    assert result["attribution_class"] == "joint_contribution"
    assert result["necessary_actions"] == []
    sets = result["minimal_prevention_sets"]
    assert [s["actions"] for s in sets] == [["a", "b"]]
    assert sets[0]["minimality"] == "minimal", (
        "both subsets were replayed and neither prevented it: minimal outright"
    )


def test_a_change_that_only_softened_the_impact_is_not_called_a_cause() -> None:
    result = classify_from_set_outcomes(
        True, [outcome(["a"], False, severity_reduction=0.4)], None
    )
    assert result["attribution_class"] == "contributing_but_not_necessary"
    assert result["contributing_actions"] == ["a"]
    assert result["necessary_actions"] == []
    assert result["minimal_prevention_sets"] == []


def test_nothing_that_was_tried_changed_anything() -> None:
    assert classify([outcome(["a"], False), outcome(["b"], False)]) == (
        "insufficient_evidence"
    )


def test_a_change_that_made_the_impact_worse_is_reported_as_mitigating() -> None:
    """Removing an action and getting a worse crash is the opposite of a cause.

    Folding this into "nothing changed" would discard a real finding: these are
    the behaviours that reduced an outcome they did not bring about, and a
    forensic report that cannot say so is missing half of what the replay
    established.
    """
    result = classify_from_set_outcomes(
        True,
        [outcome(["a"], False, severity_reduction=-0.7),
         outcome(["b"], False, severity_reduction=-0.7)],
        None,
    )
    assert result["attribution_class"] == "insufficient_evidence"
    assert result["mitigating_actions"] == ["a", "b"]
    assert result["contributing_actions"] == []
    assert result["necessary_actions"] == []
    assert "more severe" in result["rationale"]
    assert "did not cause" in result["rationale"]


def test_a_change_that_did_nothing_is_not_called_mitigating() -> None:
    result = classify_from_set_outcomes(
        True, [outcome(["a"], False, severity_reduction=0.0)], None
    )
    assert result["mitigating_actions"] == []
    assert "altered the outcome or its severity" in result["rationale"]


def test_every_verdict_carries_the_mitigating_field() -> None:
    """A consumer must be able to read it without checking which branch ran."""
    cases = [
        (True, [outcome(["a"], True)]),
        (True, [outcome(["a"], True), outcome(["b"], True)]),
        (True, [outcome(["a"], False), outcome(["b"], False), outcome(["a", "b"], True)]),
        (True, [outcome(["a"], False, 0.4)]),
        (True, [outcome(["a"], False, -0.4)]),
        (True, [outcome(["a"], False)]),
        (False, [outcome(["a"], False)]),
        (True, []),
    ]
    for factual, outcomes in cases:
        result = classify_from_set_outcomes(factual, outcomes, None)
        assert "mitigating_actions" in result, result["attribution_class"]
        assert isinstance(result["mitigating_actions"], list)


def test_a_marginal_severity_change_is_noise_not_a_contribution() -> None:
    """Below the configured threshold, a severity difference says nothing."""
    from cdf.common.config import load_run_config

    cfg = load_run_config(scenario_id="S01")
    outcomes = [outcome(["a"], False, severity_reduction=0.01)]
    assert classify_from_set_outcomes(True, outcomes, cfg)["attribution_class"] == (
        "insufficient_evidence"
    )
    generous = cfg.with_overrides(
        {"counterfactual": {"contribution": {"min_severity_reduction": 0.005}}}
    )
    assert classify_from_set_outcomes(True, outcomes, generous)[
        "attribution_class"
    ] == "contributing_but_not_necessary"


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------


def test_no_collision_means_there_is_nothing_to_attribute() -> None:
    result = classify_from_set_outcomes(False, [outcome(["a"], False)], None)
    assert result["attribution_class"] == "insufficient_evidence"
    assert "no collision" in result["rationale"]
    assert result["necessary_actions"] == []


def test_no_replays_means_no_verdict() -> None:
    result = classify_from_set_outcomes(True, [], None)
    assert result["attribution_class"] == "insufficient_evidence"
    assert result["n_replays"] == 0


def test_every_verdict_carries_the_disclaimer_and_a_declared_class() -> None:
    cases = [
        (True, [outcome(["a"], True)]),
        (True, [outcome(["a"], True), outcome(["b"], True)]),
        (True, [outcome(["a"], False), outcome(["b"], False), outcome(["a", "b"], True)]),
        (True, [outcome(["a"], False, 0.4)]),
        (True, [outcome(["a"], False)]),
        (False, [outcome(["a"], False)]),
        (True, []),
    ]
    for factual, outcomes in cases:
        result = classify_from_set_outcomes(factual, outcomes, None)
        assert result["attribution_class"] in ATTRIBUTION_CLASSES
        assert "NOT legal fault" in result["disclaimer"]
        assert "fault" not in result["rationale"].lower()
        assert "guilty" not in result["rationale"].lower()


# ---------------------------------------------------------------------------
# Minimality, honestly scoped
# ---------------------------------------------------------------------------


def test_a_superset_of_a_preventing_set_is_not_minimal() -> None:
    sets = minimal_prevention_sets(
        [outcome(["a"], True), outcome(["a", "b"], True), outcome(["b"], False)]
    )
    assert [s["actions"] for s in sets] == [["a"]]


def test_minimality_is_claimed_only_over_what_was_replayed() -> None:
    """An untested subset might have sufficed; the report must not pretend it didn't."""
    sets = minimal_prevention_sets([outcome(["a", "b"], True)])
    assert len(sets) == 1
    assert sets[0]["minimality"] == "minimal_within_tested"
    assert sets[0]["untested_subsets"] == [["a"], ["b"]]
    assert "may" in sets[0]["note"]


def test_prevention_sets_are_reported_smallest_first() -> None:
    sets = minimal_prevention_sets(
        [outcome(["c", "d"], True), outcome(["b"], True), outcome(["a"], True)]
    )
    assert [s["actions"] for s in sets] == [["a"], ["b"], ["c", "d"]]


# ---------------------------------------------------------------------------
# The bounded plan
# ---------------------------------------------------------------------------


def test_the_plan_is_deterministic_and_skips_what_was_tried() -> None:
    tested = [frozenset(["a"]), frozenset(["b"]), frozenset(["c"]), frozenset(["a", "b"])]
    plan = plan_combinations(["a", "b", "c"], tested, size=2, max_replays=10)
    assert [sorted(c) for c in plan] == [["a", "c"], ["b", "c"]]
    assert plan == plan_combinations(["c", "b", "a"], tested, 2, 10), (
        "candidate order must not change the plan"
    )


def test_the_plan_obeys_its_budget() -> None:
    candidates = ["a", "b", "c", "d", "e"]
    assert len(plan_combinations(candidates, [], size=2, max_replays=3)) == 3
    assert plan_combinations(candidates, [], size=1, max_replays=5) == []
    assert plan_combinations(["a"], [], size=2, max_replays=5) == []


# ---------------------------------------------------------------------------
# One replay that changes several actions
# ---------------------------------------------------------------------------


def test_a_joint_intervention_names_every_action_it_removes() -> None:
    iv = InterventionSpec(
        intervention_id="joint__a__b",
        action_id="a",
        op="disable",
        steps=[{"action_id": "b", "op": "disable"}, {"action_id": "a", "op": "disable"}],
    )
    assert iv.is_composite
    assert iv.action_ids == ("a", "b")
    runner = iv.as_runner_dict()
    assert runner["intervention_id"] == "joint__a__b"
    assert [s["action_id"] for s in runner["steps"]] == ["b", "a"]
    assert "op" not in runner, "a composite is described only by its steps"
    assert iv.to_dict()["composite"] is True


def test_a_single_action_intervention_is_unchanged() -> None:
    iv = InterventionSpec(intervention_id="no_brake", action_id="a", op="disable")
    assert not iv.is_composite
    assert iv.action_ids == ("a",)
    assert iv.as_runner_dict() == {
        "intervention_id": "no_brake", "action_id": "a", "op": "disable"
    }


def test_one_replay_may_not_change_the_same_action_twice() -> None:
    with pytest.raises(ValueError, match="same action twice"):
        InterventionSpec(
            intervention_id="bad", action_id="a", op="disable",
            steps=[{"action_id": "a", "op": "disable"},
                   {"action_id": "a", "op": "delay", "seconds": 1.0}],
        )


def test_a_step_is_validated_like_a_single_intervention() -> None:
    with pytest.raises(ValueError, match="unknown intervention op"):
        InterventionSpec(
            intervention_id="bad", action_id="a", op="disable",
            steps=[{"action_id": "a", "op": "teleport"}],
        )
    with pytest.raises(ValueError, match="names no action"):
        InterventionSpec(
            intervention_id="bad", action_id="a", op="disable",
            steps=[{"op": "disable"}],
        )
    with pytest.raises(ValueError, match="missing required"):
        InterventionSpec(
            intervention_id="bad", action_id="a", op="disable",
            steps=[{"action_id": "a", "op": "delay"}],
        )


def test_the_runner_applies_every_step_of_a_joint_replay() -> None:
    from cdf.common.config import load_run_config
    from cdf.simulation.runner import _apply_intervention
    from cdf.simulation.scenario_base import ScenarioSpec

    spec = ScenarioSpec.from_config(load_run_config(scenario_id="S06"))
    ids = [a.action_id for p in spec.participants for a in p.actions]
    assert len(ids) >= 2, "S06 must script at least two actions for this test"
    iv = InterventionSpec(
        intervention_id="joint__" + "__".join(sorted(ids[:2])),
        action_id=sorted(ids[:2])[0],
        op="disable",
        steps=[{"action_id": a, "op": "disable"} for a in sorted(ids[:2])],
    )
    out = _apply_intervention(spec, iv.as_runner_dict())
    state = {a.action_id: a.enabled for p in out.participants for a in p.actions}
    assert set(state) == set(ids), "a replay may not add or drop an action"
    for action_id in sorted(ids[:2]):
        assert state[action_id] is False, "both targeted actions must be disabled"
    for action_id in ids[2:]:
        assert state[action_id] is True, "nothing else may be touched"
    assert iv.intervention_id in out.variant
    assert all(
        a.enabled for p in spec.participants for a in p.actions
    ), "the scenario the replay was derived from must be left untouched"
