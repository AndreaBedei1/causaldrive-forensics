# Ground-truth audit (privileged, evaluation only): S09/run_0_merge_conflict

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 206 | B | 1.000 | 0 | 0 | 3.81 / 3.85 | 0.06 / 1.00 | 1.8 / 7.6 |
| B:track_001 | 208 | A | 1.000 | 0 | 0 | 3.54 / 3.55 | 0.01 / 0.81 | 2.8 / 6.2 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 414 | 3.55 | 2.74 | 3.83 | 3.84 | 3.86 |
| track point to true outline [m] | 414 | 0.30 | 0.21 | 0.64 | 0.83 | 1.06 |
| speed error [m/s] | 414 | 0.03 | 0.14 | 0.39 | 0.95 | 2.14 |
| velocity vector error [m/s] | 414 | 0.04 | 0.21 | 0.62 | 1.14 | 2.14 |
| heading error [deg] | 166 | 2.30 | 2.34 | 5.11 | 6.53 | 8.57 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 6.90 | PREDICTED_OVERLAP | 22.22 / 22.12 | 10.40 / 9.58 | 24.66 | 10.33 |
| B | track_001 | A | 6.65 | - | 24.10 / 22.79 | 15.41 / 14.73 | 28.08 | 10.31 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1904.842293204932, "reconstructed_as": "g17", "report_timing_error_s": 0.0, "sim_time": 24.25629462301731}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
