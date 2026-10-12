> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_final): S18/run_0_passing

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_passing | WARN |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_final/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.55.png](visual_audit_final/02_tgm005.55.png) | -5.55 | CRITICAL_TTC_START(A,track_003 (U2)) |
| [03_tgm001.40.png](visual_audit_final/03_tgm001.40.png) | -1.40 | CRITICAL_TTC_START(A,track_001#segment_3 (U2)) |
| [04_tgm001.05.png](visual_audit_final/04_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [05_tgm000.65.png](visual_audit_final/05_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [06_tgm000.45.png](visual_audit_final/06_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_001#segment_3 (U2)) |
| [07_tgm000.20.png](visual_audit_final/07_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [08_tgp000.00.png](visual_audit_final/08_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [09_tgp000.50.png](visual_audit_final/09_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
