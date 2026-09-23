import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cdf.simulation.sensors import (  # noqa: E402
    DepthObservationSpec,
    decode_carla_depth,
    depth_observations_from_depth,
    unproject_pixel,
)
from cdf.recording.depth_velocity import DepthRadialVelocityEstimator  # noqa: E402


class DepthObservationTests(unittest.TestCase):
    def test_bgra_channel_order_and_extremes(self):
        black = bytes([0, 0, 0, 255])
        white = bytes([255, 255, 255, 255])
        self.assertAlmostEqual(float(decode_carla_depth(black, 1, 1)[0, 0]), 0.0)
        self.assertAlmostEqual(float(decode_carla_depth(white, 1, 1)[0, 0]), 1000.0, places=3)
        # CARLA stores B,G,R,A; this checks that red is the least significant byte.
        one_red = bytes([0, 0, 255, 255])
        self.assertAlmostEqual(float(decode_carla_depth(one_red, 1, 1)[0, 0]), 1000.0 * 255.0 / (256 ** 3 - 1))

    def test_camera_geometry_signs(self):
        x, y, z = unproject_pixel(400, 300, 10.0, 800, 600, 90.0)
        self.assertAlmostEqual(y, 0.0, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)
        self.assertGreater(unproject_pixel(500, 300, 10.0, 800, 600, 90.0)[1], 0.0)
        self.assertGreater(unproject_pixel(400, 200, 10.0, 800, 600, 90.0)[2], 0.0)
        self.assertAlmostEqual(math.sqrt(x * x + y * y + z * z), 10.0, places=6)

    def test_filtering_sparsification_and_schema(self):
        spec = DepthObservationSpec()
        depth = np.full((600, 800), 10.0, dtype=np.float32)
        observations = depth_observations_from_depth(depth, spec, 90.0)
        self.assertLessEqual(len(observations), 45)
        self.assertTrue(observations)
        for detection in observations:
            self.assertLessEqual(detection["depth"], 90.0)
            self.assertLessEqual(abs(detection["azimuth"]), math.radians(45.0))
            self.assertLessEqual(abs(detection["altitude"]), math.radians(5.0))
            self.assertIn("depth", detection)
            self.assertIn("azimuth", detection)
            self.assertIn("altitude", detection)
            self.assertIsNone(detection["radial_velocity"])

        radar_record = {"detections": [{"depth": 1.0, "azimuth": 0.0, "altitude": 0.0, "radial_velocity": 0.0}]}
        depth_record = {"detections": observations}
        for record in (radar_record, depth_record):
            for detection in record["detections"]:
                _ = (detection["depth"], detection["azimuth"], detection["altitude"], detection["radial_velocity"])

    def test_nearest_non_ground_per_azimuth(self):
        from cdf.simulation.sensors import sparsify_depth_observations
        spec = DepthObservationSpec()
        detections = [
            {"depth": 4.0, "azimuth": 0.0, "altitude": math.radians(-4), "radial_velocity": None},
            {"depth": 8.0, "azimuth": 0.0, "altitude": math.radians(1), "radial_velocity": None},
            {"depth": 20.0, "azimuth": 0.0, "altitude": math.radians(-5), "radial_velocity": None},
            {"depth": 7.0, "azimuth": math.radians(10), "altitude": 0.0, "radial_velocity": None},
        ]
        out = sparsify_depth_observations(detections, spec)
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out[0]["depth"], 4.0)
        self.assertAlmostEqual(out[1]["depth"], 7.0)

    @staticmethod
    def _one(depth, azimuth=0.0, altitude=0.0):
        return [{"depth": depth, "azimuth": math.radians(azimuth), "altitude": math.radians(altitude), "radial_velocity": None}]

    def test_temporal_velocity_sign_and_real_dt(self):
        cases = ((10.0, 9.5, 5.0), (10.0, 10.5, -5.0), (10.0, 10.0, 0.0))
        for previous, current, expected in cases:
            estimator = DepthRadialVelocityEstimator()
            self.assertIsNone(estimator.process(1, 0.0, self._one(previous))[0]["radial_velocity"])
            result = estimator.process(2, 0.1, self._one(current))[0]["radial_velocity"]
            self.assertAlmostEqual(result, expected, places=6)

    def test_missing_callback_uses_timestamp_delta(self):
        estimator = DepthRadialVelocityEstimator()
        estimator.process(1, 0.0, self._one(10.0))
        result = estimator.process(3, 0.2, self._one(9.0))[0]["radial_velocity"]
        self.assertAlmostEqual(result, 5.0, places=6)

    def test_first_frame_and_angular_drift(self):
        estimator = DepthRadialVelocityEstimator()
        first = estimator.process(1, 0.0, self._one(10.0, 0.0))[0]
        self.assertIsNone(first["radial_velocity"])
        current = estimator.process(2, 0.1, self._one(9.5, 2.0))[0]
        self.assertAlmostEqual(current["radial_velocity"], 5.0, places=6)

    def test_angular_mismatch_and_impossible_jump_are_nan(self):
        estimator = DepthRadialVelocityEstimator()
        estimator.process(1, 0.0, self._one(10.0, 0.0))
        mismatch = estimator.process(2, 0.1, self._one(9.5, 8.0))[0]
        self.assertIsNone(mismatch["radial_velocity"])
        estimator = DepthRadialVelocityEstimator()
        estimator.process(1, 0.0, self._one(10.0))
        impossible = estimator.process(2, 0.1, self._one(0.0))[0]
        self.assertIsNone(impossible["radial_velocity"])

    def test_ambiguous_match_is_rejected(self):
        estimator = DepthRadialVelocityEstimator()
        estimator.process(1, 0.0, self._one(10.0, -1.0) + self._one(10.0, 1.0))
        current = estimator.process(2, 0.1, self._one(9.5, 0.0))[0]
        self.assertIsNone(current["radial_velocity"])

    def test_out_of_order_timestamp_does_not_rewind_state(self):
        estimator = DepthRadialVelocityEstimator()
        estimator.process(1, 1.0, self._one(10.0))
        self.assertIsNone(estimator.process(0, 0.9, self._one(9.5))[0]["radial_velocity"])
        result = estimator.process(2, 1.1, self._one(9.5))[0]["radial_velocity"]
        self.assertAlmostEqual(result, 5.0, places=6)


if __name__ == "__main__":
    unittest.main()
