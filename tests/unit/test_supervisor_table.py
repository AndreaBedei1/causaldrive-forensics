"""The per-scenario table, which is what a reader looks at first.

Every assertion here is about a cell saying what it actually knows. The failure
this table exists to prevent is a dash: "not run" and "found nothing" look
identical when gaps are filled in, and they are opposite findings.
"""

from __future__ import annotations

import pytest

from cdf.common.io import write_json
from cdf.common.layout import RunLayout
from cdf.evaluation.supervisor_table import (
    SUPERVISOR_COLUMNS,
    build_supervisor_rows,
    format_supervisor_table,
    write_supervisor_table,
)


def make_run(root, scenario="S10", variant="rolls_through", seed=0, **artifacts):
    run = root / "{0}_x".format(scenario) / "seed_{0:03d}_{1}".format(seed, variant)
    run.mkdir(parents=True, exist_ok=True)
    layout = RunLayout.from_run_dir(run)
    manifest = {
        "scenario_id": scenario, "variant": variant, "seed": seed,
        "outcome": artifacts.get("outcome", "collision"),
    }
    if artifacts.get("tick") is not None:
        manifest["fixed_delta_seconds"] = artifacts["tick"]
    write_json(layout.manifest, manifest)
    for name, payload in artifacts.items():
        if name in ("outcome", "tick") or payload is None:
            continue
        write_json(getattr(layout, name), payload)
    return layout


def one_row(root):
    rows = build_supervisor_rows(root)
    assert len(rows) == 1
    return rows[0]


# --- what happened --------------------------------------------------------


def test_the_collision_pairs_are_named(tmp_path):
    make_run(tmp_path, global_log={"rows": [
        {"event_type": "COLLISION", "participant": "A", "subject": "B"},
        {"event_type": "COLLISION", "participant": "B", "subject": "C"},
    ]})
    assert one_row(tmp_path)["what_happened"] == "collision: A-B, B-C"


def test_an_impact_with_no_counterparty_is_not_a_one_sided_pair(tmp_path):
    """Rendering it as a pair would read as a vehicle colliding with itself."""
    make_run(tmp_path, global_log={"rows": [
        {"event_type": "COLLISION", "participant": "A", "subject": "B"},
        {"event_type": "COLLISION", "participant": "C", "subject": ""},
    ]})
    happened = one_row(tmp_path)["what_happened"]
    assert "A-B" in happened
    assert "1 impact(s) with no counterparty resolved" in happened


def test_the_same_pair_reported_twice_is_named_once(tmp_path):
    make_run(tmp_path, global_log={"rows": [
        {"event_type": "COLLISION", "participant": "A", "subject": "B"},
        {"event_type": "COLLISION", "participant": "B", "subject": "A"},
    ]})
    assert one_row(tmp_path)["what_happened"] == "collision: A-B"


def test_a_run_without_a_merged_log_still_reports_its_outcome(tmp_path):
    make_run(tmp_path, outcome="near_miss")
    assert one_row(tmp_path)["what_happened"] == "near miss"


# --- every cell says what it knows ---------------------------------------


def test_an_unscored_run_says_not_scored_rather_than_zero(tmp_path):
    """A zero F1 is a method that recovered nothing; 'not scored' is a stage
    that never ran, and a table conflating them is worse than no table."""
    make_run(tmp_path)
    row = one_row(tmp_path)
    assert row["reconstructed"] == "not scored"
    assert row["clock_quality"] == "not fused"
    assert row["key_formal_violation"] == "not checked"
    assert row["physical_contributors"] == "not analysed"


def test_the_reconstruction_cell_reports_both_f1s(tmp_path):
    make_run(tmp_path, metrics={"observable_comparison": {"accounts": {
        "global_inferred": {
            "scored": True, "nodes": {"f1": 0.613}, "edges": {"f1": 0.358},
        },
    }}})
    assert one_row(tmp_path)["reconstructed"] == "nodes 0.61 / edges 0.36"


def test_the_clock_cell_names_the_method_not_only_the_status(tmp_path):
    """The harness marker must never read as a reconstruction result."""
    make_run(tmp_path, clock_alignment={
        "status": "ACQUISITION_START_ALIGNED",
        "method": "acquisition_start_marker",
        "offsets_s": {"A": 0.0, "B": 0.2},
    })
    row = one_row(tmp_path)
    assert row["clock_quality"] == "harness marker (not a reconstruction result)"
    assert row["clock_source"] == "harness marker (no contact, no radar)"


