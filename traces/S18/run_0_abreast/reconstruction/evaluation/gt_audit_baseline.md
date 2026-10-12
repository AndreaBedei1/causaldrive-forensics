> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Ground-truth audit (privileged, evaluation only): S18/run_0_abreast

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 103 | C | 0.748 | 1 | 0 | 0.32 / 0.84 | 0.05 / 0.42 | 0.5 / 11.8 |
| A:track_002 | 115 | B | 1.000 | 0 | 0 | 1.26 / 2.10 | 0.19 / 0.83 | 0.9 / 1.3 |
| A:track_003 | 102 | D | 0.961 | 1 | 0 | 0.87 / 2.80 | 0.19 / 0.71 | 0.9 / 8.5 |
| B:track_001 | 115 | A | 1.000 | 0 | 0 | 1.48 / 2.70 | 0.20 / 0.79 | 0.8 / 2.2 |
| B:track_002 | 90 | C | 1.000 | 0 | 0 | 0.36 / 0.60 | 0.04 / 0.14 | 0.4 / 1.3 |
| B:track_003 | 90 | D | 1.000 | 0 | 0 | 0.66 / 0.86 | 0.08 / 0.19 | 0.6 / 1.9 |
| B:track_004 | 46 | C | 1.000 | 0 | 0 | 3.52 / 3.64 | 0.08 / 0.19 | 0.3 / 1.9 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 661 | 0.68 | 1.30 | 2.70 | 3.49 | 3.65 |
| track point to true outline [m] | 661 | 0.43 | 0.41 | 0.65 | 0.69 | 0.91 |
| speed error [m/s] | 661 | 0.09 | 0.19 | 0.46 | 0.67 | 2.88 |
| velocity vector error [m/s] | 661 | 0.20 | 0.25 | 0.67 | 1.00 | 3.34 |
| heading error [deg] | 576 | 0.63 | 0.85 | 1.84 | 3.39 | 15.67 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | C | 2.05 | - | 15.06 / 14.96 | 0.64 / 0.00 | 14.96 | 16.83 |
| A | track_002 | B | 5.15 | - | -5.20 / -6.36 | 0.94 / 1.03 | 1.53 | 16.89 |
| B | track_001 | A | 5.55 | - | -3.83 / -2.89 | 0.91 / 0.63 | 1.26 | 18.81 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | C | 2.40 | CUT_IN_FROM_RIGHT | 0.00 / 0.00 | -2.56 / -0.00 |
| A | track_001 | C | 9.90 | CUT_IN_FROM_RIGHT | 0.96 / 0.89 | -1.24 / -1.26 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 1079.5610551393547, "reconstructed_as": "g29", "report_timing_error_s": 0.0, "sim_time": 488.62503729760647}
- extra reconstructed collisions: 0
- A:track_001: U1 (ANONYMOUS), true identity C
- A:track_002: B (ASSOCIATED), true identity B
- A:track_003: U3 (ANONYMOUS), true identity D
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: U2 (ANONYMOUS), true identity C
- B:track_003: U3 (ANONYMOUS), true identity D
- B:track_004: U2 (ANONYMOUS), true identity C

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
