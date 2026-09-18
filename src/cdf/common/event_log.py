"""The readable table that comes before any graph.

A causal DAG is the thing this project is *for*, but it is not the thing a
reader can check. A supervisor asked what happened; the honest answer is a list
of timestamped facts in order, and only then a claim about which of them led to
which. So every account -- each vehicle's own, and the merged one -- is written
first as a log::

    5.20  B    STOP_SIGN_DETECTED              camera      conf 0.94
    5.74  B    BRAKE_ONSET                     controls    -
    6.00  B    FULL_STOP                       telemetry   -
    7.11  A    CONFLICT_REGION_ENTRY    (B)    radar       -
    8.77  A-B  COLLISION                       contact     impulse 4.2e3

Two columns carry the whole clock story. ``t_local`` is what the recorder's own
clock said and always exists. ``t_common`` exists only once a shared contact has
tied the recorders together; where there was no contact it stays ``None`` and
the merged log says so in as many words, rather than quietly falling back on
simulator time. :mod:`cdf.fusion.contact_alignment` explains why that matters.

Ordering is deterministic and total, so two runs of the same pipeline produce
identical logs: time first, then participant, subject, type and event id. Ties
are broken by id rather than left to sort stability, because a log that reorders
between runs cannot be diffed.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from .schemas import SCHEMA_VERSIONS, Event, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = [
    "LOG_COLUMNS",
    "build_local_log",
    "build_global_log",
    "log_rows",
    "format_log",
]

#: The columns of a log row, in the order a reader should meet them.
LOG_COLUMNS: Tuple[str, ...] = (
    "t_local",
    "t_common",
    "participant",
    "subject",
    "event_type",
    "source_sensor",
    "confidence",
    "values",
    "evidence",
)


def _type_of(event: Event) -> str:
    return (
        event.event_type.value if hasattr(event.event_type, "value")
        else str(event.event_type)
    )


def _evidence_summary(event: Event, limit: int = 3) -> str:
    """A one-line trace back to the samples the event was read from.

    Deliberately short. The full evidence records stay in ``events.json``; this
    column exists so a reader scanning the table can see *what kind* of thing
    supports a row without opening anything.
    """
    parts: List[str] = []
    for ev in (event.evidence or [])[:limit]:
        ref = str(getattr(ev, "ref", "") or "")
        kind = str(getattr(ev, "kind", "") or "")
        parts.append("{0}:{1}".format(kind, ref) if ref else kind)
    extra = len(event.evidence or []) - len(parts)
    if extra > 0:
        parts.append("+{0} more".format(extra))
    return " ".join(p for p in parts if p)


def _sensors(event: Event) -> str:
    return ",".join(sorted(str(s) for s in (event.source_sensors or []))) or "derived"


def _row(event: Event, t_common: Optional[float]) -> Dict[str, Any]:
    return {
        "event_id": event.event_id,
        "t_local": round(float(event.t_peak), 4),
        "t_common": None if t_common is None else round(float(t_common), 4),
        "participant": str(event.participant_id),
        "subject": str(event.subject) if event.subject else "",
        "event_type": _type_of(event),
        "source_sensor": _sensors(event),
        "confidence": round(float(event.confidence), 4),
        "values": {
            k: round(float(v), 4) for k, v in sorted((event.values or {}).items())
        },
        "evidence": _evidence_summary(event),
        "t_start": round(float(event.t_start), 4),
        "t_end": None if event.t_end is None else round(float(event.t_end), 4),
        "detail": dict(event.detail or {}),
    }


def _sort_key(row: Mapping[str, Any]) -> Tuple[Any, ...]:
    """A total order, so the same events always produce the same log.

    Rows without a common time sort after rows that have one *at the same
    numeric time*, which only arises in a partially aligned run; within either
    group the remaining fields decide, and the event id guarantees no tie is
    left to sort stability.
    """
    t_common = row.get("t_common")
    return (
        float(row["t_local"]) if t_common is None else float(t_common),
        0 if t_common is not None else 1,
        str(row["participant"]),
        str(row["subject"]),
        str(row["event_type"]),
        str(row["event_id"]),
    )


def log_rows(
    events: Sequence[Event],
    to_common: Optional[Mapping[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Rows for these events, in deterministic order.

    ``to_common`` maps a participant id to something callable that converts that
    participant's local time to common time. A participant absent from the
    mapping is treated as unaligned, which is the safe direction: the row still
    appears, with an empty common time.
    """
    rows: List[Dict[str, Any]] = []
    for event in events:
        t_common: Optional[float] = None
        convert = (to_common or {}).get(str(event.participant_id))
        if convert is not None:
            try:
                t_common = float(convert(float(event.t_peak)))
            except (TypeError, ValueError):  # pragma: no cover - defensive
                LOGGER.warning(
                    "could not map %s to common time for %s",
                    event.event_id, event.participant_id,
                )
                t_common = None
        rows.append(_row(event, t_common))
    rows.sort(key=_sort_key)
    return rows


