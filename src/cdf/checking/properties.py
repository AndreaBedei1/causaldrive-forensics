"""Finite-trace temporal properties, evaluated on locally recorded evidence.

Why a hand-written monitor
--------------------------
A classical model checker answers a question we cannot honestly ask here: it
assumes the model is *complete*. A participant's onboard recording is not. Radar
tracks drop out, the log window is finite, and a participant can be involved in a
collision it never saw coming. Feeding such a trace to a two-valued checker would
turn "I had no evidence" into "the property holds", which is exactly the failure
mode this project exists to avoid.

The monitor below is therefore three-valued. Each property is evaluated over the
finite, irregular sample sequence a single participant actually recorded, and
returns

* ``PASS``    -- the property is *witnessed* to hold on this trace,
* ``FAIL``    -- a concrete violating interval exists and can be shown, and
* ``UNKNOWN`` -- the local evidence cannot decide it.

``UNKNOWN`` is produced in four distinct situations, all reported in
:attr:`PropertyResult.reason`:

1. the sensor stream the property needs was never recorded (no radar tracks, no
   controls, no telemetry);
2. the antecedent of the implication never held, so the property is only
   *vacuously* true and carries no evidential weight (a vacuous PASS would be
   indistinguishable from a real one when aggregated);
3. the trace ends before the deadline the property talks about, so the required
   response might still have occurred off-record;
4. an evidence gap sits exactly where the verdict would be decided.

Scope discipline
----------------
:data:`LOCAL_PROPERTIES` take a :class:`~cdf.common.evidence.ParticipantEvidence`
and carry ``scope=Provenance.LOCAL``. :data:`ORACLE_PROPERTIES` are privileged:
they answer questions (was the signal red? who had right of way?) that no onboard
sensor can answer, and they carry ``scope=Provenance.ORACLE``. To keep the layer
boundary structural rather than conventional, the oracle properties operate on a
plain dictionary trace, so this module never imports :mod:`cdf.oracle`. Their
verdicts are evaluation-only and must never re-enter local or fused inference --
:class:`~cdf.checking.trace_checker.TraceChecker` keeps the two families in
separate methods and separate reports.

Expected oracle trace shape
---------------------------
``check_oracle`` accepts a mapping of the form::

    {
      "run_id": "...", "scenario_id": "...",
      "samples": [
        {"t": 0.05,
         "actors": {"A": {"x": .., "y": .., "speed": ..,
                          "signal_state": "red",     # signal facing this actor
                          "in_junction": false,
                          "has_right_of_way": true}}},
        ...
      ]
    }

Any field may be missing; a property that needs an absent field returns
``UNKNOWN`` rather than guessing.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence
from ..common.geometry import time_to_collision_1d
from ..common.schemas import CheckStatus, EventType, Provenance, to_jsonable

__all__ = [
    "PropertyResult",
    "Property",
    "PropertyEvaluator",
    "TraceSample",
    "build_state_trace",
    "trace_parameters",
    "make_counterexample_ref",
    "combine_statuses",
    "oracle_participant_ids",
    "P1_BRAKE_RESPONSE",
    "P2_NO_THROTTLE_CLOSING",
    "P3_POST_COLLISION_STOP",
    "P4_CONFLICT_NO_RESPONSE",
    "O1_SIGNAL_COMPLIANCE",
    "O2_RIGHT_OF_WAY",
    "LOCAL_PROPERTIES",
    "ORACLE_PROPERTIES",
    "property_by_id",
]


#: Absolute tolerance used when comparing sample timestamps against interval
#: bounds. Sample times are exact multiples of the simulator step, so this only
#: absorbs floating-point accumulation, never a real timing difference.
_T_EPS = 1e-9


# ---------------------------------------------------------------------------
# Results and property descriptors
# ---------------------------------------------------------------------------


@dataclass
class PropertyResult:
    """Verdict of one property on one participant's (or the oracle's) trace.

    Every field exists so that a reader can reconstruct *why* the monitor said
    what it said without rerunning it: ``witness`` holds the measured quantities
    that decided the verdict, ``parameters`` holds every threshold that was in
    force, and ``violating_intervals`` localises a ``FAIL`` in simulation time.
    """

    property_id: str
    status: CheckStatus
    participant_id: str
    violating_intervals: List[Tuple[float, float]] = field(default_factory=list)
    witness: Dict[str, Any] = field(default_factory=dict)
    counterexample_ref: Optional[str] = None
    reason: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    scope: Provenance = Provenance.LOCAL

    def to_dict(self) -> Dict[str, Any]:
        """JSON-serialisable form (enums become their string values)."""
        return to_jsonable(self)

    @property
    def decided(self) -> bool:
        """Whether the verdict is ``PASS`` or ``FAIL`` (i.e. not ``UNKNOWN``)."""
        return self.status is not CheckStatus.UNKNOWN


#: Signature of a property evaluator. The first argument is a
#: :class:`~cdf.common.evidence.ParticipantEvidence` for a ``LOCAL`` property and
#: a plain oracle-trace mapping for an ``ORACLE`` one; it is typed ``Any`` because
#: one :class:`Property` container describes both families.
PropertyEvaluator = Callable[[Any, Config, Dict[str, Any]], PropertyResult]


@dataclass(frozen=True)
class Property:
    """A named finite-trace property together with its evaluator.

    ``formal`` is a semi-formal MTL-style rendering kept next to the code on
    purpose: it is what appears in the report and in the paper, and keeping it in
    the same object as the evaluator makes a drift between the two visible.
    """

    property_id: str
    description: str
    formal: str
    scope: Provenance
    evaluate: PropertyEvaluator

    def describe(self) -> Dict[str, Any]:
        """Metadata block for reports and the viewer (no evaluation performed)."""
        return {
            "property_id": self.property_id,
            "description": self.description,
            "formal": self.formal,
            "scope": self.scope.value,
        }


def make_counterexample_ref(
    property_id: str, participant_id: str, t_start: float, t_end: float
) -> str:
    """Deterministic key linking a ``FAIL`` verdict to its extracted trace.

    Determinism matters because the checking report and the counterexample report
    are written as two separate artifacts and must be joinable after the fact.
    """
    return "CE:{0}:{1}:{2:.2f}-{3:.2f}".format(
        property_id, participant_id, float(t_start), float(t_end)
    )


def combine_statuses(statuses: Sequence[CheckStatus]) -> CheckStatus:
    """Conjunctive combination of sub-verdicts.

    ``FAIL`` dominates (one witnessed violation refutes the whole conjunction),
    then ``UNKNOWN`` (an undecided conjunct makes the conjunction undecided), and
    ``PASS`` only when every conjunct passed. An empty sequence is ``UNKNOWN``:
    nothing was checked, so nothing is known.
    """
    if not statuses:
        return CheckStatus.UNKNOWN
    if any(s is CheckStatus.FAIL for s in statuses):
        return CheckStatus.FAIL
    if any(s is CheckStatus.UNKNOWN for s in statuses):
        return CheckStatus.UNKNOWN
    return CheckStatus.PASS


# ---------------------------------------------------------------------------
# The sampled state trace every local property is evaluated over
# ---------------------------------------------------------------------------


@dataclass
class TraceSample:
    """One instant of the flattened state a local property reasons about.

    ``None`` means *not observed at this instant* and is never silently coerced
    to a number -- that distinction is the whole basis of the ``UNKNOWN`` verdict.
    """

    t: float
    speed: Optional[float] = None
    throttle: Optional[float] = None
    brake: Optional[float] = None
    steer: Optional[float] = None
    min_range: Optional[float] = None
    """Smallest range over the tracks active at this instant, metres."""
    min_ttc: Optional[float] = None
    """Smallest defined time-to-collision over the active tracks, seconds."""
    closing_rate: Optional[float] = None
    """Largest closing speed over the active tracks (positive = closing), m/s."""
    active_track_ids: List[str] = field(default_factory=list)


def trace_parameters(ev: ParticipantEvidence, cfg: Config) -> Dict[str, float]:
    """Sampling tolerances used to flatten a participant's streams.

    They are recorded in every :attr:`PropertyResult.parameters` because they can
    change a verdict (a too-tight tolerance turns present controls into missing
    evidence), so reproducing a verdict requires knowing them.
    """
    period = ev.sample_period()
    tol = cfg.get("checking.trace.match_tolerance_s", None)
    if tol is None:
        # Strictly *below* one sampling period. A nearest-neighbour join has to
        # absorb timestamp jitter (which can never exceed half a period, since a
        # sample is always assigned to its closest grid point), but it must never
        # be able to bridge a whole missing sample: a tolerance at or above the
        # period silently fills a drop-out in from its neighbour, and the monitor
        # would then reason over evidence that was never recorded. At the 20 Hz
        # the pipeline records at, the previous 0.06 s floor did exactly that.
        tol = 0.75 * period if period else 0.06
    gap = cfg.get("checking.trace.max_gap_s", None)
    if gap is None:
        gap = max(3.0 * period, 0.25) if period else 0.25
    return {"match_tolerance_s": float(tol), "max_gap_s": float(gap)}


def build_state_trace(ev: ParticipantEvidence, cfg: Config) -> List[TraceSample]:
    """Flatten telemetry, controls and radar tracks onto one sample grid.

    The grid is the participant's own telemetry timeline (falling back to the
    control or track timeline when telemetry is absent), because that is the
    highest-rate stream a vehicle records about itself. Streams are joined by
    nearest-neighbour lookup inside ``match_tolerance_s``; a stream with no sample
    near a grid point leaves ``None`` there instead of being interpolated, so a
    genuine drop-out stays visible to the monitor.
    """
    params = trace_parameters(ev, cfg)
    tol = params["match_tolerance_s"]
    grid = _base_grid(ev)
    if not grid:
        return []

    samples = [TraceSample(t=t) for t in grid]
    for i, t in enumerate(grid):
        tel = ev.telemetry_at(t, max_gap=tol)
        if tel is not None:
            samples[i].speed = float(tel.speed)
        ctl = ev.control_at(t, max_gap=tol)
        if ctl is not None:
            samples[i].throttle = float(ctl.throttle)
            samples[i].brake = float(ctl.brake)
            samples[i].steer = float(ctl.steer)

    for ts in ev.tracks:
        i = _nearest_index(grid, float(ts.t), tol)
        if i is None:
            continue
        s = samples[i]
        s.active_track_ids.append(str(ts.track_id))
        rng = float(ts.range_m)
        if s.min_range is None or rng < s.min_range:
            s.min_range = rng
        ttc = ts.ttc if ts.ttc is not None else time_to_collision_1d(rng, ts.range_rate)
        if ttc is not None and float(ttc) >= 0.0:
            if s.min_ttc is None or float(ttc) < s.min_ttc:
                s.min_ttc = float(ttc)
        closing = -float(ts.range_rate)
        if closing > 0.0 and (s.closing_rate is None or closing > s.closing_rate):
            s.closing_rate = closing

    for s in samples:
        s.active_track_ids = sorted(set(s.active_track_ids))
    return samples


def _base_grid(ev: ParticipantEvidence) -> List[float]:
    """Sorted, de-duplicated sample times of the richest available own stream."""
    for stream in (ev.telemetry, ev.controls, ev.tracks):
        if stream:
            times = sorted({round(float(s.t), 9) for s in stream})
            return [float(t) for t in times]
    return []


def _nearest_index(grid: Sequence[float], t: float, tol: float) -> Optional[int]:
    """Index of the grid point nearest to ``t``, or ``None`` beyond ``tol``."""
    if not grid:
        return None
    i = bisect.bisect_left(grid, float(t))
    best: Optional[int] = None
    best_d = float("inf")
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(grid):
            d = abs(float(grid[j]) - float(t))
            if d < best_d:
                best, best_d = j, d
    if best is None or best_d > float(tol):
        return None
    return best


def _runs(
    trace: Sequence[TraceSample], flags: Sequence[bool], max_gap: float
) -> List[Tuple[int, int]]:
    """Maximal index ranges where ``flags`` holds without an evidence gap.

    A time gap larger than ``max_gap`` splits a run: the monitor must not claim a
    condition persisted across an interval it never sampled.
    """
    runs: List[Tuple[int, int]] = []
    start: Optional[int] = None
    for i, f in enumerate(flags):
        if f:
            if start is None:
                start = i
            elif float(trace[i].t) - float(trace[i - 1].t) > float(max_gap):
                runs.append((start, i - 1))
                start = i
        elif start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(flags) - 1))
    return runs


def _window(
    trace: Sequence[TraceSample], t0: float, t1: float
) -> List[TraceSample]:
    """Samples with ``t0 <= t <= t1`` (inclusive, tolerant of float noise)."""
    return [s for s in trace if float(t0) - _T_EPS <= s.t <= float(t1) + _T_EPS]


def _max_evidence_gap(
    window: Sequence[TraceSample],
    t0: float,
    t1: float,
    observed: Callable[[TraceSample], bool],
) -> float:
    """Longest stretch of ``[t0, t1]`` carrying no sample that ``observed`` accepts.

    This is what separates "the response did not happen" from "the response was
    not recorded". A property may only report ``FAIL`` when the quantity it needs
    was sampled densely enough across the whole deadline; a blackout in the
    middle of the window leaves room for an unobserved response, and a monitor
    that ignores it is claiming evidence it does not have.

    Leading and trailing gaps count: evidence that starts halfway through the
    window says nothing about the first half.
    """
    ts = sorted(float(s.t) for s in window if observed(s))
    if not ts:
        return float(t1) - float(t0)
    gap = max(ts[0] - float(t0), float(t1) - ts[-1])
    for a, b in zip(ts, ts[1:]):
        if b - a > gap:
            gap = b - a
    return max(0.0, gap)


def _last_time(items: Sequence[Any]) -> Optional[float]:
    """Largest ``.t`` in a record stream, or ``None`` when it is empty."""
    if not items:
        return None
    return max(float(s.t) for s in items)


def _result(
    property_id: str,
    participant_id: str,
    status: CheckStatus,
    parameters: Dict[str, Any],
    reason: str,
    witness: Optional[Dict[str, Any]] = None,
    intervals: Optional[Sequence[Tuple[float, float]]] = None,
    scope: Provenance = Provenance.LOCAL,
) -> PropertyResult:
    """Assemble a :class:`PropertyResult`, attaching a counterexample key on FAIL."""
    ivs = [(float(a), float(b)) for a, b in (intervals or [])]
    ivs.sort()
    ref: Optional[str] = None
    if status is CheckStatus.FAIL and ivs:
        hull_start = min(a for a, _ in ivs)
        hull_end = max(b for _, b in ivs)
        ref = make_counterexample_ref(
            property_id, participant_id, hull_start, hull_end
        )
    return PropertyResult(
        property_id=property_id,
        status=status,
        participant_id=participant_id,
        violating_intervals=ivs,
        witness=dict(witness or {}),
        counterexample_ref=ref,
        reason=reason,
        parameters=dict(parameters),
        scope=scope,
    )


def _min_optional(values: Sequence[Optional[float]]) -> Optional[float]:
    present = [float(v) for v in values if v is not None]
    return min(present) if present else None


def _max_optional(values: Sequence[Optional[float]]) -> Optional[float]:
    present = [float(v) for v in values if v is not None]
    return max(present) if present else None


# ---------------------------------------------------------------------------
# P1 -- braking response to a critical time-to-collision
# ---------------------------------------------------------------------------

P1_ID = "P1_brake_response"


def _evaluate_p1(
    ev: ParticipantEvidence, cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( critical_ttc -> F[0, response_window] brake >= brake_cmd )``.

    The antecedent is an *episode*: a maximal stretch during which the smallest
    time-to-collision over the participant's own tracks stays at or below the
    critical threshold. The response deadline is measured from the episode onset,
    because that is the first instant at which a driver or an ADAS could have
    known. Braking that was already in progress at the onset counts as a response
    -- reacting early is not a violation.
    """
    params: Dict[str, Any] = {
        "ttc_critical_s": float(cfg.get("checking.P1_brake_response.ttc_critical_s", 1.6)),
        "response_window_s": float(
            cfg.get("checking.P1_brake_response.response_window_s", 1.2)
        ),
        "brake_cmd": float(cfg.get("checking.P1_brake_response.brake_cmd", 0.25)),
    }
    params.update(trace_parameters(ev, cfg))
    pid = ev.participant_id

    trace = build_state_trace(ev, cfg)
    if not trace:
        return _result(
            P1_ID, pid, CheckStatus.UNKNOWN, params,
            "no telemetry, control or track samples were recorded for this participant",
        )

    critical_events = ev.events_of_type(EventType.CRITICAL_TTC)
    if not ev.tracks and not critical_events:
        return _result(
            P1_ID, pid, CheckStatus.UNKNOWN, params,
            "no radar track and no CRITICAL_TTC event evidence: this participant "
            "never observed a time-to-collision, so the antecedent cannot be evaluated",
            witness={"n_track_samples": 0, "n_critical_ttc_events": 0},
        )

    thr = params["ttc_critical_s"]
    window_s = params["response_window_s"]
    brake_cmd = params["brake_cmd"]
    max_gap = params["max_gap_s"]

    observed_ttc = [s.min_ttc for s in trace]
    min_ttc_observed = _min_optional(observed_ttc)

    if min_ttc_observed is not None:
        episode_source = "sampled_ttc"
        flags = [s.min_ttc is not None and s.min_ttc <= thr for s in trace]
        episodes = [
            (float(trace[a].t), float(trace[b].t)) for a, b in _runs(trace, flags, max_gap)
        ]
    elif critical_events:
        episode_source = "critical_ttc_events"
        episodes = [
            (float(e.t_start), float(e.t_end if e.t_end is not None else e.t_peak))
            for e in critical_events
        ]
        episodes.sort()
    else:
        return _result(
            P1_ID, pid, CheckStatus.UNKNOWN, params,
            "radar tracks were recorded but no time-to-collision was ever defined "
            "(nothing was closing), so the antecedent cannot be evaluated",
            witness={"n_track_samples": len(ev.tracks), "min_ttc_observed": None},
        )

    base_witness: Dict[str, Any] = {
        "evidence_source": episode_source,
        "n_track_samples": len(ev.tracks),
        "n_critical_ttc_events": len(critical_events),
        "min_ttc_observed": min_ttc_observed,
        "n_episodes": len(episodes),
    }

    if not episodes:
        base_witness["n_responded"] = 0
        return _result(
            P1_ID, pid, CheckStatus.UNKNOWN, params,
            "antecedent never held: the smallest observed time-to-collision "
            "({0}) never reached the critical threshold {1:.2f} s, so the "
            "property is only vacuously true".format(
                "{0:.2f} s".format(min_ttc_observed)
                if min_ttc_observed is not None
                else "undefined",
                thr,
            ),
            witness=base_witness,
        )

    control_horizon = _last_time(ev.controls)
    violations: List[Tuple[float, float]] = []
    undecidable: List[Dict[str, Any]] = []
    latencies: List[float] = []

    for t0, _t_end in episodes:
        deadline = t0 + window_s
        win = _window(trace, t0, deadline)
        braking = [s for s in win if s.brake is not None and s.brake >= brake_cmd]
        if braking:
            latencies.append(float(min(s.t for s in braking)) - t0)
            continue
        if not any(s.brake is not None for s in win):
            undecidable.append(
                {"onset_s": t0, "why": "no control evidence inside the response window"}
            )
            continue
        if control_horizon is None or control_horizon < deadline - _T_EPS:
            undecidable.append(
                {"onset_s": t0, "why": "trace ends before the response window elapses"}
            )
            continue
        gap = _max_evidence_gap(win, t0, deadline, lambda s: s.brake is not None)
        if gap > max_gap + _T_EPS:
            undecidable.append(
                {
                    "onset_s": t0,
                    "gap_s": gap,
                    "why": "an evidence gap sits inside the response window",
                }
            )
            continue
        violations.append((t0, deadline))

    base_witness["n_violations"] = len(violations)
    base_witness["n_undecidable"] = len(undecidable)
    base_witness["n_responded"] = len(latencies)
    base_witness["first_episode_onset_s"] = episodes[0][0]
    base_witness["max_response_latency_s"] = max(latencies) if latencies else None
    base_witness["max_brake_observed"] = _max_optional([s.brake for s in trace])
    if undecidable:
        base_witness["undecidable_episodes"] = undecidable

    if violations:
        return _result(
            P1_ID, pid, CheckStatus.FAIL, params,
            "{0} critical-TTC episode(s) were not followed by brake >= {1:.2f} "
            "within {2:.2f} s".format(len(violations), brake_cmd, window_s),
            witness=base_witness, intervals=violations,
        )
    if undecidable:
        return _result(
            P1_ID, pid, CheckStatus.UNKNOWN, params,
            "{0} of {1} critical-TTC episode(s) could not be decided ({2})".format(
                len(undecidable), len(episodes), undecidable[0]["why"]
            ),
            witness=base_witness,
        )
    return _result(
        P1_ID, pid, CheckStatus.PASS, params,
        "every one of the {0} critical-TTC episode(s) was answered by brake >= "
        "{1:.2f} within {2:.2f} s (worst latency {3:.2f} s)".format(
            len(episodes), brake_cmd, window_s, max(latencies) if latencies else 0.0
        ),
        witness=base_witness,
    )


