"""The logical 360-degree surround radar: sensor layout, footprint clearance, ego motion, tracking across +-180."""

import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig, TrackingConfig
from src.cdf.reconstruction.local import appearance_side, track_events
from src.cdf.reconstruction.pipeline import reconstruct_run
from src.cdf.reconstruction.tracking import (EgoFootprint, EgoState, EgoTrajectory, RadarMount, build_local_tracks,
                                             radar_sweeps, sensor_velocity)
from src.cdf.recording.compact_observations import CompactObservations
from src.cdf.simulation.sensors import RadarSpec, radar_specs_from_config, rotate_detections

from synthetic_run import CONTACT_T, make_run

ROOT = Path(__file__).resolve().parents[1]
STEP = 0.05
CENTRE = RadarMount(x=0.0, y=0.0, z=1.8, yaw=0.0)
MODEL3 = EgoFootprint(back=-2.37, front=2.43, left=-1.08, right=1.08)


class SensorLayoutTests(unittest.TestCase):
    def test_carla_cannot_cover_180_degrees_with_one_radar(self):
        with self.assertRaises(ValueError):
            RadarSpec(horizontal_fov_deg=200.0, physical_radars=1).physical_layout()
        with self.assertRaises(ValueError):  # 4 x 80 deg leave gaps
            RadarSpec(horizontal_fov_deg=360.0, physical_radars=4, physical_horizontal_fov_deg=80.0).physical_layout()

    def test_six_overlapping_radars_make_one_surround_sensor(self):
        layout = RadarSpec(horizontal_fov_deg=360.0, physical_radars=6, physical_horizontal_fov_deg=90.0,
                           points_per_second=21600).physical_layout()
        self.assertEqual([item["yaw_deg"] for item in layout], [0.0, 60.0, 120.0, 180.0, 240.0, 300.0])
        self.assertEqual({item["points_per_second"] for item in layout}, {3600})

    def test_returns_are_rotated_into_the_logical_frame_and_wrapped(self):
        rows = np.array([[10.0, math.radians(10.0), math.radians(5.0), -3.0],
                         [20.0, math.radians(-10.0), 0.0, 1.0],
                         [30.0, math.radians(5.0), 0.0, 0.0]])
        at_60 = rotate_detections(rows[:1], 60.0)
        self.assertAlmostEqual(math.degrees(at_60[0, 1]), 70.0, places=6)
        self.assertAlmostEqual(math.degrees(at_60[0, 2]), 5.0, places=6)
        self.assertEqual((at_60[0, 0], at_60[0, 3]), (10.0, -3.0))  # depth and Doppler along the line of sight
        self.assertAlmostEqual(math.degrees(rotate_detections(rows[1:2], 300.0)[0, 1]), -70.0, places=6)
        self.assertAlmostEqual(math.degrees(rotate_detections(rows[2:3], 180.0)[0, 1]), -175.0, places=6)
        pitched = rotate_detections(np.array([[10.0, 0.0, 0.0, 0.0]]), 0.0, -10.0)
        self.assertAlmostEqual(math.degrees(pitched[0, 2]), -10.0, places=6)

    def test_the_campaign_profiles_use_the_surround_sensor(self):
        import yaml
        from src.cdf.common.config import Config

        for path in sorted((ROOT / "configs" / "sensors").glob("radar_*.yaml")):
            profile = yaml.safe_load(path.read_text(encoding="utf-8"))
            specs = radar_specs_from_config(Config(profile))
            self.assertEqual(len(specs), 1, path.name)
            spec = specs[0]
            self.assertEqual((spec.sensor_id, spec.horizontal_fov_deg, spec.vertical_fov_deg, spec.physical_radars,
                              spec.physical_horizontal_fov_deg, spec.mount_x, spec.mount_y, spec.mount_yaw_deg,
                              spec.mount_z_above_roof_m), ("surround", 360.0, 30.0, 6, 90.0, 0.0, 0.0, 0.0, 0.3),
                             path.name)
        default = yaml.safe_load((ROOT / "configs" / "default.yaml").read_text(encoding="utf-8"))
        self.assertEqual(default["sensors"]["profile"], "radar_baseline")
        baseline = radar_specs_from_config(Config(yaml.safe_load(
            (ROOT / "configs" / "sensors" / "radar_baseline.yaml").read_text(encoding="utf-8"))))[0]
        self.assertEqual((baseline.range_m, baseline.points_per_second, baseline.sensor_tick_s), (90.0, 21600, 0.05))


