"""Recorder identity passed on through another observer's view (identity.inherited_links), and the velocity
test after an observer's own collision (anonymous.pair_evidence)."""

import dataclasses
import unittest

import numpy as np

from src.cdf.reconstruction import identity
from src.cdf.reconstruction.anonymous import ASSOCIATED, CommonView, pair_evidence
from test_retrospective import Poses, cfg, straight, track


def named(t, recorder):
    t.status, t.entity = ASSOCIATED, recorder
    return t


class InheritanceTests(unittest.TestCase):
    def setUp(self):
        self.c = cfg()
        self.rel = identity.RelativePose({"A": Poses(0.0), "B": Poses(0.0), "C": Poses(0.0)})

    def inherit(self, *tracks):
        return identity.inherited_links(CommonView(list(tracks), {}), [], self.c, self.rel)

    def test_the_same_body_seen_by_another_observer_inherits_the_recorder(self):
        a1 = named(track("A", "a1", straight([20, 0]), 0.0, [0, 0]), "C")
        b1 = track("B", "b1", straight([20, 0]), 0.0, [0, 8])
        links = self.inherit(a1, b1)
        self.assertEqual([(link.track, link.recorder, link.inherited_from) for link in links], [("B:b1", "C", "A:a1")])

    def test_the_car_in_the_next_lane_inherits_nothing(self):
        a1 = named(track("A", "a1", straight([20, 0]), 0.0, [0, 0]), "C")
        b1 = track("B", "b1", straight([20, 3.5]), 0.0, [0, 8])
        self.assertEqual(self.inherit(a1, b1), [])

    def test_a_different_velocity_inherits_nothing(self):
        a1 = named(track("A", "a1", straight([20, 0]), 0.0, [0, 0]), "C")
        b1 = track("B", "b1", straight([20, 0], speed=13.0), 0.0, [0, 8], speed=13.0)
        self.assertEqual(self.inherit(a1, b1), [])

    def test_the_same_body_as_two_recorders_stays_unresolved(self):
        a1 = named(track("A", "a1", straight([20, 0]), 0.0, [0, 0]), "C")
        c1 = named(track("C", "c1", straight([20, 0]), 0.0, [0, -8]), "D")
        b1 = track("B", "b1", straight([20, 0]), 0.0, [0, 8])
        self.assertEqual([link.track for link in self.inherit(a1, c1, b1)], [])

    def test_an_observer_never_inherits_from_its_own_tracks_or_its_own_name(self):
        a1 = named(track("A", "a1", straight([20, 0]), 0.0, [0, 0]), "C")
        a2 = track("A", "a2", straight([20, 0]), 0.0, [0, 0])
        b1 = named(track("B", "b1", straight([20, 0]), 0.0, [0, 8]), "A")
        a3 = track("A", "a3", straight([20, 0]), 0.0, [0, 0])
        self.assertEqual(self.inherit(a1, a2), [])
        self.assertEqual(self.inherit(b1, a3), [])


class PostImpactVelocityTests(unittest.TestCase):
    def test_velocity_is_not_compared_after_the_observers_own_impact(self):
        c = cfg()
        a = track("A", "a1", straight([20, 0], n=30), 0.0, [0, 0])
        b = track("B", "b1", straight([20, 0], n=30), 0.0, [0, 8])
        for sample in b.samples:  # the impulse of B's own collision corrupts its velocity estimates
            sample.velocity = np.array([6.0, 2.5])
        self.assertFalse(pair_evidence(a, b, c).accepted)
        b = dataclasses.replace(b, own_impact=b.samples[0].t_global)
        evidence = pair_evidence(a, b, c)
        self.assertTrue(evidence.accepted)
        self.assertEqual(evidence.median_velocity_chi2, 0.0)


if __name__ == "__main__":
    unittest.main()
