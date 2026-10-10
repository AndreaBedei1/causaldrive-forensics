# Visual audit (visual_audit_phase2): S12/run_0_near_simultaneous

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

All-way stop: both critical about 1.2 s before, B enters the path of A, collision; unchanged.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S12 | run_0_near_simultaneous | PASS | -1.25 .. +0.50 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.25.png](visual_audit_phase2/01_tgm004.25.png) | -4.25 | lead-in |
| [02_tgm001.25.png](visual_audit_phase2/02_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm001.10.png](visual_audit_phase2/03_tgm001.10.png) | -1.10 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm000.40.png](visual_audit_phase2/04_tgm000.40.png) | -0.40 | EGO_PATH_ENTRY(B,track_001 (A)) |
| [05_tgm000.20.png](visual_audit_phase2/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase2/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase2/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
