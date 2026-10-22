"""A recontact is part of the collision it follows (Andrea's review of S04 a_front_pushed): contacts of one pair less
than ``recontact_max_pause_s`` apart whose two bodies did not part by more than ``recontact_max_separation_m`` in
between are one collision.  The rule holds for the reconstruction (the recorders' own pose streams), the evaluation
(ground truth) and both viewers; a contact after a real separation stays a distinct collision."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.cdf.evaluation.reconstruction import evaluate_run
from src.cdf.reconstruction.config import load_config
from src.cdf.reconstruction.fusion import group_recontacts
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.replay.ground_truth import load_ground_truth_run
from src.cdf.replay.model import ReplayRun

ROOT = Path(__file__).resolve().parents[1]
S04A = ROOT / "traces" / "S04" / "run_0_a_front_pushed"


def _group(contacts, gaps):
    return group_recontacts(contacts, lambda c: c[0], lambda c: c[1],
                            lambda pair, t1, t2: gaps.get((pair, t1, t2)), 2.0, 1.0)


class Grouping(unittest.TestCase):
    def test_a_recontact_after_a_rebound_joins_its_collision(self):
        groups = _group([("AB", 0.0), ("BC", 0.5), ("AB", 0.65)], {("AB", 0.0, 0.65): 0.15})
        self.assertEqual([(g[0], [r[1] for r in rest]) for g, rest in groups], [("AB", [0.65]), ("BC", [])])

    def test_a_contact_after_the_bodies_parted_is_a_new_collision(self):
        groups = _group([("AB", 0.0), ("AB", 0.65)], {("AB", 0.0, 0.65): 3.0})
        self.assertEqual(len(groups), 2)

    def test_a_long_pause_or_an_unknown_separation_keeps_two_collisions(self):
        self.assertEqual(len(_group([("AB", 0.0), ("AB", 2.5)], {("AB", 0.0, 2.5): 0.1})), 2)
        self.assertEqual(len(_group([("AB", 0.0), ("AB", 0.65)], {})), 2)


class S04FrontPushed(unittest.TestCase):
    """A hits B (4.80 s), they rebound 0.15 m, B is pushed into C (5.30 s), A touches B again (5.45 s) and pushes."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.run_dir = Path(cls.tmp.name) / "S04" / "run_0_a_front_pushed"
        shutil.copytree(str(S04A), str(cls.run_dir), ignore=lambda d, names: ["reconstruction"] if Path(d) == S04A else [])
        reconstruct_run(cls.run_dir, load_config())
        cls.graph = json.loads((cls.run_dir / "reconstruction" / "global" / "global_graph.json").read_text(encoding="utf-8"))
        cls.evaluation = evaluate_run(cls.run_dir, clock_shift_check=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_the_reconstruction_has_one_a_b_collision_with_its_recontact(self):
        collisions = [n for n in self.graph["nodes"] if n["event_type"] == "COLLISION"]
        self.assertEqual(sorted(tuple(sorted(n["participants"])) for n in collisions), [("A", "B"), ("B", "C")])
        ab = next(n for n in collisions if sorted(n["participants"]) == ["A", "B"])
        recontacts = ab["attributes"]["recontacts"]
        self.assertEqual(len(recontacts), 1)
        self.assertAlmostEqual(recontacts[0]["t_global"] - ab["t_global"], 0.65, delta=0.06)

    def test_the_evaluation_counts_the_same_collisions(self):
        contacts = self.evaluation["collisions"]
        self.assertEqual(sorted(tuple(c["participants"]) for c in contacts), [("A", "B"), ("B", "C")])
        self.assertTrue(all(c["participants_correct"] for c in contacts))
        self.assertEqual(self.evaluation["extra_collisions"], [])
        ab = next(c for c in contacts if c["participants"] == ["A", "B"])
        self.assertEqual(len(ab["recontacts"]), 1)

    def test_the_reconstruction_viewer_shows_the_recontact_as_such(self):
        run = ReplayRun.load(self.run_dir)
        self.assertEqual(sorted(mark.participants for mark in run.collisions), [("A", "B"), ("B", "C")])
        kinds = sorted(e.event_type for e in run.local_events["A"].events if e.event_type in ("COLLISION", "RECONTACT"))
        self.assertEqual(kinds, ["COLLISION", "RECONTACT"])

    def test_the_ground_truth_viewer_shows_one_collision_and_a_recontact(self):
        truth = load_ground_truth_run(S04A)
        self.assertEqual(sorted(mark.participants for mark in truth.collisions), [("A", "B"), ("B", "C")])
        kinds = [e.event_type for e in truth.local_events["A"].events if "CONTACT" in e.event_type]
        self.assertEqual(kinds, ["CONTACT_START", "CONTACT_END", "RECONTACT_START", "RECONTACT_END"])


if __name__ == "__main__":
    unittest.main()
