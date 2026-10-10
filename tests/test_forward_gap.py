"""CRITICAL_TTC for an unsafe forward gap (safe following distance) and the CUT_IN pre-entry region.

Safe following distance d_min = max(v_ego * t_front(v_ego), 2 m), t_front from the UN R157 (ALKS,
M1/N1) table, an engineering reference, not a norm.  Geometry in the recorder's vehicle frame (x
forward, y right): a model3-sized recorder (front face 2.4 m ahead of its origin, 2.16 m wide), the
target given by its observed near surface.  Corridor +-1.5 m, front-lateral margin 1 m
(configs/reconstruction.yaml).  CASE numbers follow the 2026-10-10 specification.
"""

import json
import math
import unittest
from pathlib import Path

from src.cdf.llm.guard import LeakGuardError, check_packet
from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.conflict import assess_conflict, minimum_time_gap_s, safe_following_distance
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.local import mark_occlusions, reconstruct_vehicle, track_events
from src.cdf.reconstruction.pipeline import read_incident_context
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, EgoTrajectory, LocalTrack, TrackSample

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
ROOT = Path(__file__).resolve().parents[1]


def ego(speed):
    return EgoState(t_local=0.0, x=0.0, y=0.0, heading=0.0, vx=speed, vy=0.0)


def target(x, y, vx, vy, vel_std=0.1, t=0.0):
    """A track sample: its near surface at (x, y) (vehicle frame), ground velocity (vx, vy)."""
    return TrackSample(t_local=t, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                       pos_std_m=0.1, vel_std_mps=vel_std, range_m=math.hypot(x, y),
                       bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                       closing_speed_mps=0.0, closing_ttc_s=None, measured=True, n_returns=4,
                       clearance_m=float(CAR.distance(x, y)))


def assess(own, sample):
    return assess_conflict(sample, own, CAR, CFG)


class TimeGapTableTests(unittest.TestCase):
    def test_un_r157_time_gaps_with_linear_interpolation(self):
        table = CFG.critical_time_gap_table
        for kmh, gap in ((7.2, 1.0), (10.0, 1.1), (20.0, 1.2), (30.0, 1.3), (40.0, 1.4), (50.0, 1.5), (60.0, 1.6),
                         (45.0, 1.45), (25.0, 1.25)):
            self.assertAlmostEqual(minimum_time_gap_s(kmh / 3.6, table), gap, places=6, msg=kmh)
        self.assertEqual(minimum_time_gap_s(1.0, table), 1.0)  # below the table: its first value is held
        self.assertEqual(minimum_time_gap_s(30.0, table), 1.6)  # above it: its last value, no extrapolation

    def test_d_min_is_speed_times_time_gap_never_below_two_metres(self):
        t_front, distance, required = safe_following_distance(12.0, CFG)
        self.assertAlmostEqual(t_front, 1.4 + 0.1 * (43.2 - 40.0) / 10.0)
        self.assertAlmostEqual(distance, 12.0 * t_front)
        self.assertEqual(required, distance)  # no margin added
        self.assertAlmostEqual(safe_following_distance(50.0 / 3.6, CFG)[2], 50.0 / 3.6 * 1.5)
        for speed in [0.1 * k for k in range(0, 400)]:
            t_front, distance, required = safe_following_distance(speed, CFG)
            self.assertGreaterEqual(required, 2.0, speed)
            self.assertAlmostEqual(required, max(speed * t_front, 2.0), msg=speed)
        self.assertEqual(safe_following_distance(0.0, CFG)[2], 2.0)
        self.assertEqual(safe_following_distance(1.5, CFG)[2], 2.0)  # 1.5 m/s x 1.0 s < 2 m

    def test_the_target_speed_is_no_input(self):
        # Only the recorder's speed: the signature takes no target and the threshold cannot depend on it.
        import inspect
        self.assertEqual(list(inspect.signature(safe_following_distance).parameters), ["ego_speed_mps", "cfg"])
        slower = assess(ego(12.0), target(2.4 + 10.0, 0.0, 6.0, 0.0))
        faster = assess(ego(12.0), target(2.4 + 10.0, 0.0, 13.0, 0.0))
        self.assertEqual(slower.forward.required_distance_m, faster.forward.required_distance_m)


