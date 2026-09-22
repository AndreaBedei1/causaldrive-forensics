"""Compact, source-agnostic storage for variable-length sensor detections."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Mapping, Optional

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
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def frame_detections(self, index: int) -> np.ndarray:
        return self.detections[self.offsets[index]:self.offsets[index + 1]]

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterate frames through the same logical radar/depth interface."""
        for index, (frame, timestamp) in enumerate(zip(self.frames, self.timestamps)):
            yield {
                "frame": int(frame),
                "timestamp": float(timestamp),
                "detections": self.frame_detections(index),
            }


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
            metadata={},
        )
    metadata_path = Path(path).with_name("metadata.json")
    metadata: Dict[str, Any] = {}
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError("invalid observation metadata JSON") from exc
    observations = CompactObservations(
        frames=observations.frames, timestamps=observations.timestamps,
        offsets=observations.offsets, detections=observations.detections,
        metadata=metadata,
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


COMMON_REGION = {
    "azimuth_min_deg": -45.0,
    "azimuth_max_deg": 45.0,
    "altitude_min_deg": -5.0,
    "altitude_max_deg": 5.0,
    "range_min_m": 0.0,
    "range_max_m": 90.0,
}


def _filter_common_region(observations: CompactObservations) -> CompactObservations:
    """Return a view with the radar/depth overlap while preserving all frames."""
    az_limit = np.deg2rad(45.0)
    al_limit = np.deg2rad(5.0)
    rows = []
    offsets = [0]
    for index in range(len(observations.frames)):
        detections = observations.frame_detections(index)
        if len(detections):
            # Preserve NaN velocity rows: only geometry defines the region.
            valid = (
                np.isfinite(detections[:, 0])
                & (detections[:, 0] >= 0.0) & (detections[:, 0] <= 90.0)
                & np.isfinite(detections[:, 1]) & (np.abs(detections[:, 1]) <= az_limit)
                & np.isfinite(detections[:, 2]) & (np.abs(detections[:, 2]) <= al_limit)
            )
            rows.extend(detections[valid])
        offsets.append(len(rows))
    filtered = np.asarray(rows, dtype=np.float32).reshape((-1, 4)) if rows else np.empty((0, 4), dtype=np.float32)
    metadata = dict(observations.metadata)
    metadata["common_region"] = dict(COMMON_REGION)
    return CompactObservations(
        frames=observations.frames.copy(), timestamps=observations.timestamps.copy(),
        offsets=np.asarray(offsets, dtype=np.int64), detections=filtered, metadata=metadata,
    )


def load_observation_stream(vehicle_dir: Path, source: str = "radar", common_region: bool = False) -> CompactObservations:
    """Load either native radar or depth through one source-agnostic API.

    ``common_region=True`` filters only the returned view; native NPZ files are
    never modified, so radar observations outside the overlap remain available.
    """
    root = Path(vehicle_dir)
    source_name = str(source).lower()
    if source_name == "depth":
        path = root / "depth" / "observations.npz"
    elif source_name == "radar":
        path = root / "radar" / "observations.npz"
        if not path.exists():
            candidates = sorted((root / "radar").glob("*/observations.npz"))
            if len(candidates) == 1:
                path = candidates[0]
            elif not candidates:
                raise FileNotFoundError("no radar observations found under " + str(root))
            else:
                raise ValueError("multiple radar sensors require an explicit sensor path")
    else:
        raise ValueError("source must be 'radar' or 'depth'")
    observations = load_observations(path)
    return _filter_common_region(observations) if common_region else observations


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
