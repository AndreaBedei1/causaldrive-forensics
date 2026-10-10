"""CRITICAL_TTC and the recorder's own collisions (local.contact_partners, local.critical_intervals).

CRITICAL_TTC describes the pre-collision threat.  When the recorder collides with the track of an
active episode, the episode ends at the collision's own timestamp; the continuing contact is a
post-impact state, never a new episode; a new episode for the same pair needs the contact to be
over, the conflict clearly resolved, and a genuinely new conflict.  Pair-specific: other tracks
of the recorder keep their own episodes.  The partner of a contact comes from the recorder's own
tracks only (CLOSING and touching it at the contact), never from ground truth.

Geometry in the recorder's vehicle frame (x forward, y right), a model3-sized recorder (front face
2.4 m ahead of its origin, 2.16 m wide); the target is given by its observed near surface.  Lettered
cases follow the 2026-10-10 specification; G-H use the recorded campaign (traces/).
"""

import math
import unittest
from pathlib import Path

from src.cdf.reconstruction.checks import temporal_safety_relations
from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.local import Contact, contact_partners, reconstruct_vehicle, track_events
from src.cdf.reconstruction.pipeline import read_incident_context
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, EgoTrajectory, LocalTrack, TrackSample

CFG = SemanticsConfig()
CAR = EgoFootprint(x_min=-2.37, x_max=2.4, y_min=-1.08, y_max=1.08)
ROOT = Path(__file__).resolve().parents[1]
STEP = 0.05
TOUCHING = ReconstructionConfig().fusion.touching_clearance_m


def _times(end, start=0.0):
    return [round(start + STEP * k, 2) for k in range(int(round((end - start) / STEP)) + 1)]


def _ego(speed, end=10.0):
    states, x = [], 0.0
    for t in _times(end):
        states.append(EgoState(t_local=t, x=x, y=0.0, heading=0.0, vx=speed, vy=0.0))
        x += speed * STEP
    return EgoTrajectory(states)


def _track(motion, track_id="track_001", start=0.0, end=8.0, vel_std=0.1):
    """motion(t) -> (longitudinal, lateral, vx, vy, closing speed) of the near surface."""
    samples = []
    for t in _times(end, start):
        x, y, vx, vy, closing = motion(t)
        samples.append(TrackSample(t_local=t, x_m=x, y_m=y, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                                   pos_std_m=0.1, vel_std_mps=vel_std, range_m=math.hypot(x, y),
                                   bearing_deg=math.degrees(math.atan2(y, x)), longitudinal_m=x, lateral_m=y,
                                   closing_speed_mps=closing, closing_ttc_s=None, measured=True, n_returns=4,
                                   clearance_m=float(CAR.distance(x, y)), ahead_m=x - CAR.x_max))
    return LocalTrack(track_id, samples)


def _contact(first, last=None):
    return Contact(first=first, last=first if last is None else last, peak=5000.0, attributes={}, merged=[])


def _critical(track, ego, contacts=(), end=10.0):
    """(event, t) of the CRITICAL_TTC events of one track, given its contacts."""
    events = track_events("A", track, end, CFG, ego, footprint=CAR, contacts=contacts)
    return [(e.type, e.t_local) for e in events if e.type.startswith("CRITICAL_TTC")]


def _partners(contacts, tracks):
    return contact_partners(contacts, tracks, STEP, CFG, TOUCHING)


def _rear_end(t_contact=5.0):
    """The recorder at 12 m/s closing at 4 m/s on a car ahead in its path; touching from ``t_contact``."""
    def motion(t):
        if t < t_contact:
            return 2.4 + 4.0 * (t_contact - t), 0.0, 8.0, 0.0, 4.0
        return 2.4, 0.0, 12.0, 0.0, 0.0
    return motion


def _alongside(approach_until, lateral_speed=1.5, side=1.0, after=lambda t: (0.0, 0.0)):
    """A car beside the recorder at its 12 m/s, closing in laterally until its near side touches the
    recorder's side at ``approach_until``; then ``after(t)`` = (lateral speed away, closing)."""
    def motion(t):
        if t < approach_until:
            gap = lateral_speed * (approach_until - t)
            return 0.0, side * (1.08 + gap), 12.0, -side * lateral_speed, lateral_speed
        away, closing = after(t)
        return 0.0, side * (1.08 + away * (t - approach_until)), 12.0, side * away, closing
    return motion


