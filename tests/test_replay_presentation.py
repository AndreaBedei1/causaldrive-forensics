import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

from src.cdf.replay.presentation import HELP_LINES, anonymous_row, subject_label


class CompactPresentationTests(unittest.TestCase):
    def test_anonymous_row_has_only_id_and_observers(self):
        self.assertEqual(anonymous_row('U1', ['B', 'A', 'A']), 'U1   seen by A,B')

    def test_subject_labels_do_not_expose_fusion_members(self):
        run = SimpleNamespace(road_users={('A', 'track_001'): 'U1'}, identities={('A', 'track_002'): 'B'})
        self.assertEqual(subject_label(run, 'A', 'track_001'), 'U1')
        self.assertEqual(subject_label(run, 'A', 'track_002'), 'B')
        self.assertEqual(subject_label(run, 'A', None), '')

    def test_help_is_short_and_keeps_the_requested_controls(self):
        text = ' '.join(HELP_LINES)
        for key in ('SPACE play/pause', '←/→ seek', 'N/P event', 'C camera', 'TAB vehicle',
                    'T tracks', 'G ghosts', 'H help', 'ESC quit'):
            self.assertIn(key, text)
        self.assertLess(max(map(len, HELP_LINES)), 90)

    def test_body_label_keeps_scientific_data_off_the_screen(self):
        path = Path(__file__).resolve().parents[1] / 'scripts/replay_run.py'
        spec = importlib.util.spec_from_file_location('compact_viewer', str(path))
        viewer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(viewer)
        app = object.__new__(viewer.ReplayApp)
        app.ids = ['A', 'B']
        app._line3d = lambda *args: None
        app._project = lambda *args: (10, 10)
        labels = []
        app._label = lambda anchor, lines, *args, **kwargs: labels.extend(lines)
        entity = SimpleNamespace(entity_id='U1', length=4.6)
        state = SimpleNamespace(measured=True, heading=viewer.HEADING_UNKNOWN, yaw=None, centre=(0, 0))
        corners = [(0, 0, 0)] * 8
        app._draw_road_user(entity, state, corners, 0)()
        self.assertEqual(labels, ['U1'])
