# Visual audit (visual_audit_review): S17/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Collision and unobserved cut-in U1 correct; post-impact overlap U1/U2 at +1.75 s.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S17 | run_0_crash | WARN |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.95.png](visual_audit_review/01_tgm004.95.png) | -4.95 | lead-in |
| [02_tgm002.40.png](visual_audit_review/02_tgm002.40.png) | -2.40 | CRITICAL_TTC_START(A,U1) |
| [03_tgm002.20.png](visual_audit_review/03_tgm002.20.png) | -2.20 | CUT_IN_FROM_RIGHT_START(A,U1); CUT_IN_FROM_RIGHT_START(B,A) |
| [04_tgm002.10.png](visual_audit_review/04_tgm002.10.png) | -2.10 | EGO_PATH_ENTRY(A,U1) |
| [05_tgm001.15.png](visual_audit_review/05_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,B) |
| [06_tgm001.05.png](visual_audit_review/06_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(B,A) |
| [07_tgm000.90.png](visual_audit_review/07_tgm000.90.png) | -0.90 | EGO_PATH_ENTRY(B,A) |
| [08_tgm000.20.png](visual_audit_review/08_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [09_tgp000.00.png](visual_audit_review/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [10_tgp000.35.png](visual_audit_review/10_tgp000.35.png) | +0.35 | CUT_IN_FROM_RIGHT_END(A,U1) |
| [11_tgp000.50.png](visual_audit_review/11_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [12_tgp000.55.png](visual_audit_review/12_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,U1) |
| [13_tgp000.60.png](visual_audit_review/13_tgp000.60.png) | +0.60 | CUT_IN_FROM_RIGHT_START(B,U1) |
| [14_tgp000.70.png](visual_audit_review/14_tgp000.70.png) | +0.70 | EGO_PATH_ENTRY(B,A) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | +1.75 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
