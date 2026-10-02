"""STOP / YIELD detection: synthetic shapes and real CARLA frames (tests/data/signs)."""

import json
import math
from pathlib import Path

import cv2
import numpy as np

from src.cdf.perception.traffic_signs import STOP, YIELD, SignDetector, SignTracker, detect_signs

DATA = Path(__file__).resolve().parent / "data" / "signs"
CFG = {"camera_fov_deg": 110.0}


def _blank(width=640, height=480):
    return np.full((height, width, 3), (110, 110, 112), dtype=np.uint8)


def _octagon(image=None, radius=40, centre=(320, 160), letters=True):
    image = _blank() if image is None else image
    cx, cy = centre
    points = [(cx + radius * math.cos(math.pi / 8 + i * math.pi / 4),
               cy + radius * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    cv2.fillPoly(image, [np.asarray(points, dtype=np.int32)], (200, 24, 30))
    if letters:
        # White letters filling the central band, as on CARLA's plates (stroke ~1/8 of the radius).
        for k in range(4):
            x = int(cx - 0.62 * radius + k * 0.34 * radius)
            cv2.rectangle(image, (x, int(cy - 0.25 * radius)), (x + max(2, int(0.2 * radius)), int(cy + 0.25 * radius)),
                          (245, 245, 245), -1)
    return image


def _yield(image=None, radius=45, centre=(320, 160)):
    image = _blank() if image is None else image
    cx, cy = centre
    outer = [(cx - radius, cy - radius * .87), (cx + radius, cy - radius * .87), (cx, cy + radius * .87)]
    cv2.fillPoly(image, [np.asarray(outer, dtype=np.int32)], (200, 24, 30))
    inner_r = radius * 0.62
    inner = [(cx - inner_r, cy - radius * .87 + radius * 0.22), (cx + inner_r, cy - radius * .87 + radius * 0.22),
             (cx, cy - radius * .87 + radius * 0.22 + inner_r * 1.6)]
    cv2.fillPoly(image, [np.asarray(inner, dtype=np.int32)], (245, 245, 245))
    return image


def _real(name):
    """(expected class, [(t, full-size RGB frame)]) of a real CARLA fixture pasted into a neutral canvas."""
    fixture = next(item for item in json.loads((DATA / "fixtures.json").read_text()) if item["name"] == name)
    width, height = fixture["image_size"]
    x0, y0 = fixture["offset"]
    frames = []
    for item in fixture["frames"]:
        crop = cv2.cvtColor(cv2.imread(str(DATA / item["file"])), cv2.COLOR_BGR2RGB)
        canvas = _blank(width, height)
        canvas[y0:y0 + crop.shape[0], x0:x0 + crop.shape[1]] = crop
        frames.append((item["t"], canvas))
    return fixture["expect"], frames


def test_stop_and_yield_shape_detection():
    assert SignDetector(CFG).detect(_octagon())[0].sign_class == STOP
    assert SignDetector(CFG).detect(_yield())[0].sign_class == YIELD


def test_a_red_octagon_without_letters_is_not_a_stop():
    # A solid red octagon-ish blob (tail light, brick block, red car part) has no white letters.
    assert SignDetector(CFG).detect(_octagon(letters=False)) == []


def test_a_shape_cut_by_the_image_border_is_rejected():
    image = _octagon(centre=(632, 160))  # the plate runs off the right edge
    assert SignDetector(CFG).detect(image) == []
    assert SignDetector(CFG).detect(_octagon(centre=(560, 160)))[0].sign_class == STOP


def test_a_red_rectangle_is_neither_stop_nor_yield():
    image = _blank()
    cv2.rectangle(image, (290, 130), (350, 190), (200, 24, 30), -1)
    cv2.putText(image, "AB", (297, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (245, 245, 245), 2)
    assert SignDetector(CFG).detect(image) == []


def test_one_sign_seen_for_many_frames_is_one_confirmed_track():
    frames = [(i * .1, i, _octagon(radius=14 + i * 2)) for i in range(10)]
    result = detect_signs(frames, CFG, image_width=640)
    assert result["n_tracks"] == 1
    track = result["tracks"][0]
    assert track["frame_confirmed"] == 2
    assert track["t_confirmed"] == .2


def test_real_stop_plate_is_detected_in_every_frame_and_tracked_as_one_sign():
    expect, frames = _real("stop_approach")
    detector, tracker = SignDetector(CFG), SignTracker(CFG)
    for k, (t, image) in enumerate(frames):
        found = detector.detect(image, frame=k, t=t)
        assert [d.sign_class for d in found] == [expect], t
        tracker.update(found)
    tracks = tracker.tracks(True)
    assert len(tracks) == 1 and tracks[0].sign_class == STOP and len(tracks[0].detections) == len(frames)
    assert tracks[0].growing
    # The plate is on the right of the road: about 15-30 deg off the camera axis while approached.
    assert 10.0 < tracks[0].min_bearing_deg < 30.0


def test_real_yield_sign_is_detected_and_tracked():
    expect, frames = _real("yield_approach")
    result = detect_signs([(t, k, image) for k, (t, image) in enumerate(frames)], CFG)
    assert expect == YIELD
    assert result["n_tracks"] == 1 and result["tracks"][0]["class"] == YIELD
    assert result["n_detections"] == len(frames)


def test_s15_red_board_at_the_image_border_is_not_a_stop():
    # The former detector confirmed a STOP on this red advertising board, cut by the
    # right image border, after S15's first collision.
    _, frames = _real("s15_board_at_border")
    detector = SignDetector(dict(CFG, camera_fov_deg=90.0))
    assert all(detector.detect(image) == [] for _, image in frames)


def test_brick_facade_is_not_a_stop():
    _, frames = _real("brick_facade")
    assert all(SignDetector(CFG).detect(image) == [] for _, image in frames)


def test_detections_far_apart_or_of_different_size_are_different_tracks():
    detector, tracker = SignDetector(CFG), SignTracker(CFG)
    tracker.update(detector.detect(_octagon(radius=20, centre=(120, 160)), frame=0, t=0.0))
    tracker.update(detector.detect(_octagon(radius=20, centre=(520, 160)), frame=1, t=0.1))  # 400 px away
    tracker.update(detector.detect(_octagon(radius=60, centre=(120, 160)), frame=2, t=0.2))  # 3x the size
    assert len(tracker.tracks(False)) == 3