class FootprintTests(unittest.TestCase):
    def test_extent_is_the_ray_rectangle_exit(self):
        box = EgoFootprint(back=-2.4, front=2.4, left=-1.0, right=1.0)
        self.assertAlmostEqual(box.extent(0.0), 2.4)
        self.assertAlmostEqual(box.extent(math.pi), 2.4)
        self.assertAlmostEqual(box.extent(math.pi / 2), 1.0)
        self.assertAlmostEqual(box.extent(-math.pi / 2), 1.0)
        for degrees in np.arange(-180.0, 180.0, 7.3):
            theta = math.radians(degrees)
            c, s = abs(math.cos(theta)), abs(math.sin(theta))
            expected = min(2.4 / c if c > 1e-9 else math.inf, 1.0 / s if s > 1e-9 else math.inf)
            self.assertAlmostEqual(box.extent(theta), expected, places=9)
        corner = math.atan2(1.0, 2.4)
        self.assertAlmostEqual(box.extent(corner), math.hypot(2.4, 1.0), places=9)

    def test_an_off_centre_radar_measures_to_the_nearer_edge(self):
        bumper = EgoFootprint.from_metadata({"x_min_m": -2.4, "x_max_m": 2.4, "y_min_m": -1.0, "y_max_m": 1.0},
                                            RadarMount(x=2.2, y=0.0, z=1.0))
        self.assertAlmostEqual(bumper.extent(0.0), 0.2)
        self.assertAlmostEqual(bumper.extent(math.pi), 4.6)
        self.assertIsNone(EgoFootprint.from_metadata(None, CENTRE))


# --------------------------------------------------------------------------
# Synthetic radar returns in the recorder's local frame
# --------------------------------------------------------------------------

def ego_path(duration, speed=0.0, yaw_rate=0.0):
    """Constant speed and yaw rate from the origin (x ahead, y right, heading clockwise)."""
    states, x, y, heading = [], 0.0, 0.0, 0.0
    for k in range(int(round(duration / STEP)) + 1):
        t = round(k * STEP, 4)
        states.append(EgoState(t, x, y, heading, speed * math.cos(heading), speed * math.sin(heading)))
        x += speed * math.cos(heading) * STEP
        y += speed * math.sin(heading) * STEP
        heading += yaw_rate * STEP
    return EgoTrajectory(states)


def radar_xy(pose, mount):
    c, s = math.cos(pose.heading), math.sin(pose.heading)
    return pose.x + c * mount.x - s * mount.y, pose.y + s * mount.x + c * mount.y


def detections(pose, mount, points, velocities, previous=None):
    """[depth, azimuth, altitude, range rate] of points (local frame, z) seen by the radar.

    As CARLA's radar: its own velocity is its displacement since the previous
    sweep (``previous`` pose), not the vehicle's instantaneous velocity.
    """
    c, s = math.cos(pose.heading), math.sin(pose.heading)
    sx, sy = radar_xy(pose, mount)
    if previous is None:
        rx, ry = sx - pose.x, sy - pose.y
        svx, svy = pose.vx - pose.yaw_rate * ry, pose.vy + pose.yaw_rate * rx
    else:
        px, py = radar_xy(previous, mount)
        dt = pose.t_local - previous.t_local
        svx, svy = (sx - px) / dt, (sy - py) / dt
    rows = []
    for (px, py, pz), (vx, vy) in zip(points, velocities):
        dx, dy, dz = px - sx, py - sy, pz - mount.z
        depth = math.sqrt(dx * dx + dy * dy + dz * dz)
        along, across = c * dx + s * dy, -s * dx + c * dy
        unit = (dx / depth, dy / depth)
        rows.append([depth, math.atan2(across, along) - mount.yaw, math.atan2(dz, math.hypot(dx, dy)),
                     (vx - svx) * unit[0] + (vy - svy) * unit[1]])
    return rows


