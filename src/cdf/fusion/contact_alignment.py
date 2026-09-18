"""Tying independent recorders together by the impact they shared.

The problem
-----------

Every vehicle timestamps with its own clock. Nothing in the recordings says what
any other clock read, so before the logs can be merged something physical has to
link them. V1 used radar: fit the range and range-rate a vehicle measured against
the trajectory another vehicle recorded of itself, and read the offset off the
fit. It worked, and it estimated a drift rate too -- but a drift rate fitted over
a 25 s window from noisy radar is a number with more decimal places than
evidence, and the whole story took a page to explain.

What this module does instead
-----------------------------

If A and B were in the same collision, both felt it. Both recorded *when* they
felt it, on their own clocks. The difference between those two timestamps is the
offset between the clocks::

    offset(B -> A) = t_contact_A - t_contact_B
    t_common = t_local + offset

One equation, one unknown, no fitting. ``scale`` is fixed at exactly 1.0 and the
drift is reported as ``unestimated`` -- not as zero, and not as a fitted ppm
figure. A single impact constrains an offset; it says nothing whatever about
rate, and claiming otherwise would be inventing precision.

Matching the anchors
--------------------

The catch is that the collision sensor does not say *who* it hit -- deliberately,
since knowing that would be privileged. So which of A's impacts corresponds to
which of B's has to be inferred, and in a three-car chain there are two impacts
to get right. Each candidate pairing is scored on three things a recorder can
know about itself:

* **impulse** -- by Newton's third law the two parties to one impact feel equal
  and opposite impulses, so their magnitudes should agree;
* **place** -- each vehicle knows where *it* was, from its own localisation. Two
  vehicles in one collision were within a car length of each other; two vehicles
  in different collisions generally were not;
* **implied offset** -- the offset a pairing implies must be physically plausible
  and, where a pair shares more than one impact, consistent across them.

A pairing is accepted only if it is the best by a clear margin. Two candidates
within that margin means the evidence does not distinguish them, and the honest
answer is ``AMBIGUOUS_CONTACT_MATCH`` rather than a coin flip.

Three cars
----------

Alignment is transitive but not direct: A and C may never touch. A-B from impact
one and B-C from impact two put all three on one axis through B.

This is where position evidence stops being enough on its own. In a chain
collision all three vehicles are within a car length of each other at impact, so
pairing A's impact with C's looks perfectly plausible on position even though A
and C never touched. The timeline is therefore grown from the *best-supported*
links rather than from the best-connected recorder -- a maximum spanning tree on
match score -- and the links the tree did not need are then checked against it.
A link that contradicts the alignment is reported, not averaged in. A participant
no chain reaches stays unaligned and is named.

No collision, no offset
-----------------------

A method anchored on contact cannot align recordings with no contact in them,
and this module does not pretend otherwise: the negative-control runs come back
``UNALIGNED_NO_SHARED_CONTACT`` with every recorder on its own clock. Simulator
time is never substituted. That is a real limitation of the method rather than a
bug in it, and hiding it behind a silent fallback would make every no-collision
result meaningless.
"""

from __future__ import annotations

import itertools
import logging
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.schemas import SCHEMA_VERSIONS, Provenance, TriggerKind

LOGGER = logging.getLogger(__name__)

__all__ = [
    "ALIGNMENT_STATUSES",
    "ContactAnchor",
    "ContactMatch",
    "align_by_contact",
    "converters_from",
]

#: Every verdict this module can return, so a reader of an artifact never meets
#: an undocumented one.
ALIGNMENT_STATUSES: Tuple[str, ...] = (
    "CONTACT_ALIGNED",
    "MULTI_CONTACT_ALIGNED",
    "PARTIALLY_ALIGNED",
    "AMBIGUOUS_CONTACT_MATCH",
    "UNALIGNED_NO_SHARED_CONTACT",
)


