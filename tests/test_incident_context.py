"""The speed limit is supplied incident context: scenario -> incident_context.json -> reconstruction."""

import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.common.config import Config
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.pipeline import read_incident_context, reconstruct_run
from src.cdf.simulation.runner import write_incident_context
from src.cdf.simulation.scenario_base import ScenarioSpec

from synthetic_run import CONTACT_T, make_run


def _spec(context):
    scenario = {"scenario_id": "SX", "name": "x", "map": "Town05", "participants": [], "variants": {"v": {}}}
    if context is not None:
        scenario["context"] = context
    return ScenarioSpec.from_config(Config({"scenario": scenario}), variant="v")


class IncidentContextTests(unittest.TestCase):
    def test_scenario_context_is_parsed_and_copied_into_the_run(self):
        spec = _spec({"speed_limit_kmh": 30})
        self.assertEqual(spec.context, {"speed_limit_kmh": 30})
        with tempfile.TemporaryDirectory() as tmp:
            write_incident_context(Path(tmp), spec.context)
            written = json.loads((Path(tmp) / "incident_context.json").read_text())
            self.assertEqual(written["speed_limit_kmh"], 30)
            self.assertEqual(read_incident_context(Path(tmp))["speed_limit_kmh"], 30)

    def test_no_context_means_no_file_and_no_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_incident_context(Path(tmp), _spec(None).context)
            self.assertFalse((Path(tmp) / "incident_context.json").exists())
            self.assertEqual(read_incident_context(Path(tmp)), {})

    def test_invalid_speed_limits_are_rejected(self):
        for bad in (0, -30, "30", True):
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    write_incident_context(Path(tmp), {"speed_limit_kmh": bad})
                (Path(tmp) / "incident_context.json").write_text(json.dumps({"speed_limit_kmh": bad}))
                with self.assertRaises(ValueError):
                    read_incident_context(Path(tmp))

    def test_supplied_limit_produces_speed_limit_events(self):
        # A drives at 36 km/h and B at 21.6 km/h under a supplied 30 km/h limit.
        with tempfile.TemporaryDirectory() as tmp:
            result = reconstruct_run(make_run(Path(tmp), speed_limit_kmh=30), ReconstructionConfig())
        by_owner = {local.owner: [(n.event_type, n.t_local) for n in local.graph.nodes] for local in result.locals}
        self.assertIn(("SPEED_LIMIT_EXCEEDED_START", 0.0), by_owner["A"])
        self.assertIn(("SPEED_LIMIT_EXCEEDED_END", round(CONTACT_T, 4)), by_owner["A"])
        self.assertNotIn("SPEED_LIMIT_EXCEEDED_START", [name for name, _ in by_owner["B"]])
        self.assertEqual(result.locals[0].graph.recorder["incident_context"], {"speed_limit_kmh": 30})


if __name__ == "__main__":
    unittest.main()
