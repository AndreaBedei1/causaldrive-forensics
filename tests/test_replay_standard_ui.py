"""Standard replay interface: the recorder-centric panels of commit 848a645 (current perceived state first,
then the recorder's recent events) without UNKNOWN '?' or PREDICTED text and capped at 8 lines + '... +N more';
the C-key camera cycle over the recorders.  Headless (no CARLA, no pygame)."""

import unittest
from pathlib import Path
from types import SimpleNamespace

from src.cdf.replay.model import ReplayRun
from src.cdf.replay.presentation import (EVENT, MAX_EVENT_LINES, MAX_PANEL_LINES, MAX_STATE_LINES, MORE,
                                        camera_cycle, event_line, next_camera, recorder_panel,
                                         standard_panel_lines)

ROOT = Path(__file__).resolve().parents[1]


class _Perceived:
    def __init__(self, snapshot):
        self.snapshot = snapshot

    def state_at(self, t):
        return self.snapshot


def stub_run(events, snapshot, road_users=None, identities=None):
    road_users, identities = road_users or {}, identities or {}

    def subject_name(actor, track):
        entity = identities.get((actor, track)) or road_users.get((actor, track))
        return track if entity is None else "{0} ({1})".format(track, entity)
    return SimpleNamespace(
        recent_events=lambda actor, t, window: [e for e in events if e.actor == actor],
        perceived={"A": _Perceived(snapshot)}, road_users=road_users, identities=identities,
        subject_name=subject_name, active_states=lambda actor, t: [])


def event(kind, subject=None, actor="A"):
    return SimpleNamespace(actor=actor, event_type=kind, subject=subject)


SNAPSHOT = {"ego": {"MOVING": True, "BRAKE": True, "TURN_LEFT": "UNKNOWN"},
            "external": {"track_001": {"CLOSING": True, "CRITICAL_TTC": True, "IN_EGO_PATH": "UNKNOWN"},
                         "track_002": {"CRITICAL_TTC": True, "IN_EGO_PATH": True},
                         "track_003": {"CRITICAL_TTC": "UNKNOWN", "CUT_IN_FROM_LEFT": "UNKNOWN"},
                         "track_004": {"IN_EGO_PATH": True, "CLOSING": False}}}


