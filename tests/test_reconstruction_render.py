"""Human-readable output states the context, open states and simultaneity."""

import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.pipeline import reconstruct_run

from synthetic_run import make_run


class RenderTests(unittest.TestCase):
    def test_rendered_files_are_sparse_and_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp), speed_limit_kmh=30)
            reconstruct_run(run, ReconstructionConfig())
            rec = run / "reconstruction"
            local_md = (rec / "A" / "local_graph.md").read_text(encoding="utf-8")
            local_dot = (rec / "A" / "local_graph.dot").read_text(encoding="utf-8")
            global_md = (rec / "global" / "global_graph.md").read_text(encoding="utf-8")
            report = (rec / "report.md").read_text(encoding="utf-8")

        self.assertIn("Speed limit 30 km/h, supplied as incident context", local_md)
        self.assertIn("Speed limit 30 km/h, supplied as incident context", report)
        self.assertIn("- BRAKE, since A:e06", local_md)  # still braking when the recording ends
        self.assertIn("A began exceeding the speed limit (already the case when first observed)", local_md)
        # Simultaneous events share a DOT column and are listed as unresolved in the report.
        self.assertIn('{rank=same; "A:e07"; "A:e08"; "A:e09"; "A:e10";}', local_dot)
        self.assertIn("COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A)", report)
        self.assertIn("simultaneous at 0.05 s resolution", global_md)
        # DOT labels stay minimal: type, who, time.
        self.assertIn('"A:e06" [label="BRAKE_START\\nA\\nt=3.00"', local_dot)


if __name__ == "__main__":
    unittest.main()
