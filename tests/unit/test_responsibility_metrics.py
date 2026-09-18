"""Whether the responsibility findings matched what the scenario designed.

The defect these tests exist to prevent is a category error, and it is one this
module actually shipped with: the causal template names *physical* causes, the
responsibility layer names *normative* contributors, and an earlier version
scored one against the other. On a recorded chain that produced designed=[A, C]
against supported=[B] and a precision of 0.0 -- a meaningless number that looked
exactly like a method failure.

A vehicle that brakes hard is a designed physical cause of the crash behind it
and has broken no rule. Those two claims cannot share a metric.
"""

from __future__ import annotations

from cdf.common.io import write_json
from cdf.common.layout import RunLayout
from cdf.evaluation.responsibility_metrics import (
    aggregate_responsibility,
    designed_contributors,
    measure_responsibility,
)


def make_run(root, findings=None, template=None, scenario="S06",
             variant="a_front_pushed", design=True, mechanism=True):
    run = root / "{0}_x".format(scenario) / "seed_000_{0}".format(variant)
    run.mkdir(parents=True, exist_ok=True)
    layout = RunLayout.from_run_dir(run)
    write_json(layout.manifest, {
        "scenario_id": scenario, "variant": variant, "seed": 0,
    })
    write_json(layout.responsibility_report, {"findings": findings or {}})
    if design:
        write_json(layout.scenario_design_graph, {
            "causal_template": template or [],
            "mechanism_executed": mechanism,
        })
    return layout


def finding(evidence, physical):
    return {
        "responsibility_evidence": evidence,
        "physical_causal_contributor": physical,
    }


# The chain-collision template, as the frozen scenario actually declares it:
# entirely physical, with no rule broken by anyone.
CHAIN_TEMPLATE = [
    {"cause": {"kind": "action", "participant": "C",
               "action_id": "C_emergency_brake", "name": "C_emergency_brake"},
     "effect": {"kind": "state", "participant": "B", "name": "closing"},
     "edge": "TRIGGERS"},
    {"cause": {"kind": "action", "participant": "A",
               "action_id": "A_very_late_brake", "name": "A_very_late_brake"},
     "effect": {"kind": "outcome", "name": "collision"},
     "edge": "PREVENTS"},
    {"cause": {"kind": "state", "participant": "A", "name": "critical_ttc"},
     "effect": {"kind": "outcome", "name": "collision"},
     "edge": "CAUSES_OUTCOME"},
]

# A stop-sign template, which does make a normative claim.
STOP_TEMPLATE = [
    {"cause": {"kind": "state", "participant": "A", "name": "no_stop"},
     "effect": {"kind": "outcome", "name": "collision"},
     "edge": "CAUSES_OUTCOME"},
    {"cause": {"kind": "action", "participant": "B", "action_id": "B_cruise",
               "name": "B_cruise"},
     "effect": {"kind": "outcome", "name": "collision"},
     "edge": "CONTRIBUTES_TO"},
]


# --- the category error --------------------------------------------------


def test_a_physical_template_declares_no_normative_failing():
    """Braking hard closes a gap and breaks no rule."""
    designed = designed_contributors({"causal_template": CHAIN_TEMPLATE})
    assert designed["physical"] == ["A", "C"]
    assert designed["normative"] == []
    assert designed["declares_any_normative_failing"] is False


def test_a_normative_template_names_only_the_rule_breaker_as_normative():
    designed = designed_contributors({"causal_template": STOP_TEMPLATE})
    assert designed["physical"] == ["A", "B"]
    assert designed["normative"] == ["A"]
    assert designed["declares_any_normative_failing"] is True


def test_template_causes_are_never_scored_against_responsibility_findings(tmp_path):
    """The defect this module shipped with. The chain template names A and C as
    physical causes; the reconstruction named B as a normative contributor.
    Comparing those two directly gave precision 0.0 and meant nothing."""
    layout = make_run(tmp_path, template=CHAIN_TEMPLATE, findings={
        "A": finding("insufficient", "no"),
        "B": finding("supported", "yes"),
        "C": finding("partial", "yes"),
    })
    out = measure_responsibility(layout)
    assert out["scored"] is True
    # The physical comparison is against the physical contributors.
    assert out["physical"]["designed"] == ["A", "C"]
    assert out["physical"]["found"] == ["B", "C"]
    # The normative comparison does not happen at all, because there is no
    # normative reference to compare with.
    assert out["normative"]["applicable"] is False
    assert "sets" not in out["normative"]


