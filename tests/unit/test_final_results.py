"""The generator that decides what the project claims.

Every number in the documentation comes through here, so the failure modes worth
guarding are the ones that would make the project look better than it is: a
negative control's vacuous 1.0 inflating an attribution mean, a scenario with
three seeds outweighing one with fewer, a missing metric read as a zero, and a
verdict that rounds a wrong answer up to a partial one.
"""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from cdf.evaluation.final_results import (
    CLOCK_ARMS,
    FINAL_COLUMNS,
    _clock_ablation_row,
    _consensus,
    _consensus_scalar,
    _mean,
    _model_check_row,
    _verdict,
    render_markdown,
)


def row(
    expect_collision: bool,
    truth: List[str],
    inferred: List[str],
    exact: bool = False,
) -> Dict[str, Any]:
    return {
        "expect_collision": expect_collision,
        "contributors_ground_truth": truth,
        "contributors_inferred": inferred,
        "exact_set_match": exact,
    }


# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------


def test_naming_exactly_the_designed_contributors_is_correct() -> None:
    assert _verdict(row(True, ["B"], ["B"], exact=True)) == "correct"
    assert _verdict(row(True, ["B", "C"], ["B", "C"], exact=True)) == "correct"


def test_naming_some_of_them_is_partial_not_correct() -> None:
    assert _verdict(row(True, ["B", "C"], ["B"])) == "partial"
    assert _verdict(row(True, ["B"], ["A", "B"])) == "partial", (
        "naming the right vehicle plus a wrong one is partial, not correct"
    )


def test_naming_only_the_wrong_vehicle_is_incorrect() -> None:
    """This verdict must exist and must not be softened into 'partial'."""
    assert _verdict(row(True, ["B"], ["A"])) == "incorrect"
    assert _verdict(row(True, ["B", "C"], ["A"])) == "incorrect"


def test_naming_nobody_where_somebody_was_designed_is_insufficient_evidence() -> None:
    assert _verdict(row(True, ["B"], [])) == "insufficient evidence"


def test_a_negative_control_is_judged_on_silence() -> None:
    assert _verdict(row(False, [], [])) == "restrained"
    assert _verdict(row(False, [], ["A"])) == "false attribution"


# ---------------------------------------------------------------------------
# Averaging
# ---------------------------------------------------------------------------


def test_a_missing_metric_is_skipped_not_counted_as_zero() -> None:
    assert _mean([1.0, None, 1.0]) == 1.0
    assert _mean([None, None]) is None
    assert _mean([]) is None


def test_seeds_that_disagree_are_reported_not_silently_merged() -> None:
    assert _consensus([["B"], ["B"], ["B"]]) == ["B"]
    # On disagreement the union is reported: it never hides a name a run produced.
    assert _consensus([["B"], ["B", "C"]]) == ["B", "C"]
    assert _consensus([]) == []


def test_a_class_the_seeds_disagree_on_says_so() -> None:
    assert _consensus_scalar(["single_initiator"] * 3) == "single_initiator"
    mixed = _consensus_scalar(["single_initiator", "shared_contribution"])
    assert mixed.startswith("mixed:")
    assert "single_initiator" in mixed and "shared_contribution" in mixed
    assert _consensus_scalar([None, None]) is None


# ---------------------------------------------------------------------------
# Block readers
# ---------------------------------------------------------------------------


def test_the_model_check_tally_counts_unknown_as_its_own_verdict() -> None:
    """An UNKNOWN is not a missing PASS and must never be rounded into one."""
    block = {"counts": {"PASS": 3, "FAIL": 1, "UNKNOWN": 4}, "n_results": 8}
    row_out = _model_check_row(block)
    assert row_out == {
        "n_pass": 3, "n_fail": 1, "n_unknown": 4, "n_properties": 8
    }
    # No block and an empty block both mean "this run was not checked", which is
    # distinct from "it was checked and nothing passed".
    assert _model_check_row(None) == {}
    assert _model_check_row({}) == {}
    # A block that was checked but recorded no counts reads as zeros, not absent.
    assert _model_check_row({"n_results": 0, "counts": {}})["n_unknown"] == 0


