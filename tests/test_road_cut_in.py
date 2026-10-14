"""Road-relative CUT_IN (reconstruction.road): a car keeping its lane on a curved road is no cut-in; a car
leaving its lane toward the recorder is, on a straight road or on a curve.  Synthetic road, no CARLA."""

import math
import unittest

from src.cdf.common.opendrive import LaneSample
from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.local import RelativeMotion, cut_in_spans
from src.cdf.reconstruction.road import RoadFrame, RoadLanes
from src.cdf.reconstruction.tracking import TrackSample

RADIUS, LANE = 60.0, 3.5


def curved_road():
    """Two lanes of a left bend of radius 60 m around (0, 60): lane centres at 60 m and 63.5 m from the centre."""
    lanes = []
    for radius in (RADIUS, RADIUS + LANE):
        for k in range(120):
            a = -math.pi / 2 + k * 2.0 / RADIUS  # a 2 m stretch per step along the inner lane
            x, y = radius * math.cos(a), RADIUS + radius * math.sin(a)
            lanes.append(LaneSample(x, y, math.degrees(a + math.pi / 2), LANE, 2.5))
    return RoadLanes("bend", lanes)


def on_lane(radius, s, lateral_speed=0.0, speed=12.0):
    """Position and velocity of a car at arc length s on the circle of the given radius, with a velocity
    component across the lane (+ = toward the centre of the bend)."""
    a = -math.pi / 2 + s / RADIUS
    x, y = radius * math.cos(a), RADIUS + radius * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)  # direction of travel
    cx, cy = -math.cos(a), -math.sin(a)  # toward the centre
    return x, y, speed * tx + lateral_speed * cx, speed * ty + lateral_speed * cy


class RoadRelativeTests(unittest.TestCase):
    def setUp(self):
        # The recorder's local frame = world frame (first pose at the origin, heading 0).
        self.frame = RoadFrame(curved_road(), 0.0, 0.0, 0.0)

    def toward(self, target, ego):
        x, y, vx, vy = target
        return self.frame.lane_toward_speed(x, y, vx, vy, ego[0], ego[1])

    def test_case_a_two_cars_following_one_curved_road_do_not_cut_in(self):
        ego = on_lane(RADIUS, 0.0)
        threshold = SemanticsConfig().cut_in_lateral_speed_mps
        for s in (15.0, 25.0, 35.0):
            # In the recorder's frame the car ahead in the outer lane drifts sideways, along the road it does not
            # (the lane is sampled every ~2 m: its heading is known to about a degree).
            self.assertLess(abs(self.toward(on_lane(RADIUS + LANE, s), ego)), threshold)

    def test_case_b_a_car_entering_the_recorders_lane_cuts_in(self):
        ego = on_lane(RADIUS, 0.0)
        self.assertGreater(self.toward(on_lane(RADIUS + LANE, 20.0, lateral_speed=1.2), ego), 1.0)

    def test_case_c_a_lane_change_away_from_the_recorder_is_no_cut_in(self):
        ego = on_lane(RADIUS, 0.0)
        self.assertLess(self.toward(on_lane(RADIUS + LANE, 20.0, lateral_speed=-1.2), ego), -1.0)

    def test_off_the_driving_lanes_there_is_no_road_constraint(self):
        self.assertIsNone(self.frame.lane_toward_speed(500.0, 500.0, 10.0, 0.0, 0.0, 0.0))


def sample(t, lateral):
    return TrackSample(t_local=t, x_m=20.0, y_m=lateral, vx_mps=10.0, vy_mps=0.0, speed_mps=10.0, pos_std_m=0.2,
                       vel_std_mps=0.2, range_m=20.0, bearing_deg=0.0, longitudinal_m=20.0, lateral_m=lateral,
                       closing_speed_mps=0.0, closing_ttc_s=None, measured=True, n_returns=10, clearance_m=18.0)


class CutInGateTests(unittest.TestCase):
    """The same kinematic approach toward the corridor, with or without a lane change."""

    def run_gate(self, lane_toward):
        cfg = SemanticsConfig()
        times = [k * 0.05 for k in range(40)]
        gaps = [max(2.5 - 0.05 * k, 0.0) for k in range(40)]  # the body comes 2 m closer to the corridor
        samples = [sample(t, 4.0) for t in times]
        motions = [RelativeMotion(0.0, -1.0, 0.0, None, None, True) for _ in times]
        left, right = cut_in_spans(times, samples, motions, cfg, gaps, [-1.0] * 40, [1] * 40, [True] * 40,
                                   None if lane_toward is None else [lane_toward] * 40)
        return left + right

    def test_without_a_road_model_the_kinematic_approach_is_a_cut_in(self):
        self.assertTrue(self.run_gate(None))

    def test_a_car_leaving_its_lane_toward_the_recorder_cuts_in(self):
        self.assertTrue(self.run_gate(1.0))

    def test_a_car_keeping_its_lane_does_not_cut_in(self):
        self.assertFalse(self.run_gate(0.0))


if __name__ == "__main__":
    unittest.main()
