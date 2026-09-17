"""Canonical event identity and optimal matching between independent graphs.

Two graphs built by two different participants -- or by a participant and the
oracle -- never share event ids: :func:`cdf.common.schemas.make_event_id` derives
every id from the *producing* layer's own scope, owner and timestamps, which is
exactly what makes the reconstructions independent. Comparing such graphs
therefore needs an identity notion that survives the crossing, and that is what
this module provides.

Two levels are offered, deliberately:

* :func:`canonical_key` -- a cheap, hashable, *bucketed* identity used for set
  algebra (``GraphAnalyzer.compare_to``, ``GraphAnalyzer.knowledge_gain``). It is
  exact, symmetric and order-independent, but two events that straddle a bucket
  boundary count as different even when they are a millisecond apart.
* :func:`match_events` -- a tolerance-correct, globally optimal one-to-one
  assignment (Hungarian algorithm). It costs an assignment solve but has no
  boundary artifact and cannot match one event twice, so every published
  precision/recall number is computed from it rather than from bucket keys.

Subject resolution
------------------
An interaction event's ``subject`` is a *local* track id such as ``"A::T003"``.
It is meaningful only inside the graph that produced it. When the fusion layer
has resolved a track to a participant, callers pass the resulting
``track_id -> participant_id`` mapping and both sides of the comparison then
speak about the same physical vehicle. Without such a mapping the raw track id
is used, which is correct for self-comparison and for comparing two graphs of the
same participant.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..common.schemas import Event, EventType, GraphDocument

__all__ = [
    "DEFAULT_CANONICAL_TIME_BUCKET_S",
    "SELF_SUBJECT",
    "resolve_subject",
    "canonical_key",
    "canonical_key_index",
    "canonical_edge_key",
    "match_events",
    "match_edges",
]


#: Width of the :func:`canonical_key` time bucket, in seconds, used when no
#: explicit width is supplied. ``configs/default.yaml`` has no key for it (see
#: the module notes in the task report), so callers that own a :class:`Config`
#: should pass ``cfg.get("evaluation.event_match.canonical_time_bucket_s", ...)``.
#: The value matches ``fusion.event_alignment.time_tolerance_s`` in spirit: two
#: observations of the same physical event, seen by two independent onboard
#: recorders, are expected to land within a second of one another.
DEFAULT_CANONICAL_TIME_BUCKET_S: float = 1.0

#: Sentinel subject for own-behaviour events (no tracked third party involved).
SELF_SUBJECT: str = "self"

# --- assignment tie-breakers -------------------------------------------------
# These are NOT thresholds: they are numerically negligible preferences that make
# the optimal assignment unique and reproducible when several candidate pairs
# have exactly the same timing error. Without them, comparing a graph with itself
# could legitimately return a permutation of equal-cost node pairs and destroy
# edge identity. Ordered: prefer the same participant, then the same subject,
# then literally the same event id.
_TIE_PARTICIPANT: float = 1.0e-6
_TIE_SUBJECT: float = 1.0e-7
_TIE_IDENTITY: float = 1.0e-9

#: Cost assigned to a forbidden pair. Finite (the solver rejects infinities) but
#: far above any admissible cost, so a forbidden pair is only ever selected when
#: the solver has nothing else to fill a row/column with -- and is then dropped.
_FORBIDDEN_COST: float = 1.0e9


# ---------------------------------------------------------------------------
# Canonical identity
# ---------------------------------------------------------------------------


def _event_type_value(ev: Event) -> str:
    """Event type as a plain string, tolerating already-serialised documents."""
    return ev.event_type.value if isinstance(ev.event_type, EventType) else str(ev.event_type)


def resolve_subject(
    ev: Event, participant_of_subject: Optional[Mapping[str, str]] = None
) -> str:
    """Resolve an event's subject to a cross-graph-stable label.

    Own-behaviour events (``subject`` empty, ``None`` or already ``"self"``)
    resolve to :data:`SELF_SUBJECT`. Interaction events resolve through
    ``participant_of_subject`` when fusion has identified the tracked object;
    otherwise the raw local track id is kept, so that a comparison inside a
    single participant's own graphs still behaves.
    """
    raw = ev.subject
    if raw is None or raw == "" or raw == SELF_SUBJECT:
        return SELF_SUBJECT
    if participant_of_subject:
        mapped = participant_of_subject.get(raw)
        if mapped:
            return str(mapped)
    return str(raw)


def canonical_key(
    ev: Event,
    participant_of_subject: Optional[Mapping[str, str]] = None,
    time_bucket_s: Optional[float] = None,
) -> Tuple[str, str, str, int]:
    """Identity of an event *across* graphs.

    The key is ``(event_type, owner_participant, resolved_subject, time_bucket)``:

    * ``event_type`` -- the typed taxonomy label; two events of different types
      are never the same event.
    * ``owner_participant`` -- ``Event.participant_id``, i.e. *whose* onboard
      reconstruction claims it. Two participants observing the same physical
      interaction produce two distinct local claims on purpose; only the fusion
      layer is allowed to merge them, and a fused node carries the canonical
      owner it was merged under.
    * ``resolved_subject`` -- see :func:`resolve_subject`.
    * ``time_bucket`` -- ``floor(t_peak / bucket + 0.5)``, i.e. the index of the
      nearest bucket centre, with ties broken upwards so the mapping is a total
      function with no floating-point ambiguity.

    Bucketing is what makes the key hashable and therefore usable for set
    algebra. Its cost is a boundary artifact: with a 1.0 s bucket, 0.49 s and
    0.51 s share a bucket while 0.51 s and 1.49 s do not, even though both pairs
    are 0.02 s / 0.98 s apart. Use :func:`match_events` whenever the tolerance
    must be honoured exactly (all evaluation metrics do).
    """
    bucket = float(DEFAULT_CANONICAL_TIME_BUCKET_S if time_bucket_s is None else time_bucket_s)
    if bucket <= 0.0:
        raise ValueError("time_bucket_s must be positive, got {0!r}".format(time_bucket_s))
    index = int(math.floor(float(ev.t_peak) / bucket + 0.5))
    return (
        _event_type_value(ev),
        str(ev.participant_id),
        resolve_subject(ev, participant_of_subject),
        index,
    )


def canonical_key_index(
    events: Sequence[Event],
    participant_of_subject: Optional[Mapping[str, str]] = None,
    time_bucket_s: Optional[float] = None,
) -> Dict[Tuple[str, str, str, int], List[str]]:
    """Map every canonical key to the event ids that carry it.

    A list rather than a single id because bucketing can collide two genuinely
    distinct events (e.g. two ``BRAKE_ONSET`` on the same subject inside one
    bucket); callers that care about the collision can see it instead of having
    it silently overwritten.
    """
    out: Dict[Tuple[str, str, str, int], List[str]] = {}
    for ev in events:
        key = canonical_key(ev, participant_of_subject, time_bucket_s)
        out.setdefault(key, []).append(ev.event_id)
    return out


def canonical_edge_key(
    source: Event,
    target: Event,
    edge_type: str,
    participant_of_subject: Optional[Mapping[str, str]] = None,
    time_bucket_s: Optional[float] = None,
) -> Tuple[Tuple[str, str, str, int], Tuple[str, str, str, int], str]:
    """Cross-graph identity of an edge: ``(key(source), key(target), edge_type)``."""
    return (
        canonical_key(source, participant_of_subject, time_bucket_s),
        canonical_key(target, participant_of_subject, time_bucket_s),
        str(edge_type),
    )


# ---------------------------------------------------------------------------
# Optimal event matching
# ---------------------------------------------------------------------------


def _solver_sort_key(ev: Event, type_value: str, subject: str) -> Tuple[float, str, str, str, str]:
    """Total order used to canonicalise an event list before the assignment solve.

    Event ids are unique within a list (``_assert_unique_ids`` enforces it), so
    this is a strict total order and the permutation it induces depends only on
    the set of events -- never on how the caller happened to list them.
    """
    return (
        float(ev.t_peak),
        str(type_value),
        str(ev.participant_id),
        str(subject),
        str(ev.event_id),
    )


def _assert_unique_ids(events: Sequence[Event], label: str) -> None:
    """Duplicate event ids would corrupt the returned maps; fail loudly."""
    seen = set()
    for ev in events:
        if ev.event_id in seen:
            raise ValueError(
                "duplicate event_id {0!r} in {1}; event ids must be unique within a graph".format(
                    ev.event_id, label
                )
            )
        seen.add(ev.event_id)


def match_events(
    a: Sequence[Event],
    b: Sequence[Event],
    tolerance_s: float,
    require_same_type: bool = True,
    subject_map_a: Optional[Mapping[str, str]] = None,
    subject_map_b: Optional[Mapping[str, str]] = None,
    require_same_subject: bool = False,
    require_same_participant: bool = False,
) -> Dict[str, Any]:
    """Globally optimal one-to-one matching of two event lists.

    Why an assignment solve rather than greedy nearest-neighbour: a greedy pass
    over a dense burst of events (``RANGE_DECREASING`` fires repeatedly while a
    target closes) can consume the partner of a later, better pair and inflate
    the false-negative count. The Hungarian algorithm
    (:func:`scipy.optimize.linear_sum_assignment`) minimises the *total* absolute
    timing error instead, which makes the resulting precision/recall a property
    of the two event sets and not of their listing order.

    Parameters
    ----------
    a, b:
        Event lists to match; ``a`` is conventionally the prediction and ``b``
        the reference.
    tolerance_s:
        Maximum absolute ``t_peak`` difference for an admissible pair.
    require_same_type:
        When true (the default, mirroring
        ``evaluation.event_match.require_same_type``) only identical
        :class:`EventType` values may pair.
    subject_map_a, subject_map_b:
        Optional ``track_id -> participant_id`` resolutions, see
        :func:`resolve_subject`.
    require_same_subject, require_same_participant:
        Extra gates. Off by default because a local prediction and an oracle
        reference generally disagree on labels unless a resolution map is given.

    Returns
    -------
    dict
        ``matches`` (list of ``(a_id, b_id, dt)`` with ``dt = t_peak(a) -
        t_peak(b)``), ``unmatched_a``, ``unmatched_b``, ``mean_abs_dt``, plus
        ``n_matched`` / ``n_a`` / ``n_b`` and the ``map_a_to_b`` /``map_b_to_a``
        correspondences used by :func:`match_edges`.
    """
    tol = float(tolerance_s)
    if tol < 0.0 or tol != tol:
        raise ValueError("tolerance_s must be a non-negative number, got {0!r}".format(tolerance_s))
    _assert_unique_ids(a, "a")
    _assert_unique_ids(b, "b")

    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return _empty_match_result(a, b, tol)

    subjects_a = [resolve_subject(ev, subject_map_a) for ev in a]
    subjects_b = [resolve_subject(ev, subject_map_b) for ev in b]
    types_a = [_event_type_value(ev) for ev in a]
    types_b = [_event_type_value(ev) for ev in b]

    # The assignment is solved on canonically ordered copies of both lists, not
    # on the caller's listing order. The tie-breakers below make the *cost* of an
    # assignment unique in the common cases, but they cannot make the optimal
    # assignment itself unique: two genuinely equidistant candidates (a
    # prediction exactly between two reference events) leave the solver free to
    # pick either, and it picks by row/column index. Solving on a canonical order
    # is what turns "whichever the solver happened to see first" into a function
    # of the two event *sets*, which is the guarantee the docstring above makes
    # and which every published precision/recall/SHD number relies on.
    order_a = sorted(range(na), key=lambda i: _solver_sort_key(a[i], types_a[i], subjects_a[i]))
    order_b = sorted(range(nb), key=lambda j: _solver_sort_key(b[j], types_b[j], subjects_b[j]))

    cost = np.full((na, nb), _FORBIDDEN_COST, dtype=float)
    for r, i in enumerate(order_a):
        ea = a[i]
        for c, j in enumerate(order_b):
            eb = b[j]
            if require_same_type and types_a[i] != types_b[j]:
                continue
            if require_same_subject and subjects_a[i] != subjects_b[j]:
                continue
            if require_same_participant and str(ea.participant_id) != str(eb.participant_id):
                continue
            dt = float(ea.t_peak) - float(eb.t_peak)
            if abs(dt) > tol:
                continue
            penalty = 0.0
            if str(ea.participant_id) != str(eb.participant_id):
                penalty += _TIE_PARTICIPANT
            if subjects_a[i] != subjects_b[j]:
                penalty += _TIE_SUBJECT
            if ea.event_id != eb.event_id:
                penalty += _TIE_IDENTITY
            cost[r, c] = abs(dt) + penalty

    rows, cols = linear_sum_assignment(cost)

    pairs: Dict[int, int] = {}
    for r, c in zip(rows.tolist(), cols.tolist()):
        if cost[r, c] >= _FORBIDDEN_COST:
            continue
        pairs[order_a[r]] = order_b[c]

    matches: List[Tuple[str, str, float]] = []
    map_a_to_b: Dict[str, str] = {}
    map_b_to_a: Dict[str, str] = {}
    for i in sorted(pairs):
        j = pairs[i]
        dt = float(a[i].t_peak) - float(b[j].t_peak)
        matches.append((a[i].event_id, b[j].event_id, dt))
        map_a_to_b[a[i].event_id] = b[j].event_id
        map_b_to_a[b[j].event_id] = a[i].event_id

    unmatched_a = [ev.event_id for ev in a if ev.event_id not in map_a_to_b]
    unmatched_b = [ev.event_id for ev in b if ev.event_id not in map_b_to_a]
    abs_dts = [abs(m[2]) for m in matches]
    return {
        "matches": matches,
        "unmatched_a": unmatched_a,
        "unmatched_b": unmatched_b,
        "mean_abs_dt": float(sum(abs_dts) / len(abs_dts)) if abs_dts else 0.0,
        "n_matched": len(matches),
        "n_a": na,
        "n_b": nb,
        "map_a_to_b": map_a_to_b,
        "map_b_to_a": map_b_to_a,
        "tolerance_s": tol,
    }


def _empty_match_result(
    a: Sequence[Event], b: Sequence[Event], tolerance_s: float
) -> Dict[str, Any]:
    """Result for a degenerate match where one side is empty.

    ``tolerance_s`` is echoed back unchanged so that a caller logging the
    tolerance it evaluated under reads the same number whether or not one of the
    two graphs happened to be empty.
    """
    return {
        "matches": [],
        "unmatched_a": [ev.event_id for ev in a],
        "unmatched_b": [ev.event_id for ev in b],
        "mean_abs_dt": 0.0,
        "n_matched": 0,
        "n_a": len(a),
        "n_b": len(b),
        "map_a_to_b": {},
        "map_b_to_a": {},
        "tolerance_s": float(tolerance_s),
    }


# ---------------------------------------------------------------------------
# Edge matching under a node correspondence
# ---------------------------------------------------------------------------


def _edge_index(doc: GraphDocument, label: str) -> Dict[Tuple[str, str, str], Dict[str, Any]]:
    """Index a document's edges by ``(source, target, edge_type)``.

    :attr:`GraphEdge.key` documents that triple as the edge's identity inside a
    document, so a repeat is a malformed document rather than a parallel edge and
    is reported instead of being silently deduplicated.
    """
    out: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for e in doc.edges:
        key = (e.source, e.target, str(e.edge_type))
        if key in out:
            raise ValueError(
                "duplicate edge {0} in {1}; (source, target, edge_type) must be unique".format(
                    key, label
                )
            )
        out[key] = {
            "source": e.source,
            "target": e.target,
            "edge_type": str(e.edge_type),
            "confidence": float(e.confidence),
            "rule": e.rule,
        }
    return out


def match_edges(
    a_doc: GraphDocument,
    b_doc: GraphDocument,
    node_match: Mapping[str, str],
    restrict_to_matched_nodes: bool = False,
) -> Dict[str, Any]:
    """Classify ``a_doc``'s edges against ``b_doc``'s under a node correspondence.

    ``node_match`` maps a node id of ``a_doc`` to its counterpart in ``b_doc``
    (typically ``match_events(...)["map_a_to_b"]``). Edge identity is the triple
    ``(mapped_source, mapped_target, edge_type)`` expressed in ``b``'s id space.

    Classification
    --------------
    ``matched``
        the same triple exists on both sides;
    ``extra``
        present in ``a`` only (a false positive when ``b`` is the reference);
    ``missing``
        present in ``b`` only;
    ``reversed``
        an ``a`` edge whose *swapped* triple is present in ``b`` while the
        straight one is not. A reversal is reported once, as its own category --
        never as one ``missing`` plus one ``extra`` -- because it is a different
        failure: the pair of events was linked, only the direction of the claim
        is wrong.

    Edges touching a node the matcher could not pair
    -----------------------------------------------
    By default such an edge is still counted: a reference edge onto a node the
    prediction never found is ``missing`` (the reconstruction did miss that
    causal claim), and a predicted edge onto a node the reference does not
    contain is ``extra``. This matters for the central experiment of the project
    -- a vehicle that observed one third of a crash must not be able to report
    perfect edge recall on the third it saw, because that would make fusion look
    worthless.

    Set ``restrict_to_matched_nodes`` (the
    ``evaluation.graph_match.use_matched_nodes_only`` convention) to compare
    structure on the shared skeleton only; those edges then move to
    ``unmappable_a`` / ``unmappable_b`` and leave the counts. Either way
    ``n_touching_unmatched_a`` / ``n_touching_unmatched_b`` report how many edges
    were affected, so the two conventions can be reconciled after the fact.
    """
    a_edges = _edge_index(a_doc, "a_doc")
    b_edges = _edge_index(b_doc, "b_doc")
    b_matched_nodes = set(node_match.values())

    mapped_a: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    unmappable_a: List[Dict[str, Any]] = []
    unmatched_endpoint_a: List[Dict[str, Any]] = []
    for _key, payload in sorted(a_edges.items()):
        ms = node_match.get(payload["source"])
        mt = node_match.get(payload["target"])
        if ms is None or mt is None:
            entry = dict(payload)
            entry["a_source"] = payload["source"]
            entry["a_target"] = payload["target"]
            entry["b_source"] = ms
            entry["b_target"] = mt
            if restrict_to_matched_nodes:
                unmappable_a.append(entry)
            else:
                unmatched_endpoint_a.append(entry)
            continue
        mkey = (ms, mt, payload["edge_type"])
        if mkey in mapped_a:
            raise ValueError(
                "node correspondence collapses two distinct edges of a_doc onto {0}".format(mkey)
            )
        entry = dict(payload)
        entry["a_source"] = payload["source"]
        entry["a_target"] = payload["target"]
        entry["b_source"] = ms
        entry["b_target"] = mt
        mapped_a[mkey] = entry

    considered_b: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    unmappable_b: List[Dict[str, Any]] = []
    n_touching_unmatched_b = 0
    for key, payload in sorted(b_edges.items()):
        touches_unmatched = (
            payload["source"] not in b_matched_nodes or payload["target"] not in b_matched_nodes
        )
        entry = dict(payload)
        entry["b_source"] = payload["source"]
        entry["b_target"] = payload["target"]
        if touches_unmatched:
            n_touching_unmatched_b += 1
            if restrict_to_matched_nodes:
                unmappable_b.append(entry)
                continue
        considered_b[key] = entry

    matched: List[Dict[str, Any]] = []
    a_only: List[Tuple[str, str, str]] = []
    for mkey in sorted(mapped_a):
        if mkey in considered_b:
            entry = dict(mapped_a[mkey])
            entry["b_confidence"] = considered_b[mkey]["confidence"]
            matched.append(entry)
        else:
            a_only.append(mkey)

    b_only = set(considered_b) - set(mapped_a)

    reversed_edges: List[Dict[str, Any]] = []
    extra: List[Dict[str, Any]] = list(unmatched_endpoint_a)
    for mkey in a_only:
        swapped = (mkey[1], mkey[0], mkey[2])
        if swapped in b_only:
            entry = dict(mapped_a[mkey])
            entry["b_source"] = swapped[0]
            entry["b_target"] = swapped[1]
            reversed_edges.append(entry)
            b_only.discard(swapped)
        else:
            extra.append(dict(mapped_a[mkey]))

    missing = [dict(considered_b[k]) for k in sorted(b_only)]

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "reversed": reversed_edges,
        "unmappable_a": unmappable_a,
        "unmappable_b": unmappable_b,
        "n_matched": len(matched),
        "n_missing": len(missing),
        "n_extra": len(extra),
        "n_reversed": len(reversed_edges),
        "n_touching_unmatched_a": len(unmatched_endpoint_a) + len(unmappable_a),
        "n_touching_unmatched_b": n_touching_unmatched_b,
        "n_edges_a": len(a_edges),
        "n_edges_b": len(b_edges),
    }
