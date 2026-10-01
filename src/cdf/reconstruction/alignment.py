"""Graph-level time alignment from matched COLLISION nodes.

Input: local graphs, each in its own local clock.  Output: an ``Alignment``
that says, per graph, ``t_global = t_local + offset_to_global``.  The local
graphs are only read; their timestamps are never changed.

Two COLLISION nodes of different graphs are the same physical contact when
their peak impulses agree: the two bodies of one contact receive equal and
opposite impulses, so the test needs neither a common clock nor a common frame.
Each match also fixes the clock offset between its two graphs, so the matches
must agree in time: a match between two graphs that earlier matches already
link (directly or through a third graph) must imply the same clock offset,
within ``clock_tolerance_s``, or it is rejected.

The strongest matched contact is the reference event and only defines
t_global = 0.  Every matched contact can align a graph: one that shares a
contact with an aligned graph is aligned through it (multi-hop: A-B by one
collision, B-C by another puts C on the same clock through B).  Graphs that no
chain of matched contacts links to the reference stay UNALIGNED.
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

from .config import FusionConfig
from .models import Alignment, GraphClock, GraphNode, LocalGraph

ALIGNED = "ALIGNED"
UNALIGNED = "UNALIGNED"


def impulse_similarity(first: GraphNode, second: GraphNode) -> float:
    """1.0 for identical peak impulses, 0.0 when one of them is zero."""
    a = float(first.attributes["peak_impulse"])
    b = float(second.attributes["peak_impulse"])
    return 1.0 - abs(a - b) / max(a, b, 1e-9)


class _Clocks:
    """Clock offsets fixed by the accepted matches (a weighted union-find).

    ``t_root = t_graph + shift`` for every graph of a linked group.
    """

    def __init__(self, owners: Sequence[str]) -> None:
        self.parent = {owner: owner for owner in owners}
        self.shift = {owner: 0.0 for owner in owners}
        self.event = {owner: None for owner in owners}  # the match that linked a graph to its parent

    def root(self, owner: str) -> Tuple[str, float]:
        shift = 0.0
        while self.parent[owner] != owner:
            shift += self.shift[owner]
            owner = self.parent[owner]
        return owner, shift

    def link(self, first: str, t_first: float, second: str, t_second: float) -> None:
        """``t_first`` (first's clock) and ``t_second`` (second's clock) are the same instant."""
        (root_a, shift_a), (root_b, shift_b) = self.root(first), self.root(second)
        self.parent[root_b] = root_a
        self.shift[root_b] = (t_first + shift_a) - (t_second + shift_b)

    def residual(self, first: str, t_first: float, second: str, t_second: float) -> float:
        """How far a match between two already linked graphs is from their known clock offset."""
        (_, shift_a), (_, shift_b) = self.root(first), self.root(second)
        return (t_first + shift_a) - (t_second + shift_b)

    def linked(self, first: str, second: str) -> bool:
        return self.root(first)[0] == self.root(second)[0]


def match_collisions(graphs: Sequence[LocalGraph], cfg: FusionConfig) -> Tuple[List[Dict[str, Any]],
                                                                               List[Dict[str, Any]]]:
    """Greedy one-to-one, time-consistent matching of collision reports across graphs.

    Report pairs within ``impulse_tolerance`` are candidates, best similarity
    first.  A candidate is accepted when neither report is matched yet and its
    clock offset agrees with the matches already accepted.  Returns
    (matched events, rejected time-inconsistent candidates).
    """
    reports = [(graph.owner, node) for graph in sorted(graphs, key=lambda item: item.owner)
               for node in graph.nodes if node.event_type == "COLLISION"]
    candidates = []
    for index, (first_owner, first) in enumerate(reports):
        for second_owner, second in reports[index + 1:]:
            if first_owner == second_owner:
                continue
            similarity = impulse_similarity(first, second)
            if similarity >= 1.0 - cfg.impulse_tolerance:
                candidates.append((-similarity, first.node_id, second.node_id,
                                   first_owner, first, second_owner, second))
    candidates.sort(key=lambda item: item[:3])
    per_report: Dict[str, int] = {}
    for candidate in candidates:
        for node_id in (candidate[1], candidate[2]):
            per_report[node_id] = per_report.get(node_id, 0) + 1

    clocks = _Clocks([graph.owner for graph in graphs])
    used = set()
    matched, rejected = [], []
    for negative_similarity, first_id, second_id, first_owner, first, second_owner, second in candidates:
        if first_id in used or second_id in used:
            continue
        similarity = round(-negative_similarity, 4)
        peaks = {first_owner: first.attributes["peak_impulse"], second_owner: second.attributes["peak_impulse"]}
        timing = None
        if clocks.linked(first_owner, second_owner):
            residual = clocks.residual(first_owner, first.t_local, second_owner, second.t_local)
            if abs(residual) > cfg.clock_tolerance_s + 1e-9:
                rejected.append({"nodes": {first_owner: first_id, second_owner: second_id},
                                 "t_local": {first_owner: first.t_local, second_owner: second.t_local},
                                 "peak_impulse": peaks, "impulse_similarity": similarity,
                                 "reason": "{0:+.3f} s from the clock offset between {1} and {2} that earlier "
                                           "matches fix (tolerance {3:.2f} s)".format(
                                               residual, first_owner, second_owner, cfg.clock_tolerance_s)})
                continue
            timing = "consistent with the clock offset between {0} and {1} that earlier matches fix " \
                     "({2:+.3f} s, tolerance {3:.2f} s)".format(first_owner, second_owner, residual,
                                                                cfg.clock_tolerance_s)
        else:
            clocks.link(first_owner, first.t_local, second_owner, second.t_local)
        used.update((first_id, second_id))
        evidence = ["{0} and {1} both recorded a collision".format(first_owner, second_owner),
                    "peak impulses {0} vs {1} N*s (similarity {2:.3f}, tolerance {3:.2f})".format(
                        peaks[first_owner], peaks[second_owner], similarity, cfg.impulse_tolerance)]
        alternatives = max(per_report[first_id], per_report[second_id]) - 1
        evidence.append("no competing report within tolerance" if alternatives == 0
                        else "{0} competing report(s) within tolerance; best match kept".format(alternatives))
        if timing is not None:
            evidence.append(timing)
        matched.append({"event_id": None, "graphs": [first_owner, second_owner],
                        "nodes": {first_owner: first_id, second_owner: second_id},
                        "t_local": {first_owner: first.t_local, second_owner: second.t_local},
                        "peak_impulse": peaks, "impulse_similarity": similarity,
                        "confidence": similarity, "evidence": evidence})
    # Numbering needs no common clock: order by first graph, then its local time.
    matched.sort(key=lambda event: (event["graphs"][0], event["t_local"][event["graphs"][0]]))
    for number, event in enumerate(matched, 1):
        event["event_id"] = "collision_{0:03d}".format(number)
    return matched, rejected


def _strength(event: Dict[str, Any]) -> float:
    return max(float(value) for value in event["peak_impulse"].values())


def align_graphs(graphs: Sequence[LocalGraph], cfg: FusionConfig) -> Alignment:
    """t_global = 0 at the strongest matched collision; every match extends the common clock."""
    matched, rejected = match_collisions(graphs, cfg)
    clocks = {}
    for graph in graphs:
        has_collision = any(node.event_type == "COLLISION" for node in graph.nodes)
        reason = ("its collision report matched no other graph" if has_collision
                  else "it recorded no collision to anchor on")
        clocks[graph.owner] = GraphClock(graph=graph.owner, status=UNALIGNED, reason=reason)
    if not matched:
        return Alignment(reference_event=None, graphs=clocks, matched_events=[], rejected_matches=rejected)

    # The strongest contact is the reference; on a tie the first one is kept.
    reference = matched[0]
    for event in matched[1:]:
        if _strength(event) > _strength(reference):
            reference = event
    for owner in reference["graphs"]:
        anchor = reference["t_local"][owner]
        clocks[owner] = GraphClock(graph=owner, status=ALIGNED, anchor_node=reference["nodes"][owner],
                                   anchor_t_local=anchor, offset_to_global=round(-anchor, 4),
                                   reason="reported the reference collision " + reference["event_id"],
                                   chain=[reference["event_id"]])
    # Multi-hop: breadth first from the reference graphs, the strongest shared contact first.
    frontier = list(reference["graphs"])
    while frontier:
        reached = []
        for event in sorted(matched, key=lambda item: (-_strength(item), item["event_id"])):
            known = [owner for owner in event["graphs"] if owner in frontier]
            new = [owner for owner in event["graphs"] if clocks[owner].status != ALIGNED]
            if len(known) != 1 or len(new) != 1:
                continue
            via, owner = clocks[known[0]], new[0]
            t_global = via.to_global(event["t_local"][known[0]])
            anchor = event["t_local"][owner]
            clocks[owner] = GraphClock(
                graph=owner, status=ALIGNED, anchor_node=event["nodes"][owner], anchor_t_local=anchor,
                offset_to_global=round(t_global - anchor, 4), chain=via.chain + [event["event_id"]],
                reason="shares {0} with {1}, aligned through {2}".format(
                    event["event_id"], known[0], " -> ".join(via.chain + [event["event_id"]])))
            reached.append(owner)
        frontier = reached
    for owner, clock in clocks.items():
        if clock.status == UNALIGNED and any(owner in event["graphs"] for event in matched):
            clock.reason = "its matched collisions link it to no graph aligned with the reference"
    return Alignment(reference_event=reference["event_id"], graphs=clocks, matched_events=matched,
                     rejected_matches=rejected)
