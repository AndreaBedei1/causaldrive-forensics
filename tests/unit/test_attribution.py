"""Unit tests for cdf.causal.attribution.

Attribution is the part of the pipeline most likely to be quoted out of context,
so these tests pin down the two things that must never drift: the but-for test is
about prevention and nothing else, and a shared or unexplained outcome is
reported as such instead of being resolved into a culprit.

Outcomes are constructed directly -- no simulator, no artifacts -- so every
expected verdict is derivable from the numbers written in the test itself.
"""

from __future__ import annotations

from typing import List, Optional

import pytest

from cdf.causal.attribution import (
    ATTRIBUTION_CLASSES,
    CausalContribution,
    attribution_report,
    but_for,
    classify_attribution,
    contribution_of,
    contribution_score,
    severity_reduction,
)
from cdf.causal.counterfactuals import FACTUAL_ID, CounterfactualOutcome
from cdf.causal.interventions import InterventionSpec
from cdf.common.config import Config, load_run_config


@pytest.fixture(scope="module")
def cfg() -> Config:
    return load_run_config(scenario_id="S01")


def outcome(
    intervention_id: str = "iv",
    action_id: str = "B_emergency_brake",
    op: str = "disable",
    participant: str = "B",
    collision: bool = True,
    relative_impact_speed: Optional[float] = 8.0,
    impact_speed: Optional[float] = 8.0,
    min_distance: float = 0.5,
    near_miss: bool = False,
) -> CounterfactualOutcome:
    """A complete outcome record with the fields attribution actually reads."""
    return CounterfactualOutcome(
        intervention_id=intervention_id,
        action_id=action_id,
        op=op,
        targets_participant=participant,
        collision=collision,
        collision_pairs=[["A", "B"]] if collision else [],
        t_collision=6.55 if collision else None,
        impact_speed=impact_speed if collision else None,
        relative_impact_speed=relative_impact_speed if collision else None,
        min_ttc=0.6,
        min_distance=min_distance,
        near_miss=near_miss,
        validation_passed=collision,
    )


def factual_crash() -> CounterfactualOutcome:
    return outcome(intervention_id=FACTUAL_ID, action_id="", op="none", participant="")


# ---------------------------------------------------------------------------
# but_for
# ---------------------------------------------------------------------------


def test_but_for_is_one_when_the_replay_prevented_the_crash() -> None:
    assert but_for(factual_crash(), outcome(collision=False)) == 1


def test_but_for_is_zero_when_both_runs_collided() -> None:
    assert but_for(factual_crash(), outcome(collision=True)) == 0


def test_but_for_is_zero_when_neither_run_collided() -> None:
    """Nothing to be but-for: the factual run has no collision to prevent."""
    clean = outcome(intervention_id=FACTUAL_ID, action_id="", op="none", collision=False)
    assert but_for(clean, outcome(collision=False)) == 0


def test_but_for_rejects_a_non_outcome_argument() -> None:
    with pytest.raises(TypeError):
        but_for(factual_crash(), {"collision": False})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# severity_reduction
# ---------------------------------------------------------------------------


def test_severity_reduction_is_positive_when_the_impact_was_softer(cfg: Config) -> None:
    reduction = severity_reduction(
        factual_crash(), outcome(relative_impact_speed=2.0), cfg
    )
    assert reduction == pytest.approx(0.75)


def test_severity_reduction_is_negative_when_the_replay_was_worse(cfg: Config) -> None:
    reduction = severity_reduction(
        factual_crash(), outcome(relative_impact_speed=12.0), cfg
    )
    assert reduction == pytest.approx(-0.5)


