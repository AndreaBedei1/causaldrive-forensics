> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Ground-truth audit (privileged, evaluation only): S16/run_0_consequential

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 120 | C | 1.000 | 0 | 0 | 0.69 / 0.99 | 0.07 / 0.42 | 1.3 / 4.7 |
| A:track_002 | 67 | C | 1.000 | 0 | 0 | 2.54 / 2.92 | 0.03 / 0.10 | 0.2 / 2.3 |
| B:track_001 | 120 | A | 1.000 | 0 | 0 | 0.42 / 0.70 | 0.07 / 0.45 | 0.2 / 4.3 |
| B:track_002 | 120 | C | 1.000 | 0 | 0 | 0.79 / 1.58 | 0.08 / 0.35 | 1.5 / 5.7 |
| B:track_003 | 40 | C | 1.000 | 0 | 0 | 3.06 / 3.69 | 0.05 / 0.54 | 1.2 / 8.9 |
| B:track_004 | 4 | C | 1.000 | 0 | 0 | 3.32 / 3.40 | 0.41 / 0.53 | 7.6 / 7.7 |
| C:track_001 | 38 | A | 1.000 | 0 | 0 | 0.99 / 1.70 | 0.17 / 0.38 | 2.6 / 3.8 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 509 | 0.71 | 0.89 | 2.77 | 3.06 | 3.75 |
| track point to true outline [m] | 509 | 0.21 | 0.21 | 0.48 | 0.67 | 0.95 |
| speed error [m/s] | 509 | 0.07 | 0.12 | 0.29 | 0.43 | 2.12 |
| velocity vector error [m/s] | 509 | 0.12 | 0.30 | 0.69 | 0.98 | 2.31 |
| heading error [deg] | 371 | 0.97 | 2.39 | 4.28 | 6.53 | 9.25 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | C | 5.20 | UNSAFE_FORWARD_GAP | 1.27 / 1.30 | 0.37 / 0.10 | 1.65 | 10.22 |
| B | track_001 | A | 0.50 | UNSAFE_FORWARD_GAP | 7.16 / 6.95 | 0.00 / 0.00 | 6.95 | 18.11 |
| C | track_001 | A | 5.60 | PREDICTED_OVERLAP | -11.66 / -11.38 | 1.36 / 0.11 | 1.46 | 11.72 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | C | 5.45 | CUT_IN_FROM_LEFT | 0.00 / 0.00 | 0.99 / 1.02 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 4243.514729638987, "reconstructed_as": "g33", "report_timing_error_s": 0.0, "sim_time": 229.82582645490766}
- {"participants": ["A", "C"], "participants_correct": true, "peak_impulse": 322.104643689845, "reconstructed_as": "g48", "report_timing_error_s": 0.0, "sim_time": 230.87582647055387}
- extra reconstructed collisions: 0
- A:track_001: C (ASSOCIATED), true identity C
- A:track_002: C (ASSOCIATED), true identity C
- B:track_001: A (ASSOCIATED), true identity A
- B:track_002: C (ASSOCIATED), true identity C
- B:track_003: C (ASSOCIATED), true identity C
- B:track_004: U1 (ANONYMOUS), true identity C
- C:track_001: A (ASSOCIATED), true identity A

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
