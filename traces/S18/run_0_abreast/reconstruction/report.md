# Reconstruction report - S18/run_0_abreast

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.45 s | 116 | 26 | 49 | 5 | A:e16 @ 6.20 s |
| B | 11.45 s | 116 | 25 | 42 | 4 | B:e12 @ 6.20 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1079.56 vs 1079.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.5 m -> 15.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.90 s before the matched collision<br>lost 2.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.1 m -> 15.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.53 m/s over 0.9 s<br>anonymous road user U4: A:track_001#segment_2 |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.2 m -> 15.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.93 m/s over 2.0 s<br>clearance at the contact 15.19 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s<br>clearance at the contact 0.18 m<br>the only track of A compatible with the contact |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.4 m -> 15.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.36 m/s over 3.0 s<br>clearance at the contact 15.38 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 3.0 s<br>clearance at the contact 0.52 m<br>the only compatible track of B touching it at the contact (clearance 0.52 m; track_002, track_003, track_004 at 16.71 m, 17.18 m, 18.06 m) |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.6 m -> 16.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 16.71 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.0 m -> 17.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 3.0 s<br>clearance at the contact 17.14 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_004 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 19.1 m -> 18.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.18 m/s over 3.0 s<br>clearance at the contact 18.06 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |

## Road users in the common frame

- U1 (anonymous, -6.20 to -5.95 s): A:track_001#segment_1; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -6.20 to 4.00 s): B:track_002, B:track_004, A:track_001#segment_3 joined by same box B:track_002-B:track_004 (93% of 75 instants); same box A:track_001#segment_3-B:track_002 (100% of 69 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U3 (anonymous, -6.20 to 4.25 s): B:track_003, A:track_003 joined by same box A:track_003-B:track_003 (91% of 115 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -5.90 to -2.10 s): A:track_001#segment_2; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.

## Global graph

46 nodes, 105 edges; 16 merged node(s): g06 TRACK_APPEARED_RIGHT(A,U1) from A:e04 + A:e06, g08 TRACK_APPEARED_RIGHT(B,U2) from B:e04 + B:e24 + B:e06 + B:e23, g09 TRACK_APPEARED_RIGHT(B,U3) from B:e05 + B:e25, g10 CLOSING_START(B,U2) from B:e07 + B:e18 + B:e09 + B:e17, g11 CLOSING_START(B,U3) from B:e08 + B:e16, g12 TRACK_APPEARED_FRONT(A,U3) from A:e05 + A:e26, g14 TRACK_APPEARED_RIGHT(A,U4) from A:e07 + A:e09, g17 TRACK_APPEARED_FRONT(A,U2) from A:e10 + A:e25, g18 CRITICAL_TTC_START(A,U2) from A:e11 + A:e14, g19 CRITICAL_TTC_START(A,B) from A:e12 + A:e17, g20 CRITICAL_TTC_START(B,A) from B:e10 + B:e13, g21 CLOSING_START(A,B) from A:e13 + A:e21, g22 CLOSING_START(B,A) from B:e11 + B:e19, g25 COLLISION(A,B) from A:e16 + B:e12, g35 CLOSING_END(B,U2) from B:e18 + B:e17, g42 TRACK_LOST(B,U2) from B:e24 + B:e23.

### Event sequence (global time)