def test_severity_reduction_is_none_when_either_side_is_undefined(cfg: Config) -> None:
    unmeasured = outcome(relative_impact_speed=None)
    assert severity_reduction(factual_crash(), unmeasured, cfg) is None

    factual_unmeasured = outcome(
        intervention_id=FACTUAL_ID, action_id="", op="none", relative_impact_speed=None
    )
    assert severity_reduction(factual_unmeasured, outcome(), cfg) is None

    # A prevented collision has no impact speed at all, so the ratio is undefined
    # rather than 1.0; contribution_score is where prevention is credited.
    assert severity_reduction(factual_crash(), outcome(collision=False), cfg) is None


def test_severity_reduction_honours_the_configured_metric(cfg: Config) -> None:
    by_absolute = cfg.with_overrides({"counterfactual": {"severity_metric": "impact_speed"}})
    softer = outcome(relative_impact_speed=8.0, impact_speed=4.0)
    assert severity_reduction(factual_crash(), softer, by_absolute) == pytest.approx(0.5)
    assert severity_reduction(factual_crash(), softer, cfg) == pytest.approx(0.0)


def test_severity_reduction_rejects_an_unknown_metric(cfg: Config) -> None:
    broken = cfg.with_overrides({"counterfactual": {"severity_metric": "vibes"}})
    with pytest.raises(ValueError):
        severity_reduction(factual_crash(), outcome(), broken)


# ---------------------------------------------------------------------------
# contribution_score
# ---------------------------------------------------------------------------


def test_contribution_score_is_bounded_and_monotone(cfg: Config) -> None:
    factual = factual_crash()
    unchanged = contribution_score(factual, outcome(relative_impact_speed=8.0), cfg)
    softer = contribution_score(factual, outcome(relative_impact_speed=4.0), cfg)
    much_softer = contribution_score(factual, outcome(relative_impact_speed=1.0), cfg)
    prevented = contribution_score(factual, outcome(collision=False), cfg)

    for score in (unchanged, softer, much_softer, prevented):
        assert 0.0 <= score <= 1.0

    assert unchanged == pytest.approx(0.0)
    assert unchanged < softer < much_softer < prevented
    assert prevented == pytest.approx(1.0)


def test_contribution_score_matches_the_documented_formula(cfg: Config) -> None:
    """(w_p * but_for + w_s * clamp(reduction)) / (w_p + w_s), weights from config."""
    prevention_weight = float(cfg.get("counterfactual.contribution.prevention_weight"))
    severity_weight = float(cfg.get("counterfactual.contribution.severity_weight"))
    cf = outcome(relative_impact_speed=2.0)

    expected = (prevention_weight * 0 + severity_weight * 0.75) / (
        prevention_weight + severity_weight
    )
    assert contribution_score(factual_crash(), cf, cfg) == pytest.approx(expected)


def test_contribution_score_ignores_a_worse_replay(cfg: Config) -> None:
    """A replay that made things worse scores zero, never a negative credit."""
    assert contribution_score(
        factual_crash(), outcome(relative_impact_speed=20.0), cfg
    ) == pytest.approx(0.0)


def test_contribution_score_rejects_degenerate_weights(cfg: Config) -> None:
    broken = cfg.with_overrides(
        {"counterfactual": {"contribution": {"prevention_weight": 0.0, "severity_weight": 0.0}}}
    )
    with pytest.raises(ValueError):
        contribution_score(factual_crash(), outcome(), broken)


# ---------------------------------------------------------------------------
# classify_attribution
# ---------------------------------------------------------------------------


def contributions(
    cfg: Config, cfs: List[CounterfactualOutcome]
) -> List[CausalContribution]:
    factual = factual_crash()
    return [contribution_of(factual, cf, cfg) for cf in cfs]


def test_classify_single_initiator(cfg: Config) -> None:
    results = contributions(
        cfg,
        [
            outcome("b_disable", "B_emergency_brake", "disable", "B", collision=False),
            outcome("a_disable", "A_late_brake", "disable", "A", collision=True),
        ],
    )
    verdict = classify_attribution(results, cfg)

    assert verdict["attribution_class"] == "single_initiator"
    assert verdict["necessary_actions"] == ["B_emergency_brake"]
    assert verdict["primary_initiator"] == "B_emergency_brake"
    assert verdict["scores"]["B_emergency_brake"] == pytest.approx(1.0)
    assert verdict["scores"]["A_late_brake"] == pytest.approx(0.0)
    assert "legal fault" in verdict["disclaimer"]


