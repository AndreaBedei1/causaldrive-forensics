"""Parse formula text, rebuild the node-table AST, check both, compare them.

A tree node is a dict ``{"op": ..., "children": [...], "lo": ..., "hi": ...,
"event_type": ..., "state": ..., "actor_id": ..., "subject_id": ...}``; bounds
of ``None`` are infinite.  The verifier only ever evaluates the AST; the text
is parsed to tell whether the model wrote the same formula twice.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from .grammar import OPS, UNARY_TEMPORAL


class FormulaError(ValueError):
    """Malformed formula text or node table."""


_TOKEN = re.compile(r"\s*(?:(?P<num>-?(?:inf|\d+(?:\.\d*)?|\.\d+))(?![A-Za-z0-9_:.\-])|(?P<punct>[()\[\],])|"
                    r"(?P<word>[A-Za-z_][A-Za-z0-9_:.\-]*))")


def _tokens(text: str) -> List[Tuple[str, str]]:
    out, position = [], 0
    text = text.strip()
    while position < len(text):
        match = _TOKEN.match(text, position)
        if not match or match.end() == position:
            raise FormulaError("unexpected character {0!r} at {1}".format(text[position], position))
        kind = match.lastgroup
        out.append((kind, match.group(kind)))
        position = match.end()
        while position < len(text) and text[position].isspace():
            position += 1
    return out


def _node(op: str, children: Sequence[Dict[str, Any]] = (), **fields: Any) -> Dict[str, Any]:
    node = {"op": op, "children": list(children), "lo": None, "hi": None, "event_type": None, "state": None,
            "actor_id": None, "subject_id": None}
    node.update(fields)
    return node


class _Parser:
    def __init__(self, text: str) -> None:
        self.tokens = _tokens(text)
        self.i = 0

    def peek(self) -> Optional[Tuple[str, str]]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self, value: Optional[str] = None) -> Tuple[str, str]:
        token = self.peek()
        if token is None:
            raise FormulaError("unexpected end of formula" + ("" if value is None else ", expected " + value))
        if value is not None and token[1] != value:
            raise FormulaError("expected {0!r}, found {1!r}".format(value, token[1]))
        self.i += 1
        return token

    def formula(self) -> Dict[str, Any]:
        return self.disj()

    def _nary(self, op: str, operand) -> Dict[str, Any]:
        items = [operand()]
        while self.peek() is not None and self.peek()[1] == op:
            self.take(op)
            items.append(operand())
        return items[0] if len(items) == 1 else _node(op, items)

    def disj(self) -> Dict[str, Any]:
        return self._nary("OR", self.conj)

    def conj(self) -> Dict[str, Any]:
        return self._nary("AND", self.unary)

    def bound(self) -> Optional[float]:
        kind, value = self.take()
        if kind != "num":
            raise FormulaError("expected a bound, found {0!r}".format(value))
        if value == "inf":
            return math.inf
        if value == "-inf":
            return -math.inf
        return float(value)

    def unary(self) -> Dict[str, Any]:
        token = self.peek()
        if token is None:
            raise FormulaError("unexpected end of formula")
        kind, value = token
        if value == "NOT":
            self.take()
            return _node("NOT", [self.unary()])
        if value in UNARY_TEMPORAL:
            self.take()
            self.take("[")
            lo = self.bound()
            self.take(",")
            hi = self.bound()
            self.take("]")
            return _node(UNARY_TEMPORAL[value], [self.unary()], lo=_finite(lo), hi=_finite(hi))
        if value == "BEFORE":
            self.take()
            self.take("(")
            first = self.formula()
            self.take(",")
            second = self.formula()
            self.take(")")
            return _node("BEFORE", [first, second])
        if value == "(":
            self.take("(")
            inner = self.formula()
            self.take(")")
            return inner
        if value in ("event", "state"):
            return self.atom()
        raise FormulaError("unexpected {0!r}".format(value))

    def atom(self) -> Dict[str, Any]:
        _, kind = self.take()
        self.take("(")
        name = self.take()
        if name[0] != "word":
            raise FormulaError("expected a name after {0}(".format(kind))
        self.take(",")
        actor = self.take()
        if actor[0] != "word":
            raise FormulaError("expected an actor id")
        subject = None
        if self.peek() is not None and self.peek()[1] == ",":
            self.take(",")
            token = self.take()
            if token[0] != "word":
                raise FormulaError("expected a subject id")
            subject = token[1]
        self.take(")")
        if kind == "event":
            return _node("EVENT", event_type=name[1], actor_id=actor[1], subject_id=subject)
        return _node("STATE", state=name[1], actor_id=actor[1], subject_id=subject)


def _finite(value: float) -> Optional[float]:
    return None if math.isinf(value) else float(value)


def parse_formula(text: str) -> Dict[str, Any]:
    parser = _Parser(text)
    tree = parser.formula()
    if parser.peek() is not None:
        raise FormulaError("unexpected {0!r} after the end of the formula".format(parser.peek()[1]))
    return tree


def ast_from_table(table: Dict[str, Any]) -> Dict[str, Any]:
    """Rebuild a tree from the node table; reject cycles, sharing, dangling or unused nodes."""
    nodes = {}
    for node in table.get("nodes", []):
        if node["id"] in nodes:
            raise FormulaError("duplicate node id {0!r}".format(node["id"]))
        if node["op"] not in OPS:
            raise FormulaError("unknown op {0!r}".format(node["op"]))
        nodes[node["id"]] = node
    root = table.get("root")
    if root not in nodes:
        raise FormulaError("root {0!r} is not a node".format(root))
    used: Set[str] = set()

    def build(node_id: str, stack: Tuple[str, ...]) -> Dict[str, Any]:
        if node_id not in nodes:
            raise FormulaError("child {0!r} is not a node".format(node_id))
        if node_id in stack:
            raise FormulaError("cycle through node {0!r}".format(node_id))
        if node_id in used:
            raise FormulaError("node {0!r} is the child of more than one node".format(node_id))
        used.add(node_id)
        node = nodes[node_id]
        children = [build(child, stack + (node_id,)) for child in node.get("children") or []]
        return _node(node["op"], children, lo=node.get("lo"), hi=node.get("hi"), event_type=node.get("event_type"),
                     state=node.get("state"), actor_id=node.get("actor_id"), subject_id=node.get("subject_id"))

    tree = build(root, ())
    unused = sorted(set(nodes) - used)
    if unused:
        raise FormulaError("unused node(s) {0}".format(", ".join(unused)))
    return tree


ARITY = {"NOT": (1, 1), "EVENTUALLY": (1, 1), "ALWAYS": (1, 1), "BEFORE": (2, 2), "AND": (2, None),
         "OR": (2, None), "EVENT": (0, 0), "STATE": (0, 0)}


def walk(tree: Dict[str, Any]):
    yield tree
    for child in tree["children"]:
        for node in walk(child):
            yield node


def check_ast(tree: Dict[str, Any], vocabulary: Any, entity_ids: Set[str]) -> List[Dict[str, Any]]:
    """Structural and vocabulary problems, as {code, value, message}."""
    problems = []

    def problem(code: str, value: Any, message: str) -> None:
        problems.append({"code": code, "value": value, "message": message})

    for node in walk(tree):
        op = node["op"]
        low, high = ARITY[op]
        count = len(node["children"])
        if count < low or (high is not None and count > high):
            problem("INVALID_FORMULA", op, "{0} takes {1} operand(s), got {2}".format(
                op, low if low == high else "{0}+".format(low), count))
        if op in ("EVENTUALLY", "ALWAYS"):
            lo = -math.inf if node["lo"] is None else node["lo"]
            hi = math.inf if node["hi"] is None else node["hi"]
            if lo > hi:
                problem("INVALID_FORMULA", [node["lo"], node["hi"]], "lower bound above upper bound")
        elif node["lo"] is not None or node["hi"] is not None:
            problem("INVALID_FORMULA", op, "bounds only belong to EVENTUALLY / ALWAYS")
        if op == "EVENT":
            if vocabulary.event(node["event_type"] or "") is None:
                problem("INVALID_EVENT_TYPE", node["event_type"], "not an event type of the vocabulary")
        if op == "STATE":
            if node["state"] not in vocabulary.states:
                problem("INVALID_STATE", node["state"], "not a state of the vocabulary")
        if op in ("EVENT", "STATE"):
            if not node["actor_id"]:
                problem("INVALID_FORMULA", op, "an atom needs an actor")
            for key in ("actor_id", "subject_id"):
                if node[key] is not None and node[key] not in entity_ids:
                    problem("INVALID_IDENTITY_HALLUCINATION", node[key], "entity id not present in the packet")
        elif any(node[key] is not None for key in ("event_type", "state", "actor_id", "subject_id")):
            problem("INVALID_FORMULA", op, "only EVENT / STATE nodes carry names and ids")
    return problems


def canonical(tree: Dict[str, Any]) -> Any:
    """A hashable normal form: AND / OR flattened and their operands sorted."""
    op = tree["op"]
    if op in ("AND", "OR"):
        flat = []
        for child in tree["children"]:
            item = canonical(child)
            if isinstance(item, tuple) and item and item[0] == op:
                flat.extend(item[1])
            else:
                flat.append(item)
        return (op, tuple(sorted(flat, key=repr)))
    if op in ("EVENTUALLY", "ALWAYS"):
        lo = None if tree["lo"] is None else round(float(tree["lo"]), 6)
        hi = None if tree["hi"] is None else round(float(tree["hi"]), 6)
        return (op, lo, hi, canonical(tree["children"][0]))
    if op in ("NOT", "BEFORE"):
        return (op,) + tuple(canonical(child) for child in tree["children"])
    if op == "EVENT":
        return (op, tree["event_type"], tree["actor_id"], tree["subject_id"])
    return (op, tree["state"], tree["actor_id"], tree["subject_id"])


def equivalent(first: Dict[str, Any], second: Dict[str, Any]) -> bool:
    return canonical(first) == canonical(second)


def to_text(tree: Dict[str, Any]) -> str:
    """Render a tree in the grammar (fully parenthesised where needed)."""
    op = tree["op"]
    if op in ("AND", "OR"):
        return "(" + " {0} ".format(op).join(to_text(child) for child in tree["children"]) + ")"
    if op == "NOT":
        return "NOT " + to_text(tree["children"][0])
    if op in ("EVENTUALLY", "ALWAYS"):
        lo = "-inf" if tree["lo"] is None else "{0:g}".format(tree["lo"])
        hi = "inf" if tree["hi"] is None else "{0:g}".format(tree["hi"])
        return "{0}[{1},{2}] {3}".format("F" if op == "EVENTUALLY" else "G", lo, hi, to_text(tree["children"][0]))
    if op == "BEFORE":
        return "BEFORE({0}, {1})".format(to_text(tree["children"][0]), to_text(tree["children"][1]))
    name = tree["event_type"] if op == "EVENT" else tree["state"]
    args = [name, tree["actor_id"]] + ([tree["subject_id"]] if tree["subject_id"] is not None else [])
    return "{0}({1})".format("event" if op == "EVENT" else "state", ", ".join(args))


def to_table(tree: Dict[str, Any]) -> Dict[str, Any]:
    """The node-table form of a tree (ids n1, n2, ... in pre-order)."""
    nodes: List[Dict[str, Any]] = []

    def add(node: Dict[str, Any]) -> str:
        node_id = "n{0}".format(len(nodes) + 1)
        entry = {"id": node_id, "op": node["op"], "children": [], "lo": node["lo"], "hi": node["hi"],
                 "event_type": node["event_type"], "state": node["state"], "actor_id": node["actor_id"],
                 "subject_id": node["subject_id"]}
        nodes.append(entry)
        entry["children"] = [add(child) for child in node["children"]]
        return node_id

    root = add(tree)
    return {"root": root, "nodes": nodes}
