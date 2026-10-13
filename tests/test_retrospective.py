"""Corrected and retrospective identity association (docs/RETROSPECTIVE_RECONSTRUCTION_PLAN.md)."""

import dataclasses
import json
import math
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import numpy as np

from src.cdf.reconstruction import identity
from src.cdf.reconstruction.alignment import match_collisions
from src.cdf.reconstruction.anonymous import CROSS, SPLIT, STITCH, PairEvidence, pair_evidence
from src.cdf.reconstruction.common_frame import CommonSample, CommonTrack
from src.cdf.reconstruction.config import FusionConfig, load_config
from src.cdf.reconstruction.models import GraphNode, LocalGraph

ROOT = Path(__file__).resolve().parents[1]
CONSUMER_VAR = 1.66 ** 2  # consumer GNSS, per axis (docs/robustness_profiles.md)


def cfg(method="corrected", **fusion):
    base = load_config()
    return dataclasses.replace(base, fusion=dataclasses.replace(base.fusion, association_method=method, **fusion))


def box_returns(centre, heading, observer, length=4.6, width=1.9, per_face=8):
    """Returns on the faces of a box visible from the observer (synthetic radar)."""
    f = np.array([math.cos(heading), math.sin(heading)])
    r = np.array([-math.sin(heading), math.cos(heading)])
    faces = [(f, r, length / 2, width), (-f, r, length / 2, width), (r, f, width / 2, length), (-r, f, width / 2, length)]
    points = []
    for normal, tangent, half, span in faces:
        if float(normal @ (observer - centre)) <= 0.0:
            continue
        for u in np.linspace(-0.4, 0.4, per_face):
            points.append(centre + normal * half + tangent * u * span)
    return np.array(points)


def track(recorder, name, centres, heading, observer, speed=10.0, t0=0.0, pose_var=0.0, dt=0.05):
    samples = []
    velocity = speed * np.array([math.cos(heading), math.sin(heading)])
    for k, centre in enumerate(centres):
        centre = np.asarray(centre, float)
        returns = box_returns(centre, heading, np.asarray(observer, float))
        near = returns[np.argmin(np.hypot(*(returns - observer).T))]
        samples.append(CommonSample(t_local=t0 + k * dt, t_global=round(t0 + k * dt, 4), point=np.median(returns, axis=0),
                                    near=near, velocity=velocity, pos_std=0.3, vel_std=0.3,
                                    observer=np.asarray(observer, float), measured=True, heading=heading,
                                    pose_var=pose_var, returns=returns, origins=np.tile(observer, (len(returns), 1))))
    return CommonTrack(recorder=recorder, track_id=name, samples=samples)


def straight(start, n=20, speed=10.0, dt=0.05):
    return [np.array(start, float) + np.array([speed * k * dt, 0.0]) for k in range(n)]


class Poses:
    def __init__(self, std, yaw=0.0):
        self.position_std_m, self.yaw_std_rad = std, yaw


class RadarUncertaintyTests(unittest.TestCase):
    def test_covariance_grows_with_range(self):
        c = cfg()
        near, far = identity.radar_covariance(10.0, 0.3, c), identity.radar_covariance(50.0, 0.3, c)
        self.assertGreater(np.linalg.eigvalsh(far)[-1], np.linalg.eigvalsh(near)[-1])
        # lateral sigma = range x azimuth sigma
        self.assertAlmostEqual(math.sqrt(np.linalg.eigvalsh(far)[-1]), 50.0 * math.radians(c.fusion.radar_azimuth_std_deg),
                               places=6)
        self.assertAlmostEqual(math.sqrt(np.linalg.eigvalsh(far)[0]), c.fusion.radar_range_std_m, places=6)

    def test_the_same_detection_near_has_a_tighter_gate_than_far(self):
        c = cfg()
        a = track("A", "t", straight([5, 0], 1), 0.0, [0, 0]).samples[0]
        b = track("A", "t", straight([60, 0], 1), 0.0, [0, 0]).samples[0]
        self.assertLess(identity.measurement_variance(a, c), identity.measurement_variance(b, c))


