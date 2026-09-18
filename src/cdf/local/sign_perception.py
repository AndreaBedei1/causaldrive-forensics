"""Reading traffic signs off the camera, rather than asking the simulator.

CARLA will tell you exactly which sign governs a vehicle. Using that would make
the traffic-control layer trivially correct and completely uninformative: the
question this project asks is what a vehicle can establish from its own sensors,
and a vehicle with a map oracle is not answering it. So signs are detected from
the image, and the detector's mistakes are part of the result.

The method, and what it is not
------------------------------

Colour and shape, deterministic, with no training data and no learned weights:
threshold for sign red in HSV, clean up the mask, take contours, and classify by
polygon approximation. A stop sign is an octagon that nearly fills its own convex
hull; a give-way sign is a triangle pointing down. Both are distinctive enough in
this geometry that a classical detector is the honest choice -- it is fully
reproducible, has no training set to leak from, and its failure modes are legible.

It is not a good general-purpose sign detector and is not offered as one. It will
miss signs at distance, in shadow, and at sharp angles, and it will fire on other
red octagonal things. That is why :mod:`cdf.evaluation` measures its precision and
recall against privileged truth and reports the numbers rather than asserting that
perception works.

Tracking, and why it matters more than detection
------------------------------------------------

A sign is in view for tens of frames. Emitting one event per frame would put
dozens of ``STOP_SIGN_DETECTED`` nodes in the graph for one physical sign, which
would wreck precision against a reference that has one -- and would be wrong
anyway, because seeing a sign for two seconds is one perception, not forty. So
detections are associated across frames into tracks by class and image position,
and a track yields exactly one event, at the moment the evidence for it first
becomes good enough.

Relevance
---------

A sign at the edge of frame on a cross street is visible but not addressed to
this vehicle. Relevance is judged from the image alone: how centred the sign is,
and whether it is growing -- a sign being approached subtends a larger angle each
frame. Crude, and deliberately so; the alternative is the map, which is the thing
being avoided.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config

LOGGER = logging.getLogger(__name__)

__all__ = [
    "SignDetection",
    "SignTrack",
    "SignDetector",
    "SignTracker",
    "detect_signs",
]

#: The classes this detector distinguishes. The brief asks for these two at
#: minimum; nothing else is attempted, because a class the detector cannot tell
#: apart from another is worse than a class it does not claim.
STOP = "STOP"
YIELD = "YIELD"


def _cv2() -> Any:
    """Import OpenCV, with a message that says what is missing and why.

    Imported lazily, like the CARLA API, so that the rest of the package remains
    importable on a machine that only reads artifacts.
    """
    try:
        import cv2  # noqa: WPS433
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise ImportError(
            "sign perception needs OpenCV (opencv-python). It is a runtime "
            "dependency of the camera pipeline only; analysis of already "
            "recorded artifacts does not require it"
        ) from exc
    return cv2


@dataclass
class SignDetection:
    """One sign found in one frame."""

    frame: int
    t: float
    sign_class: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    """``(x, y, w, h)`` in image pixels."""
    n_vertices: int = 0
    fill_ratio: float = 0.0
    """Contour area over convex-hull area. Near 1 for a solid sign face."""
    redness: float = 0.0
    """Fraction of the bounding box that passed the colour threshold."""

    @property
    def area(self) -> int:
        return int(self.bbox[2] * self.bbox[3])

    @property
    def centre(self) -> Tuple[float, float]:
        x, y, w, h = self.bbox
        return (x + w / 2.0, y + h / 2.0)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "t_local": round(self.t, 4),
            "class": self.sign_class,
            "confidence": round(self.confidence, 4),
            "bbox": list(self.bbox),
            "n_vertices": self.n_vertices,
            "fill_ratio": round(self.fill_ratio, 4),
            "redness": round(self.redness, 4),
        }


@dataclass
class SignTrack:
    """One physical sign, seen over several frames."""

    track_id: str
    sign_class: str
    detections: List[SignDetection] = field(default_factory=list)

    @property
    def t_first(self) -> float:
        return self.detections[0].t

    @property
    def t_last(self) -> float:
        return self.detections[-1].t

    @property
    def best(self) -> SignDetection:
        return max(self.detections, key=lambda d: d.confidence)

    @property
    def growing(self) -> bool:
        """Whether the sign subtends a larger angle over the track.

        A sign being approached grows. One on a cross street, or receding behind
        the vehicle, does not. Compared between the first and last third of the
        track rather than adjacent frames, which would be dominated by noise.
        """
        if len(self.detections) < 4:
            return False
        third = max(1, len(self.detections) // 3)
        early = sum(d.area for d in self.detections[:third]) / third
        late = sum(d.area for d in self.detections[-third:]) / third
        return late > early * 1.15

    def centredness(self, image_width: int) -> float:
        """How close to the centre of frame the sign was, at its clearest, in [0, 1]."""
        if image_width <= 0:
            return 0.0
        x, _ = self.best.centre
        return float(max(0.0, 1.0 - abs(x - image_width / 2.0) / (image_width / 2.0)))

    def relevance(self, image_width: int) -> Dict[str, Any]:
        """Whether this sign plausibly governs this vehicle's path.

        Judged from the image alone. The map would answer it properly and is
        exactly what a vehicle does not have.
        """
        centred = self.centredness(image_width)
        growing = self.growing
        relevant = centred >= 0.35 and growing
        return {
            "relevant_to_ego_path": relevant,
            "centredness": round(centred, 4),
            "growing": growing,
            "basis": (
                "image geometry only: how centred the sign was and whether it "
                "grew as the vehicle approached. No map is consulted"
            ),
        }

    def as_dict(self, image_width: int = 0) -> Dict[str, Any]:
        return {
            "sign_track_id": self.track_id,
            "class": self.sign_class,
            "n_detections": len(self.detections),
            "t_first": round(self.t_first, 4),
            "t_last": round(self.t_last, 4),
            "best_confidence": round(self.best.confidence, 4),
            "best_bbox": list(self.best.bbox),
            "relevance": self.relevance(image_width),
            "detections": [d.as_dict() for d in self.detections],
        }


class SignDetector:
    """Finds stop and give-way signs in a single frame by colour and shape."""

    def __init__(self, cfg: Optional[Config] = None) -> None:
        cfg = cfg if cfg is not None else Config({})
        p = "perception.signs."
        self.min_area_px = int(cfg.get(p + "min_area_px", 240))
        self.min_fill_ratio = float(cfg.get(p + "min_fill_ratio", 0.80))
        self.min_redness = float(cfg.get(p + "min_redness", 0.28))
        self.min_confidence = float(cfg.get(p + "min_confidence", 0.45))
        self.approx_epsilon = float(cfg.get(p + "approx_epsilon", 0.025))
        # Sign red wraps around the hue origin, so it needs two bands. Without
        # the second, everything on the magenta side of pure red is missed.
        self.hue_bands = (
            (0, 12), (168, 179),
        )
        self.min_saturation = int(cfg.get(p + "min_saturation", 90))
        self.min_value = int(cfg.get(p + "min_value", 50))
        # A stop sign's red is an annulus: a white border outside it and white
        # lettering inside. Closing the mask with a 3x3 kernel left the letters
        # as holes and the border ragged, so the contour came out concave and
        # filled only about half its bounding box -- while the classifier looks
        # for the 0.83 an octagon should fill. On the recorded approach that cost
        # all but two frames of a twenty-two frame sighting. Treating the
        # lettering as part of the face is what a reader of the sign does.
        self.close_kernel_px = int(cfg.get(p + "close_kernel_px", 9))

    def red_mask(self, image: Any) -> Any:
        """Pixels plausibly belonging to a red sign face."""
        cv2 = _cv2()
        import numpy as np

        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask = None
        for lo, hi in self.hue_bands:
            band = cv2.inRange(
                hsv,
                np.array([lo, self.min_saturation, self.min_value], dtype=np.uint8),
                np.array([hi, 255, 255], dtype=np.uint8),
            )
            mask = band if mask is None else cv2.bitwise_or(mask, band)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        k = max(1, int(self.close_kernel_px))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
        return mask

    def detect(self, image: Any, frame: int = 0, t: float = 0.0) -> List[SignDetection]:
        """Every sign this detector can find in one RGB frame."""
        cv2 = _cv2()

        mask = self.red_mask(image)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        out: List[SignDetection] = []
        for contour in contours:
            area = float(cv2.contourArea(contour))
            if area < self.min_area_px:
                continue
            hull = cv2.convexHull(contour)
            hull_area = float(cv2.contourArea(hull))
            if hull_area <= 0.0:
                continue
            fill_ratio = area / hull_area
            if fill_ratio < self.min_fill_ratio:
                continue

            perimeter = float(cv2.arcLength(contour, True))
            approx = cv2.approxPolyDP(contour, self.approx_epsilon * perimeter, True)
            n_vertices = int(len(approx))

            x, y, w, h = (int(v) for v in cv2.boundingRect(contour))
            if w <= 0 or h <= 0:
                continue
            redness = float(mask[y:y + h, x:x + w].mean() / 255.0)
            if redness < self.min_redness:
                continue

            sign_class, confidence = self._classify(
                approx, n_vertices, area, w, h, fill_ratio, redness
            )
            if sign_class is None or confidence < self.min_confidence:
                continue
            out.append(SignDetection(
                frame=frame, t=float(t), sign_class=sign_class,
                confidence=confidence, bbox=(x, y, w, h), n_vertices=n_vertices,
                fill_ratio=fill_ratio, redness=redness,
            ))
        out.sort(key=lambda d: (-d.confidence, d.bbox))
        return out

    def _classify(
        self,
        approx: Any,
        n_vertices: int,
        area: float,
        w: int,
        h: int,
        fill_ratio: float,
        redness: float,
    ) -> Tuple[Optional[str], float]:
        """Octagon or downward triangle, or neither.

        The discriminator that does the real work is not the vertex count -- which
        is noisy at small scales -- but how much of its bounding box the shape
        fills. An octagon fills about 0.83 of it and a triangle about 0.5, and
        those are far enough apart to separate reliably even when the polygon
        approximation miscounts corners.
        """
        aspect = float(w) / float(h)
        if not (0.6 <= aspect <= 1.7):
            return None, 0.0
        box_fill = area / float(w * h)

        # A give-way sign points down: its widest part is at the top.
        points = approx.reshape(-1, 2)
        top_half = points[points[:, 1] < points[:, 1].mean()]
        bottom_half = points[points[:, 1] >= points[:, 1].mean()]
        top_span = (
            float(top_half[:, 0].max() - top_half[:, 0].min())
            if len(top_half) else 0.0
        )
        bottom_span = (
            float(bottom_half[:, 0].max() - bottom_half[:, 0].min())
            if len(bottom_half) else 0.0
        )
        points_down = top_span > bottom_span * 1.6

        if 0.70 <= box_fill <= 0.95 and 5 <= n_vertices <= 12 and 0.75 <= aspect <= 1.3:
            # Closeness to the ideal octagon fill, scaled by colour purity.
            shape_score = max(0.0, 1.0 - abs(box_fill - 0.828) / 0.15)
            return STOP, float(min(1.0, 0.55 * shape_score + 0.45 * redness))

        if 0.35 <= box_fill <= 0.68 and n_vertices <= 6 and points_down:
            shape_score = max(0.0, 1.0 - abs(box_fill - 0.50) / 0.18)
            return YIELD, float(min(1.0, 0.55 * shape_score + 0.45 * redness))

        return None, 0.0


class SignTracker:
    """Associates per-frame detections into one track per physical sign."""

    def __init__(self, cfg: Optional[Config] = None) -> None:
        cfg = cfg if cfg is not None else Config({})
        p = "perception.signs."
        self.max_centre_gap_px = float(cfg.get(p + "max_centre_gap_px", 60.0))
        self.max_time_gap_s = float(cfg.get(p + "max_time_gap_s", 0.6))
        self.min_detections = int(cfg.get(p + "min_detections_per_track", 3))
        self._tracks: List[SignTrack] = []
        self._next_id = 0

    def update(self, detections: Sequence[SignDetection]) -> None:
        """Fold one frame's detections into the open tracks."""
        for detection in detections:
            best, best_gap = None, self.max_centre_gap_px
            for track in self._tracks:
                if track.sign_class != detection.sign_class:
                    continue
                if detection.t - track.t_last > self.max_time_gap_s:
                    continue
                cx, cy = track.detections[-1].centre
                dx, dy = detection.centre
                gap = ((cx - dx) ** 2 + (cy - dy) ** 2) ** 0.5
                if gap < best_gap:
                    best, best_gap = track, gap
            if best is not None:
                best.detections.append(detection)
            else:
                self._tracks.append(SignTrack(
                    track_id="sign-{0}".format(self._next_id),
                    sign_class=detection.sign_class,
                    detections=[detection],
                ))
                self._next_id += 1

    def tracks(self, confirmed_only: bool = True) -> List[SignTrack]:
        """The tracks, optionally only those seen often enough to be believed.

        A single-frame detection is far more likely to be a red van than a sign,
        so a track has to persist before it counts. This threshold is the main
        lever on the precision/recall trade-off and is reported with the metrics.
        """
        out = [
            t for t in self._tracks
            if not confirmed_only or len(t.detections) >= self.min_detections
        ]
        return sorted(out, key=lambda t: (t.t_first, t.track_id))