class CollisionEndsTheEpisodeTests(unittest.TestCase):
    def test_a_collision_ends_the_active_episode_at_its_own_timestamp(self):  # A
        ego, track = _ego(12.0), _track(_rear_end(5.0))
        contact = _contact(5.0)
        self.assertEqual(_partners([contact], [track]), {"track_001": [(5.0, 5.0)]})
        events = _critical(track, ego, [(5.0, 5.0)])
        self.assertEqual([name for name, _ in events], ["CRITICAL_TTC_START", "CRITICAL_TTC_END"])
        self.assertEqual(events[-1], ("CRITICAL_TTC_END", 5.0))  # exactly the collision, not 5.0 - epsilon
        # Without the collision the touching car would keep the state (near contact, both moving).
        self.assertNotIn("CRITICAL_TTC_END", [name for name, _ in _critical(track, ego)])

    def test_the_collision_comes_first_at_the_same_timestamp(self):  # A (ordering)
        from src.cdf.reconstruction.models import same_time_rank
        self.assertLess(same_time_rank("COLLISION"), same_time_rank("CRITICAL_TTC_END"))

    def test_a_collision_without_a_critical_episode_invents_nothing(self):  # B
        ego = _ego(12.0)
        # The partner is seen, but its estimate is too uncertain for any CRITICAL_TTC claim.
        uncertain = _track(_rear_end(5.0), vel_std=1.5)
        self.assertEqual(_partners([_contact(5.0)], [uncertain]), {"track_001": [(5.0, 5.0)]})
        self.assertEqual(_critical(uncertain, ego, [(5.0, 5.0)]), [])
        # The partner is not seen at all (struck from the rear blind zone): nothing is attributed.
        ahead = _track(lambda t: (2.4 + 30.0, 0.0, 12.0, 0.0, 0.0))
        self.assertEqual(_partners([_contact(5.0)], [ahead]), {})

    def test_a_collision_with_one_track_leaves_the_others_alone(self):  # C
        ego = _ego(12.0)
        leader = _track(lambda t: (2.4 + 4.0, 0.0, 12.0, 0.0, 0.0), track_id="track_001")  # C: unsafe gap
        side = _track(_alongside(4.0, side=-1.0), track_id="track_002", start=1.0)  # B: sideswipe at 4.0
        partners = _partners([_contact(4.0)], [leader, side])
        self.assertEqual(partners, {"track_002": [(4.0, 4.0)]})
        before = _critical(leader, ego)
        self.assertEqual(_critical(leader, ego, partners.get("track_001", ())), before)  # A-C unchanged
        self.assertEqual(before, [("CRITICAL_TTC_START", 0.5)])  # still active after A's collision with B
        side_events = _critical(side, ego, partners["track_002"])
        self.assertTrue(side_events and side_events[-1] == ("CRITICAL_TTC_END", 4.0), side_events)


class PostImpactTests(unittest.TestCase):
    @staticmethod
    def contact_then(after, last):
        """Alongside, closing in until the contact at 3.0 (lasting to ``last``), then ``after``."""
        ego = _ego(12.0)
        track = _track(_alongside(3.0, after=after))
        return ego, track, [(3.0, last)]

    def test_no_new_episode_while_the_same_contact_lasts(self):  # D
        # Pressed together for 0.8 s; meanwhile the closing speed flares to 1.5 m/s (inside the envelope:
        # each such sample alone would start an episode), then they separate from 4.5 s.
        def after(t):
            if t < 4.5:
                return 0.0, 1.5 if 3.3 <= t < 3.5 or 3.85 <= t < 4.0 else 0.2
            return 1.0, -1.0
        ego, track, contacts = self.contact_then(after, 3.8)
        events = _critical(track, ego, contacts)
        self.assertEqual([name for name, _ in events], ["CRITICAL_TTC_START", "CRITICAL_TTC_END"])
        self.assertLess(events[0][1], 3.0)
        self.assertEqual(events[1], ("CRITICAL_TTC_END", 3.0))
        # Without the collision the state would run on through the contact, as near contact.
        self.assertGreater(max(t for _, t in _critical(track, ego)), 3.8)

    def test_a_new_episode_after_a_real_separation_and_a_new_conflict(self):  # E
        # One contact at 3.0, then they part (out of the envelope, moving apart) and much later converge again.
        ego = _ego(12.0)

        def motion(t):
            if t < 3.0:
                return _alongside(3.0)(t)
            if t < 5.0:
                return 0.0, 1.08 + 2.0 * (t - 3.0), 12.0, 2.0, -2.0  # parting to 4.1 m from the side
            if t < 6.0:
                return 0.0, 5.08, 12.0, 0.0, 0.0
            lateral = max(5.08 - 2.0 * (t - 6.0), 1.08)  # converging again, touching at 8.0
            return 0.0, lateral, 12.0, (-2.0 if lateral > 1.08 else 0.0), (2.0 if lateral > 1.08 else 0.0)
        track = _track(motion, end=9.0)
        events = _critical(track, ego, [(3.0, 3.0)])
        starts = [t for name, t in events if name == "CRITICAL_TTC_START"]
        self.assertEqual(events[1], ("CRITICAL_TTC_END", 3.0))
        self.assertEqual(len(starts), 2)
        self.assertLess(starts[0], 3.0)
        self.assertGreaterEqual(starts[1], 6.0)  # once they converge again, not the aftermath of the first


