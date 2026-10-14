"""A recorder's identity is exclusive per observer at every instant (anonymous.exclusive_recorder_links)."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.anonymous import ASSOCIATED, CommonView, RecorderLink, exclusive_recorder_links
from src.cdf.reconstruction.config import load_config
from test_retrospective import straight, track

ROOT = Path(__file__).resolve().parents[1]


def link(name, recorder="C", sigma=0.5, within=0.95, samples=20):
    return RecorderLink(name, recorder, samples, 0.1, sigma, 0.1, within, True)


def tracks(*specs):
    """(observer, id, start x, t0, samples, lateral) -> CommonTrack driving along x at 10 m/s, seen from behind."""
    out = []
    for observer, name, x0, t0, n, y in specs:
        out.append(track(observer, name, straight([x0, y], n), 0.0, [x0 - 15.0, 0.0], t0=t0))
    return out


class ExclusivityTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config()

    def run_rule(self, view_tracks, links, same):
        return exclusive_recorder_links(CommonView(view_tracks, {}), links, self.cfg, same_body=lambda a, b, recorder: same)

    def test_a_footprint_link_competing_with_a_collision_decision_is_refused(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 21.0, 0.2, 20, 0.0))
        t1.status, t1.entity = ASSOCIATED, "C"
        kept, refused = self.run_rule([t1, t2], [link("A:t2")], same=False)
        self.assertEqual(kept, [])
        self.assertEqual([r["track"] for r in refused], ["A:t2"])
        self.assertIn("no same-body", refused[0]["reason"])

    def test_a_true_same_body_split_keeps_both(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 21.0, 0.2, 20, 0.0))
        t1.status, t1.entity = ASSOCIATED, "C"
        kept, refused = self.run_rule([t1, t2], [link("A:t2")], same=True)
        self.assertEqual([k.track for k in kept], ["A:t2"])
        self.assertEqual(refused, [])

    def test_ambiguous_footprint_links_are_both_refused(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 20.0, 0.0, 30, 3.5))
        kept, refused = self.run_rule([t1, t2], [link("A:t1", sigma=0.6, within=0.95),
                                                 link("A:t2", sigma=0.5, within=0.90)], same=False)
        self.assertEqual(kept, [])
        self.assertEqual(sorted(r["track"] for r in refused), ["A:t1", "A:t2"])

    def test_a_dominating_link_keeps_the_recorder(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 20.0, 0.0, 30, 3.5))
        kept, refused = self.run_rule([t1, t2], [link("A:t1", sigma=0.2, within=1.0),
                                                 link("A:t2", sigma=1.5, within=0.85)], same=False)
        self.assertEqual([k.track for k in kept], ["A:t1"])
        self.assertEqual([r["track"] for r in refused], ["A:t2"])

    def test_a_reacquisition_after_a_gap_does_not_compete(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 20, 0.0), ("A", "t2", 32.0, 1.5, 20, 0.0))
        t1.status, t1.entity = ASSOCIATED, "C"
        kept, refused = self.run_rule([t1, t2], [link("A:t2")], same=False)
        self.assertEqual([k.track for k in kept], ["A:t2"])
        self.assertEqual(refused, [])

    def test_different_observers_never_compete(self):
        t1, t2 = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("B", "t1", 20.0, 0.0, 30, 0.0))
        kept, refused = self.run_rule([t1, t2], [link("A:t1"), link("B:t1")], same=False)
        self.assertEqual(len(kept), 2)
        self.assertEqual(refused, [])

    def test_real_split_evidence_one_body_versus_two_cars(self):
        # One body seen as two tracks (identical returns) passes the split test; two cars 3.5 m apart do not.
        a, b = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 20.0, 0.0, 30, 0.0))
        a.status, a.entity = ASSOCIATED, "C"
        kept, refused = exclusive_recorder_links(CommonView([a, b], {}), [link("A:t2")], self.cfg)
        self.assertEqual((len(kept), refused), (1, []))
        c, d = tracks(("A", "t1", 20.0, 0.0, 30, 0.0), ("A", "t2", 20.0, 0.0, 30, 3.5))
        c.status, c.entity = ASSOCIATED, "C"
        kept, refused = exclusive_recorder_links(CommonView([c, d], {}), [link("A:t2")], self.cfg)
        self.assertEqual((kept, [r["track"] for r in refused]), ([], ["A:t2"]))


class S11RecordedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="excl_"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def reconstruct(self):
        from src.cdf.reconstruction.pipeline import reconstruct_run
        if getattr(type(self), "_fresh", None) is None:
            src = ROOT / "traces/S11/run_0_consequential"
            dst = self.tmp / "run"
            shutil.copytree(src / "vehicles", dst / "vehicles")
            for name in ("metadata.json", "incident_context.json"):
                shutil.copy2(src / name, dst / name)
            reconstruct_run(dst, load_config())
            type(self)._fresh = json.loads((dst / "reconstruction/global/associations.json").read_text())
        return type(self)._fresh

    def test_s11_reconstruction_matches_the_committed_one(self):
        committed = json.loads((ROOT / "traces/S11/run_0_consequential/reconstruction/global/associations.json").read_text())
        fresh = self.reconstruct()
        self.assertEqual([(a["local_graph"], a["local_track"], a["global_entity"]) for a in committed],
                         [(a["local_graph"], a["local_track"], a["global_entity"]) for a in fresh])

    def test_s11_has_one_c_claim_per_observer(self):
        fresh = self.reconstruct()
        per_observer = {}
        for a in fresh:
            if a["global_entity"] == "C":
                per_observer.setdefault(a["local_graph"], []).append(a["local_track"])
        self.assertTrue(per_observer)
        self.assertTrue(all(len(v) == 1 for v in per_observer.values()), per_observer)

if __name__ == "__main__":
    unittest.main()
