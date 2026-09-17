"""Privileged events measured from the ground-truth trace.

PRIVILEGED LAYER -- EVALUATION ONLY.

:mod:`cdf.oracle.logger` records what actually happened; this module turns that
recording into the typed :class:`~cdf.common.schemas.Event` vocabulary so that the
ground truth and a participant's reconstruction can be compared node by node.

Why this is not the local extractor with better inputs
-----------------------------------------------------
Scoring a reconstruction against a reference that was produced by the same code
would measure nothing but numerical noise. Nothing here is therefore shared with
:mod:`cdf.local.event_extractor`, and the differences are deliberate rather than
incidental:

* **Exact relative kinematics.** Range, range-rate and TTC are computed from both
  participants' true poses and velocities (:func:`pair_kinematics`). The local
  layer can only estimate them from its own radar returns, and only for objects
  it happens to be tracking; the oracle sees every pair at every tick, including
  the pairs nobody was looking at.
* **No hysteresis.** The local extractor debounces every threshold with a Schmitt
  trigger because its signals are noisy. The oracle's signals are exact, so a
  plain minimum-duration gate is both sufficient and more faithful: the reported
  interval is the interval during which the condition genuinely held.
* **Declared intent.** Scripted-action events come from the action schedule the
  controller actually executed, not from any signal at all. No amount of onboard
  evidence can recover "this was a commanded 8 s emergency brake".
* **Privileged predicates.** Signal violations and right-of-way conflicts rest on
  map and traffic-light state, which the local layer is structurally unable to
  express.

Confidence
----------
An oracle event carries ``confidence = 1.0`` only where its time is genuinely
deterministic: a scripted action fires at a commanded instant, and a collision is
recorded by the simulator's own contact channel. Everything measured by crossing
a threshold on a continuous signal inherits a configurable, lower confidence --
the *state* is certain, but the instant assigned to it depends on where the
threshold was drawn, and pretending otherwise would overstate the reference.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from ..common.config import Config
from ..common.geometry import (
    angle_diff_deg,
    closest_approach,
    distance,
    polyline_intersection,
    time_to_collision_1d,
)
from ..common.io import read_json, read_jsonl_gz
from ..common.layout import RunLayout
from ..common.schemas import (
    Event,
    EventType,
    Evidence,
    Provenance,
    make_event_id,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "EVIDENCE_KIND",
    "STATE_EVENT_TYPES",
    "ORACLE_STATE_EVENT_TYPES",
    "OUTCOME_EVENT_TYPES_BY_NAME",
    "OracleState",
    "load_oracle_trace",
    "participant_series",
    "participant_path",
    "pair_kinematics",
    "longitudinal_acceleration",
    "nearest_state",
    "pre_impact_state",
    "pre_impact_row",
    "build_oracle_events",
]


#: ``Evidence.kind`` stamped on every back-pointer emitted by this module. It is
#: what marks a piece of evidence as unreproducible from onboard data.
EVIDENCE_KIND = "oracle"

#: Scenario ``causal_template`` ``kind: "state"`` names, mapped onto the shared
#: event taxonomy. The names are the template's vocabulary; the types are what
#: the rest of the pipeline (matching, metrics, the viewer) already understands,
#: so an oracle state node is directly comparable with the local node that should
#: have detected it.
STATE_EVENT_TYPES: Dict[str, EventType] = {
    "closing": EventType.RANGE_DECREASING,
    "critical_ttc": EventType.CRITICAL_TTC,
    "conflict_entry": EventType.CONFLICT_REGION_ENTRY,
    "decelerating": EventType.HARD_DECELERATION,
}

#: ``kind: "oracle_state"`` names. These have no local counterpart at all: they
#: are the facts the distributed reconstruction provably cannot reach; they are
#: retained on the privileged side for evaluation only.
ORACLE_STATE_EVENT_TYPES: Dict[str, EventType] = {
    "signal_violation": EventType.ORACLE_SIGNAL_VIOLATION,
    "right_of_way": EventType.ORACLE_RIGHT_OF_WAY_CONFLICT,
}

#: ``kind: "outcome"`` names. ``no_collision`` is realised by the pair's
#: :class:`~cdf.common.schemas.EventType.NEAR_MISS` event: the evidence that the
#: designed encounter genuinely happened *and* stayed short of contact. When the
#: two never came close enough for the encounter to be real there is nothing for
#: a designed ``PREVENTS`` edge to attach to, and the graph builder says so
#: instead of inventing a node for a non-event.
OUTCOME_EVENT_TYPES_BY_NAME: Dict[str, EventType] = {
    "collision": EventType.COLLISION,
    "near_miss": EventType.NEAR_MISS,
    "no_collision": EventType.NEAR_MISS,
    "post_impact_stop": EventType.POST_IMPACT_STOP,
}

#: Traffic-light state string (as CARLA stringifies it) that a vehicle may not
#: enter a junction on.
_RED = "red"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def load_oracle_trace(run_dir: Union[str, Path]) -> Dict[str, Any]:
    """Read the privileged trace and summary of a run.

    Parameters
    ----------
    run_dir:
        A ``seed_xxx`` run directory. Both files are resolved through
        :class:`~cdf.common.layout.RunLayout`.

    Returns
    -------
    dict
        ``{"frames": [...], "summary": {...}, "participants": [...],
        "collisions": [...], "collision_pairs": [...], "run_dir": str}``.
        ``frames`` are sorted by time so that every consumer sees the same order
        regardless of how the writer interleaved them.

    Raises
    ------
    FileNotFoundError
        When either privileged artifact is missing. A silent empty trace would
        turn every downstream comparison into a vacuous pass, so this fails loudly.
    """
    layout = RunLayout.from_run_dir(run_dir)
    summary_path = layout.oracle_dir / "oracle_summary.json"
    for path, what in ((layout.oracle_trace, "trace"), (summary_path, "summary")):
        if not path.exists():
            raise FileNotFoundError(
                "oracle {0} not found at {1}; the run was produced without the "
                "privileged logger and cannot be scored".format(what, path)
            )

    frames = read_jsonl_gz(layout.oracle_trace)
    frames.sort(key=lambda f: (float(f.get("t", 0.0)), int(f.get("frame", 0))))
    summary = read_json(summary_path)
    if not isinstance(summary, dict):
        raise ValueError("oracle summary at {0} is not a mapping".format(summary_path))

    participants = [str(p) for p in summary.get("participants", []) or []]
    if not participants:
        seen: List[str] = []
        for frame in frames:
            for actor in frame.get("actors", []) or []:
                pid = str(actor.get("participant_id", ""))
                if pid and pid not in seen:
                    seen.append(pid)
        participants = sorted(seen)

    return {
        "frames": frames,
        "summary": summary,
        "participants": participants,
        "collisions": list(summary.get("collisions", []) or []),
        "collision_pairs": list(summary.get("collision_pairs", []) or []),
        "run_dir": str(layout.root),
    }


# ---------------------------------------------------------------------------
# Exact per-participant and per-pair kinematics
# ---------------------------------------------------------------------------


@dataclass
class OracleState:
    """Exact relative kinematics of one ordered participant pair at one instant.

    Every field is computed from both parties' true poses and velocities, so this
    is the quantity a radar track is *trying* to estimate. Comparing the two is
    how radar-derived indicators are scored.
    """

    t: float
    a: str
    """Reference participant; the relative quantities are expressed from here."""
    b: str
    """The other participant."""
    distance: float
    """True centre-to-centre planar separation in metres."""
    range_rate: float
    """Rate of change of :attr:`distance`, m/s; **negative means closing**, the
    same sign convention the radar uses."""
    ttc: Optional[float]
    """Range-rate time-to-collision in seconds, ``None`` when not closing."""
    closing_speed: float
    """Magnitude of the closing component, ``max(0, -range_rate)``."""
    t_cpa: Optional[float]
    """Seconds until the constant-velocity closest point of approach, ``None``
    when the relative motion is not converging."""
    d_cpa: float
    """Separation at that closest point of approach, metres."""


def participant_series(trace: Dict[str, Any], participant_id: str) -> List[Dict[str, Any]]:
    """Every recorded privileged state of one participant, in time order.

    Each element is the raw actor row of a frame with the frame's ``t`` and
    ``frame`` folded in, so callers never have to carry the frame alongside.
    """
    out: List[Dict[str, Any]] = []
    for frame in trace.get("frames", []) or []:
        for actor in frame.get("actors", []) or []:
            if str(actor.get("participant_id")) == str(participant_id):
                row = dict(actor)
                row["t"] = float(frame.get("t", 0.0))
                row["frame"] = int(frame.get("frame", 0))
                out.append(row)
                break
    return out


def participant_path(trace: Dict[str, Any], participant_id: str) -> List[Tuple[float, float]]:
    """The participant's true planar trajectory as a polyline."""
    return [(float(r["x"]), float(r["y"])) for r in participant_series(trace, participant_id)]


