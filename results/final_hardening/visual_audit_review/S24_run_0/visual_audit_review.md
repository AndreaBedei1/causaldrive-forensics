# Visual audit (visual_audit_review): S24/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

A hits B between C and D: partner B named (not C or D); the post-contact same-pair CRITICAL_TTC is gone. A's view of B is split into 3 entities, D, E, F likewise (14 missed merges); A starts CRITICAL_TTC with U7 (D) after the impact (a different pair).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S24 | run_0 | PASS | 0.00 | - |  | - |
| S24 | run_0 | WARN | -7.7..+1.85 | B, D, E, F fragmented while relevant; overlaps after the contact |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.75.png](visual_audit_review/01_tgm007.75.png) | -7.75 | lead-in |
| [02_tgm007.25.png](visual_audit_review/02_tgm007.25.png) | -7.25 | CRITICAL_TTC_START(B,U5) |
| [03_tgm006.30.png](visual_audit_review/03_tgm006.30.png) | -6.30 | CRITICAL_TTC_START(A,B) |
| [04_tgm006.25.png](visual_audit_review/04_tgm006.25.png) | -6.25 | CUT_IN_FROM_RIGHT_START(A,U7) |
| [05_tgm006.00.png](visual_audit_review/05_tgm006.00.png) | -6.00 | CUT_IN_FROM_RIGHT_END(A,U7) |
| [06_tgm000.80.png](visual_audit_review/06_tgm000.80.png) | -0.80 | CUT_IN_FROM_RIGHT_START(A,U7) |
| [07_tgm000.20.png](visual_audit_review/07_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [08_tgm000.05.png](visual_audit_review/08_tgm000.05.png) | -0.05 | CUT_IN_FROM_RIGHT_END(A,U7) |
| [09_tgp000.00.png](visual_audit_review/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); COLLISION(A,B) |
| [10_tgp000.45.png](visual_audit_review/10_tgp000.45.png) | +0.45 | EGO_PATH_ENTRY(A,U7); CRITICAL_TTC_START(A,U7) |
| [11_tgp000.50.png](visual_audit_review/11_tgp000.50.png) | +0.50 | CRITICAL_TTC_END(B,U5); after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | +1.05 | U7 / U11 | drawn bodies overlap from here |
| road_user_box_jump | +1.30 | U13 | box moved 3.8 m at 10.4 m/s |
| road_users_overlap | +1.75 | U12 / U14 | drawn bodies overlap from here |
| road_users_overlap | +1.85 | U13 / U15 | drawn bodies overlap from here |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
