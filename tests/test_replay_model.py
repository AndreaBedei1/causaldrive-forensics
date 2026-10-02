"""Non-CARLA logic of the replay viewer: interpolation, clock, events, camera geometry."""

import json
import math
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.tracking import ego_trajectory
from src.cdf.replay.model import (FALLBACK_BLUEPRINT, FreeCamera, PlaybackClock, Pose, ReplayEvent, ReplayRun,
                                  Trajectory, follow_camera, lerp_angle_deg, local_to_world, overview_camera,
                                  project, state_intervals)

ROOT = Path(__file__).resolve().parents[1]
S01 = ROOT / "traces" / "S01" / "run_0_crash"


def _record(t, x, y, yaw, speed=10.0):
    return {"timestamp": t, "x": x, "y": y, "z": 0.1, "yaw_deg": yaw, "pitch_deg": 0.0, "roll_deg": 0.0,
            "velocity": {"x": speed, "y": 0.0, "z": 0.0}}


def _write(path, data, lines=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row) for row in data) + "\n" if lines else json.dumps(data)
    path.write_text(text, encoding="utf-8")


def _node(node_id, t_local, event_type, subject=None):
    return {"node_id": node_id, "event_type": event_type, "t_local": t_local, "subject_id": subject, "attributes": {}}


def _make_run(root, blueprint_a="vehicle.tesla.model3", b_offset=0.5):
    """A at x = 10 t from source time 100.0, B 30 m ahead from 100.0 + b_offset; A's graph and a collision."""
    run = root / "S99" / "run_0_test"
    _write(run / "metadata.json", {"scenario_id": "S99", "variant": "test", "participants": ["A", "B"]})
    _write(run / "vehicles" / "A" / "ego.jsonl", [_record(100.0 + 0.05 * k, 0.5 * k, 0.0, 0.0) for k in range(161)], True)
    _write(run / "vehicles" / "B" / "ego.jsonl",
           [_record(100.0 + b_offset + 0.05 * k, 30.0, 0.0, 180.0, 0.0) for k in range(141)], True)
    _write(run / "vehicles" / "A" / "metadata.json", {"blueprint": blueprint_a} if blueprint_a else {})
    graph = {"owner": "A", "recorder": {"clock": {"origin_source_timestamp": 100.0}},
             "nodes": [_node("A:e01", 0.0, "MOVING_START"), _node("A:e02", 0.0, "TRACK_APPEARED_FRONT", "track_001"),
                       _node("A:e03", 0.45, "CLOSING_START", "track_001"),
                       _node("A:e04", 1.6, "CLOSING_END", "track_001"), _node("A:e05", 6.5, "COLLISION")]}
    _write(run / "reconstruction" / "A" / "local_graph.json", graph)
    _write(run / "reconstruction" / "B" / "local_graph.json",
           {"owner": "B", "recorder": {"clock": {"origin_source_timestamp": 100.0 + b_offset}},
            "nodes": [_node("B:e01", 0.0, "STOP_START"), _node("B:e02", 6.0, "COLLISION")]})
    _write(run / "reconstruction" / "global" / "global_graph.json", {"nodes": [
        {"node_id": "g01", "event_type": "COLLISION", "participants": ["A", "B"],
         "observations": [{"graph": "A", "local_node": "A:e05", "t_local": 6.5},
                          {"graph": "B", "local_node": "B:e02", "t_local": 6.0}]}]})
    _write(run / "reconstruction" / "global" / "associations.json",
           [{"local_graph": "A", "local_track": "track_001", "global_entity": "B", "status": "ASSOCIATED"}])
    return run


class InterpolationTests(unittest.TestCase):
    def test_angles_take_the_short_way_round(self):
        self.assertAlmostEqual(lerp_angle_deg(10.0, 30.0, 0.5), 20.0)
        self.assertAlmostEqual(lerp_angle_deg(170.0, -170.0, 0.5) % 360.0, 180.0)
        self.assertAlmostEqual(lerp_angle_deg(-179.0, 179.0, 0.25), -179.5)

    def test_pose_is_exact_at_samples_linear_between_and_held_outside(self):
        trajectory = Trajectory.from_records([_record(10.0, 0.0, 0.0, 170.0), _record(10.05, 1.0, 2.0, -170.0),
                                              _record(10.10, 2.0, 4.0, -160.0)])
        self.assertEqual(trajectory.pose_at(10.05), Pose(1.0, 2.0, 0.1, -170.0, 0.0, 0.0))
        middle = trajectory.pose_at(10.025)
        self.assertAlmostEqual(middle.x, 0.5)
        self.assertAlmostEqual(middle.y, 1.0)
        self.assertAlmostEqual(middle.yaw % 360.0, 180.0)  # across the +-180 seam, not through 0
        self.assertEqual(trajectory.pose_at(9.0), trajectory.pose_at(10.0))
        self.assertEqual(trajectory.pose_at(11.0), trajectory.pose_at(10.10))


