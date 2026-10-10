# Visual audit (visual_audit_phase2): S10/run_0_rolls_through

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Phase-0 WARN resolved: B's track of A is linked to A in the common frame (no second body on A, no post-impact ghost spin).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S10 | run_0_rolls_through | PASS | -2.00 .. +0.50 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.00.png](visual_audit_phase2/01_tgm005.00.png) | -5.00 | lead-in |
| [02_tgm002.00.png](visual_audit_phase2/02_tgm002.00.png) | -2.00 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm001.80.png](visual_audit_phase2/03_tgm001.80.png) | -1.80 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm000.20.png](visual_audit_phase2/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.15.png](visual_audit_phase2/05_tgm000.15.png) | -0.15 | EGO_PATH_ENTRY(B,track_001 (A)) |
| [06_tgm000.10.png](visual_audit_phase2/06_tgm000.10.png) | -0.10 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [07_tgp000.00.png](visual_audit_phase2/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