def pair_kinematics(trace: Dict[str, Any], a: str, b: str) -> List[OracleState]:
    """Exact relative kinematics between two participants, sample by sample.

    Only frames in which *both* participants were recorded contribute, so a
    participant that spawned late or was destroyed early simply shortens the
    series instead of producing invented samples.

    Raises
    ------
    ValueError
        When ``a`` and ``b`` are the same participant: a pair-relative quantity
        between a vehicle and itself is meaningless and always indicates a caller
        bug rather than a degenerate scenario.
    """
    if str(a) == str(b):
        raise ValueError(
            "pair_kinematics needs two distinct participants, got {0!r} twice".format(a)
        )

    rows_a = {r["frame"]: r for r in participant_series(trace, a)}
    rows_b = {r["frame"]: r for r in participant_series(trace, b)}

    out: List[OracleState] = []
    for frame in sorted(set(rows_a.keys()) & set(rows_b.keys())):
        ra = rows_a[frame]
        rb = rows_b[frame]
        dx = float(rb["x"]) - float(ra["x"])
        dy = float(rb["y"]) - float(ra["y"])
        dist = math.hypot(dx, dy)
        rvx = float(rb["vx"]) - float(ra["vx"])
        rvy = float(rb["vy"]) - float(ra["vy"])
        # d(distance)/dt is the relative velocity projected on the line of sight.
        range_rate = 0.0 if dist <= 1e-9 else (dx * rvx + dy * rvy) / dist
        t_cpa, d_cpa = closest_approach(dx, dy, rvx, rvy)
        out.append(
            OracleState(
                t=float(ra["t"]),
                a=str(a),
                b=str(b),
                distance=dist,
                range_rate=range_rate,
                ttc=time_to_collision_1d(dist, range_rate),
                closing_speed=max(0.0, -range_rate),
                t_cpa=t_cpa,
                d_cpa=d_cpa,
            )
        )
    return out


def longitudinal_acceleration(rows: Sequence[Dict[str, Any]]) -> List[float]:
    """True body-frame longitudinal acceleration, m/s^2, one value per row.

    Differentiated from the exact velocity series (central differences, one-sided
    at the ends) rather than read from the simulator's per-frame acceleration
    field. Both are "ground truth", but the logged field is a sampled physics
    quantity that spikes on contact and on suspension events, while the
    derivative of the velocity projected onto the heading is exactly the
    kinematic definition of longitudinal acceleration and is reproducible from
    the persisted trace alone.
    """
    n = len(rows)
    if n == 0:
        return []

    along: List[float] = []
    for row in rows:
        yaw = math.radians(float(row["yaw"]))
        along.append(float(row["vx"]) * math.cos(yaw) + float(row["vy"]) * math.sin(yaw))

    out: List[float] = []
    for i in range(n):
        lo = max(0, i - 1)
        hi = min(n - 1, i + 1)
        dt = float(rows[hi]["t"]) - float(rows[lo]["t"])
        out.append(0.0 if dt <= 1e-9 else (along[hi] - along[lo]) / dt)
    return out


# ---------------------------------------------------------------------------
# Episode detection
# ---------------------------------------------------------------------------


@dataclass
class _Episode:
    """One contiguous stretch during which an exact condition held."""

    t_start: float
    t_end: float
    t_peak: float
    peak_value: float


