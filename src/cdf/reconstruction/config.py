"""The few reconstruction parameters that genuinely need tuning.

Defaults are physically motivated and were checked on the S01-S03 recordings;
``configs/reconstruction.yaml`` mirrors them with one comment per value.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


@dataclass
class CollisionConfig:
    # Collision callbacks closer than this belong to the same contact episode.
    merge_gap_s: float = 0.5


@dataclass
class TrackingConfig:
    # Only returns between these heights above the road can come from a vehicle
    # body; lower ones are road surface, higher ones signs, bridges, trees.
    min_height_m: float = 0.3
    max_height_m: float = 2.5
    # A return whose own speed along the line of sight (ego motion removed)
    # exceeds this is "moving"; only moving returns can start a new track.
    moving_speed_mps: float = 1.0
    # Moving returns closer than this in one sweep form one candidate object.
    cluster_distance_m: float = 2.0
    # A track claims returns within this distance of its predicted position...
    max_association_distance_m: float = 2.5
    # ...whose line-of-sight speed differs from its prediction by at most this.
    max_velocity_mismatch_mps: float = 4.0
    # A track that received no return for longer than this is ended.
    max_track_gap_s: float = 0.5
    # Sweeps with moving returns needed before a tentative track is reported.
    min_track_frames: int = 5
    # Kalman filter noise: measured position, Doppler speed, unmodelled
    # acceleration (emergency braking reaches 8-10 m/s^2; 3 m/s^2 lost S01's
    # stopping lead car).
    measurement_std_m: float = 0.5
    radial_speed_std_mps: float = 0.3
    acceleration_std_mps2: float = 6.0


@dataclass
class SemanticsConfig:
    brake_onset_threshold: float = 0.1
    # Throttle onsets are only reported for strong demand (e.g. hard acceleration).
    throttle_onset_threshold: float = 0.8
    full_stop_speed_mps: float = 0.3
    closing_speed_threshold_mps: float = 1.0
    critical_ttc_s: float = 2.0
    # Half width of the straight-ahead corridor used for ENTERED_EGO_PATH.
    path_half_width_m: float = 1.5


@dataclass
class FusionConfig:
    # Two collision reports are the same contact if their peak impulses differ
    # by at most this fraction (equal and opposite impulses).
    impulse_tolerance: float = 0.10
    # A track "is at the contact" if it was seen within this window before the
    # matched collision and at most this range from the recorder's radar.
    contact_window_s: float = 0.5
    contact_range_m: float = 3.5
    # Required tracking history before the contact.
    min_track_persistence_s: float = 1.0
    # Track speed versus the partner's own reported speed (frame independent).
    speed_consistency_mps: float = 1.5


@dataclass
class ReconstructionConfig:
    trace_hz: float = 10.0
    collision: CollisionConfig = field(default_factory=CollisionConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    semantics: SemanticsConfig = field(default_factory=SemanticsConfig)
    fusion: FusionConfig = field(default_factory=FusionConfig)

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"trace_hz": self.trace_hz}
        for section in ("collision", "tracking", "semantics", "fusion"):
            value = getattr(self, section)
            out[section] = {item.name: getattr(value, item.name) for item in fields(value)}
        return out


def _section(cls, values: Optional[Mapping[str, Any]]):
    values = dict(values or {})
    known = {item.name for item in fields(cls)}
    unknown = sorted(set(values) - known)
    if unknown:
        raise ValueError("unknown {0} parameters: {1}".format(cls.__name__, ", ".join(unknown)))
    return cls(**values)


def config_from_mapping(data: Optional[Mapping[str, Any]]) -> ReconstructionConfig:
    """Build a config from the ``reconstruction:`` mapping, rejecting typos."""
    data = dict(data or {})
    unknown = sorted(set(data) - {"trace_hz", "collision", "tracking", "semantics", "fusion"})
    if unknown:
        raise ValueError("unknown reconstruction sections: " + ", ".join(unknown))
    return ReconstructionConfig(
        trace_hz=float(data.get("trace_hz", 10.0)),
        collision=_section(CollisionConfig, data.get("collision")),
        tracking=_section(TrackingConfig, data.get("tracking")),
        semantics=_section(SemanticsConfig, data.get("semantics")),
        fusion=_section(FusionConfig, data.get("fusion")),
    )


def load_config(path: Optional[Path] = None) -> ReconstructionConfig:
    """Load ``configs/reconstruction.yaml`` (or ``path``); defaults if absent."""
    if path is None:
        path = Path(__file__).resolve().parents[3] / "configs" / "reconstruction.yaml"
    path = Path(path)
    if not path.exists():
        return ReconstructionConfig()
    import yaml  # only needed when a file is read

    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return config_from_mapping(document.get("reconstruction", {}))
