"""Unit tests for the rolling forensic recorder and own-state derivation.

The properties under test are the ones the rest of the pipeline relies on:

* the recorder is **memory bounded** before a trigger (this is checked against a
  full 60 s run, not a toy sequence),
* the frozen window is exactly ``[t_trigger - pre_event_s, t_trigger + post_event_s]``
  and is never re-armed by a later trigger,
* what the recorder retains survives a serialisation round trip unchanged,
* dense radar frames are truncated to the *nearest* returns, and
* the derived motion state matches hand-computed finite differences.
"""

from __future__ import annotations

import math
from typing import List

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import load_participant
from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    ControlSample,
    LocalTriggerRecord,
    RadarDetection,
    RadarFrame,
    TrackSample,
    TriggerKind,
    make_track_id,
)
from cdf.local.own_state import (
    body_frame_acceleration,
    derive_motion,
    make_telemetry,
)
from cdf.local.recorder import RingBuffer, RollingRecorder

PID = "A"
RATE_HZ = 20.0
PERIOD_S = 1.0 / RATE_HZ
PRE_S = 20.0
POST_S = 5.0
EXPECTED_CAPACITY = 400  # 20 s * 20 Hz


def make_cfg(**recorder_overrides: float) -> Config:
    """A minimal in-memory configuration mirroring ``configs/default.yaml``."""
    recorder = {
        "pre_event_s": PRE_S,
        "post_event_s": POST_S,
        "sample_rate_hz": RATE_HZ,
        "max_radar_points_per_frame": 400,
    }
    recorder.update(recorder_overrides)
    return Config({"recorder": recorder})


def tel(i: int, participant_id: str = PID):
    """Telemetry sample number ``i`` of a 20 Hz trace starting at t = 0."""
    return make_telemetry(
        participant_id,
        i / RATE_HZ,
        i,
        x=float(i),
        y=0.0,
        z=0.0,
        yaw=0.0,
        vx=10.0,
    )


def ctrl(i: int, participant_id: str = PID) -> ControlSample:
    return ControlSample(
        t=i / RATE_HZ, frame=i, participant_id=participant_id, throttle=0.5
    )


def radar(i: int, n_detections: int = 3, participant_id: str = PID) -> RadarFrame:
    return RadarFrame(
        t=i / RATE_HZ,
        frame=i,
        participant_id=participant_id,
        sensor_id="front",
        detections=[
            RadarDetection(
                depth=10.0 + k, azimuth=0.01 * k, altitude=0.0, velocity=-3.0
            )
            for k in range(n_detections)
        ],
    )


def track(i: int, participant_id: str = PID) -> TrackSample:
    return TrackSample(
        t=i / RATE_HZ,
        frame=i,
        participant_id=participant_id,
        track_id=make_track_id(participant_id, 1),
        rel_x=20.0 - 0.1 * i,
        rel_y=0.0,
        range_m=20.0 - 0.1 * i,
        range_rate=-2.0,
    )


def times(samples) -> List[float]:
    return [float(s.t) for s in samples]


# ---------------------------------------------------------------------------
# RingBuffer
# ---------------------------------------------------------------------------


def test_ring_buffer_never_exceeds_capacity() -> None:
    buf: RingBuffer = RingBuffer(10)
    assert buf.capacity == 10

    max_seen = 0
    for i in range(1000):
        buf.append(tel(i))
        max_seen = max(max_seen, len(buf))

    assert max_seen == 10
    assert len(buf) == 10
    # The survivors are exactly the last ten appended items.
    assert [s.frame for s in buf.items()] == list(range(990, 1000))
    assert buf.oldest.frame == 990
    assert buf.newest.frame == 999

    buf.clear()
    assert len(buf) == 0
    assert buf.items() == []
    assert buf.oldest is None


def test_ring_buffer_drop_before_evicts_only_older_items() -> None:
    buf: RingBuffer = RingBuffer(100)
    for i in range(10):
        buf.append(tel(i))  # t = 0.00 .. 0.45

    removed = buf.drop_before(0.25)
    assert removed == 5
    assert len(buf) == 5
    assert times(buf.items())[0] == pytest.approx(0.25)
    # Idempotent: a second call with the same cutoff removes nothing.
    assert buf.drop_before(0.25) == 0


