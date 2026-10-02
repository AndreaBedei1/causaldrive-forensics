"""Three physical radars on the body (front, left, right; no rear radar).

Configuration and mounts, field-of-view coverage with the rear blind zone, per-mount Doppler and
ego-motion compensation (stopped, straight, turning, accelerating, braking recorder; static scenery
and moving targets ahead, at the side and in a rear quarter), placement of each return from its own
radar, one track across the front -> side transition, appearance of a car from behind.

Synthetic returns are generated as CARLA 0.9.15 generates them: each radar at its own mount, its own
velocity = the displacement of its mount over the tick, range rate = (target velocity - radar
velocity) . line of sight, azimuth / altitude in the radar's own frame, and only inside its
horizontal / vertical field of view and range.
"""

import math
import unittest
from types import SimpleNamespace

import numpy as np

from src.cdf.common.config import available_scenarios, load_run_config
from src.cdf.reconstruction.config import SemanticsConfig, TrackingConfig
from src.cdf.reconstruction.local import appearance_side
from src.cdf.reconstruction.tracking import (EgoFootprint, EgoState, EgoTrajectory, RadarMount, RadarStream,
                                             build_local_tracks, radar_sweeps, sensor_point)
from src.cdf.simulation.scenario_base import ScenarioSpec
from src.cdf.simulation.sensors import radar_specs_from_config

DT = 0.05
# The recorded ego_footprint of the campaign blueprints: x_min, x_max, y_min, y_max (vehicle frame).
FOOTPRINTS = {
    "vehicle.tesla.model3": (-2.3667, 2.4251, -1.0817, 1.0817),
    "vehicle.audi.tt": (-2.091, 2.0902, -0.9971, 0.9971),
    "vehicle.nissan.patrol": (-2.3596, 2.2449, -0.9656, 0.966),
    "vehicle.mercedes.sprinter": (-2.9681, 2.9471, -0.9901, 0.9984),
}
MODEL3 = FOOTPRINTS["vehicle.tesla.model3"]
SPECS = radar_specs_from_config(load_run_config("S01"))


def fake_vehicle(footprint):
    x_min, x_max, y_min, y_max = footprint
    box = SimpleNamespace(location=SimpleNamespace(x=(x_min + x_max) / 2.0, y=(y_min + y_max) / 2.0, z=0.7),
                          extent=SimpleNamespace(x=(x_max - x_min) / 2.0, y=(y_max - y_min) / 2.0, z=0.7))
    return SimpleNamespace(bounding_box=box)


def radars(footprint=MODEL3):
    """[(spec, RadarMount)] as the recorder resolves them on a vehicle with this footprint."""
    out = []
    for spec in SPECS:
        t = spec.mount_transform(fake_vehicle(footprint))
        out.append((spec, RadarMount(x=t["x"], y=t["y"], z=t["z"], yaw=math.radians(t["yaw_deg"]),
                                     pitch=math.radians(t["pitch_deg"]), sensor_id=spec.sensor_id)))
    return out


def covering(footprint, bearing_deg, distance_m):
    """Sensor ids whose field of view contains the point (bearing, distance) from the footprint centre."""
    cx, cy = (footprint[0] + footprint[1]) / 2.0, (footprint[2] + footprint[3]) / 2.0
    px = cx + distance_m * math.cos(math.radians(bearing_deg))
    py = cy + distance_m * math.sin(math.radians(bearing_deg))
    out = []
    for spec, mount in radars(footprint):
        dx, dy = px - mount.x, py - mount.y
        azimuth = (math.degrees(math.atan2(dy, dx) - mount.yaw) + 180.0) % 360.0 - 180.0
        if abs(azimuth) <= spec.horizontal_fov_deg / 2.0 and math.hypot(dx, dy) <= spec.range_m:
            out.append(spec.sensor_id)
    return out


# --------------------------------------------------------------------------------------------
# A synthetic recorder: its motion in the local frame (= world here) and CARLA-like radar rows
# --------------------------------------------------------------------------------------------

def motion(kind):
    """The recorder's pose at time t (heading + = turning right, CARLA's convention)."""
    def state(t):
        if kind == "stopped":
            return EgoState(t, 0.0, 0.0, 0.0, 0.0, 0.0)
        if kind == "straight":
            return EgoState(t, 10.0 * t, 0.0, 0.0, 10.0, 0.0)
        if kind == "accelerating":
            return EgoState(t, 4.0 * t + 1.5 * t * t, 0.0, 0.0, 4.0 + 3.0 * t, 0.0)
        if kind == "braking":
            return EgoState(t, 14.0 * t - 3.0 * t * t, 0.0, 0.0, 14.0 - 6.0 * t, 0.0)
        if kind == "turning":  # 8 m/s, 20 deg/s to the right
            w, v = math.radians(20.0), 8.0
            h = w * t
            return EgoState(t, v / w * math.sin(h), v / w * (1.0 - math.cos(h)), h, v * math.cos(h), v * math.sin(h))
        raise ValueError(kind)
    return state


