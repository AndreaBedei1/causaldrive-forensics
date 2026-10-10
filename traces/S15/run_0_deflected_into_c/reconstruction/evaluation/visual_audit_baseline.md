# Visual audit (visual_audit_baseline): S15/run_0_deflected_into_c

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

B into A at 0.00, A deflected into C at +0.90, each episode ends at the collision of its own pair; B:track_001 switches from C to A at the A-C contact (ground truth); several anonymous ghosts of recorders.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S15 | run_0_deflected_into_c | WARN | +0.15 .. +1.15 | B:track_001 follows C, then A after A is pushed into C (track identity switch); its episode from +0.15 concerns C, not a post-impact episode with A | [07_tgp000.15.png](visual_audit_baseline/07_tgp000.15.png) | PHASE 1 metrics (purity); reported |
| S15 | run_0_deflected_into_c | WARN | -1.30 .. | anonymous ghosts of recorders (C:track_002 = B, B:track_001) | [02_tgm001.30.png](visual_audit_baseline/02_tgm001.30.png) | PHASE 1: association |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm003.80.png](visual_audit_baseline/01_tgm003.80.png) | -3.80 | lead-in |
| [02_tgm001.30.png](visual_audit_baseline/02_tgm001.30.png) | -1.30 | CRITICAL_TTC_START(B,track_002 (A)) |
| [03_tgm001.25.png](visual_audit_baseline/03_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.20.png](visual_audit_baseline/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.05.png](visual_audit_baseline/05_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,track_001 (C)); EGO_PATH_ENTRY(B,track_002 (A)); CRITICAL_TTC_START(C,track_001 (A)) |
| [06_tgp000.00.png](visual_audit_baseline/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [07_tgp000.15.png](visual_audit_baseline/07_tgp000.15.png) | +0.15 | CRITICAL_TTC_START(B,track_001) |
| [08_tgp000.50.png](visual_audit_baseline/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [09_tgp000.55.png](visual_audit_baseline/09_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.70.png](visual_audit_baseline/10_tgp000.70.png) | +0.70 | before COLLISION(A,C) |
| [11_tgp000.90.png](visual_audit_baseline/11_tgp000.90.png) | +0.90 | CRITICAL_TTC_END(A,track_001 (C)); CRITICAL_TTC_END(C,track_001 (A)); COLLISION(A,C) |
| [12_tgp001.25.png](visual_audit_baseline/12_tgp001.25.png) | +1.25 | CRITICAL_TTC_END(B,track_001) |
| [13_tgp001.40.png](visual_audit_baseline/13_tgp001.40.png) | +1.40 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| ghost_box_jump | +0.10 | C:track_002 | box centre moved 3.8 m, track point 0.2 m |

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
