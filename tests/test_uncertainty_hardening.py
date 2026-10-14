"""Uncertainty-driven tracking, observable-direction collision evidence, stitch posterior, operative relevance
and target timelines."""

import dataclasses
import json
import math
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from src.cdf.reconstruction import identity
from src.cdf.reconstruction.config import TrackingConfig, load_config
from src.cdf.reconstruction.tracking import RadarSweep, _impact_kicks, associate_returns, chi2_quantile
from test_retrospective import cfg, straight, track

ROOT = Path(__file__).resolve().parents[1]


def covariance_tracking(**overrides):
    return dataclasses.replace(TrackingConfig(), **overrides)


def sweeps_of(times, start=20.0, speed=10.0, lateral=0.0):
    """One radar at the origin, one car driving away along x: three returns on its rear face per sweep."""
    out = []
    seen = {round(t, 4) for t in times}
    for t in grid(0.0, max(times)):
        if round(t, 4) not in seen:
            # The radars keep sweeping while the car is not returned (occlusion): an empty sweep.
            empty = np.zeros((0, 2))
            out.append(RadarSweep(t_local=round(t, 4), points=empty, origins=empty, radar=np.zeros(0, dtype=int),
                                  radial_speed=np.zeros(0), clearance=np.zeros(0), depth=np.zeros(0)))
            continue
        x = start + speed * t
        points = np.array([[x, lateral - 0.6], [x, lateral], [x, lateral + 0.6]])
        ranges = np.hypot(points[:, 0], points[:, 1])
        out.append(RadarSweep(t_local=round(t, 4), points=points, origins=np.zeros((3, 2)), radar=np.zeros(3, dtype=int),
                              radial_speed=speed * points[:, 0] / ranges, clearance=ranges, depth=ranges))
    return out


def grid(t0, t1, dt=0.05):
    return [t0 + k * dt for k in range(int(round((t1 - t0) / dt)) + 1)]


class TrackerUncertaintyTests(unittest.TestCase):
    def test_gate_quantiles_are_chi_square(self):
        self.assertAlmostEqual(chi2_quantile(0.99, 2), 9.2103, places=3)
        self.assertAlmostEqual(chi2_quantile(0.99, 1), 6.6349, places=3)

    def test_confirmation_needs_support_duration_and_updates(self):
        c = covariance_tracking()
        # 0.15 s of support (4 updates) is not enough; 0.2 s is.
        self.assertEqual(associate_returns(sweeps_of(grid(0.0, 0.15)), c), [])
        self.assertEqual(len(associate_returns(sweeps_of(grid(0.0, 0.2)), c)), 1)

    def test_a_short_gap_survives_and_a_long_one_ends_the_track(self):
        c = covariance_tracking()
        short = associate_returns(sweeps_of(grid(0.0, 1.0) + grid(1.15, 2.0)), c)
        self.assertEqual(len(short), 1)
        long = associate_returns(sweeps_of(grid(0.0, 1.0) + grid(3.2, 4.0)), c)
        self.assertEqual(len(long), 2)

    def test_survival_follows_the_prediction_uncertainty_not_a_fixed_gap(self):
        times = grid(0.0, 1.0) + grid(1.6, 2.5)
        steady = associate_returns(sweeps_of(times), covariance_tracking(acceleration_std_mps2=0.5))
        agile = associate_returns(sweeps_of(times), covariance_tracking(acceleration_std_mps2=8.0))
        # The same 0.55 s gap: a target with a tight motion model is still predicted within a car width, one
        # with a loose model is not (and a fixed 0.5 s gap would have ended both).
        self.assertEqual(len(steady), 1)
        self.assertEqual(len(agile), 2)

    def test_the_fail_safe_cap_bounds_survival(self):
        c = covariance_tracking(acceleration_std_mps2=0.01, gap_cap_s=0.3)
        self.assertEqual(len(associate_returns(sweeps_of(grid(0.0, 1.0) + grid(1.5, 2.5)), c)), 2)

    def test_impact_widens_the_velocity_variance_by_the_measured_impulse(self):
        c = covariance_tracking()
        sweeps = sweeps_of(grid(0.0, 1.0))
        kicks = _impact_kicks(sweeps, [(0.52, 3000.0), (0.53, 1500.0)], c)
        # Both impulses fall in the interval before the 0.55 s sweep: (sum J / m)^2.
        self.assertEqual(list(kicks), [11])
        self.assertAlmostEqual(kicks[11], (4500.0 / c.nominal_vehicle_mass_kg) ** 2)
        self.assertEqual(_impact_kicks(sweeps, None, c), {})


# --------------------------------------------------------------------------
# Collision evidence in the direction the radar observes
# --------------------------------------------------------------------------

