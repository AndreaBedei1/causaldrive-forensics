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

**Commit.**  `9ad719fa3d5a98a95eb0baae4f068cd3b90582bb` -- `phase0: baseline regeneration, headless replay export,
visual and ground-truth audit, S09 fix`.

**Gate.**  PASS: full tests green on Python 3.8 and 3.14; all canonical runs reconstructible and regenerated;
replay without privileged input (poisoned tests); no open visual FAIL; S17 coherent; S02
critical-before-cut-in preserved; campaign outputs aligned with the current code.

## Phase 1 -- fusion of road users that recorded nothing

**Objective.**  One anonymous road user (U1, U2, ...) per physical road user that recorded nothing, from the
recorders' own data: a common frame, cross-observer association, face correction, same-observer stitching,
a multi-observer box fit with uncertainty, `anonymous_entities.json`; positive cases S17, S16, S08; a new
negative scenario; metrics against ground truth.

**Implementation.**
- 1A common frame (`cdf.reconstruction.common_frame`): `PoseSource` (a recorder's pose by its own clock,
  declaring its position, heading and velocity accuracy), `RecordedPoseSource` (the recorded `ego.jsonl`
  stream: the GNSS-like baseline, exact in CARLA; the robustness phase substitutes a perturbed source through
  `reconstruct_run(..., pose_factory=...)`), every track sample with its point, observed near surface,
  ground velocity, line of sight and -- in memory only, never written -- the radar returns it claimed with
  their radars' positions (`tracking.py` keeps them on the track).
- Observed alignment (`anonymous.align_by_observations`) of a recorder no matched collision aligned:
  near surfaces against footprint outlines over candidate clock offsets, pooled over the comparisons that fit
  somewhere, moving targets only; accepted when the offsets within `max(3 x best, 2 sigma)` form one interval
  (`GraphClock.method = observed_trajectories`, decisions in `alignment.json` and `anonymous_entities.json`).
- Recorder links (`link_to_recorders`): an anonymous track whose returns lie on another recorder's own
  footprint at its own velocity is that recorder; the evidence stops at the recorder's first contact with a
  third body; a track that afterwards lies clearly off it switched body and stays anonymous.
- 1B/1C/1E association and face correction (`pair_evidence`, `fit_box`): the returns of each observer are
  assigned to the box faces visible from their own radar; each face is two linear constraints (offset along
  its normal, position along it); one rigid box (centre, half length, half width with priors, heading from
  the motion) for both observers against two separate boxes: chi-square difference (2 dof) and velocity
  chi-square at 99 % on at least 80 % of at least 10 shared instants.  The same test detects a tracker
  splitting one body into two simultaneous tracks of one observer.
- 1D stitching (`stitch_evidence`): constant-velocity prediction across a loss of at most 1.5 s, uncertainty
  growing with the tracker's unmodelled acceleration; S17 B:track_002 -> B:track_003 after 0.75 s (miss
  2.16 m, d^2 1.63) is kept as two `source_track_segments`.
- Conservative clustering (`refuse_ambiguous`, `cluster`): a link with a rival is refused; an entity never
  holds two simultaneous tracks of one observer unless a link showed them to be one body.
- 1E fused state (`entity_trajectory`, 10 Hz): one box fitted to all observers' faces when they fix it (two
  faces or two observers); otherwise covariance intersection of the observers' centre estimates.  Choice:
  a track-level fusion of points is biased (two radars see different faces: their points differ by up to a
  car length, 2.4 m in S17), the box explains the faces; covariance intersection is the fallback because the
  observers' estimates share the target's unmodelled motion and their cross-correlation is unknown.
- 1F `global/anonymous_entities.json`: per entity `id`, `anonymous: true`, `source_tracks`,
  `source_track_segments`, `observers`, `time_span`, association links and confidence, `fusion_method`,
  footprint (value, source fitted / prior / observed extent, spread), trajectory (position, velocity, heading
  and its source, uncertainty, method, observers); plus the observed alignments, the recorder links and the
  evidence of every pair.  The global graph names anonymous road users U1, U2, ... (`models.is_anonymous_entity`).
