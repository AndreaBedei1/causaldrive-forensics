"""An identity passed on through another observer's track (identity.inherited_links) needs that track to single its
recorder out.  After observer R collided with X, R's track of X and a track of R itself are one box: a third
observer's track that lies on R's own body after their contact does not inherit X (S06: C's radar track slides from B
onto A at the A-B collision and stays on A for 10 s; it used to inherit B through A's track of B)."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from src.cdf.reconstruction.config import load_config
from src.cdf.reconstruction.identity import partner_cannot_single_out
from src.cdf.reconstruction.pipeline import reconstruct_run

ROOT = Path(__file__).resolve().parents[1]
S06 = ROOT / "traces" / "S06" / "run_0_crash"


class _Body:
    """A recorder body on the x axis: a 4 m x 2 m box centred at ``x``."""

    def __init__(self, x, contacts=()):
        self.x, self.contacts = x, tuple(contacts)

    def covers(self, t):
        return True

    def outline_distance(self, t, point):
        dx = max(abs(point[0] - self.x) - 2.0, 0.0)
        dy = max(abs(point[1]) - 1.0, 0.0)
        return float(np.hypot(dx, dy))


def _track(points_after):
    samples = [SimpleNamespace(t_global=t, measured=True, near=np.array(p)) for t, p in points_after]
    return SimpleNamespace(samples=samples)


class Guard(unittest.TestCase):
    def setUp(self):
        # R (observer of the track of X) at x = 0, X at x = 4.2: they touched at t = 5.
        self.bodies = {"R": _Body(0.0, [(5.0, ("X",))]), "X": _Body(4.2, [(5.0, ("R",))])}

    def test_a_track_on_the_observer_after_their_contact_cannot_inherit_its_partner(self):
        track = _track([(t, (-2.0, 0.0)) for t in (5.5, 6.0, 6.5, 7.0)])  # on R's rear edge
        self.assertTrue(partner_cannot_single_out(track, "R", "X", self.bodies))

    def test_a_track_on_the_partner_after_their_contact_still_inherits_it(self):
        track = _track([(t, (6.2, 0.0)) for t in (5.5, 6.0, 6.5, 7.0)])  # on X's front edge
        self.assertFalse(partner_cannot_single_out(track, "R", "X", self.bodies))

    def test_without_a_contact_between_them_nothing_changes(self):
        bodies = {"R": _Body(0.0), "X": _Body(4.2)}
        track = _track([(t, (-2.0, 0.0)) for t in (5.5, 6.0)])
        self.assertFalse(partner_cannot_single_out(track, "R", "X", bodies))


class S06ThirdObserver(unittest.TestCase):
    def test_the_track_that_slides_from_b_onto_a_does_not_inherit_b(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "S06" / "run_0_crash"
            shutil.copytree(str(S06), str(run), ignore=lambda d, names: ["reconstruction"] if Path(d) == S06 else [])
            reconstruct_run(run, load_config())
            associations = json.loads((run / "reconstruction" / "global" / "associations.json").read_text(encoding="utf-8"))
        track = next(a for a in associations if a["local_graph"] == "C" and a["local_track"] == "track_002")
        self.assertNotEqual((track["status"], track["global_entity"]), ("ASSOCIATED", "B"))


if __name__ == "__main__":
    unittest.main()