def test_ring_buffer_rejects_bad_capacity_and_untimed_items() -> None:
    with pytest.raises(ValueError):
        RingBuffer(0)
    with pytest.raises(ValueError):
        RingBuffer(-3)

    buf: RingBuffer = RingBuffer(4)
    buf.append(object())
    with pytest.raises(TypeError):
        buf.drop_before(1.0)


# ---------------------------------------------------------------------------
# Rolling (pre-trigger) behaviour: memory bound
# ---------------------------------------------------------------------------


def test_sixty_seconds_without_trigger_stays_at_pre_event_capacity() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    assert rec.capacity == EXPECTED_CAPACITY

    n_samples = int(60.0 * RATE_HZ)  # 1200 samples over 60 s
    max_seen = 0
    for i in range(n_samples):
        rec.record_telemetry(tel(i))
        rec.record_control(ctrl(i))
        rec.record_radar(radar(i))
        rec.record_tracks([track(i)])
        max_seen = max(max_seen, rec.counts()["telemetry"])

    assert not rec.triggered
    assert not rec.finished
    # Memory bound: never more than the pre-event capacity, on any stream.
    assert max_seen == EXPECTED_CAPACITY
    counts = rec.counts()
    for stream in ("telemetry", "controls", "radar", "tracks"):
        assert counts[stream] == EXPECTED_CAPACITY, stream

    ev = rec.to_evidence()
    assert len(ev.telemetry) == EXPECTED_CAPACITY
    assert ev.events == []


def test_retained_window_covers_the_last_pre_event_seconds() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    n_samples = int(60.0 * RATE_HZ)
    for i in range(n_samples):
        rec.record_telemetry(tel(i))

    ts = times(rec.to_evidence().telemetry)
    assert len(ts) == EXPECTED_CAPACITY
    # 1200 samples fed (t = 0.00 .. 59.95); the last 400 span t = 40.00 .. 59.95.
    assert ts[0] == pytest.approx(40.0)
    assert ts[-1] == pytest.approx(59.95)
    assert ts[-1] - ts[0] == pytest.approx(PRE_S - PERIOD_S)
    assert ts == sorted(ts)


def test_rolling_window_is_time_bounded_when_samples_arrive_faster() -> None:
    """A stream ticking at 4x the nominal rate is bounded in time, not only count."""
    rec = RollingRecorder(make_cfg(), PID)
    fast_period = PERIOD_S / 4.0
    n = int(40.0 / fast_period)
    for i in range(n):
        t = i * fast_period
        rec.record_telemetry(
            make_telemetry(PID, t, i, x=0.0, y=0.0, z=0.0, yaw=0.0, vx=10.0)
        )

    ts = times(rec.to_evidence().telemetry)
    t_last = ts[-1]
    # Count bound still holds ...
    assert len(ts) <= EXPECTED_CAPACITY
    # ... and the retained span never reaches back further than pre_event_s.
    assert t_last - ts[0] <= PRE_S + 1e-9
    assert ts[0] >= t_last - PRE_S - 1e-9


# ---------------------------------------------------------------------------
# Trigger: freeze, continue, finish
# ---------------------------------------------------------------------------


def feed(rec: RollingRecorder, first: int, last: int) -> None:
    """Feed telemetry/controls/radar/tracks for frames ``first``..``last``."""
    for i in range(first, last + 1):
        rec.record_telemetry(tel(i))
        rec.record_control(ctrl(i))
        rec.record_radar(radar(i))
        rec.record_tracks([track(i)])


def collision_at(i: int, participant_id: str = PID) -> LocalTriggerRecord:
    return LocalTriggerRecord(
        t=i / RATE_HZ,
        frame=i,
        participant_id=participant_id,
        kind=TriggerKind.COLLISION,
        collision_detected=True,
        impulse=420.0,
    )


