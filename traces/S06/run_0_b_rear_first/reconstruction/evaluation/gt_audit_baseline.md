# Ground-truth audit (privileged, evaluation only): S06/run_0_b_rear_first

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 142 | B | 1.000 | 0 | 0 | 0.29 / 0.52 | 0.01 / 0.13 | 0.3 / 2.2 |
| B:track_001 | 142 | C | 1.000 | 0 | 0 | 0.11 / 0.23 | 0.01 / 0.09 | 0.1 / 0.6 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 284 | 0.23 | 0.18 | 0.51 | 0.52 | 0.55 |
| track point to true outline [m] | 284 | 0.12 | 0.15 | 0.34 | 0.34 | 0.36 |
| speed error [m/s] | 284 | 0.01 | 0.03 | 0.10 | 0.13 | 1.81 |
| velocity vector error [m/s] | 284 | 0.01 | 0.05 | 0.14 | 0.21 | 5.06 |
| heading error [deg] | 88 | 0.22 | 0.34 | 0.85 | 1.66 | 2.29 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 4.70 | PREDICTED_OVERLAP | 20.65 / 20.72 | 0.00 / 0.00 | 20.72 | 20.49 |
| B | track_001 | C | 0.50 | UNSAFE_FORWARD_GAP | 13.54 / 13.34 | 0.00 / 0.00 | 13.34 | 20.51 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["B", "C"], "participants_correct": true, "peak_impulse": 21842.457779630535, "reconstructed_as": "g16", "report_timing_error_s": 0.0, "sim_time": 111.64463259279728}
- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 31706.269704451526, "reconstructed_as": "g26", "report_timing_error_s": 0.0, "sim_time": 113.19463261589408}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: C (ASSOCIATED), true identity C

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