P1_BRAKE_RESPONSE = Property(
    property_id=P1_ID,
    description=(
        "Whenever this participant's own radar evidence shows a critical "
        "time-to-collision, a braking command of at least brake_cmd must begin "
        "within response_window_s."
    ),
    formal="G( critical_ttc -> F[0,response_window_s] (brake >= brake_cmd) )",
    scope=Provenance.LOCAL,
    evaluate=_evaluate_p1,
)


# ---------------------------------------------------------------------------
# P2 -- no sustained throttle while closing fast
# ---------------------------------------------------------------------------

P2_ID = "P2_no_throttle_while_closing"


def _evaluate_p2(
    ev: ParticipantEvidence, cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( closing_rate >= r -> !G[0, grace_s] (throttle > throttle_cmd) )``.

    A brief overlap of throttle and closing is normal (the pedal takes time to
    release), so only a *sustained* stretch longer than ``grace_s`` is a
    violation. A stretch that is still active when the evidence ends is reported
    as undecidable rather than as compliant: we cannot see whether it continued.
    """
    params: Dict[str, Any] = {
        "closing_rate_mps": float(
            cfg.get("checking.P2_no_throttle_while_closing.closing_rate_mps", 5.0)
        ),
        "grace_s": float(cfg.get("checking.P2_no_throttle_while_closing.grace_s", 1.0)),
        "throttle_cmd": float(
            cfg.get("checking.P2_no_throttle_while_closing.throttle_cmd", 0.20)
        ),
    }
    params.update(trace_parameters(ev, cfg))
    pid = ev.participant_id

    trace = build_state_trace(ev, cfg)
    if not trace:
        return _result(
            P2_ID, pid, CheckStatus.UNKNOWN, params,
            "no telemetry, control or track samples were recorded for this participant",
        )
    if not ev.tracks:
        return _result(
            P2_ID, pid, CheckStatus.UNKNOWN, params,
            "no range-rate evidence: this participant recorded no radar tracks, so "
            "the closing-rate antecedent cannot be evaluated",
            witness={"n_track_samples": 0},
        )

    rate = params["closing_rate_mps"]
    grace = params["grace_s"]
    throttle_cmd = params["throttle_cmd"]
    max_gap = params["max_gap_s"]

    closing_flags = [s.closing_rate is not None and s.closing_rate >= rate for s in trace]
    closing_runs = _runs(trace, closing_flags, max_gap)
    max_closing = _max_optional([s.closing_rate for s in trace])

    witness: Dict[str, Any] = {
        "n_track_samples": len(ev.tracks),
        "max_closing_rate_mps": max_closing,
        "n_closing_episodes": len(closing_runs),
    }

    if not closing_runs:
        return _result(
            P2_ID, pid, CheckStatus.UNKNOWN, params,
            "antecedent never held: the largest observed closing rate ({0}) never "
            "reached {1:.2f} m/s, so the property is only vacuously true".format(
                "{0:.2f} m/s".format(max_closing) if max_closing is not None else "0 m/s",
                rate,
            ),
            witness=witness,
        )

    closing_idx = [i for i, f in enumerate(closing_flags) if f]
    if not any(trace[i].throttle is not None for i in closing_idx):
        return _result(
            P2_ID, pid, CheckStatus.UNKNOWN, params,
            "no throttle evidence inside any of the {0} closing episode(s)".format(
                len(closing_runs)
            ),
            witness=witness,
        )

    viol_flags = [
        closing_flags[i]
        and trace[i].throttle is not None
        and trace[i].throttle > throttle_cmd
        for i in range(len(trace))
    ]
    runs = _runs(trace, viol_flags, max_gap)
    last_index = len(trace) - 1

    violations: List[Tuple[float, float]] = []
    undecidable: List[Dict[str, Any]] = []
    longest = 0.0
    for a, b in runs:
        duration = float(trace[b].t) - float(trace[a].t)
        longest = max(longest, duration)
        if duration > grace + _T_EPS:
            violations.append((float(trace[a].t), float(trace[b].t)))
            continue
        # The run stopped -- but did the condition really stop, or did the
        # evidence? Only the former is compliance.
        if b == last_index:
            undecidable.append(
                {"start_s": float(trace[a].t), "why": "episode still active when the trace ends"}
            )
        elif trace[b + 1].throttle is None or not trace[b + 1].active_track_ids:
            undecidable.append(
                {
                    "start_s": float(trace[a].t),
                    "why": "evidence gap immediately after the episode",
                }
            )

    witness["longest_throttle_while_closing_s"] = longest
    witness["max_throttle_while_closing"] = _max_optional(
        [trace[i].throttle for i in closing_idx]
    )
    witness["n_violations"] = len(violations)
    witness["n_undecidable"] = len(undecidable)
    if undecidable:
        witness["undecidable_episodes"] = undecidable

    if violations:
        return _result(
            P2_ID, pid, CheckStatus.FAIL, params,
            "throttle stayed above {0:.2f} for {1:.2f} s while closing at >= "
            "{2:.2f} m/s, exceeding the {3:.2f} s grace period".format(
                throttle_cmd, longest, rate, grace
            ),
            witness=witness, intervals=violations,
        )
    if undecidable:
        return _result(
            P2_ID, pid, CheckStatus.UNKNOWN, params,
            "{0} throttle-while-closing episode(s) could not be decided ({1})".format(
                len(undecidable), undecidable[0]["why"]
            ),
            witness=witness,
        )
    return _result(
        P2_ID, pid, CheckStatus.PASS, params,
        "throttle never stayed above {0:.2f} for more than {1:.2f} s during any of "
        "the {2} closing episode(s)".format(throttle_cmd, grace, len(closing_runs)),
        witness=witness,
    )


P2_NO_THROTTLE_CLOSING = Property(
    property_id=P2_ID,
    description=(
        "While this participant's own radar shows a target closing faster than "
        "closing_rate_mps, the throttle must not stay above throttle_cmd for "
        "longer than grace_s."
    ),
    formal="G( closing_rate >= closing_rate_mps -> !G[0,grace_s] (throttle > throttle_cmd) )",
    scope=Provenance.LOCAL,
    evaluate=_evaluate_p2,
)


# ---------------------------------------------------------------------------
# P3 -- come to a stop after a collision
# ---------------------------------------------------------------------------

P3_ID = "P3_post_collision_stop"


def _evaluate_p3(
    ev: ParticipantEvidence, cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( collision -> G[0,w](throttle <= max_throttle) & F[0,w](speed < stop) )``.

    The collision instant comes from the participant's *own* onboard trigger (or,
    failing that, its own COLLISION event): nothing about the other party is
    needed. Throttle above the threshold anywhere in the window is a violation
    that can be shown immediately, even on a truncated trace, so it is reported
    as ``FAIL``; failing to *see* the stop on a truncated trace is not.
    """
    params: Dict[str, Any] = {
        "window_s": float(cfg.get("checking.P3_post_collision_stop.window_s", 3.0)),
        "max_throttle": float(
            cfg.get("checking.P3_post_collision_stop.max_throttle", 0.05)
        ),
        "stop_speed_mps": float(
            cfg.get("checking.P3_post_collision_stop.stop_speed_mps", 1.0)
        ),
    }
    params.update(trace_parameters(ev, cfg))
    pid = ev.participant_id

    trace = build_state_trace(ev, cfg)
    if not trace:
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "no telemetry, control or track samples were recorded for this participant",
        )

    trigger = ev.collision_trigger()
    collision_events = ev.events_of_type(EventType.COLLISION)
    if trigger is not None:
        t_c = float(trigger.t)
        source = "onboard_collision_trigger"
        impulse: Optional[float] = float(trigger.impulse)
    elif collision_events:
        t_c = float(collision_events[0].t_peak)
        source = "collision_event"
        impulse = None
    else:
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "antecedent never held: this participant recorded neither a collision "
            "trigger nor a COLLISION event, so the property is only vacuously true",
            witness={"n_triggers": len(ev.triggers), "n_collision_events": 0},
        )

    window_s = params["window_s"]
    max_throttle = params["max_throttle"]
    stop_speed = params["stop_speed_mps"]
    max_gap = params["max_gap_s"]

    t_end = t_c + window_s
    win = _window(trace, t_c, t_end)
    witness: Dict[str, Any] = {
        "collision_source": source,
        "t_collision_s": t_c,
        "impulse": impulse,
        "window_end_s": t_end,
        "n_samples_in_window": len(win),
    }

    if not win:
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "no samples fall inside the {0:.2f} s post-collision window".format(window_s),
            witness=witness,
        )

    throttle_present = [s for s in win if s.throttle is not None]
    speed_present = [s for s in win if s.speed is not None]
    witness["max_throttle_in_window"] = _max_optional([s.throttle for s in win])
    witness["min_speed_in_window"] = _min_optional([s.speed for s in win])

    over_flags = [s.throttle is not None and s.throttle > max_throttle for s in win]
    over_runs = _runs(win, over_flags, max_gap)
    if over_runs:
        intervals = [(float(win[a].t), float(win[b].t)) for a, b in over_runs]
        witness["n_throttle_violations"] = len(intervals)
        return _result(
            P3_ID, pid, CheckStatus.FAIL, params,
            "throttle rose above {0:.2f} within {1:.2f} s of the collision "
            "(peak {2:.2f})".format(
                max_throttle, window_s, witness["max_throttle_in_window"] or 0.0
            ),
            witness=witness, intervals=intervals,
        )

    if not throttle_present or not speed_present:
        missing = "control" if not throttle_present else "telemetry"
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "no {0} evidence inside the post-collision window".format(missing),
            witness=witness,
        )

    stopped = [s for s in speed_present if s.speed < stop_speed]
    horizon = _last_time(ev.telemetry)
    if horizon is None:
        horizon = float(trace[-1].t)
    control_horizon = _last_time(ev.controls)
    truncated = horizon < t_end - _T_EPS or (
        control_horizon is not None and control_horizon < t_end - _T_EPS
    )
    witness["truncated_window"] = bool(truncated)

    if stopped:
        t_stop = float(min(s.t for s in stopped))
        witness["t_stop_s"] = t_stop
        witness["stop_latency_s"] = t_stop - t_c
        return _result(
            P3_ID, pid, CheckStatus.PASS, params,
            "speed fell below {0:.2f} m/s {1:.2f} s after the collision and throttle "
            "never exceeded {2:.2f}".format(stop_speed, t_stop - t_c, max_throttle),
            witness=witness,
        )

    if truncated:
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "the trace ends before the {0:.2f} s post-collision window elapses, so "
            "the stop may have occurred off-record".format(window_s),
            witness=witness,
        )
    # Failing to *see* a stop is only a violation when the speed was actually
    # sampled across the whole window: a blackout leaves room for a stop that
    # was never recorded, and asserting FAIL there would be an over-claim.
    speed_gap = _max_evidence_gap(win, t_c, t_end, lambda s: s.speed is not None)
    witness["max_speed_evidence_gap_s"] = speed_gap
    if speed_gap > max_gap + _T_EPS:
        return _result(
            P3_ID, pid, CheckStatus.UNKNOWN, params,
            "a {0:.2f} s gap in the speed evidence sits inside the post-collision "
            "window, so a stop may have occurred unobserved".format(speed_gap),
            witness=witness,
        )
    return _result(
        P3_ID, pid, CheckStatus.FAIL, params,
        "speed never fell below {0:.2f} m/s within {1:.2f} s of the collision "
        "(minimum {2:.2f} m/s)".format(
            stop_speed, window_s, witness["min_speed_in_window"] or 0.0
        ),
        witness=witness, intervals=[(t_c, t_end)],
    )


