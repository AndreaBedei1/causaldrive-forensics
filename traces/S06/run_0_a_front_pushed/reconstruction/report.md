# Reconstruction report - S06/run_0_a_front_pushed

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 29.95 s | 301 | 19 | 37 | 2 | A:e13 @ 5.90 s |
| B | 29.95 s | 301 | 23 | 37 | 2 | B:e18 @ 5.90 s, B:e21 @ 6.05 s |
| C | 29.95 s | 301 | 19 | 30 | 3 | C:e19 @ 6.05 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e13 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | ALIGNED | C:e19 | 6.05 | -5.90 | shares collision_002 with B, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 11621.71 vs 11621.71 N*s (similarity 1.000, tolerance 0.10); 2 competing report(s) within tolerance; best match kept

Matched `collision_002`: B and C both recorded a collision; peak impulses 10857.64 vs 10857.64 N*s (similarity 1.000, tolerance 0.10); 2 competing report(s) within tolerance; best match kept

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.66 | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.7 m -> 0.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.37 m/s over 3.0 s<br>clearance at the contact 0.53 m<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 4.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.7 m -> 5.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.44 m/s over 3.0 s (> 1.50)<br>clearance at the contact 5.31 m (beyond 3.50 m: confidence factor 0.83) |
| B:track_001 | C | ASSOCIATED | 1.00 | B and C both reported collision_002 at 6.05 s (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 0.23 m<br>the only track of B compatible with the contact<br>collision_001 with A at 5.90 s: not compatible (not approaching before the contact: clearance 1.1 m -> 1.1 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 10.87 m/s over 3.0 s (> 1.50)) |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 at 5.90 s (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.5 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.09 m/s over 2.9 s<br>clearance at the contact 0.50 m<br>the only track of B compatible with the contact<br>collision_002 with C at 6.05 s: not compatible (track speed disagrees with C's own speed: RMSE 11.40 m/s over 2.8 s (> 1.50)) |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>lost 3.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 34.3 m -> 35.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 3.0 m -> 3.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.23 m/s over 3.0 s<br>clearance at the contact 2.95 m |
| C:track_003 | C:track_003 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.20 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.2 m -> 6.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 12.78 m/s over 1.2 s (> 1.50)<br>clearance at the contact 6.46 m (beyond 3.50 m: confidence factor 0.62) |

## Global graph

59 nodes, 121 edges; 2 merged node(s): g48 COLLISION(A,B) from A:e13 + B:e18, g51 COLLISION(B,C) from B:e21 + C:e19.

### Event sequence (global time)

- `-5.90` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,C:track_001); TRACK_APPEARED_REAR(C,C:track_002)
- `-5.45` CLOSING_START(A,B)
- `-5.40` CLOSING_START(B,A)
- `-5.10` CLOSING_START(C,C:track_001)
- `-4.90` TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
- `-4.85` CLOSING_START(B,C); CLOSING_START(C,C:track_002)
- `-4.25` CLOSING_END(A,B); CLOSING_END(B,A)
- `-3.95` CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001)
- `-3.85` CLOSING_END(B,C); CLOSING_END(C,C:track_002)
- `-3.50` SPEED_LIMIT_EXCEEDED_START(C)
- `-2.95` BRAKE_START(C)
- `-2.90` TRACK_LOST(C,C:track_001)
- `-2.85` SPEED_LIMIT_EXCEEDED_END(C)
- `-2.70` CLOSING_START(B,C)
- `-2.65` CLOSING_START(A,A:track_002)
- `-2.60` CLOSING_START(C,C:track_002)
- `-2.20` BRAKE_START(B)
- `-2.15` CRITICAL_TTC_START(B,C)
- `-1.95` CLOSING_START(B,A)
- `-1.90` CLOSING_START(A,B)
- `-1.85` MOVING_END(C); STOP_START(C)
- `-1.75` CRITICAL_TTC_START(A,A:track_002)
- `-1.30` TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003)
- `-1.20` CRITICAL_TTC_START(A,B)
- `-1.00` CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
- `-0.35` BRAKE_START(A)
- `-0.20` BRAKE_END(B)
- `-0.05` TRACK_LOST(B,A); TRACK_LOST(C,C:track_003)
- `+0.00` COLLISION(A,B); STOP_END(B); MOVING_START(B)
- `+0.15` COLLISION(B,C)
- `+0.20` CRITICAL_TTC_END(A,A:track_002); CRITICAL_TTC_END(A,B); CLOSING_END(A,A:track_002); CLOSING_END(A,B)
- `+0.25` MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B)

### What happened, in plain language