def test_trigger_freezes_window_and_finishes_after_post_event_s() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)  # t = 0.0 .. 30.0

    rec.trigger(collision_at(600))  # t = 30.0
    assert rec.triggered
    assert rec.trigger_time == pytest.approx(30.0)
    assert rec.window.start == pytest.approx(10.0)
    assert rec.window.end == pytest.approx(35.0)
    assert not rec.finished

    frozen = times(rec.to_evidence().telemetry)
    # Nothing older than t_trigger - pre_event_s survives ...
    assert min(frozen) >= 10.0 - 1e-9
    # ... and the retained history really does start at the window boundary
    # (within one sampling period of it).
    assert min(frozen) <= 10.0 + PERIOD_S + 1e-9

    # Recording continues after the trigger.
    for i in range(601, 700):  # t = 30.05 .. 34.95
        feed(rec, i, i)
        assert not rec.finished, "finished before t_trigger + post_event_s"

    feed(rec, 700, 700)  # t = 35.0 exactly
    assert rec.finished


def test_post_trigger_samples_are_retained_and_nothing_in_the_window_is_evicted() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)
    rec.trigger(collision_at(600))
    feed(rec, 601, 700)  # through t = 35.0

    ev = rec.to_evidence()
    ts = times(ev.telemetry)
    assert ts == sorted(ts)

    # Every sample fed inside [30.0, 35.0] is still there: 101 samples at 20 Hz.
    in_window = [t for t in ts if 30.0 - 1e-9 <= t <= 35.0 + 1e-9]
    assert len(in_window) == 101
    assert in_window[0] == pytest.approx(30.0)
    assert in_window[-1] == pytest.approx(35.0)

    # The pre-event history is untouched too: 400 retained + 100 post-trigger.
    assert len(ts) == EXPECTED_CAPACITY + 100
    for stream in ("controls", "radar", "tracks"):
        assert rec.counts()[stream] == EXPECTED_CAPACITY + 100, stream


def test_samples_past_the_window_end_are_not_retained() -> None:
    """The bound survives the freeze: post-window data is dropped, not buffered."""
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)
    rec.trigger(collision_at(600))
    feed(rec, 601, 700)  # closes the window at t = 35.0

    before = rec.counts()["telemetry"]
    for i in range(701, 900):  # t = 35.05 .. 44.95, all outside the window
        rec.record_telemetry(tel(i))
    assert rec.counts()["telemetry"] == before
    assert rec.meta()["recorder"]["samples_outside_window_discarded"] == 199
    assert max(times(rec.to_evidence().telemetry)) == pytest.approx(35.0)


def test_second_trigger_does_not_reset_the_window() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)
    rec.trigger(
        LocalTriggerRecord(
            t=30.0, frame=600, participant_id=PID, kind=TriggerKind.NEAR_MISS
        )
    )
    feed(rec, 601, 640)  # t = 30.05 .. 32.0
    rec.trigger(collision_at(640))  # second trigger at t = 32.0

    # Window still anchored on the first trigger.
    assert rec.trigger_time == pytest.approx(30.0)
    assert rec.window.start == pytest.approx(10.0)
    assert rec.window.end == pytest.approx(35.0)

    feed(rec, 641, 700)  # through t = 35.0
    assert rec.finished, "a re-armed window would only finish at 32.0 + 5.0 = 37.0"

    ev = rec.to_evidence()
    assert [t.kind for t in ev.triggers] == [TriggerKind.NEAR_MISS, TriggerKind.COLLISION]
    assert min(times(ev.telemetry)) >= 10.0 - 1e-9
    assert max(times(ev.telemetry)) == pytest.approx(35.0)


def test_recorder_rejects_records_owned_by_another_participant() -> None:
    rec = RollingRecorder(make_cfg(), PID)
    with pytest.raises(ValueError):
        rec.record_telemetry(tel(0, participant_id="B"))
    with pytest.raises(ValueError):
        rec.record_control(ctrl(0, participant_id="B"))
    with pytest.raises(ValueError):
        rec.record_radar(radar(0, participant_id="B"))
    with pytest.raises(ValueError):
        rec.record_tracks([track(0, participant_id="B")])
    with pytest.raises(ValueError):
        rec.trigger(collision_at(0, participant_id="B"))


