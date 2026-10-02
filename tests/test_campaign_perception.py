"""Checks on the recorded campaign (traces/): what the three radars, the camera and the reconstruction
make of the real CARLA runs.

Ground truth (``ground_truth/``) is read here only to validate, as the evaluation does.  Every test
is skipped when its run is not present.
"""

import json
import math
import unittest
from pathlib import Path

import numpy as np

from src.cdf.recording.compact_observations import load_radar_observations
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.local import read_jsonl, reconstruct_vehicle
from src.cdf.reconstruction.pipeline import read_incident_context

ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "traces"


def run_dir(name):
    path = TRACES / name
    if not (path / "vehicles").exists():
        raise unittest.SkipTest(name + " not present")
    return path


def _rotation(yaw, pitch, roll):
    """Columns: forward, right, up of a CARLA rotation (degrees), world frame."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    return np.array([[cp * cy, cy * sp * sr - sy * cr, -(cy * sp * cr + sy * sr)],
                     [cp * sy, sy * sp * sr + cy * cr, cy * sr - sy * sp * cr],
                     [sp, -cp * sr, cp * cr]])


class Box:
    """A vehicle's true oriented box (ground truth), centre at mid height."""

    def __init__(self, state):
        tf, ext = state["transform"], state["bbox_extent"]
        self.rot = _rotation(tf["yaw_deg"], tf["pitch_deg"], tf["roll_deg"])
        self.extent = np.array([ext["x"], ext["y"], ext["z"]])
        self.centre = np.array([tf["x"], tf["y"], tf["z"]]) + self.rot @ np.array([0.0, 0.0, ext["z"]])

    def local(self, points):
        return (np.atleast_2d(points) - self.centre) @ self.rot

    def contains(self, points, margin):
        return np.all(np.abs(self.local(points)) <= self.extent + margin, axis=1)


class ThreeRadarLayoutTests(unittest.TestCase):
    def test_every_recorder_carries_front_left_right_radars_on_its_body(self):
        runs = sorted(TRACES.glob("S*/run_*"))
        if not runs:
            self.skipTest("no recorded runs")
        for run in runs:
            for vehicle in sorted((run / "vehicles").iterdir()):
                meta = json.loads((vehicle / "metadata.json").read_text())
                fp = meta["ego_footprint"]
                mounts = {r["sensor_id"]: r["sensor_transform"] for r in meta["radar"]}
                self.assertEqual(sorted(mounts), ["front", "left", "right"], (run, vehicle.name))
                self.assertGreater(mounts["front"]["x"], fp["x_max_m"])
                self.assertLess(mounts["left"]["y"], fp["y_min_m"])
                self.assertGreater(mounts["right"]["y"], fp["y_max_m"])
                self.assertEqual({sid: m["yaw_deg"] for sid, m in mounts.items()},
                                 {"front": 0.0, "left": -90.0, "right": 90.0})


class OcclusionTests(unittest.TestCase):
    """S07: A behind B behind C in one lane.  A's radars see B; C, hidden behind B, is never tracked."""

    @classmethod
    def setUpClass(cls):
        cls.run_path = run_dir("S07/run_0_crash")
        cls.states = {}
        for state in read_jsonl(cls.run_path / "ground_truth" / "states.jsonl"):
            cls.states.setdefault(int(state["frame"]), {})[state["participant_id"]] = state

    def test_a_tracks_b_and_never_c(self):
        local = reconstruct_vehicle(self.run_path / "vehicles" / "A", ReconstructionConfig(),
                                    context=read_incident_context(self.run_path))
        ego = read_jsonl(self.run_path / "vehicles" / "A" / "ego.jsonl")
        origin = float(ego[0]["timestamp"])
        first = ego[0]
        yaw = math.radians(first["yaw_deg"])
        on = {"B": 0, "C": 0}
        for track in local.tracks:
            for sample in track.samples:
                if not sample.measured:
                    continue
                stamp = origin + sample.t_local
                frame = min(self.states, key=lambda f: abs(self.states[f]["A"]["timestamp"] - stamp))
                world = np.array([first["x"] + math.cos(yaw) * sample.x_m - math.sin(yaw) * sample.y_m,
                                  first["y"] + math.sin(yaw) * sample.x_m + math.cos(yaw) * sample.y_m])
                for target in on:
                    box = Box(self.states[frame][target])
                    point = np.array([world[0], world[1], box.centre[2]])
                    if box.contains(point, 1.5)[0]:
                        on[target] += 1
        self.assertEqual(len(local.tracks), 1)
        self.assertGreater(on["B"], 100)
        self.assertEqual(on["C"], 0)

    def test_no_return_reaches_c_over_or_through_b(self):
        # Returns on C's body (0.3 m above the road or more) whose ray crosses B's box: only
        # under B's floor (ray below 0.25 m there), or from a radar pressed against B at the impact.
        over_or_through, under, total = 0, 0, 0
        for observations in load_radar_observations(self.run_path / "vehicles" / "A"):
            mount = observations.metadata["sensor_transform"]
            pos = np.array([mount["x"], mount["y"], mount["z"]])
            rot = _rotation(mount["yaw_deg"], mount.get("pitch_deg", 0.0), 0.0)
            for index, frame in enumerate(observations.frames):
                world = self.states.get(int(frame))
                if not world:
                    continue
                own = world["A"]["transform"]
                own_rot = _rotation(own["yaw_deg"], own["pitch_deg"], own["roll_deg"])
                sensor = np.array([own["x"], own["y"], own["z"]]) + own_rot @ pos
                box_b, box_c = Box(world["B"]), Box(world["C"])
                if box_b.contains(sensor, 0.1)[0]:
                    continue  # the bumper radar is against B (impact): no line of sight to speak of
                rows = np.asarray(observations.frame_detections(index), dtype=float).reshape(-1, 4)
                if not len(rows):
                    continue
                depth, az, alt = rows[:, 0], rows[:, 1], rows[:, 2]
                los = np.column_stack([np.cos(alt) * np.cos(az), np.cos(alt) * np.sin(az), np.sin(alt)]) @ (own_rot @ rot).T
                points = sensor + los * depth[:, None]
                body = box_c.contains(points, 0.2) & (points[:, 2] - world["C"]["transform"]["z"] >= 0.3)
                for point in points[body]:
                    total += 1
                    start, end = box_b.local(sensor)[0], box_b.local(point)[0]
                    f = (-box_b.extent[0] - start[0]) / (end[0] - start[0])  # B's rear face plane
                    crossing = start + f * (end - start)
                    if abs(crossing[1]) > box_b.extent[1]:
                        continue  # beside B
                    if crossing[2] < -box_b.extent[2] + 0.25:
                        under += 1
                    else:
                        over_or_through += 1
        self.assertEqual(over_or_through, 0)
        self.assertLessEqual(total, 10)


