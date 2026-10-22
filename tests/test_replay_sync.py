"""Two viewers side by side (GROUND TRUTH and RECONSTRUCTION), synchronised in time.  The leader sends only the
instant it shows on the recording clock (in G0 the recorders' clocks are the simulator's), whether it plays and its
speed; the follower maps that instant through its own clock.  Nothing else crosses: no position, identity or
event, so neither viewer reads the other's data."""

import json
import unittest
from pathlib import Path

from src.cdf.replay.ground_truth import load_ground_truth_run
from src.cdf.replay.model import PlaybackClock, ReplayRun
from src.cdf.replay.sync import SyncReceiver, SyncSender, apply_sync, decode, encode

ROOT = Path(__file__).resolve().parents[1]
S01 = ROOT / "traces" / "S01" / "run_0_crash"
S04B = ROOT / "traces" / "S04" / "run_0_b_rear_first"


class Messages(unittest.TestCase):
    def test_a_message_carries_only_the_instant_the_play_state_and_the_speed(self):
        message = decode(encode(2031.25, True, 0.5))
        self.assertEqual(message, {"t_recording": 2031.25, "playing": True, "speed": 0.5})
        self.assertEqual(set(json.loads(encode(1.0, False, 1.0).decode("utf-8"))), {"t_recording", "playing", "speed"})

    def test_the_follower_reads_the_latest_message_sent_on_the_local_port(self):
        receiver = SyncReceiver(0)  # any free port
        sender = SyncSender(receiver.port)
        self.assertIsNone(receiver.latest())
        sender.send(10.0, True, 0.5)
        sender.send(10.5, False, 0.25)
        latest = None
        for _ in range(200):
            latest = receiver.latest() or latest
            if latest and latest["t_recording"] == 10.5:
                break
        self.assertEqual(latest, {"t_recording": 10.5, "playing": False, "speed": 0.25})
        sender.close()
        receiver.close()


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