class ClockTests(unittest.TestCase):
    def test_speed_scales_wall_time(self):
        clock = PlaybackClock(10.0)  # default 0.5x
        clock.advance(1.0)
        self.assertAlmostEqual(clock.time, 0.5)
        clock.set_speed(2.0)
        clock.advance(1.0)
        self.assertAlmostEqual(clock.time, 2.5)

    def test_pause_seek_restart_and_end(self):
        clock = PlaybackClock(3.0, speed=1.0)
        clock.toggle()
        clock.advance(5.0)
        self.assertEqual(clock.time, 0.0)  # paused: time does not advance
        clock.seek(-0.5)
        self.assertEqual(clock.time, 0.0)
        clock.seek(2.5)
        clock.seek(10.0)
        self.assertEqual(clock.time, 3.0)
        clock.restart()
        self.assertEqual(clock.time, 0.0)
        clock.toggle()
        clock.advance(4.0)
        self.assertTrue(clock.at_end)
        self.assertFalse(clock.playing)  # stops at the end
        clock.toggle()  # resuming at the end starts again
        self.assertEqual((clock.time, clock.playing), (0.0, True))

    def test_the_trajectory_does_not_depend_on_speed_or_seek_history(self):
        trajectory = Trajectory.from_records([_record(0.05 * k, 0.37 * k, 0.1 * k * k, 3.0 * k) for k in range(40)])
        slow, fast = PlaybackClock(1.95, speed=0.25), PlaybackClock(1.95, speed=2.0)
        for _ in range(4):
            slow.advance(1.0)
        fast.advance(0.5)
        self.assertAlmostEqual(slow.time, fast.time)
        self.assertEqual(trajectory.pose_at(slow.time), trajectory.pose_at(fast.time))
        wandering = PlaybackClock(1.95, speed=1.0, playing=False)
        for step in (0.5, 0.05, -0.5, 0.5, 0.5, -0.05, -0.5, 1.0, -1.0, 0.5):
            wandering.seek(step)
        wandering.restart()
        wandering.seek(1.0)
        self.assertEqual(trajectory.pose_at(wandering.time), trajectory.pose_at(1.0))


class EventTimelineTests(unittest.TestCase):
    def test_local_times_map_through_each_recorders_clock_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = ReplayRun.load(_make_run(Path(tmp)))
        self.assertEqual(run.start, 100.0)
        self.assertEqual([(e.time, e.event_type) for e in run.local_events["A"].events][2:4],
                         [(0.45, "CLOSING_START"), (1.6, "CLOSING_END")])
        # B's clock starts 0.5 s later: its local 6.0 s is replay 6.5 s, like A's collision.
        self.assertEqual([e.time for e in run.local_events["B"].events], [0.5, 6.5])
        self.assertEqual([(m.time, m.participants) for m in run.collisions], [(6.5, ("A", "B"))])
        self.assertEqual(run.next_event_time(0.0), 0.45)
        self.assertEqual(run.next_event_time(0.45), 0.5)
        self.assertEqual(run.previous_event_time(6.5), 1.6)
        self.assertEqual(run.subject_name("A", "track_001"), "track_001 (B)")

    def test_active_states_follow_start_and_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = ReplayRun.load(_make_run(Path(tmp)))
        active = lambda t: [(s.state, s.subject) for s in run.active_states("A", t)]  # noqa: E731
        self.assertEqual(active(0.44), [("MOVING", None)])
        self.assertEqual(active(0.45), [("MOVING", None), ("CLOSING", "track_001")])
        self.assertEqual(active(1.6), [("MOVING", None)])
        self.assertEqual([e.event_type for e in run.recent_events("A", 1.7, 1.0)], ["CLOSING_END"])
        self.assertIsNone(run.perceived_lines("A", 1.0))  # no perceived state written: pairs are used

    def test_perceived_state_is_read_from_the_trace_frames(self):
        def frame(t, closing, path=False):
            track = {"CLOSING": closing, "IN_EGO_PATH": path}
            return {"t_local": t, "facts": [], "events": [],
                    "perceived_state": {"ego": {"MOVING": True}, "external": {"track_001": track}, "signs": {}}}
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _make_run(Path(tmp))
            _write(run_dir / "reconstruction" / "A" / "local_trace.jsonl",
                   [frame(0.0, False), frame(0.5, True), frame(1.0, "UNKNOWN", "UNKNOWN")], True)
            run = ReplayRun.load(run_dir)
        self.assertEqual(run.perceived_lines("A", 0.45), ["ego: MOVING", "track_001 (B): no active state"])
        self.assertEqual(run.perceived_lines("A", 0.5), ["ego: MOVING", "track_001 (B): CLOSING"])
        # After TRACK_LOST every state of the track is UNKNOWN.
        self.assertEqual(run.perceived_lines("A", 2.0), ["ego: MOVING", "track lost, states UNKNOWN: track_001 (B)"])

    def test_zero_length_open_and_unentered_states(self):
        events = [ReplayEvent(1.0, "A", "TRACK_APPEARED_FRONT", "t1", "e1"),
                  ReplayEvent(2.0, "A", "STOP_SIGN_DETECTED_START", "sign-0", "e2"),
                  ReplayEvent(2.0, "A", "STOP_SIGN_DETECTED_END", "sign-0", "e3"),
                  ReplayEvent(3.0, "A", "EGO_PATH_EXIT", "t1", "e4"),
                  ReplayEvent(4.0, "A", "BRAKE_START", None, "e5")]
        intervals = {(i.state, i.subject): i for i in state_intervals(events)}
        self.assertFalse(intervals[("STOP_SIGN_DETECTED", "sign-0")].active_at(2.0))
        self.assertTrue(intervals[("EGO_PATH", "t1")].active_at(1.5))  # first seen inside the path
        self.assertFalse(intervals[("EGO_PATH", "t1")].active_at(3.0))
        self.assertTrue(intervals[("BRAKE", None)].active_at(100.0))  # still active when observation ended

    def test_blueprint_comes_from_the_recording_then_the_scenario_then_a_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = ReplayRun.load(_make_run(Path(tmp)), {"A": "vehicle.audi.tt", "B": "vehicle.nissan.patrol"})
            self.assertEqual([(p.blueprint, p.blueprint_source) for p in run.participants],
                             [("vehicle.tesla.model3", "recorded"), ("vehicle.nissan.patrol", "scenario")])
        with tempfile.TemporaryDirectory() as tmp:
            run = ReplayRun.load(_make_run(Path(tmp), blueprint_a=None))
            self.assertEqual(run.participants[0].blueprint, FALLBACK_BLUEPRINT)
            self.assertEqual(run.participants[0].blueprint_source, "fallback")

    @unittest.skipUnless((S01 / "reconstruction").exists(), "canonical S01 trace not present")
    def test_s01_crash_events_land_on_the_local_times(self):
        run = ReplayRun.load(S01)
        times = {(e.event_type, e.time) for e in run.local_events["A"].events}
        for expected in [("CLOSING_START", 0.45), ("CLOSING_END", 1.65), ("CLOSING_START", 4.2),
                         ("CRITICAL_TTC_START", 5.0), ("BRAKE_START", 5.55), ("COLLISION", 6.5)]:
            self.assertIn(expected, times)
        self.assertEqual([(m.time, m.participants) for m in run.collisions], [(6.5, ("A", "B"))])


