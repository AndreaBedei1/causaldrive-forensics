# Visual audit (visual_audit_review): S21/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

B passes A, A drifts into B, partner named (recorder link now correct). The other cars stay 20-40 m away: the dense passing is mostly ahead of the recorders. E split into several entities while relevant; far group with box jumps (U9) and 16 wrong samples on I (far, non relevant).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S21 | run_0 | WARN | +1.05..+4.10 | far boxes jump / overlap; E fragmented |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.75.png](visual_audit_review/01_tgm006.75.png) | -6.75 | lead-in |
| [02_tgm006.25.png](visual_audit_review/02_tgm006.25.png) | -6.25 | CRITICAL_TTC_START(A,U3) |
| [03_tgm006.15.png](visual_audit_review/03_tgm006.15.png) | -6.15 | CRITICAL_TTC_START(B,U1) |
| [04_tgm003.35.png](visual_audit_review/04_tgm003.35.png) | -3.35 | CUT_IN_FROM_RIGHT_START(B,A) |
| [05_tgm002.30.png](visual_audit_review/05_tgm002.30.png) | -2.30 | CUT_IN_FROM_RIGHT_END(B,A) |
| [06_tgm001.65.png](visual_audit_review/06_tgm001.65.png) | -1.65 | CRITICAL_TTC_START(A,B) |
| [07_tgm001.35.png](visual_audit_review/07_tgm001.35.png) | -1.35 | CRITICAL_TTC_START(B,A) |
| [08_tgm001.20.png](visual_audit_review/08_tgm001.20.png) | -1.20 | CRITICAL_TTC_START(A,U1) |
| [09_tgm001.10.png](visual_audit_review/09_tgm001.10.png) | -1.10 | EGO_PATH_ENTRY(A,U1) |
| [10_tgm000.50.png](visual_audit_review/10_tgm000.50.png) | -0.50 | EGO_PATH_ENTRY(B,A) |
| [11_tgm000.40.png](visual_audit_review/11_tgm000.40.png) | -0.40 | EGO_PATH_ENTRY(A,B) |
| [12_tgm000.20.png](visual_audit_review/12_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [13_tgp000.00.png](visual_audit_review/13_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); COLLISION(A,B) |
| [14_tgp000.10.png](visual_audit_review/14_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,U3) |
| [15_tgp000.15.png](visual_audit_review/15_tgp000.15.png) | +0.15 | EGO_PATH_ENTRY(B,U8) |
| [16_tgp000.45.png](visual_audit_review/16_tgp000.45.png) | +0.45 | EGO_PATH_ENTRY(B,U3) |
| [17_tgp000.50.png](visual_audit_review/17_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [18_tgp000.70.png](visual_audit_review/18_tgp000.70.png) | +0.70 | CRITICAL_TTC_END(A,U3) |
| [19_tgp000.80.png](visual_audit_review/19_tgp000.80.png) | +0.80 | CRITICAL_TTC_END(B,U1) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.65 | U5 / U6 | drawn bodies overlap from here |
| road_users_overlap | +1.05 | U8 / U9 | drawn bodies overlap from here |
| road_user_box_jump | +1.70 | U9 | box moved 5.0 m at 11.4 m/s |
| road_users_overlap | +1.85 | U12 / U13 | drawn bodies overlap from here |
| road_user_box_jump | +2.10 | U9 | box moved 4.8 m at 11.5 m/s |
| road_user_box_jump | +2.30 | U9 | box moved 4.7 m at 11.6 m/s |
| road_user_box_jump | +2.50 | U9 | box moved 4.4 m at 11.7 m/s |
| road_user_box_jump | +2.60 | U13 | box moved 4.1 m at 13.8 m/s |
| road_user_box_jump | +3.50 | U9 | box moved 4.3 m at 11.8 m/s |
| road_users_overlap | +3.55 | U11 / U14 | drawn bodies overlap from here |
| road_user_box_jump | +4.10 | U9 | box moved 4.3 m at 11.9 m/s |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
