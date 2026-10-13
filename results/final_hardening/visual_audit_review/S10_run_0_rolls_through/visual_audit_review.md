# Visual audit (visual_audit_review): S10/run_0_rolls_through

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Contact A-B matched and the recorder links kept; B's first track of the crossing A (22 m, -2.7..-1.5 s) stays anonymous (U1) and is drawn over A.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S10 | run_0_rolls_through | WARN | -2.70 | missed link of an early fragment (road user on recorder) |  | not tuned; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.05.png](visual_audit_review/01_tgm005.05.png) | -5.05 | lead-in |
| [02_tgm002.05.png](visual_audit_review/02_tgm002.05.png) | -2.05 | CRITICAL_TTC_START(A,B) |
| [03_tgm001.50.png](visual_audit_review/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,A) |
| [04_tgm000.25.png](visual_audit_review/04_tgm000.25.png) | -0.25 | EGO_PATH_ENTRY(A,B) |
| [05_tgm000.20.png](visual_audit_review/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_review/06_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| [07_tgp000.50.png](visual_audit_review/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_user_on_recorder | -2.70 | A / U1 | drawn bodies overlap from here |
| road_user_box_jump | -2.40 | U1 | box moved 3.2 m at 2.0 m/s |

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
