# Retrospective reconstruction: report

Branch `retrospective-reconstruction` from `main` at BASE_MAIN_COMMIT `9620483cc83c3638bed360b92d0c9852d18a7d9b`.
Design and audit: [RETROSPECTIVE_RECONSTRUCTION_PLAN](RETROSPECTIVE_RECONSTRUCTION_PLAN.md).  All results are
privileged evaluations of reconstructions that never read ground truth; every job line in
`results/retrospective/<method>/jobs_<tag>.jsonl` carries its provenance (commit `e7819cd`, clean tree, config
hash, method, seed, perturbation, run, time); summaries `results/retrospective/summary_<tag>.{md,json}`.  No CARLA
simulation, no LLM or provider call.

Labels: **[DATA]** supported by data; **[ASSUMPTION]** engineering assumption; **[NOT TESTED]**.

## 1. Baseline (main)

Test suite at BASE_MAIN_COMMIT: Python 3.14 516 passed (17 subtests), Python 3.8 516 passed (clean checkout).
METHOD 1 (`current`) is the algorithm of main, bit-identical (tested: the committed global graph of S18 abreast is
reproduced node for node; `association_method` defaults to `current`).

## 2. Problems identified (before any change)

* **Shared pose error counted as independent [DATA].**  Two tracks of one recorder share its pose error, which
  cancels in their difference; `pair_evidence` added the full absolute pose variance to both, so with consumer
  GNSS (1.66 m per axis) two cars 4-7 m apart were accepted as one body.  This is the mechanism of every S18
  false merge found in the feasibility study (section 8).
* **Large uncertainty made links easier [DATA].**  Every gate widened with the declared accuracy; a constant pose
  bias does not average out over instants.
* **Collision geometry as positive evidence [DATA].**  The contact gate (1 m + 3 sigma of the two declared
  accuracies) is 8.0 m under consumer GNSS: S06 seed 3 paired A's report with B's later one 5.96 m apart.
* **RTS smoothing is not identity association.**  Nothing propagated a later identity backward.

## 3. Radar uncertainty model

Corrected methods: per sample, extended-body scatter (`tracking.measurement_std_m`, 0.5 m, unchanged) plus the
declared polar accuracy propagated by the Jacobian, Sigma_xy = J diag(sigma_r^2, sigma_az^2) J^T, lateral sigma =
range x sigma_az.  sigma_r 0.25 m, sigma_az 0.5 deg: the nominal production values of
`docs/robustness_profiles.md` (sourced) **[ASSUMPTION: the reconstruction declares a datasheet accuracy; CARLA's
radar itself has no angular noise]**.  At 10 / 30 / 60 m the lateral sigma is 0.09 / 0.26 / 0.52 m (tests: grows
with range, near gate tighter than far).  The tracker itself is unchanged in all three methods (METHOD 1 must
remain main): its fixed gates are audited in the plan (section 4).

## 4. Threshold audit

Plan, section 2: every tracking, fusion, collision and semantic threshold classified as physical/statistical,
regulatory/definitional or engineering.  New formulas: Jacobian covariance; relative pose variance; bias
discriminability 3 sigma_bias <= `semantics.target_width_m` (vehicle geometry); backward covariance propagation
through the tracker's own white-acceleration model; relevance range.  New engineering parameters (documented):
`assignment_likelihood_ratio` 20, `retrospective_new_target_density` 3.57e-5 /(m^2 (m/s)^2) (one vehicle per 3.5 m
x 20 m of lane, velocities over +-10 m/s per axis), `retrospective_min_posterior` 0.95.  Still fixed and arbitrary
in the tracker: `max_association_distance_m` 2.5, `max_velocity_mismatch_mps` 4.0, `cluster_distance_m` 2.0,
`min_track_frames` 5, `max_track_gap_s` 0.5 (unchanged on purpose, see 17); and `speed_consistency_mps` 1.5 m/s
(see 16).

## 5. Relevance range

d_rel = d_min(v_ego) + max(v_close + 3 sigma_v, 0) x H + 3 sigma_pos, d_min the UN R157 safe following distance of
the recorder's speed, H `prediction_horizon_s` 6 s (conflict model).  At 50 km/h, not closing, 0.2 m/s and 0.5 m
sigmas: 26 m; moving away: 22.4 m; closing at 10 m/s: 86 m.  Annotation only (entities record
`relevance.relevant_from_t_global`; samples in the evaluation) **[DATA: no decision uses it]**.  Held-out, 17
runs, consumer-like conditions: within the range METHOD 2 has 0.906 correct / 0.002 wrong / 0.092 unresolved
samples (METHOD 1: 0.895 / 0.051 / 0.054); outside it 0.527 / 0.000 / 0.473 (METHOD 1: 0.713 / 0.153 / 0.134):
far, non-closing road users are the ones the corrected method leaves unresolved rather than wrong.

