"""The robustness campaign's driver, evaluation breakdowns and report: the GNSS x radar family pairs its random
draws with the single-sensor families, failed jobs are retried and counted once, distance bands and incident
participants follow their definitions, and the interaction is C - R - G + B."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def _script(name):
    import sys
    for path in (str(ROOT / "scripts"), str(ROOT / "src")):
        if path not in sys.path:
            sys.path.insert(0, path)
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rob = _script("robustness")

    def test_six_gnss_radar_cells_with_both_sensors(self):
        levels, stochastic = self.rob.FAMILIES["radar_gnss_combined"]
        self.assertTrue(stochastic)
        self.assertEqual(len(levels), 6)
        self.assertEqual({p for _, p in levels}, {(g, r) for g in ("rtk", "degraded")
                                                  for r in ("low", "nominal", "high")})
        run = str(ROOT / "traces/S12/run_0_crash")
        perturbation, pose = self.rob.build({"run": run, "family": "radar_gnss_combined", "level": levels[4][0],
                                             "parameter": levels[4][1], "seed": 2})
        self.assertEqual(perturbation.radar.name, "nominal")
        self.assertEqual(perturbation.gnss.name, "degraded")
        self.assertIsNotNone(pose)
        self.assertEqual(set(self.rob.FAMILIES["gnss"][0]), {("rtk", "rtk"), ("degraded", "degraded")})
        # G0 is measured by baseline; combined retains its exact + 10% condition.
        self.assertEqual([l for l, _ in self.rob.FAMILIES["combined"][0]],
                         ["exact + 10%", "RTK + 10%", "degraded independent + 10%",
                          "degraded common 0.9 + 10%"])

    def test_paired_draws_with_the_single_sensor_jobs(self):
        run = ROOT / "traces/S12/run_0_crash"
        if not run.exists():
            self.skipTest("canonical trace not present")
        _, combined_pose = self.rob.build({"run": str(run), "family": "radar_gnss_combined",
                                           "level": "gnss degraded + radar high", "parameter": ("degraded", "high"), "seed": 1})
        _, gnss_pose = self.rob.build({"run": str(run), "family": "gnss", "level": "degraded", "parameter": "degraded",
                                       "seed": 1})
        vehicle = run / "vehicles" / "A"
        origin = json.loads((vehicle / "ego.jsonl").open(encoding="utf-8").readline())["timestamp"]
        a, b = combined_pose(vehicle, origin), gnss_pose(vehicle, origin)
        for key in ("x", "y", "yaw", "vx", "vy"):
            np.testing.assert_array_equal(getattr(a, key), getattr(b, key))
        # The radar stream is keyed by seed, profile, recorder and radar only (never by the family).
        from cdf.robustness.perturb import stream_seed
        self.assertEqual(stream_seed(1, "radar", "high", "A", "front"), stream_seed(1, "radar", "high", "A", "front"))
        self.assertNotEqual(stream_seed(1, "radar", "high", "A", "front"), stream_seed(1, "gnss", "high", "A", "front"))

    def test_radar_draws_are_identical_in_single_and_combined_families(self):
        from src.cdf.robustness.perturb import GNSS_PROFILES, RADAR_PROFILES, Perturbation, perturbed_copy
        run = ROOT / "traces/S12/run_0_crash"
        with tempfile.TemporaryDirectory() as temp:
            single = perturbed_copy(run, Path(temp) / "single", Perturbation("radar", radar=RADAR_PROFILES["high"]), 4)
            combined = perturbed_copy(run, Path(temp) / "combined",
                                      Perturbation("combined", radar=RADAR_PROFILES["high"],
                                                   gnss=GNSS_PROFILES["degraded"]), 4)
            for single_path in single.glob("vehicles/*/radar/*/observations.npz"):
                relative = single_path.relative_to(single)
                with np.load(single_path) as a, np.load(combined / relative) as b:
                    for key in a.files:
                        np.testing.assert_array_equal(a[key], b[key])

    def test_retries_are_counted_once(self):
        job = {"run": "r", "family": "radar", "level": "low", "seed": 0}
        results = [dict(job, status="failed", error="x"), dict(job, status="complete"), dict(job, status="failed")]
        latest = self.rob.latest_results(results)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0]["status"], "complete")
        self.assertEqual(self.rob.latest_results([dict(job, status="failed", error="a"),
                                                  dict(job, status="failed", error="b")])[0]["error"], "b")


class BandTests(unittest.TestCase):
    def test_bands(self):
        from cdf.evaluation.campaign_metrics import band_of
        self.assertEqual(band_of(None), "unmeasured")
        self.assertEqual(band_of(9.99), "0-10 m")
        self.assertEqual(band_of(10.0), "10-25 m")
        self.assertEqual(band_of(25.0), ">25 m")

    def test_incident_participants_are_the_true_contact_partners(self):
        from cdf.evaluation.campaign_metrics import incident_participants
        run = ROOT / "traces/S10/run_0_deflected_into_c"
        if not run.exists():
            self.skipTest("canonical trace not present")
        self.assertEqual(incident_participants(run), ["A", "B", "C"])


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = _script("campaign_report")

    def job(self, family, level, run, seed, wrong):
        return {"family": family, "level": level, "run": run, "seed": seed, "status": "complete",
                "metrics": {"associations_correct": 10 - wrong, "associations_decided": 10, "links_wrong": wrong,
                            "links_missed": 0, "merges_false": 0, "merges_missed": 0, "recorders": 2,
                            "recorders_aligned": 2},
                "campaign": {"collisions": {"true_contacts": 1, "detected": 1, "identified": 1,
                                            "detected_wrong_participants": 0, "extra_reconstructed_vehicle_pairs": 0}},
                "events": {"base_events": 4, "matched": 4, "extra": [], "time_deltas_s": []}}

    def test_interaction_is_combined_minus_singles_plus_baseline(self):
        jobs = []
        for run in ("r1", "r2", "r3"):
            jobs.append(self.job("baseline", "none", run, 0, 0))
            for seed in (0, 1, 2):
                jobs.append(self.job("radar", "high", run, seed, 1))
                jobs.append(self.job("gnss", "degraded", run, seed, 2))
                jobs.append(self.job("radar_gnss_combined", "gnss degraded + radar high", run, seed, 5))
        rows = [r for r in self.rep.interaction_table(jobs)
                if r["gnss"] == "degraded" and r["radar"] == "high" and r["metric"] == "association_errors"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["interaction_mean"], 2.0)  # 5 - 1 - 2 + 0
        self.assertEqual(rows[0]["additive_prediction"], 3.0)
        self.assertEqual(rows[0]["runs"], 3)
        empty = [r for r in self.rep.interaction_table(jobs) if r["gnss"] == "rtk" and r["radar"] == "low"]
        self.assertTrue(all(r["runs"] == 0 and r["note"] == "insufficient paired evidence" for r in empty))

    def test_undefined_values_stay_undefined(self):
        row = self.job("radar", "low", "r1", 0, 0)
        row["metrics"]["associations_decided"] = 0
        row["metrics"]["associations_correct"] = 0
        table = self.rep.condition_table([row])
        self.assertIsNone(table[0]["association_accuracy"])

    def test_pose_tail_percentiles_reach_report_metrics(self):
        row = self.job("gnss", "degraded", "r1", 0, 0)
        stats = {"samples": 10, "rms": 1.0, "median": 0.5, "p50": 0.5, "p95": 1.5,
                 "p99": 1.9, "p995": 1.99, "max": 2.0}
        row["pose_errors"] = {"absolute_position_m": stats, "relative_position_m": stats,
                              "heading_deg": stats, "velocity_mps": stats}
        numbers = self.rep.job_numbers(row)
        self.assertEqual(numbers["pose_position_p995_m"], 1.99)
        self.assertEqual(numbers["pose_heading_max_deg"], 2.0)
        self.assertEqual(self.rep.METRICS["absolute_pose_position_p995"][0]([numbers]), 1.99)
        self.assertEqual(self.rep.METRICS["absolute_pose_velocity_p99"][0]([numbers]), 1.9)


if __name__ == "__main__":
    unittest.main()
