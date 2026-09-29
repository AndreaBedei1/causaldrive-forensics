"""The reconstruction must never use privileged simulator data as inference input."""

import ast
import builtins
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.pipeline import reconstruct_run

from synthetic_run import make_run

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "cdf" / "reconstruction"
FORBIDDEN_IMPORTS = ("carla", "simulation", "ground_truth_logger", "evaluation")


class BoundaryTests(unittest.TestCase):
    def test_reconstruction_source_never_names_privileged_inputs(self):
        for path in sorted(PACKAGE.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""]
                else:
                    names = []
                for name in names:
                    for forbidden in FORBIDDEN_IMPORTS:
                        self.assertNotIn(forbidden, name, "{0} imports {1}".format(path.name, name))
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value.strip()
                    # Path components and privileged fields (prose may still mention them).
                    self.assertNotEqual(value, "ground_truth", path.name)
                    self.assertFalse(value.startswith(("ground_truth/", "ground_truth\\")), path.name)
                    self.assertNotIn("other_actor_id", value, path.name)
                    self.assertNotIn("states.jsonl", value, path.name)

    def test_importing_the_pipeline_loads_no_privileged_module(self):
        code = ("import sys; sys.path.insert(0, 'src'); import cdf.reconstruction.pipeline; "
                "print([m for m in sys.modules if 'ground_truth' in m or 'simulation' in m "
                "or m == 'carla' or m.startswith('cdf.evaluation')])")
        output = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertEqual(output.stdout.strip(), "[]")

    def test_reconstruction_never_opens_ground_truth_or_scenario_metadata(self):
        real_open = builtins.open
        real_path_open = pathlib.Path.open
        forbidden_files = set()

        def check(path):
            if "ground_truth" in str(path) or Path(str(path)).resolve() in forbidden_files:
                raise AssertionError("reconstruction opened " + str(path))

        def guarded_open(file, *args, **kwargs):
            check(file)
            return real_open(file, *args, **kwargs)

        def guarded_path_open(self, *args, **kwargs):
            check(self)
            return real_path_open(self, *args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp:
            with_truth = make_run(Path(tmp) / "with" / "S00" / "run_0", with_ground_truth=True, speed_limit_kmh=30)
            without_truth = make_run(Path(tmp) / "without" / "S00" / "run_0", with_ground_truth=False,
                                     speed_limit_kmh=30)
            # The run's metadata.json names the scenario and variant: scenario design.
            forbidden_files.add((with_truth / "metadata.json").resolve())
            with mock.patch("builtins.open", guarded_open), mock.patch.object(pathlib.Path, "open", guarded_path_open):
                result = reconstruct_run(with_truth, ReconstructionConfig())
            reconstruct_run(without_truth, ReconstructionConfig())
            # The poisoned privileged folder changes nothing in the output.
            first = json.loads((with_truth / "reconstruction" / "global" / "global_graph.json").read_text())
            second = json.loads((without_truth / "reconstruction" / "global" / "global_graph.json").read_text())
        # The supplied incident context, by contrast, is read.
        self.assertEqual(result.locals[0].graph.recorder["incident_context"], {"speed_limit_kmh": 30})
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
