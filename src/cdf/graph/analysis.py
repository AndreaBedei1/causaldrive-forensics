"""Query, slicing and counterfactual-preparation layer over a causal graph.

A reconstructed causal DAG is only useful if questions can be asked of it:
*which chains of evidence end in the collision*, *which single claim is load
bearing*, *what did this vehicle alone know*, *what did fusion add*. This module
is that query layer. It is deliberately side-effect free -- every method that
returns a :class:`GraphDocument` builds a fresh graph from copies of the node and
edge attribute dictionaries, so the analyzer's own graph (and the payload objects
it carries) can be queried again afterwards and still describe the original
reconstruction.

Two design decisions are worth stating explicitly.

*Causal paths start at root causes.* A "causal path to the collision" means a
complete chain from something unexplained by the graph (an in-degree-0 node) down
to the outcome. Counting every path from every ancestor instead would count the
suffixes of a single explanation many times and make path-cut rankings depend on
chain length rather than on structure.

*Removal is measured against the original root set.* When a node is deleted the
graph re-roots itself: its children become in-degree-0 and would look like fresh
root causes, hiding the fact that an explanation was destroyed. ``lost_paths``
therefore always counts paths from the root causes of the **original** graph that
survive the deletion, which is the quantity a counterfactual replay is about.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

import networkx as nx

from ..common.config import Config
from ..common.schemas import (
    OUTCOME_EVENT_TYPES,
    Event,
    GraphDocument,
    Provenance,
)
from ..common.timeline import Interval
from .export import from_networkx, graph_summary, to_networkx
from .matching import (
    DEFAULT_CANONICAL_TIME_BUCKET_S,
    match_events,
    canonical_edge_key,
    canonical_key,
)

__all__ = ["GraphAnalyzer"]


#: Event type values that terminate a causal chain.
_OUTCOME_VALUES: Tuple[str, ...] = tuple(t.value for t in OUTCOME_EVENT_TYPES)


class GraphAnalyzer:
    """Read-only analysis facade over one :class:`GraphDocument`.

    The document is converted once with :func:`cdf.graph.export.to_networkx`, so
    node and edge payloads (the typed :class:`Event` / :class:`GraphEdge`
    records, their evidence and provenance) stay attached throughout and survive
    every slicing operation.
    """

    def __init__(self, doc: GraphDocument, cfg: Optional[Config] = None) -> None:
        if not isinstance(doc, GraphDocument):
            raise TypeError("GraphAnalyzer expects a GraphDocument, got {0!r}".format(type(doc)))
        self._doc = doc
        self._graph = to_networkx(doc)
        self._cfg = cfg
        # Path enumeration of the intact graph is the expensive part of every
        # removal report; it depends only on the cutoff, so it is memoised.
        self._baseline_cache: Dict[Optional[int], Dict[str, Any]] = {}
        self._time_bucket_s = (
            float(
                cfg.get(
                    "evaluation.event_match.canonical_time_bucket_s",
                    DEFAULT_CANONICAL_TIME_BUCKET_S,
                )
            )
            if cfg is not None
            else float(DEFAULT_CANONICAL_TIME_BUCKET_S)
        )

    # -- basics -----------------------------------------------------------

    @property
    def document(self) -> GraphDocument:
        """The document this analyzer was built from (not a copy)."""
        return self._doc

    @property
    def graph(self) -> nx.DiGraph:
        """The NetworkX view of the document, payloads included."""
        return self._graph

    def __len__(self) -> int:
        return self._graph.number_of_nodes()

    def __repr__(self) -> str:
        return "GraphAnalyzer(kind={0!r}, scope={1!r}, n_nodes={2}, n_edges={3})".format(
            self._doc.graph_kind,
            self._doc.scope.value if isinstance(self._doc.scope, Provenance) else self._doc.scope,
            self._graph.number_of_nodes(),
            self._graph.number_of_edges(),
        )

    def _require_node(self, node_id: str) -> str:
        """Fail loudly on an unknown node id rather than returning an empty set."""
        if node_id not in self._graph:
            raise KeyError(
                "node {0!r} is not in this graph (it has {1} nodes)".format(
                    node_id, self._graph.number_of_nodes()
                )
            )
        return node_id

    def _sorted_nodes(self, node_ids: Iterable[str]) -> List[str]:
        """Deterministic ordering: by peak time, then id."""
        return sorted(
            node_ids, key=lambda n: (float(self._graph.nodes[n]["t_peak"]), str(n))
        )

    # -- structure --------------------------------------------------------

    def outcome_nodes(self) -> List[str]:
        """Ids of the terminal outcome events (collision / near miss / post-impact)."""
        return self._sorted_nodes(
            n for n, d in self._graph.nodes(data=True) if d.get("event_type") in _OUTCOME_VALUES
        )

    def ancestors(self, node_id: str) -> List[str]:
        """All nodes from which ``node_id`` is reachable (transitive causes)."""
        self._require_node(node_id)
        return self._sorted_nodes(nx.ancestors(self._graph, node_id))

    def descendants(self, node_id: str) -> List[str]:
        """All nodes reachable from ``node_id`` (transitive effects)."""
        self._require_node(node_id)
        return self._sorted_nodes(nx.descendants(self._graph, node_id))

    def causal_paths_to(
        self, target_id: str, cutoff: Optional[int] = None
    ) -> List[List[str]]:
        """Every simple path from a root cause of ``target_id`` down to it.

        ``cutoff`` bounds the path length (in edges) exactly as
        :func:`networkx.all_simple_paths` does; it exists because path
        enumeration is exponential in the worst case and a dense event graph can
        be pathological. Paths are returned shortest-first, then
        lexicographically, so the output is reproducible.
        """
        self._require_node(target_id)
        sources = self.root_causes(target_id)
        return _enumerate_paths(self._graph, sources, target_id, cutoff)

    def all_paths_to_outcome(
        self, cutoff: Optional[int] = None
    ) -> Dict[str, List[List[str]]]:
        """:meth:`causal_paths_to` for every outcome node, keyed by outcome id."""
        return {o: self.causal_paths_to(o, cutoff=cutoff) for o in self.outcome_nodes()}

    def shortest_causal_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Shortest directed path ``source_id -> target_id``, or ``None``."""
        self._require_node(source_id)
        self._require_node(target_id)
        try:
            return list(nx.shortest_path(self._graph, source_id, target_id))
        except nx.NetworkXNoPath:
            return None

    def root_causes(self, target_id: Optional[str] = None) -> List[str]:
        """In-degree-0 ancestors: claims the graph does not itself explain.

        With ``target_id`` the answer is restricted to that node's ancestors.
        Without it, the roots of every outcome node are returned; when the graph
        has no outcome node at all (an event graph of a run that ended cleanly)
        every in-degree-0 node is returned, because there is then no privileged
        endpoint to trace back from.
        """
        if target_id is not None:
            self._require_node(target_id)
            # A predecessor of an ancestor is itself an ancestor, so in-degree in
            # the ancestor-induced subgraph equals in-degree in the full graph.
            return self._sorted_nodes(
                n for n in nx.ancestors(self._graph, target_id) if self._graph.in_degree(n) == 0
            )

        outcomes = self.outcome_nodes()
        if not outcomes:
            return self._sorted_nodes(
                n for n in self._graph.nodes if self._graph.in_degree(n) == 0
            )
        roots: Set[str] = set()
        for o in outcomes:
            roots.update(self.root_causes(o))
        return self._sorted_nodes(roots)

    # -- derived documents ------------------------------------------------

    def _derived_document(
        self,
        graph: nx.DiGraph,
        operation: str,
        detail: Dict[str, Any],
        owner: Optional[str] = None,
    ) -> GraphDocument:
        """Wrap a derived NetworkX graph back into a document.

        The derivation is stamped into ``meta`` so a slice is always traceable to
        the graph and the operation it came from -- a filtered graph that lost its
        provenance would be indistinguishable from a poor reconstruction.
        """
        doc = from_networkx(
            graph,
            graph_kind=self._doc.graph_kind,
            scope=self._doc.scope,
            owner=owner if owner is not None else self._doc.owner,
        )
        meta = dict(self._doc.meta)
        meta["derivation"] = {"operation": operation, "detail": detail}
        doc.meta = meta
        return doc

    def _induced(
        self,
        node_ids: Iterable[str],
        edge_filter: Optional[Callable[[str, str, Mapping[str, Any]], bool]] = None,
    ) -> nx.DiGraph:
        """Fresh graph over ``node_ids``, copying attribute dicts (never the payloads).

        The :class:`Event` / :class:`GraphEdge` objects are shared by reference --
        they are treated as immutable records -- but the attribute dictionaries
        are new, so mutating the result cannot corrupt the analyzer.
        """
        keep = set(node_ids)
        unknown = keep - set(self._graph.nodes)
        if unknown:
            raise KeyError("unknown node ids: {0}".format(sorted(unknown)))
        out = nx.DiGraph()
        out.graph.update(dict(self._graph.graph))
        for nid, data in self._graph.nodes(data=True):
            if nid in keep:
                out.add_node(nid, **dict(data))
        for u, v, data in self._graph.edges(data=True):
            if u in keep and v in keep and (edge_filter is None or edge_filter(u, v, data)):
                out.add_edge(u, v, **dict(data))
        return out

    def vehicle_subgraph(self, participant_id: str) -> GraphDocument:
        """The part of the graph one participant contributed.

        A node belongs to a participant when it is its canonical owner *or* when
        the participant appears in ``owners`` -- after fusion a merged node is
        owned by several recorders, and dropping it from every vehicle's slice
        would make the fused graph look like nobody's evidence.
        """
        pid = str(participant_id)
        nodes = [
            n
            for n, d in self._graph.nodes(data=True)
            if str(d.get("participant_id")) == pid or pid in (d.get("owners") or [])
        ]
        graph = self._induced(nodes)
        return self._derived_document(
            graph,
            "vehicle_subgraph",
            {"participant_id": pid},
            owner=pid,
        )

    def filter_by_confidence(
        self, min_node: float = 0.0, min_edge: float = 0.0
    ) -> GraphDocument:
        """Keep nodes and edges at or above the given confidences.

        An edge is kept only when both of its endpoints survive: an edge into a
        discarded node is a claim about something the filter just declared
        unreliable.
        """
        node_floor = float(min_node)
        edge_floor = float(min_edge)
        nodes = [
            n
            for n, d in self._graph.nodes(data=True)
            if float(d.get("confidence", 0.0)) >= node_floor
        ]
        graph = self._induced(
            nodes, lambda _u, _v, d: float(d.get("confidence", 0.0)) >= edge_floor
        )
        return self._derived_document(
            graph,
            "filter_by_confidence",
            {"min_node": node_floor, "min_edge": edge_floor},
        )

    def filter_by_provenance(self, provenances: Sequence[Provenance]) -> GraphDocument:
        """Keep only nodes and edges produced by the given layers.

        This is how an ablation asks "what would this reconstruction look like
        without the fused claims" without re-running the pipeline.
        """
        wanted = {p.value if isinstance(p, Provenance) else str(p) for p in provenances}
        if not wanted:
            raise ValueError("filter_by_provenance needs at least one provenance")
        nodes = [
            n for n, d in self._graph.nodes(data=True) if str(d.get("provenance")) in wanted
        ]
        graph = self._induced(nodes, lambda _u, _v, d: str(d.get("provenance")) in wanted)
        return self._derived_document(
            graph, "filter_by_provenance", {"provenances": sorted(wanted)}
        )

    def filter_by_time(self, t0: float, t1: float) -> GraphDocument:
        """Keep events whose temporal support intersects ``[t0, t1]``.

        Intersection rather than "``t_peak`` inside the window": an event that
        started before the window and is still active inside it is part of what
        happened during the window, and cutting it would silently shorten causal
        chains at the window boundary.
        """
        if float(t1) < float(t0):
            raise ValueError("filter_by_time needs t0 <= t1, got {0}, {1}".format(t0, t1))
        window = Interval(float(t0), float(t1))
        nodes = []
        for n, d in self._graph.nodes(data=True):
            start = float(d.get("t_start", d.get("t_peak", 0.0)))
            end = float(d.get("t_end", d.get("t_peak", 0.0)))
            if end < start:
                start, end = end, start
            if window.intersects(Interval(start, end)):
                nodes.append(n)
        graph = self._induced(nodes)
        return self._derived_document(
            graph, "filter_by_time", {"t0": float(t0), "t1": float(t1)}
        )

    def minimal_outcome_subgraph(self) -> GraphDocument:
        """The outcome nodes together with everything that can reach them.

        Anything else in the graph is, by construction, causally irrelevant to
        what happened: it is either a consequence of the outcome or an unrelated
        side observation. This is the graph a report should show.
        """
        outcomes = self.outcome_nodes()
        keep: Set[str] = set(outcomes)
        for o in outcomes:
            keep.update(nx.ancestors(self._graph, o))
        graph = self._induced(keep)
        return self._derived_document(
            graph, "minimal_outcome_subgraph", {"outcomes": list(outcomes)}
        )

    # -- interventions ----------------------------------------------------

    def _baseline(self, cutoff: Optional[int]) -> Dict[str, Any]:
        """Path/ancestor baseline of the intact graph, shared by both removals."""
        cached = self._baseline_cache.get(cutoff)
        if cached is not None:
            return cached
        outcomes = self.outcome_nodes()
        roots = self.root_causes()
        explained = [o for o in outcomes if nx.ancestors(self._graph, o)]
        paths_before = 0
        ancestors_before: Set[str] = set()
        for o in explained:
            paths_before += len(_enumerate_paths(self._graph, roots, o, cutoff))
            ancestors_before.update(nx.ancestors(self._graph, o))
        baseline = {
            "outcomes": outcomes,
            "roots": roots,
            "explained": explained,
            "paths_before": paths_before,
            "ancestors_before": ancestors_before,
        }
        self._baseline_cache[cutoff] = baseline
        return baseline

    def _reachability_report(
        self, reduced: nx.DiGraph, cutoff: Optional[int] = None
    ) -> Dict[str, Any]:
        """Compare a reduced graph against the intact one.

        ``outcome_still_reachable`` asks whether every outcome the intact graph
        *explained* is still explained: still present, and still reached by at
        least one cause. An outcome that had no ancestors to begin with is
        excluded, because a deletion elsewhere cannot be blamed for it.
        """
        base = self._baseline(cutoff)
        surviving_roots = [r for r in base["roots"] if r in reduced]
        disconnected: List[str] = []
        paths_after = 0
        ancestors_after: Set[str] = set()
        for o in base["explained"]:
            if o not in reduced or not nx.ancestors(reduced, o):
                disconnected.append(o)
                continue
            paths_after += len(_enumerate_paths(reduced, surviving_roots, o, cutoff))
            ancestors_after.update(nx.ancestors(reduced, o))
        lost_ancestors = self._sorted_nodes(
            n for n in (base["ancestors_before"] - ancestors_after) if n in self._graph
        )
        return {
            "outcome_still_reachable": not disconnected,
            "lost_paths": int(base["paths_before"] - paths_after),
            "lost_ancestors": lost_ancestors,
            "outcomes_disconnected": disconnected,
            "paths_before": int(base["paths_before"]),
            "paths_after": int(paths_after),
        }

    def remove_node(
        self, node_id: str, cutoff: Optional[int] = None
    ) -> Tuple[GraphDocument, Dict[str, Any]]:
        """Delete a node and report what the deletion cost the explanation.

        This is the structural half of a counterfactual: before replaying a
        scenario without an event, the graph already says whether that event was
        load bearing. Returns the reduced document and the reachability report
        (``outcome_still_reachable``, ``lost_paths``, ``lost_ancestors``,
        ``outcomes_disconnected``).
        """
        self._require_node(node_id)
        keep = [n for n in self._graph.nodes if n != node_id]
        graph = self._induced(keep)
        report = self._reachability_report(graph, cutoff=cutoff)
        doc = self._derived_document(graph, "remove_node", {"node_id": node_id})
        return doc, report

    def remove_edge(
        self, source: str, target: str, cutoff: Optional[int] = None
    ) -> Tuple[GraphDocument, Dict[str, Any]]:
        """Delete one causal claim (an edge) and report the same reachability loss."""
        self._require_node(source)
        self._require_node(target)
        if not self._graph.has_edge(source, target):
            raise KeyError("no edge {0!r} -> {1!r} in this graph".format(source, target))
        graph = self._induced(
            self._graph.nodes, lambda u, v, _d: not (u == source and v == target)
        )
        report = self._reachability_report(graph, cutoff=cutoff)
        doc = self._derived_document(
            graph, "remove_edge", {"source": source, "target": target}
        )
        return doc, report

    def candidate_intervention_nodes(
        self, cutoff: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Rank the nodes worth replaying counterfactually.

        A node qualifies when deleting it destroys at least one causal path to an
        outcome; ``disconnects_outcome`` marks the strict cut vertices, whose
        removal leaves an outcome with no explanation at all. Both are returned
        -- cut vertices first, then by how many paths they cut -- because the
        counterfactual layer needs the ranking, not just the binary: a node that
        cuts nine of ten explanations is a better replay candidate than one that
        cuts a single redundant branch, even though neither disconnects anything.

        Outcome nodes are never candidates: removing the collision to discover
        that the collision no longer happens explains nothing.
        """
        outcomes = set(self.outcome_nodes())
        relevant: Set[str] = set()
        for o in outcomes:
            relevant.update(nx.ancestors(self._graph, o))
        candidates: List[Dict[str, Any]] = []
        for node_id in self._sorted_nodes(relevant - outcomes):
            _doc, report = self.remove_node(node_id, cutoff=cutoff)
            if report["lost_paths"] <= 0 and not report["outcomes_disconnected"]:
                continue
            data = self._graph.nodes[node_id]
            candidates.append(
                {
                    "event_id": node_id,
                    "event_type": str(data.get("event_type")),
                    "participant_id": str(data.get("participant_id")),
                    "t_peak": float(data.get("t_peak")),
                    "paths_cut": int(report["lost_paths"]),
                    "disconnects_outcome": bool(report["outcomes_disconnected"]),
                }
            )
        candidates.sort(
            key=lambda c: (
                0 if c["disconnects_outcome"] else 1,
                -int(c["paths_cut"]),
                float(c["t_peak"]),
                str(c["event_id"]),
            )
        )
        return candidates

    # -- cross-graph comparison ------------------------------------------

    def _node_keys(
        self, doc: GraphDocument, subject_map: Optional[Mapping[str, str]] = None
    ) -> Dict[Tuple[str, str, str, int], List[str]]:
        keys: Dict[Tuple[str, str, str, int], List[str]] = {}
        for ev in doc.nodes:
            keys.setdefault(
                canonical_key(ev, subject_map, self._time_bucket_s), []
            ).append(ev.event_id)
        return keys

    def _edge_keys(
        self, doc: GraphDocument, subject_map: Optional[Mapping[str, str]] = None
    ) -> Dict[Tuple[Any, Any, str], List[Tuple[str, str, str]]]:
        by_id: Dict[str, Event] = {n.event_id: n for n in doc.nodes}
        keys: Dict[Tuple[Any, Any, str], List[Tuple[str, str, str]]] = {}
        for e in doc.edges:
            src = by_id.get(e.source)
            tgt = by_id.get(e.target)
            if src is None or tgt is None:
                raise KeyError(
                    "edge {0}->{1} refers to a node absent from the document".format(
                        e.source, e.target
                    )
                )
            key = canonical_edge_key(
                src, tgt, str(e.edge_type), subject_map, self._time_bucket_s
            )
            keys.setdefault(key, []).append((e.source, e.target, str(e.edge_type)))
        return keys

    def compare_to(
        self,
        other: GraphDocument,
        subject_map_self: Optional[Mapping[str, str]] = None,
        subject_map_other: Optional[Mapping[str, str]] = None,
    ) -> Dict[str, Any]:
        """Set difference against another graph under canonical event identity.

        Identity is :func:`cdf.graph.matching.canonical_key`, i.e. type, owner,
        resolved subject and time bucket -- event ids are never comparable across
        graphs. The result is symmetric by construction: ``only_self``,
        ``only_other`` and ``both``.

        Counting convention: the ``only_*`` counts are counts of *records*, while
        ``n_nodes_both`` / ``n_edges_both`` count shared *claims* (canonical
        keys). The two differ only when bucketing collapses two records of one
        graph onto a single key; the ``*_both`` lists then pair the first record
        of each side, and the collision itself is visible as the size mismatch.
        """
        self_nodes = self._node_keys(self._doc, subject_map_self)
        other_nodes = self._node_keys(other, subject_map_other)
        self_edges = self._edge_keys(self._doc, subject_map_self)
        other_edges = self._edge_keys(other, subject_map_other)

        shared_nodes = sorted(set(self_nodes) & set(other_nodes))
        shared_edges = sorted(set(self_edges) & set(other_edges))
        return {
            "nodes_only_self": sorted(
                i for k, ids in self_nodes.items() if k not in other_nodes for i in ids
            ),
            "nodes_only_other": sorted(
                i for k, ids in other_nodes.items() if k not in self_nodes for i in ids
            ),
            "nodes_both": [
                (self_nodes[k][0], other_nodes[k][0]) for k in shared_nodes
            ],
            "edges_only_self": sorted(
                e for k, es in self_edges.items() if k not in other_edges for e in es
            ),
            "edges_only_other": sorted(
                e for k, es in other_edges.items() if k not in self_edges for e in es
            ),
            "edges_both": [(self_edges[k][0], other_edges[k][0]) for k in shared_edges],
            "n_nodes_only_self": sum(
                len(ids) for k, ids in self_nodes.items() if k not in other_nodes
            ),
            "n_nodes_only_other": sum(
                len(ids) for k, ids in other_nodes.items() if k not in self_nodes
            ),
            "n_nodes_both": len(shared_nodes),
            "n_edges_only_self": sum(
                len(es) for k, es in self_edges.items() if k not in other_edges
            ),
            "n_edges_only_other": sum(
                len(es) for k, es in other_edges.items() if k not in self_edges
            ),
            "n_edges_both": len(shared_edges),
            "time_bucket_s": self._time_bucket_s,
        }

    def knowledge_gain(
        self,
        baseline: GraphDocument,
        reference: GraphDocument,
        subject_map_self: Optional[Mapping[str, str]] = None,
        subject_map_baseline: Optional[Mapping[str, str]] = None,
        subject_map_reference: Optional[Mapping[str, str]] = None,
        tolerance_s: Optional[float] = None,
    ) -> Dict[str, Any]:
        """What this graph recovers of ``reference`` that ``baseline`` misses.

        The intended reading is "fusion versus the best single vehicle, judged
        against the oracle": ``reference`` supplies the set of claims that are
        worth having, ``baseline`` is what was already known, and the gain is the
        part of the reference this graph recovers and the baseline does not.
        Claims this graph adds that the reference does not contain are *not* a
        gain -- they are false positives and are scored by
        :func:`cdf.graph.metrics.graph_structure_metrics`.

        ``tolerance_s`` selects how a claim is judged to be "the same claim":

        * given, the same tolerant one-to-one assignment
          (:func:`cdf.graph.matching.match_events`) that the structural metrics
          use. **This is what callers should pass**, so that the gain reported
          here and the F1 reported there describe the same correspondence.
        * omitted, exact equality of the bucketed canonical key. That is far
          stricter -- an event 50 ms from its reference counterpart lands in a
          different bucket and never matches -- and it was measured to understate
          recall by a factor of five on a three-vehicle run (0.095 against 0.500)
          while the metrics said fusion clearly helped. It is retained only for
          callers that genuinely want exact-bucket identity.
        """
        if tolerance_s is not None:
            return self._knowledge_gain_matched(
                baseline,
                reference,
                float(tolerance_s),
                subject_map_self,
                subject_map_baseline,
                subject_map_reference,
            )

        self_nodes = self._node_keys(self._doc, subject_map_self)
        base_nodes = self._node_keys(baseline, subject_map_baseline)
        ref_nodes = self._node_keys(reference, subject_map_reference)
        self_edges = self._edge_keys(self._doc, subject_map_self)
        base_edges = self._edge_keys(baseline, subject_map_baseline)
        ref_edges = self._edge_keys(reference, subject_map_reference)

        node_gain_keys = (set(self_nodes) & set(ref_nodes)) - set(base_nodes)
        edge_gain_keys = (set(self_edges) & set(ref_edges)) - set(base_edges)

        nodes_gained = sorted(i for k in node_gain_keys for i in self_nodes[k])
        edges_gained = sorted(e for k in edge_gain_keys for e in self_edges[k])

        return {
            "nodes_gained": nodes_gained,
            "edges_gained": edges_gained,
            "n_nodes_gained": len(nodes_gained),
            "n_edges_gained": len(edges_gained),
            "baseline_node_recall": _recall(set(base_nodes), set(ref_nodes)),
            "self_node_recall": _recall(set(self_nodes), set(ref_nodes)),
            "baseline_edge_recall": _recall(set(base_edges), set(ref_edges)),
            "self_edge_recall": _recall(set(self_edges), set(ref_edges)),
            "n_reference_nodes": len(ref_nodes),
            "n_reference_edges": len(ref_edges),
            "time_bucket_s": self._time_bucket_s,
        }

    def _knowledge_gain_matched(
        self,
        baseline: GraphDocument,
        reference: GraphDocument,
        tolerance_s: float,
        subject_map_self: Optional[Mapping[str, str]],
        subject_map_baseline: Optional[Mapping[str, str]],
        subject_map_reference: Optional[Mapping[str, str]],
    ) -> Dict[str, Any]:
        """Knowledge gain under tolerant one-to-one matching.

        Both this graph and the baseline are matched independently against the
        reference; the gain is the set of reference claims this graph recovers
        and the baseline does not. Working in the *reference's* id space is what
        makes the two sides comparable -- the two graphs never share event ids.
        """
        self_match = match_events(
            self._doc.nodes,
            reference.nodes,
            tolerance_s,
            subject_map_a=subject_map_self,
            subject_map_b=subject_map_reference,
        )
        base_match = match_events(
            baseline.nodes,
            reference.nodes,
            tolerance_s,
            subject_map_a=subject_map_baseline,
            subject_map_b=subject_map_reference,
        )
        self_map = dict(self_match["map_a_to_b"])
        base_map = dict(base_match["map_a_to_b"])
        self_ref = set(self_map.values())
        base_ref = set(base_map.values())

        gained_ref_nodes = self_ref - base_ref
        by_ref = {v: k for k, v in self_map.items()}
        # Report ids from THIS graph, matching the contract the bucketed path
        # established: callers look each id up in the graph it was reported from
        # and enrich it there.
        nodes_gained = sorted(
            by_ref[rid] for rid in gained_ref_nodes if rid in by_ref
        )

        self_edges = self._mapped_edge_keys(self._doc, self_map)
        base_edges = self._mapped_edge_keys(baseline, base_map)
        ref_edges = {
            (e.source, e.target, e.edge_type) for e in reference.edges
        }
        gained_edges_keys = (self_edges & ref_edges) - (base_edges & ref_edges)
        # Translate back into this graph's own ids, for the same reason.
        self_edge_by_key = {}
        for e in self._doc.edges:
            src = self_map.get(e.source)
            tgt = self_map.get(e.target)
            if src is not None and tgt is not None:
                self_edge_by_key.setdefault(
                    (src, tgt, e.edge_type), (e.source, e.target, e.edge_type)
                )
        edges_gained = sorted(
            self_edge_by_key[k] for k in gained_edges_keys if k in self_edge_by_key
        )

        n_ref_nodes = len(reference.nodes)
        n_ref_edges = len(ref_edges)
        return {
            "nodes_gained": nodes_gained,
            "edges_gained": edges_gained,
            "n_nodes_gained": len(nodes_gained),
            "n_edges_gained": len(edges_gained),
            "baseline_node_recall": (len(base_ref) / n_ref_nodes) if n_ref_nodes else 0.0,
            "self_node_recall": (len(self_ref) / n_ref_nodes) if n_ref_nodes else 0.0,
            "baseline_edge_recall": (
                len(base_edges & ref_edges) / n_ref_edges if n_ref_edges else 0.0
            ),
            "self_edge_recall": (
                len(self_edges & ref_edges) / n_ref_edges if n_ref_edges else 0.0
            ),
            "n_reference_nodes": n_ref_nodes,
            "n_reference_edges": n_ref_edges,
            "tolerance_s": float(tolerance_s),
            "matching": "tolerant_assignment",
        }

    @staticmethod
    def _mapped_edge_keys(
        doc: GraphDocument, node_map: Mapping[str, str]
    ) -> "set":
        """Edges of ``doc`` expressed in the reference's id space.

        An edge whose endpoints were not both matched cannot be compared at all,
        so it is dropped here rather than counted as recovered -- it is a claim
        about nodes the reference does not agree exist.
        """
        out = set()
        for e in doc.edges:
            src = node_map.get(e.source)
            tgt = node_map.get(e.target)
            if src is None or tgt is None:
                continue
            out.add((src, tgt, e.edge_type))
        return out

    # -- reporting --------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """Structural summary plus the causal-query quantities used in reports."""
        out: Dict[str, Any] = dict(graph_summary(self._doc))
        outcomes = self.outcome_nodes()
        paths = self.all_paths_to_outcome()
        n_paths = sum(len(p) for p in paths.values())
        longest = max((len(p) for ps in paths.values() for p in ps), default=0)
        node_conf = [float(n.confidence) for n in self._doc.nodes]
        edge_conf = [float(e.confidence) for e in self._doc.edges]
        out.update(
            {
                "outcome_nodes": outcomes,
                "n_outcome_nodes": len(outcomes),
                "root_causes": self.root_causes(),
                "n_root_causes": len(self.root_causes()),
                "n_causal_paths_to_outcome": n_paths,
                "longest_causal_path_nodes": longest,
                "n_intervention_candidates": len(self.candidate_intervention_nodes()),
                "mean_node_confidence": (
                    float(sum(node_conf) / len(node_conf)) if node_conf else 0.0
                ),
                "mean_edge_confidence": (
                    float(sum(edge_conf) / len(edge_conf)) if edge_conf else 0.0
                ),
            }
        )
        return out


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def _recall(found: Set[Any], reference: Set[Any]) -> float:
    """Fraction of ``reference`` covered by ``found`` (``0.0`` when empty)."""
    if not reference:
        return 0.0
    return float(len(found & reference)) / float(len(reference))


def _enumerate_paths(
    graph: nx.DiGraph,
    sources: Iterable[str],
    target: str,
    cutoff: Optional[int] = None,
) -> List[List[str]]:
    """All simple paths from any of ``sources`` to ``target``, deterministically ordered.

    Sources absent from ``graph`` (deleted by a counterfactual) and the target
    itself are skipped rather than raising, because the callers deliberately
    replay the *original* source set against a reduced graph.
    """
    if target not in graph:
        return []
    out: List[List[str]] = []
    for source in sorted(set(sources)):
        if source == target or source not in graph:
            continue
        for path in nx.all_simple_paths(graph, source, target, cutoff=cutoff):
            out.append(list(path))
    out.sort(key=lambda p: (len(p), tuple(p)))
    return out
