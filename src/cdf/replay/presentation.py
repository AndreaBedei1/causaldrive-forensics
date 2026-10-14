"""Compact replay labels; scientific diagnostics remain in the reconstruction files.

The standard interface is physical/global-subject oriented: a road user several local tracks contribute to is
named once, by its global identity (a recorder, a fused road user U1, ...); raw track ids, UNKNOWN states and
the measured/predicted provenance stay in the reconstruction files (and in ``ReplayRun`` for debugging).
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple


HELP_LINES = (
    "SPACE play/pause   ←/→ seek   N/P event   C camera (overview, each vehicle, free)",
    "TAB vehicle   T tracks   G ghosts   H help   ESC quit",
)

# Lines of one recorder panel at most (events never give way to states: they are listed first).
MAX_PANEL_LINES = 8
# The confirmed states worth a line, most important first; others (CLOSING, MOVING, THROTTLE) stay in the files.
SUBJECT_STATES = ("CRITICAL_TTC", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT", "IN_EGO_PATH")
EGO_STATES = ("BRAKE", "STOP", "TURN_LEFT", "TURN_RIGHT", "SPEED_LIMIT_EXCEEDED")
EVENT, ALERT, STATE, EGO, MORE = "event", "alert", "state", "ego", "more"

# Active semantic states of the scene (HUD list): at most this many lines, then "... +N more".
MAX_ACTIVE_LINES = 8
# Priority of an active state (lower first): contact, conflict, braking/throttle, manoeuvre, other.
CONFLICT_STATES = ("CRITICAL_TTC",)
CONTROL_STATES = ("BRAKE", "THROTTLE")
MANOEUVRE_STATES = ("TURN_LEFT", "TURN_RIGHT", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT")
# The graph's EGO_PATH_ENTRY / EXIT pair is the per-frame state IN_EGO_PATH of the reconstruction.
STATE_NAMES = {"EGO_PATH": "IN_EGO_PATH"}


def anonymous_row(entity_id: str, observers: Sequence[str]) -> str:
    return "{0}   seen by {1}".format(entity_id, ",".join(sorted(set(observers))))


def subject_label(run, actor: str, subject) -> str:
    """The global identity when available; a local id only if fusion has none."""
    if subject is None:
        return ""
    return run.road_users.get((actor, subject), run.identities.get((actor, subject), subject))


def _subject_states(run, actor: str, t: float) -> Tuple[Dict[str, Set[str]], Set[str]]:
    """Confirmed (True) states at ``t`` per global subject, and the recorder's own; UNKNOWN is never shown."""
    subjects: Dict[str, Set[str]] = {}
    ego: Set[str] = set()
    perceived = (getattr(run, "perceived", None) or {}).get(actor)
    snapshot = perceived.state_at(t) if perceived is not None else None
    if snapshot:
        ego = {name for name, value in (snapshot.get("ego") or {}).items() if value is True}
        for track_id, states in (snapshot.get("external") or {}).items():
            true = {name for name in SUBJECT_STATES if states.get(name) is True}
            if true:
                subjects.setdefault(subject_label(run, actor, track_id), set()).update(true)
        return subjects, ego
    for interval in run.active_states(actor, t):  # no perceived state written: the START/END pairs
        name = "IN_EGO_PATH" if interval.state == "EGO_PATH" else interval.state
        if interval.subject is None:
            ego.add(name)
        elif name in SUBJECT_STATES:
            subjects.setdefault(subject_label(run, actor, interval.subject), set()).add(name)
    return subjects, ego


