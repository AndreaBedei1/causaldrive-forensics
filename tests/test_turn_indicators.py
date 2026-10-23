"""Turn indicators: the recorder's own light state (``lights.jsonl``, CARLA VehicleLightState read back every frame)
reconstructed as INDICATOR_LEFT / INDICATOR_RIGHT with exact START / END times; UNKNOWN (not off) for a recording
without the light log; never inferred from motion; scripted independently of any manoeuvre; shown in the replay
panel."""

import unittest
from pathlib import Path

from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.local import indicator_events, reconstruct_vehicle
from src.cdf.reconstruction.world_state import UNKNOWN, PerceivedWorld
from src.cdf.simulation.controllers import RoutePlan, ScriptedAction, ScriptedController

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 100.0


def lights(on_left=(), on_right=(), until=3.0, dt=0.05):
    """A light log from frame times: the left / right blinker on inside the given (start, end) windows."""
    out, k = [], 0
    while k * dt <= until + 1e-9:
        t = round(k * dt, 4)
        left = any(a <= t < b for a, b in on_left)
        right = any(a <= t < b for a, b in on_right)
        out.append({"frame": k, "timestamp": ORIGIN + t, "light_state": (32 if left else 0) | (16 if right else 0),
                    "left_blinker": left, "right_blinker": right})
        k += 1
    return out


def events(log, world=None):
    return [(e.type, round(e.t_local, 4)) for e in indicator_events("A", log, ORIGIN, 0.0, world)]


class IndicatorEventTests(unittest.TestCase):
    def test_start_and_end_at_the_logged_frames(self):
        self.assertEqual(events(lights(on_left=[(0.5, 1.75)])),
                         [("INDICATOR_LEFT_START", 0.5), ("INDICATOR_LEFT_END", 1.75)])

    def test_both_sides_and_an_indicator_left_on(self):
        out = events(lights(on_right=[(0.3, 0.9)], on_left=[(2.0, 99.0)]))
        self.assertIn(("INDICATOR_RIGHT_START", 0.3), out)
        self.assertIn(("INDICATOR_RIGHT_END", 0.9), out)
        self.assertIn(("INDICATOR_LEFT_START", 2.0), out)
        self.assertNotIn("INDICATOR_LEFT_END", [name for name, _ in out])  # still on when the recording ends

    def test_on_from_the_first_frame(self):
        out = indicator_events("A", lights(on_left=[(0.0, 1.0)]), ORIGIN, 0.0, None)
        self.assertEqual(out[0].type, "INDICATOR_LEFT_START")
        self.assertEqual(out[0].t_local, 0.0)

    def test_states_follow_the_log(self):
        world = PerceivedWorld()
        events(lights(on_left=[(0.5, 1.0)]), world)
        self.assertIs(world.snapshot(0.25)["ego"]["INDICATOR_LEFT"], False)
        self.assertIs(world.snapshot(0.75)["ego"]["INDICATOR_LEFT"], True)
        self.assertIs(world.snapshot(0.75)["ego"]["INDICATOR_RIGHT"], False)

    def test_without_the_light_log_the_indicators_are_unknown_not_off(self):
        world = PerceivedWorld()
        self.assertEqual(indicator_events("A", None, ORIGIN, 0.0, world), [])
        ego = world.snapshot(1.0)["ego"]
        self.assertEqual(ego["INDICATOR_LEFT"], UNKNOWN)
        self.assertEqual(ego["INDICATOR_RIGHT"], UNKNOWN)


class NeverInferredTests(unittest.TestCase):
    """B changes lane in both runs; its indicators come only from its light log, never from that motion."""

    def reconstruct(self, run, owner):
        vehicle = ROOT / "traces" / run / "vehicles" / owner
        if not (vehicle / "ego.jsonl").exists():
            self.skipTest("canonical trace not present")
        return vehicle, reconstruct_vehicle(vehicle, ReconstructionConfig())

    @staticmethod
    def indicators(local, t0, t1):
        return {(frame.perceived_state["ego"].get("INDICATOR_LEFT"), frame.perceived_state["ego"].get("INDICATOR_RIGHT"))
                for frame in local.trace if t0 <= frame.t_local <= t1 and frame.perceived_state}

    def test_a_lane_change_without_a_light_log_has_unknown_indicators(self):
        # S02 crash: B cuts into A's lane from 0.2 s to 2.4 s.  Since 2026-10-22 every recording has a light log,
        # so the case of a recorder without one is a copy of B's files without it.
        import shutil
        import tempfile
        source = ROOT / "traces" / "S02" / "run_0_crash" / "vehicles" / "B"
        if not (source / "ego.jsonl").exists():
            self.skipTest("canonical trace not present")
        with tempfile.TemporaryDirectory() as tmp:
            vehicle = Path(tmp) / "B"
            shutil.copytree(str(source), str(vehicle))
            (vehicle / "lights.jsonl").unlink()
            local = reconstruct_vehicle(vehicle, ReconstructionConfig())
        self.assertFalse([n for n in local.graph.nodes if n.event_type.startswith("INDICATOR_")])
        self.assertEqual(self.indicators(local, 0.5, 2.5), {(UNKNOWN, UNKNOWN)})

    def test_an_unsignalled_lane_change_with_the_light_log_is_no_indicator(self):
        # S17, recorded with the light log: B moves into the middle lane (4.8-6.8 s) without signalling.
        vehicle, local = self.reconstruct("S17/run_0_occlusion_reappearance", "B")
        self.assertTrue((vehicle / "lights.jsonl").exists())
        self.assertFalse([n for n in local.graph.nodes if n.event_type.startswith("INDICATOR_")])
        self.assertEqual(self.indicators(local, 4.5, 7.5), {(False, False)})