class ContactAnchor:
    """One impact as a single recorder felt it.

    Everything here is onboard-derived: the time its own clock read, how hard the
    hit was, and where its own localisation put it. Who it hit is not recorded,
    because onboard it is not known.
    """

    __slots__ = ("participant_id", "index", "t_local", "impulse", "x", "y",
                 "speed", "frame")

    def __init__(
        self,
        participant_id: str,
        index: int,
        t_local: float,
        impulse: float,
        x: Optional[float],
        y: Optional[float],
        speed: Optional[float],
        frame: int = 0,
    ) -> None:
        self.participant_id = str(participant_id)
        self.index = int(index)
        self.t_local = float(t_local)
        self.impulse = float(impulse)
        self.x = None if x is None else float(x)
        self.y = None if y is None else float(y)
        self.speed = None if speed is None else float(speed)
        self.frame = int(frame)

    @property
    def key(self) -> str:
        return "{0}#{1}".format(self.participant_id, self.index)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "index": self.index,
            "t_local": round(self.t_local, 6),
            "impulse": round(self.impulse, 3),
            "x": None if self.x is None else round(self.x, 3),
            "y": None if self.y is None else round(self.y, 3),
            "speed": None if self.speed is None else round(self.speed, 3),
            "frame": self.frame,
        }

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "ContactAnchor({0} t={1:.3f} J={2:.0f})".format(
            self.key, self.t_local, self.impulse
        )


class ContactMatch:
    """A hypothesis that two recorders felt the same impact."""

    __slots__ = ("a", "b", "offset", "score", "detail")

    def __init__(
        self,
        a: ContactAnchor,
        b: ContactAnchor,
        offset: float,
        score: float,
        detail: Dict[str, Any],
    ) -> None:
        self.a = a
        self.b = b
        #: Added to ``b``'s local time to reach ``a``'s local time.
        self.offset = float(offset)
        self.score = float(score)
        self.detail = detail

    def as_dict(self) -> Dict[str, Any]:
        return {
            "participants": [self.a.participant_id, self.b.participant_id],
            "anchors": [self.a.key, self.b.key],
            "t_local": [round(self.a.t_local, 6), round(self.b.t_local, 6)],
            "offset_b_to_a_s": round(self.offset, 6),
            "score": round(self.score, 6),
            **self.detail,
        }

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "ContactMatch({0}<->{1} offset={2:+.3f} score={3:.3f})".format(
            self.a.key, self.b.key, self.offset, self.score
        )


# ---------------------------------------------------------------------------
# Reading the anchors off a recording
# ---------------------------------------------------------------------------


def contact_anchors(ev: ParticipantEvidence) -> List[ContactAnchor]:
    """Every impact this recorder felt, in the order it felt them.

    Zero-impulse triggers are dropped. An impact that transferred no momentum is
    not an anchor for anything: the impulse is half the matching evidence, and a
    zero there would match every other zero equally well.
    """
    out: List[ContactAnchor] = []
    for trigger in sorted(ev.triggers, key=lambda t: float(t.t)):
        kind = getattr(trigger, "kind", None)
        kind_value = kind.value if hasattr(kind, "value") else str(kind)
        if kind_value != TriggerKind.COLLISION.value:
            continue
        if not bool(getattr(trigger, "collision_detected", False)):
            continue
        impulse = float(getattr(trigger, "impulse", 0.0) or 0.0)
        if impulse <= 0.0:
            LOGGER.debug(
                "%s: dropping a zero-impulse contact trigger at t=%.3f",
                ev.participant_id, float(trigger.t),
            )
            continue
        sample = ev.telemetry_at(float(trigger.t), max_gap=0.25)
        out.append(ContactAnchor(
            participant_id=ev.participant_id,
            index=len(out),
            t_local=float(trigger.t),
            impulse=impulse,
            x=None if sample is None else float(sample.x),
            y=None if sample is None else float(sample.y),
            speed=None if sample is None else float(sample.speed),
            frame=int(getattr(trigger, "frame", 0) or 0),
        ))
    return out


# ---------------------------------------------------------------------------
# Scoring a candidate pairing
# ---------------------------------------------------------------------------


