"""Contact-based clock alignment: the four cases the brief names, and the traps.

The method is one subtraction, so what needs testing is not the arithmetic but
the judgement around it: does it recover a known offset, does it chain three cars
through a middle vehicle, does it refuse when two impacts are indistinguishable,
and does it stay silent when there was no impact at all. The last is the one that
matters most -- a method that quietly substituted simulator time would score
beautifully on every negative control while measuring nothing.
"""

from __future__ import annotations

from typing import List, Optional

import pytest

from cdf.common.config import Config
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import LocalTriggerRecord, TelemetrySample, TriggerKind
from cdf.fusion.contact_alignment import (
    ALIGNMENT_STATUSES,
    align_by_contact,
    contact_anchors,
    converters_from,
    converters_of,
)


def cfg() -> Config:
    return Config({})


def telemetry(
    pid: str, t0: float, t1: float, x: float, y: float, dt: float = 0.05
) -> List[TelemetrySample]:
    """A recorder standing still at (x, y) on its own clock from t0 to t1.

    Position is constant because these tests are about clocks, not motion: what
    matters is that the two parties to one impact report nearly the same place.
    """
    out = []
    n = int(round((t1 - t0) / dt)) + 1
    for i in range(n):
        t = t0 + i * dt
        out.append(TelemetrySample(
            t=t, frame=i, participant_id=pid, x=x, y=y, z=0.0, yaw=0.0, speed=8.0,
        ))
    return out


def impact(pid: str, t: float, impulse: float) -> LocalTriggerRecord:
    return LocalTriggerRecord(
        t=t, frame=int(t / 0.05), participant_id=pid,
        kind=TriggerKind.COLLISION, collision_detected=True, impulse=impulse,
    )


def participant(
    pid: str,
    impacts: List[LocalTriggerRecord],
    x: float = 0.0,
    y: float = 0.0,
    t0: float = 0.0,
    t1: float = 20.0,
) -> ParticipantEvidence:
    return ParticipantEvidence(
        participant_id=pid,
        telemetry=telemetry(pid, t0, t1, x, y),
        triggers=impacts,
    )


def run_of(*participants: ParticipantEvidence) -> RunEvidence:
    from pathlib import Path

    return RunEvidence(
        run_dir=Path("."),
        manifest={"run_id": "test", "scenario_id": "T", "seed": 0},
        participants={p.participant_id: p for p in participants},
    )


# --- reading anchors off a recording ---------------------------------------


def test_only_real_impacts_become_anchors():
    """A zero-impulse trigger matches every other zero equally well."""
    ev = ParticipantEvidence(
        participant_id="A",
        telemetry=telemetry("A", 0.0, 10.0, 0.0, 0.0),
        triggers=[
            impact("A", 5.0, 3000.0),
            impact("A", 6.0, 0.0),
            LocalTriggerRecord(t=7.0, frame=140, participant_id="A",
                               kind=TriggerKind.NEAR_MISS, collision_detected=False),
        ],
    )
    anchors = contact_anchors(ev)
    assert [a.t_local for a in anchors] == [5.0]


def test_an_anchor_carries_where_the_recorder_thought_it_was():
    ev = participant("A", [impact("A", 5.0, 3000.0)], x=12.0, y=-4.0)
    anchor = contact_anchors(ev)[0]
    assert (anchor.x, anchor.y) == (12.0, -4.0)


def test_anchors_are_indexed_in_the_order_they_were_felt():
    ev = participant("B", [impact("B", 9.0, 2000.0), impact("B", 5.0, 3000.0)])
    anchors = contact_anchors(ev)
    assert [a.index for a in anchors] == [0, 1]
    assert [a.t_local for a in anchors] == [5.0, 9.0]


# --- the two-car case: one impact, one offset ------------------------------


