"""Stop-line detection and the crossing inference, on images built to order.

The interesting assertions are the refusals. A crossing is a claim about
something that left the frame, which is exactly the kind of claim a detector can
manufacture out of its own failures -- so the tests that matter are the ones where
the band disappears and no crossing is produced.
"""

from __future__ import annotations

import numpy as np
import pytest

from cdf.common.config import Config
from cdf.common.schemas import EventType
from cdf.local.stop_line_perception import StopLineDetector, detect_stop_lines

ROAD = 70
PAINT = 235


def road(width: int = 400, height: int = 300) -> np.ndarray:
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :] = ROAD
    return image


def transverse_band(image, row: int, thickness: int = 8,
                    x0_frac: float = 0.15, x1_frac: float = 0.85):
    """A stop line: broad, bright, lying across the direction of travel."""
    width = image.shape[1]
    x0, x1 = int(width * x0_frac), int(width * x1_frac)
    image[row:row + thickness, x0:x1] = PAINT
    return image


def lane_line(image, col: int, width_px: int = 6):
    """A lane line: narrow, running away from the camera."""
    image[:, col:col + width_px] = PAINT
    return image


def types_of(result) -> list:
    return [e.event_type.value for e in result["events"]]


# --- detecting the band ---------------------------------------------------


def test_a_transverse_band_low_in_the_frame_is_found():
    sighting = StopLineDetector().detect(transverse_band(road(), 240))
    assert sighting is not None
    assert sighting.row_centre == pytest.approx(244, abs=6)
    assert sighting.width_fraction == pytest.approx(0.70, abs=0.05)


def test_an_empty_road_yields_nothing():
    assert StopLineDetector().detect(road()) is None


def test_a_lane_line_is_not_a_stop_line():
    """The distinction the detector exists to make: longitudinal, not transverse."""
    assert StopLineDetector().detect(lane_line(road(), 200)) is None


def test_two_lane_lines_are_still_not_a_stop_line():
    image = lane_line(lane_line(road(), 120), 280)
    assert StopLineDetector().detect(image) is None


def test_a_narrow_transverse_mark_is_rejected():
    """A short white patch is not a line across the road."""
    image = transverse_band(road(), 240, x0_frac=0.45, x1_frac=0.55)
    assert StopLineDetector().detect(image) is None


def test_a_band_above_the_region_of_interest_is_ignored():
    """Sky and distant scenery are not stop lines."""
    assert StopLineDetector().detect(transverse_band(road(), 40)) is None


def test_a_large_bright_area_is_not_a_marking():
    image = road()
    image[170:290, :] = PAINT
    assert StopLineDetector().detect(image) is None


def test_the_lower_of_two_bands_is_the_one_reported():
    """The nearer line is the one the vehicle is about to reach."""
    image = transverse_band(transverse_band(road(), 180), 260)
    sighting = StopLineDetector().detect(image)
    assert sighting.row_centre > 250


# --- the approach, and the crossing --------------------------------------


def approach(rows, speed=8.0, n_after=0):
    """Frames with the band descending through the given rows."""
    frames = [
        (i * 0.05, i, transverse_band(road(), row)) for i, row in enumerate(rows)
    ]
    frames.extend(
        (len(rows) * 0.05 + i * 0.05, len(rows) + i, road())
        for i in range(n_after)
    )
    return frames


def moving(speed=8.0):
    return lambda t: speed


def test_a_descending_band_is_detected_and_then_crossed():
    frames = approach([170, 195, 220, 245, 270, 288], n_after=6)
    result = detect_stop_lines(frames, speed_at=moving(), participant_id="A")
    assert sorted(types_of(result)) == ["STOP_LINE_CROSSED", "STOP_LINE_DETECTED"]
    assert result["crossing"]["last_row"] > 280


def test_the_crossing_comes_after_the_last_sighting():
    frames = approach([170, 200, 230, 260, 288], n_after=4)
    result = detect_stop_lines(frames, speed_at=moving(), participant_id="A")
    crossed = [e for e in result["events"]
               if e.event_type == EventType.STOP_LINE_CROSSED][0]
    assert crossed.t_peak > result["sightings"][-1]["t_local"]


