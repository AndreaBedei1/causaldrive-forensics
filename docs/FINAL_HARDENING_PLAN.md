# Final uncertainty hardening: plan

Branch `final-uncertainty-hardening` from PARENT_RETROSPECTIVE_COMMIT
`9cd9728c813b5e9f8f9f435982cb9cc9c6dd75d6` (`retrospective-reconstruction`).  `stress-validation` and the frozen
results of `results/retrospective/` are not modified; they are the baseline of this phase.

## What remains open (from docs/RETROSPECTIVE_RECONSTRUCTION_REPORT.md)

1. **Fixed tracking gates.**  `max_association_distance_m` 2.5 m (Euclidean, any range, any gap),
   `max_velocity_mismatch_mps` 4 m/s (radial residual, no uncertainty), `cluster_distance_m` 2 m (same at 10 and
   90 m), `moving_speed_mps` 1 m/s, `min_track_frames` 5 (sampling-rate dependent), `max_track_gap_s` 0.5 s
   (independent of how uncertain the prediction is).
2. **Doppler / velocity uncertainty under-declared on crossing targets.**  The track declares ~0.3 m/s while its
   tangential velocity is 1.5-2 m/s off; full-velocity comparisons against fixed thresholds turn that into false
   contradictions.
3. **S10 regression.**  `radar_contact_evidence` contradicts the true A-B contact of S10 rolls_through (speed RMSE
   1.55 > `speed_consistency_mps` 1.5) under exact and RTK poses: one contact and one recorder link lost per draw.
4. **Relevance range only annotated.**  No decision uses it.
5. **New parameters without sensitivity.**  `assignment_likelihood_ratio` K = 20, `retrospective_new_target_density`
   3.57e-5, `retrospective_min_posterior` 0.95.
6. **No dense-traffic scenarios.**  The campaign has at most four vehicles per run (S06/S15/S16: three; S18: four).
7. **Visual audit not rerun** after the corrected and retrospective methods.

## Approach

* METHOD 1 (`current`), METHOD 2 (`corrected`) and METHOD 3 (`retrospective`) stay as frozen on the parent branch.
  A new `fusion.association_method: final` (METHOD 3 FINAL) = METHOD 3 + uncertainty-aware tracking + the radial
  (Doppler) collision evidence + the operative relevance envelope.  The tracker's new gating is used only by
  `final`, so the earlier methods remain reproducible.
* Every fixed gate replaced by a statistic only where a covariance exists: innovation Mahalanobis distance with a
  chi-square gate (position), normalised radial residual (Doppler), uncertainty-driven track survival; a hard cap
  only as a documented fail-safe.  Larger uncertainty widens a GATE, never a MERGE: the association decisions keep
  the discriminability rule and the likelihood-ratio competition.
* New seeds, never used before: development 200-203, final held-out 300-309 (S10 and the collision study) /
  300-304 (17 runs).  Algorithm and configuration frozen before the held-out runs.
* New scenarios at the first truly free IDs.  S04, S05, S11, S13, S14 existed and were removed (retired, see
  `docs/SCENARIO_ID_MAP.md`): they are not reused; new IDs start at S19.
* Raw recordings immutable once acquired; reconstructions rerunnable.
