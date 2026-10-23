"""The campaign v3 report (scripts/campaign_v3_report.py): statistics over seeds, pooling over runs, paired changes
against the G0 baseline of the same runs and the GNSS x radar interaction of the same seeds."""

import importlib.util
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("campaign_v3_report", str(ROOT / "scripts" / "campaign_v3_report.py"))
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


def _card(identified, reportable, phantoms, represented=1, observable=2, recorders=("A", "B")):
    vehicles = [{"vehicle": r, "role": "recorder", "observable": True, "represented": True, "coverage": 1.0}
                for r in recorders] + [{"vehicle": "V{0}".format(k), "role": "non-recorder", "observable": True,
                                        "represented": k < represented, "coverage": 0.5 if k < represented else None}
                                       for k in range(observable)]
    return {"recorders": list(recorders),
            "collisions": {"true": reportable, "reportable": reportable, "detected": identified,
                           "identified": identified, "invented": 0, "recontact_splits": 0,
                           "max_abs_timing_error_s": 0.0},
            "completeness": {"true_vehicles": len(vehicles), "observable": len(vehicles),
                             "represented_observable": len(recorders) + represented, "missed_observable": [],
                             "duplicates": 0, "recorder_ghosts": [],
                             "phantoms": ["U{0}".format(k) for k in range(phantoms)], "phantoms_near": [],
                             "vehicles": vehicles},
            "errors": {"centre_error_m": {"median": None, "p95": None}, "speed_error_mps": {"median": None, "p95": None}},
            "association": {"wrong_links": 0, "missed_links": 0, "merges": {"missed": 0, "false": 0}},
            "semantics": {"justified_warnings": 1, "justified_warned_in_time": 1,
                          "path_intrusions": {"found": 1, "expected": 1}, "unconfirmed_critical_ttc": []}}


def _job(run, family, level, seed, card, errors=(), recorder=None):
    return {"run": "traces/" + run, "family": family, "level": level, "seed": seed, "status": "complete",
            "recorder": recorder, "scorecard": card, "metrics": {"recorders": 2, "recorders_aligned": 2},
            "road_user_errors_raw": {"centre_error_m": list(errors), "speed_error_mps": []}}


class Statistics(unittest.TestCase):
    def test_the_interval_is_students_t_over_the_seeds(self):
        summary = report.mean_ci([1.0, 2.0, 3.0])
        half = 4.303 * 1.0 / math.sqrt(3)
        self.assertAlmostEqual(summary["mean"], 2.0)
        self.assertAlmostEqual(summary["ci_low"], 2.0 - half)
        self.assertAlmostEqual(summary["ci_high"], 2.0 + half)
        self.assertIsNone(report.mean_ci([5.0])["ci_low"])

    def test_bounded_quantities_keep_their_range(self):
        self.assertEqual(report.bounded("identified_rate", [0.8, 1.3]), [0.8, 1.0])
        self.assertEqual(report.bounded("phantoms_per_job", [-2.0, 4.0]), [0.0, 4.0])


class Pooling(unittest.TestCase):
    def setUp(self):
        self.records = [
            _job("S01/run_0_crash", "baseline", "none", 0, _card(1, 1, 0), errors=[0.1, 0.2]),
            _job("S02/run_0_crash", "baseline", "none", 0, _card(2, 2, 0), errors=[0.3]),
            _job("S01/run_0_crash", "radar_v3", "severe", 0, _card(1, 1, 4), errors=[0.5, 0.7]),
            _job("S02/run_0_crash", "radar_v3", "severe", 0, _card(1, 2, 6), errors=[0.9]),
            _job("S01/run_0_crash", "radar_v3", "severe", 1, _card(1, 1, 2), errors=[0.4]),
            _job("S02/run_0_crash", "radar_v3", "severe", 1, _card(2, 2, 8), errors=[0.6]),
        ]

    def _row(self):
        return next(r for r in report.condition_table(self.records)
                    if r["family"] == "radar_v3" and r["recorders"] == "all")

    def test_rates_are_ratios_of_sums_counts_means_per_job_errors_over_all_states(self):
        row = self._row()
        # seed 0: identified 2 of 3, phantoms (4 + 6) / 2, errors [0.5, 0.7, 0.9]; seed 1: 3 of 3, 5, [0.4, 0.6]
        self.assertAlmostEqual(row["identified_rate"], (2 / 3 + 1.0) / 2)
        self.assertAlmostEqual(row["phantoms_per_job"], 5.0)
        self.assertAlmostEqual(row["pos_median"], (0.7 + 0.5) / 2)
        self.assertAlmostEqual(row["missed_rate"], (1 / 3 + 0.0) / 2)
        self.assertEqual((row["seeds"], row["jobs"], row["runs"]), (2, 4, 2))

    def test_paired_changes_subtract_the_baseline_of_the_same_runs(self):
        row = self._row()
        self.assertAlmostEqual(row["d_identified_rate"], ((2 / 3 - 1.0) + 0.0) / 2)
        self.assertAlmostEqual(row["d_phantoms_per_job"], 5.0)
        self.assertAlmostEqual(row["d_pos_median"], ((0.7 - 0.2) + (0.5 - 0.2)) / 2)


    def test_a_run_without_a_baseline_leaves_the_paired_change_of_the_others(self):
        records = [r for r in self.records if not (r["family"] == "baseline" and r["run"].endswith("S02/run_0_crash"))]
        row = next(r for r in report.condition_table(records)
                   if r["family"] == "radar_v3" and r["recorders"] == "all")
        # only S01 pairs: seed 0 phantoms 4 - 0, seed 1 phantoms 2 - 0
        self.assertAlmostEqual(row["d_phantoms_per_job"], 3.0)


class Interaction(unittest.TestCase):
    def test_the_interaction_of_a_seed_is_its_combined_change_minus_the_single_sensor_changes(self):
        records = [_job("S01/run_0_crash", "baseline", "none", 0, _card(1, 1, 0))]
        for seed, (g, r, gr) in enumerate(((0, 4, 6), (0, 2, 3))):
            records += [_job("S01/run_0_crash", "gnss", "degraded", seed, _card(1, 1, g)),
                        _job("S01/run_0_crash", "radar_v3", "severe", seed, _card(1, 1, r)),
                        _job("S01/run_0_crash", "radar_gnss_v3", "gnss degraded + radar severe", seed,
                             _card(1, 1, gr))]
        row = next(r for r in report.interaction_table(records) if r["gnss"] == "degraded" and r["radar"] == "severe")
        self.assertEqual(row["seeds"], 2)
        self.assertAlmostEqual(row["phantoms_per_job_interaction"], ((6 - 0 - 4) + (3 - 0 - 2)) / 2)


if __name__ == "__main__":
    unittest.main()
