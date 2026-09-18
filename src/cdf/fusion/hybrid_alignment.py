"""Contact first, radar second, unresolved last — and it says which per vehicle.

Contact is the preferred anchor because it is direct and interpretable: two
recorders felt the same impact, so the difference between the times they stamped
it is the difference between their clocks, and nothing has to be fitted.

It is not sufficient. Two recorded cases proved that, and both are the reason
this module exists.

**A vehicle that never collides has no anchor.** In the partial-view scene the
leader only brakes. Contact alignment leaves it off the common timeline entirely,
so nothing it recorded reaches the merged log and the radar track of it is never
resolved to it. That is a whole account lost for want of a constant.

**A chain can give one anchor where two impacts happened.** On the recorded
three-car chain the middle vehicle registered a single contact. The third
vehicle's anchor was matched to it, and its whole timeline moved by exactly the
0.200 s between the two impacts — measured, not estimated: the A-B offset came
out exact and C's was out by 0.200000 s. Two impacts 0.200 s apart landed on the
same instant, so their order was not recoverable. Contact alignment flags the
anchor as doing double duty but cannot repair it from contact evidence alone,
because a recorder that missed an impact has no measurement of when it happened.

So the policy is hierarchical, never blended:

============  ======================================================
CONTACT       the participant has a contact offset and no caveat
              against it
RADAR         contact is missing, ambiguous, or suspect, *and* the
              radar estimate clears its confidence floor
UNRESOLVED    neither source is sufficient
============  ======================================================

Two numbers that both exist are not averaged. Averaging a good estimate with a
bad one produces a value neither supports — this project has already measured
that happening, on the same chain, when a true impact implied +0.267 s and a
spurious pairing -0.083 s and the median implied +0.092 s. The chosen source, the
estimate each source gave, and the reason for the choice are all recorded, so a
reader can see the decision rather than only its outcome.

Sign convention
---------------
``t_common = t_local + offset``, scale fixed at 1.0. The radar estimator fits
``t_observer = t_candidate + b``, so if the observer is already on common time
with ``off_observer``, then ``t_common = t_candidate + b + off_observer`` and the
candidate's offset is ``b + off_observer``. Observed the other way round, with
the unplaced vehicle as the observer, the same relation gives
``off_observer - b``. Both directions are used; they are independent
observations of one constant and are required to agree.

What the radar fallback may not use
-----------------------------------
The estimator sees anonymous local radar tracks, the participants' own recorded
trajectories, local timestamps and local collision triggers. It never sees a
CARLA actor id, a true participant identity, an oracle collision pair, an oracle
clock parameter, simulator time, map topology, or a scenario label. Drift is not
fitted: this path estimates an offset and says so.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.schemas import SCHEMA_VERSIONS, Provenance
from .clock_alignment import estimate_track_clock
from .contact_alignment import align_by_contact

LOGGER = logging.getLogger(__name__)

__all__ = [
    "CLOCK_SOURCES",
    "HYBRID_STATUSES",
    "align_hybrid",
    "radar_offset_candidates",
]

#: How one participant came to be on common time. Recorded per participant,
#: because reporting every aligned vehicle identically hides that one of them
#: rests on a fitted trajectory and the others on a physical impact.
CLOCK_SOURCES: Tuple[str, ...] = ("REFERENCE", "CONTACT", "RADAR", "UNRESOLVED")

#: Run-level verdicts this module can return.
HYBRID_STATUSES: Tuple[str, ...] = (
    "CONTACT_ALIGNED",
    "MULTI_CONTACT_ALIGNED",
    "RADAR_ALIGNED",
    "HYBRID_ALIGNED",
    "PARTIALLY_ALIGNED",
    "UNRESOLVED_TIME_ALIGNMENT",
)


def _cfg(cfg: Config, key: str, default: Any) -> Any:
    return cfg.get("fusion.hybrid_alignment." + key, default)


def _suspect_from_contact(contact: Mapping[str, Any]) -> List[str]:
    """Participants whose contact offset the contact stage itself distrusts.

    Read off the caveats rather than recomputed, so the two stages cannot drift
    apart in what they consider suspect.
    """
    out = {
        str(p)
        for caveat in (contact.get("shared_anchor_caveats") or [])
        for p in (caveat.get("participants_with_suspect_offset") or [])
    }
    return sorted(out)


def radar_offset_candidates(
    run: RunEvidence,
    target: str,
    placed: Mapping[str, float],
    cfg: Config,
) -> List[Dict[str, Any]]:
    """Every radar-derived estimate of ``target``'s offset, on the common clock.

    One estimate per (already-placed participant, radar track) pairing, in both
    observation directions: the placed vehicle may have tracked the target, or
    the target may have tracked the placed vehicle. Each is an independent look
    at the same constant.

    Identity is a hypothesis here, never a lookup. ``estimate_track_clock``
    scores an anonymous track against a candidate trajectory on position, range,
    range rate, velocity and heading, and returns nothing when the hypothesis
    does not hold up. No oracle breaks a tie.
    """
    out: List[Dict[str, Any]] = []
    target_ev: ParticipantEvidence = run.get(target)
    for other, other_offset in sorted(placed.items()):
        if other == target:
            continue
        other_ev: ParticipantEvidence = run.get(other)

        # The placed vehicle tracked the target: t_other = t_target + b.
        for track_id in sorted(other_ev.tracks_by_id()):
            fit = estimate_track_clock(
                other_ev, track_id, target_ev, cfg, offset_only=True
            )
            if not fit:
                continue
            out.append({
                "direction": "placed_observed_target",
                "observer": other,
                "candidate": target,
                "track_id": track_id,
                "offset_s": float(fit["offset_s"]) + float(other_offset),
                "pair_offset_s": float(fit["offset_s"]),
                "via": other,
                "via_offset_s": float(other_offset),
                "confidence": float(fit["confidence"]),
                "residual": float(fit["residual"]),
                "position_residual_m": fit.get("position_residual_m"),
                "n_samples": int(fit["n_samples"]),
                "overlap_s": float(fit["overlap_s"]),
                "methods": list(fit.get("methods") or []),
            })

        # The target tracked the placed vehicle: t_target = t_other + b, so the
        # target's own offset is off_other - b.
        for track_id in sorted(target_ev.tracks_by_id()):
            fit = estimate_track_clock(
                target_ev, track_id, other_ev, cfg, offset_only=True
            )
            if not fit:
                continue
            out.append({
                "direction": "target_observed_placed",
                "observer": target,
                "candidate": other,
                "track_id": track_id,
                "offset_s": float(other_offset) - float(fit["offset_s"]),
                "pair_offset_s": -float(fit["offset_s"]),
                "via": other,
                "via_offset_s": float(other_offset),
                "confidence": float(fit["confidence"]),
                "residual": float(fit["residual"]),
                "position_residual_m": fit.get("position_residual_m"),
                "n_samples": int(fit["n_samples"]),
                "overlap_s": float(fit["overlap_s"]),
                "methods": list(fit.get("methods") or []),
            })
    out.sort(key=lambda c: (-c["confidence"], c["via"], c["track_id"]))
    return out


def _choose_radar(
    candidates: Sequence[Mapping[str, Any]],
    cfg: Config,
) -> Tuple[Optional[Dict[str, Any]], str]:
    """The radar estimate to use, or nothing and the reason why not.

    Requirements, all of which have to hold:

    *Confidence.* The best fit clears a floor. A fit that explains the track
    badly is not evidence about a clock.

    *Agreement.* Where more than one independent pairing produced an estimate,
    they must agree to within a tolerance. Two views of one constant that
    disagree are not corroboration, and taking the more confident of them would
    be choosing which to believe on no stated grounds. This is the check that
    would have caught the averaged +0.092 s on the recorded chain.
    """
    if not candidates:
        return None, "no radar pairing produced a usable fit"

    floor = float(_cfg(cfg, "radar_min_confidence", 0.4))
    usable = [c for c in candidates if float(c["confidence"]) >= floor]
    if not usable:
        return None, (
            "the best radar fit scored {0:.3f}, below the {1:.2f} floor".format(
                float(candidates[0]["confidence"]), floor
            )
        )

    best = dict(usable[0])
    spread = 0.0
    if len(usable) > 1:
        values = [float(c["offset_s"]) for c in usable]
        spread = max(values) - min(values)
        tolerance = float(_cfg(cfg, "radar_max_disagreement_s", 0.15))
        if spread > tolerance:
            return None, (
                "{0} radar pairings disagree by {1:.3f} s, over the {2:.2f} s "
                "tolerance, so none of them establishes the offset".format(
                    len(usable), spread, tolerance
                )
            )
    best["n_supporting_pairings"] = len(usable)
    best["pairing_spread_s"] = round(spread, 6)
    return best, ""


def _status(sources: Mapping[str, str]) -> str:
    """The run-level verdict, from what each participant ended up resting on."""
    used = set(sources.values())
    if not used or used == {"UNRESOLVED"}:
        return "UNRESOLVED_TIME_ALIGNMENT"
    if "UNRESOLVED" in used:
        return "PARTIALLY_ALIGNED"
    if "RADAR" in used and "CONTACT" in used:
        return "HYBRID_ALIGNED"
    if "RADAR" in used:
        return "RADAR_ALIGNED"
    n_contact = sum(1 for s in sources.values() if s == "CONTACT")
    return "MULTI_CONTACT_ALIGNED" if n_contact > 1 else "CONTACT_ALIGNED"


def align_hybrid(
    run: RunEvidence,
    cfg: Config,
    contact: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Place every recorder on one timeline, preferring contact, and say how.

    The contact stage's reference and its accepted offsets are kept exactly as
    they are, so a run whose contacts are all reliable produces the same numbers
    it did before this module existed. Radar only ever fills gaps and replaces
    offsets the contact stage itself flagged.
    """
    contact_result = dict(contact) if contact is not None else align_by_contact(run, cfg)
    participants = sorted(run.participant_ids)
    contact_offsets: Dict[str, float] = {
        str(p): float(v) for p, v in (contact_result.get("offsets_s") or {}).items()
    }
    suspect = set(_suspect_from_contact(contact_result))
    ambiguous = contact_result.get("status") == "AMBIGUOUS_CONTACT_MATCH"

    # A suspect offset is not trusted, but it is also not thrown away before a
    # replacement exists: the participant is a candidate for radar, and keeps its
    # contact number if radar cannot do better.
    reference = contact_result.get("reference")
    trusted: Dict[str, float] = {}
    needs_radar: List[str] = []
    for pid in participants:
        if pid not in contact_offsets:
            needs_radar.append(pid)
        elif pid in suspect or (ambiguous and pid != reference):
            needs_radar.append(pid)
        else:
            trusted[pid] = contact_offsets[pid]

    if not trusted and contact_offsets:
        # Every contact offset is suspect. Keep the reference as the gauge so
        # there is something to relate radar estimates to.
        if reference and reference in contact_offsets:
            trusted[str(reference)] = contact_offsets[str(reference)]
            needs_radar = [p for p in needs_radar if p != str(reference)]

    enabled = bool(_cfg(cfg, "radar_fallback", True))
    chosen: Dict[str, float] = dict(trusted)
    sources: Dict[str, str] = {p: "CONTACT" for p in trusted}
    if reference and str(reference) in sources:
        sources[str(reference)] = "REFERENCE"
    decisions: Dict[str, Dict[str, Any]] = {}

    for pid in trusted:
        decisions[pid] = {
            "source": sources[pid],
            "contact_offset_s": round(contact_offsets[pid], 6),
            "radar_offset_s": None,
            "chosen_offset_s": round(contact_offsets[pid], 6),
            "reason": (
                "reference gauge for the common timeline"
                if sources[pid] == "REFERENCE"
                else "a shared contact ties this recorder in and nothing "
                     "impeaches that anchor, so no fit is needed"
            ),
        }

    # Radar is attempted in confidence order so that a participant placed by
    # radar can itself carry a later one. Each pass re-reads `chosen`, so a
    # three-car chain can be walked outward from the contact-aligned core.
    remaining = list(needs_radar)
    while enabled and remaining and chosen:
        progressed = False
        for pid in list(remaining):
            candidates = radar_offset_candidates(run, pid, chosen, cfg)
            best, why_not = _choose_radar(candidates, cfg)
            if best is None:
                continue
            contact_value = contact_offsets.get(pid)
            chosen[pid] = float(best["offset_s"])
            sources[pid] = "RADAR"
            decisions[pid] = {
                "source": "RADAR",
                "contact_offset_s": (
                    None if contact_value is None else round(contact_value, 6)
                ),
                "radar_offset_s": round(float(best["offset_s"]), 6),
                "chosen_offset_s": round(float(best["offset_s"]), 6),
                "reason": (
                    "no shared contact ties this recorder in, and the radar fit "
                    "clears its confidence floor"
                    if contact_value is None else
                    "the contact-derived offset is impeached -- {0} -- and the "
                    "radar fit is independent of the anchor that impeached "
                    "it".format(
                        "contact matching was ambiguous" if ambiguous
                        else "its anchor also related another recorder"
                    )
                ),
                "radar_evidence": {
                    k: best.get(k) for k in (
                        "direction", "observer", "candidate", "track_id", "via",
                        "pair_offset_s", "via_offset_s", "confidence", "residual",
                        "position_residual_m", "n_samples", "overlap_s", "methods",
                        "n_supporting_pairings", "pairing_spread_s",
                    )
                },
                "drift": "not estimated; this path fits an offset only",
            }
            if contact_value is not None:
                decisions[pid]["contact_radar_difference_s"] = round(
                    float(best["offset_s"]) - float(contact_value), 6
                )
            remaining.remove(pid)
            progressed = True
        if not progressed:
            break

    for pid in remaining:
        contact_value = contact_offsets.get(pid)
        candidates = radar_offset_candidates(run, pid, chosen, cfg) if enabled and chosen else []
        _, why_not = _choose_radar(candidates, cfg) if enabled else (None, "the radar fallback is disabled")
        if contact_value is not None:
            # Suspect, and radar could not replace it. Keeping it is better than
            # discarding a whole account, but the caveat has to travel with it.
            chosen[pid] = float(contact_value)
            sources[pid] = "CONTACT"
            decisions[pid] = {
                "source": "CONTACT",
                "contact_offset_s": round(contact_value, 6),
                "radar_offset_s": None,
                "chosen_offset_s": round(contact_value, 6),
                "reason": (
                    "the contact-derived offset is impeached and radar could not "
                    "replace it ({0}), so it is kept and stays flagged: the "
                    "error is the interval between two impacts, which nothing "
                    "recorded measures".format(why_not)
                ),
                "suspect": True,
            }
        else:
            sources[pid] = "UNRESOLVED"
            decisions[pid] = {
                "source": "UNRESOLVED",
                "contact_offset_s": None,
                "radar_offset_s": None,
                "chosen_offset_s": None,
                "reason": (
                    "no shared contact and no sufficient radar evidence ({0}); "
                    "this recorder stays on its own clock and none is "
                    "assumed".format(why_not)
                ),
            }

    status = _status(sources)
    offsets = _per_participant(participants, chosen, sources, decisions, contact_result)
    out: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "method": "hybrid_contact_then_radar",
        "provenance": Provenance.FUSED.value,
        "status": status,
        "reference": reference,
        "offsets_s": {p: round(v, 6) for p, v in sorted(chosen.items())},
        "offsets": offsets,
        "clock_sources": {p: sources[p] for p in sorted(sources)},
        "n_contact_aligned": sum(
            1 for s in sources.values() if s in ("CONTACT", "REFERENCE")
        ),
        "n_radar_aligned": sum(1 for s in sources.values() if s == "RADAR"),
        "n_unresolved": sum(1 for s in sources.values() if s == "UNRESOLVED"),
        "scale": 1.0,
        "drift": {
            "estimated": False,
            "assumption": "negligible over the recorded window",
            "why_not": (
                "a contact anchor fixes one instant and says nothing about rate, "
                "and the radar fallback is deliberately restricted to an offset. "
                "Neither path claims drift"
            ),
        },
        "selection_rule": (
            "reliable contact wins; missing, ambiguous or impeached contact "
            "falls back to radar when it clears its floor and its independent "
            "pairings agree; otherwise unresolved. Contact and radar estimates "
            "are never averaged"
        ),
        "decisions": {p: decisions[p] for p in sorted(decisions)},
        "aligned_participants": sorted(chosen),
        "unaligned_participants": sorted(
            p for p in participants if sources.get(p) == "UNRESOLVED"
        ),
        "formula": "t_common = t_local + offset_s, with scale fixed at 1.0",
        # Everything the contact stage found, kept whole. The S06 ablation reads
        # its caveats and anchor counts straight out of here.
        "contact_stage": {
            k: contact_result.get(k)
            for k in (
                "status", "reason", "reference", "offsets_s", "n_contact_anchors",
                "n_shared_contacts", "shared_anchor_caveats", "ambiguous_pairings",
                "inconsistent_pairings", "anchors", "pairs", "transitive_chains",
                "n_pairings_rejected_as_weaker", "n_links_used", "n_links_spare",
            )
            if k in contact_result
        },
    }
    # No converters in here. This result is written to clock_alignment.json, and
    # callables in an artifact are a serialisation failure waiting to happen;
    # consumers derive them with contact_alignment.converters_of, so what they
    # apply is exactly what the file states.
    for key in ("common_span", "grid_dt"):
        if key in contact_result:
            out[key] = contact_result[key]
    return out


