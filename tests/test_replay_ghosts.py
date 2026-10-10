"""Replay viewer: anonymous radar tracks drawn as ghosts, from what the reconstruction knows only.

The viewer shows the reconstruction, not the simulator: it never reads ground
truth, the scenario configuration, the run's own metadata or the privileged
evaluation, replays no road user that recorded nothing and never names one.
"""

import ast
import importlib.util
import json
import math
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.config import SemanticsConfig
from src.cdf.reconstruction.conflict import _Prediction
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, TrackSample
from src.cdf.replay.model import (ANONYMOUS, ASSOCIATED, BOX_EDGES, HEADING_FROM_VELOCITY, HEADING_HELD,
                                  HEADING_UNKNOWN, GhostGeometry, Pose, ReplayRun, Trajectory, box_corners,
                                  choose_map, load_tracks, nominal_box_centre, project_segment, track_heading,
                                  wrap_deg)

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"
S16 = ROOT / "traces" / "S16" / "run_0_consequential"
VIEWER_SOURCES = (ROOT / "scripts" / "replay_run.py", ROOT / "src" / "cdf" / "replay" / "model.py")
RECONSTRUCTION_FILES = ("local_graph.json", "local_tracks.jsonl", "local_trace.jsonl")
GLOBAL_FILES = ("global_graph.json", "associations.json", "alignment.json")
FOOTPRINT = EgoFootprint(-2.0, 2.0, -1.0, 1.0)


# --------------------------------------------------------------------------
# Every file the code under test opens or lists, by any route (an audit hook)
# --------------------------------------------------------------------------

_SEEN = []
_ACTIVE = [False]


def _audit(event, args):
    if not _ACTIVE[0] or event not in ("open", "os.listdir", "os.scandir") or not args:
        return
    try:
        if isinstance(args[0], (str, bytes, os.PathLike)):
            _SEEN.append((event, os.path.normcase(os.path.abspath(os.fsdecode(os.fspath(args[0]))))))
    except Exception:  # an audit hook must never break the audited call
        pass


sys.addaudithook(_audit)


class _Reads:
    def __enter__(self):
        del _SEEN[:]
        _ACTIVE[0] = True
        return self

    def __exit__(self, *exc):
        _ACTIVE[0] = False

    def under(self, folder):
        """(event, path) of everything seen inside ``folder``."""
        prefix = os.path.normcase(os.path.abspath(str(folder))) + os.sep
        return [(event, path) for event, path in _SEEN if path.startswith(prefix)]


def _norm(path):
    return os.path.normcase(os.path.abspath(str(path)))


def _viewer_inputs(run_dir, recorders):
    """The files the viewer may read in a run: the recorders' own files and the reconstruction outputs."""
    files = set()
    for recorder in recorders:
        files |= {run_dir / "vehicles" / recorder / name for name in ("ego.jsonl", "metadata.json")}
        files |= {run_dir / "reconstruction" / recorder / name for name in RECONSTRUCTION_FILES}
    return files | {run_dir / "reconstruction" / "global" / name for name in GLOBAL_FILES}


def _copy_inputs(source, target, recorders):
    for path in _viewer_inputs(source, recorders):
        if path.exists():
            destination = target / path.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(path), str(destination))
    return target


def _write(path, data, lines=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row) for row in data) + "\n" if lines else json.dumps(data)
    path.write_text(text, encoding="utf-8")


