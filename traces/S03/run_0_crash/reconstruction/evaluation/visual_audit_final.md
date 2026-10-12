# Visual audit (visual_audit_final): S03/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S03 | run_0_crash | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_final/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.55.png](visual_audit_final/02_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,B) |
| [03_tgm001.50.png](visual_audit_final/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,A) |
| [04_tgm000.20.png](visual_audit_final/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgp000.00.png](visual_audit_final/05_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [06_tgp000.50.png](visual_audit_final/06_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [07_tgp000.65.png](visual_audit_final/07_tgp000.65.png) | +0.65 | EGO_PATH_ENTRY(B,A) |
| [08_tgp000.90.png](visual_audit_final/08_tgp000.90.png) | +0.90 | EGO_PATH_ENTRY(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
