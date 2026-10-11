# Ground-truth audit (gt_audit_baseline), campaign

Privileged evaluation only.  Per-run details in each run's reconstruction/evaluation/gt_audit_baseline.md.

## All tracks, every sample

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 6663 | 0.77 | 1.62 | 3.24 | 3.55 | 5.28 |
| track point to true outline [m] | 6663 | 0.24 | 0.29 | 0.58 | 0.64 | 1.30 |
| speed error [m/s] | 6663 | 0.05 | 0.14 | 0.44 | 0.77 | 4.47 |
| velocity vector error [m/s] | 6663 | 0.09 | 0.25 | 0.69 | 1.15 | 10.36 |
| heading error [deg] | 3429 | 0.82 | 1.51 | 4.77 | 7.60 | 176.77 |

## Anonymous tracks only

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 1517 | 0.62 | 0.87 | 3.38 | 3.53 | 5.28 |
| track point to true outline [m] | 1517 | 0.46 | 0.33 | 0.66 | 0.69 | 1.30 |
| speed error [m/s] | 1517 | 0.06 | 0.11 | 0.29 | 0.56 | 4.47 |
| velocity vector error [m/s] | 1517 | 0.16 | 0.22 | 0.68 | 1.26 | 10.36 |
| heading error [deg] | 1415 | 0.58 | 0.93 | 2.71 | 5.15 | 176.77 |

## Runs

| run | tracks | impure (<95 %) | identity switches | centre err. median / p95 [m] | CRITICAL_TTC starts | CUT_IN starts |
|---|---|---|---|---|---|---|
| S01/run_0_crash | 1 | - | - | 0.55 / 0.69 | 1 | 0 |
| S02/run_0_crash | 1 | - | - | 0.36 / 0.54 | 1 | 1 |
| S02/run_0_critical_before_cut_in | 2 | - | - | 2.07 / 3.66 | 2 | 1 |
| S03/run_0_crash | 2 | - | - | 0.94 / 2.95 | 2 | 0 |
| S06/run_0_a_front_pushed | 2 | - | - | 0.31 / 1.03 | 2 | 0 |
| S06/run_0_b_rear_first | 2 | - | - | 0.23 / 0.52 | 2 | 0 |
| S07/run_0_crash | 2 | - | - | 0.29 / 0.46 | 2 | 0 |
| S08/run_0_crash | 6 | C:track_001, C:track_002 | C:track_001, C:track_002 | 0.95 / 2.94 | 2 | 0 |
| S09/run_0_merge_conflict | 2 | - | - | 3.55 / 3.84 | 2 | 0 |
| S10/run_0_rolls_through | 2 | - | - | 2.91 / 3.25 | 2 | 0 |
| S12/run_0_near_simultaneous | 2 | - | - | 1.03 / 1.71 | 2 | 0 |
| S15/run_0_deflected_into_c | 6 | B:track_001 | B:track_001 | 1.38 / 3.55 | 5 | 0 |
| S16/run_0_consequential | 7 | - | - | 0.71 / 3.06 | 3 | 1 |
| S17/run_0_crash | 5 | - | - | 1.46 / 3.60 | 3 | 1 |
| S18/run_0_abreast | 7 | A:track_001 | A:track_001, A:track_003 | 0.68 / 3.49 | 3 | 2 |
| S18/run_0_passing | 9 | A:track_001 | A:track_001 | 0.61 / 3.51 | 4 | 2 |
| S18/run_0_platoon | 9 | - | - | 0.73 / 3.52 | 3 | 0 |

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