def test_classify_shared_contribution_is_the_s05_shape(cfg: Config) -> None:
    """S05: intervening on either participant prevents the crash, so neither
    action is necessary on its own and no primary initiator may be named."""
    results = contributions(
        cfg,
        [
            outcome("a_no_yield", "A_no_yield", "disable", "A", collision=False),
            outcome("b_no_yield", "B_no_yield", "disable", "B", collision=False),
        ],
    )
    verdict = classify_attribution(results, cfg)

    assert verdict["attribution_class"] == "shared_contribution"
    assert verdict["necessary_actions"] == ["A_no_yield", "B_no_yield"]
    assert verdict["primary_initiator"] is None


def test_classify_insufficient_evidence_when_nothing_prevented_the_crash(
    cfg: Config,
) -> None:
    results = contributions(
        cfg,
        [
            outcome("a", "A_late_brake", "disable", "A", collision=True),
            outcome("b", "B_emergency_brake", "disable", "B", collision=True),
        ],
    )
    verdict = classify_attribution(results, cfg)

    assert verdict["attribution_class"] == "insufficient_evidence"
    assert verdict["necessary_actions"] == []
    assert verdict["primary_initiator"] is None


def test_classify_insufficient_evidence_on_an_empty_result_set(cfg: Config) -> None:
    verdict = classify_attribution([], cfg)
    assert verdict["attribution_class"] == "insufficient_evidence"
    assert verdict["primary_initiator"] is None
    assert verdict["scores"] == {}
    assert verdict["n_replays"] == 0


def test_classify_aggregates_the_replays_of_one_action(cfg: Config) -> None:
    """Disabling and weakening the same action test one hypothesis, not two."""
    results = contributions(
        cfg,
        [
            outcome("b_disable", "B_emergency_brake", "disable", "B", collision=False),
            outcome(
                "b_scale",
                "B_emergency_brake",
                "scale",
                "B",
                collision=True,
                relative_impact_speed=4.0,
            ),
        ],
    )
    verdict = classify_attribution(results, cfg)

    assert verdict["attribution_class"] == "single_initiator"
    assert verdict["necessary_actions"] == ["B_emergency_brake"]
    assert verdict["scores"]["B_emergency_brake"] == pytest.approx(1.0)
    assert verdict["n_replays"] == 2


def test_classify_lists_severity_only_actions_as_contributing(cfg: Config) -> None:
    results = contributions(
        cfg,
        [
            outcome("b", "B_emergency_brake", "disable", "B", collision=False),
            outcome(
                "a",
                "A_late_brake",
                "advance",
                "A",
                collision=True,
                relative_impact_speed=4.0,
            ),
        ],
    )
    verdict = classify_attribution(results, cfg)
    assert verdict["necessary_actions"] == ["B_emergency_brake"]
    assert verdict["contributing_actions"] == ["A_late_brake"]


def test_classify_every_class_is_declared(cfg: Config) -> None:
    results = contributions(cfg, [outcome(collision=False)])
    assert classify_attribution(results, cfg)["attribution_class"] in ATTRIBUTION_CLASSES


def test_classify_rejects_raw_outcomes(cfg: Config) -> None:
    with pytest.raises(TypeError) as excinfo:
        classify_attribution([outcome()], cfg)  # type: ignore[list-item]
    assert "contribution_of" in str(excinfo.value)


# ---------------------------------------------------------------------------
# contribution_of / attribution_report
# ---------------------------------------------------------------------------


