"""The end of CRITICAL_TTC (reconstruction/conflict.py point 5, local.critical_intervals).

A CRITICAL_TTC state ends only after 0.2 s of clearly resolved samples: no collision course
(or one braking avoids below 0.75 x 6 m/s^2), no near contact with the safety envelope unless
both vehicles stand still, and a leader of the episode clearly gone (recorder below 1 m/s,
clearance beyond 1.10 x d_min, no part of it ahead, or its body more than the path hysteresis
outside the corridor and not moving back toward it), seen without occlusion.  Uncertain,
occluded and near-contact samples are no evidence of safety.

Geometry in the recorder's vehicle frame (x forward, y right), a model3-sized recorder (front face
2.4 m ahead of its origin, 2.16 m wide); the target is given by its observed near surface.  The
lettered cases follow the 2026-10-10 specification; F-H use the recorded campaign (traces/).
"""

import math
import unittest
from pathlib import Path

from src.cdf.reconstruction.checks import temporal_safety_relations
from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.conflict import assess_conflict
from src.cdf.reconstruction.local import reconstruct_vehicle, track_events, vehicle_metadata
from src.cdf.reconstruction.pipeline import read_incident_context
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, EgoTrajectory, LocalTrack, TrackSample

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
ROOT = Path(__file__).resolve().parents[1]
RELEASE = CFG.critical_release_ratio * CFG.critical_deceleration_mps2
STEP = 0.05


def _times(end, start=0.0):
    return [round(start + STEP * k, 2) for k in range(int(round((end - start) / STEP)) + 1)]


def _ego(speed, end=10.0):
    """The recorder driving straight ahead; ``speed`` is a number or a function of time."""
    profile = speed if callable(speed) else (lambda t: speed)
    states, x = [], 0.0
    for t in _times(end):
        states.append(EgoState(t_local=t, x=x, y=0.0, heading=0.0, vx=profile(t), vy=0.0))
        x += profile(t) * STEP
    return EgoTrajectory(states)


def _track(motion, end=8.0, occluded=lambda t: False):
    """A track from motion(t) -> (longitudinal, lateral, vx, vy, closing): near surface, ground velocity."""
    samples = []
    for t in _times(end):
        x, y, vx, vy, closing = motion(t)
        sample = TrackSample(t_local=t, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                             pos_std_m=0.1, vel_std_mps=0.1, range_m=math.hypot(x, y),
                             bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                             closing_speed_mps=closing, closing_ttc_s=None, measured=True, n_returns=4,
                             clearance_m=float(CAR.distance(x, y)), ahead_m=x - CAR.x_max)
        sample.occluded = occluded(t)
        samples.append(sample)
    return LocalTrack("track_001", samples)


def _events(track, ego, recording_end=10.0):
    return [(e.type, e.t_local) for e in track_events("A", track, recording_end, CFG, ego, footprint=CAR)]


def _assessments(track, ego):
    first = track.samples[0].t_local
    return {round(s.t_local, 2): assess_conflict(s, ego.at(s.t_local), CAR, CFG, s.t_local - first)
            for s in track.samples}


def _of(events, name):
    return [t for event, t in events if event == name]


def _drift(rate, until_lateral, start_lateral=0.5, t0=1.0):
    """A leader 3 m ahead of the front face at the recorder's 12 m/s, moving to the right from t0."""
    def motion(t):
        lateral = min(start_lateral + rate * max(t - t0, 0.0), until_lateral)
        moving = t >= t0 and lateral < until_lateral
        return 2.4 + 3.0, lateral, 12.0, (rate if moving else 0.0), 0.0
    return motion


