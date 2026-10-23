"""Diagnostic of the fused road users' errors by motion regime (scripts/tracking_regimes.py)."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _script(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tr = _script("tracking_regimes")


def _state(vx=10.0, vy=0.0, ax=0.0, ay=0.0, yaw_rate=0.0):
    return {"velocity": {"x": vx, "y": vy}, "acceleration": {"x": ax, "y": ay},
            "angular_velocity": {"z": yaw_rate}}


class Regimes(unittest.TestCase):
    def test_steady_cruise_seen_by_one_recorder(self):
        self.assertEqual(tr.regimes(_state(), 5.0, None, 1), ["steady", "one recorder"])

    def test_braking_is_a_deceleration_along_the_velocity(self):
        self.assertEqual(tr.regimes(_state(ax=-3.0), 5.0, None, 1), ["braking", "one recorder"])
        # accelerating backwards along a backward velocity is accelerating, not braking
        self.assertEqual(tr.regimes(_state(vx=-10.0, ax=-3.0), 5.0, None, 1), ["steady", "one recorder"])

    def test_turning_and_several_recorders(self):
        self.assertEqual(tr.regimes(_state(yaw_rate=-8.0), 5.0, None, 2), ["turning", "several recorders"])

    def test_after_the_vehicle_s_first_contact(self):
        self.assertEqual(tr.regimes(_state(ax=-9.0), 5.5, 5.0, 1), ["after contact (0-3 s)", "one recorder"])
        self.assertEqual(tr.regimes(_state(), 9.0, 5.0, 1), ["after contact (> 3 s)", "one recorder"])
        self.assertEqual(tr.regimes(_state(ax=-3.0), 4.0, 5.0, 1), ["braking", "one recorder"])

    def test_statistics_of_a_regime(self):
        stats = tr.error_stats([0.1, 0.2, 0.3, 0.4, 1.0])
        self.assertEqual(stats["n"], 5)
        self.assertAlmostEqual(stats["median"], 0.3)
        self.assertAlmostEqual(stats["rmse"], (sum(v * v for v in (0.1, 0.2, 0.3, 0.4, 1.0)) / 5) ** 0.5, places=4)


def _box(x=10.0, y=0.0, yaw=0.0):
    return {"transform": {"x": x, "y": y, "yaw_deg": yaw}, "bbox_extent": {"x": 2.0, "y": 1.0}}


class PointToBody(unittest.TestCase):
    def test_a_point_on_or_inside_the_body_is_at_zero(self):
        self.assertEqual(tr.point_body_distance(11.0, 0.5, _box()), 0.0)
        self.assertEqual(tr.point_body_distance(12.0, 1.0, _box()), 0.0)

    def test_outside_the_body_the_distance_to_its_outline(self):
        self.assertAlmostEqual(tr.point_body_distance(13.0, 0.0, _box()), 1.0)
        self.assertAlmostEqual(tr.point_body_distance(10.0, -3.0, _box()), 2.0)
        self.assertAlmostEqual(tr.point_body_distance(10.0, 3.0, _box(yaw=90.0)), 1.0)


class RecorderTracks(unittest.TestCase):
    def test_radar_tracks_of_recorders_follow_them_through_the_contact(self):
        samples = tr.recorder_track_samples(ROOT / "traces" / "S01" / "run_0_crash")
        labels = {label for s in samples for label in s["labels"]}
        self.assertIn("after contact (0-3 s)", labels)
        self.assertTrue(all(s["body_distance_m"] >= 0.0 for s in samples))
        self.assertTrue(all("one recorder" not in s["labels"] for s in samples))


if __name__ == "__main__":
    unittest.main()
