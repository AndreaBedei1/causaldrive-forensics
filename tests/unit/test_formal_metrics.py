"""Whether the property verdicts were the right ones, and what "right" excludes.

The point of this module is that a verdict can be wrong in two very different
ways and an average hides which. Accusing a vehicle of running a sign it stopped
at is not the same mistake as failing to notice one that did, and a property the
reconstruction could not decide is not a mistake at all.

Every test here is about keeping those three apart.
"""

from __future__ import annotations

from cdf.common.io import write_json
from cdf.common.layout import RunLayout
from cdf.evaluation.formal_metrics import aggregate_formal, measure_formal


def make_run(root, inferred=None, reference=None, observable=True):
    """A run whose two sets of verdicts are written directly.

    The reference is normally produced by running the checker over the
    observable trace. These tests write it in place instead, because what is
    being tested is the comparison, not the checker.
    """
    run = root / "S10_x" / "seed_000_rolls_through"
    run.mkdir(parents=True, exist_ok=True)
    layout = RunLayout.from_run_dir(run)
    write_json(layout.manifest, {
        "scenario_id": "S10", "variant": "rolls_through", "seed": 0,
    })
    write_json(layout.formal_results, {"results": inferred or []})
    if observable:
        # Written so the module tries to build a reference; the monkeypatched
        # reference_verdicts below is what actually supplies one.
        write_json(layout.observable_events, {"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_start": 1.0, "t_end": 1.0, "provenance": "oracle"},
        ]})
    return layout


def score(monkeypatch, root, inferred, reference, observable=True):
    layout = make_run(root, inferred, observable=observable)
    monkeypatch.setattr(
        "cdf.evaluation.formal_metrics.reference_verdicts",
        lambda _layout, _cfg=None: (
            {"results": reference} if reference is not None else None
        ),
    )
    return measure_formal(layout)


def prop(pid, status, vacuous=False):
    return {"property_id": pid, "status": status, "vacuous": vacuous}


# --- the two errors are counted apart ------------------------------------


def test_claiming_a_violation_the_truth_denies_is_a_false_violation(monkeypatch, tmp_path):
    """The expensive error: a vehicle accused of running a sign it stopped at."""
    out = score(monkeypatch, tmp_path, [prop("P3", "FAIL")], [prop("P3", "PASS")])
    assert out["false_violations"] == ["P3"]
    assert out["missed_violations"] == []
    assert out["false_violation_rate"] == 1.0
    assert out["per_property"]["P3"]["comparison"] == "false_violation"


def test_missing_a_violation_the_truth_shows_is_counted_separately(monkeypatch, tmp_path):
    out = score(monkeypatch, tmp_path, [prop("P3", "PASS")], [prop("P3", "FAIL")])
    assert out["missed_violations"] == ["P3"]
    assert out["false_violations"] == []
    assert out["missed_violation_rate"] == 1.0


def test_the_two_rates_are_never_added_into_one_accuracy(monkeypatch, tmp_path):
    """A single accuracy figure would let a conservative detector and a
    trigger-happy one look identical."""
    out = score(
        monkeypatch, tmp_path,
        [prop("P1", "FAIL"), prop("P2", "PASS"), prop("P3", "PASS")],
        [prop("P1", "PASS"), prop("P2", "FAIL"), prop("P3", "PASS")],
    )
    assert out["n_comparable"] == 3
    assert out["n_agree"] == 1
    assert out["false_violations"] == ["P1"]
    assert out["missed_violations"] == ["P2"]
    assert "accuracy" not in out


# --- UNKNOWN is not an error and is never folded into PASS ---------------


def test_an_undecided_property_is_not_scored_as_agreement(monkeypatch, tmp_path):
    """Folding UNKNOWN into PASS would make a run that observed nothing look
    perfect. Declining to decide is the behaviour the three-valued semantics
    exist to produce."""
    out = score(monkeypatch, tmp_path, [prop("P3", "UNKNOWN")], [prop("P3", "PASS")])
    assert out["undecided_by_reconstruction"] == ["P3"]
    assert out["n_comparable"] == 0
    assert out["n_agree"] == 0
    assert out["agreement"] is None
    assert out["false_violations"] == []
    assert out["missed_violations"] == []


def test_an_undecided_property_is_not_scored_as_a_missed_violation(monkeypatch, tmp_path):
    """The reference says FAIL and the reconstruction says UNKNOWN. It did not
    miss the violation -- it declined to claim one either way."""
    out = score(monkeypatch, tmp_path, [prop("P3", "UNKNOWN")], [prop("P3", "FAIL")])
    assert out["missed_violations"] == []
    assert out["undecided_by_reconstruction"] == ["P3"]


def test_a_property_undecidable_even_on_the_truth_does_not_blame_the_run(
    monkeypatch, tmp_path
):
    """If exact state could not decide it either, the reconstruction's verdict
    says nothing about the reconstruction. Reporting this as "the reconstruction
    declined" blames it for a limit of the property."""
    out = score(
        monkeypatch, tmp_path, [prop("P7", "UNKNOWN")], [prop("P7", "UNKNOWN")]
    )
    assert out["per_property"]["P7"]["comparison"] == "reference_undecided"
    assert out["undecided_by_reconstruction"] == []
    assert out["n_comparable"] == 0


def test_the_reference_being_undecided_is_checked_before_the_run_being_undecided(
    monkeypatch, tmp_path
):
    """Order matters: both sides UNKNOWN must read as a limit of the property,
    not as the reconstruction failing to establish something knowable."""
    out = score(
        monkeypatch, tmp_path, [prop("P7", "UNKNOWN")], [prop("P7", "UNKNOWN")]
    )
    assert out["per_property"]["P7"]["comparison"] != "undecided"


