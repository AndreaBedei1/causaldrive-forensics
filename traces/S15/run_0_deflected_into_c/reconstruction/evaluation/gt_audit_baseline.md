# Ground-truth audit (privileged, evaluation only): S15/run_0_deflected_into_c

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 140 | C | 1.000 | 0 | 0 | 3.53 / 3.59 | 0.01 / 0.55 | 1.8 / 8.8 |
| A:track_002 | 119 | B | 1.000 | 0 | 0 | 2.79 / 2.83 | 0.04 / 1.85 | 5.2 / 8.6 |
| B:track_001 | 123 | A | 0.764 | 1 | 0 | 1.38 / 2.12 | 0.10 / 1.94 | 4.0 / 164.4 |
| B:track_002 | 36 | A | 1.000 | 0 | 0 | 0.67 / 1.56 | 0.40 / 2.40 | 4.6 / 19.9 |
| C:track_001 | 140 | A | 1.000 | 0 | 0 | 0.55 / 0.60 | 0.01 / 0.28 | 1.3 / 11.7 |
| C:track_002 | 138 | B | 1.000 | 0 | 0 | 2.42 / 2.58 | 0.07 / 1.78 | 2.2 / 5.2 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 696 | 1.38 | 2.20 | 3.53 | 3.55 | 5.28 |
| track point to true outline [m] | 696 | 0.21 | 0.33 | 0.49 | 0.64 | 1.30 |
| speed error [m/s] | 696 | 0.04 | 0.21 | 0.67 | 1.34 | 3.83 |
| velocity vector error [m/s] | 696 | 0.06 | 0.38 | 1.06 | 1.92 | 10.36 |
| heading error [deg] | 216 | 2.87 | 4.47 | 11.65 | 19.53 | 176.77 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_002 | B | 2.55 | - | 17.43 / 17.01 | 9.49 / 8.55 | 19.36 | 15.43 |
| A | track_001 | C | 3.75 | - | 10.97 / 10.04 | 1.08 / 1.00 | 10.14 | 15.42 |
| B | track_002 | A | 2.50 | PREDICTED_OVERLAP | 11.81 / 11.64 | 16.19 / 15.72 | 20.16 | 13.56 |
| B | track_001 | A | 3.95 | - | 0.08 / 0.20 | 7.77 / 0.00 | 0.21 | 2.00 |
| C | track_001 | A | 3.75 | - | 10.90 / 10.04 | 0.68 / 0.92 | 10.14 | 7.28 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 10358.219383413683, "reconstructed_as": "g31", "report_timing_error_s": 0.0, "sim_time": 208.04685569182038}
- {"participants": ["A", "C"], "participants_correct": true, "peak_impulse": 1880.322026192424, "reconstructed_as": "g46", "report_timing_error_s": 0.0, "sim_time": 208.94685570523143}
- extra reconstructed collisions: 0
- A:track_001: C (ASSOCIATED), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- B:track_001: B:track_001 (ANONYMOUS), true identity A
- B:track_002: A (ASSOCIATED), true identity A
- C:track_001: A (ASSOCIATED), true identity A
- C:track_002: C:track_002 (ANONYMOUS), true identity B

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
