# Visual audit (visual_audit_final): S10/run_0_rolls_through

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S10 | run_0_rolls_through | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.00.png](visual_audit_final/01_tgm005.00.png) | -5.00 | lead-in |
| [02_tgm002.00.png](visual_audit_final/02_tgm002.00.png) | -2.00 | CRITICAL_TTC_START(A,B) |
| [03_tgm001.80.png](visual_audit_final/03_tgm001.80.png) | -1.80 | CRITICAL_TTC_START(B,A) |
| [04_tgm000.30.png](visual_audit_final/04_tgm000.30.png) | -0.30 | EGO_PATH_ENTRY(B,A) |
| [05_tgm000.25.png](visual_audit_final/05_tgm000.25.png) | -0.25 | EGO_PATH_ENTRY(A,B) |
| [06_tgm000.20.png](visual_audit_final/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_final/07_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| [08_tgp000.50.png](visual_audit_final/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