def test_one_shared_impact_recovers_the_offset():
    """B's clock runs 1.4 s behind A's. One impact is enough to say so."""
    run = run_of(
        participant("A", [impact("A", 8.60, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 7.20, 4100.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "CONTACT_ALIGNED"
    offsets = result["offsets_s"]
    assert offsets[result["reference"]] == 0.0
    # Direction matters, not just magnitude: B's clock reads 1.4 s *less* than
    # A's at the same instant, so reaching common time from B adds 1.4 s.
    assert offsets["B"] - offsets["A"] == pytest.approx(1.40, abs=1e-6)


def test_the_converters_put_both_recorders_on_one_axis():
    run = run_of(
        participant("A", [impact("A", 8.60, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 7.20, 4100.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    to_common = converters_of(result)
    # The one physical impact must land at one common time.
    assert to_common["A"](8.60) == pytest.approx(to_common["B"](7.20), abs=1e-6)


def test_scale_is_exactly_one_and_drift_is_not_claimed():
    """One impact constrains an offset and says nothing about rate."""
    run = run_of(
        participant("A", [impact("A", 8.60, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 7.20, 4100.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["scale"] == 1.0
    assert result["drift"]["estimated"] is False
    assert "negligible" in result["drift"]["assumption"]
    assert "rate" in result["drift"]["why_not"]


def test_converters_are_not_all_bound_to_the_last_offset():
    """The classic closure-over-loop-variable bug, pinned down."""
    to_common = converters_from({"A": 0.0, "B": 1.4, "C": -2.5})
    assert to_common["A"](10.0) == pytest.approx(10.0)
    assert to_common["B"](10.0) == pytest.approx(11.4)
    assert to_common["C"](10.0) == pytest.approx(7.5)


# --- three cars: transitive alignment through the middle vehicle -----------


def test_three_cars_align_transitively_through_the_middle():
    """A touches B, B touches C, A never touches C -- all three still align.

    B is hit twice, so B is the best-connected recorder and becomes the
    reference. A reaches C only through B, which is the whole point.
    """
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] in {"CONTACT_ALIGNED", "MULTI_CONTACT_ALIGNED"}
    assert result["reference"] == "B"
    assert set(result["aligned_participants"]) == {"A", "B", "C"}
    assert result["unaligned_participants"] == []

    to_common = converters_of(result)
    # A's impact and B's first impact are one event; likewise B's second and C's.
    assert to_common["A"](10.00) == pytest.approx(to_common["B"](8.00), abs=1e-6)
    assert to_common["C"](12.50) == pytest.approx(to_common["B"](9.00), abs=1e-6)


def test_the_transitive_chain_is_recorded_so_a_reader_can_see_the_route():
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    chains = align_by_contact(run, cfg())["transitive_chains"]
    assert ["B", "A"] in chains
    assert ["B", "C"] in chains


def test_a_recorder_no_chain_reaches_stays_unaligned_and_is_named():
    """C collided with something off-camera, 200 m away. It must not be folded in."""
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0)], x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 900.0)], x=-300.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "PARTIALLY_ALIGNED"
    assert result["unaligned_participants"] == ["C"]
    assert "C" not in converters_of(result)


# --- refusing what the evidence does not separate --------------------------


def test_two_indistinguishable_impacts_are_refused_not_guessed():
    """B felt two near-identical impacts at the same place; A felt one.

    Nothing in impulse or position says which of B's impacts was A's, so the
    answer has to be a refusal.
    """
    run = run_of(
        participant("A", [impact("A", 10.00, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 4000.0), impact("B", 8.40, 4000.0)],
                    x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "AMBIGUOUS_CONTACT_MATCH"
    assert result["offsets_s"] == {}
    assert result["ambiguous_pairings"]
    assert "cannot be decided" in result["ambiguous_pairings"][0]["reason"]


def test_a_clear_impulse_difference_does_separate_two_impacts():
    """The same shape as above, but the impulses differ -- so it resolves."""
    run = run_of(
        participant("A", [impact("A", 10.00, 8000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 8100.0), impact("B", 8.40, 1200.0)],
                    x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "CONTACT_ALIGNED"
    to_common = converters_of(result)
    assert to_common["A"](10.00) == pytest.approx(to_common["B"](8.00), abs=1e-6)


def test_impacts_far_apart_in_space_are_not_the_same_impact():
    """Both felt one hit of similar force, but 60 m apart. Not one event."""
    run = run_of(
        participant("A", [impact("A", 10.00, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 4050.0)], x=160.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "UNALIGNED_NO_SHARED_CONTACT"
    assert converters_of(result) == {}


def test_wildly_different_impulses_are_not_the_same_impact():
    run = run_of(
        participant("A", [impact("A", 10.00, 9000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 90.0)], x=101.0, y=0.0),
    )
    assert align_by_contact(run, cfg())["status"] == "UNALIGNED_NO_SHARED_CONTACT"


# --- the no-collision case, which must not be papered over ----------------


def test_a_run_with_no_contact_is_left_unaligned():
    run = run_of(
        participant("A", [], x=100.0, y=0.0),
        participant("B", [], x=140.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "UNALIGNED_NO_SHARED_CONTACT"
    assert result["offsets_s"] == {}
    assert converters_of(result) == {}
    assert result["reference"] is None
    assert sorted(result["unaligned_participants"]) == ["A", "B"]


def test_the_no_contact_refusal_says_why_and_rules_out_simulator_time():
    run = run_of(participant("A", []), participant("B", []))
    result = align_by_contact(run, cfg())
    assert "cannot align a no-collision run" in result["reason"]
    assert "simulator time" in result["note"].lower()


def test_one_sided_contact_does_not_align_anything():
    """A was hit by a wall; B never touched anything. No shared event exists."""
    run = run_of(
        participant("A", [impact("A", 6.0, 3000.0)], x=100.0, y=0.0),
        participant("B", [], x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "UNALIGNED_NO_SHARED_CONTACT"
    assert result["n_contact_anchors"] == 1
    assert result["n_shared_contacts"] == 0


# --- reporting contracts --------------------------------------------------


def test_every_status_returned_is_one_of_the_documented_ones():
    cases = [
        run_of(participant("A", []), participant("B", [])),
        run_of(
            participant("A", [impact("A", 10.0, 4000.0)], x=100.0, y=0.0),
            participant("B", [impact("B", 8.0, 4050.0)], x=101.0, y=0.0),
        ),
        run_of(
            participant("A", [impact("A", 10.0, 4000.0)], x=100.0, y=0.0),
            participant("B", [impact("B", 8.0, 4000.0), impact("B", 8.4, 4000.0)],
                        x=101.0, y=0.0),
        ),
    ]
    for run in cases:
        assert align_by_contact(run, cfg())["status"] in ALIGNMENT_STATUSES


def test_two_shared_impacts_report_their_internal_agreement():
    """The spread between two independently implied offsets is the only check
    available on the estimate, so it has to be in the artifact."""
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0), impact("A", 14.00, 2000.0)],
                    x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 12.02, 2050.0)],
                    x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["status"] == "MULTI_CONTACT_ALIGNED"
    pair = result["pairs"]["B->A"]
    assert pair["n_shared_contacts"] == 2
    assert pair["offset_spread_s"] == pytest.approx(0.02, abs=1e-6)
    assert "median" in pair["estimator"]


def test_the_anchors_behind_the_estimate_are_all_published():
    run = run_of(
        participant("A", [impact("A", 10.0, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.0, 4050.0)], x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert [a["t_local"] for a in result["anchors"]["A"]] == [10.0]
    assert result["anchors"]["B"][0]["impulse"] == 4050.0
    match = result["pairs"]["B->A"]["matches"][0]
    assert match["separation_m"] == pytest.approx(1.0)
    assert match["localisation_available"] is True


def test_no_privileged_collision_pair_identity_appears_anywhere():
    """The whole method rests on not knowing who hit whom."""
    import json

    run = run_of(
        participant("A", [impact("A", 10.0, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.0, 4050.0)], x=101.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    blob = json.dumps(result)
    for forbidden in ("actor_id", "collision_pair", "true_pair", "counterparty"):
        assert forbidden not in blob


def test_missing_localisation_at_contact_degrades_rather_than_fails():
    """A recorder whose telemetry gapped at impact keeps the impulse evidence."""
    a = ParticipantEvidence(
        participant_id="A",
        telemetry=telemetry("A", 0.0, 4.0, 100.0, 0.0),  # ends long before impact
        triggers=[impact("A", 10.0, 4000.0)],
    )
    run = run_of(a, participant("B", [impact("B", 8.0, 4050.0)], x=101.0, y=0.0))
    result = align_by_contact(run, cfg())
    assert result["status"] == "CONTACT_ALIGNED"
    match = result["pairs"]["B->A"]["matches"][0]
    assert match["localisation_available"] is False
    assert match["separation_m"] is None


# --- a contradicting pairing: weaker evidence, or a genuine tie? -----------


def test_the_chain_records_the_spurious_outer_pairing_it_rejected():
    """In a chain, A and C are beside each other at impact but never touched.

    Position alone will happily pair them. The impulses will not agree, so the
    pairing scores lower than the two real ones and is rejected -- but it has to
    leave a trace, or the conflict cannot be audited afterwards.
    """
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    rejected = [
        e for e in result["inconsistent_pairings"]
        if e["resolution"] == "rejected_as_weaker"
    ]
    assert [e["participants"] for e in rejected] == [["A", "C"]]
    assert result["n_pairings_rejected_as_weaker"] == 1
    # It was rejected because the links the alignment used are better evidenced.
    assert rejected[0]["weakest_link_used"] > rejected[0]["score"]
    assert result["status"] in {"CONTACT_ALIGNED", "MULTI_CONTACT_ALIGNED"}


def test_a_contradiction_the_evidence_does_not_settle_stays_unresolved():
    """The same chain, but with the bar for 'clearly better evidenced' raised
    above the gap the impulses actually provide.

    The spurious A-C pairing is 0.31 worse than the links the alignment used.
    Demanding a 0.9 margin makes that no longer decisive, and the honest answer
    becomes an ambiguous contact match rather than a quiet tie-break. This is
    what the ambiguity margin controls, so it is tested through the knob.
    """
    strict = Config(
        {"fusion": {"contact_alignment": {"consistency_margin": 0.9}}}
    )
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    result = align_by_contact(run, strict)
    assert result["status"] == "AMBIGUOUS_CONTACT_MATCH"
    unresolved = [
        e for e in result["inconsistent_pairings"] if e["resolution"] == "unresolved"
    ]
    assert [e["participants"] for e in unresolved] == [["A", "C"]]
    assert "does not clearly favour either" in unresolved[0]["reason"]


def test_a_consistent_triangle_is_not_flagged_at_all():
    """Three recorders in one multi-car impact, each feeling it once.

    The three pairwise offsets then satisfy offset(A,C) = offset(A,B) +
    offset(B,C) identically, so the spare link agrees with the tree exactly.
    The check must stay silent on evidence that is merely redundant -- and this
    is the case that catches a sign error in the consistency arithmetic, because
    an inverted sign turns a perfect agreement into a 2 s disagreement.
    """
    run = run_of(
        participant("A", [impact("A", 10.00, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 4050.0)], x=101.0, y=0.0),
        participant("C", [impact("C", 9.00, 4020.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["inconsistent_pairings"] == []
    assert result["n_links_spare"] == 1
    to_common = converters_of(result)
    assert to_common["A"](10.00) == pytest.approx(to_common["C"](9.00), abs=1e-6)


def test_the_alignment_uses_exactly_one_link_fewer_than_it_has_recorders():
    """A spanning tree over n recorders has n-1 links, by construction."""
    run = run_of(
        participant("A", [impact("A", 10.00, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 5100.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    assert result["n_links_used"] == len(result["aligned_participants"]) - 1


# --- the no-contact runs, and the marker that is not simulator time --------


def test_acquisition_start_alignment_relates_the_recorders():
    """The harness starts every recorder in one tick, which is a declared fact."""
    from cdf.fusion.contact_alignment import align_by_acquisition_start

    run = run_of(
        participant("A", [], t0=0.00, t1=20.0),
        participant("B", [], t0=1.40, t1=21.4),
    )
    result = align_by_acquisition_start(run, cfg())
    assert result["status"] == "ACQUISITION_START_ALIGNED"
    to_common = converters_of(result)
    assert to_common["A"](0.00) == pytest.approx(to_common["B"](1.40), abs=1e-6)


def test_it_is_never_reported_as_a_contact_status():
    """The distinction has to survive into the artifact, or it erodes."""
    from cdf.fusion.contact_alignment import (
        CONTACT_DERIVED_STATUSES, align_by_acquisition_start,
    )

    run = run_of(participant("A", [], t0=0.0), participant("B", [], t0=1.4))
    result = align_by_acquisition_start(run, cfg())
    assert result["status"] not in CONTACT_DERIVED_STATUSES
    assert result["method"] == "acquisition_start_marker"


def test_it_carries_the_caveat_that_says_where_the_common_time_came_from():
    from cdf.fusion.contact_alignment import align_by_acquisition_start

    run = run_of(participant("A", [], t0=0.0), participant("B", [], t0=1.4))
    caveat = align_by_acquisition_start(run, cfg())["caveat"]
    assert "experiment harness" in caveat
    assert "not from anything the vehicles observed" in caveat
    assert "reported apart" in caveat


def test_it_is_not_simulator_time_because_each_clock_keeps_its_own_jitter():
    """Simulator time would erase the offsets the experiment exists to work
    against; this takes one constant and leaves everything else alone."""
    from cdf.fusion.contact_alignment import align_by_acquisition_start

    run = run_of(participant("A", [], t0=0.0), participant("B", [], t0=1.4))
    result = align_by_acquisition_start(run, cfg())
    assert result["scale"] == 1.0
    assert result["drift"]["estimated"] is False
    assert "own clock" in result["note"]
    # One offset per recorder, and nothing else transformed.
    assert set(result["offsets_s"]) == {"A", "B"}


def test_one_recorder_alone_cannot_be_aligned_to_anything():
    from cdf.fusion.contact_alignment import align_by_acquisition_start

    run = run_of(participant("A", [], t0=0.0))
    result = align_by_acquisition_start(run, cfg())
    assert result["status"] == "UNALIGNED_NO_SHARED_CONTACT"
    assert converters_of(result) == {}


# --- the offsets block the fusion machinery consumes ----------------------


def test_an_aligned_participant_gets_a_transform_with_scale_one():
    run = run_of(
        participant("A", [impact("A", 10.0, 4000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.0, 4050.0)], x=101.0, y=0.0),
    )
    offsets = align_by_contact(run, cfg())["offsets"]
    assert offsets["A"]["status"] == "ALIGNED"
    assert offsets["A"]["scale"] == 1.0
    assert offsets["A"]["drift_ppm"] is None


def test_an_unaligned_participant_gets_no_offset_rather_than_zero():
    """Defaulting to zero would silently align a recorder nobody could align."""
    run = run_of(
        participant("A", [impact("A", 10.0, 5000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.0, 5100.0)], x=103.0, y=0.0),
        participant("C", [impact("C", 4.0, 900.0)], x=-300.0, y=0.0),
    )
    offsets = align_by_contact(run, cfg())["offsets"]
    assert offsets["C"]["status"] == "UNRESOLVED"
    assert offsets["C"]["offset_s"] is None
    assert offsets["C"]["confidence"] == 0.0


def test_a_run_with_no_contact_leaves_every_transform_unresolved():
    run = run_of(participant("A", []), participant("B", []))
    offsets = align_by_contact(run, cfg())["offsets"]
    assert {v["status"] for v in offsets.values()} == {"UNRESOLVED"}


# --- telling an impact from resting contact -------------------------------


def test_resting_contact_after_an_impact_is_not_an_impact():
    """A real recording: one impact of 11 569 N*s, then 43 reports of 30-290 N*s
    twice a second for the rest of the run as the vehicles sat touching."""
    triggers = [impact("A", 6.17, 11569.0)]
    triggers += [
        impact("A", 6.87 + i * 0.55, 30.0 + (i * 37) % 260) for i in range(43)
    ]
    ev = participant("A", triggers, x=100.0, y=0.0, t1=30.0)
    anchors = contact_anchors(ev)
    assert [round(a.t_local, 2) for a in anchors] == [6.17]


def test_the_impulse_floor_is_relative_so_it_needs_no_scenario_scale():
    """A gentle scenario keeps its gentle impacts; the test is against its own peak."""
    gentle = participant("A", [
        impact("A", 6.0, 4000.0),
        impact("A", 9.0, 2400.0),     # 60% of the peak: a real second impact
        impact("A", 12.0, 90.0),      # 2% of the peak: contact, not impact
    ], x=100.0, y=0.0, t1=20.0)
    assert [round(a.impulse) for a in contact_anchors(gentle)] == [4000, 2400]


def test_a_sustained_contact_within_the_merge_window_is_one_impact():
    triggers = [impact("A", 6.00 + i * 0.05, 9000.0 + i) for i in range(6)]
    anchors = contact_anchors(participant("A", triggers, x=100.0, y=0.0))
    assert len(anchors) == 1
    assert anchors[0].t_local == pytest.approx(6.00)
    assert anchors[0].impulse == pytest.approx(9005.0)
    assert anchors[0].n_triggers == 6


def test_two_impacts_a_second_apart_stay_two():
    triggers = [impact("A", 6.0, 9000.0), impact("A", 7.5, 8000.0)]
    assert len(contact_anchors(participant("A", triggers, x=100.0, y=0.0))) == 2


# --- disagreeing pairings are not averaged -------------------------------


def test_pairings_that_disagree_use_the_better_one_rather_than_the_mean():
    """The failure this prevents, from a real recording: a true impact implied
    +0.267 s, a spurious pairing implied -0.083 s, and the median was +0.092 --
    a value neither piece of evidence supported."""
    run = run_of(
        participant("A", [impact("A", 6.174, 11569.0), impact("A", 11.323, 9200.0)],
                    x=100.0, y=0.0, t1=20.0),
        participant("B", [impact("B", 5.906, 11569.0), impact("B", 11.406, 7400.0)],
                    x=101.0, y=0.0, t1=20.0),
    )
    result = align_by_contact(run, cfg())
    pair = result["pairs"]["B->A"]
    assert pair["offsets_agree"] is False
    assert "one of them is wrong" in pair["estimator"]
    # The best-evidenced pairing is the exact-impulse one.
    assert pair["offset_s"] == pytest.approx(0.2674, abs=1e-3)


def test_pairings_that_agree_are_still_averaged():
    run = run_of(
        participant("A", [impact("A", 6.00, 9000.0), impact("A", 11.00, 8000.0)],
                    x=100.0, y=0.0, t1=20.0),
        participant("B", [impact("B", 5.90, 9050.0), impact("B", 10.92, 8050.0)],
                    x=101.0, y=0.0, t1=20.0),
    )
    pair = align_by_contact(run, cfg())["pairs"]["B->A"]
    assert pair["offsets_agree"] is True
    assert "agree" in pair["estimator"]
    assert pair["offset_s"] == pytest.approx(0.09, abs=0.01)


# --- one impact doing duty for two --------------------------------------


def test_an_anchor_used_by_two_links_is_flagged():
    """In a chain the middle vehicle often registers one impact, not two, so its
    single anchor relates both neighbours and the second offset is derived
    through a pairing of two different physical events.

    What this test asserted originally was an error *bound* on that offset. There
    is no such bound, and the number it checked was computed by subtracting two
    counterparties' timestamps from two different clocks -- see
    test_a_shared_anchor_reports_no_error_bound.
    """
    run = run_of(
        participant("A", [impact("A", 6.17, 11569.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 5.91, 11569.0)], x=101.0, y=0.0),
        participant("C", [impact("C", 6.19, 10321.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    caveats = result["shared_anchor_caveats"]
    assert caveats, "the middle recorder anchor is used by both links"
    entry = caveats[0]
    assert entry["n_impacts_this_recorder_registered"] == 1
    assert entry["participants_with_suspect_offset"] == ["C"]
    assert "did not register its second impact" in entry["reason"]


def test_a_recorder_with_its_own_anchor_per_link_is_not_flagged():
    """The clean chain: the middle vehicle registered both of its impacts."""
    run = run_of(
        participant("A", [impact("A", 10.00, 9000.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 8.00, 9050.0), impact("B", 9.00, 3000.0)],
                    x=103.0, y=0.0),
        participant("C", [impact("C", 12.50, 3050.0)], x=106.0, y=0.0),
    )
    assert align_by_contact(run, cfg())["shared_anchor_caveats"] == []


# --- the shared anchor reports no bound, because there is none -------------


def test_a_shared_anchor_reports_no_error_bound(monkeypatch):
    """An earlier version put a number here by subtracting two counterparties'
    local timestamps -- two readings from two different clocks, which is the
    error this module exists to correct. On a recorded chain it produced 13 ms
    for an offset that was out by 200 ms, and the reassuring small number was
    worse than no number at all.
    """
    run = run_of(
        participant("A", [impact("A", 6.174, 11569.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 5.906, 11569.0)], x=101.0, y=0.0),
        participant("C", [impact("C", 6.187, 10321.0)], x=102.0, y=0.0),
    )
    caveat = align_by_contact(run, cfg())["shared_anchor_caveats"][0]
    assert caveat["offset_error_bound_s"] is None
    assert caveat["error_bound_determinable"] is False
    assert "no measurement of when it happened" in caveat["reason"]


def test_impulse_agreement_identifies_which_pairing_is_the_suspect():
    """B's impulse matches A's exactly and C's only approximately, which is the
    evidence that B's single anchor is the A-B impact and not the B-C one."""
    run = run_of(
        participant("A", [impact("A", 6.174, 11569.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 5.906, 11569.0)], x=101.0, y=0.0),
        participant("C", [impact("C", 6.187, 10321.0)], x=102.0, y=0.0),
    )
    caveat = align_by_contact(run, cfg())["shared_anchor_caveats"][0]
    assert caveat["best_supported_pairing"]["participant"] == "A"
    assert caveat["best_supported_pairing"]["impulse_agreement"] == pytest.approx(1.0)
    assert [p["participant"] for p in caveat["weaker_pairings"]] == ["C"]
    assert caveat["participants_with_suspect_offset"] == ["C"]


def test_the_well_supported_offset_is_still_accurate():
    """The caveat is about the second pairing only. On the recorded chain the
    A-B offset was right to 0.1 ms and it is the C offset that is suspect."""
    run = run_of(
        participant("A", [impact("A", 6.174, 11569.0)], x=100.0, y=0.0),
        participant("B", [impact("B", 5.906, 11569.0)], x=101.0, y=0.0),
        participant("C", [impact("C", 6.187, 10321.0)], x=102.0, y=0.0),
    )
    result = align_by_contact(run, cfg())
    offsets = result["offsets_s"]
    assert offsets["A"] - offsets["B"] == pytest.approx(-0.268, abs=1e-3)


# --- a gentle collision is still a collision --------------------------------


def test_a_low_energy_impact_is_not_discarded_as_resting_contact():
    """The absolute impulse floor is a noise floor, not a resting-contact filter.

    It used to sit at 300 N*s, chosen because resting contact after a pile-up
    reports 30-290. But a real collision can land inside that band: the recorded
    all-way-stop merge measures 120.3 N*s, and at 300 the run reported that no
    recorder had felt a contact at all and fell through to the harness marker --
    a collision run presented as a no-collision run.

    Rejecting resting contact is what the *relative* test does, and it does it
    properly, on the ratio to the recorder's own peak.
    """
    ev = ParticipantEvidence(
        participant_id="A",
        telemetry=telemetry("A", 0.0, 10.0, 0.0, 0.0),
        triggers=[impact("A", 5.0, 120.3)],
    )
    assert [a.t_local for a in contact_anchors(ev)] == [5.0], (
        "a 120 N*s impact is the only contact this recorder felt, so it is that "
        "recorder's peak and cannot be resting contact"
    )


def test_resting_contact_beside_a_real_impact_is_still_rejected():
    """The case the floor was written for, and the relative test still catches it.

    On the recorded chain the resting reports were 30-290 N*s against a peak of
    11569 -- 0.003 to 0.025 of it, well under the 0.05 fraction.
    """
    ev = ParticipantEvidence(
        participant_id="B",
        telemetry=telemetry("B", 0.0, 20.0, 0.0, 0.0),
        triggers=[
            impact("B", 5.9, 11569.0),
            impact("B", 6.5, 290.0),
            impact("B", 7.1, 120.0),
            impact("B", 7.7, 30.0),
        ],
    )
    assert [a.t_local for a in contact_anchors(ev)] == [5.9], (
        "everything after the real impact is the vehicles still touching, and "
        "each is a hundredth of the momentum this recorder actually felt"
    )


def test_a_gentle_shared_impact_aligns_two_recorders():
    """End to end: the all-way-stop case that was dropping to the harness marker."""
    run = run_of(
        participant("A", [impact("A", 7.545511, 120.341)], x=-263.5, y=-10.9),
        participant("B", [impact("B", 7.420784, 120.341)], x=-265.3, y=-8.9),
    )
    result = align_by_contact(run, Config({}))
    assert result["status"] == "CONTACT_ALIGNED", result.get("reason")
    assert result["n_contact_anchors"] == 2
    assert result["offsets_s"]["B"] == pytest.approx(0.124727, abs=1e-6)
