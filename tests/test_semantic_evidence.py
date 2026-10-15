"""Evidence behind EGO_PATH and CUT_IN, and a target's impact in the tracker.

* What changed an occupancy (local._path_cause): counterfactuals in one frame -- the target's own motion, the
  corridor's (the recorder's lateral motion), both, or neither (the front edge).
* A cut-in is confirmed by an entry its own manoeuvre was needed for (local._manoeuvre_needed), and dated from
  the onset of the lateral approach, also when it began beside the recorder (local.cut_in_spans).
* The body contains its returns (local._on_body_returns, local._returns_bounds): they bound its reach ahead and
  its occupancy margin from below where the nominal box sits short; a neighbour's returns a lane away do not count.
* A target whose velocity changes in a collision (a rebound) keeps its track; static returns where a target was
  predicted (scenery, the road) are never taken as its impact (tracking._impact_gate).
"""

import math
import unittest

import numpy as np

from src.cdf.reconstruction.config import SemanticsConfig, TrackingConfig
from src.cdf.reconstruction.conflict import box_corners
from src.cdf.reconstruction.local import (_manoeuvre_needed, _on_body_returns, _path_cause, _returns_bounds,
                                          track_events)
from src.cdf.reconstruction.tracking import (EgoFootprint, EgoState, EgoTrajectory, LocalTrack, RadarSweep,
                                             TrackSample, associate_returns)

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
HALF = (CFG.target_length_m / 2.0, CFG.target_width_m / 2.0)
DT = 0.05


def scene(target_y, recorder_y, ahead=8.0, until=1.0, speed=12.0):
    """Times, the recorder's trajectory (heading 0 along x at ``speed``, lateral ``recorder_y(t)``) and the
    target's box corners in the local frame: centre ``ahead`` m in front of the recorder, lateral
    ``target_y(t)``."""
    times = [round(DT * k, 4) for k in range(int(round(until / DT)) + 1)]
    states = [EgoState(t_local=t, x=speed * t, y=recorder_y(t), heading=0.0, vx=speed, vy=0.0) for t in times]
    bodies = [box_corners(np.array([speed * t + ahead, target_y(t)]), np.array([1.0, 0.0]), HALF) for t in times]
    return times, EgoTrajectory(states), bodies


def ramp(start, rate, t0=0.5):
    return lambda t: start + rate * max(t - t0, 0.0)


class CauseTests(unittest.TestCase):
    def cause(self, target_y, recorder_y):
        times, ego, bodies = scene(target_y, recorder_y)
        return _path_cause(len(times) - 1, times, bodies, ego, None, CFG.path_half_width_m)

    def test_the_target_moving_in(self):
        self.assertEqual(self.cause(ramp(3.5, -3.0), ramp(0.0, 0.0)), "TARGET_LATERAL")

    def test_the_recorder_moving_toward_a_car_keeping_its_lane(self):
        self.assertEqual(self.cause(ramp(3.5, 0.0), ramp(0.0, 3.0)), "RECORDER_LATERAL")

    def test_two_cars_moving_into_one_lane_need_each_other(self):
        # 0.75 m each: neither alone brings the body within the corridor, both together do.
        self.assertEqual(self.cause(ramp(3.5, -1.5), ramp(0.0, 1.5)), "MUTUAL_LATERAL")

    def test_no_lateral_change_is_the_front_edge(self):
        self.assertEqual(self.cause(ramp(1.0, 0.0), ramp(0.0, 0.0)), "LONGITUDINAL")


class ManoeuvreNeededTests(unittest.TestCase):
    def needed(self, target_y, recorder_y):
        times, ego, bodies = scene(target_y, recorder_y)
        return _manoeuvre_needed(0, len(times) - 1, times, bodies, ego, None, CFG.path_half_width_m)

    def test_a_cut_in_needs_the_targets_motion(self):
        self.assertTrue(self.needed(ramp(3.5, -3.0), ramp(0.0, 0.0)))

    def test_the_recorders_lane_change_alone_confirms_nothing(self):
        self.assertFalse(self.needed(ramp(3.5, 0.0), ramp(0.0, 3.0)))

    def test_two_cars_moving_into_one_lane_confirm_the_target_arriving(self):
        self.assertTrue(self.needed(ramp(3.5, -1.5), ramp(0.0, 1.5)))


class ReturnsBoundsTests(unittest.TestCase):
    """A car beside-ahead on the right, seen along its left side: true centre (3.5, 2.4), nominal box placed
    1.7 m short (centre (1.8, 2.4)); returns along its left side up to 0.2 m short of its true front."""

    def setUp(self):
        self.ego = EgoTrajectory([EgoState(t_local=0.0, x=0.0, y=0.0, heading=0.0, vx=12.0, vy=0.0)])
        self.box = box_corners(np.array([1.8, 2.4]), np.array([1.0, 0.0]), HALF)
        self.side = np.column_stack([np.linspace(2.0, 5.6, 10), np.full(10, 2.4 - HALF[1])])

    def bounds(self, points):
        on_body = _on_body_returns((points, np.zeros_like(points)), 0.0, self.ego, self.box, CFG.path_edge_std_m)
        return _returns_bounds(on_body, 0.0, self.ego, None, CAR.x_max, CFG.path_half_width_m)

    def test_the_returns_prove_the_reach_the_short_box_misses(self):
        margin, reach = self.bounds(self.side)
        box_reach = float(np.max(self.box[:, 0])) - CAR.x_max
        self.assertAlmostEqual(reach, 5.2 - CAR.x_max, places=6)  # the second farthest return
        self.assertGreater(reach, box_reach + 1.0)
        self.assertAlmostEqual(margin, CFG.path_half_width_m - (2.4 - HALF[1]), places=6)

    def test_a_neighbours_returns_a_lane_away_do_not_count(self):
        neighbour = self.side + np.array([0.0, 3.5])
        self.assertIsNone(self.bounds(neighbour))
        margin, reach = self.bounds(np.vstack([self.side, neighbour]))
        self.assertAlmostEqual(reach, 5.2 - CAR.x_max, places=6)

    def test_one_stray_return_decides_nothing(self):
        stray = np.array([[9.0, 0.0]])  # deep inside the corridor, far ahead of the box
        margin, reach = self.bounds(np.vstack([self.side[:3], stray]))
        self.assertLess(margin, 1.0)