class RelativeUncertaintyTests(unittest.TestCase):
    def setUp(self):
        self.c = cfg()
        # One recorder sees two cars side by side, 3.3 m apart (centre to centre), consumer GNSS declared.
        self.a = track("A", "a1", straight([20, 0]), 0.0, [0, 0], pose_var=CONSUMER_VAR)
        self.b = track("A", "a2", straight([20, 3.3]), 0.0, [0, 0], pose_var=CONSUMER_VAR)
        self.rel = identity.RelativePose({"A": Poses(1.66, math.radians(1.0)), "B": Poses(1.66, math.radians(1.0))})

    def test_shared_pose_error_cancels_for_one_recorder(self):
        old = pair_evidence(self.a, self.b, self.c)
        self.assertTrue(old.accepted)  # the absolute variance on both tracks: two cars accepted as one body
        new = identity.pair_corrected(self.a, self.b, self.c, self.rel)
        self.assertFalse(new.accepted)
        self.assertLess(identity.bias_sigma(self.a, self.b, self.rel), 0.1)  # only heading x separation

    def test_cross_recorder_relative_uncertainty_stays(self):
        self.assertAlmostEqual(self.rel.variance("A", "B"), 2 * 1.66 ** 2, places=6)
        joint = {"applied": True, "unknowns": ["A", "B"],
                 "covariance_m2": [[1, 0, 0.9, 0], [0, 1, 0, 0.9], [0.9, 0, 1, 0], [0, 0.9, 0, 1]]}
        refined = identity.RelativePose({"A": Poses(1.0), "B": Poses(1.0)}, joint)
        self.assertAlmostEqual(refined.variance("A", "B"), 0.2, places=6)  # correlated errors: small relative

    def test_high_uncertainty_does_not_make_a_merge_easier(self):
        a = track("A", "a1", straight([20, 0]), 0.0, [0, -6], pose_var=CONSUMER_VAR)
        b = track("B", "b1", straight([20, 0]), 0.0, [0, 6], pose_var=CONSUMER_VAR)
        exact = identity.pair_corrected(dataclasses.replace(a), dataclasses.replace(b), self.c,
                                        identity.RelativePose({"A": Poses(0.0), "B": Poses(0.0)}))
        self.assertTrue(exact.accepted)
        consumer = identity.pair_corrected(a, b, self.c, self.rel)
        self.assertFalse(consumer.accepted)
        self.assertIn("UNRESOLVED", consumer.refused)


class ConstraintTests(unittest.TestCase):
    def setUp(self):
        self.c = cfg()
        self.rel = identity.RelativePose({"A": Poses(0.0), "B": Poses(0.0)})
        self.a1 = track("A", "a1", straight([20, 0]), 0.0, [0, 0])
        self.a2 = track("A", "a2", straight([20, 3.3]), 0.0, [0, 0])
        self.b1 = track("B", "b1", straight([20, 1.6]), 0.0, [0, 10])

    def test_same_recorder_distinct_tracks_cannot_link(self):
        cannot = identity.cannot_links([self.a1, self.a2], self.c, self.rel)
        self.assertIn(frozenset(("A:a1", "A:a2")), cannot)

    def test_cannot_link_survives_clustering(self):
        cannot = identity.cannot_links([self.a1, self.a2], self.c, self.rel)
        links = [PairEvidence("A:a1", "B:b1", CROSS, 20, 1.0, 1.0, 0.1, 0.5, accepted=True),
                 PairEvidence("A:a2", "B:b1", CROSS, 20, 1.0, 1.5, 0.1, 0.5, accepted=True)]
        groups, used = identity.cluster_corrected([self.a1, self.a2, self.b1], links, cannot)
        for group in groups:
            self.assertFalse({"A:a1", "A:a2"} <= {t.name for t in group})

    def test_assignment_is_one_to_one_with_a_clear_winner(self):
        b2 = track("B", "b2", straight([20, 5]), 0.0, [0, 10])
        tracks = {t.name: t for t in (self.a1, self.b1, b2)}
        best = PairEvidence("A:a1", "B:b1", CROSS, 20, 1.0, 0.5, 0.1, 0.5, accepted=True)
        worse = PairEvidence("A:a1", "B:b2", CROSS, 20, 1.0, 9.0, 0.1, 3.0, accepted=True)
        identity.refuse_ambiguous_corrected([best, worse], tracks, self.c)
        self.assertTrue(best.accepted)
        self.assertFalse(worse.accepted)
        self.assertGreater(best.posterior, 0.9)

    def test_near_equal_alternatives_stay_unresolved(self):
        b2 = track("B", "b2", straight([20, 5]), 0.0, [0, 10])
        tracks = {t.name: t for t in (self.a1, self.b1, b2)}
        one = PairEvidence("A:a1", "B:b1", CROSS, 20, 1.0, 0.5, 0.1, 0.5, accepted=True)
        two = PairEvidence("A:a1", "B:b2", CROSS, 20, 1.0, 0.9, 0.1, 0.6, accepted=True)
        identity.refuse_ambiguous_corrected([one, two], tracks, self.c)
        self.assertFalse(one.accepted)
        self.assertFalse(two.accepted)