class FakeObservations:
    def __init__(self, timestamps, frames):
        self.timestamps = np.asarray(timestamps, dtype=float)
        self._frames = frames

    def frame_detections(self, index):
        return self._frames[index]


def carla_rows(spec, mount, own_now, own_before, points, velocities):
    """[depth, azimuth, altitude, range rate] of the world points one radar sees (no occlusion)."""
    origin = sensor_point(own_now, mount)
    radar_velocity = (origin - sensor_point(own_before, mount)) / DT  # CARLA: its own displacement
    phi = own_now.heading + mount.yaw
    rows = []
    for point, velocity in zip(points, velocities):
        line = np.asarray(point, dtype=float) - origin
        depth = float(np.linalg.norm(line))
        u = line / depth
        xs, ys = u[0] * math.cos(phi) + u[1] * math.sin(phi), -u[0] * math.sin(phi) + u[1] * math.cos(phi)
        azimuth, altitude = math.atan2(ys, xs), math.asin(u[2])
        if (abs(math.degrees(azimuth)) > spec.horizontal_fov_deg / 2.0
                or abs(math.degrees(altitude)) > spec.vertical_fov_deg / 2.0 or depth > spec.range_m):
            continue
        rows.append([depth, azimuth, altitude, float((np.asarray(velocity, dtype=float) - radar_velocity) @ u)])
    return np.asarray(rows, dtype=float).reshape(-1, 4)


def cruising(speed):
    """A recorder driving straight at a constant speed."""
    return lambda t: EgoState(t, speed * t, 0.0, 0.0, speed, 0.0)


def record(kind, scene, duration=2.0, footprint=MODEL3):
    """(ego trajectory, radar streams) of a recorder moving as ``kind`` (a name of :func:`motion` or a
    pose function) through ``scene(t, own, spec, mount)``: the (points, velocities) one radar could see
    at t, before its field of view is applied."""
    pose = motion(kind) if isinstance(kind, str) else kind
    times = [round(k * DT, 4) for k in range(int(round(duration / DT)) + 1)]
    ego = EgoTrajectory([pose(round(t, 4)) for t in [-DT] + times])  # one pose before the first sweep
    streams = []
    for spec, mount in radars(footprint):
        frames = []
        for t in times:
            points, velocities = scene(t, pose(t), spec, mount)
            frames.append(carla_rows(spec, mount, pose(t), pose(t - DT), points, velocities))
        streams.append(RadarStream(mount, FakeObservations(times, frames)))
    return ego, streams


def box_surface(centre, heading, length=4.6, width=1.9, height=0.8, spacing=0.4):
    """Points on the four vertical faces of a car body (x forward, y right) and their outward normals."""
    c, s = math.cos(heading), math.sin(heading)
    out = []
    for (ax, ay, nx, ny, extent) in ((length / 2, 0, 1, 0, width), (-length / 2, 0, -1, 0, width),
                                     (0, width / 2, 0, 1, length), (0, -width / 2, 0, -1, length)):
        n = max(int(extent / spacing), 1)
        for k in range(n + 1):
            offset = -extent / 2 + extent * k / n
            px, py = ax + (offset if ax == 0 else 0.0), ay + (offset if ay == 0 else 0.0)
            out.append((np.array([centre[0] + c * px - s * py, centre[1] + s * px + c * py, height]),
                        np.array([c * nx - s * ny, s * nx + c * ny])))
    return out


def car_scene(cars):
    """Scene of cars [(centre(t) -> (x, y), velocity (vx, vy))]: the faces each radar can see."""
    def scene(t, own, spec, mount):
        origin = sensor_point(own, mount)
        points, velocities = [], []
        for centre_of, velocity in cars:
            centre = centre_of(t)
            heading = math.atan2(velocity[1], velocity[0]) if math.hypot(*velocity) > 0 else 0.0
            for point, normal in box_surface(centre, heading):
                if normal @ (origin[:2] - point[:2]) > 0.0:  # the face looks at the radar
                    points.append(point)
                    velocities.append(np.array([velocity[0], velocity[1], 0.0]))
        return points, velocities
    return scene


