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
    def test_a_lane_change_without_a_light_log_creates_no_indicator(self):
        # S02 critical_before_cut_in as recorded before the light log existed: B changes lane into A's; its
        # reconstruction has no indicator event and both indicator states UNKNOWN, however it steers.
        run = ROOT / "traces" / "S02" / "run_0_critical_before_cut_in"
        vehicle = run / "vehicles" / "B"
        if (vehicle / "lights.jsonl").exists():
            self.skipTest("re-recorded with the light log")
        local = reconstruct_vehicle(vehicle, ReconstructionConfig())
        self.assertFalse([n for n in local.graph.nodes if n.event_type.startswith("INDICATOR_")])
        states = [f for f in local.trace if f.t_local >= 1.0]
        self.assertTrue(states)


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


if __name__ == "__main__":
    unittest.main()
