# Retrospective reconstruction: audit and design

Branch `retrospective-reconstruction`, from `main` at BASE_MAIN_COMMIT
`9620483cc83c3638bed360b92d0c9852d18a7d9b` (the stress/hardening branch is neither a base nor a source).
Baseline test suite before any change: Python 3.14 516 passed (17 subtests); Python 3.8 on a clean checkout
of the same commit (see the report).

Principle: the reconstruction is OFFLINE.  Later recorded evidence may resolve an earlier identity; it may
never create an earlier observation, move a timestamp or anticipate an event.  Ground truth is read only
by the privileged evaluation.

## 1. How the reconstruction works today (audit)

**Radar tracking** (`tracking.py`).  Returns of every radar are placed in the recorder's own odometric
frame; tracks compete for returns inside a fixed Euclidean gate (`max_association_distance_m` 2.5 m around
the predicted position) and a fixed Doppler gate (`max_velocity_mismatch_mps` 4 m/s); the measurement is the
median of the claimed returns with a fixed isotropic noise (`measurement_std_m` 0.5 m) plus one Doppler row per
radar (`radial_speed_std_mps` 0.3 m/s); constant-velocity Kalman filter with white acceleration
(`acceleration_std_mps2` 6 m/s^2) and a Rauch-Tung-Striebel smoother; a track is split into identity
segments where its returns span more than one body width for five sweeps (`identity_segments`).

**RTS smoothing is not retrospective identity association.**  The smoother improves the state estimate of a
track from its own later measurements; it never decides which road user a track (or a segment, or an
earlier track) belongs to.  Identity is decided later, in `fusion.py` and `anonymous.py`, and only from
evidence that overlaps the track (collision partner, recorder footprint, simultaneous tracks of other
observers) or from a short forward stitch (`stitch_max_gap_s` 1.5 s).  Nothing propagates a later, stronger
identity backward to an earlier unresolved track: that is what is missing.

**Uncertainty in the common frame** (`common_frame.py`).  Each sample carries `pose_var` = declared pose
position variance + (declared yaw std x range)^2, isotropic.  `_position_sigma` adds it to
`measurement_std_m`^2 (and the other recorder's pose variance when the outline is a recorder's).  Problems:

1. A pose error is the same for two tracks of ONE recorder; in their difference it cancels except for the
   rotation of the heading error over their separation.  `pair_evidence` nevertheless adds the full
   absolute pose variance to the faces of both tracks of a SAME_OBSERVER pair: with consumer GNSS (1.66 m per
   axis) the one-box test then accepts two tracks 5-7 m apart as one body.
2. Pose errors are slowly varying biases (run bias plus a Gauss-Markov term with tau 30-60 s): they do not
   average out over the samples of a pair.  The current tests treat each instant as independent evidence
   (a pass fraction over instants), so many samples do not make a positional link stronger, only more
   permissive.
3. The radar measurement noise is isotropic and range-independent; a real radar's lateral error grows with
   range (sigma_lateral ~ range x sigma_azimuth).
4. Larger declared uncertainty widens every gate: it makes links EASIER (the false merges of the robustness
   study come from the declared accuracy, `docs/audit/gnss_false_merge_mechanism.json` on `main`).

**Fusion** (`anonymous.py`).  Recorder links (track on another recorder's footprint at its velocity, 2 sigma
median, 80 % within 3 sigma); anonymous pairs: CROSS (two observers) and SPLIT (one observer) via a joint box
fit chi-square plus a velocity chi-square per instant, accepted when >= 10 instants are compared and >= 80 %
pass; STITCH (same observer, gap <= 1.5 s, constant-velocity prediction).  `refuse_ambiguous` refuses a link
whose track is compatible with two simultaneous tracks of another observer; `cluster` joins accepted links by
score and never puts two simultaneous tracks of one observer together unless a SPLIT link showed them to be
one body.  There is no explicit negative evidence, no global assignment, no confidence with a statistical
meaning (entity confidence = weakest pass fraction).