# ---------------------------------------------------------------------------
# Streams that produce several records per simulation step
# ---------------------------------------------------------------------------


def test_multi_record_streams_retain_the_full_pre_event_window() -> None:
    """A stream emitting N records per step must still cover ``pre_event_s``.

    The tracker emits one :class:`TrackSample` per *track* per step (up to
    ``radar_processing.tracking.max_tracks``) and a vehicle may carry several
    radars. Sizing those buffers at ``pre_event_s * sample_rate_hz`` *records*
    would silently shorten their history -- with 8 live tracks the retained
    track window would cover 2.5 s instead of 20 s -- while every count-based
    assertion in this file kept passing, because telemetry and controls really
    do produce one record per step. The track stream is the interaction
    evidence, so that loss would be invisible and fatal.
    """
    n_tracks = 8
    n_radars = 2
    cfg = Config(
        {
            "recorder": {
                "pre_event_s": PRE_S,
                "post_event_s": POST_S,
                "sample_rate_hz": RATE_HZ,
                "max_radar_points_per_frame": 400,
            },
            "radar_processing": {"tracking": {"max_tracks": n_tracks}},
            "radar": {"sensors": [{"sensor_id": "front"}, {"sensor_id": "rear"}]},
        }
    )
    rec = RollingRecorder(cfg, PID)

    # The per-step capacity is still the configured policy; the per-stream
    # capacities scale with what each stream actually produces per step.
    assert rec.capacity == EXPECTED_CAPACITY
    assert rec.stream_capacities() == {
        "telemetry": EXPECTED_CAPACITY,
        "controls": EXPECTED_CAPACITY,
        "radar": EXPECTED_CAPACITY * n_radars,
        "tracks": EXPECTED_CAPACITY * n_tracks,
    }

    max_seen = 0
    for i in range(int(60.0 * RATE_HZ)):  # 60 s, three times the window
        rec.record_telemetry(tel(i))
        for sensor in ("front", "rear"):
            frame = radar(i)
            frame.sensor_id = sensor
            rec.record_radar(frame)
        rec.record_tracks(
            [
                TrackSample(
                    t=i / RATE_HZ,
                    frame=i,
                    participant_id=PID,
                    track_id=make_track_id(PID, k),
                    range_m=20.0,
                )
                for k in range(n_tracks)
            ]
        )
        max_seen = max(max_seen, rec.counts()["tracks"])

    ev = rec.to_evidence()

    # Memory is still bounded -- by the honest bound, not by a bound that
    # happens to be met by throwing evidence away.
    assert max_seen == EXPECTED_CAPACITY * n_tracks
    assert rec.counts()["tracks"] == EXPECTED_CAPACITY * n_tracks
    assert rec.counts()["radar"] == EXPECTED_CAPACITY * n_radars

    # ... and every stream covers the same last 20 s of simulation time.
    for stream in ("telemetry", "radar", "tracks"):
        ts = times(getattr(ev, stream))
        assert ts[0] == pytest.approx(40.0), stream
        assert ts[-1] == pytest.approx(59.95), stream
        assert ts[-1] - ts[0] == pytest.approx(PRE_S - PERIOD_S), stream

    # Each individual track kept its whole history, not a shared 400-sample slot.
    per_track = {tid: 0 for tid in {s.track_id for s in ev.tracks}}
    for s in ev.tracks:
        per_track[s.track_id] += 1
    assert len(per_track) == n_tracks
    assert set(per_track.values()) == {EXPECTED_CAPACITY}