class LeaderExitTests(unittest.TestCase):
    def test_a_minimal_exit_from_the_leader_gate_while_very_close_ends_nothing(self):  # A
        # An unsafe leader 3 m ahead drifts right until its nominal body is 0.36 m outside the corridor,
        # then keeps that lane position: the start gate fails (region None) but it stays a close
        # neighbour ahead, within the path hysteresis: the state is held.
        ego, track = _ego(12.0), _track(_drift(0.5, 2.0))
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        self.assertEqual(_of(events, "CRITICAL_TTC_START"), [0.5])
        outside = [t for t, a in sorted(assessments.items()) if a.forward.lateral_body_gap_m > 0.0]
        self.assertTrue(outside and not any(assessments[t].forward.leader for t in outside))  # the gate failed
        self.assertTrue(all(assessments[t].forward.lateral_body_gap_m <= CFG.path_hysteresis_m for t in outside))
        self.assertEqual(_of(events, "CRITICAL_TTC_END"), [])

    def test_a_one_sample_exit_from_the_front_lateral_gate_ends_nothing(self):  # A
        # A front-lateral leader entering the path; at 1.0 s one sample shows no lateral approach.
        def motion(t):
            lateral = max(2.6 - 0.5 * t, 1.0)
            return 6.0, lateral, 12.0, (0.0 if abs(t - 1.0) < 1e-6 or lateral <= 1.0 else -0.5), 0.0
        ego, track = _ego(12.0), _track(motion, end=4.0)
        events = _events(track, ego, recording_end=4.0)
        assessments = _assessments(track, ego)
        self.assertEqual([assessments[t].forward.region for t in (0.95, 1.0, 1.05)],
                         ["FRONT_LATERAL", None, "FRONT_LATERAL"])
        self.assertEqual(_of(events, "CRITICAL_TTC_START"), [0.5])
        self.assertEqual(_of(events, "CRITICAL_TTC_END"), [])

    def test_a_leader_moving_clearly_aside_ends_after_the_hysteresis_and_debounce(self):  # B
        ego, track = _ego(12.0), _track(_drift(1.0, 4.5))
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        ends = _of(events, "CRITICAL_TTC_END")
        self.assertEqual(len(ends), 1)
        end = assessments[ends[0]]
        self.assertGreater(end.forward.lateral_body_gap_m, CFG.path_hysteresis_m)
        self.assertLessEqual(end.forward.lateral_approach_mps, 0.1)  # moving away (vel_std 0.1)
        gate_failed = min(t for t, a in assessments.items() if t >= 0.5 and not a.forward.leader)
        self.assertGreater(ends[0], gate_failed)  # not when the start gate first failed
        beyond = min(t for t, a in assessments.items() if a.forward.lateral_body_gap_m > CFG.path_hysteresis_m)
        self.assertEqual(ends[0], beyond)  # the first clearly resolved sample, confirmed after 0.2 s


class OcclusionTests(unittest.TestCase):
    def test_a_temporary_occlusion_does_not_end_the_state(self):  # C
        def motion(t):
            return 2.4 + 5.0, 0.0, 12.0, 0.0, 0.0
        ego = _ego(12.0)
        track = _track(motion, occluded=lambda t: 2.0 <= t < 2.6)
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        self.assertFalse(any(a.critical for t, a in assessments.items() if 2.0 <= t < 2.6))  # no evidence...
        self.assertFalse(any(a.forward_released() for t, a in assessments.items() if 2.0 <= t < 2.6))  # ...either way
        self.assertEqual(_of(events, "CRITICAL_TTC_START"), [0.5])
        self.assertEqual(_of(events, "CRITICAL_TTC_END"), [])


def _alongside(ego_speed, closing, lateral=lambda t: 1.28, vy=lambda t: 0.0):
    """A car alongside the recorder's front half, its near side 0.2 m from the recorder's right side
    (inside the 0.3 m lateral margin of the safety envelope)."""
    def motion(t):
        return 1.0, lateral(t), ego_speed(t), vy(t), closing(t)
    return motion


class NearContactTests(unittest.TestCase):
    @staticmethod
    def scenario():
        # Closing in at 2 m/s (critical: inside the envelope and closing), then only 0.5 m/s while
        # still inside it (both at 10 m/s), then moving away from 4 s at 1 m/s.
        ego = _ego(10.0)
        track = _track(_alongside(lambda t: 10.0, lambda t: 2.0 if t < 2.0 else (0.5 if t < 4.0 else -1.0),
                                  lateral=lambda t: 1.28 + max(t - 4.0, 0.0),
                                  vy=lambda t: 1.0 if t >= 4.0 else 0.0))
        return ego, track

    def test_near_contact_is_not_released_by_the_closing_speed_alone(self):  # D
        ego, track = self.scenario()
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        self.assertEqual(_of(events, "CRITICAL_TTC_START"), [0.5])
        held = [a for t, a in assessments.items() if 2.0 <= t < 4.0]
        self.assertTrue(all(a.inside_envelope and not a.collision_course and not a.critical for a in held))
        self.assertFalse([t for t in _of(events, "CRITICAL_TTC_END") if t < 4.0])

    def test_a_clear_separation_ends_the_state(self):  # E
        ego, track = self.scenario()
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        ends = _of(events, "CRITICAL_TTC_END")
        self.assertEqual(len(ends), 1)
        left = min(t for t, a in assessments.items() if t >= 4.0 and not a.inside_envelope)
        self.assertEqual(ends[0], left)
        self.assertFalse(assessments[ends[0]].collision_course)

    def test_near_contact_ends_once_both_vehicles_stand_still(self):  # E
        # Both brake to a stop side by side, still within the envelope (a crash's aftermath).
        def speed(t):
            return 10.0 if t < 2.0 else max(10.0 - 10.0 * (t - 2.0), 0.0)
        ego = _ego(speed)
        track = _track(_alongside(speed, lambda t: 2.0 if t < 2.0 else 0.5))
        events = _events(track, ego)
        assessments = _assessments(track, ego)
        ends = _of(events, "CRITICAL_TTC_END")
        self.assertEqual(len(ends), 1)
        self.assertTrue(assessments[ends[0]].inside_envelope and assessments[ends[0]].at_rest)
        self.assertEqual(ends[0], min(t for t, a in assessments.items() if a.at_rest))


