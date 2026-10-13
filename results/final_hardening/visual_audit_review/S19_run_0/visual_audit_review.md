# Visual audit (visual_audit_review): S19/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Scenario as specified (9 cars, 3 abreast rows, one A-B contact). Partner B named; 0 false merges, 5 wrong samples of 1258. Far rows fragmented (H, J: several entities, J never relevant) and C, E, F, G, H also split while relevant (21 missed merges).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S19 | run_0 | PASS | 0.00 | - |  | - |
| S19 | run_0 | WARN | -5.65..+2.25 | duplicates / fragmentation of relevant cars (U9/U10, U13/U15, U16/U17 overlap) |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.75.png](visual_audit_review/01_tgm007.75.png) | -7.75 | lead-in |
| [02_tgm007.25.png](visual_audit_review/02_tgm007.25.png) | -7.25 | CRITICAL_TTC_START(B,U3) |
| [03_tgm006.20.png](visual_audit_review/03_tgm006.20.png) | -6.20 | CRITICAL_TTC_START(A,U7) |
| [04_tgm001.40.png](visual_audit_review/04_tgm001.40.png) | -1.40 | CRITICAL_TTC_START(A,B) |
| [05_tgm001.10.png](visual_audit_review/05_tgm001.10.png) | -1.10 | CRITICAL_TTC_START(A,U3) |
| [06_tgm000.95.png](visual_audit_review/06_tgm000.95.png) | -0.95 | EGO_PATH_ENTRY(A,U3) |
| [07_tgm000.75.png](visual_audit_review/07_tgm000.75.png) | -0.75 | CRITICAL_TTC_START(B,A) |
| [08_tgm000.20.png](visual_audit_review/08_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [09_tgm000.15.png](visual_audit_review/09_tgm000.15.png) | -0.15 | CRITICAL_TTC_START(A,U6) |
| [10_tgp000.00.png](visual_audit_review/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [11_tgp000.10.png](visual_audit_review/11_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,B) |
| [12_tgp000.15.png](visual_audit_review/12_tgp000.15.png) | +0.15 | EGO_PATH_ENTRY(A,U7) |
| [13_tgp000.25.png](visual_audit_review/13_tgp000.25.png) | +0.25 | EGO_PATH_ENTRY(B,U11) |
| [14_tgp000.50.png](visual_audit_review/14_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [15_tgp000.95.png](visual_audit_review/15_tgp000.95.png) | +0.95 | EGO_PATH_ENTRY(B,U6); CRITICAL_TTC_START(B,U6) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -5.65 | U9 / U10 | drawn bodies overlap from here |
| road_users_overlap | -1.05 | U13 / U15 | drawn bodies overlap from here |
| road_users_overlap | +2.25 | U16 / U17 | drawn bodies overlap from here |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