def _poison(run_dir):
    """Privileged material a viewer must not use, all of it deliberately false: a third vehicle C in ground
    truth with simulator actor ids and positions, a false map, false triggers / counterfactuals / contacts,
    the scenario's participants in the run metadata, a scenario file, an evaluation that names the anonymous
    tracks and associates them, and a vehicle folder without a recording of its own."""
    third = [{"participant_id": "C", "actor_id": 777, "timestamp": 12.9 + 0.05 * k,
              "transform": {"x": -20.0 - k, "y": -207.0, "z": 0.3, "yaw_deg": 180.0}} for k in range(200)]
    _write(run_dir / "ground_truth" / "states.jsonl", third, lines=True)
    _write(run_dir / "ground_truth" / "metadata.json",
           {"map": "Town03", "participants": [{"participant_id": p, "record": p != "C"} for p in "ABC"]})
    _write(run_dir / "ground_truth" / "triggers.jsonl",
           [{"participant_id": "A", "action_id": "fake_action", "trigger": {"target": "C"}, "t_scenario": 1.0}],
           lines=True)
    _write(run_dir / "ground_truth" / "counterfactuals.json", {"factual": {"collisions": {"A-C": {"first_s": 2.0}}}})
    _write(run_dir / "ground_truth" / "collisions.jsonl",
           [{"participant_id": "A", "other_actor_id": 777, "timestamp": 14.0, "impulse": 9999.0}], lines=True)
    _write(run_dir / "metadata.json", {"scenario_id": "S17", "variant": "crash", "map": "Town03",
                                       "participants": ["A", "B", "C"]})
    (run_dir / "s17_unobserved_causal_vehicle.yaml").write_text("scenario:\n  scenario_id: S17\n  map: Town03\n",
                                                                encoding="utf-8")
    _write(run_dir / "reconstruction" / "evaluation" / "identity.json",
           {"A:track_001": "C", "B:track_002": "C"})
    _write(run_dir / "reconstruction" / "evaluation" / "evaluation.json",
           {"tracks": [{"track": "A:track_001", "true_identity": "C", "verdict": "C"}],
            "associations": [{"local_graph": "A", "local_track": "track_001", "global_entity": "C",
                              "status": "ASSOCIATED"}]})
    _write(run_dir / "vehicles" / "C" / "metadata.json", {"blueprint": "vehicle.nissan.patrol", "participant_id": "C"})


def _summary(run):
    """Everything the viewer shows: recorders and their poses, tracks and ghosts, events, collisions,
    perceived states, the clock and the notes."""
    tracks = [(t.name, t.status, t.entity, t.ghost, t.label,
               [(s.time, round(s.centre[0], 6), round(s.centre[1], 6), round(s.yaw, 6), s.heading, s.measured)
                for s in t.samples]) for t in run.all_tracks()]
    poses = [(p.participant_id, p.blueprint, p.blueprint_source,
              [tuple(round(v, 6) for v in (pose.x, pose.y, pose.z, pose.yaw))
               for pose in (p.trajectory.pose_at(run.start + 0.5 * k) for k in range(int(run.duration / 0.5) + 1))])
             for p in run.participants]
    perceived = {pid: (states.times, states.states) for pid, states in run.perceived.items()}
    return (poses, tracks, [(e.time, e.actor, e.event_type, e.subject) for e in run.all_events()],
            [(m.time, m.participants) for m in run.collisions], perceived, run.identities,
            (run.clock, run.start, run.duration, run.clock_origins), run.notes)


