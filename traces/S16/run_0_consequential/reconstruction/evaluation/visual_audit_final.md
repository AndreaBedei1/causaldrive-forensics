# Visual audit (visual_audit_final): S16/run_0_consequential

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S16 | run_0_consequential | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.55.png](visual_audit_final/01_tgm005.55.png) | -5.55 | lead-in |
| [02_tgm005.05.png](visual_audit_final/02_tgm005.05.png) | -5.05 | CRITICAL_TTC_START(B,A) |
| [03_tgm000.40.png](visual_audit_final/03_tgm000.40.png) | -0.40 | EGO_PATH_ENTRY(A,C) |
| [04_tgm000.35.png](visual_audit_final/04_tgm000.35.png) | -0.35 | CRITICAL_TTC_START(A,C) |
| [05_tgm000.20.png](visual_audit_final/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_final/06_tgp000.00.png) | +0.00 | COLLISION(A,B); CRITICAL_TTC_END(B,A) |
| [07_tgp000.05.png](visual_audit_final/07_tgp000.05.png) | +0.05 | CRITICAL_TTC_START(C,A) |
| [08_tgp000.50.png](visual_audit_final/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [09_tgp000.85.png](visual_audit_final/09_tgp000.85.png) | +0.85 | before COLLISION(A,C) |
| [10_tgp001.05.png](visual_audit_final/10_tgp001.05.png) | +1.05 | COLLISION(A,C) |
| [11_tgp001.55.png](visual_audit_final/11_tgp001.55.png) | +1.55 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