def test_post_trigger_storage_is_capped_when_a_stream_runs_fast() -> None:
    """Freezing the window must not make post-event storage unbounded.

    Nothing already retained may be evicted after the trigger, but a sensor
    callback that fires faster than ``sample_rate_hz`` (or twice for the same
    timestamp) must not be able to grow the post-event lists without limit --
    that would defeat the whole point of the recorder inside the simulation loop.
    """
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)
    rec.trigger(collision_at(600))

    post_capacity = int(round(POST_S * RATE_HZ)) + 1  # 101 samples of headroom
    fast_period = PERIOD_S / 4.0
    n_fast = int(POST_S / fast_period)  # 400 in-window samples at 4x the rate
    for k in range(1, n_fast + 1):
        t = 30.0 + k * fast_period
        rec.record_telemetry(
            make_telemetry(PID, t, 600 + k, x=0.0, y=0.0, z=0.0, yaw=0.0, vx=10.0)
        )

    counts = rec.counts()
    assert counts["telemetry"] == EXPECTED_CAPACITY + post_capacity
    meta = rec.meta()["recorder"]
    assert meta["samples_over_capacity_discarded"] == n_fast - post_capacity

    ts = times(rec.to_evidence().telemetry)
    # The impact itself and the moments right after it are what survive: the
    # tail is refused, never the beginning of the post-event window.
    assert ts[0] >= 10.0 - 1e-9
    assert 30.0 in ts
    assert ts[-1] == pytest.approx(30.0 + post_capacity * fast_period)

    # Discarded records still advance the observed clock, so the driving loop
    # can still tell that the run is over.
    assert rec.last_time == pytest.approx(35.0)
    assert rec.finished


# ---------------------------------------------------------------------------
# Radar point cap
# ---------------------------------------------------------------------------


def test_radar_frames_are_truncated_keeping_the_nearest_detections() -> None:
    cap = 5
    rec = RollingRecorder(make_cfg(max_radar_points_per_frame=cap), PID)

    dense = RadarFrame(
        t=0.0,
        frame=0,
        participant_id=PID,
        sensor_id="front",
        # Depths 20.0 down to 1.0: the nearest returns arrive last, so a naive
        # "keep the first N" truncation would keep exactly the wrong ones.
        detections=[
            RadarDetection(depth=20.0 - k, azimuth=0.0, altitude=0.0, velocity=-1.0)
            for k in range(20)
        ],
    )
    rec.record_radar(dense)

    stored = rec.to_evidence().radar[0]
    assert len(stored.detections) == cap
    assert sorted(d.depth for d in stored.detections) == [1.0, 2.0, 3.0, 4.0, 5.0]
    assert rec.meta()["recorder"]["radar_points_discarded"] == 15
    # The caller's frame is not mutated.
    assert len(dense.detections) == 20


def test_radar_frames_below_the_cap_are_kept_verbatim() -> None:
    rec = RollingRecorder(make_cfg(max_radar_points_per_frame=10), PID)
    frame = radar(0, n_detections=4)
    rec.record_radar(frame)
    stored = rec.to_evidence().radar[0]
    assert [d.depth for d in stored.detections] == [10.0, 11.0, 12.0, 13.0]
    assert rec.meta()["recorder"]["radar_points_discarded"] == 0


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def test_persist_round_trip_preserves_counts_and_timestamps(tmp_path) -> None:
    rec = RollingRecorder(make_cfg(), PID)
    feed(rec, 0, 600)
    rec.trigger(collision_at(600))
    feed(rec, 601, 700)

    layout = RunLayout.from_run_dir(tmp_path / "S01_rear_end" / "seed_000")
    written = rec.persist(layout)
    loaded = load_participant(layout, PID, with_radar=True)

    assert loaded.participant_id == written.participant_id
    for stream in ("telemetry", "controls", "radar", "tracks", "triggers"):
        a = getattr(written, stream)
        b = getattr(loaded, stream)
        assert len(a) == len(b), stream
        assert float(a[0].t) == pytest.approx(float(b[0].t)), stream
        assert float(a[-1].t) == pytest.approx(float(b[-1].t)), stream

    assert loaded.summary()["n_telemetry"] == EXPECTED_CAPACITY + 100
    assert loaded.span()[0] == pytest.approx(written.span()[0])
    assert loaded.span()[1] == pytest.approx(35.0)

    # Radar payloads survive intact, capped list included.
    assert sum(len(f.detections) for f in loaded.radar) == sum(
        len(f.detections) for f in written.radar
    )
    trig = loaded.collision_trigger()
    assert trig is not None
    assert trig.t == pytest.approx(30.0)
    assert trig.impulse == pytest.approx(420.0)

    # The retention policy travels with the evidence.
    meta = loaded.meta["recorder"]
    assert meta["pre_event_s"] == pytest.approx(PRE_S)
    assert meta["post_event_s"] == pytest.approx(POST_S)
    assert meta["window_start"] == pytest.approx(10.0)
    assert meta["window_end"] == pytest.approx(35.0)
    assert meta["triggered"] is True
    assert loaded.events == []


