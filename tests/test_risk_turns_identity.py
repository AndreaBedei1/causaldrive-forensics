"""Dynamic critical TTC, recorder turns, temporal safety relations and identity association."""

import dataclasses
import math
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.alignment import align_graphs
from src.cdf.reconstruction.checks import temporal_safety_relations
from src.cdf.reconstruction.config import FusionConfig, ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.fusion import associate_tracks
from src.cdf.reconstruction.local import (build_local_graph, critical_ttc_assessment, number_events,
                                          reconstruct_vehicle, turn_events)
from src.cdf.reconstruction.models import SemanticEvent, TraceFrame
from src.cdf.reconstruction.pipeline import read_incident_context, reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory, LocalTrack

from synthetic_run import make_run

CFG = SemanticsConfig()
ROOT = Path(__file__).resolve().parents[1]


def critical(ego, target, closing, range_m):
    return critical_ttc_assessment(ego, target, closing, range_m, CFG)


class CriticalTtcTests(unittest.TestCase):
    def test_ttc_is_range_over_closing_speed(self):
        self.assertAlmostEqual(critical(10.0, 0.0, 10.0, 25.0).ttc_s, 2.5)
        self.assertIsNone(critical(10.0, 10.5, -0.5, 25.0).ttc_s)  # opening: no TTC

    def test_the_threshold_and_the_required_deceleration_agree(self):
        for speed in (3.0, 6.0, 10.0, 15.0, 20.0):
            for range_m in (5.0, 10.0, 20.0, 40.0):
                a = critical(speed, 0.0, speed, range_m)
                self.assertEqual(a.critical, a.ttc_s <= a.threshold_s + 1e-9, (speed, range_m))
                expected = CFG.critical_reaction_time_s + speed / (2 * CFG.critical_deceleration_mps2) \
                    + CFG.critical_standstill_margin_m / speed
                self.assertAlmostEqual(a.threshold_s, expected)

    def test_same_distance_higher_closing_speed_is_at_least_as_critical(self):
        for make in (lambda c: critical(c, 0.0, c, 20.0),          # faster recorder, standing target
                     lambda c: critical(16.0, 16.0 - c, c, 20.0)):  # same recorder, slower target
            previous = None
            for closing in (1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0):
                a = make(closing)
                if previous is not None:
                    self.assertGreaterEqual(a.required_deceleration_mps2, previous.required_deceleration_mps2)
                    self.assertTrue(a.critical or not previous.critical)
                previous = a
            self.assertTrue(previous.critical)

    def test_a_target_at_nearly_the_recorder_speed_is_not_critical(self):
        for gap in (1.5, 3.0, 10.0):
            self.assertFalse(critical(14.0, 13.8, 0.2, gap).critical)
            self.assertFalse(critical(14.0, 14.6, -0.6, gap).critical)

    def test_a_fast_recorder_becomes_critical_earlier_at_a_standing_target(self):
        def first_critical_range(speed):
            return next(r / 2.0 for r in range(200, 0, -1) if critical(speed, 0.0, speed, r / 2.0).critical)
        self.assertGreater(first_critical_range(15.0), first_critical_range(5.0))
        self.assertGreater(critical(15.0, 0.0, 15.0, 50.0).threshold_s, critical(5.0, 0.0, 5.0, 50.0).threshold_s)

    def test_too_late_to_stop_is_critical_with_no_margin(self):
        a = critical(15.0, 0.0, 15.0, 1.0)
        self.assertTrue(a.critical)
        self.assertTrue(math.isinf(a.required_deceleration_mps2))
        self.assertIsNone(a.braking_margin_mps2)

    def test_crossing_and_oncoming_targets_need_a_full_stop(self):
        # A crossing target has no speed along the recorder's heading; an oncoming one a negative one.
        self.assertEqual(critical(10.0, 0.0, 7.0, 20.0).speed_to_shed_mps, 10.0)
        self.assertEqual(critical(10.0, -8.0, 18.0, 20.0).speed_to_shed_mps, 10.0)
        self.assertEqual(critical(10.0, 6.0, 4.0, 20.0).speed_to_shed_mps, 4.0)


def _turning_ego(rate_dps, start, end, speed=8.0, total=8.0):
    """The recorder at ``speed`` yawing at ``rate_dps`` between ``start`` and ``end``."""
    states, x, y, heading = [], 0.0, 0.0, 0.0
    for k in range(int(round(total / 0.05)) + 1):
        t = round(0.05 * k, 2)
        states.append(EgoState(t_local=t, x=x, y=y, heading=heading, vx=speed * math.cos(heading),
                               vy=speed * math.sin(heading)))
        if start <= t < end:
            heading += math.radians(rate_dps) * 0.05
        x, y = x + speed * math.cos(heading) * 0.05, y + speed * math.sin(heading) * 0.05
    return EgoTrajectory(states)