class ForwardGapTests(unittest.TestCase):
    def test_close_car_ahead_at_the_same_speed_is_critical_without_a_collision_course(self):  # CASE 1
        result = assess(ego(12.0), target(2.4 + 3.0, 0.0, 12.0, 0.0))
        self.assertFalse(result.collision_course)
        self.assertIsNone(result.ttc_s)
        self.assertTrue(result.critical)
        self.assertEqual(result.critical_reason, "UNSAFE_FORWARD_GAP")
        forward = result.forward
        self.assertEqual(forward.region, "IN_PATH")
        self.assertAlmostEqual(forward.longitudinal_clearance_m, 3.0, places=6)
        self.assertAlmostEqual(forward.time_headway_s, 0.25, places=6)
        self.assertAlmostEqual(forward.minimum_time_gap_s, 1.432, places=6)
        self.assertAlmostEqual(forward.required_distance_m, 12.0 * 1.432, places=6)
        self.assertLess(forward.margin_m, -14.0)

    def test_the_same_car_beyond_the_safe_distance_is_not_critical(self):  # CASE 2
        result = assess(ego(12.0), target(2.4 + 40.0, 0.0, 12.0, 0.0))
        self.assertTrue(result.forward.leader)
        self.assertFalse(result.forward.unsafe)
        self.assertFalse(result.critical)
        self.assertIsNone(result.critical_reason)

    def test_just_below_and_just_above_the_threshold(self):  # CASE 3 (one sample; hysteresis below)
        d_min = 12.0 * 1.432
        below = assess(ego(12.0), target(2.4 + d_min - 0.05, 0.0, 12.0, 0.0))
        above = assess(ego(12.0), target(2.4 + d_min + 0.05, 0.0, 12.0, 0.0))
        self.assertTrue(below.forward.unsafe and below.critical)
        self.assertFalse(above.forward.unsafe or above.critical)
        # Above d_min but within the release band: no new start, yet not released either.
        self.assertFalse(above.forward.released)
        released = assess(ego(12.0), target(2.4 + 1.11 * d_min, 0.0, 12.0, 0.0))
        self.assertTrue(released.forward.released)

    def test_a_slightly_faster_car_close_ahead_is_still_an_unsafe_gap(self):
        result = assess(ego(12.0), target(2.4 + 3.0, 0.0, 13.0, 0.0))
        self.assertFalse(result.collision_course)
        self.assertIsNone(result.ttc_s)
        self.assertEqual(result.critical_reason, "UNSAFE_FORWARD_GAP")

    def test_a_crawling_recorder_keeps_at_least_two_metres(self):  # CASES 4 and 5
        close = assess(ego(1.5), target(2.4 + 1.5, 0.0, 1.5, 0.0))
        self.assertEqual(close.forward.required_distance_m, 2.0)
        self.assertTrue(close.forward.leader)
        self.assertEqual(close.critical_reason, "UNSAFE_FORWARD_GAP")
        self.assertIsNone(close.ttc_s)
        enough = assess(ego(1.5), target(2.4 + 2.5, 0.0, 1.5, 0.0))
        self.assertFalse(enough.forward.unsafe)
        self.assertFalse(enough.critical)
        # A standing car 2.5 m ahead is no leader (no forward-gap claim); only a real predicted overlap can
        # make it critical: here the collision-course model does (1 s reaction at 1.5 m/s plus its 1 m
        # envelope leave no room to stop), independently of the safe gap.
        standing = assess(ego(1.5), target(2.4 + 2.5, 0.0, 0.0, 0.0))
        self.assertFalse(standing.forward.leader)
        self.assertFalse(standing.forward.unsafe)
        self.assertTrue(standing.collision_course)
        self.assertEqual(standing.critical_reason, "PREDICTED_OVERLAP")
        self.assertIsNotNone(standing.ttc_s)

    def test_the_former_braking_branch_no_longer_counts(self):
        # 14 m/s behind a car at 6 m/s, 22 m ahead: d_min = 14 x 1.504 = 21.06 m, so the gap itself is safe
        # (the former max(time gap, reaction + braking difference + 1 m) asked for 28.3 m).
        result = assess(ego(14.0), target(2.4 + 22.0, 0.0, 6.0, 0.0))
        self.assertAlmostEqual(result.forward.required_distance_m, 14.0 * 1.504, places=3)
        self.assertFalse(result.forward.unsafe)
        self.assertNotIn("UNSAFE_FORWARD_GAP", result.critical_reason or "")
        self.assertTrue(result.collision_course)  # closing at 8 m/s: the 2-D model still looks at it

    def test_a_car_behind_at_the_same_speed_is_no_leader(self):  # CASE 6
        result = assess(ego(12.0), target(-2.37 - 3.0, 0.0, 12.0, 0.0))
        self.assertLess(result.forward.longitudinal_clearance_m, 0.0)
        self.assertFalse(result.forward.leader)
        self.assertFalse(result.critical)

    def test_a_car_exactly_beside_is_no_leader_however_close(self):  # CASE 7
        for lateral in (2.0, 3.0):
            result = assess(ego(12.0), target(0.0, lateral, 12.0, 0.0))
            self.assertFalse(result.forward.leader, lateral)
            self.assertFalse(result.critical, lateral)

    def test_a_front_lateral_car_entering_the_path_close_ahead_is_critical(self):  # CASE 9
        # Its near (rear-left) corner 6 m ahead and 2 m to the right, moving toward the corridor at
        # 1 m/s: its nominal body (turned toward the corridor, front corner leading) lies just
        # outside it, a leader about 3.6 m ahead of the front face.
        entering = assess(ego(12.0), target(6.0, 2.0, 12.0, -1.0))
        self.assertEqual(entering.forward.region, "FRONT_LATERAL")
        self.assertGreater(entering.forward.lateral_body_gap_m, 0.0)
        self.assertLessEqual(entering.forward.lateral_body_gap_m, CFG.critical_front_lateral_margin_m)
        self.assertTrue(entering.forward.leader)
        self.assertTrue(entering.critical)
        self.assertIn("UNSAFE_FORWARD_GAP", entering.critical_reason)
        # The same car keeping its own lane next to the corridor is no leader: an overtaken or
        # overtaking car in the next lane is not followed.
        keeping = assess(ego(12.0), target(6.0, 2.0, 12.0, 0.0))
        self.assertIsNone(keeping.forward.region)
        self.assertFalse(keeping.critical)
        # Nor is a lateral drift within the estimate's uncertainty (0.3 m/s beyond it is needed).
        drifting = assess(ego(12.0), target(6.0, 2.0, 12.0, -0.35, vel_std=0.1))
        self.assertFalse(drifting.forward.leader)

    def test_a_car_two_lanes_away_is_no_leader_even_when_it_moves_over(self):  # CASE 8
        result = assess(ego(12.0), target(8.0, 6.0, 12.0, -1.5))
        self.assertGreater(result.forward.lateral_body_gap_m, CFG.critical_front_lateral_margin_m)
        self.assertFalse(result.forward.leader)
        self.assertFalse(result.critical)

    def test_crossing_traffic_keeps_the_collision_course_model(self):  # CASE 10
        close = assess(ego(10.0), target(20.0, 20.0, 0.0, -10.0))
        self.assertEqual(close.encounter, "CROSSING")
        self.assertTrue(close.collision_course and close.critical)
        self.assertEqual(close.critical_reason, "PREDICTED_OVERLAP")
        self.assertFalse(close.forward.leader)
        passing = assess(ego(10.0), target(15.0, 3.0, 0.0, -10.0))
        self.assertFalse(passing.critical)

    def test_oncoming_traffic_is_no_leader(self):
        result = assess(ego(10.0), target(15.0, 0.0, -10.0, 0.0))
        self.assertEqual(result.encounter, "OPPOSING")
        self.assertFalse(result.forward.leader)

    def test_a_standing_recorder_follows_nobody(self):
        for lead_speed in (0.0, 1.5):
            result = assess(ego(0.0), target(2.4 + 1.0, 0.0, lead_speed, 0.0))
            self.assertFalse(result.forward.leader)
            self.assertFalse(result.critical)

    def test_uncertain_estimates_and_occluded_samples_make_no_claim(self):
        uncertain = assess(ego(12.0), target(5.4, 0.0, 12.0, 0.0, vel_std=1.5))
        self.assertTrue(uncertain.forward.unsafe)
        self.assertFalse(uncertain.critical)
        young = assess_conflict(target(5.4, 0.0, 12.0, 0.0), ego(12.0), CAR, CFG, track_age_s=0.2)
        self.assertFalse(young.critical)
        hidden = target(5.4, 0.0, 12.0, 0.0)
        hidden.occluded = True
        result = assess(ego(12.0), hidden)
        self.assertTrue(result.occluded)
        self.assertFalse(result.critical)
        # Seen past another vehicle, it is not the vehicle the recorder follows: the reason can end.
        self.assertTrue(result.released(CFG.critical_release_ratio * CFG.critical_deceleration_mps2))