def _find_episodes(
    times: Sequence[float],
    values: Sequence[Optional[float]],
    threshold: float,
    mode: str,
    min_duration_s: float,
) -> List[_Episode]:
    """Contiguous runs of ``values`` on the far side of ``threshold``.

    ``mode`` is ``"below"`` or ``"above"``. ``None`` means the quantity is
    undefined at that sample (an undefined TTC, say) and closes an open run
    rather than silently bridging it.

    There is no hysteresis here on purpose -- see the module docstring. The only
    filter is ``min_duration_s``, which discards a condition that held for less
    than one meaningful interval; ``t_peak`` is placed at the most extreme sample
    of the run, which is the instant the state was at its worst.
    """
    if mode not in ("above", "below"):
        raise ValueError("episode mode must be 'above' or 'below', got {0!r}".format(mode))
    if len(times) != len(values):
        raise ValueError(
            "signal length {0} does not match time base {1}".format(len(values), len(times))
        )
    if min_duration_s < 0.0:
        raise ValueError("min_duration_s must not be negative, got {0!r}".format(min_duration_s))

    above = mode == "above"
    out: List[_Episode] = []
    start_i: Optional[int] = None
    peak_i = -1
    peak_v = 0.0

    def close(end_i: int) -> None:
        if start_i is None:
            return
        t0 = float(times[start_i])
        t1 = float(times[end_i])
        if (t1 - t0) >= min_duration_s - 1e-9:
            out.append(
                _Episode(t_start=t0, t_end=t1, t_peak=float(times[peak_i]), peak_value=peak_v)
            )

    for i, raw in enumerate(values):
        v = None if raw is None else float(raw)
        holds = v is not None and ((v >= threshold) if above else (v <= threshold))
        if holds:
            if start_i is None:
                start_i = i
                peak_i = i
                peak_v = float(v)
            elif (v > peak_v) if above else (v < peak_v):
                peak_i = i
                peak_v = float(v)
        elif start_i is not None:
            close(i - 1)
            start_i = None
    if start_i is not None:
        close(len(values) - 1)
    return out


# ---------------------------------------------------------------------------
# Event assembly helpers
# ---------------------------------------------------------------------------


def _oracle_event(
    participant_id: str,
    event_type: EventType,
    t_start: float,
    t_peak: float,
    t_end: Optional[float],
    subject: Optional[str],
    id_subject: str,
    values: Dict[str, Any],
    confidence: float,
    owners: Sequence[str],
    evidence: Sequence[Evidence],
) -> Event:
    """Assemble one oracle event with a deterministic, collision-free id.

    ``id_subject`` is fed to :func:`~cdf.common.schemas.make_event_id` instead of
    ``subject``. The two differ because ``subject`` carries the *template's*
    vocabulary (``"closing"``), which is not unique inside a run: with three
    participants, ``A`` can be closing on ``B`` and on ``C`` in the very same
    frame. The id therefore hashes the counterpart as well. Nothing parses an
    event id -- it is an opaque handle -- so this costs nothing and removes a
    silent collision that would drop a real ground-truth node.
    """
    return Event(
        event_id=make_event_id("oracle", participant_id, event_type.value, t_peak, id_subject),
        event_type=event_type,
        participant_id=str(participant_id),
        t_start=float(t_start),
        t_peak=float(t_peak),
        t_end=None if t_end is None else float(t_end),
        subject=subject,
        values=dict(values),
        confidence=float(max(0.0, min(1.0, confidence))),
        evidence=list(evidence),
        provenance=Provenance.ORACLE,
        source_sensors=[EVIDENCE_KIND],
        owners=[str(o) for o in owners],
    )


def _pairs(participants: Sequence[str]) -> List[Tuple[str, str]]:
    """Unordered participant pairs, in a deterministic order."""
    ordered = sorted(str(p) for p in participants)
    return [
        (ordered[i], ordered[j])
        for i in range(len(ordered))
        for j in range(i + 1, len(ordered))
    ]


def _trace_span(trace: Dict[str, Any]) -> Tuple[float, float]:
    """``(t_first, t_last)`` of the privileged trace."""
    frames = trace.get("frames", []) or []
    if not frames:
        raise ValueError("oracle trace has no frames; nothing can be measured from it")
    return (float(frames[0].get("t", 0.0)), float(frames[-1].get("t", 0.0)))


def _confidence(cfg: Config, key: str, default: float) -> float:
    """Read one oracle confidence and validate it.

    Confidences are configuration, not constants: how much an oracle timestamp
    should be trusted depends on how the threshold that produced it was drawn.
    """
    value = float(cfg.get("oracle.confidence.{0}".format(key), default))
    if not 0.0 < value <= 1.0:
        raise ValueError(
            "oracle.confidence.{0} must lie in (0, 1], got {1!r}".format(key, value)
        )
    return value


# ---------------------------------------------------------------------------
# Event families
# ---------------------------------------------------------------------------