def test_a_finding_the_design_does_not_cover_is_not_a_false_positive(tmp_path):
    """A reconstruction that finds a real rule violation the scenario never
    designed has not made an error against a reference that says nothing on the
    subject. Scoring it as a false positive punishes the method for the
    scenario's silence."""
    layout = make_run(tmp_path, template=CHAIN_TEMPLATE, findings={
        "B": finding("supported", "yes"),
    })
    out = measure_responsibility(layout)
    assert out["normative"]["applicable"] is False
    assert out["normative"]["findings_the_design_does_not_cover"] == ["B"]
    assert "not a false positive" in out["normative"]["why_not"]


def test_a_prevents_edge_is_not_a_designed_cause():
    """A's late brake is designed to act against the collision. Counting it
    would make every vehicle that braked a designed cause of the crash."""
    designed = designed_contributors({"causal_template": [
        {"cause": {"kind": "action", "participant": "Z", "name": "Z_brake"},
         "effect": {"kind": "outcome", "name": "collision"},
         "edge": "PREVENTS"},
    ]})
    assert designed["physical"] == []


# --- the normative comparison, where a reference exists ------------------


def test_naming_the_designed_rule_breaker_is_an_exact_match(tmp_path):
    layout = make_run(tmp_path, template=STOP_TEMPLATE, scenario="S10",
                      variant="rolls_through", findings={
                          "A": finding("supported", "yes"),
                          "B": finding("insufficient", "no"),
                      })
    out = measure_responsibility(layout)
    assert out["normative"]["applicable"] is True
    assert out["normative"]["designed"] == ["A"]
    assert out["normative"]["supported"] == ["A"]
    assert out["normative"]["exact_set_match"] is True
    assert out["normative"]["sets"]["precision"] == 1.0
    assert out["normative"]["sets"]["recall"] == 1.0


def test_naming_the_wrong_vehicle_is_reported_in_both_directions(tmp_path):
    """Precision and recall alone do not say which vehicle was wrong, and on a
    two-vehicle scenario the reader needs the names."""
    layout = make_run(tmp_path, template=STOP_TEMPLATE, scenario="S10",
                      variant="rolls_through", findings={
                          "A": finding("insufficient", "no"),
                          "B": finding("supported", "yes"),
                      })
    out = measure_responsibility(layout)
    assert out["normative"]["named_but_not_designed"] == ["B"]
    assert out["normative"]["designed_but_not_named"] == ["A"]
    assert out["normative"]["exact_set_match"] is False


def test_the_right_vehicle_graded_partial_is_a_different_near_miss(tmp_path):
    """Correctly identified but graded partial is not the same failure as naming
    the wrong vehicle, and the two are not averaged together."""
    layout = make_run(tmp_path, template=STOP_TEMPLATE, scenario="S10",
                      variant="rolls_through", findings={
                          "A": finding("partial", "yes"),
                      })
    out = measure_responsibility(layout)
    assert out["normative"]["designed_but_named_partial"] == ["A"]
    assert out["normative"]["designed_but_not_named"] == ["A"]


# --- the weaker reference says so ---------------------------------------


def test_a_scenario_that_did_not_execute_as_written_carries_a_caveat(tmp_path):
    """A disagreement may mean the reconstruction was wrong or may mean the
    scenario never did what it says. Those are different problems."""
    layout = make_run(tmp_path, template=STOP_TEMPLATE, mechanism=False,
                      findings={"A": finding("supported", "yes")})
    out = measure_responsibility(layout)
    assert out["scenario_mechanism_executed"] is False
    assert "may be the scenario rather than the method" in out["mechanism_caveat"]


def test_a_scenario_that_executed_carries_no_caveat(tmp_path):
    layout = make_run(tmp_path, template=STOP_TEMPLATE,
                      findings={"A": finding("supported", "yes")})
    assert measure_responsibility(layout)["mechanism_caveat"] is None


