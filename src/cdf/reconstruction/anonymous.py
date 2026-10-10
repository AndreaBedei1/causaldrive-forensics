"""Road users across observers in the common frame (reconstruction side, no ground truth).

Runs after the collision-anchored alignment and the collision-based identity association, on the
recorders' own data only: their pose streams (``common_frame.PoseSource``), their radar tracks and, in
memory, the radar returns each track claimed.  Every gate scales with the tracker's own noise parameters
(``tracking.measurement_std_m``, ``radial_speed_std_mps``, ``acceleration_std_mps2``) and the accuracy the
pose sources declare; nothing depends on a scenario.

1. OBSERVED ALIGNMENT (``align_by_observations``) of a recorder that no matched collision aligned: the
   clock offset at which the near surfaces the aligned recorders observed lie on its own footprint
   outline, or the near surfaces it observed lie on theirs.  Accepted only with a sharp, unique minimum:
   a target at rest gives no time information and leaves the recorder unaligned.
2. RECORDER LINKS (``link_to_recorders``): an anonymous track whose observed near surface lies on another
   recorder's own footprint outline, moving at that recorder's own velocity, over most of its life, is
   that recorder.  The footprint and the pose are the recorder's own: no face ambiguity.
3. ANONYMOUS ROAD USERS.  Two anonymous tracks of different observers are one road user when one rigid
   box (centre, half length, half width with priors, heading from the motion) explains the faces both
   observers' returns show, and their velocities agree, over most of their shared window
   (``pair_evidence``): radars at different places see different faces, so their track points differ by
   up to a car length while the box they imply is one.  The same test joins two simultaneous tracks of
   one observer that are faces of one body (a tracker splitting a road user).  Two tracks of one
   observer, the second starting shortly after the first ended where the first is predicted to be, are
   one road user (``stitch_evidence``).  A link with a rival (a second successor, or two simultaneous
   partners of one observer that are not one body) is refused.  The remaining links join tracks into
   entities, best first, never putting two simultaneous tracks of one observer into one entity unless a
   link showed them to be one body (``cluster``): U1, U2, ... by first appearance.
4. FUSED STATE of each entity (``entity_trajectory``): one box fitted to the faces the returns of all its
   observers show (``fit_box``: each visible face is a linear constraint on the centre and one half
   dimension); when the returns fix no box at an instant (one face of one observer, no heading), the
   observers' centre estimates are combined by covariance intersection, which assumes nothing about
   their cross-correlation.

A non-recording road user is never named after a participant: it is U1, U2, ...
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .common_frame import CommonSample, CommonTrack, PoseSource, RecorderBody, common_track, outline_distances
from .config import ReconstructionConfig
from .models import Alignment, Association, GraphClock

ASSOCIATED = "ASSOCIATED"
ANONYMOUS = "ANONYMOUS"
OBSERVED = "observed_trajectories"
CROSS, SPLIT, STITCH = "cross_observer", "same_observer", "stitch"


def chi2_2dof(probability: float) -> float:
    """Quantile of the chi-square distribution with 2 degrees of freedom (closed form)."""
    return -2.0 * math.log(1.0 - probability)


# --------------------------------------------------------------------------
# Box geometry: the visible faces as linear constraints
# --------------------------------------------------------------------------

def _faces(heading: float) -> List[Tuple[np.ndarray, np.ndarray, int]]:
    """(outward normal, tangent, half dimension: 0 = half length, 1 = half width) of front, rear, right, left."""
    f = np.array([math.cos(heading), math.sin(heading)])
    r = np.array([-math.sin(heading), math.cos(heading)])  # to the right of the heading (CARLA axes)
    return [(f, r, 0), (-f, r, 0), (r, f, 1), (-r, f, 1)]


@dataclass
class FaceMeasurement:
    normal: np.ndarray
    tangent: np.ndarray
    half: int  # 0: the face lies half a length from the centre, 1: half a width
    offset: float  # median of normal . p over the face's returns
    along: float  # median of tangent . p
    extent: float  # spread of the returns along the face (5th to 95th percentile): a lower bound of its size
    count: int
    observer: str
    pose_var: float  # what the observer's own pose adds (m^2)


def _initial_centre(sample: CommonSample, heading: Optional[float], halves: Tuple[float, float]) -> np.ndarray:
    """The near surface pushed back along the line of sight to where that ray meets the centre of a box
    of the prior size (the nominal box behind the near surface, for any viewing angle)."""
    line = sample.line_of_sight
    if heading is None:
        return sample.near + line * 0.5 * (halves[0] + halves[1])
    along = abs(line[0] * math.cos(heading) + line[1] * math.sin(heading))
    across = abs(-line[0] * math.sin(heading) + line[1] * math.cos(heading))
    depth = min(halves[0] / along if along > 1e-6 else math.inf, halves[1] / across if across > 1e-6 else math.inf)
    return sample.near + line * depth


def face_measurements(sample: CommonSample, observer: str, heading: float, centre: np.ndarray,
                      halves: Tuple[float, float], min_returns: int = 3) -> List[FaceMeasurement]:
    """The faces a sample's returns show: each return goes to the face visible from its own radar (outward
    normal against the line of sight) nearest to it for the current box; a face needs ``min_returns``.
    Without enough returns the observed near surface stands for one return."""
    faces = _faces(heading)
    if sample.returns is not None and sample.origins is not None and len(sample.returns) >= min_returns:
        points, origins = sample.returns, sample.origins
    else:
        points, origins = sample.near[None, :], sample.observer[None, :]
        min_returns = 1
    lines = points - origins
    lines = lines / np.maximum(np.hypot(lines[:, 0], lines[:, 1]), 1e-6)[:, None]
    best = np.full(len(points), -1)
    best_distance = np.full(len(points), np.inf)
    for index, (normal, _, half) in enumerate(faces):
        visible = (lines @ normal) < 0.0
        distance = np.abs((points - centre) @ normal - halves[half])
        better = visible & (distance < best_distance)
        best[better], best_distance[better] = index, distance[better]
    out = []
    for index, (normal, tangent, half) in enumerate(faces):
        chosen = best == index
        if int(chosen.sum()) >= min_returns:
            along = points[chosen] @ tangent
            extent = float(np.percentile(along, 95) - np.percentile(along, 5)) if len(along) >= 5 else 0.0
            out.append(FaceMeasurement(normal, tangent, half, float(np.median(points[chosen] @ normal)),
                                       float(np.median(along)), extent, int(chosen.sum()), observer,
                                       sample.pose_var))
    return out


@dataclass
class BoxFit:
    centre: np.ndarray
    halves: Tuple[float, float]
    covariance: np.ndarray  # 4 x 4: centre x, centre y, half length, half width
    chi2: float
    faces: int  # distinct faces observed
    observers: int  # observers whose faces entered the fit
    measurements: List[FaceMeasurement] = field(default_factory=list, repr=False)


def solve_box(measurements: Sequence[FaceMeasurement], cfg: ReconstructionConfig) -> BoxFit:
    """Weighted least squares for (centre, half length, half width) with each face as two linear constraints:
    normal . centre + half = offset (``fusion.box_face_std_m`` plus the observer's pose variance) and
    tangent . centre = along (returns spread over the face: half its size / sqrt(3)), plus priors on the
    dimensions (``semantics.target_length_m`` / ``target_width_m``, ``fusion.box_length_std_m`` / ``box_width_std_m``)."""
    fusion, semantics = cfg.fusion, cfg.semantics
    prior = (semantics.target_length_m / 2.0, semantics.target_width_m / 2.0)
    prior_std = (fusion.box_length_std_m / 2.0, fusion.box_width_std_m / 2.0)
    rows, values, sigmas = [], [], []
    for m in measurements:
        rows.append([m.normal[0], m.normal[1], 1.0 if m.half == 0 else 0.0, 1.0 if m.half == 1 else 0.0])
        values.append(m.offset)
        sigmas.append(math.sqrt(fusion.box_face_std_m ** 2 + m.pose_var))
        rows.append([m.tangent[0], m.tangent[1], 0.0, 0.0])
        values.append(m.along)
        sigmas.append(math.sqrt((prior[1 - m.half] / math.sqrt(3.0)) ** 2 + m.pose_var))
    rows += [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    values += [prior[0], prior[1]]
    sigmas += [prior_std[0], prior_std[1]]
    A, b, w = np.array(rows), np.array(values), 1.0 / np.array(sigmas)
    Aw = A * w[:, None]
    theta = np.linalg.lstsq(Aw, b * w, rcond=None)[0]
    residual = (A @ theta - b) * w
    covariance = np.linalg.pinv(Aw.T @ Aw)
    faces = {(round(float(m.normal[0]), 6), round(float(m.normal[1]), 6)) for m in measurements}
    return BoxFit(theta[:2], (float(theta[2]), float(theta[3])), covariance, float(residual @ residual),
                  len(faces), len({m.observer for m in measurements}), list(measurements))


def fit_box(observations: Sequence[Tuple[str, CommonSample]], heading: float, cfg: ReconstructionConfig,
            start: Optional[np.ndarray] = None, iterations: int = 3) -> BoxFit:
    """One box for the observations of one instant (``(observer, sample)`` pairs): the returns are
    re-assigned to the faces of the current estimate a few times (an ICP-like iteration)."""
    prior = (cfg.semantics.target_length_m / 2.0, cfg.semantics.target_width_m / 2.0)
    centre = start if start is not None else np.mean(
        [_initial_centre(sample, heading, prior) for _, sample in observations], axis=0)
    halves = prior
    fit = None
    for _ in range(iterations):
        measurements = [m for observer, sample in observations
                        for m in face_measurements(sample, observer, heading, centre, halves)]
        if not measurements:
            break
        fit = solve_box(measurements, cfg)
        centre, halves = fit.centre, fit.halves
    if fit is None:
        raise ValueError("no face measurement")
    return fit


# --------------------------------------------------------------------------
# Covariance intersection (fallback; no assumption on cross-correlation)
# --------------------------------------------------------------------------

def covariance_intersection(estimates: Sequence[Tuple[np.ndarray, np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
    """Sequential covariance intersection of (mean, covariance) pairs, each weight chosen to minimise the
    trace of the fused covariance (golden-section search)."""
    mean, cov = np.asarray(estimates[0][0], float), np.asarray(estimates[0][1], float)
    for other_mean, other_cov in estimates[1:]:
        inv_a, inv_b = np.linalg.pinv(cov), np.linalg.pinv(np.asarray(other_cov, float))
        other = np.asarray(other_mean, float)

        def fused(omega: float, inv_a: np.ndarray = inv_a, inv_b: np.ndarray = inv_b,
                  mean: np.ndarray = mean, other: np.ndarray = other) -> Tuple[np.ndarray, np.ndarray]:
            fused_cov = np.linalg.pinv(omega * inv_a + (1.0 - omega) * inv_b)
            return fused_cov @ (omega * inv_a @ mean + (1.0 - omega) * inv_b @ other), fused_cov

        lo, hi = 0.0, 1.0
        golden = (math.sqrt(5.0) - 1.0) / 2.0
        for _ in range(40):
            a, b = hi - golden * (hi - lo), lo + golden * (hi - lo)
            if np.trace(fused(a)[1]) < np.trace(fused(b)[1]):
                hi = b
            else:
                lo = a
        mean, cov = fused((lo + hi) / 2.0)
    return mean, cov


# --------------------------------------------------------------------------
# The recorders' tracks in the common frame
# --------------------------------------------------------------------------

@dataclass
class CommonView:
    """The aligned recorders' tracks and bodies in the common frame, on the global clock."""

    tracks: List[CommonTrack]
    bodies: Dict[str, RecorderBody]


def build_common_view(locals_: Sequence[Any], alignment: Alignment, associations: Sequence[Association],
                      poses: Dict[str, PoseSource]) -> CommonView:
    status = {(a.local_graph, a.local_track): a for a in associations}
    tracks, bodies = [], {}
    for local in sorted(locals_, key=lambda item: item.owner):
        clock = alignment.graphs.get(local.owner)
        if clock is None or clock.status != "ALIGNED" or clock.offset_to_global is None:
            continue
        partners = {event["nodes"][local.owner]: tuple(sorted(g for g in event["graphs"] if g != local.owner))
                    for event in alignment.matched_events if local.owner in event["nodes"]}
        contacts = tuple(sorted((round(node.t_local + clock.offset_to_global, 4), partners.get(node.node_id, ()))
                                for node in local.graph.nodes if node.event_type == "COLLISION"))
        bodies[local.owner] = RecorderBody(local.owner, poses[local.owner], local.footprint, clock.offset_to_global,
                                           contacts)
        for track in local.tracks:
            item = status.get((local.owner, track.track_id))
            linked = item is not None and item.status == ASSOCIATED
            tracks.append(common_track(track, local.owner, local.ego, poses[local.owner], local.footprint,
                                       clock.offset_to_global, ASSOCIATED if linked else ANONYMOUS,
                                       item.global_entity if linked else None))
    return CommonView(tracks, bodies)


def _position_sigma(cfg: ReconstructionConfig, sample: CommonSample, body_source: Optional[PoseSource] = None) -> float:
    """Spread of an observed near surface around the true outline: the tracker's measurement noise, the
    observer's pose and, when the outline is another recorder's, that recorder's pose."""
    other = body_source.position_std_m ** 2 if body_source is not None else 0.0
    return math.sqrt(cfg.tracking.measurement_std_m ** 2 + sample.pose_var + other)


def _velocity_sigma(cfg: ReconstructionConfig, *stds: float) -> float:
    """Per-axis spread of a velocity difference: the estimates' own uncertainties, none below the Doppler
    measurement noise (``tracking.radial_speed_std_mps``)."""
    floor = cfg.tracking.radial_speed_std_mps
    return math.sqrt(sum(max(std, floor) ** 2 for std in stds))


# --------------------------------------------------------------------------
# 1. Observed alignment of recorders no collision aligned
# --------------------------------------------------------------------------

def _moving(track: CommonTrack, cfg: ReconstructionConfig) -> List[CommonSample]:
    return [s for s in track.samples if s.measured and s.speed >= cfg.fusion.observed_alignment_min_speed_mps]


def _components(mask: np.ndarray) -> List[Tuple[int, int]]:
    """(first, last) index of every run of True in a boolean array."""
    runs, start = [], None
    for index, value in enumerate(mask):
        if value and start is None:
            start = index
        if not value and start is not None:
            runs.append((start, index - 1))
            start = None
    if start is not None:
        runs.append((start, len(mask) - 1))
    return runs


def align_by_observations(locals_: Sequence[Any], alignment: Alignment, associations: Sequence[Association],
                          poses: Dict[str, PoseSource], cfg: ReconstructionConfig) -> List[Dict[str, Any]]:
    """Give each unaligned recorder the clock offset its observations fix, when they fix one.

    Comparisons: every anonymous track of an aligned recorder against the recorder's own footprint
    outline (at t_global - delta), and every own track of the recorder against an aligned recorder's
    outline (at t_local + delta), on samples of a target moving at least ``observed_alignment_min_speed_mps``
    (only motion fixes time).  A comparison's curve is the median normalised outline distance
    (``_position_sigma``) over its samples the two recordings both cover, defined where at least
    ``observed_alignment_min_samples`` and half of its samples are covered.  The comparisons whose curve
    reaches 2 sigma somewhere could be the same body; their samples are pooled, and the pooled median is
    the score of each candidate offset (every ``observed_alignment_step_s``).  The best offset is accepted
    when its score is within 2 sigma and the offsets scoring within ``max(uniqueness_ratio x best, 2)``
    form one connected interval: a second interval is a second explanation (a target at rest, or moving
    along its own outline, fixes no time) and leaves the recorder unaligned.  That interval is the
    offset's uncertainty.  Accepted offsets are written into ``alignment`` (method
    ``observed_trajectories``); every decision is returned and kept in ``alignment.observed``."""
    fusion = cfg.fusion
    by_owner = {local.owner: local for local in locals_}
    decisions: List[Dict[str, Any]] = []
    pending = sorted(owner for owner, clock in alignment.graphs.items() if clock.status != "ALIGNED")
    progress = True
    while pending and progress:
        progress = False
        view = build_common_view(locals_, alignment, associations, poses)
        if not view.bodies:
            break
        for recorder in list(pending):
            local, source = by_owner[recorder], poses[recorder]
            # (name, outline pose source, its footprint, sample times, sign of delta, outline clock offset, near, sigma)
            comparisons = []
            for track in view.tracks:
                if track.status == ASSOCIATED:
                    continue  # already identified with another recorder
                samples = _moving(track, cfg)
                if len(samples) >= fusion.observed_alignment_min_samples:
                    comparisons.append((track.name, source, local.footprint, np.array([s.t_global for s in samples]),
                                        -1.0, 0.0, np.array([s.near for s in samples]),
                                        np.array([_position_sigma(cfg, s, source) for s in samples])))
            for track in local.tracks:
                own = common_track(track, recorder, local.ego, source, local.footprint, 0.0)
                samples = _moving(own, cfg)
                if len(samples) < fusion.observed_alignment_min_samples:
                    continue
                for body in view.bodies.values():
                    comparisons.append(("{0} on {1}".format(own.name, body.recorder), body.poses, body.footprint,
                                        np.array([s.t_local for s in samples]), 1.0, body.offset_to_global,
                                        np.array([s.near for s in samples]),
                                        np.array([_position_sigma(cfg, s, body.poses) for s in samples])))
            lows = [body.poses.start + body.offset_to_global - source.end for body in view.bodies.values()]
            highs = [body.poses.end + body.offset_to_global - source.start for body in view.bodies.values()]
            grid = np.arange(min(lows), max(highs) + 1e-9, fusion.observed_alignment_step_s)
            curves: Dict[str, List[Optional[np.ndarray]]] = {}
            for name, outline, footprint, times, sign, offset, near, sigma in comparisons:
                need = max(fusion.observed_alignment_min_samples, 0.5 * len(times))
                row: List[Optional[np.ndarray]] = []
                for delta in grid:
                    distance, valid = outline_distances(outline, footprint, times + sign * delta - offset, near)
                    row.append((distance / sigma)[valid] if valid.sum() >= need else None)
                if any(values is not None and float(np.median(values)) <= 2.0 for values in row):
                    curves[name] = row
            decision: Dict[str, Any] = {"recorder": recorder, "method": OBSERVED, "accepted": False,
                                        "comparisons": len(comparisons), "pooled": sorted(curves)}
            scores = np.full(len(grid), np.inf)
            for k in range(len(grid)):
                pooled = [row[k] for row in curves.values() if row[k] is not None]
                if pooled and sum(len(values) for values in pooled) >= fusion.observed_alignment_min_samples:
                    scores[k] = float(np.median(np.concatenate(pooled)))
            if not np.isfinite(scores).any():
                decision["reason"] = "no observation of a moving target lies on a footprint outline"
                decisions.append(decision)
                pending.remove(recorder)
                continue
            k = int(np.argmin(scores))
            threshold = max(fusion.observed_alignment_uniqueness_ratio * scores[k], 2.0)
            intervals = _components(scores <= threshold)
            home = next(run for run in intervals if run[0] <= k <= run[1])
            others = [float(np.min(scores[a:b + 1])) for a, b in intervals if (a, b) != home]
            decision.update(offset_to_global=round(float(grid[k]), 4), median_distance_sigma=round(float(scores[k]), 3),
                            interval=[round(float(grid[home[0]]), 4), round(float(grid[home[1]]), 4)],
                            other_intervals=len(others),
                            best_elsewhere_sigma=round(min(others), 3) if others else None,
                            candidates=len(grid))
            if scores[k] <= 2.0 and not others:
                decision["accepted"] = True
                alignment.graphs[recorder] = GraphClock(
                    graph=recorder, status="ALIGNED", offset_to_global=round(float(grid[k]), 4), method=OBSERVED,
                    reason="aligned through observed trajectories: the near surfaces of {0} lie on a footprint outline "
                           "(pooled median {1:.2f} sigma) at this offset; offsets within {2:.2f} sigma span "
                           "[{3:+.2f}, {4:+.2f}] s and nothing else fits".format(
                               ", ".join(sorted(curves)), scores[k], threshold, grid[home[0]], grid[home[1]]))
                progress = True
            else:
                decision["reason"] = ("median beyond 2 sigma" if scores[k] > 2.0 else
                                      "not unique: {0} other offset interval(s) fit (best {1:.2f} sigma): the observed "
                                      "target barely moves or moves along its own outline".format(len(others), min(others)))
            decisions.append(decision)
            pending.remove(recorder)
            if progress:
                break  # a newly aligned recorder may observe the remaining ones
    alignment.observed = decisions
    return decisions


# --------------------------------------------------------------------------
# 2. Anonymous tracks that are recorders
# --------------------------------------------------------------------------

@dataclass
class RecorderLink:
    track: str
    recorder: str
    samples: int
    median_distance_m: float
    median_distance_sigma: float
    median_velocity_difference_mps: float
    fraction_within: float
    accepted: bool
    until: Optional[float] = None  # the evidence stops at this contact with a third body (t_global)
    refused: Optional[str] = None


def _third_body_contact(observer: RecorderBody, target: RecorderBody) -> float:
    """The target recorder's first collision report with another body than the observer: from then on the
    observer's radar may see the target and that body as one return cluster (its contact with the
    observer mixes nothing: an observer's own returns are dropped)."""
    return min((t for t, partners in target.contacts if observer.recorder not in partners), default=math.inf)


def link_to_recorders(view: CommonView, cfg: ReconstructionConfig) -> List[RecorderLink]:
    """Per anonymous track, the recorder whose own footprint its returns lie on.

    Evidence: the track's measured samples (the median of its returns: on or inside the target's body)
    up to the candidate recorder's first contact with a third body (``_third_body_contact``).  A point
    inside the recorder's footprint is on it: no other body can be there.  Accepted when, over at least
    ``link_min_samples`` samples, the median distance to the footprint is within 2 sigma
    (``_position_sigma``), the median velocity difference within 2 sigma (``_velocity_sigma``) and at least
    ``link_min_fraction`` of the samples lie within 3 sigma of both -- unless the track's samples after
    that contact lie clearly off the recorder (median beyond 3 sigma over at least ``link_min_samples``):
    the track switched to another body and stays anonymous (identity is per track).  Of several accepted
    recorders, the closest one."""
    fusion = cfg.fusion
    links = []
    for track in view.tracks:
        if track.status == ASSOCIATED:
            continue
        observer = view.bodies[track.recorder]
        candidates = []
        for name, body in view.bodies.items():
            if name == track.recorder:
                continue
            cut = _third_body_contact(observer, body)
            covered = [s for s in track.samples if s.measured and body.covers(s.t_global)]
            samples = [s for s in covered if s.t_global < cut]
            if len(samples) < fusion.link_min_samples:
                continue
            distance, _ = outline_distances(body.poses, body.footprint,
                                            np.array([s.t_global for s in samples]) - body.offset_to_global,
                                            np.array([s.point for s in samples]), inside_zero=True)
            sigma = np.array([_position_sigma(cfg, s, body.poses) for s in samples])
            speed_gap, speed_sigma = [], []
            for s in samples:
                pose = body.pose_at_global(s.t_global)
                speed_gap.append(float(np.hypot(s.velocity[0] - pose.vx, s.velocity[1] - pose.vy)))
                speed_sigma.append(_velocity_sigma(cfg, s.vel_std, body.poses.velocity_std_mps))
            speed_gap, speed_sigma = np.array(speed_gap), np.array(speed_sigma)
            within = float(np.mean((distance <= 3.0 * sigma) & (speed_gap <= 3.0 * speed_sigma)))
            accepted = (float(np.median(distance / sigma)) <= 2.0 and float(np.median(speed_gap / speed_sigma)) <= 2.0
                        and within >= fusion.link_min_fraction)
            link = RecorderLink(track.name, name, len(samples), round(float(np.median(distance)), 3),
                                round(float(np.median(distance / sigma)), 3), round(float(np.median(speed_gap)), 3),
                                round(within, 3), accepted, None if math.isinf(cut) else round(cut, 4))
            after = [s for s in covered if s.t_global >= cut]
            if accepted and len(after) >= fusion.link_min_samples:
                rest, _ = outline_distances(body.poses, body.footprint,
                                            np.array([s.t_global for s in after]) - body.offset_to_global,
                                            np.array([s.point for s in after]), inside_zero=True)
                rest_sigma = np.array([_position_sigma(cfg, s, body.poses) for s in after])
                if float(np.median(rest / rest_sigma)) > 3.0:
                    link.accepted = False
                    link.refused = ("after {2}'s contact with a third body at {0:+.2f} s the track lies {1:.2f} m off "
                                    "{2} (median): it switched to another body".format(cut, float(np.median(rest)), name))
            candidates.append(link)
        accepted = sorted((c for c in candidates if c.accepted), key=lambda c: c.median_distance_sigma)
        links += accepted[:1]
    return links


# --------------------------------------------------------------------------
# 3. Anonymous road users: pairs across observers, stitches within one
# --------------------------------------------------------------------------

@dataclass
class PairEvidence:
    a: str
    b: str
    kind: str  # CROSS, SPLIT (two simultaneous tracks of one observer) or STITCH
    compared: int  # instants compared (1 for a stitch)
    passed: float  # fraction of them passing both tests
    median_box_chi2: Optional[float]
    median_velocity_chi2: Optional[float]
    centre_gap_m: Optional[float]  # median distance between the two single-observer box centres (stitch: miss)
    gap_s: Optional[float] = None  # stitch: time between the two tracks
    accepted: bool = False
    refused: Optional[str] = None  # why an otherwise acceptable link was refused

    @property
    def score(self) -> float:
        box = self.median_box_chi2 if self.median_box_chi2 is not None else math.inf
        return box + (self.median_velocity_chi2 or 0.0)

    def to_dict(self) -> Dict[str, Any]:
        return {"a": self.a, "b": self.b, "kind": self.kind, "compared": self.compared, "passed": self.passed,
                "median_box_chi2": self.median_box_chi2, "median_velocity_chi2": self.median_velocity_chi2,
                "centre_gap_m": self.centre_gap_m, "gap_s": self.gap_s, "accepted": self.accepted,
                "refused": self.refused}


def _heading(samples: Sequence[CommonSample], cfg: ReconstructionConfig) -> Optional[float]:
    """Direction of the inverse-variance weighted velocity, when it is clearly non-zero."""
    floor = cfg.tracking.radial_speed_std_mps
    weights = [1.0 / max(s.vel_std, floor) ** 2 for s in samples]
    v = sum(w * s.velocity for w, s in zip(weights, samples)) / sum(weights)
    speed = float(np.hypot(*v))
    spread = math.sqrt(1.0 / sum(weights))
    return math.atan2(v[1], v[0]) if speed >= max(3.0 * spread, 1.0) else None


def pair_evidence(a: CommonTrack, b: CommonTrack, cfg: ReconstructionConfig) -> Optional[PairEvidence]:
    """Same road user?  At each instant both observers measured a moving target: the box test (chi-square
    of one box fitted to both observers' faces minus those of the two separate fits, 2 dof) and the
    velocity test (difference against both uncertainties, 2 dof), each within the gate of
    ``anonymous_gate_probability``.  Two near surfaces farther apart than a box diagonal plus 6 sigma fail
    without a fit.  Accepted when at least ``anonymous_min_shared_samples`` instants were compared and at
    least ``anonymous_pass_fraction`` of them pass both."""
    fusion, semantics = cfg.fusion, cfg.semantics
    gate = chi2_2dof(fusion.anonymous_gate_probability)
    if min(a.end, b.end) < max(a.start, b.start):
        return None
    diagonal = math.hypot(semantics.target_length_m + fusion.box_length_std_m * 3.0,
                          semantics.target_width_m + fusion.box_width_std_m * 3.0)
    box, velocity, gaps, passed = [], [], [], []
    for sa in a.samples:
        if not sa.measured:
            continue
        sb = b.state_at(sa.t_global)
        if sb is None or not sb.measured:
            continue
        heading = _heading([sa, sb], cfg)
        if heading is None:
            continue
        reach = diagonal + 6.0 * math.hypot(_position_sigma(cfg, sa), _position_sigma(cfg, sb))
        dv = sa.velocity - sb.velocity
        d_vel = float(dv @ dv) / _velocity_sigma(cfg, sa.vel_std, sb.vel_std) ** 2
        if float(np.hypot(*(sa.near - sb.near))) > reach:
            box.append(math.inf)
            velocity.append(d_vel)
            passed.append(False)
            continue
        try:
            fa = fit_box([(a.recorder, sa)], heading, cfg)
            fb = fit_box([(b.recorder, sb)], heading, cfg)
            joint = fit_box([(a.recorder, sa), (b.recorder, sb)], heading, cfg, start=(fa.centre + fb.centre) / 2.0)
        except (ValueError, np.linalg.LinAlgError):
            continue
        d_box = max(joint.chi2 - fa.chi2 - fb.chi2, 0.0)
        box.append(d_box)
        velocity.append(d_vel)
        gaps.append(float(np.hypot(*(fa.centre - fb.centre))))
        passed.append(d_box <= gate and d_vel <= gate)
    if not box:
        return None
    median_box = float(np.median(box))
    evidence = PairEvidence(a.name, b.name, CROSS if a.recorder != b.recorder else SPLIT, len(box),
                            round(float(np.mean(passed)), 3),
                            round(median_box, 3) if math.isfinite(median_box) else None,
                            round(float(np.median(velocity)), 3), round(float(np.median(gaps)), 3) if gaps else None)
    evidence.accepted = (evidence.compared >= fusion.anonymous_min_shared_samples
                         and evidence.passed >= fusion.anonymous_pass_fraction)
    return evidence


def _centre_estimate(observer: str, sample: CommonSample, heading: Optional[float],
                     cfg: ReconstructionConfig) -> Tuple[np.ndarray, np.ndarray]:
    """One observer's centre estimate and covariance: its single-observer box fit, or without a heading the
    near surface pushed back along the line of sight with a car-sized covariance."""
    prior = (cfg.semantics.target_length_m / 2.0, cfg.semantics.target_width_m / 2.0)
    if heading is not None:
        try:
            fit = fit_box([(observer, sample)], heading, cfg)
            return fit.centre, fit.covariance[:2, :2]
        except (ValueError, np.linalg.LinAlgError):
            pass
    return _initial_centre(sample, None, prior), np.eye(2) * (prior[0] ** 2 + sample.pose_var)


def stitch_evidence(a: CommonTrack, b: CommonTrack, cfg: ReconstructionConfig) -> Optional[PairEvidence]:
    """Same road user tracked again by the same observer?  ``b``'s first measured sample comes at most
    ``stitch_max_gap_s`` after ``a``'s last one; ``a``'s centre and velocity there are carried to ``b``'s
    first instant at constant velocity, the uncertainty growing with white acceleration
    (``tracking.acceleration_std_mps2``); accepted when ``b``'s first centre and velocity both lie within
    the 2-dof gate of ``anonymous_gate_probability``."""
    fusion = cfg.fusion
    if a.recorder != b.recorder:
        return None
    last = next((s for s in reversed(a.samples) if s.measured), None)
    first = next((s for s in b.samples if s.measured), None)
    if last is None or first is None:
        return None
    gap = first.t_global - last.t_global
    if b.start <= a.end or gap <= 0.0 or gap > fusion.stitch_max_gap_s + 1e-9:
        return None
    ca, pa = _centre_estimate(a.recorder, last, _heading([last], cfg), cfg)
    cb, pb = _centre_estimate(b.recorder, first, _heading([first], cfg), cfg)
    sigma_a = cfg.tracking.acceleration_std_mps2
    predicted = ca + last.velocity * gap
    covariance = pa + pb + np.eye(2) * ((sigma_a * gap ** 2 / 2.0) ** 2 + (last.vel_std * gap) ** 2)
    miss = cb - predicted
    d_pos = float(miss @ np.linalg.solve(covariance, miss))
    dv = first.velocity - last.velocity
    d_vel = float(dv @ dv) / (_velocity_sigma(cfg, first.vel_std, last.vel_std) ** 2 + (sigma_a * gap) ** 2)
    gate = chi2_2dof(fusion.anonymous_gate_probability)
    ok = d_pos <= gate and d_vel <= gate
    return PairEvidence(a.name, b.name, STITCH, 1, 1.0 if ok else 0.0, round(d_pos, 3), round(d_vel, 3),
                        round(float(np.hypot(*miss)), 3), round(gap, 3), accepted=ok)


def _overlap(a: CommonTrack, b: CommonTrack) -> bool:
    return min(a.end, b.end) - max(a.start, b.start) > 1e-6


def _one_body(evidence: Sequence[PairEvidence]) -> set:
    """Pairs of simultaneous tracks of one observer that an accepted link showed to be one body."""
    return {frozenset((e.a, e.b)) for e in evidence if e.accepted and e.kind == SPLIT}


def refuse_ambiguous(evidence: Sequence[PairEvidence], tracks: Dict[str, CommonTrack]) -> None:
    """Refuse every link that has a rival: a track with two stitched successors (or predecessors), or a
    track compatible with two simultaneous tracks of one other observer that are not one body.
    Conservative: an ambiguity fragments a road user rather than merging two."""
    accepted = [e for e in evidence if e.accepted]
    one_body = _one_body(evidence)
    refusals: Dict[int, str] = {}
    for e in accepted:
        for other in accepted:
            if other is e:
                continue
            if e.kind == STITCH:
                if other.kind != STITCH:
                    continue
                if other.a == e.a:
                    refusals[id(e)] = "{0} has two possible successors ({1}, {2})".format(e.a, e.b, other.b)
                elif other.b == e.b:
                    refusals[id(e)] = "{0} has two possible predecessors ({1}, {2})".format(e.b, e.a, other.a)
                continue
            if other.kind == STITCH:
                continue
            for mine, partner in ((e.a, e.b), (e.b, e.a)):
                if mine not in (other.a, other.b):
                    continue
                rival = other.b if other.a == mine else other.a
                if (rival != partner and tracks[rival].recorder == tracks[partner].recorder
                        and tracks[rival].recorder != tracks[mine].recorder
                        and _overlap(tracks[rival], tracks[partner])
                        and frozenset((rival, partner)) not in one_body):
                    refusals[id(e)] = "{0} is compatible with two simultaneous tracks of {1} ({2}, {3})".format(
                        mine, tracks[partner].recorder, partner, rival)
    for e in accepted:
        if id(e) in refusals:
            e.accepted, e.refused = False, refusals[id(e)]


def cluster(tracks: Sequence[CommonTrack], evidence: Sequence[PairEvidence]) -> Tuple[List[List[CommonTrack]], List[PairEvidence]]:
    """(entities, the links that joined them): accepted links in order of score, never joining two
    groups that would hold two simultaneous tracks of one observer, unless an accepted link showed those
    two to be one body; every track ends in exactly one entity, entities ordered by first appearance."""
    parent = {track.name: track.name for track in tracks}
    one_body = _one_body(evidence)

    def root(name: str) -> str:
        while parent[name] != name:
            parent[name] = parent[parent[name]]
            name = parent[name]
        return name

    def conflict(x: CommonTrack, y: CommonTrack) -> bool:
        return x.recorder == y.recorder and _overlap(x, y) and frozenset((x.name, y.name)) not in one_body

    members = {track.name: [track] for track in tracks}
    used = []
    for item in sorted((e for e in evidence if e.accepted), key=lambda e: (e.score, e.a, e.b)):
        ra, rb = root(item.a), root(item.b)
        if ra == rb:
            continue
        if any(conflict(x, y) for x in members[ra] for y in members[rb]):
            item.refused = "would put two simultaneous tracks of one observer into one road user"
            continue
        parent[rb] = ra
        members[ra] += members.pop(rb)
        used.append(item)
    groups = [sorted(group, key=lambda t: (t.start, t.name)) for name, group in members.items() if root(name) == name]
    return sorted(groups, key=lambda group: (group[0].start, group[0].name)), used


# --------------------------------------------------------------------------
# 4. The fused state of an entity
# --------------------------------------------------------------------------

def entity_trajectory(group: Sequence[CommonTrack], cfg: ReconstructionConfig) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """(fused states at ``entity_output_rate_hz``, footprint) of one entity."""
    fusion, semantics = cfg.fusion, cfg.semantics
    step = 1.0 / fusion.entity_output_rate_hz
    start, end = min(t.start for t in group), max(t.end for t in group)
    states: List[Dict[str, Any]] = []
    lengths, widths, length_bounds, width_bounds = [], [], [], []
    prior_std = (fusion.box_length_std_m / 2.0, fusion.box_width_std_m / 2.0)
    floor = cfg.tracking.radial_speed_std_mps
    heading_held: Optional[float] = None
    for k in range(int(math.ceil(start / step - 1e-6)), int(math.floor(end / step + 1e-6)) + 1):
        t = round(k * step, 4)
        observations = [(track.recorder, sample) for track in group
                        for sample in [track.state_at(t, tolerance=step / 2.0 + 1e-3)] if sample is not None]
        if not observations:
            continue
        velocity, velocity_cov = covariance_intersection(
            [(s.velocity, np.eye(2) * max(s.vel_std, floor) ** 2) for _, s in observations])
        vel_std = math.sqrt(max(float(np.trace(velocity_cov)) / 2.0, 0.0))
        moving = float(np.hypot(*velocity)) >= max(3.0 * vel_std, 1.0)
        heading = math.atan2(velocity[1], velocity[0]) if moving else heading_held
        heading_source = "velocity" if moving else ("held" if heading is not None else None)
        heading_held = heading
        measured = [(o, s) for o, s in observations if s.measured]
        method, centre, covariance, halves = "covariance_intersection", None, None, None
        if heading is not None and measured:
            try:
                fit = fit_box(measured, heading, cfg)
            except (ValueError, np.linalg.LinAlgError):
                fit = None
            if fit is not None and (fit.observers >= 2 or fit.faces >= 2):
                method, centre, covariance, halves = "box_fit", fit.centre, fit.covariance[:2, :2], fit.halves
                if math.sqrt(fit.covariance[2, 2]) < 0.6 * prior_std[0]:
                    lengths.append(2.0 * fit.halves[0])
                if math.sqrt(fit.covariance[3, 3]) < 0.6 * prior_std[1]:
                    widths.append(2.0 * fit.halves[1])
            if fit is not None:
                for m in fit.measurements:
                    if m.count >= 5:
                        (width_bounds if m.half == 0 else length_bounds).append(m.extent)
        if centre is None:
            centre, covariance = covariance_intersection([_centre_estimate(o, s, heading, cfg) for o, s in observations])
        states.append({"t_global": t, "x": round(float(centre[0]), 3), "y": round(float(centre[1]), 3),
                       "pos_std_m": round(math.sqrt(max(float(np.max(np.linalg.eigvalsh(covariance))), 0.0)), 3),
                       "vx": round(float(velocity[0]), 3), "vy": round(float(velocity[1]), 3),
                       "vel_std_mps": round(vel_std, 3),
                       "heading_deg": None if heading is None else round(math.degrees(heading), 2),
                       "heading_source": heading_source,
                       "length_m": None if halves is None else round(2.0 * halves[0], 3),
                       "width_m": None if halves is None else round(2.0 * halves[1], 3),
                       "method": method, "observers": sorted({o for o, _ in observations}),
                       "measured_by": sorted({o for o, s in measured})})

    def dimension(fitted: List[float], bounds: List[float], prior: float, prior_spread: float) -> Dict[str, Any]:
        # The returns' spread along a face is a lower bound of its size, unless it exceeds any body of the
        # prior's class (3 sigma): then the face's returns came from two bodies and say nothing.
        bound = float(np.percentile(bounds, 90)) if len(bounds) >= 3 else None
        usable = bound is not None and bound <= prior + 3.0 * prior_spread
        value, source = (float(np.median(fitted)), "fitted") if fitted else (prior, "prior")
        if usable and bound > value:
            value, source = bound, "observed_extent"
        spread = float(np.std(fitted)) if len(fitted) > 1 and source == "fitted" else prior_spread
        return {"value_m": round(value, 3), "source": source, "std_m": round(spread, 3),
                "fitted_instants": len(fitted), "observed_extent_m": None if bound is None else round(bound, 3),
                "observed_extent_used": bool(usable and bound > value - 1e-9 and source == "observed_extent")}

    length = dimension(lengths, length_bounds, semantics.target_length_m, fusion.box_length_std_m)
    width = dimension(widths, width_bounds, semantics.target_width_m, fusion.box_width_std_m)
    return states, {"length_m": length["value_m"], "width_m": width["value_m"], "length": length, "width": width}


# --------------------------------------------------------------------------
# The whole step
# --------------------------------------------------------------------------

FUSION_PARAMETERS = ("observed_alignment_step_s", "observed_alignment_min_samples", "observed_alignment_min_speed_mps",
                     "observed_alignment_uniqueness_ratio", "link_min_samples",
                     "link_min_fraction", "anonymous_gate_probability", "anonymous_min_shared_samples",
                     "anonymous_pass_fraction", "stitch_max_gap_s", "box_face_std_m", "box_length_std_m",
                     "box_width_std_m", "entity_output_rate_hz")


@dataclass
class RoadUserFusion:
    """What the fusion of road users decided (``global/anonymous_entities.json``)."""

    links: List[RecorderLink]
    evidence: List[PairEvidence]
    entities: List[Dict[str, Any]]
    pose_sources: Dict[str, str]
    names: Dict[Tuple[str, str], str] = field(default_factory=dict)  # (recorder, local track) -> entity id

    def to_dict(self, cfg: ReconstructionConfig, alignment: Alignment) -> Dict[str, Any]:
        return {"definition": "road users in the common frame of the recorders' own pose streams; a road user "
                              "that recorded nothing is an anonymous entity U1, U2, ... and is never named after "
                              "a participant; t_global as in alignment.json; positions in the map frame of the "
                              "pose streams (m), headings in degrees",
                "pose_sources": dict(sorted(self.pose_sources.items())),
                "parameters": dict({key: getattr(cfg.fusion, key) for key in FUSION_PARAMETERS},
                                   measurement_std_m=cfg.tracking.measurement_std_m,
                                   radial_speed_std_mps=cfg.tracking.radial_speed_std_mps,
                                   acceleration_std_mps2=cfg.tracking.acceleration_std_mps2),
                "observed_alignment": list(alignment.observed),
                "recorder_links": [dict(link.__dict__) for link in self.links],
                "association_evidence": [dict(e.to_dict(), score=round(e.score, 3) if math.isfinite(e.score) else None)
                                         for e in self.evidence],
                "entities": self.entities}


def fuse_road_users(locals_: Sequence[Any], alignment: Alignment, associations: List[Association],
                    poses: Dict[str, PoseSource], cfg: ReconstructionConfig) -> RoadUserFusion:
    """Steps 2-4 of the module docstring (step 1 runs before the collision-based association is redone).
    ``associations`` are updated in place: recorder links become ASSOCIATED with the recorder, every other
    anonymous track of an aligned recorder gets its entity's name (U1, U2, ...)."""
    view = build_common_view(locals_, alignment, associations, poses)
    links = link_to_recorders(view, cfg)
    by_key = {(a.local_graph, a.local_track): a for a in associations}
    for link in links:
        recorder, track_id = link.track.split(":", 1)
        item = by_key[(recorder, track_id)]
        item.status, item.global_entity, item.candidate = ASSOCIATED, link.recorder, link.recorder
        item.confidence = link.fraction_within
        item.blocking = []
        item.collision_event = None
        item.evidence = list(item.evidence) + [
            "common frame: its returns lie on {0}'s own footprint (median {1:.2f} m, {2:.2f} sigma, over {3} "
            "samples{6}; {4:.0%} within 3 sigma) at {0}'s own velocity (median difference {5:.2f} m/s)".format(
                link.recorder, link.median_distance_m, link.median_distance_sigma, link.samples,
                link.fraction_within, link.median_velocity_difference_mps,
                "" if link.until is None else " before {0}'s contact with a third body at {1:+.2f} s".format(
                    link.recorder, link.until))]
        item.source_graphs = sorted(set(item.source_graphs) | {recorder, link.recorder})
    linked = {link.track for link in links}
    anonymous = [t for t in view.tracks if t.status != ASSOCIATED and t.name not in linked]
    by_name = {t.name: t for t in anonymous}
    evidence: List[PairEvidence] = []
    for i, a in enumerate(anonymous):
        for b in anonymous[i + 1:]:
            if a.recorder != b.recorder or _overlap(a, b):
                item = pair_evidence(a, b, cfg)  # across observers, or a split track of one observer
            else:
                first, second = (a, b) if (a.start, a.name) <= (b.start, b.name) else (b, a)
                item = stitch_evidence(first, second, cfg)
            if item is not None:
                evidence.append(item)
    refuse_ambiguous(evidence, by_name)
    groups, used = cluster(anonymous, evidence)
    entities, names = [], {}
    for number, group in enumerate(groups, 1):
        entity_id = "U{0}".format(number)
        members = {t.name for t in group}
        states, footprint = entity_trajectory(group, cfg)
        joins = [e for e in used if e.a in members and e.b in members]
        # The weakest link's fraction of compared instants passing (a stitch compares one instant).
        confidence = round(min(e.passed for e in joins), 3) if joins else None
        names.update({(t.recorder, t.track_id): entity_id for t in group})
        entities.append({"id": entity_id, "anonymous": True,
                         "source_tracks": [t.name for t in group],
                         "source_track_segments": [{"track": t.name, "observer": t.recorder,
                                                    "t_global": [round(t.start, 3), round(t.end, 3)]} for t in group],
                         "observers": sorted({t.recorder for t in group}),
                         "time_span": [round(min(t.start for t in group), 3), round(max(t.end for t in group), 3)],
                         "association": {"links": [dict(e.to_dict(), score=round(e.score, 3)) for e in joins],
                                         "confidence": confidence},
                         "fusion_method": "+".join(sorted({s["method"] for s in states})), "footprint": footprint,
                         "trajectory": states})
        for track in group:
            item = by_key[(track.recorder, track.track_id)]
            item.global_entity = entity_id
            item.evidence = list(item.evidence) + [
                "anonymous road user {0}: {1}".format(entity_id, ", ".join(t.name for t in group))]
    return RoadUserFusion(links, evidence, entities, {owner: source.name for owner, source in poses.items()}, names)