- `pipeline.fuse_recorders` runs every cross-recorder step; the evaluation's clock-shift check uses it too.
- 1H S18 anonymous_pair (configs/scenarios/s18_anonymous_pair.yaml): C and D record nothing and drive close
  together at about the same speed ahead of A and B -- abreast (1.4 m apart), platoon (8 m), passing (D
  overtaking C) -- then A drifts into B (their contact aligns the clocks).  Recorded on the private engine
  (port 3000), each run matching a lab run of the same variant within 0.15 m.
- 1I `cdf.evaluation.fusion_metrics` and `scripts/fusion_metrics.py` (privileged), with
  `cdf.evaluation.provenance` (git commit, code and configuration hashes, runs, time).
- The LLM oracle mode (offline, evaluation only) maps anonymous entity names too; no LLM call.

**Assumptions** (engineering choices unless stated).  Road users are rigid boxes; the heading is the direction
of motion (held when slow); length 4.6 +- 0.7 m and width 1.9 +- 0.2 m priors (the reconstruction's nominal
box; cars to vans); returns spread 0.25 m around a face (bumpers, mirrors, wheels); gates at 99 % of
chi-square with 2 dof, 80 % of instants, at least 10 instants; stitching across at most 1.5 s; the observed
alignment uses targets faster than 2 m/s and requires one interval at 3x the best score; recorder links need
80 % of at least 10 samples within 3 sigma, sigma from the tracker's measurement noise and the pose sources'
declared accuracy.  Mutual-track refinement of the pose sources is not implemented: with exact recorded poses
there is nothing to refine or measure; it is designed for phase 4, where perturbed poses make baseline vs
refined measurable.

**Tests.**  418 pass on Python 3.8 (CARLA environment) and Python 3.14.  New `tests/test_road_user_fusion.py`
(22): box fit from two observers' faces, prior along a single face, covariance intersection never tighter than
an independence fusion, one box seen from two sides is one road user, two cars abreast and two in a platoon
stay two, stitching and its refusals, ambiguous successors and simultaneous partners refused, clusters never
hold simultaneous tracks of one observer, samples carried in time, chi-square quantiles; on the canonical runs:
S17 U1 from three tracks with a cross link and a stitch, the global graph names U1 and never C, a poisoned copy
(ground truth and run metadata naming C and its track) gives identical outputs, renamed recorders give the same
road user, the fusion source names no scenario, participant or privileged field, S16 van tracks -> C, S08 C
aligned by its observed trajectory, S07 C refused.  Updated: the weak-collision-evidence test (collision-based
association alone vs the common-frame link), the S17 anonymity test (U1).

**Results** (traces/fusion_metrics.md, CAMPAIGN_REPORT section 5.13).
- Identity decisions of the aligned recorders' tracks: 41 correct links, **0 wrong**, 4 missed (S07 C
  unaligned; S08 C:track_002 and S15 B:track_001 switch body at a contact with a third vehicle; S16 B:track_004,
  0.3 s after the contacts).
- S17: U1 = A:track_001 + B:track_002 + B:track_003, purity 1.00.  S16: the van's tracks A:track_002, B:track_002,
  B:track_003 -> C.  S08: C aligned at -4.10 s (true -4.10 s, interval [-4.20, -3.75] s), A:track_001 and
  B:track_001 -> C, C:track_001 -> A.  S10 B:track_001 -> A.  S07: C refused (offsets -5.95 and -5.60 s both fit).
- Negative case S18: **0 false merges** in all three variants; fragments only (C in 2 entities in each variant,
  D in 1, 1 and 2).  Over the campaign: merges 15 correct, 0 false, 10 missed; 15 entities, purity median 1.00
  (min 0.63); entities per true road user median 1, max 2.
