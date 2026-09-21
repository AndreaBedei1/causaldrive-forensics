"""Per-vehicle raw sensor and control logging."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


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
        (self.root / "camera" / "frames").mkdir(parents=True, exist_ok=True)
        (self.root / "metadata.json").write_text(_json(metadata), encoding="utf-8")
        self._closed = False

    def log_state(self, record: Dict[str, Any]) -> None: self.state.write(record)
    def log_control(self, record: Dict[str, Any]) -> None: self.controls.write(record)
    def log_collision(self, record: Dict[str, Any]) -> None:
        # Never accept simulator actor identity in a vehicle-local file.
        self.collisions.write({k: v for k, v in record.items() if k not in {"actor_id", "other_actor_id", "other_type_id"}})
    def log_radar(self, record: Dict[str, Any]) -> None: self.radar.write(record)
    def log_camera(self, record: Dict[str, Any], data: bytes, extension: str = "bgra") -> None:
        frame = int(record["frame"])
        filename = f"{frame:08d}.{extension}"
        (self.root / "camera" / "frames" / filename).write_bytes(data)
        metadata = dict(record)
        metadata["image_filename"] = filename
        self.camera_metadata.write(metadata)

    def close(self) -> None:
        if self._closed:
            return
        for stream in (self.state, self.controls, self.collisions, self.radar, self.camera_metadata):
            stream.close()
        self._closed = True
