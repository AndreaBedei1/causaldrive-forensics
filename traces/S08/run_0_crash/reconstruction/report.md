# Reconstruction report - S08/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 153 | 21 | 48 | 2 | A:e08 @ 4.10 s |
| B | 15.15 s | 153 | 19 | 42 | 2 | B:e08 @ 4.10 s |
| C | 15.15 s | 153 | 20 | 38 | 4 | none |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| C | ALIGNED | - | - | -4.10 | aligned through observed trajectories: the near surfaces of A:track_001, B:track_001, C:track_001#segment_1 on A, C:track_001#segment_2 on A, C:track_001#segment_3 on B, C:track_002 on B lie where their lines of sight enter the body (pooled median 0.62 sigma) at this offset; offsets within 2.00 sigma span [-4.20, -4.00] s and nothing else fits |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12137.11 vs 12137.11 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 4.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.7 m -> 11.7 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.47 m/s over 3.0 s (> 1.50)<br>clearance at the contact 11.69 m (beyond 3.50 m: confidence factor 0.02)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 303 samples; 100% within 3 sigma) at C's own velocity (median difference 0.09 m/s) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.65 m/s over 2.0 s<br>clearance at the contact 0.35 m<br>the only track of A compatible with the contact |
| B:track_001 | C | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.6 m -> 10.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.61 m/s over 2.0 s (> 1.50)<br>clearance at the contact 10.71 m (beyond 3.50 m: confidence factor 0.06)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 262 samples; 94% within 3 sigma) at C's own velocity (median difference 0.05 m/s) |
| B:track_002 | A | ASSOCIATED | 0.89 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.2 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.71 m/s over 2.0 s<br>clearance at the contact 0.46 m<br>the only track of B compatible with the contact |
| C:track_001#segment_1 | A | ASSOCIATED | 1.00 | no matched collision of C names a partner<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 69 samples before A's contact with a third body at +0.00 s; 100% within 3 sigma) at A's own velocity (median difference 0.13 m/s) |
| C:track_001#segment_2 | U2 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U2: C:track_001#segment_2 |
| C:track_001#segment_3 | U3 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U3: C:track_001#segment_3 |
| C:track_002 | U1 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U1: C:track_002 |

## Road users in the common frame

- Observed-trajectory alignment of C: accepted (offset -4.10, pooled median 0.62 sigma, interval [-4.2, -4.0]).
- A:track_001 is C: its returns lie on C's own footprint (median 0.00 m over 303 samples, 100% within 3 sigma) at C's velocity.
- B:track_001 is C: its returns lie on C's own footprint (median 0.00 m over 262 samples, 94% within 3 sigma) at C's velocity.
- C:track_001#segment_1 is A: its returns lie on A's own footprint (median 0.00 m over 69 samples, 100% within 3 sigma) at A's velocity.
- U1 (anonymous, -2.00 to 1.70 s): C:track_002; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -0.40 to 0.95 s): C:track_001#segment_2; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U3 (anonymous, 1.00 to 11.05 s): C:track_001#segment_3; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.

## Global graph

59 nodes, 185 edges; 1 merged node(s): g28 COLLISION(A,B) from A:e08 + B:e08.

### Event sequence (global time)

- `-4.10` MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- `-2.05` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- `-2.00` TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_LEFT(C,U1); TRACK_APPEARED_RIGHT(B,C); CLOSING_START(B,A); CLOSING_START(B,C); CLOSING_START(C,U1)
- `-1.75` THROTTLE_END(C); BRAKE_START(C)
- `-1.55` CRITICAL_TTC_START(A,B)
- `-1.50` CRITICAL_TTC_START(B,A)
- `-1.20` MOVING_END(C); STOP_START(C)
- `-0.45` TRACK_LOST(C,A)
- `-0.40` TRACK_APPEARED_LEFT(C,U2); CLOSING_START(C,U2)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); EGO_PATH_ENTRY(A,C)
- `+0.15` EGO_PATH_EXIT(A,C); CLOSING_START(A,B); CLOSING_START(B,A)
- `+0.50` CLOSING_END(B,C); CLOSING_END(C,U2); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
- `+0.55` CLOSING_END(A,B); EGO_PATH_ENTRY(C,U1)
- `+0.60` TURN_LEFT_END(A)
- `+0.65` CLOSING_END(A,C); CLOSING_END(B,A); CLOSING_END(C,U1); MOVING_END(A); STOP_START(A)
- `+0.95` TRACK_LOST(C,U2)
- `+1.00` TRACK_APPEARED_LEFT(C,U3)
- `+1.70` TRACK_LOST(C,U1)
- `+2.15` EGO_PATH_ENTRY(C,U3)

### What happened, in plain language

