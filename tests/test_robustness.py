"""Robustness study: the perturbations do what their profiles say, never touch a recording, and the
reconstruction stays put where it should (clock offsets) or degrades as expected; the mutual refinement
recovers relative pose offsets."""

import dataclasses
import json
import math
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.reconstruction.anonymous import face_depths, scan_relative_offset
from src.cdf.reconstruction.common_frame import (DEFAULT_BODY, CommonSample, PoseSource, RecordedPoseSource, RecorderBody,
                                                 WorldPose)
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.robustness.perturb import (GNSS_PROFILES, RADAR_PROFILES, CollisionPerturbation, GnssProfile, Perturbation,
                                        PerturbedPoseSource, RadarProfile, _error_series, perturb_sweeps, perturbed_copy,
                                        stream_seed)
from src.cdf.evaluation.run_metrics import core_event_diff, graph_signature

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"
S01 = ROOT / "traces" / "S01" / "run_0_crash"


def _sweeps(n_sweeps=400, per_sweep=200, seed=0):
    rng = np.random.default_rng(seed)
    detections = np.column_stack([rng.uniform(5, 50, n_sweeps * per_sweep), rng.uniform(-1, 1, n_sweeps * per_sweep),
                                  rng.uniform(-0.1, 0.1, n_sweeps * per_sweep), rng.uniform(-5, 5, n_sweeps * per_sweep)])
    offsets = np.arange(0, n_sweeps * per_sweep + 1, per_sweep)
    return (np.arange(n_sweeps), 10.0 + 0.05 * np.arange(n_sweeps), offsets, detections.astype(np.float32))


META = {"horizontal_fov_deg": 150.0, "vertical_fov_deg": 20.0, "range_m": 90.0,
        "sensor_transform": {"x": 2.0, "y": 0.0, "z": 0.6, "yaw_deg": 0.0, "pitch_deg": 0.0}}


class RadarPerturbationTests(unittest.TestCase):
    def test_noise_drop_and_clutter_follow_the_profile(self):
        frames, times, offsets, detections = _sweeps()
        profile = RadarProfile("test", sigma_range_m=0.25, sigma_azimuth_deg=0.5, sigma_velocity_mps=0.1, p_drop=0.2,
                               clutter_per_sweep=0.0)
        rng = np.random.default_rng(1)
        _, _, new_offsets, new = perturb_sweeps(frames, times, offsets, detections, META, profile, rng, lambda t: 10.0)
        self.assertAlmostEqual(1.0 - len(new) / len(detections), 0.2, delta=0.01)
        # With the drop, rows are no longer aligned: re-run without drop to measure the noise.
        _, _, _, noisy = perturb_sweeps(frames, times, offsets, detections, META,
                                        dataclasses.replace(profile, p_drop=0.0), np.random.default_rng(2), lambda t: 10.0)
        error = noisy.astype(float) - detections.astype(float)
        self.assertAlmostEqual(float(np.std(error[:, 0])), 0.25, delta=0.01)
        self.assertAlmostEqual(float(np.std(error[:, 1])), math.radians(0.5), delta=math.radians(0.02))
        self.assertAlmostEqual(float(np.std(error[:, 3])), 0.1, delta=0.005)
        self.assertEqual(float(np.std(error[:, 2])), 0.0)  # elevation noise not asked for

    def test_clutter_is_poisson_in_the_field_of_view_with_static_or_mirrored_doppler(self):
        frames, times, offsets, detections = _sweeps(n_sweeps=600, per_sweep=20)
        profile = RadarProfile("clutter", clutter_per_sweep=3.0)
        _, _, new_offsets, new = perturb_sweeps(frames, times, offsets, detections, META, profile,
                                                np.random.default_rng(3), lambda t: 12.0)
        extra = np.diff(new_offsets) - np.diff(offsets)
        self.assertAlmostEqual(float(np.mean(extra)), 3.0, delta=0.2)
        self.assertAlmostEqual(float(np.var(extra)), 3.0, delta=0.5)  # Poisson: variance = mean
        clutter = np.vstack([new[new_offsets[i] + 20:new_offsets[i + 1]] for i in range(len(frames))])
        self.assertTrue(np.all(np.abs(clutter[:, 1]) <= math.radians(75.0) + 1e-6))
        self.assertTrue(np.all((clutter[:, 0] >= 1.0) & (clutter[:, 0] <= 90.0)))
        static = -12.0 * np.cos(clutter[:, 2]) * np.cos(clutter[:, 1])  # forward radar, static world
        share_static = float(np.mean(np.abs(clutter[:, 3] - static) < 1e-3))
        self.assertAlmostEqual(share_static, 0.5, delta=0.06)

    def test_profiles_are_ordered_and_ideal_changes_nothing(self):
        frames, times, offsets, detections = _sweeps(n_sweeps=5, per_sweep=10)
        out = perturb_sweeps(frames, times, offsets, detections, META, RADAR_PROFILES["ideal"],
                             np.random.default_rng(0), lambda t: 0.0)
        np.testing.assert_array_equal(out[3], detections)
        keys = ("sigma_range_m", "sigma_azimuth_deg", "sigma_velocity_mps", "p_drop", "clutter_per_sweep")
        for key in keys:
            values = [getattr(RADAR_PROFILES[name], key) for name in ("ideal", "low", "nominal", "high")]
            self.assertEqual(values, sorted(values), key)