- `-6.20` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U2); CLOSING_START(B,U3)
- `-5.95` TRACK_APPEARED_FRONT(A,U3); TRACK_LOST(A,U1)
- `-5.90` TRACK_APPEARED_RIGHT(A,U4)
- `-2.50` EGO_PATH_EXIT(A,U3)
- `-2.10` TRACK_LOST(A,U4)
- `-2.05` TRACK_APPEARED_FRONT(A,U2)
- `-1.55` CRITICAL_TTC_START(A,U2)
- `-1.05` CRITICAL_TTC_START(A,B)
- `-0.65` CRITICAL_TTC_START(B,A)
- `-0.60` CLOSING_START(A,B)
- `-0.55` CLOSING_START(B,A)
- `-0.45` CRITICAL_TTC_END(A,U2); EGO_PATH_EXIT(A,U2)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- `+0.10` CLOSING_END(B,U3); EGO_PATH_ENTRY(A,B)
- `+0.20` CLOSING_END(A,B); CLOSING_END(B,U2)
- `+0.30` CLOSING_END(B,A)
- `+1.05` MOVING_END(B); STOP_START(B)
- `+1.15` MOVING_END(A); STOP_START(A)
- `+1.20` EGO_PATH_ENTRY(B,A)
- `+2.75` TRACK_LOST(B,U2); TRACK_LOST(B,U3)
- `+3.20` CUT_IN_FROM_RIGHT_START(A,U3)
- `+4.00` TRACK_LOST(A,U2)
- `+4.25` TRACK_LOST(A,U3)

### What happened, in plain language

- 6.20 s before the reference collision, A started moving (already the case when first observed).
- 6.20 s before the reference collision, B started moving (already the case when first observed).
- 6.20 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.20 s before the reference collision, B observed anonymous road user U2 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 5.95 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 5.95 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 2.50 s before the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 2.10 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.05 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 1.55 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U2 stopped being critical.
- 0.45 s before the reference collision, A observed anonymous road user U2 leave its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1080, B: 1080 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 stop closing in.
- 0.30 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, B observed A enter its forward path corridor.
- 2.75 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.75 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.20 s after the reference collision, A observed anonymous road user U3 cutting in from the right.
- 4.00 s after the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001#segment_3 (unidentified U2): CRITICAL_TTC_START 4.65, COLLISION 6.20 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s); EGO_PATH_ENTRY 6.30 after critical TTC (+1.15 s) [local times; t_global: critical_ttc_start -1.05, ego_path_entry +0.10, collision +0.00]
- A's track_003 (unidentified U3): CUT_IN_FROM_RIGHT_START 9.40, no critical TTC after it [local times; t_global: cut_in +3.20]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s); EGO_PATH_ENTRY 7.40 after critical TTC (+1.85 s) [local times; t_global: critical_ttc_start -0.65, ego_path_entry +1.20, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U2); CLOSING_START(B,U3)
- TRACK_APPEARED_FRONT(A,U3); TRACK_LOST(A,U1)
- CRITICAL_TTC_END(A,U2); EGO_PATH_EXIT(A,U2)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A)
- THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- CLOSING_END(B,U3); EGO_PATH_ENTRY(A,B)
- CLOSING_END(A,B); CLOSING_END(B,U2)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)
- TRACK_LOST(B,U2); TRACK_LOST(B,U3)

### States still active when observation ended

