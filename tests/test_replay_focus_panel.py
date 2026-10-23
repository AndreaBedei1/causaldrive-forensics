"""The focused recorder panel of the replay viewer (F): event windowing and wrapping that never lose an event, the
S04 collisions in the histories of every participant, and the panels drawn headless at 1280x720 (pygame with the
dummy video driver; no CARLA)."""

import os
import unittest
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src.cdf.replay.model import ReplayRun
from src.cdf.replay.presentation import HELP_LINES, MAX_EVENT_LINES, event_window, recorder_panel, wrap_text

ROOT = Path(__file__).resolve().parents[1]
# S04 a_front_pushed: A-B at 0.0, B-C at 0.5, and A touching B again at 0.65, a recontact of the A-B collision
# (RECONTACT in A's panel; B's sensor reports the B-C contact and the recontact as one, its collision with C).
S04 = {"run_0_a_front_pushed": {"A": [0.0], "B": [0.0, 0.5], "C": [0.5]},
       "run_0_b_rear_first": {"A": [0.0], "B": [-1.55, 0.0], "C": [-1.55]}}


def _viewer():
    import importlib.util
    spec = importlib.util.spec_from_file_location("focus_viewer", str(ROOT / "scripts/replay_run.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EventWindowTests(unittest.TestCase):
    def pages(self, rows, room, step=1):
        """Every event index shown while scrolling from the newest to the oldest."""
        seen, scroll = set(), 0
        for _ in range(len(rows) + 2):
            start, end, scroll = event_window(rows, room, scroll)
            self.assertLess(start, end)
            self.assertLessEqual(end - start, MAX_EVENT_LINES)
            seen.update(range(start, end))
            scroll += step
        return seen

    def test_all_shown_when_they_fit(self):
        self.assertEqual(event_window([1] * 5, 10, 0), (0, 5, 0))
        self.assertEqual(event_window([1] * 5, 10, 7), (0, 5, 0))  # no scrolling without need
        self.assertEqual(event_window([], 10, 3), (0, 0, 0))

    def test_at_most_fifteen_at_once_and_every_event_reachable(self):
        rows = [1] * 40
        self.assertEqual(event_window(rows, 100, 0), (0, MAX_EVENT_LINES, 0))
        self.assertEqual(self.pages(rows, 100, step=3), set(range(40)))

    def test_short_room_wrapped_events_never_lost_or_cut(self):
        rows = [1, 3, 2, 1, 4, 1, 2, 2]
        for room in (1, 2, 4, 6, 9):
            self.assertEqual(self.pages(rows, room), set(range(len(rows))))
            for scroll in range(10):
                start, end, _ = event_window(rows, room, scroll)
                if end - start > 1:  # several events only when they all fit with the hint row
                    self.assertLessEqual(sum(rows[start:end]), room - 1)

    def test_scroll_clamped_to_the_last_full_page(self):
        start, end, scroll = event_window([1] * 20, 6, 99)
        self.assertEqual((start, end, scroll), (15, 20, 15))


class WrapTests(unittest.TestCase):
    def test_long_event_label_wraps_within_the_width_keeping_every_word(self):
        text = "-12.3 s  EGO_PATH_ENTRY → track_004 (B) (by own lateral motion and something longer still)"
        pieces = wrap_text(text, len, 30)
        self.assertGreater(len(pieces), 1)
        self.assertTrue(all(len(p) <= 30 for p in pieces))
        self.assertEqual(" ".join(p.strip() for p in pieces).split(), text.split())

    def test_unbreakable_word_split_by_characters(self):
        pieces = wrap_text("x" * 50, len, 20)
        self.assertTrue(all(len(p) <= 20 for p in pieces))
        self.assertEqual("".join(p.strip() for p in pieces), "x" * 50)


class S04CollisionHistoryTests(unittest.TestCase):
    """Every recording participant's panel lists its own collisions at the right global times."""

    def test_collisions_in_every_participant_history(self):
        for variant, expected in S04.items():
            run = ReplayRun.load(ROOT / "traces/S04" / variant)
            for actor, times in expected.items():
                collisions = [e for e in run.display_events() if e.actor == actor and e.event_type == "COLLISION"]
                self.assertEqual([round(run.display_time(e.time), 2) for e in collisions], times, (variant, actor))
                end = run.duration
                panel = recorder_panel(run, actor, end, 10 ** 6)
                texts = [text for text, _ in panel.events if "COLLISION" in text]
                self.assertEqual(len(texts), len(times), (variant, actor))
                self.assertEqual(len(panel.events), panel.events_total)


class _Font:
    """A pygame font that remembers the text of every surface it rendered."""

    def __init__(self, font, texts):
        self.font, self.texts = font, texts

    def render(self, text, antialias, color):
        surface = self.font.render(text, antialias, color)
        self.texts[id(surface)] = (text, surface)
        return surface

    def size(self, text):
        return self.font.size(text)

    def get_linesize(self):
        return self.font.get_linesize()


class FocusLayoutTests(unittest.TestCase):
    """``_draw_side_panels`` on a 1280x720 surface, normal and focused."""

    @classmethod
    def setUpClass(cls):
        import pygame
        pygame.init()
        cls.pygame, cls.viewer = pygame, _viewer()

    def app(self, variant, selected, focus, run_dir=None):
        pg, texts, blits = self.pygame, {}, []

        class Screen(pg.Surface):
            def blit(self, source, dest, *args, **kwargs):
                if id(source) in texts:
                    blits.append((texts[id(source)][0], tuple(dest)[:2], source.get_size()))
                return pg.Surface.blit(self, source, dest, *args, **kwargs)

        app = object.__new__(self.viewer.ReplayApp)
        mono = "consolas,dejavusansmono,couriernew,monospace"
        app.pygame, app.width, app.height = pg, 1280, 720
        app.screen = Screen((1280, 720), pg.SRCALPHA)
        app.font_small = _Font(pg.font.SysFont(mono, 13), texts)
        app.font_bold = _Font(pg.font.SysFont(mono, 15, bold=True), texts)
        app.run = ReplayRun.load(ROOT / (run_dir or "traces/S04/" + variant))
        app.ids = [p.participant_id for p in app.run.participants]
        app.colors = {pid: (200, 100, 50) for pid in app.ids}
        app.selected, app.focus, app.event_scroll, app.show_help, app.occupied = selected, focus, 0, True, []
        app.peer = None  # a standalone viewer (no viewer side by side)
        return app, blits

    def draw(self, app, blits, t):
        del blits[:]
        app._draw_side_panels(t, {})
        return list(blits)

    def test_focus_gives_the_selected_recorder_the_column_and_every_event(self):
        for variant in S04:
            for selected in ("A", "B", "C"):
                app, blits = self.app(variant, selected, True)
                t = app.run.duration
                total = recorder_panel(app.run, selected, t, 10 ** 6).events_total
                bottom = app._bottom_bar_top()
                seen, headers = set(), []
                for _ in range(total + 2):
                    shown = self.draw(app, blits, t)
                    for text, (x, y), (w, h) in shown:
                        self.assertLessEqual(y + h, bottom, text)  # nothing under the help lines and timeline
                        self.assertGreaterEqual(x, 1280 - 8 - self.viewer.FOCUS_PANEL_WIDTH)
                        self.assertLessEqual(x + w, 1280 - 8, text)  # wrapped inside the panel
                    headers += [text.split()[0] for text, _, _ in shown if "m/s" in text]
                    seen.update(text for text, _, _ in shown if text[:1] in "+-" and " s  " in text)
                    app.event_scroll += 3
                self.assertEqual(set(headers), {"A", "B", "C"})  # the others kept as headers
                self.assertEqual(len(seen), total, (variant, selected))
                collisions = [text for text in seen if "COLLISION" in text]
                self.assertEqual(len(collisions), len(S04[variant][selected]), (variant, selected))

    def test_long_history_scrolls_through_every_event(self):
        app, blits = self.app(None, "A", True, "traces/S16/run_0_overtaking")
        t = app.run.duration
        total = recorder_panel(app.run, "A", t, 10 ** 6).events_total
        self.assertGreater(total, MAX_EVENT_LINES)
        seen, hints = set(), []
        for _ in range(total):
            shown = self.draw(app, blits, t)
            events = [text for text, _, _ in shown if text[:1] in "+-" and " s  " in text]
            self.assertLessEqual(len(events), MAX_EVENT_LINES)
            seen.update(events)
            hints += [text for text, _, _ in shown if text.startswith("PgUp older")]
            app.event_scroll += 3
        self.assertEqual(len(seen), total)
        self.assertTrue(hints and hints[-1].endswith("of {0}".format(total)))

    def test_others_collapsed_in_focus_and_restored_without_it(self):
        app, blits = self.app("run_0_a_front_pushed", "B", True)
        t = app.run.duration
        sections = [text for text, _, _ in self.draw(app, blits, t) if text.startswith("recent events")]
        self.assertEqual(len(sections), 1)  # only B's panel has a body
        self.assertIn("2 collisions", sections[0])
        app.focus = False
        sections = [text for text, _, _ in self.draw(app, blits, t) if text.startswith("recent events")]
        self.assertEqual(len(sections), 3)

    def test_collision_banner_keeps_every_pair_clear_of_the_focused_panel(self):
        for variant, t in (("run_0_a_front_pushed", 5.6), ("run_0_b_rear_first", 6.4)):
            app, blits = self.app(variant, "B", True)
            app.font_banner = _Font(self.pygame.font.SysFont("arial,dejavusans", 34, bold=True), {})
            app.font_banner.texts = app.font_small.texts
            app.hud_rect = (8, 8, 415, 85)
            self.draw(app, blits, t)
            del blits[:]
            app._draw_collision_banner(t)
            pieces = [(text, x, w) for text, (x, _), (w, _) in blits]
            self.assertTrue(pieces)
            expected = ["-".join(m.participants) for m in app.run.collisions_near(t, self.viewer.COLLISION_WINDOW_S)]
            shown = " ".join(text for text, _, _ in pieces).replace("–", "-").split()
            self.assertEqual(shown, ["COLLISION"] + expected)  # every pair, repeated contacts too
            for text, x, w in pieces:
                self.assertLessEqual(x + w, app.panel_left, text)
                self.assertGreaterEqual(x, 8 + 415, text)

    def test_keys_f_toggles_and_tab_shows_the_new_recorder_newest_events(self):
        pg = SimpleNamespace(K_ESCAPE=1, K_SPACE=2, K_r=3, K_LEFT=4, K_RIGHT=5, K_KP1=6, K_KP2=7, K_KP3=8, K_KP4=9,
                             K_1=10, K_2=11, K_3=12, K_4=13, K_c=14, K_TAB=15, K_n=16, K_p=17, K_t=18, K_g=19,
                             K_h=20, K_f=21, K_PAGEUP=22, K_PAGEDOWN=23, KMOD_SHIFT=1)
        app = object.__new__(self.viewer.ReplayApp)
        app.pygame, app.ids, app.selected, app.focus, app.event_scroll = pg, ["A", "B", "C"], "A", False, 0
        app._on_key(pg.K_f, 0)
        self.assertTrue(app.focus)
        app._on_key(pg.K_PAGEUP, 0)
        self.assertEqual(app.event_scroll, 3)
        app._on_key(pg.K_TAB, 0)
        self.assertEqual((app.selected, app.event_scroll, app.focus), ("B", 0, True))
        app._on_key(pg.K_f, 0)
        self.assertFalse(app.focus)

    def test_help_names_the_focus_key(self):
        text = " ".join(HELP_LINES)
        self.assertIn("F focus", text)
        self.assertIn("PgUp/PgDn", text)


if __name__ == "__main__":
    unittest.main()
