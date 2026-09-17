"""Conversion between :class:`GraphDocument`, NetworkX and on-disk formats.

This is the single bridge between our record schema and NetworkX, so that graph
construction, fusion, analysis and evaluation all agree on node/edge attribute
names. GraphML is emitted alongside JSON so graphs can be opened in external
tools (Gephi, yEd, Cytoscape); because GraphML only supports scalar attributes,
nested structures are flattened to JSON strings on the way out.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import networkx as nx

from ..common.io import read_json, write_json
from ..common.schemas import (
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
    to_jsonable,
)

__all__ = [
    "to_networkx",
    "from_networkx",
    "save_graph",
    "load_graph",
    "write_graphml",
    "graph_summary",
]


# ---------------------------------------------------------------------------
# NetworkX bridge
# ---------------------------------------------------------------------------


def to_networkx(doc: GraphDocument) -> nx.DiGraph:
    """Build a :class:`networkx.DiGraph` carrying the full record payloads.

    Node attributes mirror :class:`Event` fields; each node additionally carries
    ``event`` (the :class:`Event` object itself) so analysis code can work with
    typed records instead of loose dicts. Edge attributes mirror
    :class:`GraphEdge` and likewise carry ``edge``.

    Parallel edges of different types between the same pair are collapsed onto a
    ``DiGraph`` keyed by ``(source, target)``; when that happens the edge with the
    higher confidence wins and the loser is recorded under ``shadowed``. Causal
    DAG construction never produces parallel edges of different types between the
    same pair, so this only affects heterogeneous event graphs.
    """
    g = nx.DiGraph()
    g.graph.update(
        {
            "graph_kind": doc.graph_kind,
            "scope": doc.scope.value if isinstance(doc.scope, Provenance) else str(doc.scope),
            "owner": doc.owner or "",
            "run_id": doc.run_id,
            "scenario_id": doc.scenario_id,
            "seed": doc.seed,
            "schema_version": doc.schema_version,
        }
    )
    for node in doc.nodes:
        g.add_node(
            node.event_id,
            event=node,
            event_type=node.event_type.value
            if isinstance(node.event_type, EventType)
            else str(node.event_type),
            participant_id=node.participant_id,
            subject=node.subject or "",
            t_start=float(node.t_start),
            t_peak=float(node.t_peak),
            t_end=float(node.t_end) if node.t_end is not None else float(node.t_peak),
            confidence=float(node.confidence),
            provenance=node.provenance.value
            if isinstance(node.provenance, Provenance)
            else str(node.provenance),
            owners=list(node.owners),
            values=dict(node.values),
        )
    for edge in doc.edges:
        if g.has_edge(edge.source, edge.target):
            existing: GraphEdge = g.edges[edge.source, edge.target]["edge"]
            if float(edge.confidence) <= float(existing.confidence):
                g.edges[edge.source, edge.target].setdefault("shadowed", []).append(
                    to_jsonable(edge)
                )
                continue
            shadowed = g.edges[edge.source, edge.target].get("shadowed", [])
            shadowed.append(to_jsonable(existing))
        else:
            shadowed = []
        g.add_edge(
            edge.source,
            edge.target,
            edge=edge,
            edge_type=edge.edge_type,
            confidence=float(edge.confidence),
            provenance=edge.provenance.value
            if isinstance(edge.provenance, Provenance)
            else str(edge.provenance),
            rule=edge.rule or "",
            temporal_relation=edge.temporal_relation or "",
            owners=list(edge.owners),
            shadowed=shadowed,
        )
    return g


def from_networkx(
    g: nx.DiGraph,
    graph_kind: Optional[str] = None,
    scope: Optional[Provenance] = None,
    owner: Optional[str] = None,
) -> GraphDocument:
    """Rebuild a :class:`GraphDocument` from a graph produced by :func:`to_networkx`.

    Node/edge payloads are taken from the ``event``/``edge`` attributes, so a
    subgraph or filtered view round-trips without losing evidence or provenance.
    """
    meta = dict(g.graph)
    nodes: List[Event] = []
    for _nid, data in g.nodes(data=True):
        ev = data.get("event")
        if ev is None:
            raise ValueError(
                "node {0!r} has no 'event' payload; graph was not built by to_networkx".format(_nid)
            )
        nodes.append(ev)
    edges: List[GraphEdge] = []
    for _u, _v, data in g.edges(data=True):
        ed = data.get("edge")
        if ed is None:
            raise ValueError("edge {0}->{1} has no 'edge' payload".format(_u, _v))
        edges.append(ed)

    resolved_scope = scope
    if resolved_scope is None:
        resolved_scope = Provenance(meta.get("scope", "local"))

    return GraphDocument(
        graph_kind=graph_kind or meta.get("graph_kind", "causal"),
        scope=resolved_scope,
        owner=owner if owner is not None else (meta.get("owner") or None),
        run_id=meta.get("run_id", ""),
        scenario_id=meta.get("scenario_id", ""),
        seed=int(meta.get("seed", 0)),
        nodes=nodes,
        edges=edges,
        meta={
            k: v
            for k, v in meta.items()
            if k
            not in {"graph_kind", "scope", "owner", "run_id", "scenario_id", "seed", "schema_version"}
        },
    )


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def save_graph(
    doc: GraphDocument, json_path: Union[str, Path], graphml_path: Optional[Union[str, Path]] = None
) -> Path:
    """Write a graph as JSON and, when a path is given, also as GraphML."""
    out = write_json(json_path, doc.to_dict())
    if graphml_path is not None:
        write_graphml(doc, graphml_path)
    return out


def load_graph(path: Union[str, Path], expect_scope: Optional[Provenance] = None) -> GraphDocument:
    """Load a graph document, optionally asserting which layer produced it.

    ``expect_scope`` is the mechanism that keeps an oracle graph from being read
    by an inference stage through a mis-wired path: the mismatch raises instead
    of silently succeeding.
    """
    doc = GraphDocument.from_dict(read_json(path))
    if expect_scope is not None and doc.scope is not expect_scope:
        raise ValueError(
            "graph at {0} has scope {1!r}, expected {2!r}".format(
                path, doc.scope.value, expect_scope.value
            )
        )
    return doc


def write_graphml(doc: GraphDocument, path: Union[str, Path]) -> Path:
    """Serialise a graph to GraphML with flattened, scalar-only attributes."""
    g = to_networkx(doc)
    flat = nx.DiGraph()
    flat.graph.update({k: _scalar(v) for k, v in g.graph.items()})
    for nid, data in g.nodes(data=True):
        flat.add_node(str(nid), **{k: _scalar(v) for k, v in data.items() if k != "event"})
    for u, v, data in g.edges(data=True):
        flat.add_edge(str(u), str(v), **{k: _scalar(v2) for k, v2 in data.items() if k != "edge"})
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(flat, str(p))
    return p


def _scalar(value: Any) -> Any:
    """Coerce an attribute to something GraphML accepts."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)):
        return value
    return json.dumps(to_jsonable(value), sort_keys=True, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def graph_summary(doc: GraphDocument) -> Dict[str, Any]:
    """Compact structural summary used in diagnostics and reports."""
    g = to_networkx(doc)
    by_type: Dict[str, int] = {}
    for n in doc.nodes:
        key = n.event_type.value if isinstance(n.event_type, EventType) else str(n.event_type)
        by_type[key] = by_type.get(key, 0) + 1
    by_edge: Dict[str, int] = {}
    for e in doc.edges:
        by_edge[e.edge_type] = by_edge.get(e.edge_type, 0) + 1
    return {
        "graph_kind": doc.graph_kind,
        "scope": doc.scope.value,
        "owner": doc.owner,
        "n_nodes": len(doc.nodes),
        "n_edges": len(doc.edges),
        "is_dag": bool(nx.is_directed_acyclic_graph(g)),
        "node_types": dict(sorted(by_type.items())),
        "edge_types": dict(sorted(by_edge.items())),
        "participants": sorted({n.participant_id for n in doc.nodes}),
    }