# --------------------------------------------------------------------------------------------
# Configuration, mounts, coverage
# --------------------------------------------------------------------------------------------

class ConfigurationTests(unittest.TestCase):
    def test_three_radars_front_left_right_and_no_rear(self):
        layout = {spec.sensor_id: (spec.anchor, spec.mount_yaw_deg) for spec in SPECS}
        self.assertEqual(layout, {"front": ("front", 0.0), "left": ("left", -90.0), "right": ("right", 90.0)})
        for spec in SPECS:
            self.assertLess(spec.horizontal_fov_deg, 180.0)  # CARLA folds a wider cone back
            self.assertEqual((spec.vertical_fov_deg, spec.range_m, spec.points_per_second, spec.sensor_tick_s),
                             (20.0, 90.0, 12000, 0.05))
        self.assertEqual({s.sensor_id: s.horizontal_fov_deg for s in SPECS}, {"front": 150.0, "left": 140.0, "right": 140.0})

    def test_every_campaign_run_uses_the_same_radars(self):
        reference = [spec.__dict__ for spec in SPECS]
        for scenario in available_scenarios():
            cfg = load_run_config(scenario)
            for variant in (cfg.get("scenario.variants", {}) or {"default": None}):
                spec = ScenarioSpec.from_config(cfg, variant=None if variant == "default" else variant)
                self.assertTrue(all(not p.sensor_profile for p in spec.participants), (scenario, variant))
            self.assertEqual([s.__dict__ for s in radar_specs_from_config(cfg)], reference, scenario)

    def test_mounts_sit_on_the_body_just_outside_the_bounding_box(self):
        for blueprint, (x_min, x_max, y_min, y_max) in FOOTPRINTS.items():
            mounts = {spec.sensor_id: mount for spec, mount in radars(FOOTPRINTS[blueprint])}
            centre_x = (x_min + x_max) / 2.0
            self.assertAlmostEqual(mounts["front"].x, x_max + 0.05, places=3, msg=blueprint)
            self.assertAlmostEqual(mounts["front"].y, (y_min + y_max) / 2.0, places=3)  # the box's centre line
            self.assertAlmostEqual(mounts["left"].y, y_min - 0.05, places=3)
            self.assertAlmostEqual(mounts["right"].y, y_max + 0.05, places=3)
            for side in ("left", "right"):
                self.assertAlmostEqual(mounts[side].x, centre_x, places=3)
            for mount in mounts.values():
                self.assertAlmostEqual(mount.z, 0.6)
                inside = x_min < mount.x < x_max and y_min < mount.y < y_max
                self.assertFalse(inside, (blueprint, mount))


class CoverageTests(unittest.TestCase):
    """Fields of view of points around the recorder (bearing and distance from its footprint centre).

    Measured spans (model3; the other blueprints within 1-7 deg): front +-46 deg at 5 m, +-61 at 10 m,
    +-69 at 25 m, +-73 at 80 m; sides from 33 deg (5 m) / 27 (10 m) / 22 (40 m) to 147 / 153 / 158 deg.
    """

    def test_front_and_sides_are_covered_without_a_gap(self):
        for blueprint, footprint in FOOTPRINTS.items():
            for distance in (5.0, 10.0, 25.0, 40.0, 80.0):
                for bearing in range(-145, 146):
                    self.assertTrue(covering(footprint, bearing, distance), (blueprint, distance, bearing))

    def test_the_front_to_side_transition_is_seen_by_two_radars(self):
        # No artificial discontinuity: where the front radar's field ends the side radar's has begun.
        for footprint in FOOTPRINTS.values():
            for distance in (10.0, 25.0, 40.0, 80.0):
                for bearing in range(30, 56):
                    self.assertEqual(sorted(covering(footprint, bearing, distance)), ["front", "right"])
                    self.assertEqual(sorted(covering(footprint, -bearing, distance)), ["front", "left"])

    def test_directly_behind_is_a_blind_zone(self):
        for blueprint, footprint in FOOTPRINTS.items():
            for distance in (5.0, 10.0, 25.0, 40.0, 80.0):
                blind = [b for b in range(-180, 180) if not covering(footprint, b, distance)]
                self.assertIn(-180, blind)
                self.assertTrue(all(abs(b) >= 148 for b in blind), (blueprint, distance))
                # Total width for a point: 41-53 deg from 10 m on, up to 65 deg at 5 m (a car's own width
                # makes the cone it hides in narrower: its near corner enters a side radar's field earlier).
                upper = 66 if distance < 10.0 else 54
                self.assertTrue(40 <= len(blind) <= upper, (blueprint, distance, len(blind)))