def _code_constants_and_names(path):
    """String constants (docstrings excluded) and identifiers of a source file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body \
                and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
            docstrings.add(id(node.body[0].value))
    constants, names = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
            constants.append(node.value)
        elif isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, ast.Attribute):
            names.append(node.attr)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.extend(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom):
                names.append(node.module or "")
    return tree, constants, names


def _load_viewer_script():
    spec = importlib.util.spec_from_file_location("replay_run_under_test", str(ROOT / "scripts" / "replay_run.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _FakeCarla:
    """Just enough of the CARLA client API for the map recognition: a map's driving lanes are
    rectangles (x0, y0, x1, y1) listed in its 'OpenDRIVE' text."""

    class Location:
        def __init__(self, x=0.0, y=0.0, z=0.0):
            self.x, self.y, self.z = x, y, z

    class LaneType:
        Driving = "Driving"

    class Map:
        def __init__(self, name, text):
            self.name, self.lanes = name, json.loads(text)

        def get_waypoint(self, location, project_to_road=True, lane_type=None):
            assert project_to_road is False and lane_type == "Driving"
            inside = any(x0 <= location.x <= x1 and y0 <= location.y <= y1 for x0, y0, x1, y1 in self.lanes)
            return object() if inside else None


def _synthetic_run(root):
    """Recorder A driving from x = 0 to x = 20 at y = 0; nothing reconstructed."""
    run = root / "S99" / "run_0"
    _write(run / "vehicles" / "A" / "ego.jsonl",
           [{"timestamp": 0.05 * k, "x": 0.5 * k, "y": 0.0, "z": 0.1, "yaw_deg": 0.0} for k in range(41)], lines=True)
    return run


# --------------------------------------------------------------------------
# The boundary: no privileged input, by construction and in practice
# --------------------------------------------------------------------------

class NoPrivilegedInputTests(unittest.TestCase):
    def test_viewer_source_names_no_privileged_input(self):
        for path in VIEWER_SOURCES:
            tree, constants, names = _code_constants_and_names(path)
            for value in constants:
                for forbidden in ("ground_truth", "evaluation", "scenarios", "states.jsonl", "triggers",
                                  "counterfactual", "actor_id"):
                    self.assertNotIn(forbidden, value, "{0}: {1!r}".format(path.name, value))
                # Keys of privileged metadata: the true map, the scenario, who recorded and who did not.
                self.assertNotIn(value, ("map", "scenario_id", "variant", "record"), path.name)
            for name in names:
                for forbidden in ("ground_truth", "evaluation", "scenario_base", "ScenarioSpec", "scenario_setup",
                                  "find_scenario_file", "scenario_id", "oracle"):
                    self.assertNotIn(forbidden, name, "{0}: {1}".format(path.name, name))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", "")) \
                        == "load_run_config":
                    # configs/default.yaml only (the simulator connection): no scenario argument.
                    self.assertEqual((node.args, node.keywords), ([], []), path.name)
                if isinstance(node, ast.BinOp) and isinstance(node.right, ast.Constant) \
                        and node.right.value == "metadata.json":
                    # Only a recorder's own metadata (blueprint, footprint), never the run's.
                    self.assertIn("vehicles_dir", ast.dump(node.left), path.name)
            self.assertEqual(sum(value == "metadata.json" for value in constants),
                             sum(1 for node in ast.walk(tree) if isinstance(node, ast.BinOp)
                                 and isinstance(node.right, ast.Constant) and node.right.value == "metadata.json"),
                             path.name)

    @unittest.skipUnless((S17 / "reconstruction").exists(), "S17 trace not present")
    def test_loading_s17_reads_only_the_recorders_and_the_reconstruction(self):
        self.assertTrue((S17 / "ground_truth").exists())  # the privileged files are right there
        with _Reads() as reads:
            run = ReplayRun.load(S17)
        allowed = {_norm(path) for path in _viewer_inputs(S17, [p.participant_id for p in run.participants])}
        seen = reads.under(S17)
        self.assertTrue(seen)
        for event, path in seen:
            if event == "open":
                self.assertIn(path, allowed)
            else:
                self.assertEqual(path, _norm(S17 / "vehicles"))  # the only folder listed: who recorded
        for event, path in reads.under(ROOT):
            for forbidden in ("ground_truth", "evaluation", os.sep + "scenarios" + os.sep, os.sep + "llm" + os.sep):
                self.assertNotIn(forbidden, path)
        self.assertIn(_norm(S17 / "reconstruction" / "global" / "associations.json"), {p for _, p in seen})

    @unittest.skipUnless((S16 / "reconstruction").exists(), "S16 trace not present")
    def test_loading_s16_reads_only_the_recorders_and_the_reconstruction(self):
        with _Reads() as reads:
            run = ReplayRun.load(S16)
        self.assertEqual([p.participant_id for p in run.participants], ["A", "B", "C"])  # three recorders
        allowed = {_norm(path) for path in _viewer_inputs(S16, ["A", "B", "C"])}
        seen = reads.under(S16)
        self.assertTrue(seen)
        for event, path in seen:
            if event == "open":
                self.assertIn(path, allowed)
            else:
                self.assertEqual(path, _norm(S16 / "vehicles"))
        for event, path in reads.under(ROOT):
            for forbidden in ("ground_truth", "evaluation", os.sep + "scenarios" + os.sep, os.sep + "llm" + os.sep):
                self.assertNotIn(forbidden, path)

    @unittest.skipUnless((S17 / "reconstruction").exists(), "S17 trace not present")
    def test_privileged_files_change_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            clean = _copy_inputs(S17, Path(tmp) / "clean" / "S17" / "run_0_crash", "AB")
            poisoned = _copy_inputs(S17, Path(tmp) / "poisoned" / "S17" / "run_0_crash", "AB")
            _poison(poisoned)
            with _Reads() as reads:
                with_privileged = ReplayRun.load(poisoned)
            without = ReplayRun.load(clean)
            opened = [path for event, path in reads.under(poisoned) if event == "open"]
        self.assertEqual(_summary(with_privileged), _summary(without))
        self.assertEqual([p.participant_id for p in with_privileged.participants], ["A", "B"])
        self.assertEqual(with_privileged.clock, "t_global")
        for path in opened:
            self.assertNotIn("ground_truth", path)
            self.assertNotIn("evaluation", path)
            self.assertNotEqual(path, _norm(poisoned / "metadata.json"))
            self.assertFalse(path.endswith(".yaml"), path)
            self.assertNotIn(_norm(poisoned / "vehicles" / "C"), path)
        self.assertEqual(set(opened), {_norm(path) for path in _viewer_inputs(poisoned, "AB")})

    def test_the_map_is_recognised_from_recorded_positions_and_public_map_files_only(self):
        viewer = _load_viewer_script()
        viewer.import_carla = lambda: _FakeCarla
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _synthetic_run(Path(tmp))
            _poison(run_dir)  # ground truth says Town03: never read
            run = viewer.ReplayRun.load(run_dir)
            maps = Path(tmp) / "carla" / viewer.OPENDRIVE_DIR
            maps.mkdir(parents=True)
            road = json.dumps([[-5.0, -2.0, 25.0, 2.0]])
            (maps / "Town05.xodr").write_text(road, encoding="utf-8")
            (maps / "Town05_Opt.xodr").write_text(road, encoding="utf-8")  # the same road network
            (maps / "Town03.xodr").write_text(json.dumps([[-5.0, -2.0, 10.0, 2.0]]), encoding="utf-8")
            with _Reads() as reads:
                chosen = viewer.resolve_map(run, Path(tmp) / "carla", current=None)
                kept = viewer.resolve_map(run, Path(tmp) / "carla", current="Town05_Opt")
            self.assertEqual((chosen, kept), ("Town05", "Town05_Opt"))
            self.assertEqual(reads.under(run_dir), [])  # positions come from the loaded recordings
            opened = [path for event, path in reads.under(Path(tmp) / "carla") if event == "open"]
            self.assertTrue(opened)
            self.assertTrue(all(path.endswith(".xodr") for path in opened))
            # Without local map files only the server's current map can be checked.
            self.assertEqual(viewer.resolve_map(run, None, "Town05", _FakeCarla.Map("Town05", road)), "Town05")
            self.assertIsNone(viewer.resolve_map(run, None, "Town10HD", _FakeCarla.Map("Town10HD", "[]")))

    def test_only_the_recorders_are_cycled_and_ghosts_start_on(self):
        viewer = _load_viewer_script()
        viewer.import_carla = lambda: _FakeCarla
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _synthetic_run(Path(tmp))
            _poison(run_dir)
            run = viewer.ReplayRun.load(run_dir)
            app = viewer.ReplayApp(run, "Town05", None, None, viewer.parse_args([str(run_dir)]))
            dots = viewer.ReplayApp(run, "Town05", None, None, viewer.parse_args([str(run_dir), "--track-dots"]))
        self.assertEqual(app.ids, ["A"])
        self.assertTrue(app.show_ghosts and app.show_tracks)
        self.assertFalse(dots.show_ghosts)


# --------------------------------------------------------------------------
# S17: two anonymous tracks of one unrecorded road user, never merged, never named
# --------------------------------------------------------------------------

@unittest.skipUnless((S17 / "reconstruction" / "global" / "associations.json").exists(), "S17 trace not present")
class S17GhostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replay = ReplayRun.load(S17)
        cls.tracks = {track.name: track for track in cls.replay.all_tracks()}

    def test_the_replay_runs_on_the_reconstructions_global_time(self):
        self.assertEqual(self.replay.clock, "t_global")
        graph = json.loads((S17 / "reconstruction" / "global" / "global_graph.json").read_text(encoding="utf-8"))
        t_global = {obs["local_node"]: node["t_global"] for node in graph["nodes"]
                    for obs in node.get("observations") or []}
        events = self.replay.all_events()
        self.assertTrue(events)
        for event in events:
            self.assertAlmostEqual(self.replay.display_time(event.time), t_global[event.node_id], places=6)
        self.assertEqual([(self.replay.display_time(m.time), m.participants) for m in self.replay.collisions],
                         [(0.0, ("A", "B"))])
        critical = next(e for e in events if e.event_type == "CRITICAL_TTC_START" and e.subject == "track_001"
                        and e.actor == "A")
        self.assertAlmostEqual(self.replay.display_time(critical.time), -2.35, places=6)

    def test_the_tracks_are_shown_as_the_fusion_decided(self):
        self.assertEqual({name: (t.status, t.entity, t.ghost) for name, t in self.tracks.items()},
                         {"A:track_001": (ANONYMOUS, None, True), "A:track_002": (ASSOCIATED, "B", False),
                          "B:track_001": (ASSOCIATED, "A", False), "B:track_002": (ANONYMOUS, None, True),
                          "B:track_003": (ANONYMOUS, None, True)})
        # An associated track is the associated recorder's replayed vehicle: no duplicate ghost.
        self.assertEqual([track.name for track in self.replay.ghost_tracks()],
                         ["A:track_001", "B:track_002", "B:track_003"])
        self.assertEqual([self.tracks[name].label for name in sorted(self.tracks)],
                         ["A:track_001 / ANONYMOUS", "A:track_002 → B", "B:track_001 → A", "B:track_002 / ANONYMOUS",
                          "B:track_003 / ANONYMOUS"])

    def test_only_the_recorders_are_replayed_and_nothing_is_named_c(self):
        self.assertEqual([p.participant_id for p in self.replay.participants], ["A", "B"])
        standalone_c = re.compile(r"(^|[^A-Za-z0-9_])C([^A-Za-z0-9_]|$)")
        texts = [t.name for t in self.replay.all_tracks()] + [t.label for t in self.replay.all_tracks()]
        texts += [self.replay.subject_name(t.recorder, t.track_id) for t in self.replay.all_tracks()]
        for t in (1.0, 4.0, 7.0):
            for recorder in ("A", "B"):
                texts += [track.name for track, _ in self.replay.anonymous_at(recorder, t)]
                texts += self.replay.perceived_lines(recorder, t) or []
        for text in texts:
            self.assertIsNone(standalone_c.search(text), text)

    def test_ghosts_are_renderable_while_tracked_and_gone_at_track_lost(self):
        size = self.replay.geometry
        for name in ("A:track_001", "B:track_002", "B:track_003"):
            track = self.tracks[name]
            lost = [e.time for e in self.replay.local_events[track.recorder].events
                    if e.event_type == "TRACK_LOST" and e.subject == track.track_id]
            self.assertEqual(len(lost), 1, name)
            self.assertLessEqual(track.end, lost[0])
            for t in (track.start, track.start + 0.37, (track.start + track.end) / 2.0, track.end):
                state = track.state_at(t)
                self.assertIsNotNone(state, (name, t))
                corners = box_corners(state.centre, state.yaw, size.length, size.width, 0.0, size.height)
                self.assertTrue(all(math.isfinite(value) for corner in corners for value in corner))
                self.assertEqual(state.heading, HEADING_FROM_VELOCITY)  # moving all along: heading known
            self.assertIsNone(track.state_at(track.end + 0.04), name)  # never continued past its last sample
            self.assertIsNone(track.state_at(lost[0] + 0.01), name)
        self.assertEqual((size.length, size.width, size.height), (4.6, 1.9, 1.5))

    def test_ghost_heading_follows_the_estimated_motion(self):
        observer = self.replay.participant("A")
        for t in (0.5, 1.0, 1.5, 2.0):  # driving alongside, the same way as A
            state = self.tracks["A:track_001"].state_at(t)
            yaw = observer.trajectory.pose_at(self.replay.start + t).yaw
            self.assertLess(abs(wrap_deg(state.yaw - yaw)), 15.0)

    def test_predicted_samples_are_marked(self):
        track = self.tracks["A:track_001"]
        predicted = [sample for sample in track.samples if not sample.measured]
        self.assertTrue(predicted)
        self.assertFalse(track.state_at(predicted[0].time).measured)

    def test_the_anonymous_tracks_stay_separate_each_in_its_observers_frame(self):
        a1 = self.tracks["A:track_001"]
        for other in (self.tracks["B:track_002"], self.tracks["B:track_003"]):
            self.assertIsNot(a1, other)
            self.assertEqual((a1.recorder, other.recorder), ("A", "B"))
            # Each went through its own observer's recorded pose and its own view of the road user (A
            # sees its rear, B partly behind A its left side): the two nominal boxes land on the same
            # road user, overlapping, without ever being compared or merged.
            common = [t for t in a1.times if other.start <= t <= other.end]
            self.assertTrue(common)
            distances = [math.hypot(a1.state_at(t).centre[0] - other.state_at(t).centre[0],
                                    a1.state_at(t).centre[1] - other.state_at(t).centre[1]) for t in common]
            self.assertLess(max(distances), self.replay.geometry.length)


# --------------------------------------------------------------------------
# Ghost geometry, heading and interpolation
# --------------------------------------------------------------------------

def _row(t, x, y, vx, vy, measured=True, vel_std=0.3, surface_offset=0.0):
    """A local_tracks.jsonl row of a stationary recorder (its vehicle frame = its local frame)."""
    return {"track_id": "track_001", "t_local": t, "x_m": x, "y_m": y, "vx_mps": vx, "vy_mps": vy,
            "vel_std_mps": vel_std, "measured": measured, "longitudinal_m": x, "lateral_m": y,
            "surface_offset_m": surface_offset}


class GhostModelTests(unittest.TestCase):
    def _tracks(self, rows, statuses=None, yaw=90.0):
        """The rows seen by a recorder standing at (100, 50) facing ``yaw``."""
        trajectory = Trajectory.from_records([{"timestamp": 10.0 + 0.05 * k, "x": 100.0, "y": 50.0, "z": 0.0,
                                               "yaw_deg": yaw} for k in range(61)])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "local_tracks.jsonl"
            _write(path, rows, lines=True)
            return load_tracks(path, "A", trajectory, Pose(100.0, 50.0, 0.0, yaw), 10.0, 10.0, FOOTPRINT,
                               GhostGeometry(), statuses)

    def test_box_lies_behind_the_observed_near_surface(self):
        # Ahead, moving away or towards: the box extends away from the recorder.
        self.assertEqual(tuple(round(v, 6) for v in nominal_box_centre(10.0, 0.0, 0.0, 0.0, FOOTPRINT, 4.6, 1.9)),
                         (12.3, 0.0))
        self.assertEqual(tuple(round(v, 6) for v in nominal_box_centre(10.0, 0.0, 0.0, 180.0, FOOTPRINT, 4.6, 1.9)),
                         (12.3, 0.0))
        # Beside it (left), its near side 0.2 m in front of the tracked point.
        self.assertEqual(tuple(round(v, 6) for v in nominal_box_centre(0.0, -2.0, 0.2, 0.0, FOOTPRINT, 4.6, 1.9)),
                         (0.0, -2.75))

    def test_box_placement_mirrors_the_critical_ttc_model(self):
        cfg = SemanticsConfig()
        own = EgoState(t_local=0.0, x=0.0, y=0.0, heading=0.0, vx=10.0, vy=0.0)
        for lon, lat, vx, vy, offset in ((10.0, 0.5, 8.0, 0.0, 0.2), (-8.0, -0.3, 12.0, 0.0, 0.1),
                                         (3.0, -3.0, 10.0, -2.0, 0.3), (1.0, 4.0, -10.0, 1.0, 0.0),
                                         (15.0, 6.0, 0.3, 0.2, 0.1), (2.5, 1.5, 6.0, 6.0, 0.4)):
            sample = TrackSample(t_local=0.0, x_m=lon, y_m=lat, vx_mps=vx, vy_mps=vy, speed_mps=math.hypot(vx, vy),
                                 pos_std_m=0.1, vel_std_mps=0.3, range_m=math.hypot(lon, lat), bearing_deg=0.0,
                                 longitudinal_m=lon, lateral_m=lat, closing_speed_mps=0.0, closing_ttc_s=None,
                                 measured=True, n_returns=10, surface_offset_m=offset)
            prediction = _Prediction(sample, own, FOOTPRINT, cfg)
            centre = nominal_box_centre(lon, lat, offset, math.degrees(prediction.target_angle), FOOTPRINT,
                                        cfg.target_length_m, cfg.target_width_m)
            self.assertAlmostEqual(centre[0], float(prediction.target_centre[0]), places=9)
            self.assertAlmostEqual(centre[1], float(prediction.target_centre[1]), places=9)

    def test_heading_needs_a_speed_that_fixes_it(self):
        self.assertAlmostEqual(track_heading(10.0, 0.0, 0.3), 0.0)
        self.assertAlmostEqual(track_heading(0.0, -5.0, 0.3), -90.0)
        self.assertIsNone(track_heading(0.6, 0.0, 0.1))  # below HEADING_MIN_SPEED_MPS
        self.assertIsNone(track_heading(1.2, 0.0, 0.7))  # within twice its own uncertainty

    def test_each_sample_goes_through_its_observers_recorded_pose(self):
        (track,) = self._tracks([_row(0.0, 10.0, 0.0, 10.0, 0.0), _row(0.1, 11.0, 0.0, 10.0, 0.0)])
        state = track.state_at(0.0)
        self.assertEqual(tuple(round(v, 6) for v in state.position), (100.0, 60.0))  # 10 m ahead of a car facing +y
        self.assertEqual(tuple(round(v, 6) for v in state.centre), (100.0, 62.3))  # its box beyond the near surface
        self.assertAlmostEqual(state.yaw, 90.0)
        self.assertEqual(state.heading, HEADING_FROM_VELOCITY)

    def test_an_uncertain_heading_is_held_or_left_unknown_never_invented(self):
        (moving,) = self._tracks([_row(0.0, 10.0, 0.0, 0.0, -8.0), _row(0.1, 10.0, -0.8, 0.4, 0.1),
                                  _row(0.2, 10.0, -0.8, 0.0, 0.0)])
        self.assertEqual([(s.heading, round(s.yaw, 6)) for s in moving.samples],
                         [(HEADING_FROM_VELOCITY, 0.0), (HEADING_HELD, 0.0), (HEADING_HELD, 0.0)])
        (standing,) = self._tracks([_row(0.0, 10.0, 0.0, 0.0, 0.0), _row(0.1, 10.0, 0.0, 0.5, 0.0)])
        self.assertEqual([(s.heading, round(s.yaw, 6)) for s in standing.samples],
                         [(HEADING_UNKNOWN, 90.0), (HEADING_UNKNOWN, 90.0)])  # parallel to the recorder

    def test_interpolation_stays_inside_one_track_and_its_gaps(self):
        (track,) = self._tracks([_row(0.0, 10.0, 0.0, 10.0, 0.0), _row(0.1, 11.0, 0.0, 10.0, 0.0, measured=False),
                                 _row(0.8, 18.0, 0.0, 10.0, 0.0)])
        self.assertAlmostEqual(track.state_at(0.05).position[1], 60.5)  # 30 fps between 10 Hz samples
        self.assertTrue(track.state_at(0.05).measured)
        self.assertFalse(track.state_at(0.1).measured)  # PREDICTED
        self.assertIsNone(track.state_at(0.45))  # 0.7 s without samples: more than max_track_gap_s
        self.assertIsNotNone(track.state_at(0.8))
        self.assertIsNone(track.state_at(-0.01))  # nothing before the first sample...
        self.assertIsNone(track.state_at(0.81))  # ...or after the last (its TRACK_LOST)

    def test_a_track_is_a_ghost_unless_the_fusion_associated_it(self):
        (anonymous,) = self._tracks([_row(0.0, 10.0, 0.0, 10.0, 0.0)])
        (associated,) = self._tracks([_row(0.0, 10.0, 0.0, 10.0, 0.0)], {("A", "track_001"): (ASSOCIATED, "B")})
        self.assertEqual((anonymous.ghost, anonymous.label), (True, "A:track_001 / ANONYMOUS"))
        self.assertEqual((associated.ghost, associated.label), (False, "A:track_001 → B"))

    def test_box_corners_and_edges(self):
        corners = box_corners((0.0, 0.0), 90.0, 4.0, 2.0, 1.0, 1.5)
        self.assertEqual(len(corners), 8)
        self.assertEqual(len(BOX_EDGES), 12)
        self.assertEqual(tuple(round(v, 6) for v in corners[0]), (1.0, 2.0, 1.0))  # front-left of a car facing +y
        lengths = sorted(round(math.dist(corners[i], corners[j]), 6) for i, j in BOX_EDGES)
        self.assertEqual(lengths, [1.5] * 4 + [2.0] * 4 + [4.0] * 4)

    def test_segments_are_clipped_at_the_camera_near_plane(self):
        camera = Pose(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        (u0, _), (u1, v1) = project_segment((-5.0, 5.0, 0.0), (10.0, 5.0, 0.0), camera, 90.0, 800, 600)
        self.assertGreater(u0, 800.0)  # the part just in front of the camera, far to the right
        self.assertAlmostEqual(u1, 600.0)
        self.assertAlmostEqual(v1, 300.0)
        self.assertIsNone(project_segment((-5.0, 1.0, 0.0), (-1.0, 1.0, 0.0), camera, 90.0, 800, 600))


class MapChoiceTests(unittest.TestCase):
    NETWORKS = {"Town05": "n5", "Town05_Opt": "n5", "Town03": "n3", "Town03_Opt": "n3", "Town01": "n1"}

    def test_the_map_carrying_every_recorded_position_wins(self):
        fits = {"Town05": 1.0, "Town05_Opt": 1.0, "Town03": 0.27, "Town03_Opt": 0.27, "Town01": 0.908}
        self.assertEqual(choose_map(fits, self.NETWORKS), "Town05")
        self.assertEqual(choose_map(fits, self.NETWORKS, current="Town05_Opt"), "Town05_Opt")  # no reload
        self.assertEqual(choose_map(fits, self.NETWORKS, current="Town03"), "Town05")

    def test_no_guess_when_unfit_or_ambiguous(self):
        self.assertIsNone(choose_map({"Town05": 0.9, "Town03": 0.2}, self.NETWORKS))
        self.assertIsNone(choose_map({"Town05": 1.0, "Town01": 0.97}, self.NETWORKS))
        self.assertIsNone(choose_map({"Town05": 1.0, "Town03": 1.0}, self.NETWORKS))
        self.assertIsNone(choose_map({}, {}))


if __name__ == "__main__":
    unittest.main()
