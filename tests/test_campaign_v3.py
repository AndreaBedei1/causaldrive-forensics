"""Campaign v3 (docs/CAMPAIGN_V3.md): asymmetric radar degradation over recorder subsets, paired random
streams, the scorecard summaries per condition, seed, scenario and recorder, and the seed rule."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.robustness.perturb import RADAR_PROFILES, Perturbation, perturbed_copy  # noqa: E402

from synthetic_run import make_run  # noqa: E402


def _script(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rob = _script("robustness")


def _fake_run(root: Path, recorders):
    for r in recorders:
        (root / "vehicles" / r).mkdir(parents=True)
        (root / "vehicles" / r / "ego.jsonl").write_text('{"timestamp": 0.0}\n', encoding="utf-8")
    return root


class AsymmetricRadarJobs(unittest.TestCase):
    def _subsets(self, recorders):
        with tempfile.TemporaryDirectory() as tmp:
            jobs = rob.jobs_for(_fake_run(Path(tmp), recorders), "radar_asym", [0])
        levels = {job["level"] for job in jobs}
        self.assertEqual(levels, {"nominal", "severe", "extreme"})
        return sorted({job["recorder"] for job in jobs}), len(jobs)

    def test_two_recorders_degrade_one_and_then_the_other(self):
        self.assertEqual(self._subsets(["A", "B"]), (["A", "B"], 6))

    def test_three_recorders_degrade_each_alone_and_each_pair(self):
        subsets, n = self._subsets(["A", "B", "C"])
        self.assertEqual(subsets, ["A", "A+B", "A+C", "B", "B+C", "C"])
        self.assertEqual(n, 18)

    def test_four_recorders_degrade_each_alone_and_all_but_each_one(self):
        subsets, _ = self._subsets(["A", "B", "C", "D"])
        self.assertEqual(subsets, ["A", "A+B+C", "A+B+D", "A+C+D", "B", "B+C+D", "C", "D"])

    def test_a_subset_job_degrades_exactly_its_recorders(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = _fake_run(Path(tmp), ["A", "B", "C"])
            job = next(j for j in rob.jobs_for(run, "radar_asym", [0]) if j["recorder"] == "A+C")
            perturbation, pose = rob.build(job)
        self.assertEqual(perturbation.radar_recorders, ("A", "C"))
        self.assertIsNone(pose)
        self.assertEqual(perturbation.radar_profile_of("B").name, "ideal")
        self.assertEqual(perturbation.radar_profile_of("C").name, "nominal")



class AsymmetricRadarUnderDegradedGnss(unittest.TestCase):
    """``radar_asym_gnss``: the recorder subsets of ``radar_asym`` with G2 degraded GNSS on every recorder, at the
    realistic radar levels (nominal, severe): the same radar errors as ``radar_asym`` and the same GNSS errors as
    ``gnss`` degraded, so each comparison is paired."""

    def test_the_jobs_are_the_asymmetric_subsets_at_the_realistic_levels(self):
        with tempfile.TemporaryDirectory() as tmp:
            jobs = rob.jobs_for(_fake_run(Path(tmp), ["A", "B", "C"]), "radar_asym_gnss", [0, 1])
        self.assertEqual(sorted({j["level"] for j in jobs}), ["gnss degraded + radar nominal",
                                                              "gnss degraded + radar severe"])
        self.assertEqual(sorted({j["recorder"] for j in jobs}), ["A", "A+B", "A+C", "B", "B+C", "C"])
        self.assertEqual(len(jobs), 2 * 6 * 2)
        self.assertIn("radar_asym_gnss", rob.V3_FAMILIES)

    def test_a_job_degrades_the_radar_of_its_subset_and_the_gnss_of_every_recorder(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp) / "run")
            job = next(j for j in rob.jobs_for(run, "radar_asym_gnss", [3])
                       if j["recorder"] == "B" and j["level"].endswith("severe"))
            perturbation, pose = rob.build(job)
            gnss_job = next(j for j in rob.jobs_for(run, "gnss", [3]) if j["level"] == "degraded")
            _, gnss_pose = rob.build(gnss_job)
            self.assertEqual(perturbation.radar_recorders, ("B",))
            self.assertEqual(perturbation.radar_profile_of("A").name, "ideal")
            self.assertEqual(perturbation.radar_profile_of("B").name, "severe")
            for recorder in ("A", "B"):  # the GNSS errors of every recorder are those of gnss degraded
                vehicle = run / "vehicles" / recorder
                first = json.loads((vehicle / "ego.jsonl").read_text(encoding="utf-8").splitlines()[0])
                here, there = pose(vehicle, first["timestamp"]).pose_at(1.0), gnss_pose(vehicle, first["timestamp"]).pose_at(1.0)
                self.assertEqual((here.x, here.y, here.yaw), (there.x, there.y, there.yaw))
                self.assertNotEqual(here.x, first["x"])



class RawErrors(unittest.TestCase):
    """Each job keeps the errors of its road users state by state (recorder ghosts excluded), so that a condition's
    median, P95 and RMSE pool the states of all its runs exactly."""

    def test_a_job_keeps_the_road_user_errors_of_every_state(self):
        fusion = {"_raw": {"road_user_errors": {"centre_error_m": [0.12345, 0.5], "speed_error_mps": [0.01],
                                                "heading_error_deg": [3.0]},
                           "errors": {"centre_error_m": [9.0, 0.12345, 0.5]}}}
        self.assertEqual(rob.raw_errors(fusion), {"centre_error_m": [0.1235, 0.5], "speed_error_mps": [0.01]})
        self.assertEqual(rob.raw_errors({}), {"centre_error_m": [], "speed_error_mps": []})



class SeedRuleRate(unittest.TestCase):
    def test_the_identified_rate_of_the_seed_rule_is_over_the_reportable_collisions(self):
        card = _card(1, 2, 1, 1)
        card["collisions"]["reportable"] = 1  # one of the two true collisions involves no recorder
        record = {"status": "complete", "scorecard": card, "events": {"base_events": 0, "time_deltas_s": [],
                                                                      "matched": 0, "extra": []}}
        self.assertEqual(rob.pooled([record])["collisions_identified_rate"], 1.0)


def _observations(run: Path, recorder: str):
    path = next((run / "vehicles" / recorder / "radar").glob("*/observations.npz"))
    with np.load(str(path)) as data:
        return {key: data[key].copy() for key in data.files}


class PairedAsymmetricStreams(unittest.TestCase):
    def test_a_recorder_degraded_alone_receives_the_errors_of_the_all_degraded_condition(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp) / "run")
            severe = RADAR_PROFILES["severe"]
            alone = perturbed_copy(run, Path(tmp) / "alone", Perturbation("severe A", radar=severe,
                                                                         radar_recorders=("A",)), seed=4)
            both = perturbed_copy(run, Path(tmp) / "both", Perturbation("severe", radar=severe), seed=4)
            a_alone, a_both = _observations(alone, "A"), _observations(both, "A")
            for key in a_both:
                np.testing.assert_array_equal(a_alone[key], a_both[key])
            b_alone, b_raw = _observations(alone, "B"), _observations(run, "B")
            for key in b_raw:
                np.testing.assert_array_equal(b_alone[key], b_raw[key])
            self.assertNotEqual(len(a_both["detections"]), len(_observations(run, "A")["detections"]))


def _card(identified, true, represented, observable, duplicates=0, phantoms=0, ghosts=0, pos=None, invented=0,
          recorders=("A", "B")):
    return {"recorders": list(recorders), "collisions": {"true": true, "detected": identified, "identified": identified, "invented": invented,
                           "max_abs_timing_error_s": 0.0},
            # observable / represented: road users that record nothing; the recorders count as observable and
            # represented in the scorecard's own totals, as in cdf.evaluation.scorecard.scorecard
            "completeness": {"true_vehicles": observable + len(recorders), "observable": observable + len(recorders),
                             "represented_observable": represented + len(recorders),
                             "missed_observable": ["X"] * (observable - represented), "duplicates": duplicates,
                             "recorder_ghosts": ["U9"] * ghosts, "phantoms": ["U{0}".format(k) for k in range(phantoms)],
                             "vehicles": [{"vehicle": r, "role": "recorder", "observable": True, "represented": True}
                                          for r in recorders]
                                         + [{"vehicle": "V{0}".format(k), "role": "non-recorder", "observable": True,
                                             "represented": k < represented} for k in range(observable)]},
            "errors": {"centre_error_m": {"median": pos, "p95": pos}, "speed_error_mps": {"median": None, "p95": None}},
            "association": {"wrong_links": 0, "merges": {"missed": 0, "false": 0}},
            "semantics": {"justified_warnings": 1, "justified_warned_in_time": 1,
                          "path_intrusions": {"found": 1, "expected": 1}, "unconfirmed_critical_ttc": []}}


def _job(run, family, level, seed, card, recorder=None):
    job = {"run": run, "family": family, "level": level, "seed": seed, "status": "complete", "scorecard": card}
    if recorder is not None:
        job["recorder"] = recorder
    return job


ABC = ("A", "B", "C")


class CampaignSummaries(unittest.TestCase):
    def setUp(self):
        from cdf.evaluation import scorecard
        self.sc = scorecard
        self.records = [
            _job("traces/S01/run_0_crash", "baseline", "none", 0, _card(1, 1, 2, 2, pos=0.2, recorders=ABC)),
            _job("traces/S10/run_0_x", "baseline", "none", 0, _card(2, 2, 3, 3, pos=0.3, recorders=ABC)),
            _job("traces/S01/run_0_crash", "radar_v3", "severe", 0, _card(1, 1, 1, 2, duplicates=1, phantoms=5, pos=0.6,
                                                                       recorders=ABC)),
            _job("traces/S10/run_0_x", "radar_v3", "severe", 0, _card(1, 2, 3, 3, phantoms=7, pos=0.5, recorders=ABC)),
            _job("traces/S01/run_0_crash", "radar_v3", "severe", 1, _card(1, 1, 2, 2, phantoms=3, pos=0.4, recorders=ABC)),
            _job("traces/S10/run_0_x", "radar_v3", "severe", 1, _card(2, 2, 2, 3, phantoms=1, pos=0.7, recorders=ABC)),
            _job("traces/S10/run_0_x", "radar_asym", "severe", 0, _card(2, 2, 3, 3, phantoms=2, recorders=ABC),
                 recorder="A+B"),
            {"run": "traces/S10/run_0_x", "family": "radar_asym", "level": "severe", "seed": 1, "recorder": "B+C",
             "status": "failed", "error": "boom"},
        ]

    def test_every_job_is_paired_with_the_baseline_of_its_own_run(self):
        rows = self.sc.campaign_rows(self.records)
        row = next(r for r in rows if r["run"] == "S10/run_0_x" and r["family"] == "radar_v3" and r["seed"] == 0)
        self.assertEqual((row["identified"], row["d_identified"]), (1, -1))
        self.assertEqual((row["phantoms"], row["d_phantoms"]), (7, 7))
        self.assertAlmostEqual(row["d_pos_med_m"], 0.2)
        asym = next(r for r in rows if r["family"] == "radar_asym")
        self.assertEqual((asym["recorder"], asym["degraded"], asym["recorders"]), ("A+B", 2, 3))
        failed = next(r for r in rows if r["status"] != "complete")
        self.assertEqual((failed["recorder"], failed["error"]), ("B+C", "boom"))

    def test_conditions_pool_the_runs_of_a_seed_then_average_the_seeds(self):
        table = self.sc.condition_table(self.sc.campaign_rows(self.records))
        row = next(r for r in table if r["family"] == "radar_v3")
        self.assertEqual((row["seeds"], row["jobs"], row["failed"]), (2, 4, 0))
        # seed 0: 2 of 3 contacts identified, seed 1: 3 of 3
        self.assertAlmostEqual(row["collisions_identified_rate"], (2 / 3 + 1.0) / 2, places=4)  # table rounds to 4
        # seed 0: 4 of 5 observable road users represented, seed 1: 4 of 5 (recorders are not counted)
        self.assertAlmostEqual(row["represented_rate"], 0.8)
        # counts and paired changes: mean per job within a seed (conditions with several subsets per run stay
        # comparable), then mean over seeds
        self.assertAlmostEqual(row["phantoms"], ((5 + 7) / 2 + (3 + 1) / 2) / 2)
        self.assertAlmostEqual(row["d_identified"], ((0 - 1) / 2 + 0) / 2)
        asym = [r for r in table if r["family"] == "radar_asym"]
        self.assertEqual([(r["subset"], r["jobs"], r["failed"]) for r in asym], [("all but one", 2, 1)])

    def test_conditions_are_stratified_by_the_number_of_recorders(self):
        records = self.records + [
            _job("traces/S02/run_0_crash", "baseline", "none", 0, _card(1, 1, 1, 1)),
            _job("traces/S02/run_0_crash", "radar_v3", "severe", 0, _card(1, 1, 1, 1, phantoms=4))]
        table = self.sc.condition_table(self.sc.campaign_rows(records))
        self.assertEqual(sorted((r["recorders"], r["jobs"]) for r in table if r["family"] == "radar_v3"),
                         [(2, 1), (3, 4)])

    def test_the_study_summary_writes_the_scorecard_tables(self):
        events = {"base_events": 0, "matched": 0, "extra": [], "time_deltas_s": []}
        records = [dict(r, events=events, attempt=1) for r in self.records]
        with tempfile.TemporaryDirectory() as tmp:
            rob.summarize(records, Path(tmp))
            conditions = (Path(tmp) / "campaign_v3_conditions.md").read_text(encoding="utf-8")
            jobs = (Path(tmp) / "campaign_v3_jobs.csv").read_text(encoding="utf-8").splitlines()
            table = json.loads((Path(tmp) / "campaign_v3.json").read_text(encoding="utf-8"))
        self.assertIn("| radar_v3 | severe | all | 3 | 2 | 4 | 0 |", conditions)
        self.assertEqual(len(jobs), 1 + len(records))
        self.assertIn("d_identified", jobs[0])
        self.assertEqual(len(table["jobs"]), len(records))

    def test_more_seeds_are_drawn_while_the_identified_collisions_vary(self):
        def record(seed, identified):
            return {"run": "r{0}".format(seed % 2), "family": "radar_v3", "level": "severe", "seed": seed,
                    "status": "complete", "events": {"base_events": 0, "matched": 0, "extra": [], "time_deltas_s": []},
                    "scorecard": _card(identified, 1, 1, 1)}
        stable = [record(0, 1), record(1, 1), record(2, 1)]
        varying = [record(0, 1), record(1, 0), record(2, 1)]
        self.assertFalse(rob.need_more_seeds(stable, "radar_v3", "severe"))
        self.assertTrue(rob.need_more_seeds(varying, "radar_v3", "severe"))


if __name__ == "__main__":
    unittest.main()
