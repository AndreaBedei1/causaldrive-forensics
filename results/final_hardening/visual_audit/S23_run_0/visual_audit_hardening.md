# Visual audit (visual_audit_hardening): S23/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Contact A-B after A swerves is named correctly; at long range (about 45 m, beyond the relevance envelope) U5/U6 overlap and U4/U5 touch; U2 drawn tilted and jumping 3.2 m at -6.3 s.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S23 | run_0 | PASS | 0.00 | - | [15_tgp000.00.png](visual_audit_hardening/15_tgp000.00.png) | - |
| S23 | run_0 | WARN | -7.30 | far U4/U5/U6 overlap | [03_tgm006.65.png](visual_audit_hardening/03_tgm006.65.png) | not tuned; reported |
| S23 | run_0 | WARN | -6.30 | U2 box jump / wrong heading | [01_tgm008.50.png](visual_audit_hardening/01_tgm008.50.png) | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm008.50.png](visual_audit_hardening/01_tgm008.50.png) | -8.50 | lead-in |
| [02_tgm006.75.png](visual_audit_hardening/02_tgm006.75.png) | -6.75 | CRITICAL_TTC_START(A,U1) |
| [03_tgm006.65.png](visual_audit_hardening/03_tgm006.65.png) | -6.65 | CUT_IN_FROM_RIGHT_START(A,U1) |
| [04_tgm005.90.png](visual_audit_hardening/04_tgm005.90.png) | -5.90 | CRITICAL_TTC_END(A,U1) |
| [05_tgm005.85.png](visual_audit_hardening/05_tgm005.85.png) | -5.85 | CUT_IN_FROM_RIGHT_END(A,U1) |
| [06_tgm003.20.png](visual_audit_hardening/06_tgm003.20.png) | -3.20 | CRITICAL_TTC_START(A,U3) |
| [07_tgm003.10.png](visual_audit_hardening/07_tgm003.10.png) | -3.10 | CUT_IN_FROM_RIGHT_START(A,U3) |
| [08_tgm002.40.png](visual_audit_hardening/08_tgm002.40.png) | -2.40 | CRITICAL_TTC_END(A,U3) |
| [09_tgm002.35.png](visual_audit_hardening/09_tgm002.35.png) | -2.35 | CUT_IN_FROM_RIGHT_END(A,U3) |
| [10_tgm001.40.png](visual_audit_hardening/10_tgm001.40.png) | -1.40 | CRITICAL_TTC_START(A,U7) |
| [11_tgm001.35.png](visual_audit_hardening/11_tgm001.35.png) | -1.35 | CRITICAL_TTC_START(A,B) |
| [12_tgm000.80.png](visual_audit_hardening/12_tgm000.80.png) | -0.80 | CRITICAL_TTC_START(B,A) |
| [13_tgm000.20.png](visual_audit_hardening/13_tgm000.20.png) | -0.20 | EGO_PATH_ENTRY(B,A); before COLLISION(A,B) |
| [14_tgm000.05.png](visual_audit_hardening/14_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,U8) |
| [15_tgp000.00.png](visual_audit_hardening/15_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [16_tgp000.30.png](visual_audit_hardening/16_tgp000.30.png) | +0.30 | CRITICAL_TTC_END(A,U8); EGO_PATH_ENTRY(A,B) |
| [17_tgp000.50.png](visual_audit_hardening/17_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -7.30 | U4 / U5 | drawn bodies overlap from here |
| road_users_overlap | -7.30 | U5 / U6 | drawn bodies overlap from here |
| road_user_box_jump | -6.30 | U2 | box moved 3.2 m at 6.5 m/s |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
