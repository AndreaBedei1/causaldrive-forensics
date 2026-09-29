"""Graph-level time alignment from matched COLLISION nodes.

Input: local graphs, each in its own local clock.  Output: an ``Alignment``
that says, per graph, ``t_global = t_local + offset_to_global``.  The local
graphs are only read; their timestamps are never changed.

Two COLLISION nodes of different graphs are the same physical contact when
their peak impulses agree: the two bodies of one contact receive equal and
opposite impulses, so the test needs neither a common clock nor a common frame.
The strongest matched contact is the reference event and defines t_global = 0.
Graphs that did not report the reference contact stay UNALIGNED (this first
version does no multi-hop alignment).
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from .config import FusionConfig
from .models import Alignment, GraphClock, GraphNode, LocalGraph


def impulse_similarity(first: GraphNode, second: GraphNode) -> float:
    """1.0 for identical peak impulses, 0.0 when one of them is zero."""
    a = float(first.attributes["peak_impulse"])
    b = float(second.attributes["peak_impulse"])
    return 1.0 - abs(a - b) / max(a, b, 1e-9)


def match_collisions(graphs: Sequence[LocalGraph], cfg: FusionConfig) -> List[Dict[str, Any]]:
    """Greedy one-to-one matching of collision reports across graphs."""
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

    used = set()
    matched = []
    for negative_similarity, first_id, second_id, first_owner, first, second_owner, second in candidates:
        if first_id in used or second_id in used:
            continue
        used.update((first_id, second_id))
        similarity = round(-negative_similarity, 4)
        peaks = {first_owner: first.attributes["peak_impulse"], second_owner: second.attributes["peak_impulse"]}
        evidence = ["{0} and {1} both recorded a collision".format(first_owner, second_owner),
                    "peak impulses {0} vs {1} N*s (similarity {2:.3f}, tolerance {3:.2f})".format(
                        peaks[first_owner], peaks[second_owner], similarity, cfg.impulse_tolerance)]
        alternatives = max(per_report[first_id], per_report[second_id]) - 1
        evidence.append("no competing report within tolerance" if alternatives == 0
                        else "{0} competing report(s) within tolerance; best match kept".format(alternatives))
        matched.append({"event_id": None, "graphs": [first_owner, second_owner],
                        "nodes": {first_owner: first_id, second_owner: second_id},
                        "t_local": {first_owner: first.t_local, second_owner: second.t_local},
                        "peak_impulse": peaks, "impulse_similarity": similarity,
                        "confidence": similarity, "evidence": evidence})
    # Numbering needs no common clock: order by first graph, then its local time.
    matched.sort(key=lambda event: (event["graphs"][0], event["t_local"][event["graphs"][0]]))
    for number, event in enumerate(matched, 1):
        event["event_id"] = "collision_{0:03d}".format(number)
    return matched


def align_graphs(graphs: Sequence[LocalGraph], cfg: FusionConfig) -> Alignment:
    """Anchor global time at the strongest matched collision."""
    matched = match_collisions(graphs, cfg)
    clocks = {}
    for graph in graphs:
        has_collision = any(node.event_type == "COLLISION" for node in graph.nodes)
        reason = ("its collision report matched no other graph" if has_collision
                  else "it recorded no collision to anchor on")
        clocks[graph.owner] = GraphClock(graph=graph.owner, status="UNALIGNED", reason=reason)
    if not matched:
        return Alignment(reference_event=None, graphs=clocks, matched_events=[])

    # The strongest contact is the reference; on a tie the first one is kept.
    reference = matched[0]
    for event in matched[1:]:
        if max(event["peak_impulse"].values()) > max(reference["peak_impulse"].values()):
            reference = event
    for owner in reference["graphs"]:
        anchor = reference["t_local"][owner]
        clocks[owner] = GraphClock(graph=owner, status="ALIGNED", anchor_node=reference["nodes"][owner],
                                   anchor_t_local=anchor, offset_to_global=round(-anchor, 4),
                                   reason="reported the reference collision " + reference["event_id"])
    for owner, clock in clocks.items():
        if clock.status == "UNALIGNED" and any(owner in event["graphs"] for event in matched):
            clock.reason = "shares only a non-reference collision (multi-hop alignment not implemented)"
    return Alignment(reference_event=reference["event_id"], graphs=clocks, matched_events=matched)