class GnssTests(unittest.TestCase):
    def test_error_components_have_the_stated_spread(self):
        times = np.arange(0.0, 20.0, 0.05)
        bias, markov, white = [], [], []
        for k in range(300):
            series = _error_series(times, 1.5, 0.0, 60.0, 0.0, 1.0, np.random.default_rng(k))
            bias.append(series[0])
            self.assertTrue(np.allclose(series, series[0]))  # a bias is constant over the run
        self.assertAlmostEqual(float(np.std(bias)), 1.5, delta=0.15)
        for k in range(300):
            markov.append(_error_series(times, 0.0, 0.7, 60.0, 0.0, 1.0, np.random.default_rng(1000 + k))[0])
        self.assertAlmostEqual(float(np.std(markov)), 0.7, delta=0.08)
        series = _error_series(np.arange(0.0, 2000.0, 1.0), 0.0, 0.0, 60.0, 0.5, 1.0, np.random.default_rng(7))
        self.assertAlmostEqual(float(np.std(series)), 0.5, delta=0.03)

    def test_a_perturbed_pose_source_declares_its_profile_and_is_reproducible(self):
        a = PerturbedPoseSource.factory(GNSS_PROFILES["consumer"], 3)(S17 / "vehicles" / "A", 14.307498775422573)
        b = PerturbedPoseSource.factory(GNSS_PROFILES["consumer"], 3)(S17 / "vehicles" / "A", 14.307498775422573)
        c = PerturbedPoseSource.factory(GNSS_PROFILES["consumer"], 4)(S17 / "vehicles" / "A", 14.307498775422573)
        exact = RecordedPoseSource.from_vehicle_dir(S17 / "vehicles" / "A", 14.307498775422573)
        self.assertAlmostEqual(a.position_std_m, math.sqrt(1.5 ** 2 + 0.7 ** 2 + 0.05 ** 2))
        self.assertEqual(a.pose_at(2.0), b.pose_at(2.0))
        self.assertNotEqual(a.pose_at(2.0), c.pose_at(2.0))
        error = math.hypot(a.pose_at(2.0).x - exact.pose_at(2.0).x, a.pose_at(2.0).y - exact.pose_at(2.0).y)
        self.assertGreater(error, 0.0)
        ideal = PerturbedPoseSource.factory(GNSS_PROFILES["ideal"], 3)(S17 / "vehicles" / "A", 14.307498775422573)
        self.assertEqual(ideal.pose_at(2.0), exact.pose_at(2.0))

    def test_streams_are_independent_of_order(self):
        self.assertEqual(stream_seed(1, "radar", "A", "front"), stream_seed(1, "radar", "A", "front"))
        self.assertNotEqual(stream_seed(1, "radar", "A", "front"), stream_seed(1, "radar", "A", "left"))


