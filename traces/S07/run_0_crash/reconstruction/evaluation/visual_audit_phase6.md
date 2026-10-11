# Visual audit (visual_audit_phase6): S07/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Resolved since phase 2: recorder C is now aligned by its observed trajectory (line-of-sight entry distances; 0.05 s from simulator time, privileged) and replayed on t_global with A and B; B's track of C is linked to the recorder C, so no anonymous road user remains.  The chain reads as recorded: A's CRITICAL_TTC on B from -5.40 s, B's on C from -2.50 s while C brakes, the A-B collision at 0.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S07 | run_0_crash | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.95.png](visual_audit_phase6/01_tgm005.95.png) | -5.95 | lead-in |
| [02_tgm005.40.png](visual_audit_phase6/02_tgm005.40.png) | -5.40 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm002.50.png](visual_audit_phase6/03_tgm002.50.png) | -2.50 | CRITICAL_TTC_START(B,track_001 (C)) |
| [04_tgm001.55.png](visual_audit_phase6/04_tgm001.55.png) | -1.55 | CRITICAL_TTC_END(B,track_001 (C)) |
| [05_tgm000.20.png](visual_audit_phase6/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase6/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase6/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
