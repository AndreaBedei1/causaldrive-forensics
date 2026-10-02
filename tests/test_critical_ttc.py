"""CRITICAL_TTC: collision course in 2-D and braking avoidability (reconstruction/conflict.py).

Geometry in the recorder's vehicle frame (x forward, y right).  The recorder is a model3-sized
footprint (front edge 2.4 m ahead of its origin, 2.16 m wide); the envelope adds the standstill
margin d0 = 1 m ahead and behind and 0.3 m at the sides.  Reaction time 1 s, available
deceleration 6 m/s^2 (configs/reconstruction.yaml).
"""

import json
import math
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.conflict import assess_conflict
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, TrackSample

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
ROOT = Path(__file__).resolve().parents[1]


def ego(speed, yaw_rate=0.0):
    return EgoState(t_local=0.0, x=0.0, y=0.0, heading=0.0, vx=speed, vy=0.0, yaw_rate=yaw_rate)


def target(x, y, vx, vy, acceleration=0.0, closing=None):
    """A track sample: its near surface at (x, y) (vehicle frame), ground velocity (vx, vy)."""
    if closing is None:  # rate at which the distance to the footprint shrinks (recorder at 10 m/s or not)
        closing = 0.0
    return TrackSample(t_local=0.0, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                       pos_std_m=0.1, vel_std_mps=0.1, range_m=math.hypot(x, y),
                       bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                       closing_speed_mps=closing, closing_ttc_s=None, measured=True, n_returns=4,
                       clearance_m=float(CAR.distance(x, y)), acceleration_mps2=acceleration)


def assess(own, sample):
    return assess_conflict(sample, own, CAR, CFG)


class LongitudinalTests(unittest.TestCase):
    def test_stopped_target_is_critical_exactly_when_stopping_no_longer_suffices(self):
        # 14 m/s: 14 m of reaction + 14^2 / 12 = 16.3 m of braking + 1 m margin from the front edge
        # (2.4 m): critical once the target's near surface is within 33.7 m of the origin.
        near = assess(ego(14.0), target(33.0, 0.0, 0.0, 0.0, closing=14.0))
        far = assess(ego(14.0), target(34.6, 0.0, 0.0, 0.0, closing=14.0))
        self.assertTrue(near.collision_course and near.critical)
        self.assertTrue(far.collision_course)
        self.assertFalse(far.critical)
        expected = 14.0 ** 2 / (2.0 * (34.6 - 2.4 - 1.0 - 14.0))
        self.assertAlmostEqual(far.required_deceleration_mps2, expected, delta=0.05)
        self.assertEqual(far.avoidance_by, "recorder")

    def test_following_a_slower_car_needs_only_its_speed_difference(self):
        # 14 m/s behind a car at 8 m/s: 6 m/s to shed, 6 m reaction + 3 m braking + 1 m margin.
        critical = assess(ego(14.0), target(12.0, 0.0, 8.0, 0.0, closing=6.0))
        safe = assess(ego(14.0), target(13.0, 0.0, 8.0, 0.0, closing=6.0))
        self.assertTrue(critical.critical)
        self.assertTrue(safe.collision_course and not safe.critical)

    def test_a_car_at_the_same_speed_is_no_collision_course(self):
        for gap in (6.0, 12.0, 30.0):
            result = assess(ego(14.0), target(gap, 0.0, 14.0, 0.0))
            self.assertFalse(result.collision_course, gap)
            self.assertFalse(result.critical)
            self.assertIsNone(result.ttc_s)
        inside = assess(ego(14.0), target(3.0, 0.0, 14.0, 0.0, closing=0.0))  # within the margin, not closing
        self.assertFalse(inside.collision_course)

    def test_a_braking_lead_car_is_taken_with_its_measured_deceleration(self):
        # Same speed, 20 m ahead: no threat at constant speed, but the lead brakes at 8 m/s^2 and stops
        # 12.25 m further: the recorder must stop within 20 - 3.4 + 12.25 m after a 14 m reaction.
        coasting = assess(ego(14.0), target(20.0, 0.0, 14.0, 0.0))
        braking = assess(ego(14.0), target(20.0, 0.0, 14.0, 0.0, acceleration=-8.0))
        self.assertFalse(coasting.collision_course)
        self.assertTrue(braking.collision_course and braking.critical)
        self.assertAlmostEqual(braking.required_deceleration_mps2,
                               14.0 ** 2 / (2.0 * (20.0 - 3.4 + 12.25 - 14.0)), delta=0.1)

    def test_a_faster_recorder_is_critical_earlier(self):
        def first_critical(speed):
            return next(d / 2.0 for d in range(160, 0, -1)
                        if assess(ego(speed), target(d / 2.0, 0.0, 0.0, 0.0, closing=speed)).critical)
        self.assertGreater(first_critical(15.0), first_critical(8.0))


