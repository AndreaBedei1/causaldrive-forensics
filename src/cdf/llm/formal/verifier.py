"""Deterministic three-valued verification of formulas on the reconstructed semantic trace.

The semantic trace is the reconstruction's own output, never shown to a model:
``reconstruction/global/global_graph.json`` (events on the global clock),
``alignment.json`` (clocks), ``associations.json`` (identities),
``<R>/local_graph.json`` (observation windows, track lifetimes) and
``<R>/local_trace.jsonl`` (each recorder's perceived state, three-valued).

Values are Kleene's: TRUE (1), UNKNOWN (1/2), FALSE (0); AND = min, OR = max,
NOT = 1 - x.  ``F[a,b]`` is the max over the window, ``G[a,b]`` the min; a
finite bound reaching outside the recorded interval contributes UNKNOWN, an
infinite one is limited to the recorded interval.  UNKNOWN also comes from a
road user that was not being tracked, a state the recorder had not
established, an entity id the reconstruction does not know, and a recorder
without global time.  Absence of evidence is never FALSE unless the recorder
was observing.

The verdict is *formal consistency of the LLM hypothesis with the
reconstructed semantic trace*; it does not prove a causal claim.
"""

from __future__ import annotations

import json
import math
from bisect import bisect_right
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import numpy as np

from ..vocabulary import Vocabulary
from .parser import walk

TRUE, UNKNOWN, FALSE = 1.0, 0.5, 0.0
LABELS = {TRUE: "TRUE", UNKNOWN: "UNKNOWN", FALSE: "FALSE"}
TRACK_STATE_KEYS = {"EGO_PATH": "IN_EGO_PATH"}
SEMANTICS = "formal consistency of the LLM hypothesis with the reconstructed semantic trace"


def label(value: float) -> str:
    return LABELS[float(value)]


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@dataclass
class TraceEvent:
    event_type: str
    actor: Optional[str]
    subject: Optional[str]
    participants: List[str]
    t_global: Optional[float]
    t_local: Dict[str, float]
    first_observation: bool = False


@dataclass
class Recorder:
    name: str
    aligned: bool
    offset: Optional[float]
    start_local: float
    end_local: float
    tracks: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # local id -> (first, last) local
    frames: List[Tuple[float, Dict[str, Any]]] = field(default_factory=list)

    def to_global(self, t_local: float) -> Optional[float]:
        return None if not self.aligned else round(t_local + self.offset, 6)

    @property
    def window(self) -> Optional[Tuple[float, float]]:
        if not self.aligned:
            return None
        return (self.start_local + self.offset, self.end_local + self.offset)