class PanelTests(unittest.TestCase):
    def setUp(self):
        # Two local tracks of one fused road user U1, one of recorder B, one unknown-only (lost) track.
        self.run = stub_run([event("TRACK_APPEARED_FRONT", "track_004"), event("CRITICAL_TTC_START", "track_001")],
                            SNAPSHOT, road_users={("A", "track_001"): "U1", ("A", "track_002"): "U1"},
                            identities={("A", "track_004"): "B"})

    def test_current_perceived_state_first_then_the_recent_events_newest_first(self):
        texts = [text for text, _ in standard_panel_lines(self.run, "A", 1.0, 1.0)]
        self.assertEqual(texts, ["ego: MOVING, BRAKE",
                                 "track_001 (U1): CLOSING, CRITICAL_TTC",
                                 "track_002 (U1): CRITICAL_TTC, IN_EGO_PATH",
                                 "track_004 (B): IN_EGO_PATH",
                                 "» CRITICAL_TTC_START → U1",
                                 "» TRACK_APPEARED_FRONT → B"])

    def test_unknown_is_hidden_not_shown_as_false(self):
        texts = [text for text, _ in standard_panel_lines(self.run, "A", 1.0, 1.0)]
        self.assertFalse(any("?" in text or "UNKNOWN" in text for text in texts))
        self.assertFalse(any(text.startswith("track_003") for text in texts))  # only unknown: no line at all
        self.assertNotIn("TURN_LEFT", texts[0])

    def test_complete_list_then_eight_lines_and_the_count_of_the_rest(self):
        many = stub_run([event("TRACK_APPEARED_LEFT", "t{0}".format(k)) for k in range(3)],
                        {"ego": {"BRAKE": True}, "external": {"x{0:02d}".format(k): {"CRITICAL_TTC": True} for k in range(12)}})
        lines = standard_panel_lines(many, "A", 1.0, 1.0)
        self.assertEqual(len(lines), MAX_PANEL_LINES + 1)
        self.assertEqual(lines[0][0], "ego: BRAKE")  # the current state comes first
        self.assertEqual(lines[-1], ("... +8 more", MORE))  # 1 + 12 + 3 lines, 8 shown

    def test_a_full_panel_keeps_the_alerts_and_the_recent_events(self):
        many = stub_run([event("CRITICAL_TTC_START", "x00"), event("TRACK_APPEARED_LEFT", "x01")],
                        {"ego": {"MOVING": True},
                         "external": dict({"x{0:02d}".format(k): {"IN_EGO_PATH": True} for k in range(1, 12)},
                                          x00={"CRITICAL_TTC": True})})
        lines = standard_panel_lines(many, "A", 1.0, 1.0)
        texts = [text for text, _ in lines]
        self.assertEqual(len(lines), MAX_PANEL_LINES + 1)
        self.assertEqual(texts[0], "ego: MOVING")
        self.assertIn("x00: CRITICAL_TTC", texts)
        self.assertIn("» CRITICAL_TTC_START → x00", texts)
        self.assertIn("» TRACK_APPEARED_LEFT → x01", texts)
        self.assertEqual(lines[-1], ("... +7 more", MORE))  # 1 + 12 + 2 lines, 8 shown, in display order
        kinds = [kind for _, kind in lines[:-1]]
        self.assertEqual(kinds[kinds.index(EVENT):], [EVENT, EVENT])

    def test_hud_event_line_names_the_global_subject(self):
        self.assertEqual(event_line(self.run, event("CRITICAL_TTC_START", "track_002")), "A CRITICAL_TTC_START U1")


class CameraTests(unittest.TestCase):
    def test_c_cycles_overview_every_recorder_free(self):
        recorders = ["A", "B", "C"]
        state, seen = ("overview", None), []
        for _ in range(6):
            state = next_camera(recorders, *state)
            seen.append(state)
        self.assertEqual(seen, [("follow", "A"), ("follow", "B"), ("follow", "C"), ("free", None),
                                ("overview", None), ("follow", "A")])
        self.assertEqual(camera_cycle(["A", "B"]), [("overview", None), ("follow", "A"), ("follow", "B"), ("free", None)])

    def test_follow_with_a_tab_selected_vehicle_continues_from_it(self):
        self.assertEqual(next_camera(["A", "B", "C"], "follow", "B"), ("follow", "C"))
        self.assertEqual(next_camera(["A", "B"], "free", "B"), ("overview", None))


class RecordedRunPanelTests(unittest.TestCase):
    """Every 0.1 s of the canonical runs: state above events, no UNKNOWN or PREDICTED, 8 lines + '... +N more'."""

    RUNS = ("traces/S11/run_0_consequential", "traces/S13/run_0_abreast", "traces/S13/run_0_passing",
            "traces/S13/run_0_platoon", "traces/S14/run_0_surrounded")

    def test_panels(self):
        for path in self.RUNS:
            run = ReplayRun.load(ROOT / path)
            for k in range(int(run.duration / 0.1) + 1):
                t = k * 0.1
                for participant in run.participants:
                    pid = participant.participant_id
                    lines = standard_panel_lines(run, pid, t, 1.0)
                    texts = [text for text, _ in lines]
                    self.assertLessEqual(len(lines), MAX_PANEL_LINES + 1, (path, t))
                    if len(lines) == MAX_PANEL_LINES + 1:
                        self.assertEqual(lines[-1][1], MORE, (path, t))
                    for text in texts:
                        self.assertNotIn("?", text, (path, t, text))
                        self.assertNotIn("PREDICTED", text, (path, t, text))
                        self.assertNotIn("UNKNOWN", text, (path, t, text))
                    kinds = [kind for _, kind in lines if kind != MORE]
                    if EVENT in kinds:
                        self.assertEqual(set(kinds[kinds.index(EVENT):]), {EVENT}, (path, t, texts))
                    if lines and lines[-1][1] != MORE:  # untruncated: every recent event is listed
                        self.assertEqual(kinds.count(EVENT), len(run.recent_events(pid, t, 1.0)), (path, t, texts))


