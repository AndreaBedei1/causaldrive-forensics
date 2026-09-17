"""In-memory bundles of persisted evidence.

:class:`ParticipantEvidence` is the unit that the local pipeline produces and
that fusion, model checking, evaluation and the viewer consume. Loading always
goes through here, which means there is exactly one place where the artifact
format is interpreted -- and exactly one place to audit for boundary violations.

``ParticipantEvidence`` deliberately has no field capable of holding another
actor's ground truth. Privileged data lives only in :class:`OracleEvidence`,
which is loaded by a separate function that inference code never calls.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from .io import read_json, read_jsonl_gz, write_json, write_jsonl_gz
from .layout import RunLayout
from .schemas import (
    ControlSample,
    Event,
    EventType,
    GraphDocument,
    LocalTriggerRecord,
    Provenance,
    RadarDetection,
    RadarFrame,
    SCHEMA_VERSIONS,
    TelemetrySample,
    TrackSample,
    TriggerKind,
    to_jsonable,
)

__all__ = [
    "ParticipantEvidence",
    "RunEvidence",
    "load_participant",
    "load_run",
    "save_participant",
]


# ---------------------------------------------------------------------------
# Per-participant bundle
# ---------------------------------------------------------------------------


@dataclass
class ParticipantEvidence:
    """Everything one participant recorded about itself and observed around it.

    All fields are strictly onboard-derived. Time series are kept sorted by ``t``
    so the lookup helpers can binary-search.
    """

    participant_id: str
    telemetry: List[TelemetrySample] = field(default_factory=list)
    controls: List[ControlSample] = field(default_factory=list)
    radar: List[RadarFrame] = field(default_factory=list)
    tracks: List[TrackSample] = field(default_factory=list)
    triggers: List[LocalTriggerRecord] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    # -- time -------------------------------------------------------------

    def times(self) -> List[float]:
        """Sorted telemetry timestamps."""
        return [float(s.t) for s in self.telemetry]

    def span(self) -> Optional[Tuple[float, float]]:
        """``(t_first, t_last)`` of the telemetry trace, or ``None`` when empty."""
        if not self.telemetry:
            return None
        return (float(self.telemetry[0].t), float(self.telemetry[-1].t))

    def sample_period(self) -> Optional[float]:
        """Median telemetry sampling period in seconds."""
        ts = self.times()
        if len(ts) < 2:
            return None
        deltas = sorted(ts[i + 1] - ts[i] for i in range(len(ts) - 1))
        return float(deltas[len(deltas) // 2])

    # -- lookups ----------------------------------------------------------

    def telemetry_at(self, t: float, max_gap: float = 0.15) -> Optional[TelemetrySample]:
        """Telemetry sample nearest to ``t``, or ``None`` if none is within ``max_gap``."""
        return _nearest(self.telemetry, t, max_gap)

    def control_at(self, t: float, max_gap: float = 0.15) -> Optional[ControlSample]:
        """Control sample nearest to ``t``."""
        return _nearest(self.controls, t, max_gap)

    def controls_by_frame(self) -> Dict[int, ControlSample]:
        """Controls indexed by frame, for joining with telemetry."""
        return {int(c.frame): c for c in self.controls}

    def tracks_by_id(self) -> Dict[str, List[TrackSample]]:
        """All track samples grouped by local track id, each sorted by time."""
        out: Dict[str, List[TrackSample]] = {}
        for s in self.tracks:
            out.setdefault(s.track_id, []).append(s)
        for v in out.values():
            v.sort(key=lambda s: float(s.t))
        return out

    def track_ids(self) -> List[str]:
        """Sorted local track ids present in this bundle."""
        return sorted({s.track_id for s in self.tracks})

    def track_span(self, track_id: str) -> Optional[Tuple[float, float]]:
        """``(t_first, t_last)`` for one track."""
        samples = [s for s in self.tracks if s.track_id == track_id]
        if not samples:
            return None
        ts = sorted(float(s.t) for s in samples)
        return (ts[0], ts[-1])

    def self_trajectory(self) -> Tuple[List[float], List[float], List[float]]:
        """``(t, x, y)`` of this participant's own localisation trace.

        This is the trajectory a participant *shares* after an incident, and the
        reference against which another participant's radar tracks are matched.
        """
        return (
            [float(s.t) for s in self.telemetry],
            [float(s.x) for s in self.telemetry],
            [float(s.y) for s in self.telemetry],
        )

    def track_trajectory(self, track_id: str) -> Tuple[List[float], List[float], List[float]]:
        """``(t, gx, gy)`` of one local radar track in global coordinates."""
        samples = sorted(
            (s for s in self.tracks if s.track_id == track_id), key=lambda s: float(s.t)
        )
        return (
            [float(s.t) for s in samples],
            [float(s.gx) for s in samples],
            [float(s.gy) for s in samples],
        )

    def events_of_type(self, event_type: EventType) -> List[Event]:
        """All events of one type, ordered by peak time."""
        return sorted(
            (e for e in self.events if e.event_type == event_type), key=lambda e: e.t_peak
        )

    def collision_trigger(self) -> Optional[LocalTriggerRecord]:
        """The earliest collision trigger recorded onboard, if any."""
        cands = [
            t
            for t in self.triggers
            if t.kind == TriggerKind.COLLISION or (t.collision_detected and t.impulse > 0.0)
        ]
        if not cands:
            return None
        return min(cands, key=lambda t: float(t.t))

    # -- summary ----------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """Counts used in manifests and diagnostics."""
        sp = self.span()
        return {
            "participant_id": self.participant_id,
            "n_telemetry": len(self.telemetry),
            "n_controls": len(self.controls),
            "n_radar_frames": len(self.radar),
            "n_radar_detections": sum(len(f.detections) for f in self.radar),
            "n_track_samples": len(self.tracks),
            "n_tracks": len(self.track_ids()),
            "n_triggers": len(self.triggers),
            "n_events": len(self.events),
            "t_start": sp[0] if sp else None,
            "t_end": sp[1] if sp else None,
        }


def _nearest(samples: Sequence[Any], t: float, max_gap: float) -> Optional[Any]:
    """Nearest sample to ``t`` by the ``.t`` attribute, within ``max_gap``."""
    if not samples:
        return None
    times = [float(s.t) for s in samples]
    i = bisect.bisect_left(times, float(t))
    best = None
    best_d = float("inf")
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(samples):
            d = abs(times[j] - float(t))
            if d < best_d:
                best, best_d = samples[j], d
    if best is None or best_d > float(max_gap):
        return None
    return best


# ---------------------------------------------------------------------------
# Whole-run bundle
# ---------------------------------------------------------------------------


@dataclass
class RunEvidence:
    """All participants' local evidence for one run, plus the run manifest."""

    run_dir: Path
    manifest: Dict[str, Any] = field(default_factory=dict)
    participants: Dict[str, ParticipantEvidence] = field(default_factory=dict)
    time_alignment: Optional[Dict[str, Any]] = None

    @property
    def participant_ids(self) -> List[str]:
        return sorted(self.participants.keys())

    def get(self, participant_id: str) -> ParticipantEvidence:
        return self.participants[participant_id]

    def spans(self) -> Dict[str, Tuple[float, float]]:
        """Time span per participant, skipping participants with no telemetry."""
        out: Dict[str, Tuple[float, float]] = {}
        for pid, ev in self.participants.items():
            sp = ev.span()
            if sp is not None:
                out[pid] = sp
        return out

    @property
    def scenario_id(self) -> str:
        return str(self.manifest.get("scenario_id", ""))

    @property
    def seed(self) -> int:
        return int(self.manifest.get("seed", 0))

    @property
    def run_id(self) -> str:
        return str(self.manifest.get("run_id", ""))

    def local_causal_graph(self, participant_id: str) -> Optional[GraphDocument]:
        """Load one participant's local causal DAG if it was persisted."""
        from ..graph.export import load_graph

        path = RunLayout.from_run_dir(self.run_dir).causal_graph(participant_id)
        if not path.exists():
            return None
        return load_graph(path, expect_scope=Provenance.LOCAL)

    def local_event_graph(self, participant_id: str) -> Optional[GraphDocument]:
        """Load one participant's local event graph if it was persisted."""
        from ..graph.export import load_graph

        path = RunLayout.from_run_dir(self.run_dir).event_graph(participant_id)
        if not path.exists():
            return None
        return load_graph(path, expect_scope=Provenance.LOCAL)