- 5.90 s before the reference collision, A started moving (already the case when first observed).
- 5.90 s before the reference collision, B started moving (already the case when first observed).
- 5.90 s before the reference collision, C started moving (already the case when first observed).
- 5.90 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking C, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 5.90 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared behind it.
- 5.90 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared behind it.
- 5.45 s before the reference collision, A observed B start closing in.
- 5.40 s before the reference collision, B observed A start closing in.
- 5.10 s before the reference collision, C observed unidentified object C:track_001 start closing in.
- 4.90 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 4.90 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.85 s before the reference collision, B observed C start closing in.
- 4.85 s before the reference collision, C observed unidentified object C:track_002 start closing in.
- 4.25 s before the reference collision, A observed B stop closing in.
- 4.25 s before the reference collision, B observed A stop closing in.
- 3.95 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 3.95 s before the reference collision, C observed unidentified object C:track_001 stop closing in.
- 3.85 s before the reference collision, B observed C stop closing in.
- 3.85 s before the reference collision, C observed unidentified object C:track_002 stop closing in.
- 3.50 s before the reference collision, C began exceeding the speed limit.
- 2.95 s before the reference collision, C started braking.
- 2.90 s before the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- 2.85 s before the reference collision, C returned within the speed limit.
- 2.70 s before the reference collision, B observed C start closing in.
- 2.65 s before the reference collision, A observed unidentified object A:track_002 start closing in.
- 2.60 s before the reference collision, C observed unidentified object C:track_002 start closing in.
- 2.20 s before the reference collision, B started braking.
- 2.15 s before the reference collision, B's time-to-contact with C became critical.
- 1.95 s before the reference collision, B observed A start closing in.
- 1.90 s before the reference collision, A observed B start closing in.
- 1.85 s before the reference collision, C stopped moving.
- 1.85 s before the reference collision, C came to a stop.
- 1.75 s before the reference collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 1.30 s before the reference collision, C's radar started tracking unidentified object C:track_003, which appeared behind it.
- 1.30 s before the reference collision, C observed unidentified object C:track_003 start closing in (already the case when first observed).
- 1.20 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, B's time-to-contact with C stopped being critical.
- 1.00 s before the reference collision, B observed C stop closing in.
- 1.00 s before the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.00 s before the reference collision, B stopped moving.
- 1.00 s before the reference collision, B came to a stop.
- 0.35 s before the reference collision, A started braking.
- 0.20 s before the reference collision, B released the brake.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, C's radar lost unidentified object C:track_003 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 11622, B: 11622 N*s).
- At the reference collision, B left its stop.
- At the reference collision, B started moving.
- 0.15 s after the reference collision, B and C both recorded this same collision (peak impulses B: 10858, C: 10858 N*s).
- 0.20 s after the reference collision, A's time-to-contact with unidentified object A:track_002 stopped being critical.
- 0.20 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.20 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, A stopped moving.
- 0.25 s after the reference collision, B stopped moving.
- 0.25 s after the reference collision, A came to a stop.
- 0.25 s after the reference collision, B came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.70, COLLISION with B 5.90 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 4.15, COLLISION 5.90 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]
- B's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 6.05 (+2.30 s) [local times; t_global: critical_ttc_start -2.15, collision +0.15]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,C:track_001); TRACK_APPEARED_REAR(C,C:track_002)
- TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
- CLOSING_START(B,C); CLOSING_START(C,C:track_002)
- CLOSING_END(A,B); CLOSING_END(B,A)
- CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001)
- CLOSING_END(B,C); CLOSING_END(C,C:track_002)
- MOVING_END(C); STOP_START(C)
- TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003)
- CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
- TRACK_LOST(B,A); TRACK_LOST(C,C:track_003)
- COLLISION(A,B); STOP_END(B); MOVING_START(B)
- CRITICAL_TTC_END(A,A:track_002); CRITICAL_TTC_END(A,B); CLOSING_END(A,A:track_002); CLOSING_END(A,B)
- MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B)

### States still active when observation ended

A:
- BRAKE, since A:e12 (t = 5.55 s)
- STOP, since A:e19 (t = 6.15 s)
B:
- CLOSING of track_002, since B:e11 (t = 3.95 s); the track was lost at 5.85 s
- STOP, since B:e23 (t = 6.15 s)
C:
- BRAKE, since C:e09 (t = 2.95 s)
- STOP, since C:e14 (t = 4.05 s)
- CLOSING of track_003, since C:e16 (t = 4.60 s); the track was lost at 5.85 s

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e13 at 5.90 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e18 at 5.90 s (local): ego: STOP; track_001: IN_EGO_PATH; track lost, states UNKNOWN: track_002
- B B:e21 at 6.05 s (local): ego: MOVING; track_001: IN_EGO_PATH; track lost, states UNKNOWN: track_002
- C C:e19 at 6.05 s (local): ego: STOP, BRAKE; track_002: no active state; track lost, states UNKNOWN: track_001, track_003

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- track_002 at 5.85 s (B:e17): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
C:
- track_003 at 5.85 s (C:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Uncertainty and limitations

- A:track_002 stays anonymous: track speed disagrees with B's own speed: RMSE 5.44 m/s over 3.0 s (> 1.50).
- C:track_001 stays anonymous: lost 3.05 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 34.3 m -> 35.8 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- C:track_002 stays anonymous: not approaching before the contact: clearance 3.0 m -> 3.7 m over the last 1.0 s.
- C:track_003 stays anonymous: track speed disagrees with B's own speed: RMSE 12.78 m/s over 1.2 s (> 1.50).
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
