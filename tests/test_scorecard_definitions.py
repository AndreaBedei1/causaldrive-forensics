"""Final definitions of the scientific scorecard (cdf.evaluation.scorecard), fixed before the campaign v3 freeze.

* Collision recall and the identified rate are over the REPORTABLE contacts (a recorder is involved: no collision
  sensor reports a contact between two vehicles that record nothing).
* An extra collision node that is a true recontact reported as a collision of its own is a recontact split, not an
  invented collision; both count against precision.
* Position and speed errors of the road users exclude recorder ghosts (an anonymous road user that is in truth a
  recorder: counted apart, its error is not a road-user estimate).
* Phantoms (road users with no true identity) are split by the median distance of their tracks to the nearest true
  vehicle: near (<= 3 m, a displaced estimate of a vehicle) or far (clutter).
* Error statistics carry the RMSE; the tracker minimum for observability is the run's own configuration."""

import json
import unittest
from pathlib import Path

from src.cdf.evaluation.gt_audit import stats
from src.cdf.evaluation.scorecard import (PHANTOM_NEAR_M, _numbers, association_score, collision_score,
                                          run_min_track_frames)

ROOT = Path(__file__).resolve().parents[1]
S06 = ROOT / "traces" / "S06" / "run_0_crash"


def _evaluation(extras, contacts):
    return {"collisions": contacts, "extra_collisions": extras}


def _contact(pair, detected=True, correct=True):
    return {"participants": list(pair), "sim_time": 10.0, "reconstructed_as": "g1" if detected else None,
            "participants_correct": correct and detected, "report_timing_error_s": 0.0 if detected else None}


class Collisions(unittest.TestCase):
    def test_recall_is_over_the_contacts_a_recorder_can_report(self):
        evaluation = _evaluation([], [_contact("AB"), _contact("XY", detected=False)])
        score = collision_score(evaluation, ["A", "B"])
        self.assertEqual((score["true"], score["reportable"], score["detected"]), (2, 1, 1))
        self.assertEqual(score["recall"], 1.0)
        self.assertEqual(score["participants_correct_rate"], 1.0)

    def test_a_recontact_reported_apart_is_a_split_not_an_invention(self):
        extras = [{"node": "g7", "participants": ["A", "B"], "t_global": 0.65, "true_recontact": True},
                  {"node": "g9", "participants": ["A", "C"], "t_global": 3.0, "true_recontact": False}]
        score = collision_score(_evaluation(extras, [_contact("AB")]), ["A", "B", "C"])
        self.assertEqual((score["invented"], score["recontact_splits"]), (1, 1))
        self.assertAlmostEqual(score["precision"], 1.0 / 3.0)


class Association(unittest.TestCase):
    def test_wrong_and_missed_recorder_links_are_counted_as_the_evaluation_names_them(self):
        fusion = {"decision_counts": {"correct link": 3, "WRONG link": 2, "missed link": 1, "anonymous": 4},
                  "merges": {"correct": 1, "false": 0, "missed": 2}, "fragmentation": {"X": ["U1", "U2"], "Y": ["U3"]}}
        score = association_score(fusion, ["U9"])
        self.assertEqual((score["wrong_links"], score["missed_links"]), (2, 1))
        self.assertEqual(score["fragmented_vehicles"], {"X": ["U1", "U2"]})
        self.assertEqual(score["phantoms"], 1)


class Statistics(unittest.TestCase):
    def test_error_statistics_carry_the_rmse(self):
        self.assertAlmostEqual(stats([3.0, 4.0])["rmse"], (12.5) ** 0.5, places=4)


class Numbers(unittest.TestCase):
    def test_the_campaign_numbers_carry_the_new_definitions(self):
        card = json.loads((ROOT / "results" / "g0_scorecard_20261022" / "scorecard.json").read_text(encoding="utf-8"))
        card = card[0] if isinstance(card, list) else card["cards"][0]
        card["collisions"].setdefault("reportable", card["collisions"]["true"])
        numbers = _numbers(card)
        for key in ("reportable", "recontact_splits", "phantoms_near", "phantoms_far", "pos_rmse_m"):
            self.assertIn(key, numbers)



class MissingSemantics(unittest.TestCase):
    def test_without_the_event_oracle_the_unconfirmed_alarms_are_unknown_not_zero(self):
        card = json.loads((ROOT / "results" / "g0_scorecard_20261022" / "scorecard.json").read_text(encoding="utf-8"))[0]
        card["semantics"] = {"available": False}
        self.assertIsNone(_numbers(card)["unconfirmed_ttc"])


class RunMetrics(unittest.TestCase):
    def test_the_fused_centre_error_of_the_run_metrics_leaves_recorder_ghosts_out(self):
        from src.cdf.evaluation.run_metrics import run_metrics
        run = ROOT / "traces" / "S01" / "run_0_crash"
        evaluation = json.loads((run / "reconstruction" / "evaluation" / "evaluation.json").read_text(encoding="utf-8"))
        fusion = json.loads((run / "reconstruction" / "evaluation" / "fusion_metrics.json").read_text(encoding="utf-8"))
        fusion["state_errors"] = {"centre_error_m": {"median": 1.75}}
        fusion["road_user_state_errors"] = {"centre_error_m": {"median": 0.25}}
        self.assertEqual(run_metrics(run, evaluation, fusion)["fused_centre_error_median_m"], 0.25)
        # A run whose only fused road users are recorder ghosts has no road-user error at all (S06).
        fusion["road_user_state_errors"] = {}
        self.assertIsNone(run_metrics(run, evaluation, fusion)["fused_centre_error_median_m"])


class PairedConditions(unittest.TestCase):
    def test_a_job_without_its_baseline_leaves_the_paired_change_of_the_others(self):
        from src.cdf.evaluation.scorecard import condition_table
        rows = [{"family": "radar_v3", "level": "severe", "recorder": None, "recorders": 2, "seed": 0,
                 "status": "complete", "identified": 1, "reportable": 1, "contacts": 1, "detected": 1, "invented": 0,
                 "represented": 1, "observable": 1, "duplicates": 0, "rec_ghosts": 0, "phantoms": p, "pos_med_m": 0.2,
                 "d_identified": 0, "d_invented": 0, "d_represented": 0, "d_duplicates": 0, "d_phantoms": d}
                for p, d in ((4, 4), (6, None))]
        row = condition_table(rows)[0]
        self.assertEqual(row["d_phantoms"], 4.0)


class RunConfiguration(unittest.TestCase):
    def test_the_tracker_minimum_is_the_one_the_reconstruction_used(self):
        graph = json.loads((S06 / "reconstruction" / "global" / "global_graph.json").read_text(encoding="utf-8"))
        self.assertEqual(run_min_track_frames(S06), graph["reconstruction_config"]["tracking"]["min_track_frames"])
        self.assertEqual(PHANTOM_NEAR_M, 3.0)


if __name__ == "__main__":
    unittest.main()
