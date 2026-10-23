"""Path intrusions in the scorecard: EGO_PATH_ENTRY and CUT_IN_*_START about the same target are one manoeuvre, in
either order and with either kind (spec: no penalty for an equivalent event a few tenths of a second off)."""

import unittest

from src.cdf.evaluation.scorecard import match_intrusions


class IntrusionManoeuvres(unittest.TestCase):
    def test_both_kinds_from_the_oracle_and_one_from_the_reconstruction_are_one_found_manoeuvre(self):
        result = match_intrusions([5.0, 5.3], [5.1])
        self.assertEqual((result["expected"], result["found"], result["missed"], result["extra"]), (1, 1, [], []))

    def test_two_reconstruction_reports_of_one_manoeuvre_are_not_an_extra(self):
        result = match_intrusions([5.0], [5.1, 5.4])
        self.assertEqual((result["expected"], result["found"], result["missed"], result["extra"]), (1, 1, [], []))

    def test_a_later_manoeuvre_is_separate(self):
        result = match_intrusions([5.0, 9.0], [5.1])
        self.assertEqual((result["expected"], result["found"], result["missed"], result["extra"]), (2, 1, [9.0], []))

    def test_a_report_without_oracle_manoeuvre_is_extra(self):
        result = match_intrusions([], [3.0, 3.5, 12.0])
        self.assertEqual((result["expected"], result["found"], result["extra"]), (0, 0, [3.0, 12.0]))

    def test_the_window_bounds_the_match(self):
        self.assertEqual(match_intrusions([5.0], [7.5])["found"], 0)
        self.assertEqual(match_intrusions([5.0], [6.9])["found"], 1)


if __name__ == "__main__":
    unittest.main()
