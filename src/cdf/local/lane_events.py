"""Road markings the vehicle crossed, from an onboard lane sensor.

The supervisor asked specifically for evidence of the kind "this vehicle crossed
a line", and CARLA offers a lane-invasion sensor that reports exactly that,
including which sort of marking was crossed. The brief permits using it as a
simulated onboard ADAS signal, which is what it is treated as here -- the same
standing as radar. It is not the map: the map would say which lane the vehicle is
in and where the lane goes, and nothing here asks either.

The problem worth solving
-------------------------

The sensor fires on crossing, and a vehicle changing lanes straddles the line for
most of a second. At 20 Hz that is a dozen or more events for one crossing, and
each would become a node. The reference has one. So the whole job of this module
is deduplication: collapse a burst of reports of the same marking into the single
crossing it was, and keep the distinct crossings distinct.

Two crossings of the *same* kind a second apart are two crossings -- that is a
lane change and then another lane change. Two reports of the same kind 50 ms apart
are one. The boundary between those is a configured window, and the price of
setting it too wide is a missed second crossing rather than a phantom one, which
is the direction to err in.

What the marking type means
---------------------------

CARLA's marking types map onto three claims a reconstruction can make. A solid
line crossed is also a marking crossed -- the solid-line event is the more
specific claim and both are emitted, because the normative layer cares about the
specific one and the physical layer cares about the general one.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import Event, EventType, Evidence, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = [
    "MARKING_KINDS",
    "lane_events_from_records",
    "build_lane_events",
]

#: How CARLA's marking types map onto what a reconstruction asserts. Lowercased
#: on lookup, so the CARLA enum's spelling does not have to be guessed exactly.
MARKING_KINDS: Dict[str, str] = {
    "solid": "solid",
    "solidsolid": "solid",
    "solidbroken": "solid",
    "brokensolid": "solid",
    "broken": "broken",
    "brokenbroken": "broken",
    "bottsdots": "broken",
    "curb": "boundary",
    "grass": "boundary",
    # Deliberately absent: "none" and "other". A marking the sensor could not
    # classify is recorded as a generic crossing rather than guessed at.
}

_EVENT_FOR_KIND: Dict[str, Tuple[EventType, ...]] = {
    "solid": (EventType.SOLID_LINE_CROSSED, EventType.LANE_MARKING_CROSSED),
    "broken": (EventType.LANE_MARKING_CROSSED,),
    "boundary": (EventType.ROAD_BOUNDARY_CROSSED,),
    "unclassified": (EventType.LANE_MARKING_CROSSED,),
}


def _kind_of(marking_type: Any) -> str:
    text = str(marking_type or "").strip().lower()
    # CARLA renders the enum as "LaneMarkingType.Solid"; take the last part.
    if "." in text:
        text = text.rsplit(".", 1)[-1]
    return MARKING_KINDS.get(text, "unclassified")


def lane_events_from_records(
    records: Sequence[Mapping[str, Any]],
    cfg: Optional[Config] = None,
) -> List[Dict[str, Any]]:
    """Collapse a burst of invasion reports into the crossings they represent.

    Each returned entry is one crossing: its kind, when it began, how many raw
    reports it absorbed, and the marking types seen during it.
    """
    cfg = cfg if cfg is not None else Config({})
    window = float(cfg.get("perception.lanes.merge_window_s", 0.8))

    crossings: List[Dict[str, Any]] = []
    for record in sorted(records, key=lambda r: float(r.get("t", 0.0))):
        t = float(record.get("t", 0.0))
        types = record.get("marking_types") or []
        if not types:
            types = ["unclassified"]
        for marking_type in types:
            kind = _kind_of(marking_type)
            open_crossing = next(
                (
                    c for c in reversed(crossings)
                    if c["kind"] == kind and t - c["t_last"] <= window
                ),
                None,
            )
            if open_crossing is not None:
                open_crossing["t_last"] = t
                open_crossing["n_reports"] += 1
                if str(marking_type) not in open_crossing["marking_types"]:
                    open_crossing["marking_types"].append(str(marking_type))
                continue
            crossings.append({
                "kind": kind,
                "t_first": t,
                "t_last": t,
                "n_reports": 1,
                "marking_types": [str(marking_type)],
                "frame": int(record.get("frame", 0) or 0),
            })
    return crossings


def build_lane_events(
    participant_id: str,
    records: Sequence[Mapping[str, Any]],
    cfg: Optional[Config] = None,
    id_prefix: str = "lane",
) -> Dict[str, Any]:
    """Turn raw lane-invasion reports into deduplicated local events."""
    cfg = cfg if cfg is not None else Config({})
    crossings = lane_events_from_records(records, cfg)

    events: List[Event] = []
    for index, crossing in enumerate(crossings):
        for event_type in _EVENT_FOR_KIND[crossing["kind"]]:
            events.append(Event(
                event_id="{0}-{1}-{2}-{3}".format(
                    id_prefix, participant_id, index,
                    event_type.value.split("_")[0].lower(),
                ),
                event_type=event_type,
                participant_id=str(participant_id),
                t_start=crossing["t_first"],
                t_peak=crossing["t_first"],
                t_end=crossing["t_last"],
                subject=None,
                values={
                    "straddle_s": round(
                        crossing["t_last"] - crossing["t_first"], 4
                    ),
                },
                detail={
                    "marking_kind": crossing["kind"],
                    "marking_types_reported": crossing["marking_types"],
                    "n_sensor_reports_merged": crossing["n_reports"],
                    "sensor": "onboard lane-invasion sensor, treated as a "
                              "simulated ADAS signal",
                },
                confidence=1.0 if crossing["kind"] != "unclassified" else 0.6,
                evidence=[Evidence(
                    kind="trigger",
                    ref="lane_invasion#{0}".format(index),
                    t_start=crossing["t_first"],
                    t_end=crossing["t_last"],
                    detail={"n_reports": crossing["n_reports"]},
                )],
                provenance=Provenance.LOCAL,
                source_sensors=["lane"],
            ))

    events.sort(key=lambda e: (float(e.t_peak), e.event_id))
    return {
        "participant_id": str(participant_id),
        "n_raw_reports": len(records),
        "n_crossings": len(crossings),
        "n_events": len(events),
        "crossings": crossings,
        "events": events,
        "merge_window_s": float(cfg.get("perception.lanes.merge_window_s", 0.8)),
        "note": (
            "the sensor reports on every tick a marking is being straddled, so "
            "raw reports are collapsed into crossings. A solid line crossed "
            "yields both the specific and the general event: the normative layer "
            "needs the first and the physical layer the second"
        ),
    }
