# Visual audit (visual_audit_hardening): S24/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

A rear-ends B between C and D: partner B named correctly, not the abreast neighbours; U3 (seen by B) and U8 (seen by A) are one car in the right lane drawn twice; A starts a CRITICAL_TTC to B 0.45 s after their own contact while they stay touching.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S24 | run_0 | PASS | 0.00 | - | [06_tgp000.00.png](visual_audit_hardening/06_tgp000.00.png) | - |
| S24 | run_0 | WARN | 0.05 | U3 / U8 unmerged duplicate | [07_tgp000.05.png](visual_audit_hardening/07_tgp000.05.png) | not tuned; reported |
| S24 | run_0 | WARN | 0.45 | CRITICAL_TTC A->B after the own collision | [08_tgp000.45.png](visual_audit_hardening/08_tgp000.45.png) | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.75.png](visual_audit_hardening/01_tgm007.75.png) | -7.75 | lead-in |
| [02_tgm007.25.png](visual_audit_hardening/02_tgm007.25.png) | -7.25 | CRITICAL_TTC_START(B,U5) |
| [03_tgm005.90.png](visual_audit_hardening/03_tgm005.90.png) | -5.90 | CRITICAL_TTC_START(A,B) |
| [04_tgm000.80.png](visual_audit_hardening/04_tgm000.80.png) | -0.80 | CUT_IN_FROM_RIGHT_START(A,U1) |
| [05_tgm000.20.png](visual_audit_hardening/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_hardening/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); COLLISION(A,B) |
| [07_tgp000.05.png](visual_audit_hardening/07_tgp000.05.png) | +0.05 | CUT_IN_FROM_RIGHT_END(A,U1) |
| [08_tgp000.45.png](visual_audit_hardening/08_tgp000.45.png) | +0.45 | CRITICAL_TTC_START(A,B) |
| [09_tgp000.50.png](visual_audit_hardening/09_tgp000.50.png) | +0.50 | CRITICAL_TTC_END(B,U5); after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| critical_start_after_own_collision | +0.45 | A:track_008 | 0.45 s after the collision |
| road_users_overlap | +1.55 | U3 / U5 | drawn bodies overlap from here |
| road_users_overlap | +1.75 | U9 / U11 | drawn bodies overlap from here |
| road_users_overlap | +1.85 | U10 / U12 | drawn bodies overlap from here |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