## 6. Corrected pose uncertainty (METHOD 2)

Same recorder: only heading error x separation; across recorders: the relative covariance, from the mutual
refinement's joint posterior when the recorders observe each other, else the sum of the declared variances (no
correlation assumed); a positional link (anonymous pair or recorder link) whose relative bias cannot separate two
bodies a car width apart stays UNRESOLVED.  CANNOT_LINK from simultaneous one-recorder distinctness (one-box test
beyond its gate on >= 10 instants) enforced through the clustering, also transitively; one-to-one links by
likelihood ratio K = 20; an association score per link (section 13).

## 7. Collision association

Pose geometry is only a veto; positive or contradicting evidence comes from each recorder's own radar: a track that
ARRIVES at its body during the approach window (from beyond the touching clearance + 3 sigma) and touches it at
the report, at the partner's own recorded speed under the clock offset the candidate implies (pose-free, no
GNSS).  A contradicted candidate is dropped; without radar evidence the existing ambiguity rules apply; a third
recorder is never required.  S06 consumer GNSS + 10 % impulse (development seeds 0 and 3,
`summary_S06_seed0_3.md`):

| run, seed | METHOD 1 matched / wrong / unmatched / ambiguous | METHOD 2 (= 3) |
|---|---|---|
| a_front_pushed, 0 | 0/3, 0, 3, 4 | 3/3, 0, 0, 0 |
| a_front_pushed, 3 | 1/3, **1 wrong**, 2, 1 | 0/3, 0, 3, 2 |
| b_rear_first, 0 | 0/2, 0, 2, 5 | 2/2, 0, 0, 0 |
| b_rear_first, 3 | 2/2, 0, 0, 0 | 2/2, 0, 0, 0 |

Held-out, 17 runs x 5 seeds (`summary_all17_heldout.md`): consumer GNSS recall 89/110 -> 105/110, ambiguous
refusals 35 -> 0; consumer + 10 % impulse 95 -> 105/110; degraded 85 -> 105/110 and wrong pairings 1 -> 0.
Wrong collision pairings with METHOD 2/3: 0 in every condition.  Regression with exact and RTK poses: 110/110 ->
105/110 (exact 22/22 -> 21/22): S10 rolls_through, see 16.

## 8. Retrospective feasibility on S18

`docs/audit/retrospective_feasibility_S18.md` (before any implementation, METHOD 1, consumer and correlated
consumer, seeds 0-3, 64 wrong links): RECOVERABLE 50 (mostly same-observer links whose recorder's own pose-free data
distinguish C and D from its first sweeps, ~6 s before the contact, 15-29 m, 3-8 m apart: the evidence is
SIMULTANEOUS, recovered by the corrected uncertainty, not by backward association), POSSIBLY_RECOVERABLE 13
(platoon: distinct only after the contact), NOT_RECOVERABLE 1 (abreast seed 1: A sees only D, B only C; no
interval distinguishes them -- backward association cannot solve it).

## 9. Retrospective algorithm (METHOD 3)

An unresolved entity that ends before an entity seen by several observers starts: the later entity's first state
is carried BACKWARD through the gap with the tracker's own model (constant velocity, white acceleration 6 m/s^2,
one prediction per 0.05 s sweep; time-reversible); 4-dof chi-square of centre and velocity; likelihood ratio of
the Gaussian density against a new-target density; posterior over all candidates; resolved at >= 0.95 with no
cannot-link and no simultaneous track of one recorder.  Confidence decays with the gap through the covariance:
position sigma 0.8 m at 1 s, 1.6 m at 1.6 s, 4 m at 3 s (tests: short gap stronger than long; long or
symmetric-ambiguous gaps unresolved).  Only identities change: the observation times, TRACK_APPEARED, path,
cut-in, CRITICAL_TTC, collision and control events keep their timestamps (test on S17 and S18 platoon: the
multiset of (event type, actor, t_global) is identical between METHOD 2 and 3); the association records
`retrospective`, `identity_resolved_from` and the posterior.

## 10. Three-method comparison, S18 (held-out seeds 100-109; development seeds 0-3 identical)

Per draw (3 runs summed), `summary_S18_heldout.md`:

| condition | method | false merges | missed merges | wrong links | correct / wrong / unresolved samples | early (>2 s) correct / wrong |
|---|---|--:|--:|--:|---|---|
| exact | 1 / 2 / 3 | 0 / 0 / 0 | 10 / 10 / **8** | 0 | 0.955/0.006/0.039, same, **0.973/0.006/0.021** | 0.939 / 0.013 |
| RTK | 1 / 2 / 3 | 0 / 0 / 0 | 10 / 10 / **8** | 0 | as exact | 0.939 / 0.013 |
| consumer | 1 | **20.1** | 10.0 | 0 | 0.753/0.216/0.031 | 0.706 / 0.258 |
| consumer | 2 = 3 | **0.0** | 11.0 | 0 | 0.955/0.006/0.039 | 0.939 / 0.013 |
| common 0.5 / 0.9 / 1.0 | 1 | 20.4 / 20.4 / 20.7 | ~10 | 0 | wrong 0.218 / 0.218 / 0.212 | wrong 0.258 |
| common 0.5 / 0.9 / 1.0 | 2 = 3 | 0 | 11 | 0 | 0.955/0.006/0.039 | 0.939 / 0.013 |

