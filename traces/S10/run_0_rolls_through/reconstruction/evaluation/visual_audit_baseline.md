# Visual audit (visual_audit_baseline): S10/run_0_rolls_through

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Junction collision consistent; the track of A by B stays anonymous (ghost box offset about 1.5 m on A) and its box jumps and spins right after the impact.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S10 | run_0_rolls_through | WARN | -1.80 .. +0.50 | B:track_001 (A) anonymous: a second body on A | [03_tgm001.80.png](visual_audit_baseline/03_tgm001.80.png) | PHASE 1: association with recorder poses |
| S10 | run_0_rolls_through | WARN | 0.00 | ghost box jump and spin at the impact | [07_tgp000.00.png](visual_audit_baseline/07_tgp000.00.png) | post-impact; PHASE 1 fused footprint |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.00.png](visual_audit_baseline/01_tgm005.00.png) | -5.00 | lead-in |
| [02_tgm002.00.png](visual_audit_baseline/02_tgm002.00.png) | -2.00 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm001.80.png](visual_audit_baseline/03_tgm001.80.png) | -1.80 | CRITICAL_TTC_START(B,track_001) |
| [04_tgm000.20.png](visual_audit_baseline/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.15.png](visual_audit_baseline/05_tgm000.15.png) | -0.15 | EGO_PATH_ENTRY(B,track_001) |
| [06_tgm000.10.png](visual_audit_baseline/06_tgm000.10.png) | -0.10 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [07_tgp000.00.png](visual_audit_baseline/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_baseline/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| ghost_box_jump | +0.00 | B:track_001 | box centre moved 3.7 m, track point 0.4 m |
| ghost_box_spin | +0.00 | B:track_001 | heading turned 51 deg |

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