def _action_events(trace: Dict[str, Any], cfg: Config) -> List[Event]:
    """One event per scripted action that actually fired.

    The schedule is read from the trace rather than from the scenario spec on
    purpose: a counterfactual replay mutates the controller's actions before the
    run, and the trace records what the controller executed. Taking the times
    from the spec would describe the *baseline* scenario while the trace
    describes the run, and every counterfactual comparison would be off by the
    intervention under study.
    """
    _t_first, t_last = _trace_span(trace)
    interventions = trace.get("summary", {}).get("interventions", {}) or {}

    out: List[Event] = []
    for pid in sorted(interventions.keys()):
        block = interventions[pid] or {}
        for action in block.get("actions", []) or []:
            action_id = str(action.get("action_id", ""))
            if not action_id:
                raise ValueError(
                    "controller description for participant {0!r} contains an action "
                    "without an action_id: {1!r}".format(pid, action)
                )
            if not bool(action.get("enabled", True)):
                LOGGER.info(
                    "oracle: scripted action %s of %s is disabled and emits no event",
                    action_id,
                    pid,
                )
                continue
            t_start = float(action.get("t_start", 0.0))
            if t_start > t_last + 1e-9:
                # The run ended before the action was due: it never fired, and an
                # event for it would be a ground truth that never happened.
                LOGGER.info(
                    "oracle: scripted action %s of %s was scheduled at t=%.2fs but the "
                    "run ended at t=%.2fs; no event emitted",
                    action_id,
                    pid,
                    t_start,
                    t_last,
                )
                continue
            duration = float(action.get("duration", 0.0))
            params = {str(k): float(v) for k, v in (action.get("params", {}) or {}).items()}
            t_end = min(t_start + max(0.0, duration), t_last)

            kind = str(action.get("kind", "")).strip().lower()
            values: Dict[str, Any] = {"duration_s": duration}
            values.update(params)
            # The action's declared kind, as numeric flags. graph._mechanical_edges
            # reads kind_is_brake and previously found it never populated, falling
            # back to a substring test on the action id; cdf.graph.canonical reads
            # it to place a scripted action in the same family as the command the
            # vehicle itself recorded.
            values["kind_is_brake"] = 1.0 if kind == "brake" else 0.0
            values["kind_is_speed"] = 1.0 if kind in ("set_speed", "hold_speed") else 0.0
            values["kind_is_lateral"] = 1.0 if kind in ("lane_shift", "steer") else 0.0
            out.append(
                _oracle_event(
                    participant_id=str(pid),
                    event_type=EventType.ORACLE_SCRIPTED_INTERVENTION,
                    t_start=t_start,
                    t_peak=t_start,
                    t_end=t_end,
                    subject=action_id,
                    id_subject="action@{0}".format(action_id),
                    values=values,
                    # Deterministic: the controller was commanded at this instant.
                    confidence=1.0,
                    owners=[str(pid)],
                    evidence=[
                        Evidence(
                            kind=EVIDENCE_KIND,
                            ref=action_id,
                            t_start=t_start,
                            t_end=t_end,
                            detail={
                                "source": "scripted_action",
                                "action_kind": str(action.get("kind", "")),
                                "params": params,
                                "participant": str(pid),
                            },
                        )
                    ],
                )
            )
    return out


def _state_event(
    name: str,
    participant_id: str,
    counterpart: Optional[str],
    episode: _Episode,
    values: Dict[str, Any],
    confidence: float,
) -> Event:
    """One measured-state event named in the ``causal_template`` vocabulary."""
    event_type = STATE_EVENT_TYPES[name]
    payload: Dict[str, Any] = {"oracle_state": name}
    payload.update(values)
    owners = [participant_id] if counterpart is None else [participant_id, counterpart]
    detail: Dict[str, Any] = {"source": "exact_kinematics", "state": name}
    if counterpart is not None:
        detail["counterpart"] = counterpart
        detail["pair"] = sorted([participant_id, counterpart])
    return _oracle_event(
        participant_id=participant_id,
        event_type=event_type,
        t_start=episode.t_start,
        t_peak=episode.t_peak,
        t_end=episode.t_end,
        subject=name,
        id_subject="{0}@{1}".format(name, counterpart or "self"),
        values=payload,
        confidence=confidence,
        owners=owners,
        evidence=[
            Evidence(
                kind=EVIDENCE_KIND,
                ref="{0}:{1}".format(name, participant_id),
                t_start=episode.t_start,
                t_end=episode.t_end,
                detail=detail,
            )
        ],
    )


def _closing_and_ttc_events(
    states: Sequence[OracleState], cfg: Config
) -> List[Event]:
    """``closing`` and ``critical_ttc`` for one ordered pair.

    Both quantities are properties of the *pair* -- the gap shrinks for the
    follower and for the leader alike -- so they are emitted from each
    participant's point of view. Which one a scenario's template names is then a
    question the template answers, not one this function has to guess.
    """
    if not states:
        return []
    a = states[0].a
    b = states[0].b
    times = [s.t for s in states]

    min_rate = float(cfg.get("events.radar.range_decreasing.min_rate_mps", 1.0))
    closing_min_duration = float(
        cfg.get("events.radar.range_decreasing.min_duration_s", 0.6)
    )
    critical_ttc_s = float(cfg.get("events.radar.critical_ttc.ttc_s", 1.6))
    min_duration_s = float(cfg.get("events.min_duration_s", 0.10))
    if min_rate <= 0.0:
        raise ValueError(
            "events.radar.range_decreasing.min_rate_mps must be positive, got "
            "{0!r}".format(min_rate)
        )
    if critical_ttc_s <= 0.0:
        raise ValueError(
            "events.radar.critical_ttc.ttc_s must be positive, got {0!r}".format(critical_ttc_s)
        )

    closing_conf = _confidence(cfg, "state", 0.9)
    out: List[Event] = []

    for episode in _find_episodes(
        times, [s.range_rate for s in states], -min_rate, "below", closing_min_duration
    ):
        window = [s for s in states if episode.t_start - 1e-9 <= s.t <= episode.t_end + 1e-9]
        values = {
            "range_rate_mps": episode.peak_value,
            "min_distance_m": min(s.distance for s in window),
            "threshold_mps": -min_rate,
        }
        out.append(_state_event("closing", a, b, episode, values, closing_conf))
        out.append(_state_event("closing", b, a, episode, values, closing_conf))

    ttc_values: List[Optional[float]] = [s.ttc for s in states]
    for episode in _find_episodes(
        times, ttc_values, critical_ttc_s, "below", min_duration_s
    ):
        window = [s for s in states if episode.t_start - 1e-9 <= s.t <= episode.t_end + 1e-9]
        values = {
            "ttc_s": episode.peak_value,
            "min_distance_m": min(s.distance for s in window),
            "threshold_s": critical_ttc_s,
        }
        out.append(_state_event("critical_ttc", a, b, episode, values, closing_conf))
        out.append(_state_event("critical_ttc", b, a, episode, values, closing_conf))

    return out


