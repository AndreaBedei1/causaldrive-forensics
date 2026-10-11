# Ground-truth audit (privileged, evaluation only): S10/run_0_rolls_through

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 134 | B | 1.000 | 0 | 0 | 2.91 / 2.92 | 0.01 / 0.15 | 0.6 / 4.7 |
| B:track_001 | 133 | A | 1.000 | 0 | 0 | 3.20 / 3.25 | 0.04 / 1.95 | 12.5 / 40.0 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 267 | 2.91 | 0.29 | 3.25 | 3.25 | 3.44 |
| track point to true outline [m] | 267 | 0.09 | 0.18 | 0.53 | 0.55 | 0.91 |
| speed error [m/s] | 267 | 0.02 | 0.08 | 0.51 | 1.41 | 3.43 |
| velocity vector error [m/s] | 267 | 0.02 | 0.10 | 0.67 | 2.11 | 4.44 |
| heading error [deg] | 56 | 2.41 | 11.89 | 24.12 | 32.18 | 43.89 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 3.40 | PREDICTED_OVERLAP | 9.64 / 9.26 | 22.83 / 22.48 | 24.83 | 5.67 |
| B | track_001 | A | 3.60 | PREDICTED_OVERLAP | 21.01 / 21.47 | 8.15 / 6.00 | 22.49 | 13.67 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 12940.27486218852, "reconstructed_as": "g20", "report_timing_error_s": 0.0, "sim_time": 170.56541202962399}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
