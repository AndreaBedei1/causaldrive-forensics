"""Headless top-down replay export (cdf.replay.topdown), the automatic visual-QA checks (cdf.replay.qa) and
the paper's core event view.  Reconstruction-only inputs (ReplayRun); no CARLA server, no ground truth."""

import math
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.models import PAPER_CORE_EVENTS, is_core_event
from src.cdf.replay.model import CollisionMark, Participant, Pose, ReplayRun, Trajectory
from src.cdf.replay.qa import check_run
from src.cdf.replay.topdown import frame_items, keyframes, render_frame, states_at

ROOT = Path(__file__).resolve().parents[1]
S12 = ROOT / "traces" / "S12" / "run_0_crash"


class CoreViewTests(unittest.TestCase):
    def test_the_paper_core_events(self):
        for name in ("COLLISION", "BRAKE_START", "BRAKE_END", "CUT_IN_FROM_LEFT_START", "CUT_IN_FROM_RIGHT_END",
                     "EGO_PATH_ENTRY", "CRITICAL_TTC_START", "CRITICAL_TTC_END", "TRACK_APPEARED_FRONT",
                     "TRACK_APPEARED_LEFT", "TRACK_APPEARED_RIGHT", "TRACK_LOST"):
            self.assertTrue(is_core_event(name), name)
        for name in ("THROTTLE_START", "CLOSING_START", "TURN_LEFT_START", "STOP_SIGN_DETECTED_START", "MOVING_START"):
            self.assertFalse(is_core_event(name), name)  # kept in the graphs, not in the paper's core view
        self.assertEqual(len(PAPER_CORE_EVENTS), len(set(PAPER_CORE_EVENTS)))


@unittest.skipUnless((S12 / "reconstruction").exists(), "S12 trace not present")
class S12ExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replay = ReplayRun.load(S12)

    def at(self, t_global):
        return t_global - self.replay.display_time(0.0)

    def test_keyframes_come_from_the_reconstructed_events(self):
        frames = keyframes(self.replay)
        times = [round(self.replay.display_time(frame.time), 2) for frame in frames]
        self.assertEqual(times, sorted(times))
        self.assertEqual(len(times), len(set(times)))
        for expected in (-2.4, -2.2, -2.1, -1.15, -0.9, 0.0, 0.55):  # one or two radar sweeps earlier than the fixed gates
            self.assertIn(expected, times)
        collision = next(frame for frame in frames if abs(self.replay.display_time(frame.time)) < 1e-6)
        self.assertIn("COLLISION(A,B)", collision.label)
        self.assertEqual(times[0], round(self.replay.display_time(0.0), 2))  # lead-in clipped to the replay start

    def test_states_are_exact_at_the_collision(self):
        own_a, tracks_a = states_at(self.replay, "A", self.at(0.0))
        own_b, tracks_b = states_at(self.replay, "B", self.at(0.0))
        self.assertNotIn("CRITICAL_TTC", tracks_a.get("track_002", []))  # ended with the collision
        self.assertNotIn("CRITICAL_TTC", tracks_b.get("track_001", []))
        self.assertIn("CRITICAL_TTC", tracks_a.get("track_001", []))  # A on the anonymous C goes on
        _, tracks_before = states_at(self.replay, "A", self.at(-0.05))
        self.assertIn("CRITICAL_TTC", tracks_before.get("track_002", []))

    def test_a_frame_draws_the_recorders_and_the_anonymous_road_user_once(self):
        items = frame_items(self.replay, self.at(-2.40))
        self.assertEqual([r["id"] for r in items["recorders"]], ["A", "B"])
        self.assertEqual(items["ghosts"], [])
        self.assertEqual([e["entity"].entity_id for e in items["entities"]], ["U1"])
        self.assertEqual(sorted(m["track"].name for m in items["members"]), ["A:track_001", "B:track_002"])
        self.assertEqual(sorted(a["track"].name for a in items["associated"]), ["A:track_002", "B:track_001"])
        u1 = items["entities"][0]
        self.assertIn("CRITICAL_TTC", u1["states"])  # A's CRITICAL_TTC on its track of U1
        self.assertEqual(u1["observers"], ["A", "B"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "frame.png"
            render_frame(self.replay, self.at(0.0), path, label="test")
            self.assertGreater(path.stat().st_size, 10000)

    def test_s12_flags_nothing(self):
        flags = check_run(self.replay)
        checks = {flag.check for flag in flags}
        # C, seen by A and by B, is one road user: no duplicated ghost any more (phase 0 flagged three).
        for duplicate in ("duplicate_ghost_across_observers", "duplicate_ghost_same_observer", "road_users_overlap",
                          "road_user_on_recorder", "road_user_box_jump", "road_user_box_spin"):
            self.assertNotIn(duplicate, checks)
        for semantic in ("critical_end_before_own_collision", "critical_start_after_own_collision",
                         "collision_without_contact", "cut_in_without_lateral_approach", "path_entry_outside_corridor",
                         "event_outside_track_lifetime", "impossible_track_speed", "impossible_recorder_speed"):
            self.assertNotIn(semantic, checks)


def _straight(x0, y0, yaw, speed, end=4.0):
    times = [0.05 * k for k in range(int(end / 0.05) + 1)]
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return Trajectory(times, [Pose(x0 + c * speed * t, y0 + s * speed * t, 0.0, yaw) for t in times])


class QaTests(unittest.TestCase):
    def test_a_collision_of_recorders_that_do_not_touch_is_flagged(self):
        a = Participant("A", "vehicle.tesla.model3", "recorded", _straight(0.0, 0.0, 0.0, 10.0), Pose(0, 0, 0, 0))
        b = Participant("B", "vehicle.tesla.model3", "recorded", _straight(0.0, 8.0, 0.0, 10.0), Pose(0, 8, 0, 0))
        run = ReplayRun(run_dir=Path("."), name="synthetic", participants=[a, b], start=0.0, duration=4.0,
                        collisions=[CollisionMark(2.0, ("A", "B"), "g01")])
        flags = check_run(run)
        self.assertEqual([f.check for f in flags], ["collision_without_contact"])
        self.assertIn("apart", flags[0].detail)

    def test_touching_recorders_are_not_flagged(self):
        a = Participant("A", "vehicle.tesla.model3", "recorded", _straight(0.0, 0.0, 0.0, 10.0), Pose(0, 0, 0, 0))
        b = Participant("B", "vehicle.tesla.model3", "recorded", _straight(4.7, 0.0, 0.0, 10.0), Pose(4.7, 0, 0, 0))
        run = ReplayRun(run_dir=Path("."), name="synthetic", participants=[a, b], start=0.0, duration=4.0,
                        collisions=[CollisionMark(2.0, ("A", "B"), "g01")])
        self.assertEqual(check_run(run), [])

    def test_a_teleporting_recorder_is_flagged(self):
        times = [0.0, 0.05, 0.1]
        poses = [Pose(0, 0, 0, 0), Pose(0.5, 0, 0, 0), Pose(20.0, 0, 0, 0)]
        a = Participant("A", "vehicle.tesla.model3", "recorded", Trajectory(times, poses), poses[0])
        run = ReplayRun(run_dir=Path("."), name="synthetic", participants=[a], start=0.0, duration=0.1)
        self.assertEqual([f.check for f in check_run(run)], ["impossible_recorder_speed"])


if __name__ == "__main__":
    unittest.main()
