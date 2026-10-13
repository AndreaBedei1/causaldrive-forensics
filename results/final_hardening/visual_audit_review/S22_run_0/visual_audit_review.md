# Visual audit (visual_audit_review): S22/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

V hides B from A, B reappears, both merge and collide, partner named; 0 wrong samples, B kept as one road user across the occlusion. G (following car) split while relevant; one lead-in overlap.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S22 | run_0 | WARN | -7.00, +1.20, +3.70 | lead-in overlap U3/U6, box jumps after the contact |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.30.png](visual_audit_review/01_tgm007.30.png) | -7.30 | lead-in |
| [02_tgm006.80.png](visual_audit_review/02_tgm006.80.png) | -6.80 | CRITICAL_TTC_START(B,U5) |
| [03_tgm001.95.png](visual_audit_review/03_tgm001.95.png) | -1.95 | CRITICAL_TTC_START(A,U1) |
| [04_tgm001.80.png](visual_audit_review/04_tgm001.80.png) | -1.80 | CRITICAL_TTC_START(A,B) |
| [05_tgm001.75.png](visual_audit_review/05_tgm001.75.png) | -1.75 | CRITICAL_TTC_START(B,A); CRITICAL_TTC_START(B,U1) |
| [06_tgm001.55.png](visual_audit_review/06_tgm001.55.png) | -1.55 | EGO_PATH_ENTRY(A,U1) |
| [07_tgm001.45.png](visual_audit_review/07_tgm001.45.png) | -1.45 | EGO_PATH_ENTRY(B,U1) |
| [08_tgm001.10.png](visual_audit_review/08_tgm001.10.png) | -1.10 | CRITICAL_TTC_END(B,U5) |
| [09_tgm000.45.png](visual_audit_review/09_tgm000.45.png) | -0.45 | CRITICAL_TTC_START(A,U5) |
| [10_tgm000.40.png](visual_audit_review/10_tgm000.40.png) | -0.40 | CUT_IN_FROM_LEFT_START(A,U5) |
| [11_tgm000.35.png](visual_audit_review/11_tgm000.35.png) | -0.35 | EGO_PATH_ENTRY(B,A) |
| [12_tgm000.20.png](visual_audit_review/12_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [13_tgp000.00.png](visual_audit_review/13_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B) |
| [14_tgp000.10.png](visual_audit_review/14_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,U5) |
| [15_tgp000.20.png](visual_audit_review/15_tgp000.20.png) | +0.20 | CUT_IN_FROM_RIGHT_START(B,A) |
| [16_tgp000.35.png](visual_audit_review/16_tgp000.35.png) | +0.35 | CRITICAL_TTC_END(A,U1); EGO_PATH_ENTRY(B,U5) |
| [17_tgp000.50.png](visual_audit_review/17_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [18_tgp000.55.png](visual_audit_review/18_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,U5) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -7.00 | U3 / U6 | drawn bodies overlap from here |
| road_user_box_jump | +1.20 | U8 | box moved 3.4 m at 8.7 m/s |
| road_user_box_jump | +3.70 | U2 | box moved 4.0 m at 12.0 m/s |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
