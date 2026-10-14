"""Replay panel lines; scientific diagnostics remain in the reconstruction files.

A recorder's panel is recorder-centric (the interface of commit 848a645): first the complete CURRENT perceived
state of that recorder as the reconstruction wrote it (its own states, then one line per local track with the
states it holds, named after the fusion's identity: ``track_001 (B): CLOSING, CRITICAL_TTC``), its anonymous
tracks and the road users it sees, then the semantic events it generated in the last second.  Unlike 848a645,
UNKNOWN states ('?', "track lost, states UNKNOWN") and the PREDICTED provenance are not shown, and a panel has
at most ``MAX_PANEL_LINES`` lines, then ``... +N more`` (the complete list is built first).
"""

from typing import List, Optional, Sequence, Tuple


HELP_LINES = (
    "SPACE play/pause   ←/→ seek   N/P event   C camera (overview, each vehicle, free)",
    "TAB vehicle   T tracks   G ghosts   H help   ESC quit",
)

MAX_PANEL_LINES = 8
EVENT, ALERT, STATE, EGO, ANONYMOUS, ROAD_USER, MORE = "event", "alert", "state", "ego", "anonymous", "road_user", "more"
UNKNOWN = "UNKNOWN"
# The states of a recorder and of a track, in the reconstruction's own order (world_state.EGO_STATES /
# TRACK_STATES): a snapshot's states are listed in this order, the others after them.
TRACK_ALERTS = ("CRITICAL_TTC", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT")


def anonymous_row(entity_id: str, observers: Sequence[str]) -> str:
    return "{0}   seen by {1}".format(entity_id, ",".join(sorted(set(observers))))


def subject_label(run, actor: str, subject) -> str:
    """The global identity when available; a local id only if fusion has none."""
    if subject is None:
        return ""
    return run.road_users.get((actor, subject), run.identities.get((actor, subject), subject))


def _true(states) -> List[str]:
    return [name for name, value in states.items() if value is True]


def perceived_state_lines(run, actor: str, t: float) -> Optional[List[Tuple[str, str]]]:
    """The recorder's perceived state at ``t`` (``local_trace``) as (text, kind) lines, like
    ``world_state.compact_state`` without its UNKNOWN parts: ``ego: MOVING, BRAKE``, then one line per track
    with the states it holds (``no active state`` when it holds none and none is unknown), then the known
    signs.  A track whose states are all or partly unknown shows only what is known; a lost track (all
    unknown) is not listed.  None when the reconstruction wrote no perceived state."""
    perceived = (getattr(run, "perceived", None) or {}).get(actor)
    if perceived is None:
        return None
    snapshot = perceived.state_at(t)
    if not snapshot:
        return []
    lines: List[Tuple[str, str]] = []
    ego = snapshot.get("ego") or {}
    true = _true(ego)
    if true:
        lines.append(("ego: " + ", ".join(true), EGO))
    elif ego and not any(value == UNKNOWN for value in ego.values()):
        lines.append(("ego: no active state", EGO))
    for track_id, states in (snapshot.get("external") or {}).items():
        true = _true(states)
        if not true and any(value == UNKNOWN for value in states.values()):
            continue  # lost or unknown: nothing known to show
        name = run.subject_name(actor, track_id)
        lines.append(("{0}: {1}".format(name, ", ".join(true) or "no active state"),
                      ALERT if set(true) & set(TRACK_ALERTS) else STATE))
    for sign_id, sign in (snapshot.get("signs") or {}).items():
        lines.append(("{0}: {1} sign known{2}".format(sign_id, sign.get("class"), ", relevant to the path"
                                                       if sign.get("relevant_to_ego_path") is True else ""), STATE))
    return lines


def standard_panel_lines(run, actor: str, t: float, window: float,
                         max_lines: int = MAX_PANEL_LINES) -> List[Tuple[str, str]]:
    """(text, kind) lines of one recorder's panel (848a645 order), complete list first:

    1. its current perceived state (``perceived_state_lines``; without one, its open START/END pairs);
    2. its anonymous tracks alive now, and the road users (U1, ...) its tracks belong to;
    3. its semantic events of the last ``window`` seconds, newest first: ``» CRITICAL_TTC_START → B``.

    Then at most ``max_lines`` lines are shown, followed by ``... +N more``.  No UNKNOWN ('?') line and no
    PREDICTED text."""
    lines = perceived_state_lines(run, actor, t)
    if lines is None:
        lines = []
        for state in run.active_states(actor, t):
            subject = run.subject_name(actor, state.subject)
            lines.append((state.state + (" → " + subject if subject else ""),
                          ALERT if state.state in TRACK_ALERTS else STATE))
    anonymous = run.anonymous_at(actor, t) if hasattr(run, "anonymous_at") else []
    if anonymous:
        lines.append(("anonymous tracks: " + ", ".join(track.name for track, _ in anonymous), ANONYMOUS))
    tracks = (getattr(run, "tracks", None) or {}).get(actor, [])
    seen = sorted({track.road_user for track in tracks if track.road_user is not None and track.state_at(t) is not None})
    for entity_id in seen:
        entity = run.entity(entity_id)
        if entity is not None and entity.identity_ambiguous:
            continue
        state = entity.state_at(t) if entity is not None else None
        lines.append((anonymous_row(entity_id, state.observers if state else [actor]), ROAD_USER))
    for event in reversed(run.recent_events(actor, t, window)):
        subject = subject_label(run, actor, event.subject)
        lines.append(("» " + event.event_type + (" → " + subject if subject else ""), EVENT))
    if len(lines) <= max_lines:
        return lines
    return lines[:max_lines] + [("... +{0} more".format(len(lines) - max_lines), MORE)]


def event_line(run, event) -> str:
    """``A CRITICAL_TTC_START U3``: an event named by its global subject (HUD last/next lines)."""
    subject = subject_label(run, event.actor, event.subject)
    return "{0} {1}{2}".format(event.actor, event.event_type, (" " + subject) if subject else "")


def camera_cycle(recorders: Sequence[str]) -> List[Tuple[str, Optional[str]]]:
    """The C key's camera sequence: overview, then a follow camera on every RECORDER vehicle in turn
    (reconstructed road users are not vehicles of the replay), then the free camera."""
    return [("overview", None)] + [("follow", pid) for pid in recorders] + [("free", None)]


def next_camera(recorders: Sequence[str], mode: str, selected: Optional[str]) -> Tuple[str, Optional[str]]:
    """The camera after (``mode``, ``selected``) in ``camera_cycle``."""
    cycle = camera_cycle(recorders)
    key = (mode, selected if mode == "follow" else None)
    index = cycle.index(key) if key in cycle else 0
    return cycle[(index + 1) % len(cycle)]