class MultiCollisionTests(unittest.TestCase):
    def test_each_collision_ends_only_its_own_pair(self):  # F
        # Recorder B: struck on its left by A at 3.0 (A then drifts away), then runs into C ahead at 4.0.
        ego = _ego(12.0)
        a = _track(_alongside(3.0, side=-1.0, after=lambda t: (1.5, -1.5)), track_id="track_001", start=0.5)

        def ahead(t):  # C, slower, in B's path: closing at 3 m/s, touching at 4.0
            if t < 4.0:
                return 2.4 + 3.0 * (4.0 - t), 0.0, 9.0, 0.0, 3.0
            return 2.4, 0.0, 12.0, 0.0, 0.0
        c = _track(ahead, track_id="track_002")
        partners = _partners([_contact(3.0), _contact(4.0)], [a, c])
        self.assertEqual(partners, {"track_001": [(3.0, 3.0)], "track_002": [(4.0, 4.0)]})
        c_events = _critical(c, ego, partners["track_002"])
        self.assertIn(("CRITICAL_TTC_END", 4.0), c_events)  # its own collision...
        self.assertNotIn(("CRITICAL_TTC_END", 3.0), c_events)  # ...not A's
        a_events = _critical(a, ego, partners["track_001"])
        self.assertTrue(all(t <= 3.0 for name, t in a_events if name == "CRITICAL_TTC_END"), a_events)

    def test_a_car_still_pressed_against_the_recorder_is_not_the_partner_of_a_new_impact(self):  # F
        # B is struck from behind (the striker is in the rear blind zone) while still touching C ahead
        # after an earlier contact: C is not closing in, so the new contact is attributed to nobody.
        pressed = _track(lambda t: (2.45, 0.0, 12.0, 0.0, 0.0))
        self.assertEqual(_partners([_contact(6.0)], [pressed]), {})

    def test_two_tracks_closing_and_touching_are_ambiguous(self):
        left = _track(_alongside(4.0, side=-1.0), track_id="track_001")
        right = _track(_alongside(4.0, side=1.0), track_id="track_002")
        self.assertEqual(_partners([_contact(4.0)], [left, right]), {})


class S17Tests(unittest.TestCase):  # G
    """S17: A (cut in on by the unrecorded C) swerves into B.  Reconstructed live from the raw files."""

    run_dir = ROOT / "traces" / "S17" / "run_0_crash"

    @classmethod
    def setUpClass(cls):
        if not (cls.run_dir / "vehicles" / "A").exists():
            raise unittest.SkipTest("canonical trace not present")
        config, context = ReconstructionConfig(), read_incident_context(cls.run_dir)
        cls.nodes = {owner: [(n.event_type, n.subject_id, n.t_local)
                             for n in reconstruct_vehicle(cls.run_dir / "vehicles" / owner, config,
                                                          context=context).graph.nodes]
                     for owner in ("A", "B")}

    def events(self, owner, subject, name):
        return [t for event, s, t in self.nodes[owner] if event == name and s == subject]

    def collision(self, owner):
        return next(t for event, _, t in self.nodes[owner] if event == "COLLISION")

    def test_both_critical_states_between_a_and_b_end_at_their_collision(self):
        for owner, track in (("A", "track_002"), ("B", "track_001")):
            collision = self.collision(owner)
            starts = self.events(owner, track, "CRITICAL_TTC_START")
            self.assertEqual(len(starts), 1)
            self.assertLess(starts[0], collision)
            self.assertEqual(self.events(owner, track, "CRITICAL_TTC_END"), [collision])

    def test_a_about_the_anonymous_track_is_not_ended_by_the_collision_with_b(self):
        collision = self.collision("A")
        self.assertEqual(self.events("A", "track_001", "CRITICAL_TTC_START"), [2.6])
        ends = self.events("A", "track_001", "CRITICAL_TTC_END")
        self.assertEqual(len(ends), 1)
        self.assertGreater(ends[0], collision)  # its own geometric release (C clearly aside)


class S02RegressionTests(unittest.TestCase):  # H
    def test_s02_critical_before_cut_in_keeps_its_order(self):
        run = ROOT / "traces" / "S02" / "run_0_critical_before_cut_in"
        if not (run / "vehicles" / "A").exists():
            self.skipTest("canonical trace not present")
        local = reconstruct_vehicle(run / "vehicles" / "A", ReconstructionConfig(), context=read_incident_context(run))
        relation = next(item for item in temporal_safety_relations(local.graph) if item["track"] == "track_001")
        self.assertEqual(relation["cut_in_vs_critical_ttc"], "CRITICAL_TTC_ALREADY_ACTIVE")
        self.assertLess(relation["critical_ttc_start"], relation["cut_in"]["t_local"])
        collision = next(n.t_local for n in local.graph.nodes if n.event_type == "COLLISION")
        ends = [n.t_local for n in local.graph.nodes if n.event_type == "CRITICAL_TTC_END" and n.subject_id == "track_001"]
        self.assertEqual(ends, [collision])


if __name__ == "__main__":
    unittest.main()
