"""Scoring a Stage-1 answer's semantic hypotheses against the reconstructed semantic trace.

A hypothesis (event_type, actor_id, subject_id, time) is a true positive when
an event of the trace has the same type, the same actor, the same subject
(after resolving identities: an associated track id is its recorder; for
COLLISION actor and subject are the two parties in either order) and a time
within ``time_tolerance_s`` of the hypothesis time (or inside its time window
widened by the tolerance).  Matching is one-to-one, closest times first.

Reference set: every event of the trace, except (configurable) those that only
record a state already active when observation began, and optionally only
event types / a time window of interest.  Recall is therefore measured against
the complete reconstructed trace, not against a hand-picked list.

Rates:
* precision = TP / hypotheses, recall = TP / reference events, F1;
* hallucination rate = hypotheses with no event of that (type, actor, subject)
  anywhere in the trace, at any time / hypotheses (a timing error is not a
  hallucination);
* identity hallucination rate = hypotheses whose actor or subject is not an
  entity of the packet / hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from .formal.verifier import SemanticTrace, TraceEvent


@dataclass
class ScoringConfig:
    time_tolerance_s: float = 0.5
    exclude_active_at_first_observation: bool = True
    reference_event_types: Optional[Sequence[str]] = None
    reference_window_s: Optional[Tuple[Optional[float], Optional[float]]] = None

    @staticmethod
    def from_mapping(data: Optional[Dict[str, Any]]) -> "ScoringConfig":
        data = data or {}
        window = data.get("reference_window_s")
        return ScoringConfig(time_tolerance_s=float(data.get("time_tolerance_s", 0.5)),
                             exclude_active_at_first_observation=bool(data.get("exclude_active_at_first_observation",
                                                                               True)),
                             reference_event_types=data.get("reference_event_types"),
                             reference_window_s=None if not window else (window[0], window[1]))

    def as_dict(self) -> Dict[str, Any]:
        return {"time_tolerance_s": self.time_tolerance_s,
                "exclude_active_at_first_observation": self.exclude_active_at_first_observation,
                "reference_event_types": None if self.reference_event_types is None else list(self.reference_event_types),
                "reference_window_s": None if self.reference_window_s is None else list(self.reference_window_s)}


def reference_events(trace: SemanticTrace, config: ScoringConfig) -> List[TraceEvent]:
    out = []
    for event in trace.events:
        if config.exclude_active_at_first_observation and event.first_observation:
            continue
        if config.reference_event_types is not None and event.event_type not in config.reference_event_types:
            continue
        if config.reference_window_s is not None and event.t_global is not None:
            lo, hi = config.reference_window_s
            if (lo is not None and event.t_global < lo) or (hi is not None and event.t_global > hi):
                continue
        out.append(event)
    return out


def _event_time(event: TraceEvent, hypothesis: Dict[str, Any]) -> Optional[float]:
    if hypothesis["time_reference"] == "LOCAL":
        return event.t_local.get(hypothesis["actor_id"])
    return event.t_global


def _time_error(event: TraceEvent, hypothesis: Dict[str, Any], tolerance: float) -> Optional[float]:
    t_event = _event_time(event, hypothesis)
    if t_event is None:
        return None
    window = hypothesis.get("time_window")
    if window is not None:
        if window["start"] - tolerance <= t_event <= window["end"] + tolerance:
            centre = hypothesis["estimated_time"]
            return 0.0 if centre is None else abs(t_event - centre)
        return None
    if hypothesis["estimated_time"] is None:
        return None
    error = abs(t_event - hypothesis["estimated_time"])
    return error if error <= tolerance + 1e-9 else None


def _same_parties(event: TraceEvent, hypothesis: Dict[str, Any], trace: SemanticTrace,
                  identity_map: Dict[str, str]) -> bool:
    def resolve(entity: Optional[str]) -> Optional[str]:
        if entity is None:
            return None
        resolved = trace.canonical(entity)
        if resolved is None and entity in identity_map.values():
            return entity  # an oracle identity, compared through identity_map below
        return resolved

    def trace_id(entity: Optional[str]) -> Optional[str]:
        return identity_map.get(entity, entity) if entity is not None else None

    actor = resolve(hypothesis["actor_id"])
    if actor is None:
        return False
    subject_given = hypothesis["subject_id"] is not None
    subject = resolve(hypothesis["subject_id"]) if subject_given else None
    if subject_given and subject is None:
        return False  # an id the reconstruction does not know matches nothing
    if event.event_type == "COLLISION":
        parties = {trace_id(p) for p in event.participants}
        if actor not in parties:
            return False
        # A single-recorder collision has an unidentified other party: it cannot refute the subject.
        return not subject_given or subject in parties or (len(parties) == 1 and subject not in trace.recorders)
    return event.actor == actor and trace_id(event.subject) == subject


def score_semantic_hypotheses(stage1: Dict[str, Any], trace: SemanticTrace, packet_ids: Set[str],
                              config: Optional[ScoringConfig] = None,
                              identity_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """TP / FP / FN, precision, recall, F1 and hallucination rates of the semantic hypotheses.

    ``identity_map`` (oracle evaluation only) renames trace entities before
    comparison, e.g. {"A:track_001": "C"}.
    """
    config = config or ScoringConfig()
    identity_map = dict(identity_map or {})
    hypotheses = list(stage1.get("semantic_hypotheses", []))
    reference = reference_events(trace, config)
    candidates = []
    for h_index, hypothesis in enumerate(hypotheses):
        for e_index, event in enumerate(reference):
            if event.event_type != hypothesis["event_type"]:
                continue
            if not _same_parties(event, hypothesis, trace, identity_map):
                continue
            error = _time_error(event, hypothesis, config.time_tolerance_s)
            if error is not None:
                candidates.append((error, h_index, e_index))
    matched_h, matched_e, pairs = set(), set(), {}
    for error, h_index, e_index in sorted(candidates):
        if h_index in matched_h or e_index in matched_e:
            continue
        matched_h.add(h_index)
        matched_e.add(e_index)
        pairs[h_index] = (e_index, error)
    rows = []
    hallucinated = identity_hallucinated = 0
    for h_index, hypothesis in enumerate(hypotheses):
        ids = [hypothesis["actor_id"]] + ([hypothesis["subject_id"]] if hypothesis["subject_id"] is not None else [])
        unknown_ids = [entity for entity in ids if entity not in packet_ids]
        exists = any(event.event_type == hypothesis["event_type"]
                     and _same_parties(event, hypothesis, trace, identity_map) for event in trace.events)
        hallucinated += 0 if exists else 1
        identity_hallucinated += 1 if unknown_ids else 0
        row = {"index": h_index, "event_type": hypothesis["event_type"], "actor_id": hypothesis["actor_id"],
               "subject_id": hypothesis["subject_id"], "time_reference": hypothesis["time_reference"],
               "estimated_time": hypothesis["estimated_time"], "outcome": "TP" if h_index in pairs else "FP",
               "exists_in_trace_at_any_time": exists, "unknown_entity_ids": unknown_ids}
        if h_index in pairs:
            event = reference[pairs[h_index][0]]
            row.update(matched_event={"event_type": event.event_type, "actor": event.actor, "subject": event.subject,
                                      "participants": event.participants, "t_global": event.t_global},
                       time_error_s=round(pairs[h_index][1], 4))
        rows.append(row)
    missed = [{"event_type": event.event_type, "actor": event.actor, "subject": event.subject,
               "participants": event.participants, "t_global": event.t_global}
              for e_index, event in enumerate(reference) if e_index not in matched_e]
    tp, fp, fn = len(pairs), len(hypotheses) - len(pairs), len(reference) - len(matched_e)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else (0.0 if precision is not None
                                                                                        and recall is not None else None)
    errors = [pairs[h][1] for h in pairs]
    return {"config": config.as_dict(), "hypotheses": len(hypotheses), "reference_events": len(reference),
            "TP": tp, "FP": fp, "FN": fn, "precision": _r(precision), "recall": _r(recall), "f1": _r(f1),
            "hallucination_rate": _r(hallucinated / len(hypotheses)) if hypotheses else None,
            "identity_hallucination_rate": _r(identity_hallucinated / len(hypotheses)) if hypotheses else None,
            "mean_abs_time_error_s": _r(sum(errors) / len(errors)) if errors else None,
            "per_hypothesis": rows, "missed_reference_events": missed}


def _r(value: Optional[float]) -> Optional[float]:
    return None if value is None else round(value, 4)


def attribution_check(stage1: Dict[str, Any], trace: SemanticTrace) -> Dict[str, Any]:
    """Who the answer holds responsible, resolved against the trace's entities (no ground truth).

    ``kind`` says whether that entity is a recorder, an anonymous track of a
    recorder, unknown to the reconstruction, or UNKNOWN by choice.
    """
    actor = (stage1.get("responsibility") or {}).get("actor")
    if actor is None or actor == "UNKNOWN":
        kind = "UNKNOWN"
    elif actor in trace.recorders:
        kind = "RECORDER"
    elif trace.canonical(actor) is None:
        kind = "NOT_IN_RECONSTRUCTION"
    elif trace.canonical(actor) in trace.recorders:
        kind = "TRACK_IDENTIFIED_AS_RECORDER"
    else:
        kind = "ANONYMOUS_TRACK"
    return {"responsible_actor": actor, "resolved_entity": trace.canonical(actor) if actor else None, "kind": kind,
            "confidence": (stage1.get("responsibility") or {}).get("confidence")}