def test_the_clock_source_names_what_placed_each_vehicle(tmp_path):
    """A run status alone hides that one vehicle rests on a fitted trajectory
    while the others rest on a physical impact."""
    make_run(tmp_path, clock_alignment={
        "status": "HYBRID_ALIGNED", "method": "hybrid_contact_then_radar",
        "offsets_s": {"A": 0.0, "B": -0.08, "C": 0.27},
        "clock_sources": {"A": "REFERENCE", "B": "CONTACT", "C": "RADAR"},
        "contact_stage": {"n_shared_contacts": 1},
    })
    row = one_row(tmp_path)
    assert row["clock_source"] == "A=reference, B=contact, C=radar"
    assert "hybrid aligned" in row["clock_quality"]
    assert "1 shared contact" in row["clock_quality"]


def test_a_contact_aligned_run_says_how_many_contacts_it_rests_on(tmp_path):
    make_run(tmp_path, clock_alignment={
        "status": "MULTI_CONTACT_ALIGNED", "method": "shared_physical_contact",
        "offsets_s": {"A": 0.0}, "n_shared_contacts": 2,
    })
    assert one_row(tmp_path)["clock_quality"] == "multi contact aligned (2 shared contacts)"


def test_the_formal_cell_names_the_first_failure_and_counts_the_rest(tmp_path):
    make_run(tmp_path, formal_results={"results": [
        {"property_id": "P4", "title": "no acceleration into a critical conflict",
         "status": "FAIL", "vacuous": False},
        {"property_id": "P6", "title": "a solid line is not crossed",
         "status": "FAIL", "vacuous": False},
    ], "summary": {}})
    cell = one_row(tmp_path)["key_formal_violation"]
    assert cell.startswith("P4: no acceleration")
    assert "+1 more" in cell


def test_a_vacuous_property_is_not_a_violation(tmp_path):
    make_run(tmp_path, formal_results={"results": [
        {"property_id": "P1", "title": "stop", "status": "PASS", "vacuous": True},
    ], "summary": {}})
    assert one_row(tmp_path)["key_formal_violation"] == "none"


def test_undecided_properties_are_reported_beside_no_failure(tmp_path):
    make_run(tmp_path, formal_results={
        "results": [{"property_id": "P5", "title": "rest", "status": "UNKNOWN",
                     "vacuous": False}],
        "summary": {"n_unknown": 1},
    })
    assert one_row(tmp_path)["key_formal_violation"] == "none failed (1 undecided)"


# --- contributors ---------------------------------------------------------


def test_physical_and_responsibility_contributors_are_separate_columns(tmp_path):
    """A vehicle can be causally involved and have broken no rule."""
    make_run(tmp_path, responsibility_report={"findings": {
        "A": {"physical_causal_contributor": "yes",
              "responsibility_evidence": "partial", "but_for_contribution": {}},
        "B": {"physical_causal_contributor": "yes",
              "responsibility_evidence": "supported", "but_for_contribution": {}},
        "C": {"physical_causal_contributor": "no",
              "responsibility_evidence": "insufficient", "but_for_contribution": {}},
    }})
    row = one_row(tmp_path)
    assert row["physical_contributors"] == "A, B"
    assert row["responsibility_contributors"] == "B (A partial)"


def test_no_supported_contributor_is_said_in_words(tmp_path):
    make_run(tmp_path, responsibility_report={"findings": {
        "A": {"physical_causal_contributor": "no",
              "responsibility_evidence": "insufficient", "but_for_contribution": {}},
    }})
    assert one_row(tmp_path)["responsibility_contributors"] == "none supported"


def test_an_untested_counterfactual_is_not_a_negative_result(tmp_path):
    make_run(tmp_path, responsibility_report={"findings": {
        "A": {"physical_causal_contributor": "yes",
              "responsibility_evidence": "partial",
              "but_for_contribution": {"verdict": "not tested"}},
    }})
    assert one_row(tmp_path)["counterfactual_validation"] == "not tested"


def test_an_established_but_for_names_the_vehicle(tmp_path):
    make_run(tmp_path, responsibility_report={"findings": {
        "B": {"physical_causal_contributor": "yes",
              "responsibility_evidence": "supported",
              "but_for_contribution": {"verdict": "yes"}},
    }})
    assert one_row(tmp_path)["counterfactual_validation"] == "but-for established for B"


def test_replays_that_ruled_it_out_are_distinguished_from_replays_never_run(tmp_path):
    make_run(tmp_path, responsibility_report={"findings": {
        "B": {"physical_causal_contributor": "yes",
              "responsibility_evidence": "partial",
              "but_for_contribution": {"verdict": "no"}},
    }})
    assert one_row(tmp_path)["counterfactual_validation"] == "tested, none established"