# ---------------------------------------------------------------------------
# Loading / saving
# ---------------------------------------------------------------------------


def load_participant(
    layout: Union[RunLayout, str, Path],
    participant_id: str,
    with_radar: bool = True,
) -> ParticipantEvidence:
    """Load one participant's evidence from disk.

    ``with_radar=False`` skips the raw detection stream, which is by far the
    largest artifact and is unnecessary for fusion, checking and evaluation.
    """
    lay = layout if isinstance(layout, RunLayout) else RunLayout.from_run_dir(layout)

    telemetry = [
        _telemetry_from_dict(d) for d in _maybe_jsonl(lay.telemetry(participant_id))
    ]
    controls = [_control_from_dict(d) for d in _maybe_jsonl(lay.controls(participant_id))]
    tracks = [_track_from_dict(d) for d in _maybe_jsonl(lay.tracks(participant_id))]
    radar: List[RadarFrame] = []
    if with_radar:
        radar = [_radar_from_dict(d) for d in _maybe_jsonl(lay.radar(participant_id))]

    triggers: List[LocalTriggerRecord] = []
    tpath = lay.triggers(participant_id)
    if tpath.exists():
        payload = read_json(tpath)
        for d in payload.get("triggers", []):
            triggers.append(_trigger_from_dict(d))

    events: List[Event] = []
    meta: Dict[str, Any] = {}
    epath = lay.events(participant_id)
    if epath.exists():
        payload = read_json(epath)
        from .schemas import _event_from_dict  # local import: private helper

        events = [_event_from_dict(d) for d in payload.get("events", [])]
        meta = payload.get("meta", {}) or {}

    telemetry.sort(key=lambda s: float(s.t))
    controls.sort(key=lambda s: float(s.t))
    tracks.sort(key=lambda s: float(s.t))
    radar.sort(key=lambda s: float(s.t))
    events.sort(key=lambda e: float(e.t_peak))

    return ParticipantEvidence(
        participant_id=participant_id,
        telemetry=telemetry,
        controls=controls,
        radar=radar,
        tracks=tracks,
        triggers=triggers,
        events=events,
        meta=meta,
    )


