"""Leader and cut-in rules (local.track_events): UNSAFE_FORWARD_GAP only for a leader (a target in the recorder's
path or in a confirmed cut-in), CUT_IN only when confirmed by the target's EGO_PATH_ENTRY, the path corridor along
the recorder's lane on a bend.  Synthetic tracks; the curved cases use a synthetic two-lane bend (no CARLA)."""

import math
import unittest

from src.cdf.common.opendrive import LanePiece, LaneSample
from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.local import track_events
from src.cdf.reconstruction.road import RoadFrame, RoadLanes
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, EgoTrajectory, LocalTrack, TrackSample

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
DT, END = 0.05, 8.0
RADIUS, LANE, SPEED = 60.0, 3.5, 12.0


def straight_ego(speed=SPEED):
    return EgoTrajectory([EgoState(t_local=round(DT * k, 2), x=speed * DT * k, y=0.0, heading=0.0, vx=speed, vy=0.0)
                          for k in range(int(round(END / DT)) + 1)])


def sample(t, ego_state, wx, wy, wvx, wvy, vel_std=0.1):
    """A track sample at world (wx, wy) with world velocity: the recorder's local frame is the world frame here."""
    c, s = math.cos(ego_state.heading), math.sin(ego_state.heading)
    dx, dy = wx - ego_state.x, wy - ego_state.y
    lon, lat = c * dx + s * dy, -s * dx + c * dy
    return TrackSample(t_local=t, x_m=wx, y_m=wy, vx_mps=wvx, vy_mps=wvy, speed_mps=math.hypot(wvx, wvy),
                       pos_std_m=0.1, vel_std_mps=vel_std, range_m=math.hypot(lon, lat),
                       bearing_deg=math.degrees(math.atan2(lat, lon)), longitudinal_m=lon, lateral_m=lat,
                       closing_speed_mps=0.0, closing_ttc_s=None, measured=True, n_returns=4,
                       clearance_m=float(CAR.distance(lon, lat)), ahead_m=lon - CAR.x_max)


def straight_track(position, ego=None):
    """position(t) -> (world x, world y, vx, vy) of the target; the recorder drives along +x."""
    ego = ego or straight_ego()
    out = []
    for k in range(int(round(END / DT)) + 1):
        t = round(DT * k, 2)
        x, y, vx, vy = position(t)
        out.append(sample(t, ego.at(t), x, y, vx, vy))
    return LocalTrack("track_001", out)


def names(events):
    return [(e.type, round(e.t_local, 2)) for e in events]


def first(events, kind):
    return next((t for name, t in events if name == kind), None)


class StraightRoadTests(unittest.TestCase):
    def run_events(self, track, ego=None, road=None):
        return names(track_events("A", track, END + 1.0, CFG, ego or straight_ego(), footprint=CAR, road=road))

    def test_an_adjacent_car_entering_the_path_cuts_in(self):
        def position(t):  # 9 m ahead, from the next lane (3.5 m to the side) into the recorder's lane at 1 m/s
            drift = min(max(t - 2.0, 0.0), 3.5)
            moving = 2.0 <= t < 5.5
            return SPEED * t + 2.4 + 9.0, 3.5 - drift, SPEED, -1.0 if moving else 0.0
        events = self.run_events(straight_track(position))
        cut_in, entry = first(events, "CUT_IN_FROM_RIGHT_START"), first(events, "EGO_PATH_ENTRY")
        self.assertIsNotNone(cut_in)
        self.assertIsNotNone(entry)
        self.assertLess(cut_in, entry)
        critical = first(events, "CRITICAL_TTC_START")
        self.assertIsNotNone(critical)
        self.assertGreaterEqual(critical, cut_in)  # a leader only once the cut-in is established

    def test_an_approach_that_never_enters_is_no_cut_in_and_no_leader(self):
        def position(t):  # drifts toward the recorder's lane, stops at its own lane edge, drifts back
            drift = 0.8 * min(max(t - 2.0, 0.0), 1.0) - 0.8 * min(max(t - 5.0, 0.0), 1.0)
            return SPEED * t + 2.4 + 6.0, 3.6 - drift, SPEED, 0.0
        events = self.run_events(straight_track(position))
        self.assertIsNone(first(events, "EGO_PATH_ENTRY"))
        self.assertIsNone(first(events, "CUT_IN_FROM_RIGHT_START"))
        self.assertIsNone(first(events, "CRITICAL_TTC_START"))

    def test_side_by_side_traffic_with_noisy_lateral_speed_is_no_leader(self):
        for ahead in (0.0, 1.5, 3.0):  # abreast, and its rear just past the recorder's front face
            def position(t, ahead=ahead):  # next lane, same speed; the lateral speed estimate wobbles +-0.6 m/s
                return SPEED * t + 2.4 + 2.3 + ahead, 3.5, SPEED, 0.6 * math.sin(2.0 * math.pi * t)
            events = self.run_events(straight_track(position))
            self.assertIsNone(first(events, "CRITICAL_TTC_START"), ahead)
            self.assertIsNone(first(events, "CUT_IN_FROM_RIGHT_START"), ahead)

    def test_a_car_turning_away_beside_the_recorder_is_no_cut_in(self):
        def position(t):  # beside and ahead, heading away to the right from t = 2 s
            angle = min(max(t - 2.0, 0.0), 2.0) * math.radians(20.0)
            return SPEED * t + 2.4 + 5.0, 3.5 + max(t - 2.0, 0.0) * 3.0, SPEED * math.cos(angle), SPEED * math.sin(angle)
        events = self.run_events(straight_track(position))
        self.assertIsNone(first(events, "CUT_IN_FROM_RIGHT_START"))
        self.assertIsNone(first(events, "CUT_IN_FROM_LEFT_START"))

    def test_a_merging_car_entering_the_path_at_an_angle_cuts_in(self):
        def position(t):  # merges from the right at 10 degrees into the recorder's lane, 10 m ahead
            lateral = max(4.5 - 2.1 * max(t - 1.0, 0.0), 0.0)
            moving = lateral > 0.0
            return SPEED * t + 2.4 + 10.0, lateral, SPEED, -2.1 if moving else 0.0
        events = self.run_events(straight_track(position))
        self.assertIsNotNone(first(events, "CUT_IN_FROM_RIGHT_START"))
        self.assertIsNotNone(first(events, "EGO_PATH_ENTRY"))