class RecorderPanelSectionsTests(unittest.TestCase):
    """The panel's two sections: current state (at most MAX_STATE_LINES, then '... +N more') and up to
    MAX_EVENT_LINES recent events, newest first, whatever their age: states never push the events out."""

    def test_states_cannot_hide_the_events(self):
        many = stub_run([event("TRACK_APPEARED_LEFT", "x{0:02d}".format(k)) for k in range(20)],
                        {"ego": {"MOVING": True},
                         "external": {"x{0:02d}".format(k): {"CRITICAL_TTC": True} for k in range(12)}})
        many.display_events = lambda: [SimpleNamespace(actor="A", time=0.1 * k, event_type="TRACK_APPEARED_LEFT",
                                                       subject="x{0:02d}".format(k), attributes={})
                                       for k in range(20)]
        panel = recorder_panel(many, "A", 5.0)
        self.assertEqual(len(panel.states), MAX_STATE_LINES + 1)
        self.assertEqual(panel.states[-1][1], MORE)
        self.assertEqual(len(panel.events), MAX_EVENT_LINES)
        self.assertEqual(panel.events_total, 20)
        self.assertIn("x19", panel.events[0][0])  # newest first
        self.assertIn("x05", panel.events[-1][0])

    def test_recorded_runs_newest_first_no_unknown(self):
        for path in ("traces/S11/run_0_consequential", "traces/S14/run_0_surrounded"):
            run = ReplayRun.load(ROOT / path)
            for k in range(0, int(run.duration / 0.5) + 1):
                t = 0.5 * k
                for participant in run.participants:
                    pid = participant.participant_id
                    panel = recorder_panel(run, pid, t)
                    history = [e for e in run.display_events() if e.actor == pid and e.time <= t + 1e-6]
                    self.assertEqual(len(panel.events), min(len(history), MAX_EVENT_LINES), (path, t, pid))
                    for (text, _), e in zip(panel.events, reversed(history)):
                        self.assertIn(e.event_type, text)
                    for text, _ in panel.states + panel.events:
                        for word in ("?", "UNKNOWN", "PREDICTED"):
                            self.assertNotIn(word, text, (path, t, text))
                    self.assertLessEqual(len(panel.states), MAX_STATE_LINES + 1)


class ClearanceLabelTests(unittest.TestCase):
    def test_tracks_carry_the_body_to_body_clearance_of_an_active_interaction(self):
        run = ReplayRun.load(ROOT / "traces/S02/run_0_crash")
        if not run.tracks.get("A"):
            self.skipTest("canonical trace not present")
        seen = 0
        for track in run.tracks["A"]:
            for k in range(int(run.duration / 0.1) + 1):
                t = k * 0.1
                state = track.state_at(t)
                states = ((run.perceived["A"].state_at(t) or {}).get("external") or {}).get(track.track_id) or {}
                if state is None or states.get("CRITICAL_TTC") is not True:
                    continue
                self.assertIsNotNone(state.clearance, t)
                self.assertGreaterEqual(state.clearance, -0.5, t)  # touching at most (box estimate)
                self.assertLess(state.clearance, 60.0, t)
                seen += 1
        self.assertGreater(seen, 0)


