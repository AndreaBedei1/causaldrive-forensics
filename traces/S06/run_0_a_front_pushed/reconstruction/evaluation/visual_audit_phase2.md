# Visual audit (visual_audit_phase2): S06/run_0_a_front_pushed

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Chain A->B->C with three contacts; every episode ends at the collision of its own pair; unchanged.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S06 | run_0_a_front_pushed | PASS | -4.30 .. +1.15 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.80.png](visual_audit_phase2/01_tgm004.80.png) | -4.80 | lead-in |
| [02_tgm004.30.png](visual_audit_phase2/02_tgm004.30.png) | -4.30 | CRITICAL_TTC_START(A,track_001 (B)); CRITICAL_TTC_START(B,track_001 (C)) |
| [03_tgm000.20.png](visual_audit_phase2/03_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [04_tgp000.00.png](visual_audit_phase2/04_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [05_tgp000.30.png](visual_audit_phase2/05_tgp000.30.png) | +0.30 | before COLLISION(B,C) |
| [06_tgp000.45.png](visual_audit_phase2/06_tgp000.45.png) | +0.45 | before COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase2/07_tgp000.50.png) | +0.50 | CRITICAL_TTC_END(B,track_001 (C)); after COLLISION(A,B); COLLISION(B,C) |
| [08_tgp000.65.png](visual_audit_phase2/08_tgp000.65.png) | +0.65 | COLLISION(A,B) |
| [09_tgp001.00.png](visual_audit_phase2/09_tgp001.00.png) | +1.00 | after COLLISION(B,C) |
| [10_tgp001.15.png](visual_audit_phase2/10_tgp001.15.png) | +1.15 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
