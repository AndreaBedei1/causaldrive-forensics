# Visual audit (visual_audit_phase2): S01/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Rear-end: A critical on B 2.35 s before the contact; END with the COLLISION; bodies in contact. Unchanged since phase 0.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S01 | run_0_crash | PASS | -2.35 .. 0.00 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.35.png](visual_audit_phase2/01_tgm005.35.png) | -5.35 | lead-in |
| [02_tgm002.35.png](visual_audit_phase2/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm000.20.png](visual_audit_phase2/03_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [04_tgp000.00.png](visual_audit_phase2/04_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [05_tgp000.50.png](visual_audit_phase2/05_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
