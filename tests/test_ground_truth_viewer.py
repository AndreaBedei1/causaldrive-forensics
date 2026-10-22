"""The GROUND TRUTH viewer model reads ground_truth/ only and shows every vehicle and every contact episode."""

import builtins
import json
import unittest
from pathlib import Path
from unittest import mock

from cdf.replay.ground_truth import CONTACT_GAP_S, contact_episodes, load_ground_truth_run

RUN = Path(__file__).resolve().parents[1] / "traces" / "S12" / "run_0_crash"


@unittest.skipUnless((RUN / "ground_truth" / "states.jsonl").exists(), "canonical S12 recording not present")
class GroundTruthViewerTests(unittest.TestCase):
    def test_reads_nothing_but_ground_truth(self):
        real_open, opened = builtins.open, []

        def guarded(path, *args, **kwargs):
            opened.append(str(path))
            if "reconstruction" in str(path) or "vehicles" in str(path):
                raise AssertionError("ground-truth viewer opened " + str(path))
            return real_open(path, *args, **kwargs)

        with mock.patch("builtins.open", guarded), mock.patch("io.open", guarded):
            run = load_ground_truth_run(RUN)
        self.assertTrue(run.participants)

    def test_every_true_vehicle_is_drawn_including_non_recorders(self):
        run = load_ground_truth_run(RUN)
        ids = {json.loads(line)["participant_id"] for line in (RUN / "ground_truth" / "states.jsonl").open()}
        self.assertEqual({p.participant_id for p in run.participants}, ids)
        self.assertTrue(set(run.recorders) < ids, "S12 has a vehicle that records nothing")

    def test_clock_is_zero_at_the_first_true_contact(self):
        run = load_ground_truth_run(RUN)
        self.assertTrue(run.collisions)
        self.assertEqual(run.display_time(run.collisions[0].time), 0.0)


class ContactEpisodeTests(unittest.TestCase):
    def test_callbacks_closer_than_the_gap_are_one_episode_and_mutual_callbacks_count_once_per_pair(self):
        ids = {1: "A", 2: "B"}
        rows = [{"participant_id": "A", "other_actor_id": 2, "timestamp": 10.0 + 0.05 * k, "impulse": 1.0}
                for k in range(4)]
        rows += [{"participant_id": "B", "other_actor_id": 1, "timestamp": 10.0, "impulse": 1.0}]
        rows += [{"participant_id": "A", "other_actor_id": 2, "timestamp": 10.15 + CONTACT_GAP_S + 0.1, "impulse": 1.0}]
        vehicles, static = contact_episodes(rows, ids, start=10.0)
        self.assertEqual([(e.pair, e.start) for e in vehicles], [(("A", "B"), 0.0), (("A", "B"), 0.75)])
        self.assertEqual(static, [])


if __name__ == "__main__":
    unittest.main()
