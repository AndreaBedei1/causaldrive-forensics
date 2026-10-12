# Visual audit (visual_audit_final): S17/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S17 | run_0_crash | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.95.png](visual_audit_final/01_tgm004.95.png) | -4.95 | lead-in |
| [02_tgm002.35.png](visual_audit_final/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,U1) |
| [03_tgm002.20.png](visual_audit_final/03_tgm002.20.png) | -2.20 | CUT_IN_FROM_RIGHT_START(A,U1) |
| [04_tgm002.05.png](visual_audit_final/04_tgm002.05.png) | -2.05 | EGO_PATH_ENTRY(A,U1) |
| [05_tgm001.15.png](visual_audit_final/05_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,B) |
| [06_tgm000.80.png](visual_audit_final/06_tgm000.80.png) | -0.80 | CRITICAL_TTC_START(B,A) |
| [07_tgm000.50.png](visual_audit_final/07_tgm000.50.png) | -0.50 | CUT_IN_FROM_RIGHT_START(B,A) |
| [08_tgm000.40.png](visual_audit_final/08_tgm000.40.png) | -0.40 | EGO_PATH_ENTRY(B,A) |
| [09_tgm000.20.png](visual_audit_final/09_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [10_tgp000.00.png](visual_audit_final/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); EGO_PATH_ENTRY(A,B); CRITICAL_TTC_END(B,A); COLLISION(A,B) |
| [11_tgp000.40.png](visual_audit_final/11_tgp000.40.png) | +0.40 | CUT_IN_FROM_RIGHT_END(A,U1) |
| [12_tgp000.50.png](visual_audit_final/12_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [13_tgp000.55.png](visual_audit_final/13_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,U1) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
