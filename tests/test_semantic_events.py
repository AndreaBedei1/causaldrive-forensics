"""Semantic transitions of the recorder itself, signs, and graph structure."""

import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.checks import open_states, sign_windows
from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.local import (build_local_graph, control_events, motion_events,
                                          number_events, sign_events)
from src.cdf.reconstruction.models import SemanticEvent, TraceFrame, display_order
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory

from synthetic_run import CONTACT_T, make_run

ORIGIN = 100.0
CFG = SemanticsConfig()


def _grid(start=5.0, end=9.0):
    return [round(start + 0.05 * k, 2) for k in range(int(round((end - start) / 0.05)) + 1)]


def _pedals(brake=lambda t: 0.0, throttle=lambda t: 0.0, end=9.0):
    controls = [{"timestamp": ORIGIN + t, "brake": brake(t), "throttle": throttle(t)} for t in _grid(end=end)]
    return [(event.type, event.t_local) for event in control_events("A", controls, ORIGIN, CFG)]


def _motion(speed, speed_limit_kmh=None, end=9.0):
    ego = EgoTrajectory([EgoState(t_local=t, x=0.0, y=0.0, heading=0.0, vx=speed(t), vy=0.0) for t in _grid(end=end)])
    events = motion_events("A", ego, CFG, speed_limit_kmh)
    return [(event.type, event.t_local) for event in number_events("A", events)], events


def _graph(events):
    numbered = number_events("A", list(events))
    frames = [TraceFrame(t_local=event.t_local, events=[event]) for event in numbered]
    return build_local_graph("A", frames, [], {"end_t_local": 9.0})


def _event(event_type, t_local, subject=None, **attributes):
    return SemanticEvent(type=event_type, kind="FACT", actor_id="A", t_local=t_local, subject_id=subject,
                         attributes=attributes)


class BrakingTests(unittest.TestCase):
    def test_continuous_braking_is_one_start_and_one_end(self):
        self.assertEqual(_pedals(brake=lambda t: 0.5 if 6.0 <= t < 7.0 else 0.0),
                         [("BRAKE_START", 6.0), ("BRAKE_END", 7.0)])

    def test_braking_at_recording_end_has_no_invented_end(self):
        events = _pedals(brake=lambda t: 1.0 if t >= 8.0 else 0.0)
        self.assertEqual(sorted(events), [("BRAKE_START", 8.0), ("HARD_BRAKE_START", 8.0)])

    def test_brake_release_brake_gives_two_sequences(self):
        events = _pedals(brake=lambda t: 0.5 if 6.0 <= t < 6.5 or 7.5 <= t < 8.0 else 0.0)
        self.assertEqual(events, [("BRAKE_START", 6.0), ("BRAKE_END", 6.5), ("BRAKE_START", 7.5), ("BRAKE_END", 8.0)])

    def test_short_sub_threshold_noise_does_not_split_braking(self):
        def brake(t):
            if t in (6.5, 7.0, 7.05, 7.1):  # a one-sample and a 0.15 s dip
                return 0.02
            return 0.8 if 6.0 <= t < 8.0 else 0.0
        self.assertEqual(_pedals(brake=brake), [("BRAKE_START", 6.0), ("BRAKE_END", 8.0)])

    def test_hard_braking_nests_inside_braking(self):
        def brake(t):
            if 6.5 <= t < 7.5:
                return 1.0
            return 0.3 if 6.0 <= t < 8.0 else 0.0
        events = sorted(_pedals(brake=brake), key=lambda item: item[1])
        self.assertEqual(events, [("BRAKE_START", 6.0), ("HARD_BRAKE_START", 6.5), ("HARD_BRAKE_END", 7.5),
                                  ("BRAKE_END", 8.0)])

    def test_releasing_a_hard_brake_at_once_ends_both_states_together(self):
        events = _pedals(brake=lambda t: 1.0 if 6.0 <= t < 7.0 else 0.0)
        self.assertEqual(sorted(events, key=lambda item: item[1]),
                         [("BRAKE_START", 6.0), ("HARD_BRAKE_START", 6.0), ("BRAKE_END", 7.0), ("HARD_BRAKE_END", 7.0)])

    def test_pedal_values_stay_out_of_the_events(self):
        controls = [{"timestamp": ORIGIN + t, "brake": 0.95 if t >= 6.0 else 0.0, "throttle": 0.0} for t in _grid()]
        for event in control_events("A", controls, ORIGIN, CFG):
            self.assertEqual(event.attributes, {})


