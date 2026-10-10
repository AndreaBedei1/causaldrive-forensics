"""Leak guard: fail closed before anything reaches a model.

Every packet is checked when it is exported and again before every request;
every rendered prompt is checked before it is sent.  A violation raises
:class:`LeakGuardError` and no request is made.

What is refused:

* any key containing a blacklisted token (``ground_truth``, ``expected``,
  ``culprit``, ``scenario``, ``variant``, ``semantic_trace``,
  ``perceived_state``, ``events``, ``critical``, ``collision_course``,
  ``required_deceleration``, ``time_headway``, ``required_safe_distance``, ... )
  or equal to ``ttc_s``;
* the same tokens inside the packet's string values and inside the prompt
  templates' own text;
* any semantic event type of the vocabulary (``CRITICAL_TTC_START``,
  ``CUT_IN_FROM_LEFT_START``, ...) inside the packet;
* anything that names the scenario: scenario ids (``S17``), scenario file
  stems, scenario and variant names from ``configs/scenarios/`` (a one-word
  name such as ``crossing`` only as a whole value, since the supplied road
  environment may use the word), run directory names, ``traces/`` paths.

The vocabulary block, the grammar block and the model's own previous answer are
the only parts of a prompt exempt from the prose check (they are rendered by
this package, or produced by the model from admissible input).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import yaml

from ..common.config import configs_dir

FORBIDDEN_TOKENS = (
    "ground_truth", "ground truth", "expected", "culprit", "scenario", "variant",
    "semantic_trace", "semantic trace", "perceived_state", "perceived state", "events",
    "critical", "collision_course", "collision course", "required_deceleration",
    "encounter", "motion_relation", "avoidance", "braking_margin", "unavoidable",
    "predicted_overlap", "cut_in", "ego_path", "privileged", "oracle",
    # safe-following-distance outputs of the conflict model (UNSAFE_FORWARD_GAP)
    "time_headway", "minimum_time_gap", "time_gap_distance", "required_safe_distance", "safe_distance_margin",
    "forward_region",
    "forward_leader", "lateral_body_gap", "longitudinal_clearance", "line_of_sight_occluded",
    "safety_envelope",
)
FORBIDDEN_EXACT_KEYS = ("ttc_s",)
PATH_PATTERNS = (re.compile(r"traces[\\/]"), re.compile(r"\brun_\d+"), re.compile(r"\bS\d{2}\b"))
# A scenario or variant name that is one plain word ("crash", "crossing", "roundabout") is also ordinary
# language, e.g. in the supplied road environment ("urban junction, perpendicular crossing"): it is refused
# only as a whole string value.  Names with an underscore, scenario ids and file stems are refused anywhere.
_PLAIN_WORD = re.compile(r"^[a-z]+$")


class LeakGuardError(RuntimeError):
    """Forbidden information was about to reach a model."""

    def __init__(self, violations: Sequence[str]) -> None:
        self.violations = list(violations)
        super().__init__("leak guard: {0} violation(s): {1}".format(
            len(self.violations), "; ".join(self.violations[:8])))


def scenario_tokens(root: Optional[Path] = None) -> Tuple[Set[str], Set[str]]:
    """(specific tokens, plain words) naming scenarios: ids, file stems, names, variant names."""
    specific, generic = set(), {"default"}
    for path in sorted(Path(root or configs_dir() / "scenarios").glob("*.yaml")):
        block = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("scenario") or {}
        specific.add(path.stem.lower())
        for value in [block.get("scenario_id"), block.get("name")] + list((block.get("variants") or {}).keys()):
            if not value:
                continue
            value = str(value).lower()
            (generic if _PLAIN_WORD.match(value) else specific).add(value)
    return specific, generic


def _event_names() -> List[str]:
    from .vocabulary import load_vocabulary

    return load_vocabulary().event_names


def _walk(value: Any, path: str = "$") -> Iterable[Tuple[str, Optional[str], Any]]:
    """(json path, key or None, value) for every key and every leaf."""
    if isinstance(value, dict):
        for key, item in value.items():
            yield path + "." + str(key), str(key), None
            for entry in _walk(item, path + "." + str(key)):
                yield entry
    elif isinstance(value, list):
        for index, item in enumerate(value):
            for entry in _walk(item, "{0}[{1}]".format(path, index)):
                yield entry
    else:
        yield path, None, value


def _token_hits(text: str, tokens: Iterable[str]) -> List[str]:
    lowered = text.lower()
    return [token for token in tokens if token in lowered]


def check_packet(packet: Dict[str, Any], extra_forbidden: Sequence[str] = ()) -> None:
    """Raise LeakGuardError if the packet names anything forbidden."""
    violations = []
    specific, generic = scenario_tokens()
    events = [re.compile(r"\b{0}\b".format(re.escape(name))) for name in _event_names()]
    tokens = tuple(FORBIDDEN_TOKENS) + tuple(token.lower() for token in extra_forbidden)
    for path, key, value in _walk(packet):
        if key is not None:
            hits = _token_hits(key, tokens)
            if key.lower() in FORBIDDEN_EXACT_KEYS:
                hits.append(key)
            if hits:
                violations.append("key {0} ({1})".format(path, ", ".join(hits)))
            continue
        if not isinstance(value, str):
            continue
        hits = _token_hits(value, tokens)
        if value.lower() in FORBIDDEN_EXACT_KEYS:  # a field name listed as a column
            hits.append(value)
        hits += [pattern.pattern for pattern in events if pattern.search(value)]
        hits += [token for token in specific if token in value.lower()]
        hits += [word for word in generic if value.strip().lower() == word]
        hits += [pattern.pattern for pattern in PATH_PATTERNS if pattern.search(value)]
        if hits:
            violations.append("value at {0} ({1})".format(path, ", ".join(sorted(set(hits)))))
    if violations:
        raise LeakGuardError(violations)


def check_prompt_text(prose: str) -> None:
    """Raise LeakGuardError if a prompt's own text (exempt blocks removed) names anything forbidden."""
    violations = []
    hits = _token_hits(prose, FORBIDDEN_TOKENS)
    if hits:
        violations.append("prompt text ({0})".format(", ".join(hits)))
    specific, _ = scenario_tokens()
    named = [token for token in specific if re.search(r"\b{0}\b".format(re.escape(token)), prose.lower())]
    if named:
        violations.append("prompt text names a scenario ({0})".format(", ".join(sorted(named))))
    paths = [pattern.pattern for pattern in PATH_PATTERNS if pattern.search(prose)]
    if paths:
        violations.append("prompt text has a path or run name ({0})".format(", ".join(paths)))
    if violations:
        raise LeakGuardError(violations)


def check_request(prompt: str, packet: Dict[str, Any], exempt_blocks: Sequence[str],
                  packet_json: str) -> None:
    """The full check before a request: the packet itself, then the prompt's own text.

    ``prompt`` is the rendered prompt, ``packet_json`` the exact packet text in
    it, ``exempt_blocks`` the vocabulary / grammar / previous-answer texts.
    """
    check_packet(packet)
    if packet_json not in prompt:
        raise LeakGuardError(["the prompt does not contain the checked packet verbatim"])
    prose = prompt.replace(packet_json, " ")
    for block in sorted(exempt_blocks, key=len, reverse=True):
        if block and block in prose:
            prose = prose.replace(block, " ")
    check_prompt_text(prose)
