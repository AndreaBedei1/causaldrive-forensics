# Visual audit (visual_audit_hardening): S17/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Collision A-B and the unobserved cut-in U1 are correct up to +0.5 s; the automatic flag reports a second anonymous body overlapping U1 from +1.75 s (post-impact duplicate, after the analysed window).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S17 | run_0_crash | PASS | 0.00 | - | [10_tgp000.00.png](visual_audit_hardening/10_tgp000.00.png) | - |
| S17 | run_0_crash | WARN | 1.75 | U1 / U2 drawn bodies overlap (likely one car split after the crash) |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.95.png](visual_audit_hardening/01_tgm004.95.png) | -4.95 | lead-in |
| [02_tgm002.35.png](visual_audit_hardening/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,U1) |
| [03_tgm002.20.png](visual_audit_hardening/03_tgm002.20.png) | -2.20 | CUT_IN_FROM_RIGHT_START(A,U1) |
| [04_tgm002.05.png](visual_audit_hardening/04_tgm002.05.png) | -2.05 | EGO_PATH_ENTRY(A,U1) |
| [05_tgm001.15.png](visual_audit_hardening/05_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,B) |
| [06_tgm000.80.png](visual_audit_hardening/06_tgm000.80.png) | -0.80 | CRITICAL_TTC_START(B,A) |
| [07_tgm000.50.png](visual_audit_hardening/07_tgm000.50.png) | -0.50 | CUT_IN_FROM_RIGHT_START(B,A) |
| [08_tgm000.40.png](visual_audit_hardening/08_tgm000.40.png) | -0.40 | EGO_PATH_ENTRY(B,A) |
| [09_tgm000.20.png](visual_audit_hardening/09_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [10_tgp000.00.png](visual_audit_hardening/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); EGO_PATH_ENTRY(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [11_tgp000.40.png](visual_audit_hardening/11_tgp000.40.png) | +0.40 | CUT_IN_FROM_RIGHT_END(A,U1) |
| [12_tgp000.50.png](visual_audit_hardening/12_tgp000.50.png) | +0.50 | CRITICAL_TTC_END(A,U1); after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | +1.75 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `e2cd1c5274e1ff54971be53f88fdfe0a6222a014`.