- 4.10 s before the reference collision, A started moving (already the case when first observed).
- 4.10 s before the reference collision, B started moving (already the case when first observed).
- 4.10 s before the reference collision, C started moving (already the case when first observed).
- 4.10 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 4.10 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 4.10 s before the reference collision, A observed C start closing in (already the case when first observed).
- 4.10 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.05 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.00 s before the reference collision, C's radar started tracking anonymous road user U1, which appeared on its left.
- 2.00 s before the reference collision, B's radar started tracking C, which appeared on its right.
- 2.00 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.00 s before the reference collision, B observed C start closing in (already the case when first observed).
- 2.00 s before the reference collision, C observed anonymous road user U1 start closing in (already the case when first observed).
- 1.75 s before the reference collision, C released the accelerator.
- 1.75 s before the reference collision, C started braking.
- 1.55 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, B's time-to-contact with A became critical.
- 1.20 s before the reference collision, C stopped moving.
- 1.20 s before the reference collision, C came to a stop.
- 0.45 s before the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.40 s before the reference collision, C's radar started tracking anonymous road user U2, which appeared on its left.
- 0.40 s before the reference collision, C observed anonymous road user U2 start closing in (already the case when first observed).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12137, B: 12137 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- At the reference collision, A started turning left.
- At the reference collision, B started turning right.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A observed C enter its forward path corridor.
- 0.15 s after the reference collision, A observed C leave its forward path corridor.
- 0.15 s after the reference collision, A observed B start closing in.
- 0.15 s after the reference collision, B observed A start closing in.
- 0.50 s after the reference collision, B observed C stop closing in.
- 0.50 s after the reference collision, C observed anonymous road user U2 stop closing in.
- 0.50 s after the reference collision, B stopped turning right.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, A observed B stop closing in.
- 0.55 s after the reference collision, C observed anonymous road user U1 enter its forward path corridor.
- 0.60 s after the reference collision, A stopped turning left.
- 0.65 s after the reference collision, A observed C stop closing in.
- 0.65 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, C observed anonymous road user U1 stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- 0.95 s after the reference collision, C's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, C's radar started tracking anonymous road user U3, which appeared on its left.
- 1.70 s after the reference collision, C's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 2.15 s after the reference collision, C observed anonymous road user U3 enter its forward path corridor.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (C): EGO_PATH_ENTRY 4.15, no critical TTC [local times; t_global: ego_path_entry +0.05]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 4.10 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.60, COLLISION with A 4.10 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]
- C's track_001#segment_3 (unidentified U3): EGO_PATH_ENTRY 6.25, no critical TTC [local times; t_global: ego_path_entry +2.15]
- C's track_002 (unidentified U1): EGO_PATH_ENTRY 4.65, no critical TTC [local times; t_global: ego_path_entry +0.55]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_LEFT(C,U1); TRACK_APPEARED_RIGHT(B,C); CLOSING_START(B,A); CLOSING_START(B,C); CLOSING_START(C,U1)
- THROTTLE_END(C); BRAKE_START(C)
- MOVING_END(C); STOP_START(C)
- TRACK_APPEARED_LEFT(C,U2); CLOSING_START(C,U2)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B)
- THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); EGO_PATH_ENTRY(A,C)
- EGO_PATH_EXIT(A,C); CLOSING_START(A,B); CLOSING_START(B,A)
- CLOSING_END(B,C); CLOSING_END(C,U2); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
- CLOSING_END(A,B); EGO_PATH_ENTRY(C,U1)
- CLOSING_END(A,C); CLOSING_END(B,A); CLOSING_END(C,U1); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e13 (t = 4.15 s)
- STOP, since A:e21 (t = 4.75 s)
B:
- BRAKE, since B:e13 (t = 4.15 s)
- STOP, since B:e18 (t = 4.60 s)
C:
- CLOSING of track_001#segment_1, since C:e04 (t = 0.00 s); the track was lost at 3.65 s
- BRAKE, since C:e08 (t = 2.35 s)
- STOP, since C:e10 (t = 2.90 s)
- EGO_PATH of track_002, since C:e15 (t = 4.65 s); the track was lost at 5.80 s
- EGO_PATH of track_001#segment_3, since C:e20 (t = 6.25 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e08 at 4.10 s (local): ego: MOVING, THROTTLE; track_001: CLOSING; track_002: CLOSING, CRITICAL_TTC
- B B:e08 at 4.10 s (local): ego: MOVING, THROTTLE; track_001: CLOSING; track_002: CLOSING, CRITICAL_TTC

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost
C:
- track_001#segment_1 at 3.65 s (C:e11): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 5.80 s (C:e19): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_2

## Uncertainty and limitations

- C:track_001#segment_2 stays anonymous (U2): no matched collision of C names a partner.
- C:track_001#segment_3 stays anonymous (U3): no matched collision of C names a partner.
- C:track_002 stays anonymous (U1): no matched collision of C names a partner.
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