- Fused state over 1062 pure instants: centre error median 0.39 m, IQR 0.54, p90 1.42, p95 1.51, max 6.59 m (box
  fit: median 0.27 m) against the phase-0 nominal ghost box of each source track at the same instants: median
  0.57 m, p95 3.53 m.  Velocity error median 0.12 m/s (p95 0.69); speed 0.05 m/s (p95 0.27); heading 0.53 deg
  (p95 2.8; max 177 deg in a post-impact slide, S15).  Footprint: length error median 0.19 m (max 1.3 m: a van
  seen 0.3 s), width 0.26 m; mostly the prior (opposite faces are rarely seen).  Coverage per entity median 9.0 s.
  Calibration: 0.60 / 0.92 / 0.97 of the errors within 1 / 2 / 3 declared sigma (Gaussian 0.39 / 0.86 / 0.99).
- Clock-shift check: global graph identical in all 17 runs (S08: the observed alignment absorbs the 0.73 s shift).
- Cost: cross-recorder steps 0.03-1.3 s per canonical run, 3.7-5.9 s per S18 run; `anonymous_entities.json`
  684 kB over 17 runs; S18 raw recordings 40 MB.

**Regressions.**  None: local outputs byte-identical over all runs; every collision and every association
of phase 0 unchanged (evaluation headlines); global names changed where intended (U entities, new links).
The LLM forensic packets were not re-exported (LLM pipeline out of the paper; stored analyses refer to them).

**Limitations.**  Identity is per track: a track that switches body at a contact stays anonymous (two cases)
instead of being split.  A recorder at rest or moving along its own outline cannot be aligned by observation
(S07).  Fragmentation is the price of conservative gates (S18: 10 missed merges); a local tracker mixing two
cars 1.4 m apart (S18 abreast, A:track_001 purity 0.73) also yields a spurious CUT_IN in A's local graph
(phase 5).  Heading from motion fails in post-impact slides.  The declared position uncertainty is
conservative in the bulk with a heavier tail.  Box dimensions mostly come from the prior.  An observed alignment
is not propagated through a matched collision between two recorders that are both unaligned (no such case).

**Commit.**  `c79b1e627cbfaa5c042749291876597e922509f7` -- `phase1: road users in the common frame of the
recorders' pose streams; S18 negative case`.

**Gate.**  PASS: S17 / S16 / S08 correct; the negative case passes (0 false merges in three configurations);
no ground truth at runtime (boundary, poisoned-copy and renamed-recorder tests); tests green on both Pythons;
metrics produced with provenance.

## Phase 2 -- definitive replay

**Objective.**  A replay built only from the reconstruction, on t_global, with recorders at the poses of their
pose source, one body per anonymous road user with its uncertainty, no privileged input, audited visually.

**Implementation.**
- `cdf.replay.model`: GLOBAL_CLOCK whenever a recorder is aligned (a recorder without a global clock is not
  replayed: `ReplayRun.hidden`, a note); SOURCE_CLOCK only when none is.  `ReplayRun.load(pose_factory=...)`
  draws each recorder from its pose source (`Participant.trajectory`; the recorded stream kept as
  `Participant.recorded` for the local headings); a track sample is placed by its vehicle-frame measurement
  from its observer's pose.  `EntityPath` / `EntityState` / `load_entities` read `global/anonymous_entities.json`:
  one road user with its fitted footprint, fused states, uncertainty, method and observers;
  `TrackPath.road_user` marks the tracks it fuses (no ghost of their own), `subject_name` gives
  `track_001 (U1)`, `entities_at(t)`.
- `cdf.replay.topdown`: one grey box per road user (solid measured, dashed predicted), a dotted circle of
  twice its position uncertainty when that exceeds 0.3 m, the source tracks' radar points in their observers'
  colours, its states (CRITICAL_TTC / CUT_IN / IN_EGO_PATH of any observer on its tracks), a panel line
  `U1 = A:track_001 + B:track_002 + B:track_003` with footprint, speed, +-sigma and method, and the recorders not
  on the timeline.
