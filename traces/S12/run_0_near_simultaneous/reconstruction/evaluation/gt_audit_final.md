# Ground-truth audit (privileged, evaluation only): S12/run_0_near_simultaneous

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 104 | B | 1.000 | 0 | 0 | 1.02 / 1.21 | 0.10 / 1.23 | 7.3 / 17.6 |
| B:track_001#segment_1 | 43 | A | 1.000 | 0 | 0 | 1.11 / 2.04 | 0.74 / 1.70 | 6.8 / 12.7 |
| B:track_001#segment_2 | 13 | A | 1.000 | 0 | 0 | 0.97 / 2.25 | 1.49 / 3.65 | 31.2 / 61.4 |
| B:track_001#segment_3 | 48 | A | 1.000 | 0 | 0 | 1.88 / 1.92 | 0.04 / 0.15 | - / - |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 208 | 1.18 | 1.02 | 1.90 | 1.93 | 2.54 |
| track point to true outline [m] | 208 | 0.14 | 0.23 | 0.52 | 0.61 | 0.79 |
| speed error [m/s] | 208 | 0.11 | 0.50 | 1.23 | 1.63 | 3.68 |
| velocity vector error [m/s] | 208 | 0.13 | 0.90 | 1.50 | 1.89 | 3.77 |
| heading error [deg] | 64 | 7.29 | 3.93 | 17.36 | 41.96 | 63.51 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 5.90 | PREDICTED_OVERLAP | 4.08 / 4.46 | 12.41 / 12.02 | 13.21 | 6.95 |
| B | track_001#segment_1 | A | 6.05 | - | 11.45 / 11.58 | 5.20 / 2.91 | 12.09 | 6.88 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 7661.461427344263, "reconstructed_as": "g37", "report_timing_error_s": 0.0, "sim_time": 192.76600752398372}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B
- B:track_001#segment_1: A (ASSOCIATED), true identity A
- B:track_001#segment_2: A (ASSOCIATED), true identity A
- B:track_001#segment_3: A (ASSOCIATED), true identity A

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