class ScriptedIndicatorTests(unittest.TestCase):
    def controller(self, actions):
        route = RoutePlan(points=[(float(x), 0.0) for x in range(0, 200, 2)], headings=[0.0] * 100)
        return ScriptedController("A", route, 10.0, actions)

    def test_the_indicator_follows_its_action_only(self):
        c = self.controller([
            ScriptedAction("signal_left", "indicator", 1.0, 2.0, {"side": -1.0}),
            ScriptedAction("move_right", "lane_shift", 4.0, 2.0, {"lateral_m": 3.5}),  # unsignalled
            ScriptedAction("signal_right", "indicator", 7.0, 1.0, {"side": 1.0})])
        self.assertEqual(c.indicator(0.5), 0)
        self.assertEqual(c.indicator(1.0), -1)
        self.assertEqual(c.indicator(2.99), -1)
        self.assertEqual(c.indicator(3.0), 0)
        self.assertEqual(c.indicator(5.0), 0)  # the lane change is not signalled
        self.assertEqual(c.indicator(7.5), 1)
        self.assertEqual(c.indicator(8.0), 0)



_LOCAL = {}


def canonical_local(run, owner):
    """The reconstruction of one canonical recorder, once per test session."""
    if (run, owner) not in _LOCAL:
        _LOCAL[(run, owner)] = reconstruct_vehicle(ROOT / "traces" / run / "vehicles" / owner, ReconstructionConfig())
    return _LOCAL[(run, owner)]


class CanonicalSignalTests(unittest.TestCase):
    """S07 and S08 signal their turns: the reconstructed events are exactly the logged light transitions (local time
    = scenario time - 0.05 s); an indicator still on when the recording ends has no END."""

    # The canonical set re-acquired on 2026-10-22 logs every light change at its scripted instant (S07: A signals
    # from 1.0 s); the earlier recordings logged them one tick (0.05 s) before.
    EXPECTED = {
        ("S07/run_0_merge_conflict", "A"): [("INDICATOR_LEFT_START", 1.0)],  # still circulating when hit
        ("S07/run_0_merge_conflict", "B"): [("INDICATOR_RIGHT_START", 13.0), ("INDICATOR_RIGHT_END", 19.1)],
        ("S08/run_0_rolls_through", "A"): [("INDICATOR_LEFT_START", 0.5)],  # the turn ends in the collision
        ("S08/run_0_rolls_through", "B"): [],
    }

    @staticmethod
    def logged(vehicle):
        import json
        rows = [json.loads(line) for line in (vehicle / "lights.jsonl").read_text(encoding="utf-8").splitlines()]
        return rows

    def test_events_are_the_logged_transitions(self):
        for (run, owner), expected in self.EXPECTED.items():
            vehicle = ROOT / "traces" / run / "vehicles" / owner
            if not vehicle.exists():
                continue
            local = canonical_local(run, owner)
            found = sorted((n.event_type, round(n.t_local, 2)) for n in local.graph.nodes
                           if n.event_type.startswith("INDICATOR_"))
            self.assertEqual(found, sorted(expected), (run, owner))
            # Every transition of the log is an event and nothing else: count the on/off changes.
            rows, changes, previous = self.logged(vehicle), 0, (False, False)
            for row in rows:
                state = (row["left_blinker"], row["right_blinker"])
                changes += (state[0] != previous[0]) + (state[1] != previous[1])
                previous = state
            self.assertEqual(changes, len(expected), (run, owner))

    def test_signals_precede_the_turns(self):
        def first(run, owner, event):
            local = canonical_local(run, owner)
            return min(n.t_local for n in local.graph.nodes if n.event_type == event)
        if not (ROOT / "traces/S08/run_0_rolls_through/vehicles/A/lights.jsonl").exists():
            self.skipTest("canonical trace not present")
        self.assertLess(first("S08/run_0_rolls_through", "A", "INDICATOR_LEFT_START"),
                        first("S08/run_0_rolls_through", "A", "STOP_SIGN_DETECTED_START"))
        self.assertLess(first("S07/run_0_merge_conflict", "A", "INDICATOR_LEFT_START"),
                        first("S07/run_0_merge_conflict", "A", "TURN_LEFT_START"))
        b = "S07/run_0_merge_conflict"
        self.assertLess(first(b, "B", "INDICATOR_RIGHT_START"), first(b, "B", "TURN_RIGHT_START"))
        self.assertLess(first(b, "B", "TURN_RIGHT_END"), first(b, "B", "INDICATOR_RIGHT_END"))
        self.assertLess(first(b, "B", "INDICATOR_RIGHT_END"), first(b, "B", "COLLISION"))


class CaptureTests(unittest.TestCase):
    def test_an_indicator_left_on_does_not_extend_the_recording(self):
        from types import SimpleNamespace
        from src.cdf.simulation.runner import _scheduled_end
        spec = SimpleNamespace(participants=[SimpleNamespace(actions=[
            ScriptedAction("brake", "brake", 2.0, 3.0, {"intensity": 1.0}),
            ScriptedAction("signal", "indicator", 0.5, 60.0, {"side": -1.0})])])
        self.assertEqual(_scheduled_end(spec), 5.0)


if __name__ == "__main__":
    unittest.main()
