"""The RECONSTRUCTION viewer draws each recorder at the pose the reconstruction used (requirement: never the
simulator's exact pose when the algorithm worked on a measured one).  In G0 that pose is the recorded
synthetic GNSS/INS stream itself; when the pose source differs (perturbed GNSS, mutual refinement) the
reconstruction writes the poses it used to ``global/recorder_poses.json`` and the viewer reads them."""

import json
import tempfile
import unittest
from pathlib import Path

from synthetic_run import make_run

from src.cdf.reconstruction.config import load_config
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.replay.model import ReplayRun
from src.cdf.robustness.perturb import GNSS_PROFILES, PerturbedPoseSource


def _ego(run: Path, recorder: str):
    with (run / "vehicles" / recorder / "ego.jsonl").open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


class RecorderPoseOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.g0 = make_run(root / "g0")
        reconstruct_run(cls.g0, load_config())
        cls.degraded = make_run(root / "degraded")
        cls.pose = staticmethod(PerturbedPoseSource.factory(GNSS_PROFILES["degraded"], 3))
        reconstruct_run(cls.degraded, load_config(), pose_factory=cls.pose)
        cls.poses_file = cls.degraded / "reconstruction" / "global" / "recorder_poses.json"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_a_g0_reconstruction_writes_no_pose_file(self):
        self.assertFalse((self.g0 / "reconstruction" / "global" / "recorder_poses.json").exists())

    def test_a_perturbed_reconstruction_writes_the_poses_it_used(self):
        record = json.loads(self.poses_file.read_text(encoding="utf-8"))
        entities = json.loads((self.degraded / "reconstruction" / "global" / "anonymous_entities.json")
                              .read_text(encoding="utf-8"))
        refinement = entities.get("mutual_refinement") or {}
        for recorder in ("A", "B"):
            ego = _ego(self.degraded, recorder)
            used = record["recorders"][recorder]
            self.assertEqual(len(used["t_local"]), len(ego))
            source = self.pose(self.degraded / "vehicles" / recorder, float(ego[0]["timestamp"]))
            dx, dy = refinement["offsets_m"][recorder] if refinement.get("applied") else (0.0, 0.0)
            for k in (0, len(ego) // 2, len(ego) - 1):
                expected = source.pose_at(used["t_local"][k])
                self.assertAlmostEqual(used["x"][k], expected.x + dx, places=6)
                self.assertAlmostEqual(used["y"][k], expected.y + dy, places=6)
            # not the recorded (exact) stream
            self.assertGreater(max(abs(x - float(e["x"])) for x, e in zip(used["x"], ego)), 0.01)

    def test_the_viewer_draws_recorders_at_the_poses_the_reconstruction_used(self):
        record = json.loads(self.poses_file.read_text(encoding="utf-8"))
        run = ReplayRun.load(self.degraded)
        for participant in run.participants:
            used = record["recorders"][participant.participant_id]
            drawn = participant.trajectory
            self.assertEqual(len(drawn.poses), len(used["x"]))
            for k in (0, len(used["x"]) // 2, len(used["x"]) - 1):
                self.assertAlmostEqual(drawn.poses[k].x, used["x"][k], places=6)
                self.assertAlmostEqual(drawn.poses[k].y, used["y"][k], places=6)


if __name__ == "__main__":
    unittest.main()