Collisions on S18: no change except common 0.5 (development 9/12 -> 12/12).  Answer to the main question
**[DATA]**: after correcting the shared pose uncertainty, every S18 false merge disappears; retrospective
association then adds value only where the relative pose is precise (exact, RTK: one backward resolution per draw,
2 more correct merges, unresolved samples 3.9 % -> 2.1 %, all resolutions correct); under consumer GNSS it resolves
nothing (the cross-observer relative bias makes the backward density too low) and stays UNRESOLVED, never wrong.

## 11. Held-out results

Development seeds 0-3 (all design and debugging); held-out seeds 100-109 (S18) and 100-104 (17 runs), run once on
the frozen commit `e7819cd`; no parameter changed after them.  S18 held-out reproduces the development numbers
exactly.  One held-out failure was found and is reported, not tuned (16).

## 12. All 17 canonical scenarios (held-out seeds 100-104)

Per draw (17 runs summed), `summary_all17_heldout.md`:

| condition | M1 false / missed merges | M2 = M3 false / missed | M3 missed | wrong links M1 -> M2 | missed links M1 -> M2 | wrong samples M1 -> M2 | unresolved M1 -> M2 | collisions M1 -> M2 (wrong) |
|---|---|---|--:|---|---|---|---|---|
| exact | 0 / 10 | 0 / 10 | 8 | 0 -> 0 | 1 -> 2 | 0.0016 -> 0.0016 | 0.011 -> 0.031 (M3 0.026) | 22 -> 21 /22 (0) |
| RTK (and + 10 %) | 0 / 10 | 0 / 10 | 8 | 0 -> 0 | 1 -> 2 | 0.0016 -> 0.0016 | 0.011 -> 0.031 | 110 -> 105 /110 (0) |
| consumer | 20.4 / 11.0 | 0 / 14.0 | 14 | 0.2 -> 0 | 4.8 -> 7.4 | 0.066 -> 0.0017 | 0.092 -> 0.130 | 89 -> 105 /110 (0) |
| consumer + 10 % | 20.4 / 11.0 | 0 / 14.0 | 14 | 0 -> 0 | 4.4 -> 7.4 | 0.060 -> 0.0017 | 0.082 -> 0.130 | 95 -> 105 /110 (0) |
| common 0.5 / 0.9 / 1.0 | ~20.6 / ~10.5 | 0 / 14 | 14 | <= 0.4 -> 0 | 2.4-3.8 -> 7.4-8.6 | 0.058-0.070 -> 0.0017 | 0.03-0.07 -> 0.13-0.15 | 88-95 -> 105 /110 (0) |
| degraded | 20.8 / 10.6 | 0 / 28 | 28 | 1.6 -> 0 | 7.8 -> 13.0 | 0.074 -> 0.0017 | 0.136 -> 0.270 | 85 -> 105 /110 (1 -> 0) |

Recorders aligned: within -5 / +5 of METHOD 1 (out of 200 per condition).  S12 (B keeps A through the contact), S16 (no CUT_IN of C), S17 (U1
with its cut-in at -2.20 s) and S18 (C and D distinct) hold under METHOD 2/3 (regression tests, exact; S18 also
consumer).  Replay: reads the same files; entities and their events are consistent (the visual audit was not
rerun **[NOT TESTED]**).

## 13. Confidence calibration

The association score (a link's posterior among its rival candidates and a not-this-road-user hypothesis at the
gate, from the same chi-squares) is NOT calibrated as a probability **[DATA]**: 17 runs held-out, empirical accuracy
per score bin 0.5-0.8: 1.00 (96 tracks), 0.8-0.9: 1.00 (517), 0.9-0.95: 1.00 (481), 0.95-0.99: 0.92 (1438;
METHOD 3 0.945), 0.99-1: 0.995 (391).  Conservative below 0.95, slightly optimistic in 0.95-0.99.  It is reported
as an association score, not a probability.  Median score by range: 0.94 (0-10 m), 0.99 (10-30 m); by time
before contact: 0.90-0.91 (1-4 s), 0.98 (> 4 s).

## 14. Distance breakdown (17 runs held-out, consumer-like conditions, correct / wrong / unresolved samples)