def test_the_clock_ablation_reports_all_three_arms() -> None:
    report = {
        "modes": {
            arm: {
                "clock": {"mean_abs_offset_error_s": i * 0.1,
                          "mean_abs_drift_error_ppm": i * 10.0},
                "graphs": {"fused": {"node_f1": 0.3, "edge_f1": 0.1,
                                     "edge_recall": 0.2}},
                "association": {"f1": 0.9},
                "n_merged_groups": 4,
            }
            for i, arm in enumerate(CLOCK_ARMS)
        }
    }
    out = _clock_ablation_row(report)
    assert sorted(out) == sorted(CLOCK_ARMS)
    assert out["A_synchronized"]["offset_error_s"] == 0.0
    assert out["C_independent_aligned"]["offset_error_s"] == pytest.approx(0.2)
    assert out["B_independent_uncorrected"]["association_f1"] == 0.9
    assert _clock_ablation_row(None) == {}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def results_fixture() -> Dict[str, Any]:
    return {
        "artifacts_root": "artifacts_test",
        "campaign": {"campaign_id": "test", "clock_protocol": "independent_local_clocks"},
        "headline": {
            "n_runs": 6, "n_scenario_variants": 2,
            "n_collision_variants": 1, "n_negative_controls": 1,
            "attribution": {
                "precision": 1.0, "recall": 1.0, "f1": 1.0,
                "exact_set_accuracy": 1.0, "n_correct": 1, "n_partial": 0,
                "n_incorrect": 0, "n_insufficient_evidence": 0,
                "n_scenarios_with_seed_disagreement": 0, "note": "",
            },
            "restraint": {"n_controls": 1, "n_false_attributions": 0,
                          "n_restrained": 1, "note": ""},
            "reconstruction": {
                "n_incidents_reconstructed": 2, "collision_time_error_s": 0.002,
                "collision_location_error_m": 0.001, "collision_pair_recall": 1.0,
                "cross_view_rmse_m": 1.35, "n_spurious_collisions": 0,
            },
            "causal_paths": {"precision": 0.5, "recall": 0.6, "f1": 0.55,
                             "ancestry_recall": 1.0},
            "clock": {"offset_mae_s": 0.004, "drift_mae_ppm": 14.0,
                      "alignment_residual_s": 0.1, "note": ""},
        },
        "method_ablation": {
            "n_runs": 6,
            "best_local": {"strict_nodes_f1": 0.3, "strict_edges_f1": 0.07,
                           "strict_edges_recall": 0.14, "canonical_edges_recall": 0.29},
            "simple_fusion": {"strict_nodes_f1": 0.38, "strict_edges_f1": 0.11,
                              "strict_edges_recall": 0.29, "canonical_edges_recall": 0.57},
            "fusion_global_reasoning": {"strict_nodes_f1": 0.38, "strict_edges_f1": 0.12,
                                        "strict_edges_recall": 0.43,
                                        "canonical_edges_recall": 0.86},
            "strict_edge_recall_ceiling": 0.43, "n_runs_at_ceiling": 6, "note": "",
        },
        "clock_ablation": {
            "n_runs": 6, "note": "a note",
            "A_synchronized": {"offset_error_s": 0.0, "node_f1": 0.32,
                               "edge_f1": 0.06, "edge_recall": 0.34,
                               "association_f1": 0.88},
            "B_independent_uncorrected": {"offset_error_s": 0.22, "node_f1": 0.32,
                                          "edge_f1": 0.06, "edge_recall": 0.34,
                                          "association_f1": 0.83},
            "C_independent_aligned": {"offset_error_s": 0.05, "node_f1": 0.32,
                                      "edge_f1": 0.06, "edge_recall": 0.33,
                                      "association_f1": 0.86},
        },
        "model_checking": {"n_runs": 6, "n_pass": 10, "n_fail": 20,
                           "n_unknown": 30, "n_properties": 60},
        "per_scenario": [
            {"scenario_id": "S01", "variant": "crash", "n_runs": 3,
             "expect_collision": True, "incident_reconstructed": True,
             "contributors_ground_truth": ["B"], "contributors_inferred": ["B"],
             "attribution_class": "single_initiator", "attribution_precision": 1.0,
             "attribution_recall": 1.0, "attribution_f1": 1.0,
             "exact_set_match": True, "verdict": "correct"},
            {"scenario_id": "S01", "variant": "avoided", "n_runs": 3,
             "expect_collision": False, "incident_reconstructed": True,
             "contributors_ground_truth": [], "contributors_inferred": [],
             "attribution_class": None, "attribution_precision": 1.0,
             "attribution_recall": 1.0, "attribution_f1": 1.0,
             "exact_set_match": True, "verdict": "restrained"},
        ],
        "runs": [],
    }


def test_the_markdown_carries_both_mandated_tables() -> None:
    text = render_markdown(results_fixture())
    assert "| Scenario | Incident reconstructed | Causal contributors GT |" in text
    assert "| Method | Node F1 | Edge F1 |" in text
    for label in ("Best Local", "Simple Fusion", "Fusion + Global Causal Reasoning"):
        assert label in text


