# Ground-truth audit (gt_audit_replay_followup), campaign

Privileged evaluation only.  Per-run details in each run's reconstruction/evaluation/gt_audit_replay_followup.md.

## All tracks, every sample

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 4289 | 0.74 | 1.46 | 2.78 | 2.94 | 4.95 |
| track point to true outline [m] | 4289 | 0.28 | 0.31 | 0.57 | 0.63 | 1.07 |
| speed error [m/s] | 4289 | 0.07 | 0.17 | 0.43 | 0.72 | 4.69 |
| velocity vector error [m/s] | 4289 | 0.13 | 0.27 | 0.68 | 1.02 | 7.76 |
| heading error [deg] | 2568 | 0.77 | 1.13 | 3.49 | 5.78 | 179.25 |

## Anonymous tracks only

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 1330 | 0.56 | 0.80 | 2.43 | 2.86 | 3.56 |
| track point to true outline [m] | 1330 | 0.45 | 0.26 | 0.64 | 0.70 | 1.07 |
| speed error [m/s] | 1330 | 0.07 | 0.11 | 0.24 | 0.33 | 0.97 |
| velocity vector error [m/s] | 1330 | 0.16 | 0.21 | 0.54 | 0.77 | 3.64 |
| heading error [deg] | 1330 | 0.53 | 0.91 | 2.27 | 3.20 | 16.83 |

## Runs

| run | tracks | impure (<95 %) | identity switches | centre err. median / p95 [m] | CRITICAL_TTC starts | CUT_IN starts |
|---|---|---|---|---|---|---|
| S02/run_0_crash | 1 | - | - | 0.31 / 0.65 | 1 | 1 |
| S08/run_0_crash | 6 | - | - | 0.96 / 2.94 | 2 | 0 |
| S15/run_0_deflected_into_c | 6 | - | B:track_001 | 1.30 / 3.54 | 4 | 0 |
| S16/run_0_consequential | 7 | - | - | 0.73 / 2.38 | 4 | 1 |
| S18/run_0_abreast | 9 | A:track_001#segment_2 | A:track_001#segment_2, A:track_003 | 0.72 / 2.70 | 3 | 1 |
| S18/run_0_passing | 8 | - | - | 0.57 / 2.45 | 3 | 1 |
| S18/run_0_platoon | 9 | - | - | 0.85 / 2.87 | 3 | 0 |

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.
