"""The CARLA launch command: quality level and unattended mode."""

import tempfile
import unittest
from pathlib import Path

from src.cdf.common.config import load_run_config
from src.cdf.simulation.carla_client import CarlaServer, session_from_config


def _fake_root(tmp):
    (Path(tmp) / "CarlaUE4.exe").write_bytes(b"")
    return tmp


class CarlaServerCommandTests(unittest.TestCase):
    def test_default_is_epic_quality_and_unattended(self):
        # Low quality crashes CARLA 0.9.15 deterministically in some scenarios.
        with tempfile.TemporaryDirectory() as tmp:
            command = CarlaServer(root=_fake_root(tmp), gpu=None).command()
        self.assertIn("-quality-level=Epic", command)
        self.assertIn("-unattended", command)
        self.assertIn("-RenderOffScreen", command)

    def test_low_quality_and_dialogs_remain_available_on_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = CarlaServer(root=_fake_root(tmp), gpu=None, quality="Low", unattended=False).command()
        self.assertIn("-quality-level=Low", command)
        self.assertNotIn("-unattended", command)

    def test_configuration_selects_the_quality_level(self):
        cfg = load_run_config("S01")
        self.assertEqual(cfg.get("simulation.quality_level"), "Epic")
        self.assertIs(cfg.get("simulation.unattended"), True)
        with tempfile.TemporaryDirectory() as tmp:
            session = session_from_config(cfg, autostart=False)
            session.server.root = Path(_fake_root(tmp))
            session.server.gpu = None
            command = session.server.command()
        self.assertIn("-quality-level=Epic", command)
        self.assertIn("-unattended", command)


if __name__ == "__main__":
    unittest.main()
