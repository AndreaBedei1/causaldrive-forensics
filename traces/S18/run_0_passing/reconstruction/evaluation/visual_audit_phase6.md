> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase6): S18/run_0_passing

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Negative case passes: C and D never fused.  D is one road user (U3 = A:track_004 + B:track_003 + B:track_005), C two (U1, U2).  As in abreast, A:track_001 starts on D and settles on C: a spurious CUT_IN_FROM_RIGHT / EGO_PATH_ENTRY of A on U1.  Phase 6: frames pixel-identical to the phase-2 frames inspected then; the verdict stands.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_passing | WARN | -6.20 .. +0.50 | C drawn as two road users (U1, U2): missed merge | [05_tgm002.75.png](visual_audit_phase6/05_tgm002.75.png) | fragmentation (fusion metrics: missed merges) |
| S18 | run_0_passing | WARN | -3.20 .. -1.90 | spurious CUT_IN_FROM_RIGHT / EGO_PATH_ENTRY of A on U1 (track drifting from D to C) | [04_tgm003.20.png](visual_audit_phase6/04_tgm003.20.png) | local tracker limitation; phase-5 false positives |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_phase6/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.55.png](visual_audit_phase6/02_tgm005.55.png) | -5.55 | CRITICAL_TTC_START(A,track_003 (U2)) |
| [03_tgm003.60.png](visual_audit_phase6/03_tgm003.60.png) | -3.60 | CRITICAL_TTC_START(A,track_001 (U1)) |
| [04_tgm003.20.png](visual_audit_phase6/04_tgm003.20.png) | -3.20 | CUT_IN_FROM_RIGHT_START(A,track_001 (U1)) |
| [05_tgm002.75.png](visual_audit_phase6/05_tgm002.75.png) | -2.75 | EGO_PATH_ENTRY(A,track_001 (U1)) |
| [06_tgm001.90.png](visual_audit_phase6/06_tgm001.90.png) | -1.90 | CUT_IN_FROM_RIGHT_END(A,track_001 (U1)) |
| [07_tgm001.05.png](visual_audit_phase6/07_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [08_tgm000.65.png](visual_audit_phase6/08_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [09_tgm000.45.png](visual_audit_phase6/09_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_001 (U1)) |
| [10_tgm000.20.png](visual_audit_phase6/10_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [11_tgp000.00.png](visual_audit_phase6/11_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [12_tgp000.50.png](visual_audit_phase6/12_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U3 | drawn bodies overlap from here |
| road_users_overlap | -3.00 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