- CARLA viewer (`scripts/replay_run.py`): the same road users as wireframe boxes with labels (sources,
  +-sigma, observers), member tracks as dots, panels `sees road users: U1 (track_001)`; `--port` to choose
  the server.  Smoke-tested headless (SDL dummy driver) on the private engine (port 3000) for S17, S18
  platoon and S07: road users drawn with labels, no error.
- `cdf.replay.qa`: road-user speed / jump / spin, two road users overlapping, a road user on a recorder's body.
- Visual audit `visual_audit_phase2` (17 runs, 151 keyframes).

**Assumptions.**  The drawn footprint is the fitted one, else the prior; heading unknown -> parallel to the
first observer (no arrow), as the CRITICAL_TTC model takes it; the entity grid is the 10 Hz global grid, so a
road user appears up to 0.1 s after its first radar sample.

**Tests.**  422 pass on Python 3.8 and 3.14.  New / updated: S17 shows the non-recorder once (U1) while both
recorders track it; the tracks are drawn as the fusion decided (no ghost of their own); the road users come from
the reconstruction, never from the evaluation (poisoned fusion metrics and LLM oracle naming C); a pose source
moves the recorders and what they observe together (constant 2 m / 1 m offset); the poisoned-copy comparison
now covers road users, links and hidden recorders; an unaligned recorder is not replayed and the replay says
so; the source clock only when no recorder is aligned; the headless export of S17 flags nothing; the viewer's
only configuration read is the simulator connection.  The anti-leak tests poison ground truth (states with
actor ids, collisions, triggers, counterfactuals, its metadata), the run's metadata, a scenario YAML beside the
run, the evaluation (true identities of tracks and of U1), the LLM oracle identities and a vehicle folder with
no recording; an audit hook checks every file opened.

