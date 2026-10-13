"""Standard replay interface: global-subject panels, event priority, no UNKNOWN '?' or PREDICTED text, the
C-key camera cycle over the recorders.  Headless (no CARLA, no pygame)."""

import unittest
from pathlib import Path
from types import SimpleNamespace

from src.cdf.replay.model import ReplayRun
from src.cdf.replay.presentation import (EVENT, MAX_PANEL_LINES, MORE, camera_cycle, event_line, next_camera,
                                         standard_panel_lines, subject_label)

ROOT = Path(__file__).resolve().parents[1]


class _Perceived:
    def __init__(self, snapshot):
        self.snapshot = snapshot

    def state_at(self, t):
        return self.snapshot


def stub_run(events, snapshot, road_users=None, identities=None):
    return SimpleNamespace(
        recent_events=lambda actor, t, window: [e for e in events if e.actor == actor],
        perceived={"A": _Perceived(snapshot)}, road_users=road_users or {}, identities=identities or {},
        active_states=lambda actor, t: [])


def event(kind, subject=None, actor="A"):
    return SimpleNamespace(actor=actor, event_type=kind, subject=subject)


SNAPSHOT = {"ego": {"MOVING": True, "BRAKE": True, "TURN_LEFT": "UNKNOWN"},
            "external": {"track_001": {"CLOSING": True, "CRITICAL_TTC": True, "IN_EGO_PATH": "UNKNOWN"},
                         "track_002": {"CRITICAL_TTC": True, "IN_EGO_PATH": True},
                         "track_003": {"CRITICAL_TTC": "UNKNOWN", "CUT_IN_FROM_LEFT": "UNKNOWN"},
                         "track_004": {"IN_EGO_PATH": True}}}


class PanelTests(unittest.TestCase):
    def setUp(self):
        # Two local tracks of one fused road user U1, one of recorder B, one unknown-only track.
        self.run = stub_run([event("TRACK_APPEARED_FRONT", "track_004"), event("CRITICAL_TTC_START", "track_001")],
                            SNAPSHOT, road_users={("A", "track_001"): "U1", ("A", "track_002"): "U1"},
                            identities={("A", "track_004"): "B"})

    def test_events_first_newest_first_with_global_subjects(self):
        lines = standard_panel_lines(self.run, "A", 1.0, 1.0)
        self.assertEqual(lines[0], ("» CRITICAL_TTC_START → U1", EVENT))
        self.assertEqual(lines[1], ("» TRACK_APPEARED_FRONT → B", EVENT))

    def test_one_line_per_global_subject_and_no_unknown(self):
        texts = [text for text, _ in standard_panel_lines(self.run, "A", 1.0, 1.0)]
        self.assertEqual(texts[2:], ["U1: CRITICAL_TTC, IN_EGO_PATH", "B: IN_EGO_PATH", "ego: BRAKE"])
        self.assertFalse(any("?" in text or "UNKNOWN" in text or "track_00" in text for text in texts))

    def test_cap_with_more_and_events_never_pushed_out(self):
        many = stub_run([event("TRACK_APPEARED_LEFT", "t{0}".format(k)) for k in range(3)],
                        {"ego": {"BRAKE": True}, "external": {"x{0}".format(k): {"CRITICAL_TTC": True} for k in range(12)}})
        lines = standard_panel_lines(many, "A", 1.0, 1.0, max_lines=6)
        self.assertEqual(len(lines), 6)
        self.assertEqual([kind for _, kind in lines[:3]], [EVENT] * 3)
        self.assertEqual(lines[-1], ("... +11 more", MORE))

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
    """Every 0.1 s of the canonical runs: the standard panels stay clean and keep every recent event."""

    RUNS = ("traces/S11/run_0_consequential", "traces/S13/run_0_abreast", "traces/S13/run_0_passing",
            "traces/S13/run_0_platoon")

    def test_panels(self):
        for path in self.RUNS:
            run = ReplayRun.load(ROOT / path)
            for k in range(int(run.duration / 0.1) + 1):
                t = k * 0.1
                for participant in run.participants:
                    pid = participant.participant_id
                    lines = standard_panel_lines(run, pid, t, 1.0)
                    texts = [text for text, _ in lines]
                    self.assertLessEqual(len(lines), MAX_PANEL_LINES, (path, t))
                    for text in texts:
                        self.assertNotIn("?", text, (path, t, text))
                        self.assertNotIn("PREDICTED", text, (path, t, text))
                        self.assertNotIn("anonymous tracks", text, (path, t, text))
                    subjects = [text.split(":")[0] for text, kind in lines if kind not in (EVENT, MORE)]
                    self.assertEqual(len(subjects), len(set(subjects)), (path, t, texts))
                    recent = {(e.event_type, subject_label(run, pid, e.subject)) for e in run.recent_events(pid, t, 1.0)}
                    if len(recent) < MAX_PANEL_LINES:  # every recent event is shown, whatever the states
                        self.assertEqual(sum(kind == EVENT for _, kind in lines), len(recent), (path, t, texts))

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

    def test_vehicle_panel_uses_the_standard_lines(self):
        self.app.run = ReplayRun.load(ROOT / "traces/S13/run_0_platoon")
        for t in (2.0, 6.0, 7.0, 8.0):
            for text, rgb, font in self.app._vehicle_lines("A", t):
                self.assertNotIn("?", text)
                self.assertNotIn("PREDICTED", text)
                self.assertNotIn("anonymous tracks", text)

    def test_c_key_cycles_every_recorder_then_free(self):
        pg = SimpleNamespace(K_ESCAPE=1, K_SPACE=2, K_r=3, K_LEFT=4, K_RIGHT=5, K_KP1=6, K_KP2=7, K_KP3=8, K_KP4=9,
                             K_1=10, K_2=11, K_3=12, K_4=13, K_c=14, K_TAB=15, K_n=16, K_p=17, K_t=18, K_g=19, K_h=20,
                             KMOD_SHIFT=1)
        app = self.app
        app.pygame, app.ids, app.selected, app.camera_mode = pg, ["A", "B", "C"], "A", "overview"
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