def observations(ego, mount, scene):
    """CompactObservations of ``scene(t) -> (points, velocities)`` over the ego's samples."""
    frames, stamps, offsets, rows = [], [], [0], []
    for k, state in enumerate(ego.states):
        pose = ego.at(state.t_local)
        points, velocities = scene(state.t_local)
        previous = ego.at(ego.states[k - 1].t_local) if k else None
        rows += detections(pose, mount, points, velocities, previous)
        frames.append(k)
        stamps.append(state.t_local)
        offsets.append(len(rows))
    return CompactObservations(frames=np.array(frames), timestamps=np.array(stamps, dtype=float),
                               offsets=np.array(offsets), detections=np.array(rows, dtype=np.float32).reshape(-1, 4))


def car_returns(cx, cy, heading=0.0, length=4.2, width=1.9, height=1.4, density=0.5):
    """Points on the visible outline of a car box (all four faces, several heights)."""
    out = []
    c, s = math.cos(heading), math.sin(heading)
    for along in np.arange(-length / 2, length / 2 + 1e-6, density):
        for side in (-width / 2, width / 2):
            for z in (0.5, 1.0, height):
                out.append((cx + c * along - s * side, cy + s * along + c * side, z))
    for across in np.arange(-width / 2, width / 2 + 1e-6, density):
        for end in (-length / 2, length / 2):
            for z in (0.5, 1.0):
                out.append((cx + c * end - s * across, cy + s * end + c * across, z))
    return out


def static_scene(points):
    return lambda t: (points, [(0.0, 0.0)] * len(points))


