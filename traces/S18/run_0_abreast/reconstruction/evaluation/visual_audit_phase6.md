# Visual audit (visual_audit_phase6): S18/run_0_abreast

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Negative case passes: C and D are never one road user.  C is drawn twice (U1 = A:track_001, U2 = B's tracks: a missed merge), D once (U3 = A:track_003 + B:track_003).  A:track_001 starts on D (C and D 1.4 m apart side to side: A's radar clusters their returns) and settles on C: the drift is reconstructed as a CUT_IN_FROM_RIGHT and an EGO_PATH_ENTRY of A on U1 that did not happen.  Phase 6: frames pixel-identical to the phase-2 frames inspected then; the verdict stands.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_abreast | WARN | -6.20 .. +0.50 | C drawn as two road users (U1, U2) overlapping: missed merge | [04_tgm003.55.png](visual_audit_phase6/04_tgm003.55.png) | fragmentation, the price of conservative gates (fusion metrics: missed merges) |
| S18 | run_0_abreast | WARN | -3.80 .. -2.65 | spurious CUT_IN_FROM_RIGHT / EGO_PATH_ENTRY of A on U1: A's track moves from D to C, no vehicle cuts in | [03_tgm003.80.png](visual_audit_phase6/03_tgm003.80.png) | local tracker limitation (returns of two cars within the 2 m cluster distance); counted as false positives by the phase-5 semantic evaluation |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_phase6/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm004.15.png](visual_audit_phase6/02_tgm004.15.png) | -4.15 | CRITICAL_TTC_START(A,track_001 (U1)) |
| [03_tgm003.80.png](visual_audit_phase6/03_tgm003.80.png) | -3.80 | CUT_IN_FROM_RIGHT_START(A,track_001 (U1)) |
| [04_tgm003.55.png](visual_audit_phase6/04_tgm003.55.png) | -3.55 | EGO_PATH_ENTRY(A,track_001 (U1)) |
| [05_tgm002.65.png](visual_audit_phase6/05_tgm002.65.png) | -2.65 | CUT_IN_FROM_RIGHT_END(A,track_001 (U1)) |
| [06_tgm001.05.png](visual_audit_phase6/06_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [07_tgm000.65.png](visual_audit_phase6/07_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [08_tgm000.45.png](visual_audit_phase6/08_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_001 (U1)) |
| [09_tgm000.20.png](visual_audit_phase6/09_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [10_tgp000.00.png](visual_audit_phase6/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [11_tgp000.50.png](visual_audit_phase6/11_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U3 | drawn bodies overlap from here |
| road_users_overlap | -6.00 | U2 / U3 | drawn bodies overlap from here |
| road_user_box_jump | -5.70 | U2 | box moved 4.5 m at 11.9 m/s |
| road_users_overlap | -3.80 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