**Results.**  Visual audit: 10 PASS, 7 WARN, 0 FAIL (phase 0: 7 PASS, 7 WARN over 14 runs).  Resolved: S17,
S10; S08, S15, S16 without ghosts of recorders.  Remaining WARNs, all documented limitations: identity switches
at contacts (S08, S15), an unaligned recorder (S07), a post-contact fragment and an episode open at TRACK_LOST
(S16), fragmentation and two spurious CUT_IN / EGO_PATH_ENTRY caused by A's radar clustering two cars 1.4 m
apart (S18 abreast, passing).  The pose-based placement of the tracks agrees with the local-frame one to the
millimetre (fusion metrics' single-track baseline 0.5714 vs 0.5715 m median).

**Regressions.**  None in the reconstruction (unchanged).  Replay behaviour changed on purpose: S07 is now on
t_global without C (phase 0: source clock with C).

**Limitations.**  Uncertainty is shown for position only (heading and footprint spreads are in the files, not
drawn); with a perturbed pose source the recorded headings still orient the track velocities in the vehicle
frame (exact odometry assumption); an unaligned recorder cannot be shown at all.

**Commit.**  Phase 1: `c79b1e627cbfaa5c042749291876597e922509f7`.  Phase 2:
`c80eab47ec83dcc66909751b0514f1bcb4d5066e`.

**Gate.**  PASS: t_global only; poses from the pose source; one body per road user with its uncertainty;
anti-leak tests green; visual audit of every run with no FAIL; tests green on both Pythons.

## Phase 3 -- scenario sweeps

**Objective.**  Scale the evaluation beyond the canonical runs without overwriting them: parameterised sweeps
of six scenario families with a per-run manifest, a batch runner that resumes, logs failures and never
overwrites, a pilot that sizes N from data, and a balance of crash, borderline and no-crash outcomes.

**Implementation.**
- `configs/sweeps/*.yaml`: rear_end (S01: speeds, gap, A's brake time, B's brake intensity), cut_in (S02),
  crossing (S03), unobserved_cut_in (S17), anonymous_pair_adjacent and anonymous_pair_platoon (S18: D's
  position relative to C and its speed, B's spawn).
- `scripts/run_sweep.py`: run k takes the k-th Halton point shifted by a SHA-256 of the sweep's seed (every
  prefix covers the ranges; runs never change once recorded); variants through `--override`, recorded by the
  unchanged `run_scenario.py` on a private CARLA (port 3000, real-time pacing on) into `sweeps/` (git-ignored),
  never `traces/`; `sweep_manifest.json` per run (sweep, scenario, variants, k, seed, parameters, code at
  recording and at reconstruction: commit, dirty flag, code hash; wall times; outcome from ground truth: crash,
  borderline under 1 m checked at every simulator frame, no crash; metrics; status); a completed run is
  skipped, an incomplete one set aside, failures logged; `--reconstruct-only` redoes the analysis of every
  recorded run; summaries with provenance in `results/sweeps/<sweep>.{json,md,csv}`.
- `scripts/experiment_size.py`: per paper metric a bootstrap (2000 replicates) of the campaign statistic from
  the first 5 runs at N = 5 ... 100, the rule of three for errors never seen, a cap of 40 runs (recording
  budget), settling tables over all runs, campaign totals (`docs/experiment_size.md`).
- Reconstruction, no ground truth:
  - The observed alignment compares each observed near surface with where its own line of sight enters the
    other recorder's footprint (entry distances) instead of with the nearest point of the whole outline (an
    "inside" degeneracy had biased it by 0.3 s): S07's C is aligned (-5.95 s, true -5.90 s), S08's interval
    narrows to [-4.20, -4.00] s.
  - With no matched collision at all (a near miss) the first recorder's own clock is the global one
    (`reference_recorder`) and the others are aligned to it by observation.
  - Contact gate of the collision matching (found by the sweeps): in five crossing near misses each car ran into
    roadside objects with impulses within 3-8 % of each other, and the impulse test matched the two
    single-vehicle contacts as one A-B collision -- a fabricated collision and clocks off by 0.25-4.9 s.  A
    match now also needs the two bodies to touch, each at its own report time from its own pose stream:
    footprints within `contact_consistency_m` = 1.0 m + 3 sigma of the declared pose accuracy.  Over the
    campaign every genuine match lies within 0.06 m, the rejected ones 54-73 m apart.
  - A guard against a NaN start of the box fit; `offset_decision` extracted (tested on synthetic score curves).
- Evaluation: event times and alignment against the reference recorder's clock in near misses (the pilot
  reported errors of thousands of seconds); `cdf.evaluation.run_metrics`.
- Operations: unpaced runs hung the engine, so pacing is on by default; the private engine still crashed (a
  C++ runtime dialog) every few runs whenever heavy analysis ran in parallel: a supervisor outside the
  repository restarted it and resumed the batch, stopping only processes with `-carla-rpc-port=3000`.  The
  user's server on port 2000 was never touched.

**Assumptions.**  Parameter ranges are engineering choices that keep each scenario's question; outcome classes
from ground truth (evaluation only); the S18 sweeps crash by design (A drifts into B to give the alignment an
anchor; the question there is the fusion of C and D).

**Tests.**  `tests/test_sweeps.py` (13: Halton determinism and coverage, seed shifts, ranges, decimals, `also`
and `relative_to`, variant overrides, the variant builds a valid scenario, run naming, set-aside never deletes,
outcomes from ground truth, entry distances, the reference recorder, near-miss evaluation on its clock);
`tests/test_multi_collision.py` (contact gate: two contacts far apart are not one; footprint gap);
`tests/test_road_user_fusion.py` (S07 aligned along the lines of sight; refusal of non-unique offsets).

**Results** (`results/sweeps/`, `docs/experiment_size.md`, table T2).
- 240 runs, 6 x 40, all complete after the reconstruct-only refresh with the final code (one reconstruction
  code hash over the 240 manifests).  Outcomes crash / borderline / no crash: rear_end 8/4/28, cut_in
  17/2/21, crossing 18/7/15, unobserved_cut_in 32/0/8, the two S18 sweeps 40/0/0.