class S17Tests(unittest.TestCase):
    """S17: A (cut in on by C) swerves into B.  Reconstructed live from the recorders' own files."""

    run_dir = ROOT / "traces" / "S17" / "run_0_crash"

    @classmethod
    def setUpClass(cls):
        if not (cls.run_dir / "vehicles" / "A").exists():
            raise unittest.SkipTest("canonical trace not present")
        config, context = ReconstructionConfig(), read_incident_context(cls.run_dir)
        cls.local = {owner: reconstruct_vehicle(cls.run_dir / "vehicles" / owner, config, context=context)
                     for owner in ("A", "B")}

    def nodes(self, owner, subject=None):
        return [(n.event_type, n.t_local) for n in self.local[owner].graph.nodes
                if subject is None or n.subject_id == subject]

    def assessment_at(self, owner, track_id, t_local):
        """(assessment, sample) of a track at one of its sample times."""
        local = self.local[owner]
        track = next(t for t in local.tracks if t.track_id == track_id)
        sample = next(s for s in track.samples if abs(s.t_local - t_local) < 1e-6)
        footprint = EgoFootprint.from_metadata(vehicle_metadata(self.run_dir / "vehicles" / owner).get("ego_footprint"))
        return assess_conflict(sample, local.ego.at(sample.t_local), footprint, CFG,
                               sample.t_local - track.samples[0].t_local), sample

    def collision(self, owner):
        return next(t for name, t in self.nodes(owner) if name == "COLLISION")

    def test_b_stays_critical_about_a_until_the_collision(self):  # F
        collision = self.collision("B")
        events = self.nodes("B", "track_001")
        starts, ends = _of(events, "CRITICAL_TTC_START"), _of(events, "CRITICAL_TTC_END")
        self.assertEqual(len(starts), 1)
        self.assertLess(starts[0], collision)
        self.assertTrue(all(end > collision for end in ends), (ends, collision))
        for end in ends:  # resolved by geometry: out of the envelope, or both standing still
            assessment, _ = self.assessment_at("B", "track_001", end)
            self.assertTrue(assessment.released(RELEASE, False))
            self.assertTrue(assessment.at_rest or not assessment.inside_envelope)

    def test_a_ends_the_episode_about_c_only_once_c_is_clearly_aside(self):  # G
        collision = self.collision("A")
        events = self.nodes("A", "track_001")
        self.assertEqual(len(_of(events, "CRITICAL_TTC_START")), 1)
        ends = _of(events, "CRITICAL_TTC_END")
        self.assertTrue(all(end > collision for end in ends), (ends, collision))
        for end in ends:  # C's body beyond the path hysteresis and moving away, no near contact
            assessment, sample = self.assessment_at("A", "track_001", end)
            self.assertTrue(assessment.released(RELEASE, True))
            self.assertGreater(assessment.forward.lateral_body_gap_m, CFG.path_hysteresis_m)
            self.assertLessEqual(assessment.forward.lateral_approach_mps, sample.vel_std_mps)
            self.assertFalse(assessment.inside_envelope)


class S02RegressionTests(unittest.TestCase):
    def test_s02_critical_before_cut_in_is_still_critical_at_the_cut_in(self):  # H
        run = ROOT / "traces" / "S02" / "run_0_critical_before_cut_in"
        if not (run / "vehicles" / "A").exists():
            self.skipTest("canonical trace not present")
        local = reconstruct_vehicle(run / "vehicles" / "A", ReconstructionConfig(), context=read_incident_context(run))
        relation = next(item for item in temporal_safety_relations(local.graph) if item["track"] == "track_001")
        self.assertEqual(relation["cut_in"]["type"], "CUT_IN_FROM_LEFT_START")
        self.assertEqual(relation["cut_in_vs_critical_ttc"], "CRITICAL_TTC_ALREADY_ACTIVE")
        self.assertLess(relation["critical_ttc_start"], relation["cut_in"]["t_local"])


if __name__ == "__main__":
    unittest.main()
