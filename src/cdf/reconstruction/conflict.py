"""Collision course and braking avoidability of a radar track: the CRITICAL_TTC model.

Everything is local to one recorder: its own odometry (speed, yaw rate), its own
footprint and one smoothed radar track.  At each track sample the future is
predicted over ``prediction_horizon_s`` in the recorder's vehicle frame:

  recorder  its footprint, inflated into a safety envelope (the standstill
            margin d0 ahead and behind, ``critical_lateral_margin_m`` at the
            sides), moving along its current path: constant speed and yaw rate
            (a circular arc, a straight line when not turning);
  target    a box of nominal size (``target_length_m`` x ``target_width_m``: the
            radar measures no size) placed behind its observed near surface
            (the corner towards the recorder when seen obliquely, the middle of
            the facing side when seen along one of its axes) and moving at its
            estimated velocity.  Its velocity across the recorder's heading
            counts only beyond the estimate's uncertainty (a car's null
            hypothesis is to keep its lane).  A target decelerating at least
            ``target_braking_min_mps2`` keeps its measured deceleration until
            it stops.

1. COLLISION COURSE: the two boxes overlap somewhere within the horizon.  The
   time of the first overlap is the TTC; the span of overlapping instants is the
   temporal overlap of the two vehicles in the conflict area.  A target that
   approaches radially but passes ahead of or behind the recorder never
   overlaps: no collision course, whatever its range rate.  A target already
   inside the envelope counts only while it still closes in.
2. AVOIDANCE BY BRAKING: the smallest deceleration that removes every overlap
   when the braking vehicle reacts after ``critical_reaction_time_s`` and then
   brakes along its path until it stops (bisection; the overlap disappears
   monotonically with harder braking).  The braking vehicle is the recorder
   when its braking can avoid the conflict (it closes on the target, or crosses
   its path); when even an instant stop of the recorder cannot (a target
   closing in from behind or from the side), it is the target, with the same
   reaction time.
3. CRITICAL: a collision course whose required deceleration is at least the
   available one (``critical_deceleration_mps2``), claimed only while the track
   estimate is precise enough (``max_position_std_m``, ``max_velocity_std_mps``,
   as for CUT_IN) and the track at least ``critical_min_track_age_s`` old: a
   young track's velocity is not yet known (the smoother's uncertainty at a
   track's first samples already draws on later data and understates it).

For a target ahead in the same lane this is the stopping-capability check of a
following vehicle: with the reaction distance, the braking distance and the
margin it must stop short of the target, which keeps its speed or (when
braking) its measured deceleration.  This is the idea of the safety distance of
art. 149 of the Italian Highway Code (room to stop if the vehicle ahead brakes),
used as a concept only: the code prescribes no numbers.  For crossing traffic the
space-time overlap of the two predicted footprints replaces any one-dimensional
distance: a car that crosses ahead of or behind the recorder's envelope is not
on a collision course, whatever its range rate.

Parameters are global and documented in ``configs/reconstruction.yaml``; they
are modelling assumptions, not a norm.  Limits: constant velocity / yaw rate
(no intent, no lane geometry), a nominal target size, braking as the only
avoidance manoeuvre (no swerve), one track at a time (no occlusion of the
predicted paths by third vehicles).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np

from .config import SemanticsConfig
from .tracking import EgoFootprint, EgoState, TrackSample

# Bisection on the deceleration: upper bound (no road vehicle brakes harder) and steps.
MAX_SEARCH_DECELERATION_MPS2 = 30.0
BISECTION_STEPS = 14
# Below this speed a target's heading is unknown: it is taken parallel to the recorder.
HEADING_MIN_SPEED_MPS = 1.0
# The recorder's path curvature is limited to this (a 5 m radius).
MAX_CURVATURE_PER_M = 0.2
# Beyond this angle between the line of sight and a target's axis, its near surface point is
# taken as the corner towards the recorder (see _Prediction).
OBLIQUE_VIEW_DEG = 20.0


@dataclass
class ConflictAssessment:
    """What the prediction says about one target at one instant."""

    encounter: str  # SAME_DIRECTION, OPPOSING, CROSSING, OBLIQUE or STATIONARY
    collision_course: bool
    ttc_s: Optional[float]  # time to the first predicted overlap (constant speeds)
    overlap_s: Optional[Tuple[float, float]]  # first and last predicted overlapping instants
    required_deceleration_mps2: Optional[float]  # None without collision course; inf: braking cannot avoid it
    avoidance_by: Optional[str]  # "recorder" or "target": whose braking the requirement refers to
    available_deceleration_mps2: float
    critical: bool
    known: bool  # the track estimate is precise enough for a claim (max_position_std_m, max_velocity_std_mps)
    target_speed_mps: float
    target_acceleration_mps2: float  # used in the prediction (0 unless it brakes)
    ego_speed_mps: float

    @property
    def braking_margin_mps2(self) -> Optional[float]:
        """Available minus required deceleration (negative when critical)."""
        if self.required_deceleration_mps2 is None or math.isinf(self.required_deceleration_mps2):
            return None
        return self.available_deceleration_mps2 - self.required_deceleration_mps2


def _corners(half_x: float, half_y: float) -> np.ndarray:
    return np.array([[half_x, half_y], [half_x, -half_y], [-half_x, -half_y], [-half_x, half_y]])


def _overlap(centre_a: np.ndarray, angle_a: np.ndarray, half_a: Tuple[float, float],
             centre_b: np.ndarray, angle_b: float, half_b: Tuple[float, float]) -> np.ndarray:
    """Separating-axis test of two oriented rectangles, vectorised over time (A moves, B's angle is fixed)."""
    ca, sa = np.cos(angle_a), np.sin(angle_a)
    axes_a = [np.column_stack([ca, sa]), np.column_stack([-sa, ca])]
    cb, sb = math.cos(angle_b), math.sin(angle_b)
    axes_b = [np.tile([cb, sb], (len(angle_a), 1)), np.tile([-sb, cb], (len(angle_a), 1))]
    offset = centre_b - centre_a
    separated = np.zeros(len(angle_a), dtype=bool)
    for axis in axes_a + axes_b:
        radius_a = half_a[0] * np.abs(np.sum(axes_a[0] * axis, axis=1)) + half_a[1] * np.abs(np.sum(axes_a[1] * axis, axis=1))
        radius_b = half_b[0] * np.abs(np.sum(axes_b[0] * axis, axis=1)) + half_b[1] * np.abs(np.sum(axes_b[1] * axis, axis=1))
        separated |= np.abs(np.sum(offset * axis, axis=1)) > radius_a + radius_b
    return ~separated


def _travel(times: np.ndarray, speed: float, reaction: float, deceleration: float) -> np.ndarray:
    """Distance along the path: constant speed until ``reaction``, then braking at ``deceleration`` to a stop."""
    distance = speed * np.minimum(times, reaction)
    after = np.maximum(times - reaction, 0.0)
    if deceleration <= 0.0:
        return distance + speed * after
    stop = speed / deceleration
    braking = np.minimum(after, stop)
    return distance + speed * braking - 0.5 * deceleration * braking * braking


def _target_travel(times: np.ndarray, speed: float, acceleration: float) -> np.ndarray:
    """Distance of a target that keeps a (negative) acceleration until it stops."""
    if acceleration >= 0.0 or speed <= 0.0:
        return speed * times
    stop = speed / -acceleration
    moving = np.minimum(times, stop)
    return speed * moving + 0.5 * acceleration * moving * moving


def _encounter(target_speed: float, angle_deg: float) -> str:
    if target_speed < HEADING_MIN_SPEED_MPS:
        return "STATIONARY"
    angle = abs(angle_deg)
    if angle <= 30.0:
        return "SAME_DIRECTION"
    if angle >= 150.0:
        return "OPPOSING"
    if 60.0 <= angle <= 120.0:
        return "CROSSING"
    return "OBLIQUE"


class _Prediction:
    """The two predicted footprints of one sample, ready for repeated overlap tests."""

    def __init__(self, sample: TrackSample, own: EgoState, footprint: Optional[EgoFootprint],
                 cfg: SemanticsConfig) -> None:
        self.cfg = cfg
        self.times = np.arange(0.0, cfg.prediction_horizon_s + 1e-9, cfg.prediction_time_step_s)
        c, s = math.cos(own.heading), math.sin(own.heading)
        self.ego_speed = max(c * own.vx + s * own.vy, 0.0)
        curvature = own.yaw_rate / self.ego_speed if self.ego_speed > 1.0 else 0.0
        self.curvature = max(-MAX_CURVATURE_PER_M, min(MAX_CURVATURE_PER_M, curvature))
        if footprint is None:
            footprint = EgoFootprint(-2.3, 2.3, -0.95, 0.95)
        d0, lateral = cfg.critical_standstill_margin_m, cfg.critical_lateral_margin_m
        x_min, x_max = footprint.x_min - d0, footprint.x_max + d0
        y_min, y_max = footprint.y_min - lateral, footprint.y_max + lateral
        self.ego_half = ((x_max - x_min) / 2.0, (y_max - y_min) / 2.0)
        self.ego_offset = np.array([(x_max + x_min) / 2.0, (y_max + y_min) / 2.0])
        # Target: ground velocity in the recorder's axes, heading, near surface, box centre.
        tvx, tvy = c * sample.vx_mps + s * sample.vy_mps, -s * sample.vx_mps + c * sample.vy_mps
        # The target's motion across the recorder's heading counts only beyond the uncertainty of
        # its estimate: a radar track's median point slides over the target's visible body while
        # the view angle changes (S08: an oncoming car passing beside the recorder looked 1 m/s
        # closer to its lane than it was), and the null hypothesis for a car is to keep to its
        # lane, parallel to the recorder, not to head straight at it.
        tvy = math.copysign(max(abs(tvy) - sample.vel_std_mps, 0.0), tvy)
        self.target_speed = math.hypot(tvx, tvy)
        if self.target_speed >= HEADING_MIN_SPEED_MPS:
            ux, uy = tvx / self.target_speed, tvy / self.target_speed
        else:
            ux, uy = 1.0, 0.0
        self.target_angle = math.atan2(uy, ux)
        acceleration = sample.acceleration_mps2 if self.target_speed >= HEADING_MIN_SPEED_MPS else 0.0
        self.target_acceleration = (max(acceleration, -MAX_SEARCH_DECELERATION_MPS2)
                                    if acceleration <= -cfg.target_braking_min_mps2 else 0.0)
        px, py = sample.longitudinal_m, sample.lateral_m
        nx, ny = footprint.outward(px, py)
        near = np.array([px - sample.surface_offset_m * nx, py - sample.surface_offset_m * ny])
        length, width = cfg.target_length_m, cfg.target_width_m
        # The near surface point is the part of the target closest to the recorder: seen obliquely,
        # the corner towards it; seen along one of its axes, the middle of the facing side.  The
        # box lies behind it, in each of its two axes by a weight growing from 0 (looking along
        # that face) to 1 at OBLIQUE_VIEW_DEG and beyond.
        gx, gy = -nx, -ny  # from the target towards the recorder
        along, across = gx * ux + gy * uy, gx * -uy + gy * ux  # in the target's axes (across = its right)
        oblique = math.sin(math.radians(OBLIQUE_VIEW_DEG))
        weight_along, weight_across = min(abs(along) / oblique, 1.0), min(abs(across) / oblique, 1.0)
        centre = (near - math.copysign(length / 2.0 * weight_along, along) * np.array([ux, uy])
                  - math.copysign(width / 2.0 * weight_across, across) * np.array([-uy, ux]))
        self.target_centre = centre
        self.target_unit = np.array([ux, uy])
        self.target_half = (length / 2.0, width / 2.0)
        self.encounter = _encounter(self.target_speed, math.degrees(self.target_angle))

    def ego_pose(self, travel: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Envelope centres and headings after travelling ``travel`` metres along the path."""
        k = self.curvature
        if abs(k) < 1e-6:
            x, y, theta = travel, np.zeros_like(travel), np.zeros_like(travel)
        else:
            theta = k * travel
            x, y = np.sin(theta) / k, (1.0 - np.cos(theta)) / k
        c, s = np.cos(theta), np.sin(theta)
        ox, oy = self.ego_offset
        return np.column_stack([x + c * ox - s * oy, y + s * ox + c * oy]), theta

    def overlaps(self, ego_deceleration: float = 0.0, ego_reaction: float = 0.0,
                 target_deceleration: float = 0.0, target_reaction: float = 0.0) -> np.ndarray:
        """Overlap at every predicted instant, given who brakes how hard after what reaction time."""
        centres, angles = self.ego_pose(_travel(self.times, self.ego_speed, ego_reaction, ego_deceleration))
        if target_deceleration > 0.0:
            moved = _travel(self.times, self.target_speed, target_reaction, target_deceleration)
        else:
            moved = _target_travel(self.times, self.target_speed, self.target_acceleration)
        targets = self.target_centre + moved[:, None] * self.target_unit
        return _overlap(centres, angles, self.ego_half, targets, self.target_angle, self.target_half)


def _required(predict) -> float:
    """Smallest deceleration (bisection) for which ``predict(a)`` shows no overlap; inf if none suffices."""
    if predict(MAX_SEARCH_DECELERATION_MPS2).any():
        return math.inf
    low, high = 0.0, MAX_SEARCH_DECELERATION_MPS2
    for _ in range(BISECTION_STEPS):
        middle = 0.5 * (low + high)
        if predict(middle).any():
            low = middle
        else:
            high = middle
    return high


def assess_conflict(sample: TrackSample, own: EgoState, footprint: Optional[EgoFootprint],
                    cfg: SemanticsConfig, track_age_s: Optional[float] = None) -> ConflictAssessment:
    """Collision course, TTC and braking avoidability of one track sample (see the module docstring).

    ``track_age_s``: time since the track's first sample (None: old enough).
    """
    prediction = _Prediction(sample, own, footprint, cfg)
    available = cfg.critical_deceleration_mps2
    known = (sample.pos_std_m <= cfg.max_position_std_m and sample.vel_std_mps <= cfg.max_velocity_std_mps
             and (track_age_s is None or track_age_s >= cfg.critical_min_track_age_s - 1e-9))
    result = ConflictAssessment(encounter=prediction.encounter, collision_course=False, ttc_s=None, overlap_s=None,
                                required_deceleration_mps2=None, avoidance_by=None,
                                available_deceleration_mps2=available, critical=False, known=known,
                                target_speed_mps=prediction.target_speed,
                                target_acceleration_mps2=prediction.target_acceleration,
                                ego_speed_mps=prediction.ego_speed)
    overlap = prediction.overlaps()
    if not overlap.any():
        return result
    if overlap[0] and sample.closing_speed_mps < cfg.closing_speed_threshold_mps:
        return result  # already inside the envelope, but no longer closing in
    times = prediction.times[overlap]
    result.collision_course = True
    result.ttc_s = round(float(times[0]), 3)
    result.overlap_s = (round(float(times[0]), 3), round(float(times[-1]), 3))
    reaction = cfg.critical_reaction_time_s
    if not prediction.overlaps(ego_deceleration=MAX_SEARCH_DECELERATION_MPS2).any():
        # The recorder's own braking can remove the overlap (it closes on the target or
        # crosses its path): its requirement, with its reaction time.
        required = _required(lambda a: prediction.overlaps(ego_deceleration=a, ego_reaction=reaction))
        by = "recorder"
    else:
        # Even an instant stop of the recorder leaves the overlap (a target closing in from
        # behind or from the side): only the target's braking can avoid it.
        required = _required(lambda b: prediction.overlaps(target_deceleration=b, target_reaction=reaction))
        by = "target"
    result.required_deceleration_mps2 = required
    result.avoidance_by = by
    result.critical = known and required >= available
    return result