def pieces(lines):
    """Lane pieces (one road section, lanes -1, -2, ...) from centre polylines in the direction of travel."""
    out = []
    for number, points in enumerate(lines, 1):
        heads = [math.atan2(b[1] - a[1], b[0] - a[0]) for a, b in zip(points, points[1:])]
        out.append(LanePiece(("road", 0, -number), tuple(points), tuple(heads + heads[-1:]),
                             tuple(LANE for _ in points), "-1"))
    return out


def three_lanes():
    """A straight three-lane road along +x: lane centres at y = -3.5, 0 (the recorder's) and +3.5."""
    lines = [[(float(x), y) for x in range(-60, 261)] for y in (-LANE, 0.0, LANE)]
    return RoadLanes("straight", [LaneSample(x, y, 0.0, LANE, 2.0) for y in (-LANE, 0.0, LANE)
                                  for x in range(-60, 260, 2)], pieces(lines))


class LaneKeepingNullHypothesisTests(unittest.TestCase):
    """PREDICTED_OVERLAP that only the target's motion across its own lane creates needs that motion confirmed
    (path entry or contact); a car passing beside the recorder, its track point sliding over its faces, is none."""

    def setUp(self):
        self.road = RoadFrame(three_lanes(), 0.0, 0.0, 0.0)

    def run_events(self, track, ego, road):
        return names(track_events("A", track, END + 1.0, CFG, ego, footprint=CAR, road=road))

    def passing(self, ego):
        """A car in the right lane overtaking the slow recorder: as it comes abreast its track point slides 1 m
        inward (front face, then side face) at 1.4 m/s, and back out once it is ahead (side, then rear face)."""
        def position(t):
            slide = min(max(t - 1.6, 0.0) / 0.7, 1.0) - min(max(t - 2.9, 0.0) / 0.7, 1.0)
            vy = -1.4 if 1.6 <= t < 2.3 else (1.4 if 2.9 <= t < 3.6 else 0.0)
            return 12.0 * t - 25.0, 3.0 - slide, 12.0, vy
        return straight_track(position, ego)

    def test_a_car_passing_beside_with_a_sliding_track_point_is_not_critical(self):
        ego = straight_ego(3.0)
        events = self.run_events(self.passing(ego), ego, None)
        self.assertIsNotNone(first(events, "CRITICAL_TTC_START"))  # the artefact, without a road model
        events = self.run_events(self.passing(ego), ego, self.road)
        self.assertIsNone(first(events, "CRITICAL_TTC_START"))
        self.assertIsNone(first(events, "EGO_PATH_ENTRY"))

    def test_a_real_lane_change_into_the_path_stays_critical(self):
        def position(t):  # 8 m ahead in the right lane, slower, changing into the recorder's lane from t = 1 s
            moving = 1.0 <= t < 1.0 + LANE / 1.2
            lateral = LANE - 1.2 * min(max(t - 1.0, 0.0), LANE / 1.2)
            return 2.4 + 8.0 + 9.0 * t, lateral, 9.0, -1.2 if moving else 0.0
        ego = straight_ego()
        with_road = self.run_events(straight_track(position, ego), ego, self.road)
        without = self.run_events(straight_track(position, ego), ego, None)
        self.assertIsNotNone(first(with_road, "EGO_PATH_ENTRY"))
        self.assertIsNotNone(first(with_road, "CRITICAL_TTC_START"))
        self.assertEqual(first(with_road, "CRITICAL_TTC_START"), first(without, "CRITICAL_TTC_START"))

    def test_the_recorder_drifting_into_a_car_beside_it_stays_critical(self):
        states = []
        for k in range(int(round(END / DT)) + 1):
            t = round(DT * k, 2)
            vy = 1.2 if 2.0 <= t < 5.0 else 0.0
            y = 1.2 * min(max(t - 2.0, 0.0), 3.0)
            states.append(EgoState(t_local=t, x=SPEED * t, y=y, heading=math.atan2(vy, SPEED), vx=SPEED, vy=vy))
        ego = EgoTrajectory(states)
        track = straight_track(lambda t: (SPEED * t + 1.0, 3.5, SPEED, 0.0), ego)  # abreast in the right lane
        self.assertIsNotNone(first(self.run_events(track, ego, self.road), "CRITICAL_TTC_START"))


