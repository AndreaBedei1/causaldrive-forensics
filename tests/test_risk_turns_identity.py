"""Recorder turns, temporal safety relations and identity association (the CRITICAL_TTC
model has its own tests in test_critical_ttc.py)."""

import dataclasses
import math
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.alignment import align_graphs
from src.cdf.reconstruction.checks import temporal_safety_relations
from src.cdf.reconstruction.config import FusionConfig, ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.fusion import associate_tracks
from src.cdf.reconstruction.local import build_local_graph, number_events, reconstruct_vehicle, turn_events
from src.cdf.reconstruction.models import SemanticEvent, TraceFrame
from src.cdf.reconstruction.pipeline import read_incident_context, reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory, LocalTrack

from synthetic_run import make_run

CFG = SemanticsConfig()
ROOT = Path(__file__).resolve().parents[1]


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
    """S03 (real recording): the persistent partner tracks are associated.  In memory only:
    nothing is written to traces/."""

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


if __name__ == "__main__":
    unittest.main()
