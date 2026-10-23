"""The road map is supplied incident context (``incident_context.json``: ``map``), like the speed limit: an
investigation knows where the incident happened.  The CARLA towns share coordinates around the origin, so a
recorder's own poses can fit a lane of another town; with the supplied map the reconstruction, the event oracle and
the RECONSTRUCTION viewer use the incident's map, never the simulator server's state."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import load_config
from src.cdf.reconstruction.local import reconstruct_vehicle
from src.cdf.reconstruction.pipeline import incident_map, read_incident_context
from src.cdf.simulation.runner import write_incident_context

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = sorted(p.parent for p in (ROOT / "traces").glob("S*/run_0_*/metadata.json"))
S06 = ROOT / "traces" / "S06" / "run_0_crash"


class Context(unittest.TestCase):
    def test_the_runner_writes_the_scenario_map_into_the_incident_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_incident_context(Path(tmp), {"speed_limit_kmh": 50}, "Town03_Opt")
            context = json.loads((Path(tmp) / "incident_context.json").read_text(encoding="utf-8"))
        self.assertEqual((context["map"], context["speed_limit_kmh"]), ("Town03_Opt", 50))

    def test_a_map_must_be_a_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "incident_context.json").write_text(json.dumps({"map": ""}), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_incident_context(Path(tmp))

    def test_every_canonical_run_supplies_the_map_it_was_recorded_on(self):
        self.assertEqual(len(CANONICAL), 22)
        for run in CANONICAL:
            acquired = json.loads((run / "ground_truth" / "metadata.json").read_text(encoding="utf-8"))["map"]
            self.assertEqual(incident_map(run), acquired, str(run))
        self.assertEqual(incident_map(ROOT / "traces" / "S07" / "run_0_merge_conflict"), "Town03_Opt")
        self.assertEqual(incident_map(ROOT / "traces" / "S19" / "run_0_highway_curve"), "Town04")


class RoadModel(unittest.TestCase):
    """S06, recorder C: its own poses fit a Town01 lane better than the Town05 lanes it drove on."""

    def _road_map(self, context):
        with tempfile.TemporaryDirectory() as tmp:
            vehicle = Path(tmp) / "C"
            shutil.copytree(str(S06 / "vehicles" / "C"), str(vehicle))
            local = reconstruct_vehicle(vehicle, load_config(), context=context)
        return local.graph.recorder["road_map"]

    def test_the_supplied_map_is_the_recorders_road(self):
        self.assertEqual(self._road_map(read_incident_context(S06)), {"name": "Town05", "source": "incident context"})

    def test_without_a_supplied_map_the_recorders_own_poses_choose_it(self):
        self.assertEqual(self._road_map({"speed_limit_kmh": 50}), {"name": "Town01", "source": "own poses"})


class Viewer(unittest.TestCase):
    def test_the_reconstruction_viewer_takes_the_supplied_map(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("replay_run", str(ROOT / "scripts" / "replay_run.py"))
        replay_run = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(replay_run)
        for run, expected in (("S07/run_0_merge_conflict", "Town03_Opt"), ("S19/run_0_highway_curve", "Town04"),
                              ("S01/run_0_crash", "Town05")):
            args = replay_run.parse_args([str(ROOT / "traces" / run)])
            self.assertEqual(replay_run.supplied_map(args), (expected, "the supplied incident context"), run)
        args = replay_run.parse_args([str(ROOT / "traces" / "S07" / "run_0_merge_conflict"), "--map", "Town03"])
        self.assertEqual(replay_run.supplied_map(args), ("Town03", "--map"))


if __name__ == "__main__":
    unittest.main()