| range [m] | METHOD 1 | METHOD 2 = 3 | samples |
|---|---|---|--:|
| 0-10 | 0.948 / 0.003 / 0.049 | 0.924 / 0.000 / 0.076 | 118k |
| 10-20 | 0.768 / 0.117 / 0.115 | 0.708 / 0.007 / 0.285 | 43k |
| 20-30 | 0.703 / 0.267 / 0.031 | 0.849 / 0.000 / 0.151 | 20k |
| 30-40 | 0.735 / 0.195 / 0.070 | 0.804 / 0.000 / 0.196 | 3.8k |
| 40-50 | 0.787 / 0.144 / 0.069 | 0.837 / 0.000 / 0.163 | 2.1k |
| 50-60 | 0.771 / 0.129 / 0.100 | 0.819 / 0.000 / 0.181 | 1.2k |
| 60+ | 0.891 / 0.000 / 0.109 | 0.797 / 0.000 / 0.203 | 1.9k (few runs) |

Exact/RTK: METHOD 3 brings the 20-60 m bins from 0.84-0.95 to 1.00 correct (S18; backward resolution of re-acquired
far tracks).

## 15. Time-before-impact breakdown (same conditions)

| before first contact [s] | METHOD 1 | METHOD 2 = 3 |
|---|---|---|
| 0-0.5 | 0.905 / 0.055 / 0.040 | 0.908 / 0.000 / 0.092 |
| 0.5-1 | 0.916 / 0.047 / 0.037 | 0.892 / 0.000 / 0.108 |
| 1-2 | 0.889 / 0.076 / 0.035 | 0.896 / 0.000 / 0.105 |
| 2-4 | 0.853 / 0.121 / 0.026 | 0.897 / 0.009 / 0.094 |
| > 4 | 0.832 / 0.143 / 0.025 | 0.909 / 0.003 / 0.088 |

Backward decisions by gap (METHOD 3, 17 runs held-out): 1-2 s: 16 resolved, 16 correct; > 4 s: 16 candidates
(other vehicles) left unresolved; no decision in 0-1 s or 2-4 s.

## 16. Failure modes

* **S10 rolls_through, exact/RTK poses (held-out) [DATA].**  METHOD 2's radar check contradicts the TRUE A-B
  contact: B's track of A (a crossing target) reports 5.8-7.1 m/s against A's own 5.0 m/s (the tracker's known
  tangential velocity error on crossing targets, while it declares 0.3 m/s), RMSE 1.55 > `speed_consistency_mps`
  1.5.  Effect per draw: one true contact unmatched and one recorder link missed (exact 22 -> 21/22 contacts; links
  missed 1 -> 2).  Not fixed after the held-out results: the contradiction should come only from the Doppler
  (radial) component, or from a tangential velocity uncertainty the tracker does not yet declare; to be validated
  on fresh seeds **[NOT TESTED]**.
* Missed merges increase under consumer GNSS (11 -> 14 per draw; degraded 10.6 -> 28) and unresolved samples rise
  (0.09 -> 0.13): positional cross-observer links are refused when the relative pose bias exceeds a car width / 3
  (forensic preference: missed over false).
* The exact-pose 0.0016 wrong-sample share is unchanged by all methods (S18 early mixed segments of C and D).
* METHOD 3 gains nothing under consumer GNSS.

## 17. Limitations

Simulation only; the tracker's fixed gates are not reworked (METHOD 1 had to remain main); the score is not a
calibrated probability; the new-target density, K and the 0.95 posterior are engineering assumptions (no
sensitivity study run **[NOT TESTED]**); the retrospective step joins only entities ending before a multi-observer
entity starts (not short overlaps, not recorders); the relevance range is an annotation; held-out seeds 5 per
condition for the 17 runs; the visual audit was not rerun.

## 18. Supported claims

* **[DATA]** Treating the pose error as relative (common to two tracks of one recorder) and refusing positional
  links that cannot separate adjacent bodies removes every false merge (S18: 20.1 -> 0 per draw; 17 runs: ~20.5 ->
  0, all consumer variants and degraded) and every wrong recorder link, with no new wrong collision pairing.
* **[DATA]** The cost is more unresolved identity (missed merges +3 per draw under consumer GNSS, +17 degraded) and,
  with precise poses, one S10 contact lost to an over-strict speed contradiction.
* **[DATA]** Later, higher-quality evidence recovers earlier identities without wrong associations when the gap is
  1-2 s and the relative pose is precise (exact/RTK: 100 % of 16 + 11 decisions correct; missed merges 10 -> 8);
  beyond 4 s or with consumer-grade relative pose it leaves the identity unresolved.  Operating envelope: gap <=
  ~2 s, relative pose sigma below ~0.6 m.
* **[DATA]** Pose-free radar evidence turns consumer-GNSS collision matching from ambiguous to matched (89 -> 105 /
  110) with 0 wrong pairings; S06 seed 3's wrong pairing is gone.