def _per_participant(
    participants: Sequence[str],
    chosen: Mapping[str, float],
    sources: Mapping[str, str],
    decisions: Mapping[str, Mapping[str, Any]],
    contact_result: Mapping[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """The transform block the fusion machinery consumes, plus its provenance.

    ``status`` stays ``ALIGNED``/``UNRESOLVED`` because that is what
    :class:`~cdf.fusion.aligned_evidence.AlignedRunEvidence` reads. ``source``
    is the new field, and it is what stops a radar-placed vehicle from being
    presented exactly like one tied in by a physical impact.
    """
    contact_confidence = {
        str(p): (v or {}).get("confidence")
        for p, v in (contact_result.get("offsets") or {}).items()
    }
    out: Dict[str, Dict[str, Any]] = {}
    for pid in sorted(participants):
        source = sources.get(pid, "UNRESOLVED")
        decision = decisions.get(pid, {})
        if pid in chosen:
            if source == "RADAR":
                evidence = decision.get("radar_evidence") or {}
                confidence = float(evidence.get("confidence") or 0.0)
                residual = evidence.get("residual")
            else:
                confidence = float(contact_confidence.get(pid) or 0.0)
                residual = None
            out[pid] = {
                "status": "ALIGNED",
                "source": source,
                "scale": 1.0,
                "offset_s": round(float(chosen[pid]), 6),
                "confidence": round(confidence, 6),
                "drift_ppm": None,
                "residual": residual,
                "note": "scale fixed at 1.0; drift not estimated",
                "caveat": decision.get("reason"),
                "suspect": bool(decision.get("suspect")),
            }
        else:
            out[pid] = {
                "status": "UNRESOLVED",
                "source": "UNRESOLVED",
                "scale": 1.0,
                "offset_s": None,
                "confidence": 0.0,
                "drift_ppm": None,
                "residual": None,
                "note": (
                    "neither a shared contact nor a sufficient radar fit places "
                    "this recorder, so no offset was estimated and none is "
                    "assumed"
                ),
                "caveat": decision.get("reason"),
                "suspect": False,
            }
    return out