class RetrospectiveTests(unittest.TestCase):
    def setUp(self):
        self.c = cfg("retrospective")
        self.rel = identity.RelativePose({"A": Poses(0.0), "B": Poses(0.0)})

    def groups(self, gap, later_y=0.0, second_candidate=False, old_y=0.0):
        """An earlier track of A ends; after ``gap`` s the same car is seen by A and B (a strong entity)."""
        old = track("A", "a_old", straight([0, old_y]), 0.0, [-20, -5])
        start = 0.95 + gap  # the earlier track's last sample is at 0.95 s
        x = 10.0 * start
        new_a = track("A", "a_new", straight([x, later_y]), 0.0, [x - 20, -5], t0=start)
        new_b = track("B", "b_new", straight([x, later_y]), 0.0, [x - 20, 8], t0=start)
        groups = [[old], [new_a, new_b]]
        if second_candidate:
            other_a = track("A", "a_other", straight([x, later_y + 2.2]), 0.0, [x - 20, -5], t0=start)
            other_b = track("B", "b_other", straight([x, later_y + 2.2]), 0.0, [x - 20, 8], t0=start)
            groups.append([other_a, other_b])
        return groups

    def test_later_strong_evidence_resolves_an_earlier_identity(self):
        groups, decisions = identity.retrospective_links(self.groups(0.5), {}, self.c, self.rel)
        self.assertEqual(len(groups), 1)
        resolved = [d for d in decisions if d.get("resolved")]
        self.assertEqual(resolved[0]["earlier"], ["A:a_old"])
        self.assertGreaterEqual(resolved[0]["posterior"], self.c.fusion.retrospective_min_posterior)

    def test_a_short_gap_is_stronger_evidence_than_a_long_one(self):
        old, new = self.groups(0.3)[0], self.groups(0.3)[1]
        short = identity.backward_test(old, new, self.c, self.rel)
        old, new = self.groups(2.5)[0], self.groups(2.5)[1]
        long = identity.backward_test(old, new, self.c, self.rel)
        self.assertGreater(short["density"], long["density"])
        self.assertLess(short["position_sigma_m"], long["position_sigma_m"])

    def test_a_long_or_ambiguous_gap_stays_unresolved(self):
        groups, decisions = identity.retrospective_links(self.groups(5.5), {}, self.c, self.rel)
        self.assertEqual(len(groups), 2)
        # Two adjacent cars seen later, the earlier track midway between them: both explain it equally.
        groups, decisions = identity.retrospective_links(self.groups(1.0, second_candidate=True, old_y=1.1), {},
                                                         self.c, self.rel)
        self.assertEqual(len(groups), 3)
        self.assertTrue(all(not d.get("resolved") for d in decisions))

    def test_retrospective_identity_creates_no_earlier_observation(self):
        groups = self.groups(0.5)
        before = [(s.t_global, tuple(s.point)) for s in groups[0][0].samples]
        joined, _ = identity.retrospective_links(groups, {}, self.c, self.rel)
        entity = joined[0]
        self.assertEqual(min(t.start for t in entity), 0.0)  # its first observation, not earlier
        after = [(s.t_global, tuple(s.point)) for s in next(t for t in entity if t.name == "A:a_old").samples]
        self.assertEqual(before, after)  # samples untouched

    def test_cannot_link_blocks_a_retrospective_merge(self):
        groups = self.groups(0.5)
        cannot = {frozenset(("A:a_old", "B:b_new")): {}}
        joined, _ = identity.retrospective_links(groups, cannot, self.c, self.rel)
        self.assertEqual(len(joined), 2)