class ThrottleTests(unittest.TestCase):
    def test_strong_throttle_has_start_and_end(self):
        self.assertEqual(_pedals(throttle=lambda t: 0.9 if 6.0 <= t < 7.0 else 0.4),
                         [("STRONG_THROTTLE_START", 6.0), ("STRONG_THROTTLE_END", 7.0)])

    def test_brief_throttle_noise_does_not_flicker(self):
        self.assertEqual(_pedals(throttle=lambda t: 0.7 if t == 6.5 else 0.9 if 6.0 <= t < 7.0 else 0.4),
                         [("STRONG_THROTTLE_START", 6.0), ("STRONG_THROTTLE_END", 7.0)])


class MovementTests(unittest.TestCase):
    def test_moving_then_stopping(self):
        events, raw = _motion(lambda t: max(0.0, 10.0 - 5.0 * max(0.0, t - 6.0)))  # stops at 8.0 s
        self.assertEqual(events, [("MOVING_START", 5.0), ("MOVING_END", 7.95), ("STOP_START", 7.95)])
        self.assertEqual(raw[0].attributes, {"active_at_first_observation": True})

    def test_restart_gives_stop_end_and_moving_start(self):
        def speed(t):
            if t < 6.0:
                return 0.0
            if t < 7.0:  # creeping inside the 0.3-1.0 m/s hysteresis band: no flicker
                return 0.6 + 0.2 * ((round(t * 20) % 2) * 2 - 1)
            return 3.0
        events, _ = _motion(speed)
        self.assertEqual(events, [("STOP_START", 5.0), ("STOP_END", 7.0), ("MOVING_START", 7.0)])


class SpeedLimitTests(unittest.TestCase):
    @staticmethod
    def _kmh(value):
        return value / 3.6

    def test_limit_in_kmh_is_converted_with_one_kmh_hysteresis(self):
        just_below, _ = _motion(lambda t: self._kmh(30.9), speed_limit_kmh=30)
        just_above, _ = _motion(lambda t: self._kmh(31.1), speed_limit_kmh=30)
        self.assertNotIn("SPEED_LIMIT_EXCEEDED_START", [name for name, _ in just_below])
        self.assertIn(("SPEED_LIMIT_EXCEEDED_START", 5.0), just_above)

    def test_below_the_limit_never_starts(self):
        events, _ = _motion(lambda t: self._kmh(25), speed_limit_kmh=30)
        self.assertEqual([name for name, _ in events], ["MOVING_START"])

    def test_crossing_above_and_back_gives_one_start_and_one_end_inside_moving(self):
        events, _ = _motion(lambda t: self._kmh(40 if 6.0 <= t < 7.0 else 25), speed_limit_kmh=30)
        self.assertEqual(events, [("MOVING_START", 5.0), ("SPEED_LIMIT_EXCEEDED_START", 6.0),
                                  ("SPEED_LIMIT_EXCEEDED_END", 7.0)])

    def test_jitter_around_the_limit_does_not_flicker(self):
        events, _ = _motion(lambda t: self._kmh(30.5 if round(t * 20) % 2 else 31.5), speed_limit_kmh=30)
        self.assertEqual([name for name, _ in events].count("SPEED_LIMIT_EXCEEDED_START"), 1)
        self.assertNotIn("SPEED_LIMIT_EXCEEDED_END", [name for name, _ in events])

    def test_recording_ending_while_speeding_has_no_invented_end(self):
        events, _ = _motion(lambda t: self._kmh(45 if t >= 8.0 else 25), speed_limit_kmh=30)
        self.assertEqual(events[-1], ("SPEED_LIMIT_EXCEEDED_START", 8.0))

    def test_a_crash_stop_ends_speeding_and_moving_together(self):
        events, _ = _motion(lambda t: self._kmh(45) if t < 7.0 else 0.0, speed_limit_kmh=30)
        self.assertEqual(events, [("MOVING_START", 5.0), ("SPEED_LIMIT_EXCEEDED_START", 5.0),
                                  ("SPEED_LIMIT_EXCEEDED_END", 7.0), ("MOVING_END", 7.0), ("STOP_START", 7.0)])

    def test_no_supplied_limit_means_no_speed_limit_events(self):
        events, _ = _motion(lambda t: self._kmh(90))
        self.assertEqual([name for name, _ in events], ["MOVING_START"])


