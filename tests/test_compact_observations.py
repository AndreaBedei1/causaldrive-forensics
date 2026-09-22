import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.recording.compact_observations import (
    CompactObservationWriter,
    load_observations,
)


class CompactObservationTests(unittest.TestCase):
    def test_radar_and_depth_share_the_same_loader(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            radar_path = root / "radar" / "observations.npz"
            depth_path = root / "depth" / "observations.npz"
            metadata = {"schema_version": 1, "columns": ["depth_m", "azimuth_rad", "altitude_rad", "radial_velocity_mps"]}
            radar_metadata = dict(metadata)
            radar_metadata["source"] = "radar"
            radar = CompactObservationWriter(radar_path, radar_metadata)
            radar.append(10, 1.0, [{"depth": 12.5, "azimuth": 0.1, "altitude": -0.2, "radial_velocity": -3.0}])
            radar.append(11, 1.05, [])
            radar.close()
            depth_metadata = dict(metadata)
            depth_metadata.update({"source": "depth", "radial_velocity_status": "not_estimated"})
            depth = CompactObservationWriter(depth_path, depth_metadata)
            depth.append(10, 1.0, [{"depth": 12.5, "azimuth": 0.1, "altitude": -0.2, "radial_velocity": None}])
            depth.close()

            radar_loaded = load_observations(radar_path)
            depth_loaded = load_observations(depth_path)
            for observations in (radar_loaded, depth_loaded):
                self.assertEqual(observations.detections.shape[1], 4)
                self.assertEqual(observations.offsets[0], 0)
                self.assertEqual(observations.offsets[-1], len(observations.detections))
            self.assertTrue(np.isfinite(radar_loaded.detections[0, 3]))
            self.assertTrue(np.isnan(depth_loaded.detections[0, 3]))
            np.testing.assert_allclose(radar_loaded.detections[0, :3], [12.5, 0.1, -0.2], rtol=1e-6, atol=1e-6)

    def test_empty_frames_keep_offsets_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "observations.npz"
            writer = CompactObservationWriter(path, {"schema_version": 1})
            writer.append(1, 0.0, [])
            writer.close()
            loaded = load_observations(path)
            self.assertEqual(loaded.detections.shape, (0, 4))
            np.testing.assert_array_equal(loaded.offsets, [0, 0])


if __name__ == "__main__":
    unittest.main()
