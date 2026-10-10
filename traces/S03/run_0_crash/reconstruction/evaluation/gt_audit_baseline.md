# Ground-truth audit (privileged, evaluation only): S03/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 131 | B | 1.000 | 0 | 0 | 0.42 / 0.91 | 0.01 / 0.90 | 1.7 / 17.2 |
| B:track_001 | 131 | A | 1.000 | 0 | 0 | 2.93 / 2.96 | 0.02 / 1.27 | 1.8 / 11.5 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 262 | 0.94 | 2.51 | 2.94 | 2.95 | 2.97 |
| track point to true outline [m] | 262 | 0.10 | 0.09 | 0.18 | 0.33 | 0.71 |
| speed error [m/s] | 262 | 0.02 | 0.12 | 0.47 | 1.10 | 2.74 |
| velocity vector error [m/s] | 262 | 0.02 | 0.16 | 0.70 | 1.49 | 2.75 |
| heading error [deg] | 51 | 1.74 | 4.89 | 10.57 | 15.73 | 28.85 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 2.55 | - | 15.00 / 14.52 | 18.96 / 18.02 | 23.51 | 13.71 |
| B | track_001 | A | 2.60 | PREDICTED_OVERLAP | 17.08 / 17.54 | 14.67 / 13.83 | 22.71 | 18.36 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 12137.594220167219, "reconstructed_as": "g11", "report_timing_error_s": 0.0, "sim_time": 72.69340289756656}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
