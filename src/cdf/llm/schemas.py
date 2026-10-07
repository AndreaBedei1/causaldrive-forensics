"""Response schemas of the two LLM stages, a minimal JSON-Schema validator, and
the programmatic checks run on every answer.

The schemas use only what both providers' structured-output modes accept:
``type`` (with ``"null"`` in a type list for optional values), ``properties``,
``required`` (every property), ``additionalProperties: false``, ``items``,
``enum``, ``anyOf`` and ``description``.  Ranges (confidence in [0, 1]) and
cross-references (ids, fact ids, claim references) are checked here, after
the answer is saved; nothing in an answer is ever corrected silently.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

from .vocabulary import Vocabulary

STAGE1_SCHEMA_VERSION = "cdf.llm.stage1/1"
STAGE2_SCHEMA_VERSION = "cdf.llm.stage2/1"
TIME_REFERENCES = ("GLOBAL", "LOCAL")
UNKNOWN_ACTOR = "UNKNOWN"
AST_OPS = ("AND", "OR", "NOT", "EVENTUALLY", "ALWAYS", "BEFORE", "EVENT", "STATE")

# Issue codes.
INVALID_SCHEMA = "INVALID_SCHEMA"
INVALID_IDENTITY_HALLUCINATION = "INVALID_IDENTITY_HALLUCINATION"
INVALID_EVIDENCE_REFERENCE = "INVALID_EVIDENCE_REFERENCE"
INVALID_EVENT_TYPE = "INVALID_EVENT_TYPE"
INVALID_STATE = "INVALID_STATE"
INVALID_VALUE = "INVALID_VALUE"
INVALID_CLAIM_REFERENCE = "INVALID_CLAIM_REFERENCE"
INVALID_FORMULA = "INVALID_FORMULA"
FORMULA_TEXT_AST_MISMATCH = "FORMULA_TEXT_AST_MISMATCH"


def _nullable(schema: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(schema)
    out["type"] = [schema["type"], "null"]
    return out


def _object(properties: Dict[str, Any], description: str = "") -> Dict[str, Any]:
    out = {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}
    if description:
        out["description"] = description
    return out


STRING = {"type": "string"}
NUMBER = {"type": "number"}
FACT_IDS = {"type": "array", "items": {"type": "string"}, "description": "fact_id values from the packet"}


def stage1_schema(vocabulary: Vocabulary) -> Dict[str, Any]:
    """Abductive explanation."""
    time_fields = {
        "time_reference": {"type": "string", "enum": list(TIME_REFERENCES),
                           "description": "GLOBAL: t_global_s; LOCAL: the actor's own t_local_s"},
        "estimated_time": _nullable({"type": "number", "description": "seconds, in time_reference"}),
    }
    return _object({
        "explanation": {"type": "string", "description": "the most plausible account, in prose"},
        "primary_hypothesis": {"type": "string", "description": "one sentence"},
        "causal_chain": {"type": "array", "items": _object(dict(
            {"step": {"type": "integer"}, "claim": STRING,
             "actor_id": _nullable({"type": "string", "description": "entity id from the packet"})},
            **time_fields, evidence_fact_ids=FACT_IDS))},
        "responsibility": _object({
            "actor": {"type": "string", "description": "entity id from the packet, or UNKNOWN"},
            "assessment": {"type": "string", "description": "causal contribution through traffic behaviour; "
                                                             "not a legal verdict"},
            "confidence": {"type": "number", "description": "0..1"},
            "limitations": {"type": "array", "items": STRING},
        }),
        "alternative_hypotheses": {"type": "array", "items": _object({
            "hypothesis": STRING,
            "responsible_actor": {"type": "string", "description": "entity id from the packet, or UNKNOWN"},
            "plausibility": {"type": "number", "description": "0..1"},
            "evidence_fact_ids": FACT_IDS,
        })},
        "semantic_hypotheses": {"type": "array", "items": _object(dict(
            {"event_type": {"type": "string", "enum": vocabulary.event_names},
             "actor_id": {"type": "string", "description": "the recorder that would report the event"},
             "subject_id": _nullable({"type": "string", "description": "entity id the event is about"})},
            **time_fields,
            time_window={"anyOf": [_object({"start": NUMBER, "end": NUMBER}), {"type": "null"}]},
            confidence={"type": "number", "description": "0..1"},
            evidence_fact_ids=FACT_IDS))},
        "unresolved_entities": {"type": "array", "items": _object({
            "entity_id": STRING, "role": STRING, "reason": STRING})},
    })


def stage2_schema() -> Dict[str, Any]:
    """Formalisation: one formula per testable claim, as text and as a node table."""
    node = _object({
        "id": STRING,
        "op": {"type": "string", "enum": list(AST_OPS)},
        "children": {"type": "array", "items": STRING, "description": "ids of the operand nodes, in order"},
        "lo": _nullable({"type": "number", "description": "lower bound (s) of EVENTUALLY / ALWAYS; null = -inf"}),
        "hi": _nullable({"type": "number", "description": "upper bound (s) of EVENTUALLY / ALWAYS; null = +inf"}),
        "event_type": _nullable({"type": "string", "description": "EVENT only"}),
        "state": _nullable({"type": "string", "description": "STATE only"}),
        "actor_id": _nullable({"type": "string", "description": "EVENT / STATE only"}),
        "subject_id": _nullable({"type": "string", "description": "EVENT / STATE only, optional"}),
    })
    return _object({
        "formulas": {"type": "array", "items": _object({
            "formula_id": STRING,
            "claim_ref": {"type": "string", "description": "causal_chain[i] or semantic_hypotheses[j]"},
            "claim": STRING,
            "formula_text": STRING,
            "formula_ast": _object({"root": STRING, "nodes": {"type": "array", "items": node}}),
        })},
        "untestable_claims": {"type": "array", "items": _object({"claim_ref": STRING, "claim": STRING,
                                                                  "reason": STRING})},
    })


# ---------------------------------------------------------------------------
# A minimal JSON-Schema validator (the subset above)
# ---------------------------------------------------------------------------

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def _is_type(value: Any, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[name])


def validate_json_schema(value: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """Errors of ``value`` against ``schema`` (empty when valid)."""
    if "anyOf" in schema:
        options = [validate_json_schema(value, option, path) for option in schema["anyOf"]]
        if any(not errors for errors in options):
            return []
        return ["{0}: matches none of anyOf ({1})".format(path, "; ".join(min(options, key=len)))]
    errors: List[str] = []
    types = schema.get("type")
    if types is not None:
        names = types if isinstance(types, list) else [types]
        if not any(_is_type(value, name) for name in names):
            return ["{0}: expected type {1}, got {2}".format(path, "/".join(names), type(value).__name__)]
    if "enum" in schema and value not in schema["enum"]:
        errors.append("{0}: {1!r} not in enum".format(path, value))
    if isinstance(value, dict) and "properties" in schema:
        for key in schema.get("required", []):
            if key not in value:
                errors.append("{0}: missing required property {1!r}".format(path, key))
        for key, item in value.items():
            if key in schema["properties"]:
                errors += validate_json_schema(item, schema["properties"][key], path + "." + key)
            elif schema.get("additionalProperties") is False:
                errors.append("{0}: unexpected property {1!r}".format(path, key))
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            errors += validate_json_schema(item, schema["items"], "{0}[{1}]".format(path, index))
    return errors


# ---------------------------------------------------------------------------
# Programmatic checks
# ---------------------------------------------------------------------------

# Free-text mentions that look like an identity: "vehicle C", "car D", "recorder E",
# "road user F", or an explicit "<X>:track_NNN" / "<X>:sign-N" id.
_TEXT_ID_PATTERNS = (
    re.compile(r"\b(?i:vehicle|car|recorder|road user|truck|van|driver of)\s+([A-Z])\b"),
    re.compile(r"\b([A-Z]:track_\d+)\b"),
    re.compile(r"\b([A-Z]:sign-\d+)\b"),
)


def known_ids(packet: Dict[str, Any]) -> Set[str]:
    """Every id a model may use: recorders, local track ids, observed subjects, sign ids."""
    ids = set()
    for entity in packet["entities"]:
        ids.add(entity["entity_id"])
        if entity.get("observed_subject"):
            ids.add(entity["observed_subject"])
    return ids


def recorder_ids(packet: Dict[str, Any]) -> Set[str]:
    return {item["recorder_id"] for item in packet["known_recorders"]}


def _issue(code: str, path: str, value: Any, message: str) -> Dict[str, Any]:
    return {"code": code, "path": path, "value": value, "message": message}


def text_identity_mentions(text: str) -> List[str]:
    found = []
    for pattern in _TEXT_ID_PATTERNS:
        found += pattern.findall(text or "")
    return found


def _check_id(value: Optional[str], path: str, ids: Set[str], issues: List[Dict[str, Any]],
              allow_unknown: bool = False) -> None:
    if value is None:
        return
    if allow_unknown and value == UNKNOWN_ACTOR:
        return
    if value not in ids:
        issues.append(_issue(INVALID_IDENTITY_HALLUCINATION, path, value,
                             "entity id not present in the packet"))


def _check_text_ids(text: str, path: str, ids: Set[str], issues: List[Dict[str, Any]]) -> None:
    for mention in text_identity_mentions(text):
        if mention not in ids:
            issues.append(_issue(INVALID_IDENTITY_HALLUCINATION, path, mention,
                                 "the text names an entity that is not in the packet"))


def _check_fact_ids(values: Sequence[str], path: str, fact_ids: Set[str], issues: List[Dict[str, Any]]) -> None:
    for index, value in enumerate(values or []):
        if value not in fact_ids:
            issues.append(_issue(INVALID_EVIDENCE_REFERENCE, "{0}[{1}]".format(path, index), value,
                                 "fact_id not present in the packet"))


def _check_unit(value: Any, path: str, issues: List[Dict[str, Any]]) -> None:
    if isinstance(value, (int, float)) and not 0.0 <= float(value) <= 1.0:
        issues.append(_issue(INVALID_VALUE, path, value, "must be within [0, 1]"))


def validate_stage1(answer: Any, packet: Dict[str, Any], vocabulary: Vocabulary,
                    fact_ids: Iterable[str]) -> Dict[str, Any]:
    """Schema plus programmatic checks of a Stage-1 answer.  Never modifies it."""
    schema_errors = validate_json_schema(answer, stage1_schema(vocabulary))
    issues: List[Dict[str, Any]] = []
    if schema_errors:
        return {"status": "INVALID", "schema_errors": schema_errors, "issues": issues}
    ids, facts, recorders = known_ids(packet), set(fact_ids), recorder_ids(packet)
    for field in ("explanation", "primary_hypothesis"):
        _check_text_ids(answer[field], "$." + field, ids, issues)
    for i, step in enumerate(answer["causal_chain"]):
        path = "$.causal_chain[{0}]".format(i)
        _check_id(step["actor_id"], path + ".actor_id", ids, issues, allow_unknown=True)
        _check_text_ids(step["claim"], path + ".claim", ids, issues)
        _check_fact_ids(step["evidence_fact_ids"], path + ".evidence_fact_ids", facts, issues)
    _check_id(answer["responsibility"]["actor"], "$.responsibility.actor", ids, issues, allow_unknown=True)
    _check_unit(answer["responsibility"]["confidence"], "$.responsibility.confidence", issues)
    _check_text_ids(answer["responsibility"]["assessment"], "$.responsibility.assessment", ids, issues)
    for i, item in enumerate(answer["alternative_hypotheses"]):
        path = "$.alternative_hypotheses[{0}]".format(i)
        _check_id(item["responsible_actor"], path + ".responsible_actor", ids, issues, allow_unknown=True)
        _check_unit(item["plausibility"], path + ".plausibility", issues)
        _check_text_ids(item["hypothesis"], path + ".hypothesis", ids, issues)
        _check_fact_ids(item["evidence_fact_ids"], path + ".evidence_fact_ids", facts, issues)
    for i, item in enumerate(answer["semantic_hypotheses"]):
        path = "$.semantic_hypotheses[{0}]".format(i)
        event = vocabulary.event(item["event_type"])
        if event is None:
            issues.append(_issue(INVALID_EVENT_TYPE, path + ".event_type", item["event_type"],
                                 "not an event type of the vocabulary"))
        if item["actor_id"] not in recorders:
            code = INVALID_IDENTITY_HALLUCINATION if item["actor_id"] not in ids else INVALID_VALUE
            issues.append(_issue(code, path + ".actor_id", item["actor_id"],
                                 "the actor of an event must be a recorder of the packet"))
        _check_id(item["subject_id"], path + ".subject_id", ids, issues)
        if event is not None and event.subject == "none" and item["subject_id"] is not None:
            issues.append(_issue(INVALID_VALUE, path + ".subject_id", item["subject_id"],
                                 "{0} has no subject".format(event.name)))
        _check_unit(item["confidence"], path + ".confidence", issues)
        window = item["time_window"]
        if window is not None and window["start"] > window["end"]:
            issues.append(_issue(INVALID_VALUE, path + ".time_window", window, "start after end"))
        _check_fact_ids(item["evidence_fact_ids"], path + ".evidence_fact_ids", facts, issues)
    for i, item in enumerate(answer["unresolved_entities"]):
        _check_id(item["entity_id"], "$.unresolved_entities[{0}].entity_id".format(i), ids, issues)
    return {"status": "VALID" if not issues else "INVALID", "schema_errors": [], "issues": issues}


def claim_refs(stage1: Dict[str, Any]) -> Set[str]:
    refs = {"causal_chain[{0}]".format(i) for i in range(len(stage1.get("causal_chain", [])))}
    refs |= {"semantic_hypotheses[{0}]".format(i) for i in range(len(stage1.get("semantic_hypotheses", [])))}
    return refs


def validate_stage2(answer: Any, packet: Dict[str, Any], vocabulary: Vocabulary,
                    stage1: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Schema, grammar and reference checks of a Stage-2 answer, formula by formula."""
    from .formal.parser import FormulaError, ast_from_table, check_ast, equivalent, parse_formula

    schema_errors = validate_json_schema(answer, stage2_schema())
    if schema_errors:
        return {"status": "INVALID", "schema_errors": schema_errors, "issues": [], "formulas": []}
    ids, refs = known_ids(packet), claim_refs(stage1 or {})
    issues: List[Dict[str, Any]] = []
    formulas = []
    seen = set()
    for i, item in enumerate(answer["formulas"]):
        path = "$.formulas[{0}]".format(i)
        row = {"formula_id": item["formula_id"], "claim_ref": item["claim_ref"], "ast_valid": False,
               "text_valid": False, "text_matches_ast": None, "issues": []}
        if item["formula_id"] in seen:
            row["issues"].append(_issue(INVALID_FORMULA, path + ".formula_id", item["formula_id"], "duplicate id"))
        seen.add(item["formula_id"])
        if item["claim_ref"] not in refs:
            row["issues"].append(_issue(INVALID_CLAIM_REFERENCE, path + ".claim_ref", item["claim_ref"],
                                        "no such claim in the previous explanation"))
        tree = text_tree = None
        try:
            tree = ast_from_table(item["formula_ast"])
            for problem in check_ast(tree, vocabulary, ids):
                row["issues"].append(_issue(problem["code"], path + ".formula_ast", problem["value"],
                                            problem["message"]))
            row["ast_valid"] = not any(p["code"] in (INVALID_FORMULA, INVALID_EVENT_TYPE, INVALID_STATE)
                                       for p in row["issues"])
        except FormulaError as error:
            row["issues"].append(_issue(INVALID_FORMULA, path + ".formula_ast", None, str(error)))
        try:
            text_tree = parse_formula(item["formula_text"])
            row["text_valid"] = True
        except FormulaError as error:
            row["issues"].append(_issue(INVALID_FORMULA, path + ".formula_text", item["formula_text"], str(error)))
        if tree is not None and text_tree is not None:
            row["text_matches_ast"] = equivalent(tree, text_tree)
            if not row["text_matches_ast"]:
                row["issues"].append(_issue(FORMULA_TEXT_AST_MISMATCH, path, item["formula_text"],
                                            "formula_text and formula_ast differ; the verifier uses the AST"))
        issues += row["issues"]
        formulas.append(row)
    blocking = [issue for issue in issues if issue["code"] != FORMULA_TEXT_AST_MISMATCH]
    return {"status": "VALID" if not blocking else "INVALID", "schema_errors": [], "issues": issues,
            "formulas": formulas}
