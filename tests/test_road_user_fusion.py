"""Road users in the common frame: box fit, covariance intersection, cross-observer association,
stitching, clustering, observed alignment, recorder links -- and no privileged input anywhere."""

import json
import math
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.reconstruction.anonymous import (CROSS, STITCH, PairEvidence, chi2_2dof,
                                              covariance_intersection, fit_box, offset_decision, pair_evidence,
                                              stitch_evidence)
from src.cdf.reconstruction.identity import cluster_corrected, refuse_ambiguous_corrected
from src.cdf.reconstruction.common_frame import CommonSample, CommonTrack, RecordedPoseSource, shifted
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.models import is_anonymous_entity
from src.cdf.reconstruction.pipeline import reconstruct_run

ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "traces"
CFG = ReconstructionConfig()


# --------------------------------------------------------------------------
# Synthetic observations of rigid boxes
# --------------------------------------------------------------------------

def box_returns(centre, heading, length, width, radar, per_face=9):
    """Radar returns on the faces of a box that face the radar, and their radar positions."""
    f = np.array([math.cos(heading), math.sin(heading)])
    r = np.array([-math.sin(heading), math.cos(heading)])
    centre, radar = np.asarray(centre, float), np.asarray(radar, float)
    points = []
    for normal, tangent, half, other in ((f, r, length / 2, width / 2), (-f, r, length / 2, width / 2),
                                         (r, f, width / 2, length / 2), (-r, f, width / 2, length / 2)):
        middle = centre + normal * half
        if normal @ (radar - middle) <= 0.0:
            continue
        for s in np.linspace(-0.9 * other, 0.9 * other, per_face):
            points.append(middle + tangent * s)
    points = np.array(points)
    return points, np.repeat(radar[None, :], len(points), axis=0)


def observe(t, centre, heading, speed, radar, length=4.6, width=1.9, measured=True):
    points, origins = box_returns(centre, heading, length, width, radar)
    near = points[np.argmin(np.hypot(*(points - radar).T))]
    velocity = speed * np.array([math.cos(heading), math.sin(heading)])
    return CommonSample(t_local=t, t_global=round(t, 4), point=np.median(points, axis=0), near=near,
                        velocity=velocity, pos_std=0.3, vel_std=0.2, observer=np.asarray(radar, float),
                        measured=measured, heading=heading, returns=points, origins=origins)


def track(recorder, track_id, times, motion, radar_of, length=4.6, width=1.9):
    """A track of one box: ``motion(t) -> (centre, heading, speed)``, ``radar_of(t) -> radar position``."""
    samples = []
    for t in times:
        centre, heading, speed = motion(t)
        samples.append(observe(t, centre, heading, speed, radar_of(t), length, width))
    return CommonTrack(recorder, track_id, samples)


def straight(x0, y0, speed, heading=0.0):
    return lambda t: (np.array([x0 + speed * t * math.cos(heading), y0 + speed * t * math.sin(heading)]),
                      heading, speed)


def following(x0, y0, speed):
    """A radar moving along x at ``speed`` from (x0, y0)."""
    return lambda t: np.array([x0 + speed * t, y0])


TIMES = [round(0.05 * k, 4) for k in range(60)]  # 3 s at 20 Hz


