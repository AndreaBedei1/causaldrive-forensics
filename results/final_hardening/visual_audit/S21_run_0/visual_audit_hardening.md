# Visual audit (visual_audit_hardening): S21/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Sideswipe A-B named correctly; 25-35 m ahead a far group (U9/U10/U11, U14/U15) is drawn with overlapping bodies, U11 spins 46 deg and several boxes jump 4 m after the contact: far single-observer fragments, outside the relevance envelope, not merged.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S21 | run_0 | PASS | 0.00 | - |  | - |
| S21 | run_0 | WARN | 0.80 | U11 heading spin 46 deg; U9/U10/U11 overlap | [18_tgp000.80.png](visual_audit_hardening/18_tgp000.80.png) | not tuned; reported |
| S21 | run_0 | WARN | 2.6-5.0 | box jumps 3.7-4.6 m (U14, U10, U3) |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.75.png](visual_audit_hardening/01_tgm006.75.png) | -6.75 | lead-in |
| [02_tgm006.25.png](visual_audit_hardening/02_tgm006.25.png) | -6.25 | CRITICAL_TTC_START(A,U3); CRITICAL_TTC_START(B,U1) |
| [03_tgm003.25.png](visual_audit_hardening/03_tgm003.25.png) | -3.25 | CUT_IN_FROM_RIGHT_START(B,A) |
| [04_tgm002.45.png](visual_audit_hardening/04_tgm002.45.png) | -2.45 | CUT_IN_FROM_RIGHT_END(B,A) |
| [05_tgm001.65.png](visual_audit_hardening/05_tgm001.65.png) | -1.65 | CRITICAL_TTC_START(A,B) |
| [06_tgm001.20.png](visual_audit_hardening/06_tgm001.20.png) | -1.20 | CRITICAL_TTC_START(B,A) |
| [07_tgm001.15.png](visual_audit_hardening/07_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,U1) |
| [08_tgm001.05.png](visual_audit_hardening/08_tgm001.05.png) | -1.05 | EGO_PATH_ENTRY(A,U1) |
| [09_tgm000.35.png](visual_audit_hardening/09_tgm000.35.png) | -0.35 | EGO_PATH_ENTRY(A,B) |
| [10_tgm000.20.png](visual_audit_hardening/10_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [11_tgp000.00.png](visual_audit_hardening/11_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [12_tgp000.10.png](visual_audit_hardening/12_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,U3); CRITICAL_TTC_START(A,U3) |
| [13_tgp000.20.png](visual_audit_hardening/13_tgp000.20.png) | +0.20 | EGO_PATH_ENTRY(B,U9) |
| [14_tgp000.45.png](visual_audit_hardening/14_tgp000.45.png) | +0.45 | EGO_PATH_ENTRY(B,U11) |
| [15_tgp000.50.png](visual_audit_hardening/15_tgp000.50.png) | +0.50 | EGO_PATH_ENTRY(B,U3); after COLLISION(A,B) |
| [16_tgp000.65.png](visual_audit_hardening/16_tgp000.65.png) | +0.65 | CRITICAL_TTC_START(B,U3) |
| [17_tgp000.70.png](visual_audit_hardening/17_tgp000.70.png) | +0.70 | CRITICAL_TTC_END(A,U3) |
| [18_tgp000.80.png](visual_audit_hardening/18_tgp000.80.png) | +0.80 | CRITICAL_TTC_END(B,U1) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.65 | U5 / U6 | drawn bodies overlap from here |
| road_user_box_spin | +0.80 | U11 | heading turned 46 deg |
| road_users_overlap | +1.05 | U10 / U11 | drawn bodies overlap from here |
| road_users_overlap | +1.05 | U9 / U10 | drawn bodies overlap from here |
| road_users_overlap | +1.05 | U9 / U11 | drawn bodies overlap from here |
| road_users_overlap | +1.95 | U1 / U11 | drawn bodies overlap from here |
| road_users_overlap | +1.95 | U14 / U15 | drawn bodies overlap from here |
| road_user_box_jump | +2.60 | U14 | box moved 4.1 m at 13.8 m/s |
| road_user_box_jump | +3.80 | U10 | box moved 4.6 m at 11.6 m/s |
| road_user_box_jump | +4.10 | U10 | box moved 4.5 m at 11.7 m/s |
| road_user_box_jump | +5.00 | U3 | box moved 3.7 m at 11.8 m/s |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
