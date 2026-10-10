# Ground-truth audit (privileged, evaluation only): S12/run_0_near_simultaneous

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 104 | B | 1.000 | 0 | 0 | 1.02 / 1.21 | 0.10 / 1.23 | 7.3 / 17.6 |
| B:track_001 | 104 | A | 1.000 | 0 | 0 | 1.03 / 1.89 | 0.16 / 1.71 | 5.9 / 68.1 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 208 | 1.03 | 0.36 | 1.36 | 1.71 | 1.94 |
| track point to true outline [m] | 208 | 0.13 | 0.23 | 0.50 | 0.61 | 0.81 |
| speed error [m/s] | 208 | 0.13 | 0.44 | 1.09 | 1.57 | 3.21 |
| velocity vector error [m/s] | 208 | 0.15 | 0.79 | 1.47 | 1.80 | 3.33 |
| heading error [deg] | 64 | 6.32 | 3.97 | 13.46 | 42.70 | 89.20 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 5.90 | PREDICTED_OVERLAP | 4.08 / 4.46 | 12.41 / 12.02 | 13.21 | 6.95 |
| B | track_001 | A | 6.05 | - | 11.59 / 11.58 | 5.21 / 2.91 | 12.09 | 6.88 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 7661.461427344263, "reconstructed_as": "g37", "report_timing_error_s": 0.0, "sim_time": 192.76600752398372}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