def _ego_trajectory(speed, end=10.0):
    return EgoTrajectory([EgoState(t_local=round(0.05 * k, 2), x=speed * 0.05 * k, y=0.0, heading=0.0,
                                   vx=speed, vy=0.0) for k in range(int(round(end / 0.05)) + 1)])


def _track(motion, start=0.0, end=8.0, track_id="track_001"):
    """A track from motion(t) -> (longitudinal, lateral, vx, vy) relative to the recorder (heading 0)."""
    samples = []
    for k in range(int(round((end - start) / 0.05)) + 1):
        t = round(start + 0.05 * k, 2)
        x, y, vx, vy = motion(t)
        samples.append(TrackSample(t_local=t, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                                   pos_std_m=0.1, vel_std_mps=0.1, range_m=math.hypot(x, y),
                                   bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                                   closing_speed_mps=0.0, closing_ttc_s=None, measured=True, n_returns=4,
                                   clearance_m=float(CAR.distance(x, y)), ahead_m=x - CAR.x_max))
    return LocalTrack(track_id, samples)


def _events(track, ego_speed=12.0, recording_end=10.0):
    return [(e.type, e.t_local) for e in track_events("A", track, recording_end, CFG, _ego_trajectory(ego_speed),
                                                    footprint=CAR)]


