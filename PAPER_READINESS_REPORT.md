# Paper readiness report

Target: a journal of the IEEE Intelligent Transportation Systems Society.  Paper scope: multi-vehicle
accident reconstruction from partial onboard recordings -- collision-anchored temporal alignment,
identity association between recorders, reconstruction and fusion of road users that recorded nothing,
a global semantic event trace, a replay built only from the reconstruction, and per-vehicle event graphs
that expose when a hazard became perceivable from each vehicle's onboard sensors and when the vehicle
reacted.  The reconstruction supports an expert's avoidability analysis; it never decides avoidability
or liability, and sensor perception is not a driver's mental perception.  The LLM pipeline and the
temporal-logic verifier stay in the repository as future work, out of the paper: no LLM API call is made
anywhere in this work.

Non-negotiable rules applied in every phase: the reconstruction, the fusion and the standard replay never
read ground truth, run metadata, scenario configurations, actor ids or the identities of non-recording
participants; ground truth is used only by the evaluation; a non-recording road user stays anonymous
(U1, U2, ...); errors are given in physical units (m, m/s, ms, deg) as distributions; nothing is tuned per
scenario.

Phase starting point: `215170a1d7f1a87cc455eb85d718183c1fcee7b9` (2026-10-10).

## Phase 0 -- baseline / regression audit

**Objective.**  Regenerate the 14 canonical runs with the current code, define the paper's core event view,
audit every run visually and semantically from the reconstruction alone, audit it separately against
ground truth, and fix any FAIL before the anonymous-road-user fusion.

**Implementation.**
- Regeneration of the 14 canonical runs from the same raw files (`scripts/reconstruct_run.py --evaluate`,
  `scripts/export_forensic_facts.py`, derived files).  The generators of the derived campaign files, so far
  ad-hoc, are now in the repository: `scripts/campaign_summary.py`, `scripts/report_sequences.py`.
- Paper core view: `cdf.reconstruction.models.PAPER_CORE_EVENTS` (COLLISION, BRAKE, CUT_IN, EGO_PATH_ENTRY,
  CRITICAL_TTC, TRACK_APPEARED, TRACK_LOST); the other events stay in the graphs.
- Headless replay export: `scripts/replay_run.py --export DIR [--at T ...] [--format png|svg|pdf]`, a
  top-down renderer of the replay model (`cdf.replay.topdown`) with no CARLA server; lanes from the public
  OpenDRIVE file of the map recognised from the recorded positions.  Keyframes from the reconstructed events.
- Automatic visual-QA checks (`cdf.replay.qa`, reconstruction only) and the audit driver
  `scripts/visual_audit.py` (evaluation side), reviewer verdicts in `docs/audit/visual_audit_baseline_verdicts.json`.
- Privileged ground-truth audit: `cdf.evaluation.gt_audit`, `scripts/gt_audit.py`.
- Fix (FAIL found by the audit, S09): CRITICAL_TTC release also requires that no line-of-sight contact is
  imminent (`conflict.py` point 5, `ConflictAssessment.contact_imminent`).

**Assumptions.**  The recorders' `ego.jsonl` poses are the recorded GNSS-like pose stream (in CARLA they are
exact; the robustness phase perturbs them).  The ground-truth audit takes a vehicle's bounding box as centred
on its origin in the horizontal plane (CARLA offsets of a few centimetres) and the recorders' raw clocks as
the simulator clock (privileged assumption, evaluation only).

**Tests.**  396 tests pass on Python 3.8 (CARLA environment) and Python 3.14, among them new
`tests/test_replay_export.py` (core view, keyframes, exact states at the collision, frame contents, QA checks
on S17 and synthetic runs), new anti-leak test of the headless export on a poisoned copy of S17
(`tests/test_replay_ghosts.py`, which also checks the new modules' sources for privileged names), the
imminent-contact release and the S09 regression (`tests/test_critical_release.py`).

**Results.**
- Regeneration: 562 raw and ground-truth files byte-identical; the 14 forensic packets byte-identical.
  Against the outputs of 2026-10-09 only CRITICAL_TTC events changed: 16 ENDs moved to the collision of their
  own pair, S06/run_0_b_rear_first A->B CRITICAL_TTC_START 4.65 -> 4.70 s (safe-gap simplification).
- Visual audit of the 14 runs (127 keyframes, all inspected; `traces/visual_audit_baseline.md`):
  7 PASS, 7 WARN, 0 open FAIL.  FAIL found and fixed: S09 A->B CRITICAL_TTC ended 0.80 s before the collision
  with B 2-3 m away and closing at 1.6-3.5 m/s (line-of-sight time to contact 0.66-0.83 s); it now ends at the
  collision.  WARNs: anonymous ghosts of recorders (S07, S08, S10, S15, S16) and of the non-recorder C (S17,
  three ghosts) -- the target of phase 1; post-impact ghost boxes turning while their observer spins (S08,
  S10); S15 B:track_001 switching identity at the A-C contact; S16 C's episode on A open at TRACK_LOST 0.15 s
  before their contact; S07 and S08 replayed on source time (recorder C has no collision to be aligned).
- Ground-truth audit (`traces/gt_audit_baseline.md`, 4761 track samples): track point to the true outline
  median 0.20 m (p95 0.60 m); nominal box centre error median 0.86 m, IQR 2.02 m, p95 3.59 m, max 5.28 m (worst
  S09, S10); speed error median 0.04 m/s (p95 0.90 m/s); heading error median 1.2 deg (p95 10.6 deg).
  Identity purity 1.0 except S08 C:track_001 / C:track_002 and S15 B:track_001.  Collisions: every true
  vehicle contact reconstructed, associations all correct (evaluation.json of each run).
- S17 coherent (A critical on C from -2.35 s, CUT_IN -2.20 s, path entry -1.60 s; A-B and B-A end at the
  collision, A on C at +0.55 s); S02 critical_before_cut_in preserved (CRITICAL_TTC 2.60 s < CUT_IN 2.95 s).

**Regressions.**  None open.  The S09 fix changes two ENDs in the campaign (S09 A->B to the collision, S15
B on B:track_001 +0.10 s after the collision); no START changes.

**Limitations.**  The nominal box (4.6 x 1.9 m behind the near surface) is a large error source for the
centre (p95 3.6 m) -- addressed by the face correction of phase 1.  Collision-free recorders cannot be
aligned by collisions (S07, S08 C).  The 2-D prediction keeps a constant-velocity target (S09); the
imminent-contact release prevents the premature END but not a late START.

**Commit.**  `phase0: baseline regeneration, headless replay export, visual and ground-truth audit, S09 fix`
(SHA recorded in the phase 1 section).

**Gate.**  PASS: full tests green on Python 3.8 and 3.14; all canonical runs reconstructible and regenerated;
replay without privileged input (poisoned tests); no open visual FAIL; S17 coherent; S02
critical-before-cut-in preserved; campaign outputs aligned with the current code.