def test_contribution_of_keeps_the_raw_outcome(cfg: Config) -> None:
    cf = outcome(collision=False, near_miss=True)
    contribution = contribution_of(factual_crash(), cf, cfg)

    assert contribution.but_for == 1
    assert contribution.prevented_collision is True
    assert contribution.outcome is cf
    assert contribution.to_dict()["outcome"]["collision"] is False
    assert any("near miss" in note for note in contribution.notes)


def test_attribution_report_carries_evidence_and_verdict(cfg: Config) -> None:
    factual = factual_crash()
    cfs = [
        outcome("b_disable", "B_emergency_brake", "disable", "B", collision=False),
        outcome("a_disable", "A_late_brake", "disable", "A", collision=True),
    ]
    interventions = [
        InterventionSpec("b_disable", "B_emergency_brake", "disable", {}, "", "B"),
        InterventionSpec("a_disable", "A_late_brake", "disable", {}, "", "A"),
    ]
    failures = [{"intervention_id": "a_advance", "error": "RuntimeError: server lost"}]

    report = attribution_report(
        factual,
        cfs,
        cfg,
        interventions=interventions,
        failures=failures,
        scenario_id="S01",
        variant="crash",
        seed=0,
    )

    assert report["scenario_id"] == "S01"
    assert report["n_requested"] == 2
    assert report["n_completed"] == 2
    assert report["n_failed"] == 1
    assert report["factual"]["collision"] is True
    assert len(report["contributions"]) == 2
    assert report["classification"]["attribution_class"] == "single_initiator"
    assert report["severity_metric"] == "relative_impact_speed"
    # A replay that never ran must be distinguishable from one that ran and
    # failed to prevent anything.
    assert any("a_advance" in note for note in report["notes"])


def test_attribution_report_without_a_factual_outcome(cfg: Config) -> None:
    report = attribution_report(None, [outcome(collision=False)], cfg)
    assert report["classification"]["attribution_class"] == "insufficient_evidence"
    assert report["factual"] is None
    assert report["contributions"] == []


def test_attribution_report_is_json_serialisable(cfg: Config, tmp_path) -> None:
    from cdf.common.io import read_json, write_json

    report = attribution_report(
        factual_crash(),
        [outcome("b", "B_emergency_brake", "disable", "B", collision=False)],
        cfg,
        scenario_id="S01",
        variant="crash",
    )
    path = write_json(tmp_path / "causal_contribution.json", report)
    assert read_json(path)["classification"]["primary_initiator"] == "B_emergency_brake"


def test_a_run_that_never_collided_is_not_told_that_a_collision_survived() -> None:
    """The class was always right here; the sentence beside it was a falsehood.

    A negative control produces no collision, so every replay leaves the outcome
    unchanged and no action is ever but-for necessary -- which reaches
    ``insufficient_evidence`` correctly. The rationale, however, described "the
    collision still occurred in all N replays" about a run in which no collision
    ever occurred, and that sentence is what the viewer prints to a reader.
    """
    from cdf.causal.attribution import classify_attribution, contribution_of
    from cdf.causal.counterfactuals import CounterfactualOutcome

    factual = CounterfactualOutcome(
        intervention_id="factual", collision=False, near_miss=False,
        min_distance=20.0, min_ttc=3.0, impact_speed=None,
        relative_impact_speed=None, t_collision=None, collision_pairs=[],
        validation_passed=True, notes=[],
    )
    replays = [
        CounterfactualOutcome(
            intervention_id="{0}__disable".format(action), action_id=action,
            op="disable", collision=False, near_miss=False, min_distance=18.0,
            min_ttc=2.5, impact_speed=None, relative_impact_speed=None,
            t_collision=None, collision_pairs=[], validation_passed=True, notes=[],
        )
        for action in ("A_late_brake", "B_emergency_brake")
    ]
    contributions = [contribution_of(factual, cf, None) for cf in replays]

    verdict = classify_attribution(contributions, None, factual_collision=False)
    assert verdict["attribution_class"] == "insufficient_evidence"
    assert verdict["necessary_actions"] == []
    assert "no collision" in verdict["rationale"]
    assert "still occurred" not in verdict["rationale"], (
        "the rationale must not describe a collision that never happened"
    )

    # The collided case keeps its own, equally truthful sentence.
    collided = classify_attribution(contributions, None, factual_collision=True)
    assert collided["attribution_class"] == "insufficient_evidence"
    assert "still occurred" in collided["rationale"]