class BoxFitTests(unittest.TestCase):
    def test_two_observers_seeing_different_faces_fix_the_centre_and_the_size(self):
        centre, heading = np.array([10.0, 5.0]), math.radians(30.0)
        f = np.array([math.cos(heading), math.sin(heading)])
        r = np.array([-math.sin(heading), math.cos(heading)])  # to the right of the heading
        behind_left = centre - 12.0 * f - 6.0 * r  # sees the rear and the left face
        ahead_right = centre + 9.0 * f + 6.0 * r   # sees the front and the right face
        a = observe(0.0, centre, heading, 10.0, behind_left, length=4.2, width=1.8)
        b = observe(0.0, centre, heading, 10.0, ahead_right, length=4.2, width=1.8)
        fit = fit_box([("A", a), ("B", b)], heading, CFG)
        self.assertLess(float(np.hypot(*(fit.centre - centre))), 0.05)
        self.assertAlmostEqual(2.0 * fit.halves[0], 4.2, delta=0.1)
        self.assertAlmostEqual(2.0 * fit.halves[1], 1.8, delta=0.1)
        self.assertEqual((fit.faces, fit.observers), (4, 2))

    def test_one_face_of_one_observer_leans_on_the_prior_along_the_face(self):
        centre, heading = np.array([0.0, 0.0]), 0.0
        behind = np.array([-20.0, 0.0])  # the rear face only
        fit = fit_box([("A", observe(0.0, centre, heading, 10.0, behind))], heading, CFG)
        self.assertLess(float(np.hypot(*(fit.centre - centre))), 0.05)  # prior length = true length
        # Along the rear face (the lateral axis) the centre is known only from the returns' spread.
        self.assertGreater(math.sqrt(fit.covariance[1, 1]), math.sqrt(fit.covariance[0, 0]))

    def test_covariance_intersection_never_beats_the_better_estimate_by_assuming_independence(self):
        a = (np.array([0.0, 0.0]), np.diag([1.0, 4.0]))
        b = (np.array([1.0, 0.0]), np.diag([4.0, 1.0]))
        mean, cov = covariance_intersection([a, b])
        self.assertLessEqual(np.trace(cov), min(np.trace(a[1]), np.trace(b[1])) + 1e-9)
        # Consistent for any cross-correlation: never tighter than the Kalman (independent) fusion.
        independent = np.linalg.inv(np.linalg.inv(a[1]) + np.linalg.inv(b[1]))
        self.assertTrue(np.all(np.linalg.eigvalsh(cov - independent) >= -1e-9))
        self.assertTrue(0.0 <= mean[0] <= 1.0)
        same, same_cov = covariance_intersection([a, a])
        np.testing.assert_allclose(same, a[0])
        np.testing.assert_allclose(same_cov, a[1], atol=1e-6)


