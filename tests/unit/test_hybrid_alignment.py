"""The selection rule: contact first, radar second, unresolved last.

Every test here is about *which source was chosen and why*, not about whether a
number is close. The failure this module exists to prevent is a timeline that
looks uniformly aligned while one vehicle on it rests on a fitted trajectory and
another on a physical impact — and the failure it must not introduce is a radar
fit quietly replacing a contact anchor that was fine.

The radar estimator is stubbed in most of these. What is under test is the
policy; the estimator has its own tests, and the measured accuracy of the whole
comes from the recorded runs rather than from a fixture.
"""

from __future__ import annotations

import pytest

from cdf.common.config import Config
from cdf.fusion import hybrid_alignment
from cdf.fusion.hybrid_alignment import CLOCK_SOURCES, align_hybrid


class FakeParticipant:
    def __init__(self, pid, tracks=()):
        self.participant_id = pid
        self._tracks = {t: [object()] for t in tracks}

    def tracks_by_id(self):
        return self._tracks


class FakeRun:
    """Just enough of RunEvidence for the selection logic."""

    def __init__(self, participants, tracks=None):
        self.participant_ids = list(participants)
        tracks = tracks or {}
        self._by_id = {
            p: FakeParticipant(p, tracks.get(p, ())) for p in participants
        }

    def get(self, pid):
        return self._by_id[pid]


def contact_result(offsets, status="CONTACT_ALIGNED", reference="A", caveats=()):
    return {
        "status": status,
        "reference": reference,
        "offsets_s": dict(offsets),
        "offsets": {
            p: {"status": "ALIGNED", "offset_s": v, "confidence": 0.9}
            for p, v in offsets.items()
        },
        "shared_anchor_caveats": list(caveats),
        "n_contact_anchors": len(offsets),
    }


def stub_radar(monkeypatch, per_target):
    """Make the radar stage return fixed candidates per target participant.

    ``per_target`` maps a participant id to a list of ``(offset, confidence)``
    pairs, each standing for one independent pairing. The offsets are already on
    the common clock, which is what the real function returns.
    """
    def fake(run, target, placed, cfg):
        out = []
        for i, (offset, confidence) in enumerate(per_target.get(target, [])):
            out.append({
                "direction": "placed_observed_target",
                "observer": sorted(placed)[0] if placed else "?",
                "candidate": target,
                "track_id": "{0}::T{1:03d}".format(target, i + 1),
                "offset_s": float(offset),
                "pair_offset_s": float(offset),
                "via": sorted(placed)[0] if placed else "?",
                "via_offset_s": 0.0,
                "confidence": float(confidence),
                "residual": 0.01,
                "position_residual_m": 0.2,
                "n_samples": 120,
                "overlap_s": 6.0,
                "methods": ["radar_position", "radar_range"],
            })
        out.sort(key=lambda c: -c["confidence"])
        return out

    monkeypatch.setattr(hybrid_alignment, "radar_offset_candidates", fake)


CFG = Config({})


# --- contact is preferred wherever it is sound -----------------------------


def test_a_clean_contact_selects_contact(monkeypatch):
    stub_radar(monkeypatch, {})
    run = FakeRun(["A", "B"])
    out = align_hybrid(run, CFG, contact=contact_result({"A": 0.0, "B": -0.25}))
    assert out["clock_sources"] == {"A": "REFERENCE", "B": "CONTACT"}
    assert out["status"] == "CONTACT_ALIGNED"
    assert out["offsets_s"] == {"A": 0.0, "B": -0.25}
    assert out["n_radar_aligned"] == 0


def test_a_reliable_contact_keeps_contact_even_when_radar_is_available(monkeypatch):
    """The fallback must not replace an anchor that nothing impeached, however
    confident the fit. A physical impact is better evidence than a trajectory."""
    stub_radar(monkeypatch, {"B": [(-0.9, 0.99)]})
    run = FakeRun(["A", "B"], {"A": ("A::T001",)})
    out = align_hybrid(run, CFG, contact=contact_result({"A": 0.0, "B": -0.25}))
    assert out["clock_sources"]["B"] == "CONTACT"
    assert out["offsets_s"]["B"] == -0.25
    assert out["decisions"]["B"]["radar_offset_s"] is None
    assert "no fit is needed" in out["decisions"]["B"]["reason"]


# --- radar fills the gaps --------------------------------------------------


