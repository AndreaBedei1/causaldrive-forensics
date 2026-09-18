"""The camera buffer has to stay bounded, and keep the right 25 seconds.

Section 46 asks for the 20 + 5 window, the timestamps and the frame index. The
subtle requirement is the *shape* of the window: it is not a 25 s sliding buffer.
A sliding buffer would have thrown away the 20 s before the impact by the time
the run ended, which is the only part anybody wants.
"""

from __future__ import annotations

import pytest

from cdf.local.video_buffer import VideoBuffer


def fill(buffer: VideoBuffer, t0: float, t1: float, dt: float = 0.05,
         size: int = 100) -> int:
    """Feed frames at a steady rate, returning how many were accepted."""
    accepted = 0
    n = int(round((t1 - t0) / dt))
    for i in range(n):
        t = t0 + i * dt
        if buffer.add(t, int(t / dt), b"x" * size, width=800, height=600):
            accepted += 1
    return accepted


# --- the bound ------------------------------------------------------------


def test_before_any_event_the_buffer_holds_only_the_pre_event_window():
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 60.0)
    span = buffer.span()
    assert span[1] - span[0] <= 20.0 + 0.05
    assert span[1] == pytest.approx(59.95)


def test_memory_does_not_grow_with_run_length():
    """A ten-minute run must cost no more than a one-minute one."""
    short = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(short, 0.0, 60.0)
    long = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(long, 0.0, 600.0)
    assert long.nbytes == short.nbytes
    assert len(long) == len(short)


def test_the_frame_count_backstop_holds_even_with_a_broken_clock():
    """A caller feeding frames with a stuck timestamp must not exhaust memory."""
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0, max_frames=100)
    for i in range(5000):
        buffer.add(7.0, i, b"x" * 10)     # time never advances
    assert len(buffer) == 100


# --- the shape of the window ---------------------------------------------


def test_the_twenty_seconds_before_the_event_survive_to_the_end_of_the_run():
    """The requirement a sliding window would quietly fail."""
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 40.0)
    buffer.mark_event(40.0)
    fill(buffer, 40.0, 60.0)          # the run continues well past the event
    span = buffer.span()
    assert span[0] == pytest.approx(20.0, abs=0.1)
    assert span[1] == pytest.approx(45.0, abs=0.1)


def test_recording_stops_five_seconds_after_the_event():
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 30.0)
    buffer.mark_event(30.0)
    accepted = fill(buffer, 30.0, 45.0)
    assert buffer.closed is True
    # 5 s of frames at 20 Hz, then refusals.
    assert accepted == pytest.approx(100, abs=2)
    assert buffer.index()["n_refused_after_window_closed"] > 0


def test_a_second_trigger_does_not_extend_the_tail():
    """A chain collision fires several triggers; the tail must stay bounded."""
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 30.0)
    buffer.mark_event(30.0)
    fill(buffer, 30.0, 33.0)
    buffer.mark_event(33.0)           # second impact in the chain
    fill(buffer, 33.0, 45.0)
    assert buffer.span()[1] == pytest.approx(35.0, abs=0.1)


def test_the_event_time_is_the_one_the_window_is_measured_from():
    buffer = VideoBuffer(pre_event_s=10.0, post_event_s=2.0)
    fill(buffer, 0.0, 25.0)
    buffer.mark_event(25.0)
    fill(buffer, 25.0, 30.0)
    index = buffer.index()
    assert index["event_t_local"] == pytest.approx(25.0)
    assert index["t_first"] == pytest.approx(15.0, abs=0.1)
    assert index["t_last"] == pytest.approx(27.0, abs=0.1)


def test_a_run_with_no_event_keeps_rolling_and_never_closes():
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 40.0)
    assert buffer.triggered is False
    assert buffer.closed is False
    assert buffer.index()["event_t_local"] is None


# --- the index ------------------------------------------------------------


def test_every_frame_is_indexed_with_its_local_time():
    buffer = VideoBuffer(pre_event_s=5.0, post_event_s=1.0)
    fill(buffer, 0.0, 3.0)
    index = buffer.index()
    assert index["n_frames"] == len(index["frames"])
    assert index["frames"][0]["i"] == 0
    assert index["frames"][-1]["t_local"] == pytest.approx(2.95)


def test_the_index_says_whose_clock_it_is():
    buffer = VideoBuffer(participant_id="B", sensor_id="front")
    fill(buffer, 0.0, 2.0)
    index = buffer.index()
    assert index["participant_id"] == "B"
    assert index["clock"] == "participant-local"


def test_the_index_reports_what_the_window_discarded():
    """A buffer that silently dropped frames would look like a short recording."""
    buffer = VideoBuffer(pre_event_s=2.0, post_event_s=1.0)
    fill(buffer, 0.0, 10.0)
    index = buffer.index()
    assert index["n_accepted"] == 200
    assert index["n_evicted_by_window"] > 150
    assert index["n_frames"] < index["n_accepted"]


def test_an_event_time_maps_to_a_frame_so_a_viewer_can_seek():
    buffer = VideoBuffer(pre_event_s=20.0, post_event_s=5.0)
    fill(buffer, 0.0, 10.0)
    i = buffer.frame_at(8.42)
    assert i is not None
    assert buffer.frames[i].t == pytest.approx(8.40, abs=0.05)


def test_seeking_an_empty_buffer_returns_nothing_rather_than_zero():
    assert VideoBuffer().frame_at(3.0) is None


def test_the_index_of_an_empty_buffer_is_still_well_formed():
    index = VideoBuffer(participant_id="C").index()
    assert index["n_frames"] == 0
    assert index["t_first"] is None
    assert index["frames"] == []


def test_frame_dimensions_reach_the_index():
    buffer = VideoBuffer()
    fill(buffer, 0.0, 1.0)
    index = buffer.index()
    assert (index["width"], index["height"]) == (800, 600)
