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

Allocated in `docs/FINAL_UNCERTAINTY_HARDENING_REPORT.md` and in each `configs/scenarios/s19..._*.yaml`.
