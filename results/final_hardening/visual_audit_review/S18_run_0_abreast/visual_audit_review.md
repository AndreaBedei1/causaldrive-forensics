# Visual audit (visual_audit_review): S18/run_0_abreast

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Collision A-B, no flag, 0 false merges.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_abreast | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_review/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.65.png](visual_audit_review/02_tgm005.65.png) | -5.65 | CRITICAL_TTC_START(A,U2) |
| [03_tgm001.05.png](visual_audit_review/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,B) |
| [04_tgm000.65.png](visual_audit_review/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,A) |
| [05_tgm000.45.png](visual_audit_review/05_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,U2) |
| [06_tgm000.20.png](visual_audit_review/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_review/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [08_tgp000.10.png](visual_audit_review/08_tgp000.10.png) | +0.10 | EGO_PATH_ENTRY(A,B) |
| [09_tgp000.50.png](visual_audit_review/09_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
