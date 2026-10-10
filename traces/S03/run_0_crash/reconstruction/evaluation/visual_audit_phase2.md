# Visual audit (visual_audit_phase2): S03/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Crossing: both recorders critical about 1.5 s before; B strikes the side of A; both episodes end with the collision; unchanged.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S03 | run_0_crash | PASS | -1.55 .. 0.00 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_phase2/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.55.png](visual_audit_phase2/02_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm001.50.png](visual_audit_phase2/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm000.20.png](visual_audit_phase2/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgp000.00.png](visual_audit_phase2/05_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [06_tgp000.50.png](visual_audit_phase2/06_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
