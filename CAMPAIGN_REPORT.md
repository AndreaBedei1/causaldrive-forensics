# Campaign report: three body radars (2026-10-03), S17 partial observability (2026-10-07, re-recorded 2026-10-08), safe following distance in CRITICAL_TTC (2026-10-09), CRITICAL_TTC release hysteresis and end at the collision (2026-10-10)

Front, left and right radars on each vehicle's body; a windscreen camera at 110 deg; THROTTLE events; a 2-D collision-course CRITICAL_TTC (13 runs recorded 2026-10-03).  Added 2026-10-07: S17, a causally relevant vehicle that records nothing (record: false; re-recorded 2026-10-08 with a closer cut-in), and the LLM forensic pipeline (admissible facts -> explanation -> formulas -> verification), sections 8-9.  Added 2026-10-09: CRITICAL_TTC also for an unsafe forward gap (safe following distance), a pre-entry region for CUT_IN and an occlusion gate; the 14 runs re-reconstructed from the same raw files, nothing re-recorded (section 4.3, before/after in section 5.8).  Added 2026-10-10: the end of CRITICAL_TTC became a geometric hysteresis (near contact, uncertain and occluded samples never end it; S17 regenerated, section 5.10), and a recorder's collision with the road user of an episode ends it at the collision (section 5.11).  Ground truth is read only by the evaluation, the audits and the counterfactual summary.

## 1. Campaign

