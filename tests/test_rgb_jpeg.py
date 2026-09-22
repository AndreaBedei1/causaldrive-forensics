import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.cdf.recording.vehicle_logger import VehicleLogger


class RGBJpegTests(unittest.TestCase):
    def test_rgb_is_jpeg_rgb_800x600_and_metadata_matches(self):
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
            frames = list((root / "vehicles" / "A" / "camera" / "frames").glob("*"))
            self.assertEqual([frame.suffix for frame in frames], [".jpg"])
            with Image.open(frames[0]) as image:
                self.assertEqual(image.size, (800, 600))
                self.assertEqual(image.mode, "RGB")
            records = [json.loads(line) for line in (root / "vehicles" / "A" / "camera" / "metadata.jsonl").read_text().splitlines()]
            self.assertEqual(records[0]["image_filename"], frames[0].name)
            self.assertEqual(records[0]["file_format"], "jpeg")
            self.assertEqual(records[0]["jpeg_quality"], 90)
            sensor_metadata = json.loads((root / "vehicles" / "A" / "camera" / "metadata.json").read_text())
            self.assertEqual(sensor_metadata["file_format"], "jpeg")
            self.assertEqual(sensor_metadata["jpeg_quality"], 90)


if __name__ == "__main__":
    unittest.main()