def graph(owner, reports):
    return LocalGraph(owner, [GraphNode(owner + ":" + str(i), "COLLISION", "OUTCOME", owner, None, t,
                                        {"peak_impulse": v}, "collision_sensor", 1.0) for i, (t, v) in enumerate(reports)])


class CollisionTests(unittest.TestCase):
    def test_competing_collision_candidates_remain_ambiguous(self):
        graphs = [graph("A", [(4.8, 10000.0)]), graph("B", [(4.8, 10100.0), (5.3, 9900.0)])]
        matched, rejected = match_collisions(graphs, FusionConfig(), lambda *a: (2.0, 8.0), lambda *a: None)
        self.assertEqual(matched, [])
        self.assertTrue(any("ambiguous" in r["reason"] for r in rejected))

    def test_a_radar_contradiction_removes_a_candidate(self):
        graphs = [graph("A", [(4.8, 10000.0)]), graph("B", [(4.8, 10100.0), (5.3, 9900.0)])]
        check = lambda a, ta, b, tb: False if abs((tb if a == "A" else ta) - 5.3) < 1e-6 else None
        matched, _ = match_collisions(graphs, FusionConfig(), lambda *a: (2.0, 8.0), check)
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["t_local"]["B"], 4.8)


class RelevanceAndGeneralityTests(unittest.TestCase):
    def test_relevance_range_follows_the_conflict_model(self):
        c = cfg()
        still = identity.relevance_range(13.9, 0.0, 0.2, 0.5, c)
        closing = identity.relevance_range(13.9, 10.0, 0.2, 0.5, c)
        receding = identity.relevance_range(13.9, -10.0, 0.2, 0.5, c)
        self.assertGreater(closing, still)  # closing fast: relevant from farther away
        self.assertLess(receding, still)  # moving away: no possible closure, only the safe distance and 3 sigma
        self.assertAlmostEqual(receding, 13.9 * 1.5 + 1.5, places=1)
        self.assertGreater(identity.relevance_range(13.9, 0.0, 0.2, 2.0, c), still)  # uncertainty widens it
        # 50 km/h, not closing: UN R157 1.5 s gap -> about 20.8 m, plus 3 sigma (velocity) x 6 s and 3 sigma position
        self.assertAlmostEqual(still, 13.9 * 1.5 + 0.6 * 6.0 + 1.5, places=1)

    def test_no_scenario_specific_reconstruction_logic(self):
        import re
        pattern = re.compile(r"""["']S\d{2}["']|scenario_id|run_0_""")
        for path in (ROOT / "src/cdf/reconstruction").glob("*.py"):
            code = [line for line in path.read_text(encoding="utf-8").splitlines() if not line.strip().startswith("#")]
            self.assertFalse([line for line in code if pattern.search(line)], path.name)


