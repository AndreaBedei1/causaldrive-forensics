"""Semantic transitions of anonymous radar tracks."""

import math
import unittest

from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.local import track_events
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory, LocalTrack, TrackSample

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
            closing_ttc_s=distance / closing if closing > 0.1 else None, measured=True, n_returns=4))
    return LocalTrack(track_id="track_001", samples=samples)


def _events(track, recording_end=10.0, ego=None):
    return [(event.type, event.t_local) for event in track_events("A", track, recording_end, CFG, ego)]


def _ego(speed, stop_at=99.0, after=0.0, end=10.0):
    """The recorder driving straight ahead at ``speed`` until ``stop_at``, then at ``after``."""
    states, x = [], 0.0
    for k in range(int(round(end / 0.05)) + 1):
        t = round(0.05 * k, 2)
        v = speed if t < stop_at else after
        states.append(EgoState(t_local=t, x=x, y=0.0, heading=0.0, vx=v, vy=0.0))
        x += v * 0.05
    return EgoTrajectory(states)


class RadarTransitionTests(unittest.TestCase):
    def test_track_appeared_and_lost(self):
        events = _events(_track(lambda t: (30.0, 8.0, 0.0), start=1.0, end=3.0), recording_end=10.0)
        self.assertEqual(events, [("TRACK_APPEARED_RIGHT", 1.0), ("TRACK_LOST", 3.0)])
        still_tracked = _events(_track(lambda t: (30.0, 8.0, 0.0), start=1.0, end=10.0), recording_end=10.0)
        self.assertEqual(still_tracked, [("TRACK_APPEARED_RIGHT", 1.0)])

    def test_closing_start_and_end(self):
        events = _events(_track(lambda t: (30.0, 8.0, 3.0 if 2.0 <= t < 3.0 else 0.0)))
        self.assertIn(("CLOSING_START", 2.0), events)
        self.assertIn(("CLOSING_END", 3.0), events)

    def test_short_closing_flicker_is_ignored(self):
        events = _events(_track(lambda t: (30.0, 8.0, 3.0 if 2.0 <= t < 2.15 else 0.0)))
        self.assertNotIn("CLOSING_START", [name for name, _ in events])

    def test_critical_ttc_start_and_end(self):
        # The recorder drives at 10 m/s at a standing target ahead and stops at 3.6 s.  Without its
        # own footprint the recorder is a 4.6 m box (front edge 2.3 m ahead of its origin); its
        # envelope reaches 1 m further.  Braking at 6 m/s^2 after 1 s needs 10 + 10^2 / 12 = 18.3 m:
        # critical once the target is within 2.3 + 1 + 18.3 = 21.6 m, at t = 2.84: sample 2.85.
        def profile(t):
            if t < 3.6:
                return 40.0 - 10.0 * (t - 1.0), 0.0, 10.0
            return 14.0, 0.0, 0.0
        events = _events(_track(profile), ego=_ego(10.0, stop_at=3.6))
        self.assertIn(("CRITICAL_TTC_START", 2.85), events)
        self.assertIn(("CRITICAL_TTC_END", 3.6), events)  # standing still: no collision course
        self.assertIn(("CLOSING_END", 3.6), events)
        self.assertIn(("CLOSING_START", 1.0), events)

    def test_a_slower_approach_becomes_critical_closer_to_the_target(self):
        # 5 m/s at the same standing target: 5 + 25 / 12 = 7.1 m to stop, critical within 10.4 m of
        # the recorder's origin, at t = 2.92 (sample 2.95) -- later and closer than at 10 m/s.
        def profile(t):
            if t < 3.6:
                return 20.0 - 5.0 * (t - 1.0), 0.0, 5.0
            return 7.0, 0.0, 0.0
        events = _events(_track(profile), ego=_ego(5.0, stop_at=3.6))
        self.assertIn(("CRITICAL_TTC_START", 2.95), events)
        self.assertIn(("CRITICAL_TTC_END", 3.6), events)

    def test_critical_ttc_never_outlasts_closing(self):
        # Closing slows to 0.3 m/s at 0.5 m while the recorder creeps at 0.3 m/s toward the standing
        # target: inside the envelope, which the closing speed alone would not release, but both now
        # stand still (below 1 m/s), so the critical state ends with CLOSING.
        def profile(t):
            if t < 3.0:
                return 10.0 - 4.0 * (t - 1.0), 0.0, 4.0
            return 0.5, 0.0, 0.3
        events = _events(_track(profile), ego=_ego(4.0, stop_at=3.0, after=0.3))
        # Critical from 1.35 s by geometry, claimed once the track (first seen at 1.0 s) is
        # critical_min_track_age_s old.
        self.assertIn(("CRITICAL_TTC_START", 1.5), events)
        self.assertIn(("CLOSING_END", 3.0), events)
        self.assertIn(("CRITICAL_TTC_END", 3.0), events)

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
