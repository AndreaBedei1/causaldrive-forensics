"""The manual review menu (scripts/review_canonical_runs.py) names the CARLA server it will use."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review_canonical_runs", str(ROOT / "scripts" / "review_canonical_runs.py"))
menu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(menu)


class ServerLine(unittest.TestCase):
    def test_the_port_passed_to_the_viewers_is_the_one_announced(self):
        self.assertIn("port 2000", menu.server_line(["--port", "2000", "--speed", "0.25"]))
        self.assertIn("port 3000", menu.server_line(["--speed", "0.25", "--port=3000"]))

    def test_without_a_port_the_configured_one_is_used(self):
        self.assertIn("configs/default.yaml", menu.server_line([]))


class ClockOffset(unittest.TestCase):
    """The two viewers' clocks: t_contact (first true contact) and t_global (the reconstruction's reference)."""

    S04B = ROOT / "traces" / "S04" / "run_0_b_rear_first"
    S01 = ROOT / "traces" / "S01" / "run_0_crash"

    def test_the_offset_between_the_two_clocks(self):
        self.assertAlmostEqual(menu.clock_offset(self.S04B), 1.55, delta=0.01)
        self.assertAlmostEqual(menu.clock_offset(self.S01), 0.0, delta=0.001)

    def test_the_menu_states_a_non_zero_offset(self):
        self.assertIn("t_contact = t_global + 1.55 s", menu.clock_note(self.S04B))
        self.assertIsNone(menu.clock_note(self.S01))


if __name__ == "__main__":
    unittest.main()
