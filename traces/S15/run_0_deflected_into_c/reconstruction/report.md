# Reconstruction report - S15/run_0_deflected_into_c

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 21 | 42 | 2 | A:e09 @ 3.80 s, A:e15 @ 4.70 s |
| B | 13.95 s | 141 | 28 | 49 | 2 | B:e16 @ 3.80 s |
| C | 13.95 s | 141 | 15 | 31 | 2 | C:e08 @ 4.70 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e08 | 4.70 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 10358.22 vs 10358.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1880.32 vs 1880.32 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.98 | A and C both reported collision_002 at 4.70 s (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 0.0 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.34 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.67 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.82 | A and B both reported collision_001 at 3.80 s (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.5 m -> 0.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.94 m/s over 1.8 s<br>clearance at the contact 0.56 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.70 s: not compatible (not approaching before the contact: clearance 1.1 m -> 1.3 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 3.39 m/s over 2.7 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 2.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.2 m -> 9.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.95 m/s over 2.1 s (> 1.50)<br>clearance at the contact 9.08 m (beyond 3.50 m: confidence factor 0.18) |
| B:track_002 | A | ASSOCIATED | 0.93 | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.6 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.57 m/s over 1.8 s<br>clearance at the contact 0.34 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.98 | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 0.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.27 m/s over 3.0 s<br>clearance at the contact 0.06 m<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.7 m -> 5.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.90 m/s over 3.0 s (> 1.50)<br>clearance at the contact 5.19 m (beyond 3.50 m: confidence factor 0.85) |

## Global graph

62 nodes, 143 edges; 2 merged node(s): g31 COLLISION(A,B) from A:e09 + B:e16, g46 COLLISION(A,C) from A:e15 + C:e08.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- `-3.60` TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
- `-2.70` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-2.10` TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- `-1.80` TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- `-1.75` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- `-1.55` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.50` TURN_LEFT_START(B)
- `-1.30` CRITICAL_TTC_START(B,A)
- `-1.25` CRITICAL_TTC_START(A,B)
- `-0.85` THROTTLE_END(B); BRAKE_START(B)
- `-0.30` BRAKE_END(B)
- `-0.15` THROTTLE_START(B)
- `-0.05` EGO_PATH_ENTRY(B,A); CRITICAL_TTC_START(A,C); CRITICAL_TTC_START(C,A)
- `+0.00` COLLISION(A,B); CLOSING_END(A,B); TURN_LEFT_END(B)
- `+0.05` CRITICAL_TTC_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(B); TURN_LEFT_START(A)
- `+0.15` CLOSING_END(B,A); CRITICAL_TTC_START(B,B:track_001)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.25` CRITICAL_TTC_END(B,A)
- `+0.55` EGO_PATH_ENTRY(A,C)
- `+0.75` EGO_PATH_EXIT(B,A)
- `+0.90` COLLISION(A,C); CRITICAL_TTC_END(C,A); CLOSING_END(C,A); EGO_PATH_EXIT(A,C)
- `+0.95` THROTTLE_END(C); BRAKE_START(C)
- `+1.05` CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
- `+1.15` CRITICAL_TTC_END(B,B:track_001)
- `+1.20` CLOSING_END(C,C:track_002); MOVING_END(C); STOP_START(C)
- `+1.25` TURN_LEFT_END(A)
- `+1.30` MOVING_END(A); STOP_START(A)
- `+1.70` TRACK_LOST(B,A)
- `+1.80` CLOSING_END(B,B:track_001)

### What happened, in plain language

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.80 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.80 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.80 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.80 s before the reference collision, C observed A start closing in (already the case when first observed).
- 3.60 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its left.
- 3.60 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 2.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 2.10 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.10 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.80 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.80 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.75 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.75 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.55 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.50 s before the reference collision, B started turning left.
- 1.30 s before the reference collision, B's time-to-contact with A became critical.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, B released the accelerator.
- 0.85 s before the reference collision, B started braking.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B pressed the accelerator.
- 0.05 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's time-to-contact with C became critical.
- 0.05 s before the reference collision, C's time-to-contact with A became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 10358, B: 10358 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, B stopped turning left.
- 0.05 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A started turning left.
- 0.15 s after the reference collision, B observed A stop closing in.
- 0.15 s after the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.25 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.55 s after the reference collision, A observed C enter its forward path corridor.
- 0.75 s after the reference collision, B observed A leave its forward path corridor.
- 0.90 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1880, C: 1880 N*s).
- 0.90 s after the reference collision, C's time-to-contact with A stopped being critical.
- 0.90 s after the reference collision, C observed A stop closing in.
- 0.90 s after the reference collision, A observed C leave its forward path corridor.
- 0.95 s after the reference collision, C released the accelerator.
- 0.95 s after the reference collision, C started braking.
- 1.05 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.15 s after the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.20 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.20 s after the reference collision, C stopped moving.
- 1.20 s after the reference collision, C came to a stop.
- 1.25 s after the reference collision, A stopped turning left.
- 1.30 s after the reference collision, A stopped moving.
- 1.30 s after the reference collision, A came to a stop.
- 1.70 s after the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 1.80 s after the reference collision, B observed unidentified object B:track_001 stop closing in.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 4.70 (+0.95 s); EGO_PATH_ENTRY 4.35 after critical TTC (+0.60 s) [local times; t_global: critical_ttc_start -0.05, ego_path_entry +0.55, collision +0.90]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 3.80 (+1.25 s) [local times; t_global: critical_ttc_start -1.25, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.95 [local times; t_global: critical_ttc_start +0.15]
- B's track_002 (A): CRITICAL_TTC_START 2.50, COLLISION with A 3.80 (+1.30 s); EGO_PATH_ENTRY 3.75 after critical TTC (+1.25 s) [local times; t_global: critical_ttc_start -1.30, ego_path_entry -0.05, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 3.75, COLLISION with A 4.70 (+0.95 s) [local times; t_global: critical_ttc_start -0.05, collision +0.90]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
- TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- THROTTLE_END(B); BRAKE_START(B)
- EGO_PATH_ENTRY(B,A); CRITICAL_TTC_START(A,C); CRITICAL_TTC_START(C,A)
- COLLISION(A,B); CLOSING_END(A,B); TURN_LEFT_END(B)
- CRITICAL_TTC_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(B); TURN_LEFT_START(A)
- CLOSING_END(B,A); CRITICAL_TTC_START(B,B:track_001)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,C); CRITICAL_TTC_END(C,A); CLOSING_END(C,A); EGO_PATH_EXIT(A,C)
- THROTTLE_END(C); BRAKE_START(C)
- CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
- CLOSING_END(C,C:track_002); MOVING_END(C); STOP_START(C)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- STOP, since A:e21 (t = 5.10 s)
B:
- BRAKE, since B:e19 (t = 3.85 s)
- STOP, since B:e23 (t = 4.00 s)
C:
- BRAKE, since C:e12 (t = 4.75 s)
- STOP, since C:e15 (t = 5.00 s)

### Sign detection windows

A:
- none
B:
- STOP sign sign-0: detected 1.10 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
C:
- none

### Perceived state just before each collision report

- A A:e09 at 3.80 s (local): ego: MOVING, THROTTLE; track_001: CLOSING, CRITICAL_TTC; track_002: CLOSING, CRITICAL_TTC
- A A:e15 at 4.70 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_002: no active state
- B B:e16 at 3.80 s (local): ego: MOVING, THROTTLE, TURN_LEFT; track_001: CLOSING; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH; sign-0: STOP sign known, relevant to the path
- C C:e08 at 4.70 s (local): ego: MOVING, THROTTLE; track_001: CLOSING, CRITICAL_TTC; track_002: CLOSING

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- lost with no state active: track_002
C:
- no track was lost

## Uncertainty and limitations

- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 4.95 m/s over 2.1 s (> 1.50).
- C:track_002 stays anonymous: track speed disagrees with A's own speed: RMSE 3.90 m/s over 3.0 s (> 1.50).
- Global time rests on matched collisions (t_global = 0 at the reference one) and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from the collisions that align each recorder.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

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
    "min_slowdown_returns": 3
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
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
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
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "clock_tolerance_s": 0.1,
    "contact_window_s": 1.0,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5,
    "touching_clearance_m": 1.0,
    "rival_clearance_m": 2.0
  }
}
```
