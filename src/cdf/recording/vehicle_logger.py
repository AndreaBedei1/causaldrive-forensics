"""Per-vehicle raw sensor and control logging."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _without_privileged_ids(value: Any) -> Any:
    """Drop simulator identity fields from every vehicle-local record."""
    if isinstance(value, dict):
        return {k: _without_privileged_ids(v) for k, v in value.items()
                if k not in {"actor_id", "other_actor_id", "other_type_id"}}
    if isinstance(value, list):
        return [_without_privileged_ids(item) for item in value]
    return value


class _Jsonl:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.handle = path.open("w", encoding="utf-8")

    def write(self, record: Dict[str, Any]) -> None:
        self.handle.write(_json(record) + "\n")

    def close(self) -> None:
        self.handle.close()


class VehicleLogger:
    """Write only observations available to one vehicle."""

    def __init__(self, root: Path, participant_id: str, metadata: Dict[str, Any]) -> None:
        self.root = Path(root) / "vehicles" / str(participant_id)
        self.root.mkdir(parents=True, exist_ok=True)
        self.state = _Jsonl(self.root / "ego.jsonl")
        self.controls = _Jsonl(self.root / "controls.jsonl")
        self.collisions = _Jsonl(self.root / "collisions.jsonl")
        self.radar = _Jsonl(self.root / "radar.jsonl")
        self.camera_metadata = _Jsonl(self.root / "camera" / "metadata.jsonl")
        self.depth_metadata = _Jsonl(self.root / "depth" / "metadata.jsonl")
        (self.root / "camera" / "frames").mkdir(parents=True, exist_ok=True)
        (self.root / "depth" / "frames").mkdir(parents=True, exist_ok=True)
        (self.root / "metadata.json").write_text(_json(_without_privileged_ids(metadata)), encoding="utf-8")
        self._closed = False

    def log_state(self, record: Dict[str, Any]) -> None: self.state.write(_without_privileged_ids(record))
    def log_control(self, record: Dict[str, Any]) -> None: self.controls.write(_without_privileged_ids(record))
    def log_collision(self, record: Dict[str, Any]) -> None:
        # Never accept simulator actor identity in a vehicle-local file.
        self.collisions.write(_without_privileged_ids(record))
    def log_radar(self, record: Dict[str, Any]) -> None: self.radar.write(_without_privileged_ids(record))
    def log_camera(self, record: Dict[str, Any], data: bytes, extension: str = "bgra") -> None:
        frame = int(record["frame"])
        filename = f"{frame:08d}.{extension}"
        (self.root / "camera" / "frames" / filename).write_bytes(data)
        metadata = _without_privileged_ids(record)
        metadata["image_filename"] = filename
        self.camera_metadata.write(metadata)

    def log_depth(self, record: Dict[str, Any], data: bytes, extension: str = "bgra") -> None:
        frame = int(record["frame"])
        filename = f"{frame:08d}.{extension}"
        (self.root / "depth" / "frames" / filename).write_bytes(data)
        metadata = _without_privileged_ids(record)
        metadata["image_filename"] = filename
        metadata["encoding"] = "CARLA depth: BGRA bytes encode normalized 24-bit depth; meters = 1000 * (R + 256*G + 65536*B) / (256**3 - 1)."
        self.depth_metadata.write(metadata)

    def close(self) -> None:
        if self._closed:
            return
        for stream in (self.state, self.controls, self.collisions, self.radar, self.camera_metadata, self.depth_metadata):
            stream.close()
        self._closed = True
