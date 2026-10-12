# Ground-truth audit (privileged, evaluation only): S18/run_0_abreast

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001#segment_1 | 3 | D | 1.000 | 0 | 0 | 0.37 / 0.59 | 0.12 / 0.18 | 13.9 / 13.9 |
| A:track_001#segment_2 | 39 | D | 0.795 | 1 | 0 | 0.29 / 1.31 | 0.12 / 0.84 | 2.6 / 16.3 |
| A:track_001#segment_3 | 61 | C | 1.000 | 0 | 0 | 0.34 / 0.72 | 0.07 / 0.19 | 0.3 / 0.9 |
| A:track_002 | 115 | B | 1.000 | 0 | 0 | 1.26 / 2.10 | 0.19 / 0.83 | 0.9 / 1.3 |
| A:track_003 | 102 | D | 0.961 | 1 | 0 | 0.86 / 2.21 | 0.16 / 0.65 | 0.7 / 9.2 |
| B:track_001 | 115 | A | 1.000 | 0 | 0 | 1.48 / 2.70 | 0.20 / 0.79 | 0.8 / 2.2 |
| B:track_002 | 90 | C | 1.000 | 0 | 0 | 0.38 / 0.53 | 0.03 / 0.12 | 0.4 / 1.2 |
| B:track_003 | 90 | D | 1.000 | 0 | 0 | 0.66 / 0.86 | 0.08 / 0.19 | 0.6 / 1.9 |
| B:track_004 | 86 | C | 1.000 | 0 | 0 | 2.37 / 2.99 | 0.18 / 0.42 | 0.8 / 3.6 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 701 | 0.72 | 1.44 | 2.54 | 2.70 | 3.00 |
| track point to true outline [m] | 701 | 0.38 | 0.37 | 0.64 | 0.68 | 0.95 |
| speed error [m/s] | 701 | 0.11 | 0.19 | 0.43 | 0.64 | 2.88 |
| velocity vector error [m/s] | 701 | 0.21 | 0.26 | 0.71 | 1.07 | 3.64 |
| heading error [deg] | 616 | 0.67 | 0.91 | 2.43 | 4.21 | 16.83 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001#segment_3 | C | 4.65 | - | 15.51 / 15.03 | 0.00 / 0.00 | 15.03 | 16.83 |
| A | track_002 | B | 5.15 | - | -5.20 / -6.36 | 0.94 / 1.03 | 1.53 | 16.89 |
| B | track_001 | A | 5.55 | - | -3.83 / -2.89 | 0.91 / 0.63 | 1.26 | 18.81 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_003 | D | 9.40 | CUT_IN_FROM_RIGHT | 5.23 / 5.05 | -0.34 / -0.40 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1079.5610551393547, "reconstructed_as": "g25", "report_timing_error_s": 0.0, "sim_time": 488.62503729760647}
- extra reconstructed collisions: 0
- A:track_001#segment_1: U1 (ANONYMOUS), true identity D
- A:track_001#segment_2: U4 (ANONYMOUS), true identity D
- A:track_001#segment_3: U2 (ANONYMOUS), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- A:track_003: U3 (ANONYMOUS), true identity D
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U2 (ANONYMOUS), true identity C
- B:track_003: U3 (ANONYMOUS), true identity D
- B:track_004: U2 (ANONYMOUS), true identity C

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