# --- the limitation column is derived, not written ------------------------


def test_a_run_with_no_common_clock_says_so_first(tmp_path):
    """Ordered by severity: with no merged timeline nothing else in the row
    means much."""
    make_run(
        tmp_path,
        clock_alignment={"status": "UNALIGNED_NO_SHARED_CONTACT", "offsets_s": {}},
        formal_results={"results": [], "summary": {"n_unknown": 3}},
    )
    assert "never on one timeline" in one_row(tmp_path)["main_limitation"]


def test_a_harness_aligned_run_names_that_as_its_limitation(tmp_path):
    make_run(tmp_path, clock_alignment={
        "status": "ACQUISITION_START_ALIGNED",
        "method": "acquisition_start_marker",
        "offsets_s": {"A": 0.0, "B": 0.2},
    })
    assert "not from the vehicles" in one_row(tmp_path)["main_limitation"]


def test_an_ambiguous_contact_outranks_an_undecided_property(tmp_path):
    make_run(
        tmp_path,
        clock_alignment={"status": "AMBIGUOUS_CONTACT_MATCH",
                         "method": "shared_physical_contact",
                         "offsets_s": {"A": 0.0}},
        formal_results={"results": [], "summary": {"n_unknown": 2}},
    )
    assert "which impact is which" in one_row(tmp_path)["main_limitation"]


def test_a_shared_anchor_is_reported_when_nothing_worse_applies(tmp_path):
    """And it names the recorder, and does not offer a bound. The bound this cell
    used to promise was computed by subtracting two timestamps from two different
    clocks; it read 13 ms where the true error was 200 ms."""
    make_run(
        tmp_path,
        clock_alignment={
            "status": "MULTI_CONTACT_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": 0.0, "B": 0.2},
            "shared_anchor_caveats": [
                {"anchor": "B#0", "participants_with_suspect_offset": ["C"]}
            ],
        },
        perception_metrics={"scored": True, "signs": {"n_real": 0}},
        responsibility_report={"findings": {
            "A": {"physical_causal_contributor": "no",
                  "responsibility_evidence": "insufficient",
                  "but_for_contribution": {"verdict": "no"}},
        }},
        formal_results={"results": [], "summary": {}},
    )
    cell = one_row(tmp_path)["main_limitation"]
    assert "C's offset is out by the interval between two impacts" in cell
    assert "nothing recorded measures" in cell
    assert "bounded" not in cell


def test_a_shared_anchor_with_no_named_recorder_still_reads_as_a_sentence(tmp_path):
    make_run(
        tmp_path,
        clock_alignment={
            "status": "MULTI_CONTACT_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": 0.0, "B": 0.2},
            "shared_anchor_caveats": [{"anchor": "B#0"}],
        },
        perception_metrics={"scored": True, "signs": {"n_real": 0}},
        responsibility_report={"findings": {
            "A": {"physical_causal_contributor": "no",
                  "responsibility_evidence": "insufficient",
                  "but_for_contribution": {"verdict": "no"}},
        }},
        formal_results={"results": [], "summary": {}},
    )
    assert "one offset is out by" in one_row(tmp_path)["main_limitation"]


def test_a_clean_run_identifies_no_limitation(tmp_path):
    make_run(
        tmp_path,
        clock_alignment={"status": "MULTI_CONTACT_ALIGNED",
                         "method": "shared_physical_contact",
                         "offsets_s": {"A": 0.0, "B": 0.2}},
        perception_metrics={"scored": True, "signs": {"n_real": 0}},
        responsibility_report={"findings": {
            "A": {"physical_causal_contributor": "yes",
                  "responsibility_evidence": "supported",
                  "but_for_contribution": {"verdict": "yes"}},
        }},
        formal_results={"results": [], "summary": {}},
    )
    assert one_row(tmp_path)["main_limitation"] == "none identified"


# --- output ---------------------------------------------------------------


def test_every_row_has_every_column(tmp_path):
    make_run(tmp_path)
    row = one_row(tmp_path)
    for column in SUPERVISOR_COLUMNS:
        assert column in row, column


def test_rows_are_sorted_for_reading(tmp_path):
    make_run(tmp_path, scenario="S12", variant="b_arrives_first")
    make_run(tmp_path, scenario="S10", variant="rolls_through")
    make_run(tmp_path, scenario="S12", variant="a_arrives_first")
    rows = build_supervisor_rows(tmp_path)
    assert [(r["scenario"], r["variant"]) for r in rows] == [
        ("S10", "rolls_through"),
        ("S12", "a_arrives_first"),
        ("S12", "b_arrives_first"),
    ]


