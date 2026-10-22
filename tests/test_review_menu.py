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


if __name__ == "__main__":
    unittest.main()