def test_no_contact_at_all_with_strong_radar_selects_radar(monkeypatch):
    stub_radar(monkeypatch, {"B": [(-0.4, 0.95)]})
    run = FakeRun(["A", "B"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"] == {"A": "REFERENCE", "B": "RADAR"}
    assert out["status"] == "RADAR_ALIGNED"
    assert out["offsets_s"]["B"] == -0.4


def test_contact_for_two_and_radar_for_the_non_contact_third_is_hybrid(monkeypatch):
    """The partial-view shape: A and B collide, C only brakes."""
    stub_radar(monkeypatch, {"C": [(0.12, 0.93)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"] == {
        "A": "REFERENCE", "B": "CONTACT", "C": "RADAR",
    }
    assert out["status"] == "HYBRID_ALIGNED"
    assert out["n_contact_aligned"] == 2
    assert out["n_radar_aligned"] == 1
    assert out["n_unresolved"] == 0


def test_an_ambiguous_contact_match_falls_back_to_radar(monkeypatch):
    """Which impact is which could not be decided, so the offsets it implies are
    not offsets this method established."""
    stub_radar(monkeypatch, {"B": [(-0.31, 0.92)]})
    run = FakeRun(["A", "B"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.25},
            status="AMBIGUOUS_CONTACT_MATCH", reference="A",
        ),
    )
    assert out["clock_sources"]["B"] == "RADAR"
    assert out["offsets_s"]["B"] == -0.31
    assert "ambiguous" in out["decisions"]["B"]["reason"]


def test_a_suspect_shared_anchor_falls_back_to_radar_for_that_participant(
    monkeypatch,
):
    """The chain case. B's single anchor related both neighbours, so C's offset
    is impeached -- and only C's. A keeps its contact offset."""
    stub_radar(monkeypatch, {"C": [(-0.0826, 0.99)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": -0.2674, "B": 0.0, "C": -0.2808},
            status="MULTI_CONTACT_ALIGNED", reference="B",
            caveats=[{
                "anchor": "B#0",
                "participants_with_suspect_offset": ["C"],
            }],
        ),
    )
    assert out["clock_sources"] == {
        "A": "CONTACT", "B": "REFERENCE", "C": "RADAR",
    }
    assert out["offsets_s"]["A"] == -0.2674, "A's sound anchor must survive"
    assert out["offsets_s"]["C"] == -0.0826
    decision = out["decisions"]["C"]
    assert decision["contact_offset_s"] == -0.2808
    assert decision["radar_offset_s"] == -0.0826
    assert decision["contact_radar_difference_s"] == pytest.approx(0.1982, abs=1e-4)
    assert "impeached" in decision["reason"]


# --- when radar is not good enough ----------------------------------------


def test_weak_radar_leaves_a_non_contact_participant_unresolved(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.12, 0.10)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"]["C"] == "UNRESOLVED"
    assert out["status"] == "PARTIALLY_ALIGNED"
    assert "C" in out["unaligned_participants"]
    assert out["offsets"]["C"]["offset_s"] is None
    assert "below the 0.40 floor" in out["decisions"]["C"]["reason"]


def test_no_radar_evidence_at_all_leaves_the_participant_unresolved(monkeypatch):
    stub_radar(monkeypatch, {})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"]["C"] == "UNRESOLVED"
    assert "no radar pairing" in out["decisions"]["C"]["reason"]


def test_disagreeing_radar_pairings_establish_nothing(monkeypatch):
    """Two looks at one constant that disagree are not corroboration, and
    believing the more confident one would be a choice on no stated grounds.
    This is the check that would have caught the averaged +0.092 s."""
    stub_radar(monkeypatch, {"C": [(0.267, 0.95), (-0.083, 0.91)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"]["C"] == "UNRESOLVED"
    reason = out["decisions"]["C"]["reason"]
    assert "disagree by" in reason
    assert "0.350" in reason, "the spread itself has to be reported"


def test_agreeing_radar_pairings_are_accepted_and_the_spread_recorded(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.120, 0.95), (0.130, 0.91)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"]["C"] == "RADAR"
    evidence = out["decisions"]["C"]["radar_evidence"]
    assert evidence["n_supporting_pairings"] == 2
    assert evidence["pairing_spread_s"] == pytest.approx(0.01, abs=1e-9)


def test_an_impeached_contact_offset_radar_cannot_replace_is_kept_and_flagged(
    monkeypatch,
):
    """Discarding it would throw away a whole account over a caveat. Keeping it
    silently would hide the caveat. It is kept, and it stays flagged."""
    stub_radar(monkeypatch, {})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": -0.2674, "B": 0.0, "C": -0.2808},
            status="MULTI_CONTACT_ALIGNED", reference="B",
            caveats=[{
                "anchor": "B#0", "participants_with_suspect_offset": ["C"],
            }],
        ),
    )
    assert out["clock_sources"]["C"] == "CONTACT"
    assert out["offsets_s"]["C"] == -0.2808
    assert out["offsets"]["C"]["suspect"] is True
    reason = out["decisions"]["C"]["reason"]
    assert "radar could not replace it" in reason
    assert "nothing recorded measures" in reason


# --- the fallback can be switched off, which is the ablation --------------


def test_the_radar_fallback_can_be_disabled_to_reproduce_contact_only(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.12, 0.99)]})
    run = FakeRun(["A", "B", "C"])
    cfg = Config({"fusion": {"hybrid_alignment": {"radar_fallback": False}}})
    out = align_hybrid(
        run, cfg,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["clock_sources"]["C"] == "UNRESOLVED"
    assert "disabled" in out["decisions"]["C"]["reason"]


# --- what the result must always say -------------------------------------


def test_every_participant_carries_a_source(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.12, 0.93)]})
    run = FakeRun(["A", "B", "C", "D"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    for pid in ("A", "B", "C", "D"):
        assert out["offsets"][pid]["source"] in CLOCK_SOURCES
        assert out["clock_sources"][pid] in CLOCK_SOURCES
        assert out["offsets"][pid]["caveat"], "every placement states its grounds"


def test_no_result_claims_drift_or_a_scale(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.12, 0.93)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    assert out["scale"] == 1.0
    assert out["drift"]["estimated"] is False
    for pid in ("A", "B", "C"):
        assert out["offsets"][pid]["scale"] == 1.0
        assert out["offsets"][pid]["drift_ppm"] is None


def test_the_result_is_serialisable(monkeypatch):
    """It is written to clock_alignment.json. Callables in an artifact are a
    serialisation failure waiting to happen, and this module had one."""
    import json

    stub_radar(monkeypatch, {"C": [(0.12, 0.93)]})
    run = FakeRun(["A", "B", "C"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A"
        ),
    )
    json.dumps(out)
    assert "converters" not in out


def test_the_contact_stage_is_kept_whole_for_the_ablation(monkeypatch):
    stub_radar(monkeypatch, {"C": [(0.12, 0.93)]})
    run = FakeRun(["A", "B", "C"])
    contact = contact_result(
        {"A": 0.0, "B": -0.2}, status="PARTIALLY_ALIGNED", reference="A",
        caveats=[{"anchor": "B#0", "participants_with_suspect_offset": []}],
    )
    out = align_hybrid(run, CFG, contact=contact)
    stage = out["contact_stage"]
    assert stage["status"] == "PARTIALLY_ALIGNED"
    assert stage["offsets_s"] == {"A": 0.0, "B": -0.2}
    assert stage["shared_anchor_caveats"]


def test_nothing_placed_by_either_source_is_unresolved(monkeypatch):
    stub_radar(monkeypatch, {})
    run = FakeRun(["A", "B"])
    out = align_hybrid(
        run, CFG,
        contact=contact_result(
            {}, status="UNALIGNED_NO_SHARED_CONTACT", reference=None
        ),
    )
    assert out["status"] == "UNRESOLVED_TIME_ALIGNMENT"
    assert out["offsets_s"] == {}
    assert sorted(out["unaligned_participants"]) == ["A", "B"]


def test_a_radar_fit_on_the_search_bound_is_declined() -> None:
    """An offset at the edge of the window is a failure to find one.

    The optimiser is bounded, so when no offset fits it returns the bound and
    reports it with the same confidence as a real answer. In the campaign that
    found this, a vehicle that could not be placed at all came back placed a
    full second out with confidence 0.94. Every offset this estimator resolves
    legitimately lands well inside the window -- the largest measured across
    the campaign is 0.57 s against a 1.0 s limit -- so the bound is never a
    right answer, and saying nothing is better than saying that.
    """
    import inspect

    from cdf.fusion import clock_alignment

    source = inspect.getsource(clock_alignment)
    assert "if abs(b) >= limit - step:" in source, (
        "the bound-hit guard has gone; a radar fit that ran out of search "
        "window will be reported as a confident offset again"
    )
