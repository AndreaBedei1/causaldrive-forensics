# Reconstruction report - S16/run_0_consequential

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 14 | 18 | 1 | A:e07 @ 5.15 s, A:e11 @ 5.90 s |
| B | 9.95 s | 101 | 14 | 24 | 1 | B:e10 @ 5.15 s |
| C | 9.95 s | 101 | 15 | 25 | 2 | C:e10 @ 5.90 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | ALIGNED | C:e10 | 5.90 | -5.15 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.3 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 0.20 m<br>the only track of A compatible with the contact<br>collision_002 with C at 5.90 s: not compatible (not approaching before the contact: clearance 1.1 m -> 2.1 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 10.63 m/s over 3.0 s (> 1.50)) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 0.66 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.84 | C and A both reported collision_002 (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.75 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.0 m -> 5.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 2.2 s<br>clearance at the contact 4.97 m (beyond 3.50 m: confidence factor 0.89)<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.0 m -> 6.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.66 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.05 m (beyond 3.50 m: confidence factor 0.70) |

## Global graph

41 nodes, 83 edges; 2 merged node(s): g23 COLLISION(A,B) from A:e07 + B:e10, g33 COLLISION(A,C) from A:e11 + C:e10.

### Event sequence (global time)

- `-5.15` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B); TRACK_APPEARED_REAR(C,A); CLOSING_START(C,A)
- `-5.00` TRACK_APPEARED_REAR(C,C:track_002); CLOSING_START(C,C:track_002)
- `-4.85` MOVING_END(C); STOP_START(C)
- `-4.50` CLOSING_START(B,A)
- `-4.45` CLOSING_START(A,B)
- `-4.40` CRITICAL_TTC_START(B,A)
- `-3.75` CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
- `-1.20` BRAKE_START(A)
- `-0.95` CLOSING_START(A,B)
- `-0.90` CLOSING_START(B,A)
- `-0.75` CRITICAL_TTC_START(B,A)
- `-0.40` BRAKE_START(B)
- `+0.00` COLLISION(A,B); CLOSING_END(A,B); TRACK_LOST(C,A)
- `+0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
- `+0.25` TURN_LEFT_START(A)
- `+0.45` CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
- `+0.75` COLLISION(A,C); STOP_END(C); MOVING_START(C)
- `+0.80` BRAKE_START(C)
- `+0.85` TURN_LEFT_END(A)
- `+0.90` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### What happened, in plain language

- 5.15 s before the reference collision, A started moving (already the case when first observed).
- 5.15 s before the reference collision, B started moving (already the case when first observed).
- 5.15 s before the reference collision, C started moving (already the case when first observed).
- 5.15 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.15 s before the reference collision, A's radar started tracking B, which appeared behind it.
- 5.15 s before the reference collision, C's radar started tracking A, which appeared behind it.
- 5.15 s before the reference collision, C observed A start closing in (already the case when first observed).
- 5.00 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared behind it.
- 5.00 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 4.85 s before the reference collision, C stopped moving.
- 4.85 s before the reference collision, C came to a stop.
- 4.50 s before the reference collision, B observed A start closing in.
- 4.45 s before the reference collision, A observed B start closing in.
- 4.40 s before the reference collision, B's time-to-contact with A became critical.
- 3.75 s before the reference collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the reference collision, A observed B stop closing in.
- 3.75 s before the reference collision, B observed A stop closing in.
- 1.20 s before the reference collision, A started braking.
- 0.95 s before the reference collision, A observed B start closing in.
- 0.90 s before the reference collision, B observed A start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.40 s before the reference collision, B started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the brake.
- 0.25 s after the reference collision, A started turning left.
- 0.45 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.75 s after the reference collision, A and C both recorded this same collision (peak impulses A: 2696, C: 2696 N*s).
- 0.75 s after the reference collision, C left its stop.
- 0.75 s after the reference collision, C started moving.
- 0.80 s after the reference collision, C started braking.
- 0.85 s after the reference collision, A stopped turning left.
- 0.90 s after the reference collision, A stopped moving.
- 0.90 s after the reference collision, C stopped moving.
- 0.90 s after the reference collision, A came to a stop.
- 0.90 s after the reference collision, C came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B); TRACK_APPEARED_REAR(C,A); CLOSING_START(C,A)
- TRACK_APPEARED_REAR(C,C:track_002); CLOSING_START(C,C:track_002)
- MOVING_END(C); STOP_START(C)
- CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
- COLLISION(A,B); CLOSING_END(A,B); TRACK_LOST(C,A)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
- CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
- COLLISION(A,C); STOP_END(C); MOVING_START(C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### States still active when observation ended

A:
- STOP, since A:e14 (t = 6.05 s)
B:
- BRAKE, since B:e09 (t = 4.75 s)
- STOP, since B:e14 (t = 5.60 s)
C:
- CLOSING of track_001, since C:e03 (t = 0.00 s); the track was lost at 5.15 s
- BRAKE, since C:e13 (t = 5.95 s)
- STOP, since C:e15 (t = 6.05 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e07 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING
- A A:e11 at 5.90 s (local): ego: MOVING, TURN_LEFT; track_001: no active state
- B B:e10 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- C C:e10 at 5.90 s (local): ego: STOP; track_002: no active state; track lost, states UNKNOWN: track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost
C:
- track_001 at 5.15 s (C:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- C:track_002 stays anonymous: track speed disagrees with A's own speed: RMSE 2.66 m/s over 3.0 s (> 1.50).
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
    "acceleration_std_mps2": 6.0
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_release_ratio": 0.75,
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
    "track_appeared_front_deg": 5.0,
    "track_appeared_rear_deg": 5.0,
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
    "speed_consistency_mps": 1.5
  }
}
```
