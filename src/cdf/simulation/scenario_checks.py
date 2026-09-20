"""Physical checks on what a recorded scenario actually did.

SCENARIO GENERATION AND EVALUATION ONLY. Everything here reads the privileged
oracle trace, and nothing in the forensic pipeline may import it.

The existing validation asks whether the declared collision happened. That turns
out to be far too weak a question. A run in which both vehicles drove in circles
for twenty seconds, left the road and demolished a fence still "passed", because
somewhere in all of that the declared pair had touched. What a person watching
would have said is that the scenario was nonsense.

So these are the questions a person watching asks:

* did they hit *where* the scenario meant, or thirty metres past it?
* did the car that was supposed to change lane actually move sideways?
* did anybody drive in a circle, or wander off and hit the scenery?
* in a chain, how long between the two impacts, and was the pushed car under
  power or coasting?

Each check is opt-in from the scenario's ``validation:`` block, because the right
answer differs per scenario and a check nobody declared should not invent a
requirement. What they share is that failing one makes the run *fail*, rather
than being recorded as a curiosity nobody reads.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

__all__ = ["run_physical_checks"]


def _angle_diff(a: float, b: float) -> float:
    return (a - b + 180.0) % 360.0 - 180.0


def _path(states: Sequence[Any]) -> Dict[str, Any]:
    """Shape facts about one vehicle's path."""
    if len(states) < 2:
        return {}
    xs = [s.x for s in states]
    ys = [s.y for s in states]
    yaws = [s.yaw for s in states]

    travelled = sum(
        math.hypot(xs[i + 1] - xs[i], ys[i + 1] - ys[i]) for i in range(len(xs) - 1)
    )
    net = math.hypot(xs[-1] - xs[0], ys[-1] - ys[0])
    turned = sum(abs(_angle_diff(yaws[i + 1], yaws[i])) for i in range(len(yaws) - 1))

    # Displacement across the direction it set out in. This is the number that
    # says whether a declared lane change happened, and it is measured from the
    # trajectory rather than from the command, so a lane shift the controller
    # never received reads as zero.
    heading = math.radians(yaws[0])
    nx, ny = -math.sin(heading), math.cos(heading)
    lateral = [(xs[i] - xs[0]) * nx + (ys[i] - ys[0]) * ny for i in range(len(xs))]

    return {
        "travelled_m": round(travelled, 2),
        "net_displacement_m": round(net, 2),
        # 1.0 is a straight line. A vehicle that loops back on itself collapses
        # toward 0, which is what "driving in circles" looks like as a number.
        "straightness": round(net / travelled, 3) if travelled > 1e-6 else 0.0,
        "accumulated_turn_deg": round(turned, 1),
        "net_turn_deg": round(_angle_diff(yaws[-1], yaws[0]), 1),
        "max_abs_lateral_m": round(max(abs(v) for v in lateral), 2),
        "signed_peak_lateral_m": round(max(lateral, key=abs), 2),
    }


#: Below this, a *repeat* contact between a pair that has already touched is two
#: cars leaning on each other rather than a second collision. The chain merge
#: below collapses a contact that is continuously reported, but two vehicles at
#: rest against each other also stop and restart reporting seconds later, and
#: each restart would otherwise read as a fresh impact.
#:
#: It is deliberately not applied to a pair's first contact. A pair that has
#: never touched and now touches has collided, however lightly, and hiding that
#: from the physical checks while ``collision_pairs`` still reported it left one
#: validation file contradicting itself. Whether a light contact is the
#: collision a variant *declared* is a different question, asked of the whole
#: campaign in tests/integration/test_final_campaign_physics.py.
RESTING_CONTACT_IMPULSE = 500.0

#: Contacts arriving closer together than this are the same impact still
#: being reported. CARLA re-reports a standing contact at exactly 0.5 s
#: intervals, so the window has to be wider than that to catch them.
CONTACT_CHAIN_WINDOW_S = 0.75


