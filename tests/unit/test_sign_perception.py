"""The sign detector, on synthetic images whose answers are known by construction.

This tests the detector's *logic*, not its performance on CARLA. Those are
different claims and it matters which is being made: a red octagon drawn into a
numpy array is a fair test of whether the classifier separates octagons from
triangles and rejects other shapes, and no test at all of whether it finds a sign
at forty metres in shadow. The second question is answered by measuring precision
and recall against privileged truth on recorded runs, and reporting the numbers.

The tracking tests are the ones that protect the graph: one physical sign must
produce one event, whatever it produces per frame.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from cdf.common.config import Config
from cdf.local.sign_perception import (
    STOP, YIELD, SignDetector, SignTracker, detect_signs,
)

SIGN_RED = (200, 24, 30)
ROAD_GREY = (110, 110, 112)


def blank(width: int = 400, height: int = 300) -> np.ndarray:
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :] = ROAD_GREY
    return image


def polygon(image, points, colour=SIGN_RED):
    import cv2

    cv2.fillPoly(image, [np.array(points, dtype=np.int32)], colour)
    return image


def octagon(image, cx, cy, r, colour=SIGN_RED):
    """A regular octagon -- a stop sign face."""
    points = [
        (cx + r * math.cos(math.pi / 8 + i * math.pi / 4),
         cy + r * math.sin(math.pi / 8 + i * math.pi / 4))
        for i in range(8)
    ]
    return polygon(image, points, colour)


def down_triangle(image, cx, cy, r, colour=SIGN_RED):
    """A triangle pointing down -- a give-way sign face."""
    return polygon(image, [
        (cx - r, cy - r * 0.87), (cx + r, cy - r * 0.87), (cx, cy + r * 0.87),
    ], colour)


def up_triangle(image, cx, cy, r, colour=SIGN_RED):
    return polygon(image, [
        (cx - r, cy + r * 0.87), (cx + r, cy + r * 0.87), (cx, cy - r * 0.87),
    ], colour)


def circle(image, cx, cy, r, colour=SIGN_RED):
    import cv2

    cv2.circle(image, (int(cx), int(cy)), int(r), colour, -1)
    return image


def square(image, cx, cy, r, colour=SIGN_RED):
    import cv2

    cv2.rectangle(image, (int(cx - r), int(cy - r)), (int(cx + r), int(cy + r)),
                  colour, -1)
    return image


# --- what the detector should find ----------------------------------------


def test_a_stop_sign_is_found_and_classified():
    image = octagon(blank(), 200, 150, 40)
    found = SignDetector().detect(image)
    assert [d.sign_class for d in found] == [STOP]
    assert found[0].confidence > 0.5


def test_a_give_way_sign_is_found_and_classified():
    image = down_triangle(blank(), 200, 150, 45)
    found = SignDetector().detect(image)
    assert [d.sign_class for d in found] == [YIELD]


def test_the_bounding_box_locates_the_sign():
    image = octagon(blank(), 300, 100, 30)
    detection = SignDetector().detect(image)[0]
    cx, cy = detection.centre
    assert cx == pytest.approx(300, abs=6)
    assert cy == pytest.approx(100, abs=6)


def test_two_signs_in_one_frame_are_both_found():
    image = octagon(blank(640, 480), 150, 200, 35)
    image = down_triangle(image, 480, 200, 40)
    found = SignDetector().detect(image)
    assert sorted(d.sign_class for d in found) == [STOP, YIELD]


# --- what it should not find ----------------------------------------------


def test_an_empty_road_produces_nothing():
    assert SignDetector().detect(blank()) == []


def test_a_triangle_pointing_up_is_not_a_give_way_sign():
    """The orientation is the whole distinction; a warning sign points up."""
    found = SignDetector().detect(up_triangle(blank(), 200, 150, 45))
    assert YIELD not in [d.sign_class for d in found]


def test_a_red_square_is_not_a_sign():
    found = SignDetector().detect(square(blank(), 200, 150, 40))
    assert found == []


def test_a_sign_too_small_to_read_is_not_claimed():
    """Better to miss a distant sign than to guess at four pixels of red."""
    assert SignDetector().detect(octagon(blank(), 200, 150, 5)) == []


def test_a_grey_octagon_is_not_a_sign():
    image = octagon(blank(), 200, 150, 40, colour=(90, 90, 90))
    assert SignDetector().detect(image) == []


def test_a_long_thin_red_shape_is_rejected_on_aspect_ratio():
    image = polygon(blank(), [(40, 140), (360, 140), (360, 165), (40, 165)])
    assert SignDetector().detect(image) == []


# --- the colour band has to wrap around the hue origin --------------------


def test_both_sides_of_pure_red_are_detected():
    """Sign red sits either side of hue 0, so one band would miss half of it."""
    for colour in ((205, 20, 20), (200, 20, 55)):
        image = octagon(blank(), 200, 150, 40, colour=colour)
        found = SignDetector().detect(image)
        assert [d.sign_class for d in found] == [STOP], colour


# --- tracking: one sign, one event ----------------------------------------


def frames_of_an_approach(n=30, width=400, height=300):
    """A sign growing in the centre of frame, as if being driven towards."""
    out = []
    for i in range(n):
        r = 12 + i * 1.5
        image = octagon(blank(width, height), width // 2, height // 2, r)
        out.append((i * 0.05, i, image))
    return out


def test_thirty_frames_of_one_sign_produce_one_track():
    result = detect_signs(frames_of_an_approach(), image_width=400)
    assert result["n_tracks"] == 1
    assert result["n_detections"] > 20
    assert result["tracks"][0]["class"] == STOP


def test_the_track_records_when_the_sign_was_first_and_last_seen():
    result = detect_signs(frames_of_an_approach(), image_width=400)
    track = result["tracks"][0]
    assert track["t_first"] == pytest.approx(0.0, abs=0.2)
    assert track["t_last"] > track["t_first"]
    assert track["n_detections"] == len(track["detections"])


def test_a_single_frame_detection_is_not_confirmed():
    """One frame of red is far more likely to be a van than a sign."""
    frames = [(0.0, 0, octagon(blank(), 200, 150, 40))]
    result = detect_signs(frames, image_width=400)
    assert result["n_tracks"] == 0
    assert result["rejected_short_tracks"]


def test_short_tracks_are_listed_rather_than_dropped_silently():
    frames = [
        (0.0, 0, octagon(blank(), 200, 150, 40)),
        (0.05, 1, octagon(blank(), 201, 150, 40)),
    ]
    result = detect_signs(frames, image_width=400)
    assert result["n_tracks"] == 0
    assert result["rejected_short_tracks"][0]["n_detections"] == 2


def test_the_confirmation_threshold_is_configurable_and_reported():
    frames = [
        (0.0, 0, octagon(blank(), 200, 150, 40)),
        (0.05, 1, octagon(blank(), 201, 150, 40)),
    ]
    lenient = Config({"perception": {"signs": {"min_detections_per_track": 2}}})
    result = detect_signs(frames, cfg=lenient, image_width=400)
    assert result["n_tracks"] == 1
    assert result["min_detections_per_track"] == 2


def test_two_signs_at_different_places_stay_two_tracks():
    frames = []
    for i in range(10):
        image = octagon(blank(640, 480), 120, 240, 30 + i)
        image = octagon(image, 520, 240, 30 + i)
        frames.append((i * 0.05, i, image))
    result = detect_signs(frames, image_width=640)
    assert result["n_tracks"] == 2


def test_a_sign_that_disappears_and_returns_becomes_two_tracks():
    """A gap longer than the association window is a new sighting, not one."""
    frames = []
    for i in range(6):
        frames.append((i * 0.05, i, octagon(blank(), 200, 150, 40)))
    for i in range(6):
        frames.append((3.0 + i * 0.05, 100 + i, octagon(blank(), 200, 150, 40)))
    result = detect_signs(frames, image_width=400)
    assert result["n_tracks"] == 2


# --- relevance to the ego path, from the image alone ---------------------


def test_a_sign_growing_in_the_centre_is_judged_relevant():
    result = detect_signs(frames_of_an_approach(), image_width=400)
    relevance = result["tracks"][0]["relevance"]
    assert relevance["relevant_to_ego_path"] is True
    assert relevance["growing"] is True
    assert relevance["centredness"] > 0.9


def test_a_sign_at_constant_size_at_the_edge_is_not():
    """Visible, but not being approached and not addressed to this vehicle."""
    frames = [
        (i * 0.05, i, octagon(blank(640, 480), 40, 240, 28)) for i in range(20)
    ]
    result = detect_signs(frames, image_width=640)
    relevance = result["tracks"][0]["relevance"]
    assert relevance["relevant_to_ego_path"] is False
    assert relevance["growing"] is False
    assert relevance["centredness"] < 0.3


def test_relevance_says_it_used_no_map():
    result = detect_signs(frames_of_an_approach(), image_width=400)
    assert "No map is consulted" in result["tracks"][0]["relevance"]["basis"]


# --- the method has to be honest about itself ----------------------------


def test_the_method_is_described_and_names_no_privileged_source():
    result = detect_signs(frames_of_an_approach(), image_width=400)
    assert "no privileged sign labels" in result["method"]
    assert "no training data" in result["method"]


def test_detection_is_deterministic():
    """Same frames, same answer: a reproducible detector has no seed to set."""
    frames = frames_of_an_approach()
    first = detect_signs(frames, image_width=400)
    second = detect_signs(frames, image_width=400)
    assert first["tracks"] == second["tracks"]
    assert first["n_detections"] == second["n_detections"]
