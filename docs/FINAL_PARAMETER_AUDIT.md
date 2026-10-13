# Final parameter audit (METHOD 3 FINAL)

Every numeric parameter the reconstruction uses to decide tracking, identity, collision partners and relevance,
with its **category** and what is known about its **sensitivity**.  Values are those of `configs/default.yaml` /
`src/cdf/reconstruction/config.py` at the frozen commit `c410bca`.

Categories:

* **SENSOR**: the sensor's specification or the simulator's noise model (would be a datasheet value on a real car).
* **PHYSICAL**: a physical prior (vehicle size, mass, kinematics), not fitted to the data.
* **STATISTICAL**: a probability level or a likelihood ratio: the declared decision risk, applied to a computed
  statistic (chi-square, posterior, ratio).  Not a distance or a speed.
* **STANDARD**: taken from a regulation (UN R157 time gaps).
* **FAIL-SAFE**: a hard cap that should never decide in normal operation; documented as such.
* **LEGACY**: a fixed threshold still used by METHODS 1-3 (and kept so they stay reproducible); METHOD 3 FINAL
  replaces or bounds it as noted.
* **AUDITED-FIXED**: a fixed threshold METHOD 3 FINAL still uses; justified below, not replaced.

Sensitivity sources: S = `results/final_hardening/sensitivity/SUMMARY.md` (seed 200, 23 runs, exact + consumer);
T = tracker-component development study (seeds 200-201, the 17 canonical runs, exact / consumer / consumer
common 0.9; `docs/FINAL_HARDENING_PLAN.md`); "-" = not varied in this phase.

## Tracking (`tracking.*`)

| parameter | value | category | used by FINAL | sensitivity / evidence |
|---|--:|---|---|---|
| `gating` | fixed (FINAL: covariance) | switch | `effective_config` sets covariance for FINAL | - |
| `covariance_components` | survival,confirmation | switch | yes | T: position gate adds missed links (exact 3 -> 6, consumer 17 -> 20) by fragmenting tracks at impacts; the Doppler gate produced wrong links on S06 b_rear_first and S08 during development.  Both are implemented and NOT adopted. |
| `gate_probability` | 0.99 | STATISTICAL | chi-square quantile of the (unused) position/Doppler gates | - (gates not adopted) |
| `measurement_std_m` | 0.5 | SENSOR | KF measurement noise; "arriving" test of the collision evidence (touching + 3 sigma) | - |
| `radial_speed_std_mps` | 0.3 | SENSOR | Doppler noise; sigma of the normal-component collision rule | - |
| `radar_range_std_m` / `radar_azimuth_std_deg` | 0.25 / 0.5 | SENSOR | polar measurement covariance in covariance mode | - |
| `acceleration_std_mps2` | 6.0 | PHYSICAL | KF process noise; drives the survival rule (prediction spread) and the stitch density | unit test: a 0.55 s gap survives at 0.5 m/s^2, ends at 8 m/s^2 (survival follows the model, not a timer) |
| `body_width_m` / `body_length_m` | 1.9 / 4.6 | PHYSICAL | survival: track ends when 3 sigma of the predicted position > a car width; impact noise applied within one car length | - |
| `min_track_support_s` / `min_track_updates` | 0.2 s / 3 | STATISTICAL (evidence) | confirmation by support duration and accumulated updates (replaces 5 frames, rate-independent) | T: survival+confirmation vs none, exact correct 0.970 -> 0.977, missed merges 11 -> 3 |
| `gap_cap_s` | 2.0 | FAIL-SAFE | hard upper bound on survival | unit test only (cap 0.3 s ends a track the model would keep) |
| `position_cap_m` | 10.0 | FAIL-SAFE | Euclidean upper bound of any covariance gate | - |
| `nominal_vehicle_mass_kg` | 1500 | PHYSICAL | impact process noise (J/m)^2 at the recorder's own collision callbacks | - |
| `max_association_distance_m` | 2.5 | LEGACY / AUDITED-FIXED | METHODS 1-3: gate.  FINAL: still the position gate (the Mahalanobis gate was not adopted) and the birth suppression distance | the chi-square gate was tried (T) and rejected; documented as the main remaining fixed gate |
| `max_velocity_mismatch_mps` | 4.0 | LEGACY / AUDITED-FIXED | Doppler gate in all methods (normalised Doppler gate rejected, T) | - |
| `max_track_gap_s` | 0.5 | LEGACY | METHODS 1-3 survival; not used by FINAL | replaced by survival rule |
| `min_track_frames` | 5 | LEGACY | METHODS 1-3 confirmation; not used by FINAL | replaced by support + updates |
| `cluster_distance_m` | 2.0 | AUDITED-FIXED | single-linkage clustering of returns (all methods) | not varied.  Justification: 2 m is just above a car width (1.9 m), below the 3.5 m lane spacing: returns of two cars in adjacent lanes are never joined at any range within the radar's azimuth resolution (0.5 deg x 100 m = 0.9 m).  Two cars closer than 2 m in one lane are one cluster: a known limitation (dense platoons at standstill). |
| `moving_speed_mps` | 1.0 | AUDITED-FIXED | a return starts a track only if moving | not varied.  1.0 m/s = 3.3 sigma of the Doppler noise (0.3 m/s): a static return passes with probability < 0.1 %.  Not a free parameter but the 3-sigma rule on `radial_speed_std_mps`. |
| `min_height_m` / `max_height_m` | 0.3 / 2.5 | PHYSICAL | object-height returns | - |
| `smoothing_innovation_sigma` | 3.0 | STATISTICAL | RTS smoother outlier rejection | - |
| `min_slowdown_returns` | 3 | AUDITED-FIXED | slowdown gate support | - |
| `identity_body_width_m` | 2.5 | AUDITED-FIXED | identity segmentation of a track | - |