def test_capacity_comes_from_the_shipped_default_config() -> None:
    """No magic numbers: the 400-sample bound is the configured policy."""
    cfg = load_run_config()
    rec = RollingRecorder(cfg, PID)
    assert rec.pre_event_s == pytest.approx(20.0)
    assert rec.post_event_s == pytest.approx(5.0)
    assert rec.sample_rate_hz == pytest.approx(20.0)
    assert rec.capacity == EXPECTED_CAPACITY
    assert rec.max_radar_points_per_frame == 400


def test_invalid_recorder_configuration_fails_loudly() -> None:
    with pytest.raises(ValueError):
        RollingRecorder(make_cfg(pre_event_s=0.0), PID)
    with pytest.raises(ValueError):
        RollingRecorder(make_cfg(sample_rate_hz=0.0), PID)
    with pytest.raises(ValueError):
        RollingRecorder(make_cfg(post_event_s=-1.0), PID)
    with pytest.raises(ValueError):
        RollingRecorder(make_cfg(max_radar_points_per_frame=0), PID)


# ---------------------------------------------------------------------------
# own_state
# ---------------------------------------------------------------------------


def test_body_frame_acceleration_rotates_into_the_heading_frame() -> None:
    # Heading along +x: the body frame coincides with the world frame.
    assert body_frame_acceleration(3.0, -1.0, 0.0) == pytest.approx((3.0, -1.0))

    # Heading along +y (CARLA yaw = 90 deg): world +y is now straight ahead.
    lon, lat = body_frame_acceleration(0.0, 2.0, 90.0)
    assert lon == pytest.approx(2.0)
    assert lat == pytest.approx(0.0, abs=1e-12)

    # Same heading, world acceleration pointing at -x: that is to the right.
    lon, lat = body_frame_acceleration(-2.0, 0.0, 90.0)
    assert lon == pytest.approx(0.0, abs=1e-12)
    assert lat == pytest.approx(2.0)

    # Reversed heading flips both axes.
    assert body_frame_acceleration(1.0, 1.0, 180.0) == pytest.approx((-1.0, -1.0))

    # Rotation preserves magnitude for an arbitrary heading.
    lon, lat = body_frame_acceleration(1.3, -2.7, 37.5)
    assert math.hypot(lon, lat) == pytest.approx(math.hypot(1.3, -2.7))


def test_derive_motion_finite_differences_velocity_and_yaw() -> None:
    prev = make_telemetry(PID, 1.0, 20, x=0.0, y=0.0, z=0.0, yaw=0.0, vx=10.0, vy=0.0)
    got = derive_motion(prev, {"yaw": 0.0, "vx": 8.0, "vy": 0.0}, 0.5)

    assert got["ax"] == pytest.approx(-4.0)  # (8 - 10) / 0.5
    assert got["ay"] == pytest.approx(0.0)
    assert got["accel_long"] == pytest.approx(-4.0)
    assert got["accel_lat"] == pytest.approx(0.0)
    assert got["speed"] == pytest.approx(8.0)
    assert got["yaw_rate"] == pytest.approx(0.0)


def test_derive_motion_projects_into_the_body_frame_while_turning() -> None:
    # Driving along +y (yaw 90) and decelerating: world -y is a braking force.
    prev = make_telemetry(PID, 2.0, 40, x=0.0, y=0.0, z=0.0, yaw=90.0, vx=0.0, vy=12.0)
    got = derive_motion(prev, {"yaw": 90.0, "vx": 0.0, "vy": 9.0}, 0.25)

    assert got["ay"] == pytest.approx(-12.0)  # (9 - 12) / 0.25
    assert got["accel_long"] == pytest.approx(-12.0)
    assert got["accel_lat"] == pytest.approx(0.0, abs=1e-9)
    assert got["speed"] == pytest.approx(9.0)