def _pair_impacts(collisions: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Distinct participant-to-participant impacts, in time order."""
    rows = []
    for c in collisions:
        if not c.get("is_participant_pair"):
            continue
        pair = tuple(sorted([str(c["participant_id"]), str(c["other_participant_id"])]))
        rows.append({"t": float(c["t"]), "pair": pair,
                     "impulse": float(c.get("impulse") or 0.0)})
    # Vehicles that stay in contact are reported again every half second for as
    # long as it lasts. That is one impact, however long it lasts, so the merge
    # follows the chain: each further contact is absorbed if it arrives within
    # the window of the *previous* one, not of the first. Comparing against the
    # first is what let an indefinite run of contacts reappear as a second
    # impact a few seconds later, which is then whatever an interval check is
    # reading. A genuine second collision between the same pair, after they had
    # come apart, still registers: it is more than a window away from the last
    # contact of the first one.
    merged: List[Dict[str, Any]] = []
    last_seen: Dict[Tuple[str, str], Tuple[int, float]] = {}
    for row in sorted(rows, key=lambda r: (r["t"], r["pair"])):
        prev = last_seen.get(row["pair"])
        if prev is not None and row["t"] - prev[1] < CONTACT_CHAIN_WINDOW_S:
            merged[prev[0]]["impulse"] = max(merged[prev[0]]["impulse"], row["impulse"])
            last_seen[row["pair"]] = (prev[0], row["t"])
            continue
        if prev is not None and row["impulse"] < RESTING_CONTACT_IMPULSE:
            # This pair has touched before and is touching again, gently: they
            # are resting against each other, not colliding a second time.
            last_seen[row["pair"]] = (prev[0], row["t"])
            continue
        last_seen[row["pair"]] = (len(merged), row["t"])
        merged.append(row)
    return merged


def _scenery_impacts(collisions: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for c in collisions:
        if c.get("is_participant_pair"):
            continue
        out.append({"t": round(float(c["t"]), 3),
                    "participant": str(c.get("participant_id")),
                    "what": str(c.get("other_type_id") or "unknown"),
                    "impulse": round(float(c.get("impulse") or 0.0), 1)})
    return out


def _state_at(states: Sequence[Any], t: float) -> Optional[Any]:
    return min(states, key=lambda s: abs(getattr(s, "t", 0.0) - t)) if states else None


def run_physical_checks(
    spec: Any,
    oracle: Any,
    validation: Dict[str, Any],
) -> Tuple[List[str], Dict[str, Any]]:
    """Return ``(problems, checks)`` for the physical-sanity block.

    ``validation`` is the scenario's own ``validation:`` mapping. Only the keys
    it declares are enforced.
    """
    problems: List[str] = []
    checks: Dict[str, Any] = {}

    series = {pid: oracle.state_series(pid) for pid in spec.participant_ids}
    # The oracle's states carry no timestamp of their own, so pair them with the
    # frame times to answer "what were the controls just after the impact".
    times: Dict[str, List[Tuple[float, Any]]] = {}
    for frame in oracle.frames:
        for actor in frame.actors:
            if actor.participant_id:
                times.setdefault(actor.participant_id, []).append((float(frame.t), actor))

    paths = {pid: _path(states) for pid, states in series.items() if states}
    checks["paths"] = paths

    impacts = _pair_impacts(oracle.collisions)
    checks["impacts"] = [
        {"t": round(i["t"], 3), "pair": list(i["pair"]), "impulse": round(i["impulse"], 1)}
        for i in impacts
    ]

    # -- the collision happened where the scenario meant ---------------------
    near = validation.get("collision_near")
    if near and impacts:
        jx, jy = float(near["x"]), float(near["y"])
        max_d = float(near.get("max_distance_m", 15.0))
        which = int(near.get("impact_index", 0))
        require_junction = bool(near.get("require_in_junction", False))
        if which < len(impacts):
            hit = impacts[which]
            positions = []
            for pid in hit["pair"]:
                rows = times.get(pid) or []
                if not rows:
                    continue
                _t, actor = min(rows, key=lambda r: abs(r[0] - hit["t"]))
                d = math.hypot(actor.x - jx, actor.y - jy)
                positions.append({"participant": pid, "x": round(actor.x, 2),
                                  "y": round(actor.y, 2), "distance_m": round(d, 2),
                                  "in_junction": bool(actor.is_junction)})
            checks["collision_near"] = {"target": [jx, jy], "max_distance_m": max_d,
                                        "at": positions}
            worst = max((p["distance_m"] for p in positions), default=None)
            if worst is not None and worst > max_d:
                problems.append(
                    "impact {0} between {1} happened {2:.1f} m from the intended "
                    "conflict point ({3:.1f}, {4:.1f}), limit {5:.1f} m: the "
                    "vehicles met somewhere other than where the scenario means"
                    .format(which + 1, "-".join(hit["pair"]), worst, jx, jy, max_d)
                )
            if require_junction and positions and not any(p["in_junction"] for p in positions):
                problems.append(
                    "impact {0} between {1} happened outside the junction; this "
                    "scenario is about a conflict inside it"
                    .format(which + 1, "-".join(hit["pair"]))
                )
        else:
            problems.append(
                "validation asks about impact {0} but only {1} occurred"
                .format(which + 1, len(impacts))
            )

    # -- the interval between two impacts -----------------------------------
    interval = validation.get("impact_interval_s")
    if interval:
        if len(impacts) < 2:
            problems.append(
                "an interval between two impacts was declared but {0} occurred"
                .format(len(impacts))
            )
        else:
            gap = impacts[1]["t"] - impacts[0]["t"]
            checks["impact_interval_s"] = round(gap, 3)
            lo = interval.get("min")
            hi = interval.get("max")
            if lo is not None and gap < float(lo):
                problems.append(
                    "the two impacts were {0:.2f} s apart, less than the {1:.2f} s "
                    "this variant requires".format(gap, float(lo))
                )
            if hi is not None and gap > float(hi):
                problems.append(
                    "the two impacts were {0:.2f} s apart, more than the {1:.2f} s "
                    "this variant allows: the second no longer reads as following "
                    "from the first".format(gap, float(hi))
                )

    # -- a declared lane change really moved the vehicle sideways -----------
    for pid, wanted in (validation.get("min_lateral_displacement_m") or {}).items():
        got = (paths.get(pid) or {}).get("max_abs_lateral_m")
        if got is None:
            problems.append("no trajectory recorded for {0}".format(pid))
        elif got < float(wanted):
            problems.append(
                "{0} moved {1:.2f} m sideways; this variant needs at least "
                "{2:.2f} m, so the lane change it declares is not visibly "
                "happening".format(pid, got, float(wanted))
            )

    # -- nobody drove in a circle -------------------------------------------
    turn_cap = validation.get("max_accumulated_turn_deg")
    if turn_cap is not None:
        for pid, facts in sorted(paths.items()):
            if facts.get("accumulated_turn_deg", 0.0) > float(turn_cap):
                problems.append(
                    "{0} turned through {1:.0f} deg in total, more than the "
                    "{2:.0f} deg this scenario allows: it is circling or "
                    "recovering its route rather than driving the encounter"
                    .format(pid, facts["accumulated_turn_deg"], float(turn_cap))
                )
    straight_floor = validation.get("min_straightness")
    if straight_floor is not None:
        for pid, facts in sorted(paths.items()):
            if facts.get("straightness", 1.0) < float(straight_floor):
                problems.append(
                    "{0}'s path doubles back on itself (straightness {1:.2f} "
                    "against a floor of {2:.2f})"
                    .format(pid, facts["straightness"], float(straight_floor))
                )

    # -- nothing hit the scenery --------------------------------------------
    scenery = _scenery_impacts(oracle.collisions)
    checks["scenery_impacts"] = scenery
    if validation.get("no_scenery_collision") and scenery:
        first = scenery[0]
        problems.append(
            "{0} collided with {1} at t={2:.2f}s: an unintended collision with "
            "the world, not part of the encounter"
            .format(first["participant"], first["what"], first["t"])
        )

    # -- the vehicle stopped where the sign told it to ----------------------
    # "It stopped" is not the claim a stop-sign scenario makes. The claim is
    # that it stopped *before the line*, and a vehicle that brakes to rest in
    # the middle of the junction has satisfied the first and broken the second.
    for pid, want in (validation.get("stop_point") or {}).items():
        # A variant can switch one off by setting it null, which is how
        # b_fails_to_stop says that B is not supposed to stop.
        if not want:
            continue
        rows = times.get(pid) or []
        if not rows:
            problems.append("no states recorded for {0}".format(pid))
            continue
        moving = float(want.get("moving_above_ms", 0.5))
        at_rest = next(
            ((t, a) for t, a in rows
             if a.speed < moving and t > float(want.get("after_s", 1.0))),
            None,
        )
        if at_rest is None:
            problems.append(
                "{0} never came to rest: this variant requires it to stop at "
                "its stop line".format(pid)
            )
            continue
        t_stop, actor = at_rest
        d = math.hypot(actor.x - float(want["x"]), actor.y - float(want["y"]))
        checks.setdefault("stop_point", {})[pid] = {
            "t": round(t_stop, 3), "x": round(actor.x, 2), "y": round(actor.y, 2),
            "distance_m": round(d, 2), "in_junction": bool(actor.is_junction),
        }
        if d > float(want.get("max_distance_m", 8.0)):
            problems.append(
                "{0} came to rest {1:.1f} m from its stop line at ({2:.1f}, "
                "{3:.1f}), limit {4:.1f} m: it stopped somewhere other than the "
                "line, which for a stop-sign scenario is the whole question"
                .format(pid, d, float(want["x"]), float(want["y"]),
                        float(want.get("max_distance_m", 8.0)))
            )
        if want.get("must_be_outside_junction", True) and actor.is_junction:
            problems.append(
                "{0} came to rest inside the junction at ({1:.1f}, {2:.1f}): a "
                "stop sign is obeyed before the junction, not in it"
                .format(pid, actor.x, actor.y)
            )

    # -- a pushed vehicle is not driving itself ------------------------------
    coasting = validation.get("coasting_after_impact") or []
    if coasting and impacts:
        t0 = impacts[0]["t"]
        window = float(validation.get("coasting_window_s", 1.5))
        limit = float(validation.get("coasting_throttle_max", 0.05))
        for pid in coasting:
            # Strictly after: the frame the impact is stamped on still carries
            # the control the vehicle was applying when it was hit, which in a
            # scenario where the struck vehicle was cruising is a throttle
            # reading that says nothing about what it did afterwards.
            rows = [a for t, a in (times.get(pid) or []) if t0 < t <= t0 + window]
            if not rows:
                problems.append("no states recorded for {0} after the first impact".format(pid))
                continue
            peak = max(a.throttle for a in rows)
            checks.setdefault("coasting", {})[pid] = round(peak, 3)
            if peak > limit:
                problems.append(
                    "{0} applied up to {1:.2f} throttle in the {2:.1f} s after "
                    "being struck; a pushed vehicle must coast, not accelerate "
                    "under its own power".format(pid, peak, window)
                )

    # -- a displacement that the impact, and nothing else, produced ---------
    # A floor on total sideways movement says a vehicle left its lane. It does
    # not say why, and in a scenario whose whole claim is "because it was hit"
    # that is the part worth checking. So the displacement is measured on both
    # sides of the first impact: near zero before it, and real after it. A
    # scripted lane change at a fixed time would fail this whichever side of
    # the impact the clock happened to put it on.
    begins = validation.get("lateral_begins_at_impact") or {}
    if begins:
        if not impacts:
            problems.append("an impact-triggered displacement was declared but none occurred")
        else:
            t0 = impacts[0]["t"]
            for pid, want in sorted(begins.items()):
                rows = times.get(pid) or []
                if len(rows) < 2:
                    problems.append("no trajectory recorded for {0}".format(pid))
                    continue
                x0, y0 = rows[0][1].x, rows[0][1].y
                heading = math.radians(rows[0][1].yaw)
                nx, ny = -math.sin(heading), math.cos(heading)
                before = [abs((a.x - x0) * nx + (a.y - y0) * ny) for t, a in rows if t < t0]
                after = [abs((a.x - x0) * nx + (a.y - y0) * ny) for t, a in rows if t >= t0]
                pre = max(before) if before else 0.0
                post = max(after) if after else 0.0
                checks.setdefault("lateral_at_impact", {})[pid] = {
                    "before_m": round(pre, 2), "after_m": round(post, 2)}
                cap = float(want.get("before_max_m", 0.3))
                floor = float(want.get("after_min_m", 1.0))
                if pre > cap:
                    problems.append(
                        "{0} had already moved {1:.2f} m sideways before the first "
                        "impact, more than the {2:.2f} m this variant allows: the "
                        "displacement is not the impact's doing"
                        .format(pid, pre, cap))
                if post < floor:
                    problems.append(
                        "{0} moved {1:.2f} m sideways after the first impact; this "
                        "variant needs at least {2:.2f} m, so the vehicle was not "
                        "visibly carried anywhere".format(pid, post, floor))

    # -- a vehicle that reached the second impact under its own power -------
    # The mirror of the check above, and the one that separates a consequence
    # from a coincidence. In a variant whose story is "the driver did this
    # later, of its own accord", the throttle between the two impacts is the
    # evidence: if it is zero the second impact was still the first one paying
    # out, whatever the interval says.
    driven = validation.get("self_driven_between_impacts") or {}
    if driven:
        if len(impacts) < 2:
            problems.append(
                "a self-driven second impact was declared but {0} occurred"
                .format(len(impacts))
            )
        else:
            t0, t1 = impacts[0]["t"], impacts[1]["t"]
            for pid, floor in sorted(driven.items()):
                rows = [a for t, a in (times.get(pid) or []) if t0 < t < t1]
                if not rows:
                    problems.append(
                        "no states recorded for {0} between the two impacts".format(pid)
                    )
                    continue
                peak = max(a.throttle for a in rows)
                checks.setdefault("self_driven", {})[pid] = round(peak, 3)
                if peak < float(floor):
                    problems.append(
                        "{0} never applied more than {1:.2f} throttle between the "
                        "two impacts; this variant claims the second one was {0}'s "
                        "own doing, and a coasting vehicle has not done anything"
                        .format(pid, peak)
                    )

    # -- a pair the variant says must stay apart ----------------------------
    for pair in validation.get("forbidden_collision_pairs") or []:
        key = tuple(sorted(str(p) for p in pair))
        hit = [i for i in impacts if i["pair"] == key]
        if hit:
            problems.append(
                "{0} and {1} collided at t={2:.2f}s; this variant is the one "
                "where that does not happen".format(key[0], key[1], hit[0]["t"])
            )

    return problems, checks
