# Ground-truth audit (privileged, evaluation only): S06/run_0_a_front_pushed

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 138 | B | 1.000 | 0 | 0 | 0.96 / 1.04 | 0.04 / 1.11 | 0.1 / 17.0 |
| B:track_001 | 138 | C | 1.000 | 0 | 0 | 0.16 / 0.23 | 0.01 / 0.11 | 0.1 / 0.7 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 276 | 0.31 | 0.80 | 1.01 | 1.03 | 1.34 |
| track point to true outline [m] | 276 | 0.23 | 0.41 | 0.60 | 0.60 | 0.62 |
| speed error [m/s] | 276 | 0.02 | 0.06 | 0.14 | 0.27 | 4.46 |
| velocity vector error [m/s] | 276 | 0.03 | 0.08 | 0.16 | 0.44 | 5.42 |
| heading error [deg] | 93 | 0.13 | 0.35 | 1.22 | 8.65 | 23.95 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 0.50 | UNSAFE_FORWARD_GAP | 4.52 / 4.36 | 0.00 / 0.00 | 4.36 | 20.59 |
| B | track_001 | C | 0.50 | UNSAFE_FORWARD_GAP | 13.54 / 13.34 | 0.00 / 0.00 | 13.34 | 20.51 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 10281.411958816992, "reconstructed_as": "g21", "report_timing_error_s": 0.0, "sim_time": 93.58650696277618}
- {"participants": ["B", "C"], "participants_correct": true, "peak_impulse": 8788.05213279538, "reconstructed_as": "g25", "report_timing_error_s": 0.0, "sim_time": 94.08650697022676}
- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1509.7550582790507, "reconstructed_as": "g30", "report_timing_error_s": 0.0, "sim_time": 94.23650697246194}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001: C (ASSOCIATED), true identity C

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
