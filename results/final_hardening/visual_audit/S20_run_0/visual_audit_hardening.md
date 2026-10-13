# Visual audit (visual_audit_hardening): S20/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

B rear-ends A, named correctly (the collision lost during development is back); a transient duplicate U5/U8 in the right lane at -1.05 s ends when B's track is lost.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S20 | run_0 | WARN | -1.05 | U5 / U8 transient duplicate | [05_tgm000.90.png](visual_audit_hardening/05_tgm000.90.png) | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.45.png](visual_audit_hardening/01_tgm007.45.png) | -7.45 | lead-in |
| [02_tgm006.95.png](visual_audit_hardening/02_tgm006.95.png) | -6.95 | CRITICAL_TTC_START(A,U2) |
| [03_tgm006.90.png](visual_audit_hardening/03_tgm006.90.png) | -6.90 | CRITICAL_TTC_START(B,A) |
| [04_tgm000.95.png](visual_audit_hardening/04_tgm000.95.png) | -0.95 | CRITICAL_TTC_START(A,U7) |
| [05_tgm000.90.png](visual_audit_hardening/05_tgm000.90.png) | -0.90 | CRITICAL_TTC_START(A,U6) |
| [06_tgm000.65.png](visual_audit_hardening/06_tgm000.65.png) | -0.65 | CRITICAL_TTC_END(A,U2) |
| [07_tgm000.40.png](visual_audit_hardening/07_tgm000.40.png) | -0.40 | CRITICAL_TTC_END(A,U7) |
| [08_tgm000.30.png](visual_audit_hardening/08_tgm000.30.png) | -0.30 | CRITICAL_TTC_END(A,U6) |
| [09_tgm000.20.png](visual_audit_hardening/09_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [10_tgp000.00.png](visual_audit_hardening/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [11_tgp000.50.png](visual_audit_hardening/11_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [12_tgp000.90.png](visual_audit_hardening/12_tgp000.90.png) | +0.90 | EGO_PATH_ENTRY(A,U4) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -1.05 | U5 / U8 | drawn bodies overlap from here |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
