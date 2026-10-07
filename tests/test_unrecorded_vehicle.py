"""record: false participants, privileged triggers, and the recorded S17 run (no CARLA needed)."""

import json
import math
import unittest
from pathlib import Path

from src.cdf.common.config import Config, load_run_config
from src.cdf.simulation.controllers import RoutePlan, ScriptedAction, ScriptedController, VehicleState
from src.cdf.simulation.runner import _scheduled_end
from src.cdf.simulation.scenario_base import ParticipantSpec, ScenarioSpec
from src.cdf.simulation.triggers import ActionTrigger, Pose, envelope_entry, fire_due_triggers

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"


def read_jsonl(path):
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


class EnvelopeTriggerTests(unittest.TestCase):
    owner = Pose(x=0.0, y=0.0, yaw_deg=0.0, half_length=2.1, half_width=1.0)

    def target(self, x, y, yaw=0.0):
        return Pose(x=x, y=y, yaw_deg=yaw, half_length=2.4, half_width=0.95)

    def test_corridor_ahead_of_the_front_face(self):
        self.assertTrue(envelope_entry(self.owner, self.target(8.0, 0.0), 12.0, 0.2))
        self.assertTrue(envelope_entry(self.owner, self.target(8.0, 2.1), 12.0, 0.2))   # left edge at 1.15
        self.assertFalse(envelope_entry(self.owner, self.target(8.0, 2.3), 12.0, 0.2))  # left edge at 1.35
        self.assertFalse(envelope_entry(self.owner, self.target(17.0, 0.0), 12.0, 0.2))  # beyond 2.1 + 12
        self.assertFalse(envelope_entry(self.owner, self.target(-6.0, 0.0), 12.0, 0.2))  # behind
        self.assertFalse(envelope_entry(self.owner, self.target(8.0, 3.5), 12.0, 0.2))  # next lane

    def test_corridor_turns_with_the_owner(self):
        owner = Pose(x=10.0, y=5.0, yaw_deg=90.0, half_length=2.1, half_width=1.0)  # heading +y
        self.assertTrue(envelope_entry(owner, self.target(10.0, 13.0, 90.0), 12.0, 0.2))
        self.assertFalse(envelope_entry(owner, self.target(18.0, 5.0, 90.0), 12.0, 0.2))

    def test_armed_action_fires_once_and_starts_after_the_reaction(self):
        trigger = ActionTrigger(kind="envelope_entry", target="C", ahead_m=12.0, lateral_margin_m=0.2,
                                reaction_s=0.4, window_start_s=0.0, window_end_s=8.0)
        action = ScriptedAction("A_swerve", "lane_shift", 0.0, 1.6, {"lateral_m": -3.5}, trigger=trigger)
        self.assertTrue(action.armed)
        self.assertTrue(math.isinf(action.t_start))
        self.assertFalse(action.started(100.0))
        self.assertAlmostEqual(action.latest_end(), 8.0 + 0.4 + 1.6)
        poses = {"A": self.owner, "C": self.target(30.0, 3.5)}
        self.assertEqual(fire_due_triggers(1.0, poses, [("A", action)]), [])
        poses["C"] = self.target(8.0, 1.5)
        fired = fire_due_triggers(3.75, poses, [("A", action)])
        self.assertEqual(len(fired), 1)
        self.assertAlmostEqual(action.t_start, 4.15)
        self.assertFalse(action.armed)
        self.assertEqual(fire_due_triggers(3.80, poses, [("A", action)]), [])
        self.assertTrue(action.active_at(4.2) and not action.active_at(4.1))

    def test_a_trigger_without_its_target_never_fires(self):
        trigger = ActionTrigger(kind="envelope_entry", target="C")
        action = ScriptedAction("A_swerve", "lane_shift", 0.0, 1.6, {"lateral_m": -3.5}, trigger=trigger)
        for t in range(20):
            self.assertEqual(fire_due_triggers(float(t), {"A": self.owner}, [("A", action)]), [])
        self.assertTrue(action.armed)

    def test_an_armed_lane_shift_does_not_move_the_vehicle(self):
        route = RoutePlan(points=[(float(x), 0.0) for x in range(0, 200, 2)])
        trigger = ActionTrigger(kind="envelope_entry", target="C")
        action = ScriptedAction("A_swerve", "lane_shift", 0.0, 1.6, {"lateral_m": -3.5}, trigger=trigger)
        controller = ScriptedController("A", route, 12.0, [action])
        for k in range(40):
            controller.step(VehicleState(t=0.05 * k, x=0.6 * k, y=0.0, yaw=0.0, speed=12.0), 0.05)
        self.assertEqual(controller.lateral_offset, 0.0)
        action.fire(2.0)
        controller.step(VehicleState(t=3.0, x=36.0, y=0.0, yaw=0.0, speed=12.0), 0.05)
        self.assertLess(controller.lateral_offset, -0.1)

    def test_bad_triggers_are_rejected(self):
        with self.assertRaises(ValueError):
            ActionTrigger(kind="telepathy", target="C")
        with self.assertRaises(ValueError):
            ParticipantSpec.from_dict({"id": "A", "actions": [{"action_id": "x", "kind": "lane_shift", "t_start": 1.0,
                                                                "trigger": {"kind": "envelope_entry", "target": "C"}}]})