def bend():
    """Two lanes of a bend of radius 60 m around (0, 60): lane centres 60 m and 63.5 m from the centre."""
    lanes, lines = [], []
    for radius in (RADIUS, RADIUS + LANE):
        line = []
        for k in range(160):
            a = -math.pi / 2 + (k - 20) * 2.0 / RADIUS
            lanes.append(LaneSample(radius * math.cos(a), RADIUS + radius * math.sin(a),
                                    math.degrees(a + math.pi / 2), LANE, 2.5))
        for k in range(320):
            a = -math.pi / 2 + (k - 40) * 1.0 / RADIUS
            line.append((radius * math.cos(a), RADIUS + radius * math.sin(a)))
        lines.append(line)
    return RoadLanes("bend", lanes, pieces(lines))


def on_bend(radius, s, speed=SPEED, lateral_speed=0.0):
    """World position, velocity and heading at arc length s (along the inner lane) on the circle of ``radius``."""
    a = -math.pi / 2 + s / RADIUS
    x, y = radius * math.cos(a), RADIUS + radius * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    cx, cy = -math.cos(a), -math.sin(a)
    return x, y, speed * tx + lateral_speed * cx, speed * ty + lateral_speed * cy, a + math.pi / 2


def bend_ego():
    states = []
    for k in range(int(round(END / DT)) + 1):
        t = round(DT * k, 2)
        x, y, vx, vy, heading = on_bend(RADIUS, SPEED * t)
        states.append(EgoState(t_local=t, x=x, y=y, heading=heading, vx=vx, vy=vy))
    return EgoTrajectory(states)


class BendTests(unittest.TestCase):
    def setUp(self):
        self.ego = bend_ego()
        self.road = RoadFrame(bend(), 0.0, 0.0, 0.0)  # local frame = world frame

    def track(self, radius_of_t, ahead_m=14.0, lateral_speed_of_t=lambda t: 0.0):
        out = []
        for k in range(int(round(END / DT)) + 1):
            t = round(DT * k, 2)
            x, y, vx, vy, _ = on_bend(radius_of_t(t), SPEED * t + ahead_m, lateral_speed=lateral_speed_of_t(t))
            out.append(sample(t, self.ego.at(t), x, y, vx, vy))
        return LocalTrack("track_001", out)

    def run_events(self, track, road):
        return names(track_events("A", track, END + 1.0, CFG, self.ego, footprint=CAR, road=road))

    def test_two_cars_following_one_bend_are_not_in_each_others_path(self):
        track = self.track(lambda t: RADIUS + LANE)  # the outer lane, 14 m ahead along the bend
        events = self.run_events(track, self.road)
        self.assertIsNone(first(events, "EGO_PATH_ENTRY"))
        self.assertIsNone(first(events, "CUT_IN_FROM_LEFT_START"))
        self.assertIsNone(first(events, "CUT_IN_FROM_RIGHT_START"))
        self.assertIsNone(first(events, "CRITICAL_TTC_START"))

    def test_a_real_lane_change_on_the_bend_cuts_in(self):
        def radius(t):  # from the outer lane into the recorder's lane between 2 and 4.9 s
            return RADIUS + LANE - min(max(t - 2.0, 0.0) * 1.2, LANE)
        track = self.track(radius, lateral_speed_of_t=lambda t: 1.2 if 2.0 <= t < 2.0 + LANE / 1.2 else 0.0)
        events = self.run_events(track, self.road)
        entry = first(events, "EGO_PATH_ENTRY")
        cut_in = first(events, "CUT_IN_FROM_LEFT_START") or first(events, "CUT_IN_FROM_RIGHT_START")
        self.assertIsNotNone(entry)
        self.assertIsNotNone(cut_in)
        self.assertLess(cut_in, entry)


if __name__ == "__main__":
    unittest.main()
