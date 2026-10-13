# Visual audit (visual_audit_hardening): S19/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Contact A-B named correctly at the sideswipe, abreast rows kept apart near the recorders; at lead-in two single-observer tracks of one far car overlap (U2/U9 region) and at the far front U14/U15 overlap briefly.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S19 | run_0 | PASS | 0.00 | - | [07_tgp000.00.png](visual_audit_hardening/07_tgp000.00.png) | - |
| S19 | run_0 | WARN | -7.35 | overlapping single-observer duplicates of a far car | [03_tgm007.20.png](visual_audit_hardening/03_tgm007.20.png) | not tuned; reported |
| S19 | run_0 | WARN | -1.05 | U14 / U15 overlap far ahead | [05_tgm000.75.png](visual_audit_hardening/05_tgm000.75.png) | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.75.png](visual_audit_hardening/01_tgm007.75.png) | -7.75 | lead-in |
| [02_tgm007.25.png](visual_audit_hardening/02_tgm007.25.png) | -7.25 | CRITICAL_TTC_START(B,U4) |
| [03_tgm007.20.png](visual_audit_hardening/03_tgm007.20.png) | -7.20 | CRITICAL_TTC_START(A,U6) |
| [04_tgm001.40.png](visual_audit_hardening/04_tgm001.40.png) | -1.40 | CRITICAL_TTC_START(A,B) |
| [05_tgm000.75.png](visual_audit_hardening/05_tgm000.75.png) | -0.75 | EGO_PATH_ENTRY(A,U15); CRITICAL_TTC_START(B,A) |
| [06_tgm000.20.png](visual_audit_hardening/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_hardening/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [08_tgp000.10.png](visual_audit_hardening/08_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,B) |
| [09_tgp000.25.png](visual_audit_hardening/09_tgp000.25.png) | +0.25 | EGO_PATH_ENTRY(B,U11) |
| [10_tgp000.50.png](visual_audit_hardening/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.60.png](visual_audit_hardening/11_tgp000.60.png) | +0.60 | CRITICAL_TTC_START(A,U6) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -7.35 | U3 / U9 | drawn bodies overlap from here |
| road_users_overlap | -1.05 | U13 / U15 | drawn bodies overlap from here |
| road_users_overlap | +2.25 | U16 / U17 | drawn bodies overlap from here |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
