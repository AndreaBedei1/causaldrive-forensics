# Reconstruction parameter audit

Every numeric parameter the reconstruction uses to decide tracking, identity, collision partners and relevance,
with its **category** and what is known about its **sensitivity**.  Values are those of
`configs/reconstruction.yaml` / `src/cdf/reconstruction/config.py`.  There is one reconstruction method; no
parameter selects an alternative algorithm.

Categories:

* **SENSOR**: the sensor's specification or the simulator's noise model (would be a datasheet value on a real car).
* **PHYSICAL**: a physical prior (vehicle size, mass, kinematics), not fitted to the data.
* **STATISTICAL**: a probability level or a likelihood ratio: the declared decision risk, applied to a computed
  statistic (chi-square, posterior, ratio).  Not a distance or a speed.
* **STANDARD**: taken from a regulation (UN R157 time gaps).
* **FAIL-SAFE**: a hard cap that should never decide in normal operation; documented as such.
* **AUDITED-FIXED**: a fixed threshold the reconstruction uses; justified below, not replaced.

Sensitivity sources: S = development sensitivity study (seed 200, 23 runs, exact + consumer GNSS; git history);
T = tracker-component development study (seeds 200-201, the non-dense canonical runs; git history); "-" = not
varied.  Both studies predate the adoption of the Mahalanobis position gate and the line-of-sight Doppler gate in
the tracker (commit `30e54a5`) and were not rerun afterwards: they document the identity parameters, not the
present tracker gates.

## Tracking (`tracking.*`)

