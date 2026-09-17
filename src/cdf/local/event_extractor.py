"""Turn a participant's own time series into typed, discrete, local events.

This is the step that converts continuous onboard evidence into the nodes of a
local event graph. Three design constraints shape it:

**Only observable language.** Every event type names something the vehicle's own
sensors can witness: a brake command, a closing range, a lateral drift, an
inferred path conflict. Nothing here is allowed to name a lane, a junction, a
signal phase or another actor's identity -- those are privileged facts the local
layer must not be able to express.

**Thresholds are intervals, not instants.** A raw threshold test on a noisy
signal fires on every sample that wobbles across the line and would bury the
graph in near-duplicate nodes. Every threshold here is therefore a Schmitt
trigger: an episode *opens* at the enter threshold and only *closes* once the
signal has retreated past ``events.hysteresis_ratio`` times that threshold. The
episode's extreme value fixes ``t_peak``; its span fixes ``t_start``/``t_end``.
Episodes shorter than ``events.min_duration_s`` are dropped as chatter, and two
episodes of the same ``(type, subject)`` whose peaks fall within
``events.min_separation_s`` are merged into a single wider event.

**Every event carries its provenance.** Each event points back at the raw records
that support it (``Evidence``), names the sensors involved, and carries a
confidence that propagates the tracker's own confidence for radar-derived
claims. Downstream causal reasoning weights edges by these numbers, so an event
that rests on a weak track must not look as solid as a recorded brake command.

Hysteresis direction
--------------------
``events.hysteresis_ratio`` scales the enter threshold *towards the non-event
region*. For a magnitude threshold crossed from below (acceleration >= 1.5) or a
negative threshold crossed from above (deceleration <= -1.8) that is
``enter * ratio``. For a positive threshold crossed from above (TTC <= 3.0 s)
the non-event region lies at larger values, so the release threshold is
``enter / ratio`` instead. Both cases are handled by
:func:`_release_threshold`.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence
from ..common.geometry import distance
from ..common.schemas import (
    Event,
    EventType,
    Evidence,
    Provenance,
    TriggerKind,
    make_event_id,
)
from .indicators import (
    OwnIndicators,
    TrackIndicators,
    compute_own_indicators,
    compute_track_indicators,
    cumulative_heading_change,
    net_heading_change,
)

__all__ = ["EventExtractor"]


# ---------------------------------------------------------------------------
# Episode detection with hysteresis
# ---------------------------------------------------------------------------


@dataclass
class _Episode:
    """One contiguous stretch during which a threshold condition held."""

    t_start: float
    t_end: float
    t_peak: float
    peak_value: float
    i_start: int
    i_end: int
    i_peak: int

    @property
    def duration(self) -> float:
        return float(self.t_end) - float(self.t_start)


def _release_threshold(enter: float, mode: str, ratio: float) -> float:
    """Hysteresis release threshold for ``enter`` under comparison ``mode``.

    The release threshold always sits *between* the enter threshold and the
    non-event region, so an active episode survives a signal that retreats only
    slightly. See the module docstring for why the sign handling is asymmetric.
    """
    if not 0.0 < ratio <= 1.0:
        raise ValueError(
            "events.hysteresis_ratio must lie in (0, 1], got {0}".format(ratio)
        )
    if enter == 0.0:
        return 0.0
    if (mode == "above") == (enter > 0.0):
        return enter * ratio
    return enter / ratio


def _find_episodes(
    times: Sequence[float],
    values: Sequence[Optional[float]],
    enter: float,
    mode: str,
    ratio: float,
    min_duration_s: float,
) -> List[_Episode]:
    """Extract hysteresis-gated episodes from a sampled signal.

    ``values`` may contain ``None`` for samples where the quantity is undefined
    (an undefined TTC, for instance). ``None`` is treated as "condition not met",
    which closes an open episode rather than silently extending it.
    """
    if mode not in ("above", "below"):
        raise ValueError("episode mode must be 'above' or 'below', got {0!r}".format(mode))
    if len(times) != len(values):
        raise ValueError(
            "signal length {0} does not match time base {1}".format(len(values), len(times))
        )

    release = _release_threshold(enter, mode, ratio)
    above = mode == "above"

    out: List[_Episode] = []
    open_start: Optional[int] = None
    last_in: int = -1
    peak_i: int = -1
    peak_v: float = 0.0

    for i, raw in enumerate(values):
        v = None if raw is None else float(raw)
        if open_start is None:
            if v is None:
                continue
            if (v >= enter) if above else (v <= enter):
                open_start = i
                last_in = i
                peak_i = i
                peak_v = v
            continue

        holds = v is not None and ((v >= release) if above else (v <= release))
        if holds and v is not None:
            last_in = i
            if (v > peak_v) if above else (v < peak_v):
                peak_i, peak_v = i, v
        else:
            out.append(
                _Episode(
                    t_start=float(times[open_start]),
                    t_end=float(times[last_in]),
                    t_peak=float(times[peak_i]),
                    peak_value=peak_v,
                    i_start=open_start,
                    i_end=last_in,
                    i_peak=peak_i,
                )
            )
            open_start = None

    if open_start is not None:
        out.append(
            _Episode(
                t_start=float(times[open_start]),
                t_end=float(times[last_in]),
                t_peak=float(times[peak_i]),
                peak_value=peak_v,
                i_start=open_start,
                i_end=last_in,
                i_peak=peak_i,
            )
        )

    return [e for e in out if e.duration >= float(min_duration_s) - 1e-9]


def _rolling_max(
    times: Sequence[float], values: Sequence[float], window_s: float
) -> List[float]:
    """Maximum of ``values`` over the trailing ``window_s`` at each sample."""
    out: List[float] = []
    for i in range(len(times)):
        j = bisect.bisect_left(times, float(times[i]) - float(window_s))
        out.append(max(float(v) for v in values[j : i + 1]))
    return out


# ---------------------------------------------------------------------------
# Candidate events (pre-merge)
# ---------------------------------------------------------------------------


@dataclass
class _Candidate:
    """An event before debouncing and id assignment.

    ``peak_value`` plus ``extreme_is_max`` let the merge step decide which of two
    near-simultaneous detections is the more extreme one to keep.
    """

    event_type: EventType
    subject: Optional[str]
    t_start: float
    t_peak: float
    t_end: Optional[float]
    peak_value: float
    extreme_is_max: bool
    values: Dict[str, float] = field(default_factory=dict)
    confidence: float = 1.0
    evidence: List[Evidence] = field(default_factory=list)
    source_sensors: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class EventExtractor:
    """Convert one participant's own evidence into typed local events.

    The extractor is stateless between calls: :meth:`extract` recomputes the
    indicator series it needs, so the same evidence always yields byte-identical
    events for a given configuration.
    """

    def __init__(self, cfg: Config) -> None:
        self._cfg = cfg
        self._min_sep = float(cfg.get("events.min_separation_s", 0.75))
        self._min_dur = float(cfg.get("events.min_duration_s", 0.10))
        self._ratio = float(cfg.get("events.hysteresis_ratio", 0.75))
        if not 0.0 < self._ratio <= 1.0:
            raise ValueError(
                "events.hysteresis_ratio must lie in (0, 1], got {0}".format(self._ratio)
            )
        if self._min_sep < 0.0 or self._min_dur < 0.0:
            raise ValueError(
                "events.min_separation_s and events.min_duration_s must be non-negative"
            )

    # -- public API -------------------------------------------------------

    def extract(self, ev: ParticipantEvidence) -> List[Event]:
        """Extract every local event supported by ``ev``.

        Derived outcome events (a near miss inferred from an unresolved critical
        TTC, a post-impact stop) are built in a second pass, from the *already
        debounced* primary events, so that they can cite a stable event id.
        """
        own = compute_own_indicators(ev, self._cfg)
        tracks = compute_track_indicators(ev, self._cfg)

        candidates: List[_Candidate] = []
        candidates.extend(self._own_candidates(ev, own))
        candidates.extend(self._track_candidates(ev, tracks))
        candidates.extend(self._trigger_candidates(ev))

        merged = self._merge(candidates)
        merged = self._merge(merged + self._derived_candidates(ev, own, merged))

        events = [self._to_event(ev.participant_id, c) for c in merged]
        events.sort(
            key=lambda e: (
                float(e.t_peak),
                float(e.t_start),
                e.event_type.value,
                e.subject or "",
                e.event_id,
            )
        )

        seen: Dict[str, Event] = {}
        for e in events:
            if e.event_id in seen:
                raise ValueError(
                    "duplicate local event id {0} ({1} vs {2})".format(
                        e.event_id, seen[e.event_id].event_type.value, e.event_type.value
                    )
                )
            seen[e.event_id] = e
        return events

    # -- own behaviour ----------------------------------------------------

    def _own_candidates(
        self, ev: ParticipantEvidence, own: List[OwnIndicators]
    ) -> List[_Candidate]:
        """Events derived from own telemetry and own actuator commands."""
        if not own:
            return []
        cfg = self._cfg
        pid = ev.participant_id
        times = [o.t for o in own]
        out: List[_Candidate] = []

        speed = [o.speed for o in own]
        accel_long = [o.accel_long for o in own]
        throttle = [o.throttle for o in own]
        brake = [o.brake for o in own]
        steer = [o.steer for o in own]
        abs_steer = [abs(v) for v in steer]
        heading_change = [o.heading_change_deg for o in own]
        lateral = [o.lateral_offset_m for o in own]

        # --- VEHICLE_STARTED: the first sustained departure from standstill.
        #     Unlike the threshold events around it, this one claims a *transition*
        #     ("the vehicle pulled away"), so it may only be asserted when the
        #     recording actually witnessed the standstill it departed from. The
        #     recorder is a rolling buffer, so a trace routinely opens with the
        #     vehicle already in motion; an episode that is already open on the
        #     first sample is evidence that the recording started, not that the
        #     vehicle did, and reporting it would manufacture a departure that the
        #     downstream causal rules then blame for the closing range. The first
        #     *witnessed* departure is still reported, so a trace that opens in
        #     motion, stops and pulls away again keeps the departure it observed.
        start_eps = _find_episodes(
            times,
            speed,
            float(cfg.get("events.vehicle_started.speed_mps", 0.8)),
            "above",
            self._ratio,
            self._min_dur,
        )
        witnessed = [e for e in start_eps if e.i_start > 0]
        if witnessed:
            first = witnessed[0]
            out.append(
                _Candidate(
                    event_type=EventType.VEHICLE_STARTED,
                    subject=None,
                    t_start=first.t_start,
                    t_peak=first.t_start,
                    t_end=first.t_start,
                    peak_value=speed[first.i_start],
                    extreme_is_max=True,
                    values={"speed_mps": float(speed[first.i_start])},
                    confidence=1.0,
                    evidence=[
                        Evidence(
                            kind="telemetry",
                            ref=pid,
                            t_start=first.t_start,
                            t_end=first.t_start,
                        )
                    ],
                    source_sensors=["telemetry"],
                )
            )

        # --- longitudinal dynamics (own telemetry).
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                accel_long,
                EventType.ACCELERATION,
                float(cfg.get("events.acceleration.enter_mps2", 1.5)),
                "above",
                "accel_long_mps2",
                "telemetry",
                ["telemetry"],
            )
        )
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                accel_long,
                EventType.DECELERATION,
                float(cfg.get("events.deceleration.enter_mps2", -1.8)),
                "below",
                "accel_long_mps2",
                "telemetry",
                ["telemetry"],
            )
        )
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                accel_long,
                EventType.HARD_DECELERATION,
                float(cfg.get("events.hard_deceleration.enter_mps2", -4.5)),
                "below",
                "accel_long_mps2",
                "telemetry",
                ["telemetry"],
            )
        )

        # --- actuator commands (own controls).
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                brake,
                EventType.BRAKE_ONSET,
                float(cfg.get("events.brake_onset.brake_cmd", 0.12)),
                "above",
                "brake_cmd",
                "controls",
                ["controls"],
            )
        )
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                brake,
                EventType.HARD_BRAKE,
                float(cfg.get("events.hard_brake.brake_cmd", 0.65)),
                "above",
                "brake_cmd",
                "controls",
                ["controls"],
            )
        )
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                throttle,
                EventType.THROTTLE_ONSET,
                float(cfg.get("events.throttle_onset.throttle_cmd", 0.25)),
                "above",
                "throttle_cmd",
                "controls",
                ["controls"],
            )
        )
        steer_thr = float(cfg.get("events.steer_onset.steer_cmd", 0.14))
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                abs_steer,
                EventType.STEER_ONSET,
                steer_thr,
                "above",
                "abs_steer_cmd",
                "controls",
                ["controls"],
                extra_values=lambda i: {"steer_cmd": float(steer[i])},
            )
        )

        # --- heading manoeuvres (own pose history).
        out.extend(
            self._threshold_candidates(
                pid,
                times,
                heading_change,
                EventType.SIGNIFICANT_HEADING_CHANGE,
                float(cfg.get("events.heading_change.total_deg", 12.0)),
                "above",
                "heading_change_deg",
                "telemetry",
                ["telemetry"],
            )
        )

        # --- LANE_CHANGE_LIKE_MANEUVER.
        # A lateral displacement alone is ambiguous: a turn produces a far larger
        # one. Three further conditions, all from own pose and own controls,
        # separate the two without a map:
        #   * the window must not contain the total heading change a turn needs
        #     (``max_heading_change_deg``);
        #   * the heading excursion must be an *out-and-back*: a lane change ends
        #     on the heading it began with, so its net change is a small fraction
        #     of its cumulative change, whereas a turn spends all of its
        #     cumulative change on a net change. Without this a window that
        #     catches only the tail of a turn plus the straight run after it looks
        #     exactly like a lane change;
        #   * the driver must actually have steered inside the window, which rules
        #     out sideways displacement caused by road curvature alone.
        lc_window = float(cfg.get("events.lane_change_like.window_s", 3.0))
        max_turn = float(cfg.get("events.lane_change_like.max_heading_change_deg", 45.0))
        net_ratio = float(cfg.get("events.lane_change_like.max_net_heading_ratio", 0.5))
        lat_thr = float(cfg.get("events.lane_change_like.lateral_offset_m", 1.8))
        yaw_series = [float(s.yaw) for s in ev.telemetry]
        if len(yaw_series) != len(times):  # pragma: no cover - built in lockstep
            raise ValueError(
                "own indicator series ({0}) does not match telemetry ({1})".format(
                    len(times), len(yaw_series)
                )
            )
        heading_change_lc = cumulative_heading_change(times, yaw_series, lc_window)
        heading_net_lc = net_heading_change(times, yaw_series, lc_window)
        steer_window_max = _rolling_max(times, abs_steer, lc_window)
        lane_signal = [
            abs(lateral[i])
            if (
                heading_change_lc[i] <= max_turn
                and heading_net_lc[i] <= net_ratio * heading_change_lc[i] + 1e-9
                and steer_window_max[i] >= steer_thr
            )
            else 0.0
            for i in range(len(times))
        ]
        for episode in _find_episodes(
            times, lane_signal, lat_thr, "above", self._ratio, self._min_dur
        ):
            out.append(
                _Candidate(
                    event_type=EventType.LANE_CHANGE_LIKE_MANEUVER,
                    subject=None,
                    t_start=episode.t_start,
                    t_peak=episode.t_peak,
                    t_end=episode.t_end,
                    peak_value=episode.peak_value,
                    extreme_is_max=True,
                    values={
                        "lateral_offset_m": float(lateral[episode.i_peak]),
                        "abs_lateral_offset_m": float(episode.peak_value),
                        "heading_change_deg": float(heading_change_lc[episode.i_peak]),
                        "net_heading_change_deg": float(heading_net_lc[episode.i_peak]),
                        "peak_steer_cmd": float(steer_window_max[episode.i_peak]),
                    },
                    confidence=1.0,
                    evidence=[
                        Evidence(
                            kind="telemetry",
                            ref=pid,
                            t_start=episode.t_start,
                            t_end=episode.t_end,
                        ),
                        Evidence(
                            kind="controls",
                            ref=pid,
                            t_start=episode.t_start,
                            t_end=episode.t_end,
                        ),
                    ],
                    source_sensors=["telemetry", "controls"],
                )
            )

        return out

    def _threshold_candidates(
        self,
        pid: str,
        times: Sequence[float],
        values: Sequence[Optional[float]],
        event_type: EventType,
        enter: float,
        mode: str,
        value_key: str,
        evidence_kind: str,
        sensors: List[str],
        subject: Optional[str] = None,
        evidence_ref: Optional[str] = None,
        min_duration_s: Optional[float] = None,
        confidence_fn: Optional[Callable[[_Episode], float]] = None,
        extra_values: Optional[Callable[[int], Dict[str, float]]] = None,
    ) -> List[_Candidate]:
        """Build candidates for one simple threshold signal.

        Factored out because a dozen event types differ only in threshold, sign
        and provenance; writing each one by hand would invite them to drift apart.
        """
        min_dur = self._min_dur if min_duration_s is None else float(min_duration_s)
        episodes = _find_episodes(times, values, enter, mode, self._ratio, min_dur)
        out: List[_Candidate] = []
        for episode in episodes:
            vals: Dict[str, float] = {value_key: float(episode.peak_value)}
            if extra_values is not None:
                vals.update(extra_values(episode.i_peak))
            out.append(
                _Candidate(
                    event_type=event_type,
                    subject=subject,
                    t_start=episode.t_start,
                    t_peak=episode.t_peak,
                    t_end=episode.t_end,
                    peak_value=float(episode.peak_value),
                    extreme_is_max=(mode == "above"),
                    values=vals,
                    confidence=1.0 if confidence_fn is None else confidence_fn(episode),
                    evidence=[
                        Evidence(
                            kind=evidence_kind,
                            ref=evidence_ref if evidence_ref is not None else pid,
                            t_start=episode.t_start,
                            t_end=episode.t_end,
                        )
                    ],
                    source_sensors=list(sensors),
                )
            )
        return out

    # -- radar / interaction ----------------------------------------------

    def _track_candidates(
        self, ev: ParticipantEvidence, tracks: Dict[str, List[TrackIndicators]]
    ) -> List[_Candidate]:
        """Events derived from the participant's own radar tracks."""
        cfg = self._cfg
        pid = ev.participant_id
        out: List[_Candidate] = []
        if not tracks:
            return out

        raw_by_id = ev.tracks_by_id()
        default_conf = float(cfg.get("events.radar.default_confidence", 0.6))
        run_end = self._run_end(ev, tracks)
        lost_gap = self._track_lost_gap(ev)

        for track_id in sorted(tracks.keys()):
            ti = tracks[track_id]
            if not ti:
                continue
            raw = raw_by_id.get(track_id, [])
            if len(raw) != len(ti):  # pragma: no cover - built from the same samples
                raise ValueError(
                    "track {0}: {1} indicator samples for {2} raw samples".format(
                        track_id, len(ti), len(raw)
                    )
                )
            track_conf = [float(s.confidence) for s in raw]

            def _conf(episode: _Episode, _c: List[float] = track_conf) -> float:
                """Mean tracker confidence over the episode, or the configured default."""
                window = _c[episode.i_start : episode.i_end + 1]
                if not window:
                    return default_conf
                mean = sum(window) / float(len(window))
                return mean if mean > 0.0 else default_conf

            times = [s.t for s in ti]
            closing = [-s.range_rate for s in ti]
            ttc: List[Optional[float]] = [s.ttc for s in ti]
            lateral = [s.lateral_offset_m for s in ti]
            lateral_rate = [s.lateral_rate_mps for s in ti]
            longitudinal = [s.longitudinal_m for s in ti]
            target_accel = [s.target_accel_long for s in ti]
            conflict = [s.conflict_score for s in ti]

            # --- track lifecycle. These are instantaneous by nature: a track
            #     appearing is a single observation, not an interval.
            out.append(
                _Candidate(
                    event_type=EventType.RADAR_TRACK_APPEARED,
                    subject=track_id,
                    t_start=ti[0].t,
                    t_peak=ti[0].t,
                    t_end=ti[0].t,
                    peak_value=float(ti[0].range_m),
                    extreme_is_max=False,
                    values={
                        "range_m": float(ti[0].range_m),
                        "longitudinal_m": float(ti[0].longitudinal_m),
                        "lateral_offset_m": float(ti[0].lateral_offset_m),
                    },
                    confidence=track_conf[0] if track_conf[0] > 0.0 else default_conf,
                    evidence=[
                        Evidence(kind="track", ref=track_id, t_start=ti[0].t, t_end=ti[0].t)
                    ],
                    source_sensors=["radar"],
                )
            )
            # A track whose last sample sits at the end of the recording was not
            # lost -- the recording stopped. Only a genuine gap counts.
            if run_end is not None and (run_end - ti[-1].t) >= lost_gap:
                out.append(
                    _Candidate(
                        event_type=EventType.RADAR_TRACK_LOST,
                        subject=track_id,
                        t_start=ti[-1].t,
                        t_peak=ti[-1].t,
                        t_end=ti[-1].t,
                        peak_value=float(ti[-1].range_m),
                        extreme_is_max=True,
                        values={
                            "range_m": float(ti[-1].range_m),
                            "track_duration_s": float(ti[-1].t - ti[0].t),
                        },
                        confidence=track_conf[-1] if track_conf[-1] > 0.0 else default_conf,
                        evidence=[
                            Evidence(
                                kind="track", ref=track_id, t_start=ti[-1].t, t_end=ti[-1].t
                            )
                        ],
                        source_sensors=["radar"],
                    )
                )

            # --- closing geometry.
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    closing,
                    EventType.RANGE_DECREASING,
                    float(cfg.get("events.radar.range_decreasing.min_rate_mps", 1.0)),
                    "above",
                    "closing_rate_mps",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    min_duration_s=float(
                        cfg.get("events.radar.range_decreasing.min_duration_s", 0.6)
                    ),
                    confidence_fn=_conf,
                )
            )
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    closing,
                    EventType.RAPID_CLOSING,
                    float(cfg.get("events.radar.rapid_closing.min_rate_mps", 6.0)),
                    "above",
                    "closing_rate_mps",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                )
            )
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    ttc,
                    EventType.LOW_TTC,
                    float(cfg.get("events.radar.low_ttc.ttc_s", 3.0)),
                    "below",
                    "ttc_s",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                )
            )
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    ttc,
                    EventType.CRITICAL_TTC,
                    float(cfg.get("events.radar.critical_ttc.ttc_s", 1.6)),
                    "below",
                    "ttc_s",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                )
            )

            # --- lateral behaviour of the target.
            max_cross_range = float(
                cfg.get("events.radar.lateral_crossing.max_range_m", 45.0)
            )
            cross_signal = [
                abs(lateral_rate[i]) if ti[i].range_m <= max_cross_range else 0.0
                for i in range(len(ti))
            ]
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    cross_signal,
                    EventType.LATERAL_CROSSING,
                    float(
                        cfg.get("events.radar.lateral_crossing.min_lateral_rate_mps", 1.8)
                    ),
                    "above",
                    "lateral_rate_mps",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                    extra_values=lambda i: {
                        "range_m": float(ti[i].range_m),
                        "lateral_offset_m": float(lateral[i]),
                    },
                )
            )
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    self._cut_in_signal(times, lateral, longitudinal),
                    EventType.CUT_IN_LIKE_MOTION,
                    float(cfg.get("events.radar.cut_in_like.lateral_closing_mps", 1.2)),
                    "above",
                    "lateral_closing_mps",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                    extra_values=lambda i: {
                        "lateral_offset_m": float(lateral[i]),
                        "longitudinal_m": float(longitudinal[i]),
                    },
                )
            )

            # --- inferred target dynamics.
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    target_accel,
                    EventType.TARGET_DECELERATION,
                    -float(
                        cfg.get("events.radar.target_deceleration.min_decel_mps2", 2.5)
                    ),
                    "below",
                    "target_accel_long_mps2",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=_conf,
                )
            )

            # --- inferred path conflict. The score *is* the confidence here, so
            #     it is used directly rather than the tracker's own number.
            min_conflict = float(
                cfg.get("events.radar.path_conflict.min_confidence", 0.35)
            )
            out.extend(
                self._threshold_candidates(
                    pid,
                    times,
                    conflict,
                    EventType.PREDICTED_PATH_CONFLICT,
                    min_conflict,
                    "above",
                    "conflict_score",
                    "track",
                    ["radar"],
                    subject=track_id,
                    evidence_ref=track_id,
                    confidence_fn=lambda e: float(e.peak_value),
                    extra_values=lambda i: self._conflict_point_values(ti[i]),
                )
            )
            out.extend(self._conflict_region_candidates(ev, track_id, ti, _conf))

        return out

    def _cut_in_signal(
        self,
        times: Sequence[float],
        lateral: Sequence[float],
        longitudinal: Sequence[float],
    ) -> List[float]:
        """Rate at which a target ahead is closing on our own path centre-line.

        A cut-in is not merely lateral motion: it is lateral motion *towards* the
        observer's own longitudinal axis, by a target that is ahead and already
        near that axis. The signal is the average reduction of ``|rel_y|`` over
        ``events.radar.cut_in_like.window_s``; averaging over the window rather
        than differentiating pointwise keeps a single noisy sample from inventing
        a cut-in. Samples whose window is less than half-covered report 0.0
        because their denominator would be dominated by noise.
        """
        cfg = self._cfg
        window = float(cfg.get("events.radar.cut_in_like.window_s", 2.5))
        max_off = float(cfg.get("events.radar.cut_in_like.max_lateral_offset_m", 4.5))
        min_long = float(cfg.get("events.radar.cut_in_like.min_longitudinal_m", 4.0))

        out: List[float] = []
        for i in range(len(times)):
            gated = abs(lateral[i]) <= max_off and longitudinal[i] >= min_long
            if not gated:
                out.append(0.0)
                continue
            j = bisect.bisect_left(times, float(times[i]) - window)
            dt = float(times[i]) - float(times[j])
            if dt < 0.5 * window:
                out.append(0.0)
                continue
            out.append((abs(lateral[j]) - abs(lateral[i])) / dt)
        return out

    @staticmethod
    def _conflict_point_values(sample: TrackIndicators) -> Dict[str, float]:
        """Conflict-point coordinates as event values (omitted when unknown)."""
        vals: Dict[str, float] = {}
        if sample.conflict_x is not None and sample.conflict_y is not None:
            vals["conflict_x"] = float(sample.conflict_x)
            vals["conflict_y"] = float(sample.conflict_y)
        return vals

    def _conflict_region_candidates(
        self,
        ev: ParticipantEvidence,
        track_id: str,
        ti: List[TrackIndicators],
        conf_fn: Callable[[_Episode], float],
    ) -> List[_Candidate]:
        """CONFLICT_REGION_ENTRY: the ego enters the region it inferred itself.

        The signal is the distance from our own position to the inferred conflict
        point, defined only while the conflict hypothesis itself is credible. The
        event therefore states "I drove into the area I had predicted we would
        contest", which is checkable against the same recorded evidence.
        """
        cfg = self._cfg
        radius = float(cfg.get("indicators.conflict.region_radius_m", 6.0))
        min_conflict = float(cfg.get("events.radar.path_conflict.min_confidence", 0.35))
        max_gap = float(cfg.get("indicators.max_sync_gap_s", 0.15))

        times = [s.t for s in ti]
        dist: List[Optional[float]] = []
        for s in ti:
            if (
                s.conflict_x is None
                or s.conflict_y is None
                or s.conflict_score < min_conflict
            ):
                dist.append(None)
                continue
            own = ev.telemetry_at(s.t, max_gap)
            if own is None:
                dist.append(None)
                continue
            dist.append(distance(own.x, own.y, s.conflict_x, s.conflict_y))

        return self._threshold_candidates(
            ev.participant_id,
            times,
            dist,
            EventType.CONFLICT_REGION_ENTRY,
            radius,
            "below",
            "distance_to_conflict_m",
            "track",
            ["radar", "telemetry"],
            subject=track_id,
            evidence_ref=track_id,
            confidence_fn=conf_fn,
            extra_values=lambda i: self._conflict_point_values(ti[i]),
        )

    def _run_end(
        self, ev: ParticipantEvidence, tracks: Dict[str, List[TrackIndicators]]
    ) -> Optional[float]:
        """Last instant covered by this participant's recording."""
        span = ev.span()
        if span is not None:
            return float(span[1])
        ends = [series[-1].t for series in tracks.values() if series]
        return max(ends) if ends else None

    def _track_lost_gap(self, ev: ParticipantEvidence) -> float:
        """How long a track must be absent before the end to count as lost.

        Defaults to the tracker's own drop criterion -- ``max_misses`` frames --
        because that is exactly how long the tracker itself waits before deciding
        a track is gone.
        """
        configured = self._cfg.get("events.radar.track_lost.min_gap_to_end_s", None)
        if configured is not None:
            return float(configured)
        max_misses = float(self._cfg.get("radar_processing.tracking.max_misses", 6))
        period = ev.sample_period()
        if period is None or period <= 0.0:
            period = float(self._cfg.get("simulation.fixed_delta_seconds", 0.05))
        return max_misses * float(period)

    # -- triggers and outcomes --------------------------------------------

    def _trigger_candidates(self, ev: ParticipantEvidence) -> List[_Candidate]:
        """Outcome events read straight off the onboard recorder triggers."""
        out: List[_Candidate] = []
        for trig in sorted(ev.triggers, key=lambda t: float(t.t)):
            subject = trig.detail.get("track_id")
            subject = str(subject) if isinstance(subject, str) else None

            if trig.kind == TriggerKind.COLLISION or trig.collision_detected:
                out.append(
                    _Candidate(
                        event_type=EventType.COLLISION,
                        subject=subject,
                        t_start=float(trig.t),
                        t_peak=float(trig.t),
                        t_end=float(trig.t),
                        peak_value=float(trig.impulse),
                        extreme_is_max=True,
                        values={"impulse": float(trig.impulse)},
                        confidence=1.0,
                        evidence=[
                            Evidence(
                                kind="trigger",
                                ref=TriggerKind.COLLISION.value,
                                t_start=float(trig.t),
                                t_end=float(trig.t),
                            )
                        ],
                        source_sensors=["collision"],
                    )
                )
            elif trig.kind == TriggerKind.NEAR_MISS:
                values: Dict[str, float] = {}
                for key in ("min_ttc", "min_range_m", "ttc", "range_m"):
                    raw = trig.detail.get(key)
                    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                        values[key] = float(raw)
                out.append(
                    _Candidate(
                        event_type=EventType.NEAR_MISS,
                        subject=subject,
                        t_start=float(trig.t),
                        t_peak=float(trig.t),
                        t_end=float(trig.t),
                        peak_value=float(values.get("min_ttc", values.get("ttc", 0.0))),
                        extreme_is_max=False,
                        values=values,
                        confidence=1.0,
                        evidence=[
                            Evidence(
                                kind="trigger",
                                ref=TriggerKind.NEAR_MISS.value,
                                t_start=float(trig.t),
                                t_end=float(trig.t),
                            )
                        ],
                        source_sensors=["radar"],
                    )
                )
        return out

    def _derived_candidates(
        self,
        ev: ParticipantEvidence,
        own: List[OwnIndicators],
        merged: List[_Candidate],
    ) -> List[_Candidate]:
        """Outcome events inferred from already-debounced primary events."""
        cfg = self._cfg
        pid = ev.participant_id
        out: List[_Candidate] = []

        collisions = [c for c in merged if c.event_type == EventType.COLLISION]
        collision_times = sorted(c.t_peak for c in collisions)
        resolve_window = float(cfg.get("events.outcome.near_miss.resolve_window_s", 3.0))

        # --- NEAR_MISS: a critical TTC episode that ended without an impact. The
        #     absence of a collision is itself the evidence, so the derived event
        #     cites the critical-TTC event it was inferred from.
        for cand in merged:
            if cand.event_type != EventType.CRITICAL_TTC:
                continue
            end = cand.t_end if cand.t_end is not None else cand.t_peak
            if any(cand.t_start - 1e-9 <= t <= end + resolve_window for t in collision_times):
                continue
            source_id = make_event_id(
                "local", pid, EventType.CRITICAL_TTC.value, cand.t_peak, cand.subject
            )
            values = {"ttc_s": float(cand.peak_value)}
            out.append(
                _Candidate(
                    event_type=EventType.NEAR_MISS,
                    subject=cand.subject,
                    t_start=cand.t_start,
                    t_peak=cand.t_peak,
                    t_end=cand.t_end,
                    peak_value=float(cand.peak_value),
                    extreme_is_max=False,
                    values=values,
                    confidence=float(cand.confidence),
                    evidence=list(cand.evidence)
                    + [
                        Evidence(
                            kind="event",
                            ref=source_id,
                            t_start=cand.t_start,
                            t_end=cand.t_end,
                        )
                    ],
                    source_sensors=["radar"],
                )
            )

        # --- POST_IMPACT_STOP: the vehicle came to rest shortly after an impact.
        stop_speed = float(cfg.get("events.outcome.post_impact_stop.speed_mps", 0.6))
        within = float(cfg.get("events.outcome.post_impact_stop.within_s", 4.0))
        times = [o.t for o in own]
        for cand in collisions:
            t_col = cand.t_peak
            i = bisect.bisect_left(times, t_col)
            stop_t: Optional[float] = None
            stop_speed_value = 0.0
            while i < len(own) and own[i].t <= t_col + within:
                if own[i].speed <= stop_speed:
                    stop_t = own[i].t
                    stop_speed_value = own[i].speed
                    break
                i += 1
            if stop_t is None:
                continue
            collision_id = make_event_id(
                "local", pid, EventType.COLLISION.value, t_col, cand.subject
            )
            out.append(
                _Candidate(
                    event_type=EventType.POST_IMPACT_STOP,
                    subject=None,
                    t_start=float(t_col),
                    t_peak=float(stop_t),
                    t_end=float(stop_t),
                    peak_value=float(stop_speed_value),
                    extreme_is_max=False,
                    values={
                        "speed_mps": float(stop_speed_value),
                        "delay_s": float(stop_t - t_col),
                    },
                    confidence=1.0,
                    evidence=[
                        Evidence(
                            kind="telemetry", ref=pid, t_start=float(t_col), t_end=float(stop_t)
                        ),
                        Evidence(
                            kind="event",
                            ref=collision_id,
                            t_start=float(t_col),
                            t_end=float(t_col),
                        ),
                    ],
                    source_sensors=["telemetry", "collision"],
                )
            )

        return out

    # -- debouncing and finalisation ---------------------------------------

    def _merge(self, candidates: List[_Candidate]) -> List[_Candidate]:
        """Collapse same-``(type, subject)`` detections closer than the debounce.

        Two detections merge when their peaks fall within
        ``events.min_separation_s``, and *also* when the episodes themselves are
        that close end-to-start. The second rule matters for a signal that
        chatters across the release threshold on a long plateau: keeping the
        earlier (equally extreme) peak would otherwise walk the comparison point
        backwards and let a single sustained manoeuvre fragment into several
        events.

        Merging is idempotent -- a list already separated by the debounce passes
        through unchanged -- which is what lets :meth:`extract` run it twice
        around the derived-event pass.
        """
        groups: Dict[Tuple[str, str], List[_Candidate]] = {}
        for c in candidates:
            groups.setdefault((c.event_type.value, c.subject or ""), []).append(c)

        out: List[_Candidate] = []
        for key in sorted(groups.keys()):
            items = sorted(groups[key], key=lambda c: (c.t_peak, c.t_start))
            kept: List[_Candidate] = []
            for cand in items:
                if kept and self._should_merge(kept[-1], cand):
                    kept[-1] = self._merge_pair(kept[-1], cand)
                else:
                    kept.append(cand)
            out.extend(kept)
        return out

    def _should_merge(self, prev: _Candidate, cand: _Candidate) -> bool:
        """Whether ``cand`` is too close to ``prev`` to count as a separate event."""
        if (cand.t_peak - prev.t_peak) < self._min_sep:
            return True
        prev_end = prev.t_end if prev.t_end is not None else prev.t_peak
        return (cand.t_start - prev_end) < self._min_sep

    @staticmethod
    def _merge_pair(a: _Candidate, b: _Candidate) -> _Candidate:
        """Merge two detections, keeping the more extreme peak and the wider span."""
        keep = a
        if (b.peak_value > a.peak_value) if a.extreme_is_max else (b.peak_value < a.peak_value):
            keep = b
        ends = [t for t in (a.t_end, b.t_end) if t is not None]
        sensors: List[str] = list(a.source_sensors)
        for s in b.source_sensors:
            if s not in sensors:
                sensors.append(s)
        evidence: List[Evidence] = list(a.evidence)
        for e in b.evidence:
            if e not in evidence:
                evidence.append(e)
        return _Candidate(
            event_type=keep.event_type,
            subject=keep.subject,
            t_start=min(a.t_start, b.t_start),
            t_peak=keep.t_peak,
            t_end=max(ends) if ends else None,
            peak_value=keep.peak_value,
            extreme_is_max=keep.extreme_is_max,
            values=dict(keep.values),
            confidence=max(a.confidence, b.confidence),
            evidence=evidence,
            source_sensors=sensors,
        )

    @staticmethod
    def _to_event(pid: str, cand: _Candidate) -> Event:
        """Freeze a candidate into a persisted :class:`Event` with a stable id."""
        values = {
            k: float(v)
            for k, v in cand.values.items()
            if v is not None and not math.isnan(float(v)) and not math.isinf(float(v))
        }
        return Event(
            event_id=make_event_id(
                "local", pid, cand.event_type.value, cand.t_peak, cand.subject
            ),
            event_type=cand.event_type,
            participant_id=pid,
            t_start=float(cand.t_start),
            t_peak=float(cand.t_peak),
            t_end=None if cand.t_end is None else float(cand.t_end),
            subject=cand.subject,
            values=values,
            confidence=float(max(0.0, min(1.0, cand.confidence))),
            evidence=list(cand.evidence),
            provenance=Provenance.LOCAL,
            source_sensors=list(cand.source_sensors),
        )
