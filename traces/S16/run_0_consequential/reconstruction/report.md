# Reconstruction report - S16/run_0_consequential

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 32 | 63 | 2 | A:e16 @ 5.55 s, A:e24 @ 6.60 s |
| B | 11.95 s | 121 | 23 | 42 | 4 | B:e15 @ 5.55 s |
| C | 11.95 s | 121 | 13 | 21 | 1 | C:e09 @ 6.60 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 5.55 | -5.55 | reported the reference collision collision_001 |
| B | ALIGNED | B:e15 | 5.55 | -5.55 | reported the reference collision collision_001 |
| C | ALIGNED | C:e09 | 6.60 | -5.55 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4243.51 vs 4243.51 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 322.1 vs 322.1 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.99 | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.16 m/s over 3.0 s<br>clearance at the contact 0.07 m<br>the only compatible track of A touching it at the contact (clearance 0.07 m; track_002 at 3.00 m)<br>collision_001 with B at 5.55 s: not compatible (track speed disagrees with B's own speed: RMSE 3.42 m/s over 3.0 s (> 1.50)) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 3.0 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.04 m/s over 3.0 s<br>clearance at the contact 2.99 m<br>collision_001 with B at 5.55 s: not compatible (not approaching before the contact: clearance 3.9 m -> 4.5 m over the last 1.0 s; track speed disagrees with B's own speed: RMSE 3.49 m/s over 3.0 s (> 1.50))<br>ambiguous: 2 persistent tracks of A are compatible with the contact collision_002 (track_001, track_002) |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.47 m/s over 3.0 s<br>clearance at the contact 0.04 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.1 m -> 6.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.30 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.02 m (beyond 3.50 m: confidence factor 0.70) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.70 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.9 m -> 11.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.55 m/s over 2.3 s (> 1.50)<br>clearance at the contact 11.44 m (beyond 3.50 m: confidence factor 0.03) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | A | ASSOCIATED | 0.98 | C and A both reported collision_002 (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 3.95 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.3 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 2.9 s<br>clearance at the contact 1.08 m<br>the only track of C compatible with the contact |

## Global graph

66 nodes, 146 edges; 2 merged node(s): g35 COLLISION(A,B) from A:e16 + B:e15, g51 COLLISION(A,C) from A:e24 + C:e09.

### Event sequence (global time)

- `-5.55` MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_LEFT(A,C); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(A,C); CLOSING_START(B,B:track_002)
- `-5.50` TRACK_APPEARED_LEFT(A,A:track_002); CLOSING_START(A,A:track_002)
- `-4.70` TRACK_APPEARED_LEFT(B,B:track_003); CLOSING_START(B,B:track_003)
- `-4.20` CUT_IN_FROM_LEFT_START(B,B:track_003)
- `-2.90` TRACK_APPEARED_RIGHT(C,A); CLOSING_START(C,A)
- `-2.85` CUT_IN_FROM_LEFT_END(B,B:track_003)
- `-1.60` THROTTLE_END(A); BRAKE_START(A)
- `-1.40` CLOSING_START(B,A); CRITICAL_TTC_START(B,A)
- `-1.15` CLOSING_END(C,A)
- `-1.10` CLOSING_END(A,A:track_002); CLOSING_END(A,C)
- `-1.00` BRAKE_END(A)
- `-0.90` THROTTLE_START(A)
- `-0.70` TRACK_LOST(B,B:track_003)
- `-0.35` CUT_IN_FROM_LEFT_START(A,A:track_002)
- `-0.15` THROTTLE_END(B); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_002)
- `-0.10` CUT_IN_FROM_LEFT_START(A,C)
- `+0.00` COLLISION(A,B); THROTTLE_END(A); BRAKE_START(A); CLOSING_START(A,A:track_002); CLOSING_START(A,C); CLOSING_START(C,A); CRITICAL_TTC_START(A,C)
- `+0.05` CRITICAL_TTC_END(B,A); BRAKE_END(A); CRITICAL_TTC_START(C,A)
- `+0.10` CLOSING_END(B,A)
- `+0.20` EGO_PATH_ENTRY(A,C)
- `+0.25` CLOSING_END(B,B:track_002)
- `+0.65` MOVING_END(B); STOP_START(B)
- `+0.90` TRACK_LOST(C,A)
- `+1.05` COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,A:track_002); CLOSING_END(A,C)
- `+1.10` THROTTLE_END(C); BRAKE_START(C)
- `+1.20` TRACK_LOST(A,A:track_002)
- `+1.25` TRACK_APPEARED_LEFT(B,B:track_004)
- `+1.30` CUT_IN_FROM_LEFT_END(A,C)
- `+1.55` TRACK_LOST(B,B:track_004)
- `+1.70` EGO_PATH_EXIT(B,A)
- `+1.90` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C); BRAKE_START(A)

