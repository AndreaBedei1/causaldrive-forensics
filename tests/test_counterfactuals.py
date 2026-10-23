"""The privileged summary of a scenario run and its offline counterfactual runs (scripts/counterfactuals.py),
read by the S12 worked example."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _script(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cf = _script("counterfactuals")


def _write(path: Path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _run(root: Path, closing_mps=2.0, collisions=(), triggers=()):
    """A (actor 1) at x = 0 and B (actor 2) ahead at x = 10 - closing * t, both 4 m x 2 m, for 2 s at 20 Hz."""
    gt = root / "ground_truth"
    gt.mkdir(parents=True)
    states = []
    for k in range(41):
        t = 100.0 + 0.05 * k
        for pid, actor, x in (("A", 1, 0.0), ("B", 2, 10.0 - closing_mps * 0.05 * k)):
            states.append({"participant_id": pid, "actor_id": actor, "timestamp": t,
                           "transform": {"x": x, "y": 0.0, "yaw_deg": 0.0}, "bbox_extent": {"x": 2.0, "y": 1.0},
                           "velocity": {"x": 0.0, "y": 0.0}})
    _write(gt / "states.jsonl", states)
    _write(gt / "collisions.jsonl", list(collisions))
    _write(gt / "triggers.jsonl", list(triggers))
    (gt / "metadata.json").write_text(json.dumps({"participants": [{"participant_id": "A", "record": True},
                                                                   {"participant_id": "B", "record": True}]}),
                                      encoding="utf-8")
    return root


class RunSummary(unittest.TestCase):
    def test_smallest_box_gap_of_each_pair_and_when(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = cf.run_summary(_run(Path(tmp)))
        # centre distance 10 - 2 t, boxes 4 m long: gap 6 - 2 t, smallest at t = 2 s
        self.assertAlmostEqual(summary["box_gaps"]["A-B"]["min_box_gap_m"], 2.0, delta=0.06)
        self.assertAlmostEqual(summary["box_gaps"]["A-B"]["at_s"], 2.0)
        self.assertEqual(summary["participants"], ["A", "B"])
        self.assertAlmostEqual(summary["recorded_duration_s"], 2.0)
        self.assertEqual(summary["collisions"], {})

    def test_vehicle_vehicle_contacts_by_pair(self):
        rows = [{"participant_id": "A", "other_actor_id": 2, "impulse": 300.0, "timestamp": 100.5},
                {"participant_id": "B", "other_actor_id": 1, "impulse": 300.0, "timestamp": 100.5},
                {"participant_id": "A", "other_actor_id": 2, "impulse": 900.0, "timestamp": 100.8},
                {"participant_id": "A", "other_actor_id": 77, "impulse": 50.0, "timestamp": 101.0}]  # a prop
        with tempfile.TemporaryDirectory() as tmp:
            summary = cf.run_summary(_run(Path(tmp), closing_mps=4.0, collisions=rows))
        self.assertEqual(summary["collisions"], {"A-B": {"first_s": 0.5, "last_s": 0.8, "peak_impulse_Ns": 900.0}})
        self.assertEqual(summary["box_gaps"]["A-B"]["min_box_gap_m"], 0.0)

    def test_lateral_departure_of_each_vehicle_from_its_initial_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = _run(Path(tmp))
            path = run / "ground_truth" / "states.jsonl"
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            for row in rows:  # B drifts to its left (CARLA: y to the right), 0.5 m/s
                if row["participant_id"] == "B":
                    row["transform"]["y"] = -0.5 * (row["timestamp"] - 100.0)
            _write(path, rows)
            summary = cf.run_summary(run)
        self.assertAlmostEqual(summary["B_max_left_departure_m"], 1.0, places=2)
        self.assertEqual(summary["B_max_right_departure_m"], 0.0)
        self.assertEqual((summary["A_max_left_departure_m"], summary["A_max_right_departure_m"]), (0.0, 0.0))

    def test_triggers_that_fired(self):
        trigger = {"action_id": "A_swerve", "participant_id": "A", "t_scenario": 0.4, "action_t_start": 0.75,
                   "measured": {"front_clearance_m": 2.5}, "frame": 7, "timestamp": 100.4, "trigger": {"kind": "x"}}
        with tempfile.TemporaryDirectory() as tmp:
            summary = cf.run_summary(_run(Path(tmp), triggers=[trigger]))
        self.assertEqual(summary["triggers_fired"], [{"action_id": "A_swerve", "participant_id": "A", "t_scenario": 0.4,
                                                      "action_t_start": 0.75, "measured": {"front_clearance_m": 2.5}}])


if __name__ == "__main__":
    unittest.main()
