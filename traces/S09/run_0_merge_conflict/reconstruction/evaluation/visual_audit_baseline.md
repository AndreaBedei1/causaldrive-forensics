# Visual audit (visual_audit_baseline): S09/run_0_merge_conflict

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

FAIL found and fixed: the CRITICAL_TTC of A on B ended 0.80 s before the collision while B, merging along a curve, was 2-3 m away and closing at 1.6-3.5 m/s (line-of-sight time to contact 0.66-0.83 s); the release now waits until no line-of-sight contact is imminent; both episodes end at the collision.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S09 | run_0_merge_conflict | FAIL (fixed) | -0.80 | premature CRITICAL_TTC_END(A, B): the straight-line target prediction misses the curved merge of B while the radar shows B closing with a 0.66-0.83 s time to contact | [05_tgm000.20.png](visual_audit_baseline/05_tgm000.20.png) | release condition: no imminent line-of-sight contact (closing >= 1 m/s and clearance < 1 s x closing speed); END now at the collision |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.95.png](visual_audit_baseline/01_tgm007.95.png) | -7.95 | lead-in |
| [02_tgm004.95.png](visual_audit_baseline/02_tgm004.95.png) | -4.95 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [03_tgm003.60.png](visual_audit_baseline/03_tgm003.60.png) | -3.60 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm003.35.png](visual_audit_baseline/04_tgm003.35.png) | -3.35 | CRITICAL_TTC_START(A,track_001 (B)) |
| [05_tgm000.20.png](visual_audit_baseline/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_baseline/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_baseline/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