def _impulse_agreement(a: ContactAnchor, b: ContactAnchor) -> float:
    """How well two impulse magnitudes agree, in [0, 1].

    Newton's third law makes the two impulses of one impact equal in magnitude,
    but the sensors report them through different vehicle masses and filters, so
    the comparison is a ratio rather than an equality.
    """
    lo, hi = sorted((abs(a.impulse), abs(b.impulse)))
    if hi <= 0.0:
        return 0.0
    return float(lo / hi)


def _separation_m(a: ContactAnchor, b: ContactAnchor) -> Optional[float]:
    """Distance between where the two recorders put themselves at contact."""
    if a.x is None or a.y is None or b.x is None or b.y is None:
        return None
    return float(((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5)


def _place_agreement(separation: Optional[float], tolerance_m: float) -> float:
    """1.0 when the two recorders were on top of each other, falling to 0.

    Two vehicles in one collision are in contact, so their reported centres are
    roughly one vehicle length apart. The score decays linearly to zero at
    ``tolerance_m`` so a pairing of two genuinely different impacts, tens of
    metres apart, scores nothing here.
    """
    if separation is None:
        # No localisation at contact. Neutral rather than zero: the impulse and
        # the offset still carry evidence, and refusing to score would make
        # every pairing impossible instead of merely less certain.
        return 0.5
    if tolerance_m <= 0.0:
        return 0.0
    return float(max(0.0, 1.0 - separation / tolerance_m))


def _candidate_matches(
    anchors_a: Sequence[ContactAnchor],
    anchors_b: Sequence[ContactAnchor],
    cfg: Config,
) -> List[ContactMatch]:
    """Every plausible pairing between two recorders' impacts, scored."""
    tolerance_m = float(cfg.get("fusion.contact_alignment.max_separation_m", 12.0))
    max_offset = float(cfg.get("fusion.contact_alignment.max_offset_s", 30.0))
    min_impulse_ratio = float(
        cfg.get("fusion.contact_alignment.min_impulse_ratio", 0.05)
    )

    out: List[ContactMatch] = []
    for a, b in itertools.product(anchors_a, anchors_b):
        offset = a.t_local - b.t_local
        if abs(offset) > max_offset:
            continue
        impulse = _impulse_agreement(a, b)
        if impulse < min_impulse_ratio:
            continue
        separation = _separation_m(a, b)
        place = _place_agreement(separation, tolerance_m)
        if separation is not None and separation > tolerance_m:
            continue
        # Equal weight: the two kinds of evidence are independent and neither is
        # obviously stronger. Weighting one higher would need a calibration this
        # experiment has not done.
        score = 0.5 * impulse + 0.5 * place
        out.append(ContactMatch(a, b, offset, score, {
            "impulse_agreement": round(impulse, 6),
            "separation_m": None if separation is None else round(separation, 3),
            "place_agreement": round(place, 6),
            "localisation_available": separation is not None,
        }))
    out.sort(key=lambda m: (-m.score, m.a.index, m.b.index))
    return out


def _resolve_pair(
    anchors_a: Sequence[ContactAnchor],
    anchors_b: Sequence[ContactAnchor],
    cfg: Config,
) -> Dict[str, Any]:
    """Decide which of two recorders' impacts are the same impact.

    Greedy on score, refusing anything the evidence does not separate. Each
    anchor may be used once: one impact has one counterpart, and a recorder that
    felt two impacts felt two distinct ones.
    """
    margin = float(cfg.get("fusion.contact_alignment.ambiguity_margin", 0.12))
    candidates = _candidate_matches(anchors_a, anchors_b, cfg)
    if not candidates:
        return {"matches": [], "ambiguous": [], "status": "no_candidate"}

    used_a: set = set()
    used_b: set = set()
    matches: List[ContactMatch] = []
    ambiguous: List[Dict[str, Any]] = []

    for candidate in candidates:
        if candidate.a.key in used_a or candidate.b.key in used_b:
            continue
        # Anything else still available that pairs one of these two anchors and
        # scores about as well means the evidence does not tell them apart.
        rivals = [
            other for other in candidates
            if other is not candidate
            and other.a.key not in used_a and other.b.key not in used_b
            and (other.a.key == candidate.a.key or other.b.key == candidate.b.key)
            and candidate.score - other.score < margin
        ]
        if rivals:
            ambiguous.append({
                "anchors": [candidate.a.key, candidate.b.key],
                "score": round(candidate.score, 6),
                "rival_scores": sorted(round(r.score, 6) for r in rivals),
                "margin_required": margin,
                "reason": (
                    "more than one pairing of these impacts fits the impulse and "
                    "position evidence about equally well, so which impact is "
                    "which cannot be decided from the recordings"
                ),
            })
            used_a.add(candidate.a.key)
            used_b.add(candidate.b.key)
            continue
        matches.append(candidate)
        used_a.add(candidate.a.key)
        used_b.add(candidate.b.key)

    return {
        "matches": matches,
        "ambiguous": ambiguous,
        "status": "matched" if matches else "ambiguous_only",
    }


# ---------------------------------------------------------------------------
# Growing one timeline out of the accepted matches
# ---------------------------------------------------------------------------


def _offset_for_pair(matches: Sequence[ContactMatch]) -> Tuple[float, Dict[str, Any]]:
    """One offset for a pair of recorders, and how consistent the evidence was.

    With two shared impacts the two implied offsets should agree. Their spread is
    the only internal check available on the estimate, so it is reported even
    though it is not used to correct anything -- a 40 ms spread and a 400 ms
    spread mean very different things about the result.
    """
    offsets = sorted(m.offset for m in matches)
    mid = offsets[len(offsets) // 2] if len(offsets) % 2 else (
        0.5 * (offsets[len(offsets) // 2 - 1] + offsets[len(offsets) // 2])
    )
    spread = float(offsets[-1] - offsets[0]) if len(offsets) > 1 else 0.0
    return float(mid), {
        "n_shared_contacts": len(matches),
        "offsets_s": [round(o, 6) for o in offsets],
        "offset_spread_s": round(spread, 6),
        "estimator": "median of the per-contact offsets" if len(matches) > 1
        else "single shared contact",
    }


def _spanning_alignment(
    pair_offsets: Mapping[Tuple[str, str], float],
    pair_scores: Mapping[Tuple[str, str], float],
    participants: Sequence[str],
    max_disagreement_s: float,
    consistency_margin: float,
) -> Dict[str, Any]:
    """Put every reachable recorder on one axis, using the best-supported links.

    In a three-car chain every vehicle is within a car length of every other at
    the moment of impact, so position alone will happily pair A's impact with C's
    even though A and C never touched. Growing the timeline from whichever
    recorder has the most links would then propagate that pairing. So the tree is
    grown from the *strongest evidence* instead: links are taken in descending
    score until every reachable recorder is attached, which is Kruskal's
    algorithm on a maximum spanning tree.

    That leaves the links the tree did not need, and those are the only
    independent check this method has. Each implies an offset; if it disagrees
    with the one the tree derived by more than ``max_disagreement_s``, the
    pairings cannot all be right and the disagreement is reported rather than
    averaged away.

    ``offsets[p]`` is added to ``p``'s local time to reach the reference's local
    time. The reference gets exactly 0.0, stated rather than implied by absence.
    """
    edges = sorted(
        pair_offsets.items(),
        key=lambda item: (-float(pair_scores.get(item[0], 0.0)), item[0]),
    )
    parent: Dict[str, str] = {p: p for p in participants}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree: Dict[str, Dict[str, float]] = {p: {} for p in participants}
    link_score: Dict[Tuple[str, str], float] = {}
    tree_edges: List[Tuple[str, str]] = []
    spare: List[Tuple[str, str]] = []
    for (p, q), offset in edges:
        if p not in parent or q not in parent:
            continue
        root_p, root_q = find(p), find(q)
        if root_p == root_q:
            spare.append((p, q))
            continue
        parent[root_p] = root_q
        # `offset` was measured as t_p - t_q at the shared impact, and
        # offsets[X] is what is *added* to X's local time to reach common time.
        # Take p as the reference for a moment: common time is then p's clock,
        # so offsets[q] must satisfy t_q + offsets[q] = t_p, giving offsets[q] =
        # t_p - t_q = +offset. Hence stepping from p to q adds it and stepping
        # the other way subtracts it. Getting this backwards pushes the two
        # recorders twice as far apart instead of together, which is what the
        # test asserting the one physical impact lands at one common time is for.
        tree[p][q] = offset
        tree[q][p] = -offset
        score = float(pair_scores.get((p, q), 0.0))
        link_score[(p, q)] = score
        link_score[(q, p)] = score
        tree_edges.append((p, q))

    if not tree_edges:
        return {"reference": None, "offsets": {}, "chains": [], "inconsistent": []}

    degree: Dict[str, int] = {p: len(tree[p]) for p in participants}
    linked = [p for p in participants if degree[p] > 0]
    reference = sorted(linked, key=lambda p: (-degree[p], p))[0]

    offsets: Dict[str, float] = {reference: 0.0}
    chains: List[List[str]] = []
    route: Dict[str, List[str]] = {reference: [reference]}
    frontier: List[Tuple[str, List[str]]] = [(reference, [reference])]
    while frontier:
        current, path = frontier.pop(0)
        for neighbour in sorted(tree[current]):
            if neighbour in offsets:
                continue
            offsets[neighbour] = offsets[current] + tree[current][neighbour]
            route[neighbour] = path + [neighbour]
            chains.append(path + [neighbour])
            frontier.append((neighbour, path + [neighbour]))

    def weakest_link_between(p: str, q: str) -> Optional[float]:
        """The least well-evidenced tree link the alignment used to relate p and q.

        A spare link contradicting the tree is only a genuine tie if it is about
        as strong as the links it contradicts. The right comparison is the
        weakest step on the route between its endpoints: that step is the
        alignment own weakest claim about this pair.
        """
        route_p, route_q = route.get(p), route.get(q)
        if route_p is None or route_q is None:
            return None
        shared = 0
        while (shared < min(len(route_p), len(route_q))
               and route_p[shared] == route_q[shared]):
            shared += 1
        walk = list(reversed(route_p[shared - 1:])) + route_q[shared:]
        scores = [
            link_score.get((walk[i], walk[i + 1]))
            for i in range(len(walk) - 1)
        ]
        present = [v for v in scores if v is not None]
        return min(present) if present else None

    inconsistent: List[Dict[str, Any]] = []
    for (p, q) in spare:
        if p not in offsets or q not in offsets:
            continue
        # Both recorders map to one common time at a shared impact, so
        # t_p + offsets[p] = t_q + offsets[q], giving t_p - t_q = offsets[q] -
        # offsets[p]. That is what the alignment says this link should have
        # measured; the link itself measured pair_offsets[(p, q)].
        implied_by_tree = offsets[q] - offsets[p]
        disagreement = abs(pair_offsets[(p, q)] - implied_by_tree)
        if disagreement <= max_disagreement_s:
            continue
        score = float(pair_scores.get((p, q), 0.0))
        weakest = weakest_link_between(p, q)
        # Is this a tie, or simply weaker evidence?
        #
        # In a chain collision every vehicle is beside every other at impact, so
        # a spurious pairing between the two outer cars is almost guaranteed to
        # look plausible on position. What separates it from the real pairings is
        # that its impulses do not match, so it scores distinctly lower. Calling
        # that an unresolvable tie would make every three-car run ambiguous,
        # which is wrong in the other direction. So the weaker hypothesis is
        # rejected in favour of the stronger one -- and recorded either way,
        # because a conflict that leaves no trace cannot be audited.
        decisive = weakest is not None and (weakest - score) >= consistency_margin
        inconsistent.append({
            "participants": [p, q],
            "offset_from_this_pairing_s": round(pair_offsets[(p, q)], 6),
            "offset_implied_by_alignment_s": round(implied_by_tree, 6),
            "disagreement_s": round(disagreement, 6),
            "tolerance_s": max_disagreement_s,
            "score": round(score, 6),
            "weakest_link_used": None if weakest is None else round(weakest, 6),
            "resolution": "rejected_as_weaker" if decisive else "unresolved",
            "reason": (
                "this pairing of impacts and the alignment cannot both be "
                "right. The pairings the alignment used are better evidenced "
                "by a clear margin, so this one is rejected"
                if decisive else
                "this pairing of impacts and the alignment cannot both be "
                "right, and the evidence does not clearly favour either, so "
                "the run is reported as an ambiguous contact match"
            ),
        })

    return {
        "reference": reference,
        "offsets": offsets,
        "chains": chains,
        "inconsistent": inconsistent,
        "n_links_used": len(tree_edges),
        "n_links_spare": len(spare),
    }


def align_by_contact(
    run: RunEvidence,
    cfg: Config,
) -> Dict[str, Any]:
    """Estimate a common timeline from shared physical contact alone.

    Returns the offsets, the anchors and matches they came from, and a status
    from :data:`ALIGNMENT_STATUSES`. ``converters`` holds a callable per aligned
    participant, for :func:`cdf.common.event_log.build_global_log`.
    """
    participants = list(run.participant_ids)
    anchors: Dict[str, List[ContactAnchor]] = {
        pid: contact_anchors(run.get(pid)) for pid in participants
    }
    n_anchors = sum(len(v) for v in anchors.values())

    if n_anchors == 0:
        return _unaligned(
            participants, anchors,
            reason=(
                "no recorder felt a contact, so nothing physical links the "
                "clocks. This method cannot align a no-collision run and does "
                "not substitute simulator time"
            ),
        )

    pair_offsets: Dict[Tuple[str, str], float] = {}
    pair_scores: Dict[Tuple[str, str], float] = {}
    pair_detail: Dict[str, Any] = {}
    all_matches: List[ContactMatch] = []
    ambiguous: List[Dict[str, Any]] = []

    for p, q in itertools.combinations(participants, 2):
        if not anchors[p] or not anchors[q]:
            continue
        resolved = _resolve_pair(anchors[p], anchors[q], cfg)
        ambiguous.extend(
            dict(entry, participants=[p, q]) for entry in resolved["ambiguous"]
        )
        matches: List[ContactMatch] = list(resolved["matches"])
        if not matches:
            continue
        offset, detail = _offset_for_pair(matches)
        pair_offsets[(p, q)] = offset
        # The strength of this link, for choosing which links the timeline is
        # built from. Best rather than mean: one well-evidenced shared impact is
        # a firmer tie than two mediocre ones.
        pair_scores[(p, q)] = max(m.score for m in matches)
        pair_detail["{0}->{1}".format(q, p)] = dict(
            detail,
            offset_s=round(offset, 6),
            link_score=round(pair_scores[(p, q)], 6),
            matches=[m.as_dict() for m in matches],
        )
        all_matches.extend(matches)

    if not pair_offsets:
        if ambiguous:
            return _unaligned(
                participants, anchors,
                status="AMBIGUOUS_CONTACT_MATCH",
                reason=(
                    "contacts were felt, but which impact corresponds to which "
                    "could not be decided from impulse and position alone"
                ),
                ambiguous=ambiguous,
            )
        return _unaligned(
            participants, anchors,
            reason=(
                "each recorder felt a contact, but no two of them can be shown "
                "to be the same contact, so no pair of clocks is linked"
            ),
        )

    spanning = _spanning_alignment(
        pair_offsets, pair_scores, participants,
        float(cfg.get("fusion.contact_alignment.max_offset_disagreement_s", 0.15)),
        # A separate knob from the within-pair ambiguity margin above. That one
        # asks whether two candidate pairings of the same anchors are too close
        # to call; this one asks whether a link contradicting the alignment is
        # clearly the weaker hypothesis. Different questions, so one value
        # should not have to serve both.
        float(cfg.get("fusion.contact_alignment.consistency_margin", 0.12)),
    )
    reference = spanning["reference"]
    offsets = spanning["offsets"]
    chains = spanning["chains"]
    aligned = sorted(offsets)
    unaligned = sorted(p for p in participants if p not in offsets)

    if unaligned:
        status = "PARTIALLY_ALIGNED"
    elif any(entry["resolution"] == "unresolved"
             for entry in spanning.get("inconsistent") or []):
        # Every recorder is on the axis, but a pairing contradicts it and the
        # evidence does not say which to believe. Reporting that as a clean
        # alignment would hide the contradiction.
        status = "AMBIGUOUS_CONTACT_MATCH"
    elif len(all_matches) > 1:
        status = "MULTI_CONTACT_ALIGNED"
    else:
        status = "CONTACT_ALIGNED"

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "method": "shared_physical_contact",
        "provenance": Provenance.FUSED.value,
        "status": status,
        "reference": reference,
        "offsets_s": {p: round(v, 6) for p, v in sorted(offsets.items())},
        "scale": 1.0,
        "drift": {
            "estimated": False,
            "assumption": "negligible over the recorded window",
            "why_not": (
                "a single impact constrains one offset and carries no "
                "information about rate. Fitting a drift to it would report "
                "more precision than the evidence supports"
            ),
        },
        "converters": converters_from(offsets),
        "aligned_participants": aligned,
        "unaligned_participants": unaligned,
        "transitive_chains": [c for c in chains if len(c) > 1],
        "n_contact_anchors": n_anchors,
        "n_shared_contacts": len(all_matches),
        "n_links_used": spanning.get("n_links_used", 0),
        "n_links_spare": spanning.get("n_links_spare", 0),
        "anchors": {p: [a.as_dict() for a in v] for p, v in sorted(anchors.items())},
        "pairs": pair_detail,
        "ambiguous_pairings": ambiguous,
        "inconsistent_pairings": spanning.get("inconsistent") or [],
        "n_pairings_rejected_as_weaker": sum(
            1 for e in (spanning.get("inconsistent") or [])
            if e["resolution"] == "rejected_as_weaker"
        ),
        "note": (
            "t_common = t_local + offset, with scale fixed at 1.0. Offsets come "
            "from the timestamps two recorders put on the same physical impact; "
            "no privileged collision-pair identity is used"
        ),
    }


def _unaligned(
    participants: Sequence[str],
    anchors: Mapping[str, Sequence[ContactAnchor]],
    reason: str,
    status: str = "UNALIGNED_NO_SHARED_CONTACT",
    ambiguous: Optional[Sequence[Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    """A refusal, with the reason in the artifact rather than in a log line."""
    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "method": "shared_physical_contact",
        "provenance": Provenance.FUSED.value,
        "status": status,
        "reference": None,
        "offsets_s": {},
        "scale": 1.0,
        "drift": {"estimated": False, "assumption": "not applicable"},
        "converters": {},
        "aligned_participants": [],
        "unaligned_participants": sorted(participants),
        "transitive_chains": [],
        "n_contact_anchors": sum(len(v) for v in anchors.values()),
        "n_shared_contacts": 0,
        "anchors": {p: [a.as_dict() for a in v] for p, v in sorted(anchors.items())},
        "pairs": {},
        "ambiguous_pairings": list(ambiguous or []),
        "inconsistent_pairings": [],
        "n_pairings_rejected_as_weaker": 0,
        "n_links_used": 0,
        "n_links_spare": 0,
        "reason": reason,
        "note": (
            "every recorder keeps its own clock. Simulator time is deliberately "
            "not used as a fallback: it would make the merged timeline look "
            "correct while resting on knowledge no vehicle has"
        ),
    }


def converters_from(
    offsets: Mapping[str, float],
) -> Dict[str, Callable[[float], float]]:
    """Local-to-common converters for the aligned participants.

    ``scale`` is 1.0 throughout, so each is a pure translation. Bound through a
    default argument rather than a closure over the loop variable, which would
    give every participant the last offset.
    """
    return {
        str(pid): (lambda t, _o=float(offset): float(t) + _o)
        for pid, offset in offsets.items()
    }