# ---------------------------------------------------------------------------
# What kind of replay can establish causation
# ---------------------------------------------------------------------------


def _outcome(op: str, collision: bool, action_id: str = "a") -> Any:
    from cdf.causal.counterfactuals import CounterfactualOutcome

    return CounterfactualOutcome(
        intervention_id="{0}__{1}".format(action_id, op), action_id=action_id,
        op=op, collision=collision, near_miss=False, min_distance=5.0,
        min_ttc=1.0, impact_speed=8.0 if collision else None,
        relative_impact_speed=8.0 if collision else None,
        t_collision=5.0 if collision else None, collision_pairs=[],
        validation_passed=True, notes=[],
    )


def test_removing_weakening_or_delaying_an_action_can_establish_causation() -> None:
    from cdf.causal.attribution import establishes_but_for

    for op in ("disable", "scale", "delay", "set"):
        assert establishes_but_for(_outcome(op, collision=False)) is True, op


def test_performing_an_action_sooner_cannot() -> None:
    """Braking earlier avoiding a crash says it was avoidable, not that it caused it."""
    from cdf.causal.attribution import establishes_but_for

    assert establishes_but_for(_outcome("advance", collision=False)) is False


def test_the_victim_is_not_named_because_it_could_have_reacted_sooner() -> None:
    """The rear-end shape, which is where this goes wrong if it goes wrong.

    A follows B. B brakes hard, A brakes too late, A hits B. Removing or
    weakening A's brake changes nothing -- A was reacting, not causing. Only
    advancing it avoids the crash. Count that as but-for causation and the
    method names the vehicle that was hit.
    """
    from cdf.causal.attribution import but_for, classify_attribution, contribution_of

    factual = _outcome("none", collision=True)
    replays = [
        _outcome("disable", collision=True, action_id="A_late_brake"),
        _outcome("scale", collision=True, action_id="A_late_brake"),
        _outcome("advance", collision=False, action_id="A_late_brake"),
        _outcome("disable", collision=False, action_id="B_emergency_brake"),
        _outcome("scale", collision=False, action_id="B_emergency_brake"),
        _outcome("advance", collision=True, action_id="B_emergency_brake"),
    ]
    contributions = [contribution_of(factual, cf, None) for cf in replays]
    verdict = classify_attribution(contributions, None, factual_collision=True)

    assert verdict["attribution_class"] == "single_initiator"
    assert verdict["necessary_actions"] == ["B_emergency_brake"]
    assert "A_late_brake" not in verdict["necessary_actions"], (
        "the vehicle that braked too late did not cause the collision it was in"
    )

    advanced = next(c for c in contributions
                    if c.op == "advance" and c.action_id == "A_late_brake")
    assert advanced.prevented_collision is True, "the replay did avoid the crash"
    assert advanced.establishes_causation is False
    assert but_for(factual, advanced.outcome) == 0
    assert any("sooner" in note for note in advanced.notes), (
        "a prevention that is not a cause must say which it is"
    )


def test_a_replay_that_prevents_by_removal_still_establishes_causation() -> None:
    from cdf.causal.attribution import but_for, contribution_of

    factual = _outcome("none", collision=True)
    removed = _outcome("disable", collision=False, action_id="B_emergency_brake")
    record = contribution_of(factual, removed, None)
    assert record.prevented_collision is True
    assert record.establishes_causation is True
    assert but_for(factual, removed) == 1