class CopyTests(unittest.TestCase):
    def test_the_copy_links_what_it_does_not_change_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = perturbed_copy(S17, Path(tmp) / "S17" / "run_0_crash",
                                    Perturbation("radar", radar=RADAR_PROFILES["nominal"]), 0)
            ego, original = target / "vehicles" / "A" / "ego.jsonl", S17 / "vehicles" / "A" / "ego.jsonl"
            self.assertTrue(os.path.samefile(ego, original) or ego.read_bytes() == original.read_bytes())
            self.assertFalse(os.path.samefile(target / "vehicles" / "A" / "radar" / "front" / "observations.npz",
                                              S17 / "vehicles" / "A" / "radar" / "front" / "observations.npz"))
            self.assertFalse((target / "reconstruction").exists())
            record = json.loads((target / "perturbation.json").read_text())
            self.assertEqual(record["perturbation"]["radar"]["name"], "nominal")
            with self.assertRaises(FileExistsError):
                perturbed_copy(S17, target, Perturbation("again"), 0)

    def test_clock_offsets_downsampling_dropout_and_collision_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = perturbed_copy(S17, Path(tmp) / "a", Perturbation(
                "mixed", clock_offsets_s=(("B", 12.5),), downsample=2, drop_recorders=("A",),
                collisions=CollisionPerturbation(latency_s=0.25, latency_recorders=("B",))), 0)
            self.assertFalse((copy / "vehicles" / "A").exists())
            rows = [json.loads(l) for l in (S17 / "vehicles" / "B" / "ego.jsonl").read_text().splitlines()]
            new = [json.loads(l) for l in (copy / "vehicles" / "B" / "ego.jsonl").read_text().splitlines()]
            self.assertEqual(len(new), (len(rows) + 1) // 2)
            self.assertAlmostEqual(new[1]["timestamp"] - rows[2]["timestamp"], 12.5, places=6)
            hits = [json.loads(l) for l in (S17 / "vehicles" / "B" / "collisions.jsonl").read_text().splitlines()]
            moved = [json.loads(l) for l in (copy / "vehicles" / "B" / "collisions.jsonl").read_text().splitlines()]
            self.assertAlmostEqual(moved[0]["timestamp"] - hits[0]["timestamp"], 12.75, places=6)
            with np.load(str(S17 / "vehicles" / "B" / "radar" / "front" / "observations.npz")) as a, \
                    np.load(str(copy / "vehicles" / "B" / "radar" / "front" / "observations.npz")) as b:
                self.assertEqual(len(b["frames"]), (len(a["frames"]) + 1) // 2)
                self.assertAlmostEqual(float(b["timestamps"][1] - a["timestamps"][2]), 12.5, places=6)
            self.assertTrue((copy / "ground_truth" / "states.jsonl").exists())


class ReconstructionUnderPerturbationTests(unittest.TestCase):
    def test_clock_offsets_move_every_time_a_recorder_wrote(self):
        run = ROOT / "traces" / "S10" / "run_0_rolls_through"  # A records a STOP sign
        with tempfile.TemporaryDirectory() as tmp:
            copy = perturbed_copy(run, Path(tmp) / "c", Perturbation("clock", clock_offsets_s=(("A", 7.31),)), 0)
            before = [json.loads(l) for l in (run / "vehicles" / "A" / "traffic_signs.jsonl").read_text().splitlines() if l]
            after = [json.loads(l) for l in (copy / "vehicles" / "A" / "traffic_signs.jsonl").read_text().splitlines() if l]
        self.assertTrue(before)
        for a, b in zip(before, after):
            for key in ("timestamp_first", "timestamp_confirmed", "timestamp_last"):
                self.assertAlmostEqual(b[key] - a[key], 7.31, places=6)
            self.assertEqual(a["frame_first"], b["frame_first"])  # frame numbers are not times

    def test_constant_clock_offsets_leave_the_global_graph_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = perturbed_copy(S17, Path(tmp) / "S17" / "run_0_crash",
                                  Perturbation("clock", clock_offsets_s=(("A", 7.31), ("B", -14.62))), 0)
            reconstruct_run(copy, ReconstructionConfig())
            new = json.loads((copy / "reconstruction" / "global" / "global_graph.json").read_text())
        base = json.loads((S17 / "reconstruction" / "global" / "global_graph.json").read_text())
        self.assertEqual(graph_signature(new), graph_signature(base))
        self.assertTrue(core_event_diff(base, new)["identical"])


def _refined(run, bias_m, seed):
    """The run reconstructed with a pure position bias on every pose source and the mutual refinement on:
    (refinement record, true bias of each source)."""
    cfg = ReconstructionConfig()
    refined = dataclasses.replace(cfg, fusion=dataclasses.replace(cfg.fusion, mutual_refinement=True))
    factory = PerturbedPoseSource.factory(GnssProfile("bias_only", bias_m=bias_m), seed)
    with tempfile.TemporaryDirectory() as tmp:
        copy = perturbed_copy(run, Path(tmp) / run.parent.name / run.name, Perturbation("gnss"), 0)
        result = reconstruct_run(copy, refined, pose_factory=factory)
        biased = {l.owner: factory(copy / "vehicles" / l.owner, l.clock_origin) for l in result.locals}
    exact = {l.owner: RecordedPoseSource.from_vehicle_dir(run / "vehicles" / l.owner, l.clock_origin) for l in result.locals}
    bias = {r: np.array([biased[r].x[0] - exact[r].x[0], biased[r].y[0] - exact[r].y[0]]) for r in biased}
    return result.road_users.refinement, bias


def _relative(refinement, bias, a, b):
    """(relative bias of b against a before, after the correction, posterior covariance of the correction)."""
    before = bias[b] - bias[a]
    after = (bias[b] + refinement["offsets_m"][b]) - (bias[a] + refinement["offsets_m"][a])
    names, P = refinement["unknowns"], np.array(refinement["covariance_m2"])
    i, j = 2 * names.index(a), 2 * names.index(b)
    return before, after, P[i:i + 2, i:i + 2] + P[j:j + 2, j:j + 2] - P[i:i + 2, j:j + 2] - P[j:j + 2, i:i + 2]


class MutualRefinementTests(unittest.TestCase):
    def test_recovers_the_relative_offset_when_both_directions_are_seen(self):
        refinement, bias = _refined(S17, 2.0, 5)  # S17: B is seen from behind and alongside
        before, after, covariance = _relative(refinement, bias, "A", "B")
        self.assertGreater(float(np.hypot(*before)), 2.0)
        self.assertLess(float(np.hypot(*after)), 0.35)
        self.assertLess(float(after @ np.linalg.solve(covariance, after)), 13.8)  # chi-square 2 dof, 99.9 %
        self.assertTrue(all(value <= 2.0 + 1e-9 for value in refinement["declared_position_std_m"].values()))

    def test_leaves_alone_what_no_face_constrains(self):
        refinement, bias = _refined(S01, 2.0, 5)  # S01: A only ever sees B's rear (the lateral is unobservable)
        before, after, covariance = _relative(refinement, bias, "A", "B")
        values, vectors = np.linalg.eigh(covariance)
        seen, unseen = vectors[:, 0], vectors[:, 1]
        self.assertGreater(abs(float(before @ seen)), 2.0)
        self.assertLess(abs(float(after @ seen)), 0.5)
        self.assertLess(abs(float((after - before) @ unseen)), 0.1)
        self.assertGreater(math.sqrt(values[1]), 0.9 * 2.0 * math.sqrt(2.0))  # the prior: nothing learnt
        self.assertEqual(refinement["declared_position_std_m"], {"A": 2.0, "B": 2.0})

    def test_exact_pose_sources_are_not_refined(self):
        cfg = ReconstructionConfig()
        refined = dataclasses.replace(cfg, fusion=dataclasses.replace(cfg.fusion, mutual_refinement=True))
        with tempfile.TemporaryDirectory() as tmp:
            copy = perturbed_copy(S17, Path(tmp) / "S17" / "run_0_crash", Perturbation("none"), 0)
            result = reconstruct_run(copy, refined)
            new = json.loads((copy / "reconstruction" / "global" / "global_graph.json").read_text())
        self.assertFalse(result.road_users.refinement["applied"])
        base = json.loads((S17 / "reconstruction" / "global" / "global_graph.json").read_text())
        self.assertEqual(graph_signature(new), graph_signature(base))


class _StaticPose(PoseSource):
    name = "static"

    def __init__(self, x, y, yaw):
        self.pose = WorldPose(x, y, yaw)

    def pose_at(self, t_local):
        return self.pose

    @property
    def start(self):
        return 0.0

    @property
    def end(self):
        return 100.0


def _sample(t, points, origin):
    points = np.asarray(points, float)
    return CommonSample(t, t, points.mean(axis=0), points[0], np.zeros(2), 0.1, 0.1, np.asarray(origin, float), True,
                        returns=points, origins=np.repeat(np.asarray(origin, float)[None, :], len(points), axis=0))


class FaceGeometryTests(unittest.TestCase):
    """A recorder's box at (10, 5) heading 30 degrees; an observer's returns on its surface, moved by a
    known position error of the observer relative to it."""

    def setUp(self):
        self.pose = WorldPose(10.0, 5.0, math.radians(30.0))
        self.body = RecorderBody("R", _StaticPose(10.0, 5.0, math.radians(30.0)), DEFAULT_BODY, 0.0)
        fp = DEFAULT_BODY
        self.rear = [(fp.x_min, y) for y in np.linspace(-0.8, 0.8, 9)]
        self.right = [(x, fp.y_max) for x in np.linspace(-2.0, 1.6, 10)]

    def world(self, local_points, shift):
        return np.array([self.pose.to_world(x, y) for x, y in local_points]) + np.asarray(shift)

    def test_depths_are_the_shift_along_each_seen_face(self):
        shift = np.array([0.4, -0.3])  # b_observer - b_recorder
        origin = self.pose.to_world(-12.0, 6.0)  # behind and to the right: rear and right faces seen
        faces = {name: (normal, depth, count) for name, normal, depth, count in
                 face_depths(self.body, _sample(1.0, self.world(self.rear + self.right, shift), origin))}
        self.assertEqual(set(faces), {"rear", "right"})
        for name, (normal, depth, count) in faces.items():
            self.assertAlmostEqual(depth, float(normal @ -shift), places=6)
        self.assertEqual(faces["rear"][2], 9)
        self.assertEqual(faces["right"][2], 10)

    def test_a_face_the_radar_cannot_see_gets_nothing(self):
        origin = self.pose.to_world(-12.0, 0.0)  # straight behind: only the rear face
        faces = face_depths(self.body, _sample(1.0, self.world(self.rear, [0.0, 2.5]), origin))
        self.assertEqual([face[0] for face in faces], ["rear"])
        inside = self.pose.to_world(-1.0, 0.0)  # a radar inside the box (bodies in contact) sees nothing
        self.assertEqual(face_depths(self.body, _sample(1.0, self.world(self.rear, [0.0, 0.0]), inside)), [])

    def test_the_scan_finds_large_offsets(self):
        shift = np.array([-3.1, 2.2])
        origin = self.pose.to_world(-12.0, 6.0)
        samples = [_sample(t, self.world(self.rear + self.right, shift), origin) for t in np.arange(0.0, 3.0, 0.1)]
        found = scan_relative_offset(self.body, samples, spread_m=2.0 * math.sqrt(2.0))
        np.testing.assert_allclose(found, -shift, atol=0.05)  # b_R - b_O


if __name__ == "__main__":
    unittest.main()