class ForwardGapHysteresisTests(unittest.TestCase):
    def test_the_state_ends_only_beyond_ten_percent_more_than_the_safe_distance(self):
        # Recorder at 12 m/s (safe distance 17.18 m); the car ahead first 10 m away, then pulls away
        # at 2 m/s: unsafe until 17.18 m, held up to 1.10 x 17.18 = 18.9 m, released beyond.
        required = safe_following_distance(12.0, CFG)[2]

        def motion(t):
            return 2.4 + 10.0 + 2.0 * max(t - 1.0, 0.0), 0.0, 12.0 + (2.0 if t >= 1.0 else 0.0), 0.0

        events = _events(_track(motion))
        starts = [t for name, t in events if name == "CRITICAL_TTC_START"]
        ends = [t for name, t in events if name == "CRITICAL_TTC_END"]
        self.assertEqual(starts, [0.5])  # as soon as the track is old enough
        self.assertEqual(len(ends), 1)
        gap_at_end = 10.0 + 2.0 * (ends[0] - 1.0)
        self.assertGreater(gap_at_end, CFG.critical_forward_release_factor * required - 0.11)
        self.assertLess(gap_at_end, CFG.critical_forward_release_factor * required + 0.2 + 2.0 * 0.25)

    def test_a_safe_follower_never_turns_critical(self):
        events = _events(_track(lambda t: (2.4 + 25.0, 0.0, 12.0, 0.0)))
        self.assertNotIn("CRITICAL_TTC_START", [name for name, _ in events])


def _lane_change(start_lateral, speed=1.0, t0=2.0, until=6.0, longitudinal=8.0):
    """A car ahead (same speed as the recorder) drifting toward the recorder's lane from its right."""
    def motion(t):
        moving = t0 <= t < until
        drift = speed * (min(max(t, t0), until) - t0)
        return longitudinal, start_lateral - drift, 12.0, (-speed if moving else 0.0)
    return motion


class CutInPreEntryTests(unittest.TestCase):
    def test_an_adjacent_car_moving_into_the_path_cuts_in_and_is_critical_first(self):  # A
        # Close to the lane line (near side 2.9 m out): its body is within the front-lateral margin
        # as soon as it heads for the path, before the cut-in has persisted long enough.
        events = _events(_track(_lane_change(2.9)))
        cut_in = next(t for name, t in events if name == "CUT_IN_FROM_RIGHT_START")
        critical = next(t for name, t in events if name == "CRITICAL_TTC_START")
        entry = next(t for name, t in events if name == "EGO_PATH_ENTRY")
        self.assertLess(critical, cut_in)
        self.assertLess(cut_in, entry)
        # From the middle of the next lane (near side 3.4 m out) the body reaches the margin when the
        # cut-in is already established: both start together, the gap is never critical later.
        events = _events(_track(_lane_change(3.4)))
        cut_in = next(t for name, t in events if name == "CUT_IN_FROM_RIGHT_START")
        critical = next(t for name, t in events if name == "CRITICAL_TTC_START")
        self.assertLessEqual(critical, cut_in)

    def test_a_car_still_two_lanes_away_does_not_cut_in(self):  # B
        # It changes lanes toward the recorder but stops in the lane next to the recorder's.
        events = _events(_track(_lane_change(7.0, speed=1.5, until=4.4)))
        names = [name for name, _ in events]
        self.assertNotIn("CUT_IN_FROM_RIGHT_START", names)
        self.assertNotIn("CRITICAL_TTC_START", names)

    def test_a_car_seen_past_another_vehicle_gives_no_cut_in_evidence(self):
        near = _track(lambda t: (2.4 + 2.0, 1.5, 12.0, 0.0), track_id="track_001")  # right in front-right
        far = _track(_lane_change(6.0, speed=1.5, longitudinal=14.0), track_id="track_002")
        mark_occlusions([near, far], _ego_trajectory(12.0), CAR, CFG)
        self.assertTrue(any(sample.occluded for sample in far.samples))
        self.assertFalse(any(sample.occluded for sample in near.samples))
        events = [(e.type, e.t_local) for e in track_events("A", far, 10.0, CFG, _ego_trajectory(12.0),
                                                           footprint=CAR)]
        hidden = {round(s.t_local, 2) for s in far.samples if s.occluded}
        for name, t in events:
            if name in ("CUT_IN_FROM_RIGHT_START", "CRITICAL_TTC_START"):
                self.assertNotIn(round(t, 2), hidden, (name, t))