def build_local_log(
    participant_id: str,
    events: Sequence[Event],
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> Dict[str, Any]:
    """One vehicle's account of the incident, on its own clock.

    There is no common-time column here by construction: a vehicle alone has no
    way to know what another recorder's clock said, and a local log that carried
    common time would be claiming knowledge the vehicle does not have.
    """
    rows = log_rows(list(events))
    for row in rows:
        row.pop("t_common", None)
    by_type: Dict[str, int] = {}
    for row in rows:
        by_type[row["event_type"]] = by_type.get(row["event_type"], 0) + 1
    return {
        "schema_version": SCHEMA_VERSIONS["events"],
        "log_kind": "local",
        "provenance": Provenance.LOCAL.value,
        "participant_id": str(participant_id),
        "run_id": run_id,
        "scenario_id": scenario_id,
        "seed": int(seed),
        "clock": (
            "participant-local; this vehicle has no access to any other "
            "recorder's clock"
        ),
        "columns": [c for c in LOG_COLUMNS if c != "t_common"],
        "n_rows": len(rows),
        "counts_by_type": dict(sorted(by_type.items())),
        "rows": rows,
    }


def build_global_log(
    events: Sequence[Event],
    alignment: Optional[Mapping[str, Any]] = None,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> Dict[str, Any]:
    """The merged account, on common time where common time exists.

    ``alignment`` is the contact-alignment result. Participants it could align
    get a common time; participants it could not keep only their local time and
    are named in ``unaligned_participants``, so a reader of the table can see
    which rows are not on the same axis as the rest.
    """
    alignment = alignment or {}
    # Prefer the published offsets over any callables handed in: the log then
    # shows exactly the transform the alignment artifact states, and cannot drift
    # from it. `converters` remains accepted so a test can supply one directly.
    converters = dict(alignment.get("converters") or {})
    for pid, offset in (alignment.get("offsets_s") or {}).items():
        converters[str(pid)] = (lambda t, _o=float(offset): float(t) + _o)
    rows = log_rows(list(events), to_common=converters)

    aligned = sorted({
        r["participant"] for r in rows if r.get("t_common") is not None
    })
    # Also from the alignment, not only from the rows. A recorder that could not
    # be tied in often contributes no rows at all -- fusion has nowhere to put
    # its events -- and a log that derived this from the rows alone would then
    # report a clean single timeline while quietly omitting a whole vehicle.
    # "C's events are missing from this table" is exactly what a reader needs.
    unaligned = sorted(
        {r["participant"] for r in rows if r.get("t_common") is None}
        | {str(p) for p in (alignment.get("unaligned_participants") or [])}
    )
    aligned = [p for p in aligned if p not in set(unaligned)]
    by_type: Dict[str, int] = {}
    for row in rows:
        by_type[row["event_type"]] = by_type.get(row["event_type"], 0) + 1

    status = str(alignment.get("status") or "UNALIGNED_NO_SHARED_CONTACT")
    return {
        "schema_version": SCHEMA_VERSIONS["events"],
        "log_kind": "global",
        "provenance": Provenance.FUSED.value,
        "run_id": run_id,
        "scenario_id": scenario_id,
        "seed": int(seed),
        "alignment_status": status,
        "reference_participant": alignment.get("reference"),
        "aligned_participants": aligned,
        "unaligned_participants": unaligned,
        "common_time_available": bool(aligned) and not unaligned,
        "columns": list(LOG_COLUMNS),
        "n_rows": len(rows),
        "counts_by_type": dict(sorted(by_type.items())),
        "participants_with_no_rows": sorted(
            set(unaligned) - {r["participant"] for r in rows}
        ),
        "note": (
            "common time comes from shared physical contact between recorders. "
            "Where no contact tied a recorder to the rest, its rows keep only "
            "local time and it is named in unaligned_participants; simulator "
            "time is never used as a fallback"
        ),
        "rows": rows,
    }


def format_log(log: Mapping[str, Any], limit: Optional[int] = None) -> str:
    """The log as aligned plain text, for a console or a report.

    Uses common time when the log has it and local time otherwise, and says
    which in the header, so a pasted excerpt is never ambiguous about its axis.
    """
    rows = list(log.get("rows") or [])
    if limit is not None:
        rows = rows[:limit]
    use_common = any(r.get("t_common") is not None for r in rows)
    header = "{0:>8}  {1:<6} {2:<38} {3:<12} {4}".format(
        "t_common" if use_common else "t_local", "who", "event", "sensor", "detail",
    )
    lines = [header]
    for row in rows:
        t = row.get("t_common") if use_common else row.get("t_local")
        who = row["participant"]
        if row.get("subject"):
            who = "{0}-{1}".format(who, row["subject"])
        values = " ".join(
            "{0}={1:g}".format(k, v) for k, v in (row.get("values") or {}).items()
        )
        lines.append("{0:>8}  {1:<6} {2:<38} {3:<12} {4}".format(
            "--" if t is None else "{0:.2f}".format(float(t)),
            who,
            row["event_type"],
            row.get("source_sensor", ""),
            values or row.get("evidence", ""),
        ))
    total = len(log.get("rows") or [])
    if limit is not None and total > limit:
        lines.append("... {0} more rows".format(total - limit))
    return "\n".join(lines)