class S17SpecificationTests(unittest.TestCase):
    def setUp(self):
        self.spec = ScenarioSpec.from_config(load_run_config("S17"))

    def test_c_is_physical_but_not_a_recorder(self):
        self.assertEqual(self.spec.participant_ids, ["A", "B", "C"])
        self.assertEqual(self.spec.recorder_ids, ["A", "B"])
        self.assertFalse(self.spec.participant("C").record)

    def test_a_reacts_to_c_through_a_privileged_trigger(self):
        action = self.spec.participant("A").actions[0]
        self.assertEqual((action.kind, action.trigger.kind, action.trigger.target), ("lane_shift", "envelope_entry", "C"))
        self.assertTrue(action.armed)
        self.assertLess(action.params["lateral_m"], 0.0)  # to the left, into B's lane

    def test_counterfactual_without_c(self):
        counterfactual = self.spec.without(["C"])
        self.assertEqual(counterfactual.participant_ids, ["A", "B"])
        self.assertEqual(_scheduled_end(counterfactual), 8.0 + 0.4 + 1.6)
        with self.assertRaises(KeyError):
            self.spec.without(["D"])

    def test_triggers_must_name_a_participant(self):
        data = load_run_config("S17").data
        data["scenario"]["participants"][0]["actions"][0]["trigger"]["target"] = "Z"
        with self.assertRaises(ValueError):
            ScenarioSpec.from_config(Config(data))


@unittest.skipUnless((S17 / "ground_truth" / "states.jsonl").exists(), "S17 not recorded")
class S17RecordingTests(unittest.TestCase):
    """The recorded run: C drove and was seen, but recorded nothing and is named nowhere admissible."""

    def test_only_recorders_write_data_and_the_run_metadata_lists_only_them(self):
        self.assertEqual(sorted(p.name for p in (S17 / "vehicles").iterdir()), ["A", "B"])
        self.assertEqual(json.loads((S17 / "metadata.json").read_text())["participants"], ["A", "B"])
        truth = json.loads((S17 / "ground_truth" / "metadata.json").read_text())
        self.assertIn({"participant_id": "C", "record": False}, truth["participants"])
        self.assertEqual({s["participant_id"] for s in read_jsonl(S17 / "ground_truth" / "states.jsonl")},
                         {"A", "B", "C"})

    def test_a_and_b_collide_and_nobody_touches_c(self):
        states = read_jsonl(S17 / "ground_truth" / "states.jsonl")
        names = {s["actor_id"]: s["participant_id"] for s in states}
        pairs = set()
        for record in read_jsonl(S17 / "ground_truth" / "collisions.jsonl"):
            pairs.add(tuple(sorted((record["participant_id"], names.get(record["other_actor_id"], "static")))))
        self.assertEqual(pairs, {("A", "B")})

    def test_the_swerve_was_fired_by_c_entering_the_corridor_before_the_collision(self):
        triggers = read_jsonl(S17 / "ground_truth" / "triggers.jsonl")
        self.assertEqual([(t["participant_id"], t["action_id"], t["trigger"]["target"]) for t in triggers],
                         [("A", "A_evasive_swerve_left", "C")])
        states = read_jsonl(S17 / "ground_truth" / "states.jsonl")
        t0 = states[0]["timestamp"]
        first_contact = min(r["timestamp"] for r in read_jsonl(S17 / "ground_truth" / "collisions.jsonl")) - t0
        self.assertLess(triggers[0]["action_t_start"], first_contact - 1.0)

    def test_privileged_counterfactuals_have_no_collision(self):
        summary = json.loads((S17 / "ground_truth" / "counterfactuals.json").read_text())
        self.assertTrue(summary["_notice"].startswith("PRIVILEGED"))
        self.assertEqual(summary["factual"]["collisions"].keys(), {"A-B"})
        for case in ("without_C", "trigger_never_fired"):
            self.assertEqual(summary["counterfactuals"][case]["collisions"], {}, case)
            self.assertEqual(summary["counterfactuals"][case]["triggers_fired"], [], case)

    def test_reconstruction_keeps_c_anonymous(self):
        associations = json.loads((S17 / "reconstruction" / "global" / "associations.json").read_text())
        entities = {(a["local_graph"], a["local_track"]): (a["status"], a["global_entity"]) for a in associations}
        self.assertEqual(entities[("A", "track_001")], ("ANONYMOUS", "A:track_001"))
        self.assertEqual(entities[("A", "track_002")], ("ASSOCIATED", "B"))
        graph = json.loads((S17 / "reconstruction" / "global" / "global_graph.json").read_text())
        mentioned = {n["actor_id"] for n in graph["nodes"]} | {n["subject_id"] for n in graph["nodes"]}
        self.assertNotIn("C", mentioned)
        types = {(n["event_type"], n["subject_id"]) for n in graph["nodes"] if n["actor_id"] == "A"}
        self.assertIn(("CUT_IN_FROM_RIGHT_START", "A:track_001"), types)
        self.assertIn(("EGO_PATH_ENTRY", "A:track_001"), types)
        evaluation = json.loads((S17 / "reconstruction" / "evaluation" / "evaluation.json").read_text())
        verdicts = {row["track"]: (row["true_identity"], row["verdict"]) for row in evaluation["tracks"]}
        self.assertEqual(verdicts["A:track_001"], ("C", "correctly left anonymous"))


if __name__ == "__main__":
    unittest.main()
