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
    "CONTACT_DERIVED_STATUSES",
    "ContactAnchor",
    "ContactMatch",
    "align_by_contact",
    "align_by_acquisition_start",
    "converters_from",
    "converters_of",
    "offsets_block",
]

#: Every verdict this module can return, so a reader of an artifact never meets
#: an undocumented one.
ALIGNMENT_STATUSES: Tuple[str, ...] = (
    "CONTACT_ALIGNED",
    "MULTI_CONTACT_ALIGNED",
    "PARTIALLY_ALIGNED",
    "AMBIGUOUS_CONTACT_MATCH",
    "UNALIGNED_NO_SHARED_CONTACT",
    "ACQUISITION_START_ALIGNED",
)

#: Statuses in which a common timeline exists and was derived from the vehicles
#: own recordings. Results from these runs are the ones that say anything about
#: what the method can do; the acquisition-start runs are reported apart.
CONTACT_DERIVED_STATUSES: Tuple[str, ...] = (
    "CONTACT_ALIGNED", "MULTI_CONTACT_ALIGNED", "PARTIALLY_ALIGNED",
)


class ContactAnchor:
    """One impact as a single recorder felt it.

    Everything here is onboard-derived: the time its own clock read, how hard the
    hit was, and where its own localisation put it. Who it hit is not recorded,
    because onboard it is not known.
    """

    __slots__ = ("participant_id", "index", "t_local", "impulse", "x", "y",
                 "speed", "frame", "n_triggers")

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
        n_triggers: int = 1,
    ) -> None:
        self.participant_id = str(participant_id)
        self.index = int(index)
        self.t_local = float(t_local)
        self.impulse = float(impulse)
        self.x = None if x is None else float(x)
        self.y = None if y is None else float(y)
        self.speed = None if speed is None else float(speed)
        self.frame = int(frame)
        #: How many raw sensor triggers this one impact was reported by.
        self.n_triggers = int(n_triggers)

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
            "n_sensor_triggers_merged": self.n_triggers,
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


def contact_anchors(
    ev: ParticipantEvidence,
    merge_window_s: float = 0.3,
    min_impulse_fraction: float = 0.05,
    min_impulse_ns: float = 300.0,
) -> List[ContactAnchor]:
    """Every impact this recorder felt, in the order it felt them.

    Two filters, and the second matters more than it looks.

    Zero-impulse triggers are dropped: an impact that transferred no momentum is
    not an anchor for anything, since the impulse is half the matching evidence
    and a zero there would match every other zero equally well.

    And a burst of triggers is one impact. The collision sensor fires on every
    tick the vehicles remain in contact, so a half-second of contact arrives as a
    dozen records -- on a recorded three-car chain, 44 of them for one vehicle
    that was hit twice. Left uncollapsed they are not merely wasteful: each is a
    candidate for matching, they all have nearly the same impulse and position,
    and so they manufacture exactly the pattern the ambiguity check is built to
    reject. Collapsing them first means the ambiguity check fires on impacts that
    are genuinely indistinguishable rather than on the same impact counted twelve
    times.

    The merged anchor takes the *first* timestamp, which is the moment of impact,
    and the *largest* impulse, which is the most characteristic thing about it.
    The window is short enough that two impacts in a chain, typically a second or
    more apart, stay separate.

    Resting contact is the harder case, and it is the one that shows up only on
    real recordings. After a pile-up the vehicles stay touching, and the sensor
    goes on reporting a small contact roughly twice a second for the rest of the
    run -- on one recorded chain, 43 such reports after the single real impact,
    at impulses of 30 to 290 N*s against the impact's 11 569. They are too far
    apart in time for the burst merge to reach and they look, to the matcher,
    exactly like impacts: similar impulse to each other, similar position.

    Left in, they do active harm rather than merely wasting work. Two recorders
    both rubbing produce a high-scoring pairing at an arbitrary time, and an
    offset estimated from it is wrong by however long the rubbing went on. So an
    anchor must carry a real share of the momentum transfer this recorder felt:
    at least ``min_impulse_fraction`` of its own largest impulse, and at least
    ``min_impulse_ns`` outright. The relative test is what separates an impact
    from a nudge without needing to know the scale of the scenario; the absolute
    floor catches a run in which nothing was ever a real impact.
    """
    hits: List[Any] = []
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
        hits.append(trigger)

    peak = max(
        (float(getattr(t, "impulse", 0.0) or 0.0) for t in hits), default=0.0
    )
    floor = max(float(min_impulse_ns), peak * float(min_impulse_fraction))
    impacts = [
        t for t in hits
        if float(getattr(t, "impulse", 0.0) or 0.0) >= floor
    ]
    if len(impacts) != len(hits):
        LOGGER.debug(
            "%s: %d of %d contact trigger(s) below the impact floor of %.0f N*s "
            "(peak %.0f); treated as resting contact, not impacts",
            ev.participant_id, len(hits) - len(impacts), len(hits), floor, peak,
        )
    hits = impacts

    bursts: List[List[Any]] = []
    for trigger in hits:
        if bursts and float(trigger.t) - float(bursts[-1][-1].t) <= merge_window_s:
            bursts[-1].append(trigger)
            continue
        bursts.append([trigger])

    out: List[ContactAnchor] = []
    for burst in bursts:
        first = burst[0]
        strongest = max(burst, key=lambda t: float(getattr(t, "impulse", 0.0) or 0.0))
        sample = ev.telemetry_at(float(first.t), max_gap=0.25)
        out.append(ContactAnchor(
            participant_id=ev.participant_id,
            index=len(out),
            t_local=float(first.t),
            impulse=float(getattr(strongest, "impulse", 0.0) or 0.0),
            x=None if sample is None else float(sample.x),
            y=None if sample is None else float(sample.y),
            speed=None if sample is None else float(sample.speed),
            frame=int(getattr(first, "frame", 0) or 0),
            n_triggers=len(burst),
        ))
    if len(hits) != len(out):
        LOGGER.debug(
            "%s: %d contact trigger(s) collapsed into %d impact(s)",
            ev.participant_id, len(hits), len(out),
        )
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


