import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.recording.vehicle_logger import VehicleLogger


class RGBJpegTests(unittest.TestCase):
    def test_rgb_is_processed_transiently_and_no_image_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logger = VehicleLogger(root, "A", {
                "participant_id": "A",
                "camera": {
                    "sensor_id": "front_rgb", "width": 800, "height": 600,
                    "fov_deg": 90.0, "sensor_tick_s": 0.25,
                },
                "depth_camera": {"sensor_id": "front_depth", "sensor_tick_s": 0.05, "fov_deg": 90.0},
                "depth_observations": {},
                "radar": [],
            })
            bgra = bytes([10, 20, 30, 255]) * (800 * 600)
            logger.log_camera({"frame": 7, "timestamp": 1.25, "width": 800, "height": 600}, bgra)
            logger.close()
            self.assertFalse((root / "vehicles" / "A" / "camera" / "frames").exists())
            self.assertFalse(list((root / "vehicles" / "A").rglob("*.jpg")))
            self.assertFalse((root / "vehicles" / "A" / "camera" / "metadata.jsonl").exists())
            sensor_metadata = json.loads((root / "vehicles" / "A" / "camera" / "metadata.json").read_text())
            self.assertFalse(sensor_metadata["images_persisted"])
            signs = (root / "vehicles" / "A" / "traffic_signs.jsonl").read_text()
            self.assertEqual(signs, "")


if __name__ == "__main__":
    unittest.main()
