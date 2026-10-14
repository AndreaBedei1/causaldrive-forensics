"""The replay HUD lists the semantic states active at the replay time (presentation.active_states_at /
active_state_lines): START..END intervals of the reconstructed events, at most 8 lines then ``... +N more``,
deterministic priority, no UNKNOWN ('?') line and no PREDICTED text."""

import unittest
from pathlib import Path

from src.cdf.replay.model import LocalEvents, PerceivedStates, ReplayEvent, ReplayRun, state_intervals
from src.cdf.replay.presentation import (MAX_ACTIVE_LINES, active_state_lines, active_states_at,
                                         standard_panel_lines)


def run_of(*events, duration=10.0):
    """A replay run made only of the given (time, actor, event type, subject[, attributes]) events."""
    by_actor = {}
    for number, item in enumerate(events):
        time, actor, kind, subject = item[:4]
        attributes = item[4] if len(item) > 4 else {}
        by_actor.setdefault(actor, []).append(
            ReplayEvent(time, actor, kind, subject, "{0}:e{1:02d}".format(actor, number), dict(attributes)))
    local = {actor: LocalEvents(actor, 0.0, evs, state_intervals(evs), 0.0) for actor, evs in by_actor.items()}
    return ReplayRun(run_dir=Path("."), name="synthetic", participants=[], start=0.0, duration=duration,
                     local_events=local)


def texts(run, t):
    return [text for text, _ in active_state_lines(active_states_at(run, t))]


