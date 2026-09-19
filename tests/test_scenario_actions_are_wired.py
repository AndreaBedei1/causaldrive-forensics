"""Every scripted action a scenario declares must actually reach the controller.

``ScriptedController`` reads its parameters with ``params.get(name, default)``.
A parameter under the wrong name is therefore not an error: the lookup returns
the default, the action runs and does nothing, and the only place the manoeuvre
still exists is the scenario's own description.

That is exactly what happened. Every ``lane_shift`` in S13 and S16 declared
``lateral_offset`` where the controller reads ``lateral_m``, so five designed
manoeuvres, both disputed lane changes, the deflection that makes S16's second
impact a consequence, and the deliberate lane change that makes it independent,
never occurred in any recorded run. Nothing raised, nothing warned, and the
recordings looked like scenarios whose vehicles simply drove straight.

This test is the guard. It reads the parameter names out of ``controllers.py``
rather than restating them, so a new kind or a renamed parameter has to be taught
to both sides at once.
"""

from __future__ import annotations

import glob
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = REPO_ROOT / "configs" / "scenarios"

#: What ``ScriptedController`` consumes, per action kind. Keep this beside the
#: code it mirrors: ``_resolve_target_speed``, ``_resolve_brake_override`` and
#: ``_resolve_lateral_offset`` in ``cdf.simulation.controllers``.
CONSUMED: Dict[str, set] = {
    "brake": {"intensity"},
    "set_speed": {"target_speed"},
    "hold": {"target_speed"},
    "lane_shift": {"lateral_m"},
    "stop": set(),
}

#: Keys a scenario may carry on an action for a reader rather than the
#: controller. They are documentation, and documentation is not a manoeuvre.
ANNOTATIONS = {"reason", "note", "comment"}


def _walk_actions(node: Any, where: str = "") -> Iterator[Tuple[str, Dict[str, Any]]]:
    """Every scripted action anywhere in a scenario document."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("scripted_actions", "actions") and isinstance(value, list):
                for i, action in enumerate(value):
                    if isinstance(action, dict):
                        yield "{0}/{1}[{2}]".format(where, key, i), action
            else:
                yield from _walk_actions(value, "{0}/{1}".format(where, key))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _walk_actions(value, "{0}[{1}]".format(where, i))


def _scenarios():
    return sorted(glob.glob(str(SCENARIO_DIR / "*.yaml")))


def _actions(path: str):
    with open(path, encoding="utf-8") as handle:
        return list(_walk_actions(yaml.safe_load(handle)))


@pytest.mark.parametrize("path", _scenarios(), ids=lambda p: Path(p).stem)
def test_every_action_kind_is_one_the_controller_runs(path: str) -> None:
    for where, action in _actions(path):
        kind = str(action.get("kind", ""))
        assert kind in CONSUMED, (
            "{0} declares action {1!r} of kind {2!r} at {3}, which "
            "ScriptedController does not implement, so it would never run"
            .format(Path(path).name, action.get("action_id"), kind, where)
        )


@pytest.mark.parametrize("path", _scenarios(), ids=lambda p: Path(p).stem)
def test_no_action_parameter_is_silently_ignored(path: str) -> None:
    """A parameter the controller does not read is a manoeuvre that never happens."""
    for where, action in _actions(path):
        kind = str(action.get("kind", ""))
        params = set(action.get("params") or {})
        ignored = sorted(params - CONSUMED.get(kind, set()) - ANNOTATIONS)
        assert not ignored, (
            "{0}: action {1!r} ({2}) at {3} declares {4}, which the controller "
            "never reads. The action would run and do nothing. Did you mean {5}?"
            .format(Path(path).name, action.get("action_id"), kind, where,
                    ", ".join(ignored), " or ".join(sorted(CONSUMED.get(kind, set()))) or "no parameters")
        )


@pytest.mark.parametrize("path", _scenarios(), ids=lambda p: Path(p).stem)
def test_every_action_carries_the_parameter_its_kind_needs(path: str) -> None:
    """A lane shift with no distance, or a set_speed with no speed, is a no-op."""
    for where, action in _actions(path):
        kind = str(action.get("kind", ""))
        params = set(action.get("params") or {})
        missing = sorted(CONSUMED.get(kind, set()) - params)
        assert not missing, (
            "{0}: action {1!r} ({2}) at {3} is missing {4}, so the controller "
            "would fall back to its default and the action would have no effect"
            .format(Path(path).name, action.get("action_id"), kind, where,
                    ", ".join(missing))
        )


def test_the_table_above_matches_what_the_controller_actually_reads() -> None:
    """If the controller learns a parameter, this test has to learn it too.

    Read out of the source rather than imported, because the names appear inside
    ``params.get(...)`` calls rather than as module constants, and the point is
    to notice when one of those calls changes.
    """
    import re

    source = (REPO_ROOT / "src" / "cdf" / "simulation" / "controllers.py").read_text(
        encoding="utf-8"
    )
    read_by_controller = set(re.findall(r'params\.get\(\s*"([a-z_]+)"', source))
    declared_here = set().union(*CONSUMED.values())
    assert read_by_controller == declared_here, (
        "controllers.py reads {0}; this test knows about {1}. Teach both sides."
        .format(sorted(read_by_controller), sorted(declared_here))
    )
