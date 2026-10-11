# Visual audit (visual_audit_phase6): S06/run_0_b_rear_first

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

B into C at -1.55, A critical on the stopped chain, A into B at 0.00; unchanged.  Phase 6: frames pixel-identical to the phase-2 frames inspected then; the verdict stands.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S06 | run_0_b_rear_first | PASS | -5.75 .. +0.50 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.25.png](visual_audit_phase6/01_tgm006.25.png) | -6.25 | lead-in |
| [02_tgm005.75.png](visual_audit_phase6/02_tgm005.75.png) | -5.75 | CRITICAL_TTC_START(B,track_001 (C)) |
| [03_tgm001.75.png](visual_audit_phase6/03_tgm001.75.png) | -1.75 | before COLLISION(B,C) |
| [04_tgm001.55.png](visual_audit_phase6/04_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (C)); COLLISION(B,C) |
| [05_tgm001.05.png](visual_audit_phase6/05_tgm001.05.png) | -1.05 | after COLLISION(B,C) |
| [06_tgm000.20.png](visual_audit_phase6/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_phase6/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_phase6/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
