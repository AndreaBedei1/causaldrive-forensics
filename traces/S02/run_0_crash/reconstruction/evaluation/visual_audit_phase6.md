# Visual audit (visual_audit_phase6): S02/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

B cuts in from the left ahead of A: CRITICAL_TTC, CUT_IN_FROM_LEFT and EGO_PATH_ENTRY in that order; unchanged since phase 0.  Phase 6: frames pixel-identical to the phase-2 frames inspected then; the verdict stands.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S02 | run_0_crash | PASS | -2.85 .. 0.00 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.65.png](visual_audit_phase6/01_tgm004.65.png) | -4.65 | lead-in |
| [02_tgm002.85.png](visual_audit_phase6/02_tgm002.85.png) | -2.85 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm002.55.png](visual_audit_phase6/03_tgm002.55.png) | -2.55 | CUT_IN_FROM_LEFT_START(A,track_001 (B)) |
| [04_tgm001.40.png](visual_audit_phase6/04_tgm001.40.png) | -1.40 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [05_tgm000.20.png](visual_audit_phase6/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase6/06_tgp000.00.png) | +0.00 | CUT_IN_FROM_LEFT_END(A,track_001 (B)); CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase6/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