- N from the pilot: 40 (capped) for four sweeps, 30 for cut_in, 34 for unobserved_cut_in (40 recorded each);
  the binding needs are the rule of three for errors never seen and the median fused centre error, whose
  five-value bootstrap cannot narrow.
- Alignment: every recorder of every run on t_global; event times within 0.05 s (one radar period) of the truth
  in all 240 runs; relative clock offsets within 0.05 s.  Every true collision between recorders reconstructed;
  no fabricated collision once the contact gate is in.
- Identities: 397/397 decided tracks correct; recorder links 0 wrong in 464 trials (95 % upper bound 0.65 %);
  67 tracks of a recorder left anonymous, 55 of them in crossing near misses, where the tracker's velocity of a
  crossing target is about 1 m/s off (twice its declared RMS uncertainty) and the link test refuses them.  An
  offline what-if testing the velocity separately along the line of sight (Doppler) and across it would recover
  16 of the 68 with no wrong link: left as an improvement.
- Road users that recorded nothing: 3 false merges in 503 trials, all in the side-by-side S18 configuration
  where a recorder's tracker mixes the returns of the two cars 1.4 m apart into one track.  Fused centre error
  against the single-track nominal box, paired per run: unobserved_cut_in 0.12 m vs 0.51 m (fused better in
  39/40 runs), crossing 0.54 vs 0.79 m (22/23), side-by-side pair 0.32 vs 0.40 m (36/40), platoon 0.44 vs 0.39 m
  (19/40: no gain when every observer sees only rear faces).
- Cost: recording 29-38 s per run (median per sweep), reconstruction 1.7-9.3 s, evaluation 0.1-9.0 s; storage
  3.15 GB of raw recordings (12.1 MB per run) and 0.28 GB of reconstructions, outside the repository; the
  canonical traces are regenerated with the final code (substantive outputs unchanged since the start of phase
  3 except S07 / S08, as intended).

**Regressions.**  Canonical: S07 and S08 change as intended; every other canonical reconstruction is unchanged
(only configuration keys and evidence text).  Canonical fusion metrics: 42 correct links (was 41), 3 missed
(was 4), merges unchanged.

**Limitations.**  Borderline outcomes are rare in some families; the S18 sweeps cannot test near misses; the
recording budget caps N at 40 and several metrics are reported at the precision 40 runs give.

**Commit.**  `phase3: ...` (SHA in the phase 4 section).

**Gate.**  PASS: canonical runs untouched by the sweeps; manifests with provenance; resumable batch with
failure logging and no overwrite; N chosen from data; outcomes balanced where the scenario allows; the full
suite passes on both Pythons (464 tests at the end of the program).

## Phase 4 -- robustness

**Objective.**  A non-destructive perturbation layer and a robustness study: radar noise, missed detections
and clutter from sourced profiles; GNSS errors that reach the common frame, the fusion and the replay;
collision-report impulse noise and latency, with CARLA's symmetric impulses documented and checked on the
multi-vehicle runs; constant clock offsets; downsampling; a missing recorder; a radar outage; seeded draws
with a stopping rule; metrics against the level of each perturbation with plots; and the optional mutual
refinement of the pose sources measured against the plain reconstruction.

**Implementation.**
- `cdf.robustness.perturb`: `perturbed_copy` writes a new folder (an existing one is refused), hard-links
  every file it does not change and records the condition (`perturbation.json`, never read by the
  reconstruction).  Radar (`RadarProfile`, `perturb_sweeps`): per-detection drop, Gaussian range / azimuth /
  elevation / radial-velocity noise, Poisson clutter uniform in the field of view with a static-world or a
  mirrored Doppler.  GNSS (`GnssProfile`, `PerturbedPoseSource`): per axis a run bias, a first-order
  Gauss-Markov term and white noise drawn at a receiver rate, a heading error with the same terms and a
  velocity noise; the source declares its accuracy (root sum of squares) and enters through the
  reconstruction's `pose_factory`.  Collision reports (`CollisionPerturbation`): multiplicative impulse noise
  per callback, latency of one recorder, drops.  Constant clock offsets of every time a recorder wrote,
  downsampling of ego, controls and radar, a recorder left out, a radar outage.  Every random quantity has its
  own SHA-256-seeded stream.