class SemanticTrace:
    """The reconstruction of one run, as the verifier reads it."""

    def __init__(self, recorders: Dict[str, Recorder], events: List[TraceEvent],
                 track_identity: Dict[Tuple[str, str], str], vocabulary: Vocabulary, step: float = 0.05) -> None:
        self.recorders = recorders
        self.events = events
        self.track_identity = track_identity  # (recorder, local track) -> global entity
        self.vocabulary = vocabulary
        self.step = float(step)
        windows = [r.window for r in recorders.values() if r.window is not None]
        if windows:
            start = math.floor(min(w[0] for w in windows) / self.step + 1e-9) * self.step
            end = math.ceil(max(w[1] for w in windows) / self.step - 1e-9) * self.step
            count = int(round((end - start) / self.step)) + 1
            self.grid = np.round(start + self.step * np.arange(count), 6)
        else:
            self.grid = np.zeros(0)
        self.entities: Set[str] = set(recorders) | set(track_identity.values())
        self.entities |= {"{0}:{1}".format(owner, track) for owner, track in track_identity}
        self.entities |= {event.subject for event in events if event.subject}

    # -- loading -----------------------------------------------------------

    @classmethod
    def load(cls, run_dir: Path, vocabulary: Vocabulary, step: float = 0.05) -> "SemanticTrace":
        rec = Path(run_dir) / "reconstruction"
        alignment = _read_json(rec / "global" / "alignment.json")
        associations = _read_json(rec / "global" / "associations.json")
        graph = _read_json(rec / "global" / "global_graph.json")
        recorders = {}
        for name, clock in sorted(alignment["graphs"].items()):
            local = _read_json(rec / name / "local_graph.json")
            info = local["recorder"]
            recorder = Recorder(name=name, aligned=clock["status"] == "ALIGNED" and clock.get("offset_to_global") is not None,
                                offset=clock.get("offset_to_global"), start_local=float(info["start_t_local"]),
                                end_local=float(info["end_t_local"]))
            for track in local.get("tracks", []):
                recorder.tracks[track["track_id"]] = (float(track["first_seen_t_local"]),
                                                      float(track["last_seen_t_local"]))
            with (rec / name / "local_trace.jsonl").open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        frame = json.loads(line)
                        recorder.frames.append((float(frame["t_local"]), frame["perceived_state"]))
            recorders[name] = recorder
        identity = {(item["local_graph"], item["local_track"]): item["global_entity"] for item in associations}
        events = []
        for node in graph["nodes"]:
            events.append(TraceEvent(
                event_type=node["event_type"], actor=node.get("actor_id"), subject=node.get("subject_id"),
                participants=list(node.get("participants") or []), t_global=node.get("t_global"),
                t_local={obs["graph"]: float(obs["t_local"]) for obs in node.get("observations", [])},
                first_observation=bool((node.get("attributes") or {}).get("active_at_first_observation"))))
        return cls(recorders, events, identity, vocabulary, step)

    # -- identities --------------------------------------------------------

    def canonical(self, entity: Optional[str]) -> Optional[str]:
        """Global entity of an id: a recorder, an associated track's recorder, or the anonymous track itself."""
        if entity is None:
            return None
        if entity in self.recorders:
            return entity
        if ":" in entity:
            owner, track = entity.split(":", 1)
            if (owner, track) in self.track_identity:
                return self.track_identity[(owner, track)]
        return entity if entity in self.entities else None

    def local_tracks(self, actor: str, subject: Optional[str]) -> List[str]:
        """The actor's local tracks that are ``subject`` (all of them when subject is None)."""
        recorder = self.recorders[actor]
        if subject is None:
            return sorted(recorder.tracks)
        return sorted(track for track in recorder.tracks
                      if self.track_identity.get((actor, track), "{0}:{1}".format(actor, track)) == subject)

    # -- grid helpers --------------------------------------------------------

    def _mask(self, intervals: Sequence[Tuple[float, float]]) -> np.ndarray:
        mask = np.zeros(len(self.grid), dtype=bool)
        for start, end in intervals:
            mask |= (self.grid >= start - 1e-6) & (self.grid <= end + 1e-6)
        return mask

    def _index(self, t: float) -> Optional[int]:
        if not len(self.grid):
            return None
        i = int(round((t - self.grid[0]) / self.step))
        return i if 0 <= i < len(self.grid) and abs(self.grid[i] - t) < self.step / 2 + 1e-9 else None

    # -- atoms ---------------------------------------------------------------

    def _actor_problem(self, actor: str) -> Optional[str]:
        if actor not in self.recorders:
            if self.canonical(actor) is not None:
                return "{0} is not a recorder: it reports no events or states of its own".format(actor)
            return "identity {0} is not available in the reconstruction".format(actor)
        if not self.recorders[actor].aligned:
            return "{0} has no global time (unaligned recorder)".format(actor)
        return None

    def event_signal(self, event_type: str, actor: str, subject: Optional[str]) -> Tuple[np.ndarray, List[str]]:
        values = np.full(len(self.grid), UNKNOWN)
        problem = self._actor_problem(actor)
        if problem:
            return values, [problem]
        recorder = self.recorders[actor]
        definition = self.vocabulary.event(event_type)
        kind = definition.subject if definition is not None else "none"
        notes: List[str] = []
        target = self.canonical(subject)
        if subject is not None and target is None:
            return values, ["identity {0} is not available in the reconstruction".format(subject)]
        foreign_track = (target is not None and ":" in target and target.split(":", 1)[0] != actor
                         and target not in self.recorders)
        if event_type == "COLLISION" or kind in ("none", "sign") or event_type.startswith("TRACK_"):
            if foreign_track and event_type != "COLLISION":
                return values, ["{0} is a track of another recorder: {1} cannot be shown to observe it".format(
                    subject, actor)]
            covered = self._mask([recorder.window])
        else:
            if foreign_track:
                return values, ["{0} is a track of another recorder: {1} cannot be shown to observe it".format(
                    subject, actor)]
            tracks = self.local_tracks(actor, target)
            spans = [(recorder.to_global(recorder.tracks[t][0]), recorder.to_global(recorder.tracks[t][1]))
                     for t in tracks]
            covered = self._mask(spans)
            if not tracks:
                notes.append("{0} never tracked {1}".format(actor, subject))
        values[covered] = FALSE
        for event in self.events:
            if event.event_type != event_type or event.t_global is None:
                continue
            index = self._index(event.t_global)
            if index is None:
                continue
            if event_type == "COLLISION":
                parties = set(event.participants)
                if actor not in parties:
                    continue
                if target is None or target in parties:
                    values[index] = TRUE
                elif len(parties) == 1:
                    values[index] = max(values[index], UNKNOWN)  # the other party is unidentified
                    notes.append("collision at {0:+.2f} s: the other party is unidentified".format(event.t_global))
                continue
            if event.actor != actor:
                continue
            if subject is None or event.subject == target:
                values[index] = TRUE
        return values, notes

    def _frame_value(self, state: Dict[str, Any], state_name: str, kind: str, track: Optional[str]) -> float:
        if kind == "none":
            value = (state.get("ego") or {}).get(state_name, "UNKNOWN")
        else:
            entry = (state.get("external") or {}).get(track)
            if entry is None:
                return UNKNOWN
            value = entry.get(TRACK_STATE_KEYS.get(state_name, state_name), "UNKNOWN")
        if value is True:
            return TRUE
        if value is False:
            return FALSE
        return UNKNOWN

    def _sample(self, changes: List[Tuple[float, int, float]], window: Tuple[float, float]) -> np.ndarray:
        """Piecewise-constant value from (global time, priority, value) change points, UNKNOWN outside window."""
        changes = sorted(changes)
        times = [c[0] for c in changes]
        out = np.full(len(self.grid), UNKNOWN)
        for i, t in enumerate(self.grid):
            if t < window[0] - 1e-6 or t > window[1] + 1e-6:
                continue
            k = bisect_right(times, t + 1e-6) - 1
            if k >= 0:
                out[i] = changes[k][2]
        return out

    def state_signal(self, state: str, actor: str, subject: Optional[str]) -> Tuple[np.ndarray, List[str]]:
        values = np.full(len(self.grid), UNKNOWN)
        problem = self._actor_problem(actor)
        if problem:
            return values, [problem]
        if state not in self.vocabulary.states:
            return values, ["unknown state {0}".format(state)]
        recorder = self.recorders[actor]
        start_event, end_event = self.vocabulary.states[state]
        kind = self.vocabulary.subject_kind_of_state(state)
        target = self.canonical(subject)
        if subject is not None and target is None:
            return values, ["identity {0} is not available in the reconstruction".format(subject)]

        def transitions(match_subject) -> List[Tuple[float, int, float]]:
            out = []
            for event in self.events:
                if event.actor == actor and event.t_global is not None and match_subject(event.subject):
                    if event.event_type == start_event:
                        out.append((event.t_global, 1, TRUE))
                    elif event.event_type == end_event:
                        out.append((event.t_global, 1, FALSE))
            return out

        if kind == "none":
            changes = [(recorder.to_global(t), 0, self._frame_value(s, state, kind, None)) for t, s in recorder.frames]
            changes += transitions(lambda s: s is None)
            return self._sample(changes, recorder.window), []
        if kind == "sign":
            signs = [target] if subject is not None else sorted({
                event.subject for event in self.events
                if event.actor == actor and event.event_type in (start_event, end_event) and event.subject})
            combined = self._sample([(recorder.window[0], 0, FALSE)], recorder.window)
            for sign in signs:
                changes = [(recorder.window[0], 0, FALSE)] + transitions(lambda s, e=sign: s == e)
                combined = np.maximum(combined, self._sample(changes, recorder.window))
            return combined, []
        tracks = self.local_tracks(actor, target)
        if not tracks:
            return values, ["{0} never tracked {1}".format(actor, subject)]
        combined = None
        for track in tracks:
            changes = [(recorder.to_global(t), 0, self._frame_value(s, state, kind, track)) for t, s in recorder.frames]
            entity = self.track_identity.get((actor, track), "{0}:{1}".format(actor, track))
            changes += [c for c in transitions(lambda s, e=entity: s == e)]
            signal = self._sample(changes, recorder.window)
            combined = signal if combined is None else np.maximum(combined, signal)
        return combined, []

    # -- formulas ------------------------------------------------------------

    def signal(self, tree: Dict[str, Any], notes: Dict[str, List[str]]) -> np.ndarray:
        op = tree["op"]
        if op == "EVENT":
            values, why = self.event_signal(tree["event_type"], tree["actor_id"], tree["subject_id"])
            notes.setdefault(_atom_key(tree), []).extend(why)
            return values
        if op == "STATE":
            values, why = self.state_signal(tree["state"], tree["actor_id"], tree["subject_id"])
            notes.setdefault(_atom_key(tree), []).extend(why)
            return values
        children = [self.signal(child, notes) for child in tree["children"]]
        if op == "NOT":
            return 1.0 - children[0]
        if op == "AND":
            return np.minimum.reduce(children)
        if op == "OR":
            return np.maximum.reduce(children)
        if op in ("EVENTUALLY", "ALWAYS"):
            return self._window(children[0], tree["lo"], tree["hi"], op == "EVENTUALLY")
        if op == "BEFORE":
            first, second = children
            best = FALSE
            running = FALSE
            for j in range(len(self.grid)):
                if j > 0:
                    running = max(running, first[j - 1])
                best = max(best, min(running, second[j]))
            return np.full(len(self.grid), best)
        raise ValueError(op)

    def _window(self, values: np.ndarray, lo: Optional[float], hi: Optional[float], eventually: bool) -> np.ndarray:
        n = len(values)
        out = np.empty(n)
        for i in range(n):
            a = 0 if lo is None else i + int(math.ceil(lo / self.step - 1e-9))
            b = n - 1 if hi is None else i + int(math.floor(hi / self.step + 1e-9))
            partial = (lo is not None and a < 0) or (hi is not None and b > n - 1)
            a, b = max(a, 0), min(b, n - 1)
            inside = values[a:b + 1] if a <= b else np.zeros(0)
            if eventually:
                r = float(inside.max()) if len(inside) else FALSE
                out[i] = UNKNOWN if partial and r < TRUE else r
            else:
                r = float(inside.min()) if len(inside) else TRUE
                out[i] = UNKNOWN if partial and r > FALSE else r
        return out

    def evaluate(self, tree: Dict[str, Any], at: float = 0.0) -> Dict[str, Any]:
        notes: Dict[str, List[str]] = {}
        index = self._index(at)
        if index is None:
            signal = None
            value = UNKNOWN
            reason = ["t_global = {0} lies outside the recorded interval (or no recorder has global time)".format(at)]
        else:
            signal = self.signal(tree, notes)
            value = float(signal[index])
            reason = []
        atoms = []
        for node in walk(tree):
            if node["op"] in ("EVENT", "STATE"):
                key = _atom_key(node)
                if node["op"] == "EVENT":
                    values, _ = self.event_signal(node["event_type"], node["actor_id"], node["subject_id"])
                else:
                    values, _ = self.state_signal(node["state"], node["actor_id"], node["subject_id"])
                true_times = [float(t) for t, v in zip(self.grid, values) if v == TRUE]
                atoms.append({"atom": key, "true_at_t_global": _spans(true_times, self.step),
                              "samples": {"TRUE": int(np.sum(values == TRUE)), "FALSE": int(np.sum(values == FALSE)),
                                          "UNKNOWN": int(np.sum(values == UNKNOWN))},
                              "notes": sorted(set(notes.get(key, [])))})
        return {"result": label(value), "evaluated_at_t_global": at, "reasons": reason, "atoms": atoms}


def _atom_key(node: Dict[str, Any]) -> str:
    name = node["event_type"] if node["op"] == "EVENT" else node["state"]
    args = [name, node["actor_id"]] + ([node["subject_id"]] if node["subject_id"] is not None else [])
    return "{0}({1})".format("event" if node["op"] == "EVENT" else "state", ", ".join(str(a) for a in args))


def _spans(times: Sequence[float], step: float) -> List[List[float]]:
    """Consecutive grid instants merged into [start, end] spans."""
    spans: List[List[float]] = []
    for t in times:
        if spans and t - spans[-1][1] <= step * 1.5:
            spans[-1][1] = round(t, 4)
        else:
            spans.append([round(t, 4), round(t, 4)])
    return spans
