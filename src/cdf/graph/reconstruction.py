"""From the fused causal DAG to a readable account of the incident.

Three artifacts come out of this module, and the order matters.

``incident_reconstruction.json``
    What happened. Per collision: who was involved, when it happened on the
    common clock, where it sits in the order of impacts, the causal chains that
    lead to it, the evidence behind each link, and -- explicitly -- what could
    not be established.

``causal_attribution.json``
    Which behaviours contributed, as a **hypothesis derived from the graph
    alone**. Counterfactual replay may later confirm, weaken or leave it
    unresolved; until it does, the document says so in the ``validation`` block
    of every contributor.

The narrative
    A sentence per link, generated from the structured records by fixed
    templates. No language model is involved and none is needed: the graph
    already says what happened, and the templates only read it out.

Vocabulary discipline: *causal initiator*, *causal contributor*, *shared* and
*joint causal contribution*, *causal chain*, *insufficient evidence*. Never
fault, liability, blame or a percentage. A chain is a statement about what the
evidence supports, not about what anybody owed anybody.

Nothing here reads a scenario file, an action id or an oracle artifact: a chain
is read off the fused graph, and the behaviours it names are the episodes of
:mod:`cdf.graph.episodes`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.schemas import (
    SCHEMA_VERSIONS,
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
)
from .analysis import GraphAnalyzer
from .episodes import CausalEpisode, extract_episodes

__all__ = [
    "ATTRIBUTION_CLASSES",
    "ancestors_of_outcome",
    "causal_paths_to_outcome",
    "root_contributors",
    "explain_outcome",
    "build_incident_reconstruction",
    "build_attribution_hypothesis",
]


#: Graph-only classes. ``joint_contribution`` is deliberately absent: no amount
#: of graph reading can establish that two behaviours were *jointly* necessary --
#: only a replay that removes both can. The counterfactual layer adds it.
ATTRIBUTION_CLASSES: Tuple[str, ...] = (
    "single_initiator",
    "shared_contribution",
    "insufficient_evidence",
)

_OUTCOME_TYPES = frozenset(
    {EventType.COLLISION.value, EventType.NEAR_MISS.value}
)
_PREVENTIVE = CausalEdgeType.PREVENTS.value


def _type_of(node: Event) -> str:
    return node.event_type.value if isinstance(node.event_type, EventType) else str(
        node.event_type
    )


# ---------------------------------------------------------------------------
# Graph queries, under the names the reconstruction speaks in
# ---------------------------------------------------------------------------


def ancestors_of_outcome(analyzer: GraphAnalyzer, outcome_id: str) -> List[str]:
    """Every node that can reach ``outcome_id``, sorted."""
    return sorted(analyzer.ancestors(outcome_id))


def causal_paths_to_outcome(
    analyzer: GraphAnalyzer, outcome_id: str, cutoff: Optional[int] = None
) -> List[List[str]]:
    """Root-to-outcome causal paths, deterministically ordered."""
    return analyzer.causal_paths_to(outcome_id, cutoff=cutoff)


def root_contributors(
    analyzer: GraphAnalyzer,
    outcome_id: str,
    episodes: Sequence[CausalEpisode],
) -> List[CausalEpisode]:
    """The behavioural episodes at the roots of the paths into ``outcome_id``.

    A root of the causal DAG is a node nothing else explains. Reported as a
    *behaviour* rather than as a node, because "B braked hard at 4.0 s" is an
    answer and "fused:B:HARD_BRAKE:1c2f..." is not.
    """
    by_node: Dict[str, CausalEpisode] = {}
    for episode in episodes:
        for node_id in episode.node_ids:
            by_node[node_id] = episode
    # ``root_causes`` already restricts itself to this outcome's ancestors.
    out: Dict[str, CausalEpisode] = {}
    for node_id in analyzer.root_causes(outcome_id):
        episode = by_node.get(node_id)
        if episode is not None:
            out[episode.episode_id] = episode
    return sorted(out.values(), key=lambda e: (e.t_start, e.participant_id, e.kind))


# ---------------------------------------------------------------------------
# Chains
# ---------------------------------------------------------------------------


def _chain_signature(
    path: Sequence[str], nodes: Mapping[str, Event], participants: Set[str]
) -> Tuple[Tuple[str, str], ...]:
    """Semantic fingerprint of a path, so two ways of saying it collapse to one."""
    signature: List[Tuple[str, str]] = []
    for node_id in path:
        node = nodes[node_id]
        actor = str(node.participant_id)
        subject = node.subject
        if subject not in (None, "", "self") and str(subject) in participants:
            type_value = _type_of(node)
            if type_value not in (
                EventType.RANGE_DECREASING.value,
                EventType.RAPID_CLOSING.value,
                EventType.LOW_TTC.value,
                EventType.CRITICAL_TTC.value,
                EventType.CONFLICT_REGION_ENTRY.value,
                EventType.PREDICTED_PATH_CONFLICT.value,
                EventType.LATERAL_CROSSING.value,
                EventType.NEAR_MISS.value,
                EventType.COLLISION.value,
            ):
                actor = str(subject)
        step = (_type_of(node), actor)
        if not signature or signature[-1] != step:
            signature.append(step)
    return tuple(signature)


def _describe_link(source: Event, edge: Any, target: Event, participants: Set[str]) -> str:
    """One sentence for one causal link, from the record alone."""
    verbs = {
        CausalEdgeType.TRIGGERS.value: "led to",
        CausalEdgeType.CONTRIBUTES_TO.value: "contributed to",
        CausalEdgeType.INCREASES_RISK_OF.value: "increased the risk of",
        CausalEdgeType.CAUSES_OUTCOME.value: "resulted in",
        CausalEdgeType.PREVENTS.value: "prevented",
    }
    return "{0} {1} {2}".format(
        _phrase(source, participants), verbs.get(edge.edge_type, "relates to"),
        _phrase(target, participants),
    )


_PHRASES = {
    EventType.BRAKE_ONSET.value: "{a} braking",
    EventType.HARD_BRAKE.value: "{a} braking hard",
    EventType.DECELERATION.value: "{a} slowing",
    EventType.HARD_DECELERATION.value: "{a} slowing sharply",
    EventType.TARGET_DECELERATION.value: "{a} slowing sharply",
    EventType.THROTTLE_ONSET.value: "{a} opening the throttle",
    EventType.ACCELERATION.value: "{a} accelerating",
    EventType.VEHICLE_STARTED.value: "{a} moving off",
    EventType.STEER_ONSET.value: "{a} steering",
    EventType.SIGNIFICANT_HEADING_CHANGE.value: "{a} changing heading",
    EventType.LANE_CHANGE_LIKE_MANEUVER.value: "{a} moving out of its lane",
    EventType.CUT_IN_LIKE_MOTION.value: "{a} cutting in front of {b}",
    EventType.RANGE_DECREASING.value: "the gap between {a} and {b} closing",
    EventType.RAPID_CLOSING.value: "{a} closing rapidly on {b}",
    EventType.LOW_TTC.value: "{a}'s time-to-collision with {b} falling",
    EventType.CRITICAL_TTC.value: "{a}'s time-to-collision with {b} becoming critical",
    EventType.LATERAL_CROSSING.value: "{b} crossing {a}'s path",
    EventType.PREDICTED_PATH_CONFLICT.value: "a predicted path conflict between {a} and {b}",
    EventType.CONFLICT_REGION_ENTRY.value: "{a} entering the conflict region with {b}",
    EventType.COLLISION.value: "the impact between {a} and {b}",
    EventType.NEAR_MISS.value: "{a} and {b} passing without contact",
    EventType.POST_IMPACT_STOP.value: "{a} coming to rest",
}


def _phrase(node: Event, participants: Set[str]) -> str:
    type_value = _type_of(node)
    actor = str(node.participant_id)
    subject = node.subject
    other = str(subject) if subject not in (None, "", "self") and str(subject) in participants else None
    template = _PHRASES.get(type_value)
    if template is None:
        return "{0} ({1})".format(type_value.lower().replace("_", " "), actor)
    if "{b}" in template and other is None:
        other = "another vehicle"
    if type_value in (
        EventType.DECELERATION.value,
        EventType.HARD_DECELERATION.value,
        EventType.TARGET_DECELERATION.value,
        EventType.BRAKE_ONSET.value,
        EventType.HARD_BRAKE.value,
    ) and other is not None:
        # A unary behaviour recorded about another vehicle is that vehicle's.
        actor = other
    return template.format(a=actor, b=other or "another vehicle")


# ---------------------------------------------------------------------------
# Incident reconstruction
# ---------------------------------------------------------------------------


def build_incident_reconstruction(
    fused: GraphDocument,
    cfg: Config,
    participants: Sequence[str],
    alignment: Optional[Mapping[str, Any]] = None,
    episodes: Optional[Sequence[CausalEpisode]] = None,
) -> Dict[str, Any]:
    """Reconstruct every outcome in the fused graph, with its causal chains."""
    known = set(str(p) for p in participants)
    analyzer = GraphAnalyzer(fused, cfg)
    nodes = {n.event_id: n for n in fused.nodes}
    edges = {(e.source, e.target): e for e in fused.edges}
    if episodes is None:
        episodes = extract_episodes(fused, cfg, participants)
    by_node: Dict[str, CausalEpisode] = {}
    for episode in episodes:
        for node_id in episode.node_ids:
            by_node[node_id] = episode

    max_paths = int(cfg.get("graph.reconstruction.max_chains_per_outcome", 8))
    cutoff = cfg.get("graph.reconstruction.max_chain_length", None)
    cutoff = int(cutoff) if cutoff is not None else None

    outcome_ids = [
        n.event_id for n in fused.nodes if _type_of(n) in _OUTCOME_TYPES
    ]
    outcome_ids.sort(key=lambda i: (float(nodes[i].t_peak), i))
    collisions = [i for i in outcome_ids if _type_of(nodes[i]) == EventType.COLLISION.value]

    incidents: List[Dict[str, Any]] = []
    for order, outcome_id in enumerate(outcome_ids, start=1):
        node = nodes[outcome_id]
        pair = sorted({str(node.participant_id)} | (
            {str(node.subject)} if node.subject not in (None, "", "self")
            and str(node.subject) in known else set()
        ))
        uncertainties: List[str] = []
        if len(pair) < 2:
            uncertainties.append(
                "the other party to this outcome could not be named from the "
                "exchanged evidence"
            )

        seen: Dict[Tuple[Tuple[str, str], ...], Dict[str, Any]] = {}
        for path in causal_paths_to_outcome(analyzer, outcome_id, cutoff=cutoff):
            signature = _chain_signature(path, nodes, known)
            if signature in seen:
                continue
            links = []
            confidences = []
            for a, b in zip(path, path[1:]):
                edge = edges.get((a, b))
                if edge is None:
                    continue
                confidences.append(float(edge.confidence))
                links.append(
                    {
                        "source": a,
                        "target": b,
                        "edge_type": edge.edge_type,
                        "rule": edge.rule,
                        "origin": (edge.detail or {}).get("origin", "local"),
                        "confidence": round(float(edge.confidence), 6),
                        "delta_t_s": (edge.detail or {}).get("delta_t_s"),
                        "sentence": _describe_link(nodes[a], edge, nodes[b], known),
                    }
                )
            if not links:
                continue
            root_episode = by_node.get(path[0])
            seen[signature] = {
                "chain_id": "chain:{0}:{1}".format(outcome_id[-10:], len(seen) + 1),
                "node_ids": list(path),
                "links": links,
                "n_links": len(links),
                "confidence": round(min(confidences), 6) if confidences else 0.0,
                "root_node_id": path[0],
                "root_episode_id": root_episode.episode_id if root_episode else None,
                "root_participant": (
                    root_episode.participant_id if root_episode
                    else str(nodes[path[0]].participant_id)
                ),
                "preventive": any(l["edge_type"] == _PREVENTIVE for l in links),
                "cross_participant": any(
                    l["origin"] == "post_fusion_inference" for l in links
                ),
                "narrative": [l["sentence"] for l in links],
            }
        chains = sorted(
            seen.values(), key=lambda c: (-c["confidence"], c["n_links"], c["chain_id"])
        )
        if len(chains) > max_paths:
            uncertainties.append(
                "{0} causal chains reach this outcome; the {1} best supported are "
                "reported (graph.reconstruction.max_chains_per_outcome)".format(
                    len(chains), max_paths
                )
            )
            chains = chains[:max_paths]
        if not chains:
            uncertainties.append(
                "no causal chain in the fused graph reaches this outcome"
            )

        roots = root_contributors(analyzer, outcome_id, episodes)
        incidents.append(
            {
                "outcome_id": outcome_id,
                "outcome_type": _type_of(node),
                "participants": pair,
                "t_common": round(float(node.t_peak), 6),
                "order": order,
                "confidence": round(float(node.confidence), 6),
                "owners": list(node.owners),
                "preceding_events": [
                    {
                        "event_id": i,
                        "event_type": _type_of(nodes[i]),
                        "participant_id": nodes[i].participant_id,
                        "subject": nodes[i].subject,
                        "t_common": round(float(nodes[i].t_peak), 6),
                    }
                    for i in sorted(
                        analyzer.ancestors(outcome_id),
                        key=lambda i: (float(nodes[i].t_peak), i),
                    )
                ],
                "chains": chains,
                "root_contributors": [e.to_dict() for e in roots],
                "uncertainties": uncertainties,
            }
        )

    return {
        "schema_version": SCHEMA_VERSIONS.get("fusion_diagnostics", "1.0.0"),
        "run_id": fused.run_id,
        "scenario_id": fused.scenario_id,
        "seed": fused.seed,
        "time_domain": "common",
        "time_reference": (alignment or {}).get("reference"),
        "participants": sorted(known),
        "n_collisions": len(collisions),
        "collision_order": [
            {
                "outcome_id": i,
                "participants": sorted(
                    {str(nodes[i].participant_id)}
                    | ({str(nodes[i].subject)} if nodes[i].subject in known else set())
                ),
                "t_common": round(float(nodes[i].t_peak), 6),
            }
            for i in collisions
        ],
        "episodes": [e.to_dict() for e in episodes],
        "incidents": incidents,
        "note": (
            "Reconstructed from the exchanged vehicle logs alone. Times are on "
            "the common clock estimated by fusion; no simulator state was used."
        ),
    }


# ---------------------------------------------------------------------------
# Attribution hypothesis, from the graph only
# ---------------------------------------------------------------------------


def build_attribution_hypothesis(
    reconstruction: Mapping[str, Any],
    fused: GraphDocument,
    cfg: Config,
) -> Dict[str, Any]:
    """Which behaviours the graph says contributed, before any replay.

    A contributor is a behavioural episode that (a) lies at the root of at least
    one causal chain into a collision, and (b) is not purely preventive. Chains
    made only of preventive links are reported separately as preventive
    behaviour, because a vehicle that braked and avoided the crash is not a
    contributor to it.
    """
    min_conf = float(cfg.get("graph.attribution.min_chain_confidence", 0.15))
    episodes = {e["episode_id"]: e for e in reconstruction.get("episodes", [])}
    results: List[Dict[str, Any]] = []

    for incident in reconstruction.get("incidents", []):
        if incident["outcome_type"] != EventType.COLLISION.value:
            continue
        contributors: Dict[str, Dict[str, Any]] = {}
        preventive: Dict[str, Dict[str, Any]] = {}
        for chain in incident.get("chains", []):
            if chain["confidence"] < min_conf:
                continue
            episode_id = chain.get("root_episode_id")
            bucket = preventive if chain["preventive"] else contributors
            if episode_id is None:
                continue
            entry = bucket.setdefault(
                episode_id,
                {
                    "episode_id": episode_id,
                    "participant_id": episodes.get(episode_id, {}).get(
                        "participant_id", chain["root_participant"]
                    ),
                    "episode_kind": episodes.get(episode_id, {}).get("kind"),
                    "description": episodes.get(episode_id, {}).get("description", ""),
                    "chains": [],
                    "confidence": 0.0,
                    "independently_observed": False,
                    "evidence_node_ids": episodes.get(episode_id, {}).get("node_ids", []),
                },
            )
            entry["chains"].append(chain["chain_id"])
            entry["confidence"] = round(
                max(entry["confidence"], chain["confidence"]), 6
            )
            if chain["cross_participant"]:
                entry["independently_observed"] = True

        ranked = sorted(
            contributors.values(),
            key=lambda c: (-c["confidence"], c["participant_id"], c["episode_id"]),
        )
        for entry in ranked:
            entry["validation"] = {
                "status": "not_validated",
                "note": (
                    "derived from the fused causal graph; controlled replay has "
                    "not yet been run for this contributor"
                ),
            }
        vehicles = sorted({c["participant_id"] for c in ranked})
        if not ranked:
            attribution_class = "insufficient_evidence"
            rationale = (
                "no causal chain of sufficient confidence reaches this collision "
                "from an observable behaviour"
            )
        elif len(vehicles) == 1 and len(ranked) == 1:
            attribution_class = "single_initiator"
            rationale = (
                "one behaviour sits at the root of every supported causal chain "
                "into this collision"
            )
        else:
            attribution_class = "shared_contribution"
            rationale = (
                "{0} behaviours across {1} vehicle(s) each root a supported causal "
                "chain into this collision".format(len(ranked), len(vehicles))
            )
        results.append(
            {
                "outcome_id": incident["outcome_id"],
                "participants": incident["participants"],
                "t_common": incident["t_common"],
                "order": incident["order"],
                "attribution_class": attribution_class,
                "rationale": rationale,
                "contributors": ranked,
                "preventive_behaviour": sorted(
                    preventive.values(),
                    key=lambda c: (-c["confidence"], c["participant_id"]),
                ),
                "contributing_participants": vehicles,
                "uncertainties": incident.get("uncertainties", []),
            }
        )

    return {
        "schema_version": SCHEMA_VERSIONS.get("counterfactual", "1.0.0"),
        "run_id": reconstruction.get("run_id"),
        "scenario_id": reconstruction.get("scenario_id"),
        "seed": reconstruction.get("seed"),
        "source": "fused_causal_graph",
        "time_domain": "common",
        "collisions": results,
        "disclaimer": (
            "Causal contribution reconstructed from vehicle-local evidence. This "
            "is not a finding of legal fault and not a fault percentage."
        ),
        "note": (
            "A hypothesis derived from the graph alone. Counterfactual replay may "
            "confirm it, weaken it or leave it unresolved; until it runs, every "
            "contributor is marked not_validated."
        ),
    }


def explain_outcome(
    reconstruction: Mapping[str, Any],
    attribution: Optional[Mapping[str, Any]],
    outcome_id: str,
) -> Dict[str, Any]:
    """"Why did this happen?" -- assembled from the records, by template.

    Returns ``{"headline", "chains", "attribution", "uncertainties"}`` where every
    string is generated from the structured reconstruction; no free text and no
    language model.
    """
    incident = next(
        (i for i in reconstruction.get("incidents", []) if i["outcome_id"] == outcome_id),
        None,
    )
    if incident is None:
        raise KeyError("no reconstructed outcome with id {0!r}".format(outcome_id))

    who = " and ".join(incident["participants"]) or "the vehicles involved"
    kind = (
        "collided" if incident["outcome_type"] == EventType.COLLISION.value
        else "passed without contact"
    )
    headline = "{0} {1} at t = {2:.2f} s on the common clock.".format(
        who, kind, incident["t_common"]
    )

    verdict: Dict[str, Any] = {"class": None, "sentences": []}
    if attribution is not None:
        block = next(
            (c for c in attribution.get("collisions", [])
             if c["outcome_id"] == outcome_id),
            None,
        )
        if block is not None:
            verdict["class"] = block["attribution_class"]
            if block["attribution_class"] == "insufficient_evidence":
                verdict["sentences"].append(
                    "The exchanged evidence does not support naming a contributing "
                    "behaviour for this outcome."
                )
            else:
                for entry in block["contributors"]:
                    status = entry.get("validation", {}).get("status", "not_validated")
                    support = {
                        "confirmed": "confirmed by controlled replay",
                        "weakened": "not confirmed by controlled replay",
                        "unresolved": "replay could not settle it",
                    }.get(status, "graph-supported only, not yet replayed")
                    verdict["sentences"].append(
                        "{0} ({1}) -- {2}.".format(
                            entry["description"] or entry["episode_kind"],
                            entry["participant_id"],
                            support,
                        )
                    )
            for entry in block.get("preventive_behaviour", []):
                verdict["sentences"].append(
                    "Preventive behaviour: {0}.".format(
                        entry["description"] or entry["episode_kind"]
                    )
                )

    return {
        "outcome_id": outcome_id,
        "headline": headline,
        "chains": [
            {
                "chain_id": chain["chain_id"],
                "confidence": chain["confidence"],
                "cross_participant": chain["cross_participant"],
                "sentences": chain["narrative"],
            }
            for chain in incident.get("chains", [])
        ],
        "attribution": verdict,
        "uncertainties": incident.get("uncertainties", []),
    }
