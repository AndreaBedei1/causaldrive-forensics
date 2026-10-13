# Visual audit (visual_audit_review): S23/run_0

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **FAIL**

Contact A-B named and C/D never merged (2 wrong samples), but the scenario objective is not met: C and D, which A swerves around, stay split into 4 entities each while inside the relevance envelope (22 missed merges) instead of being resolved as they come close.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S23 | run_0 | FAIL | -4.0..0.0 | C and D fragmented inside the relevance envelope |  | not tuned; open algorithmic issue |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm008.50.png](visual_audit_review/01_tgm008.50.png) | -8.50 | lead-in |
| [02_tgm006.70.png](visual_audit_review/02_tgm006.70.png) | -6.70 | CRITICAL_TTC_START(A,U1) |
| [03_tgm006.55.png](visual_audit_review/03_tgm006.55.png) | -6.55 | CUT_IN_FROM_RIGHT_START(A,U1) |
| [04_tgm005.85.png](visual_audit_review/04_tgm005.85.png) | -5.85 | CUT_IN_FROM_RIGHT_END(A,U1); CRITICAL_TTC_END(A,U1) |
| [05_tgm003.05.png](visual_audit_review/05_tgm003.05.png) | -3.05 | CRITICAL_TTC_START(A,U3) |
| [06_tgm002.90.png](visual_audit_review/06_tgm002.90.png) | -2.90 | CUT_IN_FROM_RIGHT_START(A,U3) |
| [07_tgm002.35.png](visual_audit_review/07_tgm002.35.png) | -2.35 | CRITICAL_TTC_END(A,U3) |
| [08_tgm002.30.png](visual_audit_review/08_tgm002.30.png) | -2.30 | CUT_IN_FROM_RIGHT_END(A,U3) |
| [09_tgm001.35.png](visual_audit_review/09_tgm001.35.png) | -1.35 | CRITICAL_TTC_START(A,B) |
| [10_tgm000.90.png](visual_audit_review/10_tgm000.90.png) | -0.90 | CRITICAL_TTC_START(B,A) |
| [11_tgm000.45.png](visual_audit_review/11_tgm000.45.png) | -0.45 | CRITICAL_TTC_START(A,U10) |
| [12_tgm000.20.png](visual_audit_review/12_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [13_tgm000.05.png](visual_audit_review/13_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,U11) |
| [14_tgp000.00.png](visual_audit_review/14_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); EGO_PATH_ENTRY(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [15_tgp000.30.png](visual_audit_review/15_tgp000.30.png) | +0.30 | CRITICAL_TTC_END(A,U11) |
| [16_tgp000.50.png](visual_audit_review/16_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [17_tgp000.60.png](visual_audit_review/17_tgp000.60.png) | +0.60 | EGO_PATH_ENTRY(B,A) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.30 | U6 / U7 | drawn bodies overlap from here |
| road_users_overlap | -5.90 | U6 / U8 | drawn bodies overlap from here |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
