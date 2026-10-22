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


if __name__ == "__main__":
    unittest.main()
