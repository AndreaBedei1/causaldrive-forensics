# Ground-truth audit (privileged, evaluation only): S02/run_0_critical_before_cut_in

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 113 | B | 1.000 | 0 | 0 | 2.06 / 2.10 | 0.03 / 0.82 | 3.5 / 7.9 |
| B:track_001 | 93 | A | 1.000 | 0 | 0 | 3.65 / 3.69 | 0.01 / 0.49 | 3.3 / 7.4 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 206 | 2.07 | 2.41 | 3.65 | 3.66 | 3.71 |
| track point to true outline [m] | 206 | 0.06 | 0.11 | 0.54 | 0.56 | 0.61 |
| speed error [m/s] | 206 | 0.03 | 0.09 | 0.46 | 0.77 | 1.16 |
| velocity vector error [m/s] | 206 | 0.04 | 0.23 | 0.80 | 0.94 | 1.79 |
| heading error [deg] | 68 | 3.43 | 4.20 | 7.31 | 7.57 | 12.72 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 2.60 | UNSAFE_FORWARD_GAP | 3.77 / 3.58 | 0.98 / 0.63 | 3.84 | 19.53 |
| B | track_001 | A | 2.70 | PREDICTED_OVERLAP | -11.34 / -11.67 | 1.91 / 1.11 | 3.16 | 7.02 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | B | 2.95 | CUT_IN_FROM_LEFT | 0.20 / 0.22 | 1.38 / 1.05 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 604.4798968714863, "reconstructed_as": "g17", "report_timing_error_s": 0.0, "sim_time": 54.93444100022316}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
