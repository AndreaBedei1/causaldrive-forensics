"""Versioned prompt templates (``prompts/<name>.txt``) and their rendering.

A template has a ``=== SYSTEM ===`` and a ``=== USER ===`` part and the
placeholders ``{{VOCABULARY}}``, ``{{SUPPLIED_CONTEXT}}``, ``{{PACKET_JSON}}``,
``{{GRAMMAR}}`` and ``{{STAGE1_RESPONSE}}``.  A changed wording is a new file
(``..._v2.txt``), never an edit of a published version: every analysis records
the template name and its SHA-256.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..common.config import repo_root
from .facts import sha256_text
from .formal.grammar import GRAMMAR_TEXT
from .vocabulary import Vocabulary

SYSTEM_MARK = "=== SYSTEM ==="
USER_MARK = "=== USER ==="
DEFAULT_PROMPTS = {"explanation": "accident_abduction_v1", "formalize": "formalize_hypothesis_v1"}


def prompts_dir() -> Path:
    return repo_root() / "prompts"


@dataclass
class Template:
    name: str
    system: str
    user: str
    sha256: str


@dataclass
class RenderedPrompt:
    template: str
    template_sha256: str
    system: str
    user: str
    packet_json: str
    exempt_blocks: List[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return self.system + "\n" + self.user

    def digest(self) -> Dict[str, str]:
        return {"template": self.template, "template_sha256": self.template_sha256,
                "system_sha256": sha256_text(self.system), "user_sha256": sha256_text(self.user)}


def load_template(name: str, directory: Optional[Path] = None) -> Template:
    path = Path(directory or prompts_dir()) / (name + ".txt")
    raw = path.read_text(encoding="utf-8")
    if raw.count(SYSTEM_MARK) != 1 or raw.count(USER_MARK) != 1 or raw.index(SYSTEM_MARK) > raw.index(USER_MARK):
        raise ValueError("{0}: needs one {1} part followed by one {2} part".format(path.name, SYSTEM_MARK, USER_MARK))
    system, user = raw.split(USER_MARK)
    return Template(name=name, system=system.replace(SYSTEM_MARK, "").strip() + "\n", user=user.strip() + "\n",
                    sha256=sha256_text(raw))


def packet_text(packet: Dict[str, Any]) -> str:
    """The packet exactly as it is sent (compact, key order as exported)."""
    return json.dumps(packet, separators=(",", ":"), ensure_ascii=False)


PLACEHOLDERS = ("VOCABULARY", "SUPPLIED_CONTEXT", "PACKET_JSON", "GRAMMAR", "STAGE1_RESPONSE")


def _fill(text: str, values: Dict[str, str]) -> str:
    for key in PLACEHOLDERS:
        mark = "{{" + key + "}}"
        if mark in text and key not in values:
            raise ValueError("template placeholder {0} has no value".format(mark))
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def render_explanation(packet: Dict[str, Any], vocabulary: Vocabulary,
                       template: str = DEFAULT_PROMPTS["explanation"]) -> RenderedPrompt:
    loaded = load_template(template)
    packet_json = packet_text(packet)
    vocabulary_text = vocabulary.render()
    context = json.dumps(packet["supplied_context"], indent=1, ensure_ascii=False)
    values = {"VOCABULARY": vocabulary_text, "SUPPLIED_CONTEXT": context, "PACKET_JSON": packet_json}
    return RenderedPrompt(template=loaded.name, template_sha256=loaded.sha256, system=_fill(loaded.system, values),
                          user=_fill(loaded.user, values), packet_json=packet_json,
                          exempt_blocks=[vocabulary_text, context])


def render_formalization(packet: Dict[str, Any], vocabulary: Vocabulary, stage1_answer: Dict[str, Any],
                         template: str = DEFAULT_PROMPTS["formalize"]) -> RenderedPrompt:
    loaded = load_template(template)
    packet_json = packet_text(packet)
    vocabulary_text = vocabulary.render()
    answer = json.dumps(stage1_answer, indent=1, ensure_ascii=False)
    values = {"VOCABULARY": vocabulary_text, "GRAMMAR": GRAMMAR_TEXT, "PACKET_JSON": packet_json,
              "STAGE1_RESPONSE": answer}
    return RenderedPrompt(template=loaded.name, template_sha256=loaded.sha256, system=_fill(loaded.system, values),
                          user=_fill(loaded.user, values), packet_json=packet_json,
                          exempt_blocks=[vocabulary_text, GRAMMAR_TEXT, answer])