# --------------------------------------------------------------------------------------------
# Doppler and placement from each radar's own mount
# --------------------------------------------------------------------------------------------

POLES = [np.array([x, y, 1.0]) for x, y in ((30.0, 0.5), (20.0, -8.0), (12.0, 10.0), (3.0, -9.0), (0.0, 12.0),
                                            (-12.0, -7.0), (-6.0, 9.0), (40.0, 25.0), (8.0, -30.0), (-2.0, -15.0))]


def static_scene(t, own, spec, mount):
    return POLES, [np.zeros(3)] * len(POLES)


MOVERS = {  # name: (position at t = 0, ground velocity)
    "ahead": (np.array([25.0, 0.0, 0.8]), np.array([6.0, 0.0, 0.0])),
    "crossing": (np.array([20.0, 15.0, 0.8]), np.array([0.0, -8.0, 0.0])),
    "left_side": (np.array([0.0, -4.0, 0.8]), np.array([12.0, 0.0, 0.0])),
    "rear_quarter": (np.array([-9.0, 5.0, 0.8]), np.array([15.0, 0.0, 0.0])),
    "oncoming": (np.array([45.0, -3.5, 0.8]), np.array([-10.0, 0.0, 0.0])),
}


def moving_scene(t, own, spec, mount):
    return [p + v * t for p, v in MOVERS.values()], [v for _, v in MOVERS.values()]


class DopplerTests(unittest.TestCase):
    KINDS = ("stopped", "straight", "turning", "accelerating", "braking")

    def test_static_scenery_stays_static_for_every_radar_and_every_motion(self):
        cfg = TrackingConfig()
        for kind in self.KINDS:
            ego, streams = record(kind, static_scene)
            seen = set()
            for sweep in radar_sweeps(streams, ego, 0.0, cfg, EgoFootprint(*MODEL3)):
                self.assertLess(float(np.max(np.abs(sweep.radial_speed), initial=0.0)), 0.02, (kind, sweep.t_local))
                seen |= {sweep.radars[k] for k in sweep.radar.tolist()}
            self.assertEqual(seen, {"front", "left", "right"}, kind)

    def test_the_lever_arm_of_a_turn_is_large_enough_to_matter(self):
        # A front radar 2.48 m ahead of the origin, turning at 20 deg/s, moves 0.87 m/s sideways that
        # the vehicle origin does not: compensating with the vehicle's velocity would leave static
        # poles moving by up to that much, far above the 0.02 m/s checked above.
        mount = dict((spec.sensor_id, m) for spec, m in radars())["front"]
        self.assertGreater(math.radians(20.0) * mount.x, 0.8)

    def test_moving_targets_keep_their_own_line_of_sight_speed(self):
        cfg = TrackingConfig()
        for kind in self.KINDS:
            ego, streams = record(kind, moving_scene)
            by_radar = {name: set() for name in MOVERS}
            for sweep in radar_sweeps(streams, ego, 0.0, cfg, EgoFootprint(*MODEL3)):
                for point, origin, radar, radial in zip(sweep.points, sweep.origins, sweep.radar, sweep.radial_speed):
                    name, (start, velocity) = min(MOVERS.items(), key=lambda item: np.hypot(
                        *(item[1][0][:2] + item[1][1][:2] * sweep.t_local - point)))
                    truth = start[:2] + velocity[:2] * sweep.t_local
                    self.assertLess(float(np.hypot(*(truth - point))), 1e-3, (kind, name))  # placed from its radar
                    mount = streams[radar].mount
                    own = ego.at(sweep.t_local)
                    expected_origin = sensor_point(own, mount)[:2]
                    self.assertLess(float(np.hypot(*(origin - expected_origin))), 1e-6)
                    line = (truth - expected_origin) / np.linalg.norm(truth - expected_origin)
                    self.assertAlmostEqual(float(radial), float(velocity[:2] @ line), delta=0.02, msg=(kind, name))
                    by_radar[name].add(sweep.radars[radar])
            self.assertIn("front", by_radar["ahead"], kind)
            self.assertIn("left", by_radar["left_side"], kind)
            self.assertIn("right", by_radar["rear_quarter"], kind)
            self.assertTrue(by_radar["crossing"] and by_radar["oncoming"], kind)


# --------------------------------------------------------------------------------------------
# Tracks: clearance, front -> side, appearance from behind, the blind zone
# --------------------------------------------------------------------------------------------

