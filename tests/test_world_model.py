"""The local semantic world model: perceived state, track loss and STOP-sign knowledge."""

import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.checks import sign_windows
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.local import build_local_graph, number_events, sign_continuity, sign_events
from src.cdf.reconstruction.models import TraceFrame
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory
from src.cdf.reconstruction.world_state import UNKNOWN, PerceivedWorld, Timeline, compact_state

from synthetic_run import CONTACT_T, make_run

ORIGIN = 100.0


def _ego(speed=0.0, end=12.0):
    """The recorder driving straight along its own +x at a constant speed."""
    return EgoTrajectory([EgoState(t_local=round(0.05 * k, 2), x=speed * 0.05 * k, y=0.0, heading=0.0,
                                   vx=speed, vy=0.0) for k in range(int(round(end / 0.05)) + 1)])


class PerceivedStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        run = make_run(Path(cls._tmp.name) / "seen", speed_limit_kmh=30)
        cls.result = reconstruct_run(run, ReconstructionConfig())
        cls.local = {local.owner: local for local in cls.result.locals}
        lost_run = make_run(Path(cls._tmp.name) / "lost", a_sees_b_until=CONTACT_T - 1.0)
        cls.lost = {local.owner: local for local in reconstruct_run(lost_run, ReconstructionConfig()).locals}
        cls.trace_rows = [json.loads(line) for line in
                          (run / "reconstruction" / "A" / "local_trace.jsonl").read_text(encoding="utf-8").splitlines()]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_every_event_node_has_a_perceived_state_before(self):
        for local in self.result.locals:
            for node in local.graph.nodes:
                state = node.perceived_state_before
                self.assertIsNotNone(state, node.node_id)
                self.assertEqual(set(state), {"ego", "external", "signs", "facts_t_local"})

    def test_events_at_one_timestamp_share_an_identical_state_before(self):
        groups = {}
        for node in self.local["A"].graph.nodes:
            groups.setdefault(round(node.t_local, 6), []).append(node.perceived_state_before)
        shared = [states for states in groups.values() if len(states) > 1]
        self.assertTrue(shared)  # the run has simultaneous events (collision, stop, ...)
        for states in shared:
            for state in states[1:]:
                self.assertEqual(state, states[0])

    def test_the_state_before_excludes_the_transitions_at_that_time(self):
        nodes = {node.event_type: node for node in self.local["A"].graph.nodes}
        brake = nodes["BRAKE_START"]
        self.assertIs(brake.perceived_state_before["ego"]["BRAKE"], False)
        frame = next(row for row in self.trace_rows if abs(row["t_local"] - brake.t_local) < 1e-6)
        self.assertIs(frame["perceived_state"]["ego"]["BRAKE"], True)  # a frame holds the state after t
        self.assertAlmostEqual(brake.perceived_state_before["facts_t_local"], brake.t_local - 0.1)

    def test_nothing_is_known_before_the_first_observation(self):
        first = self.local["A"].graph.nodes[0]
        self.assertEqual(first.t_local, 0.0)
        self.assertTrue(all(value == UNKNOWN for value in first.perceived_state_before["ego"].values()))
        self.assertEqual(first.perceived_state_before["external"], {})

    def test_external_objects_keep_local_names(self):
        for node in self.local["A"].graph.nodes:
            for name in node.perceived_state_before["external"]:
                self.assertTrue(name.startswith("track_"), name)
        later = self.local["A"].graph.nodes[-1].perceived_state_before["external"]["track_001"]
        self.assertEqual(set(later), {"visible", "CLOSING", "CRITICAL_TTC", "IN_EGO_PATH"})

    def test_global_nodes_keep_each_observers_local_belief(self):
        for node in self.result.graph.nodes:
            self.assertEqual(set(node.perceived_state_before), {obs.graph for obs in node.observations})
        merged = next(node for node in self.result.graph.nodes if node.event_type == "COLLISION")
        self.assertEqual(set(merged.perceived_state_before), {"A", "B"})
        self.assertIn("track_001", merged.perceived_state_before["A"]["external"])  # not renamed to B

    def test_track_loss_makes_states_unknown_without_an_end(self):
        graph = self.lost["A"].graph
        lost = next(node for node in graph.nodes if node.event_type == "TRACK_LOST")
        before = lost.perceived_state_before["external"]["track_001"]
        self.assertTrue(before["visible"])
        self.assertIs(before["CLOSING"], True)  # closing in when it was lost
        self.assertNotIn("CLOSING_END", [node.event_type for node in graph.nodes if node.subject_id == "track_001"])
        later = [node for node in graph.nodes if node.t_local > lost.t_local]
        self.assertTrue(later)
        for node in later:
            state = node.perceived_state_before["external"]["track_001"]
            self.assertFalse(state["visible"])
            self.assertTrue(all(value == UNKNOWN for key, value in state.items() if key != "visible"))
        self.assertIn("lost (states UNKNOWN): track_001", compact_state(later[0].perceived_state_before))


