"""The minimal semantic vocabulary given to an LLM (``configs/semantic_vocabulary.yaml``)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ..common.config import configs_dir

SUBJECT_KINDS = ("none", "road_user", "sign")


@dataclass(frozen=True)
class EventType:
    name: str
    description: str
    actor: str
    subject: str
    note: str = ""


@dataclass(frozen=True)
class Vocabulary:
    version: int
    events: Tuple[EventType, ...]
    states: Dict[str, Tuple[str, str]]

    @property
    def event_names(self) -> List[str]:
        return [event.name for event in self.events]

    @property
    def state_names(self) -> List[str]:
        return sorted(self.states)

    def event(self, name: str) -> Optional[EventType]:
        return next((event for event in self.events if event.name == name), None)

    def state_of(self, event_name: str) -> Optional[Tuple[str, bool]]:
        """(state, True for the opening event / False for the closing one), or None."""
        for state, (start, end) in self.states.items():
            if event_name == start:
                return state, True
            if event_name == end:
                return state, False
        return None

    def subject_kind_of_state(self, state: str) -> str:
        return self.event(self.states[state][0]).subject

    def render(self) -> str:
        """The text block shown to the model: name, description, actor and subject only."""
        lines = ["Event types (actor: who reports the event; subject: what it is about):"]
        for event in self.events:
            lines.append("- {0}: {1} [actor: {2}; subject: {3}]{4}".format(
                event.name, event.description, event.actor, event.subject,
                " " + event.note if event.note else ""))
        lines.append("")
        lines.append("Subject kinds: road_user = a recorder id when the observation is identified with that "
                     "recorder, otherwise an anonymous track id such as \"A:track_001\"; sign = a sign "
                     "detection id such as \"A:sign-0\"; none = no subject.")
        lines.append("")
        lines.append("States (each opened and closed by a pair of events above):")
        for state in sorted(self.states):
            start, end = self.states[state]
            lines.append("- {0}: from {1} to {2}".format(state, start, end))
        return "\n".join(lines)


def vocabulary_path() -> Path:
    return configs_dir() / "semantic_vocabulary.yaml"


def load_vocabulary(path: Optional[Path] = None) -> Vocabulary:
    data: Dict[str, Any] = yaml.safe_load(Path(path or vocabulary_path()).read_text(encoding="utf-8"))
    events = []
    for item in data["events"]:
        if set(item) - {"name", "description", "actor", "subject", "note"}:
            raise ValueError("vocabulary entry {0} has unexpected keys".format(item.get("name")))
        if item["subject"] not in SUBJECT_KINDS or item["actor"] != "recorder":
            raise ValueError("vocabulary entry {0}: bad actor/subject".format(item["name"]))
        events.append(EventType(name=str(item["name"]), description=str(item["description"]).strip(),
                                actor=str(item["actor"]), subject=str(item["subject"]),
                                note=str(item.get("note", "")).strip()))
    names = [event.name for event in events]
    if len(set(names)) != len(names):
        raise ValueError("duplicate event types in the vocabulary")
    states = {}
    for state, pair in (data.get("states") or {}).items():
        start, end = pair
        if start not in names or end not in names:
            raise ValueError("state {0} refers to unknown events".format(state))
        states[str(state)] = (str(start), str(end))
    return Vocabulary(version=int(data.get("version", 1)), events=tuple(events), states=states)