| parameter | value | category | role | sensitivity / evidence |
|---|--:|---|---|---|
| `gate_probability` | 0.99 | STATISTICAL | chi-square quantile of the position gate (2 dof) and the Doppler gate (1 dof) | - |
| `measurement_std_m` | 0.5 | SENSOR | track-point measurement noise (plus the polar noise at its range); "arriving" test of the collision evidence (touching + 3 sigma) | - |
| `radial_speed_std_mps` | 0.3 | SENSOR | Doppler noise; sigma of the line-of-sight Doppler gate and of the normal-component collision rule | - |
| `radar_range_std_m` / `radar_azimuth_std_deg` | 0.25 / 0.5 | SENSOR | polar covariance of every return: lateral sigma = range x azimuth sigma | - |
| `acceleration_std_mps2` | 6.0 | PHYSICAL | process noise; drives the predicted covariance, the survival rule and the stitch density | unit test: a 0.55 s gap survives at 0.5 m/s^2, ends at 8 m/s^2 (survival follows the model, not a timer) |
| `yaw_rate_std_rps` | 0.3 | PHYSICAL | across-track process noise (v x yaw rate)^2: a fast target's prediction spreads faster sideways | - |
| `body_width_m` / `body_length_m` | 1.9 / 4.6 | PHYSICAL | body spread in the position gate; survival (3 sigma of the predicted position > a car width ends a track); same-body region of births and confirmations; impact noise within one car length | - |
| `return_likelihood_ratio` | 20 | STATISTICAL | a return inside two tracks' gates goes to the more likely one only at this ratio; otherwise it is ambiguous and updates no track | - |
| `min_track_support_s` / `min_track_updates` | 0.2 s / 3 | STATISTICAL (evidence) | confirmation by support duration and accumulated updates (rate-independent) | T: survival + confirmation vs none, exact correct 0.970 -> 0.977, missed merges 11 -> 3 |
| `nominal_vehicle_mass_kg` | 1500 | PHYSICAL | impact process noise (J/m)^2 at the recorder's own collision callbacks | - |
| `gap_cap_s` | 2.0 | FAIL-SAFE | hard upper bound on survival | unit test only (cap 0.3 s ends a track the model would keep) |
| `position_cap_m` / `doppler_cap_mps` | 10.0 / 10.0 | FAIL-SAFE | Euclidean and Doppler upper bounds of the statistical gates (how often they bind is counted in the tracking stats) | - |
| `cluster_distance_m` | 2.0 | AUDITED-FIXED | single-linkage clustering of the returns that start a track | not varied.  Justification: 2 m is just above a car width (1.9 m), below the 3.5 m lane spacing: returns of two cars in adjacent lanes are never joined at any range within the radar's azimuth resolution (0.5 deg x 100 m = 0.9 m).  Two cars closer than 2 m in one lane are one cluster: a known limitation (dense platoons at standstill). |
| `moving_speed_mps` | 1.0 | AUDITED-FIXED | a return starts a track only if moving | not varied.  1.0 m/s = 3.3 sigma of the Doppler noise (0.3 m/s): a static return passes with probability < 0.1 %.  Not a free parameter but the 3-sigma rule on `radial_speed_std_mps`. |
| `min_height_m` / `max_height_m` | 0.3 / 2.5 | PHYSICAL | object-height returns | - |
| `max_track_gap_s` / `min_track_frames` | 0.5 s / 5 | AUDITED-FIXED | smoother segment boundary and fewest measurements of a smoothed segment; identity checks across short gaps | - |
| `smoothing_innovation_sigma` | 3.0 | STATISTICAL | RTS smoother outlier rejection | - |
| `max_braking_mps2` | 30 m/s^2 | PHYSICAL | a confirmed track left without returns by its gates takes the returns on its own body whose Doppler is that of the predicted velocity slowed by at most this x dt (manoeuvre gate), and the update carries that braking as process noise | development: S06 C braking 22 m/s^2 followed; a moving track never "stops" on static scenery in one sweep (the S11 phantom of the earlier unbounded slowdown gate) |
| impact gate | moving returns only; at least max(2, half the median count of the last 5 updates) | rule / AUDITED-FIXED | a target whose velocity changed in a collision (its returns on its own body region, inside its position gate, outside every other track's gate, still moving) keeps its track; the measured line-of-sight change is an impulse (velocity variance in every direction) and an RTS boundary | unit tests (`test_semantic_evidence`); S04 b_rear_first: A follows B through its rebound off C (13.8 -> -3.4 m/s in one sweep); static returns never qualify (the road surface ahead of a moving recorder is new every sweep) |
| `contact_clearance_m` | 1.0 m | PHYSICAL | the recorder's own impact kick applies only to a body whose near surface may touch it (this + 3 sigma) | - |
| `lane_heading_std_deg` | 10 deg | PHYSICAL (map prior) | body orientation and initial velocity of a new track from its lane's direction | development: S07 young-track loss, S13/S15 abreast births |
| scenery by history | `max_track_gap_s` | rule | a stopped track takes no static return of a place that returned static echoes more than `max_track_gap_s` before it stopped (a stopping body brings its echoes with it) | development: S06/S09 stopped cars kept |
| entanglement split (code) | contact distance 0.5 x (length + width) | AUDITED-FIXED | a track ended within this of a track that competed for its returns is split from it at the evidence (two bodies exchanged returns at a contact) | development: S06 C wrong link removed; S13 passing not split |
| `identity_body_width_m` | 2.5 | AUDITED-FIXED | identity segmentation of a track | - |

## Identity and collision association (`fusion.*`)

| parameter | value | category | role | sensitivity / evidence |
|---|--:|---|---|---|
| `assignment_likelihood_ratio` (K) | 20 | STATISTICAL | one-to-one assignment: the best candidate must beat the second by K | S: **no change from 5 to 100** (exact and consumer) |
| `retrospective_new_target_density` | 3.57e-5 /m^2 | PHYSICAL (traffic density) | posterior of a stitch / retrospective link against "a new road user" | S: 3.57e-6 / 3.57e-4 move missed merges (exact 62 / 92 vs 74); false merges 0, wrong links 0, collision errors 0 at every level |
| `retrospective_min_posterior` | 0.95 | STATISTICAL | acceptance of a stitch / retrospective link | S: 0.90 / 0.99 move missed merges (exact 68 / 85 vs 74); errors unchanged |
| `anonymous_gate_probability` | 0.99 | STATISTICAL | chi-square gate of cross-recorder pair evidence | - |
| `anonymous_min_shared_samples` / `anonymous_pass_fraction` | 10 / 0.8 | STATISTICAL (evidence) | pair evidence needs 10 shared instants, 80 % inside the gate; also the resolution time | - |
| `radar_range_std_m` / `radar_azimuth_std_deg` | 0.25 / 0.5 | SENSOR | range-dependent measurement covariance in pair tests | - |
| `box_face_std_m`, `box_length_std_m`, `box_width_std_m` | 0.25 / 0.7 / 0.2 | PHYSICAL / SENSOR | centre estimate from the visible faces | - |
| `stitch_max_gap_s` | 1.5 | FAIL-SAFE | upper bound of a stitch; the decision is the stitch posterior (density decays with the gap) | unit test: posterior decays with the gap; a 4 m miss after 1.5 s is refused |
| `mutual_refinement` / `mutual_refinement_iterations` | off / 3 | switch (robustness study) / AUDITED-FIXED | the pose refinement runs whenever a pose source declares an error; the switch also forces it on error-free pose sources | - |
| `touching_clearance_m` | 1.0 | PHYSICAL | a track "touches" the recorder (collision evidence) | - |
| `contact_window_s` / `approach_window_s` | 1.0 / 1.0 | AUDITED-FIXED | windows of the collision evidence | - |
| closing window | 0.2 s (code constant, 4 sweeps) | AUDITED-FIXED | the arriving body must still be closing over the last 0.2 s | development: fixes the S15 passing-car contradiction without losing S04 b_rear_first |
| `speed_consistency_mps` | 1.5 | AUDITED-FIXED | scale of the full-speed RMSE in the association confidence only; compatibility is the normal-component rule (3 sigma of Doppler + track velocity noise) | S08 collision kept (S) |
| `impulse_relative_std`, `impulse_sigma_gate`, `impulse_tolerance` | 0.1 / 3.0 / 0.1 | SENSOR / STATISTICAL | collision report matching | - |
| `clock_tolerance_s`, `contact_consistency_m`, `contact_range_m`, `contact_range_scale_m`, `rival_clearance_m` | 0.1 / 1.0 / 3.5 / 3.0 / 2.0 | AUDITED-FIXED | collision matching | - |
| `observed_alignment_*` | step 0.05, min 10 samples, 2 m/s, ratio 3 | AUDITED-FIXED | clock alignment without a matched collision | - |
| `link_min_samples`, `link_min_fraction` | 10 / 0.8 | STATISTICAL (evidence) | recorder links | - |
| `min_track_persistence_s` | 1.0 | AUDITED-FIXED | collision-based association | - |
| short overlap (code constant `SHORT_FRAGMENT_MIN_SAMPLES`) | 5 instants | STATISTICAL (evidence) | a cross-observer pair or a recorder link with 5-9 compared instants is accepted only when every instant passes | development: S12/S13/S15 duplicates removed, 0 false merges on the canonical runs |
| long overlap (code constant `LONG_OVERLAP_FACTOR`) | 3 x `anonymous_min_shared_samples` | STATISTICAL (evidence) | a cross-observer pair compared on 30+ instants is accepted when the median instant passes both gates | development: distinct-vehicle pairs pass at most 17 % of instants (235 pairs), same-vehicle pairs 77-100 % |
| retrospective anchor | a cross-observer link compared on >= `anonymous_min_shared_samples` | STATISTICAL (evidence) | a later entity anchors a backward resolution only with a full-strength cross-observer link; every other earlier entity passing the backward test competes in the posterior | development: removed a false merge in S14 |
| identity inheritance | same pair test as a cross-observer link, one recorder only | STATISTICAL (evidence) | an unnamed track inherits recorder X when it is the same body (`pair_corrected`; a short overlap must pass every instant) as another observer's track already named X, and as no track named another recorder | development: S11 B's post-contact fragment of C named C (correct per ground truth); 0 false merges, 0 wrong links on the canonical runs |
| post-impact velocity | not compared | PHYSICAL | after an observer's own collision its velocity estimates carry the impulse: the pair test then compares the box only | unit test (`test_identity_inheritance`) |
| crowd / rival exclusion (`decisively_same_body`) | every shared instant passes (at least 2); 3 sigma of the relative uncertainty below `semantics.target_width_m` | STATISTICAL (evidence) | another observer's track that agreed with a re-acquired body at every shared instant, under an uncertainty that separates bodies a car width apart, is that body: neither a confusable neighbour nor a rival of the stitch (with consumer-grade pose sources it never applies) | development: S19 E's re-acquisitions by A stitched (missed merges 14 -> 11), 0 false merges on the canonical runs |
| entity smoother | `tracking.acceleration_std_mps2`, `tracking.max_track_gap_s` | rule | the fused per-instant states of a road user (box fit or covariance intersection) are RTS-smoothed; no smoothing across gaps, the observers' own impacts, or a velocity change beyond 3 sigma (an impact of the road user) | development: implied accelerations of S15 fused trajectories 100-1190 -> mostly below 35 m/s^2; the steps left are the observers' own impacts (their recorded pose lags the jolt) |

## Road model (`reconstruction/road.py`, `common/opendrive.py`)

| parameter | value | category | role | sensitivity / evidence |
|---|--:|---|---|---|
| map fit (`MAP_MIN_FIT`) | 0.8 | STATISTICAL | the map is the one whose driving lanes contain 80 % of the recorder's own positions with a consistent heading; else no road model (kinematic CUT_IN, straight corridor) | - |
| lane pieces | 1 m spacing; pieces narrower than 0.5 m dropped | AUDITED-FIXED | lane centre lines of the OpenDRIVE lanes (CARLA frame) | Town05: 486 pieces, every one with a successor |
| lane graph (`CONTACT_M`, `CONTINUATION_DEG`) | 0.3 m / 30 deg | AUDITED-FIXED | a piece continues another when their end points touch (OpenDRIVE contact points) and their headings agree | unit tests (`test_path_occupancy`) |
| map matching (`MATCH_RADIUS_M`, `MATCH_EDGE_MARGIN_M`, `MATCH_HEADING_DEG`, `MATCH_HEADING_STD_DEG`) | 6 m / 1 m / 45 deg / 20 deg | AUDITED-FIXED | lane candidates of each recorder position and their emission cost (offset over half the lane width, heading misfit) | - |
| transition costs (`LANE_CHANGE_COST`, `JUMP_COST`) | 3 / 20 emission units | AUDITED-FIXED | the Viterbi sequence over the whole trajectory: staying in a lane or following its successor is free, a neighbouring lane costs 3 (no flip-flop on the lane line), an unconnected jump 20 | canonical audit: no reference-path flip-flop |
| reference path (`PATH_AHEAD_M`, `PATH_BEHIND_M`) | 80 m / 10 m | AUDITED-FIXED | one path per lane episode (`ReferencePath`), traced ahead along successors; at a branch the one the recorder's own later positions take (its recorded future, never ground truth) | unit tests (junction branch, lane change) |
| lane direction search (`LANE_SEARCH_M`) | 4 m | AUDITED-FIXED | lane stretches considered for the direction of travel at a point (the target's lane-relative velocity, the lane-keeping null hypothesis) | - |
| `cut_in_lateral_speed_mps` (reused) | 0.3 | AUDITED-FIXED | the target must leave its own lane toward the recorder at least this fast | - |
| CUT_IN confirmation | an EGO_PATH_ENTRY the target's own manoeuvre was needed for | rule | the target's body at the cut-in's start, against the corridor of the entry, would not overlap it; START at the onset of the uninterrupted lateral approach | canonical audit: 9 of the 11 true cut-ins found (the 2 left: a roundabout merge, S07, and a sideswipe level with the front, S14), 0 false, onset errors within 0.3 s (`docs/STABILITY_AUDIT.md`) |
| leader | in the path, or in a confirmed cut-in | rule | UNSAFE_FORWARD_GAP only for a leader (abreast or adjacent-lane cars never) | unit tests; canonical CRITICAL_TTC audit |
| lane-keeping null hypothesis (`LANE_TRAVEL_DEG`) | 30 deg | rule / AUDITED-FIXED | a PREDICTED_OVERLAP that only the target's velocity across its own lane creates (target within 30 deg of its lane's direction) needs a confirmation: path entry (now or later) or a strike (a contact of the track, closing in over `STRIKE_CLOSING_WINDOW_S` = 0.2 s before it, or the track lost while closing within `approach_window_s` before a contact); else the course is predicted at its velocity along the lane | development: removes the passing-car episodes of S15 (A on G, J) and S18 (B on E, F) |
| lane curvature of the target prediction | dh/ds over 5 m either side; none in a junction | rule / AUDITED-FIXED | the target's predicted footprint follows the curvature of the lane it keeps (as the recorder's follows its yaw rate) | S19: the false episodes of A on C (abreast, 0.9 m gap) and B on C (two lanes away) on the 185 m curve removed |

