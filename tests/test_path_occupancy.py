"""EGO_PATH occupancy with uncertainty (local.path_occupancy) and the temporally consistent reference path
(road.ReferencePath: lane graph, sequence-level map matching, one chain per lane episode)."""

import math
import unittest

import numpy as np

from src.cdf.common.opendrive import LanePiece
from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.local import path_occupancy
from src.cdf.reconstruction.road import LaneGraph, ReferencePath

CFG = SemanticsConfig()
DT = 0.05


def times(n):
    return [round(DT * k, 4) for k in range(n)]


class OccupancyTests(unittest.TestCase):
    def test_noise_on_the_boundary_makes_no_transition(self):
        # A body whose edge stays within one sigma of the corridor boundary, alternating sides every sweep.
        margins = [0.2 if k % 2 else -0.2 for k in range(80)]
        spans, initial = path_occupancy(times(80), margins, [0.5] * 80, CFG)
        self.assertEqual(spans, [])
        self.assertIsNone(initial)

    def test_one_definite_sweep_is_no_state_change(self):
        margins = [-2.0] * 20 + [2.0] + [-2.0] * 20
        spans, initial = path_occupancy(times(41), margins, [0.3] * 41, CFG)
        self.assertEqual(spans, [])
        self.assertIs(initial, False)

    def test_entry_is_dated_at_the_boundary_crossing_not_at_certainty(self):
        # Outside, then the edge moves in at 1 m/s: it crosses the boundary at sample 20, is certain later.
        margins = [-2.0 + 0.05 * max(k - 0, 0) for k in range(80)]
        spans, initial = path_occupancy(times(80), margins, [0.3] * 80, CFG)
        self.assertIs(initial, False)
        self.assertEqual(len(spans), 1)
        start, end = spans[0]
        self.assertEqual(start, next(k for k, m in enumerate(margins) if m > 0.0))
        self.assertIsNone(end)

    def test_inside_at_first_observation_invents_no_entry(self):
        spans, initial = path_occupancy(times(30), [1.5] * 30, [0.3] * 30, CFG)
        self.assertIs(initial, True)
        self.assertEqual(spans, [(0, None)])

    def test_missing_evidence_is_no_exit(self):
        # Inside, then only predicted samples (None) until the track is lost: still inside, never an exit.
        margins = [1.5] * 20 + [None] * 20
        spans, _ = path_occupancy(times(40), margins, [0.3] * 40, CFG)
        self.assertEqual(spans, [(0, None)])

    def test_a_real_exit_is_kept(self):
        margins = [1.5] * 20 + [1.5 - 0.1 * k for k in range(1, 40)]
        spans, _ = path_occupancy(times(59), margins, [0.3] * 59, CFG)
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0][1], next(k for k, m in enumerate(margins) if m is not None and m <= 0.0))


def straight_piece(key, y, x0, x1, heading=0.0):
    xs = np.arange(x0, x1 + 1e-9, 1.0)
    return LanePiece(key, tuple((float(x), y) for x in xs), tuple(heading for _ in xs), tuple(3.5 for _ in xs), "-1")


def turn_piece(key, start, radius, sign, length=20.0):
    """A quarter-circle-ish connector from ``start`` heading +x, turning right (sign +1, CARLA +y) or left."""
    pts, heads = [], []
    for k in range(int(length) + 1):
        a = k / radius
        pts.append((start[0] + radius * math.sin(a), start[1] + sign * radius * (1.0 - math.cos(a))))
        heads.append(sign * a)
    return LanePiece(key, tuple(pts), tuple(heads), tuple(3.5 for _ in pts), "1")


class ReferencePathTests(unittest.TestCase):
    def graph(self):
        approach = straight_piece(("1", 0, -1), 0.0, 0.0, 50.0)
        approach_left = straight_piece(("1", 0, -2), -3.5, 0.0, 50.0)
        straight = straight_piece(("2", 0, -1), 0.0, 50.0, 120.0)
        right_turn = turn_piece(("3", 0, -1), (50.0, 0.0), 15.0, 1.0)
        return LaneGraph([approach, approach_left, straight, right_turn])

    def reference(self, graph, ys, xs=None, headings=None):
        xs = np.arange(0.0, 45.0, 0.5) if xs is None else xs
        ys = np.full(len(xs), ys) if np.isscalar(ys) else ys
        headings = np.zeros(len(xs)) if headings is None else headings
        return ReferencePath(graph, np.arange(len(xs)) * DT, np.column_stack([xs, ys]), headings)

    def test_one_path_per_lane_episode(self):
        ref = self.reference(self.graph(), 0.0)
        self.assertIs(ref.path(0), ref.path(len(ref.match) - 1))
        self.assertEqual({ref.lane_at(k) for k in range(len(ref.match))}, {("1", 0, -1)})

    def test_at_a_junction_the_branch_the_recorder_takes_later(self):
        graph = self.graph()
        # Straight through: the path continues straight.
        ref = self.reference(graph, 0.0, np.arange(0.0, 90.0, 0.5))
        end = ref.path(0).points[-1]
        self.assertAlmostEqual(end[1], 0.0, places=6)
        # Turning right after the junction: the path at the approach already follows the right turn.
        xs = list(np.arange(0.0, 50.0, 0.5))
        pts = [(x, 0.0) for x in xs] + [graph.points[3][k] for k in range(1, 21)]
        heads = [0.0] * len(xs) + [graph.pieces[3].headings[k] for k in range(1, 21)]
        ref = ReferencePath(graph, np.arange(len(pts)) * DT, np.array(pts), np.array(heads))
        self.assertGreater(float(ref.path(0).points[-1][1]), 5.0)

    def test_a_lane_change_of_the_recorder_switches_lane_once(self):
        xs = np.arange(0.0, 45.0, 0.5)
        ys = np.clip((xs - 15.0) / 10.0, 0.0, 1.0) * -3.5  # from lane -1 to lane -2 between x = 15 and 25
        ref = self.reference(self.graph(), ys, xs)
        lanes = [ref.lane_at(k) for k in range(len(xs))]
        switches = [k for k in range(1, len(lanes)) if lanes[k] != lanes[k - 1]]
        self.assertEqual(len(switches), 1)
        self.assertEqual((lanes[0], lanes[-1]), (("1", 0, -1), ("1", 0, -2)))


if __name__ == "__main__":
    unittest.main()