# --- vacuity ------------------------------------------------------------


def test_a_property_whose_trigger_never_fired_is_not_scored(monkeypatch, tmp_path):
    """A property that never applied has not been got right."""
    out = score(
        monkeypatch, tmp_path,
        [prop("P5", "PASS", vacuous=True)], [prop("P5", "PASS", vacuous=True)],
    )
    assert out["per_property"]["P5"]["comparison"] == "not_comparable"
    assert out["n_comparable"] == 0


def test_vacuous_on_one_side_only_is_still_not_comparable(monkeypatch, tmp_path):
    """The obligation arose on one side and not the other, so there is no shared
    obligation to agree about."""
    out = score(
        monkeypatch, tmp_path,
        [prop("P5", "PASS", vacuous=True)], [prop("P5", "FAIL")],
    )
    assert out["per_property"]["P5"]["comparison"] == "not_comparable"
    assert out["missed_violations"] == []


def test_vacuous_properties_are_counted_but_kept_out_of_the_verdict_counts(
    monkeypatch, tmp_path
):
    out = score(
        monkeypatch, tmp_path,
        [prop("P1", "PASS"), prop("P5", "PASS", vacuous=True)],
        [prop("P1", "PASS"), prop("P5", "PASS", vacuous=True)],
    )
    assert out["verdict_counts"]["vacuous"] == 1
    assert out["verdict_counts"]["PASS"] == 1


# --- a property present on only one side ---------------------------------


def test_a_property_only_one_side_checked_is_not_comparable(monkeypatch, tmp_path):
    out = score(monkeypatch, tmp_path, [prop("P1", "FAIL")], [prop("P2", "PASS")])
    assert out["per_property"]["P1"]["comparison"] == "not_comparable"
    assert out["per_property"]["P2"]["comparison"] == "not_comparable"
    assert out["false_violations"] == []


# --- no reference at all -------------------------------------------------


def test_without_a_reference_the_verdicts_are_reported_and_not_scored(
    monkeypatch, tmp_path
):
    """A run with no observable truth cannot be scored, but "the checker said
    this" is still a useful and different statement."""
    out = score(
        monkeypatch, tmp_path, [prop("P1", "FAIL")], None, observable=False
    )
    assert out["scored"] is False
    assert out["verdict_counts"]["FAIL"] == 1
    assert out["per_property"]["P1"]["inferred"] == "FAIL"
    assert "cannot be checked" in out["reason"]


def test_a_run_with_no_checker_output_says_so(tmp_path):
    run = tmp_path / "S10_x" / "seed_000_rolls_through"
    run.mkdir(parents=True, exist_ok=True)
    layout = RunLayout.from_run_dir(run)
    write_json(layout.manifest, {"scenario_id": "S10", "variant": "x", "seed": 0})
    out = measure_formal(layout)
    assert out["scored"] is False
    assert "has not run" in out["reason"]


# --- witnesses -----------------------------------------------------------


def test_a_disagreement_carries_a_concrete_instance(monkeypatch, tmp_path):
    """A rate without an example is a number nobody can check."""
    inferred = [{
        "property_id": "P3", "status": "FAIL", "vacuous": False,
        "counterexamples": [{
            "trigger_event_id": "fused:A:STOP_SIGN:1", "participant": "A",
            "t": 4.25, "interval": [4.0, 6.0], "witness": ["e1", "e2"],
            "reason": "no full stop inside the window",
        }],
    }]
    out = score(monkeypatch, tmp_path, inferred, [prop("P3", "PASS")])
    witness = out["per_property"]["P3"]["witness"]
    assert witness["participant"] == "A"
    assert witness["t"] == 4.25
    assert witness["witness_event_ids"] == ["e1", "e2"]


# --- campaign totals -----------------------------------------------------


def test_totals_sum_counts_rather_than_averaging_rates():
    """Averaging per-run rates would let a run with one comparable property
    outweigh a run with eight."""
    runs = [
        {"scored": True, "n_comparable": 1, "n_agree": 0,
         "false_violations": ["P1"], "missed_violations": [],
         "undecided_by_reconstruction": []},
        {"scored": True, "n_comparable": 8, "n_agree": 8,
         "false_violations": [], "missed_violations": [],
         "undecided_by_reconstruction": []},
    ]
    out = aggregate_formal(runs)
    assert out["n_comparable"] == 9
    assert out["n_agree"] == 8
    assert out["agreement"] == round(8 / 9, 4)
    # Averaging the two runs' rates would have given 0.5.
    assert out["false_violation_rate"] == round(1 / 9, 4)


def test_totals_name_which_property_produced_the_false_violations():
    """One property failing everywhere and eight failing once each give the same
    rate and are completely different problems."""
    runs = [
        {"scored": True, "n_comparable": 3, "n_agree": 2,
         "false_violations": ["P3"], "missed_violations": [],
         "undecided_by_reconstruction": ["P7"]},
        {"scored": True, "n_comparable": 3, "n_agree": 2,
         "false_violations": ["P3"], "missed_violations": [],
         "undecided_by_reconstruction": []},
    ]
    out = aggregate_formal(runs)
    assert out["false_violations_by_property"] == {"P3": 2}
    assert out["undecided_by_property"] == {"P7": 1}


def test_totals_over_nothing_say_so_rather_than_reporting_zero():
    out = aggregate_formal([])
    assert out["scored"] is False
    assert out["n_runs"] == 0