class _Ego:
    def __init__(self, speed=0.0, start=0.0, end=10.0):
        self.start, self.end, self._speed = start, end, speed

    def at(self, t):
        return SimpleNamespace(heading=0.0, vx=self._speed, vy=0.0, speed=self._speed)


def contact_window(rel_v, at=(0.0, 1.5), n=6, vel_std=0.3):
    """Samples of a target touching the recorder's right side, moving with relative velocity rel_v."""
    return [SimpleNamespace(t_local=5.0 - 0.05 * (n - 1 - k), relative_vx_mps=rel_v[0], relative_vy_mps=rel_v[1],
                            longitudinal_m=at[0], lateral_m=at[1], vel_std_mps=vel_std) for k in range(n)]


class NormalComponentTests(unittest.TestCase):
    def setUp(self):
        self.c = load_config()

    def check(self, rel_v, partner_speed, recorder_speed=0.0):
        local = SimpleNamespace(footprint=None, ego=_Ego(recorder_speed))
        other = SimpleNamespace(ego=_Ego(partner_speed))
        window = contact_window(rel_v)
        return identity._normal_component_consistent(local, other, window, 5.0, 5.0, self.c)

    def test_a_slow_true_partner_with_a_poorly_observed_tangential_component_is_not_contradicted(self):
        # S08-like: the track's ground velocity is mostly tangential (8 m/s, badly observed), only 2 m/s along
        # the line of sight; the true partner rolls at 3 m/s.  A full-velocity comparison would reject it.
        self.assertTrue(self.check((8.0, -2.0), 3.0))

    def test_a_partner_slower_than_the_observed_doppler_component_is_contradicted(self):
        self.assertFalse(self.check((0.0, -6.0), 1.0))

    def test_a_partner_faster_than_the_whole_ground_velocity_is_contradicted(self):
        # S04-like wrong clock offset: the candidate drives at 12 m/s while the arriving body moves at 4 m/s.
        self.assertFalse(self.check((0.0, -4.0), 12.0))

    def test_a_consistent_partner_is_supported(self):
        self.assertTrue(self.check((0.0, -5.0), 5.0))


def stub_track(clearances, speed, dt=0.05, t_end=5.0):
    n = len(clearances)
    samples = [SimpleNamespace(t_local=round(t_end - dt * (n - 1 - k), 4), measured=True, clearance_m=c, speed_mps=speed,
                               relative_vx_mps=0.0, relative_vy_mps=-speed, longitudinal_m=0.0, lateral_m=1.0 + c,
                               vel_std_mps=0.3) for k, c in enumerate(clearances)]
    return SimpleNamespace(identity_ambiguous=False, samples=samples)


class ClosingBodyTests(unittest.TestCase):
    def evidence(self, clearances):
        c = cfg()
        a = SimpleNamespace(owner="A", tracks=[stub_track(clearances, 4.0)], footprint=None, ego=_Ego(0.0))
        b = SimpleNamespace(owner="B", tracks=[], footprint=None, ego=_Ego(9.0))
        return identity.radar_contact_evidence([a, b], c)("A", 5.0, "B", 5.0)

    def test_a_body_passing_alongside_is_no_evidence(self):
        # S15-like: a car arrives beside the recorder and keeps its distance through the last 0.2 s (passing,
        # not hitting): it can neither support nor contradict the partner.
        passing = [3.0, 2.4, 1.8, 1.2, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6]
        self.assertIsNone(self.evidence(passing))

    def test_a_closing_body_still_counts(self):
        closing = [3.0, 2.6, 2.2, 1.8, 1.4, 1.2, 1.0, 0.8, 0.5, 0.2]
        # Still closing at the report: it counts, and a 9 m/s partner is faster than the 4 m/s body by > 3 sigma.
        self.assertFalse(self.evidence(closing))


# --------------------------------------------------------------------------
# Stitches as hypotheses, relevance envelope
# --------------------------------------------------------------------------

class StitchPosteriorTests(unittest.TestCase):
    def posterior(self, gap, miss=0.0):
        c = cfg()
        first = track("A", "t1", straight([0, 0], 20), 0.0, [-15, 0])
        start = 0.95 + gap
        second = track("A", "t2", straight([10.0 * start + miss, 0], 20), 0.0, [-15, 0], t0=start)
        r = identity.stitch_density(first, second, c) / c.fusion.retrospective_new_target_density
        return r / (1.0 + r)

    def test_the_posterior_decays_with_the_gap(self):
        self.assertGreater(self.posterior(0.2), self.posterior(1.0))
        self.assertGreater(self.posterior(1.0), self.posterior(3.0))

    def test_a_short_consistent_reacquisition_is_accepted_and_a_long_missed_one_is_not(self):
        c = cfg()
        self.assertGreaterEqual(self.posterior(0.2), c.fusion.retrospective_min_posterior)
        self.assertLess(self.posterior(1.5, miss=4.0), c.fusion.retrospective_min_posterior)

    def test_a_large_miss_is_not_absorbed_by_a_long_gap(self):
        # Larger uncertainty never makes the merge easier: a long gap does not turn a 4 m miss into a stitch.
        self.assertLess(self.posterior(1.5, miss=4.0), self.posterior(0.2))


