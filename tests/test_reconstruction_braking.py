"""BRAKE_EPISODE: one graph node per continuous braking action."""

import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.local import brake_episodes
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory

from synthetic_run import make_run

CLOCK_ORIGIN = 100.0


def _grid(start, end):
    return [round(start + 0.05 * k, 2) for k in range(int(round((end - start) / 0.05)) + 1)]


def _episodes(brake_at, speed_at=lambda t: 10.0, start=5.0, end=9.0):
    """Run the extractor on a 20 Hz profile given as functions of local time."""
    times = _grid(start, end)
    controls = [{"timestamp": CLOCK_ORIGIN + t, "brake": brake_at(t), "throttle": 0.0} for t in times]
    ego = EgoTrajectory([EgoState(t_local=t, x=0.0, y=0.0, heading=0.0, vx=speed_at(t), vy=0.0)
                         for t in times])
    return brake_episodes("A", controls, CLOCK_ORIGIN, ego, SemanticsConfig())


def _example_brake(t):
    """The profile of the task: pressed at 5.55, released at 7.80."""
    fixed = {5.55: 0.72, 5.60: 0.85, 7.70: 0.45, 7.75: 0.20}
    if t in fixed:
        return fixed[t]
    return 0.91 if 5.65 <= t <= 7.65 else 0.0


def _example_speed(t):
    """14 m/s, down to 3 m/s at 7.0 s while braking, back up to 5 m/s at 7.8 s."""
    if t < 5.55:
        return 14.0
    if t <= 7.0:
        return 14.0 - 11.0 * (t - 5.55) / 1.45
    if t <= 7.8:
        return 3.0 + 2.0 * (t - 7.0) / 0.8
    return 5.0


class BrakeEpisodeTests(unittest.TestCase):
    def test_one_continuous_braking_action_is_one_episode(self):
        events = _episodes(_example_brake)
        self.assertEqual([event.type for event in events], ["BRAKE_EPISODE"])
        episode = events[0]
        self.assertEqual(episode.t_local, 5.55)
        self.assertEqual(episode.attributes["start_t_local"], 5.55)
        self.assertEqual(episode.attributes["end_t_local"], 7.80)
        self.assertTrue(episode.attributes["released"])
        self.assertFalse(episode.attributes["began_before_recording"])
        self.assertEqual(episode.attributes["n_samples"], 45)  # 5.55 .. 7.75

    def test_brake_release_brake_gives_two_episodes(self):
        def brake(t):
            return 0.5 if 6.0 <= t < 6.5 else 0.6 if 7.5 <= t < 8.0 else 0.0
        events = _episodes(brake)
        self.assertEqual([(e.attributes["start_t_local"], e.attributes["end_t_local"]) for e in events],
                         [(6.0, 6.5), (7.5, 8.0)])
        self.assertTrue(all(e.attributes["released"] for e in events))

    def test_brief_drop_below_threshold_does_not_split_an_episode(self):
        def brake(t):
            if t in (6.5, 7.0, 7.05, 7.1):  # one-sample and three-sample (0.15 s) dips
                return 0.02
            return 0.8 if 6.0 <= t < 8.0 else 0.0
        events = _episodes(brake)
        self.assertEqual(len(events), 1)
        self.assertEqual((events[0].attributes["start_t_local"], events[0].attributes["end_t_local"]), (6.0, 8.0))

    def test_duration(self):
        self.assertAlmostEqual(_episodes(_example_brake)[0].attributes["duration_s"], 2.25)

    def test_peak_brake(self):
        self.assertEqual(_episodes(_example_brake)[0].attributes["peak_brake"], 0.91)

    def test_mean_brake(self):
        pressed = [0.72, 0.85] + [0.91] * 41 + [0.45, 0.20]  # samples 5.55 .. 7.75
        self.assertAlmostEqual(_episodes(_example_brake)[0].attributes["mean_brake"],
                               round(sum(pressed) / len(pressed), 3))

    def test_speed_start_end_min_and_delta(self):
        attributes = _episodes(_example_brake, _example_speed)[0].attributes
        self.assertEqual(attributes["speed_start_mps"], 14.0)
        self.assertEqual(attributes["speed_end_mps"], 5.0)
        self.assertEqual(attributes["min_speed_mps"], 3.0)
        self.assertEqual(attributes["delta_speed_mps"], -9.0)

    def test_recording_ending_while_braking_is_not_released(self):
        events = _episodes(lambda t: 1.0 if t >= 8.0 else 0.0, end=9.0)
        self.assertEqual(len(events), 1)
        attributes = events[0].attributes
        self.assertFalse(attributes["released"])
        self.assertEqual((attributes["start_t_local"], attributes["end_t_local"]), (8.0, 9.0))
        self.assertAlmostEqual(attributes["duration_s"], 1.0)

    def test_braking_already_active_when_recording_starts_is_flagged(self):
        events = _episodes(lambda t: 0.7 if t < 6.0 else 0.0)
        self.assertEqual(len(events), 1)
        self.assertTrue(events[0].attributes["began_before_recording"])
        self.assertEqual(events[0].attributes["end_t_local"], 6.0)


class BrakeEpisodePipelineTests(unittest.TestCase):
    def test_brake_onset_no_longer_appears_in_reconstructed_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp))
            result = reconstruct_run(run, ReconstructionConfig())
            texts = {path.relative_to(run).as_posix(): path.read_text(encoding="utf-8")
                     for path in (run / "reconstruction").rglob("*") if path.is_file()}
        self.assertTrue(texts)
        for name, text in texts.items():
            self.assertNotIn("BRAKE_ONSET", text, name)
        a = next(local for local in result.locals if local.owner == "A")
        self.assertEqual([n.event_type for n in a.graph.nodes].count("BRAKE_EPISODE"), 1)
        self.assertEqual([n.event_type for n in result.graph.nodes].count("BRAKE_EPISODE"), 1)
        self.assertIn("BRAKE_EPISODE", texts["reconstruction/A/local_graph.dot"])

    def test_local_trace_keeps_every_brake_value_while_the_graph_has_one_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp))
            reconstruct_run(run, ReconstructionConfig())
            frames = [json.loads(line) for line in
                      (run / "reconstruction" / "A" / "local_trace.jsonl").read_text().splitlines()]
            graph = json.loads((run / "reconstruction" / "A" / "local_graph.json").read_text())
        braking_frames = [frame["t_local"] for frame in frames for fact in frame["facts"]
                          if fact["type"] == "EGO_CONTROL" and fact["attributes"]["brake"] >= 0.1]
        # A brakes at 0.8 from t = 3.0 s to the end of its 6 s recording.
        self.assertEqual(len(braking_frames), 31)
        self.assertEqual((braking_frames[0], braking_frames[-1]), (3.0, 6.0))
        episodes = [node for node in graph["nodes"] if node["event_type"] == "BRAKE_EPISODE"]
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["attributes"]["n_samples"], 61)  # raw 20 Hz samples, one node
        self.assertFalse(episodes[0]["attributes"]["released"])


if __name__ == "__main__":
    unittest.main()