class RealRunRegressions(unittest.TestCase):
    """The reconstruction on non-destructive copies (hard links) of committed runs."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="retro_"))
        cls.cache = {}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def reconstruct(self, run, method, condition="exact", seed=0):
        key = (run, method, condition, seed)
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
        target = self.tmp / "_".join((method, condition, str(seed))) / run
        perturbed_copy(ROOT / run, target, perturbation, seed)
        result = reconstruct_run(target, cfg(method), pose_factory=pose)
        self.cache[key] = (target, result)
        return target, result

    def events(self, result):
        return [(n.event_type, n.actor_id, n.subject_id, n.t_global) for n in result.graph.nodes]

    def test_s04_consumer_gnss_impulse_seed3_makes_no_wrong_pairing(self):
        from src.cdf.evaluation.reconstruction import evaluate_run
        for method in ("corrected", "retrospective"):
            target, _ = self.reconstruct("traces/S04/run_0_a_front_pushed", method, "consumer_impulse10", 3)
            evaluation = evaluate_run(target, clock_shift_check=False)
            from src.cdf.evaluation.run_metrics import run_metrics
            from src.cdf.evaluation.fusion_metrics import evaluate_fusion
            metrics = run_metrics(target, evaluation, evaluate_fusion(target, write=False))
            # The wrong pairing of METHOD 1 (A's report with B's later one, 6 m apart under consumer GNSS) is gone:
            # with no decisive evidence the reports stay unmatched rather than wrongly paired.
            self.assertEqual(metrics["false_collision_matches"], 0, method)
        target, _ = self.reconstruct("traces/S04/run_0_a_front_pushed", "corrected", "consumer_impulse10", 0)
        evaluation = evaluate_run(target, clock_shift_check=False)
        self.assertGreaterEqual(sum(c.get("reconstructed_as") is not None for c in evaluation["collisions"]), 2)

    def test_collision_partner_from_the_pre_contact_radar_approach(self):
        from src.cdf.reconstruction.local import reconstruct_vehicle
        from src.cdf.reconstruction.pipeline import read_incident_context
        run = ROOT / "traces/S04/run_0_b_rear_first"
        c = cfg()
        locals_ = [reconstruct_vehicle(p, c, context=read_incident_context(run))
                   for p in sorted((run / "vehicles").iterdir()) if p.is_dir()]
        check = identity.radar_contact_evidence(locals_, c)
        self.assertTrue(check("A", 6.25, "B", 6.25))   # A's front radar sees B arrive at A's report
        self.assertFalse(check("A", 6.25, "B", 4.7))   # under that clock offset B moved otherwise
        self.assertTrue(check("B", 4.7, "C", 4.7))
        # The last radar sweep before the report missing: the approach history still names the partner.
        a = next(l for l in locals_ if l.owner == "A")
        for t in a.tracks:
            t.samples = [s for s in t.samples if s.t_local < 6.25 - 0.06]
        self.assertTrue(check("A", 6.25, "B", 6.25))

    def test_s13_consumer_gnss_has_no_false_merge(self):
        from src.cdf.evaluation.fusion_metrics import evaluate_fusion
        for run in ("traces/S13/run_0_abreast", "traces/S13/run_0_passing", "traces/S13/run_0_platoon"):
            for method in ("corrected", "retrospective"):
                target, _ = self.reconstruct(run, method, "consumer", 0)
                fusion = evaluate_fusion(target, write=False)
                self.assertEqual(fusion["merges"]["false"], 0, (run, method))
                self.assertEqual(sum(d["verdict"].startswith("WRONG") for d in fusion["track_decisions"]), 0)
            target, _ = self.reconstruct(run, "corrected", "exact", 0)
            entities = json.loads((target / "reconstruction/global/anonymous_entities.json").read_text())
            self.assertIn("cannot_links", entities)

    def test_retrospective_moves_no_event_timestamp(self):
        for run in ("traces/S13/run_0_platoon", "traces/S12/run_0_crash"):
            _, corrected = self.reconstruct(run, "corrected")
            _, retrospective = self.reconstruct(run, "retrospective")
            onsets = lambda result: Counter((t, a, round(time, 4)) for t, a, _, time in self.events(result))
            self.assertEqual(onsets(corrected), onsets(retrospective), run)

    def test_s09_s11_s12_regressions(self):
        for method in ("corrected", "retrospective"):
            _, s09 = self.reconstruct("traces/S09/run_0_near_simultaneous", method)
            b = {a.local_track: a.global_entity for a in s09.associations if a.local_graph == "B"}
            self.assertTrue(all(b[k] == "A" for k in b if k.startswith("track_001")), b)
            _, s11 = self.reconstruct("traces/S11/run_0_consequential", method)
            cut_ins = [e for e in self.events(s11) if e[0].startswith("CUT_IN") and e[1] == "A" and e[2] == "C"]
            self.assertEqual(cut_ins, [])
            _, s12 = self.reconstruct("traces/S12/run_0_crash", method)
            u1 = [e for e in self.events(s12) if e[0] == "CUT_IN_FROM_RIGHT_START" and e[1] == "A" and e[2] == "U1"]
            self.assertEqual(len(u1), 1)
            self.assertAlmostEqual(u1[0][3], -2.2, places=2)

    def test_current_method_is_unchanged(self):
        _, current = self.reconstruct("traces/S13/run_0_abreast", "current")
        committed = json.loads((ROOT / "traces/S13/run_0_abreast/reconstruction/global/global_graph.json").read_text())
        mine = json.loads((self.tmp / "current_exact_0/traces/S13/run_0_abreast/reconstruction/global/global_graph.json").read_text())
        self.assertEqual(committed["nodes"], mine["nodes"])
        self.assertEqual(committed["entities"], mine["entities"])


if __name__ == "__main__":
    unittest.main()