def detect_signs(
    frames: Sequence[Tuple[float, int, Any]],
    cfg: Optional[Config] = None,
    image_width: int = 0,
) -> Dict[str, Any]:
    """Run detection and tracking over a sequence of ``(t, frame_id, image)``.

    Returns the tracks and the per-frame detections behind them, so a reader can
    see what was rejected as well as what was kept.
    """
    cfg = cfg if cfg is not None else Config({})
    detector = SignDetector(cfg)
    tracker = SignTracker(cfg)

    all_detections: List[SignDetection] = []
    width = int(image_width)
    for t, frame_id, image in frames:
        if width == 0 and image is not None:
            width = int(image.shape[1])
        found = detector.detect(image, frame=int(frame_id), t=float(t))
        all_detections.extend(found)
        tracker.update(found)

    confirmed = tracker.tracks(confirmed_only=True)
    provisional = [
        t for t in tracker.tracks(confirmed_only=False) if t not in confirmed
    ]
    return {
        "method": (
            "colour-and-shape detection in HSV followed by polygon "
            "classification, then association across frames. Deterministic, no "
            "training data, no learned weights, no privileged sign labels"
        ),
        "image_width": width,
        "n_frames": len(frames),
        "n_detections": len(all_detections),
        "n_tracks": len(confirmed),
        "min_detections_per_track": tracker.min_detections,
        "tracks": [t.as_dict(width) for t in confirmed],
        "rejected_short_tracks": [
            {"class": t.sign_class, "n_detections": len(t.detections),
             "t_first": round(t.t_first, 4)}
            for t in provisional
        ],
        "note": (
            "one event per track, not per frame: a sign in view for two seconds "
            "is one perception. Short tracks are rejected and listed rather than "
            "dropped silently, because they are the detector's false positives "
            "and belong in its measured precision"
        ),
    }
