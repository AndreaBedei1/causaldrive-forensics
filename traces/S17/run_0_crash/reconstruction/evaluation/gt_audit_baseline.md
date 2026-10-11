# Ground-truth audit (privileged, evaluation only): S17/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 75 | C | 1.000 | 0 | 0 | 0.32 / 0.69 | 0.07 / 0.14 | 0.9 / 2.0 |
| A:track_002 | 110 | B | 1.000 | 0 | 0 | 1.87 / 3.68 | 0.09 / 0.72 | 1.3 / 4.7 |
| B:track_001 | 110 | A | 1.000 | 0 | 0 | 1.67 / 2.47 | 0.17 / 0.94 | 0.8 / 4.5 |
| B:track_002 | 58 | C | 1.000 | 0 | 0 | 1.89 / 2.67 | 0.38 / 1.02 | 1.4 / 5.3 |
| B:track_003 | 7 | C | 1.000 | 0 | 0 | 1.65 / 1.90 | 0.42 / 0.45 | 11.0 / 11.1 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 360 | 1.46 | 1.92 | 3.59 | 3.60 | 3.78 |
| track point to true outline [m] | 360 | 0.17 | 0.24 | 0.41 | 0.48 | 1.06 |
| speed error [m/s] | 360 | 0.11 | 0.28 | 0.71 | 0.90 | 2.10 |
| velocity vector error [m/s] | 360 | 0.23 | 0.38 | 1.04 | 1.35 | 2.14 |
| heading error [deg] | 259 | 1.07 | 1.08 | 4.23 | 5.43 | 11.13 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | C | 2.60 | UNSAFE_FORWARD_GAP | 3.31 / 3.19 | 0.89 / 0.40 | 3.49 | 16.83 |
| A | track_002 | B | 3.80 | PREDICTED_OVERLAP | -6.03 / -7.70 | 0.81 / 1.03 | 1.53 | 16.83 |
| B | track_001 | A | 4.15 | - | -1.95 / -1.50 | 0.55 / 0.71 | 1.42 | 18.66 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | C | 2.75 | CUT_IN_FROM_RIGHT | 0.56 / 0.05 | -1.79 / -1.90 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1576.923849978709, "reconstructed_as": "g20", "report_timing_error_s": 0.0, "sim_time": 19.25749884918332}
- extra reconstructed collisions: 0
- A:track_001: U1 (ANONYMOUS), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U1 (ANONYMOUS), true identity C
- B:track_003: U1 (ANONYMOUS), true identity C

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
