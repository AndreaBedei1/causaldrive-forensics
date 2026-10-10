# Ground-truth audit (privileged, evaluation only): S01/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 120 | B | 1.000 | 0 | 0 | 0.55 / 0.69 | 0.08 / 0.22 | 0.2 / 0.9 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 120 | 0.55 | 0.14 | 0.68 | 0.69 | 0.71 |
| track point to true outline [m] | 120 | 0.38 | 0.20 | 0.59 | 0.60 | 0.62 |
| speed error [m/s] | 120 | 0.08 | 0.09 | 0.18 | 0.22 | 0.40 |
| velocity vector error [m/s] | 120 | 0.10 | 0.08 | 0.20 | 0.27 | 0.40 |
| heading error [deg] | 51 | 0.24 | 0.21 | 0.50 | 0.91 | 1.31 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 4.40 | PREDICTED_OVERLAP | 22.69 / 22.38 | 0.00 / 0.00 | 22.38 | 20.49 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 14394.111443951086, "reconstructed_as": "g14", "report_timing_error_s": 0.0, "sim_time": 19.773502379655838}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
