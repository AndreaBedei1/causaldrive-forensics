"""S12 worked example: the reconstruction part reads admissible files only, the privileged part never feeds back."""

import unittest
from pathlib import Path

from src.cdf.evaluation.worked_example import (FileAudit, isolation_check, part_files, privileged_part,
                                               privileged_reads, reconstruction_part, render)

ROOT = Path(__file__).resolve().parents[1]
S12 = ROOT / "traces" / "S12" / "run_0_crash"


@unittest.skipUnless((S12 / "reconstruction" / "global" / "alignment.json").exists(), "S12 trace not present")
class S12WorkedExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.part = reconstruction_part(S12, "A", "track_001")

    def test_the_reconstruction_part_opens_admissible_files_only(self):
        self.assertEqual(privileged_reads(self.part.opened, S12), [])
        self.assertEqual(part_files(self.part, S12), [
            "reconstruction/A/local_graph.json", "reconstruction/A/local_trace.jsonl",
            "reconstruction/B/local_graph.json", "reconstruction/global/alignment.json",
            "reconstruction/global/associations.json", "reconstruction/global/global_graph.json",
            "vehicles/A/controls.jsonl"])

    def test_the_audit_catches_a_privileged_read(self):
        with FileAudit() as audit:
            (S12 / "ground_truth" / "metadata.json").read_text(encoding="utf-8")
        self.assertTrue(privileged_reads(audit.opened, S12))

    def test_s12_order_critical_cut_in_path_entry_reaction_conflict_collision(self):
        times = {}
        for row in self.part.timeline:
            times.setdefault((row.event, row.subject.split(" ")[0]), row.t_local)
        # U1 is A's leader only within its confirmed cut-in, dated at the onset of its lateral approach: the unsafe
        # gap starts within it (once U1's body is near A's corridor), before U1 enters A's path.
        self.assertLessEqual(times[("CUT_IN_FROM_RIGHT_START", "A:track_001")], times[("CRITICAL_TTC_START", "A:track_001")])
        self.assertLess(times[("CRITICAL_TTC_START", "A:track_001")], times[("EGO_PATH_ENTRY", "A:track_001")])
        sequence = [times[("CUT_IN_FROM_RIGHT_START", "A:track_001")],
                    times[("EGO_PATH_ENTRY", "A:track_001")], times[("steering command onset (controls.jsonl)", "-")],
                    times[("CRITICAL_TTC_START", "B")], times[("COLLISION", "B")]]
        self.assertEqual(sequence, sorted(sequence))
        self.assertEqual(len(set(sequence)), len(sequence))
        critical = next(r for r in self.part.timeline if r.event == "CRITICAL_TTC_START"
                        and r.subject.startswith("A:track_001"))
        self.assertEqual(critical.reason, "UNSAFE_FORWARD_GAP")
        self.assertLess(critical.clearance_m, critical.required_m)

    def test_a_establishes_u1_cutin_and_b_observes_a_lateral_manoeuvre(self):
        self.assertEqual(len(self.part.cut_ins["A"]), 1)
        self.assertIn("A:track_001", self.part.cut_ins["A"][0])
        self.assertEqual(len(self.part.cut_ins['B']),1)
        self.assertIn(' A (associated, B:track_001)',self.part.cut_ins['B'][0])

    def test_response_delays_are_measured_from_sensor_events_to_the_steering_command(self):
        delays = self.part.delays
        # The cut-in (the onset of U1's lateral approach) precedes the unsafe gap it makes.
        self.assertGreaterEqual(delays["perception (CUT_IN start) -> steering"],
                                delays["critical (CRITICAL_TTC_START on the track) -> steering"])
        self.assertGreater(delays["perception (CUT_IN start) -> steering"],
                           delays["path entry (EGO_PATH_ENTRY) -> steering"])
        self.assertGreater(delays["path entry (EGO_PATH_ENTRY) -> steering"], 0.0)

    def test_privileged_files_do_not_reach_the_reconstruction(self):
        result = isolation_check(S12)
        self.assertTrue(result["identical"], result["different_files"])
        self.assertGreater(result["compared_files"], 10)
        self.assertEqual(result["privileged_inputs_absent_from_copy"], ["ground_truth", "metadata.json"])

    def test_privileged_checks_pass_and_the_committed_report_is_current(self):
        truth = privileged_part(S12, self.part)
        self.assertTrue(all(passed for _, passed, _ in truth["checks"]), truth["checks"])
        committed = S12 / "reconstruction" / "evaluation" / "s12_worked_example.md"
        fresh = render(S12, self.part, isolation_check(S12), truth,
                       [0.5, 1.0, 2.0] + [round(2.3 + 0.1 * k, 1) for k in range(28)])
        self.assertEqual(committed.read_text(encoding="utf-8"), fresh)


if __name__ == "__main__":
    unittest.main()
