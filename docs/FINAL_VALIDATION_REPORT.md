# Final validation

**ANALYSIS_FREEZE_COMMIT = `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`.**  Every table, figure, canonical
reconstruction and study record in this tree was regenerated offline (no CARLA, no provider call) by
`scripts/final_validation.py` from a clean detached checkout of that commit into a separate data directory:
17/17 canonical runs, 240/240 sweep runs, 2035/2035 robustness jobs (0 failed, 7.2 CPU h), canonical and
sweep event oracles, the independent oracle check (133 onsets), one-at-a-time sensitivity (257 runs), the
visual audit, all tables and figures (`results_qa.py`: 14 tables, 11 figures, 17 study records, PASS).  464
provenance records name that commit with `analysis_started_from_clean_tree` true; `results/clean_start.json`
holds the SHA-256 of the 9,097 raw and manifest files, verified unchanged when publishing.  The historical
acquisition provenance of the recordings is unchanged.

The first freeze, `7bf721d`, stopped in the aggregation: the independent privileged checker passed single
2-vectors to its time-vectorised separating-axis test.  `8d7343d` fixes only that evaluation script (with a
regression test); `src/cdf` is identical in both commits.  Nothing produced from `7bf721d` was published.

## Reconstruction changes

S12 collision continuity requires a short segment with the same parent, two strongly
named flanking segments, a matched contact, consistent body geometry across measured
samples, and no compatible local rival or competing recorder. Impact-disturbed velocity
alone no longer creates a new road user. Motion ambiguity remains internal; a real
identity switch cannot inherit the name through incompatible geometry.

PATH ENTRY/EXIT, CUT_IN and CRITICAL_TTC share estimated body geometry. PATH tests the
body's intersection with the forward corridor, with hysteresis and no invented first-seen
entry. CUT_IN additionally requires persistent absolute target lateral motion in a
straight path frame fixed at first observation; ego yaw and translation alone cannot
create the manoeuvre. This removes the S16 C cut-in, preserving true S02 and S17 cut-ins.
The reference oracle uses true oriented body geometry only within privileged evaluation.

Global events union source-track state intervals per observer/entity/state, preserving
source local nodes and source tracks. Sampling cells join adjoining handoffs. Appearance
is unique while any source supports the entity; loss waits for the last source. Silent
initial path states remain silent even when another source subsequently enters.
Replay reads those persisted entity events for its displayed timeline, while the original
local events remain available for diagnosis. Headless state labels also union source labels.
New geometric evidence uses declared decimal precision; differences below 1e-13 m/s between
NumPy versions cannot invalidate the byte comparison proving independence from privileged files.

## Evaluation and assumptions

The historical fusion medians are decomposed on identical physical instants in
[fusion_accuracy_regression](audit/fusion_accuracy_regression.md). The single-track
comparator now has one median source error per fused entity/instant, avoiding unequal
weighting with source count. Fused-state errors exclude mixed-identity source instants;
identity mistakes and fragmentation are always reported separately.

GNSS common fractions 0.5, 0.9 and 1.0 are sensitivity assumptions, supported only as
parametric exploration of slow common errors. Independent white noise, heading and
velocity remain. Absolute and simultaneous pairwise position errors are separate;
common translation can preserve relative identity but displace absolute fused centres.
The empirical relative-error reliability boundary is conditional, not a universal claim.

Combined pose/10% impulse robustness includes all canonical runs; wrong pairings are
counted separately from unpaired singleton callbacks and unmatched true contacts.
All semantic thresholds retain their documented values; no recall target tuning.

## Preservation and cleanup

Initial tree: 2,352 tracked files, 332.8 MiB. All 9,097 raw/manifest SHA-256 hashes
checked unchanged before freeze. Superseded audit image sets, intermediate diagnoses,
old verdicts and generated LLM outputs were removed after fusion regression diagnosis.
The classification is in [final_tree_inventory](audit/final_tree_inventory.json).
Unique recording/calibration details and the verified bibliography were preserved.

