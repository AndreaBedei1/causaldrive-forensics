"""Data model, local clocks and collision episodes."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import CollisionConfig, ReconstructionConfig
from src.cdf.reconstruction.local import build_trace, collision_events, reconstruct_vehicle
from src.cdf.reconstruction.models import GraphEdge, GraphNode, LocalGraph, SemanticEvent
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory

from synthetic_run import CONTACT_T, make_run


class ModelTests(unittest.TestCase):
    def test_semantic_event_and_local_graph_round_trip_through_json(self):
        event = SemanticEvent(type="CLOSING", kind="PERCEPTION", actor_id="A", t_local=12.9,
                              subject_id="track_001", attributes={"range_m": 14.2, "closing_speed_mps": 5.1},
                              source="radar", confidence=0.8, event_id="A:e02")
        self.assertEqual(SemanticEvent.from_dict(json.loads(json.dumps(event.to_dict()))), event)

        graph = LocalGraph(owner="A", nodes=[GraphNode.from_event(event)],
                           edges=[GraphEdge("A:e01", "A:e02", "PRECEDES")],
                           tracks=[{"track_id": "track_001"}], recorder={"owner": "A"})
        again = LocalGraph.from_dict(json.loads(json.dumps(graph.to_dict())))
        self.assertEqual(again, graph)
        self.assertEqual(again.node("A:e02").attributes["range_m"], 14.2)

    def test_new_event_types_need_no_new_class(self):
        # Event-specific values live in attributes, so any type serialises the same way.
        event = SemanticEvent(type="SOMETHING_NEW", kind="FACT", actor_id="B", t_local=1.0,
                              attributes={"anything": [1, 2]})
        self.assertEqual(SemanticEvent.from_dict(event.to_dict()).attributes, {"anything": [1, 2]})


class LocalClockTests(unittest.TestCase):
    def test_local_trace_timestamps_remain_local(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp), b_late_start_s=0.5)
            cfg = ReconstructionConfig()
            a = reconstruct_vehicle(run / "vehicles" / "A", cfg)
            b = reconstruct_vehicle(run / "vehicles" / "B", cfg)

        # Each recorder counts from its own first sample in its own clock.
        self.assertEqual(a.clock_origin, 100.0)
        self.assertEqual(b.clock_origin, 250.5)
        self.assertEqual(a.trace[0].t_local, 0.0)
        self.assertEqual(b.trace[0].t_local, 0.0)
        a_collision = [n for n in a.graph.nodes if n.event_type == "COLLISION"][0]
        b_collision = [n for n in b.graph.nodes if n.event_type == "COLLISION"][0]
        self.assertAlmostEqual(a_collision.t_local, CONTACT_T, places=3)
        self.assertAlmostEqual(b_collision.t_local, CONTACT_T - 0.5, places=3)
        # The raw reading of the recorder's own clock stays recoverable from its origin.
        self.assertAlmostEqual(a.clock_origin + a_collision.t_local, 100.0 + CONTACT_T, places=4)
        self.assertAlmostEqual(b.clock_origin + b_collision.t_local, 250.0 + CONTACT_T, places=4)
        self.assertEqual(a.graph.recorder["clock"]["origin_source_timestamp"], 100.0)
        # Trace frames are on each recorder's own 10 Hz grid (the last one may sit at
        # the recording end); events keep exact times.
        for frame in a.trace[:-1]:
            self.assertAlmostEqual(frame.t_local * 10, round(frame.t_local * 10), places=6)
        for frame in a.trace:
            for event in frame.events:
                self.assertTrue(frame.t_local - 0.1 < event.t_local <= frame.t_local + 1e-9)

    def test_a_recording_ending_between_grid_instants_gets_a_final_frame(self):
        def trace(end):
            ego = EgoTrajectory([EgoState(t_local=0.05 * k, x=0.0, y=0.0, heading=0.0, vx=5.0, vy=0.0)
                                 for k in range(int(round(end / 0.05)) + 1)])
            events = [SemanticEvent(type=name, kind="ACTION", actor_id="A", t_local=t, event_id="A:e%02d" % k)
                      for k, (name, t) in enumerate([("BRAKE_START", 0.0), ("BRAKE_END", 0.95),
                                                     ("STRONG_THROTTLE_START", end)], 1)]
            return build_trace("A", ego, [], [], events, clock_origin=0.0, trace_hz=10.0)

        frames = trace(1.05)
        self.assertEqual([frame.t_local for frame in frames][-3:], [0.9, 1.0, 1.05])
        self.assertEqual({frame.t_local: [e.type for e in frame.events] for frame in frames if frame.events},
                         {0.0: ["BRAKE_START"], 1.0: ["BRAKE_END"], 1.05: ["STRONG_THROTTLE_START"]})
        self.assertEqual(frames[-1].facts[0].attributes["speed_mps"], 5.0)
        self.assertEqual([frame.t_local for frame in trace(1.0)][-2:], [0.9, 1.0])  # on the grid: no extra frame

    def test_a_local_graph_does_not_depend_on_another_recorder(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp))
            cfg = ReconstructionConfig()
            before = reconstruct_vehicle(run / "vehicles" / "A", cfg).graph.to_dict()
            (run / "vehicles" / "B" / "collisions.jsonl").write_text("", encoding="utf-8")
            (run / "vehicles" / "B" / "ego.jsonl").write_text("", encoding="utf-8")
            after = reconstruct_vehicle(run / "vehicles" / "A", cfg).graph.to_dict()
        self.assertEqual(before, after)


class CollisionEventTests(unittest.TestCase):
    def test_repeated_collision_callbacks_collapse_into_one_minimal_event(self):
        burst = [{"timestamp": 10.0 + 0.05 * k, "impulse": 100.0 + k} for k in range(21)]
        later = [{"timestamp": 13.0, "impulse": 42.0}]
        events = collision_events("A", copy.deepcopy(burst + later), clock_origin=10.0,
                                  cfg=CollisionConfig(merge_gap_s=0.5))
        self.assertEqual([(event.type, event.t_local) for event in events], [("COLLISION", 0.0), ("COLLISION", 3.0)])
        # Only the peak impulse, which alignment needs; callback details stay in the raw log.
        self.assertEqual(events[0].attributes, {"peak_impulse": 120.0})
        self.assertEqual(events[1].attributes, {"peak_impulse": 42.0})


if __name__ == "__main__":
    unittest.main()
