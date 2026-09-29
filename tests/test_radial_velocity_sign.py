"""Radar stores CARLA's range rate, depth a closing speed; comparisons convert both."""

import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from scripts.evaluate_radial_oracle import evaluate
from scripts.validate_observations import radar_depth_metrics
from src.cdf.recording.compact_observations import CompactObservationWriter, closing_speed
from src.cdf.recording.vehicle_logger import VehicleLogger

MOUNT = {"x": 2.2, "y": 0.0, "z": 1.0, "yaw_deg": 0.0, "pitch_deg": 0.0}


def _approach_run(root: Path) -> Path:
    """A drives at 10 m/s towards B, parked 30 m ahead; both sensors see B's rear."""
    times = [round(0.05 * k, 2) for k in range(41)]
    states = []
    for t in times:
        for name, x, speed in (("A", 10.0 * t, 10.0), ("B", 30.0, 0.0)):
            states.append({"participant_id": name, "timestamp": t,
                           "transform": {"x": x, "y": 0.0, "z": 0.0, "roll_deg": 0.0, "pitch_deg": 0.0, "yaw_deg": 0.0},
                           "bbox_extent": {"x": 2.0, "y": 0.9, "z": 0.7},
                           "velocity": {"x": speed, "y": 0.0, "z": 0.0}})
    (root / "ground_truth").mkdir(parents=True)
    (root / "ground_truth" / "states.jsonl").write_text("".join(json.dumps(s) + "\n" for s in states), encoding="utf-8")

    vehicle = root / "vehicles" / "A"
    radar = CompactObservationWriter(vehicle / "radar" / "observations.npz", {"source": "radar", "sensor_transform": MOUNT})
    depth = CompactObservationWriter(vehicle / "depth" / "observations.npz", {"source": "depth", "sensor_transform": MOUNT})
    for frame, t in enumerate(times):
        sensor = np.array([10.0 * t + MOUNT["x"], 0.0, MOUNT["z"]])
        radar_rows, depth_rows = [], []
        for lateral in (-0.5, 0.0, 0.5):
            for height in (0.7, 0.9):
                offset = np.array([28.0, lateral, height]) - sensor  # B's rear face
                distance = float(np.linalg.norm(offset))
                range_rate = -10.0 * offset[0] / distance  # the range shrinks
                geometry = {"depth": distance, "azimuth": math.atan2(offset[1], offset[0]),
                            "altitude": math.atan2(offset[2], math.hypot(offset[0], offset[1]))}
                radar_rows.append(dict(geometry, radial_velocity=range_rate))    # CARLA native
                depth_rows.append(dict(geometry, radial_velocity=-range_rate))   # estimator convention
        radar.append(frame, t, radar_rows)
        depth.append(frame, t, depth_rows)
    radar.close()
    depth.close()
    return root


class RadialVelocitySignTests(unittest.TestCase):
    def test_closing_speed_is_positive_when_approaching_for_both_sources(self):
        np.testing.assert_allclose(closing_speed(np.array([-3.0, 2.0]), "radar"), [3.0, -2.0])
        np.testing.assert_allclose(closing_speed(np.array([3.0, -2.0]), "depth"), [3.0, -2.0])
        self.assertTrue(np.isnan(closing_speed(np.array([np.nan]), "radar"))[0])

    def test_new_recordings_label_each_stored_sign(self):
        with tempfile.TemporaryDirectory() as tmp:
            logger = VehicleLogger(Path(tmp), "A", {"radar": [{"sensor_id": "front"}]})
            logger.close()
            radar = json.loads((Path(tmp) / "vehicles" / "A" / "radar" / "metadata.json").read_text())
            depth = json.loads((Path(tmp) / "vehicles" / "A" / "depth" / "metadata.json").read_text())
        self.assertEqual((radar["radial_velocity_sign"], radar["radial_velocity_definition"]),
                         ("positive_away_from_sensor", "carla_range_rate"))
        self.assertEqual((depth["radial_velocity_sign"], depth["radial_velocity_definition"]),
                         ("positive_towards_sensor", "closing_speed"))

    def test_oracle_scores_radar_and_depth_as_closing_speed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = evaluate(_approach_run(Path(tmp)), "A", "B")
        for source in ("radar", "depth"):
            self.assertGreater(result[source]["target_frame_samples"], 30)
            self.assertEqual(result[source]["sign_agreement_percentage"], 100.0)
            self.assertLess(result[source]["mae"], 0.2)

    def test_validator_compares_radar_and_depth_as_closing_speed(self):
        with tempfile.TemporaryDirectory() as tmp:
            metrics = radar_depth_metrics(_approach_run(Path(tmp)) / "vehicles" / "A")
        self.assertGreater(metrics["matched_pairs"], 100)
        self.assertEqual(metrics["sign_agreement_percentage"], 100.0)
        self.assertLess(metrics["mae_mps"], 1e-3)
        self.assertGreater(metrics["median_radar_closing_speed_mps"], 9.0)


if __name__ == "__main__":
    unittest.main()