def test_without_a_design_reference_nothing_is_scored(tmp_path):
    layout = make_run(tmp_path, design=False,
                      findings={"B": finding("supported", "yes")})
    out = measure_responsibility(layout)
    assert out["scored"] is False
    assert out["supported_contributors"] == ["B"]


def test_without_a_responsibility_report_nothing_is_scored(tmp_path):
    run = tmp_path / "S06_x" / "seed_000_a_front_pushed"
    run.mkdir(parents=True)
    layout = RunLayout.from_run_dir(run)
    write_json(layout.manifest, {"scenario_id": "S06", "variant": "x", "seed": 0})
    out = measure_responsibility(layout)
    assert out["scored"] is False
    assert "has not run" in out["reason"]


# --- the hard cases are named, not averaged -----------------------------


def test_a_hard_case_is_flagged_by_name(tmp_path):
    """The pushed vehicle must not become an initiating contributor merely
    because it struck the vehicle ahead. An aggregate can hide getting this
    exactly backwards."""
    layout = make_run(tmp_path, template=CHAIN_TEMPLATE, scenario="S14",
                      variant="c_pushes_b",
                      findings={"B": finding("supported", "yes")})
    out = measure_responsibility(layout)
    assert "pushed vehicle" in out["hard_case"]


def test_an_ordinary_run_has_no_hard_case_note(tmp_path):
    layout = make_run(tmp_path, template=STOP_TEMPLATE, scenario="S10",
                      variant="rolls_through",
                      findings={"A": finding("supported", "yes")})
    assert measure_responsibility(layout)["hard_case"] is None


# --- campaign totals ----------------------------------------------------


def test_normative_totals_cover_only_the_runs_with_a_normative_reference():
    """Runs whose scenario designs no rule violation must not be counted as
    zero-precision runs -- they are runs the question does not apply to."""
    runs = [
        {"scored": True, "scenario": "S06", "variant": "a_front_pushed",
         "physical": {"designed": ["A", "C"], "found": ["B", "C"],
                      "sets": {"n_expected": 2, "n_found": 2, "n_matched": 1},
                      "exact_set_match": False},
         "normative": {"applicable": False, "designed": [], "supported": ["B"]}},
        {"scored": True, "scenario": "S10", "variant": "rolls_through",
         "physical": {"designed": ["A"], "found": ["A"],
                      "sets": {"n_expected": 1, "n_found": 1, "n_matched": 1},
                      "exact_set_match": True},
         "normative": {"applicable": True, "designed": ["A"], "supported": ["A"],
                       "sets": {"n_expected": 1, "n_found": 1, "n_matched": 1}}},
    ]
    out = aggregate_responsibility(runs)
    assert out["n_runs"] == 2
    assert out["n_runs_with_a_normative_reference"] == 1
    assert out["normative_contributor_sets"]["precision"] == 1.0
    # The physical comparison covers both runs.
    assert out["physical_contributor_sets"]["n_expected"] == 3
    assert out["n_exact_physical_match"] == 1


def test_totals_sum_counts_so_a_three_car_run_weighs_more_than_a_two_car_one():
    runs = [
        {"scored": True, "physical": {
            "sets": {"n_expected": 1, "n_found": 1, "n_matched": 0},
            "exact_set_match": False},
         "normative": {"applicable": False}},
        {"scored": True, "physical": {
            "sets": {"n_expected": 3, "n_found": 3, "n_matched": 3},
            "exact_set_match": True},
         "normative": {"applicable": False}},
    ]
    out = aggregate_responsibility(runs)
    assert out["physical_contributor_sets"]["n_matched"] == 3
    # Averaging the two runs' precisions would have given 0.5.
    assert out["physical_contributor_sets"]["precision"] == 0.75


def test_totals_with_no_normative_reference_anywhere_report_none_not_zero():
    runs = [{"scored": True, "physical": {
        "sets": {"n_expected": 1, "n_found": 1, "n_matched": 1},
        "exact_set_match": True}, "normative": {"applicable": False}}]
    out = aggregate_responsibility(runs)
    assert out["n_runs_with_a_normative_reference"] == 0
    assert out["normative_contributor_sets"] is None


def test_totals_over_nothing_say_so():
    out = aggregate_responsibility([])
    assert out["scored"] is False
    assert out["n_runs"] == 0