class SignTests(unittest.TestCase):
    @staticmethod
    def _sign(sign_class, confirmed, last, relevant=True):
        return {"sign_track_id": "sign-3", "class": sign_class, "timestamp_first": ORIGIN + confirmed - 0.2,
                "timestamp_confirmed": ORIGIN + confirmed, "timestamp_last": ORIGIN + last,
                "best_confidence": 0.8, "relevant_to_ego_path": relevant}

    def test_confirmed_stop_sign_gives_a_detection_window(self):
        events = sign_events("A", [self._sign("STOP", 2.0, 5.0)], ORIGIN, recording_end=12.0, track_gap_s=0.6)
        self.assertEqual([(e.type, e.t_local, e.subject_id) for e in events],
                         [("STOP_SIGN_DETECTED_START", 2.0, "sign-3"), ("STOP_SIGN_DETECTED_END", 5.0, "sign-3")])
        self.assertEqual(events[0].attributes, {"relevant_to_ego_path": True})
        self.assertEqual(events[1].attributes, {})

    def test_yield_sign_window_and_sign_still_in_view_at_the_end(self):
        events = sign_events("A", [self._sign("YIELD", 2.0, 11.8)], ORIGIN, recording_end=12.0, track_gap_s=0.6)
        self.assertEqual([e.type for e in events], ["YIELD_SIGN_DETECTED_START"])

    def test_sign_confirmed_at_its_last_detection_gives_a_zero_length_window(self):
        # Confirmed and last seen in the same frame: START and END share one timestamp.
        events = sign_events("A", [self._sign("STOP", 3.15, 3.15)], ORIGIN, recording_end=12.0, track_gap_s=0.6)
        graph = _graph(events + [_event("MOVING_START", 0.0), _event("TRACK_APPEARED", 3.15, "track_001")])
        types = [node.event_type for node in graph.nodes if node.subject_id == "sign-3"]
        self.assertEqual(types, ["STOP_SIGN_DETECTED_START", "STOP_SIGN_DETECTED_END"])
        self.assertEqual([item["state"] for item in open_states(graph)], ["MOVING"])
        window = sign_windows(graph)[0]
        self.assertEqual((window["start_t_local"], window["end_t_local"]), (3.15, 3.15))
        self.assertEqual(window["stop_starts_inside"], [])
        start, end = (node.node_id for node in graph.nodes if node.subject_id == "sign-3")
        precedes = {(edge.from_node, edge.to_node) for edge in graph.edges if edge.relation == "PRECEDES"}
        self.assertNotIn((start, end), precedes)  # same timestamp: simultaneous, not ordered

    def test_stop_inside_the_window_is_detectable(self):
        graph = _graph([_event("STOP_SIGN_DETECTED_START", 2.0, "sign-3", relevant_to_ego_path=True),
                        _event("STOP_START", 4.0), _event("STOP_SIGN_DETECTED_END", 5.0, "sign-3")])
        window = sign_windows(graph)[0]
        self.assertEqual((window["start_t_local"], window["end_t_local"]), (2.0, 5.0))
        self.assertEqual(len(window["stop_starts_inside"]), 1)

    def test_missing_stop_inside_the_window_is_detectable(self):
        graph = _graph([_event("STOP_SIGN_DETECTED_START", 2.0, "sign-3"),
                        _event("STOP_SIGN_DETECTED_END", 5.0, "sign-3"), _event("STOP_START", 6.0)])
        window = sign_windows(graph)[0]
        self.assertEqual(window["stop_starts_inside"], [])
        self.assertFalse(window["already_stopped_at_start"])


