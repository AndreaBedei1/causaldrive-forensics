# Ground-truth audit (privileged, evaluation only): S18/run_0_passing

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 103 | C | 0.670 | 1 | 0 | 0.32 / 0.92 | 0.06 / 0.36 | 0.6 / 11.7 |
| A:track_002 | 115 | B | 1.000 | 0 | 0 | 1.25 / 2.11 | 0.19 / 0.82 | 1.0 / 1.3 |
| A:track_003 | 34 | C | 1.000 | 0 | 0 | 0.14 / 0.29 | 0.01 / 0.03 | 0.5 / 2.9 |
| A:track_004 | 59 | D | 1.000 | 0 | 0 | 0.59 / 0.72 | 0.06 / 0.28 | 0.3 / 4.4 |
| B:track_001 | 115 | A | 1.000 | 0 | 0 | 1.50 / 2.02 | 0.19 / 0.82 | 0.8 / 2.1 |
| B:track_002 | 90 | C | 1.000 | 0 | 0 | 0.37 / 0.60 | 0.03 / 0.15 | 0.4 / 1.5 |
| B:track_003 | 51 | D | 1.000 | 0 | 0 | 0.62 / 0.86 | 0.07 / 0.25 | 0.5 / 1.8 |
| B:track_004 | 46 | C | 1.000 | 0 | 0 | 3.55 / 3.67 | 0.09 / 0.20 | 0.3 / 1.9 |
| B:track_005 | 28 | D | 1.000 | 0 | 0 | 0.82 / 0.90 | 0.14 / 0.28 | 1.1 / 1.7 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 641 | 0.61 | 1.00 | 2.02 | 3.51 | 3.67 |
| track point to true outline [m] | 641 | 0.39 | 0.36 | 0.64 | 0.67 | 0.74 |
| speed error [m/s] | 641 | 0.08 | 0.16 | 0.33 | 0.52 | 2.89 |
| velocity vector error [m/s] | 641 | 0.18 | 0.25 | 0.55 | 0.91 | 3.18 |
| heading error [deg] | 556 | 0.57 | 0.83 | 1.74 | 2.88 | 14.54 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_003 | C | 0.65 | - | 15.22 / 14.98 | 0.00 / 0.00 | 14.98 | 16.86 |
| A | track_001 | C | 2.60 | UNSAFE_FORWARD_GAP | 14.46 / 14.96 | 0.98 / 0.00 | 14.96 | 16.83 |
| A | track_002 | B | 5.15 | - | -5.20 / -6.37 | 0.92 / 1.03 | 1.53 | 16.89 |
| B | track_001 | A | 5.55 | - | -3.80 / -2.87 | 0.92 / 0.63 | 1.27 | 18.81 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | C | 3.00 | CUT_IN_FROM_RIGHT | 0.17 / 0.00 | -2.04 / 0.00 |
| A | track_001 | C | 9.90 | CUT_IN_FROM_RIGHT | 0.95 / 1.00 | -1.25 / -1.24 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1092.4276850565568, "reconstructed_as": "g30", "report_timing_error_s": 0.0, "sim_time": 519.1178570948541}
- extra reconstructed collisions: 0
- A:track_001: U1 (ANONYMOUS), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- A:track_003: U2 (ANONYMOUS), true identity C
- A:track_004: U3 (ANONYMOUS), true identity D
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U2 (ANONYMOUS), true identity C
- B:track_003: U3 (ANONYMOUS), true identity D
- B:track_004: U2 (ANONYMOUS), true identity C
- B:track_005: U3 (ANONYMOUS), true identity D

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
