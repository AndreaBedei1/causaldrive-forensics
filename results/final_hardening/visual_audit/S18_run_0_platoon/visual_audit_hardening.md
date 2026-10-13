# Visual audit (visual_audit_hardening): S18/run_0_platoon

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Collision A-B correct; after the contact U3 (seen by B) and U4 (seen by A) are drawn on top of each other ahead: one car not merged (conservative, but a visible duplicate).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_platoon | WARN | 0.50 | U3 / U4 duplicate of one car | [09_tgp000.50.png](visual_audit_hardening/09_tgp000.50.png) | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_hardening/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.70.png](visual_audit_hardening/02_tgm005.70.png) | -5.70 | CRITICAL_TTC_START(A,U1) |
| [03_tgm001.05.png](visual_audit_hardening/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,B) |
| [04_tgm000.65.png](visual_audit_hardening/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,A) |
| [05_tgm000.35.png](visual_audit_hardening/05_tgm000.35.png) | -0.35 | CRITICAL_TTC_END(A,U1) |
| [06_tgm000.20.png](visual_audit_hardening/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_hardening/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [08_tgp000.10.png](visual_audit_hardening/08_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,B) |
| [09_tgp000.50.png](visual_audit_hardening/09_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | +1.10 | U3 / U4 | drawn bodies overlap from here |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
