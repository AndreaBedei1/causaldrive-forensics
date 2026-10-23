"""Each true collision against the reconstruction's COLLISION nodes (cdf.evaluation.reconstruction.match_collisions):
IDENTIFIED by a node naming exactly its recorders; else DETECTED with the wrong participants by a node one of its own
recorders reported at that time (its collision sensor felt it); else MISSED.  Nodes matched neither way are extra."""

import unittest

from src.cdf.evaluation.reconstruction import match_collisions

ORIGINS = {"A": 100.0, "B": 200.0, "C": 300.0}


def _contact(pair, sim_time):
    return {"participants": sorted(pair), "sim_time": sim_time, "peak_impulse": 1000.0, "recontacts": []}


def _node(node_id, participants, sim_times):
    """A COLLISION node observed by each participant at the given simulator time (local time = sim - origin)."""
    return {"node_id": node_id, "participants": sorted(participants), "t_global": 0.0,
            "observations": [{"graph": g, "local_node": g + ":e1", "t_local": t - ORIGINS[g]}
                             for g, t in zip(participants, sim_times)]}


class Matching(unittest.TestCase):
    def test_a_node_naming_the_collisions_recorders_identifies_it(self):
        rows, used = match_collisions([_contact("AB", 110.0)], [_node("g1", ["A", "B"], [110.0, 110.05])],
                                      ["A", "B"], ORIGINS)
        self.assertEqual((rows[0]["reconstructed_as"], rows[0]["participants_correct"]), ("g1", True))
        self.assertEqual(rows[0]["reconstructed_participants"], ["A", "B"])
        self.assertAlmostEqual(rows[0]["report_timing_error_s"], 0.05)
        self.assertEqual(used, {"g1"})

    def test_a_node_with_the_wrong_partner_detects_the_collision_without_identifying_it(self):
        # A-B happened; the reconstruction paired A's report with C's.
        rows, used = match_collisions([_contact("AB", 110.0)], [_node("g1", ["A", "C"], [110.0, 110.1])],
                                      ["A", "B", "C"], ORIGINS)
        self.assertEqual((rows[0]["reconstructed_as"], rows[0]["participants_correct"]), ("g1", False))
        self.assertEqual(rows[0]["reconstructed_participants"], ["A", "C"])
        self.assertEqual(used, {"g1"})

    def test_an_unpaired_report_of_one_recorder_detects_the_collision_without_identifying_it(self):
        rows, _ = match_collisions([_contact("AB", 110.0)], [_node("g1", ["A"], [110.2])], ["A", "B"], ORIGINS)
        self.assertEqual((rows[0]["reconstructed_as"], rows[0]["participants_correct"]), ("g1", False))

    def test_an_exact_match_is_never_taken_by_a_wrong_one(self):
        # A-C at 110.0 is identified by g2; A-B at 110.1 has only g2 near it, already used: missed.
        rows, used = match_collisions([_contact("AB", 110.1), _contact("AC", 110.0)],
                                      [_node("g2", ["A", "C"], [110.0, 110.0])], ["A", "B", "C"], ORIGINS)
        by_pair = {"-".join(r["participants"]): r for r in rows}
        self.assertEqual(by_pair["A-C"]["reconstructed_as"], "g2")
        self.assertIsNone(by_pair["A-B"]["reconstructed_as"])
        self.assertEqual(used, {"g2"})

    def test_a_report_far_from_the_collision_or_by_another_recorder_detects_nothing(self):
        rows, used = match_collisions([_contact("AB", 110.0)],
                                      [_node("g1", ["A"], [111.0]), _node("g2", ["C"], [110.0])],
                                      ["A", "B", "C"], ORIGINS)
        self.assertIsNone(rows[0]["reconstructed_as"])
        self.assertEqual(used, set())


if __name__ == "__main__":
    unittest.main()
