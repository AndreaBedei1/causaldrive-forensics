> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase2): S02/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

B cuts in from the left ahead of A: CRITICAL_TTC, CUT_IN_FROM_LEFT and EGO_PATH_ENTRY in that order; unchanged since phase 0.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S02 | run_0_crash | PASS | -2.85 .. 0.00 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.65.png](visual_audit_phase2/01_tgm004.65.png) | -4.65 | lead-in |
| [02_tgm002.85.png](visual_audit_phase2/02_tgm002.85.png) | -2.85 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm002.55.png](visual_audit_phase2/03_tgm002.55.png) | -2.55 | CUT_IN_FROM_LEFT_START(A,track_001 (B)) |
| [04_tgm001.40.png](visual_audit_phase2/04_tgm001.40.png) | -1.40 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [05_tgm000.20.png](visual_audit_phase2/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase2/06_tgp000.00.png) | +0.00 | CUT_IN_FROM_LEFT_END(A,track_001 (B)); CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase2/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