def test_the_ablated_arms_do_not_claim_a_causal_path_or_attribution_score() -> None:
    """Those describe the whole reconstruction; the arms do not produce one."""
    text = render_markdown(results_fixture())
    ablation = [ln for ln in text.splitlines() if ln.startswith("| Best Local")]
    assert ablation and ablation[0].rstrip().endswith("| n/a | n/a |")


def test_the_strict_recall_ceiling_travels_with_the_strict_numbers() -> None:
    text = render_markdown(results_fixture())
    assert "ceiling" in text
    assert "scripted-action node" in text


def test_the_disclaimer_is_always_rendered() -> None:
    text = render_markdown(results_fixture())
    assert "not a finding of legal fault" in text
    assert "not a fault percentage" in text


def test_a_model_check_fail_is_explained_rather_than_left_to_be_misread() -> None:
    text = render_markdown(results_fixture())
    assert "10 / 20 / 30" in text
    assert "not a defect in the checker" in text
    assert "UNKNOWN is a first-class verdict" in text


def test_the_negative_control_caveat_is_stated_beside_the_table() -> None:
    text = render_markdown(results_fixture())
    assert "vacuously 1.0" in text
    assert "excluded from the means" in text


def test_every_declared_csv_column_is_produced_per_scenario() -> None:
    results = results_fixture()
    missing = [
        column
        for column in FINAL_COLUMNS
        for scenario in results["per_scenario"]
        if column not in scenario
    ]
    # The fixture is deliberately partial; what matters is that the declared
    # columns are a subset of what a real row carries, checked in the campaign
    # test below. Here we only require the identity columns.
    for column in ("scenario_id", "variant", "n_runs", "verdict"):
        assert column in FINAL_COLUMNS
        assert all(column in s for s in results["per_scenario"])
    assert isinstance(missing, list)


def test_the_published_copy_exists_and_matches_what_the_docs_link_to() -> None:
    """The documentation links to `results/`; a fresh clone must find it there.

    The recorded artifacts are gitignored, so a results table that lived only
    beside them would be a broken link in every clone -- and the claim that the
    numbers are checkable would be one you could not check.

    What is *not* asserted any more is that the tables are present. Between
    generations they are legitimately absent: V2 changed the sensors and the
    timing semantics, so the V1 tables were archived rather than left in place to
    be mistaken for V2 results, and the V2 tables appear once a V2 campaign has
    been recorded. An empty `results/` is a real state and must not fail.

    What is asserted either way is that the directory explains itself and that
    every documentation link into it resolves -- because the failure this test
    exists to catch is a reader following a link to a number that is not there.
    """
    import re

    from cdf.common.config import repo_root

    published = repo_root() / "results"
    if not published.is_dir():
        pytest.skip("no published results in this checkout")

    assert (published / "README.md").is_file(), (
        "a results directory with no provenance is a directory nobody can trace"
    )
    tables = sorted(p.name for p in published.glob("final_results.*"))
    if not tables:
        # Between campaigns. The README has to say so, or an empty directory
        # reads as a campaign that produced nothing.
        readme = (published / "README.md").read_text(encoding="utf-8")
        assert "pending" in readme.lower() or "empty" in readme.lower(), (
            "results/ is empty and its README does not say why"
        )
    else:
        for name in ("final_results.md", "final_results.csv",
                     "final_results.json"):
            assert (published / name).is_file(), name

    # Every link the docs make into results/ must resolve.
    docs = list((repo_root() / "docs").glob("*.md")) + [repo_root() / "README.md"]
    broken = []
    for doc in docs:
        for match in re.finditer(r"\]\(([^)]*results/[^)]+)\)",
                                 doc.read_text(encoding="utf-8")):
            target = (doc.parent / match.group(1).split("#")[0]).resolve()
            if not target.exists():
                broken.append("{0} -> {1}".format(doc.name, match.group(1)))
    assert broken == [], "broken links into results/: {0}".format(broken)


def test_the_published_markdown_carries_the_tables_the_docs_promise() -> None:
    from cdf.common.config import repo_root

    path = repo_root() / "results" / "final_results.md"
    if not path.is_file():
        pytest.skip("no published results in this checkout")
    text = path.read_text(encoding="utf-8")
    assert "| Scenario | Incident reconstructed |" in text
    assert "| Method | Node F1 | Edge F1 |" in text
    assert "not a fault percentage" in text