### What happened, in plain language

- 5.55 s before the reference collision, A started moving (already the case when first observed).
- 5.55 s before the reference collision, B started moving (already the case when first observed).
- 5.55 s before the reference collision, C started moving (already the case when first observed).
- 5.55 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.55 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 5.55 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 5.55 s before the reference collision, A observed C start closing in (already the case when first observed).
- 5.55 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 5.50 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 5.50 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.70 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 4.70 s before the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 4.20 s before the reference collision, B observed unidentified object B:track_003 cutting in from the left.
- 2.90 s before the reference collision, C's radar started tracking A, which appeared on its right.
- 2.90 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.85 s before the reference collision, B observed unidentified object B:track_003's cut-in from the left settle.
- 1.60 s before the reference collision, A released the accelerator.
- 1.60 s before the reference collision, A started braking.
- 1.40 s before the reference collision, B observed A start closing in.
- 1.40 s before the reference collision, B's time-to-contact with A became critical.
- 1.15 s before the reference collision, C observed A stop closing in.
- 1.10 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 1.10 s before the reference collision, A observed C stop closing in.
- 1.00 s before the reference collision, A released the brake.
- 0.90 s before the reference collision, A pressed the accelerator.
- 0.70 s before the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.35 s before the reference collision, A observed unidentified object A:track_002 cutting in from the left.
- 0.15 s before the reference collision, B released the accelerator.
- 0.15 s before the reference collision, B started braking.
- 0.15 s before the reference collision, A observed unidentified object A:track_002 enter its forward path corridor.
- 0.10 s before the reference collision, A observed C cutting in from the left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4244, B: 4244 N*s).
- At the reference collision, A released the accelerator.
- At the reference collision, A started braking.
- At the reference collision, A observed unidentified object A:track_002 start closing in.
- At the reference collision, A observed C start closing in.
- At the reference collision, C observed A start closing in.
- At the reference collision, A's time-to-contact with C became critical.
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the brake.
- 0.05 s after the reference collision, C's time-to-contact with A became critical.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.20 s after the reference collision, A observed C enter its forward path corridor.
- 0.25 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.65 s after the reference collision, B stopped moving.
- 0.65 s after the reference collision, B came to a stop.
- 0.90 s after the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, A and C both recorded this same collision (peak impulses A: 322, C: 322 N*s).
- 1.05 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.05 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.10 s after the reference collision, C released the accelerator.
- 1.10 s after the reference collision, C started braking.
- 1.20 s after the reference collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 1.30 s after the reference collision, A observed C's cut-in from the left settle.
- 1.55 s after the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 1.70 s after the reference collision, B observed A leave its forward path corridor.
- 1.90 s after the reference collision, A stopped moving.
- 1.90 s after the reference collision, C stopped moving.
- 1.90 s after the reference collision, A came to a stop.
- 1.90 s after the reference collision, C came to a stop.
- 1.90 s after the reference collision, A started braking.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (C): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 5.45 < CRITICAL_TTC_START 5.55 (+0.10 s) < COLLISION with C 6.60 (+1.05 s); EGO_PATH_ENTRY 5.75 after critical TTC (+0.20 s) [local times; t_global: cut_in -0.10, critical_ttc_start +0.00, ego_path_entry +0.20, collision +1.05]
- A's track_002 (unidentified A:track_002): CUT_IN_FROM_LEFT_START 5.20, no critical TTC after it; EGO_PATH_ENTRY 5.40, no critical TTC [local times; t_global: cut_in -0.35, ego_path_entry -0.15, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.15, COLLISION with A 5.55 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]
- B's track_003 (unidentified B:track_003): CUT_IN_FROM_LEFT_START 1.35, no critical TTC after it [local times; t_global: cut_in -4.20, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 5.60, COLLISION with A 6.60 (+1.00 s) [local times; t_global: critical_ttc_start +0.05, collision +1.05]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_LEFT(A,C); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(A,C); CLOSING_START(B,B:track_002)
- TRACK_APPEARED_LEFT(A,A:track_002); CLOSING_START(A,A:track_002)
- TRACK_APPEARED_LEFT(B,B:track_003); CLOSING_START(B,B:track_003)
- TRACK_APPEARED_RIGHT(C,A); CLOSING_START(C,A)
- THROTTLE_END(A); BRAKE_START(A)
- CLOSING_START(B,A); CRITICAL_TTC_START(B,A)
- CLOSING_END(A,A:track_002); CLOSING_END(A,C)
- THROTTLE_END(B); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_002)
- COLLISION(A,B); THROTTLE_END(A); BRAKE_START(A); CLOSING_START(A,A:track_002); CLOSING_START(A,C); CLOSING_START(C,A); CRITICAL_TTC_START(A,C)
- CRITICAL_TTC_END(B,A); BRAKE_END(A); CRITICAL_TTC_START(C,A)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,A:track_002); CLOSING_END(A,C)
- THROTTLE_END(C); BRAKE_START(C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C); BRAKE_START(A)

