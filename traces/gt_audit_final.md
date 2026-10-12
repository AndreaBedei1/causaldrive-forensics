# Ground-truth audit (gt_audit_final), campaign

Privileged evaluation only.  Per-run details in each run's reconstruction/evaluation/gt_audit_final.md.

## All tracks, every sample

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 6960 | 0.79 | 1.60 | 2.94 | 3.55 | 4.95 |
| track point to true outline [m] | 6960 | 0.24 | 0.30 | 0.55 | 0.62 | 1.07 |
| speed error [m/s] | 6960 | 0.05 | 0.15 | 0.43 | 0.76 | 4.69 |
| velocity vector error [m/s] | 6960 | 0.09 | 0.25 | 0.67 | 1.09 | 7.76 |
| heading error [deg] | 3555 | 0.81 | 1.47 | 4.46 | 7.39 | 179.25 |

## Anonymous tracks only

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 1470 | 0.57 | 1.07 | 2.40 | 2.84 | 3.56 |
| track point to true outline [m] | 1470 | 0.44 | 0.27 | 0.64 | 0.70 | 1.07 |
| speed error [m/s] | 1470 | 0.07 | 0.11 | 0.26 | 0.41 | 1.12 |
| velocity vector error [m/s] | 1470 | 0.16 | 0.22 | 0.61 | 0.94 | 3.64 |
| heading error [deg] | 1470 | 0.57 | 0.97 | 2.47 | 3.93 | 16.83 |

## Runs

| run | tracks | impure (<95 %) | identity switches | centre err. median / p95 [m] | CRITICAL_TTC starts | CUT_IN starts |
|---|---|---|---|---|---|---|
| S01/run_0_crash | 1 | - | - | 0.55 / 0.69 | 1 | 0 |
| S02/run_0_crash | 1 | - | - | 0.31 / 0.65 | 1 | 1 |
| S02/run_0_critical_before_cut_in | 2 | - | - | 2.07 / 3.66 | 2 | 1 |
| S03/run_0_crash | 2 | - | - | 0.94 / 2.95 | 2 | 0 |
| S06/run_0_a_front_pushed | 2 | - | - | 0.31 / 1.03 | 2 | 0 |
| S06/run_0_b_rear_first | 2 | - | - | 0.23 / 0.52 | 2 | 0 |
| S07/run_0_crash | 2 | - | - | 0.29 / 0.46 | 2 | 0 |
| S08/run_0_crash | 6 | - | - | 0.96 / 2.94 | 2 | 0 |
| S09/run_0_merge_conflict | 2 | - | - | 3.55 / 3.84 | 2 | 0 |
| S10/run_0_rolls_through | 2 | - | - | 2.91 / 3.25 | 2 | 0 |
| S12/run_0_near_simultaneous | 4 | - | - | 1.18 / 1.93 | 2 | 0 |
| S15/run_0_deflected_into_c | 6 | - | B:track_001 | 1.30 / 3.54 | 4 | 0 |
| S16/run_0_consequential | 7 | - | - | 0.73 / 2.38 | 4 | 0 |
| S17/run_0_crash | 5 | - | - | 1.46 / 3.60 | 3 | 2 |
| S18/run_0_abreast | 9 | A:track_001#segment_2 | A:track_001#segment_2, A:track_003 | 0.72 / 2.70 | 3 | 1 |
| S18/run_0_passing | 8 | - | - | 0.57 / 2.45 | 3 | 1 |
| S18/run_0_platoon | 9 | - | - | 0.85 / 2.87 | 3 | 0 |

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