def standard_panel_lines(run, actor: str, t: float, window: float,
                         max_lines: int = MAX_PANEL_LINES) -> List[Tuple[str, str]]:
    """(text, kind) lines of one recorder's panel in the standard interface, most important first:

    1. the recorder's semantic events of the last ``window`` seconds, newest first (one line per event type
       and global subject);
    2. its confirmed important states per GLOBAL subject (a road user seen through several local tracks is
       one line), CRITICAL_TTC first;
    3. its own braking / stop / turn state.

    At most ``max_lines`` lines; what does not fit is summarised as ``... +N more``.  Events come first, so a
    state line can never push an event out.  No UNKNOWN ('?') state, no PREDICTED text, no raw track list."""
    events: List[Tuple[str, str]] = []
    seen: Set[Tuple[str, str]] = set()
    for event in reversed(run.recent_events(actor, t, window)):
        subject = subject_label(run, actor, event.subject)
        key = (event.event_type, subject)
        if key in seen:
            continue
        seen.add(key)
        events.append(("» " + event.event_type + (" → " + subject if subject else ""), EVENT))
    subjects, ego = _subject_states(run, actor, t)

    def rank(names: Set[str]) -> int:
        return min(SUBJECT_STATES.index(name) for name in names)
    states = [("{0}: {1}".format(subject, ", ".join(name for name in SUBJECT_STATES if name in names)),
               ALERT if names & {"CRITICAL_TTC", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT"} else STATE)
              for subject, names in sorted(subjects.items(), key=lambda item: (rank(item[1]), item[0]))]
    own = [name for name in EGO_STATES if name in ego]
    lines = events + states + ([("ego: " + ", ".join(own), EGO)] if own else [])
    if len(lines) <= max_lines:
        return lines
    shown = lines[:max(max_lines - 1, 0)]
    return shown + [("... +{0} more".format(len(lines) - len(shown)), MORE)]


def state_priority(state: str) -> int:
    """0 contact, 1 conflict (CRITICAL_TTC), 2 braking / throttle, 3 turn / cut-in manoeuvre, 4 other."""
    if "COLLISION" in state or "CONTACT" in state:
        return 0
    if state in CONFLICT_STATES:
        return 1
    if state in CONTROL_STATES:
        return 2
    if state in MANOEUVRE_STATES:
        return 3
    return 4


def _unknown(run, actor: str, subject: Optional[str], state: str, t: float) -> bool:
    """The recorder's per-frame state (``local_trace``) says UNKNOWN for ``state`` of ``subject`` (or of the
    recorder itself) and none of the subject's local tracks holds it True."""
    perceived = (getattr(run, "perceived", None) or {}).get(actor)
    snapshot = perceived.state_at(t) if perceived is not None else None
    if not snapshot:
        return False
    if subject is None:
        values = [(snapshot.get("ego") or {}).get(state, False)]
    else:
        values = [states.get(state, False) for track, states in (snapshot.get("external") or {}).items()
                  if subject_label(run, actor, track) == subject]
    return True not in values and any(value is None or value == "UNKNOWN" for value in values)


def active_states_at(run, t: float) -> List[Tuple[str, Optional[str], str]]:
    """(recorder, global subject or None, state) of every semantic state active at ``t``, in display priority:
    the START/END intervals of the reconstructed events (``ReplayRun.display_intervals``), each subject named
    by its global identity (several local tracks of one road user give one line).  A state whose subject is
    unknown (after its TRACK_LOST, or UNKNOWN in the recorder's per-frame state while no track of that subject
    holds it) is not shown -- hidden, not read as false; instantaneous events are never states.
    Within one priority: by recorder, subject and state name."""
    items = set()
    for actor in sorted(run.local_events):
        for interval in run.display_intervals(actor):
            if not interval.active_at(t):
                continue
            subject = subject_label(run, actor, interval.subject) or None
            state = STATE_NAMES.get(interval.state, interval.state)
            if not _unknown(run, actor, subject, state, t):
                items.add((actor, subject, state))
    return sorted(items, key=lambda item: (state_priority(item[2]), item[0], item[1] or "", item[2]))


def active_state_lines(states: Sequence[Tuple[str, Optional[str], str]],
                       max_lines: int = MAX_ACTIVE_LINES) -> List[Tuple[str, str]]:
    """(text, kind) lines of the active states, ``A -> B  CRITICAL_TTC`` or ``A       BRAKE``: the first
    ``max_lines`` in the given order, then ``... +N more`` for the rest (nothing is dropped from the data).
    No UNKNOWN ('?') line and no PREDICTED text: only recorder, subject and state names."""
    shown = list(states[:max_lines])
    lefts = [actor if subject is None else "{0} -> {1}".format(actor, subject) for actor, subject, _ in shown]
    width = max((len(left) for left in lefts), default=0)
    lines = [("{0}  {1}".format(left.ljust(width), state),
              ALERT if state_priority(state) <= 1 else (EGO if subject is None else STATE))
             for left, (_, subject, state) in zip(lefts, shown)]
    if len(states) > max_lines:
        lines.append(("... +{0} more".format(len(states) - max_lines), MORE))
    return lines


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
