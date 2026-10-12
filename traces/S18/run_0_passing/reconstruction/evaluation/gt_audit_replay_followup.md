# Ground-truth audit (privileged, evaluation only): S18/run_0_passing

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 98 | D | 1.000 | 0 | 0 | 0.43 / 0.66 | 0.04 / 0.21 | 0.4 / 2.0 |
| A:track_002 | 115 | B | 1.000 | 0 | 0 | 1.25 / 2.11 | 0.19 / 0.82 | 1.0 / 1.3 |
| A:track_003 | 101 | C | 1.000 | 0 | 0 | 0.23 / 0.73 | 0.03 / 0.18 | 0.3 / 1.4 |
| B:track_001 | 115 | A | 1.000 | 0 | 0 | 1.50 / 2.02 | 0.19 / 0.82 | 0.8 / 2.1 |
| B:track_002 | 90 | C | 1.000 | 0 | 0 | 0.40 / 0.53 | 0.03 / 0.12 | 0.4 / 1.3 |
| B:track_003 | 51 | D | 1.000 | 0 | 0 | 0.62 / 0.86 | 0.07 / 0.25 | 0.5 / 1.7 |
| B:track_004 | 81 | C | 1.000 | 0 | 0 | 2.40 / 3.02 | 0.18 / 0.42 | 0.8 / 3.6 |
| B:track_005 | 23 | D | 1.000 | 0 | 0 | 0.75 / 0.90 | 0.17 / 0.23 | 0.9 / 2.9 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 674 | 0.57 | 1.40 | 2.05 | 2.45 | 3.03 |
| track point to true outline [m] | 674 | 0.40 | 0.29 | 0.61 | 0.65 | 0.95 |
| speed error [m/s] | 674 | 0.08 | 0.17 | 0.33 | 0.49 | 2.89 |
| velocity vector error [m/s] | 674 | 0.16 | 0.24 | 0.53 | 0.73 | 2.89 |
| heading error [deg] | 589 | 0.52 | 0.82 | 1.53 | 2.52 | 5.18 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_003 | C | 0.65 | - | 15.26 / 14.98 | 0.00 / 0.00 | 14.98 | 16.86 |
| A | track_002 | B | 5.15 | - | -5.20 / -6.37 | 0.92 / 1.03 | 1.53 | 16.89 |
| B | track_001 | A | 5.55 | - | -3.80 / -2.87 | 0.92 / 0.63 | 1.27 | 18.81 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_003 | C | 9.90 | CUT_IN_FROM_RIGHT | 0.95 / 1.00 | -1.25 / -1.24 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1092.4276850565568, "reconstructed_as": "g22", "report_timing_error_s": 0.0, "sim_time": 519.1178570948541}
- extra reconstructed collisions: 0
- A:track_001: U1 (ANONYMOUS), true identity D
- A:track_002: B (ASSOCIATED), true identity B
- A:track_003: U2 (ANONYMOUS), true identity C
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U2 (ANONYMOUS), true identity C
- B:track_003: U1 (ANONYMOUS), true identity D
- B:track_004: U2 (ANONYMOUS), true identity C
- B:track_005: U1 (ANONYMOUS), true identity D

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.
