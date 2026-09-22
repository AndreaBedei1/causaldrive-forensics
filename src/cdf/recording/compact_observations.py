"""Compact, source-agnostic storage for variable-length sensor detections."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

import numpy as np


OBSERVATION_COLUMNS = (
    "depth_m",
    "azimuth_rad",
    "altitude_rad",
    "radial_velocity_mps",
)


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False)


def _detection_row(detection: Any) -> np.ndarray:
    """Convert either the radar/depth dict schema or a numeric row to float32."""
    if isinstance(detection, Mapping):
        depth = detection.get("depth_m", detection.get("depth"))
        azimuth = detection.get("azimuth_rad", detection.get("azimuth"))
        altitude = detection.get("altitude_rad", detection.get("altitude"))
        velocity = detection.get("radial_velocity_mps", detection.get("radial_velocity"))
        if velocity is None:
            velocity = np.nan
        if depth is None or azimuth is None or altitude is None:
            raise ValueError("detection is missing depth, azimuth, or altitude")
        return np.asarray([depth, azimuth, altitude, velocity], dtype=np.float32)
    row = np.asarray(detection, dtype=np.float32)
    if row.shape != (4,):
        raise ValueError("numeric detections must have shape (4,)")
    return row


@dataclass(frozen=True)
class CompactObservations:
    """Loaded variable-length observations with common radar/depth columns."""

    frames: np.ndarray
    timestamps: np.ndarray
    offsets: np.ndarray
    detections: np.ndarray

    def frame_detections(self, index: int) -> np.ndarray:
        return self.detections[self.offsets[index]:self.offsets[index + 1]]


def load_observations(path: Path) -> CompactObservations:
    """Load a radar or depth NPZ without permitting object/pickle arrays."""
    with np.load(Path(path), allow_pickle=False) as data:
        required = {"frames", "timestamps", "offsets", "detections"}
        missing = required.difference(data.files)
        if missing:
            raise ValueError("observation NPZ is missing: " + ", ".join(sorted(missing)))
        observations = CompactObservations(
            frames=np.asarray(data["frames"], dtype=np.int64).copy(),
            timestamps=np.asarray(data["timestamps"], dtype=np.float64).copy(),
            offsets=np.asarray(data["offsets"], dtype=np.int64).copy(),
            detections=np.asarray(data["detections"], dtype=np.float32).copy(),
        )
    if observations.detections.ndim != 2 or observations.detections.shape[1] != 4:
        raise ValueError("detections must have shape [N, 4]")
    if len(observations.offsets) != len(observations.frames) + 1:
        raise ValueError("offsets must have one more entry than frames")
    if len(observations.timestamps) != len(observations.frames):
        raise ValueError("timestamps and frames must have equal length")
    if len(observations.offsets) and (
        observations.offsets[0] != 0
        or observations.offsets[-1] != len(observations.detections)
        or np.any(np.diff(observations.offsets) < 0)
    ):
        raise ValueError("invalid observation offsets")
    return observations


class CompactObservationWriter:
    """Accumulate compact numeric rows and emit one compressed NPZ at close."""

    def __init__(self, path: Path, metadata: Mapping[str, Any]) -> None:
        self.path = Path(path)
        self.metadata_path = self.path.with_name("metadata.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._metadata: Dict[str, Any] = dict(metadata)
        self._frames = []
        self._timestamps = []
        self._offsets = [0]
        self._detections = []
        self._closed = False

    def append(self, frame: int, timestamp: float, detections: Iterable[Any]) -> None:
        if self._closed:
            raise RuntimeError("cannot append after writer close")
        rows = [_detection_row(detection) for detection in detections]
        self._frames.append(int(frame))
        self._timestamps.append(float(timestamp))
        if rows:
            self._detections.extend(rows)
        self._offsets.append(len(self._detections))

    @property
    def frames_written(self) -> int:
        return len(self._frames)

    @property
    def frame_numbers(self):
        return self._frames

    def stats(self) -> Dict[str, Any]:
        frames = self._frames
        gaps = sum(max(0, later - earlier - 1) for earlier, later in zip(frames, frames[1:]))
        return {
            "frames_written": len(frames),
            "first_frame": frames[0] if frames else None,
            "last_frame": frames[-1] if frames else None,
            "missing_frame_count": int(gaps),
        }

    def close(self, metadata_updates: Optional[Mapping[str, Any]] = None) -> None:
        if self._closed:
            return
        detections = np.asarray(self._detections, dtype=np.float32)
        if detections.size == 0:
            detections = np.empty((0, 4), dtype=np.float32)
        else:
            detections = detections.reshape((-1, 4))
        np.savez_compressed(
            self.path,
            frames=np.asarray(self._frames, dtype=np.int64),
            timestamps=np.asarray(self._timestamps, dtype=np.float64),
            offsets=np.asarray(self._offsets, dtype=np.int64),
            detections=detections,
        )
        self._metadata.update(self.stats())
        if metadata_updates:
            self._metadata.update(dict(metadata_updates))
        self.metadata_path.write_text(_json(self._metadata), encoding="utf-8")
        self._closed = True