- Profiles with their sources or engineering assumptions: `docs/robustness_profiles.md` (drafted from the
  research notes by a sub-agent, reviewed; two incomplete references completed from their DOIs; three source
  comments in the code corrected).
- `scripts/robustness.py`: families x levels x runs, `ProcessPoolExecutor`, seeds 0, 1, 2, ... until the
  standard error over seeds of every pooled metric is below its tolerance (3 to 8 seeds); per job the
  unchanged reconstruction, the privileged evaluation, the fusion metrics and the core-event diff against the
  unperturbed reconstruction (`cdf.evaluation.run_metrics.core_event_diff`, which first removes a shift of
  the clock origin); `results/robustness/jobs.jsonl`, `summary.{json,md,csv}`, `figures/` (one per family,
  plain and refined GNSS overlaid).
- `scripts/impulse_symmetry.py` (privileged): the two reports of every true contact in the ground-truth log,
  the matched pairs with their nearest competing report, and the Monte Carlo survival of the alignment's
  impulse test under per-report noise (`results/robustness/impulse_symmetry.md`).
- Mutual refinement (`fusion.mutual_refinement`, off by default; `anonymous.mutual_offsets`), rebuilt after a
  first version corrected only one component and declared far too small an uncertainty.  The returns of every
  track identified with a recorder, before that recorder's first contact (in contact the boxes overlap and a
  radar can sit inside the other body), are assigned to the faces of its box that their radar can see (the
  radar on the outer side of the face plane) by segment distance; each face gives n . (b_R - b_O) = its median
  depth, with a systematic variance shared by the face's heading bins plus the spread over the distinct
  seconds; the offsets are the maximum a posteriori estimate with each source's declared accuracy as a
  zero-mean prior (unobservable directions stay uncorrected), the posterior inflated by the reduced
  chi-square above one.  The face assignment starts from a correlative scan match of each observer's returns
  on each recorder and then uses the estimate where the faces inform it and the scan match where they do not
  (a pull-back to the prior along an unobserved direction had recreated the biased geometry).  Two stages:
  the collision-identified tracks, then every link found on the corrected poses.
- `cdf.evaluation.figures`: the paper's figure style (IEEE widths, TrueType fonts, text as text).

**Assumptions.**  Vendor accuracies read as 1 sigma; radar errors independent per detection, clutter uniform;
GNSS errors are a translation plus a heading error, independent between vehicles, stationary over a run, with
exact odometry; the refinement estimates translations only; the impulse tolerance of the alignment
(`fusion.impulse_tolerance` = 0.10) is an engineering assumption.  All in `docs/robustness_profiles.md`.

**Tests.**  `tests/test_robustness.py` (16): radar drop rate, noise sigmas and Poisson clutter in the field of
view with its Doppler model; ideal changes nothing and the profiles are ordered; GNSS bias, Gauss-Markov and
white spreads; a perturbed source declares its accuracy and is reproducible; streams independent of the order
of drawing; the copy hard-links what it does not change and never overwrites; clock offsets shift every time a
recorder wrote (signs included), downsampling, dropout, collision latency; constant clock offsets leave the
global graph unchanged; the refinement recovers a 3.5 m relative bias seen from two directions (S17), leaves
the unobservable lateral of a rear-end follow untouched with its prior uncertainty (S01) and does nothing to
exact sources; face depths, face visibility from the radar's side, a radar inside the box, the scan match of
a 3.8 m offset.

**Results** (`results/robustness/summary.md`, final code with the phase-3 contact gate: 1389 jobs, 0 failed, 4.3 CPU
hours, median 5.7 s per job; the copies are deleted, so storage stays at the results: 2.6 MB).
- Baseline copies reproduce the canonical reconstruction exactly.  Constant clock offsets (+7.31, -14.62,
  +21.93 s ...) leave all 17 global graphs identical, once the traffic-sign stream's own time fields were
  shifted too: the first run found 14/17, the three others differing only in their STOP_SIGN events.