def load_run(
    run_dir: Union[str, Path], with_radar: bool = False
) -> RunEvidence:
    """Load every participant's evidence plus the manifest for one run."""
    lay = RunLayout.from_run_dir(run_dir)
    manifest: Dict[str, Any] = {}
    if lay.manifest.exists():
        recorded = read_json(lay.manifest)
        # An inference bundle carries session labels, never simulator timing,
        # scripted actions, true collision pairs or replay/clock parameters.
        manifest = {k: recorded[k] for k in ("run_id", "scenario_id", "seed", "variant",
                    "clock_protocol") if k in recorded}
    participants = {
        pid: load_participant(lay, pid, with_radar=with_radar)
        for pid in lay.participant_ids()
    }
    return RunEvidence(run_dir=lay.root, manifest=manifest, participants=participants)


def save_participant(layout: RunLayout, ev: ParticipantEvidence) -> None:
    """Persist one participant's evidence in the canonical layout."""
    layout.vehicle_dir(ev.participant_id).mkdir(parents=True, exist_ok=True)
    write_jsonl_gz(layout.telemetry(ev.participant_id), ev.telemetry)
    write_jsonl_gz(layout.controls(ev.participant_id), ev.controls)
    write_jsonl_gz(layout.radar(ev.participant_id), ev.radar)
    write_jsonl_gz(layout.tracks(ev.participant_id), ev.tracks)
    write_json(
        layout.triggers(ev.participant_id),
        {
            "schema_version": SCHEMA_VERSIONS["events"],
            "participant_id": ev.participant_id,
            "triggers": [to_jsonable(t) for t in ev.triggers],
        },
    )
    write_json(
        layout.events(ev.participant_id),
        {
            "schema_version": SCHEMA_VERSIONS["events"],
            "participant_id": ev.participant_id,
            "provenance": Provenance.LOCAL.value,
            "meta": ev.meta,
            "events": [to_jsonable(e) for e in ev.events],
        },
    )


# ---------------------------------------------------------------------------
# Record decoders
# ---------------------------------------------------------------------------


def _maybe_jsonl(path: Path) -> List[Dict[str, Any]]:
    return read_jsonl_gz(path) if path.exists() else []


