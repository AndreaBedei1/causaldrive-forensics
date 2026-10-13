# Visual audit (visual_audit_review): S20/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Column of 4 + staggered side lanes, B rear-ends A, partner named; 0 wrong samples. G (beside A/B) drawn twice (U6 from A, U8 from B) while relevant; U8 spins at the impact.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S20 | run_0 | WARN | -7.35..+0.10 | G duplicated across recorders (U6/U8), box spin |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.45.png](visual_audit_review/01_tgm007.45.png) | -7.45 | lead-in |
| [02_tgm006.95.png](visual_audit_review/02_tgm006.95.png) | -6.95 | CRITICAL_TTC_START(A,U2) |
| [03_tgm006.90.png](visual_audit_review/03_tgm006.90.png) | -6.90 | CRITICAL_TTC_START(B,A) |
| [04_tgm000.90.png](visual_audit_review/04_tgm000.90.png) | -0.90 | CRITICAL_TTC_START(A,U6); CRITICAL_TTC_START(A,U7) |
| [05_tgm000.65.png](visual_audit_review/05_tgm000.65.png) | -0.65 | CRITICAL_TTC_END(A,U2) |
| [06_tgm000.40.png](visual_audit_review/06_tgm000.40.png) | -0.40 | CRITICAL_TTC_END(A,U7) |
| [07_tgm000.25.png](visual_audit_review/07_tgm000.25.png) | -0.25 | CRITICAL_TTC_END(A,U6) |
| [08_tgm000.20.png](visual_audit_review/08_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [09_tgp000.00.png](visual_audit_review/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [10_tgp000.50.png](visual_audit_review/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.80.png](visual_audit_review/11_tgp000.80.png) | +0.80 | EGO_PATH_ENTRY(A,U4) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -7.35 | U6 / U8 | drawn bodies overlap from here |
| road_users_overlap | -1.05 | U5 / U9 | drawn bodies overlap from here |
| road_user_box_jump | +0.10 | U8 | box moved 6.1 m at 4.1 m/s |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