def _conflict_entry_events(
    trace: Dict[str, Any], a: str, b: str, cfg: Config
) -> List[Event]:
    """``conflict_entry`` for a pair whose true paths genuinely cross.

    A conflict region is a piece of road two vehicles both needed. Two kinds of
    evidence say that happened:

    * the driven paths **intersect**; or
    * the pair **collided**, in which case the contact point is a path crossing
      in the limit. This case has to be handled separately rather than left to
      the geometry: an impact stops both vehicles at the contact point, so the
      driven polylines end there and never actually cross. Without it every
      crossing scenario that succeeds in producing its crash would report no
      conflict region at all -- the detector would fire only when the scenario
      failed.

    A candidate then has to survive two filters, and dropping either produces
    nonsense:

    1. **A real crossing angle.** A follower drives *along* its leader's path and
       clips it repeatedly through nothing but lateral jitter. The angle is taken
       from the two vehicles' recorded headings, not from the direction of the
       intersecting polyline segments: those segments span centimetres of lateral
       wobble, so their direction is noise and same-lane following produces
       apparent 180-degree "crossings". A longitudinal conflict is what
       ``closing`` and ``critical_ttc`` already describe.
    2. **A real arrival gap.** Both parties must reach the crossing within
       ``indicators.conflict.max_arrival_gap_s`` of each other; two vehicles that
       use the same junction a minute apart never conflicted.

    When several candidates qualify, the one with the smallest arrival gap is the
    conflict; the others are recorded in the event's values by count only.
    """
    radius = float(cfg.get("indicators.conflict.region_radius_m", 6.0))
    max_gap = float(cfg.get("indicators.conflict.max_arrival_gap_s", 2.5))
    min_angle = float(cfg.get("oracle.conflict.min_crossing_angle_deg", 20.0))
    if radius <= 0.0:
        raise ValueError(
            "indicators.conflict.region_radius_m must be positive, got {0!r}".format(radius)
        )
    if not 0.0 <= min_angle < 180.0:
        raise ValueError(
            "oracle.conflict.min_crossing_angle_deg must lie in [0, 180), got "
            "{0!r}".format(min_angle)
        )

    rows_a = participant_series(trace, a)
    rows_b = participant_series(trace, b)
    if len(rows_a) < 2 or len(rows_b) < 2:
        return []
    path_a = [(float(r["x"]), float(r["y"])) for r in rows_a]
    path_b = [(float(r["x"]), float(r["y"])) for r in rows_b]

    candidates: List[Tuple[float, float, float, float, str]] = []
    for (cx, cy, i, j) in polyline_intersection(path_a, path_b):
        candidates.append(
            (cx, cy, float(rows_a[i]["yaw"]), float(rows_b[j]["yaw"]), "path_crossing")
        )
    impact = _collision_pairs(trace).get(tuple(sorted([a, b])))
    if impact is not None:
        contact_a = pre_impact_row(rows_a, impact[0])
        contact_b = pre_impact_row(rows_b, impact[0])
        if contact_a is not None and contact_b is not None:
            candidates.append(
                (
                    0.5 * (float(contact_a["x"]) + float(contact_b["x"])),
                    0.5 * (float(contact_a["y"]) + float(contact_b["y"])),
                    float(contact_a["yaw"]),
                    float(contact_b["yaw"]),
                    "impact_point",
                )
            )

    best: Optional[Dict[str, Any]] = None
    n_qualifying = 0
    for (cx, cy, yaw_a, yaw_b, origin) in candidates:
        crossing_angle = abs(angle_diff_deg(yaw_a, yaw_b))
        if crossing_angle < min_angle:
            continue
        window_a = _region_window(rows_a, cx, cy, radius)
        window_b = _region_window(rows_b, cx, cy, radius)
        if window_a is None or window_b is None:
            continue
        gap = abs(window_a[2] - window_b[2])
        if gap > max_gap:
            continue
        n_qualifying += 1
        if best is None or gap < float(best["gap"]):
            best = {
                "gap": gap,
                "x": cx,
                "y": cy,
                "angle": crossing_angle,
                "origin": origin,
                "window_a": window_a,
                "window_b": window_b,
            }

    if best is None:
        return []

    gap = float(best["gap"])
    cx = float(best["x"])
    cy = float(best["y"])
    crossing_angle = float(best["angle"])
    origin = str(best["origin"])
    confidence = _confidence(cfg, "state", 0.9)
    out: List[Event] = []
    for pid, counterpart, window in (
        (a, b, best["window_a"]),
        (b, a, best["window_b"]),
    ):
        t_start, t_end, t_peak, min_d = window
        episode = _Episode(t_start=t_start, t_end=t_end, t_peak=t_peak, peak_value=min_d)
        values = {
            "crossing_x": cx,
            "crossing_y": cy,
            "crossing_angle_deg": crossing_angle,
            "arrival_gap_s": gap,
            "min_distance_to_crossing_m": min_d,
            "region_radius_m": radius,
            "n_qualifying_crossings": float(n_qualifying),
            "crossing_evidence": origin,
        }
        out.append(_state_event("conflict_entry", pid, counterpart, episode, values, confidence))
    return out


def _region_window(
    rows: Sequence[Dict[str, Any]], cx: float, cy: float, radius: float
) -> Optional[Tuple[float, float, float, float]]:
    """First contiguous visit of ``rows`` to the disc of ``radius`` around a point.

    Returns ``(t_entry, t_exit, t_closest, min_distance)`` or ``None`` when the
    participant never entered the region.
    """
    t_entry: Optional[float] = None
    t_exit = 0.0
    t_closest = 0.0
    best = float("inf")
    for row in rows:
        d = distance(float(row["x"]), float(row["y"]), cx, cy)
        inside = d <= radius
        if inside:
            if t_entry is None:
                t_entry = float(row["t"])
            t_exit = float(row["t"])
            if d < best:
                best = d
                t_closest = float(row["t"])
        elif t_entry is not None:
            break
    if t_entry is None:
        return None
    return (t_entry, t_exit, t_closest, best)


