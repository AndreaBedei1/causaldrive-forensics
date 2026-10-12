# Ground-truth audit (privileged, evaluation only): S15/run_0_deflected_into_c

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 140 | C | 1.000 | 0 | 0 | 3.53 / 3.59 | 0.01 / 0.55 | 1.8 / 8.8 |
| A:track_002 | 119 | B | 1.000 | 0 | 0 | 2.79 / 2.83 | 0.04 / 1.85 | 5.2 / 8.6 |
| B:track_001 | 123 | C | 0.968 | 2 | 0 | 2.78 / 3.04 | 0.04 / 1.52 | 4.4 / 176.9 |
| B:track_002 | 120 | A | 1.000 | 0 | 0 | 0.46 / 1.09 | 0.05 / 1.03 | 5.1 / 21.3 |
| C:track_001 | 140 | A | 1.000 | 0 | 0 | 0.55 / 0.60 | 0.01 / 0.28 | 1.3 / 11.7 |
| C:track_002 | 138 | B | 1.000 | 0 | 0 | 2.42 / 2.58 | 0.07 / 1.78 | 2.2 / 5.2 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 780 | 1.30 | 2.25 | 3.53 | 3.54 | 4.95 |
| track point to true outline [m] | 780 | 0.18 | 0.31 | 0.46 | 0.53 | 0.96 |
| speed error [m/s] | 780 | 0.03 | 0.16 | 0.67 | 1.21 | 3.48 |
| velocity vector error [m/s] | 780 | 0.05 | 0.30 | 1.00 | 1.70 | 7.76 |
| heading error [deg] | 216 | 3.09 | 4.65 | 10.87 | 18.08 | 179.25 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_002 | B | 2.55 | - | 17.43 / 17.01 | 9.49 / 8.55 | 19.36 | 15.43 |
| A | track_001 | C | 3.75 | - | 10.97 / 10.04 | 1.08 / 1.00 | 10.14 | 15.42 |
| B | track_002 | A | 2.50 | PREDICTED_OVERLAP | 11.81 / 11.64 | 16.17 / 15.72 | 20.16 | 13.56 |
| C | track_001 | A | 3.75 | - | 10.90 / 10.04 | 0.68 / 0.92 | 10.14 | 7.28 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 10358.219383413683, "reconstructed_as": "g32", "report_timing_error_s": 0.0, "sim_time": 208.04685569182038}
- {"participants": ["A", "C"], "participants_correct": true, "peak_impulse": 1880.322026192424, "reconstructed_as": "g47", "report_timing_error_s": 0.0, "sim_time": 208.94685570523143}
- extra reconstructed collisions: 0
- A:track_001: C (ASSOCIATED), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- B:track_001: C (ASSOCIATED), true identity C
- B:track_002: A (ASSOCIATED), true identity A
- C:track_001: A (ASSOCIATED), true identity A
- C:track_002: B (ASSOCIATED), true identity B

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
