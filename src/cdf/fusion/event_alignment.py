"""Deciding which local events of different participants are the same event.

The problem
-----------
Two participants recording the same incident describe it from incompatible
viewpoints. ``B`` decelerating hard records an own-behaviour ``DECELERATION``
(derived from its own telemetry, ``subject = None``). ``A``, following it,
records a ``TARGET_DECELERATION`` about an anonymous radar track
(``subject = "A::T001"``). These are two descriptions of *one physical fact*, and
a fusion layer that cannot merge them produces a graph with duplicated, weakly
supported nodes instead of a corroborated one.

Merging them requires three things, all of which this module makes explicit:

1. **Identity** -- ``A::T001`` must first have been resolved to participant ``B``
   by :mod:`cdf.fusion.track_association`. Without that resolution the event is
   left alone: an unresolved subject is a reason not to merge, never a reason to
   guess.
2. **A type correspondence that survives the change of viewpoint** -- the
   observed-from-outside type and the own-behaviour type are different
   :class:`~cdf.common.schemas.EventType` values by construction, so equality of
   ``event_type`` is the wrong test. Types are grouped into *families* (see
   :data:`DEFAULT_TYPE_FAMILIES`), and ``require_same_type`` is interpreted as
   "same family".
3. **A subject rule that respects the unary/relational distinction** -- a
   deceleration is a fact *about one vehicle* (whoever observed it), whereas a
   low TTC or a collision is a fact *about a pair*. Unary families are keyed by
   the vehicle they describe, relational families by the unordered pair. This is
   precisely what lets ``A``'s observation of ``B`` merge with ``B``'s own report
   while still keeping ``A``'s observation of ``B`` apart from ``C``'s
   observation of ``D``.

A group never contains two events from the same participant: within one log a
repeated detection is a separate event, and collapsing those would silently
rewrite that participant's own account.

Only exported local evidence is consulted. No actor ids, no map data, no oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import RunEvidence
from ..common.schemas import Event, EventType, ORACLE_ONLY_EVENT_TYPES
from .track_association import STATUS_AMBIGUOUS, STATUS_RESOLVED, TrackAssignment
from .aligned_evidence import participant_is_aligned, require_common_time

__all__ = [
    "DEFAULT_TYPE_FAMILIES",
    "RELATIONAL_FAMILIES",
    "EventGroup",
    "resolve_subjects",
    "align_events",
    "align_event_records",
    "family_of",
    "reconcile_mutual_impacts",
]


#: Event types that describe the same physical fact from different viewpoints are
#: placed in one family. The interesting entries are the cross-viewpoint ones:
#: ``TARGET_DECELERATION`` (what an observer sees) belongs with ``DECELERATION``
#: and ``HARD_DECELERATION`` (what the decelerating vehicle records about itself),
#: and ``CUT_IN_LIKE_MOTION`` belongs with ``LANE_CHANGE_LIKE_MANEUVER``.
DEFAULT_TYPE_FAMILIES: Dict[str, Tuple[str, ...]] = {
    # -- unary: a fact about a single vehicle's behaviour ------------------
    "vehicle_started": (EventType.VEHICLE_STARTED.value,),
    "acceleration": (EventType.ACCELERATION.value,),
    "deceleration": (
        EventType.DECELERATION.value,
        EventType.HARD_DECELERATION.value,
        EventType.TARGET_DECELERATION.value,
    ),
    "brake_command": (EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value),
    "throttle_command": (EventType.THROTTLE_ONSET.value,),
    "steer_command": (EventType.STEER_ONSET.value,),
    "heading_change": (EventType.SIGNIFICANT_HEADING_CHANGE.value,),
    "lane_change": (
        EventType.LANE_CHANGE_LIKE_MANEUVER.value,
        EventType.CUT_IN_LIKE_MOTION.value,
    ),
    "post_impact_stop": (EventType.POST_IMPACT_STOP.value,),
    # -- relational: a fact about a pair of vehicles -----------------------
    "track_appeared": (EventType.RADAR_TRACK_APPEARED.value,),
    "track_lost": (EventType.RADAR_TRACK_LOST.value,),
    "closing": (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value),
    "low_ttc": (EventType.LOW_TTC.value,),
    "critical_ttc": (EventType.CRITICAL_TTC.value,),
    "lateral_crossing": (EventType.LATERAL_CROSSING.value,),
    "path_conflict": (
        EventType.PREDICTED_PATH_CONFLICT.value,
        EventType.CONFLICT_REGION_ENTRY.value,
    ),
    "near_miss": (EventType.NEAR_MISS.value,),
    "collision": (EventType.COLLISION.value,),
}

#: Families whose events are statements about a *pair* of vehicles rather than
#: about one vehicle's own behaviour.
RELATIONAL_FAMILIES: Tuple[str, ...] = (
    "track_appeared",
    "track_lost",
    "closing",
    "low_ttc",
    "critical_ttc",
    "lateral_crossing",
    "path_conflict",
    "near_miss",
    "collision",
)

#: Subject values that mean "this event is about the recording vehicle itself".
_SELF_SUBJECTS = (None, "", "self")


@dataclass
class EventGroup:
    """A set of local events judged to describe one physical event.

    Singleton groups are kept explicitly so that downstream code can treat merged
    and unmerged events uniformly, and so that the reason an event stayed alone is
    still attached to it.
    """

    members: List[str]
    """Contributing local event ids, sorted."""
    family: str
    vehicles: List[str]
    """Participants the group is about (one for unary, two for relational)."""
    relational: bool
    t_peak_min: float
    t_peak_max: float
    mergeable: bool = True
    """``False`` when the event could not be keyed (unresolved subject)."""
    note: str = ""

    @property
    def size(self) -> int:
        return len(self.members)


# ---------------------------------------------------------------------------
# Subjects
# ---------------------------------------------------------------------------


def resolve_subjects(assignments: Mapping[str, TrackAssignment]) -> Dict[str, str]:
    """Local track id -> participant id, for named assignments only.

    ``AMBIGUOUS`` assignments are included because they *do* name a participant
    (with reduced confidence, which propagates into the fused node's confidence);
    ``UNRESOLVED`` ones are excluded because they name nobody. The distinction is
    deliberately preserved rather than collapsed into a single boolean.
    """
    out: Dict[str, str] = {}
    for track_id in sorted(assignments.keys()):
        a = assignments[track_id]
        if a.status in (STATUS_RESOLVED, STATUS_AMBIGUOUS) and a.assigned_participant:
            out[track_id] = a.assigned_participant
    return out


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------


#: Memoised family tables, keyed by the configuration hash. Building the tables
#: per event would dominate the cost of alignment on long runs; keying by the
#: hash keeps the memo correct when a different configuration is used.
_FAMILY_TABLE_CACHE: Dict[str, Tuple[Dict[str, str], Dict[str, bool]]] = {}


def _family_tables(cfg: Config) -> Tuple[Dict[str, str], Dict[str, bool]]:
    """Build ``type -> family`` and ``family -> relational`` lookup tables.

    The table may be overridden through ``fusion.event_alignment.type_families``
    (a mapping ``family -> [event type, ...]``), which is how a scenario can
    declare an additional cross-viewpoint correspondence without touching code.
    """
    cached = _FAMILY_TABLE_CACHE.get(cfg.hash)
    if cached is not None:
        return cached

    raw = cfg.get("fusion.event_alignment.type_families", None)
    families: Dict[str, Tuple[str, ...]]
    if raw is None:
        families = dict(DEFAULT_TYPE_FAMILIES)
    else:
        if not isinstance(raw, Mapping):
            raise TypeError(
                "fusion.event_alignment.type_families must be a mapping "
                "family -> [event_type, ...], got {0!r}".format(type(raw).__name__)
            )
        families = {str(k): tuple(str(v) for v in vals) for k, vals in raw.items()}

    relational_names = cfg.get(
        "fusion.event_alignment.relational_families", list(RELATIONAL_FAMILIES)
    )
    relational = {str(name): True for name in relational_names}

    type_to_family: Dict[str, str] = {}
    for fam, types in sorted(families.items()):
        for t in types:
            if t in type_to_family:
                raise ValueError(
                    "event type {0!r} is declared in two families ({1!r} and {2!r})".format(
                        t, type_to_family[t], fam
                    )
                )
            type_to_family[t] = fam

    family_relational = {fam: bool(relational.get(fam, False)) for fam in families}
    _FAMILY_TABLE_CACHE[cfg.hash] = (type_to_family, family_relational)
    return type_to_family, family_relational


def family_of(event_type: Any, cfg: Config) -> Tuple[str, bool]:
    """``(family, is_relational)`` for one event type.

    An unlisted type forms its own singleton family, which keeps the alignment
    conservative: an unknown type can still merge with an identical unknown type
    but never with anything else.
    """
    type_to_family, family_relational = _family_tables(cfg)
    value = event_type.value if isinstance(event_type, EventType) else str(event_type)
    fam = type_to_family.get(value, value)
    return fam, bool(family_relational.get(fam, False))


# ---------------------------------------------------------------------------
# Alignment
# ---------------------------------------------------------------------------


@dataclass
class _Record:
    """Internal per-event working record."""

    event: Event
    participant_id: str
    family: str
    relational: bool
    key: Optional[Tuple[str, ...]]
    note: str = ""


def align_events(
    run: RunEvidence, subject_map: Mapping[str, str], cfg: Config
) -> Dict[str, Any]:
    """Group the participants' exported local events into physical events.

    Returns ``{"groups": [[event_id, ...], ...], "singletons": [event_id, ...],
    "diagnostics": [...]}``; ``groups`` holds only the multi-participant groups,
    and together the two lists partition every input event exactly once.
    """
    events_by_participant = {
        pid: list(run.get(pid).events) for pid in run.participant_ids
    }
    groups, diagnostics = align_event_records(
        events_by_participant, subject_map, cfg, run=run
    )
    merged = [g.members for g in groups if g.size > 1]
    singles = [g.members[0] for g in groups if g.size == 1]
    return {
        "groups": merged,
        "singletons": singles,
        "n_groups": len(merged),
        "n_singletons": len(singles),
        "time_tolerance_s": float(cfg.get("fusion.event_alignment.time_tolerance_s", 1.0)),
        "require_same_type": bool(cfg.get("fusion.event_alignment.require_same_type", True)),
        "subject_must_agree": bool(
            cfg.get("fusion.event_alignment.subject_must_agree", True)
        ),
        "diagnostics": diagnostics,
    }


def align_event_records(
    events_by_participant: Mapping[str, Sequence[Event]],
    subject_map: Mapping[str, str],
    cfg: Config,
    run: Optional[RunEvidence] = None,
) -> Tuple[List[EventGroup], List[Dict[str, Any]]]:
    """Shared alignment core, returning every group including singletons.

    :func:`align_events` reports on the participants' exported event lists;
    :mod:`cdf.fusion.graph_fusion` runs the identical algorithm over the *nodes of
    the local graphs*, which is why the core is factored out here instead of being
    reimplemented (and allowed to drift) on the graph side.
    """
    tol = float(cfg.get("fusion.event_alignment.time_tolerance_s", 1.0))
    if run is not None:
        require_common_time(run)
    require_same_type = bool(cfg.get("fusion.event_alignment.require_same_type", True))
    subject_must_agree = bool(cfg.get("fusion.event_alignment.subject_must_agree", True))

    diagnostics: List[Dict[str, Any]] = []
    records: List[_Record] = []

    # An impact is mutual: settle both sides of it before keying anything, so a
    # vehicle struck from behind is not left guessing from a forward radar.
    aligned_events: Dict[str, List[Event]] = {}
    for pid in sorted(events_by_participant.keys()):
        evs = events_by_participant[pid]
        if run is not None and hasattr(run, "align_event") and participant_is_aligned(run, pid):
            evs = [run.align_event(pid, e) for e in evs]
        aligned_events[pid] = list(evs)
    mutual = reconcile_mutual_impacts(aligned_events, cfg, run, diagnostics)

    for pid in sorted(events_by_participant.keys()):
        events = events_by_participant[pid]
        if run is not None and hasattr(run, "align_event") and participant_is_aligned(run, pid):
            events = [run.align_event(pid, e) for e in events]
        for event in sorted(events, key=lambda e: (e.t_peak, e.event_id)):
            if event.event_type in ORACLE_ONLY_EVENT_TYPES:
                raise ValueError(
                    "privileged event type {0} reached the fusion layer (event {1!r})".format(
                        event.event_type.value, event.event_id
                    )
                )
            fam, relational = family_of(event.event_type, cfg)
            key, note = _subject_key(
                event, pid, relational, subject_map, cfg, run, diagnostics, mutual
            )
            records.append(
                _Record(
                    event=event,
                    participant_id=pid,
                    family=fam,
                    relational=relational,
                    key=key,
                    note=note,
                )
            )

    parent = list(range(len(records)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def compatible(i: int, j: int) -> bool:
        a, b = records[i], records[j]
        if a.participant_id == b.participant_id:
            return False
        if run is not None and not all(participant_is_aligned(run,p) for p in (a.participant_id,b.participant_id)):
            return False
        if require_same_type and a.family != b.family:
            return False
        if subject_must_agree:
            if a.key is None or b.key is None or a.key != b.key:
                return False
        if abs(float(a.event.t_peak) - float(b.event.t_peak)) > tol:
            return False
        return True

    pairs: List[Tuple[float, str, str, int, int]] = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            if compatible(i, j):
                dt = abs(float(records[i].event.t_peak) - float(records[j].event.t_peak))
                pairs.append(
                    (round(dt, 9), records[i].event.event_id, records[j].event.event_id, i, j)
                )
    # Best-first (closest in time) single-linkage merging with a validity check on
    # every union, so the result does not depend on input order.
    pairs.sort()

    members: Dict[int, List[int]] = {i: [i] for i in range(len(records))}
    for _dt, _id_i, _id_j, i, j in pairs:
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        if not _union_is_valid(members[ri], members[rj], compatible, records):
            diagnostics.append(
                {
                    "kind": "group_union_rejected",
                    "severity": "info",
                    "message": (
                        "events {0} and {1} are pairwise compatible but their groups "
                        "could not be merged without violating the one-event-per-"
                        "participant or time-tolerance constraint".format(_id_i, _id_j)
                    ),
                }
            )
            continue
        parent[rj] = ri
        members[ri] = members[ri] + members[rj]
        del members[rj]

    groups: List[EventGroup] = []
    for root in sorted(members.keys()):
        idx = sorted(members[root], key=lambda k: (records[k].event.t_peak, records[k].event.event_id))
        recs = [records[k] for k in idx]
        vehicles: List[str] = []
        for r in recs:
            for v in r.key or ():
                if v not in vehicles:
                    vehicles.append(v)
        t_peaks = [float(r.event.t_peak) for r in recs]
        groups.append(
            EventGroup(
                members=[r.event.event_id for r in recs],
                family=recs[0].family,
                vehicles=sorted(vehicles),
                relational=recs[0].relational,
                t_peak_min=min(t_peaks),
                t_peak_max=max(t_peaks),
                mergeable=recs[0].key is not None,
                note="; ".join(sorted({r.note for r in recs if r.note})),
            )
        )

    groups.sort(key=lambda g: (g.t_peak_min, g.members[0]))

    for g in groups:
        if g.size > 1:
            diagnostics.append(
                {
                    "kind": "events_merged",
                    "severity": "info",
                    "family": g.family,
                    "vehicles": list(g.vehicles),
                    "members": list(g.members),
                    "t_peak_spread_s": float(g.t_peak_max - g.t_peak_min),
                    "message": (
                        "{0} local events of family {1!r} about {2} were judged to be "
                        "one physical event".format(g.size, g.family, "+".join(g.vehicles))
                    ),
                }
            )

    return groups, diagnostics


def _union_is_valid(
    left: Sequence[int],
    right: Sequence[int],
    compatible: Any,
    records: Sequence[_Record],
) -> bool:
    """Whether two groups may merge: every cross pair must itself be compatible.

    Plain single-linkage would chain events transitively across a time span far
    wider than the tolerance, and could put two events of the same participant in
    one group. Checking all cross pairs keeps a group a genuine clique.
    """
    seen = {records[i].participant_id for i in left}
    for j in right:
        if records[j].participant_id in seen:
            return False
    for i in left:
        for j in right:
            if not compatible(i, j):
                return False
    return True


def _subject_key(
    event: Event,
    observer_id: str,
    relational: bool,
    subject_map: Mapping[str, str],
    cfg: Config,
    run: Optional[RunEvidence],
    diagnostics: List[Dict[str, Any]],
    mutual: Optional[Mapping[str, str]] = None,
) -> Tuple[Optional[Tuple[str, ...]], str]:
    """The physical subject of an event: which vehicles it makes a claim about.

    Returns ``(key, note)``; ``key is None`` marks an event that cannot be matched
    across participants because its subject track was never resolved to a
    participant. Such an event is kept -- as a singleton -- rather than merged on
    weaker grounds.
    """
    subject = event.subject
    subject_pid: Optional[str] = None

    if subject not in _SELF_SUBJECTS:
        subject_pid = subject_map.get(str(subject))
        if subject_pid is None:
            diagnostics.append(
                {
                    "kind": "unresolved_subject",
                    "severity": "warning",
                    "participant_id": observer_id,
                    "event_id": event.event_id,
                    "subject": str(subject),
                    "message": (
                        "event {0} concerns unresolved track {1!r}; it cannot be "
                        "matched against another participant's account".format(
                            event.event_id, subject
                        )
                    ),
                }
            )
            return None, "unresolved subject track {0!r}".format(subject)

    if not relational:
        return (subject_pid or observer_id,), ""

    if subject_pid is None and mutual:
        reciprocal = mutual.get(event.event_id)
        if reciprocal is not None and reciprocal != observer_id:
            return tuple(sorted({observer_id, reciprocal})), (
                "counterpart {0} established by mutual impact records".format(reciprocal)
            )

    if subject_pid is None:
        inferred, detail, verdict = _infer_counterpart(
            event, observer_id, subject_map, cfg, run
        )
        if inferred is None:
            diagnostics.append(
                {
                    "kind": (
                        "counterpart_ambiguous"
                        if verdict == "ambiguous"
                        else "counterpart_unknown"
                    ),
                    "severity": "warning",
                    "participant_id": observer_id,
                    "event_id": event.event_id,
                    "message": (
                        "relational event {0} of {1} names no counterpart and none "
                        "could be inferred from its own resolved tracks; it stays "
                        "unmerged ({2})".format(event.event_id, observer_id, detail)
                    ),
                }
            )
            return None, "counterpart {0}: {1}".format(verdict, detail)
        diagnostics.append(
            {
                "kind": "counterpart_inferred",
                "severity": "info",
                "participant_id": observer_id,
                "event_id": event.event_id,
                "counterpart": inferred,
                "message": detail,
            }
        )
        subject_pid = inferred

    return tuple(sorted({observer_id, subject_pid})), ""


def _position_at(evidence: Any, t: float, max_gap_s: float) -> Optional[Tuple[float, float]]:
    """A participant's own position at common time ``t``, or None if not covered.

    Linear interpolation between the two bracketing telemetry samples; a gap
    wider than ``max_gap_s`` yields None rather than an extrapolation.
    """
    samples = getattr(evidence, "telemetry", None) or []
    if not samples:
        return None
    before = None
    after = None
    for sample in samples:
        ts = float(sample.t)
        if ts <= t and (before is None or ts > float(before.t)):
            before = sample
        if ts >= t and (after is None or ts < float(after.t)):
            after = sample
    if before is None and after is None:
        return None
    if before is None:
        return (float(after.x), float(after.y)) if abs(float(after.t) - t) <= max_gap_s else None
    if after is None:
        return (float(before.x), float(before.y)) if abs(float(before.t) - t) <= max_gap_s else None
    if before is after:
        return (float(before.x), float(before.y)) if abs(float(before.t) - t) <= max_gap_s else None
    span = float(after.t) - float(before.t)
    if span > max_gap_s:
        return None
    frac = 0.0 if span <= 0.0 else (t - float(before.t)) / span
    return (
        float(before.x) + frac * (float(after.x) - float(before.x)),
        float(before.y) + frac * (float(after.y) - float(before.y)),
    )


def _telemetry_ranges(
    observer_id: str,
    t: float,
    run: Optional[RunEvidence],
    max_gap_s: float,
) -> Dict[str, float]:
    """Distance from the observer to every other participant at common time ``t``.

    This is evidence only fusion has. A vehicle's own radar cannot see what is
    behind it, so an impact from the rear is unattributable from one log alone --
    but every participant exported its own trajectory, and once the clocks are
    aligned those trajectories answer the question directly. Nothing privileged
    is consulted: these are the participants' own recorded positions.
    """
    if run is None or observer_id not in getattr(run, "participants", {}):
        return {}
    if not participant_is_aligned(run, observer_id):
        return {}
    own = _position_at(run.get(observer_id), t, max_gap_s)
    if own is None:
        return {}
    out: Dict[str, float] = {}
    for pid in run.participant_ids:
        if pid == observer_id or not participant_is_aligned(run, pid):
            continue
        other = _position_at(run.get(pid), t, max_gap_s)
        if other is None:
            continue
        out[pid] = float(
            ((own[0] - other[0]) ** 2 + (own[1] - other[1]) ** 2) ** 0.5
        )
    return out


def reconcile_mutual_impacts(
    events_by_participant: Mapping[str, Sequence[Event]],
    cfg: Config,
    run: Optional[RunEvidence],
    diagnostics: List[Dict[str, Any]],
) -> Dict[str, str]:
    """Pair up the two sides of the same impact, and name each side's counterpart.

    An impact is *mutual*: it is recorded by both vehicles involved, at the same
    instant, and at that instant they are touching. A single onboard collision
    sensor reports only that something was hit, and a forward radar cannot see a
    vehicle that struck from behind -- so from one log the counterpart may be
    genuinely unknowable. Two logs on a common clock settle it.

    Candidate pairings are scored on how close the two records are in time and
    how close the two vehicles were in space, and matched best-first so that each
    collision record is used at most once. A record left unmatched keeps whatever
    its own evidence supports; nothing is forced.

    Returns ``{event_id: counterpart participant id}``.
    """
    tol = float(cfg.get("fusion.event_alignment.mutual_impact_tolerance_s", 0.5))
    max_gap_s = float(cfg.get("fusion.event_alignment.counterpart_max_time_gap_s", 0.5))
    contact_m = float(cfg.get("fusion.event_alignment.mutual_impact_max_distance_m", 12.0))

    records: List[Tuple[str, str, float]] = []
    for pid in sorted(events_by_participant.keys()):
        if run is not None and not participant_is_aligned(run, pid):
            continue
        for event in events_by_participant[pid]:
            if event.event_type is not EventType.COLLISION:
                continue
            records.append((event.event_id, pid, float(event.t_peak)))
    if len(records) < 2:
        return {}

    candidates: List[Tuple[float, float, str, str, str, str]] = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            eid_a, pid_a, t_a = records[i]
            eid_b, pid_b, t_b = records[j]
            if pid_a == pid_b:
                continue
            dt = abs(t_a - t_b)
            if dt > tol:
                continue
            midpoint = 0.5 * (t_a + t_b)
            ranges = _telemetry_ranges(pid_a, midpoint, run, max_gap_s)
            distance = ranges.get(pid_b)
            if distance is None:
                # Without exchanged positions the pairing rests on time alone;
                # allow it but rank it behind every distance-supported pairing.
                distance = contact_m
            elif distance > contact_m:
                continue
            candidates.append((round(dt, 9), round(distance, 6), eid_a, eid_b, pid_a, pid_b))

    candidates.sort()

    # Reciprocity settles an impact only when it singles one partner out. Three
    # vehicles that all record an impact at the same instant, all equally close,
    # are not reconciled by a tie-break: that would let measurement noise decide
    # which pair the fused COLLISION node names. The same discipline as
    # `_infer_counterpart`, applied to the pairing rather than to the range.
    margin_m = float(
        cfg.get("fusion.event_alignment.counterpart_ambiguity_margin_m", 1.0)
    )
    margin_s = float(
        cfg.get("fusion.event_alignment.mutual_impact_ambiguity_dt_s", 0.1)
    )
    by_event: Dict[str, List[Tuple[float, float, str]]] = {}
    for dt, distance, eid_a, eid_b, pid_a, pid_b in candidates:
        by_event.setdefault(eid_a, []).append((dt, distance, pid_b))
        by_event.setdefault(eid_b, []).append((dt, distance, pid_a))

    def decisive(event_id: str, partner: str) -> Tuple[bool, str]:
        """Whether this event's best partner is distinguishable from the next.

        Two records of one impact coincide in *time* and in *space*, and either
        axis can settle the question alone: a rival half a second away is not the
        same impact however close it stood, and a rival ten metres away is not
        the same impact however well the timestamps agree. Only when neither
        separates them is the pairing a guess.
        """
        ranked = sorted(by_event.get(event_id, []))
        rivals = [row for row in ranked if row[2] != partner]
        if not rivals:
            return True, ""
        best = next(row for row in ranked if row[2] == partner)
        rival = rivals[0]
        if (rival[0] - best[0]) >= margin_s or (rival[1] - best[1]) >= margin_m:
            return True, ""
        return False, (
            "{0} ({1:.3f}s, {2:.3f}m) and {3} ({4:.3f}s, {5:.3f}m) are "
            "indistinguishable as the other side of this impact, in time and in "
            "range alike (counterpart_ambiguity_margin_m={6}m, "
            "mutual_impact_ambiguity_dt_s={7}s); naming either would be a "
            "guess".format(
                partner, best[0], best[1], rival[2], rival[0], rival[1],
                margin_m, margin_s,
            )
        )

    used: set = set()
    resolved: Dict[str, str] = {}
    for dt, distance, eid_a, eid_b, pid_a, pid_b in candidates:
        if eid_a in used or eid_b in used:
            continue
        ok_a, why_a = decisive(eid_a, pid_b)
        ok_b, why_b = decisive(eid_b, pid_a)
        if not (ok_a and ok_b):
            diagnostics.append(
                {
                    "kind": "mutual_impact_ambiguous",
                    "severity": "warning",
                    "participants": [pid_a, pid_b],
                    "events": [eid_a, eid_b],
                    "message": why_a or why_b,
                }
            )
            used.add(eid_a)
            used.add(eid_b)
            continue
        used.add(eid_a)
        used.add(eid_b)
        resolved[eid_a] = pid_b
        resolved[eid_b] = pid_a
        diagnostics.append(
            {
                "kind": "mutual_impact_reconciled",
                "severity": "info",
                "participants": [pid_a, pid_b],
                "events": [eid_a, eid_b],
                "dt_s": dt,
                "distance_m": distance,
                "message": (
                    "{0} and {1} each recorded an impact {2:.3f}s apart on the "
                    "common clock and were {3:.2f}m apart; they are two accounts "
                    "of one impact".format(pid_a, pid_b, dt, distance)
                ),
            }
        )
    return resolved


def _infer_counterpart(
    event: Event,
    observer_id: str,
    subject_map: Mapping[str, str],
    cfg: Config,
    run: Optional[RunEvidence],
) -> Tuple[Optional[str], str, str]:
    """Name the other party of an own-recorded relational event, or give up.

    An onboard collision sensor reports *that* an impact happened, never *with
    whom* -- that is the whole point of the local evidence boundary. The other
    party can still be named legitimately: take the observer's own radar tracks
    that the association stage already resolved to a participant, and pick the one
    that was closest at the moment of the event. Everything used here is the
    observer's own evidence plus the association result; no privileged data.

    Proximity alone is only *decisive evidence* when it actually singles one
    participant out. Two resolved tracks a few centimetres apart at the moment of
    impact are not distinguishable by range, and naming the nearer of the two
    would let a millimetre of measurement noise decide which vehicle the fused
    collision node accuses. So this follows the same discipline as
    :func:`cdf.fusion.track_association.associate_tracks`: when the runner-up lies
    within ``fusion.event_alignment.counterpart_ambiguity_margin_m`` of the best
    candidate, no counterpart is named at all and the event stays unmerged with an
    explicit ``counterpart_ambiguous`` diagnostic.

    Returns ``(participant_id, explanation, verdict)`` where ``verdict`` is one of
    ``"inferred"``, ``"ambiguous"`` or ``"unknown"``; ``participant_id`` is
    ``None`` for anything but ``"inferred"``.
    """
    # None of these keys exists in configs/default.yaml -- reported as a contract
    # issue. The ambiguity margin is vehicle-scale: two candidate counterparts
    # whose ranges differ by less than a car length are not told apart by range.
    max_gap_s = float(cfg.get("fusion.event_alignment.counterpart_max_time_gap_s", 0.5))
    max_range_m = float(cfg.get("fusion.event_alignment.counterpart_max_range_m", 8.0))
    ambiguity_margin_m = float(
        cfg.get("fusion.event_alignment.counterpart_ambiguity_margin_m", 1.0)
    )

    if run is None or observer_id not in run.participants:
        return None, "no local evidence available for {0}".format(observer_id), "unknown"

    ev = run.get(observer_id)
    # Best (smallest) range per candidate *participant*: two tracks of the same
    # observer that resolved to one participant are one hypothesis, not two.
    by_participant: Dict[str, float] = {}
    for track_id in ev.track_ids():
        pid = subject_map.get(track_id)
        if pid is None or pid == observer_id:
            continue
        nearest = None
        nearest_dt = float("inf")
        for s in ev.tracks:
            if s.track_id != track_id:
                continue
            dt = abs(float(s.t) - float(event.t_peak))
            if dt < nearest_dt:
                nearest, nearest_dt = s, dt
        if nearest is None or nearest_dt > max_gap_s:
            continue
        rng = float(nearest.range_m)
        if rng <= 0.0:
            rng = float((nearest.rel_x ** 2 + nearest.rel_y ** 2) ** 0.5)
        if rng > max_range_m:
            continue
        if pid not in by_participant or rng < by_participant[pid]:
            by_participant[pid] = rng

    # Second evidence source, available only after fusion: the other
    # participants' own exported trajectories on the common clock. A rear impact
    # is invisible to a forward radar but obvious in the exchanged telemetry.
    source: Dict[str, str] = {pid: "own_radar_track" for pid in by_participant}
    for pid, distance in _telemetry_ranges(
        observer_id, float(event.t_peak), run, max_gap_s
    ).items():
        if distance > max_range_m:
            continue
        if pid not in by_participant or distance < by_participant[pid]:
            by_participant[pid] = distance
            source[pid] = (
                "exchanged_telemetry" if pid not in source else "radar+telemetry"
            )

    if not by_participant:
        return (
            None,
            "no resolved track and no exchanged trajectory was within {0}m at "
            "t={1:.3f}s".format(max_range_m, float(event.t_peak)),
            "unknown",
        )

    ranked = sorted(by_participant.items(), key=lambda kv: (kv[1], kv[0]))
    best_pid, best_range = ranked[0]
    if len(ranked) > 1:
        runner_pid, runner_range = ranked[1]
        if (runner_range - best_range) < ambiguity_margin_m:
            return (
                None,
                (
                    "{0} at {1:.3f}m and {2} at {3:.3f}m are indistinguishable by "
                    "range at t={4:.3f}s (margin {5:.3f}m < "
                    "fusion.event_alignment.counterpart_ambiguity_margin_m={6}m); "
                    "naming either would be a guess".format(
                        best_pid,
                        best_range,
                        runner_pid,
                        runner_range,
                        float(event.t_peak),
                        runner_range - best_range,
                        ambiguity_margin_m,
                    )
                ),
                "ambiguous",
            )

    return (
        best_pid,
        "counterpart {0} inferred from {1} at {2:.2f}m at t={3:.3f}s".format(
            best_pid, source.get(best_pid, "own track"), best_range, float(event.t_peak)
        ),
        "inferred",
    )
