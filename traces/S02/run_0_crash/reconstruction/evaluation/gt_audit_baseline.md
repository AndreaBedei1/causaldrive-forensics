> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Ground-truth audit (privileged, evaluation only): S02/run_0_crash

Reconstruction result vs ground truth; the reconstruction never reads these files.

## Tracks

| track | samples | identity | purity | switches | unmatched | centre err. median / p95 [m] | speed err. median / p95 [m/s] | heading err. median / p95 [deg] |
|---|---|---|---|---|---|---|---|---|
| A:track_001 | 150 | B | 1.000 | 0 | 0 | 0.36 / 0.54 | 0.03 / 0.23 | 1.8 / 8.1 |

## Pooled track errors (every track sample)

| quantity | n | median | IQR | p90 | p95 | max |
|---|---|---|---|---|---|---|
| box centre error [m] | 150 | 0.36 | 0.02 | 0.48 | 0.54 | 0.70 |
| track point to true outline [m] | 150 | 0.14 | 0.15 | 0.35 | 0.39 | 0.40 |
| speed error [m/s] | 150 | 0.03 | 0.05 | 0.14 | 0.23 | 0.71 |
| velocity vector error [m/s] | 150 | 0.03 | 0.17 | 0.43 | 0.69 | 1.22 |
| heading error [deg] | 50 | 1.77 | 3.03 | 5.53 | 8.15 | 9.88 |

## CRITICAL_TTC_START geometry

| recorder | track | true identity | t_local [s] | reason | clearance rec / true [m] | body gap rec / true [m] | bumper gap true [m] | d_min [m] |
|---|---|---|---|---|---|---|---|---|
| A | track_001 | B | 1.80 | UNSAFE_FORWARD_GAP | 15.99 / 15.73 | 0.84 / 0.76 | 15.79 | 20.54 |

## CUT_IN start geometry

| recorder | track | true identity | t_local [s] | direction | body gap rec / true [m] | lateral speed rec / true [m/s] |
|---|---|---|---|---|---|---|
| A | track_001 | B | 2.10 | CUT_IN_FROM_LEFT | 0.57 / 0.46 | 0.83 / 0.96 |

## Collisions and associations (from evaluation.json)

- {"participants": ["A", "B"], "participants_correct": true, "peak_impulse": 2900.2340186474003, "reconstructed_as": "g16", "report_timing_error_s": 0.0, "sim_time": 35.291471753269434}
- extra reconstructed collisions: 0
- A:track_001: B (ASSOCIATED), true identity B

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
