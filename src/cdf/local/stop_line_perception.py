"""Finding the stop line in the image, and knowing when it has been crossed.

The brief is explicit that this must not come from the map. The map knows where
every stop line is to the centimetre, and a vehicle that consults it is not
demonstrating anything about onboard forensics. So the line is found in the image,
and crossing it is inferred from what happens to that image.

How a stop line looks, and what that buys
-----------------------------------------

A stop line is a broad bright band lying across the direction of travel. In a
forward camera it appears as a group of image rows with an unusually high
proportion of bright pixels spread over a wide horizontal extent -- which is a
different signature from a lane line, running away from the camera as a narrow
near-vertical streak. Distinguishing the two is the whole detection: transverse
and wide, not longitudinal and narrow.

As the vehicle approaches, the band moves down the image and grows. Crossing is
the moment it leaves the bottom of frame. That is inferred rather than observed:
the band is tracked while it descends, and when it disappears from near the bottom
edge while the vehicle is still moving forward, it has passed under the car.

The failure mode this design accepts
------------------------------------

A band that disappears because the detector lost it -- shadow, glare, a vehicle
occluding it -- looks the same as one that passed underneath. The guard is that
the last sighting must have been low in the frame *and* the vehicle must have been
moving; a line lost at mid-frame produces no crossing. That makes the detector
conservative: it misses crossings rather than inventing them. Missing one shows up
as recall, and inventing one would corrupt every non-action built on top of it,
so the asymmetry is deliberate.

Speed comes from the vehicle's own telemetry, which it is entitled to. No map, no
waypoints, no lane ids.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import Event, EventType, Evidence, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = [
    "StopLineSighting",
    "StopLineDetector",
    "detect_stop_lines",
]


@dataclass
class StopLineSighting:
    """A transverse bright band seen in one frame."""

    frame: int
    t: float
    row_centre: int
    """Image row of the band's middle. Larger is lower in frame, so nearer."""
    row_span: int
    width_fraction: float
    """How much of the image width the band spans, in [0, 1]."""
    brightness: float
    confidence: float

    def as_dict(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "t_local": round(self.t, 4),
            "row_centre": self.row_centre,
            "row_span": self.row_span,
            "width_fraction": round(self.width_fraction, 4),
            "brightness": round(self.brightness, 4),
            "confidence": round(self.confidence, 4),
        }


