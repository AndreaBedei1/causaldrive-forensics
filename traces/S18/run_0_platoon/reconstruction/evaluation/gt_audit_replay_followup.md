# Ground-truth audit (privileged, evaluation only): S18/run_0_platoon

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 106 | D | 1.000 | 0 | 0 | 0.26 / 0.63 | 0.03 / 0.16 | 0.3 / 2.3 |
| A:track_002 | 115 | B | 1.000 | 0 | 0 | 1.25 / 2.12 | 0.20 / 0.82 | 1.0 / 1.3 |
| A:track_003 | 15 | D | 1.000 | 0 | 0 | 3.49 / 3.55 | 0.03 / 0.13 | 2.0 / 2.7 |
| A:track_004 | 37 | C | 1.000 | 0 | 0 | 1.10 / 1.21 | 0.04 / 0.33 | 0.6 / 4.2 |
| B:track_001 | 115 | A | 1.000 | 0 | 0 | 1.52 / 2.06 | 0.20 / 0.82 | 0.8 / 2.3 |
| B:track_002 | 90 | D | 1.000 | 0 | 0 | 0.37 / 0.50 | 0.05 / 0.10 | 0.6 / 2.4 |
| B:track_003 | 46 | C | 1.000 | 0 | 0 | 0.87 / 1.02 | 0.04 / 0.16 | 0.7 / 2.1 |
| B:track_004 | 96 | D | 1.000 | 0 | 0 | 2.25 / 2.99 | 0.10 / 0.35 | 1.0 / 2.3 |
| B:track_005 | 21 | C | 1.000 | 0 | 0 | 0.66 / 0.73 | 0.01 / 0.21 | 0.5 / 1.9 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 641 | 0.85 | 1.65 | 2.21 | 2.87 | 3.56 |
| track point to true outline [m] | 641 | 0.30 | 0.19 | 0.55 | 0.63 | 1.07 |
| speed error [m/s] | 641 | 0.07 | 0.16 | 0.33 | 0.49 | 2.87 |
| velocity vector error [m/s] | 641 | 0.20 | 0.25 | 0.55 | 0.76 | 2.87 |
| heading error [deg] | 556 | 0.72 | 0.93 | 1.86 | 2.47 | 5.94 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | D | 0.50 | UNSAFE_FORWARD_GAP | 13.37 / 13.16 | 0.00 / 0.00 | 13.16 | 16.87 |
| A | track_002 | B | 5.15 | - | -5.21 / -6.38 | 0.93 / 1.03 | 1.53 | 16.89 |
| B | track_001 | A | 5.55 | - | -3.79 / -2.87 | 0.92 / 0.63 | 1.27 | 18.81 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1097.5294421779033, "reconstructed_as": "g24", "report_timing_error_s": 0.0, "sim_time": 503.78820499777794}
- extra reconstructed collisions: 0
- A:track_001: U1 (ANONYMOUS), true identity D
- A:track_002: B (ASSOCIATED), true identity B
- A:track_003: U2 (ANONYMOUS), true identity D
- A:track_004: U4 (ANONYMOUS), true identity C
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U1 (ANONYMOUS), true identity D
- B:track_003: U3 (ANONYMOUS), true identity C
- B:track_004: U1 (ANONYMOUS), true identity D
- B:track_005: U4 (ANONYMOUS), true identity C

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.