class RelevanceTests(unittest.TestCase):
    def test_closing_speed_and_uncertainty_widen_the_envelope(self):
        c = load_config()
        base = identity.relevance_range(10.0, 0.0, 0.0, 0.0, c)
        self.assertGreater(identity.relevance_range(10.0, 8.0, 0.0, 0.0, c), base)
        self.assertGreater(identity.relevance_range(10.0, 0.0, 0.5, 0.5, c), base)
        # A target pulling away never needs more than the following distance and its uncertainty.
        self.assertAlmostEqual(identity.relevance_range(10.0, -8.0, 0.0, 0.0, c), base)


# --------------------------------------------------------------------------
# Recorded runs: S08, dense scenarios, timelines
# --------------------------------------------------------------------------

class RecordedRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="hardening_"))
        cls.cache = {}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def reconstruct(self, run, condition="exact", seed=0, **fusion):
        key = (run, condition, seed, tuple(sorted(fusion.items())))
        if key in self.cache:
            return self.cache[key]
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import robustness
        from retrospective_study import CONDITIONS
        from src.cdf.reconstruction.pipeline import reconstruct_run
        from src.cdf.robustness.perturb import perturbed_copy
        family, level, parameter = CONDITIONS[condition]
        perturbation, pose = robustness.build(dict(run=str(ROOT / run), family=family, level=level,
                                                   parameter=parameter, seed=seed))
        target = self.tmp / "_".join((condition, str(seed), str(len(self.cache)))) / run
        perturbed_copy(ROOT / run, target, perturbation, seed)
        result = reconstruct_run(target, cfg(**fusion), pose_factory=pose)
        self.cache[key] = (target, result)
        return target, result

    def collisions(self, result):
        nodes = [n for n in result.graph.nodes if n.event_type == "COLLISION"]
        return sorted(tuple(sorted(getattr(n, "participants", None) or [])) for n in nodes)

    def test_s08_collision_is_named(self):
        _, result = self.reconstruct("traces/S08/run_0_rolls_through")
        self.assertIn(("A", "B"), self.collisions(result))

    def test_dense_collisions_name_the_single_partner(self):
        for run in ("traces/S15/run_0_dense_platoon", "traces/S18/run_0_collision_ambiguity"):
            _, result = self.reconstruct(run)
            self.assertEqual(set(self.collisions(result)), {("A", "B")}, run)

    def test_s14_dense_abreast_has_no_false_merge(self):
        from src.cdf.evaluation.fusion_metrics import evaluate_fusion
        target, _ = self.reconstruct("traces/S14/run_0_surrounded")
        self.assertEqual(evaluate_fusion(target, write=False)["merges"]["false"], 0)

    def test_timelines_keep_observation_before_resolution(self):
        target, _ = self.reconstruct("traces/S15/run_0_dense_platoon")
        entities = json.loads((target / "reconstruction/global/anonymous_entities.json").read_text())["entities"]
        self.assertTrue(entities)
        for entity in entities:
            timeline = entity["timeline"]
            self.assertAlmostEqual(timeline["first_detected"], min(s["t_global"][0] for s in entity["source_track_segments"]),
                                   places=2)
            for key in ("first_tracked", "first_identity_resolved"):
                if timeline[key] is not None:
                    self.assertGreaterEqual(timeline[key], timeline["first_detected"] - 1e-6, (entity["id"], key))

    def test_retrospective_resolution_moves_no_event_timestamp(self):
        # The same tracker with the late identity resolution disabled (no posterior reaches 1.01): identity
        # decisions may differ, the event onsets may not.
        for run in ("traces/S12/run_0_crash", "traces/S15/run_0_dense_platoon"):
            _, final = self.reconstruct(run)
            _, plain = self.reconstruct(run, retrospective_min_posterior=1.01)
            onsets = lambda result: Counter((n.event_type, n.actor_id, round(n.t_global, 4)) for n in result.graph.nodes)
            self.assertEqual(onsets(final), onsets(plain), run)


if __name__ == "__main__":
    unittest.main()