def _assignments(
    candidates: Sequence[ContactMatch],
    max_anchors: int = 6,
) -> List[List[ContactMatch]]:
    """Every way of pairing impacts one-to-one, including partial pairings.

    Greedy matching is not good enough here, and the reason is instructive. Two
    recorders that each felt two similar impacts have four candidate pairings and
    the impulses cannot separate them -- but the *times* can, because only one of
    the two possible pairings implies a consistent clock offset for both. That
    information is in the assignment as a whole and invisible to any rule that
    commits to the best single pairing first.

    The search is exhaustive because it can afford to be: after the impulse
    filter a recorder has a handful of impacts, not dozens, and ``max_anchors``
    keeps a pathological run from turning this into a combinatorial problem.
    """
    by_a: Dict[str, List[ContactMatch]] = {}
    for candidate in candidates:
        by_a.setdefault(candidate.a.key, []).append(candidate)
    a_keys = sorted(by_a)[:max_anchors]

    out: List[List[ContactMatch]] = []

    def walk(index: int, used_b: set, chosen: List[ContactMatch]) -> None:
        if index == len(a_keys):
            if chosen:
                out.append(list(chosen))
            return
        # This anchor may be left unpaired: a recorder can feel an impact whose
        # counterparty is a wall, or a vehicle that is not in the run.
        walk(index + 1, used_b, chosen)
        for candidate in by_a[a_keys[index]]:
            if candidate.b.key in used_b:
                continue
            chosen.append(candidate)
            walk(index + 1, used_b | {candidate.b.key}, chosen)
            chosen.pop()

    walk(0, set(), [])
    return out


def _assignment_score(
    assignment: Sequence[ContactMatch],
    max_disagreement_s: float,
) -> Tuple[float, float]:
    """How good an assignment is, and the spread of the offsets it implies.

    Three things make an assignment good, in order of importance. The pairings
    should be individually well evidenced. The offsets they imply should agree --
    and that is the term that does the real work, because it is the only thing
    that can separate two similar impacts from each other. And, mildly, an
    assignment that explains more of the impacts is preferred to one that leaves
    them unpaired, so redundant evidence is used rather than discarded.

    Agreement within tolerance carries no penalty at all: two offsets 20 ms apart
    are the same offset measured twice, and docking them for it would make one
    pairing always beat two.
    """
    offsets = sorted(m.offset for m in assignment)
    spread = float(offsets[-1] - offsets[0]) if len(offsets) > 1 else 0.0
    mean_score = sum(m.score for m in assignment) / float(len(assignment))
    coherence = (
        1.0 if spread <= max_disagreement_s
        else float(max_disagreement_s) / float(spread)
    )
    size_bonus = 1.0 + 0.05 * (len(assignment) - 1)
    return float(mean_score * coherence * size_bonus), spread