class WorldStateUnitTests(unittest.TestCase):
    def test_timeline_before_and_after(self):
        timeline = Timeline()
        timeline.set(1.0, False)
        timeline.set(2.0, True)
        self.assertIsNone(timeline.value(1.0, before=True))
        self.assertIs(timeline.value(2.0, before=True), False)
        self.assertIs(timeline.value(2.0, before=False), True)
        with self.assertRaises(ValueError):
            timeline.set(1.5, False)

    def test_a_sign_stays_known_after_it_leaves_view(self):
        world = PerceivedWorld()
        world.add_sign_window("sign-0", "STOP", 2.0, 4.0, True)
        self.assertNotIn("sign-0", world.snapshot(2.0, before=True)["signs"])
        self.assertTrue(world.snapshot(3.0)["signs"]["sign-0"]["visible"])
        after = world.snapshot(9.0)["signs"]["sign-0"]
        self.assertEqual((after["visible"], after["known"], after["relevant_to_ego_path"]), (False, True, True))


class SignKnowledgeTests(unittest.TestCase):
    @staticmethod
    def _sign(track_id, first, last, bbox=(600, 300, 40, 40), sign_class="STOP"):
        return {"sign_track_id": track_id, "class": sign_class, "timestamp_first": ORIGIN + first,
                "timestamp_confirmed": ORIGIN + first + 0.2, "timestamp_last": ORIGIN + last,
                "best_confidence": 0.8, "relevant_to_ego_path": True, "best_bbox": list(bbox)}

    def test_a_sign_reacquired_while_standing_still_keeps_its_identity(self):
        signs = [self._sign("sign-1", 2.0, 3.0), self._sign("sign-2", 4.0, 5.0, bbox=(604, 302, 42, 41))]
        self.assertEqual(sign_continuity(signs, ORIGIN, _ego(0.0)), {"sign-1": "sign-1", "sign-2": "sign-1"})
        world = PerceivedWorld()
        events = sign_events("A", signs, ORIGIN, recording_end=12.0, track_gap_s=0.6, ego=_ego(0.0), world=world)
        self.assertEqual([(e.type, e.subject_id) for e in events],
                         [("STOP_SIGN_DETECTED_START", "sign-1"), ("STOP_SIGN_DETECTED_END", "sign-1"),
                          ("STOP_SIGN_DETECTED_START", "sign-1"), ("STOP_SIGN_DETECTED_END", "sign-1")])
        self.assertEqual(events[2].attributes, {"relevant_to_ego_path": True, "reacquired": True,
                                                "sign_track": "sign-2"})
        between = world.snapshot(3.5)["signs"]["sign-1"]
        self.assertEqual((between["visible"], between["known"]), (False, True))
        graph = build_local_graph("A", [TraceFrame(t_local=e.t_local, events=[e])
                                        for e in number_events("A", events)], [], {"end_t_local": 12.0})
        windows = sign_windows(graph)
        self.assertEqual([(w["start_t_local"], w["end_t_local"], w["reacquired"]) for w in windows],
                         [(2.2, 3.0, False), (4.2, 5.0, True)])

    def test_no_continuity_while_moving_elsewhere_in_the_image_or_for_another_class(self):
        moving = [self._sign("sign-1", 2.0, 3.0), self._sign("sign-2", 4.0, 5.0)]
        self.assertEqual(sign_continuity(moving, ORIGIN, _ego(5.0))["sign-2"], "sign-2")
        moved = [self._sign("sign-1", 2.0, 3.0), self._sign("sign-2", 4.0, 5.0, bbox=(700, 300, 40, 40))]
        self.assertEqual(sign_continuity(moved, ORIGIN, _ego(0.0))["sign-2"], "sign-2")
        other = [self._sign("sign-1", 2.0, 3.0), self._sign("sign-2", 4.0, 5.0, sign_class="YIELD")]
        self.assertEqual(sign_continuity(other, ORIGIN, _ego(0.0))["sign-2"], "sign-2")
        late = [self._sign("sign-1", 2.0, 3.0), self._sign("sign-2", 9.0, 10.0)]
        self.assertEqual(sign_continuity(late, ORIGIN, _ego(0.0))["sign-2"], "sign-2")

    def test_sign_detection_events_stay_pure_perception(self):
        events = sign_events("A", [self._sign("sign-1", 2.0, 3.0)], ORIGIN, recording_end=12.0, track_gap_s=0.6)
        self.assertEqual({event.kind for event in events}, {"PERCEPTION"})
        self.assertEqual([event.t_local for event in events], [2.2, 3.0])  # confirmation .. last detection

if __name__ == "__main__":
    unittest.main()
