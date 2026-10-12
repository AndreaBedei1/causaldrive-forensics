# Ground-truth audit (privileged, evaluation only): S16/run_0_consequential

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 120 | C | 1.000 | 0 | 0 | 0.72 / 1.01 | 0.06 / 0.39 | 1.2 / 4.9 |
| A:track_002 | 67 | C | 1.000 | 0 | 0 | 1.62 / 2.34 | 0.09 / 0.18 | 0.2 / 2.1 |
| B:track_001 | 120 | A | 1.000 | 0 | 0 | 0.42 / 0.70 | 0.07 / 0.45 | 0.2 / 4.3 |
| B:track_002 | 120 | C | 1.000 | 0 | 0 | 0.79 / 1.61 | 0.07 / 0.32 | 1.6 / 5.3 |
| B:track_003 | 47 | C | 1.000 | 0 | 0 | 2.30 / 3.38 | 0.11 / 0.84 | 1.3 / 9.1 |
| B:track_004 | 4 | C | 1.000 | 0 | 0 | 3.32 / 3.40 | 0.41 / 0.53 | 7.6 / 7.7 |
| C:track_001 | 38 | A | 1.000 | 0 | 0 | 0.99 / 1.70 | 0.17 / 0.38 | 2.6 / 3.8 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 516 | 0.73 | 0.84 | 1.98 | 2.38 | 3.48 |
| track point to true outline [m] | 516 | 0.21 | 0.20 | 0.48 | 0.66 | 0.96 |
| speed error [m/s] | 516 | 0.09 | 0.13 | 0.28 | 0.44 | 2.12 |
| velocity vector error [m/s] | 516 | 0.13 | 0.27 | 0.68 | 0.97 | 2.31 |
| heading error [deg] | 378 | 0.96 | 2.39 | 4.18 | 6.28 | 9.86 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | C | 5.20 | UNSAFE_FORWARD_GAP | 1.27 / 1.30 | 0.48 / 0.10 | 1.65 | 10.22 |
| A | track_002 | C | 5.55 | - | 3.48 / 1.49 | 0.00 / 0.00 | 1.58 | 10.60 |
| B | track_001 | A | 0.50 | UNSAFE_FORWARD_GAP | 7.16 / 6.95 | 0.00 / 0.00 | 6.95 | 18.11 |
| C | track_001 | A | 5.60 | PREDICTED_OVERLAP | -11.66 / -11.38 | 1.36 / 0.11 | 1.46 | 11.72 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | C | 5.45 | CUT_IN_FROM_LEFT | 0.06 / 0.00 | 0.98 / 1.02 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 4243.514729638987, "reconstructed_as": "g32", "report_timing_error_s": 0.0, "sim_time": 229.82582645490766}
- {"participants": ["A", "C"], "participants_correct": true, "peak_impulse": 322.104643689845, "reconstructed_as": "g49", "report_timing_error_s": 0.0, "sim_time": 230.87582647055387}
- extra reconstructed collisions: 0
- A:track_001: C (ASSOCIATED), true identity C
- A:track_002: C (ASSOCIATED), true identity C
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: C (ASSOCIATED), true identity C
- B:track_003: C (ASSOCIATED), true identity C
- B:track_004: U1 (ANONYMOUS), true identity C
- C:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.
