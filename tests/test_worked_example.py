"""S17 worked example: the reconstruction part reads admissible files only, the privileged part never feeds back."""

import unittest
from pathlib import Path

from src.cdf.evaluation.worked_example import (FileAudit, isolation_check, part_files, privileged_part,
                                               privileged_reads, reconstruction_part, render)

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"


@unittest.skipUnless((S17 / "reconstruction" / "global" / "alignment.json").exists(), "S17 trace not present")
class S17WorkedExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.part = reconstruction_part(S17, "A", "track_001")

    def test_the_reconstruction_part_opens_admissible_files_only(self):
        self.assertEqual(privileged_reads(self.part.opened, S17), [])
        self.assertEqual(part_files(self.part, S17), [
            "reconstruction/A/local_graph.json", "reconstruction/A/local_trace.jsonl",
            "reconstruction/B/local_graph.json", "reconstruction/global/alignment.json",
            "reconstruction/global/associations.json", "reconstruction/global/global_graph.json",
            "vehicles/A/controls.jsonl"])

    def test_the_audit_catches_a_privileged_read(self):
        with FileAudit() as audit:
            (S17 / "ground_truth" / "metadata.json").read_text(encoding="utf-8")
        self.assertTrue(privileged_reads(audit.opened, S17))

    def test_s17_order_critical_cut_in_path_entry_reaction_conflict_collision(self):
        times = {}
        for row in self.part.timeline:
            times.setdefault((row.event, row.subject.split(" ")[0]), row.t_local)
        sequence = [times[("CRITICAL_TTC_START", "A:track_001")], times[("CUT_IN_FROM_RIGHT_START", "A:track_001")],
                    times[("EGO_PATH_ENTRY", "A:track_001")], times[("steering command onset (controls.jsonl)", "-")],
                    times[("CRITICAL_TTC_START", "B")], times[("COLLISION", "B")]]
        self.assertEqual(sequence, sorted(sequence))
        self.assertEqual(len(set(sequence)), len(sequence))
        critical = next(r for r in self.part.timeline if r.event == "CRITICAL_TTC_START"
                        and r.subject.startswith("A:track_001"))
        self.assertEqual(critical.reason, "UNSAFE_FORWARD_GAP")
        self.assertLess(critical.clearance_m, critical.required_m)

    def test_only_a_establishes_a_cut_in(self):
        self.assertEqual(len(self.part.cut_ins["A"]), 1)
        self.assertIn("A:track_001", self.part.cut_ins["A"][0])
        self.assertEqual(self.part.cut_ins["B"], [])

    def test_response_delays_are_measured_from_sensor_events_to_the_steering_command(self):
        delays = self.part.delays
        self.assertGreater(delays["critical (CRITICAL_TTC_START on the track) -> steering"],
                           delays["perception (CUT_IN start) -> steering"])
        self.assertGreater(delays["perception (CUT_IN start) -> steering"],
                           delays["path entry (EGO_PATH_ENTRY) -> steering"])
        self.assertGreater(delays["path entry (EGO_PATH_ENTRY) -> steering"], 0.0)

    def test_privileged_files_do_not_reach_the_reconstruction(self):
        result = isolation_check(S17)
        self.assertTrue(result["identical"], result["different_files"])
        self.assertGreater(result["compared_files"], 10)
        self.assertEqual(result["privileged_inputs_absent_from_copy"], ["ground_truth", "metadata.json"])

    def test_privileged_checks_pass_and_the_committed_report_is_current(self):
        truth = privileged_part(S17, self.part)
        self.assertTrue(all(passed for _, passed, _ in truth["checks"]), truth["checks"])
        committed = S17 / "reconstruction" / "evaluation" / "s17_worked_example.md"
        fresh = render(S17, self.part, isolation_check(S17), truth,
                       [0.5, 1.0, 2.0] + [round(2.3 + 0.1 * k, 1) for k in range(28)])
        self.assertEqual(committed.read_text(encoding="utf-8"), fresh)


if __name__ == "__main__":
    unittest.main()
