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
    # The collision sensor calls back once per sample while bodies touch, with
    # the impulse magnitude only.  Callbacks without a missing sample between
    # them form a burst.  A pause longer than this always separates two contacts.
    merge_gap_s: float = 0.5
    # A shorter pause separates them when the burst after the break (at least
    # one sample without a callback) peaks at this fraction of the current
    # contact's peak or more: a rebound of the same two bodies comes back with
    # about the restitution coefficient times the first impulse (below 0.5
    # between vehicles) and the persistent contact after an impact with far less.
    new_impact_ratio: float = 0.5
    # Supplementary evidence, never decisive alone: a weaker burst (from this
    # fraction of the contact's peak) also starts a new contact when the
    # recorder's own velocity jumps like an impact both at the contact's start
    # and at the burst's, in directions more than reversal_angle_deg apart (a
    # rebound pushes the recorder the same way again).  An impact-like jump is
    # a mean acceleration of at least impact_acceleration_mps2 from the sample
    # before the callback to the sample after it: twice what tyres can produce
    # (about 1 g), so braking or steering cannot cause it.
    reversal_impact_ratio: float = 0.25
    impact_acceleration_mps2: float = 20.0
    reversal_angle_deg: float = 90.0


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
    # Brake level that starts braking (BRAKE_START); below it braking ends.
    brake_onset_threshold: float = 0.1
    # Below this speed the recorder is stopped (STOP_START); it moves again above 1 m/s.
    full_stop_speed_mps: float = 0.3
    # Hysteresis around the supplied speed limit: exceeding starts above
    # limit + this and ends at or below limit - this.
    speed_limit_hysteresis_kmh: float = 1.0
    closing_speed_threshold_mps: float = 1.0
    # CRITICAL_TTC: avoiding the target by braking would need at least the
    # available deceleration.  The recorder reacts after this time...
    critical_reaction_time_s: float = 1.0
    # ...then brakes at up to this deceleration (hard, non-emergency braking on
    # a dry road; emergency braking reaches about 8-10 m/s^2)...
    critical_deceleration_mps2: float = 6.0
    # ...and must keep at least this distance from the target.
    critical_standstill_margin_m: float = 1.0
    # The state ends once the required deceleration falls below this fraction
    # of the available one (hysteresis).
    critical_release_ratio: float = 0.75
    # TURN_LEFT / TURN_RIGHT from the recorder's own unwrapped heading: the yaw
    # rate (over the preceding window) reaches the on threshold while moving at least
    # the minimum speed, and the turn ends below the off threshold...
    turn_yaw_rate_window_s: float = 0.2
    turn_yaw_rate_on_dps: float = 10.0
    turn_yaw_rate_off_dps: float = 5.0
    turn_min_speed_mps: float = 1.0
    # ...unless the yaw rate recovers within this time (debounce).  A turn lasts
    # at least this long and changes the heading by at least this much, so lane
    # changes and road curvature are not turns.
    turn_release_debounce_s: float = 0.3
    turn_min_duration_s: float = 0.5
    turn_min_heading_change_deg: float = 15.0
    # Half width of the straight-ahead corridor used for EGO_PATH_ENTRY / EXIT.
    path_half_width_m: float = 1.5
    # TRACK_APPEARED_FRONT when the track's first azimuth from the radar lies
    # within this angle of the recorder's heading (about its own lane at 20 m);
    # otherwise TRACK_APPEARED_LEFT (negative azimuth) or _RIGHT.
    track_appeared_front_deg: float = 5.0
    # Track estimates more uncertain than this (Kalman standard deviations)
    # support no CUT_IN claim: it stays UNKNOWN.
    max_position_std_m: float = 1.0
    max_velocity_std_mps: float = 1.0
    # CUT_IN_FROM_LEFT/RIGHT: a target ahead, moving within this angle of the
    # recorder's heading and at least this fast, approaches the corridor
    # laterally at this speed or more, for this long, starting at least this
    # far outside the corridor, by at least this lateral displacement, and is
    # due to reach the corridor within this lateral time.
    cut_in_max_heading_deg: float = 25.0
    cut_in_min_target_speed_mps: float = 2.0
    cut_in_lateral_speed_mps: float = 0.3
    cut_in_persistence_s: float = 0.5
    cut_in_outside_margin_m: float = 0.5
    cut_in_min_displacement_m: float = 0.5
    cut_in_horizon_s: float = 3.0
    # The manoeuvre ends once its lateral approach stays below this speed this long.
    cut_in_settle_speed_mps: float = 0.2
    cut_in_settle_s: float = 0.3


@dataclass
class FusionConfig:
    # Two collision reports are the same contact if their peak impulses differ
    # by at most this fraction (equal and opposite impulses).
    impulse_tolerance: float = 0.10
    # A match also fixes the clock offset between its two graphs: a further
    # match between graphs already linked (directly or through other matches)
    # must imply the same offset within this (two sensor samples at 20 Hz).
    clock_tolerance_s: float = 0.1
    # A track is continuous up to the contact if it was still observed within
    # this window before the matched collision (radars lose a target at point
    # blank range or at the edge of their field of view just before impact).
    contact_window_s: float = 0.5
    # Range at the contact is evidence, not a veto: up to this range it counts
    # fully; beyond it the confidence decays with this scale (radar mount,
    # vehicle geometry and impact orientation can keep the last range high).
    contact_range_m: float = 3.5
    contact_range_scale_m: float = 3.0
    # The range must shrink over this last stretch of tracking before the contact.
    approach_window_s: float = 1.0
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
