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
        self.assertLessEqual(len(observations), spec.max_bins)
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


if __name__ == "__main__":
    unittest.main()