def _is_maximal(
    assignment: Sequence[ContactMatch],
    candidates: Sequence[ContactMatch],
) -> bool:
    """Whether no further candidate pairing could be added without a clash.

    A non-maximal assignment is not a competing account of the impacts; it is the
    same account with a pairing left out. Only maximal ones are compared.
    """
    used_a = {m.a.key for m in assignment}
    used_b = {m.b.key for m in assignment}
    for candidate in candidates:
        if candidate.a.key not in used_a and candidate.b.key not in used_b:
            return False
    return True


def _conflicts(a: Sequence[ContactMatch], b: Sequence[ContactMatch]) -> bool:
    """Whether two assignments disagree about some impact's counterpart.

    Only conflicting assignments are rivals. Two assignments that pair different
    impacts entirely are not competing explanations of the same thing -- one is
    simply more complete -- and treating them as rivals made every run with two
    impacts look ambiguous.
    """
    left = {m.a.key: m.b.key for m in a}
    right = {m.a.key: m.b.key for m in b}
    for key in set(left) & set(right):
        if left[key] != right[key]:
            return True
    left_b = {m.b.key: m.a.key for m in a}
    right_b = {m.b.key: m.a.key for m in b}
    for key in set(left_b) & set(right_b):
        if left_b[key] != right_b[key]:
            return True
    return False


def _resolve_pair(
    anchors_a: Sequence[ContactAnchor],
    anchors_b: Sequence[ContactAnchor],
    cfg: Config,
) -> Dict[str, Any]:
    """Decide which of two recorders impacts are the same impact.

    Chooses the best-scoring assignment, then checks whether any *conflicting*
    assignment scores about as well. If one does, the evidence does not say which
    impact is which, and the honest answer is a refusal rather than a coin flip.
    """
    margin = float(cfg.get("fusion.contact_alignment.ambiguity_margin", 0.12))
    tolerance = float(
        cfg.get("fusion.contact_alignment.max_offset_disagreement_s", 0.15)
    )
    candidates = _candidate_matches(anchors_a, anchors_b, cfg)
    if not candidates:
        return {"matches": [], "ambiguous": [], "status": "no_candidate"}

    # Only maximal assignments compete. Comparing a two-pairing assignment with a
    # one-pairing subset of it on mean score is unfair to the larger: the subset
    # keeps only its best match while the larger one averages in its second. That
    # made every run with two impacts look ambiguous, because dropping the weaker
    # pairing always scored better than keeping it.
    maximal = [a for a in _assignments(candidates) if _is_maximal(a, candidates)]
    scored = [
        (score, spread, assignment)
        for assignment in maximal
        for score, spread in [_assignment_score(assignment, tolerance)]
    ]
    scored.sort(key=lambda item: (
        -item[0], [m.a.index for m in item[2]], [m.b.index for m in item[2]]
    ))
    best_score, _best_spread, best = scored[0]

    rivals = [
        (score, assignment) for score, _spread, assignment in scored[1:]
        if _conflicts(best, assignment) and best_score - score < margin
    ]
    if rivals:
        return {
            "matches": [],
            "ambiguous": [{
                "anchors": [m.a.key + "<->" + m.b.key for m in best],
                "score": round(best_score, 6),
                "rival_scores": sorted(round(s, 6) for s, _ in rivals)[:4],
                "margin_required": margin,
                "reason": (
                    "more than one pairing of these impacts fits the impulse, "
                    "position and timing evidence about equally well, so which "
                    "impact is which cannot be decided from the recordings"
                ),
            }],
            "status": "ambiguous_only",
        }

    return {"matches": list(best), "ambiguous": [], "status": "matched"}


# ---------------------------------------------------------------------------
# Growing one timeline out of the accepted matches
# ---------------------------------------------------------------------------