def test_derive_motion_wraps_the_yaw_difference() -> None:
    prev = make_telemetry(PID, 0.0, 0, x=0.0, y=0.0, z=0.0, yaw=179.0)
    got = derive_motion(prev, {"yaw": -179.0, "vx": 0.0, "vy": 0.0}, 0.1)
    # +2 deg across the wrap, not -358 deg.
    assert got["yaw_rate"] == pytest.approx(20.0)


def test_derive_motion_prefers_supplied_measurements() -> None:
    prev = make_telemetry(PID, 0.0, 0, x=0.0, y=0.0, z=0.0, yaw=0.0, vx=10.0)
    got = derive_motion(
        prev,
        {"yaw": 0.0, "vx": 8.0, "vy": 0.0, "ax": 1.5, "ay": -0.5, "yaw_rate": 4.0},
        0.5,
    )
    assert got["ax"] == pytest.approx(1.5)
    assert got["ay"] == pytest.approx(-0.5)
    assert got["accel_long"] == pytest.approx(1.5)
    assert got["accel_lat"] == pytest.approx(-0.5)
    assert got["yaw_rate"] == pytest.approx(4.0)


def test_derive_motion_first_sample_has_no_derivatives() -> None:
    got = derive_motion(None, {"yaw": 12.0, "vx": 3.0, "vy": 4.0}, 0.05)
    assert got["ax"] == 0.0
    assert got["ay"] == 0.0
    assert got["accel_long"] == 0.0
    assert got["accel_lat"] == 0.0
    assert got["yaw_rate"] == 0.0
    assert got["speed"] == pytest.approx(5.0)


def test_derive_motion_rejects_out_of_order_or_incomplete_input() -> None:
    prev = make_telemetry(PID, 1.0, 20, x=0.0, y=0.0, z=0.0, yaw=0.0)
    with pytest.raises(ValueError):
        derive_motion(prev, {"yaw": 0.0}, -0.05)
    with pytest.raises(ValueError):
        derive_motion(prev, {"vx": 1.0}, 0.05)


def test_make_telemetry_fills_speed_and_body_frame_accelerations() -> None:
    s = make_telemetry(
        PID,
        3.25,
        65,
        x=12.0,
        y=-4.0,
        z=0.5,
        yaw=90.0,
        vx=3.0,
        vy=4.0,
        ax=0.0,
        ay=-6.0,
        yaw_rate=2.5,
    )
    assert s.participant_id == PID
    assert s.t == pytest.approx(3.25)
    assert s.frame == 65
    assert s.speed == pytest.approx(5.0)
    assert s.accel_long == pytest.approx(-6.0)
    assert s.accel_lat == pytest.approx(0.0, abs=1e-12)
    assert s.yaw_rate == pytest.approx(2.5)


def test_derive_motion_output_feeds_make_telemetry() -> None:
    """The two helpers compose: derived world accelerations round-trip."""
    prev = make_telemetry(PID, 0.0, 0, x=0.0, y=0.0, z=0.0, yaw=0.0, vx=10.0)
    motion = derive_motion(prev, {"yaw": 0.0, "vx": 4.0, "vy": 0.0}, 0.2)
    s = make_telemetry(
        PID,
        0.2,
        4,
        x=1.4,
        y=0.0,
        z=0.0,
        yaw=0.0,
        vx=4.0,
        vy=0.0,
        ax=motion["ax"],
        ay=motion["ay"],
        yaw_rate=motion["yaw_rate"],
    )
    assert s.accel_long == pytest.approx(motion["accel_long"])
    assert s.accel_lat == pytest.approx(motion["accel_lat"])
    assert s.speed == pytest.approx(motion["speed"])
    assert s.accel_long == pytest.approx(-30.0)  # (4 - 10) / 0.2