def _track(motion, start=0.0, end=8.0):
    samples = []
    for k in range(int(round((end - start) / DT)) + 1):
        t = round(start + DT * k, 2)
        x, y, vx, vy = motion(t)
        samples.append(TrackSample(t_local=t, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                                   pos_std_m=0.1, vel_std_mps=0.1, range_m=math.hypot(x, y),
                                   bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                                   closing_speed_mps=0.0, closing_ttc_s=None, measured=True, n_returns=4,
                                   clearance_m=float(CAR.distance(x, y)), ahead_m=x - CAR.x_max))
    return LocalTrack("track_001", samples)


class CutInOnsetTests(unittest.TestCase):
    def test_a_lane_change_begun_beside_the_recorder_is_dated_from_its_onset(self):
        # The recorder at 12 m/s; a car on its right 2 m/s faster, its near side 2.9 m out, still beside the
        # recorder when it starts moving toward the recorder's lane at t0 = 1.0 s (1 m/s); it draws ahead and
        # enters the path.  One manoeuvre: the cut-in starts at its onset, not once the car is ahead.
        t0 = 1.0

        def motion(t):
            moving = t0 <= t < 4.0
            return -2.0 + 2.0 * t, 2.9 - 1.0 * (min(max(t, t0), 4.0) - t0), 14.0, (-1.0 if moving else 0.0)

        ego = EgoTrajectory([EgoState(t_local=0.05 * k, x=12.0 * 0.05 * k, y=0.0, heading=0.0, vx=12.0, vy=0.0)
                             for k in range(201)])
        events = [(e.type, e.t_local) for e in track_events("A", _track(motion), 10.0, CFG, ego, footprint=CAR)]
        starts = [t for name, t in events if name == "CUT_IN_FROM_RIGHT_START"]
        entries = [t for name, t in events if name == "EGO_PATH_ENTRY"]
        self.assertEqual(starts, [t0])
        self.assertEqual(len(entries), 1)
        self.assertLess(starts[0], entries[0])


def _sweep(t, points, radial):
    points = np.asarray(points, float)
    ranges = np.hypot(*points.T)
    return RadarSweep(t_local=round(t, 4), points=points, origins=np.zeros_like(points),
                      radar=np.zeros(len(points), dtype=int), radial_speed=np.asarray(radial, float),
                      clearance=ranges, depth=ranges)


def _rear(x, n=8):
    return np.column_stack([np.full(n, x), np.linspace(-0.8, 0.8, n)])


class ImpactGateTests(unittest.TestCase):
    def test_a_target_that_rebounds_off_another_car_keeps_its_track(self):
        # Driving away at 14 m/s, it hits something at t = 2 s: -3 m/s at once (a rebound), standstill 0.5 s
        # later.  Its returns stay on its body all along.
        c = TrackingConfig()
        x, sweeps = 20.0, []
        for k in range(81):
            t = DT * k
            v = 14.0 if t < 2.0 - 1e-9 else min(-3.0 + 6.0 * (t - 2.0), 0.0)
            x += v * DT if k else 0.0
            points = _rear(x)
            sweeps.append(_sweep(t, points, v * points[:, 0] / np.hypot(*points.T)))
        tracks = associate_returns(sweeps, c)
        self.assertEqual(len(tracks), 1)
        measured = [m for m in tracks[0].measurements if m.xy is not None]
        self.assertGreaterEqual(measured[-1].t_local, 3.9)
        self.assertTrue(any(m.impulse_var > 0.0 for m in measured))

    def test_static_returns_where_a_target_was_predicted_are_not_its_impact(self):
        # Driving away at 10 m/s; from t = 2 s its own returns vanish and static ones (a wall, the road) lie
        # where it is predicted: it did not stop there.
        c = TrackingConfig()
        sweeps = []
        for k in range(61):
            t = DT * k
            if t < 2.0 - 1e-9:
                points = _rear(20.0 + 10.0 * t)
                radial = 10.0 * points[:, 0] / np.hypot(*points.T)
            else:
                points = _rear(20.0 + 10.0 * t, 12)
                radial = np.zeros(len(points))
            sweeps.append(_sweep(t, points, radial))
        tracks = associate_returns(sweeps, c)
        self.assertEqual(len(tracks), 1)
        late = [m for m in tracks[0].measurements if m.xy is not None and m.t_local >= 2.0 - 1e-9]
        self.assertEqual(late, [])


if __name__ == "__main__":
    unittest.main()
