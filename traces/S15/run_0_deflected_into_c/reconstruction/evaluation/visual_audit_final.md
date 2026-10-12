# Visual audit (visual_audit_final): S15/run_0_deflected_into_c

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S15 | run_0_deflected_into_c | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm003.80.png](visual_audit_final/01_tgm003.80.png) | -3.80 | lead-in |
| [02_tgm001.30.png](visual_audit_final/02_tgm001.30.png) | -1.30 | CRITICAL_TTC_START(B,A) |
| [03_tgm001.25.png](visual_audit_final/03_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,B) |
| [04_tgm000.20.png](visual_audit_final/04_tgm000.20.png) | -0.20 | before COLLISION(A,B); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,A) |
| [05_tgm000.05.png](visual_audit_final/05_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,C); CRITICAL_TTC_START(C,A) |
| [06_tgp000.00.png](visual_audit_final/06_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| [07_tgp000.05.png](visual_audit_final/07_tgp000.05.png) | +0.05 | EGO_PATH_ENTRY(A,C) |
| [08_tgp000.40.png](visual_audit_final/08_tgp000.40.png) | +0.40 | EGO_PATH_ENTRY(C,A) |
| [09_tgp000.50.png](visual_audit_final/09_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [10_tgp000.70.png](visual_audit_final/10_tgp000.70.png) | +0.70 | before COLLISION(A,C) |
| [11_tgp000.90.png](visual_audit_final/11_tgp000.90.png) | +0.90 | COLLISION(A,C); CRITICAL_TTC_END(A,C); CRITICAL_TTC_END(C,A) |
| [12_tgp001.30.png](visual_audit_final/12_tgp001.30.png) | +1.30 | EGO_PATH_ENTRY(A,C) |
| [13_tgp001.40.png](visual_audit_final/13_tgp001.40.png) | +1.40 | after COLLISION(A,C) |
| [14_tgp001.55.png](visual_audit_final/14_tgp001.55.png) | +1.55 | EGO_PATH_ENTRY(B,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