- Radar: low and nominal noise keep every identity, collision and alignment (core events 0.97 found again,
  centre error 0.41 / 0.51 m against 0.41 m); the high profile (30 clutter returns per sweep) costs 1.3 % of
  the identities and 2 % of the alignments, adds about 800 clutter entities and 236 spurious core events per
  draw over the 17 runs, and 15 false merges; centre error 1.27 m.
- GNSS: RTK changes nothing (centre error 0.43 m).  Consumer (1.66 m per axis): identities and collisions
  intact, 96 % of the runs fully aligned, centre error 2.99 m, 19 false merges per draw; with the mutual
  refinement 2.00 m and 8.6 false merges.  Degraded (5.43 m): identity accuracy 0.950 (refined 0.964), centre
  error 6.58 m (refined 5.24 m), false merges 19.5 (refined 21.5: no gain).  The common part of the errors
  stays in the map frame and in every absolute position.
- Refinement alone (pure 2 m biases, 17 runs x 3 seeds, 87 recorder pairs): no pair inconsistent with its
  posterior (largest Mahalanobis^2 10.3, none above the 99.9 % bound 13.8); where both directions are seen (53
  pairs) the median relative bias falls from 2.80 m to 0.18 m; 84/87 pairs improve; the others keep the prior.
- Collision reports: CARLA gives both bodies of a contact the same impulse magnitude (largest relative
  difference 0.0 over all runs).  The alignment's 10 % impulse test keeps a pair with probability 1.00 / 0.86 /
  0.54 / 0.29 at 2 / 5 / 10 / 20 % independent error per report; in the study 10 % noise leaves 41 % of the
  collisions matched and 87 % of the runs fully aligned (the observed-trajectory alignment recovers part), 20 %
  29 % and 84 %.  S06's two contacts of B have peaks 14.5 % apart: noise can make them compete, and only the
  clock consistency of earlier matches separates them.  A report latency on one recorder shifts its events by
  the latency (event time p95 = latency) and degrades the fused positions from 0.05 s on (0.76 m at 0.05 s,
  1.09 m at 0.10 s); at 0.25-0.5 s the recorder links fail (11-20 missed) instead of linking wrongly, and the
  contact gate refuses some genuine matches (the late report puts the two bodies 1.7 m apart): collisions 0.86 /
  0.82, runs fully aligned 0.88 / 0.94.  The alignment assumes report times within its 0.1 s clock tolerance;
  without the gate those matches went through with clocks off by the latency.
- Downsampling to 10 Hz is nearly free (core events 0.99); 5 Hz costs identities (0.976), collisions
  (0.955) and core events (0.91).  A missing recorder costs 2.5 % of the alignments; a 1 s radar outage before
  the contact 1.2 % of the core events.

**Regressions.**  None: the refinement is off by default and the baseline copies are identical.  Found and
fixed on the way: the clock perturbation did not shift the traffic-sign stream (no effect on the other
families).

**Limitations.**  Each condition perturbs one family; the refinement estimates translations only (heading
errors and drifts remain) and does not help the degraded profile's false merges; a collision-impulse gate
scaled by a declared impulse accuracy (as the pose sources declare theirs) is left for future work; heavy
clutter defeats the tracker's confirmation rule (spurious entities and events).

**Commit.**  Phase 3: `d6ebdfd9a84e034795ac3513f0049a7a42dfd84a`.  Phase 4: `phase4: ...` (SHA in the phase 5 section).

**Gate.**  PASS: sourced or flagged profiles; non-destructive copies; seeded draws with a stopping rule;
metrics against level with plots; CARLA's impulse symmetry documented and checked on S06, S15, S16; the
refinement measured against the plain reconstruction; tests green on both Pythons (phase gate run).
