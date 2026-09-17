"""Joint radar identity/time hypotheses and a robust global clock graph.

Only local positions, radar-derived tracks and local triggers enter estimation.
Sampling cadence, frame equality, seeds and simulator times are not evidence.
The common clock is a recorder clock, with unobservable absolute time/scale.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np
from scipy.optimize import least_squares, linear_sum_assignment
from ..common.config import Config
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.schemas import TriggerKind
from ..common.timeline import build_common_grid


def aligned_spans(run, offsets):
    out = {}
    for pid, span in sorted(run.spans().items()):
        m = offsets.get(pid, {})
        if m.get("status") == "UNRESOLVED_TIME_ALIGNMENT" or m.get("offset_s") is None:
            continue
        a, b = float(m.get("scale", 1)), float(m["offset_s"])
        out[pid] = (a * span[0] + b, a * span[1] + b)
    return out


def _interpolate(samples, query, fields, max_gap):
    ts = np.array([s.t for s in samples], dtype=float)
    vals = np.array([[getattr(s, k) for k in fields] for s in samples], dtype=float)
    if len(ts) < 2:
        return np.zeros((len(query), len(fields))), np.zeros(len(query), dtype=bool)
    idx = np.searchsorted(ts, query).clip(1, len(ts) - 1)
    valid = (query >= ts[0]) & (query <= ts[-1]) & ((ts[idx] - ts[idx - 1]) <= max_gap)
    data = np.column_stack(
        [np.interp(query, ts, vals[:, i]) for i in range(len(fields))]
    )
    return data, valid


def estimate_track_clock(
    observer: ParticipantEvidence,
    track_id: str,
    candidate: ParticipantEvidence,
    cfg: Config,
) -> Optional[Dict[str, Any]]:
    """Fit t_observer = scale*t_candidate + offset for one identity hypothesis.

    Range is the track centroid's body-origin range. Range-rate retains the
    measured sign (negative closing) and sensor-origin line of sight. Robust
    loss tolerates surface/centre discrepancies and reports their residuals.
    """
    get = lambda k, default: cfg.get("fusion.time_alignment." + k, default)
    samples = observer.tracks_by_id().get(track_id, [])
    min_n = int(get("min_samples", 12))
    if len(samples) < min_n or len(candidate.telemetry) < min_n:
        return None
    samples = samples[:: max(1, len(samples) // 160)]
    ts = np.array([s.t for s in samples])
    span = float(ts[-1] - ts[0])
    if span < float(get("min_overlap_s", 1)):
        return None
    gap = float(get("max_interpolation_gap_s", 0.3))
    own, own_valid = _interpolate(
        observer.telemetry, ts, ("x", "y", "vx", "vy", "yaw"), gap
    )
    target = np.array([[s.gx, s.gy] for s in samples])
    velocity = np.array([[s.gvx, s.gvy] for s in samples])
    ranges = np.array([s.range_m for s in samples])
    rates = np.array([s.range_rate for s in samples])
    sigmas = [
        float(get(k, d))
        for k, d in [
            ("position_sigma_m", 2),
            ("range_sigma_m", 2),
            ("range_rate_sigma_mps", 1.5),
            ("velocity_sigma_mps", 3),
        ]
    ]
    if any(s <= 0 for s in sigmas):
        raise ValueError("residual scales must be positive")
    weights = np.sqrt(np.array([max(0.05, min(1.0, s.confidence)) for s in samples]))
    mount = observer.radar[0] if observer.radar else None
    sensor_xy = own[:, :2].copy()
    if mount is not None:
        yaw = np.deg2rad(own[:, 4])
        sensor_xy[:, 0] += mount.sensor_x * np.cos(yaw) - mount.sensor_y * np.sin(yaw)
        sensor_xy[:, 1] += mount.sensor_x * np.sin(yaw) + mount.sensor_y * np.cos(yaw)
    anchors = []

    def channels(b, ppm):
        a = 1 + ppm * 1e-6
        other, valid = _interpolate(
            candidate.telemetry, (ts - b) / a, ("x", "y", "vx", "vy"), gap
        )
        valid &= own_valid & np.all(np.isfinite(target), axis=1)
        delta = other[:, :2] - own[:, :2]
        distance = np.linalg.norm(delta, axis=1)
        los = other[:, :2] - sensor_xy
        los /= np.maximum(np.linalg.norm(los, axis=1)[:, None], 1e-6)
        predicted_rate = np.sum((other[:, 2:4] - own[:, 2:4]) * los, axis=1)
        pos = target - other[:, :2]
        rng = ranges - distance
        rate = rates - predicted_rate
        vel = velocity - other[:, 2:4]
        vnorm = np.linalg.norm(velocity, axis=1) * np.linalg.norm(other[:, 2:4], axis=1)
        heading = np.zeros(len(ts))
        moving = vnorm > 0.25
        heading[moving] = 1 - np.clip(
            np.sum(velocity[moving] * other[moving, 2:4], axis=1) / vnorm[moving], -1, 1
        )
        return valid, pos, rng, rate, vel, heading

    def residual(params):
        b, ppm = float(params[0]), float(params[1]) if len(params) > 1 else 0.0
        valid, pos, rng, rate, vel, heading = channels(b, ppm)
        r = np.column_stack(
            [
                pos / sigmas[0],
                rng / sigmas[1],
                rate / sigmas[2],
                0.5 * vel / sigmas[3],
                0.25 * heading,
            ]
        )
        r *= weights[:, None]
        r[~valid, :] = 4.0
        result = r.ravel()
        if anchors:
            sigma = float(get("collision_anchor_sigma_s", 0.03))
            result = np.r_[
                result,
                [(o - (1 + ppm * 1e-6) * c - b) / sigma for o, c in anchors],
            ]
        return result

    def robust_loss(z):
        # Balance the impact constraint against a trajectory channel *outside*
        # soft-L1. Scaling its residual by sqrt(N) before robustification would
        # incorrectly classify a valid anchor as an outlier as tracks get longer.
        weight = np.ones_like(z)
        if anchors:
            weight[-len(anchors) :] = len(ts)
        root = np.sqrt(1 + z)
        return np.array(
            [2 * weight * (root - 1), weight / root, -0.5 * weight / root**3]
        )

    def objective(b):
        r = residual([b])
        return float(np.mean(robust_loss(r * r)[0]))

    limit = float(get("max_offset_s", 1))
    step = float(get("coarse_offset_step_s", 0.05))
    if limit <= 0 or step <= 0:
        raise ValueError("clock search window and step must be positive")
    coarse = np.linspace(-limit, limit, max(3, int(math.ceil(2 * limit / step)) + 1))
    best = min(coarse, key=lambda b: (objective(b), abs(b)))
    fit = least_squares(
        residual,
        [best],
        bounds=([-limit], [limit]),
        loss=robust_loss,
        ftol=1e-9,
        xtol=1e-9,
        gtol=1e-9,
    )
    b = float(fit.x[0])
    valid, pos, rng, rate, vel, heading = channels(b, 0)
    if np.count_nonzero(valid) < min_n or np.mean(valid) < float(
        get("min_overlap_fraction", 0.6)
    ):
        return None
    rmse = float(np.sqrt(np.mean(np.sum(pos[valid] ** 2, axis=1))))
    if rmse > float(cfg.get("fusion.track_association.max_rmse_m", 6)):
        return None
    if max(math.hypot(s.vx, s.vy) for s in candidate.telemetry) < 0.5:
        return None

    # Supplementary impacts only after a physically viable radar hypothesis.
    # No local collision record identifies the other vehicle.
    obs_hits = [t for t in observer.triggers if t.kind == TriggerKind.COLLISION]
    cand_hits = [t for t in candidate.triggers if t.kind == TriggerKind.COLLISION]
    for hit in obs_hits:
        near = min(samples, key=lambda s: abs(s.t - hit.t))
        if abs(near.t - hit.t) > 0.5 or near.range_m > 8:
            continue
        ranked = sorted(cand_hits, key=lambda t: abs(hit.t - t.t - b))
        if not ranked or abs(hit.t - ranked[0].t - b) > float(
            get("collision_anchor_tolerance_s", 0.3)
        ):
            continue
        if (
            len(ranked) > 1
            and abs(hit.t - ranked[1].t - b) - abs(hit.t - ranked[0].t - b) < 0.1
        ):
            continue
        cpos, cvalid = _interpolate(
            candidate.telemetry, np.array([hit.t - b]), ("x", "y"), gap
        )
        opos, ovalid = _interpolate(
            observer.telemetry, np.array([hit.t]), ("x", "y"), gap
        )
        if cvalid[0] and ovalid[0] and np.linalg.norm(cpos[0] - opos[0]) <= 8:
            anchors.append((float(hit.t), float(ranked[0].t)))
    if anchors:
        # The objective has changed. Restart its coarse search rather than
        # reusing a radar-only minimum at a discontinuous overlap boundary.
        best = min(coarse, key=lambda value: (objective(value), abs(value)))
        fit = least_squares(
            residual,
            [best],
            bounds=([-limit], [limit]),
            loss=robust_loss,
            ftol=1e-9,
            xtol=1e-9,
            gtol=1e-9,
        )
        b = float(fit.x[0])

    ppm = 0.0
    drift_status = "OFFSET_ONLY_UNOBSERVABLE_DRIFT"
    uncertainty = None
    drift_limit = float(get("max_drift_ppm", 2000))
    if span >= float(get("min_drift_span_s", 15)) and drift_limit > 0:
        affine = least_squares(
            residual,
            [b, 0],
            bounds=([-limit, -drift_limit], [limit, drift_limit]),
            x_scale=[1.0, max(1.0, drift_limit)],
            loss=robust_loss,
            ftol=1e-10,
            xtol=1e-10,
            gtol=1e-10,
        )
        jac = affine.jac
        if np.linalg.matrix_rank(jac) == 2:
            variance = max(
                1e-12, float(np.sum(affine.fun**2) / max(1, len(affine.fun) - 2))
            )
            uncertainty = float(
                math.sqrt(max(0.0, np.linalg.inv(jac.T @ jac)[1, 1] * variance))
            )
        gain = float((fit.cost - affine.cost) / max(1, len(affine.fun)))
        if (
            uncertainty is not None
            and uncertainty <= float(get("max_drift_uncertainty_ppm", 250))
            and abs(affine.x[1]) > 2 * uncertainty
            and gain > float(get("min_drift_loss_improvement", 0.01))
            and abs(affine.x[1]) < 0.99 * drift_limit
        ):
            b, ppm = map(float, affine.x)
            fit = affine
            drift_status = "AFFINE_DRIFT_ESTIMATED"
    valid, pos, rng, rate, vel, heading = channels(b, ppm)
    n = int(np.count_nonzero(valid))
    if n < min_n or np.mean(valid) < float(get("min_overlap_fraction", 0.6)):
        return None
    if float(np.linalg.norm(fit.jac[:, 0])) < 0.1:
        return None
    final_residual = residual([b, ppm])
    normalization = len(ts) * (7 + len(anchors))
    residual_value = float(np.sum(robust_loss(final_residual**2)[0]) / normalization)
    confidence = float(1 / (1 + residual_value) * np.mean(valid))
    return {
        "observer": observer.participant_id,
        "candidate": candidate.participant_id,
        "track_id": track_id,
        "offset_s": b,
        "scale": 1 + ppm * 1e-6,
        "drift_ppm": ppm,
        "drift_status": drift_status,
        "drift_uncertainty_ppm": uncertainty,
        "position_residual_m": float(np.sqrt(np.mean(np.sum(pos[valid] ** 2, axis=1)))),
        "range_residual_m": float(np.sqrt(np.mean(rng[valid] ** 2))),
        "range_rate_residual_mps": float(np.sqrt(np.mean(rate[valid] ** 2))),
        "velocity_residual_mps": float(
            np.sqrt(np.mean(np.sum(vel[valid] ** 2, axis=1)))
        ),
        "heading_consistency": float(1 - np.mean(heading[valid]) / 2),
        "residual": residual_value,
        "confidence": confidence,
        "n_samples": n,
        "overlap_s": span * float(np.mean(valid)),
        "candidate_time_span": [
            float((ts[valid][0] - b) / (1 + ppm * 1e-6)),
            float((ts[valid][-1] - b) / (1 + ppm * 1e-6)),
        ],
        "collision_anchors": len(anchors),
        "methods": [
            "radar_position",
            "radar_range",
            "radar_range_rate",
            "target_velocity",
            "heading",
        ]
        + (["local_collision_supplement"] if anchors else []),
    }


def _initial_constraints(run, cfg):
    hypotheses = []
    constraints = []
    for observer in run.participant_ids:
        ev = run.get(observer)
        tracks = ev.track_ids()
        others = [p for p in run.participant_ids if p != observer]
        if not tracks or not others:
            continue
        matrix = np.full((len(tracks), len(others)), 1e6)
        lookup = {}
        for i, track in enumerate(tracks):
            for j, pid in enumerate(others):
                h = estimate_track_clock(ev, track, run.get(pid), cfg)
                if h is None:
                    continue
                h["status"] = "CANDIDATE"
                hypotheses.append(h)
                matrix[i, j] = 1 - h["confidence"]
                lookup[i, j] = h
        rows, cols = linear_sum_assignment(matrix)
        for i, j in zip(rows, cols):
            h = lookup.get((i, j))
            if h is None:
                continue
            rivals = [v for (r, c), v in lookup.items() if r == i and c != j]
            margin = h["confidence"] - max(
                [r["confidence"] for r in rivals], default=0.0
            )
            if h["confidence"] < float(
                cfg.get("fusion.time_alignment.min_confidence", 0.4)
            ):
                h["status"] = "INSUFFICIENT_CONFIDENCE"
            elif rivals and margin < float(
                cfg.get("fusion.time_alignment.ambiguity_margin", 0.12)
            ):
                h["status"] = "AMBIGUOUS_IDENTITY_TIME"
            else:
                h["status"] = "ACCEPTED_CLOCK_CONSTRAINT"
                constraints.append(h)
    return hypotheses, constraints


def _solve_global(constraints, reference):
    connected = {reference}
    changed = True
    while changed:
        changed = False
        for h in constraints:
            if h["observer"] in connected or h["candidate"] in connected:
                before = len(connected)
                connected.update([h["observer"], h["candidate"]])
                changed |= len(connected) > before
    others = sorted(connected - {reference})
    index = {p: i for i, p in enumerate(others)}
    edges = [h for h in constraints if h["observer"] in connected]

    def scale(x, p):
        return 1.0 if p == reference else math.exp(x[index[p]])

    def offset(x, p):
        return 0.0 if p == reference else x[index[p] + len(others)]

    def residual(x):
        values = []
        for h in edges:
            o, c = h["observer"], h["candidate"]
            w = math.sqrt(h["confidence"] / (0.1 + h["residual"]))
            values.extend(
                [
                    w
                    * 1e4
                    * (
                        math.log(scale(x, c))
                        - math.log(scale(x, o))
                        - math.log(h["scale"])
                    ),
                    w * (offset(x, c) - offset(x, o) - scale(x, o) * h["offset_s"]),
                ]
            )
        return values

    x = np.zeros(2 * len(others))
    if others:
        x = least_squares(residual, x, loss="soft_l1", f_scale=0.1, max_nfev=200).x
    return {p: (scale(x, p), offset(x, p)) for p in connected}, edges


def align_participants(run: RunEvidence, cfg: Config) -> Dict[str, Any]:
    ids = run.participant_ids
    grid_dt = float(cfg.get("fusion.time_alignment.grid_dt", 0.05))
    hypotheses, constraints = _initial_constraints(run, cfg)
    degree = {
        p: sum(
            h["confidence"] for h in constraints if p in (h["observer"], h["candidate"])
        )
        for p in ids
    }
    reference = min(ids, key=lambda p: (-degree[p], p)) if ids else None
    solutions, edges = (
        _solve_global(constraints, reference) if reference is not None else ({}, [])
    )
    diagnostics = []
    bad = []
    for h in edges:
        ao, bo = solutions[h["observer"]]
        ac, bc = solutions[h["candidate"]]
        err = max(
            abs(ac * t + bc - (ao * (h["scale"] * t + h["offset_s"]) + bo))
            for t in h["candidate_time_span"]
        )
        h["global_constraint_residual_s"] = float(err)
        if err > float(
            cfg.get("fusion.time_alignment.max_clock_constraint_residual_s", 0.2)
        ):
            bad.append(h)
    if bad:
        for h in bad:
            h["status"] = "INCONSISTENT_CLOCK_CONSTRAINT"
        constraints = [h for h in constraints if h not in bad]
        solutions, edges = _solve_global(constraints, reference)
        diagnostics.append(
            {"kind": "inconsistent_clock_constraints", "n_rejected": len(bad)}
        )
    offsets = {}
    for pid in ids:
        support = [h for h in edges if pid in (h["observer"], h["candidate"])]
        resolved = pid in solutions and bool(run.get(pid).telemetry)
        a, b = solutions.get(pid, (None, None)) if resolved else (None, None)
        confidence = (
            1.0
            if pid == reference and resolved
            else min([h["confidence"] for h in edges], default=0.0)
        )
        offsets[pid] = {
            "offset_s": b,
            "scale": a,
            "drift_ppm": None if a is None else (a - 1) * 1e6,
            "reference": reference,
            "is_reference": pid == reference,
            "confidence": confidence,
            "n_constraints": len(support),
            "n_samples": sum(h["n_samples"] for h in support),
            "residual": (
                float(np.mean([h["residual"] for h in support])) if support else None
            ),
            "method": "reference" if pid == reference else "evidence_clock_graph",
            "methods": sorted({m for h in support for m in h["methods"]}),
            "status": "ALIGNED" if resolved else "UNRESOLVED_TIME_ALIGNMENT",
            "drift_status": (
                "REFERENCE_GAUGE"
                if pid == reference
                else (
                    "AFFINE_DRIFT_ESTIMATED"
                    if a is not None and abs(a - 1.0) > 1e-9
                    else "OFFSET_ONLY_UNOBSERVABLE_DRIFT"
                )
            ),
        }
        if not resolved:
            diagnostics.append(
                {
                    "kind": "UNRESOLVED_TIME_ALIGNMENT",
                    "participant_id": pid,
                    "message": "no unambiguous physical evidence path to reference; raw time is not comparable",
                }
            )
    corrected = aligned_spans(run, offsets)
    grid = (
        build_common_grid(list(corrected.values()), grid_dt)
        if len(corrected) > 1
        else None
    )
    return {
        "reference": reference,
        "offsets": offsets,
        "common_span": None if grid is None else [grid.t0, grid.t1],
        "grid_dt": grid_dt,
        "diagnostics": diagnostics,
        "hypotheses": hypotheses,
        "constraints": edges,
        "reference_rule": "maximum accepted evidence-weighted degree; lexical tie break",
        "formula": "t_common = scale * t_local + offset_s",
    }
