# Ground-truth audit (privileged, evaluation only): S07/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 137 | B | 1.000 | 0 | 0 | 0.32 / 0.47 | 0.02 / 0.15 | 0.2 / 1.1 |
| B:track_001 | 137 | C | 1.000 | 0 | 0 | 0.21 / 0.34 | 0.04 / 0.12 | 0.1 / 0.5 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 274 | 0.29 | 0.12 | 0.42 | 0.46 | 0.49 |
| track point to true outline [m] | 274 | 0.35 | 0.31 | 0.49 | 0.50 | 0.52 |
| speed error [m/s] | 274 | 0.03 | 0.05 | 0.11 | 0.14 | 0.51 |
| velocity vector error [m/s] | 274 | 0.04 | 0.06 | 0.14 | 0.18 | 0.51 |
| heading error [deg] | 91 | 0.15 | 0.25 | 0.71 | 0.80 | 1.62 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 0.50 | UNSAFE_FORWARD_GAP | 19.32 / 19.15 | 0.00 / 0.00 | 19.15 | 20.88 |
| B | track_001 | C | 3.40 | PREDICTED_OVERLAP | 20.92 / 20.62 | 0.00 / 0.00 | 20.62 | 20.53 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 22183.348832025982, "reconstructed_as": "g19", "report_timing_error_s": 0.0, "sim_time": 132.15217785164714}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: B:track_001 (ANONYMOUS), true identity C

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