def test_an_empty_root_says_no_campaign_rather_than_rendering_a_blank_table(tmp_path):
    assert "no campaign has been recorded" in format_supervisor_table([])


def test_the_table_is_written_as_csv_and_markdown(tmp_path):
    make_run(tmp_path)
    out = tmp_path / "published"
    result = write_supervisor_table(tmp_path, publish_dir=out)
    assert result["n_rows"] == 1
    assert (out / "supervisor_table.csv").is_file()
    assert (out / "supervisor_table.md").is_file()
    text = (out / "supervisor_table.md").read_text(encoding="utf-8")
    assert "Generated from artifacts" in text
    assert "different findings" in text


# --- an order built on a suspect offset is not an order -------------------


def test_an_order_resting_on_a_shared_anchor_is_not_reported_as_established(tmp_path):
    """The middle vehicle of a chain often registers one impact, and its anchor
    then relates both neighbours, which leaves the third vehicle's whole timeline
    displaced. An order read off those timestamps is an artefact of the anchor,
    and this holds however far apart the impacts happen to land -- so the column
    must withhold the order rather than print one and mark it wrong."""
    make_run(
        tmp_path,
        global_log={"rows": [
            {"event_type": "COLLISION", "participant": "C", "subject": "B",
             "t_common": 5.625, "t_local": 5.906},
            {"event_type": "COLLISION", "participant": "A", "subject": "B",
             "t_common": 5.639, "t_local": 5.906},
        ]},
        observable_events={"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_peak": 5.95},
            {"event_type": "COLLISION", "participant_id": "B", "subject": "C",
             "t_peak": 6.15},
        ]},
        clock_alignment={
            "status": "MULTI_CONTACT_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": -0.267, "B": 0.0, "C": -0.281},
            "shared_anchor_caveats": [
                {"anchor": "B#0", "participants_with_suspect_offset": ["C"]}
            ],
        },
    )
    cell = one_row(tmp_path)["collision_order"]
    assert "order not established" in cell
    assert "C offset rests on a shared anchor" in cell
    # Both pairs are still named, so the reader knows what was reconstructed.
    assert "B-C" in cell and "A-B" in cell
    # But never as a sequence: the method did not establish one.
    assert "then A-B" not in cell
    # The reference is still shown, because the order was in fact knowable.
    assert "truth A-B then B-C" in cell


def test_impacts_closer_than_the_recording_resolution_are_not_ordered(tmp_path):
    """Sorting always yields an order, including for timestamps a microsecond
    apart. On the recorded chain the two impacts were reconstructed onto very
    nearly the same instant and a sort tie-break decided which came first; the
    column reported that tie as a confident wrong answer. Inside one tick the
    recording cannot separate them, so there is no order to be wrong about."""
    make_run(
        tmp_path,
        tick=0.05,
        global_log={"rows": [
            {"event_type": "COLLISION", "participant": "C", "subject": "B",
             "t_common": 5.906272},
            {"event_type": "COLLISION", "participant": "A", "subject": "B",
             "t_common": 5.906273},
        ]},
        observable_events={"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_peak": 5.95},
            {"event_type": "COLLISION", "participant_id": "B", "subject": "C",
             "t_peak": 6.15},
        ]},
    )
    cell = one_row(tmp_path)["collision_order"]
    assert "order not established" in cell
    assert "0.000 s apart" in cell
    assert "0.050 s recording resolution" in cell
    assert "then" not in cell.split("truth")[0]
    # The truth was 200 ms apart, which one tick could have resolved. Reporting
    # that gap is what tells a reader the limit was the alignment, not the tick.
    assert "truth A-B then B-C 0.200 s apart" in cell


def test_impacts_far_enough_apart_on_sound_offsets_keep_their_order(tmp_path):
    """The resolution rule must not swallow an order the method did establish."""
    make_run(
        tmp_path,
        tick=0.05,
        global_log={"rows": [
            {"event_type": "COLLISION", "participant": "A", "subject": "B",
             "t_common": 5.95},
            {"event_type": "COLLISION", "participant": "B", "subject": "C",
             "t_common": 6.15},
        ]},
        observable_events={"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_peak": 5.95},
            {"event_type": "COLLISION", "participant_id": "B", "subject": "C",
             "t_peak": 6.15},
        ]},
    )
    assert one_row(tmp_path)["collision_order"] == "A-B then B-C (correct)"


