"""A recorder's replay panel (presentation.standard_panel_lines, the 848a645 layout) on a real ReplayRun: the
recorder's complete current perceived state, then its recent events; UNKNOWN and PREDICTED never shown; at
most 8 lines, then ``... +N more``."""

import unittest
from pathlib import Path

from src.cdf.replay.model import LocalEvents, PerceivedStates, ReplayEvent, ReplayRun, TrackPath, state_intervals
from src.cdf.replay.presentation import MAX_PANEL_LINES, MORE, standard_panel_lines


def run_of(frames, events=(), duration=10.0):
    """Recorder A with per-frame perceived states [(t, snapshot)] and events [(t, type, subject)]."""
    evs = [ReplayEvent(t, "A", kind, subject, "A:e{0:02d}".format(n)) for n, (t, kind, subject) in enumerate(events)]
    run = ReplayRun(run_dir=Path("."), name="synthetic", participants=[], start=0.0, duration=duration,
                    local_events={"A": LocalEvents("A", 0.0, evs, state_intervals(evs))})
    run.perceived = {"A": PerceivedStates([t for t, _ in frames], [snap for _, snap in frames])}
    return run


def frame(ego=None, **tracks):
    return {"ego": ego or {"MOVING": True}, "external": tracks}


def texts(run, t):
    return [text for text, _ in standard_panel_lines(run, "A", t, 1.0)]


class RecorderPanelTests(unittest.TestCase):
    def test_a_three_states_all_visible(self):
        run = run_of([(0.0, frame({"MOVING": True, "BRAKE": True}, track_001={"CRITICAL_TTC": True},
                                  track_002={"CLOSING": True}))])
        self.assertEqual(texts(run, 1.0), ["ego: MOVING, BRAKE", "track_001: CRITICAL_TTC", "track_002: CLOSING"])

    def test_b_eight_lines_all_visible_without_ellipsis(self):
        run = run_of([(0.0, frame(**{"track_{0:03d}".format(k): {"CLOSING": True} for k in range(1, 8)}))])
        lines = texts(run, 1.0)
        self.assertEqual(len(lines), MAX_PANEL_LINES)
        self.assertFalse(any(line.startswith("...") for line in lines))

    def test_c_eleven_lines_show_eight_and_the_count_of_the_rest(self):
        run = run_of([(0.0, frame(**{"track_{0:03d}".format(k): {"CLOSING": True} for k in range(1, 11)}))])
        lines = standard_panel_lines(run, "A", 1.0, 1.0)
        self.assertEqual(len(lines), MAX_PANEL_LINES + 1)
        self.assertEqual(lines[-1], ("... +3 more", MORE))

    def test_d_unknown_states_are_hidden(self):
        run = run_of([(0.0, frame({"MOVING": True, "TURN_LEFT": "UNKNOWN"},
                                  track_001={"CRITICAL_TTC": True, "IN_EGO_PATH": "UNKNOWN"},
                                  track_002={"CLOSING": "UNKNOWN", "CRITICAL_TTC": "UNKNOWN"}))])
        self.assertEqual(texts(run, 1.0), ["ego: MOVING", "track_001: CRITICAL_TTC"])
        self.assertFalse(any("?" in line or "UNKNOWN" in line for line in texts(run, 1.0)))

    def test_e_predicted_states_never_show_the_word(self):
        run = run_of([(0.0, frame())])
        track = TrackPath(recorder="A", track_id="track_009", samples=[])
        run.tracks = {"A": [track]}
        run.anonymous_at = lambda recorder, t: [(track, type("S", (), {"measured": False})())]
        lines = texts(run, 1.0)
        self.assertIn("anonymous tracks: A:track_009", lines)
        self.assertFalse(any("PREDICTED" in line for line in lines))

    def test_f_a_state_that_ended_is_no_longer_displayed(self):
        run = run_of([(0.0, frame(track_001={"CRITICAL_TTC": True})), (2.0, frame(track_001={"CRITICAL_TTC": False}))])
        self.assertEqual(texts(run, 1.0), ["ego: MOVING", "track_001: CRITICAL_TTC"])
        self.assertEqual(texts(run, 2.5), ["ego: MOVING"])  # a track holding no state has no line

    def test_the_current_state_is_listed_above_the_recent_events(self):
        run = run_of([(0.0, frame(track_001={"CRITICAL_TTC": True}))],
                     events=[(0.8, "TRACK_APPEARED_FRONT", "track_001"), (0.9, "CRITICAL_TTC_START", "track_001")])
        self.assertEqual(texts(run, 1.0), ["ego: MOVING", "track_001: CRITICAL_TTC",
                                           "» CRITICAL_TTC_START → track_001", "» TRACK_APPEARED_FRONT → track_001"])

    def test_an_end_without_start_counts_from_the_latest_appearance_only(self):
        # Pairing of a road user seen in two segments: the second, first seen inside the ego path, leaves it at 9.
        evs = [ReplayEvent(t, "A", kind, "U3", "A:e{0}".format(n)) for n, (t, kind) in enumerate(
            [(0.1, "TRACK_APPEARED_LEFT"), (3.0, "TRACK_LOST"), (6.0, "TRACK_APPEARED_FRONT"), (9.0, "EGO_PATH_EXIT")])]
        (interval,) = state_intervals(evs)
        self.assertEqual((interval.state, interval.start, interval.end), ("EGO_PATH", 6.0, 9.0))


if __name__ == "__main__":
    unittest.main()