class AssociationTests(unittest.TestCase):
    def test_one_box_seen_from_two_sides_is_one_road_user(self):
        motion = straight(30.0, 0.0, 12.0)
        a = track("A", "track_001", TIMES, motion, following(0.0, 0.0, 12.0))      # behind it
        b = track("B", "track_002", TIMES, motion, following(40.0, -3.5, 12.0))    # ahead of it, left lane
        evidence = pair_evidence(a, b, CFG)
        self.assertTrue(evidence.accepted, evidence)
        self.assertGreaterEqual(evidence.passed, 0.95)
        # Their track points (rear face; front-left corner) differ by most of a car length; their boxes do not.
        self.assertGreater(float(np.hypot(*(a.samples[0].point - b.samples[0].point))), 1.5)
        self.assertLess(evidence.centre_gap_m, 0.3)

    def test_two_cars_abreast_at_the_same_speed_stay_two(self):
        middle, right = straight(30.0, 0.0, 12.0), straight(30.0, 3.5, 12.0)
        a = track("A", "track_001", TIMES, middle, following(0.0, 0.0, 12.0))     # A behind the middle car
        b = track("B", "track_001", TIMES, right, following(25.0, -3.5, 12.0))    # B's track of the right car
        evidence = pair_evidence(a, b, CFG)
        self.assertIsNotNone(evidence)
        self.assertFalse(evidence.accepted, evidence)
        self.assertLess(evidence.passed, 0.2)

    def test_two_cars_in_a_platoon_stay_two(self):
        lead, follower = straight(38.0, 0.0, 12.0), straight(30.0, 0.0, 12.0)
        a = track("A", "track_001", TIMES, follower, following(0.0, 0.0, 12.0))   # the follower's rear
        b = track("B", "track_001", TIMES, lead, following(30.0, -3.5, 12.0))     # the leader's left side
        evidence = pair_evidence(a, b, CFG)
        self.assertFalse(evidence.accepted, evidence)

    def test_a_road_user_lost_and_found_again_is_stitched(self):
        motion = straight(30.0, 0.0, 12.0)
        radar = following(0.0, 0.0, 12.0)
        before = track("B", "track_002", TIMES[:30], motion, radar)
        after = track("B", "track_003", [round(t + 0.7, 4) for t in TIMES[30:]], motion, radar)
        evidence = stitch_evidence(before, after, CFG)
        self.assertTrue(evidence.accepted, evidence)
        self.assertEqual(evidence.kind, STITCH)
        self.assertAlmostEqual(evidence.gap_s, 0.75, places=2)

    def test_a_track_starting_where_no_prediction_goes_is_not_stitched(self):
        radar = following(0.0, 0.0, 12.0)
        before = track("B", "track_002", TIMES[:30], straight(30.0, 0.0, 12.0), radar)
        after = track("B", "track_003", [round(t + 0.7, 4) for t in TIMES[30:]], straight(30.0, 7.0, 12.0), radar)
        self.assertFalse(stitch_evidence(before, after, CFG).accepted)
        late = track("B", "track_004", [round(t + 3.0, 4) for t in TIMES[30:]], straight(30.0, 0.0, 12.0), radar)
        self.assertIsNone(stitch_evidence(before, late, CFG))

    def test_a_detected_identity_boundary_cannot_stitch_to_a_different_track(self):
        motion, radar = straight(30.0, 0.0, 12.0), following(0.0, 0.0, 12.0)
        before = track('B', 'track_001#segment_1', TIMES[:30], motion, radar)
        after = track('B', 'track_003', [round(t + 0.7, 4) for t in TIMES[30:]], motion, radar)
        self.assertTrue(stitch_evidence(before, after, CFG).accepted)
        before.parent_track = 'track_001'
        self.assertIsNone(stitch_evidence(before, after, CFG))
        # Actual simultaneous evidence is still usable on the stable part.
        other = track('A', 'track_001', TIMES[:30], motion, following(40.0, -3.5, 12.0))
        self.assertTrue(pair_evidence(before, other, CFG).accepted)

    def test_parallel_bodies_cannot_stitch_across_an_unobserved_lane_jump(self):
        radar = following(0.0, 0.0, 12.0)
        before = track('B', 'track_001', TIMES[:30], straight(30.0, 0.0, 12.0), radar)
        after = track('B', 'track_002', [round(t + 1.0, 4) for t in TIMES[30:]],
                      straight(30.0, 3.5, 12.0), radar)
        evidence = stitch_evidence(before, after, CFG)
        # The old isotropic acceleration allowance admitted this same-speed
        # lane jump. Independent lateral face support must reject it.
        self.assertLess(evidence.median_box_chi2, chi2_2dof(CFG.fusion.anonymous_gate_probability))
        self.assertGreater(evidence.lateral_chi2, chi2_2dof(CFG.fusion.anonymous_gate_probability))
        self.assertFalse(evidence.accepted)

    def test_a_track_with_two_possible_successors_is_stitched_to_neither(self):
        tracks = {name: CommonTrack(name.split(":")[0], name.split(":")[1],
                                    [observe(t, np.zeros(2), 0.0, 5.0, np.array([-20.0, 0.0])) for t in times])
                  for name, times in (("B:t1", [0.0, 0.05]), ("B:t2", [0.5, 0.55]), ("B:t3", [0.5, 0.55]))}
        first = PairEvidence("B:t1", "B:t2", STITCH, 1, 1.0, 1.0, 0.5, 0.5, 0.45, accepted=True)
        second = PairEvidence("B:t1", "B:t3", STITCH, 1, 1.0, 2.0, 0.5, 0.5, 0.45, accepted=True)
        refuse_ambiguous_corrected([first, second], tracks, CFG)
        self.assertFalse(first.accepted or second.accepted)
        self.assertIn("two possible successors", first.refused)

    def test_a_track_compatible_with_two_simultaneous_tracks_of_one_observer_is_joined_to_neither(self):
        times = [0.0, 0.05, 0.1]
        tracks = {name: CommonTrack(name.split(":")[0], name.split(":")[1],
                                    [observe(t, np.zeros(2), 0.0, 5.0, np.array([-20.0, 0.0])) for t in times])
                  for name in ("A:t1", "B:t1", "B:t2")}
        one = PairEvidence("A:t1", "B:t1", CROSS, 20, 1.0, 0.5, 0.5, 0.2, accepted=True)
        two = PairEvidence("A:t1", "B:t2", CROSS, 20, 0.9, 0.7, 0.5, 0.3, accepted=True)
        refuse_ambiguous_corrected([one, two], tracks, CFG)
        self.assertFalse(one.accepted or two.accepted)
        self.assertIn("two simultaneous tracks of B", one.refused)

    def test_clusters_never_hold_two_simultaneous_tracks_of_one_observer(self):
        times = [0.0, 0.05, 0.1]
        tracks = [CommonTrack(name.split(":")[0], name.split(":")[1],
                              [observe(t, np.zeros(2), 0.0, 5.0, np.array([-20.0, 0.0])) for t in times])
                  for name in ("A:t1", "B:t1", "B:t2")]
        # Two accepted links that would chain B:t1 and B:t2 (simultaneous) through A:t1.
        links = [PairEvidence("A:t1", "B:t1", CROSS, 20, 1.0, 0.1, 0.1, 0.1, accepted=True),
                 PairEvidence("A:t1", "B:t2", CROSS, 20, 1.0, 0.2, 0.2, 0.1, accepted=True)]
        groups, used = cluster_corrected(tracks, links, {})
        self.assertEqual(sorted(len(group) for group in groups), [1, 2])
        self.assertEqual(len(used), 1)
        self.assertIn("simultaneous", links[1].refused)

    def test_a_sample_carried_to_a_nearby_instant_moves_at_its_own_velocity(self):
        sample = observe(1.0, np.array([0.0, 0.0]), 0.0, 10.0, np.array([-20.0, 0.0]))
        moved = shifted(sample, 1.02)
        np.testing.assert_allclose(moved.point - sample.point, [0.2, 0.0], atol=1e-9)
        np.testing.assert_allclose(moved.returns - sample.returns, np.tile([0.2, 0.0], (len(sample.returns), 1)))
        np.testing.assert_allclose(moved.observer, sample.observer)

    def test_the_gates_are_chi_square_quantiles(self):
        self.assertAlmostEqual(chi2_2dof(0.99), 9.2103, places=3)
        self.assertAlmostEqual(chi2_2dof(0.95), 5.9915, places=3)


