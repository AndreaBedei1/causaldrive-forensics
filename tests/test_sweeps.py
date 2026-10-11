"""Scenario sweeps (scripts/run_sweep.py): deterministic sampling, variants, run bookkeeping, outcomes;
and the alignment pieces sweeps rely on: line-of-sight entry distances and the reference recorder of a
run without a matched collision."""

import importlib.util
import json
import math
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.evaluation.reconstruction import evaluate_run
from src.cdf.reconstruction.common_frame import RecordedPoseSource, entry_distances
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import EgoFootprint

ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "traces"


def _runner():
    spec = importlib.util.spec_from_file_location("run_sweep", str(ROOT / "scripts" / "run_sweep.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SWEEP = _runner()


class SamplingTests(unittest.TestCase):
    def test_halton_points_are_deterministic_and_every_prefix_covers_the_range(self):
        a = [SWEEP.halton_point(k, 3, 101) for k in range(40)]
        self.assertEqual(a, [SWEEP.halton_point(k, 3, 101) for k in range(40)])
        for n in (5, 10, 40):
            for j in range(3):
                values = sorted(point[j] for point in a[:n])
                # Low discrepancy: the largest empty interval shrinks like 1/n (random sampling: log n / n).
                gaps = np.diff([0.0] + values + [1.0])
                self.assertLess(max(gaps), 3.0 / n + 1e-9, (n, j))
        self.assertNotEqual(SWEEP.halton_point(0, 3, 101), SWEEP.halton_point(0, 3, 202))

    def test_seeds_of_different_sweeps_shift_every_dimension_differently(self):
        for j in range(4):
            self.assertNotAlmostEqual(SWEEP.seed_shift(505, j), SWEEP.seed_shift(606, j))

    def test_parameters_respect_ranges_decimals_also_and_relative_to(self):
        sweep = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "rear_end.yaml")
        for k in range(10):
            values = SWEEP.sample_parameters(sweep, k)
            self.assertEqual(values, SWEEP.sample_parameters(sweep, k))
            speed = values["participants.A.initial_speed"]
            self.assertTrue(11.0 <= speed <= 16.0)
            self.assertEqual(round(speed, 1), speed)
            for other in ("participants.A.target_speed", "participants.B.initial_speed", "participants.B.target_speed"):
                self.assertEqual(values[other], speed)
            self.assertTrue(4.2 <= values["participants.A.actions.A_late_brake.t_start"] <= 6.2)
        adjacent = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "anonymous_pair_adjacent.yaml")
        for k in range(10):
            d = SWEEP.sample_parameters(adjacent, k)["participants.D.spawn.forward_m"]
            self.assertTrue(40.0 - 6.0 <= d <= 40.0 + 6.0)  # relative to C's forward_m (40) in the base variant

    def test_a_variant_overrides_only_the_sampled_values_and_keeps_every_action(self):
        sweep = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "cut_in.yaml")
        values = SWEEP.sample_parameters(sweep, 3)
        body = SWEEP.sweep_variant(sweep, values)
        b = body["participant_overrides"]["B"]
        self.assertEqual([a["action_id"] for a in b["actions"]], ["B_cut_in", "B_slow_after_cut_in"])
        cut_in = next(a for a in b["actions"] if a["action_id"] == "B_cut_in")
        self.assertEqual(cut_in["t_start"], values["participants.B.actions.B_cut_in.t_start"])
        self.assertEqual(cut_in["params"]["lateral_m"], 3.5)  # untouched
        self.assertEqual(b["spawn"], {"forward_m": values["participants.B.spawn.forward_m"]})
        a = body["participant_overrides"]["A"]
        self.assertEqual(a["actions"][0]["t_start"], values["participants.A.actions.A_late_brake.t_start"])
        self.assertEqual(a["actions"][0]["params"]["intensity"], 0.85)
        # The base variant's own overrides survive (S18 platoon moves C and D).
        platoon = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "anonymous_pair_platoon.yaml")
        body = SWEEP.sweep_variant(platoon, SWEEP.sample_parameters(platoon, 0))
        self.assertEqual(body["participant_overrides"]["C"]["spawn"]["forward_m"], 46.0)
        self.assertEqual(body["participant_overrides"]["D"]["spawn"]["lane_offset"], 0)

    def test_the_variant_builds_a_valid_scenario(self):
        from src.cdf.common.config import load_run_config
        from src.cdf.simulation.scenario_base import ScenarioSpec
        sweep = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "unobserved_cut_in.yaml")
        values = SWEEP.sample_parameters(sweep, 2)
        variant, _ = SWEEP.run_paths(Path("out"), sweep, 2)
        cfg = load_run_config("S17", overrides=["scenario.variants.{0}={1}".format(
            variant, json.dumps(SWEEP.sweep_variant(sweep, values)))])
        spec = ScenarioSpec.from_config(cfg, variant=variant)
        c = next(p for p in spec.participants if p.participant_id == "C")
        self.assertEqual((c.spawn.forward_m, c.initial_speed), (values["participants.C.spawn.forward_m"],
                                                                 values["participants.C.initial_speed"]))
        self.assertEqual(next(a for a in c.actions if a.action_id == "C_cut_in_left").t_start,
                         values["participants.C.actions.C_cut_in_left.t_start"])