def _deceleration_events(trace: Dict[str, Any], participants: Sequence[str], cfg: Config) -> List[Event]:
    """``decelerating`` for each participant, from its exact longitudinal acceleration."""
    enter = float(cfg.get("events.hard_deceleration.enter_mps2", -4.5))
    if enter >= 0.0:
        raise ValueError(
            "events.hard_deceleration.enter_mps2 must be negative, got {0!r}".format(enter)
        )
    min_duration_s = float(cfg.get("events.min_duration_s", 0.10))
    confidence = _confidence(cfg, "state", 0.9)

    out: List[Event] = []
    for pid in sorted(str(p) for p in participants):
        rows = participant_series(trace, pid)
        if len(rows) < 2:
            continue
        times = [float(r["t"]) for r in rows]
        accel = longitudinal_acceleration(rows)
        for episode in _find_episodes(times, accel, enter, "below", min_duration_s):
            window = [
                r for r in rows if episode.t_start - 1e-9 <= float(r["t"]) <= episode.t_end + 1e-9
            ]
            values = {
                "accel_long_mps2": episode.peak_value,
                "speed_at_onset_mps": float(window[0]["speed"]) if window else 0.0,
                "speed_at_end_mps": float(window[-1]["speed"]) if window else 0.0,
                "duration_s": float(episode.t_end - episode.t_start),
                "threshold_mps2": enter,
            }
            out.append(_state_event("decelerating", pid, None, episode, values, confidence))
    return out


def _signal_violation_events(
    trace: Dict[str, Any], participants: Sequence[str], cfg: Config
) -> List[Event]:
    """``signal_violation``: inside a junction on a red governing light.

    Structurally unreachable from onboard evidence -- neither the junction
    geometry nor the signal phase appears anywhere in a participant's own
    recording -- which is exactly what makes it a privileged reference event.

    The predicate carries the governing light forward. CARLA reports a vehicle's
    traffic light only while the vehicle is *approaching* the stop line; the
    moment it crosses into the junction the reference goes away and
    ``traffic_light_state`` reads ``None``. Testing "inside the junction AND the
    light reads red" literally against the recorded field can therefore never be
    true, and the detector would silently report zero violations for ever. The
    violation is instead the real-world one: the last signal that governed this
    approach was red when the vehicle entered the junction. The carried state is
    cleared on leaving a junction, so a light cannot be blamed for the next one.
    """
    min_duration_s = float(cfg.get("oracle.signal_violation.min_duration_s", 0.0))
    confidence = _confidence(cfg, "oracle_state", 0.95)

    out: List[Event] = []
    for pid in sorted(str(p) for p in participants):
        rows = participant_series(trace, pid)
        times = [float(r["t"]) for r in rows]
        flags: List[Optional[float]] = []
        governing: Optional[str] = None
        was_in_junction = False
        for row in rows:
            in_junction = bool(row.get("is_junction", False))
            state = row.get("traffic_light_state")
            if state is not None:
                governing = str(state).strip()
            elif was_in_junction and not in_junction:
                # Left the junction with no new light in sight: whatever governed
                # the approach we just completed no longer governs anything.
                governing = None
            red = governing is not None and governing.lower().endswith(_RED)
            flags.append(1.0 if (in_junction and red) else 0.0)
            was_in_junction = in_junction
        for episode in _find_episodes(times, flags, 1.0, "above", min_duration_s):
            window = [r for r in rows if episode.t_start - 1e-9 <= float(r["t"]) <= episode.t_end + 1e-9]
            junction_ids = sorted(
                {int(r["junction_id"]) for r in window if r.get("junction_id") is not None}
            )
            values = {
                "oracle_state": "signal_violation",
                "entry_speed_mps": float(window[0]["speed"]) if window else 0.0,
                "duration_s": float(episode.t_end - episode.t_start),
            }
            out.append(
                _oracle_event(
                    participant_id=pid,
                    event_type=ORACLE_STATE_EVENT_TYPES["signal_violation"],
                    t_start=episode.t_start,
                    t_peak=episode.t_start,
                    t_end=episode.t_end,
                    subject="signal_violation",
                    id_subject="signal_violation@self",
                    values=values,
                    confidence=confidence,
                    owners=[pid],
                    evidence=[
                        Evidence(
                            kind=EVIDENCE_KIND,
                            ref="signal_violation:{0}".format(pid),
                            t_start=episode.t_start,
                            t_end=episode.t_end,
                            detail={
                                "source": "privileged_map_and_signal_state",
                                "junction_ids": junction_ids,
                                "traffic_light_state": "Red",
                            },
                        )
                    ],
                )
            )
    return out


def _right_of_way_events(
    trace: Dict[str, Any], participants: Sequence[str], cfg: Config
) -> List[Event]:
    """``right_of_way``: two participants inside the same junction at once.

    Shared occupancy of one junction is the privileged, map-level statement of a
    right-of-way conflict. It is emitted from each party's point of view, like
    the pair states, so a template may name either of them.
    """
    min_duration_s = float(cfg.get("oracle.right_of_way.min_duration_s", 0.0))
    confidence = _confidence(cfg, "oracle_state", 0.95)

    out: List[Event] = []
    for (a, b) in _pairs(participants):
        rows_a = {r["frame"]: r for r in participant_series(trace, a)}
        rows_b = {r["frame"]: r for r in participant_series(trace, b)}
        frames = sorted(set(rows_a.keys()) & set(rows_b.keys()))
        if not frames:
            continue
        times = [float(rows_a[f]["t"]) for f in frames]
        flags: List[Optional[float]] = []
        junctions: List[Optional[int]] = []
        for f in frames:
            ra, rb = rows_a[f], rows_b[f]
            ja, jb = ra.get("junction_id"), rb.get("junction_id")
            shared = (
                bool(ra.get("is_junction", False))
                and bool(rb.get("is_junction", False))
                and ja is not None
                and jb is not None
                and int(ja) == int(jb)
            )
            flags.append(1.0 if shared else 0.0)
            junctions.append(int(ja) if shared else None)

        for episode in _find_episodes(times, flags, 1.0, "above", min_duration_s):
            ids = sorted(
                {
                    j
                    for t, j in zip(times, junctions)
                    if j is not None and episode.t_start - 1e-9 <= t <= episode.t_end + 1e-9
                }
            )
            values = {
                "oracle_state": "right_of_way",
                "duration_s": float(episode.t_end - episode.t_start),
            }
            for pid, counterpart in ((a, b), (b, a)):
                out.append(
                    _oracle_event(
                        participant_id=pid,
                        event_type=ORACLE_STATE_EVENT_TYPES["right_of_way"],
                        t_start=episode.t_start,
                        t_peak=episode.t_start,
                        t_end=episode.t_end,
                        subject="right_of_way",
                        id_subject="right_of_way@{0}".format(counterpart),
                        values=values,
                        confidence=confidence,
                        owners=[pid, counterpart],
                        evidence=[
                            Evidence(
                                kind=EVIDENCE_KIND,
                                ref="right_of_way:{0}|{1}".format(*sorted([a, b])),
                                t_start=episode.t_start,
                                t_end=episode.t_end,
                                detail={
                                    "source": "privileged_map_state",
                                    "junction_ids": ids,
                                    "counterpart": counterpart,
                                    "pair": sorted([a, b]),
                                },
                            )
                        ],
                    )
                )
    return out


