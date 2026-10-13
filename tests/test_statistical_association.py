"""Uncertainty-normalised association of the local radar tracker (METHOD 3 FINAL; TrackingConfig.gating
"covariance"): range-dependent radar covariance, Mahalanobis position gate, Doppler residual along the line of
sight, ambiguity instead of an arbitrary choice, covariance growth without data, post-contact CRITICAL_TTC."""

import dataclasses
import math
import unittest

import numpy as np

from src.cdf.reconstruction.config import SemanticsConfig, TrackingConfig
from src.cdf.reconstruction.local import contact_holds, critical_intervals
from src.cdf.reconstruction.tracking import (TrackMeasurement, _ActiveTrack, _measurement_model,
                                             _statistical_assignment, associate_returns, chi2_quantile,
                                             covariance_gate, kf_predict_speed, polar_covariances)
import test_uncertainty_hardening as base
from test_uncertainty_hardening import grid, sweeps_of

G2 = chi2_quantile(0.99, 2)


def statistical(**overrides):
    return dataclasses.replace(TrackingConfig(), gating="covariance", **overrides)


def sweep_at(points, radial, origin=(0.0, 0.0)):
    from src.cdf.reconstruction.tracking import RadarSweep
    points = np.asarray(points, float)
    ranges = np.hypot(*(points - np.asarray(origin)).T)
    return RadarSweep(t_local=0.0, points=points, origins=np.tile(origin, (len(points), 1)),
                      radar=np.zeros(len(points), dtype=int), radial_speed=np.asarray(radial, float),
                      clearance=ranges, depth=ranges)


def tracked(start, speed, until, c, n_returns=8):
    """The confirmed track of a car driving away along x from ``start`` (returns spread 1.6 m across its rear)."""
    sweeps = []
    for t in grid(0.0, until):
        x = start + speed * t
        points = np.column_stack([np.full(n_returns, x), np.linspace(-0.8, 0.8, n_returns)])
        sweeps.append(sweep_at(points, speed * points[:, 0] / np.hypot(*points.T)))
        sweeps[-1].t_local = round(t, 4)
    tracks = associate_returns(sweeps, c)
    assert len(tracks) == 1, len(tracks)
    return tracks[0]


class RadarCovarianceTests(unittest.TestCase):
    def test_near_covariance_is_small_and_far_is_larger(self):
        c = statistical()
        near, far = (polar_covariances(np.array([[r, 0.0]]), np.zeros((1, 2)), c)[0] for r in (5.0, 80.0))
        self.assertLess(np.linalg.eigvalsh(near)[-1], np.linalg.eigvalsh(far)[-1])
        self.assertLess(math.sqrt(np.linalg.eigvalsh(near)[-1]), 0.3)  # decimetres close by

    def test_angular_error_grows_laterally_with_range(self):
        c = statistical()
        for r in (10.0, 40.0, 80.0):
            cov = polar_covariances(np.array([[r, 0.0]]), np.zeros((1, 2)), c)[0]
            self.assertAlmostEqual(math.sqrt(cov[1, 1]), r * math.radians(c.radar_azimuth_std_deg), places=6)
            self.assertAlmostEqual(math.sqrt(cov[0, 0]), c.radar_range_std_m, places=6)  # along: range sigma

    def test_the_same_physical_residual_fails_near_and_passes_far(self):
        # One return 3.0 m beside a car driving away (across its heading): impossible close by (decimetre
        # radar noise, a 1.9 m wide body), within the angular uncertainty at 80 m.
        c = statistical()
        for start, expected in ((4.0, False), (78.0, True)):
            track = tracked(start, 2.0, 1.0, c)
            point = track.x[:2] + np.array([0.0, 3.0])
            radial = float(point @ track.x[2:] / np.linalg.norm(point))
            d2, radial2, _ = covariance_gate(track, sweep_at([point], [radial]), c)
            self.assertEqual(bool(d2[0] <= G2), expected, (start, d2[0]))


