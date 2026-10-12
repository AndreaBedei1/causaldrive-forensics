# Ground-truth audit (privileged, evaluation only): S08/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 152 | C | 1.000 | 0 | 0 | 0.50 / 0.62 | 0.06 / 0.33 | 1.1 / 3.6 |
| A:track_002 | 131 | B | 1.000 | 0 | 0 | 0.42 / 0.91 | 0.01 / 0.90 | 1.7 / 17.2 |
| B:track_001 | 131 | C | 1.000 | 0 | 0 | 0.97 / 1.32 | 0.05 / 1.72 | 14.8 / 15.8 |
| B:track_002 | 131 | A | 1.000 | 0 | 0 | 2.93 / 2.96 | 0.02 / 1.27 | 1.8 / 11.5 |
| C:track_001 | 152 | A | 1.000 | 0 | 0 | 1.47 / 1.92 | 0.07 / 0.66 | 0.9 / 3.5 |
| C:track_002 | 131 | B | 1.000 | 0 | 0 | 1.64 / 1.98 | 0.24 / 1.93 | 1.4 / 15.4 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 828 | 0.96 | 1.20 | 2.93 | 2.94 | 2.99 |
| track point to true outline [m] | 828 | 0.19 | 0.24 | 0.45 | 0.48 | 0.88 |
| speed error [m/s] | 828 | 0.05 | 0.19 | 0.54 | 1.23 | 4.69 |
| velocity vector error [m/s] | 828 | 0.07 | 0.22 | 0.70 | 1.45 | 5.53 |
| heading error [deg] | 158 | 1.26 | 2.53 | 10.53 | 14.80 | 30.14 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_002 | B | 2.55 | - | 15.00 / 14.52 | 18.96 / 18.02 | 23.51 | 13.71 |
| B | track_002 | A | 2.60 | PREDICTED_OVERLAP | 17.08 / 17.54 | 14.67 / 13.83 | 22.71 | 18.36 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 12137.113644320716, "reconstructed_as": "g25", "report_timing_error_s": 0.0, "sim_time": 148.73758325725794}
- extra reconstructed collisions: 0
- A:track_001: C (ASSOCIATED), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- B:track_001: C (ASSOCIATED), true identity C
- B:track_002: A (ASSOCIATED), true identity A
- C:track_001: A (ASSOCIATED), true identity A
- C:track_002: B (ASSOCIATED), true identity B

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