def _outcome_events(trace: Dict[str, Any], participants: Sequence[str], cfg: Config) -> List[Event]:
    """Collisions, near misses and post-impact stops from the privileged record."""
    near_miss_m = float(
        cfg.get(
            "oracle.near_miss.min_separation_m",
            cfg.get("recorder.triggers.near_miss.min_range_m", 12.0),
        )
    )
    if near_miss_m <= 0.0:
        raise ValueError(
            "oracle.near_miss.min_separation_m must be positive, got {0!r}".format(near_miss_m)
        )
    stop_speed = float(cfg.get("events.outcome.post_impact_stop.speed_mps", 0.6))
    stop_within = float(cfg.get("events.outcome.post_impact_stop.within_s", 4.0))
    near_miss_conf = _confidence(cfg, "near_miss", 0.9)
    stop_conf = _confidence(cfg, "post_impact_stop", 0.9)

    impacts = _collision_pairs(trace)
    out: List[Event] = []

    for (a, b), (t_impact, impulse, frame) in sorted(impacts.items()):
        states = pair_kinematics(trace, a, b)
        at_impact = pre_impact_state(states, t_impact)
        speeds = _speeds_before(trace, [a, b], t_impact)
        values: Dict[str, Any] = {
            "impulse": impulse,
            "separation_m": at_impact.distance if at_impact is not None else 0.0,
            "relative_speed_mps": at_impact.closing_speed if at_impact is not None else 0.0,
            "own_speed_mps": speeds.get(a, 0.0),
            "other_speed_mps": speeds.get(b, 0.0),
        }
        out.append(
            _oracle_event(
                participant_id=a,
                event_type=EventType.COLLISION,
                t_start=t_impact,
                t_peak=t_impact,
                t_end=t_impact,
                subject=None,
                id_subject="collision@{0}|{1}".format(a, b),
                values=values,
                # Deterministic: the simulator's own contact channel recorded it.
                confidence=1.0,
                owners=[a, b],
                evidence=[
                    Evidence(
                        kind=EVIDENCE_KIND,
                        ref="collision:{0}|{1}".format(a, b),
                        t_start=t_impact,
                        t_end=t_impact,
                        detail={
                            "source": "privileged_collision_sensor",
                            "pair": [a, b],
                            "impulse": impulse,
                            "frame": frame,
                        },
                    )
                ],
            )
        )

    for (a, b) in _pairs(participants):
        if (a, b) in impacts:
            continue
        states = pair_kinematics(trace, a, b)
        if not states:
            continue
        closest = min(states, key=lambda s: (s.distance, s.t))
        if closest.distance > near_miss_m:
            continue
        values = {
            "min_separation_m": closest.distance,
            "relative_speed_mps": closest.closing_speed,
            "threshold_m": near_miss_m,
        }
        out.append(
            _oracle_event(
                participant_id=a,
                event_type=EventType.NEAR_MISS,
                t_start=closest.t,
                t_peak=closest.t,
                t_end=closest.t,
                subject=None,
                id_subject="near_miss@{0}|{1}".format(a, b),
                values=values,
                confidence=near_miss_conf,
                owners=[a, b],
                evidence=[
                    Evidence(
                        kind=EVIDENCE_KIND,
                        ref="near_miss:{0}|{1}".format(a, b),
                        t_start=closest.t,
                        t_end=closest.t,
                        detail={
                            "source": "exact_kinematics",
                            "pair": [a, b],
                            "min_separation_m": closest.distance,
                        },
                    )
                ],
            )
        )

    # Post-impact stop: the first time an involved vehicle is at rest after its
    # own impact. Measured from the true speed, not from a brake command.
    impacted: Dict[str, float] = {}
    for (a, b), (t_impact, _impulse, _frame) in impacts.items():
        for pid in (a, b):
            if pid not in impacted or t_impact < impacted[pid]:
                impacted[pid] = t_impact
    for pid in sorted(impacted.keys()):
        t_impact = impacted[pid]
        rows = participant_series(trace, pid)
        stop_row = None
        for row in rows:
            t = float(row["t"])
            if t < t_impact - 1e-9:
                continue
            if t > t_impact + stop_within + 1e-9:
                break
            if float(row["speed"]) <= stop_speed:
                stop_row = row
                break
        if stop_row is None:
            continue
        t_stop = float(stop_row["t"])
        values = {
            "speed_mps": float(stop_row["speed"]),
            "delay_s": t_stop - t_impact,
            "threshold_mps": stop_speed,
        }
        out.append(
            _oracle_event(
                participant_id=pid,
                event_type=EventType.POST_IMPACT_STOP,
                t_start=t_impact,
                t_peak=t_stop,
                t_end=t_stop,
                subject=None,
                id_subject="post_impact_stop@self",
                values=values,
                confidence=stop_conf,
                owners=[pid],
                evidence=[
                    Evidence(
                        kind=EVIDENCE_KIND,
                        ref="post_impact_stop:{0}".format(pid),
                        t_start=t_impact,
                        t_end=t_stop,
                        detail={"source": "exact_kinematics", "t_impact": t_impact},
                    )
                ],
            )
        )
    return out


