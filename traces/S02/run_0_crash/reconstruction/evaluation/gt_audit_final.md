# Ground-truth audit (privileged, evaluation only): S02/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 149 | B | 1.000 | 0 | 0 | 0.31 / 0.65 | 0.02 / 0.23 | 0.7 / 3.4 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 149 | 0.31 | 0.28 | 0.62 | 0.65 | 0.69 |
| track point to true outline [m] | 149 | 0.11 | 0.33 | 0.46 | 0.47 | 0.48 |
| speed error [m/s] | 149 | 0.02 | 0.05 | 0.10 | 0.23 | 1.97 |
| velocity vector error [m/s] | 149 | 0.05 | 0.13 | 0.25 | 0.32 | 1.98 |
| heading error [deg] | 55 | 0.72 | 1.03 | 1.80 | 3.43 | 5.49 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 1.90 | UNSAFE_FORWARD_GAP | 20.33 / 20.02 | 0.00 / 0.00 | 20.03 | 20.51 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | B | 1.45 | CUT_IN_FROM_LEFT | 0.56 / 0.25 | 0.94 / 1.15 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 2460.669927422933, "reconstructed_as": "g17", "report_timing_error_s": 0.0, "sim_time": 1776.7966108731925}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
