"""Anonymous radar tracks and the Kalman + RTS smoother."""

import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.recording.compact_observations import load_radar_observations
from src.cdf.reconstruction.config import TrackingConfig
from src.cdf.reconstruction.tracking import (RadarMount, RadarStream, TrackMeasurement, build_local_tracks,
                                             ego_trajectory, filter_and_smooth)

from synthetic_run import CONTACT_T, V_B, make_run


class RadarTrackTests(unittest.TestCase):
    def test_synthetic_radar_target_gives_one_stable_anonymous_track(self):
        with tempfile.TemporaryDirectory() as tmp:
            vehicle = make_run(Path(tmp)) / "vehicles" / "A"
            records = [json.loads(line) for line in (vehicle / "ego.jsonl").read_text().splitlines()]
            streams = [RadarStream(RadarMount.from_metadata(radar.metadata), radar)
                       for radar in load_radar_observations(vehicle)]
            ego = ego_trajectory(records, records[0]["timestamp"])
            tracks = build_local_tracks(streams, ego, records[0]["timestamp"], TrackingConfig())

        # The static poles never become tracks; the car ahead is one anonymous track
        # that survives its stop at the collision.
        self.assertEqual([track.track_id for track in tracks], ["track_001"])
        track = tracks[0]
        self.assertLessEqual(track.first_t, 0.05)
        # A bumper radar loses the car ahead at the contact (its rear is then behind the radar).
        self.assertGreater(track.last_t, CONTACT_T - 0.1)
        # The synthetic stop is instantaneous; a smoother spreads such a step over
        # a few tenths of a second, so speed is checked away from it.
        moving = [s for s in track.samples if 0.5 < s.t_local < CONTACT_T - 0.5]
        self.assertLess(max(abs(s.speed_mps - V_B) for s in moving), 0.5)
        self.assertLess(max(abs(s.lateral_m) for s in moving), 0.5)


class SmootherTests(unittest.TestCase):
    def test_kalman_rts_improves_a_noisy_trajectory(self):
        rng = np.random.RandomState(3)
        cfg = TrackingConfig(measurement_std_m=0.5, acceleration_std_mps2=3.0)
        times = np.arange(0.0, 8.0, 0.05)
        # 12 m/s along x, then braking at 6 m/s^2 from t = 4 s; gentle lateral drift.
        speed = np.where(times < 4.0, 12.0, np.maximum(12.0 - 6.0 * (times - 4.0), 0.0))
        x = np.cumsum(speed) * 0.05
        y = 0.3 * np.sin(times / 2.0)
        truth = np.column_stack([x, y])
        noisy = truth + rng.normal(0.0, 0.5, truth.shape)
        measurements = [TrackMeasurement(t_local=float(t), xy=noisy[k], n_returns=1)
                        for k, t in enumerate(times)]
        smoothed, covariances, filtered = filter_and_smooth(measurements, cfg)

        def rmse(estimate):
            return math.sqrt(np.mean(np.sum((estimate - truth) ** 2, axis=1)))

        self.assertLess(rmse(smoothed[:, :2]), rmse(noisy))
        self.assertLessEqual(rmse(smoothed[:, :2]), rmse(filtered[:, :2]))
        self.assertLess(rmse(smoothed[:, :2]), 0.5 * rmse(noisy))
        # Covariances stay symmetric positive definite.
        for covariance in covariances:
            self.assertTrue(np.allclose(covariance, covariance.T, atol=1e-9))
            self.assertTrue(np.all(np.linalg.eigvalsh(covariance) > 0))


if __name__ == "__main__":
    unittest.main()