class SignTests(unittest.TestCase):
    def signs(self, run, vehicle):
        return read_jsonl(run_dir(run) / "vehicles" / vehicle / "traffic_signs.jsonl")

    def test_real_stop_signs_are_detected_and_relevant(self):
        for run, vehicle in (("S10/run_0_rolls_through", "A"), ("S12/run_0_near_simultaneous", "A"),
                             ("S12/run_0_near_simultaneous", "B"), ("S15/run_0_deflected_into_c", "B")):
            stops = [s for s in self.signs(run, vehicle) if s["class"] == "STOP" and s["relevant_to_ego_path"]]
            self.assertEqual(len(stops), 1, (run, vehicle))
            self.assertGreaterEqual(stops[0]["n_detections"], 10, (run, vehicle))

    def test_s15_has_no_phantom_stop_after_the_collision(self):
        self.assertEqual(self.signs("S15/run_0_deflected_into_c", "A"), [])

    def test_road_marking_stops_are_not_signs(self):
        # S03 / S08: the junction's "STOP" is painted on the road only.
        for run in ("S03/run_0_crash", "S08/run_0_crash"):
            for vehicle in sorted((run_dir(run) / "vehicles").iterdir()):
                self.assertEqual(self.signs(run, vehicle.name), [], (run, vehicle.name))


class ScenarioTimingTests(unittest.TestCase):
    def local(self, run, vehicle):
        path = run_dir(run)
        return reconstruct_vehicle(path / "vehicles" / vehicle, ReconstructionConfig(),
                                   context=read_incident_context(path))

    def test_s12_stops_last_about_one_and_a_half_seconds_then_both_pull_away(self):
        ends = []
        for vehicle in ("A", "B"):
            nodes = self.local("S12/run_0_near_simultaneous", vehicle).graph.nodes
            start = next(n.t_local for n in nodes if n.event_type == "STOP_START")
            end = next(n.t_local for n in nodes if n.event_type == "STOP_END")
            self.assertTrue(1.0 <= end - start <= 2.0, (vehicle, start, end))
            restart = [n.t_local for n in nodes if n.event_type == "THROTTLE_START" and start < n.t_local <= end]
            self.assertEqual(len(restart), 1, vehicle)  # the accelerator pressed to pull away
            ends.append(end)
        self.assertLessEqual(abs(ends[0] - ends[1]), 0.3)

    def test_s09_approach_before_the_first_critical_situation(self):
        first = min(n.t_local for vehicle in ("A", "B")
                    for n in self.local("S09/run_0_merge_conflict", vehicle).graph.nodes
                    if n.event_type == "CRITICAL_TTC_START")
        self.assertGreaterEqual(first, 5.0)

    def test_s16_c_drives_in_the_next_lane_until_the_second_collision(self):
        run = run_dir("S16/run_0_consequential")
        ego = read_jsonl(run / "vehicles" / "C" / "ego.jsonl")
        collisions = read_jsonl(run / "vehicles" / "C" / "collisions.jsonl")
        first = min(float(c["timestamp"]) for c in collisions)
        speeds = [math.hypot(r["velocity"]["x"], r["velocity"]["y"]) for r in ego if float(r["timestamp"]) < first]
        self.assertTrue(all(7.0 <= v <= 10.0 for v in speeds), (min(speeds), max(speeds)))
        scenario = (ROOT / "configs" / "scenarios" / "s16_secondary_collision.yaml").read_text(encoding="utf-8")
        self.assertNotIn("deflect", scenario.split("participants:")[1])


if __name__ == "__main__":
    unittest.main()
