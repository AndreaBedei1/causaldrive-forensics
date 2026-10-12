# Visual audit (visual_audit_final): S01/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PENDING**

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S01 | run_0_crash | PENDING |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.35.png](visual_audit_final/01_tgm005.35.png) | -5.35 | lead-in |
| [02_tgm002.35.png](visual_audit_final/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,B) |
| [03_tgm000.20.png](visual_audit_final/03_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [04_tgp000.00.png](visual_audit_final/04_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,B); COLLISION(A,B) |
| [05_tgp000.50.png](visual_audit_final/05_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.
