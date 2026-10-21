from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from src.cdf.common.config import load_run_config
from src.cdf.simulation.sensors import camera_spec_from_config, depth_camera_spec_from_config, radar_specs_from_config
from src.cdf.simulation.vehicle_agent import RawVehicleAgent


class _Radar:
    def __init__(self, _world, _vehicle, spec):
        self.spec = spec
        self.stats = {}

    def metadata(self):
        return {"sensor_id": self.spec.sensor_id, "sensor_tick_s": self.spec.sensor_tick_s}


class _Camera:
    stats = {}


def test_future_default_keeps_radar_and_rgb_but_disables_depth():
    cfg = load_run_config()

    assert cfg.get("sensors.depth_camera.enabled") is False
    assert depth_camera_spec_from_config(cfg) is None
    assert camera_spec_from_config(cfg) is not None
    assert radar_specs_from_config(cfg)


def test_disabled_depth_is_not_instantiated_or_written_and_radar_rgb_remain(tmp_path: Path):
    cfg = load_run_config()
    vehicle = SimpleNamespace(bounding_box=SimpleNamespace(
        location=SimpleNamespace(x=0.0, y=0.0, z=0.0),
        extent=SimpleNamespace(x=2.0, y=1.0, z=0.5)))
    world = SimpleNamespace(spawn_vehicle=lambda *_: vehicle)
    spec = SimpleNamespace(blueprint="vehicle.tesla.model3", record=True, sensor_profile=None,
                           participant_id="A")
    spawn = SimpleNamespace(location=SimpleNamespace(x=0.0, y=0.0, z=0.0),
                            rotation=SimpleNamespace(yaw=0.0))
    expected_radars = radar_specs_from_config(cfg)

    with patch("src.cdf.simulation.vehicle_agent.RadarSensor", side_effect=_Radar), \
            patch("src.cdf.simulation.vehicle_agent.CameraSensor", side_effect=lambda *_args, **_kwargs: _Camera()) as camera, \
            patch("src.cdf.simulation.vehicle_agent.CollisionSensor"):
        agent = RawVehicleAgent(world, cfg, spec, None, spawn, tmp_path)
        assert agent.depth_camera is None
        assert agent._depth_executor is None
        assert agent._depth_estimator is None
        assert camera.call_count == 1
        assert camera.call_args.args[2].blueprint == "sensor.camera.rgb"
        assert len(agent.radar) == len(expected_radars)

        sensor_id = expected_radars[0].sensor_id
        agent.logger.log_radar({"sensor_id": sensor_id, "frame": 1, "timestamp": 0.05, "detections": []})
        agent.logger.log_camera({"frame": 1, "timestamp": 0.1, "width": 800, "height": 600},
                                bytes([0, 0, 0, 255]) * (800 * 600))
        agent.close()

    recorder = tmp_path / "vehicles" / "A"
    assert (recorder / "radar" / sensor_id / "observations.npz").exists()
    assert np.load(recorder / "radar" / sensor_id / "observations.npz")["frames"].tolist() == [1]
    assert (recorder / "camera" / "metadata.json").exists()
    assert not (recorder / "depth").exists()