After publication: 1,713 tracked files, 302.8 MiB (before the hardening, tag `pre-final-hardening`:
2,352 files, 332.8 MiB).  Removed from the current tree (kept in Git history): the superseded visual audits
(baseline, phase 2, phase 6, replay follow-up and their verdicts), intermediate diagnoses and before/after
dumps (S02, S08, S18, hardening), the generated LLM outputs (`traces/*/reconstruction/llm/`,
`llm_comparison_S17`).  The phase reports `CAMPAIGN_REPORT.md` and `PAPER_READINESS_REPORT.md` are reduced to
pointers; their paper material is kept in [paper_positioning](paper_positioning.md).  The pilot sizing record
moved to `docs/audit/experiment_size_pilot.json` (a design record, not an analysis output).

## Final results (analysis commit 8d7343d)

Tables: [results](../results/README.md).

**Canonical runs (T1, T3).**  17/17 aligned (every recorder on t_global; max relative clock-offset error 0.05 s, S07; max t_global error of the run 0.10 s in S16 and 0.60 s in S18 platoon, 0 elsewhere except S07 0.05 s);
every true vehicle contact reconstructed; identities 46/46 decided correct; recorder links 46 correct,
0 wrong, 1 missed; merges 17 correct, 0 false, 10 missed; fused centre error median 0.35 m (box fit 0.26 m,
covariance intersection 0.77 m) against 0.61 m for the single-track nominal box; the declared uncertainty
holds 0.61 / 0.91 / 0.96 of the errors within 1 / 2 / 3 sigma.

**Sweeps (T2, T8).**  240/240 runs; median |t_global error| <= 0.05 s in every sweep, p95 <= 0.05 s except the two S18 sweeps (0.55 / 0.40 s); identities 405/405; recorder links
405 correct, 0 wrong, 70 missed (54 in crossing); merges 329 correct, 0 false, 194 missed; fused better than
single track in 40/40 unobserved cut-in runs (0.12 vs 0.55 m), 21/22 crossing, 40/40 side by side, 28/40
platoon.

**S12.**  B:track_001 segments 1 / 2 / 3: before A / U1 / A, now A / A / A (segment 2 anchored by the
matched collision, touching geometry, the same parent track and no compatible rival).

**S16.**  The CUT_IN_FROM_LEFT_START(A,C) at -0.10 s came from A's own rotation: C's lateral motion was
measured in A's instantaneous frame.  CUT_IN now needs the target's own lateral motion in a path frame fixed
at the start of the observation.  S16 keeps EGO_PATH_ENTRY(A,C) at -0.40 s and CRITICAL_TTC_START(A,C) at
-0.35 s, and has no cut-in.  True cut-ins kept: S02 crash -3.85 s, S02 critical_before_cut_in -1.25 s (after
its CRITICAL_TTC, as designed), S17 U1 -2.20 s; one more true cut-in is now found (S17, B on A, -0.50 s,
present in the ground-truth oracle).

**S18 and global events.**  Simultaneous duplicate global events over the canonical runs: 9 before (S16 2,
S18 abreast 2, passing 2, platoon 3), 0 after.  States are the union of the source-track intervals per
observer / entity / state, with one START and one END; TRACK_LOST only when the last source track is lost;
source nodes and tracks kept as provenance.

**Body-based events (T4, T8; sweeps, before the first contact, against COVERAGE).**  Path entry: recall
0.464 -> 0.655, precision 0.947 -> 0.862, onset median +0.50 -> +0.10 s.  Cut-in from right: recall 0.464 ->
0.726 (precision 0.957).  Cut-in from left: 1.000.  CRITICAL_TTC_START: precision 0.940, recall 0.942,
+0.05 s.  Canonical: path 0.429 -> 0.667, cut-in right 0.20 -> 0.40.  Coverage loss: the radars hide 12 % of
the CRITICAL_TTC onsets an all-seeing sensor would establish (COVERAGE vs PERFECT recall 0.882); no path
entry or cut-in is lost to coverage.  The ~0.9 target is not reached overall.  Failure mode
(`scripts/diagnose_body_event_misses.py`, `docs/audit/body_event_misses.txt`): path-entry recall is 0.85 for
entries more than 0.5 s before the observer's first contact (140 expected) and 0.44 in the last 0.5 s (127
expected: the scripted side-by-side drift of S18 into contact, 54 misses, and the S17 swerve, 12).  Cut-in
from right: 0.98 (83/85) before the last 0.5 s, 0.41 within it.  80 of the 92 path misses are tracked
targets whose body enters the corridor alongside the observer at contact range; 9 crossing entries are found
more than 2 s off.  No threshold was changed to raise recall.