class DopplerTests(unittest.TestCase):
    def make(self, velocity, P_v):
        c = statistical()
        first = TrackMeasurement(t_local=0.0, xy=np.array([20.0, 0.0]), dopplers=[], n_returns=3,
                                 points=np.array([[20.0, -0.5], [20.0, 0.0], [20.0, 0.5]]), origins=np.zeros((3, 2)))
        track = _ActiveTrack(1, first, c)
        track.x = np.array([20.0, 0.0, velocity[0], velocity[1]])
        track.P = np.diag([0.1, 0.1, P_v[0], P_v[1]])
        return track, c

    def test_doppler_residual_is_along_the_line_of_sight(self):
        # A crossing car (10 m/s across the line of sight) returns radial speed 0: consistent.
        track, c = self.make((0.0, 10.0), (0.1, 0.1))
        _, radial2, _ = covariance_gate(track, sweep_at([[20.0, 0.0]], [0.0]), c)
        self.assertLess(radial2[0], 1e-6)
        # The same car measured at 3 m/s along the line of sight is not.
        _, radial2, _ = covariance_gate(track, sweep_at([[20.0, 0.0]], [3.0]), c)
        self.assertGreater(radial2[0], chi2_quantile(0.99, 1))

    def test_tangential_uncertainty_creates_no_contradiction(self):
        # A huge tangential velocity uncertainty (badly reconstructed crossing speed) leaves the radial test as is.
        tight, c = self.make((0.0, 10.0), (0.1, 0.1))
        loose, _ = self.make((0.0, 10.0), (0.1, 25.0))
        sweep = sweep_at([[20.0, 0.0]], [0.4])
        self.assertAlmostEqual(covariance_gate(tight, sweep, c)[1][0], covariance_gate(loose, sweep, c)[1][0])

    def test_the_recorders_own_impact_widens_the_doppler_gate(self):
        track, c = self.make((5.0, 0.0), (0.1, 0.1))
        sweep = sweep_at([[20.0, 0.0]], [7.0])
        calm = covariance_gate(track, sweep, c)[1][0]
        impact = covariance_gate(track, sweep, c, ego_variance=(3000.0 / 1500.0) ** 2)[1][0]
        self.assertGreater(calm, chi2_quantile(0.99, 1))
        self.assertLess(impact, chi2_quantile(0.99, 1))


class AmbiguityTests(unittest.TestCase):
    def two_tracks(self, c, gap, P):
        tracks = []
        for k, y in enumerate((-gap / 2.0, gap / 2.0)):
            first = TrackMeasurement(t_local=0.0, xy=np.array([40.0, y]), dopplers=[], n_returns=3,
                                     points=np.array([[40.0, y - 0.3], [40.0, y], [40.0, y + 0.3]]),
                                     origins=np.zeros((3, 2)))
            track = _ActiveTrack(k + 1, first, c)
            track.track_id = "track_{0:03d}".format(k + 1)
            track.x = np.array([40.0, y, 10.0, 0.0])
            track.P = np.diag([P, P, 0.1, 0.1])
            tracks.append(track)
        return tracks

    def test_high_uncertainty_alone_does_not_force_an_association(self):
        c = statistical()
        sweep = sweep_at([[40.0, 0.0]], [10.0])
        # Two tracks 3.5 m apart, both uncertain: the return between them gates with both, equally likely.
        masks, winners, ambiguous = _statistical_assignment(self.two_tracks(c, 3.5, 4.0), sweep,
                                                            np.ones(1, dtype=bool), c, 0.0, None)
        self.assertTrue(ambiguous[0])
        self.assertFalse(any(m[0] for m in masks))

    def test_a_clear_winner_is_assigned(self):
        c = statistical()
        sweep = sweep_at([[40.0, -1.75]], [10.0])
        masks, winners, ambiguous = _statistical_assignment(self.two_tracks(c, 3.5, 0.05), sweep,
                                                            np.ones(1, dtype=bool), c, 0.0, None)
        self.assertFalse(ambiguous[0])
        self.assertEqual(winners[0], 0)


class PredictionGrowthTests(unittest.TestCase):
    def test_covariance_grows_while_measurements_are_missing(self):
        c = statistical()
        x, P = np.array([20.0, 0.0, 10.0, 0.0]), np.diag([0.05, 0.05, 0.1, 0.1])
        sizes = []
        for _ in range(20):
            x, P = kf_predict_speed(x, P, 0.05, c.acceleration_std_mps2, c.yaw_rate_std_rps)
            sizes.append(np.trace(P[:2, :2]))
        self.assertTrue(all(b > a for a, b in zip(sizes, sizes[1:])))

    def test_a_fast_target_spreads_faster_sideways(self):
        c = statistical()
        P0 = np.diag([0.05, 0.05, 0.1, 0.1])

        def across(speed):
            x, P = np.array([20.0, 0.0, speed, 0.0]), P0.copy()
            for _ in range(10):
                x, P = kf_predict_speed(x, P, 0.05, c.acceleration_std_mps2, c.yaw_rate_std_rps)
            return P[1, 1], P[0, 0]
        slow, fast = across(2.0), across(30.0)
        self.assertGreater(fast[0], slow[0])          # across the track
        self.assertAlmostEqual(fast[1], slow[1])      # along it: the same acceleration noise

    def test_a_long_gap_ends_the_track_before_the_fail_safe(self):
        c = statistical()
        tracks = associate_returns(sweeps_of(grid(0.0, 1.0) + grid(1.9, 2.5)), c)
        self.assertEqual(len(tracks), 2)  # 0.9 s without data: no longer useful, gap cap 2 s not reached