class PacketTests(unittest.TestCase):
    def test_forward_gap_outputs_are_refused_by_the_leak_guard(self):
        for key in ("required_safe_distance_m", "time_headway_s", "minimum_time_gap_s", "safe_distance_margin_m",
                    "critical_reason", "lateral_body_gap_m", "longitudinal_clearance_m", "forward_region"):
            with self.assertRaises(LeakGuardError, msg=key):
                check_packet({"facts": [{"type": "TRACK_STATE", key: 1.0}]})


def _graph(run, owner):
    path = ROOT / "traces" / run / "reconstruction" / owner / "local_graph.json"
    return json.loads(path.read_text(encoding="utf-8"))["nodes"] if path.exists() else None


class CampaignRegressionTests(unittest.TestCase):
    """The recorded campaign, reconstructed with these rules (traces/)."""

    def first(self, nodes, event_type, subject):
        return next((n["t_local"] for n in nodes if n["event_type"] == event_type and n["subject_id"] == subject), None)

    def test_s02_critical_before_cut_in_keeps_its_order(self):  # E
        run = ROOT / "traces" / "S02" / "run_0_critical_before_cut_in"
        if not (run / "vehicles" / "A").exists():
            self.skipTest("canonical trace not present")
        # Reconstructed now from the raw files with the current rules (not read from the stored outputs).
        local = reconstruct_vehicle(run / "vehicles" / "A", ReconstructionConfig(), context=read_incident_context(run))
        nodes = [{"event_type": n.event_type, "subject_id": n.subject_id, "t_local": n.t_local}
                 for n in local.graph.nodes]
        critical = self.first(nodes, "CRITICAL_TTC_START", "track_001")
        cut_in = self.first(nodes, "CUT_IN_FROM_LEFT_START", "track_001")
        self.assertIsNotNone(critical)
        self.assertIsNotNone(cut_in)
        self.assertLess(critical, cut_in)

    def test_s02_crash_still_cuts_in(self):  # E
        nodes = _graph("S02/run_0_crash", "A")
        if nodes is None:
            self.skipTest("canonical trace not present")
        self.assertIsNotNone(self.first(nodes, "CUT_IN_FROM_LEFT_START", "track_001"))

    def test_s17_a_is_critical_before_the_cut_in_and_b_sees_no_cut_in(self):  # C, D
        a_nodes, b_nodes = _graph("S17/run_0_crash", "A"), _graph("S17/run_0_crash", "B")
        if a_nodes is None or b_nodes is None:
            self.skipTest("canonical trace not present")
        critical = self.first(a_nodes, "CRITICAL_TTC_START", "track_001")
        cut_in = self.first(a_nodes, "CUT_IN_FROM_RIGHT_START", "track_001")
        entry = self.first(a_nodes, "EGO_PATH_ENTRY", "track_001")
        collision = next(n["t_local"] for n in a_nodes if n["event_type"] == "COLLISION")
        self.assertTrue(critical < cut_in < entry < collision, (critical, cut_in, entry, collision))
        self.assertFalse([n for n in b_nodes if n["event_type"].startswith("CUT_IN")])

    def test_no_critical_ttc_on_a_car_behind_or_beside_for_the_gap_alone(self):
        for run in sorted(p for p in (ROOT / "traces").glob("S*/run_*") if p.is_dir()):
            for owner_dir in sorted((run / "reconstruction").glob("*/local_trace.jsonl")):
                with owner_dir.open(encoding="utf-8") as handle:
                    for line in handle:
                        for fact in json.loads(line)["facts"]:
                            attributes = fact.get("attributes") or {}
                            if fact["type"] == "TRACK_STATE" and attributes.get("critical_reason") == "UNSAFE_FORWARD_GAP":
                                self.assertGreater(attributes["longitudinal_clearance_m"], 0.0)
                                self.assertLessEqual(attributes["lateral_body_gap_m"],
                                                     CFG.critical_front_lateral_margin_m + 1e-6)


if __name__ == "__main__":
    unittest.main()
