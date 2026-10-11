"""Compact replay labels; scientific diagnostics remain in the reconstruction files."""

from typing import Sequence


HELP_LINES = (
    "SPACE play/pause   ←/→ seek   N/P event   C camera   TAB vehicle",
    "T tracks   G ghosts   H help   ESC quit",
)


def anonymous_row(entity_id: str, observers: Sequence[str]) -> str:
    return "{0}   seen by {1}".format(entity_id, ",".join(sorted(set(observers))))


def subject_label(run, actor: str, subject) -> str:
    """The global identity when available; a local id only if fusion has none."""
    if subject is None:
        return ""
    return run.road_users.get((actor, subject), run.identities.get((actor, subject), subject))