**Collision association** (`alignment.py`, `fusion.py`, `pipeline.py`).  Reports are paired by impulse
(10 % relative tolerance; with geometry an impulse z-test, 10 % per report, 3 sigma) and by footprint contact
from the pose streams: gap <= `contact_consistency_m` + 3 sqrt(sigma_A^2 + sigma_B^2).  With consumer GNSS the
tolerance is 8.0 m: two bodies 6 m apart "touch" (S06 seed 3: a wrong pairing), and in other seeds every pair
becomes geometry-compatible, mutually ambiguous, and nothing is matched.  The radar approach check of
`pipeline.approach_check` also goes through the partner's GNSS pose, so it is silent under consumer GNSS.
Track-to-partner association (`associate_tracks`) uses frame-independent speed RMSE and clearance.

## 2. Threshold audit

A = physical / statistical (derivable from error models, speeds, sampling, geometry); B = regulatory /
definitional; C = engineering parameter (documented, sensitivity where it matters).

| Parameter | Value | Class | Today | Plan |
|---|---|---|---|---|
| tracking.moving_speed_mps | 1.0 | C | fixed | keep; documented (Doppler noise 0.3 m/s x ~3) |
| tracking.cluster_distance_m | 2.0 | C | fixed | keep (body scale; tracker unchanged in all methods) |
| tracking.max_association_distance_m | 2.5 | A (gate) | fixed Euclidean | tracker unchanged in all three methods (METHOD 1 must stay main); the fusion layer gets the range-dependent covariance below |
| tracking.max_velocity_mismatch_mps | 4.0 | A (gate) | fixed | unchanged (tracker) |
| tracking.max_track_gap_s | 0.5 | C | fixed | unchanged |
| tracking.min_track_frames | 5 | C | fixed | unchanged |
| tracking.measurement_std_m | 0.5 | A/C | isotropic median-return scatter | kept as the extended-body scatter term; radar polar noise added by Jacobian (corrected methods) |
| tracking.radial_speed_std_mps | 0.3 | A | Doppler noise | unchanged |
| tracking.acceleration_std_mps2 | 6.0 | A | white acceleration (emergency braking) | also drives the backward covariance propagation |
| fusion.link_min_samples | 10 | C | count | unchanged |
| fusion.link_min_fraction | 0.8 | C | fraction | unchanged |
| fusion.anonymous_gate_probability | 0.99 | A (chi-square) | per-instant gate | kept; plus bias-aware discriminability and hypothesis comparison |
| fusion.anonymous_min_shared_samples | 10 | C | count | unchanged |
| fusion.anonymous_pass_fraction | 0.8 | C | fraction | unchanged |
| fusion.stitch_max_gap_s | 1.5 | C | fixed | forward stitch unchanged; the retrospective step replaces the fixed limit with a covariance-propagated likelihood ratio |
| fusion.contact_consistency_m | 1.0 | A/C | + 3 sigma pose | veto only; positive contact evidence from the pose-free radar approach history |
| fusion.contact_window_s | 1.0 | C | | unchanged |
| fusion.contact_range_m / _scale_m | 3.5 / 3.0 | C | confidence factor | unchanged |
| fusion.approach_window_s | 1.0 | C | | used by the pose-free radar evidence |
| fusion.speed_consistency_mps | 1.5 | A/C | RMSE | used by the pose-free radar evidence |
| fusion.touching_clearance_m / rival_clearance_m | 1.0 / 2.0 | C | | unchanged |
| semantics.critical_* (time-gap table, d_min) | UN R157 | B | | unchanged |
| semantics.critical_reaction_time_s, deceleration | 1.0 s, 6 m/s^2 | C (literature range) | | unchanged; relevance range uses them |
| semantics.prediction_horizon_s | 6.0 | C | | relevance range |
| semantics.target_length/width_m | 4.6 / 1.9 | A (vehicle geometry) | | minimum separation of two bodies (discriminability) |
| new: radar declared accuracy sigma_r, sigma_az | 0.25 m, 0.5 deg | A (sourced: robustness_profiles nominal) | - | covariance by Jacobian |
| new: retrospective new-target density | see report | C | - | null hypothesis of the likelihood ratio, sensitivity |
| new: decision posterior | 0.95 | C | - | minimum posterior to resolve; sensitivity |