def test_a_resolvable_order_that_is_wrong_is_still_called_wrong(tmp_path):
    """Withholding an unresolvable order must not become a way of never being
    marked wrong. With sound offsets and a gap the recording can resolve, a
    reversed order is a reversed order."""
    make_run(
        tmp_path,
        tick=0.05,
        global_log={"rows": [
            {"event_type": "COLLISION", "participant": "B", "subject": "C",
             "t_common": 5.95},
            {"event_type": "COLLISION", "participant": "A", "subject": "B",
             "t_common": 6.15},
        ]},
        observable_events={"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_peak": 5.95},
            {"event_type": "COLLISION", "participant_id": "B", "subject": "C",
             "t_peak": 6.15},
        ]},
    )
    cell = one_row(tmp_path)["collision_order"]
    assert cell == "B-C then A-B (WRONG, truth A-B then B-C)"


def test_a_correct_order_on_sound_offsets_is_reported_plainly(tmp_path):
    make_run(
        tmp_path,
        global_log={"rows": [
            {"event_type": "COLLISION", "participant": "A", "subject": "B",
             "t_common": 5.95, "t_local": 5.95},
            {"event_type": "COLLISION", "participant": "B", "subject": "C",
             "t_common": 6.15, "t_local": 6.15},
        ]},
        observable_events={"events": [
            {"event_type": "COLLISION", "participant_id": "A", "subject": "B",
             "t_peak": 5.95},
            {"event_type": "COLLISION", "participant_id": "B", "subject": "C",
             "t_peak": 6.15},
        ]},
        clock_alignment={
            "status": "MULTI_CONTACT_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": 0.0, "B": 0.0, "C": 0.0},
        },
    )
    assert one_row(tmp_path)["collision_order"] == "A-B then B-C (correct)"


def test_a_single_impact_has_no_order_to_get_wrong(tmp_path):
    make_run(tmp_path, global_log={"rows": [
        {"event_type": "COLLISION", "participant": "A", "subject": "B",
         "t_common": 5.95, "t_local": 5.95},
    ]})
    assert one_row(tmp_path)["collision_order"] == "single impact (A-B)"


def test_a_run_with_no_impact_says_so(tmp_path):
    make_run(tmp_path, outcome="near_miss", global_log={"rows": []})
    assert one_row(tmp_path)["collision_order"] == "no impact"


def test_line_evidence_reports_what_the_lane_sensor_said(tmp_path):
    layout = make_run(tmp_path)
    layout.perception_dir("A").mkdir(parents=True, exist_ok=True)
    write_json(layout.lane_events("A"), {"events": [
        {"event_type": "SOLID_LINE_CROSSED", "participant_id": "A"},
        {"event_type": "LANE_MARKING_CROSSED", "participant_id": "A"},
    ]})
    cell = one_row(tmp_path)["line_evidence"]
    assert "solid line x1" in cell
    assert "lane marking x1" in cell


def test_no_lane_sensor_is_distinguished_from_no_crossing(tmp_path):
    """A zero would read as a vehicle that crossed nothing."""
    make_run(tmp_path)
    assert one_row(tmp_path)["line_evidence"] == "no lane sensor"


def test_a_lane_sensor_that_saw_nothing_says_that_instead(tmp_path):
    layout = make_run(tmp_path)
    layout.perception_dir("A").mkdir(parents=True, exist_ok=True)
    write_json(layout.lane_events("A"), {"events": []})
    assert one_row(tmp_path)["line_evidence"] == "no crossing reported"


def test_the_limitation_names_the_recorder_that_could_not_be_tied_in(tmp_path):
    """"At least one recorder" is not actionable. A run missing the vehicle that
    initiated the incident is a different matter from one missing a bystander,
    and contact-based alignment drops any vehicle that never touched anything."""
    make_run(
        tmp_path,
        clock_alignment={
            "status": "PARTIALLY_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": 0.0, "B": 0.0},
            "unaligned_participants": ["C"],
        },
    )
    cell = one_row(tmp_path)["main_limitation"]
    assert cell.startswith("C could not be tied to the others")
    assert "nothing it recorded reaches the merged timeline" in cell


def test_a_partial_alignment_with_no_names_still_reads_as_a_sentence(tmp_path):
    make_run(
        tmp_path,
        clock_alignment={
            "status": "PARTIALLY_ALIGNED", "method": "shared_physical_contact",
            "offsets_s": {"A": 0.0},
        },
    )
    assert "a recorder could not be tied" in one_row(tmp_path)["main_limitation"]