# --------------------------------------------------------------------------
# The canonical runs (reconstructed into a scratch copy; never written back)
# --------------------------------------------------------------------------

def scratch_copy(run: Path, destination: Path, poison: bool = False, rename: dict = None) -> Path:
    """The recorders' own files (and the incident context) of a run; optionally with poisoned privileged
    files beside them, or with the recorders renamed."""
    target = destination / run.parent.name / run.name
    for vehicle in sorted((run / "vehicles").iterdir()):
        if vehicle.is_dir():
            shutil.copytree(vehicle, target / "vehicles" / (rename or {}).get(vehicle.name, vehicle.name))
    if (run / "incident_context.json").exists():
        shutil.copy(run / "incident_context.json", target / "incident_context.json")
    if poison:
        (target / "ground_truth").mkdir(parents=True)
        lie = {"participant_id": "C", "actor_id": 1, "timestamp": 0.0, "note": "poisoned: must never be read"}
        for name in ("states.jsonl", "collisions.jsonl", "events.jsonl", "triggers.jsonl"):
            (target / "ground_truth" / name).write_text(json.dumps(lie) + "\n", encoding="utf-8")
        (target / "metadata.json").write_text(json.dumps({"scenario_id": "S99", "participants": {
            "C": {"record": False, "track": "A:track_001"}}}), encoding="utf-8")
    return target


def entities_of(run_dir: Path):
    return json.loads((run_dir / "reconstruction" / "global" / "anonymous_entities.json").read_text(encoding="utf-8"))


class CanonicalRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name)
        cls.s12 = scratch_copy(TRACES / "S12" / "run_0_crash", base / "clean")
        cls.s12_result = reconstruct_run(cls.s12, CFG)
        cls.s12_poisoned = scratch_copy(TRACES / "S12" / "run_0_crash", base / "poisoned", poison=True)
        reconstruct_run(cls.s12_poisoned, CFG)
        cls.s12_renamed = scratch_copy(TRACES / "S12" / "run_0_crash", base / "renamed", rename={"A": "P", "B": "Q"})
        reconstruct_run(cls.s12_renamed, CFG)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_s12_the_three_tracks_of_the_non_recorder_are_one_anonymous_road_user(self):
        entities = entities_of(self.s12)["entities"]
        self.assertEqual([e["id"] for e in entities], ["U1"])
        u1 = entities[0]
        self.assertEqual(u1["source_tracks"], ["A:track_001", "B:track_002", "B:track_003"])
        self.assertTrue(u1["anonymous"])
        self.assertEqual(u1["observers"], ["A", "B"])
        # Every member is joined by accepted evidence that passed at every compared instant (the brief third
        # track through its simultaneous observation by A, not by a stitch across B's gap).
        links = u1["association"]["links"]
        self.assertEqual(len(links), 2)
        self.assertTrue(all(link["accepted"] and link["passed"] == 1.0 for link in links))
        joined = {link["a"] for link in links} | {link["b"] for link in links}
        self.assertEqual(joined, {"A:track_001", "B:track_002", "B:track_003"})
        self.assertTrue(all(link["kind"] in (CROSS, STITCH) for link in links))
        self.assertIn("box_fit", u1["fusion_method"])
        names = {(a.local_graph, a.local_track): a.global_entity for a in self.s12_result.associations}
        self.assertEqual({names[("A", "track_001")], names[("B", "track_002")], names[("B", "track_003")]}, {"U1"})
        self.assertEqual((names[("A", "track_002")], names[("B", "track_001")]), ("B", "A"))

    def test_s12_the_global_graph_names_the_road_user_u1_and_never_c(self):
        graph = json.loads((self.s12 / "reconstruction" / "global" / "global_graph.json").read_text())
        mentioned = {n["actor_id"] for n in graph["nodes"]} | {n["subject_id"] for n in graph["nodes"]}
        self.assertNotIn("C", mentioned)
        self.assertIn(("EGO_PATH_ENTRY", "U1"), {(n["event_type"], n["subject_id"]) for n in graph["nodes"]
                                                 if n["actor_id"] == "A"})
        anonymous = [e for e in graph["entities"] if e["kind"] == "anonymous_road_user"]
        self.assertEqual([(e["entity_id"], e["observed_as"]) for e in anonymous],
                         [("U1", ["A:track_001", "B:track_002", "B:track_003"])])
        self.assertTrue(all(is_anonymous_entity(e["entity_id"]) for e in anonymous))

    def test_poisoned_privileged_files_change_nothing(self):
        clean, poisoned = entities_of(self.s12), entities_of(self.s12_poisoned)
        self.assertEqual(clean, poisoned)
        for name in ("associations.json", "alignment.json", "global_graph.json"):
            self.assertEqual((self.s12 / "reconstruction" / "global" / name).read_text(encoding="utf-8"),
                             (self.s12_poisoned / "reconstruction" / "global" / name).read_text(encoding="utf-8"))

    def test_renamed_recorders_give_the_same_road_user(self):
        # No rule knows a participant's name: renaming the recorders renames the source tracks only.
        renamed = entities_of(self.s12_renamed)["entities"]
        self.assertEqual([e["id"] for e in renamed], ["U1"])
        self.assertEqual(renamed[0]["source_tracks"], ["P:track_001", "Q:track_002", "Q:track_003"])
        clean = entities_of(self.s12)["entities"][0]
        self.assertEqual([s["x"] for s in renamed[0]["trajectory"]], [s["x"] for s in clean["trajectory"]])

    def test_the_fusion_source_names_no_scenario_and_no_participant(self):
        for name in ("anonymous.py", "common_frame.py"):
            text = (ROOT / "src" / "cdf" / "reconstruction" / name).read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[\"']S\d\d[\"'/]", text), name)
            self.assertNotIn("record: false", text)
            for field in ("ground_truth", "actor_id", "participant_id", "metadata.json", "scenario_id"):
                self.assertNotIn(field, text, (name, field))


