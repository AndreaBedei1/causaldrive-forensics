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
        # The perceived state is rendered compactly, once per timestamp, never as JSON in the node table.
        self.assertIn("## Perceived state before each event", local_md)
        self.assertIn("| 3.00 | A:e06 BRAKE_START | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: "
                      "CLOSING, CRITICAL_TTC, IN_EGO_PATH | 2.90 |", local_md)
        self.assertNotIn('{"ego"', local_md)
        # The appearance side is part of the event and of the plain-language reading.
        self.assertIn("| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 |", local_md)
        self.assertIn("A's radar started tracking track_001, which appeared in front of it", local_md)
        for gone in ("VISIBLE", "visible", "PATH_CONFLICT"):
            self.assertNotIn(gone, local_md.replace("visible surface", ""))
            self.assertNotIn(gone, global_md.replace("visible surface", ""))
        self.assertIn("## Perceived state before each event, per observing recorder", global_md)
        self.assertIn("### Perceived state just before each collision report", report)
        self.assertIn("### Tracks lost while a state was active", report)


if __name__ == "__main__":
    unittest.main()
