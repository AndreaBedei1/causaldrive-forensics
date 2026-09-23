"""Deterministic STOP/YIELD perception from transient RGB frames.

This is the small historical colour-and-shape detector, moved into the current
recording pipeline.  It uses no CARLA labels, actor IDs, maps, or ground truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

STOP = "STOP"
YIELD = "YIELD"


def _cv2() -> Any:
    try:
        import cv2
    except ImportError as exc:  # pragma: no cover
        raise ImportError("sign perception needs OpenCV; install opencv-python") from exc
    return cv2


def _get(cfg: Any, key: str, default: Any) -> Any:
    if cfg is None:
        return default
    if hasattr(cfg, "get"):
        try:
            value = cfg.get(key, default)
            if value != default:
                return value
        except TypeError:
            pass
    if isinstance(cfg, Mapping):
        if key in cfg:
            return cfg[key]
        node: Any = cfg
        for part in key.split("."):
            if not isinstance(node, Mapping) or part not in node:
                return default
            node = node[part]
        return node
    return default


@dataclass
class SignDetection:
    frame: int
    t: float
    sign_class: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    n_vertices: int = 0
    fill_ratio: float = 0.0
    redness: float = 0.0

    @property
    def area(self) -> int:
        return int(self.bbox[2] * self.bbox[3])

    @property
    def centre(self) -> Tuple[float, float]:
        x, y, w, h = self.bbox
        return x + w / 2.0, y + h / 2.0

    def as_dict(self) -> Dict[str, Any]:
        return {"frame": self.frame, "t_local": round(self.t, 4), "class": self.sign_class,
                "confidence": round(self.confidence, 4), "bbox": list(self.bbox),
                "n_vertices": self.n_vertices, "fill_ratio": round(self.fill_ratio, 4),
                "redness": round(self.redness, 4)}


@dataclass
class SignTrack:
    track_id: str
    sign_class: str
    detections: List[SignDetection] = field(default_factory=list)

    @property
    def t_first(self) -> float: return self.detections[0].t
    @property
    def frame_first(self) -> int: return self.detections[0].frame
    @property
    def frame_confirmed(self) -> int:
        # The tracker writes this value at serialization time; callers that do
        # not know the configured threshold use the historical default of 3.
        return self.detections[min(2, len(self.detections) - 1)].frame
    @property
    def t_last(self) -> float: return self.detections[-1].t
    @property
    def best(self) -> SignDetection: return max(self.detections, key=lambda d: d.confidence)
    @property
    def growing(self) -> bool:
        if len(self.detections) < 4:
            return False
        third = max(1, len(self.detections) // 3)
        early = sum(d.area for d in self.detections[:third]) / third
        late = sum(d.area for d in self.detections[-third:]) / third
        return late > early * 1.15

    def centredness(self, image_width: int) -> float:
        if image_width <= 0:
            return 0.0
        x, _ = self.best.centre
        return float(max(0.0, 1.0 - abs(x - image_width / 2.0) / (image_width / 2.0)))

    def relevance(self, image_width: int) -> Dict[str, Any]:
        centred = self.centredness(image_width)
        return {"relevant_to_ego_path": bool(centred >= 0.35 and self.growing),
                "centredness": round(centred, 4), "growing": self.growing,
                "basis": "image geometry only: how centred the sign was and whether it grew as the vehicle approached. No map is consulted"}

    def as_dict(self, image_width: int = 0) -> Dict[str, Any]:
        return {"sign_track_id": self.track_id, "class": self.sign_class,
                "frame_first": self.frame_first, "frame_confirmed": self.frame_confirmed,
                "frame_last": self.detections[-1].frame,
                "n_detections": len(self.detections), "t_first": round(self.t_first, 4),
                "t_confirmed": round(self.detections[min(2, len(self.detections) - 1)].t, 4),
                "t_last": round(self.t_last, 4), "best_confidence": round(self.best.confidence, 4),
                "best_bbox": list(self.best.bbox), "relevance": self.relevance(image_width),
                "detections": [d.as_dict() for d in self.detections]}


class SignDetector:
    def __init__(self, cfg: Optional[Any] = None) -> None:
        # Accept the current traffic_signs namespace and the historical nested
        # perception.signs namespace for compatibility with old unit tests.
        def val(name: str, old: str, default: Any) -> Any:
            got = _get(cfg, "traffic_signs." + name, None)
            if got is None:
                got = _get(cfg, name, None)
            if got is None:
                got = _get(cfg, "perception.signs." + old, default)
            return got
        self.min_area_px = int(val("min_area_px", "min_area_px", 240))
        self.min_fill_ratio = float(val("min_fill_ratio", "min_fill_ratio", 0.80))
        self.min_redness = float(val("min_redness", "min_redness", 0.28))
        self.min_confidence = float(val("min_confidence", "min_confidence", 0.45))
        self.approx_epsilon = float(val("approx_epsilon", "approx_epsilon", 0.025))
        self.min_saturation = int(val("min_saturation", "min_saturation", 90))
        self.min_value = int(val("min_value", "min_value", 50))
        self.close_kernel_px = int(val("close_kernel_px", "close_kernel_px", 9))
        self.max_centre_row_fraction = float(val("max_centre_row_fraction", "max_centre_row_fraction", 0.62))

    def red_mask(self, image: Any) -> Any:
        cv2 = _cv2()
        import numpy as np
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask = None
        for lo, hi in ((0, 12), (168, 179)):
            band = cv2.inRange(hsv, np.array([lo, self.min_saturation, self.min_value], np.uint8),
                               np.array([hi, 255, 255], np.uint8))
            mask = band if mask is None else cv2.bitwise_or(mask, band)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        k = max(1, self.close_kernel_px)
        return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))

    def detect(self, image: Any, frame: int = 0, t: float = 0.0) -> List[SignDetection]:
        cv2 = _cv2(); mask = self.red_mask(image)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        out: List[SignDetection] = []
        for contour in contours:
            area = float(cv2.contourArea(contour))
            if area < self.min_area_px:
                continue
            hull_area = float(cv2.contourArea(cv2.convexHull(contour)))
            if hull_area <= 0 or area / hull_area < self.min_fill_ratio:
                continue
            perimeter = float(cv2.arcLength(contour, True))
            approx = cv2.approxPolyDP(contour, self.approx_epsilon * perimeter, True)
            n_vertices = int(len(approx)); x, y, w, h = (int(v) for v in cv2.boundingRect(contour))
            if w <= 0 or h <= 0 or (y + h / 2.0) > self.max_centre_row_fraction * int(image.shape[0]):
                continue
            fill_ratio = area / hull_area
            redness = float(mask[y:y + h, x:x + w].mean() / 255.0)
            if redness < self.min_redness:
                continue
            sign_class, confidence = self._classify(approx, n_vertices, area, w, h, fill_ratio, redness)
            if sign_class and confidence >= self.min_confidence:
                out.append(SignDetection(int(frame), float(t), sign_class, confidence, (x, y, w, h),
                                         n_vertices, fill_ratio, redness))
        return sorted(out, key=lambda d: (-d.confidence, d.bbox))

    def _classify(self, approx: Any, n_vertices: int, area: float, w: int, h: int,
                  fill_ratio: float, redness: float) -> Tuple[Optional[str], float]:
        aspect = float(w) / float(h)
        if not 0.6 <= aspect <= 1.7:
            return None, 0.0
        box_fill = area / float(w * h)
        points = approx.reshape(-1, 2)
        mean_y = points[:, 1].mean()
        top = points[points[:, 1] < mean_y]; bottom = points[points[:, 1] >= mean_y]
        top_span = float(top[:, 0].max() - top[:, 0].min()) if len(top) else 0.0
        bottom_span = float(bottom[:, 0].max() - bottom[:, 0].min()) if len(bottom) else 0.0
        if 0.70 <= box_fill <= 0.95 and 5 <= n_vertices <= 12 and 0.75 <= aspect <= 1.3:
            score = max(0.0, 1.0 - abs(box_fill - 0.828) / 0.15)
            return STOP, float(min(1.0, 0.55 * score + 0.45 * redness))
        if 0.35 <= box_fill <= 0.68 and n_vertices <= 6 and top_span > bottom_span * 1.6:
            score = max(0.0, 1.0 - abs(box_fill - 0.50) / 0.18)
            return YIELD, float(min(1.0, 0.55 * score + 0.45 * redness))
        return None, 0.0


class SignTracker:
    def __init__(self, cfg: Optional[Any] = None) -> None:
        def val(name: str, default: Any) -> Any:
            got = _get(cfg, "traffic_signs." + name, None)
            if got is None:
                got = _get(cfg, name, None)
            if got is None:
                old = {"max_centre_gap_px": "max_centre_gap_px", "max_time_gap_s": "max_time_gap_s",
                       "min_detections_per_track": "min_detections_per_track"}[name]
                got = _get(cfg, "perception.signs." + old, None)
            return default if got is None else got
        self.max_centre_gap_px = float(val("max_centre_gap_px", 60.0))
        self.max_time_gap_s = float(val("max_time_gap_s", 0.6))
        self.min_detections = int(val("min_detections_per_track", 3))
        self._tracks: List[SignTrack] = []; self._next_id = 0

    def update(self, detections: Sequence[SignDetection]) -> None:
        for detection in detections:
            best, best_gap = None, self.max_centre_gap_px
            for track in self._tracks:
                if track.sign_class != detection.sign_class or detection.t - track.t_last > self.max_time_gap_s:
                    continue
                cx, cy = track.detections[-1].centre; dx, dy = detection.centre
                gap = ((cx - dx) ** 2 + (cy - dy) ** 2) ** 0.5
                if gap < best_gap:
                    best, best_gap = track, gap
            if best is None:
                best = SignTrack("sign-{0}".format(self._next_id), detection.sign_class, [detection])
                self._next_id += 1; self._tracks.append(best)
            else:
                best.detections.append(detection)

    def tracks(self, confirmed_only: bool = True) -> List[SignTrack]:
        return sorted([t for t in self._tracks if not confirmed_only or len(t.detections) >= self.min_detections],
                       key=lambda t: (t.t_first, t.track_id))

    @property
    def n_detections(self) -> int:
        return sum(len(t.detections) for t in self._tracks)

    @property
    def rejected_short_tracks(self) -> int:
        return sum(len(t.detections) < self.min_detections for t in self._tracks)


def detect_signs(frames: Sequence[Tuple[float, int, Any]], cfg: Optional[Any] = None,
                 image_width: int = 0) -> Dict[str, Any]:
    """Run the detector/tracker over ``(timestamp, frame, RGB image)`` tuples."""
    detector = SignDetector(cfg); tracker = SignTracker(cfg)
    all_detections: List[SignDetection] = []; width = int(image_width)
    for timestamp, frame, image in frames:
        if width == 0 and image is not None:
            width = int(image.shape[1])
        detections = detector.detect(image, frame=int(frame), t=float(timestamp))
        all_detections.extend(detections); tracker.update(detections)
    confirmed = tracker.tracks(True)
    provisional = tracker.tracks(False)
    method = ("colour-and-shape detection in HSV followed by polygon classification, "
              "then association across frames. Deterministic, no training data, "
              "no learned weights, no privileged sign labels")
    return {"method": method, "image_width": width, "n_frames": len(frames),
            "n_detections": len(all_detections), "n_tracks": len(confirmed),
            "min_detections_per_track": tracker.min_detections,
            "tracks": [track.as_dict(width) for track in confirmed],
            "rejected_short_tracks": [{"class": track.sign_class,
                "n_detections": len(track.detections), "t_first": round(track.t_first, 4)}
                for track in provisional if track not in confirmed]}
