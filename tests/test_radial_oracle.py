import numpy as np

from scripts.evaluate_radial_oracle import _sensor_origin


def test_sensor_extrinsic_is_rotated_by_ego_yaw():
    observer = {"transform": {"x": 10.0, "y": 20.0, "z": 1.0, "roll_deg": 0.0,
                               "pitch_deg": 0.0, "yaw_deg": 90.0}}
    origin = _sensor_origin(observer, {"x": 2.0, "y": 0.0, "z": 0.0})
    assert np.allclose(origin, [10.0, 22.0, 1.0])
