"""The ground-truth event oracle (privileged evaluation): its ideal tracks reproduce the true geometry, its
events follow the reconstruction's definitions, coverage never adds events, and the matching is one to one."""

import importlib.util
import json
import math
import unittest
from pathlib import Path

from src.cdf.evaluation.event_oracle import (COMPARISONS, ideal_samples, match, oracle_events, prepare_truth,
                                             reconstruction_events)
from src.cdf.evaluation.reconstruction import box_gap
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.local import read_jsonl
from src.cdf.evaluation.visibility import frames_by_participant

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"


def _load_script(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = ReconstructionConfig()
        cls.truth = prepare_truth(S17, cls.cfg)
        cls.events = oracle_events(S17, cls.cfg, cls.truth)

    def test_ideal_clearance_is_the_true_box_gap(self):
        states = read_jsonl(S17 / "ground_truth" / "states.jsonl")
        frames = frames_by_participant(states)
        rec = self.truth["recorders"]["A"]
        samples = {round(s.t_local, 2): s for s in self.truth["ideal"]["A"]["C"]["samples"]}
        checked = 0
        for frame, t in rec.sweeps[::20]:
            sample = samples.get(round(t, 2))
            if sample is None or "C" not in frames[frame]:
                continue
            true_gap = box_gap(frames[frame]["A"], frames[frame]["C"])
            self.assertAlmostEqual(sample.clearance_m, true_gap, delta=0.08)
            checked += 1
        self.assertGreater(checked, 5)

    def test_ideal_track_agrees_with_the_radar_track_of_the_same_vehicle(self):
        # A:track_002 is B (privileged evaluation); its near surface against the ideal one, while tracked.
        evaluation = json.loads((S17 / "reconstruction" / "evaluation" / "evaluation.json").read_text())
        self.assertEqual({r["track"]: r["true_identity"] for r in evaluation["tracks"]}["A:track_002"], "B")
        tracks = {row["track_id"]: row for row in read_jsonl(S17 / "reconstruction" / "A" / "local_tracks.jsonl")
                  if row["track_id"] == "track_002"}
        self.assertTrue(tracks)
        ideal = {round(s.t_local, 2): s for s in self.truth["ideal"]["A"]["B"]["samples"]}
        rows = [r for r in read_jsonl(S17 / "reconstruction" / "A" / "local_tracks.jsonl") if r["track_id"] == "track_002"]
        speeds = []
        for row in rows:
            sample = ideal.get(round(float(row["t_local"]), 2))
            if sample is not None:
                speeds.append(abs(float(row["speed_mps"]) - sample.speed_mps))
        self.assertGreater(len(speeds), 20)
        self.assertLess(sorted(speeds)[len(speeds) // 2], 0.5)

    def test_the_tracked_point_lies_on_the_faces_the_radars_see(self):
        nearest = self.truth["ideal"]["A"]["B"]["samples"]
        tracked = self.truth["ideal"]["A"]["B"]["tracked"]
        self.assertEqual(len(nearest), len(tracked))
        for a, b in zip(nearest[::25], tracked[::25]):
            self.assertAlmostEqual(a.clearance_m, b.clearance_m, places=9)  # the clearance stays the nearest point's
            self.assertGreaterEqual(b.surface_offset_m, 0.0)  # the tracked point lies behind the near surface
            self.assertLess(b.surface_offset_m, 4.0)

    def test_s17_hazards_are_where_the_ground_truth_puts_them(self):
        perfect = {(e["type"], e["subject"]): e["t_local"] for e in self.events["PERFECT"]["A"]}
        self.assertAlmostEqual(perfect[("CRITICAL_TTC_START", "C")], 2.30, places=2)
        self.assertIn(("CUT_IN_FROM_RIGHT_START", "C"), perfect)
        self.assertIn(("CRITICAL_TTC_START", "B"), perfect)
        self.assertNotIn("TRACK_APPEARED", {t for t, _ in perfect})

    def test_coverage_never_adds_an_event_to_perfect_perception(self):
        for owner, events in self.events["COVERAGE"].items():
            perfect = self.events["PERFECT"][owner]
            for event in events:
                if event["type"] in ("TRACK_APPEARED", "CRITICAL_TTC_END"):
                    continue  # a coverage piece starts an appearance; its end may cut an episode short
                self.assertTrue(any(p["type"] == event["type"] and p["subject"] == event["subject"]
                                    and p["t_local"] <= event["t_local"] + 1e-6 for p in perfect), event)

    def test_reconstruction_events_carry_the_true_identity_of_their_track(self):
        events = reconstruction_events(S17)
        subjects = {(e["track"], e["subject"]) for e in events["A"]}
        self.assertIn(("track_001", "C"), subjects)
        self.assertIn(("track_002", "B"), subjects)


class MatchTests(unittest.TestCase):
    def event(self, t, subject="B", kind="CRITICAL_TTC_START"):
        return {"type": kind, "subject": subject, "t_local": t, "side": kind}

    def test_one_to_one_nearest_first_within_the_window(self):
        found = [self.event(1.0), self.event(1.2), self.event(9.0)]
        expected = [self.event(1.05), self.event(5.0)]
        pairs, extra, missed = match(found, expected, window_s=2.0)
        self.assertEqual(pairs, [(0, 0)])
        self.assertEqual(extra, [1, 2])
        self.assertEqual(missed, [1])

    def test_type_and_subject_must_agree_and_unknown_subjects_never_match(self):
        found = [self.event(1.0, "C"), self.event(1.0, None), self.event(1.0, "B", "EGO_PATH_ENTRY")]
        expected = [self.event(1.0, "B"), self.event(1.0, None)]
        pairs, _, missed = match(found, expected)
        self.assertEqual(pairs, [])
        self.assertEqual(missed, [0, 1])

    def test_every_comparison_is_reported(self):
        self.assertEqual([f + " vs " + e for f, e in COMPARISONS],
                         ["RECONSTRUCTION vs COVERAGE", "RECONSTRUCTION vs COVERAGE_TRACKED", "RECONSTRUCTION vs PERFECT",
                          "COVERAGE_TRACKED vs COVERAGE", "COVERAGE vs PERFECT"])


class SensitivityTests(unittest.TestCase):
    def test_variants_change_one_threshold_only(self):
        module = _load_script("semantic_sensitivity")
        base = ReconstructionConfig().semantics
        scaled = module.variant_semantics(base, "critical_time_gap_table", "x1.2")
        for (speed, gap), (speed2, gap2) in zip(base.critical_time_gap_table, scaled.critical_time_gap_table):
            self.assertEqual(speed, speed2)
            self.assertAlmostEqual(gap2, round(gap * 1.2, 3))
        width = module.variant_semantics(base, "path_half_width_m", 1.75)
        self.assertEqual(width.path_half_width_m, 1.75)
        self.assertEqual(width.critical_reaction_time_s, base.critical_reaction_time_s)
        names = [name for name, _, _ in module.VARIANTS]
        self.assertEqual(len(names), len(set(names)))
        for name, values, _ in module.VARIANTS:
            if name != "critical_time_gap_table":
                self.assertTrue(hasattr(base, name), name)
                self.assertNotIn(getattr(base, name), values)


if __name__ == "__main__":
    unittest.main()