## EGO_PATH occupancy (`semantics.*`, `local.path_occupancy`)

| parameter | value | category | role | sensitivity / evidence |
|---|--:|---|---|---|
| `path_half_width_m` | 1.5 m | AUDITED-FIXED | corridor half width around the recorder's own line | - |
| `path_edge_std_m` | 0.25 m | SENSOR / PHYSICAL | the box face spread (`fusion.box_face_std_m`): sigma of a body edge, and of a return of it | - |
| `path_occupancy_quantile` | 1.645 | STATISTICAL | definitely in / out at one-sided 95 %; between: uncertain, no change | canonical audit: 0 EGO_PATH oscillations (25 before) |
| `path_min_definite_samples` | 2 | STATISTICAL (evidence) | consecutive definite sweeps for a change of state, dated at the boundary crossing | unit tests (`test_path_occupancy`) |
| returns lower bound | second deepest on-body return; width band = half width + 2 x `path_edge_std_m`; one body length along | rule / AUDITED-FIXED | the body contains its returns: they bound its margin and its reach ahead from below where the nominal box sits short (side views) | S13: B's entry of A at 5.95 s (ground truth 5.87 s), its cut-in confirmed; a young track's mixed neighbour returns ignored (S13 A) |
| `path_hysteresis_m` | 0.5 m | AUDITED-FIXED | release of an UNSAFE_FORWARD_GAP leader (and the point-geometry ablation); the occupancy itself has none | - |

## Relevance envelope (`semantics.*`)

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

1. `cluster_distance_m` 2.0 m, `moving_speed_mps` 1.0 m/s: audited and justified (above), not replaced.
2. The collision-evidence windows (1.0 s, 0.2 s closing) and `touching_clearance_m` 1.0 m are fixed.
3. Fail-safe caps (`gap_cap_s` 2.0 s, `position_cap_m` 10 m, `doppler_cap_mps` 10 m/s, `stitch_max_gap_s`
   1.5 s) bound the statistical rules; they are not expected to decide.
4. The median of a sweep's returns is the track point; its noise is `measurement_std_m` plus the polar noise,
   not the median's standard error (the median slides over the body as the visible faces change).