class GraphTests(unittest.TestCase):
    def test_simultaneous_events_get_no_precedes_between_them(self):
        graph = _graph([_event("BRAKE_START", 1.0), _event("HARD_BRAKE_START", 1.0), _event("COLLISION", 2.0)])
        pairs = {(edge.from_node, edge.to_node) for edge in graph.edges if edge.relation == "PRECEDES"}
        self.assertEqual(pairs, {("A:e01", "A:e03"), ("A:e02", "A:e03")})

    def test_display_order_keeps_a_zero_length_state_start_before_its_end(self):
        # Ends normally precede starts at one timestamp; an END of a state that
        # starts at that very timestamp (same actor and subject) must follow it.
        items = [("CLOSING_END", 2.0, "track_001"), ("CLOSING_START", 2.0, "track_001"),
                 ("CLOSING_END", 2.0, "track_002"), ("COLLISION", 2.0, None), ("BRAKE_START", 1.0, None)]
        ordered = display_order(items, lambda item: item[1], lambda item: item[0],
                                lambda item: "A", lambda item: item[2])
        self.assertEqual(ordered, [("BRAKE_START", 1.0, None), ("COLLISION", 2.0, None),
                                   ("CLOSING_END", 2.0, "track_002"), ("CLOSING_START", 2.0, "track_001"),
                                   ("CLOSING_END", 2.0, "track_001")])

    def test_same_track_links_the_track_appearance_to_its_events(self):
        graph = _graph([_event("TRACK_APPEARED", 1.0, "track_001"), _event("CLOSING_START", 1.0, "track_001"),
                        _event("TRACK_APPEARED", 1.5, "track_002"), _event("CRITICAL_TTC_START", 2.0, "track_001")])
        same = {(edge.from_node, edge.to_node) for edge in graph.edges if edge.relation == "SAME_TRACK"}
        self.assertEqual(same, {("A:e01", "A:e02"), ("A:e01", "A:e04")})

    def test_open_states_are_those_never_ended(self):
        graph = _graph([_event("MOVING_START", 0.0), _event("BRAKE_START", 1.0), _event("BRAKE_END", 2.0),
                        _event("HARD_BRAKE_START", 3.0), _event("EGO_PATH_ENTRY", 3.5, "track_001")])
        self.assertEqual([(item["state"], item["subject"]) for item in open_states(graph)],
                         [("MOVING", None), ("HARD_BRAKE", None), ("EGO_PATH", "track_001")])

    def test_reconstructed_graph_is_sparse_and_uses_the_new_vocabulary(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp))
            result = reconstruct_run(run, ReconstructionConfig())
            texts = [path.read_text(encoding="utf-8") for path in (run / "reconstruction").rglob("*") if path.is_file()]
        for old in ("BRAKE_EPISODE", "BRAKE_ONSET", "THROTTLE_ONSET", "FULL_STOP", "ENTERED_EGO_PATH"):
            self.assertFalse(any(old in text for text in texts), old)
        a_types = [node.event_type for node in next(l for l in result.locals if l.owner == "A").graph.nodes]
        for expected in ("MOVING_START", "BRAKE_START", "COLLISION", "MOVING_END", "STOP_START",
                         "TRACK_APPEARED", "CLOSING_START", "CRITICAL_TTC_START"):
            self.assertIn(expected, a_types)
        self.assertNotIn("BRAKE_END", a_types)  # still braking when the synthetic recording ends
        allowed = {"peak_impulse", "active_at_first_observation", "relevant_to_ego_path"}
        for local in result.locals:
            for node in local.graph.nodes:
                self.assertLessEqual(set(node.attributes), allowed, node.event_type)
        collision = next(node for node in result.graph.nodes if node.event_type == "COLLISION")
        self.assertEqual(collision.t_global, 0.0)
        self.assertEqual(set(collision.attributes["peak_impulse"]), {"A", "B"})
        self.assertAlmostEqual(next(node for node in result.graph.nodes if node.event_type == "BRAKE_START").t_global,
                               3.0 - CONTACT_T, places=3)


if __name__ == "__main__":
    unittest.main()
