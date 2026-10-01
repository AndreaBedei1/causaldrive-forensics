"""Read-only queries over one local graph, for validation and reports.

They describe the observed order of events in one recorder's own clock; they
are not legal or causal judgements.  For example ``sign_windows`` says whether
a STOP_START of the recorder lies inside a STOP-sign detection window, from
which a later reasoning layer may derive NO_STOP_AFTER_STOP_SIGN.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .models import GraphNode, LocalGraph, transition_of


def open_states(graph: LocalGraph) -> List[Dict[str, Any]]:
    """States that started and never ended: still active when observation ended.

    Observation of a track's states ends at its TRACK_LOST; of everything else
    at the end of the recording.  No END is inferred in either case.
    """
    active: Dict[Tuple[str, Optional[str]], GraphNode] = {}
    lost: Dict[Optional[str], float] = {}
    for node in graph.nodes:
        if node.event_type == "TRACK_LOST":
            lost[node.subject_id] = node.t_local
        transition = transition_of(node.event_type)
        if transition is None:
            continue
        name, starts = transition
        if starts:
            active[(name, node.subject_id)] = node
        else:
            active.pop((name, node.subject_id), None)
    return [{"state": name, "subject": subject, "since_node": node.node_id, "since_t_local": node.t_local,
             "observed_until": "TRACK_LOST" if subject in lost else "recording end",
             "observed_until_t_local": lost.get(subject, graph.recorder.get("end_t_local"))}
            for (name, subject), node in sorted(active.items(), key=lambda item: item[1].node_id)]


def _stopped_at(graph: LocalGraph, t_local: float) -> bool:
    """Whether the recorder was in the STOP state at ``t_local`` (strictly before any later change)."""
    stopped = False
    for node in graph.nodes:
        if node.t_local >= t_local:
            break
        if node.event_type == "STOP_START":
            stopped = True
        elif node.event_type == "STOP_END":
            stopped = False
    return stopped


def sign_windows(graph: LocalGraph, sign: str = "STOP_SIGN_DETECTED") -> List[Dict[str, Any]]:
    """Each detection window of a sign, and the recorder's STOP_START events inside it.

    Inside means strictly after the window's START and strictly before its END
    (equal times are simultaneous, hence unresolved).  A window without END (the
    sign still in view when the recording ended) lasts until the recording end.
    A reacquired sign has several windows; each START pairs with the next END
    of the same sign.
    """
    stops = [node for node in graph.nodes if node.event_type == "STOP_START"]
    recording_end = float(graph.recorder.get("end_t_local", float("inf")))
    pairs: List[Tuple[GraphNode, Optional[GraphNode]]] = []
    open_: Dict[Optional[str], int] = {}
    for node in graph.nodes:
        if node.event_type == sign + "_START":
            open_[node.subject_id] = len(pairs)
            pairs.append((node, None))
        elif node.event_type == sign + "_END" and node.subject_id in open_:
            index = open_.pop(node.subject_id)
            pairs[index] = (pairs[index][0], node)
    windows = []
    for start, end in pairs:
        if end is not None:
            inside = [stop for stop in stops if start.t_local < stop.t_local < end.t_local]
        else:
            inside = [stop for stop in stops if start.t_local < stop.t_local <= recording_end]
        windows.append({"sign": start.subject_id, "start_node": start.node_id, "start_t_local": start.t_local,
                        "end_node": None if end is None else end.node_id,
                        "end_t_local": None if end is None else end.t_local,
                        "relevant_to_ego_path": start.attributes.get("relevant_to_ego_path"),
                        "reacquired": bool(start.attributes.get("reacquired")),
                        "stop_starts_inside": [stop.node_id for stop in inside],
                        "already_stopped_at_start": _stopped_at(graph, start.t_local)})
    return windows