class PostContactCriticalTests(unittest.TestCase):
    class _Assessment:
        def __init__(self, critical, released=None):
            self.critical, self.critical_reason = critical, None
            self._released = (not critical) if released is None else released

        def released(self, *_):
            return self._released

    def test_a_touching_non_partner_starts_no_episode_after_the_contact(self):
        times = [round(0.05 * k, 2) for k in range(40)]
        # Critical from 0.5 s after the contact at 1.0 s (the same body re-acquired as a new track).
        # In contact from 1.0 s: never clearly released (near contact is not a release).
        assessments = [self._Assessment(t >= 1.5, released=t < 1.0) for t in times]
        free, _ = critical_intervals(times, assessments, 4.5, 0.2)
        held, _ = critical_intervals(times, assessments, 4.5, 0.2, holds=[(1.0, 1.0)])
        self.assertEqual(len(free), 1)
        self.assertEqual(held, [])

    def test_a_hold_does_not_end_a_running_episode(self):
        times = [round(0.05 * k, 2) for k in range(40)]
        assessments = [self._Assessment(0.5 <= t <= 1.6) for t in times]
        spans, collided = critical_intervals(times, assessments, 4.5, 0.2, holds=[(1.0, 1.0)])
        self.assertEqual(collided, [])
        self.assertEqual(len(spans), 1)
        self.assertGreater(times[spans[0][1]], 1.6)

    def test_a_pair_still_touching_is_never_released_after_its_contact(self):
        times = [round(0.05 * k, 2) for k in range(40)]
        # Critical before the contact at 1.0 s; after it the pair stops closing (released by speed) but stays
        # 0.3 m apart; a new critical sample at 1.7 s must not start a second episode of the same pair.
        assessments = [self._Assessment(t < 1.0 or abs(t - 1.7) < 1e-6, released=not (t < 1.0 or abs(t - 1.7) < 1e-6))
                       for t in times]
        touching = [t >= 1.0 for t in times]
        free, _ = critical_intervals(times, assessments, 4.5, 0.2, contacts=[(1.0, 1.0)])
        held, _ = critical_intervals(times, assessments, 4.5, 0.2, contacts=[(1.0, 1.0)], touching=touching)
        self.assertEqual(len(free), 2)
        self.assertEqual(len(held), 1)

    def test_holds_go_to_touching_tracks_that_are_not_the_partner(self):
        from types import SimpleNamespace
        contact = SimpleNamespace(first=1.0, last=1.1)
        sample = lambda t, c: SimpleNamespace(t_local=t, clearance_m=c)
        partner = SimpleNamespace(track_id="t1", samples=[sample(0.95, 0.2), sample(1.0, 0.0)])
        second = SimpleNamespace(track_id="t2", samples=[sample(0.95, 0.4), sample(1.05, 0.1)])
        far = SimpleNamespace(track_id="t3", samples=[sample(1.0, 6.0)])
        holds = contact_holds([contact], [partner, second, far], 0.05, 1.0, {"t1": [(1.0, 1.1)]})
        self.assertEqual(holds, {"t2": [(1.0, 1.1)]})


class StatisticalRecordedRunTests(unittest.TestCase):
    """Known cases with the uncertainty-normalised tracker."""

    setUpClass = classmethod(base.RecordedRunTests.setUpClass.__func__)
    tearDownClass = classmethod(base.RecordedRunTests.tearDownClass.__func__)
    reconstruct = base.RecordedRunTests.reconstruct
    collisions = base.RecordedRunTests.collisions

    def test_s08_crossing_contact_matched_and_recorder_link_kept(self):
        _, result = self.reconstruct("traces/S08/run_0_rolls_through", "final")
        self.assertIn(("A", "B"), self.collisions(result))
        links = {(a.local_graph, a.global_entity) for a in result.associations}
        self.assertIn(("B", "A"), links)
        self.assertIn(("A", "B"), links)

    def test_s04_consumer_impulse_seeds_0_and_3_make_no_wrong_pairing(self):
        from src.cdf.evaluation.fusion_metrics import evaluate_fusion
        from src.cdf.evaluation.reconstruction import evaluate_run
        from src.cdf.evaluation.run_metrics import run_metrics
        for seed in (0, 3):
            target, _ = self.reconstruct("traces/S04/run_0_a_front_pushed", "final", "consumer_impulse10", seed)
            metrics = run_metrics(target, evaluate_run(target, clock_shift_check=False),
                                  evaluate_fusion(target, write=False))
            self.assertEqual(metrics["false_collision_matches"], 0, seed)

    def test_s19_no_same_pair_critical_episode_after_their_contact(self):
        _, result = self.reconstruct("traces/S19/run_0_collision_ambiguity", "final")
        contact = min(n.t_global for n in result.graph.nodes
                      if n.event_type == "COLLISION" and sorted(n.participants or []) == ["A", "B"])
        late = [n for n in result.graph.nodes if n.event_type == "CRITICAL_TTC_START" and n.t_global > contact
                and {n.actor_id, n.subject_id} == {"A", "B"}]
        self.assertEqual(late, [])

    def test_s13_platoon_no_same_pair_critical_episode_while_touching(self):
        _, result = self.reconstruct("traces/S13/run_0_platoon", "final")
        contact = min(n.t_global for n in result.graph.nodes if n.event_type == "COLLISION")
        late = [n for n in result.graph.nodes if n.event_type == "CRITICAL_TTC_START" and n.t_global > contact
                and {n.actor_id, n.subject_id} == {"A", "B"}]
        self.assertEqual(late, [])


if __name__ == "__main__":
    unittest.main()
