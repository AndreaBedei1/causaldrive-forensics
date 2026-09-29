"""Semantic transitions of anonymous radar tracks."""

import math
import unittest

from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.local import track_events
from src.cdf.reconstruction.tracking import LocalTrack, TrackSample

CFG = SemanticsConfig()


def _track(profile, start=1.0, end=5.0):
    """A track whose (longitudinal, lateral, closing speed) follow ``profile(t)``."""
    samples = []
    for k in range(int(round((end - start) / 0.05)) + 1):
        t = round(start + 0.05 * k, 2)
        longitudinal, lateral, closing = profile(t)
        distance = math.hypot(longitudinal, lateral)
        samples.append(TrackSample(
            t_local=t, x_m=longitudinal, y_m=lateral, vx_mps=0.0, vy_mps=0.0, speed_mps=5.0,
            pos_std_m=0.1, vel_std_mps=0.1, range_m=distance,
            bearing_deg=math.degrees(math.atan2(lateral, longitudinal)), longitudinal_m=longitudinal,
            lateral_m=lateral, closing_speed_mps=closing,
            ttc_s=distance / closing if closing > 0.1 else None, measured=True, n_returns=4))
    return LocalTrack(track_id="track_001", samples=samples)


def _events(track, recording_end=10.0):
    return [(event.type, event.t_local) for event in track_events("A", track, recording_end, CFG)]


class RadarTransitionTests(unittest.TestCase):
    def test_track_appeared_and_lost(self):
        events = _events(_track(lambda t: (30.0, 8.0, 0.0), start=1.0, end=3.0), recording_end=10.0)
        self.assertEqual(events, [("TRACK_APPEARED", 1.0), ("TRACK_LOST", 3.0)])
        still_tracked = _events(_track(lambda t: (30.0, 8.0, 0.0), start=1.0, end=10.0), recording_end=10.0)
        self.assertEqual(still_tracked, [("TRACK_APPEARED", 1.0)])

    def test_closing_start_and_end(self):
        events = _events(_track(lambda t: (30.0, 8.0, 3.0 if 2.0 <= t < 3.0 else 0.0)))
        self.assertIn(("CLOSING_START", 2.0), events)
        self.assertIn(("CLOSING_END", 3.0), events)

    def test_short_closing_flicker_is_ignored(self):
        events = _events(_track(lambda t: (30.0, 8.0, 3.0 if 2.0 <= t < 2.15 else 0.0)))
        self.assertNotIn("CLOSING_START", [name for name, _ in events])

    def test_critical_ttc_start_and_end(self):
        # Closing at 5 m/s from 20 m: TTC reaches 2 s at 10 m (t = 3 s); closing stops at 3.5 s.
        def profile(t):
            if t < 3.5:
                return 20.0 - 5.0 * (t - 1.0), 0.0, 5.0
            return 7.5, 0.0, 0.0
        events = _events(_track(profile))
        self.assertIn(("CRITICAL_TTC_START", 3.0), events)
        self.assertIn(("CRITICAL_TTC_END", 3.5), events)
        self.assertIn(("CLOSING_END", 3.5), events)
        self.assertIn(("CLOSING_START", 1.0), events)

    def test_ego_path_entry_and_exit(self):
        def profile(t):  # moves across the corridor from left to right
            return 15.0, -3.5 + 2.0 * (t - 1.0), 0.0
        events = _events(_track(profile))
        entry = next(t for name, t in events if name == "EGO_PATH_ENTRY")
        exit_ = next(t for name, t in events if name == "EGO_PATH_EXIT")
        self.assertAlmostEqual(entry, 2.0)   # lateral reaches -1.5 m
        self.assertAlmostEqual(exit_, 3.8)   # lateral exceeds +2.0 m (corridor + hysteresis)

    def test_no_invented_entry_for_a_track_first_seen_in_the_path(self):
        events = _events(_track(lambda t: (15.0, 0.0 if t < 3.0 else 4.0, 0.0)))
        names = [name for name, _ in events]
        self.assertNotIn("EGO_PATH_ENTRY", names)
        self.assertIn(("EGO_PATH_EXIT", 3.0), events)

    def test_boundary_noise_does_not_flicker(self):
        # Enters, then wanders between 1.4 and 1.9 m: inside the hysteresis band.
        def profile(t):
            if t < 2.0:
                return 15.0, -4.0, 0.0
            return 15.0, 1.4 if round(t * 20) % 2 else 1.9, 0.0
        names = [name for name, _ in _events(_track(profile))]
        self.assertEqual(names.count("EGO_PATH_ENTRY"), 1)
        self.assertNotIn("EGO_PATH_EXIT", names)

    def test_track_events_carry_no_telemetry(self):
        for event in track_events("A", _track(lambda t: (20.0 - 5.0 * (t - 1.0), 0.0, 5.0)), 10.0, CFG):
            self.assertLessEqual(set(event.attributes), {"active_at_first_observation"})
            self.assertEqual(event.subject_id, "track_001")


if __name__ == "__main__":
    unittest.main()
