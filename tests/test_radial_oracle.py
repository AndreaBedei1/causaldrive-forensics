import math

import numpy as np

from scripts.evaluate_radial_oracle import _rotation, _sensor_origin


def test_sensor_extrinsic_is_rotated_by_ego_yaw():
    observer = {"transform": {"x": 10.0, "y": 20.0, "z": 1.0, "roll_deg": 0.0,
                               "pitch_deg": 0.0, "yaw_deg": 90.0}}
    origin = _sensor_origin(observer, {"x": 2.0, "y": 0.0, "z": 0.0})
    assert np.allclose(origin, [10.0, 22.0, 1.0])


def _unreal_rotation(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Unreal's FRotationMatrix (rows = forward, right, up), as columns."""
    sr, cr = math.sin(roll), math.cos(roll)
    sp, cp = math.sin(pitch), math.cos(pitch)
    sy, cy = math.sin(yaw), math.cos(yaw)
    rows = np.array([[cp * cy, cp * sy, sp],
                     [sr * sp * cy - cr * sy, sr * sp * sy + cr * cy, -sr * cp],
                     [-(cr * sp * cy + sr * sy), cy * sr - cr * sp * sy, cr * cp]])
    return rows.T


def test_rotation_follows_carla_angle_conventions():
    # CARLA: positive pitch lifts the nose (S01 climbs with pitch +7 degrees).
    forward = _rotation(0.0, math.radians(7.0), 0.0) @ np.array([1.0, 0.0, 0.0])
    assert forward[2] > 0.12
    for roll, pitch, yaw in ((0.1, 0.2, 0.3), (-0.4, 0.12, 2.5), (0.0, -0.3, -1.0)):
        assert np.allclose(_rotation(roll, pitch, yaw), _unreal_rotation(roll, pitch, yaw))


def test_sensor_on_a_climbing_car_is_raised_by_the_mount():
    observer = {"transform": {"x": 0.0, "y": 0.0, "z": 0.0, "roll_deg": 0.0,
                               "pitch_deg": 7.0, "yaw_deg": 0.0}}
    origin = _sensor_origin(observer, {"x": 2.2, "y": 0.0, "z": 1.0})
    assert np.allclose(origin, [2.2 * math.cos(math.radians(7.0)) - math.sin(math.radians(7.0)), 0.0,
                                2.2 * math.sin(math.radians(7.0)) + math.cos(math.radians(7.0))])