class EgoMotionTests(unittest.TestCase):
    """Static objects must stay static whatever the recorder does."""

    # Poles at object height in front, at the sides and behind, 6-30 m from the start (a moving
    # recorder passes some of them: those inside its footprint are its own-body filter's business).
    POLES = [(r * math.cos(math.radians(b)), r * math.sin(math.radians(b)), 1.0)
             for r in (6.0, 15.0, 30.0) for b in range(-180, 180, 30)]

    def moving_returns(self, ego, mount):
        cfg = TrackingConfig()
        sweeps = radar_sweeps(observations(ego, mount, static_scene(self.POLES)), ego, mount, 0.0, cfg, MODEL3)
        speeds = np.concatenate([sweep.radial_speed for sweep in sweeps[1:-1]])
        self.assertGreater(len(speeds), 0.95 * len(self.POLES) * (len(sweeps) - 2))
        return float(np.max(np.abs(speeds)))

    def test_stationary_straight_and_turning_recorders_see_static_scenery(self):
        for label, ego in (("stationary", ego_path(2.0)), ("straight 12 m/s", ego_path(2.0, speed=12.0)),
                           ("turning 8 m/s at 30 deg/s", ego_path(2.0, speed=8.0, yaw_rate=math.radians(30.0)))):
            with self.subTest(label):
                self.assertLess(self.moving_returns(ego, CENTRE), 0.05)

    def test_a_turning_off_centre_radar_needs_the_lever_arm(self):
        bumper = RadarMount(x=2.2, y=0.0, z=1.0)
        ego = ego_path(2.0, speed=8.0, yaw_rate=math.radians(30.0))
        self.assertLess(self.moving_returns(ego, bumper), 0.05)
        pose = ego.at(1.0)
        forward, right = sensor_velocity(pose, bumper)
        self.assertAlmostEqual(right - sensor_velocity(pose, CENTRE)[1], math.radians(30.0) * 2.2, places=3)

    def test_an_impact_does_not_make_the_scenery_move(self):
        # The recorder is struck: its speed drops from 12 to 4 m/s within one 50 ms step.  The radar's
        # displacement over the step (what CARLA's radar uses) is not the instantaneous velocity.
        states, x = [], 0.0
        for k in range(41):
            t = round(k * STEP, 4)
            speed = 12.0 if t < 1.0 - 1e-9 else 4.0
            states.append(EgoState(t, x, 0.0, 0.0, speed, 0.0))
            x += (12.0 if t < 1.0 - 1e-9 else 4.0) * STEP
        ego = EgoTrajectory(states)
        self.assertLess(self.moving_returns(ego, CENTRE), 0.05)

    def test_a_moving_target_keeps_its_own_radial_speed(self):
        ego = ego_path(2.0, speed=10.0, yaw_rate=math.radians(20.0))
        target = lambda t: ([(20.0, -10.0 + 5.0 * t, 1.0)], [(0.0, 5.0)])  # crossing left to right at 5 m/s
        sweeps = radar_sweeps(observations(ego, CENTRE, target), ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
        for sweep in sweeps:
            pose = ego.at(sweep.t_local)
            los = sweep.points[0] - sweep.sensor_xy
            expected = 5.0 * los[1] / np.linalg.norm(los)
            self.assertAlmostEqual(float(sweep.radial_speed[0]), expected, places=3)


class ClearanceTests(unittest.TestCase):
    def test_returns_from_the_own_body_are_dropped(self):
        ego = ego_path(1.0)
        own = [(0.5, 0.3, 1.45), (-1.0, -0.2, 1.4), (1.8, 0.0, 1.0)]  # roof and hood seen from the roof radar
        far = [(15.0, 0.0, 1.0)]
        stats = {}
        sweeps = radar_sweeps(observations(ego, CENTRE, static_scene(own + far)), ego, CENTRE, 0.0,
                              TrackingConfig(), MODEL3)
        self.assertEqual({len(sweep.points) for sweep in sweeps}, {1})
        self.assertEqual(sweeps[0].own_body, 3)
        build_local_tracks(observations(ego, CENTRE, static_scene(own + far)), ego, CENTRE, 0.0, TrackingConfig(),
                           MODEL3, stats)
        self.assertEqual(stats["own_body_returns_dropped"], 3 * len(ego.states))

    def test_clearance_reaches_zero_at_contact_and_ttc_uses_it(self):
        # A car 2.0 m shorter in front, closing at 5 m/s from 20 m to contact with the recorder's front edge.
        ego = ego_path(4.2)
        gap0, closing, half = 21.0, 5.0, 2.1

        def scene(t):
            gap = max(gap0 - closing * t, 0.0)
            centre = MODEL3.front + gap + half
            points = car_returns(centre, 0.0)
            return points, [(-closing if gap > 0 else 0.0, 0.0)] * len(points)

        tracks = build_local_tracks(observations(ego, CENTRE, scene), ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
        self.assertEqual(len(tracks), 1)
        samples = [s for s in tracks[0].samples if 0.5 <= s.t_local <= 3.8]
        for sample in samples:
            true_gap = max(gap0 - closing * sample.t_local, 0.0)
            self.assertLess(abs(sample.clearance_m - true_gap), 0.35, sample.t_local)
            # The raw range is from the centred radar to the car's tracked (median) point: much longer.
            self.assertGreater(sample.range_m, sample.clearance_m + MODEL3.front)
            if sample.ttc_s is not None and true_gap > 1.0:
                self.assertAlmostEqual(sample.ttc_s, sample.clearance_m / sample.closing_speed_mps, places=2)
        at_contact = min(tracks[0].samples, key=lambda s: abs(s.t_local - gap0 / closing))
        self.assertLess(at_contact.clearance_m, 0.35)

    def test_ego_path_starts_at_the_front_edge(self):
        ego = ego_path(3.0)
        beside = lambda t: (car_returns(1.0 + 0.0 * t, 2.6), [(0.0, 0.0)] * len(car_returns(1.0, 2.6)))
        ahead = lambda t: (car_returns(12.0 - 2.0 * t, 0.0), [(-2.0, 0.0)] * len(car_returns(12.0, 0.0)))
        for name, scene, expected in (("ahead", ahead, True),):
            tracks = build_local_tracks(observations(ego, CENTRE, scene), ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
            events = [e.type for e in track_events("A", tracks[0], ego.end, SemanticsConfig(), ego,
                                                   footprint=MODEL3)]
            self.assertEqual("EGO_PATH_ENTRY" in events or tracks[0].samples[0].ahead_m > 0, expected, name)
        sample = build_local_tracks(observations(ego, CENTRE, lambda t: (car_returns(1.0, 2.6),
                                                                          [(0.5, 0.0)] * len(car_returns(1.0, 2.6)))),
                                    ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
        # A car beside the front half is ahead of the radar but not of the front edge.
        for track in sample:
            self.assertTrue(all(s.ahead_m < 0 for s in track.samples))


class SurroundTrackingTests(unittest.TestCase):
    def test_a_target_passing_behind_stays_one_track(self):
        # The recorder stands; a car drives across behind it, from its right to its left, 8 m back.
        ego = ego_path(4.0)

        def scene(t):
            y = 12.0 - 6.0 * t
            points = car_returns(-8.0, y, heading=-math.pi / 2)
            return points, [(0.0, -6.0)] * len(points)

        tracks = build_local_tracks(observations(ego, CENTRE, scene), ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
        self.assertEqual(len(tracks), 1)
        bearings = [s.bearing_deg for s in tracks[0].samples]
        self.assertTrue(any(b > 170.0 for b in bearings) and any(b < -170.0 for b in bearings))
        self.assertGreater(tracks[0].last_t - tracks[0].first_t, 3.0)

    def test_returns_either_side_of_180_degrees_are_one_cluster(self):
        ego = ego_path(0.5)
        points = [(-10.0, 0.08, 1.0), (-10.0, -0.08, 1.0)]  # bearings +179.5 and -179.5 deg
        sweeps = radar_sweeps(observations(ego, CENTRE, lambda t: (points, [(-3.0, 0.0)] * 2)), ego, CENTRE, 0.0,
                              TrackingConfig(), MODEL3)
        from src.cdf.reconstruction.tracking import cluster_points
        self.assertEqual(len(cluster_points(sweeps[0].points, TrackingConfig().cluster_distance_m)), 1)

    def test_appearance_sides(self):
        cfg = SemanticsConfig()
        self.assertEqual([appearance_side(b, cfg) for b in (0.0, 4.0, -60.0, 60.0, 176.0, -179.0, 170.0, -100.0)],
                         ["FRONT", "FRONT", "LEFT", "RIGHT", "REAR", "REAR", "RIGHT", "LEFT"])

    def test_a_car_approaching_from_behind_appears_behind(self):
        ego = ego_path(3.0, speed=8.0)

        def scene(t):
            points = car_returns(-25.0 + 12.0 * t, 0.0)
            return points, [(12.0, 0.0)] * len(points)

        tracks = build_local_tracks(observations(ego, CENTRE, scene), ego, CENTRE, 0.0, TrackingConfig(), MODEL3)
        events = track_events("A", tracks[0], ego.end + 1.0, SemanticsConfig(), ego, footprint=MODEL3)
        self.assertEqual(events[0].type, "TRACK_APPEARED_REAR")


class ContactWindowTests(unittest.TestCase):
    def association(self, lost_before_s):
        with tempfile.TemporaryDirectory() as tmp:
            result = reconstruct_run(make_run(Path(tmp), a_sees_b_until=CONTACT_T - lost_before_s),
                                     ReconstructionConfig())
        return next(item for item in result.associations if item.local_graph == "A")

    def test_a_track_lost_up_to_one_second_before_the_contact_can_be_associated(self):
        item = self.association(0.8)
        self.assertEqual((item.status, item.global_entity), ("ASSOCIATED", "B"))
        self.assertTrue(any("continuous up to the contact" in line and "window 1.00 s" in line for line in item.evidence))

    def test_a_track_lost_longer_before_stays_anonymous(self):
        item = self.association(1.3)
        self.assertEqual(item.status, "ANONYMOUS")
        self.assertTrue(any(reason.startswith("lost 1.3") and reason.endswith("before the matched collision "
                                                                          "(window 1.00 s)")
                            for reason in item.blocking), item.blocking)


if __name__ == "__main__":
    unittest.main()