class GeometryTests(unittest.TestCase):
    def test_track_frame_inverts_the_reconstruction_frame(self):
        records = [_record(0.0, 10.0, 20.0, 30.0), _record(0.05, 15.0, 27.0, 35.0)]
        local = ego_trajectory(records, 0.0).states[1]
        origin = Pose(10.0, 20.0, 0.0, 30.0)
        x, y = local_to_world(origin, local.x, local.y)
        self.assertAlmostEqual(x, 15.0)
        self.assertAlmostEqual(y, 27.0)

    def test_projection_follows_carla_axes(self):
        camera = Pose(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(project((10.0, 0.0, 0.0), camera, 90.0, 800, 600), (400.0, 300.0))
        self.assertGreater(project((10.0, 2.0, 0.0), camera, 90.0, 800, 600)[0], 400.0)  # y is to the right
        self.assertLess(project((10.0, 0.0, 2.0), camera, 90.0, 800, 600)[1], 300.0)  # z is up
        self.assertIsNone(project((-5.0, 0.0, 0.0), camera, 90.0, 800, 600))
        u, v = project((0.0, 10.0, 0.0), Pose(0.0, 0.0, 0.0, 90.0), 90.0, 800, 600)
        self.assertAlmostEqual(u, 400.0)
        self.assertAlmostEqual(v, 300.0)

    def test_cameras_look_at_their_targets(self):
        points = [(0.0, 0.0, 0.0), (20.0, 5.0, 0.0)]
        camera = overview_camera(points, heading=0.0)
        u, v = project((10.0, 2.5, 0.0), camera, 90.0, 800, 600)
        self.assertAlmostEqual(u, 400.0, places=3)
        self.assertAlmostEqual(v, 300.0, places=3)
        self.assertLess(camera.x, 10.0)  # behind the centroid along the heading
        vehicle = Pose(50.0, 0.0, 0.0, 90.0)
        chase = follow_camera(vehicle, distance=9.0)
        self.assertAlmostEqual(chase.x, 50.0)
        self.assertAlmostEqual(chase.y, -9.0)
        self.assertAlmostEqual(project((50.0, 0.0, 1.0), chase, 90.0, 800, 600)[0], 400.0, places=3)

    def test_free_camera_moves_in_its_own_frame(self):
        camera = FreeCamera(Pose(0.0, 0.0, 5.0, 90.0, -10.0))
        camera.move(2.0, 1.0, 0.5)
        self.assertAlmostEqual(camera.x, -1.0)
        self.assertAlmostEqual(camera.y, 2.0)
        self.assertAlmostEqual(camera.z, 5.5)
        camera.turn(100.0, -200.0)
        self.assertEqual((camera.yaw, camera.pitch), (-170.0, -89.0))


if __name__ == "__main__":
    unittest.main()