### States still active when observation ended

A:
- CUT_IN_FROM_LEFT of track_002, since A:e13 (t = 5.20 s); the track was lost at 6.75 s
- EGO_PATH of track_002, since A:e14 (t = 5.40 s); the track was lost at 6.75 s
- EGO_PATH of track_001, since A:e23 (t = 5.75 s)
- STOP, since A:e31 (t = 7.45 s)
- BRAKE, since A:e32 (t = 7.45 s)
B:
- CLOSING of track_003, since B:e07 (t = 0.85 s); the track was lost at 4.85 s
- BRAKE, since B:e14 (t = 5.40 s)
- STOP, since B:e20 (t = 6.20 s)
C:
- CLOSING of track_001, since C:e06 (t = 5.55 s); the track was lost at 6.45 s
- CRITICAL_TTC of track_001, since C:e07 (t = 5.60 s); the track was lost at 6.45 s
- BRAKE, since C:e11 (t = 6.65 s)
- STOP, since C:e13 (t = 7.45 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e16 at 5.55 s (local): ego: MOVING, THROTTLE; track_001: CUT_IN_FROM_LEFT; track_002: IN_EGO_PATH, CUT_IN_FROM_LEFT
- A A:e24 at 6.60 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT; track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT
- B B:e15 at 5.55 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_002: CLOSING; track lost, states UNKNOWN: track_003
- C C:e09 at 6.60 s (local): ego: MOVING, THROTTLE; track lost, states UNKNOWN: track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 6.75 s (A:e28): IN_EGO_PATH, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_003 at 4.85 s (B:e12): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004
C:
- track_001 at 6.45 s (C:e08): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- A:track_002 stays anonymous: ambiguous: 2 persistent tracks of A are compatible with the contact collision_002 (track_001, track_002).
- B:track_002 stays anonymous: track speed disagrees with A's own speed: RMSE 2.30 m/s over 3.0 s (> 1.50).
- B:track_003 stays anonymous: track speed disagrees with A's own speed: RMSE 2.55 m/s over 2.3 s (> 1.50).
- B:track_004 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.25 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