def _collision_pairs(trace: Dict[str, Any]) -> Dict[Tuple[str, str], Tuple[float, float, int]]:
    """Deduplicated true collisions, keyed by the ordered pair.

    The simulator reports one record per involved actor, so every participant
    pair appears twice in the raw list; the canonical key is order independent
    and the earliest record wins. Only participant-to-participant impacts are
    kept: a vehicle clipping street furniture is not a forensic outcome of this
    scenario.
    """
    out: Dict[Tuple[str, str], Tuple[float, float, int]] = {}
    for record in trace.get("collisions", []) or []:
        other = record.get("other_participant_id")
        if other is None:
            continue
        a, b = sorted([str(record["participant_id"]), str(other)])
        t = float(record["t"])
        entry = (t, float(record.get("impulse", 0.0)), int(record.get("frame", 0)))
        if (a, b) not in out or t < out[(a, b)][0]:
            out[(a, b)] = entry
    return out


def nearest_state(states: Sequence[OracleState], t: float) -> Optional[OracleState]:
    """The pair state sampled closest to ``t``."""
    if not states:
        return None
    return min(states, key=lambda s: (abs(s.t - float(t)), s.t))


def pre_impact_state(states: Sequence[OracleState], t: float) -> Optional[OracleState]:
    """The last pair state recorded strictly before ``t``.

    Impact kinematics must be read from the sample *before* the contact, not from
    the one that reports it: the simulator resolves the collision inside the tick
    it reports, so that frame already carries the post-contact velocities. Reading
    it would put the closing speed of a 28 km/h rear-end at zero, and the severity
    of every impact in the study with it.
    """
    earlier = [s for s in states if s.t < float(t) - 1e-9]
    if earlier:
        return earlier[-1]
    return nearest_state(states, t)


def pre_impact_row(
    rows: Sequence[Dict[str, Any]], t: float
) -> Optional[Dict[str, Any]]:
    """The last privileged state of one participant strictly before ``t``.

    Same reasoning as :func:`pre_impact_state`, for a single participant.
    """
    if not rows:
        return None
    earlier = [r for r in rows if float(r["t"]) < float(t) - 1e-9]
    if earlier:
        return earlier[-1]
    return min(rows, key=lambda r: (abs(float(r["t"]) - float(t)), float(r["t"])))


def _speeds_before(
    trace: Dict[str, Any], participants: Sequence[str], t: float
) -> Dict[str, float]:
    """True speed of each participant at the last sample before ``t``."""
    out: Dict[str, float] = {}
    for pid in participants:
        row = pre_impact_row(participant_series(trace, pid), t)
        if row is not None:
            out[str(pid)] = float(row["speed"])
    return out


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def build_oracle_events(trace: Dict[str, Any], spec: Any, cfg: Config) -> List[Event]:
    """Measure every privileged event of one run.

    Parameters
    ----------
    trace:
        The mapping returned by :func:`load_oracle_trace`.
    spec:
        The :class:`~cdf.simulation.scenario_base.ScenarioSpec` of the run. Used
        only to cross-check that every participant the scenario declared is
        actually present in the trace; the events themselves are measured, never
        assumed from the specification. ``None`` skips the cross-check.
    cfg:
        Threshold registry. Keys read: ``events.radar.range_decreasing.*``,
        ``events.radar.critical_ttc.ttc_s``, ``events.hard_deceleration.enter_mps2``,
        ``events.min_duration_s``, ``events.outcome.post_impact_stop.*``,
        ``indicators.conflict.region_radius_m``,
        ``indicators.conflict.max_arrival_gap_s``,
        ``oracle.conflict.min_crossing_angle_deg``,
        ``oracle.near_miss.min_separation_m`` (defaulting to
        ``recorder.triggers.near_miss.min_range_m``),
        ``oracle.signal_violation.min_duration_s``,
        ``oracle.right_of_way.min_duration_s`` and ``oracle.confidence.*``.

    Returns
    -------
    list of Event
        Every event carries ``provenance=ORACLE``, sorted by peak time then type
        then id so that two runs of the same seed produce identical output.

    Raises
    ------
    ValueError
        When the scenario declares a participant the trace never recorded. That
        means the run did not execute the scenario it claims to, and scoring
        against it would be meaningless.
    """
    participants = [str(p) for p in trace.get("participants", []) or []]
    if not participants:
        raise ValueError("oracle trace lists no participants; nothing can be measured")
    if spec is not None:
        missing = [p for p in getattr(spec, "participant_ids", []) if p not in participants]
        if missing:
            raise ValueError(
                "scenario {0} declares participant(s) {1} that the privileged trace "
                "never recorded (recorded: {2})".format(
                    getattr(spec, "scenario_id", "?"), missing, participants
                )
            )

    events: List[Event] = []
    events.extend(_action_events(trace, cfg))
    for (a, b) in _pairs(participants):
        events.extend(_closing_and_ttc_events(pair_kinematics(trace, a, b), cfg))
        events.extend(_conflict_entry_events(trace, a, b, cfg))
    events.extend(_deceleration_events(trace, participants, cfg))
    events.extend(_signal_violation_events(trace, participants, cfg))
    events.extend(_right_of_way_events(trace, participants, cfg))
    events.extend(_outcome_events(trace, participants, cfg))

    events.sort(
        key=lambda e: (
            float(e.t_peak),
            float(e.t_start),
            e.event_type.value,
            str(e.participant_id),
            str(e.event_id),
        )
    )
    _assert_unique_ids(events)
    return events


def _assert_unique_ids(events: Sequence[Event]) -> None:
    """Fail loudly on a duplicated event id.

    A collision here would silently drop a ground-truth node from every graph
    built on these events, quietly deflating recall for the layer being scored.
    """
    seen: Dict[str, Event] = {}
    for event in events:
        if event.event_id in seen:
            other = seen[event.event_id]
            raise ValueError(
                "duplicate oracle event id {0}: {1}@{2:.3f} and {3}@{4:.3f}".format(
                    event.event_id,
                    event.event_type.value,
                    event.t_peak,
                    other.event_type.value,
                    other.t_peak,
                )
            )
        seen[event.event_id] = event