P3_POST_COLLISION_STOP = Property(
    property_id=P3_ID,
    description=(
        "After this participant's own collision trigger, the throttle must stay "
        "at or below max_throttle and the speed must fall below stop_speed_mps "
        "within window_s."
    ),
    formal=(
        "G( collision -> ( G[0,window_s] (throttle <= max_throttle) "
        "& F[0,window_s] (speed < stop_speed_mps) ) )"
    ),
    scope=Provenance.LOCAL,
    evaluate=_evaluate_p3,
)


# ---------------------------------------------------------------------------
# P4 -- a detected conflict without any evasive response
# ---------------------------------------------------------------------------

P4_ID = "P4_conflict_without_response"

#: Event types that count as "this participant locally detected a conflict".
_CONFLICT_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.PREDICTED_PATH_CONFLICT,
    EventType.CONFLICT_REGION_ENTRY,
)


def _evaluate_p4(
    ev: ParticipantEvidence, cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( conflict_detected -> F[0,lookahead] (brake >= b | |steer| >= s) )``.

    This is the property that turns "it saw the conflict coming" into a checkable
    statement. The response window is clipped at the outcome (collision or near
    miss) when one occurred earlier: after the outcome there is no longer an
    opportunity to avoid it, so counting that time would be unfair to the
    participant.
    """
    params: Dict[str, Any] = {
        "lookahead_s": float(
            cfg.get("checking.P4_conflict_without_response.lookahead_s", 3.0)
        ),
        "min_evasive_brake": float(
            cfg.get("checking.P4_conflict_without_response.min_evasive_brake", 0.2)
        ),
        "min_evasive_steer": float(
            cfg.get("checking.P4_conflict_without_response.min_evasive_steer", 0.15)
        ),
    }
    params.update(trace_parameters(ev, cfg))
    pid = ev.participant_id

    trace = build_state_trace(ev, cfg)
    if not trace:
        return _result(
            P4_ID, pid, CheckStatus.UNKNOWN, params,
            "no telemetry, control or track samples were recorded for this participant",
        )

    conflicts = []
    for etype in _CONFLICT_EVENT_TYPES:
        conflicts.extend(ev.events_of_type(etype))
    conflicts.sort(key=lambda e: (float(e.t_start), e.event_id))

    if not conflicts:
        return _result(
            P4_ID, pid, CheckStatus.UNKNOWN, params,
            "antecedent never held: this participant detected no predicted path "
            "conflict and no conflict-region entry, so the property is only "
            "vacuously true",
            witness={"n_conflicts": 0, "n_events": len(ev.events)},
        )

    lookahead = params["lookahead_s"]
    min_brake = params["min_evasive_brake"]
    min_steer = params["min_evasive_steer"]

    outcome_times: List[float] = []
    trigger = ev.collision_trigger()
    if trigger is not None:
        outcome_times.append(float(trigger.t))
    for etype in (EventType.COLLISION, EventType.NEAR_MISS):
        outcome_times.extend(float(e.t_peak) for e in ev.events_of_type(etype))
    outcome_t = min(outcome_times) if outcome_times else None

    control_horizon = _last_time(ev.controls)
    violations: List[Tuple[float, float]] = []
    undecidable: List[Dict[str, Any]] = []
    responded: List[float] = []

    for conflict in conflicts:
        t0 = float(conflict.t_start)
        deadline = t0 + lookahead
        clipped = False
        if outcome_t is not None and outcome_t < deadline:
            deadline = outcome_t
            clipped = True
        if deadline <= t0 + _T_EPS:
            undecidable.append(
                {
                    "conflict_t_s": t0,
                    "why": "the outcome left no time in which a response could be observed",
                }
            )
            continue

        win = _window(trace, t0, deadline)
        controls_present = [
            s for s in win if s.brake is not None and s.steer is not None
        ]
        if not controls_present:
            undecidable.append(
                {"conflict_t_s": t0, "why": "no control evidence inside the response window"}
            )
            continue

        evasive = [
            s
            for s in controls_present
            if s.brake >= min_brake or abs(s.steer) >= min_steer
        ]
        if evasive:
            responded.append(float(min(s.t for s in evasive)) - t0)
            continue
        if not clipped and (
            control_horizon is None or control_horizon < deadline - _T_EPS
        ):
            undecidable.append(
                {"conflict_t_s": t0, "why": "trace ends before the lookahead elapses"}
            )
            continue
        gap = _max_evidence_gap(
            win, t0, deadline, lambda s: s.brake is not None and s.steer is not None
        )
        if gap > params["max_gap_s"] + _T_EPS:
            undecidable.append(
                {
                    "conflict_t_s": t0,
                    "gap_s": gap,
                    "why": "an evidence gap sits inside the response window",
                }
            )
            continue
        violations.append((t0, deadline))

    witness: Dict[str, Any] = {
        "n_conflicts": len(conflicts),
        "n_responded": len(responded),
        "n_violations": len(violations),
        "n_undecidable": len(undecidable),
        "first_conflict_t_s": float(conflicts[0].t_start),
        "outcome_t_s": outcome_t,
        "max_brake_after_first_conflict": _max_optional(
            [s.brake for s in trace if s.t >= float(conflicts[0].t_start) - _T_EPS]
        ),
        "max_abs_steer_after_first_conflict": _max_optional(
            [
                abs(s.steer)
                for s in trace
                if s.steer is not None and s.t >= float(conflicts[0].t_start) - _T_EPS
            ]
        ),
        "max_response_latency_s": max(responded) if responded else None,
    }
    if undecidable:
        witness["undecidable_conflicts"] = undecidable

    if violations:
        return _result(
            P4_ID, pid, CheckStatus.FAIL, params,
            "{0} locally detected conflict(s) were followed by no evasive response "
            "(brake >= {1:.2f} or |steer| >= {2:.2f}) within {3:.2f} s".format(
                len(violations), min_brake, min_steer, lookahead
            ),
            witness=witness, intervals=violations,
        )
    if undecidable:
        return _result(
            P4_ID, pid, CheckStatus.UNKNOWN, params,
            "{0} of {1} detected conflict(s) could not be decided ({2})".format(
                len(undecidable), len(conflicts), undecidable[0]["why"]
            ),
            witness=witness,
        )
    return _result(
        P4_ID, pid, CheckStatus.PASS, params,
        "every one of the {0} detected conflict(s) was followed by an evasive "
        "response within {1:.2f} s".format(len(conflicts), lookahead),
        witness=witness,
    )


P4_CONFLICT_NO_RESPONSE = Property(
    property_id=P4_ID,
    description=(
        "A conflict this participant itself detected (predicted path conflict or "
        "conflict-region entry) must be followed by an evasive response -- braking "
        "or steering -- within lookahead_s, or before the outcome if one occurs "
        "sooner."
    ),
    formal=(
        "G( (predicted_path_conflict | conflict_region_entry) -> "
        "F[0,lookahead_s] (brake >= min_evasive_brake | |steer| >= min_evasive_steer) )"
    ),
    scope=Provenance.LOCAL,
    evaluate=_evaluate_p4,
)


# ---------------------------------------------------------------------------
# Oracle (privileged) properties -- evaluation only, never inference
# ---------------------------------------------------------------------------

O1_ID = "O1_signal_compliance"
O2_ID = "O2_right_of_way"

#: Normalised signal strings that count as "must not enter".
_RED_STATES: Tuple[str, ...] = ("red",)


def oracle_participant_ids(oracle_trace: Dict[str, Any]) -> List[str]:
    """Sorted actor ids mentioned by an oracle trace mapping.

    Reads the declared ``participants`` block when present and otherwise unions
    the per-sample ``actors`` keys, so a trace written by any oracle
    implementation that follows the documented shape can be checked.
    """
    declared = oracle_trace.get("participants")
    if isinstance(declared, dict) and declared:
        return sorted(str(k) for k in declared.keys())
    if isinstance(declared, (list, tuple)) and declared:
        return sorted(str(k) for k in declared)
    found = set()
    for sample in _oracle_samples(oracle_trace):
        actors = sample.get("actors")
        if isinstance(actors, dict):
            found.update(str(k) for k in actors.keys())
    return sorted(found)


def _oracle_samples(oracle_trace: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Per-instant records of an oracle trace, sorted by time.

    Accepts ``samples`` or ``trace`` as the container key; anything else is
    treated as "no samples" and drives the properties to ``UNKNOWN``.
    """
    raw = oracle_trace.get("samples")
    if raw is None:
        raw = oracle_trace.get("trace")
    if not isinstance(raw, (list, tuple)):
        return []
    out = [dict(s) for s in raw if isinstance(s, dict) and "t" in s]
    out.sort(key=lambda s: float(s["t"]))
    return out


def _actor_series(
    samples: Sequence[Dict[str, Any]], participant_id: str
) -> List[Tuple[float, Dict[str, Any]]]:
    """``(t, state)`` pairs for one actor, skipping instants it is absent from."""
    out: List[Tuple[float, Dict[str, Any]]] = []
    for s in samples:
        actors = s.get("actors")
        if not isinstance(actors, dict):
            continue
        state = actors.get(participant_id)
        if isinstance(state, dict):
            out.append((float(s["t"]), state))
    return out


def _as_bool(value: Any) -> Optional[bool]:
    """Strict optional-bool coercion; unrecognised values are 'not stated'."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        low = value.strip().lower()
        if low in ("true", "yes", "1"):
            return True
        if low in ("false", "no", "0"):
            return False
    return None


def _oracle_target_ids(
    oracle_trace: Dict[str, Any], context: Dict[str, Any]
) -> Tuple[List[str], str]:
    """Which actors to evaluate, and the id to stamp on the combined result."""
    requested = context.get("participant_id")
    if requested:
        return ([str(requested)], str(requested))
    return (oracle_participant_ids(oracle_trace), "*")


def _evaluate_o1(
    oracle_trace: Dict[str, Any], cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( junction_entry -> signal_at_entry != red )`` on the privileged trace.

    Needs two fields no onboard sensor of ours produces: the state of the signal
    facing the actor and whether the actor is inside the junction. Absent either,
    the verdict is ``UNKNOWN`` -- the oracle is privileged, not omniscient.
    """
    raw_red = cfg.get("checking.O1_signal_compliance.red_states", list(_RED_STATES))
    if isinstance(raw_red, str):
        raw_red = [raw_red]
    if not isinstance(raw_red, (list, tuple)) or not raw_red:
        raise ValueError(
            "checking.O1_signal_compliance.red_states must be a non-empty list of "
            "signal state names, got {0!r}".format(raw_red)
        )
    params: Dict[str, Any] = {
        "min_entry_speed_mps": float(
            cfg.get("checking.O1_signal_compliance.min_entry_speed_mps", 0.5)
        ),
        "red_states": [str(s) for s in raw_red],
        "fields": ["in_junction", "signal_state", "speed"],
    }
    samples = _oracle_samples(oracle_trace)
    pids, result_pid = _oracle_target_ids(oracle_trace, context)

    if not samples:
        return _result(
            O1_ID, result_pid, CheckStatus.UNKNOWN, params,
            "the oracle trace carries no 'samples' block",
            scope=Provenance.ORACLE,
        )
    if not pids:
        return _result(
            O1_ID, result_pid, CheckStatus.UNKNOWN, params,
            "the oracle trace names no actors",
            scope=Provenance.ORACLE,
        )

    red = tuple(str(s).strip().lower() for s in params["red_states"])
    min_speed = params["min_entry_speed_mps"]

    statuses: List[CheckStatus] = []
    intervals: List[Tuple[float, float]] = []
    witness: Dict[str, Any] = {"per_participant": {}}
    reasons: List[str] = []

    for pid in pids:
        series = _actor_series(samples, pid)
        usable = [
            (t, st)
            for t, st in series
            if _as_bool(st.get("in_junction")) is not None and "signal_state" in st
        ]
        if not usable:
            statuses.append(CheckStatus.UNKNOWN)
            witness["per_participant"][pid] = {"status": CheckStatus.UNKNOWN.value,
                                               "why": "no in_junction/signal_state fields"}
            reasons.append(
                "{0}: the privileged fields in_junction/signal_state are absent".format(pid)
            )
            continue

        entries: List[Dict[str, Any]] = []
        violations: List[Tuple[float, float]] = []
        prev_in = _as_bool(usable[0][1].get("in_junction"))
        for idx in range(1, len(usable)):
            t, st = usable[idx]
            cur_in = _as_bool(st.get("in_junction"))
            if cur_in and not prev_in:
                signal = str(st.get("signal_state", "")).strip().lower()
                speed = st.get("speed")
                speed_f = float(speed) if speed is not None else None
                entries.append({"t_s": t, "signal_at_entry": signal, "speed_mps": speed_f})
                moving = speed_f is None or speed_f >= min_speed
                if signal in red and moving:
                    violations.append((float(usable[idx - 1][0]), float(t)))
            prev_in = cur_in

        if not entries:
            statuses.append(CheckStatus.UNKNOWN)
            witness["per_participant"][pid] = {"status": CheckStatus.UNKNOWN.value,
                                               "why": "no junction entry observed"}
            reasons.append("{0}: never entered a signalised junction".format(pid))
            continue
        if violations:
            statuses.append(CheckStatus.FAIL)
            intervals.extend(violations)
            witness["per_participant"][pid] = {
                "status": CheckStatus.FAIL.value,
                "entries": entries,
                "n_violations": len(violations),
            }
            reasons.append(
                "{0}: entered the junction on a red signal {1} time(s)".format(
                    pid, len(violations)
                )
            )
        else:
            statuses.append(CheckStatus.PASS)
            witness["per_participant"][pid] = {
                "status": CheckStatus.PASS.value,
                "entries": entries,
            }
            reasons.append("{0}: every junction entry was on a permissive signal".format(pid))

    status = combine_statuses(statuses)
    return _result(
        O1_ID, result_pid, status, params, "; ".join(reasons),
        witness=witness, intervals=intervals if status is CheckStatus.FAIL else None,
        scope=Provenance.ORACLE,
    )


O1_SIGNAL_COMPLIANCE = Property(
    property_id=O1_ID,
    description=(
        "PRIVILEGED: an actor must not enter a junction while the traffic signal "
        "facing it is red. Requires ground-truth signal state, which no onboard "
        "sensor in this project observes."
    ),
    formal="G( junction_entry -> signal_at_entry != red )",
    scope=Provenance.ORACLE,
    evaluate=_evaluate_o1,
)


def _evaluate_o2(
    oracle_trace: Dict[str, Any], cfg: Config, context: Dict[str, Any]
) -> PropertyResult:
    """``G( in_junction & !has_right_of_way -> !exists q: in_junction(q) & has_right_of_way(q) )``.

    A yielding actor sharing the junction with a priority actor is a right-of-way
    violation. The overlap must last at least ``min_overlap_s`` so that a single
    sample of geometric coincidence at the boundary is not reported as a breach.
    """
    params: Dict[str, Any] = {
        "min_overlap_s": float(cfg.get("checking.O2_right_of_way.min_overlap_s", 0.1)),
        "fields": ["in_junction", "has_right_of_way"],
    }
    samples = _oracle_samples(oracle_trace)
    pids, result_pid = _oracle_target_ids(oracle_trace, context)
    all_ids = oracle_participant_ids(oracle_trace)

    if not samples:
        return _result(
            O2_ID, result_pid, CheckStatus.UNKNOWN, params,
            "the oracle trace carries no 'samples' block",
            scope=Provenance.ORACLE,
        )
    if len(all_ids) < 2:
        return _result(
            O2_ID, result_pid, CheckStatus.UNKNOWN, params,
            "right of way needs at least two actors; the oracle trace names {0}".format(
                len(all_ids)
            ),
            scope=Provenance.ORACLE,
        )

    min_overlap = params["min_overlap_s"]
    statuses: List[CheckStatus] = []
    intervals: List[Tuple[float, float]] = []
    witness: Dict[str, Any] = {"per_participant": {}}
    reasons: List[str] = []

    for pid in pids:
        series = _actor_series(samples, pid)
        usable = [
            (t, st)
            for t, st in series
            if _as_bool(st.get("in_junction")) is not None
            and _as_bool(st.get("has_right_of_way")) is not None
        ]
        if not usable:
            statuses.append(CheckStatus.UNKNOWN)
            witness["per_participant"][pid] = {
                "status": CheckStatus.UNKNOWN.value,
                "why": "no in_junction/has_right_of_way fields",
            }
            reasons.append(
                "{0}: the privileged fields in_junction/has_right_of_way are absent".format(pid)
            )
            continue

        yielding = [
            t
            for t, st in usable
            if _as_bool(st.get("in_junction")) and not _as_bool(st.get("has_right_of_way"))
        ]
        if not yielding:
            statuses.append(CheckStatus.UNKNOWN)
            witness["per_participant"][pid] = {
                "status": CheckStatus.UNKNOWN.value,
                "why": "never occupied a junction while obliged to yield",
            }
            reasons.append("{0}: never had to yield inside a junction".format(pid))
            continue

        yielding_set = set(round(t, 9) for t in yielding)
        conflicts: Dict[str, List[float]] = {}
        for other in all_ids:
            if other == pid:
                continue
            for t, st in _actor_series(samples, other):
                if round(t, 9) not in yielding_set:
                    continue
                if _as_bool(st.get("in_junction")) and _as_bool(st.get("has_right_of_way")):
                    conflicts.setdefault(other, []).append(float(t))

        breaches: List[Tuple[float, float]] = []
        for other, times in sorted(conflicts.items()):
            times.sort()
            span = times[-1] - times[0]
            if span >= min_overlap - _T_EPS:
                breaches.append((times[0], times[-1]))

        if breaches:
            statuses.append(CheckStatus.FAIL)
            intervals.extend(breaches)
            witness["per_participant"][pid] = {
                "status": CheckStatus.FAIL.value,
                "priority_participants": sorted(conflicts.keys()),
                "n_overlap_samples": sum(len(v) for v in conflicts.values()),
            }
            reasons.append(
                "{0}: occupied the junction together with priority actor(s) {1}".format(
                    pid, ", ".join(sorted(conflicts.keys()))
                )
            )
        else:
            statuses.append(CheckStatus.PASS)
            witness["per_participant"][pid] = {
                "status": CheckStatus.PASS.value,
                "priority_participants": [],
            }
            reasons.append(
                "{0}: yielded -- no priority actor shared the junction".format(pid)
            )

    status = combine_statuses(statuses)
    return _result(
        O2_ID, result_pid, status, params, "; ".join(reasons),
        witness=witness, intervals=intervals if status is CheckStatus.FAIL else None,
        scope=Provenance.ORACLE,
    )


O2_RIGHT_OF_WAY = Property(
    property_id=O2_ID,
    description=(
        "PRIVILEGED: an actor obliged to yield must not share a junction with an "
        "actor that has right of way. Requires ground-truth priority assignment."
    ),
    formal=(
        "G( in_junction & !has_right_of_way -> "
        "!(exists q != self: in_junction(q) & has_right_of_way(q)) )"
    ),
    scope=Provenance.ORACLE,
    evaluate=_evaluate_o2,
)


# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

#: Properties decidable from a single participant's own onboard evidence.
LOCAL_PROPERTIES: Tuple[Property, ...] = (
    P1_BRAKE_RESPONSE,
    P2_NO_THROTTLE_CLOSING,
    P3_POST_COLLISION_STOP,
    P4_CONFLICT_NO_RESPONSE,
)

#: Privileged properties. Evaluation only -- never an input to inference.
ORACLE_PROPERTIES: Tuple[Property, ...] = (
    O1_SIGNAL_COMPLIANCE,
    O2_RIGHT_OF_WAY,
)


def property_by_id(property_id: str) -> Property:
    """Look up a registered property, failing loudly on an unknown id."""
    for prop in LOCAL_PROPERTIES + ORACLE_PROPERTIES:
        if prop.property_id == property_id:
            return prop
    raise KeyError(
        "unknown property id {0!r} (known: {1})".format(
            property_id,
            ", ".join(p.property_id for p in LOCAL_PROPERTIES + ORACLE_PROPERTIES),
        )
    )
