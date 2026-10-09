"""The few reconstruction parameters that genuinely need tuning.

Defaults are physically motivated and were checked on the S01-S03 recordings;
``configs/reconstruction.yaml`` mirrors them with one comment per value.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

# UN Regulation No. 157 (ALKS), vehicles of categories M1 / N1: present speed (km/h) -> minimum
# following time gap (s).  An engineering anchor for the safe following distance of CRITICAL_TTC,
# not a legal rule for human drivers (reconstruction/conflict.py).
UNECE_R157_TIME_GAP = ((7.2, 1.0), (10.0, 1.1), (20.0, 1.2), (30.0, 1.3), (40.0, 1.4), (50.0, 1.5), (60.0, 1.6))


@dataclass
class CollisionConfig:
    # The collision sensor calls back once per sample while bodies touch, with
    # the impulse magnitude only.  Callbacks without a missing sample between
    # them form a burst.  A pause longer than this always separates two contacts.
    merge_gap_s: float = 0.5
    # After a shorter break (at least one sample without a callback) a burst
    # peaking at this fraction of the current contact's peak or more is a new
    # impact: the strongest rebound of the same two bodies measured in CARLA
    # came back with 0.52 of the first impulse (0.43 in the earlier recordings),
    # persistent contact with 0.25 or less, a second body with 0.85-0.93.
    new_impact_ratio: float = 0.75
    # Below this fraction the burst continues the contact (persistent contact).
    min_impact_ratio: float = 0.25
    # A burst weaker than this (N*s) never starts a new contact within merge_gap_s,
    # whatever its ratio: bodies scraping or pushing along each other (S16: a 2 s
    # scrape of 35-320 N*s bursts).  1000 N*s changes a 1.2-2.5 t vehicle's speed by
    # 0.4-0.8 m/s; every distinct impact measured in the campaign was stronger.
    min_new_impact_impulse: float = 1000.0
    # In between, the recorder's own velocity jumps decide when both, at the
    # contact's start and at the burst's, are impact-like (a mean acceleration
    # of at least impact_acceleration_mps2 across the callback: about twice what
    # tyres can produce, so neither braking nor steering): directions more than
    # reversal_angle_deg apart are a new impact from the other side, closer
    # ones a rebound (it pushes the recorder the same way again).  Without that
    # evidence the burst is a new impact from undirected_impact_ratio.
    impact_acceleration_mps2: float = 20.0
    reversal_angle_deg: float = 90.0
    undirected_impact_ratio: float = 0.5


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
    # A confirmed track whose target stops abruptly (a crash: tens of m/s^2, the
    # Doppler speed leaves the gate in one sweep) may take this many returns or
    # more whose speed lies between standstill and the predicted one, when its
    # previous sweep was free of foreign returns (tracking._slowdown_gate).
    min_slowdown_returns: int = 3


@dataclass
class SemanticsConfig:
    # Brake level that starts braking (BRAKE_START); below it braking ends.
    brake_onset_threshold: float = 0.1
    # Accelerator pedal (THROTTLE_START / THROTTLE_END): on at or above this level, off at or
    # below the release level (hysteresis), and a release shorter than the debounce does not end
    # it.  The recorded throttle is 0 (coasting, braking) or 0.15-1.0 (cruise, acceleration);
    # only about 0.5 % of the samples lie between 0.02 and 0.10.
    throttle_on_threshold: float = 0.10
    throttle_off_threshold: float = 0.05
    throttle_release_debounce_s: float = 0.2
    # Below this speed the recorder is stopped (STOP_START); it moves again above 1 m/s.
    full_stop_speed_mps: float = 0.3
    # Hysteresis around the supplied speed limit: exceeding starts above
    # limit + this and ends at or below limit - this.
    speed_limit_hysteresis_kmh: float = 1.0
    closing_speed_threshold_mps: float = 1.0
    # CRITICAL_TTC (reconstruction/conflict.py): a predicted collision course
    # (the recorder's safety envelope and the target's box overlap within the
    # horizon, both moving as now) that braking cannot avoid with the available
    # deceleration.  The braking vehicle reacts after this time...
    critical_reaction_time_s: float = 1.0
    # ...then brakes at up to this deceleration (hard, non-emergency braking on
    # a dry road; emergency braking reaches about 8-10 m/s^2)...
    critical_deceleration_mps2: float = 6.0
    # ...and must keep at least this distance ahead / behind (the envelope)...
    critical_standstill_margin_m: float = 1.0
    # ...and this much at the sides.
    critical_lateral_margin_m: float = 0.3
    # The state ends once the required deceleration falls below this fraction
    # of the available one, or no collision course remains (hysteresis).
    critical_release_ratio: float = 0.75
    # Prediction horizon and step of the collision-course test.
    prediction_horizon_s: float = 6.0
    prediction_time_step_s: float = 0.05
    # The radar measures no size: a target is a box of this nominal size (a
    # passenger car) behind its observed near surface...
    target_length_m: float = 4.6
    target_width_m: float = 1.9
    # ...that keeps its measured deceleration until it stops when it brakes at
    # least this hard (otherwise its velocity is held constant).
    target_braking_min_mps2: float = 1.0
    # No CRITICAL_TTC claim (either way) on a track younger than this.
    critical_min_track_age_s: float = 0.5
    # CRITICAL_TTC also for an unsafe forward gap (UNSAFE_FORWARD_GAP): a leader (same direction,
    # body ahead of the front face, in the path corridor or within the front-lateral margin of it
    # while approaching it) closer than the larger of the time-gap distance (speed x this table's
    # time gap, linear interpolation, ends held, at least the minimum distance) and the braking
    # distance (reaction + own braking - the lead's braking at the lead deceleration + d0).
    critical_time_gap_table: Tuple[Tuple[float, float], ...] = UNECE_R157_TIME_GAP
    critical_min_following_distance_m: float = 2.0
    # Hypothetical braking of the vehicle ahead (its measured acceleration is not used).
    critical_lead_deceleration_mps2: float = 6.0
    # The recorder must be moving: a standing recorder follows nobody.
    critical_forward_min_speed_mps: float = 1.0
    # Beside the corridor a body counts only within this margin and approaching it laterally at
    # least this fast beyond the velocity uncertainty (a car keeping its lane next to the
    # corridor is not a leader; in 3.5 m lanes it sits about 1 m outside the 3 m corridor).
    critical_front_lateral_margin_m: float = 1.0
    critical_front_lateral_speed_mps: float = 0.3
    # The forward-gap reason ends once the clearance exceeds this factor x the required distance.
    critical_forward_release_factor: float = 1.10
    # A track whose line of sight from the recorder crosses another track's nominal box grown by
    # this margin (the radar's position noise, tracking.measurement_std_m) is seen past that
    # vehicle: no CUT_IN evidence and no forward-gap evidence either way.
    occlusion_margin_m: float = 0.5
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
    # Half width of the straight-ahead corridor used for EGO_PATH_ENTRY / EXIT;
    # the corridor starts at the recorder's front edge (its own footprint).
    path_half_width_m: float = 1.5
    # TRACK_APPEARED_FRONT when the track's first bearing from the vehicle
    # origin lies within this angle of the recorder's heading (about its own
    # lane at 20 m); otherwise TRACK_APPEARED_LEFT (negative bearing) or _RIGHT.
    # There is no rear radar, so nothing appears straight behind.
    track_appeared_front_deg: float = 5.0
    # Track estimates more uncertain than this (Kalman standard deviations)
    # support no CUT_IN claim: it stays UNKNOWN.
    max_position_std_m: float = 1.0
    max_velocity_std_mps: float = 1.0
    # CUT_IN_FROM_LEFT/RIGHT: a target ahead, moving within this angle of the
    # recorder's heading and at least this fast, approaches the corridor
    # laterally at this speed or more, for this long, starting at least this
    # far outside the corridor, by at least this lateral displacement, and is
    # due to reach the corridor within this lateral time...
    cut_in_max_heading_deg: float = 25.0
    cut_in_min_target_speed_mps: float = 2.0
    cut_in_lateral_speed_mps: float = 0.3
    cut_in_persistence_s: float = 0.5
    cut_in_outside_margin_m: float = 0.5
    cut_in_min_displacement_m: float = 0.5
    cut_in_horizon_s: float = 3.0
    # ...and its nominal body is already within this distance of the corridor (pre-entry): a car
    # still crossing a lane further away is not cutting in yet.
    cut_in_preentry_margin_m: float = 1.0
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
    # this window before the matched collision: a radar can lose a target just
    # before impact (point blank, seen from the roof, or tracked through the
    # crash).  Identity association only: the tracker itself still ends a
    # silent track after tracking.max_track_gap_s (TRACK_LOST), and every other
    # check (persistence, approach, speed, matched collision, uniqueness) holds.
    contact_window_s: float = 1.0
    # Clearance at the contact is evidence, not a veto: up to this distance it
    # counts fully; beyond it the confidence decays with this scale (vehicle
    # geometry, impact orientation and a roof radar's view can keep it high).
    contact_range_m: float = 3.5
    contact_range_scale_m: float = 3.0
    # The range must shrink over this last stretch of tracking before the contact.
    approach_window_s: float = 1.0
    # Required tracking history before the contact.
    min_track_persistence_s: float = 1.0
    # Track speed versus the partner's own reported speed (frame independent).
    speed_consistency_mps: float = 1.5
    # Several compatible tracks for one contact are ambiguous, unless exactly one
    # of them touches the recorder: observed within one sample of the contact,
    # its near surface at most touching_clearance_m from the recorder's body,
    # while every rival is at least rival_clearance_m away (a long vehicle seen
    # as two tracks, S16's van: the one at its touching end is the partner).
    touching_clearance_m: float = 1.0
    rival_clearance_m: float = 2.0


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