def _offset_for_pair(
    matches: Sequence[ContactMatch],
    max_disagreement_s: float = 0.15,
) -> Tuple[float, Dict[str, Any]]:
    """One offset for a pair of recorders, and how consistent the evidence was.

    With two genuinely shared impacts the two implied offsets should agree, and
    averaging them is worth a little noise reduction. When they *disagree*,
    averaging is the wrong move and not a conservative one: on a recorded chain a
    real impact implied +0.267 s and a spurious pairing implied -0.083 s, and
    their median was +0.092 -- a number neither piece of evidence supported, and
    wrong by more than a tenth of a second.

    So agreement decides the estimator. Within tolerance, the median. Beyond it,
    the single best-evidenced pairing, with the disagreement recorded: one of
    those pairings is wrong and the right response is to believe the better one,
    not to split the difference between them.
    """
    ordered = sorted(matches, key=lambda m: (-m.score, m.a.index, m.b.index))
    offsets = sorted(m.offset for m in matches)
    spread = float(offsets[-1] - offsets[0]) if len(offsets) > 1 else 0.0

    if len(offsets) == 1:
        estimate, estimator = offsets[0], "single shared contact"
    elif spread <= max_disagreement_s:
        estimate = (
            offsets[len(offsets) // 2] if len(offsets) % 2 else
            0.5 * (offsets[len(offsets) // 2 - 1] + offsets[len(offsets) // 2])
        )
        estimator = "median of the per-contact offsets, which agree"
    else:
        estimate = ordered[0].offset
        estimator = (
            "the best-evidenced pairing alone; the pairings disagree by "
            "{0:.3f} s, so one of them is wrong and averaging would produce a "
            "number neither supports".format(spread)
        )

    return float(estimate), {
        "n_shared_contacts": len(matches),
        "offsets_s": [round(o, 6) for o in offsets],
        "offset_spread_s": round(spread, 6),
        "offsets_agree": spread <= max_disagreement_s,
        "max_disagreement_s": max_disagreement_s,
        "estimator": estimator,
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
        "tree_edges": tree_edges,
        "n_links_used": len(tree_edges),
        "n_links_spare": len(spare),
    }


def _shared_anchor_caveats(
    pair_matches: Mapping[Tuple[str, str], Sequence[ContactMatch]],
    tree_edges: Sequence[Tuple[str, str]],
    anchors: Mapping[str, Sequence[ContactAnchor]],
) -> List[Dict[str, Any]]:
    """Note where one recorder impact was matched to two different recorders.

    Sometimes that is simply true: three vehicles can meet in one impact. But in
    a chain it means something else, and the chain is the common case. A recorded
    three-car pile-up has B struck by C and then striking A, roughly a quarter of
    a second apart -- and B's collision sensor reported *one* impact, not two. So
    B's single anchor gets matched to A on impulse (an exact match) and, through
    the spanning tree, also relates C.

    The method cannot tell those two situations apart from the recordings, and
    should not pretend to. What it can do is say which anchor is doing double
    duty, which pairing through it the impulse evidence favours, and which
    recorders therefore have a suspect offset.

    What it must not do is put a number on the error, and an earlier version did.
    It took the two counterparties' local timestamps and subtracted them -- two
    readings from two different clocks, which is the very error this module
    exists to correct, committed inside the code that corrects it. On a recorded
    chain that produced a bound of 13 ms for an offset that was out by 200 ms,
    and the reassuring small number was worse than no number at all.

    The honest position: if B never registered its second impact, B has no
    measurement of when that impact happened, so nothing in the recordings bounds
    how far the derived offset is out. The interval between the two impacts is
    exactly the error, and it is unobserved.
    """
    used: Dict[str, List[Tuple[str, str]]] = {}
    pairings: Dict[str, List[Dict[str, Any]]] = {}
    for edge in tree_edges:
        for match in pair_matches.get(edge, []):
            agreement = _impulse_agreement(match.a, match.b)
            for anchor, other in ((match.a, match.b), (match.b, match.a)):
                used.setdefault(anchor.key, []).append(edge)
                pairings.setdefault(anchor.key, []).append({
                    "with": other.key,
                    "participant": other.participant_id,
                    "impulse_agreement": round(agreement, 6),
                    "link": list(edge),
                })

    out: List[Dict[str, Any]] = []
    for key, edges in sorted(used.items()):
        distinct = sorted({e for e in edges})
        if len(distinct) < 2:
            continue
        participant = key.split("#")[0]
        ranked = sorted(
            pairings[key], key=lambda p: (-p["impulse_agreement"], p["with"])
        )
        best, rest = ranked[0], ranked[1:]
        affected = sorted({p["participant"] for p in rest})
        out.append({
            "anchor": key,
            "participant": participant,
            "links_using_it": [list(e) for e in distinct],
            "n_impacts_this_recorder_registered": len(anchors.get(participant, [])),
            "best_supported_pairing": best,
            "weaker_pairings": rest,
            "participants_with_suspect_offset": affected,
            # There is no number to put here, and putting one was worse than
            # leaving it empty. See the reason below.
            "offset_error_bound_s": None,
            "error_bound_determinable": False,
            "reason": (
                "this recorder registered one impact and it was matched to more "
                "than one counterparty. Either the impact genuinely involved all "
                "of them at once, or this recorder did not register its second "
                "impact -- which is what happens in a chain, where the two "
                "contacts are a fraction of a second apart. Impulse agreement "
                "favours the pairing with {0} ({1:.3f}); the offset for {2} is "
                "derived through the same anchor and, if the two impacts were in "
                "fact distinct, is out by the interval between them. Nothing in "
                "the recordings bounds that interval, so no error bound is "
                "given: a recorder that never registered the second impact has "
                "no measurement of when it happened".format(
                    best["participant"], best["impulse_agreement"],
                    ", ".join(affected) or "the other recorder(s)",
                )
            ),
        })
    return out


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
        pid: contact_anchors(
            run.get(pid),
            merge_window_s=float(
                cfg.get("fusion.contact_alignment.trigger_merge_window_s", 0.3)
            ),
            min_impulse_fraction=float(
                cfg.get("fusion.contact_alignment.min_impulse_fraction_of_peak",
                        0.05)
            ),
            min_impulse_ns=float(
                cfg.get("fusion.contact_alignment.min_impulse_ns", 300.0)
            ),
        )
        for pid in participants
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
    pair_matches: Dict[Tuple[str, str], List[ContactMatch]] = {}
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
        offset, detail = _offset_for_pair(
            matches,
            max_disagreement_s=float(
                cfg.get("fusion.contact_alignment.max_offset_disagreement_s", 0.15)
            ),
        )
        pair_offsets[(p, q)] = offset
        # The strength of this link, for choosing which links the timeline is
        # built from. Best rather than mean: one well-evidenced shared impact is
        # a firmer tie than two mediocre ones.
        pair_scores[(p, q)] = max(m.score for m in matches)
        pair_matches[(p, q)] = list(matches)
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
    shared_anchors = _shared_anchor_caveats(
        pair_matches, spanning.get("tree_edges") or [], anchors
    )
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
        "offsets": offsets_block(
            offsets, participants,
            # One well-evidenced shared impact is a firm tie; a pair that
            # disagreed across two impacts is less so. Reported rather than used
            # to weight anything, since there is nothing here to weight.
            confidence=max(
                0.0, min(1.0, max((m.score for m in all_matches), default=0.0))
            ),
        ),
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
        "shared_anchor_caveats": shared_anchors,
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
        "offsets": offsets_block({}, participants),
        "scale": 1.0,
        "drift": {"estimated": False, "assumption": "not applicable"},
        "aligned_participants": [],
        "unaligned_participants": sorted(participants),
        "transitive_chains": [],
        "n_contact_anchors": sum(len(v) for v in anchors.values()),
        "n_shared_contacts": 0,
        "anchors": {p: [a.as_dict() for a in v] for p, v in sorted(anchors.items())},
        "pairs": {},
        "ambiguous_pairings": list(ambiguous or []),
        "inconsistent_pairings": [],
        "shared_anchor_caveats": [],
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


def converters_of(
    alignment: Optional[Mapping[str, Any]],
) -> Dict[str, Callable[[float], float]]:
    """The transforms an alignment result implies, derived from what it publishes.

    Deliberately not stored in the result. An alignment is an artifact before it
    is anything else -- it gets written to ``clock_alignment.json`` -- so keeping
    callables out of it means the file always serialises, and it also guarantees
    that whatever a consumer applies is exactly what the file states rather than
    something computed alongside it.
    """
    if not alignment:
        return {}
    return converters_from(alignment.get("offsets_s") or {})


def offsets_block(
    offsets: Mapping[str, float],
    participants: Sequence[str],
    confidence: float = 1.0,
) -> Dict[str, Dict[str, Any]]:
    """The per-participant transform in the form the fusion machinery consumes.

    ``scale`` is 1.0 throughout, which is the whole claim of a contact anchor: it
    fixes an offset and says nothing about rate. Participants with no offset get
    a status other than ``ALIGNED`` so that
    :class:`~cdf.fusion.aligned_evidence.AlignedRunEvidence` leaves their streams
    on their own clock rather than transforming them with a number nobody
    estimated.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for pid in sorted(participants):
        if pid in offsets:
            out[str(pid)] = {
                "status": "ALIGNED",
                "scale": 1.0,
                "offset_s": round(float(offsets[pid]), 6),
                "confidence": round(float(confidence), 6),
                "drift_ppm": None,
                "note": "scale fixed at 1.0; drift not estimated",
            }
        else:
            out[str(pid)] = {
                "status": "UNRESOLVED",
                "scale": 1.0,
                "offset_s": None,
                "confidence": 0.0,
                "drift_ppm": None,
                "note": (
                    "no shared contact ties this recorder to the others, so no "
                    "offset was estimated and none is assumed"
                ),
            }
    return out


def align_by_acquisition_start(
    run: RunEvidence,
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Align on the moment the experiment started the recorders, not on physics.

    A contact-anchored method cannot align a run with no contact in it. The
    negative controls are exactly those runs, and they are also the runs where a
    silent fallback would do most damage: every one of them would appear
    perfectly aligned while resting on knowledge no vehicle has.

    So this is the alternative the brief permits, and it is deliberately not the
    same kind of thing. The experiment infrastructure starts every recorder in
    one simulator tick, and that fact -- a property of the harness, declared
    here, not inferred from any recording -- makes the first sample of each log
    a common instant. It is a clapperboard, and it is honest as long as nobody
    mistakes it for a result.

    Two things keep that distinction from eroding. The status is its own value,
    ``ACQUISITION_START_ALIGNED``, never one of the contact ones. And the
    artifact carries the caveat, so a reader of a merged log from one of these
    runs can see that its common time came from the harness and not from the
    vehicles.

    This is *not* simulator time. Simulator time would give every recorder the
    engine clock, erasing the offsets and the jitter the experiment exists to
    work against. Here each recorder keeps its own clock and its own jitter; only
    the single constant relating the two is taken from the harness.
    """
    cfg = cfg if cfg is not None else Config({})
    participants = list(run.participant_ids)
    starts: Dict[str, float] = {}
    for pid in participants:
        span = run.get(pid).span()
        if span is not None:
            starts[pid] = float(span[0])

    if len(starts) < 2:
        return _unaligned(
            participants, {p: [] for p in participants},
            reason=(
                "fewer than two recorders produced telemetry, so there is "
                "nothing to relate"
            ),
        )

    reference = sorted(starts)[0]
    offsets = {pid: starts[reference] - t for pid, t in sorted(starts.items())}
    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "method": "acquisition_start_marker",
        "provenance": Provenance.FUSED.value,
        "status": "ACQUISITION_START_ALIGNED",
        "reference": reference,
        "offsets_s": {p: round(v, 6) for p, v in offsets.items()},
        "offsets": offsets_block(offsets, participants, confidence=0.5),
        "scale": 1.0,
        "drift": {
            "estimated": False,
            "assumption": "negligible over the recorded window",
            "why_not": "the marker fixes one instant and says nothing about rate",
        },
        "aligned_participants": sorted(offsets),
        "unaligned_participants": sorted(set(participants) - set(offsets)),
        "transitive_chains": [],
        "n_contact_anchors": 0,
        "n_shared_contacts": 0,
        "anchors": {},
        "pairs": {},
        "ambiguous_pairings": [],
        "inconsistent_pairings": [],
        "shared_anchor_caveats": [],
        "n_pairings_rejected_as_weaker": 0,
        "n_links_used": 0,
        "n_links_spare": 0,
        "acquisition_start_local_s": {
            p: round(t, 6) for p, t in sorted(starts.items())
        },
        "caveat": (
            "common time here comes from the experiment harness, which starts "
            "every recorder in one simulator tick, and not from anything the "
            "vehicles observed. It is a declared synchronisation signal rather "
            "than a reconstruction result, and runs aligned this way must be "
            "reported apart from contact-aligned ones"
        ),
        "note": (
            "not simulator time: each recorder keeps its own clock and its own "
            "jitter, and only the single constant relating them is taken from "
            "the harness"
        ),
    }
