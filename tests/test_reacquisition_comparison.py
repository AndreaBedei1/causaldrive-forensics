import json
from pathlib import Path

import numpy as np
import pytest

from scripts.compare_reacquisition import (
    _incomplete_sensor_ids,
    _load_run,
    _sensor_quality,
    _sensor_inventory,
    collision_events,
    collision_episodes,
    trajectory_metrics,
)


def _state(timestamp, x, yaw, actor_id):
    return {
        "timestamp": timestamp,
        "participant_id": "A",
        "actor_id": actor_id,
        "transform": {"x": x, "y": 2.0, "yaw_deg": yaw},
        "velocity": {"x": 12.0, "y": 0.0},
    }


def test_trajectory_comparison_aligns_time_and_separates_spawn_offset_from_motion():
    old = [_state(100.05, 1.0, 179.0, 11), _state(100.10, 1.6, -179.0, 11)]
    new = [_state(7.05, 1.25, -181.0, 27), _state(7.10, 1.85, -179.0, 27)]

    result = trajectory_metrics(old, 100.0, new, 7.0)

    assert result["position_world_max_m"] == pytest.approx(0.25)
    assert result["position_from_start_max_m"] == pytest.approx(0.0)
    assert result["velocity_2d_max_mps"] == pytest.approx(0.0)
    assert result["heading_abs_max_deg"] == pytest.approx(0.0)


def test_collision_events_deduplicate_reciprocal_callbacks_but_keep_later_impacts():
    rows = [
        {"frame": 150, "timestamp": 101.0, "participant_id": "A", "other_actor_id": 22, "impulse": 4.0},
        {"frame": 150, "timestamp": 101.0, "participant_id": "B", "other_actor_id": 11, "impulse": 4.0},
        {"frame": 151, "timestamp": 101.05, "participant_id": "A", "other_actor_id": 22, "impulse": 2.0},
    ]

    events = collision_events(rows, {11: "A", 22: "B"}, 100.0)

    assert [(event["pair"], event["t_rel_s"], event["callback_count"])
            for event in events] == [("A-B", 1.0, 2), ("A-B", 1.05, 1)]


def test_collision_episodes_group_contact_ticks_and_keep_separated_impacts():
    events = [
        {"pair": "A-B", "t_rel_s": 1.0, "frame": 100, "impulse_sum": 20.0},
        {"pair": "A-B", "t_rel_s": 1.05, "frame": 101, "impulse_sum": 5.0},
        {"pair": "A-B", "t_rel_s": 1.15, "frame": 103, "impulse_sum": 2.0},
        {"pair": "A-C", "t_rel_s": 1.2, "frame": 104, "impulse_sum": 9.0},
        {"pair": "A-B", "t_rel_s": 1.3, "frame": 106, "impulse_sum": 1.0},
    ]

    result = collision_episodes(events, dt_s=0.05)

    assert [(event["pair"], event["start_t_rel_s"], event["end_t_rel_s"], event["contact_ticks"])
            for event in result] == [
                ("A-B", 1.0, 1.15, 3), ("A-C", 1.2, 1.2, 1), ("A-B", 1.3, 1.3, 1),
            ]
    assert result[0]["impulse_sum"] == 27.0


def test_all_incomplete_configured_sensors_are_reported_as_gate_blockers():
    rows = [
        {"sensor": "A/radar/front", "old_present": True, "new_present": True, "new_complete": True},
        {"sensor": "A/depth/front_depth", "old_present": True, "new_present": True, "new_complete": False},
        {"sensor": "B/camera/front_rgb", "old_present": True, "new_present": False, "new_complete": None},
        {"sensor": "C/radar/right", "old_present": False, "new_present": True,
         "old_complete": None, "new_complete": True},
    ]

    assert _incomplete_sensor_ids(rows) == ["A/depth/front_depth", "B/camera/front_rgb"]
    assert _incomplete_sensor_ids(rows, "old") == ["C/radar/right"]


def test_depth_incompleteness_is_reported_but_is_not_a_required_sensor_gate():
    rows = [
        {"sensor": "A/radar/front", "kind": "radar", "old_present": True, "new_present": True,
         "old_complete": True, "new_complete": True, "static_config_equal": True},
        {"sensor": "A/camera/front_rgb", "kind": "rgb", "old_present": True, "new_present": True,
         "old_complete": True, "new_complete": True, "static_config_equal": True},
        {"sensor": "A/depth/front_depth", "kind": "depth", "old_present": True, "new_present": False,
         "old_complete": False, "new_complete": None, "static_config_equal": False},
    ]

    quality = _sensor_quality(rows)

    assert quality["sensor_gate"] == "PASS"
    assert quality["new_required_incomplete_sensors"] == []
    assert quality["new_depth_advisory_incomplete_sensors"] == ["A/depth/front_depth"]
    assert _incomplete_sensor_ids(rows) == ["A/depth/front_depth"]


def test_missing_radar_or_rgb_still_blocks_sensor_gate():
    rows = [
        {"sensor": "A/radar/front", "kind": "radar", "old_present": True, "new_present": True,
         "old_complete": True, "new_complete": False, "static_config_equal": True},
        {"sensor": "A/camera/front_rgb", "kind": "rgb", "old_present": True, "new_present": True,
         "old_complete": True, "new_complete": True, "static_config_equal": True},
    ]

    assert _sensor_quality(rows)["sensor_gate"] == "FAIL"


def test_legacy_ground_truth_without_role_metadata_derives_nonrecorders_from_states(tmp_path: Path):
    run = tmp_path / "S01" / "run_0_crash"
    (run / "ground_truth").mkdir(parents=True)
    (run / "vehicles" / "A").mkdir(parents=True)
    (run / "metadata.json").write_text(json.dumps({"scenario_id": "S01", "variant": "crash",
                                                    "seed": 0, "participants": ["A"],
                                                    "simulation_start_timestamp": 10.0}), encoding="utf-8")
    (run / "ground_truth" / "metadata.json").write_text(json.dumps({"map": "Town05"}), encoding="utf-8")
    states = [{"timestamp": 10.05, "frame": 1, "actor_id": 10, "participant_id": "A"},
              {"timestamp": 10.05, "frame": 1, "actor_id": 20, "participant_id": "C"}]
    (run / "ground_truth" / "states.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in states), encoding="utf-8")

    result = _load_run(run)

    assert result["participant_roles"] == {"A": True, "C": False}


def test_sensor_config_comparison_ignores_run_local_absolute_frame_ids(tmp_path: Path):
    sensor = tmp_path / "run" / "vehicles" / "A" / "radar" / "front"
    sensor.mkdir(parents=True)
    (sensor / "metadata.json").write_text(json.dumps({
        "sensor_id": "front", "sensor_tick_s": 0.05, "first_frame": 10,
        "last_frame": 11, "frames_written": 2, "callbacks_received": 2,
        "queue_drops": 0, "missing_frame_count": 0, "frames_without_measurement": 0,
        "duplicate_callbacks": 0, "horizontal_fov_deg": 150.0,
    }), encoding="utf-8")
    np.savez(sensor / "observations.npz", frames=np.array([10, 11]), timestamps=np.array([1.0, 1.05]))

    result = _sensor_inventory(tmp_path / "run", 0.1)["A/radar/front"]

    assert "first_frame" not in result["static_config"]
    assert "last_frame" not in result["static_config"]
    assert result["static_config"]["horizontal_fov_deg"] == 150.0
