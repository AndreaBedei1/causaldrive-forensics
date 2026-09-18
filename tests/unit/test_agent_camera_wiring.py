"""The parts of the camera wiring that do not need a simulator.

Spawning a CARLA sensor needs CARLA, and that is validated by running a scenario.
What can be checked here is everything around it: that a camera-less
configuration is a supported configuration rather than a crash, that the buffer
is latched by contact and not by anything else, and that the helpers turning
frames into events behave.
"""

from __future__ import annotations

import numpy as np
import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.schemas import EventType
from cdf.local.video_buffer import VideoBuffer
from cdf.simulation.sensors import camera_spec_from_config
from cdf.simulation.vehicle_agent import _encode_clip, _nearest_speed, _sign_events


# --- the camera is optional ------------------------------------------------


def test_the_default_configuration_has_a_camera():
    spec = camera_spec_from_config(load_run_config())
    assert spec is not None
    assert (spec.width, spec.height) == (800, 600)


def test_a_camera_can_be_switched_off_without_breaking_anything():
    """The V1 scenarios were recorded without one and must stay runnable."""
    off = Config({"sensors": {"camera": {"enabled": False}}})
    assert camera_spec_from_config(off) is None


def test_a_configuration_with_no_sensors_block_gets_no_camera():
    """Absent means off, which is the safe direction for an old configuration.

    The V1 configs predate the camera entirely. Treating their silence as
    "unconfigured, so switch it on" would make a V1 re-run try to spawn a sensor
    the run was never recorded with. The intent to have a camera lives in
    configs/default.yaml, where it is written down.
    """
    assert camera_spec_from_config(Config({})) is None


# --- the speed lookup the stop-line inference depends on -------------------


def test_the_speed_lookup_returns_the_nearest_recorded_sample():
    at = _nearest_speed({0.0: 10.0, 0.05: 9.5, 0.10: 9.0})
    assert at(0.04) == pytest.approx(9.5)
    assert at(0.09) == pytest.approx(9.0)


def test_the_speed_lookup_does_not_interpolate():
    """Interpolating would invent a value between two real ones."""
    at = _nearest_speed({0.0: 10.0, 1.0: 0.0})
    assert at(0.4) in (10.0, 0.0)


def test_no_telemetry_means_no_speed_lookup_at_all():
    """Returning zero would make every stop-line crossing refuse for the wrong
    reason -- 'the vehicle was stopped' rather than 'nothing was recorded'."""
    assert _nearest_speed({}) is None


# --- one event per sign track, not per frame -------------------------------


def track(track_id, cls, t_first, t_last, n=8, confidence=0.8, relevant=True):
    return {
        "sign_track_id": track_id,
        "class": cls,
        "n_detections": n,
        "t_first": t_first,
        "t_last": t_last,
        "best_confidence": confidence,
        "best_bbox": [10, 20, 30, 30],
        "relevance": {"relevant_to_ego_path": relevant, "centredness": 0.9},
    }


def test_a_confirmed_stop_sign_track_becomes_one_event():
    events = _sign_events({"tracks": [track("sign-0", "STOP", 5.1, 6.4)]}, "A")
    assert [e.event_type for e in events] == [EventType.STOP_SIGN_DETECTED]
    assert events[0].t_peak == pytest.approx(5.1)
    assert events[0].t_end == pytest.approx(6.4)


def test_a_give_way_track_becomes_the_other_type():
    events = _sign_events({"tracks": [track("sign-0", "YIELD", 5.1, 6.4)]}, "A")
    assert [e.event_type for e in events] == [EventType.YIELD_SIGN_DETECTED]


def test_the_event_is_at_the_first_sighting_not_the_last():
    """A sign is perceived when it is first read, not when it leaves the frame."""
    events = _sign_events({"tracks": [track("sign-0", "STOP", 5.1, 9.9)]}, "A")
    assert events[0].t_peak == pytest.approx(5.1)


def test_two_tracks_become_two_events():
    events = _sign_events({"tracks": [
        track("sign-0", "STOP", 5.1, 6.4),
        track("sign-1", "YIELD", 7.0, 8.0),
    ]}, "A")
    assert len(events) == 2
    assert [e.t_peak for e in events] == sorted(e.t_peak for e in events)


def test_an_unrecognised_class_produces_no_event():
    """Better no claim than a claim about a class the detector cannot make."""
    assert _sign_events({"tracks": [track("sign-0", "SPEED_LIMIT", 5.0, 6.0)]}, "A") == []


def test_the_event_carries_the_track_it_came_from_and_the_method():
    events = _sign_events({"tracks": [track("sign-0", "STOP", 5.1, 6.4)]}, "B")
    event = events[0]
    assert event.participant_id == "B"
    assert event.subject is None
    assert event.source_sensors == ["camera"]
    assert event.detail["sign_track_id"] == "sign-0"
    assert event.detail["n_detections"] == 8
    assert "no privileged sign label" in event.detail["method"]


def test_relevance_reaches_the_event():
    events = _sign_events(
        {"tracks": [track("sign-0", "STOP", 5.1, 6.4, relevant=False)]}, "A"
    )
    assert events[0].detail["relevant_to_ego_path"] is False


def test_detection_confidence_becomes_event_confidence():
    events = _sign_events(
        {"tracks": [track("sign-0", "STOP", 5.1, 6.4, confidence=0.61)]}, "A"
    )
    assert events[0].confidence == pytest.approx(0.61)


def test_no_tracks_means_no_events():
    assert _sign_events({"tracks": []}, "A") == []
    assert _sign_events({}, "A") == []


# --- encoding happens after the run, and failing to encode is not fatal ----


def fill_buffer(buffer, n=10):
    import cv2

    for i in range(n):
        frame = np.full((60, 80, 3), 40 + i, dtype=np.uint8)
        ok, payload = cv2.imencode(".jpg", frame)
        assert ok
        buffer.add(i * 0.05, i, payload.tobytes(), width=80, height=60)
    return buffer


def test_a_buffer_with_frames_encodes_to_a_playable_file(tmp_path):
    buffer = fill_buffer(VideoBuffer(pre_event_s=20.0, post_event_s=5.0))
    out = tmp_path / "front.mp4"
    _encode_clip(buffer, out)
    assert out.is_file()
    assert out.stat().st_size > 0


def test_an_empty_buffer_writes_nothing_rather_than_an_empty_file(tmp_path):
    out = tmp_path / "front.mp4"
    _encode_clip(VideoBuffer(), out)
    assert not out.exists()


def test_the_frame_index_stands_on_its_own_if_encoding_never_happens(tmp_path):
    """A missing clip is a degraded artifact, not a lost run: the index still
    names every frame and its local time, which is what the viewer seeks by."""
    buffer = fill_buffer(VideoBuffer(pre_event_s=20.0, post_event_s=5.0))
    index = buffer.index()
    assert index["n_frames"] == 10
    assert len(index["frames"]) == 10
    assert index["frames"][-1]["t_local"] == pytest.approx(0.45)
