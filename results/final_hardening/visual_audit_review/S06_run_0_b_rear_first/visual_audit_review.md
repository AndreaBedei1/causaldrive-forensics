# Visual audit (visual_audit_review): S06/run_0_b_rear_first

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

B-C then A-B named; no flag.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S06 | run_0_b_rear_first | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.25.png](visual_audit_review/01_tgm006.25.png) | -6.25 | lead-in |
| [02_tgm005.75.png](visual_audit_review/02_tgm005.75.png) | -5.75 | CRITICAL_TTC_START(B,C) |
| [03_tgm001.75.png](visual_audit_review/03_tgm001.75.png) | -1.75 | before COLLISION(B,C) |
| [04_tgm001.55.png](visual_audit_review/04_tgm001.55.png) | -1.55 | CRITICAL_TTC_END(B,C); COLLISION(B,C) |
| [05_tgm001.05.png](visual_audit_review/05_tgm001.05.png) | -1.05 | after COLLISION(B,C) |
| [06_tgm000.20.png](visual_audit_review/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_review/07_tgp000.00.png) | +0.00 | COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_review/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `30e54a5a3179833cfc0d8a023b78d54825ade943`.