class CrossingTests(unittest.TestCase):
    def test_crossing_traffic_that_passes_ahead_is_not_critical(self):
        # A car from the right at 10 m/s, already 15 m ahead and 3 m to the side: it clears the
        # recorder's lane well before the recorder (10 m/s) gets there.
        result = assess(ego(10.0), target(15.0, 3.0, 0.0, -10.0, closing=5.0))
        self.assertFalse(result.collision_course)
        self.assertFalse(result.critical)

    def test_crossing_traffic_that_passes_behind_is_not_critical(self):
        # The recorder (14 m/s) is through the crossing long before a slow car from the right arrives.
        result = assess(ego(14.0), target(6.0, 25.0, 0.0, -4.0, closing=4.0))
        self.assertFalse(result.collision_course)

    def test_a_collision_course_is_critical_only_when_braking_no_longer_suffices(self):
        # Both 2 s from the same crossing point, then the same geometry three times further away.
        close = assess(ego(10.0), target(20.0, 20.0, 0.0, -10.0, closing=10.0))
        distant = assess(ego(10.0), target(60.0, 60.0, 0.0, -10.0, closing=10.0))
        self.assertTrue(close.collision_course and close.critical)
        self.assertEqual(close.encounter, "CROSSING")
        self.assertTrue(distant.collision_course)
        self.assertFalse(distant.critical)
        self.assertGreater(distant.ttc_s, close.ttc_s)

    def test_oncoming_traffic_in_the_next_lane_is_not_critical(self):
        # S08 A and C: 36 m apart, closing at 19 m/s, 3.8 m apart laterally (the former model
        # called this critical at TTC 1.9 s).
        result = assess(ego(9.6), target(36.0, -3.8, -8.7, 0.0, closing=18.3))
        self.assertEqual(result.encounter, "OPPOSING")
        self.assertFalse(result.collision_course)
        self.assertFalse(result.critical)

    def test_a_standing_recorder_is_not_threatened_by_traffic_crossing_ahead(self):
        # S08's C stopped short of the junction while B crosses 13 m ahead of it.
        result = assess(ego(0.0), target(13.0, -15.0, 0.0, 12.6, closing=9.5))
        self.assertFalse(result.collision_course)


class RearThreatTests(unittest.TestCase):
    def test_a_car_closing_in_from_behind_can_only_be_avoided_by_its_own_braking(self):
        late = assess(ego(5.0), target(-15.0, 0.0, 15.0, 0.0, closing=10.0))
        early = assess(ego(5.0), target(-40.0, 0.0, 15.0, 0.0, closing=10.0))
        self.assertTrue(late.collision_course and early.collision_course)
        self.assertEqual(late.avoidance_by, "target")
        self.assertTrue(late.critical)
        self.assertFalse(early.critical)
        # 10 m/s to shed after a 10 m reaction, keeping 1 m behind the recorder's rear (-2.37 m).
        self.assertAlmostEqual(early.required_deceleration_mps2, 10.0 ** 2 / (2.0 * (40.0 - 3.37 - 10.0)), delta=0.1)

    def test_an_overtaking_car_in_the_next_lane_is_no_threat(self):
        result = assess(ego(10.0), target(-12.0, -3.6, 15.0, 0.0, closing=0.0))
        self.assertFalse(result.collision_course)


class S08RegressionTests(unittest.TestCase):
    """The recorded S08: CRITICAL_TTC only between the two vehicles that really collide (A, B)."""

    def test_only_the_colliding_pair_is_critical(self):
        run = ROOT / "traces" / "S08" / "run_0_crash"
        evaluation = run / "reconstruction" / "evaluation" / "evaluation.json"
        if not evaluation.exists():
            self.skipTest("canonical trace not present")
        identity = {row["track"]: row["true_identity"]
                    for row in json.loads(evaluation.read_text(encoding="utf-8"))["tracks"]}
        critical = set()
        for owner in ("A", "B", "C"):
            graph = json.loads((run / "reconstruction" / owner / "local_graph.json").read_text(encoding="utf-8"))
            for node in graph["nodes"]:
                if node["event_type"] == "CRITICAL_TTC_START":
                    critical.add((owner, identity.get(owner + ":" + node["subject_id"])))
        self.assertTrue(critical <= {("A", "B"), ("B", "A")}, critical)
        self.assertTrue(critical)


if __name__ == "__main__":
    unittest.main()