A:
- BRAKE, since A:e19 (t = 6.25 s)
- EGO_PATH of track_002, since A:e20 (t = 6.30 s)
- STOP, since A:e23 (t = 7.35 s)
- CUT_IN_FROM_RIGHT of track_003, since A:e24 (t = 9.40 s); the track was lost at 10.45 s
B:
- BRAKE, since B:e15 (t = 6.25 s)
- STOP, since B:e21 (t = 7.25 s)
- EGO_PATH of track_001, since B:e22 (t = 7.40 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e16 at 6.20 s (local): ego: MOVING, THROTTLE; track_001#segment_3: no active state; track_002: CLOSING, CRITICAL_TTC; track_003: no active state; track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2
- B B:e12 at 6.20 s (local): ego: MOVING, THROTTLE; track_001: CLOSING, CRITICAL_TTC; track_002: CLOSING; track_003: CLOSING; track_004: CLOSING

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_003 at 10.45 s (A:e26): CUT_IN_FROM_RIGHT were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_1, track_001#segment_2, track_001#segment_3
B:
- lost with no state active: track_004, track_002, track_003

## Uncertainty and limitations

- A:track_001#segment_1 stays anonymous (U1): lost 5.95 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 15.5 m -> 15.6 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_001#segment_2 stays anonymous (U4): lost 2.10 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 15.1 m -> 15.2 m over the last 1.0 s.
- A:track_001#segment_3 stays anonymous (U2): not approaching before the contact: clearance 15.2 m -> 15.4 m over the last 1.0 s.
- A:track_003 stays anonymous (U3): not approaching before the contact: clearance 15.4 m -> 15.7 m over the last 1.0 s.
- B:track_002 stays anonymous (U2): ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004).
- B:track_003 stays anonymous (U3): ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004).
- B:track_004 stays anonymous (U2): ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004).
- Global time rests on matched collisions (t_global = 0 at the reference one) and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from the collisions that align each recorder.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `anonymous_entities.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5,
    "new_impact_ratio": 0.75,
    "min_impact_ratio": 0.25,
    "min_new_impact_impulse": 1000.0,
    "impact_acceleration_mps2": 20.0,
    "reversal_angle_deg": 90.0,
    "undirected_impact_ratio": 0.5
  },
  "tracking": {
    "min_height_m": 0.3,
    "max_height_m": 2.5,
    "moving_speed_mps": 1.0,
    "cluster_distance_m": 2.0,
    "max_association_distance_m": 2.5,
    "max_velocity_mismatch_mps": 4.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0,
    "smoothing_innovation_sigma": 3.0,
    "min_slowdown_returns": 3,
    "identity_body_width_m": 2.5
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "throttle_on_threshold": 0.1,
    "throttle_off_threshold": 0.05,
    "throttle_release_debounce_s": 0.2,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_lateral_margin_m": 0.3,
    "critical_release_ratio": 0.75,
    "prediction_horizon_s": 6.0,
    "prediction_time_step_s": 0.05,
    "target_length_m": 4.6,
    "target_width_m": 1.9,
    "target_braking_min_mps2": 1.0,
    "critical_min_track_age_s": 0.5,
    "critical_time_gap_table": [
      [
        7.2,
        1.0
      ],
      [
        10.0,
        1.1
      ],
      [
        20.0,
        1.2
      ],
      [
        30.0,
        1.3
      ],
      [
        40.0,
        1.4
      ],
      [
        50.0,
        1.5
      ],
      [
        60.0,
        1.6
      ]
    ],
    "critical_min_following_distance_m": 2.0,
    "critical_forward_min_speed_mps": 1.0,
    "critical_front_lateral_margin_m": 1.0,
    "critical_front_lateral_speed_mps": 0.3,
    "critical_forward_release_factor": 1.1,
    "occlusion_margin_m": 0.5,
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
    "path_hysteresis_m": 0.5,
    "track_appeared_front_deg": 5.0,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "cut_in_max_heading_deg": 25.0,
    "cut_in_min_target_speed_mps": 2.0,
    "cut_in_lateral_speed_mps": 0.3,
    "cut_in_persistence_s": 0.5,
    "cut_in_outside_margin_m": 0.5,
    "cut_in_min_displacement_m": 0.5,
    "cut_in_horizon_s": 3.0,
    "cut_in_preentry_margin_m": 1.0,
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "impulse_relative_std": 0.1,
    "impulse_sigma_gate": 3.0,
    "contact_consistency_m": 1.0,
    "clock_tolerance_s": 0.1,
    "contact_window_s": 1.0,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5,
    "touching_clearance_m": 1.0,
    "rival_clearance_m": 2.0,
    "observed_alignment_step_s": 0.05,
    "observed_alignment_min_samples": 10,
    "observed_alignment_min_speed_mps": 2.0,
    "observed_alignment_uniqueness_ratio": 3.0,
    "link_min_samples": 10,
    "link_min_fraction": 0.8,
    "anonymous_gate_probability": 0.99,
    "anonymous_min_shared_samples": 10,
    "anonymous_pass_fraction": 0.8,
    "stitch_max_gap_s": 1.5,
    "box_face_std_m": 0.25,
    "box_length_std_m": 0.7,
    "box_width_std_m": 0.2,
    "entity_output_rate_hz": 10.0,
    "mutual_refinement": false,
    "mutual_refinement_iterations": 3
  }
}
```
