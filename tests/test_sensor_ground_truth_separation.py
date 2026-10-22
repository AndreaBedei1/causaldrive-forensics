"""Sensor / ground-truth separation (docs/SENSORS_AND_GROUND_TRUTH.md): what the recorders' own files carry in
the canonical set, and that the reconstruction does not use the simulator's frame counter, a bookkeeping field
shared by every vehicle (a perfect common clock no real recorder has)."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from synthetic_run import make_run

from src.cdf.evaluation.run_metrics import graph_signature
from src.cdf.reconstruction.config import load_config
from src.cdf.reconstruction.pipeline import reconstruct_run

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = sorted(p.parent for p in (ROOT / "traces").glob("S*/run_0_*/metadata.json"))


def _jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


class RecorderFilesOfTheCanonicalSet(unittest.TestCase):
    def test_the_canonical_set_has_22_runs(self):
        self.assertEqual(len(CANONICAL), 22)

    def test_recorder_collision_records_carry_no_partner_identity(self):
        for run in CANONICAL:
            for path in (run / "vehicles").glob("*/collisions.jsonl"):
                for row in _jsonl(path):
                    self.assertEqual(set(row), {"frame", "timestamp", "impulse"}, str(path))

    def test_recorder_pose_streams_carry_the_declared_pose_sensor_fields_only(self):
        for run in CANONICAL:
            for vehicle in sorted(p for p in (run / "vehicles").iterdir() if (p / "ego.jsonl").exists()):
                declared = json.loads((vehicle / "metadata.json").read_text(encoding="utf-8"))["pose_sensor"]
                with (vehicle / "ego.jsonl").open(encoding="utf-8") as handle:
                    first = json.loads(handle.readline())
                # ``frame``: the simulator's frame counter, bookkeeping the reconstruction never uses (below)
                self.assertEqual(set(first) - {"frame"}, set(declared["fields"]), str(vehicle))
                self.assertEqual((declared["profile"], declared["added_error"]), ("G0", "none"))


def _scramble_frames(run: Path, rng: np.random.Generator) -> int:
    changed = 0
    for path in (run / "vehicles").rglob("*.jsonl"):
        rows = _jsonl(path)
        for row in rows:
            for key in [k for k in row if k == "frame" or k.startswith("frame_")]:
                row[key] = int(rng.integers(0, 10 ** 9))
                changed += 1
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    for path in (run / "vehicles").rglob("observations.npz"):
        with np.load(str(path)) as data:
            arrays = {key: data[key] for key in data.files}
        arrays["frames"] = rng.integers(0, 10 ** 9, len(arrays["frames"])).astype(np.int64)
        changed += len(arrays["frames"])
        np.savez_compressed(str(path), **arrays)
    return changed


class SimulatorFrameCounter(unittest.TestCase):
    def test_the_reconstruction_ignores_the_simulator_frame_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp) / "run")
            scrambled = Path(tmp) / "scrambled"
            shutil.copytree(str(run), str(scrambled))
            self.assertGreater(_scramble_frames(scrambled, np.random.default_rng(5)), 100)
            graphs = []
            for path in (run, scrambled):
                reconstruct_run(path, load_config())
                graphs.append(json.loads((path / "reconstruction" / "global" / "global_graph.json")
                                         .read_text(encoding="utf-8")))
        self.assertTrue(graphs[0]["nodes"])
        self.assertEqual(graph_signature(graphs[1]), graph_signature(graphs[0]))


if __name__ == "__main__":
    unittest.main()