class ActiveStateTests(unittest.TestCase):
    def test_a_three_active_states_are_all_shown(self):
        run = run_of((1.0, "A", "BRAKE_START", None), (1.0, "A", "CRITICAL_TTC_START", "B"),
                     (1.0, "B", "TURN_LEFT_START", None))
        self.assertEqual(texts(run, 2.0), ["A -> B  CRITICAL_TTC", "A       BRAKE", "B       TURN_LEFT"])

    def test_b_eight_active_states_are_all_shown_without_ellipsis(self):
        run = run_of(*[(1.0, "A", "CLOSING_START", "U{0}".format(k)) for k in range(1, 9)])
        lines = texts(run, 2.0)
        self.assertEqual(len(lines), MAX_ACTIVE_LINES)
        self.assertFalse(any(line.startswith("...") for line in lines))

    def test_c_eleven_active_states_show_eight_and_the_count_of_the_rest(self):
        run = run_of(*[(1.0, "A", "CLOSING_START", "U{0:02d}".format(k)) for k in range(1, 12)])
        lines = texts(run, 2.0)
        self.assertEqual(len(lines), MAX_ACTIVE_LINES + 1)
        self.assertEqual(lines[-1], "... +3 more")
        self.assertEqual(len(active_states_at(run, 2.0)), 11)  # nothing dropped from the data

    def test_d_an_unknown_state_is_hidden(self):
        # The subject is lost while critical and no END follows: its state is unknown from then on.
        run = run_of((1.0, "A", "CRITICAL_TTC_START", "track_009"), (2.0, "A", "TRACK_LOST", "track_009"))
        self.assertEqual(texts(run, 1.5), ["A -> track_009  CRITICAL_TTC"])
        self.assertEqual(texts(run, 3.0), [])
        for t in (1.5, 3.0):
            self.assertFalse(any("?" in line or "UNKNOWN" in line for line in texts(run, t)))
            self.assertFalse(any("?" in text for text, _ in standard_panel_lines(run, "A", t, 1.0)))

    def test_d_a_state_the_frame_marks_unknown_is_hidden_not_false(self):
        # The graph's interval stays open (a second track of C took over, then became UNKNOWN).
        run = run_of((1.0, "A", "CRITICAL_TTC_START", "C"))
        frame = lambda value: {"ego": {}, "external": {"track_001": {"CRITICAL_TTC": False},
                                                        "track_002": {"CRITICAL_TTC": value}}}
        run.identities = {("A", "track_001"): "C", ("A", "track_002"): "C"}
        run.perceived = {"A": PerceivedStates([1.0, 2.0, 3.0], [frame(True), frame("UNKNOWN"), frame(False)])}
        self.assertEqual(texts(run, 1.5), ["A -> C  CRITICAL_TTC"])
        self.assertEqual(texts(run, 2.5), [])  # UNKNOWN: hidden
        self.assertEqual(texts(run, 3.5), ["A -> C  CRITICAL_TTC"])  # False in a frame is not read as unknown

    def test_e_predicted_provenance_never_shows_as_text(self):
        run = run_of((1.0, "A", "CRITICAL_TTC_START", "B", {"predicted": True, "provenance": "PREDICTED"}),
                     (1.0, "A", "CLOSING_START", "B", {"measured": False}))
        lines = texts(run, 2.0)
        self.assertEqual(lines, ["A -> B  CRITICAL_TTC", "A -> B  CLOSING"])
        self.assertFalse(any("PREDICTED" in line.upper() for line in lines))

    def test_f_a_state_disappears_when_its_end_has_passed(self):
        run = run_of((1.0, "A", "BRAKE_START", None), (2.0, "A", "BRAKE_END", None))
        self.assertEqual(texts(run, 0.5), [])
        self.assertEqual(texts(run, 1.0), ["A  BRAKE"])  # from its START...
        self.assertEqual(texts(run, 1.99), ["A  BRAKE"])
        self.assertEqual(texts(run, 2.0), [])  # ...until its END
        self.assertEqual(texts(run, 2.5), [])

    def test_priority_contact_conflict_control_manoeuvre_other(self):
        run = run_of((1.0, "B", "CLOSING_START", "U1"), (1.0, "B", "TURN_RIGHT_START", None),
                     (1.0, "C", "THROTTLE_START", None), (1.0, "A", "BRAKE_START", None),
                     (1.0, "B", "CRITICAL_TTC_START", "C"), (1.0, "A", "EGO_PATH_ENTRY", "U2"))
        self.assertEqual(texts(run, 2.0), ["B -> C   CRITICAL_TTC", "A        BRAKE", "C        THROTTLE",
                                           "B        TURN_RIGHT", "A -> U2  IN_EGO_PATH", "B -> U1  CLOSING"])

    def test_instantaneous_events_are_not_states(self):
        run = run_of((1.0, "A", "COLLISION", None), (1.0, "A", "TRACK_APPEARED_FRONT", "U1"))
        self.assertEqual(active_states_at(run, 1.0), [])

    def test_an_end_without_start_counts_from_the_latest_appearance_only(self):
        # A road user seen in two segments; the second was first seen inside the ego path and leaves it at 9.
        run = run_of((0.1, "A", "TRACK_APPEARED_LEFT", "U3"), (3.0, "A", "TRACK_LOST", "U3"),
                     (6.0, "A", "TRACK_APPEARED_FRONT", "U3"), (9.0, "A", "EGO_PATH_EXIT", "U3"))
        self.assertEqual(texts(run, 1.0), [])  # never asserted for the first segment
        self.assertEqual(texts(run, 7.0), ["A -> U3  IN_EGO_PATH"])
        self.assertEqual(texts(run, 9.5), [])

    def test_one_road_user_seen_through_two_tracks_is_one_line(self):
        run = run_of((1.0, "A", "CLOSING_START", "track_001"), (1.5, "A", "CLOSING_START", "track_002"))
        run.road_users = {("A", "track_001"): "U1", ("A", "track_002"): "U1"}
        self.assertEqual(texts(run, 2.0), ["A -> U1  CLOSING"])


class CanonicalRunTests(unittest.TestCase):
    """The HUD list on the committed reconstructions (read-only)."""

    RUNS = ("traces/S11/run_0_consequential", "traces/S13/run_0_platoon", "traces/S14/run_0_surrounded",
            "traces/S15/run_0_dense_platoon", "traces/S19/run_0_collision_ambiguity")

    def test_dense_runs_show_active_states_within_the_limit_and_follow_the_intervals(self):
        root = Path(__file__).resolve().parents[1]
        for name in self.RUNS:
            run = ReplayRun.load(root / name)
            busiest = 0
            for k in range(int(run.duration / 0.1) + 1):
                t = k * 0.1
                states = active_states_at(run, t)
                lines = active_state_lines(states)
                busiest = max(busiest, len(states))
                self.assertLessEqual(len(lines), MAX_ACTIVE_LINES + 1, (name, t))
                self.assertEqual(len(lines), min(len(states), MAX_ACTIVE_LINES) + (len(states) > MAX_ACTIVE_LINES))
                self.assertFalse(any("?" in text or "PREDICTED" in text for text, _ in lines), (name, t))
                for actor, subject, state in states:  # every shown state lies inside one of its intervals
                    self.assertTrue(any(i.active_at(t) for i in run.display_intervals(actor)), (name, t, state))
            self.assertGreater(busiest, 0, name)


if __name__ == "__main__":
    unittest.main()
