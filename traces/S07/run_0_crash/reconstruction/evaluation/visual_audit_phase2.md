# Visual audit (visual_audit_phase2): S07/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Now replayed on t_global (phase 0: source clock).  Recorder C has no global clock -- its observed trajectory fits two offsets 0.35 s apart (C barely moves) -- so it is not replayed and the panel says so; B's track of C is the anonymous road user U1, drawn once.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S07 | run_0_crash | WARN | -5.90 .. | U1 (B:track_001) is the recorder C, which the reconstruction could not align: shown as an anonymous road user, C's own data not replayed | [03_tgm002.50.png](visual_audit_phase2/03_tgm002.50.png) | limitation: an observed alignment needs a moving target (phase 1 refused it, correctly ambiguous) |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.90.png](visual_audit_phase2/01_tgm005.90.png) | -5.90 | lead-in |
| [02_tgm005.40.png](visual_audit_phase2/02_tgm005.40.png) | -5.40 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm002.50.png](visual_audit_phase2/03_tgm002.50.png) | -2.50 | CRITICAL_TTC_START(B,track_001 (U1)) |
| [04_tgm001.55.png](visual_audit_phase2/04_tgm001.55.png) | -1.55 | CRITICAL_TTC_END(B,track_001 (U1)) |
| [05_tgm000.20.png](visual_audit_phase2/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase2/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase2/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