## Identity and collision association (`fusion.*`)

| parameter | value | category | used by FINAL | sensitivity / evidence |
|---|--:|---|---|---|
| `association_method` | current (FINAL: final) | switch | - | - |
| `assignment_likelihood_ratio` (K) | 20 | STATISTICAL | one-to-one assignment: the best candidate must beat the second by K | S: **no change from 5 to 100** (exact and consumer) |
| `retrospective_new_target_density` | 3.57e-5 /m^2 | PHYSICAL (traffic density) | posterior of a stitch / retrospective link against "a new road user" | S: 3.57e-6 / 3.57e-4 move missed merges (exact 62 / 92 vs 74); false merges 0, wrong links 0, collision errors 0 at every level |
| `retrospective_min_posterior` | 0.95 | STATISTICAL | acceptance of a stitch / retrospective link | S: 0.90 / 0.99 move missed merges (exact 68 / 85 vs 74); errors unchanged |
| `anonymous_gate_probability` | 0.99 | STATISTICAL | chi-square gate of cross-recorder pair evidence | - |
| `anonymous_min_shared_samples` / `anonymous_pass_fraction` | 10 / 0.8 | STATISTICAL (evidence) | pair evidence needs 10 shared instants, 80 % inside the gate; also the resolution time | - |
| `radar_range_std_m` / `radar_azimuth_std_deg` | 0.25 / 0.5 | SENSOR | range-dependent measurement covariance in pair tests | - |
| `box_face_std_m`, `box_length_std_m`, `box_width_std_m` | 0.25 / 0.7 / 0.2 | PHYSICAL / SENSOR | centre estimate from the visible faces | - |
| `stitch_max_gap_s` | 1.5 | LEGACY / FAIL-SAFE | METHODS 1-3: stitch gate.  FINAL: only an upper bound; the decision is the stitch posterior (density decays with the gap) | unit test: posterior decays with the gap; a 4 m miss after 1.5 s is refused |
| `touching_clearance_m` | 1.0 | PHYSICAL | a track "touches" the recorder (collision evidence) | - |
| `contact_window_s` / `approach_window_s` | 1.0 / 1.0 | AUDITED-FIXED | windows of the collision evidence | - |
| closing window | 0.2 s (code constant, 4 sweeps) | AUDITED-FIXED | FINAL: the arriving body must still be closing over the last 0.2 s | development: fixes the S20 passing-car contradiction without losing S06 b_rear_first |
| `speed_consistency_mps` | 1.5 | LEGACY | METHODS 2-3 speed RMSE test; FINAL uses the normal-component rule (3 sigma of Doppler + track velocity noise) instead | S10 regression fixed in FINAL (0 collisions lost, S) |
| `impulse_relative_std`, `impulse_sigma_gate`, `impulse_tolerance` | 0.1 / 3.0 / 0.1 | SENSOR / STATISTICAL | collision report matching (unchanged) | - |
| `clock_tolerance_s`, `contact_consistency_m`, `contact_range_m`, `contact_range_scale_m`, `rival_clearance_m` | 0.1 / 1.0 / 3.5 / 3.0 / 2.0 | LEGACY (collision matching, unchanged) | yes | - |
| `observed_alignment_*` | step 0.05, min 10 samples, 2 m/s, ratio 3 | LEGACY (clock alignment, unchanged) | yes | - |
| `link_min_samples`, `link_min_fraction` | 10 / 0.8 | LEGACY (recorder links, unchanged) | yes | - |
| `min_track_persistence_s` | 1.0 | LEGACY | yes | - |

## Relevance envelope (`semantics.*` used by FINAL)

d_rel = d_min(v_ego) + max(v_close + 3 sigma_v, 0) x H + 3 sigma_pos.

| parameter | value | category | sensitivity |
|---|--:|---|---|
| `critical_time_gap_table` | UN R157 (1.0 s at 7.2 m/s ... 1.6 s at 60 m/s) | STANDARD | - |
| `critical_min_following_distance_m` | 2.0 | STANDARD (R157 floor) | - |
| `prediction_horizon_s` (H) | 6.0 | AUDITED-FIXED (event semantics' own horizon) | - |
| 3 sigma | - | STATISTICAL | - |

Relevance gates **evidence**, never a merge on its own: cross-recorder pair evidence counts only instants that
are relevant for at least one of the two observers.  Sensor range is not relevance: a target the radar sees at
80 m that does not close in stays DETECTED/TRACKED and is not merged across recorders.

## Remaining fixed thresholds (honest list)

1. `max_association_distance_m` 2.5 m and `max_velocity_mismatch_mps` 4 m/s remain the tracker gates of every
   method: their covariance replacements were implemented, evaluated and rejected (fragmentation at impacts, wrong
   links), so the claim "no fixed association gate" is **not** made.
2. `cluster_distance_m` 2.0 m, `moving_speed_mps` 1.0 m/s: audited and justified (above), not replaced.
3. The collision-evidence windows (1.0 s, 0.2 s closing) and `touching_clearance_m` 1.0 m are fixed.
4. Fail-safe caps (`gap_cap_s` 2.0 s, `position_cap_m` 10 m, `stitch_max_gap_s` 1.5 s) bound the statistical
   rules; they are not expected to decide.