## 3. Feasibility on S18 before any implementation

`scripts/retrospective_feasibility.py` on METHOD 1 with consumer GNSS and its correlated variants
(development seeds 0-3): `docs/audit/retrospective_feasibility_S18.md`.  Result: nearly every false merge is
a SAME_OBSERVER link between two simultaneous tracks of one recorder, one on C and one on D, and the same
recorder's own data, free of the pose error, distinguish C and D from the first sweep (about 6 s before the
contact, 19-29 m, 3-8 m apart).  The distinguishing evidence is SIMULTANEOUS, not later: these merges are
recoverable by correcting the shared uncertainty, not by backward association.  One cross-observer wrong link
(A sees only D, B only C) has no distinguishing interval at all: backward association cannot solve it.
With exact poses the remaining errors are missed merges (short tracks, a 1.85 s re-acquisition gap of the
same car while it is strongly identified by both recorders): these are the cases where later evidence can
help.

## 4. Methods (identical recordings, perturbations, seeds)

METHOD 1 `current`: the algorithm of `main`, bit-identical (default of `fusion.association_method`).

METHOD 2 `corrected` (no retrospection):
- radar observation covariance in the common frame: extended-body scatter (`measurement_std_m`) plus the
  declared polar accuracy propagated by the Jacobian, Sigma_xy = J diag(sigma_r^2, sigma_az^2) J^T (lateral
  sigma = range x sigma_az): near targets get tight gates, far targets wide ones;
- pose uncertainty as a relative quantity: for two tracks of one recorder only the heading error times their
  separation; for two recorders their relative pose covariance (sum of the declared ones when nothing better
  is known -- their correlation is unknown and is not assumed);
- bias-aware discriminability: a positional link is identity evidence only if the relative pose uncertainty
  can tell two bodies one car width apart (3 sigma_rel <= target width); otherwise the link stays
  UNRESOLVED (large uncertainty = less confidence, never an easier merge);
- CANNOT_LINK: two simultaneous tracks of one recorder whose returns cannot be one body (pose-free one-box
  test beyond the gate on enough instants); tracks named after different recorders; the clustering refuses
  every merge that would join a cannot-link pair, also transitively;
- conservative one-to-one association between the tracks of two observers: a candidate link must be clearly
  better than every rival (likelihood ratio), else UNRESOLVED;
- an association score from the same covariances (posterior over the candidates, with a new-target
  hypothesis); calibrated empirically, called a probability only if the calibration supports it;
- collision association: the pose geometry is a veto only; positive evidence comes from the recorders' own
  radar approach history (a track touching the reporter at its report, approaching, at the partner's own speed
  under the candidate clock offset) -- pose-free; a candidate the radar contradicts is refused; competing
  candidates without decisive evidence stay unmatched.

METHOD 3 `retrospective` = METHOD 2 + backward identity resolution: an unresolved track that ends before a
strongly identified entity (or recorder track) is seen again is tested against it by propagating the later
state BACKWARD with the motion model (covariance growing with the gap through `acceleration_std_mps2`); the
likelihood ratio against every competing entity and a new-target hypothesis gives the confidence; cannot-link
constraints and near-equal alternatives leave it UNRESOLVED.  Only the identity of existing observations
changes: observation times, TRACK_APPEARED, path, cut-in, CRITICAL_TTC, collision and control events keep their
timestamps; the association records `identity_resolved_from` and `retrospective_confidence`.

## 5. Relevance range

Sensor range is not reconstruction relevance.  From the conflict model: a target can become a conflict within
the prediction horizon H (`prediction_horizon_s`) when its clearance is below
d_rel = d_min(v_ego) + max(v_close + 3 sigma_v, 0) H + 3 sigma_pos, with d_min the UN R157 following distance
of the recorder's speed, v_close its closing speed.  The range is annotated per sample and used to report
results in and out of the relevant envelope; it does not change any decision (an irrelevant road user is not
deleted, only not required to be resolved).

## 6. Seeds

Development seeds 0, 1, 2, 3 (debugging, design).  Held-out seeds 100-109: never used to choose a parameter;
the final comparison is reported on them.  No parameter changes after the held-out results.