**GNSS (T9) and combined collisions (T10).**  Relative pose error (RMS over simultaneous recorder pairs):
RTK 0.03 m; consumer independent 2.70 m; common fraction 0.5 / 0.9 / 1.0: 1.91 / 0.86 / 0.08 m (absolute
2.08 / 1.81 / 1.71 m).  Fused centre error: 0.43 m (RTK), 2.84 m (consumer; 1.94 m refined), 2.39-2.49 m
(common).  Wrong recorder links per draw: 0.0 (RTK), 0.6 (consumer), 0.4 / 0.1 / 0.0 (common).  False merges
per draw: 0 at RTK and about 18-21 for every consumer variant, all in the three S18 runs, independent of the
relative error (20.6 at 0.08 m).  Diagnostic ([gnss_false_merge_mechanism](audit/gnss_false_merge_mechanism.json),
`scripts/diagnose_gnss_false_merges.py`, S18, 3 seeds): a pure common translation with consumer declared
accuracy gives 18 false merges per draw; the same translation declared at RTK accuracy gives 0; consumer
heading error alone gives 0.  The merges come from gates widened by the declared accuracy (1.66 m) until C and
D, 1.4 m apart, become compatible -- not from the relative pose error.  Supported statement: identity fusion
was error-free with relative pose error <= 0.05 m and RTK-level declared accuracy; with a declared accuracy of
about 1.7 m, road users 1.4 m apart are merged whatever the actual relative error.  A threshold of the form
"X m of relative error" cannot be read from these data; intermediate declared accuracies are untested.
Collisions with 10 % impulse noise: exact and RTK poses recall 1.000, 0 wrong pairings, all runs aligned;
consumer independent recall 0.767, 0.1 wrong pairings per draw, 5.1 unmatched true contacts, 5.4 ambiguous
refusals, 87.5 % aligned; consumer common 0.9: 0.784, 0.1, 4.8, 4.5, 89.7 %.  Impulse noise alone (T5): 2-10 %
recall 1.000, 20 % 0.985, 0 wrong.  "Zero wrong collision matches" holds for exact and RTK poses, not for
consumer-grade poses (about one wrong pairing in ten draws over the 17 runs).

**Fusion accuracy history.**  [fusion_accuracy_regression](audit/fusion_accuracy_regression.md): 0.45 -> 0.53 m
compared different populations (on the 789 shared instants 0.480 -> 0.466 m; the 407 equal-source comparisons
are identical); CI 0.68 -> 0.97 m is a different, harder CI subset (CI states 535 -> 481, box fit 390 -> 477);
0.41 -> 0.72 m is a median of run medians, not the pooled median.  Final: pooled fused median 0.35 m
(canonical, T3); robustness baseline 0.40 m (median of run medians).

**Sensitivity (T6).**  CRITICAL_TTC recall 0.91-0.96 for every threshold; path entry 0.62-0.68; cut-in from
right drops to 0.44-0.45 with a 1.75 m corridor or a 0.8 m outside margin (definitional: the oracle's own
cut-ins change too).

**Visual audit.**  17 canonical runs, every keyframe: 15 PASS, 2 WARN, 0 FAIL
([verdicts](audit/visual_audit_final_verdicts.json)).  WARNs: S18 abreast and platoon, first sweeps only (the
same car drawn as two U's before the cross-observer merge; conservative missed merge, no false merge).
Manual replay review prepared for S12, S16, S17, S18 abreast / platoon / passing (`manual_*` frames,
[checklist](manual_replay_checklist.md)).

**Tests.**  516 passed on Python 3.14 (plus 17 subtests) and 516 on Python 3.8, at `8d7343d`.

Reconstruction GT access: NO.  Fusion GT access: NO.  Replay GT access: NO.  GT evaluation only: YES.
LLM API calls: ZERO.  New CARLA simulations: ZERO.  Push: NO.
