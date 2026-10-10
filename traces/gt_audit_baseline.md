# Ground-truth audit (gt_audit_baseline), campaign

Privileged evaluation only.  Per-run details in each run's reconstruction/evaluation/gt_audit_baseline.md.

## All tracks, every sample

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 4761 | 0.86 | 2.02 | 3.27 | 3.59 | 5.28 |
| track point to true outline [m] | 4761 | 0.20 | 0.26 | 0.50 | 0.60 | 1.30 |
| speed error [m/s] | 4761 | 0.04 | 0.13 | 0.45 | 0.90 | 4.47 |
| velocity vector error [m/s] | 4761 | 0.06 | 0.21 | 0.76 | 1.25 | 10.36 |
| heading error [deg] | 1782 | 1.20 | 3.16 | 6.98 | 10.58 | 176.77 |

## Anonymous tracks only

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 1375 | 0.98 | 1.64 | 3.04 | 3.23 | 5.28 |
| track point to true outline [m] | 1375 | 0.28 | 0.26 | 0.49 | 0.59 | 1.30 |
| speed error [m/s] | 1375 | 0.07 | 0.16 | 0.57 | 1.21 | 4.47 |
| velocity vector error [m/s] | 1375 | 0.10 | 0.25 | 1.02 | 2.10 | 10.36 |
| heading error [deg] | 572 | 1.10 | 3.14 | 8.32 | 15.02 | 176.77 |

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

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