def _viewer():
    import importlib.util
    spec = importlib.util.spec_from_file_location("standard_viewer", str(ROOT / "scripts/replay_run.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ViewerTests(unittest.TestCase):
    """The interactive viewer's own methods, headless (no CARLA, no pygame window)."""

    def setUp(self):
        self.viewer = _viewer()
        self.app = object.__new__(self.viewer.ReplayApp)
        self.app.font_bold, self.app.font_small = "bold", "small"

    def test_vehicle_panel_shows_the_recorder_state_first(self):
        self.app.run = ReplayRun.load(ROOT / "traces/S13/run_0_platoon")
        for t in (2.0, 6.0, 7.0, 8.0):
            lines = self.app._vehicle_lines("A", t)
            self.assertTrue(lines)
            self.assertTrue(lines[0][0].startswith("ego: "))  # the recorder's current state first
            for text, rgb, font in lines:
                self.assertNotIn("?", text)
                self.assertNotIn("PREDICTED", text)

    def test_c_key_cycles_every_recorder_then_free(self):
        pg = SimpleNamespace(K_ESCAPE=1, K_SPACE=2, K_r=3, K_LEFT=4, K_RIGHT=5, K_KP1=6, K_KP2=7, K_KP3=8, K_KP4=9,
                             K_1=10, K_2=11, K_3=12, K_4=13, K_c=14, K_TAB=15, K_n=16, K_p=17, K_t=18, K_g=19, K_h=20,
                             KMOD_SHIFT=1)
        app = self.app
        app.pygame, app.ids, app.selected, app.camera_mode = pg, ["A", "B", "C"], "A", "overview"
        app.view_ids = app.ids  # standalone: the camera moves over every replayed vehicle
        app.camera_pose, app.free = None, None
        seen = []
        for _ in range(5):
            app._on_key(pg.K_c, 0)
            seen.append(app.camera_mode + (" " + app.selected if app.camera_mode == "follow" else ""))
        self.assertEqual(seen, ["follow A", "follow B", "follow C", "free", "overview"])

    def test_associated_dots_have_no_second_label_and_one_line_per_subject(self):
        app = self.app
        lines = []
        app.colors, app.associated_lines = {"A": (1, 2, 3)}, set()
        app._ground_z = lambda x, y, z: 0.0
        app._project = lambda point: (10, 10)
        app._line3d = lambda a, b, *args, **kwargs: lines.append((a, b))
        app.pygame = SimpleNamespace(draw=SimpleNamespace(circle=lambda *args, **kwargs: None))
        app.screen = None
        observer = SimpleNamespace(x=0.0, y=0.0, z=0.0)
        state = SimpleNamespace(position=(5.0, 0.0), measured=False)
        labels = []
        for track_id in ("track_001", "track_002"):  # two tracks of one recorder C
            track = SimpleNamespace(recorder="A", track_id=track_id, status=self.viewer.ASSOCIATED, entity="C",
                                    road_user=None, ghost=False)
            labels.append(app._draw_track_dot(track, state, observer, 0))
        self.assertEqual(labels, [None, None])
        self.assertEqual(len(lines), 1)


class NoGroundTruthTests(unittest.TestCase):
    def test_replay_and_standard_panels_need_no_ground_truth(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = ROOT / "traces/S15/run_0_dense_platoon", Path(tmp) / "S15" / "run_0_dense_platoon"
            for item in ("vehicles", "reconstruction"):
                shutil.copytree(src / item, dst / item)
            shutil.copy2(src / "metadata.json", dst / "metadata.json")
            self.assertFalse((dst / "ground_truth").exists())
            run = ReplayRun.load(dst)
            self.assertEqual(run.clock, "t_global")
            self.assertGreater(max(len(run.entities_at(k * 0.1)) for k in range(int(run.duration / 0.1))), 0)
            self.assertGreater(len(run.display_events()), 0)
            self.assertTrue(standard_panel_lines(run, "A", run.duration - 5.0, 1.0) is not None)


if __name__ == "__main__":
    unittest.main()