class TrackTests(unittest.TestCase):
    def test_clearance_is_from_the_body_and_range_from_the_observing_radar(self):
        # Recorder stopped; a car ahead (rear face 20 m ahead of the origin) drives away at 3 m/s.
        lead = [(lambda t: (22.3 + 3.0 * t, 0.0), (3.0, 0.0))]
        ego, streams = record("stopped", car_scene(lead), duration=2.0)
        tracks = build_local_tracks(streams, ego, 0.0, TrackingConfig(), EgoFootprint(*MODEL3))
        self.assertEqual(len(tracks), 1)
        for sample in tracks[0].samples[5:]:
            rear_face = 20.0 + 3.0 * sample.t_local
            self.assertAlmostEqual(sample.clearance_m, rear_face - MODEL3[1], delta=0.15)
            self.assertEqual(sample.radar, "front")
            # The raw range runs from the front radar (2.475 m ahead) to the tracked point.
            self.assertAlmostEqual(sample.range_m, math.hypot(sample.longitudinal_m - 2.4751, sample.lateral_m),
                                   delta=0.01)
            self.assertAlmostEqual(sample.speed_mps, 3.0, delta=0.3)

    def test_a_car_passing_from_the_front_to_the_side_is_one_track(self):
        # Recorder at 14 m/s overtakes a car at 6 m/s in the next lane on its left.
        slow = [(lambda t: (25.0 + 6.0 * t, -3.5), (6.0, 0.0))]
        ego, streams = record(cruising(14.0), car_scene(slow), duration=4.5)
        tracks = build_local_tracks(streams, ego, 0.0, TrackingConfig(), EgoFootprint(*MODEL3))
        self.assertEqual(len(tracks), 1, [t.summary() for t in tracks])
        track = tracks[0]
        summary = track.summary()
        self.assertEqual(summary["radars"], ["front", "left"])
        self.assertLess(track.first_t, 0.3)
        gaps = np.diff([s.t_local for s in track.samples if s.measured])
        self.assertLessEqual(float(gaps.max()), DT + 1e-6)
        self.assertLess(summary["last_bearing_deg"], -120.0)  # followed well into the rear quarter
        # While only its rear face is visible the speed is exact.  Passing the recorder, the median of
        # its returns slides from the rear face onto the side face (an extended target seen from a
        # changing aspect): the filter takes part of that slide for motion.  Known limitation, bounded
        # here; on the recorded campaign the side-aspect velocity error is 0.48 m/s rms.
        for sample in track.samples[5:]:
            limit = 0.3 if abs(sample.bearing_deg) < 15.0 else 3.5
            self.assertAlmostEqual(sample.speed_mps, 6.0, delta=limit, msg=sample.t_local)

    def test_a_car_overtaking_from_behind_appears_on_the_side(self):
        # Recorder at 8 m/s; a car at 14 m/s in the next lane on its left starts 35 m behind.
        fast = [(lambda t: (-35.0 + 14.0 * t, -3.5), (14.0, 0.0))]
        ego, streams = record(cruising(8.0), car_scene(fast), duration=6.0)
        tracks = build_local_tracks(streams, ego, 0.0, TrackingConfig(), EgoFootprint(*MODEL3))
        self.assertEqual(len(tracks), 1)
        first = tracks[0].samples[0]
        self.assertLess(first.bearing_deg, -120.0)  # first seen in the left rear quarter...
        self.assertGreater(first.longitudinal_m, -12.0)  # ...only once close: the blind zone behind
        self.assertEqual(appearance_side(first.bearing_deg, SemanticsConfig()), "LEFT")
        self.assertIn("left", tracks[0].summary()["radars"])

    def test_a_car_directly_behind_is_not_seen(self):
        # Recorder at 8 m/s; a follower at 13 m/s in the same lane closes in from 25 m to 2 m behind
        # its rear bumper: it stays in the rear blind zone (an S01-like rear-end seen by the lead car).
        follower = [(lambda t: (-29.7 + 13.0 * t, 0.0), (13.0, 0.0))]
        ego, streams = record(cruising(8.0), car_scene(follower), duration=4.5)
        returns = sum(len(stream.observations.frame_detections(k)) for stream in streams
                      for k in range(len(stream.observations.timestamps)))
        self.assertEqual(returns, 0)
        self.assertEqual(build_local_tracks(streams, ego, 0.0, TrackingConfig(), EgoFootprint(*MODEL3)), [])


if __name__ == "__main__":
    unittest.main()