def _telemetry_from_dict(d: Dict[str, Any]) -> TelemetrySample:
    return TelemetrySample(
        t=float(d["t"]),
        frame=int(d["frame"]),
        participant_id=d["participant_id"],
        x=float(d["x"]),
        y=float(d["y"]),
        z=float(d.get("z", 0.0)),
        yaw=float(d["yaw"]),
        pitch=float(d.get("pitch", 0.0)),
        roll=float(d.get("roll", 0.0)),
        vx=float(d.get("vx", 0.0)),
        vy=float(d.get("vy", 0.0)),
        vz=float(d.get("vz", 0.0)),
        speed=float(d.get("speed", 0.0)),
        ax=float(d.get("ax", 0.0)),
        ay=float(d.get("ay", 0.0)),
        az=float(d.get("az", 0.0)),
        accel_long=float(d.get("accel_long", 0.0)),
        accel_lat=float(d.get("accel_lat", 0.0)),
        yaw_rate=float(d.get("yaw_rate", 0.0)),
        schema_version=d.get("schema_version", SCHEMA_VERSIONS["telemetry"]),
    )


def _control_from_dict(d: Dict[str, Any]) -> ControlSample:
    return ControlSample(
        t=float(d["t"]),
        frame=int(d["frame"]),
        participant_id=d["participant_id"],
        throttle=float(d.get("throttle", 0.0)),
        brake=float(d.get("brake", 0.0)),
        steer=float(d.get("steer", 0.0)),
        hand_brake=bool(d.get("hand_brake", False)),
        reverse=bool(d.get("reverse", False)),
        gear=int(d.get("gear", 0)),
        schema_version=d.get("schema_version", SCHEMA_VERSIONS["controls"]),
    )


def _radar_from_dict(d: Dict[str, Any]) -> RadarFrame:
    return RadarFrame(
        t=float(d["t"]),
        frame=int(d["frame"]),
        participant_id=d["participant_id"],
        sensor_id=d.get("sensor_id", "front"),
        detections=[
            RadarDetection(
                depth=float(x["depth"]),
                azimuth=float(x["azimuth"]),
                altitude=float(x["altitude"]),
                velocity=float(x["velocity"]),
            )
            for x in d.get("detections", [])
        ],
        sensor_yaw=float(d.get("sensor_yaw", 0.0)),
        sensor_x=float(d.get("sensor_x", 0.0)),
        sensor_y=float(d.get("sensor_y", 0.0)),
        sensor_z=float(d.get("sensor_z", 0.0)),
        schema_version=d.get("schema_version", SCHEMA_VERSIONS["radar"]),
    )


def _track_from_dict(d: Dict[str, Any]) -> TrackSample:
    return TrackSample(
        t=float(d["t"]),
        frame=int(d["frame"]),
        participant_id=d["participant_id"],
        track_id=d["track_id"],
        rel_x=float(d.get("rel_x", 0.0)),
        rel_y=float(d.get("rel_y", 0.0)),
        gx=float(d.get("gx", 0.0)),
        gy=float(d.get("gy", 0.0)),
        gvx=float(d.get("gvx", 0.0)),
        gvy=float(d.get("gvy", 0.0)),
        range_m=float(d.get("range_m", 0.0)),
        azimuth_rad=float(d.get("azimuth_rad", 0.0)),
        range_rate=float(d.get("range_rate", 0.0)),
        rel_vx=float(d.get("rel_vx", 0.0)),
        rel_vy=float(d.get("rel_vy", 0.0)),
        n_points=int(d.get("n_points", 0)),
        extent_x=float(d.get("extent_x", 0.0)),
        extent_y=float(d.get("extent_y", 0.0)),
        confidence=float(d.get("confidence", 0.0)),
        age=int(d.get("age", 0)),
        misses=int(d.get("misses", 0)),
        ttc=d.get("ttc"),
        schema_version=d.get("schema_version", SCHEMA_VERSIONS["tracks"]),
    )


def _trigger_from_dict(d: Dict[str, Any]) -> LocalTriggerRecord:
    return LocalTriggerRecord(
        t=float(d["t"]),
        frame=int(d["frame"]),
        participant_id=d["participant_id"],
        kind=TriggerKind(d["kind"]),
        collision_detected=bool(d.get("collision_detected", False)),
        impulse=float(d.get("impulse", 0.0)),
        detail=d.get("detail", {}) or {},
    )
