# Visual audit (visual_audit_final): S09/run_0_merge_conflict

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S09 | run_0_merge_conflict | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm008.05.png](visual_audit_final/01_tgm008.05.png) | -8.05 | lead-in |
| [02_tgm005.05.png](visual_audit_final/02_tgm005.05.png) | -5.05 | EGO_PATH_ENTRY(A,B) |
| [03_tgm003.60.png](visual_audit_final/03_tgm003.60.png) | -3.60 | CRITICAL_TTC_START(B,A) |
| [04_tgm003.35.png](visual_audit_final/04_tgm003.35.png) | -3.35 | CRITICAL_TTC_START(A,B) |
| [05_tgm000.35.png](visual_audit_final/05_tgm000.35.png) | -0.35 | EGO_PATH_ENTRY(B,A) |
| [06_tgm000.20.png](visual_audit_final/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_final/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_final/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [09_tgp000.60.png](visual_audit_final/09_tgp000.60.png) | +0.60 | EGO_PATH_ENTRY(B,A) |
| [10_tgp000.85.png](visual_audit_final/10_tgp000.85.png) | +0.85 | EGO_PATH_ENTRY(B,A) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
