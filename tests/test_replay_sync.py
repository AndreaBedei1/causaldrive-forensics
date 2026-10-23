"""Two viewers side by side (GROUND TRUTH and RECONSTRUCTION), driven from either window.  The leader sends the
instant it shows on the recording clock (in G0 the recorders' clocks are the simulator's), whether it plays and its
speed; the follower maps that instant through its own clock.  Play, pause, seek and speed in the follower's window
go to the leader as numbered commands; the camera (C, mouse, free camera) and ESC act on both.  Nothing about the
recordings crosses: no position, no event, no identity but a recorder both viewers replay."""

import json
import socket
import unittest
from pathlib import Path

from src.cdf.replay.ground_truth import load_ground_truth_run
from src.cdf.replay.model import PlaybackClock, ReplayRun
from src.cdf.replay.sync import (SyncPeer, apply_sync, decode, encode, encode_quit, encode_view, follow_ports,
                                 lead_ports)

ROOT = Path(__file__).resolve().parents[1]
S01 = ROOT / "traces" / "S01" / "run_0_crash"
S04B = ROOT / "traces" / "S04" / "run_0_b_rear_first"
S12 = ROOT / "traces" / "S12" / "run_0_crash"


def _free_port_pair():
    for port in range(47900, 48900, 2):
        sockets = []
        try:
            for p in (port, port + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sockets.append(s)
                s.bind(("127.0.0.1", p))
            return port
        except OSError:
            continue
        finally:
            for s in sockets:
                s.close()
    raise RuntimeError("no free port pair")


class Messages(unittest.TestCase):
    def test_a_clock_message_carries_only_the_instant_the_play_state_the_speed_and_a_command_number(self):
        message = decode(encode(2031.25, True, 0.5, 3))
        self.assertEqual(message, {"type": "clock", "t_recording": 2031.25, "playing": True, "speed": 0.5, "n": 3})
        self.assertEqual(set(json.loads(encode(1.0, False, 1.0).decode("utf-8"))),
                         {"type", "t_recording", "playing", "speed", "n"})

    def test_a_view_message_carries_only_the_camera(self):
        view = {"camera": "follow", "selected": "A", "heading": 10.0, "elevation": 30.0, "zoom": 1.0, "orbit": 0.0,
                "distance": 9.0, "free": None, "position": [1.0, 2.0]}
        message = decode(encode_view(view))
        self.assertEqual(set(message), {"type", "camera", "selected", "heading", "elevation", "zoom", "orbit",
                                        "distance", "free"})
        self.assertEqual(decode(encode_quit()), {"type": "quit"})

    def test_the_two_ends_talk_both_ways(self):
        port = _free_port_pair()
        lead, follow = SyncPeer(*lead_ports(port)), SyncPeer(*follow_ports(port))
        try:
            lead.send(encode(10.0, True, 0.5))
            follow.send(encode_quit())
            received = {"follow": [], "lead": []}
            for _ in range(200):
                received["follow"] += follow.received()
                received["lead"] += lead.received()
                if received["follow"] and received["lead"]:
                    break
            self.assertEqual(received["follow"][0]["t_recording"], 10.0)
            self.assertEqual(received["lead"][0], {"type": "quit"})
        finally:
            lead.close()
            follow.close()


class Clocks(unittest.TestCase):
    def _first_contact_recording_time(self, run_dir):
        truth = load_ground_truth_run(run_dir)
        return truth, truth.recording_time(truth.contact_zero)

    def test_the_ground_truth_viewer_runs_on_the_simulator_clock(self):
        truth, t = self._first_contact_recording_time(S01)
        self.assertAlmostEqual(truth.replay_time_of(t), truth.contact_zero, places=6)
        self.assertAlmostEqual(truth.display_time(truth.replay_time_of(t)), 0.0, places=6)

    def test_the_same_instant_in_the_reconstruction_viewer(self):
        # S01: the reconstruction's t_global = 0 is the first contact; S04 b_rear_first: it is the strongest
        # contact, 1.55 s after the first one (docs/REPLAY.md).
        for run_dir, expected in ((S01, 0.0), (S04B, -1.55)):
            _, t = self._first_contact_recording_time(run_dir)
            rec = ReplayRun.load(run_dir)
            self.assertAlmostEqual(rec.display_time(rec.replay_time_of(t)), expected, delta=0.01, msg=str(run_dir))
            self.assertAlmostEqual(rec.recording_time(rec.replay_time_of(t)), t, places=6)


class Following(unittest.TestCase):
    def test_the_follower_takes_the_leaders_instant_play_state_and_speed(self):
        truth = load_ground_truth_run(S01)
        clock = PlaybackClock(truth.duration, speed=0.5, start=0.0, playing=True)
        apply_sync(clock, truth, {"t_recording": truth.recording_time(3.0), "playing": False, "speed": 0.25})
        self.assertAlmostEqual(clock.time, 3.0, places=6)
        self.assertFalse(clock.playing)
        self.assertEqual(clock.speed, 0.25)
        apply_sync(clock, truth, {"t_recording": truth.recording_time(4.0), "playing": True, "speed": 1.0})
        self.assertTrue(clock.playing)
        self.assertAlmostEqual(clock.time, 4.0, places=6)


def _script(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BothWindows(unittest.TestCase):
    """The real viewer's handlers, without CARLA or a window: GROUND TRUTH leading, RECONSTRUCTION following."""

    @classmethod
    def setUpClass(cls):
        cls.replay_run = _script("replay_run")
        cls.truth, cls.rec = load_ground_truth_run(S12), ReplayRun.load(S12)

    def _app(self, run, peer, leading):
        app = object.__new__(self.replay_run.ReplayApp)
        app.run, app.peer, app.leading = run, peer, leading
        app.commands, app.command_sent, app.synced, app.running = 0, 0.0, False, True
        app.ids = [p.participant_id for p in run.participants]
        recorders = getattr(run, "recorders", None) or app.ids
        app.view_ids = [pid for pid in app.ids if pid in recorders]
        app.clock = PlaybackClock(run.duration, speed=0.5, start=1.0, playing=True)
        app.camera_mode, app.selected, app.free, app.camera_pose = "overview", app.ids[0], None, None
        app.heading, app.elevation, app.zoom, app.follow_orbit, app.follow_distance = 0.0, 30.0, 1.0, 0.0, 9.0
        return app

    def setUp(self):
        port = _free_port_pair()
        self.lead = self._app(self.truth, SyncPeer(*lead_ports(port)), True)
        self.follow = self._app(self.rec, SyncPeer(*follow_ports(port)), False)

    def tearDown(self):
        self.lead.peer.close()
        self.follow.peer.close()

    def _frame(self, app, act=None, now=10.0):
        before = (app._clock_state(), app._view_state())
        if act is not None:
            act(app)
        followed = app._exchange(before, now)
        if app.leading:
            app.peer.send(encode(app.run.recording_time(app.clock.time), app.clock.playing, app.clock.speed,
                                 app.commands))
        return followed

    def _settle(self, frames=20):
        for _ in range(frames):
            self._frame(self.lead)
            self._frame(self.follow)

    def test_the_ground_truth_camera_moves_over_the_recorders_only(self):
        self.assertIn("C", self.lead.ids)  # S12: C records nothing; the ground truth shows it
        self.assertEqual((self.lead.view_ids, self.follow.view_ids), (["A", "B"], ["A", "B"]))

    def test_c_in_the_follower_changes_the_camera_of_both(self):
        def press_c(app):
            app.camera_mode, app.selected = self.replay_run.next_camera(app.view_ids, app.camera_mode, app.selected)
        self._frame(self.follow, press_c)
        self._settle()
        self.assertEqual((self.lead.camera_mode, self.lead.selected), ("follow", "A"))
        self._frame(self.lead, press_c)
        self._settle()
        self.assertEqual((self.follow.camera_mode, self.follow.selected), ("follow", "B"))

    def test_a_pause_and_a_seek_in_the_follower_reach_the_leader(self):
        self._settle()
        def pause_and_seek(app):
            app.clock.pause()
            app.clock.seek_to(app.clock.time + 2.0)
        self._frame(self.follow, pause_and_seek)
        wanted = self.rec.recording_time(self.follow.clock.time)
        self._settle()
        self.assertFalse(self.lead.clock.playing)
        self.assertAlmostEqual(self.truth.recording_time(self.lead.clock.time), wanted, places=6)
        self.assertFalse(self.follow.clock.playing)
        self.assertAlmostEqual(self.rec.recording_time(self.follow.clock.time), wanted, places=6)

    def test_the_follower_keeps_its_command_until_the_leader_applied_it(self):
        self._settle()
        self._frame(self.follow, lambda app: app.clock.set_speed(1.0))
        stale = encode(self.truth.recording_time(self.lead.clock.time), True, 0.5, 0)
        self.lead.peer.send(stale)  # sent before the leader read the command
        self._frame(self.follow)
        self.assertEqual(self.follow.clock.speed, 1.0)
        self._settle()
        self.assertEqual((self.lead.clock.speed, self.follow.clock.speed), (1.0, 1.0))

    def test_escape_in_either_window_closes_both(self):
        self.follow._quit()
        self._frame(self.lead)
        self.assertFalse(self.lead.running)
        port = _free_port_pair()
        self.lead.peer.close()
        self.follow.peer.close()
        self.lead = self._app(self.truth, SyncPeer(*lead_ports(port)), True)
        self.follow = self._app(self.rec, SyncPeer(*follow_ports(port)), False)
        self.lead._quit()
        self._frame(self.follow)
        self.assertFalse(self.follow.running)

    def test_a_vehicle_that_records_nothing_never_crosses(self):
        self.lead.selected = "C"
        self.assertIsNone(self.lead._view_state()["selected"])

    def test_tab_side_by_side_selects_only_the_vehicles_both_viewers_replay(self):
        from types import SimpleNamespace
        pg = SimpleNamespace(K_ESCAPE=1, K_SPACE=2, K_r=3, K_LEFT=4, K_RIGHT=5, K_KP1=6, K_KP2=7, K_KP3=8, K_KP4=9,
                             K_1=10, K_2=11, K_3=12, K_4=13, K_c=14, K_TAB=15, K_n=16, K_p=17, K_t=18, K_g=19,
                             K_h=20, K_f=21, K_PAGEUP=22, K_PAGEDOWN=23, KMOD_SHIFT=1)
        app = self.lead  # GROUND TRUTH of S12: A and B record, C does not
        app.pygame, app.event_scroll, app.selected = pg, 0, "A"
        seen = []
        for _ in range(3):
            app._on_key(pg.K_TAB, 0)
            seen.append(app.selected)
        self.assertEqual(seen, ["B", "A", "B"])


class Launch(unittest.TestCase):
    def test_both_viewers_take_the_sync_options(self):
        replay_run = _script("replay_run")
        args = replay_run.parse_args(["traces/S01/run_0_crash", "--sync-lead", "47811"])
        self.assertEqual((args.sync_lead, args.sync_follow), (47811, None))
        args = replay_run.parse_args(["traces/S01/run_0_crash", "--sync-follow", "47811"])
        self.assertEqual((args.sync_lead, args.sync_follow), (None, 47811))

    def test_the_menu_opens_both_viewers_side_by_side_on_two_servers(self):
        menu = _script("review_canonical_runs")
        (gt_cmd, gt_env), (rec_cmd, rec_env) = menu.side_by_side(S01, ["--speed", "0.25", "--res", "960x540"],
                                                                 gt_port=3100, rec_port=3000, sync_port=47811)
        self.assertTrue(gt_cmd[1].endswith("view_ground_truth.py") and rec_cmd[1].endswith("replay_run.py"))
        self.assertEqual(gt_cmd[gt_cmd.index("--port") + 1], "3100")
        self.assertEqual(rec_cmd[rec_cmd.index("--port") + 1], "3000")
        self.assertEqual(gt_cmd[gt_cmd.index("--sync-lead") + 1], "47811")
        self.assertEqual(rec_cmd[rec_cmd.index("--sync-follow") + 1], "47811")
        self.assertEqual((gt_env["SDL_VIDEO_WINDOW_POS"], rec_env["SDL_VIDEO_WINDOW_POS"]), ("0,40", "970,40"))
        self.assertIn("--speed", rec_cmd)


if __name__ == "__main__":
    unittest.main()