def test_a_band_lost_in_mid_frame_yields_no_crossing():
    """The likeliest explanation is that the detector lost it, not that the
    vehicle drove over it."""
    frames = approach([170, 185, 200, 210], n_after=8)
    result = detect_stop_lines(frames, speed_at=moving(), participant_id="A")
    assert types_of(result) == ["STOP_LINE_DETECTED"]
    assert "too high in the frame" in result["no_crossing_because"]


def test_a_stationary_vehicle_at_the_line_has_not_crossed_it():
    """Waiting at a stop line is the opposite of crossing it."""
    frames = approach([200, 240, 270, 288], n_after=6)
    result = detect_stop_lines(frames, speed_at=moving(0.0), participant_id="A")
    assert types_of(result) == ["STOP_LINE_DETECTED"]
    assert "not moving" in result["no_crossing_because"]


def test_without_speed_no_crossing_is_claimed():
    """The claim rests on the vehicle having moved, and guessing that is the one
    place this module could invent an event."""
    frames = approach([200, 240, 270, 288], n_after=6)
    result = detect_stop_lines(frames, speed_at=None, participant_id="A")
    assert types_of(result) == ["STOP_LINE_DETECTED"]
    assert "no speed was available" in result["no_crossing_because"]


def test_a_single_glimpse_is_not_a_stop_line():
    frames = [(0.0, 0, transverse_band(road(), 250))]
    result = detect_stop_lines(frames, speed_at=moving(), participant_id="A")
    assert result["events"] == []
    assert "more likely glare" in result["no_crossing_because"]


def test_the_sighting_threshold_is_configurable():
    frames = [
        (0.0, 0, transverse_band(road(), 250)),
        (0.05, 1, transverse_band(road(), 260)),
    ]
    lenient = Config({"perception": {"stop_lines": {"min_sightings": 2}}})
    result = detect_stop_lines(
        frames, speed_at=moving(), cfg=lenient, participant_id="A"
    )
    assert "STOP_LINE_DETECTED" in types_of(result)


def test_no_frames_produce_no_events_and_no_refusal():
    result = detect_stop_lines([], speed_at=moving(), participant_id="A")
    assert result["events"] == []
    assert result["no_crossing_because"] is None


# --- reporting contracts -------------------------------------------------


def test_the_method_says_it_read_no_map():
    result = detect_stop_lines(
        approach([170, 200, 230, 260, 288], n_after=4),
        speed_at=moving(), participant_id="A",
    )
    assert "No map geometry is read" in result["method"]
    crossed = [e for e in result["events"]
               if e.event_type == EventType.STOP_LINE_CROSSED][0]
    assert "no map geometry consulted" in crossed.detail["method"]


def test_the_crossing_carries_the_uncertainty_of_the_inference():
    """It is inferred from a disappearance, so it has a timing uncertainty."""
    result = detect_stop_lines(
        approach([170, 200, 230, 260, 288], n_after=4),
        speed_at=moving(), participant_id="A",
    )
    crossed = [e for e in result["events"]
               if e.event_type == EventType.STOP_LINE_CROSSED][0]
    assert crossed.detail["uncertainty_s"] > 0
    assert crossed.confidence < 1.0


def test_the_crossing_explains_what_it_was_inferred_from():
    result = detect_stop_lines(
        approach([170, 200, 230, 260, 288], n_after=4),
        speed_at=moving(), participant_id="A",
    )
    crossed = [e for e in result["events"]
               if e.event_type == EventType.STOP_LINE_CROSSED][0]
    assert "passed under the" in crossed.detail["inferred_from"]


def test_every_sighting_is_published_so_the_detection_can_be_checked():
    frames = approach([170, 200, 230, 260, 288], n_after=4)
    result = detect_stop_lines(frames, speed_at=moving(), participant_id="A")
    assert result["n_sightings"] == len(result["sightings"]) == 5
    rows = [s["row_centre"] for s in result["sightings"]]
    assert rows == sorted(rows)


def test_the_events_carry_the_camera_as_their_sensor():
    result = detect_stop_lines(
        approach([170, 200, 230, 260, 288], n_after=4),
        speed_at=moving(), participant_id="B",
    )
    for event in result["events"]:
        assert event.source_sensors == ["camera"]
        assert event.participant_id == "B"
        assert event.subject is None