class LinkAndAlignmentTests(unittest.TestCase):
    def test_s11_the_van_tracks_are_recorder_c(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = scratch_copy(TRACES / "S11" / "run_0_consequential", Path(tmp))
            result = reconstruct_run(run, CFG)
            record = entities_of(run)
        names = {(a.local_graph + ":" + a.local_track): (a.status, a.global_entity) for a in result.associations}
        # A's and B's tracks of the van (identities verified against the evaluation's ground truth).
        for name in ("A:track_001", "B:track_002#segment_1"):
            self.assertEqual(names[name], ("ASSOCIATED", "C"), name)
        # A's track is named by the A-C collision evidence, B's by its returns on the van's own outline.
        self.assertEqual(sorted(link["track"] for link in record["recorder_links"]), ["B:track_002#segment_1"])
        # B's later fragment of the van starts after the van touched A: its returns lie within the uncertainty of
        # both bodies, so it is named neither (unresolved, conservatively), and never wrongly.
        self.assertEqual(names["B:track_003"][0], "ANONYMOUS")
        self.assertNotIn(names["B:track_003"][1], ("A", "B", "C"))

    def test_s06_recorder_c_is_aligned_by_its_observed_trajectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = scratch_copy(TRACES / "S06" / "run_0_crash", Path(tmp))
            result = reconstruct_run(run, CFG)
            record = entities_of(run)
        clock = result.alignment.graphs["C"]
        self.assertEqual((clock.status, clock.method), ("ALIGNED", "observed_trajectories"))
        # The recorders' clocks started together (A and B are aligned at -4.10 by their collision).
        self.assertAlmostEqual(clock.offset_to_global, result.alignment.graphs["A"].offset_to_global, delta=0.051)
        decision = record["observed_alignment"][0]
        self.assertTrue(decision["accepted"])
        self.assertLessEqual(decision["interval"][0], -4.1)
        self.assertGreaterEqual(decision["interval"][1], -4.1)
        names = {(a.local_graph + ":" + a.local_track): a.global_entity for a in result.associations}
        # C's two tracks of A and its track of B (identities verified against the evaluation's ground truth).
        self.assertEqual(names["C:track_003"], "B")
        self.assertEqual((names["A:track_001"], names["B:track_001"], names["C:track_001"], names["C:track_002"]),
                         ("C", "C", "A", "A"))
        observed = next(local for local in result.locals if local.owner == 'C')
        # At 75 m one missed sweep already makes A's predicted position too uncertain to tell two cars apart, so
        # the tracker ends the track and starts a new one (uncertainty-driven survival); the fusion names every
        # fragment: none of C's tracks stays ambiguous or anonymous.
        self.assertFalse([t for t in observed.tracks if t.identity_ambiguous])
        self.assertEqual({names["C:" + t.track_id] for t in observed.tracks}, {"A", "B"})

    def test_s05_a_slowly_moving_recorder_is_aligned_along_the_lines_of_sight(self):
        # C, ahead of B, stops early: only B's view of it fixes its clock.  Comparing each near surface with
        # where its line of sight enters C's body (not with C's whole outline) leaves one interval of offsets,
        # within one radar period of the truth (-5.90 s, privileged; phase 1 refused it as not unique).
        with tempfile.TemporaryDirectory() as tmp:
            run = scratch_copy(TRACES / "S05" / "run_0_crash", Path(tmp))
            result = reconstruct_run(run, CFG)
            record = entities_of(run)
        clock = result.alignment.graphs["C"]
        self.assertEqual((clock.status, clock.method), ("ALIGNED", "observed_trajectories"))
        self.assertLessEqual(abs(clock.offset_to_global - (-5.90)), 0.051)
        decision = record["observed_alignment"][0]
        self.assertTrue(decision["accepted"])
        self.assertEqual(decision["other_intervals"], 0)
        self.assertLessEqual(decision["interval"][1] - decision["interval"][0], 0.1 + 1e-9)
        names = {(a.local_graph, a.local_track): (a.status, a.global_entity) for a in result.associations}
        self.assertEqual(names[("B", "track_001")], ("ASSOCIATED", "C"))

    def test_an_offset_is_refused_when_another_interval_fits(self):
        grid = np.arange(0, 40)
        one = np.full(40, 9.0)
        one[10:13] = [1.5, 0.6, 1.5]
        k, threshold, home, others = offset_decision(one, 3.0)
        self.assertEqual((k, home, others), (11, (10, 12), []))  # one sharp minimum: accepted
        two = one.copy()
        two[30:32] = [1.1, 1.2]  # a second place where the observations fit (a target at rest)
        k, threshold, home, others = offset_decision(two, 3.0)
        self.assertEqual(k, 11)
        self.assertEqual(len(others), 1)  # refused: not unique
        far = np.full(40, 9.0)
        far[20] = 2.5
        k, threshold, home, others = offset_decision(far, 3.0)
        self.assertGreater(float(far[k]), 2.0)  # refused: beyond 2 sigma
        self.assertEqual(len(grid), 40)

    def test_pose_sources_declare_their_accuracy(self):
        rows = [{"timestamp": t, "x": t, "y": 0.0, "yaw_deg": 0.0, "velocity": {"x": 1.0, "y": 0.0}} for t in (0.0, 1.0)]
        source = RecordedPoseSource(rows, 0.0)
        self.assertEqual((source.position_std_m, source.yaw_std_rad, source.velocity_std_mps), (0.0, 0.0, 0.0))
        pose = source.pose_at(0.5)
        self.assertAlmostEqual(pose.x, 0.5)
        xs, _, _ = source.poses_at([0.25, 0.75, 2.0])
        np.testing.assert_allclose(xs, [0.25, 0.75, 1.0])


if __name__ == "__main__":
    unittest.main()
