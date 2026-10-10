# Visual audit (visual_audit_baseline): S01/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Rear-end: A critical on B 2.35 s before the contact (B braking ahead); END with the COLLISION; bodies in contact at the collision.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S01 | run_0_crash | PASS | -2.35 .. 0.00 | none: CRITICAL_TTC from -2.35 to the collision, positions and headings plausible | [02_tgm002.35.png](visual_audit_baseline/02_tgm002.35.png) | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.35.png](visual_audit_baseline/01_tgm005.35.png) | -5.35 | lead-in |
| [02_tgm002.35.png](visual_audit_baseline/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm000.20.png](visual_audit_baseline/03_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [04_tgp000.00.png](visual_audit_baseline/04_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [05_tgp000.50.png](visual_audit_baseline/05_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
