"""The local semantic world model: perceived state, track loss, cut-in,
predicted path conflict, STOP-sign knowledge and the radar audit boundary."""

import ast
import json
import math
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.checks import sign_windows
from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.local import (build_local_graph, number_events, relative_motion, sign_continuity,
                                          sign_events, track_events)
from src.cdf.reconstruction.models import TraceFrame
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory, LocalTrack, TrackSample
from src.cdf.reconstruction.world_state import (UNKNOWN, PerceivedWorld, Timeline, compact_state,
                                                span_values)

from synthetic_run import CONTACT_T, make_run

CFG = SemanticsConfig()
ORIGIN = 100.0
ROOT = Path(__file__).resolve().parents[1]


def _ego(speed=0.0, end=12.0):
    """The recorder driving straight along its own +x at a constant speed."""
    return EgoTrajectory([EgoState(t_local=round(0.05 * k, 2), x=speed * 0.05 * k, y=0.0, heading=0.0,
                                   vx=speed, vy=0.0) for k in range(int(round(end / 0.05)) + 1)])


def _target(motion, start=1.0, end=8.0, vel_std=0.1, track_id="track_001"):
    """A track from ``motion(t) -> (longitudinal, lateral, vx, vy)``: position relative to the
    radar in the recorder's frame and ground velocity in the local frame (recorder heading 0)."""
    samples = []
    for k in range(int(round((end - start) / 0.05)) + 1):
        t = round(start + 0.05 * k, 2)
        longitudinal, lateral, vx, vy = motion(t)
        distance = math.hypot(longitudinal, lateral)
        samples.append(TrackSample(
            t_local=t, x_m=longitudinal, y_m=lateral, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
            pos_std_m=0.1, vel_std_mps=vel_std, range_m=distance,
            bearing_deg=math.degrees(math.atan2(lateral, longitudinal)), longitudinal_m=longitudinal,
            lateral_m=lateral, closing_speed_mps=0.0, ttc_s=None, measured=True, n_returns=4))
    return LocalTrack(track_id=track_id, samples=samples)


def _lane_change(side, until=5.0, lateral_speed=1.0, settle_at=5.0):
    """A car ahead (recorder at 10 m/s) drifting from 3.5 m to one side toward the
    recorder's lane at ``lateral_speed`` from t = 2 s until ``settle_at``."""
    def motion(t):
        moving = 2.0 <= t < settle_at
        drift = lateral_speed * (min(max(t, 2.0), settle_at) - 2.0)
        lateral = side * (3.5 - drift)
        return 15.0 + 0.5 * (t - 1.0), lateral, 10.5, (-side * lateral_speed if moving else 0.0)
    return motion


def _events(track, ego=None, recording_end=10.0, world=None):
    return [(event.type, event.t_local) for event in track_events("A", track, recording_end, CFG, ego, world)]


