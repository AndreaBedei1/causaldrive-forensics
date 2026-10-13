# Scenario ID map

Scanned `configs/scenarios/`, `traces/`, `docs/` and the Git history (deleted scenario files).  Existing IDs are
never renumbered; an ID that existed and was removed is retired and never reused.

## In use

| ID | name | map | vehicles | recorders |
|---|---|---|--:|--:|
| S01 | rear_end | Town05 | 2 | 2 |
| S02 | cut_in | Town05 | 2 | 2 |
| S03 | crossing | Town05 | 2 | 2 |
| S06 | chain_collision | Town05 | 3 | 3 |
| S07 | occluded_chain_stop | Town05 | 3 | 3 |
| S08 | multidirection_crossing | Town05 | 3 | 3 |
| S09 | roundabout | Town03_Opt | 2 | 2 |
| S10 | single_stop_a | Town05 | 2 | 2 |
| S12 | all_way_stop | Town05 | 2 | 2 |
| S15 | intersection_pileup | Town05 | 3 | 3 |
| S16 | secondary_collision | Town05 | 3 | 3 |
| S17 | unobserved_causal_vehicle | Town05 | 3 | 2 |
| S18 | anonymous_pair | Town05 | 4 | 2 |

## Retired (existed, removed: not reused)

| ID | last file | removed in |
|---|---|---|
| S04 | `s04_crossing_braking.yaml` | `10ce287` 2026-10-02 "re-record the campaign without S04" |
| S05 | `s05_simultaneous_crossing.yaml` | `7cf8cda` 2026-10-03 (13-run campaign) |
| S11 | `s11_single_stop_b.yaml` | `7cf8cda` 2026-10-03 |
| S13 | `s13_disputed_lane_change.yaml` | `7cf8cda` 2026-10-03 |
| S14 | `s14_three_car_chain.yaml` | `cfb4b87` 2026-09-22 "Remove unused S14 scenario" |

`configs/default.yaml` still mentions S05 and S13 in a historical comment about a camera crash.

## New (this branch): S19 onwards

| ID | name | vehicles | recorders | intended single contact | raw run |
|---|---|--:|--:|---|---|
| S19 | dense_abreast | 9 | 2 (A, B) | A-B sideswipe, 7.75 s | `traces/S19/run_0` |
| S20 | dense_platoon | 10 | 2 | B rear-ends A, 7.45 s | `traces/S20/run_0` |
| S21 | dense_overtaking | 9 | 2 | A-B sideswipe while B passes, 6.75 s | `traces/S21/run_0` |
| S22 | occlusion_reappearance | 8 | 2 | A-B merging into one lane, 7.3 s | `traces/S22/run_0` |
| S23 | far_to_near | 8 | 2 | A-B after A swerves from C, 8.5 s | `traces/S23/run_0` |
| S24 | collision_ambiguity | 8 | 2 | A rear-ends B between C and D, 7.75 s | `traces/S24/run_0` |

Each was acquired once on a private CARLA 0.9.15 engine (Town05, three-lane one-way arterial, spawn 265) and
checked with `scripts/check_scenario_run.py` (ground truth, scenario check only): exactly one vehicle contact, no
contact with the road edge, no car standing without a crash.  Earlier trial recordings of the same IDs were
discarded before acceptance (fixes: observation window, secondary contacts, timing); accepted raw runs are
immutable.
