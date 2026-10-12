> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase2): S18/run_0_platoon

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Negative case passes: C and D never fused.  D is U1 (A:track_001 + B:track_002 + B:track_004) with a short duplicate U2 (A:track_003) at the start; C is U3 then U4 (fragments).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_platoon | WARN | -6.20 .. -5.45 | D drawn twice at the start (U1, U2 = A:track_003) | [01_tgm006.20.png](visual_audit_phase2/01_tgm006.20.png) | fragmentation (fusion metrics: missed merges) |
| S18 | run_0_platoon | WARN | -6.20 .. | C appears as two successive road users (U3, U4) | [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | fragmentation |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_phase2/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.70.png](visual_audit_phase2/02_tgm005.70.png) | -5.70 | CRITICAL_TTC_START(A,track_001 (U1)) |
| [03_tgm001.05.png](visual_audit_phase2/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.65.png](visual_audit_phase2/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [05_tgm000.35.png](visual_audit_phase2/05_tgm000.35.png) | -0.35 | CRITICAL_TTC_END(A,track_001 (U1)) |
| [06_tgm000.20.png](visual_audit_phase2/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_phase2/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