def _types(events):
    return [name for name, _ in events]


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
        self.assertEqual(set(later), {"visible", "CLOSING", "CRITICAL_TTC", "IN_EGO_PATH",
                                      "PREDICTED_PATH_CONFLICT", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT"})

    def test_global_nodes_keep_each_observers_local_belief(self):
        for node in self.result.graph.nodes:
            self.assertEqual(set(node.perceived_state_before), {obs.graph for obs in node.observations})
        merged = next(node for node in self.result.graph.nodes if node.event_type == "COLLISION")
        self.assertEqual(set(merged.perceived_state_before), {"A", "B"})
        self.assertIn("track_001", merged.perceived_state_before["A"]["external"])  # not renamed to B

    def test_track_state_facts_hold_the_quantities(self):
        fact = next(fact for row in self.trace_rows for fact in row["facts"] if fact["type"] == "TRACK_STATE")
        for key in ("vx_mps", "vy_mps", "vel_std_mps", "relative_longitudinal_speed_mps",
                    "relative_lateral_speed_mps", "relative_motion_angle_deg", "motion_relation",
                    "t_cpa_s", "d_cpa_m"):
            self.assertIn(key, fact["attributes"])

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

    def test_span_values_are_unknown_until_the_state_can_be_established(self):
        self.assertEqual(span_values(5, [(2, 4)], unknown_before=1), [UNKNOWN, False, True, True, False])

    def test_a_sign_stays_known_after_it_leaves_view(self):
        world = PerceivedWorld()
        world.add_sign_window("sign-0", "STOP", 2.0, 4.0, True)
        self.assertNotIn("sign-0", world.snapshot(2.0, before=True)["signs"])
        self.assertTrue(world.snapshot(3.0)["signs"]["sign-0"]["visible"])
        after = world.snapshot(9.0)["signs"]["sign-0"]
        self.assertEqual((after["visible"], after["known"], after["relevant_to_ego_path"]), (False, True, True))


class RelativeMotionTests(unittest.TestCase):
    def test_closest_point_of_approach(self):
        track = _target(lambda t: (10.0, 2.0, -5.0, 0.0), start=1.0, end=1.0)
        motion = relative_motion(track.samples[0], _ego().at(1.0), CFG)
        self.assertAlmostEqual(motion.t_cpa_s, 2.0)
        self.assertAlmostEqual(motion.d_cpa_m, 2.0)
        self.assertAlmostEqual(abs(motion.heading_deg), 180.0)  # oncoming

    def test_no_relative_motion_has_no_closest_approach(self):
        track = _target(lambda t: (10.0, 0.0, 10.0, 0.0), start=1.0, end=1.0)
        motion = relative_motion(track.samples[0], _ego(speed=10.0).at(1.0), CFG)
        self.assertIsNone(motion.t_cpa_s)
        self.assertIsNone(motion.d_cpa_m)


class PathConflictTests(unittest.TestCase):
    def test_conflict_starts_within_the_horizon_and_ends_once_the_approach_is_past(self):
        # Oncoming 1 m beside the radar line at 5 m/s from 30 m: closest approach due in 4 s at t = 3 s.
        events = _events(_target(lambda t: (30.0 - 5.0 * (t - 1.0), 1.0, -5.0, 0.0), end=9.0), recording_end=12.0)
        self.assertIn(("PREDICTED_PATH_CONFLICT_START", 3.0), events)
        self.assertIn(("PREDICTED_PATH_CONFLICT_END", 7.0), events)

    def test_adjacent_lane_traffic_is_not_a_conflict(self):
        events = _events(_target(lambda t: (30.0 - 5.0 * (t - 1.0), 3.5, -5.0, 0.0), end=9.0), recording_end=12.0)
        self.assertNotIn("PREDICTED_PATH_CONFLICT_START", _types(events))

    def test_crossing_traffic_on_a_collision_course_is_a_conflict(self):
        # Recorder at 10 m/s; a car from the right at 10 m/s, both 20 m from the meeting point.
        def motion(t):
            return 20.0 - 10.0 * (t - 1.0), 20.0 - 10.0 * (t - 1.0), 0.0, -10.0
        events = _events(_target(motion, end=2.5), ego=_ego(10.0), recording_end=12.0)
        self.assertEqual(events[:2], [("TRACK_APPEARED", 1.0), ("PREDICTED_PATH_CONFLICT_START", 1.0)])
        self.assertNotIn("CUT_IN_FROM_RIGHT_START", _types(events))  # crossing is not a cut-in

    def test_a_lead_car_at_constant_gap_is_not_a_conflict(self):
        events = _events(_target(lambda t: (15.0, 0.0, 10.0, 0.0)), ego=_ego(10.0))
        self.assertNotIn("PREDICTED_PATH_CONFLICT_START", _types(events))

    def test_uncertain_estimates_leave_the_conflict_unknown(self):
        world = PerceivedWorld()
        events = _events(_target(lambda t: (30.0 - 5.0 * (t - 1.0), 0.0, -5.0, 0.0), vel_std=2.0), world=world)
        self.assertNotIn("PREDICTED_PATH_CONFLICT_START", _types(events))
        self.assertEqual(world.snapshot(5.0)["external"]["track_001"]["PREDICTED_PATH_CONFLICT"], UNKNOWN)
        self.assertIs(world.snapshot(5.0)["external"]["track_001"]["CLOSING"], False)


class CutInTests(unittest.TestCase):
    def test_cut_in_from_the_left_starts_on_evidence_and_ends_when_it_settles(self):
        events = _events(_target(_lane_change(side=-1)), ego=_ego(10.0))
        self.assertIn(("CUT_IN_FROM_LEFT_START", 2.5), events)
        self.assertIn(("CUT_IN_FROM_LEFT_END", 5.0), events)
        self.assertNotIn("CUT_IN_FROM_RIGHT_START", _types(events))

    def test_cut_in_from_the_right(self):
        events = _events(_target(_lane_change(side=1)), ego=_ego(10.0))
        self.assertIn(("CUT_IN_FROM_RIGHT_START", 2.5), events)
        self.assertNotIn("CUT_IN_FROM_LEFT_START", _types(events))

    def test_brief_lateral_drift_is_not_a_cut_in(self):
        events = _events(_target(_lane_change(side=-1, settle_at=2.3)), ego=_ego(10.0))
        self.assertNotIn("CUT_IN_FROM_LEFT_START", _types(events))

    def test_a_car_already_in_the_corridor_does_not_cut_in(self):
        def motion(t):
            return 15.0, -1.2 + 0.5 * min(max(t - 2.0, 0.0), 2.0), 10.0, (0.5 if 2.0 <= t < 4.0 else 0.0)
        events = _events(_target(motion), ego=_ego(10.0))
        self.assertNotIn("CUT_IN_FROM_LEFT_START", _types(events))

    def test_uncertain_estimates_give_no_cut_in_and_an_unknown_state(self):
        world = PerceivedWorld()
        events = _events(_target(_lane_change(side=-1), vel_std=2.0), ego=_ego(10.0), world=world)
        self.assertNotIn("CUT_IN_FROM_LEFT_START", _types(events))
        self.assertEqual(world.snapshot(4.0)["external"]["track_001"]["CUT_IN_FROM_LEFT"], UNKNOWN)

    def test_a_cut_in_still_under_way_when_the_track_is_lost_has_no_end(self):
        world = PerceivedWorld()
        events = _events(_target(_lane_change(side=-1), end=3.5), ego=_ego(10.0), world=world)
        self.assertIn(("CUT_IN_FROM_LEFT_START", 2.5), events)
        self.assertIn(("TRACK_LOST", 3.5), events)
        self.assertNotIn("CUT_IN_FROM_LEFT_END", _types(events))
        self.assertIs(world.snapshot(3.5, before=True)["external"]["track_001"]["CUT_IN_FROM_LEFT"], True)
        after = world.snapshot(3.5, before=False)["external"]["track_001"]
        self.assertEqual((after["visible"], after["CUT_IN_FROM_LEFT"]), (False, UNKNOWN))


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


class RadarBoundaryTests(unittest.TestCase):
    def test_reconstruction_never_imports_the_privileged_audit_or_ground_truth(self):
        for path in sorted((ROOT / "src" / "cdf" / "reconstruction").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""]
                for name in names:
                    self.assertNotIn("audit", name, path.name)
                    self.assertNotIn("evaluation", name, path.name)
                    self.assertNotIn("replay", name, path.name)

    def test_the_audit_is_marked_privileged(self):
        text = (ROOT / "scripts" / "audit_radar_visibility.py").read_text(encoding="utf-8")
        self.assertIn("PRIVILEGED EVALUATION", text.split("\n\n")[0] + text[:400])

    def test_the_campaign_sensor_setup_is_still_one_forward_radar(self):
        import yaml
        default = yaml.safe_load((ROOT / "configs" / "default.yaml").read_text(encoding="utf-8"))
        self.assertEqual(default["sensors"]["profile"], "radar_baseline")
        profile = yaml.safe_load((ROOT / "configs" / "sensors" / "radar_baseline.yaml").read_text(encoding="utf-8"))
        sensors = profile["radar"]["sensors"]
        self.assertEqual(len(sensors), 1)
        self.assertEqual((sensors[0]["horizontal_fov_deg"], sensors[0]["range_m"], sensors[0]["mount"]["x"]),
                         (120.0, 90.0, 2.2))


if __name__ == "__main__":
    unittest.main()
