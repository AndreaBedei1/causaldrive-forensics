# Visual audit (visual_audit_hardening): S22/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Merge contact A-B correct, the occluded car reappears as one road user near the recorders; overlapping pair U3/U6 at lead-in and a 3.8 m box jump of U2 at +3.7 s.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S22 | run_0 | PASS | 0.00 | - | [12_tgp000.00.png](visual_audit_hardening/12_tgp000.00.png) | - |
| S22 | run_0 | WARN | -7.30 | U3 / U6 overlap at lead-in |  | not tuned; reported |
| S22 | run_0 | WARN | 3.70 | U2 box jump 3.8 m |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.30.png](visual_audit_hardening/01_tgm007.30.png) | -7.30 | lead-in |
| [02_tgm006.80.png](visual_audit_hardening/02_tgm006.80.png) | -6.80 | CRITICAL_TTC_START(B,U5) |
| [03_tgm001.85.png](visual_audit_hardening/03_tgm001.85.png) | -1.85 | EGO_PATH_ENTRY(A,U1); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(A,U1) |
| [04_tgm001.80.png](visual_audit_hardening/04_tgm001.80.png) | -1.80 | EGO_PATH_ENTRY(B,U1) |
| [05_tgm001.75.png](visual_audit_hardening/05_tgm001.75.png) | -1.75 | CRITICAL_TTC_START(B,A) |
| [06_tgm001.70.png](visual_audit_hardening/06_tgm001.70.png) | -1.70 | CRITICAL_TTC_START(B,U1) |
| [07_tgm001.15.png](visual_audit_hardening/07_tgm001.15.png) | -1.15 | CRITICAL_TTC_END(B,U5) |
| [08_tgm000.45.png](visual_audit_hardening/08_tgm000.45.png) | -0.45 | CRITICAL_TTC_START(A,U5) |
| [09_tgm000.35.png](visual_audit_hardening/09_tgm000.35.png) | -0.35 | EGO_PATH_ENTRY(B,A) |
| [10_tgm000.25.png](visual_audit_hardening/10_tgm000.25.png) | -0.25 | CUT_IN_FROM_LEFT_START(A,U5) |
| [11_tgm000.20.png](visual_audit_hardening/11_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [12_tgp000.00.png](visual_audit_hardening/12_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B) |
| [13_tgp000.10.png](visual_audit_hardening/13_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,U5) |
| [14_tgp000.20.png](visual_audit_hardening/14_tgp000.20.png) | +0.20 | CUT_IN_FROM_RIGHT_START(B,A) |
| [15_tgp000.35.png](visual_audit_hardening/15_tgp000.35.png) | +0.35 | CRITICAL_TTC_END(A,U1); EGO_PATH_ENTRY(B,U5) |
| [16_tgp000.50.png](visual_audit_hardening/16_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [17_tgp000.55.png](visual_audit_hardening/17_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,U5) |
| [18_tgp000.95.png](visual_audit_hardening/18_tgp000.95.png) | +0.95 | EGO_PATH_ENTRY(A,B) |
| [19_tgp001.00.png](visual_audit_hardening/19_tgp001.00.png) | +1.00 | CRITICAL_TTC_END(B,A) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -7.30 | U3 / U6 | drawn bodies overlap from here |
| road_user_box_jump | +3.70 | U2 | box moved 3.8 m at 12.0 m/s |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