class StopLineDetector:
    """Finds a transverse bright band in the lower part of a forward image."""

    def __init__(self, cfg: Optional[Config] = None) -> None:
        cfg = cfg if cfg is not None else Config({})
        p = "perception.stop_lines."
        self.roi_top_fraction = float(cfg.get(p + "roi_top_fraction", 0.55))
        self.min_brightness = int(cfg.get(p + "min_brightness", 165))
        self.min_row_bright_fraction = float(
            cfg.get(p + "min_row_bright_fraction", 0.30)
        )
        self.min_width_fraction = float(cfg.get(p + "min_width_fraction", 0.35))
        self.min_rows = int(cfg.get(p + "min_rows", 3))
        self.max_rows = int(cfg.get(p + "max_rows", 90))
        self.min_confidence = float(cfg.get(p + "min_confidence", 0.40))

    def detect(
        self, image: Any, frame: int = 0, t: float = 0.0
    ) -> Optional[StopLineSighting]:
        """The most prominent transverse band, or ``None``."""
        import numpy as np

        height, width = int(image.shape[0]), int(image.shape[1])
        if height < 8 or width < 8:
            return None

        grey = image.mean(axis=2) if image.ndim == 3 else image.astype(float)
        top = int(height * self.roi_top_fraction)
        roi = grey[top:, :]
        if roi.size == 0:
            return None

        bright = roi >= self.min_brightness
        row_fraction = bright.mean(axis=1)
        candidate_rows = np.flatnonzero(row_fraction >= self.min_row_bright_fraction)
        if candidate_rows.size == 0:
            return None

        # Take the lowest contiguous run of qualifying rows: the nearest band is
        # the one that matters, and a band further up the image is a line the
        # vehicle has not reached yet.
        runs: List[Tuple[int, int]] = []
        start = prev = int(candidate_rows[0])
        for row in candidate_rows[1:]:
            row = int(row)
            if row == prev + 1:
                prev = row
                continue
            runs.append((start, prev))
            start = prev = row
        runs.append((start, prev))
        runs = [r for r in runs if (r[1] - r[0] + 1) >= self.min_rows]
        if not runs:
            return None
        lo, hi = runs[-1]
        span = hi - lo + 1
        if span > self.max_rows:
            # Too tall to be a line across the road: this is a bright surface,
            # not a marking.
            return None

        band = bright[lo:hi + 1, :]
        columns = band.any(axis=0)
        # A transverse line spans a broad, contiguous horizontal extent. A
        # longitudinal lane line touches few columns, which is what separates
        # them without needing any geometry.
        column_indices = np.flatnonzero(columns)
        width_fraction = float(
            (column_indices[-1] - column_indices[0] + 1) / width
        ) if column_indices.size else 0.0
        if width_fraction < self.min_width_fraction:
            return None
        fill = float(columns.mean())

        brightness = float(roi[lo:hi + 1, :][band].mean() / 255.0)
        confidence = float(min(1.0, 0.45 * width_fraction + 0.35 * fill
                               + 0.20 * brightness))
        if confidence < self.min_confidence:
            return None
        return StopLineSighting(
            frame=int(frame), t=float(t),
            row_centre=int(top + (lo + hi) // 2),
            row_span=int(span),
            width_fraction=width_fraction,
            brightness=brightness,
            confidence=confidence,
        )


def detect_stop_lines(
    frames: Sequence[Tuple[float, int, Any]],
    speed_at: Optional[Any] = None,
    cfg: Optional[Config] = None,
    participant_id: str = "",
    id_prefix: str = "sl",
) -> Dict[str, Any]:
    """Detect a stop line and infer whether it was crossed.

    ``speed_at(t)`` returns the vehicle's own speed at a local time, from its own
    telemetry. Without it, no crossing is inferred at all: the crossing claim
    rests on the vehicle having been in motion, and guessing that would be the
    one place this module could invent an event.
    """
    cfg = cfg if cfg is not None else Config({})
    p = "perception.stop_lines."
    near_bottom = float(cfg.get(p + "crossing_row_fraction", 0.80))
    min_speed = float(cfg.get(p + "crossing_min_speed_mps", 0.5))
    min_sightings = int(cfg.get(p + "min_sightings", 3))
    lost_after_s = float(cfg.get(p + "lost_after_s", 0.4))

    detector = StopLineDetector(cfg)
    sightings: List[StopLineSighting] = []
    height = 0
    for t, frame_id, image in frames:
        if image is not None and height == 0:
            height = int(image.shape[0])
        found = detector.detect(image, frame=int(frame_id), t=float(t))
        if found is not None:
            sightings.append(found)

    events: List[Event] = []
    crossing: Optional[Dict[str, Any]] = None
    refusal: Optional[str] = None

    if len(sightings) >= min_sightings:
        first = sightings[0]
        events.append(Event(
            event_id="{0}-{1}-detected".format(id_prefix, participant_id),
            event_type=EventType.STOP_LINE_DETECTED,
            participant_id=str(participant_id),
            t_start=first.t, t_peak=first.t, t_end=sightings[-1].t,
            values={"width_fraction": round(first.width_fraction, 4)},
            detail={
                "n_sightings": len(sightings),
                "method": "transverse bright band in the lower image",
                "row_first": first.row_centre,
                "row_last": sightings[-1].row_centre,
            },
            confidence=max(s.confidence for s in sightings),
            evidence=[Evidence(
                kind="camera", ref="frame:{0}".format(first.frame),
                t_start=first.t, t_end=sightings[-1].t,
                detail={"row_centre": first.row_centre},
            )],
            provenance=Provenance.LOCAL,
            source_sensors=["camera"],
        ))

        last = sightings[-1]
        descended = last.row_centre >= near_bottom * max(height, 1)
        moving = None
        if speed_at is not None:
            try:
                moving = float(speed_at(last.t)) >= min_speed
            except (TypeError, ValueError):  # pragma: no cover - defensive
                moving = None
        # The band was last seen low in the frame and the vehicle was moving, so
        # it passed underneath. Each condition on its own is not enough: a band
        # lost mid-frame was lost by the detector, and a band low in frame with
        # the vehicle stopped is a line the vehicle is waiting at.
        if descended and moving:
            t_cross = last.t + lost_after_s / 2.0
            crossing = {
                "t": round(t_cross, 4),
                "last_row": last.row_centre,
                "image_height": height,
                "speed_mps": round(float(speed_at(last.t)), 3),
            }
            events.append(Event(
                event_id="{0}-{1}-crossed".format(id_prefix, participant_id),
                event_type=EventType.STOP_LINE_CROSSED,
                participant_id=str(participant_id),
                t_start=last.t, t_peak=t_cross, t_end=t_cross,
                values={"speed_mps": round(float(speed_at(last.t)), 3)},
                detail={
                    "inferred_from": (
                        "the band was last seen at row {0} of {1} and the "
                        "vehicle was still moving, so it passed under the "
                        "car".format(last.row_centre, height)
                    ),
                    "method": "camera only; no map geometry consulted",
                    "uncertainty_s": lost_after_s,
                },
                confidence=round(0.75 * last.confidence, 4),
                evidence=[Evidence(
                    kind="camera", ref="frame:{0}".format(last.frame),
                    t_start=last.t, t_end=t_cross,
                    detail={"row_centre": last.row_centre},
                )],
                provenance=Provenance.LOCAL,
                source_sensors=["camera"],
            ))
        elif not descended:
            refusal = (
                "the band was last seen at row {0} of {1}, too high in the "
                "frame to have passed under the vehicle. More likely the "
                "detector lost it, so no crossing is claimed".format(
                    last.row_centre, height)
            )
        elif moving is None:
            refusal = (
                "no speed was available, and the crossing claim rests on the "
                "vehicle having been in motion"
            )
        else:
            refusal = (
                "the band reached the bottom of the frame but the vehicle was "
                "not moving, which is a vehicle waiting at the line rather than "
                "one crossing it"
            )
    elif sightings:
        refusal = (
            "{0} sighting(s), fewer than the {1} required. A band seen once or "
            "twice is more likely glare than a marking".format(
                len(sightings), min_sightings)
        )

    return {
        "participant_id": str(participant_id),
        "n_frames": len(frames),
        "n_sightings": len(sightings),
        "sightings": [s.as_dict() for s in sightings],
        "crossing": crossing,
        "no_crossing_because": refusal,
        "events": events,
        "method": (
            "a transverse bright band in the lower image, tracked as it descends. "
            "Crossing is inferred from the band leaving the bottom of frame while "
            "the vehicle is moving. No map geometry is read"
        ),
        "note": (
            "deliberately conservative: a band lost mid-frame yields no crossing. "
            "Missing a crossing costs recall; inventing one would corrupt every "
            "non-action built on top of it"
        ),
    }
