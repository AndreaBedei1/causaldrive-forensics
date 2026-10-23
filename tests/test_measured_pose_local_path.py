"""Under a perturbed GNSS/INS the local reconstruction reads the measured pose, never the exact one."""

import math
import unittest
from pathlib import Path

from cdf.reconstruction.common_frame import RecordedPoseSource
from cdf.reconstruction.local import read_jsonl
from cdf.reconstruction.pipeline import measured_ego_records
from cdf.robustness.perturb import GNSS_PROFILES, PerturbedPoseSource

RUN = Path(__file__).resolve().parents[1] / "traces" / "S01" / "run_0_crash" / "vehicles" / "A"


@unittest.skipUnless((RUN / "ego.jsonl").exists(), "canonical S01 recording not present")
class MeasuredPoseTests(unittest.TestCase):
    def test_recorded_source_leaves_the_recorded_stream(self):
        self.assertIsNone(measured_ego_records(RUN, None))
        self.assertIsNone(measured_ego_records(RUN, RecordedPoseSource.from_vehicle_dir))

    def test_degraded_source_reaches_every_local_record(self):
        exact = sorted(read_jsonl(RUN / "ego.jsonl"), key=lambda r: float(r["timestamp"]))
        measured = measured_ego_records(RUN, PerturbedPoseSource.factory(GNSS_PROFILES["degraded"], 7))
        self.assertEqual(len(measured), len(exact))
        errors = [math.hypot(m["x"] - e["x"], m["y"] - e["y"]) for m, e in zip(measured, exact)]
        self.assertGreater(min(errors), 0.0)  # bias + Gauss-Markov: no sample is left exact
        self.assertLess(max(errors), 2.0)
        self.assertEqual([m["timestamp"] for m in measured], [e["timestamp"] for e in exact])
        self.assertEqual([m["z"] for m in measured], [e["z"] for e in exact])  # attitude/height kept (documented)


if __name__ == "__main__":
    unittest.main()
