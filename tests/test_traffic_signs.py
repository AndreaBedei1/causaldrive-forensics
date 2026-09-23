import math

import cv2
import numpy as np

from src.cdf.perception.traffic_signs import STOP, YIELD, SignDetector, detect_signs


def _blank():
    image = np.full((300, 400, 3), (110, 110, 112), dtype=np.uint8)
    return image


def _octagon(image=None, radius=40):
    image = _blank() if image is None else image
    points = [(200 + radius * math.cos(math.pi / 8 + i * math.pi / 4),
               150 + radius * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    cv2.fillPoly(image, [np.asarray(points, dtype=np.int32)], (200, 24, 30))
    return image


def _yield(image=None, radius=45):
    image = _blank() if image is None else image
    points = [(200 - radius, 150 - radius * .87), (200 + radius, 150 - radius * .87),
              (200, 150 + radius * .87)]
    cv2.fillPoly(image, [np.asarray(points, dtype=np.int32)], (200, 24, 30))
    return image


def test_stop_and_yield_shape_detection():
    assert SignDetector().detect(_octagon())[0].sign_class == STOP
    assert SignDetector().detect(_yield())[0].sign_class == YIELD


def test_one_sign_seen_for_many_frames_is_one_confirmed_track():
    frames = [(i * .1, i, _octagon(radius=12 + i * 1.5)) for i in range(10)]
    result = detect_signs(frames, image_width=400)
    assert result["n_tracks"] == 1
    track = result["tracks"][0]
    assert track["frame_confirmed"] == 2
    assert track["t_confirmed"] == .2