def _turns(ego):
    return [(e.type, e.t_local, bool(e.attributes.get("active_at_first_observation")))
            for e in sorted(turn_events("A", ego, CFG), key=lambda e: e.t_local)]


class TurnTests(unittest.TestCase):
    def test_left_turn_from_a_decreasing_heading(self):
        # -30 deg/s from 2 s to 4 s; over the preceding 0.2 s the rate reaches 10 deg/s at 2.10 s
        # and drops below 5 deg/s at 4.20 s.
        self.assertEqual(_turns(_turning_ego(-30.0, 2.0, 4.0)),
                         [("TURN_LEFT_START", 2.1, False), ("TURN_LEFT_END", 4.2, False)])

    def test_right_turn_from_an_increasing_heading(self):
        self.assertEqual([name for name, _, _ in _turns(_turning_ego(30.0, 2.0, 4.0))],
                         ["TURN_RIGHT_START", "TURN_RIGHT_END"])

    def test_lane_change_and_small_heading_changes_are_not_turns(self):
        lane_change = _turning_ego(8.0, 2.0, 3.0)  # 8 deg/s: below the on threshold
        self.assertEqual(_turns(lane_change), [])
        self.assertEqual(_turns(_turning_ego(25.0, 2.0, 2.4)), [])  # 10 deg in 0.4 s: too short and small

    def test_no_turn_while_standing(self):
        self.assertEqual(_turns(_turning_ego(-30.0, 2.0, 4.0, speed=0.5)), [])

    def test_a_turn_under_way_at_the_first_sample(self):
        events = _turns(_turning_ego(-30.0, 0.0, 2.0))
        self.assertEqual(events[0], ("TURN_LEFT_START", 0.0, True))

    def test_a_spin_is_never_reported_before_it_starts(self):
        events = _turns(_turning_ego(-300.0, 3.0, 3.5))
        self.assertEqual(events[0][0], "TURN_LEFT_START")
        self.assertGreaterEqual(events[0][1], 3.0)


def _graph(spec):
    events = [SemanticEvent(type=name, kind="PERCEPTION", actor_id="A", t_local=t, subject_id=subject)
              for name, t, subject in spec]
    numbered = number_events("A", events)
    return build_local_graph("A", [TraceFrame(t_local=e.t_local, events=[e]) for e in numbered], [], {"end_t_local": 9.0})


class TemporalRelationTests(unittest.TestCase):
    def relation(self, spec):
        return next(item for item in temporal_safety_relations(_graph(spec)) if item["track"] == "track_001")

    def test_cut_in_before_critical_ttc_before_collision(self):
        item = self.relation([("TRACK_APPEARED_LEFT", 0.0, "track_001"), ("CUT_IN_FROM_LEFT_START", 3.9, "track_001"),
                              ("CRITICAL_TTC_START", 4.2, "track_001"), ("EGO_PATH_ENTRY", 4.8, "track_001"),
                              ("COLLISION", 5.25, None)])
        self.assertEqual(item["cut_in_vs_critical_ttc"], "CUT_IN_BEFORE_CRITICAL_TTC")
        self.assertEqual(item["chain"], "CUT_IN_FROM_LEFT_START < CRITICAL_TTC_START < COLLISION")
        self.assertEqual(item["deltas_s"]["critical_ttc_start_minus_cut_in"], 0.3)
        self.assertEqual(item["deltas_s"]["collision_minus_critical_ttc_start"], 1.05)
        self.assertEqual(item["ego_path_entry_vs_critical_ttc"], "AFTER")

    def test_critical_ttc_already_active_before_the_cut_in(self):
        for critical_start in (3.65, 3.9):  # earlier, and at the same time (CRITICAL_TTC_START <= CUT_IN)
            item = self.relation([("CRITICAL_TTC_START", critical_start, "track_001"),
                                  ("CUT_IN_FROM_RIGHT_START", 3.9, "track_001"), ("COLLISION", 5.0, None)])
            self.assertEqual(item["cut_in_vs_critical_ttc"], "CRITICAL_TTC_ALREADY_ACTIVE")
            self.assertIsNone(item["chain"])
            self.assertEqual(item["deltas_s"]["cut_in_minus_critical_ttc_start"], round(3.9 - critical_start, 3))

    def test_an_episode_that_ended_before_the_cut_in_does_not_count(self):
        item = self.relation([("CRITICAL_TTC_START", 2.0, "track_001"), ("CRITICAL_TTC_END", 2.5, "track_001"),
                              ("CUT_IN_FROM_LEFT_START", 3.0, "track_001"), ("CRITICAL_TTC_START", 3.5, "track_001")])
        self.assertEqual(item["cut_in_vs_critical_ttc"], "CUT_IN_BEFORE_CRITICAL_TTC")
        self.assertEqual(item["critical_ttc_start"], 3.5)

    def test_cut_in_without_critical_ttc(self):
        item = self.relation([("CUT_IN_FROM_LEFT_START", 3.0, "track_001"), ("EGO_PATH_ENTRY", 4.0, "track_001")])
        self.assertEqual(item["cut_in_vs_critical_ttc"], "NO_CRITICAL_TTC_AFTER_CUT_IN")
        self.assertIsNone(item["ego_path_entry_vs_critical_ttc"])


class IdentityAssociationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.result = reconstruct_run(make_run(Path(cls._tmp.name)), ReconstructionConfig())
        cls.fusion = FusionConfig()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _associate(self, edit):
        locals_ = [dataclasses.replace(local, tracks=list(local.tracks)) for local in self.result.locals]
        a = next(local for local in locals_ if local.owner == "A")
        edit(a)
        return {(item.local_graph, item.local_track): item for item in associate_tracks(locals_, self.result.alignment,
                                                                                        self.fusion)}

    def test_range_at_the_contact_is_evidence_not_a_veto(self):
        def farther(a):
            track = a.tracks[0]
            a.tracks[0] = LocalTrack(track.track_id, [dataclasses.replace(s, range_m=s.range_m + 4.0,
                                                                          clearance_m=s.clearance_m + 4.0)
                                                      for s in track.samples])
        far = self._associate(farther)[("A", "track_001")]
        near = self._associate(lambda a: None)[("A", "track_001")]
        self.assertEqual((far.status, far.global_entity), ("ASSOCIATED", "B"))
        self.assertLess(far.confidence, near.confidence)
        self.assertTrue(any("beyond 3.50 m" in line for line in far.evidence))

    def test_two_compatible_tracks_stay_anonymous(self):
        def twin(a):
            a.tracks.append(LocalTrack("track_002", list(a.tracks[0].samples)))
        decisions = self._associate(twin)
        for track in ("track_001", "track_002"):
            item = decisions[("A", track)]
            self.assertEqual(item.status, "ANONYMOUS")
            self.assertTrue(any(reason.startswith("ambiguous: 2 persistent tracks") for reason in item.blocking))


class IdentityRegressionTests(unittest.TestCase):
    """S03 and S05 (real recordings): the persistent partner tracks are associated, any
    short or spurious one is not.  In memory only: nothing is written to traces/."""

    def decisions(self, run_name):
        run = ROOT / "traces" / run_name
        if not (run / "vehicles").exists():
            self.skipTest("canonical trace not present")
        cfg = ReconstructionConfig()
        context = read_incident_context(run)
        locals_ = [reconstruct_vehicle(path, cfg, context=context) for path in sorted((run / "vehicles").iterdir())]
        alignment = align_graphs([local.graph for local in locals_], cfg.fusion)
        return {(item.local_graph, item.local_track): item for item in associate_tracks(locals_, alignment, cfg.fusion)}

    def test_s03_both_crossing_partners_are_associated(self):
        decisions = self.decisions("S03/run_0_crash")
        self.assertEqual(decisions[("A", "track_001")].global_entity, "B")
        self.assertEqual(decisions[("B", "track_001")].global_entity, "A")

    def test_s05_partners_associated_and_any_other_track_anonymous(self):
        # B spins after the impact.  With the radar's own motion taken as its displacement (as CARLA
        # measures it) the scenery no longer looks like moving targets, so no post-impact clutter
        # tracks remain; any other track would have to stay anonymous.
        decisions = self.decisions("S05/run_0_crash")
        self.assertEqual(decisions[("A", "track_001")].global_entity, "B")
        self.assertEqual(decisions[("B", "track_001")].global_entity, "A")
        others = [item for key, item in decisions.items() if key not in (("A", "track_001"), ("B", "track_001"))]
        self.assertTrue(all(item.status == "ANONYMOUS" for item in others))
        self.assertLessEqual(len(others), 2)


if __name__ == "__main__":
    unittest.main()