Fourteen runs on a private CARLA 0.9.15 (port 3000; the user's port-2000 server was never used) with the sensors of section 2: the thirteen runs of the three-radar campaign (recorded 2026-10-03, unchanged) and S17 unobserved_causal_vehicle (recorded 2026-10-07, re-recorded 2026-10-08 with a closer cut-in, section 8).  The 13 earlier runs were not re-recorded; their reconstruction, evaluation and audits regenerate identically.  A vehicle marked 'not recorded' is a physical participant with record: false (no sensors, nothing under vehicles/).

| run | vehicles | s | true contacts (pair, time) | reconstructed | associations correct | anonymous tracks |
|---|---|---|---|---|---|---|
| S01/run_0_crash | A model3, B tt | 12.0 | A-B 6.75 s | yes (1/1 vehicle contacts) | 1/1 | 0 |
| S02/run_0_crash | A model3, B tt | 15.2 | A-B 4.65 s | yes (1/1 vehicle contacts) | 1/1 | 0 |
| S02/run_0_critical_before_cut_in | A model3, B tt | 11.5 | A-B 4.10 s | yes (1/1 vehicle contacts) | 2/2 | 0 |
| S03/run_0_crash | A model3, B tt | 15.2 | A-B 4.10 s | yes (1/1 vehicle contacts) | 2/2 | 0 |
| S06/run_0_a_front_pushed | A model3, B tt, C patrol | 13.8 | A-B 4.80 s; B-C 5.30 s; A-B 5.45 s | yes (3/3 vehicle contacts) | 2/2 | 0 |
| S06/run_0_b_rear_first | A model3, B tt, C patrol | 14.2 | B-C 4.70 s; A-B 6.25 s | yes (2/2 vehicle contacts) | 2/2 | 0 |
| S07/run_0_crash | A model3, B tt, C model3 | 13.7 | A-B 5.90 s | yes (1/1 vehicle contacts) | 1/1 | 1 |
| S08/run_0_crash | A model3, B tt, C patrol | 15.2 | A-B 4.10 s | yes (1/1 vehicle contacts) | 2/2 | 4 |
| S09/run_0_merge_conflict | A model3, B tt | 23.4 | A-B 10.25 s | yes (1/1 vehicle contacts) | 2/2 | 0 |
| S10/run_0_rolls_through | A model3, B tt | 16.0 | A-B 5.40 s | yes (1/1 vehicle contacts) | 1/1 | 1 |
| S12/run_0_near_simultaneous | A model3, B tt | 12.9 | A-B 7.15 s | yes (1/1 vehicle contacts) | 2/2 | 0 |
| S15/run_0_deflected_into_c | A model3, B tt, C tt | 14.0 | A-B 3.80 s; A-C 4.70 s | yes (2/2 vehicle contacts) | 4/4 | 2 |
| S16/run_0_consequential | A tt, B patrol, C sprinter | 12.0 | A-B 5.55 s; A-C 6.60 s | yes (2/2 vehicle contacts) | 3/3 | 4 |
| S17/run_0_crash | A tt, B patrol, C model3 (not recorded) | 11.0 | A-B 4.95 s | yes (1/1 vehicle contacts) | 2/2 | 3 |

Deleted on request (runs, directories under traces/ and their configuration): S01 avoided; S02 avoided; S05 (whole scenario); S07 full_view and occluded (replaced by S07 crash); S10 stops_safely and stops_then_proceeds; S11 (whole scenario); S12 a_arrives_first, b_arrives_first, b_fails_to_stop; S13 (whole scenario); S15 b_stops and single_impact; S16 avoided and independent.  Scenario numbers were kept.  The radar_degraded / dropout / narrow_fov / noisy sensor profiles were deleted (no run used them; their degradation block was never implemented).

## 2. Sensors

### 2.1 Three body-mounted radars (no rear radar)

CARLA traces a radar's rays in a cone of half-width tan(hfov/2) x range around its axis: a horizontal FOV of 180 deg or more folds back (measured: 200 deg -> +-80 deg, 360 deg -> a vertical slice).  The 360-degree logical sensor (six co-located roof radars) is gone; each vehicle carries three physical radars on its own body, every one recorded as its own stream (vehicles/X/radar/<id>/) with its resolved mount in its metadata (``sensor_transform``).

| radar | mount (from the vehicle's own bounding box) | yaw | H FOV | V FOV | range | points/s | tick | height |
|---|---|---|---|---|---|---|---|---|
| front | front face centre, 0.05 m beyond x_max, y = box centre | 0 | 150 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |
| left | left side, mid-length (x = box centre), 0.05 m beyond y_min | -90 | 140 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |
| right | right side, mirrored | +90 | 140 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |

Resolved mounts (vehicle frame, x forward, y right, metres):

| blueprint | box L x W | front | left | right |
|---|---|---|---|---|
| model3 | 4.79 x 2.16 | (2.475, 0.000) | (0.029, -1.132) | (0.029, 1.132) |
| tt | 4.18 x 1.99 | (2.140, 0.000) | (-0.000, -1.047) | (-0.000, 1.047) |
| patrol | 4.60 x 1.93 | (2.295, 0.000) | (-0.057, -1.016) | (-0.057, 1.016) |
| sprinter | 5.92 x 1.99 | (2.997, 0.004) | (-0.011, -1.040) | (-0.011, 1.048) |

Measured with a car target on the private engine (returns per sweep at 10 / 25 / 40 / 60 m, all three radars together; bearing from the recorder, + = right):

| bearing | 10 m | 25 m | 40 m | 60 m |
|---|---|---|---|---|
| 0 deg | 76 | 19 | 11 | 7 |
| 30 deg | 149 | 28 | 11 | 4 |
| 60 deg | 150 | 42 | 15 | 6 |
| 90 deg | 112 | 42 | 24 | 16 |
| 120 deg | 67 | 11 | 5 | 3 |
| 140 deg | 91 | 14 | 5 | 2 |
| -90 deg | 116 | 39 | 24 | 17 |

- Field of view, geometric (tests/test_three_radars.py): front +-46 deg at 5 m, +-61 at 10 m, +-69 at 25 m, +-73 at 80 m; sides from 33 deg (5 m) / 27 (10 m) / 22 (40 m) to 147 / 153 / 158 deg.  Bearings 30-55 deg are seen by the front radar and a side radar together from 10 m on: no gap and no discontinuity at the front -> side transition (a target passing from one to the other stays one track, tested synthetically and seen in the campaign).
- Rear blind zone (measured): a car directly behind is not seen within +-12 deg at 5 m and +-16 deg from 10 to 40 m (total 24-32 deg); for a point target the blind cone is 41-53 deg wide from 10 m on, up to 65 deg at 5 m.  A follower in the same lane is invisible to the car it follows (S01, S06, S07: B never tracks A; S16: A never tracks B).
- The radars never see their own vehicle (0 own-body returns; returns inside the footprint are dropped anyway).  Vertical FOV 20 deg: 10 deg halves the returns on cars at 40-60 m, 30 deg adds mostly road and sky returns.  12000 points/s per radar: 6000 left 4-7 returns on a car at 60 m, 24000 doubled the scenery returns without changing first detections.

### 2.2 Occlusion A -> B -> C

Lab (private engine, 864 configurations: observer A in {model3, audi.tt, sprinter}, B and C in {model3, audi.tt, nissan.patrol, sprinter}, gaps A-B 5 / 10 m, B-C 5 / 15 m, C lateral offset 0 / 0.5 / 1.0 m): body returns on C per sweep, mean over the gaps:

| B (middle) | C (hidden) | C aligned | C 0.5 m aside | C 1.0 m aside |
|---|---|---|---|---|
| model3 | model3 | 0.00 | 0.02 | 0.46 |
| model3 | tt | 0.00 | 0.02 | 0.53 |
| model3 | patrol | 0.00 | 0.02 | 0.58 |
| model3 | sprinter | 0.20 | 0.26 | 1.04 |
| tt | model3 | 0.00 | 0.06 | 0.71 |
| tt | tt | 0.00 | 0.04 | 0.59 |
| tt | patrol | 0.03 | 0.12 | 0.72 |
| tt | sprinter | 0.38 | 0.42 | 1.28 |
| patrol | model3 | 0.00 | 0.03 | 0.71 |
| patrol | tt | 0.00 | 0.01 | 0.57 |
| patrol | patrol | 0.00 | 0.07 | 0.62 |
| patrol | sprinter | 0.02 | 0.12 | 0.88 |
| sprinter | model3 | 0.00 | 0.00 | 0.26 |
| sprinter | tt | 0.00 | 0.00 | 0.30 |
| sprinter | patrol | 0.00 | 0.00 | 0.23 |
| sprinter | sprinter | 0.00 | 0.00 | 0.49 |

- Aligned behind a car or SUV, a car or SUV C returns nothing: the radar 0.6 m above the road does not look over a low car (B sedan, C sedan: 0.00).  Only a van taller than B shows its upper body (sprinter behind a model3 / audi.tt: 0.2-0.4 returns per sweep), as it physically should.
- In the recorded S07 (A model3 -> B audi.tt -> C model3): A tracks B from 0.00 s to the end and never has a track on C (tests/test_campaign_perception.py).  A received 13 returns on C's body in 4 of 274 sweeps: 3 single returns under B's floor (the ray crosses B's rear plane 0.12-0.15 m above the road) and 10 at the impact instant, A's bumper radar pressed against B.  None over B's roof, none through B; no rule hides C: occlusion is CARLA's ray casting.

### 2.3 Camera

One RGB camera per vehicle, 1280x720, 10 Hz, behind the windscreen at its top centre in front of the interior mirror, per blueprint (checked visually on every campaign blueprint with physics on; a mount further back sees the windscreen header across the horizon):

| blueprint | x | z |
|---|---|---|
| model3 | 0.50 | 1.30 |
| tt | 0.40 | 1.18 |
| patrol | 0.60 | 1.62 |
| sprinter | 1.80 | 2.10 |

FOV chosen 110 deg (tested 100 / 110 / 120 on GT replays of the campaign with the new mounts): first STOP detection at 24.1 / 24.1 / 22.4 m (S10 A), 31.2 / 30.4 / 29.5 m (S12 A), 25.6 m each (Town10HD STOP), YIELD 20.7 / 15.9 / 10.5 m; at 100 deg the plate leaves the image 0.4-0.7 m earlier than at 110 deg (lost before the stop line at the S12 junction), at 120 deg it is smaller (later first detection).  110 deg is the smallest FOV that keeps the sign until the stop.  Images are not persisted; signs are detected on board (section 4.7).

### 2.4 Recording health

- Every recorder of every run (verify_campaign): the three radars with the expected ids, FOVs, range, points/s and mounts at the box faces (+0.05 m); one sweep per tick for every radar, 0 queue drops, 0 frames without measurement, 0 missing frames; the RGB camera complete (frames = ticks / 2), 0 drops, 0 duplicates; ego.jsonl and controls.jsonl one record per tick; the recorders' collision callbacks equal the ground-truth callbacks; metadata (footprint, mounts, camera) present.  Problems: none.
- The depth camera (800x600, 20 Hz, not used by the reconstruction) misses frames on the second and third vehicle when three cameras render per tick (as in the earlier campaigns): this does not affect any output.

## 3. Scenarios

- Recording start (all runs).  CARLA spawns a vehicle in neutral; given its initial velocity directly, the automatic gearbox engaged first gear at cruising speed after the recording had started and the over-revving engine braked the car at 10-20 m/s^2 for about 0.5 s under full throttle (every non-Tesla vehicle of the 360-degree campaign: e.g. S06 C -15.8 m/s^2 at 0.75 s).  That was read as a braking target.  Now each moving vehicle is launched over 12 ticks in the gear its gearbox would hold at that speed, at a nominal cruising throttle, and its speed controller starts from that throttle; it is spawned 0.6 s x its speed back along its lane, so the recording starts with it at its scenario spawn point.  Measured: |acceleration| <= 0.45 m/s^2 in the first second for every campaign blueprint (simulation.launch_ticks / launch_throttle).
- post_impact_mode coast (A in S16, B in S06 a_front_pushed): no pedals, no steering, gearbox in neutral, and the brake held once at rest.  With the clutch engaged CARLA's zero-throttle engine braking decelerates a car at 4-7 m/s^2, several times a real car rolling off the pedals; in neutral a shunted car is carried on as it should be.
- S06 a_front_pushed: B's brake action used to expire at 5.75 s and its post-impact mode was 'drive': B drove into C under full throttle and kept pushing it for 24 s.  Now B stops 3 m short of C and holds its brake; A, following 4.5 m behind at 14 m/s, strikes it while it is still slowing (3.2 m/s) and pushes it into C.  A stationary braked car cannot be pushed in CARLA (measured: it stops the striking car dead), hence the closer following.
- S07 occluded_chain_stop (new single variant crash): A -> B -> C in one lane; C stops hard at 3.0 s (permanent stop), B stops 13.7 m short of C, A brakes late (5.3 s) and runs into B at 5.90 s.  One collision, A-B.
- S07 C and S08 C: their stop is now a permanent stop (the brake action used to expire near the end of the recording and they drove off).
- S09: both vehicles start 67-68 m (8.4 s at 8 m/s) further back along their own routes (A still on the circulating lane; the routes contain the original ones exactly), B's acceleration moved by the same time.  Collision at 10.25 s (was 1.8 s), same place and pair; first CRITICAL_TTC at 6.65 s.
- S12 near_simultaneous: braking 0.3 instead of 0.95, started earlier so that both stop at their stop lines; brake released at 4.87 / 4.73 s.  Stops (STOP_START -> STOP_END) 1.50 s (A) and 1.55 s (B); both pull away within 0.05 s; collision at 7.15 s.
- S16 consequential (rebuilt): three lanes; C, a van, drives in the left lane at 9 m/s; A moves over into the left lane behind C and slows to its speed; B follows A too closely, reacts late and runs into A at 5.55 s while A is angled across the lane line; the shunt (A from 8.2 to 11.3 m/s, coasting in neutral) carries A into the back of C at 6.60 s.  No scripted deflection; without B, A's merge ends 2.0 m behind C (checked).  A sideways knock is not used because CARLA does not carry a struck car sideways (measured: a rear-corner impact turned A by at most 7 deg and moved it 0.8 m; a sideswipe 0.3 m).
- S15 deflected_into_c keeps its scripted post-impact deflection (unchanged on request; documented in section 7).
- The two reference links were studied for geometry: their patterns (rear-end chains, junction crossings, roundabout merge, cut-in, multi-vehicle pile-up) are covered by S01-S16; the remaining elements (a lane-change dispute, removed with S13 on request; hit-and-run; weather) are not new geometries.  No scenario was added in the three-radar campaign.
- S17 unobserved_causal_vehicle (2026-10-07, re-recorded 2026-10-08, section 8): a close cut-in by a vehicle that records nothing (record: false) makes A swerve into B; A's swerve is a reactive action fired when C's box is inside A's corridor within 3 m of its front (privileged corridor_clearance trigger, ground_truth/triggers.jsonl only); without the swerve A runs into C.

## 4. Reconstruction

### 4.1 THROTTLE_START / THROTTLE_END

From the recorder's own accelerator command (controls.jsonl): THROTTLE_START at or above 0.10, THROTTLE_END at or below 0.05, a release shorter than 0.2 s does not end it (throttle_on_threshold, throttle_off_threshold, throttle_release_debounce_s).  The recorded throttle is 0 or 0.15-1.0; only ~0.5 % of the samples lie in 0.02-0.10.  A throttle already applied at the first sample is THROTTLE_START flagged active_at_first_observation.  The raw pedal values stay facts in the trace (EGO_CONTROL).  No STRONG_THROTTLE / HARD_THROTTLE remains; BRAKE is unchanged.  THROTTLE is an ego state of the perceived world, rendered in local/global graphs, replay and report.

### 4.2 Three radars in the reconstruction

Each return is placed from its own radar's mount along that radar's line of sight; its Doppler speed is compensated with that radar's own velocity, the displacement of its mount point over the sweep (lever arm of a turning, pitching body included), as CARLA measures it.  The Kalman filter takes one Doppler row per radar that saw the track.  range_m stays the raw range from the observing radar; clearance_m is the distance from the recorder's footprint to the target's near surface.  Static scenery stays static in turns (synthetic test: < 0.02 m/s with a 20 deg/s turn, while the front radar's lever arm alone is 0.87 m/s).

### 4.3 CRITICAL_TTC (src/cdf/reconstruction/conflict.py)

At each track sample the next 6 s are predicted in the recorder's frame, every 0.05 s:

- recorder: its footprint inflated into an envelope (1 m ahead and behind, the standstill margin d0; 0.3 m at the sides) along its current path (constant speed and yaw rate: a circular arc);
- target: a nominal box 4.6 x 1.9 m behind its observed near surface (the corner towards the recorder seen obliquely, the facing side seen along an axis), moving at its estimated velocity; its velocity across the recorder's heading counts only beyond its uncertainty (a car keeps its lane unless the evidence says otherwise); a target decelerating at 1 m/s^2 or more keeps that deceleration until it stops.

Collision course = the two boxes overlap within the horizon; TTC = the first overlapping instant; the overlap span is the temporal occupancy overlap of the conflict area.  A target closing in radially that passes ahead of or behind the envelope never overlaps: no collision course.  Required deceleration a_req = the smallest deceleration (bisection) that removes every overlap when the braking vehicle reacts after 1 s and brakes to a stop along its path; the braking vehicle is the recorder, or the target when even an instant stop of the recorder cannot avoid it (a car from behind).  CRITICAL_TTC_START when a collision course needs a_req >= 6 m/s^2 (available, hard non-emergency braking); the end is the release below (a_req below 75 % of that, or no course, is one of its conditions).  No claim either way while the track's estimate is not known: position or velocity std above 1 m / 1 m/s, or the track younger than 0.5 s (UNKNOWN).

For a target ahead in the same lane this is the stopping-capability check of a following driver: reaction distance v x 1 s, braking distance v^2 / (2 x 6 m/s^2), 1 m left over, against a lead car that keeps its speed or its measured deceleration.  Example: at 14 m/s behind a stopped car the state turns critical with the near surface within 33.7 m of the vehicle origin (tests/test_critical_ttc.py).  A car ahead at the recorder's own speed is never on a collision course, however close: this reason is PREDICTED_OVERLAP.

UNSAFE_FORWARD_GAP (added 2026-10-09, simplified 2026-10-10) is the second reason: a leader closer than the safe following distance, collision course or not.  Clearance = from the recorder's front face to the rear face of the target's nominal box, along the recorder's heading (never the radar range).  Safe following distance:

    d_min = max(v_ego x t_front_UN_R157(v_ego), 2.0 m)

with t_front from the UN R157 (ALKS, M1/N1) table 7.2 km/h 1.0 s, 10 km/h 1.1 s, 20 km/h 1.2 s, 30 km/h 1.3 s, 40 km/h 1.4 s, 50 km/h 1.5 s, 60 km/h 1.6 s, linear in between, the ends held (no extrapolation beyond 60 km/h; the campaign stays below it).  The 2 m minimum is part of the rule; no margin is added and the target's speed is not used (the gap can be unsafe at equal speeds or with a slightly faster target).  The 2026-10-09 version also took the larger of this and a braking distance (v x 1 s + v^2 / 12 - v_lead^2 / 12 + 1 m); that branch is removed from the safe gap (the reaction time and the 6 m/s^2 now belong to the collision-course reason only).  CRITICAL_TTC is the event's historical name: an UNSAFE_FORWARD_GAP alone has no classical TTC (ttc_s null; the time headway is not a TTC).

A leader is a road user moving in the same direction, its body ahead of the front face and either overlapping the path corridor (+-1.5 m) or within 1.0 m of it while approaching it laterally (0.3 m/s beyond the estimate's uncertainty), with the recorder moving (>= 1 m/s).  Cars behind, beside or two lanes away, and a car keeping its own lane next to the corridor, are never critical for this reason; crossing and oblique conflicts keep the collision-course model.  No TTC is invented: ttc_s stays null without a predicted overlap.  The reason starts below d_min; it ends only through the release below; the estimate gates (std, 0.5 s track age) apply as before.  The conflict model's outputs (critical_reason, longitudinal_clearance_m, lateral_body_gap_m, time_headway_s, minimum_time_gap_s, time_gap_distance_m, required_safe_distance_m, safe_distance_margin_m, forward_region, line_of_sight_occluded, inside_safety_envelope) are TRACK_STATE facts of the local trace; the forensic packet drops them (TRACK_STATE_REMOVED) and the leak guard refuses them: the 14 packet SHA-256 are unchanged.

Why a lateral approach is required beside the corridor: in these 3.5 m lanes a car keeping its own lane next to the recorder's has its body about 1.0 m outside the 3.0 m corridor (ground truth: 0.92-1.01 m in S16 and S17), and the nominal box placed from a radar track misses that by up to ~0.7 m either way (S16's van in the next lane: 0.30-0.66 m; S02's cutting-in car seen from behind: within 0.1 m).  A purely geometric 1.0 m margin made the van a leader of A for the whole of S16 and B's overtaking of A in S17 critical.

References, used as engineering anchors only: art. 149 of the Italian Highway Code (a distance that allows the following vehicle to stop in time and avoid a collision with the one ahead) and Directive 2006/126/EC (adequate distance to the vehicles in front and at the side; a speed that allows stopping within the visible free road), which prescribe no numbers; UN Regulation No. 157 (ALKS), whose minimum time gaps apply to automated lane keeping systems and whose text names the temporary disruption of the following distance by a cutting-in vehicle; UN Regulation No. 152 (AEBS), which asks for a braking demand of at least 5.0 m/s^2 when an imminent car-to-car collision is detected.  There is no single European critical-TTC threshold for human drivers; the 1 s reaction time and the 6 m/s^2 decelerations are this reconstruction's modelling assumptions, not values prescribed by EU or UNECE rules.  Limits: constant velocity and yaw rate (no intent, no lane geometry: a target turning in a roundabout is predicted straight), a nominal target size, braking as the only avoidance manoeuvre, one track at a time for the prediction.

CUT_IN (same date): a cut-in now also needs the target's nominal body within 1.0 m of the corridor (cut_in_preentry_margin_m), so a car still crossing a lane further away is not cutting in yet (S17: B's CUT_IN_FROM_RIGHT on C, which was moving from the right lane into A's middle lane two lanes away, is gone).  Occlusion gate: a track sample whose line of sight from the recorder's body to its near surface crosses another track's nominal box grown by 0.5 m (the radar's position noise) is seen past that vehicle; it gives no CUT_IN and no UNSAFE_FORWARD_GAP evidence either way (its returns can be partly hidden or mixed with the nearer vehicle's).  It removes the apparent lateral approach of C seen by B past A in S17 (at 4.55-4.95 s the track most likely picked up returns of A's swerving front: ground truth puts A's front corner about 1 m from C's rear corner, on B's line of sight) and of S16's van seen by B past A (B's former CUT_IN_FROM_LEFT 1.35-2.70 s on a van that never moved laterally).  The collision-course prediction is not gated.

Robustness added in this campaign: the target's deceleration used by the prediction is bounded by what the forward-filtered track shows up to that instant (the smoother would otherwise announce an abrupt stop, a crash, up to 0.2 s before it happens); a confirmed track follows its target through an abrupt stop (section 4.5); the 0.5 s minimum track age (a track 0.1 s old at 74 m in S15 drifted laterally and was claimed critical by the first model).

Release (CRITICAL_TTC_END, 2026-10-10; conflict.py point 5, local.critical_intervals).  The start conditions are gates, the end is a geometric hysteresis.  Each sample is critical, clearly resolved or neither; the state ends only after 0.2 s of clearly resolved samples without interruption, the END being the first of them.  Clearly resolved means: a known estimate; no collision course, or one braking avoids below 0.75 x 6 m/s^2; the target's box outside the recorder's safety envelope, unless recorder and target both move slower than 1 m/s (a target touching the envelope that closes in below 1 m/s starts no collision course, but that it stops closing in does not end one); and, when UNSAFE_FORWARD_GAP was a reason of the episode, that leader seen without occlusion and gone: the recorder below 1 m/s, or the clearance beyond 1.10 x d_min, or no part of its body ahead of the front face, or its body more than path_hysteresis_m = 0.5 m outside the corridor (the EGO_PATH_EXIT hysteresis, now a configuration parameter) and not moving back toward it beyond its velocity std.  A reason that never applied in the episode cannot hold it.  Uncertain, occluded and near-contact samples are no evidence of safety: they interrupt the release.

Collision (2026-10-10; conflict.py point 6, local.contact_partners).  CRITICAL_TTC describes the pre-collision threat episode.  When the recorder collides with the road user of an active episode, the episode ends at the collision's timestamp (COLLISION listed first, CRITICAL_TTC_END at the same instant), whatever the release says.  The continuing contact is a post-impact state, not a new episode: none starts for that pair while the contact lasts (to its last callback, from the contact segmentation of section 4.4) nor afterwards until the conflict has been clearly resolved by the release; a genuinely new conflict can then start a new episode.  The termination is pair-specific.  The collision sensor names no partner: it is the recorder's only track CLOSING just before the contact and touching it at the contact (near surface within fusion.touching_clearance_m = 1 m of its body); with none (a car striking from the rear blind zone) or several, nothing is attributed and the release alone ends the state.

### 4.4 Collisions

- A burst of callbacks weaker than 1000 N*s never starts a new contact within 0.5 s of the previous one (min_new_impact_impulse): S16's A-C scrape (2 s of 35-320 N*s bursts) is one collision, not three.
- A contact that absorbed later bursts lists them (merged_bursts).  An unmatched report of one recorder is matched to an identical-impulse burst inside another recorder's contact, between graphs already linked by other matches and at their clock offset: S06 a_front_pushed, where A strikes B again 0.15 s after B's impact on C (B's sensor reports magnitudes only and merges the two), now gives the three true contacts A-B, B-C, A-B.

### 4.5 Tracking

- Abrupt stop: when a target crashes, its Doppler speed leaves the gate in one sweep and the track was dropped (S06 b_rear_first: A lost B the instant B hit C and then drove into the stopped B with no perception event).  A confirmed track whose previous sweep was free of foreign returns may now take at least 3 returns around it whose speed lies between standstill and the predicted one (min_slowdown_returns).  A road crest or a guardrail next to a target is foreign clutter in every sweep, so it never qualifies: across the campaign the rule changes only that run.
- Evaluated and not adopted: an anisotropic measurement noise for extended targets and a different surface-offset definition (synthetic gains, no gain on the recorded runs; section 5.6).

### 4.6 Identity association

Several compatible tracks for one contact remain ambiguous, unless exactly one of them touches the recorder at the contact (observed within one sample of it, within 1.0 m) while every rival is at least 2.0 m away (touching_clearance_m, rival_clearance_m).  S16: the van C is seen by A as two tracks; the one at C's rear (0.07 m) is its partner, the other (2.99 m) stays anonymous.

### 4.7 STOP / YIELD detection (src/cdf/perception/traffic_signs.py)

Recalibrated for the 1280x720 110-deg camera on real CARLA frames: red mask (HSV), external contours not touching the image border, polygon approximation; STOP = a compact regular octagon (compactness >= 0.85, >= 6 vertices, aspect 0.70-1.15, red fraction 0.55-0.88, white letters >= 0.30 of the inner area, not in the lower half of the image); YIELD = an inverted triangle (3-4 vertices, box fill 0.38-0.62, solidity >= 0.8, white interior >= 0.30, top edge >= 1.6 x the bottom).  Tracking: centre gap <= 8 % of the image width, size ratio <= 1.8, aspect spread <= 0.35, >= 3 detections to confirm; relevant to the path when the sign came within 30 deg of the camera axis and grew.  No CARLA label, id or map lookup; ground truth only offline.

S15 false STOP (360-degree campaign, A after its first collision): a red advertising board with a white curved letter behind a fence, cut by the right image border (bbox [778, 233, 22, 25] at frame 7413, 5 vertices, fill 0.96, redness 0.93, confidence 0.83-0.95) and confirmed as a STOP from frame 7383 to the end, plus a brick-facade blob at the left border at frame 7373.  Fixed in general: border contact rejects a candidate, the octagon test needs compactness and 6+ vertices, a STOP needs its white letters.  Regression fixtures (real frames) in tests/data/signs.

## 5. Validation

### 5.1 Contacts, associations, CRITICAL_TTC

| run | CRITICAL_TTC_START (recorder->true target, local s; (gap) = UNSAFE_FORWARD_GAP at the start) | associated (all correct) | anonymous (true identity, offline) |
|---|---|---|---|
| S01/run_0_crash | A->B 4.40 | A:track_001=B | - |
| S02/run_0_crash | A->B 1.80 (gap) | A:track_001=B | - |
| S02/run_0_critical_before_cut_in | A->B 2.60 (gap); B->A 2.70 | A:track_001=B, B:track_001=A | - |
| S03/run_0_crash | A->B 2.55; B->A 2.60 | A:track_001=B, B:track_001=A | - |
| S06/run_0_a_front_pushed | A->B 0.50 (gap); B->C 0.50 (gap) | A:track_001=B, B:track_001=C | - |
| S06/run_0_b_rear_first | A->B 4.65 (gap+overlap); B->C 0.50 (gap) | A:track_001=B, B:track_001=C | - |
| S07/run_0_crash | A->B 0.50 (gap); B->C 3.40 | A:track_001=B | B:track_001 (is C) |
| S08/run_0_crash | A->B 2.55; B->A 2.60 | A:track_002=B, B:track_002=A | A:track_001 (is C), B:track_001 (is C), C:track_001 (is A), C:track_002 (is B) |
| S09/run_0_merge_conflict | A->B 6.90; B->A 6.65 | A:track_001=B, B:track_001=A | - |
| S10/run_0_rolls_through | A->B 3.40; B->A 3.60 | A:track_001=B | B:track_001 (is A) |
| S12/run_0_near_simultaneous | A->B 5.90; B->A 6.05 | A:track_001=B, B:track_001=A | - |
| S15/run_0_deflected_into_c | A->B 2.55; A->C 3.75; B->A 2.50; B->A 3.95; C->A 3.75 | A:track_001=C, A:track_002=B, B:track_002=A, C:track_001=A | B:track_001 (is A), C:track_002 (is B) |
| S16/run_0_consequential | A->C 5.20 (gap); B->A 0.50 (gap); C->A 5.60 | A:track_001=C, B:track_001=A, C:track_001=A | A:track_002 (is C), B:track_002 (is C), B:track_003 (is C), B:track_004 (is C) |
| S17/run_0_crash | A->C 2.60 (gap); A->B 3.80; B->A 4.15 | A:track_002=B, B:track_001=A | A:track_001 (is C), B:track_002 (is C), B:track_003 (is C) |

Every true vehicle contact is reconstructed, every association is correct, no extra collision node.  Tracks lost before their contact but associated: S16 C:track_001 -> A (last observed 0.15 s before the contact); synthetic regression: lost 0.85 s before (window 1.0 s).

### 5.2 S08 CRITICAL_TTC before and after

Before (360-degree campaign, previous model: TTC from range rate against a stopping-distance threshold), eight CRITICAL_TTC_START:

| pair | t | rel. long / lat m | clearance | v ego | v target | closing | TTC | t_CPA | d_CPA | d_CPA clear. | relation | to junction ego / target m | arrival at crossing ego / target s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A->C | 2.20 | 36.6 / -3.8 | 34.3 | 9.7 | 8.7 | 18.2 | 1.88 | 1.99 | 3.90 | 2.82 | OPPOSING | 18.8 / 19.2 | never / never |
| A->B | 2.45 | 17.1 / 23.9 | 27.9 | 9.3 | 12.6 | 15.6 | 1.79 | 1.88 | 0.37 | 0.00 | CROSSING | 16.5 / 26.9 | 1.93 / 2.04 |
| A->C | 3.50 | 20.4 / -3.1 | 17.9 | 9.5 | 0.0 | 9.4 | 1.90 | 2.14 | 3.02 | 1.65 | UNKNOWN | 6.6 / 15.3 | - / - |
| B->A | 2.35 | 24.9 / -18.6 | 29.4 | 12.1 | 9.2 | 15.3 | 1.93 | 2.04 | 0.18 | 0.00 | CROSSING | 28.1 / 17.4 | 2.24 / 2.01 |
| B->C | 2.45 | 28.1 / 14.4 | 29.2 | 12.5 | 4.2 | 14.9 | 1.96 | 2.00 | 7.48 | 6.25 | UNKNOWN | 26.9 / 17.1 | 2.37 / 1.75 |
| C->A | 2.25 | 36.4 / -4.1 | 34.3 | 8.6 | 9.6 | 18.1 | 1.90 | 2.00 | 4.02 | 3.04 | OPPOSING | 18.8 / 18.4 | never / never |
| C->B | 2.80 | 13.2 / -24.1 | 25.5 | 0.8 | 12.6 | 11.6 | 2.19 | 2.01 | 10.56 | 7.45 | CROSSING | 15.4 / 22.4 | 15.88 / 1.94 |
| C->B | 3.55 | 13.1 / -15.2 | 18.1 | 0.0 | 12.6 | 9.6 | 1.90 | 1.21 | 13.12 | 10.16 | CROSSING | 15.3 / 13.0 | - / - |

Only A->B (2.45 s) and B->A (2.35 s) concern the vehicles that collide.  A->C and C->A were two oncoming cars in adjacent lanes passing at d_CPA 3.9-4.0 m (their paths never cross); B->C and C->B passed 7-13 m apart (C stopped short of the junction); A->C at 3.5 s was C standing still beside A's lane.  The old model called them critical from the range rate alone.

After (this campaign, model of section 4.3), two CRITICAL_TTC_START:

| pair | t | rel. long / lat m | clearance | v ego | v target | closing | TTC | t_CPA | d_CPA | d_CPA clear. | relation | to junction ego / target m | arrival at crossing ego / target s | occupancy overlap s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A->B | 2.55 | 17.8 / 21.0 | 24.6 | 10.1 | 12.0 | 16.0 | 1.70 | 1.71 | 0.69 | 0.00 | CROSSING | 16.5 / 23.3 | 1.82 / 1.72 | 0.49 |
| B->A | 2.60 | 19.9 / -16.9 | 22.9 | 12.6 | 9.4 | 16.0 | 1.65 | 1.62 | 2.12 | 0.00 | CROSSING | 22.7 / 16.0 | 1.67 / 1.76 | 0.49 |

Both on a collision course in 2-D (the predicted boxes overlap 1.65-1.7 s ahead), arriving at the crossing point within 0.1 s of each other (overlapping occupancy 0.49 s), with braking needs beyond 6 m/s^2 after a 1 s reaction.  C, the third viewpoint, raises none: the oncoming A passes it in its own lane, B crosses 13 m ahead of the stopped C.  Collision at 4.10 s.

### 5.3 Scenario timing

- S07: C stops at 4.35 s, B at 4.85 s (13.7 m short of C), A brakes at 5.25 s and strikes B at 5.90 s; one collision.
- S09: approach of 6.65 s before the first CRITICAL_TTC (B on A at 6.65 s, A on B at 6.90 s), collision at 10.25 s.
- S12: STOP_START -> STOP_END 3.70 -> 5.20 s (A, 1.50 s) and 3.60 -> 5.15 s (B, 1.55 s); THROTTLE_START at the restart of each; collision at 7.15 s.
- S16: C at 8.6-9.2 m/s until the second collision; A-B at 5.55 s, A-C at 6.60 s; no deflection.
- S10: A's STOP window opens at 1.15 s with the sign 17.4 m ahead (camera) and lasts to 2.75 s.
- S17: C's cut-in starts at 2.0 s (its lateral motion at 2.45 s); its left side enters A's lane at 2.85 s; the trigger fires at 3.30 s (2.32 m box to box); A's swerve starts at 3.65 s (1.96 m); A-B contact at 4.95 s; C closest to A 0.59 m (5.20 s).

### 5.4 Signs

| run | recorder | STOP/YIELD windows | sign actors on its path (offline) | STOP_START |
|---|---|---|---|---|
| S03/run_0_crash | A | - | stop#58, stop#59 | [4.75] |
| S03/run_0_crash | B | - | stop#54, stop#57 | [4.6] |
| S08/run_0_crash | A | - | stop#58, stop#59 | [4.75] |
| S08/run_0_crash | B | - | stop#54, stop#57 | [4.6] |
| S08/run_0_crash | C | - | stop#27, stop#63 | [2.9] |
| S10/run_0_rolls_through | A | sign-0 1.15-2.75 s | stop#27, stop#63 | [5.5] |
| S10/run_0_rolls_through | B | - | stop#36 | [5.6] |
| S12/run_0_near_simultaneous | A | sign-0 0.20-2.75 s | stop#56 | [3.7, 7.65] |
| S12/run_0_near_simultaneous | B | sign-0 0.70-2.80 s | stop#29, stop#53 | [3.6, 7.45] |
| S15/run_0_deflected_into_c | A | - | stop#36 | [5.1] |
| S15/run_0_deflected_into_c | B | sign-0 1.10-2.25 s | stop#27, stop#63 | [4.0] |
| S15/run_0_deflected_into_c | C | - | stop#62 | [5.0] |

Over the campaign: 89 STOP candidates in 4640 camera frames, 4 confirmed STOP tracks, all on real signs (S10 A 19 detections, S12 A 29, S12 B 24, S15 B 15); 2 single-frame candidates rejected by the tracker (S08 B, S15 B); 0 YIELD candidates (no YIELD sign on these routes; the YIELD detector is validated on the Town10HD yield sign: every frame of the approach).  S15 A: no sign at all (the phantom STOP is gone).  S03 / S08 junction 'STOP' is a road marking: never a sign.  S17 (2 x 111 frames, same road as S01 / S02 / S16): no sign candidate, no sign track and no sign trigger volume on its path (the audit, re-run on the 14 runs with the sign actors extracted again, adds no row; the 2026-10-08 re-recording drives the same lanes).

### 5.5 Radar visibility (privileged audit, traces/radar_visibility_audit.json)

First detection of every vehicle by every recorder against what could be seen.  The delays come from buildings at junction corners (OCCLUSION static: S03, S08, S10, S12, S15, 2.0-2.7 s) and from the rear blind zone (a follower directly behind: never inside the field of view).  No track is delayed by the tracker by more than 0.3 s once usable returns exist.

### 5.6 Track quality against ground truth (offline)

| aspect | samples (< 10 m) | clearance bias m | clearance rms m | velocity rms m/s | velocity p95 m/s | heading rms deg |
|---|---|---|---|---|---|---|
| front | 3068 | 0.30 | 0.65 | 0.64 | 0.99 | 7.0 |
| oblique | 923 | 0.31 | 0.48 | 0.71 | 1.73 | 6.9 |
| side | 2115 | 0.37 | 0.58 | 0.49 | 1.13 | 9.3 |
| rear | 300 | 0.89 | 0.94 | 0.66 | 1.78 | 3.7 |
| all | 6406 | 0.35 | 0.62 | 0.62 | 1.22 | 7.0 |

The clearance is biased high (track farther than the box): radar returns lie on the body, not on its bounding-box extremes; largest for a van seen from behind (rays under its high floor reach the axle: S16 A->C +1.0 m) and for cars side by side in the roundabout (S09 A->B +1.4 m).  Passing from the front radar's field to a side radar's the median of the returns slides from the rear face onto the side face: a known extended-target effect, bounded in the tests.

### 5.7 Tests

384 tests pass on Python 3.8 (CARLA environment) and 3.14 (2026-10-10), among them tests/test_critical_collision.py (a collision ends the active episode at its own timestamp, COLLISION ordered first; no episode invented by a collision without one; pair-specific with another critical track; no new episode during a 0.8 s contact; a new one after a real separation and a new convergence; multi-collision A-B then B-C; a car still pressed against the recorder and two touching tracks are no partner; S17 A-B / B-A ended at the collision, A about the anonymous track not; S02 order), tests/test_critical_release.py (the end of CRITICAL_TTC: a 1 cm exit from the leader gate and a one-sample loss of lateral approach end nothing, a leader clearly aside ends it after the path hysteresis and the debounce, a temporary occlusion and near contact with a closing speed below 1 m/s end nothing, separation or both vehicles at rest end it; S17 B about A held until the collision, A about C ended only once C is clearly aside; S02 cut-in inside the critical episode), tests/test_forward_gap.py (safe following distance: UN R157 table and interpolation, the required distance, a close car at the same speed, the same car far enough, a car behind, beside, front-lateral entering / keeping its lane, two lanes away, crossing traffic unchanged, a standing recorder, uncertain and occluded estimates, the 1.10 release hysteresis, cut-in pre-entry and occlusion, the leak guard, S02 / S17 campaign regressions), tests/test_llm_pipeline.py and tests/test_unrecorded_vehicle.py (section 9), tests/test_three_radars.py (layout, mounts, coverage, rear blind zone, front -> side continuity, per-mount Doppler for a stopped / straight / turning / accelerating / braking recorder, static and moving targets ahead, at the side and in a rear quarter), tests/test_critical_ttc.py (following, stopped target, same speed, crossing ahead / behind, collision course near and far, oncoming traffic, a car from behind, S08 regression), tests/test_semantic_events.py (THROTTLE), tests/test_traffic_signs.py, tests/test_multi_collision.py, tests/test_campaign_perception.py (recorded campaign: radar layout, S07 occlusion, signs, S09 / S12 / S16 timing).

### 5.8 CRITICAL_TTC and CUT_IN before and after the safe following distance (2026-10-09)

The 14 runs were re-reconstructed from the same raw files (562 raw and ground-truth files byte-identical, nothing re-recorded, no CARLA).  Collisions, alignment, associations and every event other than CRITICAL_TTC / CUT_IN are unchanged; the 14 forensic packets are byte-identical (same SHA-256), the radar visibility audit too.

| run | CRITICAL_TTC_START before -> after | CUT_IN_*_START before -> after | changes (local s) | assessment |
|---|---|---|---|---|
| S01/run_0_crash | 1 -> 1 | 0 -> 0 | none | - |
| S02/run_0_crash | 1 -> 1 | 1 -> 1 | A->B 3.25 -> 1.80; END 4.65 -> 5.00 | correct: B enters A's lane 16.0 m ahead (ground truth 15.8 m) while A at 49 km/h needs 24.0 m (headway 1.16 s); critical now 0.30 s before the cut-in (2.10) instead of 1.15 s after it; the collision-course reason joins at 3.30 (the former start); END when A comes to rest after the impact |
| S02/run_0_critical_before_cut_in | 2 -> 2 | 1 -> 1 | A->B 2.65 -> 2.60 | correct, order kept: CRITICAL_TTC 2.60 < CUT_IN_FROM_LEFT 2.95 < EGO_PATH_ENTRY 3.65 (B entering 3.8 m ahead, headway 0.29 s) |
| S03/run_0_crash | 2 -> 2 | 0 -> 0 | none | crossing: collision-course model |
| S06/run_0_a_front_pushed | 2 -> 2 | 0 -> 0 | A->B 3.90 -> 0.50; B->C 3.30 -> 0.50 | correct, the scenario's own premise ("A following B far too closely"): A 4.5 m behind B at 50 km/h (0.33 s), B 13.5 m behind C (0.99 s); C's braking shows as the collision-course reason joining at 3.30 / 3.90 |
| S06/run_0_b_rear_first | 2 -> 2 | 0 -> 0 | B->C 3.30 -> 0.50; A->B 4.70 -> 4.65 | correct: B 13.5 m behind C at 49 km/h (0.99 s); A closing on the braking B with 21 m against 23 m |
| S07/run_0_crash | 2 -> 2 | 0 -> 0 | A->B 4.00 -> 0.50 | correct by the definition, the weakest case: 19.3 m at 50 km/h = 1.39 s < 1.5 s (UN R157 time gap); the braking criterion alone (14.9 m) would call it safe; the emergency (C and B braking) is the collision-course reason joining at 4.00 |
| S08/run_0_crash | 2 -> 2 | 0 -> 0 | none | crossing; still critical only between the colliding pair (test) |
| S09/run_0_merge_conflict | 2 -> 2 | 0 -> 0 | none | roundabout merge: collision-course model |
| S10/run_0_rolls_through | 2 -> 2 | 0 -> 0 | none | junction: collision-course model |
| S12/run_0_near_simultaneous | 2 -> 2 | 0 -> 0 | none | all-way stop: no standing recorder follows anybody |
| S15/run_0_deflected_into_c | 5 -> 5 | 0 -> 0 | none | junction pile-up: collision-course model |
| S16/run_0_consequential | 3 -> 3 | 3 -> 1 | B->A 4.15 -> 0.50; A->C 5.55 -> 5.20 (END 6.60 -> 7.00); CUT_IN_FROM_LEFT(B, B:track_003) 1.35 removed; CUT_IN_FROM_LEFT(A, A:track_002) 5.20 removed | B 7.2 m behind A at 45 km/h (0.57 s; the scenario's "B, following A too closely"); A's merge ends 1.3 m behind the van, critical at 5.20, before the first collision (5.55); B's cut-in was false (the van never moved laterally; it is seen past A: occlusion gate); A's cut-in on track_002 was A's own lane change into the van's lane (that track is seen past the van's other track); the same relative-motion artefact remains on A:track_001 (CUT_IN_FROM_LEFT 5.45, section 7) |
| S17/run_0_crash | 3 -> 3 | 2 -> 1 | A->C 3.60 -> 2.60 (END 4.55 -> 4.65); CUT_IN_FROM_RIGHT(B, B:track_002) 2.85 removed | correct: section 8.5 |

New false positives searched for: no UNSAFE_FORWARD_GAP fact on a target behind the front face, beside the recorder or with its body more than 1.0 m outside the corridor (tests/test_forward_gap.py); no new CUT_IN anywhere; crossing runs unchanged.  Every new early start is a same-lane or entering leader closer than the safe distance, and the reconstructed clearances agree with the ground-truth bumper-to-bumper gaps within 0.2 m (S06 4.36 / 13.34 m, S07 19.16 m, S16 6.95 m, S02 15.78 m, S17 3.29 m).  Scenario adaptations: none needed (every run still exercises its question; S06 and S16 are designed around a too-close follower, S07's 1.39 s is below the R157 time gap).  Temporal safety relations that changed: S02/run_0_crash and S16 A:track_001 (C) become "critical TTC already active before the cut-in", S17 A:track_001 too.

### 5.9 Safe following distance simplified (2026-10-10; S17 only regenerated)

The safe gap became d_min = max(v_ego x t_front, 2 m) (section 4.3): the braking-distance branch is gone.  By request, only S17 was regenerated (from the same raw files, CARLA not used); the other 13 runs keep the 2026-10-09 outputs until Andrea has reviewed S17.

- S17: every event, both local graphs and the global trace are byte-identical (global_graph.json and report.md differ only in the recorded configuration); only the diagnostic facts change (new time_gap_distance_m; required_safe_distance_m unchanged, because for A and C (11.8 and 10.8 m/s) the time gap was already the larger branch: 16.8-18.0 m against 14.5-16.3 m).  Forensic packet unchanged (97cb278d).  A's CRITICAL_TTC_START on A:track_001 stays at local 2.60 s (t_global -2.35 s): clearance 3.31 m, v_ego 11.81 m/s, t_front 1.425 s, d_min 16.83 m, UNSAFE_FORWARD_GAP; CUT_IN_FROM_RIGHT_START 2.75 s; B establishes no cut-in.  Worked example: reconstruction/evaluation/s17_worked_example.md.
- S02/run_0_critical_before_cut_in, reconstructed from its raw files with the new rule (not written): CRITICAL_TTC_START 2.60 s (UNSAFE_FORWARD_GAP, clearance 3.77 m, d_min 19.53 m instead of 25.95 m) < CUT_IN_FROM_LEFT_START 2.95 s: order kept.
- Dry run of the whole campaign in a scratch copy (not written): one event would change, S06/run_0_b_rear_first A->B CRITICAL_TTC_START 4.65 -> 4.70 s (the braking branch had made A's closing on the braking B unsafe 0.05 s before the collision-course reason); the diagnostic facts of every run would change where the braking branch was the larger one.

### 5.10 CRITICAL_TTC release: geometric hysteresis (2026-10-10; S17 only regenerated)

In the S17 replay two CRITICAL_TTC_END came before the collision (t_global 0): B about A at -0.05 s and A about C (A:track_001) at -0.30 s.  Diagnosis from the recorders' own data, every quantity of the conflict model per 0.05 s sample (admissible), then against the ground truth (evaluation only):

- B about A (B:track_001), END at local 4.90 s: one boolean changed, collision_course, true at 4.85 s and false at 4.90 s.  A's box was already inside B's safety envelope (0.16 m from B's body; ground truth 0.00 m, the bodies touching) and its closing speed read 0.96 m/s, just below the 1 m/s threshold, so the collision-course test returned "no course" (a target inside the envelope counts only while it closes in) and the old release accepted that as the end of the conflict; the forward gap played no part (A never was ahead of B: clearance -4.1 m), occlusion none.  The radar closing speed under-reads the approach of a car beside the recorder (1.24-0.96 m/s against 2.2-1.2 m/s for the true body distance, lateral approach 1.9 m/s), but the defect is the release logic: a rule meant to keep a parked car inside the envelope from being a collision course was also taken as evidence that the conflict was over.  A's state about B had the same defect at -0.15 s (closing 0.79 m/s for one sample; the debounce saved it) and ended at the impact (closing -0.50 m/s).
- A about C (A:track_001), END at local 4.65 s: one boolean changed, forward.leader, because the region turned from IN_PATH to none: C's nominal box left A's corridor by 0.01 m while C moved away laterally (-1.44 m/s relative), so it was neither in the path nor front-lateral (which needs an approach); the collision-course reason had been off since 4.55 s; clearance 0.77 m against d_min 16.8 m.  The leader start gate was used as the release, with no hysteresis, and a 0.0-0.2 m lateral error of the nominal box made it fail: the ground truth shows C's body still overlapping A's corridor, 0.65 m ahead of A's front, until after the collision.
- Category: release logic (a start-suppression rule of the collision-course model and the leader start gate used as end conditions), helped by radar/tracking (closing speed) and the nominal box (0.0-0.2 m); not the replay, not occlusion.

S17 regenerated with the release of section 4.3 from the same raw files (36 raw and ground-truth files byte-identical, CARLA not used); the forensic packet is unchanged (97cb278d: the new fact inside_safety_envelope is dropped from it); only these three events moved:

| pair | CRITICAL_TTC_START | END before | END after | why it ends now |
|---|---|---|---|---|
| A about C (A:track_001) | -2.35 | -0.30 | +0.55 | C's box 0.60 m outside A's corridor and moving away (-1.37 m/s); by the ground truth 0.46 / 0.61 m at +0.70 / +0.80 s |
| A about B (A:track_002) | -1.15 | 0.00 (the impact) | +1.00 | B's box 0.32 m from A, out of A's envelope, as A slows through 3 m/s (the ground truth still has them touching) |
| B about A (B:track_001) | -0.80 | -0.05 | +1.30 | both at rest (B stopped, A below 1 m/s), A still within B's envelope |

New S17 order (t_global): CRITICAL_TTC_START(A,A:track_001) -2.35 < CUT_IN_FROM_RIGHT_START(A,A:track_001) -2.20 < EGO_PATH_ENTRY(A,A:track_001) -1.60 < CRITICAL_TTC_START(A,B) -1.15 < CRITICAL_TTC_START(B,A) -0.80 < COLLISION(A,B) 0.00 < CRITICAL_TTC_END(A,A:track_001) +0.55 < CRITICAL_TTC_END(A,B) +1.00 < CRITICAL_TTC_END(B,A) +1.30: every critical state is active at the collision.

- S02/run_0_critical_before_cut_in reconstructed from its raw files (not written): CRITICAL_TTC_START 2.60 s < CUT_IN_FROM_LEFT_START 2.95 s, the cut-in inside the critical episode (CRITICAL_TTC_ALREADY_ACTIVE); its two ENDs move from the collision (4.10 s) to 4.70 s.
- Dry run of the whole campaign, both rule sets on the same raw files (nothing written): only CRITICAL_TTC events change, all after the collisions.  16 ENDs of the other 13 runs move later by 0.10-0.60 s, none earlier (S02 crash, S02 critical_before_cut_in x2, S03 x2, S06 a_front_pushed, S08 x2, S10 x2, S12, S15 x3, S16 x2), and S09 gains a post-impact episode B about A (local 10.65-11.10 s) during the persistent contact the ground truth records (10.25-11.05 s), formerly dropped as a 0.10 s flicker.  Before this change only S17 had a CRITICAL_TTC_END before its collision.  The 13 runs keep their 2026-10-09 outputs until Andrea's review.

### 5.11 CRITICAL_TTC ends at the collision (2026-10-10; S17 only regenerated)

CRITICAL_TTC describes the pre-collision threat episode.  A recorder's own collision with the road user of an active episode now ends that episode at the collision's timestamp; the continuing contact is a post-impact state: no episode starts for that pair until the contact is over (its last callback) and the conflict has been clearly resolved by the release; a genuinely new conflict can then start one (section 4.3).

The collision sensor reports no partner, so the partner is read from the recorder's own tracks: the only one CLOSING just before the contact and touching the recorder at it.  Over the 37 contacts of the campaign a partner is found for 27, every one the true partner by the ground truth (evaluation only), none wrong.  No partner for the other 10: 8 strikes from the rear blind zone (S01 B, S02 crash B, S06 a_front_pushed B and C, S06 b_rear_first B and C, S07 B, S16 A), S06 a_front_pushed A's second contact with B (B receding just before it) and S16 C (its track of A lost 0.15 s before the contact).  In S06 b_rear_first B is struck from behind while still pressed against C: C is touching but not closing in, so that contact is not attributed to C.

S17 regenerated (raw files byte-identical, forensic packet unchanged, 97cb278d); only two events moved:

| pair | CRITICAL_TTC_START | END by the release (section 5.10) | END now |
|---|---|---|---|
| A about B (A:track_002) | -1.15 | +1.00 | 0.00, the COLLISION(A,B) |
| B about A (B:track_001) | -0.80 | +1.30 | 0.00, the COLLISION(A,B) |
| A about C (A:track_001, anonymous) | -2.35 | +0.55 | +0.55, unchanged: A and C never collide |

At t_global 0.00 the global trace reads COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A).  The replay (code unchanged) lists the two ENDs with the collision at 0.00; its perceived-state panel follows the 10 Hz trace, so from the frame at +0.05 s no CRITICAL_TTC between A and B is shown, while A's state about the anonymous track lasts to +0.55 s.

- S02/run_0_critical_before_cut_in from its raw files (not written): CRITICAL_TTC_START 2.60 s < CUT_IN_FROM_LEFT_START 2.95 s, the cut-in inside the critical episode; both ENDs now at the collision (4.10 s instead of 4.70 s).
- Dry run of the other 13 runs, the release of section 5.10 against this rule on the same raw files (nothing written): only CRITICAL_TTC events change.  18 ENDs move to their own pair's collision, none from before it (S02 crash; S02 critical_before_cut_in x2; S03 x2; S06 a_front_pushed A about B at 4.80; S08 x2; S10 x2; S12 x2; S15 A about B 3.80, A about C 4.70, B about A 3.80, C about A 4.70; S16 A about C 6.60, B about A 5.55), and the S09 post-impact episode (B about A, 10.65-11.10 s, during the contact) disappears.  Multi-contact runs stay pair-specific: in S06 a_front_pushed B's state about C ends at B's own contact with C (5.30), not when A strikes B from behind (4.80); in S15 A's state about C survives A's earlier collision with B and ends at A's contact with C; in S16 A's state about C survives B striking A from behind (5.55) and ends at A's contact with C (6.60).  No episode before a collision is lost.  Unchanged and outside this rule: S09 A about B ends at 9.45 s, 0.80 s before the contact (the straight-line target prediction finds no overlap from 9.50 s while A turns at -20 deg/s in the roundabout, section 7); S15 B:track_001, an anonymous second track of A 9 m away at the B-A contact, starts an episode at 3.95 s that only an identity fusion could attribute to A; S16 C's track of A, lost 0.15 s before their contact, keeps its episode open to the track's end.

## 6. Compared with the 360-degree campaign

| run | 360-degree: reconstruction | CRITICAL | three radars: reconstruction | CRITICAL |
|---|---|---|---|---|
| S01/run_0_crash | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 1 | yes (1/1 vehicle contacts); associations correct: 1/1; anonymous: 0 | 1 |
| S02/run_0_crash | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 1 | yes (1/1 vehicle contacts); associations correct: 1/1; anonymous: 0 | 1 |
| S02/run_0_critical_before_cut_in | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 1 | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S03/run_0_crash | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S06/run_0_a_front_pushed | yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 4 | 3 | yes (3/3 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S06/run_0_b_rear_first | yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 4 | 2 | yes (2/2 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S07/run_0_crash | S07 had full_view / occluded variants | - | yes (1/1 vehicle contacts); associations correct: 1/1; anonymous: 1 | 2 |
| S08/run_0_crash | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 4 | 8 | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 4 | 2 |
| S09/run_0_merge_conflict | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 3 | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S10/run_0_rolls_through | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 | yes (1/1 vehicle contacts); associations correct: 1/1; anonymous: 1 | 2 |
| S12/run_0_near_simultaneous | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0 | 2 |
| S15/run_0_deflected_into_c | yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 2 | 6 | yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 2 | 5 |
| S16/run_0_consequential | yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 1 | 2 | yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 4 | 3 |
| S17/run_0_crash | new run (2026-10-07; re-recorded 2026-10-08) | - | yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 3 | 3 |

- Fewer associations where the struck vehicle cannot see its follower (rear blind zone): S01, S02, S10 (2 -> 1).  The identity of the striking car still comes from its own track of the struck one.
- CRITICAL_TTC concentrates on the colliding pairs (S08 8 -> 2) and starts causally (after the event that creates the danger: S06 b_rear_first A on B exactly at B's crash).
- S06 a_front_pushed: three true contacts (one of them merged by B's sensor) all reconstructed; 0 anonymous tracks (4 before, B's view of A behind it from the roof).
- Contacts, alignment (multi-hop) and timing errors (0.0 s) are as good as before; the per-recorder radar data are 3 streams of 12000 points/s instead of one logical 21600 points/s stream.

## 7. Residual anomalies and limitations

- S15 keeps its scripted post-impact deflection (A carried 5.2 m sideways into C): CARLA does not carry a struck car sideways (section 3).
- Rear blind zone by design: a follower directly behind is never perceived by the car it follows; the struck car's view cannot name the striker (it is named from the striker's own track).
- Extended targets: the median of a vehicle's returns slides with the aspect (front -> side passage: up to ~3 m/s of transient speed error in the synthetic case, 0.49 m/s rms side-aspect velocity error in the campaign) and the clearance is biased high by 0.3-1.4 m depending on the body (section 5.6).
- CRITICAL_TTC predicts targets on straight lines: in S09 the circulating A is predicted straight, so the onset (6.65 s, 3.6 s before the collision) is earlier than a curved prediction would give.
- A track born less than 0.5 s earlier makes no CRITICAL claim: a target appearing on a collision course gets its CRITICAL_TTC at least 0.5 s after it appears (S15 A on B at 2.55 s, collision 3.80 s).
- S16: A sees the van C as two tracks; B sees C as up to four short tracks (never in contact with it: anonymous).
- Lateral body gap from a radar track: the nominal 4.6 x 1.9 m box placed behind the near surface misses a car's real inner side by up to ~0.7 m either way (section 4.3), about the distance between a car keeping the next lane and the 3 m corridor; a car next to the corridor is therefore a leader (UNSAFE_FORWARD_GAP) only while it approaches the corridor, and a cut-in needs its body within 1.0 m of the corridor.
- UNSAFE_FORWARD_GAP keeps CRITICAL_TTC active through a whole car-following phase when the gap is short from the start (S06, S07, S16): the onset of the braking emergency is no separate event, it is in the TRACK_STATE facts (critical_reason gains PREDICTED_OVERLAP at the former start time).  S07's 1.39 s headway is critical only by the R157 time gap.
- CUT_IN uses the relative lateral motion (no lane map): a recorder that changes lanes toward a car sees that car "cut in".  S16: A's merge into the van's lane gives CUT_IN_FROM_LEFT(A, A:track_001) at 5.45 although the van never moved laterally (pre-existing; the van's second track, seen past the first, is now gated by occlusion).
- The occlusion gate works on nominal boxes grown by 0.5 m: it can withhold CUT_IN / forward-gap evidence for a car seen right past another one (S08 and S15 around their contacts, where no event changed; S16, see section 5.8).
- CRITICAL_TTC ends at a collision only when the recorder's own tracks name the partner (CLOSING and touching at the contact, section 5.11): struck from the rear blind zone, or by a car whose track was lost just before, the state ends by the release, after the impact, when the boxes separate or both vehicles stand still.  A second, anonymous track of the colliding car is another road user for the recorder (S15 B:track_001).
- A leader that settles less than 0.5 m outside the corridor (the box error reaches ~0.7 m) keeps an UNSAFE_FORWARD_GAP episode active until it is 1.10 x d_min ahead, no longer ahead, or the recorder stops: conservative by design (unknown is not safe).
- A stationary braked vehicle is immovable when struck in CARLA; chain scenarios rely on the struck car still rolling (S06 a_front_pushed).
- The depth camera (unused) misses frames on the second and third vehicle (section 2.4).
- S17: the reconstruction cannot know that A:track_001, B:track_002 and B:track_003 are one road user (C): identities are anchored on collisions and C collides with nobody.  A's swerve is not precautionary: with it disabled A runs into the back of C (section 8.4).  A's track of B is associated only because C is slower than B: a second track of A near A at the contact, with a speed within 1.5 m/s RMSE of B's (C at 11 m/s against B at 12.5 m/s in a first design), leaves both anonymous (fusion: ambiguous), so B drives at 13 m/s.
- S17 launch: in about one recording in four C starts one tick of travel (0.6 m) closer to A (the spawn-and-launch phase, before the recording); everything after t = 0 is reproducible to the centimetre.  The recording and both counterfactual runs are in the usual mode (C 10.4 m ahead of A at the start).
- A record: false participant is not replayed by scripts/replay_run.py (no ego.jsonl; ground truth, the run metadata and the scenario configuration are never read there): S17's C appears only as the anonymous ghost tracks A:track_001, B:track_002 and B:track_003 (nominal boxes from each observer's own track, never merged, never named; A's and B's boxes of C are about 2 m apart because A sees its rear and B, partly behind A, its left side).

## 8. S17 unobserved_causal_vehicle: partial observability

Research question: *how does partial observability of a causally relevant but non-colliding road user affect accident explanation and attribution?*  First recorded 2026-10-07; re-recorded 2026-10-08 with a closer cut-in (1 attempt, 40.8 s wall time), Town05, spawn point 265 (three same-direction lanes, 3.5 m wide), speed limit 50 km/h (supplied).  In the first recording C entered A's lane about 5 m ahead and, with A's swerve disabled, A and C would have passed 2.6 m apart: the swerve looked like an over-reaction.  Now C cuts in about 2 m in front of A, and without the swerve A runs into it.

### 8.1 Dynamics

- A (audi.tt, recorder) drives the middle lane at 11.8 m/s; B (nissan.patrol, recorder) drives the left lane at 12.9 m/s, starting 7.2 m behind A and catching up; C (tesla.model3, record: false) drives the right lane at 10.8 m/s, 10.4 m ahead of A (centres): A is about to pass it.
- 2.0 s: C cuts into A's lane without braking (lane shift -3.5 m commanded over 1.0 s): its lateral motion starts at 2.45 s, its left side crosses into A's lane at 2.85 s and it is centred in A's lane by 4.45 s; peak lateral acceleration 3.9 m/s^2, heading at most 13 deg off A's.
- 3.30 s: C's box is inside A's corridor (A's width + 0.3 m a side) within 3 m of A's front face (measured 2.48 m in the corridor, 2.32 m box to box): privileged corridor_clearance trigger, logged only in ground_truth/triggers.jsonl.  3.65 s: after a 0.35 s reaction A swerves left (lane shift -3.5 m over 1.0 s; 1.96 m box to box when it starts, lateral motion from 4.10 s, peak lateral acceleration 3.8 m/s^2) into B's lane.
- 4.95 s: A-B collision (A's left side against B's right front; peak impulse 1577 N*s, contact until 5.75 s); both brake to a stop side by side.  C touches nobody: closest 0.59 m to A (5.20 s), 3.13 m to B.
- 7.0 s: C accelerates to 16 m/s (speeding up from 7.15 s) and drives away in the middle lane.

### 8.2 Scene

```
          direction of travel ------------------------------------------------------>
 left   | B==>  B catches up (13 m/s) ........................ [A][B] contact 4.95 s
 middle | A==>  A swerves left from 3.65 s .............../
        |             C==> in A's lane ~2 m ahead from ~3.3 s ...... C==> 16 m/s from 7.0 s, away
 right  |      C==> (11 m/s) cuts left at 2.0 s __/
```

True positions (ground truth; forward / right of A's first pose, metres; centre of each vehicle):

| t s | moment | A forward / right @ m/s | B | C |
|---|---|---|---|---|
| 0.00 | start | -0.0 / +0.0 @ 11.9 | -7.2 / -3.5 @ 12.9 | 10.4 / +3.5 @ 10.7 |
| 2.00 | C starts its cut-in | 23.6 / +0.0 @ 11.8 | 18.6 / -3.5 @ 12.8 | 32.0 / +3.5 @ 10.8 |
| 2.85 | C's left side in A's lane | 33.7 / +0.0 @ 11.8 | 29.4 / -3.5 @ 12.8 | 41.2 / +2.8 @ 10.8 |
| 3.30 | trigger: C within 3 m in A's corridor | 39.0 / +0.0 @ 11.8 | 35.2 / -3.5 @ 12.8 | 45.9 / +1.8 @ 10.8 |
| 3.65 | A starts swerving | 43.1 / +0.0 @ 11.8 | 39.6 / -3.5 @ 12.8 | 49.7 / +1.2 @ 10.8 |
| 4.95 | A-B contact | 58.3 / -1.6 @ 12.5 | 56.3 / -3.5 @ 12.4 | 63.7 / +0.3 @ 10.9 |
| 5.20 | C closest to A | 61.4 / -1.9 @ 11.7 | 59.3 / -3.6 @ 11.5 | 66.4 / +0.2 @ 10.9 |
| 7.00 | C speeds up | 67.6 / -2.7 @ 0.0 | 64.5 / -4.2 @ 0.0 | 86.2 / +0.0 @ 11.1 |

Clearance A-C: box to box, inside A's corridor, longitudinal (C's rear - A's front, along A's initial heading) and as A's radar track of C reports it (``clearance_m`` of A:track_001, biased high: section 5.6):

| t s | moment | box gap m | in A's corridor m | longitudinal m | radar m |
|---|---|---|---|---|---|
| 1.10 | box gap first <= 5 m | 4.98 | - | 4.78 | 5.17 |
| 2.90 | box gap first <= 3 m | 3.00 | 6.82 | 2.95 | 3.15 |
| 3.30 | trigger | 2.32 | 2.31 | 2.47 | 2.51 |
| 3.65 | A's reaction starts | 1.96 | 1.96 | 2.08 | 2.20 |
| 3.65 | box gap first <= 2 m | 1.96 | 1.96 | 2.08 | 2.20 |
| 4.10 | A starts moving left | 1.54 | 1.54 | 1.62 | 1.77 |
| 4.95 | A-B contact | 0.78 | - | 0.91 | 1.06 |
| 5.20 | minimum | 0.59 | - | 0.58 | 0.85 |

### 8.3 Recorders and the non-recorder

| participant | role | data |
|---|---|---|
| A | recorder | vehicles/A: 3 radars, camera, ego, controls, collisions, signs |
| B | recorder | vehicles/B: same |
| C | record: false | no vehicles/C; the run's metadata.json lists A, B only; C is in ground_truth/ (states, controls, its collision sensor: no contact) and in ground_truth/metadata.json with record: false |

Radar visibility of C (privileged audit): A first raw return 0.00, track track_001 0.00-7.45 s; B first raw return 0.00, track track_002 0.00-5.70 s, track_003 6.40-7.00 s.  B's view of C is partly behind A (B loses it after the contact and picks it up again briefly as track_003); both see it from the first sweep.

### 8.4 Privileged counterfactuals (ground_truth/counterfactuals.json)

Same configuration on the same private engine, cameras on, into a scratch directory; only the ground-truth summary is kept in the run.  Never read by the reconstruction, never given to a model.

| run | collisions | min gap A-B m | min gap A-C m | A's swerve | A's max left departure m |
|---|---|---|---|---|---|
| factual (S17 as recorded) | A-B 4.95 s (1577 N*s) | 0.0 | 0.59 | A_evasive_swerve_left at 3.30 s | 2.71 |
| without C (--without-participant C) | none | 1.54 | - | none | 0.0 |
| C present, swerve disabled (--disable-action A_evasive_swerve_left) | A-C 5.95 s (478 N*s) | 1.51 | 0.0 | none | 0.01 |

Without C there is no swerve and no collision: C's presence is causally relevant although C touches nobody.  With C but no swerve, A runs into the back of C at 5.95 s (closing at 0.96 m/s, 478 N*s) and never touches B: A's evasion answered a real conflict, and turned a rear-end collision with C into a sideswipe with B.  C starts 10.36 m ahead of A in every run (the same launch).

### 8.5 What the reconstruction knows

| local track | status | global entity |
|---|---|---|
| A:track_001 | ANONYMOUS | A:track_001 |
| A:track_002 | ASSOCIATED | B |
| B:track_001 | ASSOCIATED | A |
| B:track_002 | ANONYMOUS | B:track_002 |
| B:track_003 | ANONYMOUS | B:track_003 |

Events about the anonymous tracks (global time, s):

| t_global | event | actor | subject |
|---|---|---|---|
| -4.95 | TRACK_APPEARED_RIGHT | A | A:track_001 |
| -4.95 | TRACK_APPEARED_RIGHT | B | B:track_002 |
| -4.95 | CLOSING_START | A | A:track_001 |
| -4.95 | CLOSING_START | B | B:track_002 |
| -2.35 | CRITICAL_TTC_START | A | A:track_001 |
| -2.20 | CUT_IN_FROM_RIGHT_START | A | A:track_001 |
| -1.60 | EGO_PATH_ENTRY | A | A:track_001 |
| -0.85 | CUT_IN_FROM_RIGHT_END | A | A:track_001 |
| -0.40 | CLOSING_END | A | A:track_001 |
| 0.00 | COLLISION | - | A, B |
| 0.20 | CLOSING_END | B | B:track_002 |
| 0.25 | EGO_PATH_EXIT | A | A:track_001 |
| 0.55 | CRITICAL_TTC_END | A | A:track_001 |
| 0.75 | TRACK_LOST | B | B:track_002 |
| 1.45 | TRACK_APPEARED_RIGHT | B | B:track_003 |
| 2.05 | TRACK_LOST | B | B:track_003 |
| 2.50 | TRACK_LOST | A | A:track_001 |

A's critical TTC on the anonymous track starts at -2.35 s (local 2.60) for an unsafe forward gap, 0.15 s before the cut-in is established (-2.20) and 0.75 s before C's body enters A's corridor (-1.60): clearance 3.31 m (ground truth 3.29 m bumper to bumper) against a required 16.83 m (A at 11.81 m/s, UN R157 time gap 1.43 s; braking criterion 14.8 m), time headway 0.28 s, C at 10.84 m/s, front-lateral and approaching A's corridor at 1.4 m/s.  The collision-course reason joins at -1.35 s (the former start).  The state ends at +0.55 s, once C's box is 0.60 m outside A's corridor and moving away (until 2026-10-10 at -0.30 s, when the box had left the corridor by 0.01 m: section 5.10); B's state about A lasts from -0.80 s to the contact, where it ends, as A's about B (section 5.11).  B sees no cut-in: C moved from the right lane into A's middle lane, two lanes from B, and B sees it past A (occlusion gate).

Privileged evaluation: A:track_001 is C (correctly left anonymous), B:track_002 is C (correctly left anonymous), B:track_003 is C (correctly left anonymous); associations 2/2 correct.  No entity C exists anywhere in reconstruction/ outside evaluation/.

### 8.6 What an LLM receives

reconstruction/llm/forensic_packet.json, run_id case-1378e3e335bdf143, packet SHA-256 97cb278d7eab664e: 807 facts (COLLISION_OBSERVATION 1, EGO_CONTROL 222, EGO_MOTION 222, TRACK_STATE 362).  Entities: A (recorder), B (recorder), A:track_001 (radar_track, anonymous -> A:track_001), A:track_002 (radar_track, associated -> B), B:track_001 (radar_track, associated -> A), B:track_002 (radar_track, anonymous -> B:track_002), B:track_003 (radar_track, anonymous -> B:track_003).  Neither the letter C nor any semantic event, perceived state, scenario name or ground truth appears in it (tests/test_llm_pipeline.py: S17PacketTests).

## 9. LLM abductive forensics (infrastructure)

FACTS -> abductive explanation (Stage 1) -> semantic hypotheses -> temporal formulas (Stage 2, a separate call) -> deterministic three-valued verification on the semantic trace, loaded only after both answers are saved.  Description, diagram and caveats: docs/llm_abductive_forensics.md.  Providers, schemas, guard, verifier and scoring are tested with mock transports only; dry-run prompts for S17 are in traces/S17/run_0_crash/reconstruction/llm/runs/*_dryrun/.  First real calls 2026-10-08/09, S17 only: one complete analysis with gpt-6-luna and one with gemini-3.5-flash-lite; gemini-3.8-flash gave no answer (HTTP 503, then the free-tier daily quota): traces/S17/run_0_crash/reconstruction/evaluation/llm_comparison_S17.md.  After the 2026-10-09 reconstruction change (section 4.3) the 14 packets are byte-identical; the two saved answers were re-verified against the regenerated semantic trace into reverification_20261009/ (deterministic verifier only, no model call; formula verdicts unchanged, 34 reference events instead of 36).

Forensic packets exported for every run (reconstruction/llm/; the leak guard passed for all):

| run | run_id | facts | TRACK_STATE | SIGN | COLLISION | anonymous tracks | packet KiB | SHA-256 |
|---|---|---|---|---|---|---|---|---|
| S01/run_0_crash | case-b93d9e03f59ecdc2 | 606 | 121 | 0 | 1 | 0 | 109 | 628e75d3dc15 |
| S02/run_0_crash | case-f26f0bed62fd8a5b | 764 | 151 | 0 | 1 | 0 | 135 | 811a21c99609 |
| S02/run_0_critical_before_cut_in | case-893f647b9cb36a63 | 673 | 208 | 0 | 1 | 0 | 139 | 5986753e2239 |
| S03/run_0_crash | case-3ff854c61d8e8a08 | 877 | 264 | 0 | 1 | 0 | 177 | 50ed73829956 |
| S06/run_0_a_front_pushed | case-43c5a5788d1a9a19 | 1107 | 276 | 0 | 3 | 0 | 207 | b6b29b309ee2 |
| S06/run_0_b_rear_first | case-7202c5a4933604c5 | 1146 | 286 | 0 | 2 | 0 | 215 | efdde8eed675 |
| S07/run_0_crash | case-a5478bd50abe12db | 1105 | 276 | 0 | 1 | 1 | 208 | 71118072466a |
| S08/run_0_crash | case-59f4c77fe3da70f8 | 1659 | 740 | 0 | 1 | 4 | 398 | b5f734c686d6 |
| S09/run_0_merge_conflict | case-3302772030bd0a80 | 1357 | 416 | 0 | 1 | 0 | 275 | 4ebf53931b02 |
| S10/run_0_rolls_through | case-7f400bb834f48527 | 915 | 269 | 1 | 1 | 1 | 184 | de948f555ed1 |
| S12/run_0_near_simultaneous | case-891ca9b5821d62c6 | 733 | 210 | 2 | 1 | 0 | 149 | b907f1269e31 |
| S15/run_0_deflected_into_c | case-0f891d8e43b20f3a | 1550 | 701 | 1 | 2 | 2 | 374 | 64db22a4f0a4 |
| S16/run_0_consequential | case-16dc7a2c76943785 | 1240 | 512 | 0 | 2 | 4 | 290 | 7ca298f6c691 |
| S17/run_0_crash | case-1378e3e335bdf143 | 807 | 362 | 0 | 1 | 3 | 198 | 97cb278d7eab |

## 10. Global event sequences

### S01/run_0_crash

```
-6.75 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B)
-2.80 THROTTLE_END(B); BRAKE_START(B)
-2.55 CLOSING_START(A,B)
-2.35 CRITICAL_TTC_START(A,B)
-1.60 MOVING_END(B); STOP_START(B)
-1.20 THROTTLE_END(A); BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 MOVING_END(A); STOP_START(A)
```

### S02/run_0_crash

```
-4.65 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B)
-4.50 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-2.85 CRITICAL_TTC_START(A,B)
-2.55 CUT_IN_FROM_LEFT_START(A,B)
-1.50 THROTTLE_END(B); BRAKE_START(B)
-1.40 EGO_PATH_ENTRY(A,B)
-1.00 BRAKE_END(B)
-0.90 THROTTLE_START(B)
-0.80 THROTTLE_END(A); BRAKE_START(A)
+0.00 COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B); CLOSING_END(A,B); THROTTLE_END(B); BRAKE_START(B)
+0.35 CRITICAL_TTC_END(A,B)
+0.40 MOVING_END(A); STOP_START(A)
+0.55 MOVING_END(B); STOP_START(B)
```

### S02/run_0_critical_before_cut_in

```
-4.10 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B)
-3.95 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-1.90 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-1.65 THROTTLE_END(A); BRAKE_START(A)
-1.50 CRITICAL_TTC_START(A,B)
-1.40 CRITICAL_TTC_START(B,A)
-1.15 CUT_IN_FROM_LEFT_START(A,B)
-0.85 BRAKE_END(A)
-0.75 THROTTLE_START(A)
-0.45 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A)
+0.05 CLOSING_END(A,B); CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.55 MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B)
+0.80 CUT_IN_FROM_LEFT_END(A,B)
```

### S03/run_0_crash

```
-4.10 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B)
-2.05 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.00 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.55 CRITICAL_TTC_START(A,B)
-1.50 CRITICAL_TTC_START(B,A)
+0.00 COLLISION(A,B); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B)
+0.05 THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.15 CLOSING_START(A,B); CLOSING_START(B,A)
+0.45 CRITICAL_TTC_END(A,B)
+0.50 TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
+0.55 CRITICAL_TTC_END(B,A); CLOSING_END(A,B)
+0.60 TURN_LEFT_END(A)
+0.65 CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
```

### S06/run_0_a_front_pushed

```
-4.80 MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C)
-4.30 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,C)
-1.85 THROTTLE_END(C); BRAKE_START(C)
-1.60 CLOSING_START(B,C)
-1.10 THROTTLE_END(B); BRAKE_START(B)
-0.85 CLOSING_START(A,B)
-0.75 MOVING_END(C); STOP_START(C)
-0.25 THROTTLE_END(A); BRAKE_START(A)
+0.00 COLLISION(A,B)
+0.05 BRAKE_END(B)
+0.40 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.50 COLLISION(B,C); CRITICAL_TTC_END(B,C); CLOSING_END(B,C)
+0.55 MOVING_END(A); STOP_START(A)
+0.65 COLLISION(A,B); MOVING_END(B); STOP_START(B); BRAKE_START(B)
```

### S06/run_0_b_rear_first

```
-6.25 MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C)
-5.75 CRITICAL_TTC_START(B,C)
-3.30 THROTTLE_END(C); BRAKE_START(C)
-3.05 CLOSING_START(B,C)
-2.20 MOVING_END(C); STOP_START(C)
-1.65 CLOSING_START(A,B)
-1.60 CRITICAL_TTC_START(A,B)
-1.55 COLLISION(B,C); CRITICAL_TTC_END(B,C); CLOSING_END(B,C)
-1.50 THROTTLE_END(B); BRAKE_START(B)
-1.40 MOVING_END(B); STOP_START(B)
-0.10 THROTTLE_END(A); BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.10 MOVING_END(A); STOP_START(A)
```

### S07/run_0_crash

```
-5.90 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001)
-5.40 CRITICAL_TTC_START(A,B)
-2.70 CLOSING_START(B,B:track_001)
-2.50 CRITICAL_TTC_START(B,B:track_001)
-2.25 THROTTLE_END(B); BRAKE_START(B)
-2.05 CLOSING_START(A,B)
-1.55 CRITICAL_TTC_END(B,B:track_001)
-1.05 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
-0.65 THROTTLE_END(A); BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.10 MOVING_END(A); STOP_START(A)
```

### S08/run_0_crash

```
-4.10 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
-2.05 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.00 TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,A); CLOSING_START(B,B:track_001)
-1.55 CRITICAL_TTC_START(A,B)
-1.50 CRITICAL_TTC_START(B,A)
+0.00 COLLISION(A,B); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B)
+0.05 THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_001)
+0.15 EGO_PATH_EXIT(A,A:track_001); CLOSING_START(A,B); CLOSING_START(B,A)
+0.45 CRITICAL_TTC_END(A,B)
+0.50 CLOSING_END(B,B:track_001); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
+0.55 CRITICAL_TTC_END(B,A); CLOSING_END(A,B)
+0.60 TURN_LEFT_END(A)
+0.65 CLOSING_END(A,A:track_001); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
```

### S09/run_0_merge_conflict

```
-10.25 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TURN_LEFT_START(A)
-7.70 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-7.50 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-4.95 EGO_PATH_ENTRY(A,B)
-4.70 EGO_PATH_EXIT(A,B)
-3.60 CRITICAL_TTC_START(B,A)
-3.35 CRITICAL_TTC_START(A,B)
-2.05 TURN_RIGHT_START(B)
-0.80 CRITICAL_TTC_END(A,B)
-0.30 TURN_RIGHT_END(B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
+0.05 THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.30 TURN_LEFT_END(A)
+0.75 MOVING_END(B); STOP_START(B)
+0.80 MOVING_END(A); STOP_START(A)
```

### S10/run_0_rolls_through

```
-5.40 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B)
-4.25 STOP_SIGN_DETECTED_START(A,A:sign-0)
-3.45 THROTTLE_END(A); BRAKE_START(A)
-2.80 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-2.70 TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
-2.65 STOP_SIGN_DETECTED_END(A,A:sign-0)
-2.55 BRAKE_END(A); THROTTLE_START(A)
-2.00 CRITICAL_TTC_START(A,B)
-1.80 CRITICAL_TTC_START(B,B:track_001)
-1.70 TURN_LEFT_START(A)
-0.15 EGO_PATH_ENTRY(B,B:track_001)
-0.10 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); TURN_LEFT_END(A)
+0.05 CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.10 MOVING_END(A); STOP_START(A)
+0.20 MOVING_END(B); STOP_START(B)
```

### S12/run_0_near_simultaneous

```
-7.15 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B)
-6.95 STOP_SIGN_DETECTED_START(A,A:sign-0)
-6.45 STOP_SIGN_DETECTED_START(B,B:sign-0)
-4.75 THROTTLE_END(A); BRAKE_START(A)
-4.65 THROTTLE_END(B); BRAKE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A)
-4.40 STOP_SIGN_DETECTED_END(A,A:sign-0)
-4.35 STOP_SIGN_DETECTED_END(B,B:sign-0)
-3.55 MOVING_END(B); STOP_START(B)
-3.45 CLOSING_END(A,B); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
-2.45 BRAKE_END(B); THROTTLE_START(B)
-2.30 BRAKE_END(A); THROTTLE_START(A)
-2.05 CLOSING_START(A,B); CLOSING_START(B,A)
-2.00 STOP_END(B); MOVING_START(B)
-1.95 STOP_END(A); MOVING_START(A)
-1.25 CRITICAL_TTC_START(A,B)
-1.10 CRITICAL_TTC_START(B,A)
-1.00 TURN_LEFT_START(A)
-0.40 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.05 CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.20 CRITICAL_TTC_END(A,B)
+0.30 MOVING_END(B); STOP_START(B)
+0.50 TURN_LEFT_END(A); MOVING_END(A); STOP_START(A)
```

### S15/run_0_deflected_into_c

```
-3.80 MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
-3.60 TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
-2.70 STOP_SIGN_DETECTED_START(B,B:sign-0)
-2.10 TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
-1.80 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.75 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-1.55 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.50 TURN_LEFT_START(B)
-1.30 CRITICAL_TTC_START(B,A)
-1.25 CRITICAL_TTC_START(A,B)
-0.85 THROTTLE_END(B); BRAKE_START(B)
-0.30 BRAKE_END(B)
-0.15 THROTTLE_START(B)
-0.05 EGO_PATH_ENTRY(B,A); CRITICAL_TTC_START(A,C); CRITICAL_TTC_START(C,A)
+0.00 COLLISION(A,B); CLOSING_END(A,B); TURN_LEFT_END(B)
+0.05 CRITICAL_TTC_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(B); TURN_LEFT_START(A)
+0.15 CLOSING_END(B,A); CRITICAL_TTC_START(B,B:track_001)
+0.20 MOVING_END(B); STOP_START(B)
+0.25 CRITICAL_TTC_END(B,A)
+0.55 EGO_PATH_ENTRY(A,C)
+0.75 EGO_PATH_EXIT(B,A)
+0.90 COLLISION(A,C); CRITICAL_TTC_END(C,A); CLOSING_END(C,A); EGO_PATH_EXIT(A,C)
+0.95 THROTTLE_END(C); BRAKE_START(C)
+1.05 CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
+1.15 CRITICAL_TTC_END(B,B:track_001)
+1.20 CLOSING_END(C,C:track_002); MOVING_END(C); STOP_START(C)
+1.25 TURN_LEFT_END(A)
+1.30 MOVING_END(A); STOP_START(A)
+1.70 TRACK_LOST(B,A)
+1.80 CLOSING_END(B,B:track_001)
```

### S16/run_0_consequential

```
-5.55 MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_LEFT(A,C); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(A,C); CLOSING_START(B,B:track_002)
-5.50 TRACK_APPEARED_LEFT(A,A:track_002); CLOSING_START(A,A:track_002)
-5.05 CRITICAL_TTC_START(B,A)
-4.70 TRACK_APPEARED_LEFT(B,B:track_003); CLOSING_START(B,B:track_003)
-2.90 TRACK_APPEARED_RIGHT(C,A); CLOSING_START(C,A)
-1.60 THROTTLE_END(A); BRAKE_START(A)
-1.40 CLOSING_START(B,A)
-1.15 CLOSING_END(C,A)
-1.10 CLOSING_END(A,A:track_002); CLOSING_END(A,C)
-1.00 BRAKE_END(A)
-0.90 THROTTLE_START(A)
-0.70 TRACK_LOST(B,B:track_003)
-0.35 CRITICAL_TTC_START(A,C)
-0.15 THROTTLE_END(B); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_002)
-0.10 CUT_IN_FROM_LEFT_START(A,C)
+0.00 COLLISION(A,B); THROTTLE_END(A); BRAKE_START(A); CLOSING_START(A,A:track_002); CLOSING_START(A,C); CLOSING_START(C,A)
+0.05 CRITICAL_TTC_END(B,A); BRAKE_END(A); CRITICAL_TTC_START(C,A)
+0.10 CLOSING_END(B,A)
+0.20 EGO_PATH_ENTRY(A,C)
+0.25 CLOSING_END(B,B:track_002)
+0.65 MOVING_END(B); STOP_START(B)
+0.90 TRACK_LOST(C,A)
+1.05 COLLISION(A,C); CLOSING_END(A,A:track_002); CLOSING_END(A,C)
+1.10 THROTTLE_END(C); BRAKE_START(C)
+1.20 TRACK_LOST(A,A:track_002)
+1.25 TRACK_APPEARED_LEFT(B,B:track_004)
+1.30 CUT_IN_FROM_LEFT_END(A,C)
+1.45 CRITICAL_TTC_END(A,C)
+1.55 TRACK_LOST(B,B:track_004)
+1.70 EGO_PATH_EXIT(B,A)
+1.90 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C); BRAKE_START(A)
```

### S17/run_0_crash

```
-4.95 MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_001); CLOSING_START(B,B:track_002)
-2.35 CRITICAL_TTC_START(A,A:track_001)
-2.20 CUT_IN_FROM_RIGHT_START(A,A:track_001)
-1.60 EGO_PATH_ENTRY(A,A:track_001)
-1.15 CRITICAL_TTC_START(A,B)
-0.85 CUT_IN_FROM_RIGHT_END(A,A:track_001)
-0.80 CRITICAL_TTC_START(B,A)
-0.75 CLOSING_START(A,B)
-0.70 CLOSING_START(B,A)
-0.40 CLOSING_END(A,A:track_001)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
+0.05 THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
+0.20 CLOSING_END(B,B:track_002)
+0.25 EGO_PATH_EXIT(A,A:track_001)
+0.55 CRITICAL_TTC_END(A,A:track_001)
+0.75 TRACK_LOST(B,B:track_002)
+1.00 MOVING_END(B); STOP_START(B)
+1.10 MOVING_END(A); STOP_START(A)
+1.30 EGO_PATH_ENTRY(B,A)
+1.45 TRACK_APPEARED_RIGHT(B,B:track_003)
+2.05 TRACK_LOST(B,B:track_003)
+2.50 TRACK_LOST(A,A:track_001)
```

