"""The recorder's perceived semantic state over time, from its own evidence only.

Every state variable is a timeline whose value is True, False or UNKNOWN:

  True / False  established from this recorder's own evidence
  UNKNOWN       the recorder cannot establish it: before its first observation,
                without the needed context, or after the subject was lost

A value holds from the sample where it was established until evidence changes
it, so the events are exactly the transitions of a variable into and out of
True.  Losing
sight of a subject (TRACK_LOST) moves its states to UNKNOWN; that is not an
END and no END is invented for it.

``snapshot(t, before=True)`` is the state just BEFORE ``t``: none of the
transitions at ``t`` are applied, so every event at one timestamp shares it.
``snapshot(t, before=False)`` includes the transitions at ``t`` (the state after
them), as stored in each trace frame.  External subjects keep their local
names (``track_001``, ``sign-0``): no global identity enters a local state.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from typing import Any, Dict, List, Optional, Sequence, Tuple

UNKNOWN = "UNKNOWN"
EGO_STATES = ("MOVING", "STOP", "BRAKE", "HARD_BRAKE", "STRONG_THROTTLE", "SPEED_LIMIT_EXCEEDED")
TRACK_STATES = ("CLOSING", "CRITICAL_TTC", "IN_EGO_PATH")
_EPS = 1e-6

Span = Tuple[int, Optional[int]]


class Timeline:
    """A piecewise-constant value given by (time, value) change points."""

    def __init__(self) -> None:
        self.times: List[float] = []
        self.values: List[Any] = []

    def set(self, t: float, value: Any) -> None:
        if self.times and t < self.times[-1] - _EPS:
            raise ValueError("timeline changes must be set in time order")
        if self.times and abs(self.times[-1] - t) < _EPS:
            self.values[-1] = value  # a later setting at the same instant wins
            if len(self.values) > 1 and self.values[-2] == value:
                self.times.pop()
                self.values.pop()
            return
        if self.values and self.values[-1] == value:
            return
        self.times.append(float(t))
        self.values.append(value)

    def value(self, t: float, before: bool = True) -> Any:
        """The value just before ``t`` (or at ``t``, transitions at ``t`` included); None if not yet set."""
        index = (bisect_left(self.times, t - _EPS) if before else bisect_right(self.times, t + _EPS)) - 1
        return None if index < 0 else self.values[index]


def timeline_from_samples(times: Sequence[float], values: Sequence[Any]) -> Timeline:
    timeline = Timeline()
    for t, value in zip(times, values):
        timeline.set(t, value)
    return timeline


def span_values(count: int, spans: Sequence[Span]) -> List[Any]:
    """Per-sample True inside a span and False outside."""
    values: List[Any] = [False] * count
    for start, end in spans:
        for index in range(start, count if end is None else end):
            values[index] = True
    return values


def _json(value: Any) -> Any:
    return UNKNOWN if value is None else value


class PerceivedWorld:
    """Timelines of one recorder: its own states, its radar tracks and its signs."""

    def __init__(self) -> None:
        self.ego: Dict[str, Timeline] = {}
        self.tracks: Dict[str, Dict[str, Timeline]] = {}
        self.track_first: Dict[str, float] = {}
        self.signs: Dict[str, Dict[str, Any]] = {}

    # -- registration ------------------------------------------------------------

    def add_ego_state(self, name: str, times: Sequence[float], spans: Sequence[Span]) -> None:
        self.ego[name] = timeline_from_samples(times, span_values(len(times), spans))

    def add_ego_unknown(self, name: str, t: float) -> None:
        timeline = Timeline()
        timeline.set(t, UNKNOWN)
        self.ego[name] = timeline

    def add_track(self, track_id: str, times: Sequence[float], states: Dict[str, Sequence[Any]],
                  lost_at: Optional[float]) -> None:
        """Per-sample state values of one track; after ``lost_at`` everything is UNKNOWN."""
        timelines = {"visible": timeline_from_samples(times, [True] * len(times))}
        for name, values in states.items():
            timelines[name] = timeline_from_samples(times, values)
        if lost_at is not None:
            # From the TRACK_LOST instant on, nothing about the track is observable.
            timelines["visible"].set(lost_at, False)
            for name in states:
                timelines[name].set(lost_at, UNKNOWN)
        self.tracks[track_id] = timelines
        self.track_first[track_id] = float(times[0])

    def add_sign_window(self, sign_id: str, sign_class: str, start: float, end: Optional[float],
                        relevant: Optional[bool]) -> None:
        sign = self.signs.setdefault(sign_id, {"class": sign_class, "visible": Timeline(), "relevant": Timeline(),
                                               "first": start})
        sign["first"] = min(sign["first"], start)
        sign["visible"].set(start, True)
        sign["relevant"].set(start, UNKNOWN if relevant is None else bool(relevant))
        if end is not None:
            sign["visible"].set(end, False)

    # -- queries --------------------------------------------------------------------

    def snapshot(self, t: float, before: bool = True) -> Dict[str, Any]:
        def seen(first: float) -> bool:
            return first < t - _EPS if before else first <= t + _EPS

        ego = {name: _json(self.ego[name].value(t, before)) for name in EGO_STATES if name in self.ego}
        external: Dict[str, Any] = {}
        for track_id in sorted(self.tracks):
            if not seen(self.track_first[track_id]):
                continue
            timelines = self.tracks[track_id]
            state = {"visible": bool(timelines["visible"].value(t, before))}
            for name in TRACK_STATES:
                if name in timelines:
                    state[name] = _json(timelines[name].value(t, before))
            external[track_id] = state
        signs: Dict[str, Any] = {}
        for sign_id in sorted(self.signs):
            sign = self.signs[sign_id]
            if not seen(sign["first"]):
                continue
            # Known: perceived at some point and remembered.  No admissible local
            # evidence tells when the controlled point has been passed, so the
            # knowledge is never cleared here.
            signs[sign_id] = {"class": sign["class"], "visible": bool(sign["visible"].value(t, before)),
                              "known": True, "relevant_to_ego_path": _json(sign["relevant"].value(t, before))}
        return {"ego": ego, "external": external, "signs": signs}


def compact_state(snapshot: Optional[Dict[str, Any]]) -> List[str]:
    """Short human-readable lines: true states by name, unknown ones with '?',
    false ones omitted, lost tracks on one line."""
    if not snapshot:
        return []
    lines = []
    ego = snapshot.get("ego", {})
    if ego and all(value == UNKNOWN for value in ego.values()):
        lines.append("ego: not yet observed")
    elif ego:
        true = [name for name, value in ego.items() if value is True]
        unknown = [name + "?" for name, value in ego.items() if value == UNKNOWN and name != "SPEED_LIMIT_EXCEEDED"]
        lines.append("ego: " + (", ".join(true + unknown) or "no active state"))
    lost = []
    for track_id, state in snapshot.get("external", {}).items():
        if not state.get("visible"):
            lost.append(track_id)
            continue
        names = [(name, state.get(name)) for name in TRACK_STATES]
        shown = [name for name, value in names if value is True] + [name + "?" for name, value in names if value == UNKNOWN]
        lines.append("{0}: VISIBLE{1}".format(track_id, "".join(", " + item for item in shown)))
    if lost:
        lines.append("lost (states UNKNOWN): " + ", ".join(lost))
    for sign_id, sign in snapshot.get("signs", {}).items():
        lines.append("{0}: {1} sign {2}, known{3}".format(
            sign_id, sign.get("class"), "VISIBLE" if sign.get("visible") else "not visible",
            "" if sign.get("relevant_to_ego_path") is not True else ", relevant to the path"))
    return lines