class BookkeepingTests(unittest.TestCase):
    def test_runs_are_named_by_index_and_never_go_into_the_campaign(self):
        sweep = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "rear_end.yaml")
        variant, path = SWEEP.run_paths(Path("sweeps"), sweep, 7)
        self.assertEqual((variant, path.as_posix()), ("rear_end_007", "sweeps/rear_end/S01/run_7_rear_end_007"))
        with self.assertRaises(SystemExit):
            SWEEP.main([str(ROOT / "configs" / "sweeps" / "rear_end.yaml"), "--out", str(TRACES)])

    def test_an_incomplete_run_is_set_aside_never_deleted_and_a_complete_one_is_kept(self):
        sweep = SWEEP.load_sweep(ROOT / "configs" / "sweeps" / "rear_end.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            _, run = SWEEP.run_paths(Path(tmp), sweep, 0)
            (run / "vehicles").mkdir(parents=True)
            (run / "vehicles" / "partial.txt").write_text("x", encoding="utf-8")
            self.assertFalse(SWEEP.complete(run))
            moved = SWEEP.set_aside(Path(tmp), sweep, run)
            self.assertFalse(run.exists())
            self.assertTrue((moved / "vehicles" / "partial.txt").exists())
            self.assertEqual(moved.parent.name, "_failed")
            run.mkdir(parents=True)
            (run / "sweep_manifest.json").write_text(json.dumps({"status": "complete"}), encoding="utf-8")
            self.assertTrue(SWEEP.complete(run))

    def test_outcomes_from_ground_truth(self):
        crash = SWEEP.classify_outcome(TRACES / "S17" / "run_0_crash")
        self.assertEqual((crash["outcome"], crash["contacts"]), ("crash", ["A-B"]))
        self.assertLess(crash["min_gap_m"], 0.1)


class EntryDistanceTests(unittest.TestCase):
    def setUp(self):
        rows = [{"timestamp": t, "x": 0.0, "y": 0.0, "yaw_deg": 0.0, "velocity": {"x": 0.0, "y": 0.0}} for t in (0.0, 1.0)]
        self.poses = RecordedPoseSource(rows, 0.0)
        self.body = EgoFootprint(-2.3, 2.3, -0.95, 0.95)

    def test_a_near_surface_where_the_line_of_sight_enters_the_body_is_on_it(self):
        observer = np.array([[-20.0, 0.0]])
        d, valid = entry_distances(self.poses, self.body, [0.5], np.array([[-2.3, 0.2]]), observer)
        self.assertTrue(valid[0])
        self.assertAlmostEqual(float(d[0]), 0.0, places=6)

    def test_a_point_the_body_would_hide_is_off_by_its_depth(self):
        observer = np.array([[-20.0, 0.0]])
        # Inside the body near its far (front) face: an outline measure would call it 0.3 m off.
        d, _ = entry_distances(self.poses, self.body, [0.5], np.array([[2.0, 0.0]]), observer)
        self.assertAlmostEqual(float(d[0]), 4.3, places=6)

    def test_a_ray_that_misses_the_body_gives_the_distance_to_it(self):
        observer = np.array([[-20.0, 5.0]])
        d, _ = entry_distances(self.poses, self.body, [0.5], np.array([[0.0, 3.0]]), observer)
        self.assertAlmostEqual(float(d[0]), 3.0 - 0.95, places=6)
        _, valid = entry_distances(self.poses, self.body, [2.0], np.array([[0.0, 3.0]]), observer)
        self.assertFalse(valid[0])  # outside the pose stream


class ReferenceRecorderTests(unittest.TestCase):
    def test_without_a_matched_collision_the_first_recorder_defines_the_clock(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "S01" / "run_0_crash"
            shutil.copytree(TRACES / "S01" / "run_0_crash" / "vehicles", run / "vehicles")
            shutil.copy(TRACES / "S01" / "run_0_crash" / "incident_context.json", run / "incident_context.json")
            for recorder in ("A", "B"):  # a near miss: nobody reported a collision
                (run / "vehicles" / recorder / "collisions.jsonl").write_text("", encoding="utf-8")
            result = reconstruct_run(run, ReconstructionConfig())
            record = json.loads((run / "reconstruction" / "global" / "anonymous_entities.json").read_text())
        clocks = result.alignment.graphs
        self.assertEqual((clocks["A"].status, clocks["A"].offset_to_global, clocks["A"].method),
                         ("ALIGNED", 0.0, "reference_recorder"))
        # B is aligned to A by A's radar view of it: both clocks started together (true offset 0).
        self.assertEqual((clocks["B"].status, clocks["B"].method), ("ALIGNED", "observed_trajectories"))
        self.assertLessEqual(abs(clocks["B"].offset_to_global), 0.051)
        self.assertEqual([d["method"] for d in record["observed_alignment"]],
                         ["reference_recorder", "observed_trajectories"])
        names = {(a.local_graph, a.local_track): (a.status, a.global_entity) for a in result.associations}
        self.assertEqual(names[("A", "track_001")], ("ASSOCIATED", "B"))  # linked in the common frame

    def test_a_near_miss_is_evaluated_on_the_reference_recorder_clock(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "S01" / "run_0_crash"
            for part in ("vehicles", "ground_truth"):
                shutil.copytree(TRACES / "S01" / "run_0_crash" / part, run / part)
            for part in ("incident_context.json", "metadata.json"):
                shutil.copy(TRACES / "S01" / "run_0_crash" / part, run / part)
            for recorder in ("A", "B"):
                (run / "vehicles" / recorder / "collisions.jsonl").write_text("", encoding="utf-8")
            reconstruct_run(run, ReconstructionConfig())
            result = evaluate_run(run, clock_shift_check=False)
        # The true t_global is A's own clock: event times are off by B's alignment error at most.
        self.assertGreater(result["event_timing"]["nodes"], 10)
        self.assertLessEqual(result["event_timing"]["max_abs_error_s"], 0.051)
        self.assertEqual(result["event_timing"]["order_concordant"], result["event_timing"]["order_pairs"])
        errors = {row["graph"]: row["error_s"] for row in result["alignment"]}
        self.assertEqual(errors["A"], 0.0)
        self.assertLessEqual(abs(errors["B"]), 0.051)


if __name__ == "__main__":
    unittest.main()
