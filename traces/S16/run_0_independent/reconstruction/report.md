# Reconstruction report - S16/run_0_independent

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 17.95 s | 181 | 22 | 47 | 2 | A:e07 @ 5.15 s, A:e17 @ 14.10 s |
| B | 17.95 s | 181 | 17 | 30 | 2 | B:e10 @ 5.15 s |
| C | 17.95 s | 181 | 21 | 35 | 3 | C:e18 @ 14.10 s |

## Graph alignment

Reference event: `collision_002` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e17 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | ALIGNED | B:e10 | 5.15 | -14.10 | shares collision_001 with A, aligned through collision_002 -> collision_001 |
| C | ALIGNED | C:e18 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9089.81 vs 9089.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 0.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.37 m<br>the only track of A compatible with the contact<br>collision_002 with C at 14.10 s: not compatible (not approaching before the contact: clearance 11.5 m -> 20.3 m over the last 1.0 s) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 at 14.10 s (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.24 m/s over 0.9 s<br>clearance at the contact 0.10 m<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 8.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 3.0 s<br>clearance at the contact 0.65 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 6.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 10.65 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>not approaching before the contact: clearance 24.0 m -> 25.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.46 m/s over 3.0 s (> 1.50)<br>clearance at the contact 24.07 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 9.90 s before the matched collision<br>lost 8.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 22.7 m -> 14.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision |
| C:track_003 | C:track_003 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.60 s before the matched collision<br>lost 1.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 16.7 m -> 15.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.41 m/s over 0.8 s |

## Global graph

58 nodes, 131 edges; 2 merged node(s): g23 COLLISION(A,B) from A:e07 + B:e10, g50 COLLISION(A,C) from A:e17 + C:e18.

### Event sequence (global time)

- `-14.10` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B)
- `-13.60` MOVING_END(C); STOP_START(C)
- `-13.45` CLOSING_START(B,A)
- `-13.40` CLOSING_START(A,B)
- `-13.35` CRITICAL_TTC_START(B,A)
- `-12.70` CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
- `-10.65` TRACK_APPEARED_REAR(C,C:track_001); CLOSING_START(C,C:track_001)
- `-10.15` BRAKE_START(A)
- `-9.90` TRACK_APPEARED_RIGHT(C,C:track_002); CLOSING_START(A,B); CLOSING_START(B,A); CLOSING_START(C,C:track_002)
- `-9.70` CRITICAL_TTC_START(B,A)
- `-9.35` BRAKE_START(B)
- `-8.95` COLLISION(A,B); CLOSING_END(A,B)
- `-8.90` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-8.85` TRACK_LOST(C,C:track_002)
- `-8.50` CLOSING_END(C,C:track_001); MOVING_END(B); STOP_START(B)
- `-8.30` MOVING_END(A); STOP_START(A)
- `-3.15` BRAKE_END(A)
- `-2.70` STOP_END(A); MOVING_START(A)
- `-2.60` TRACK_APPEARED_RIGHT(C,C:track_003)
- `-2.35` CLOSING_START(C,C:track_003)
- `-2.15` STOP_END(C); MOVING_START(C); TRACK_APPEARED_LEFT(B,B:track_002)
- `-1.85` TRACK_LOST(C,C:track_003)
- `-0.95` TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_002)
- `-0.70` EGO_PATH_EXIT(B,A); STOP_SIGN_DETECTED_START(C,C:sign-3)
- `-0.50` STOP_SIGN_DETECTED_END(C,C:sign-3)
- `-0.05` TRACK_LOST(B,A); TRACK_LOST(C,C:track_001)
- `+0.00` COLLISION(A,C); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002); BRAKE_START(C)
- `+0.55` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
- `+3.70` TRACK_LOST(A,B)

### What happened, in plain language

- 14.10 s before the reference collision, A started moving (already the case when first observed).
- 14.10 s before the reference collision, B started moving (already the case when first observed).
- 14.10 s before the reference collision, C started moving (already the case when first observed).
- 14.10 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 14.10 s before the reference collision, A's radar started tracking B, which appeared behind it.
- 13.60 s before the reference collision, C stopped moving.
- 13.60 s before the reference collision, C came to a stop.
- 13.45 s before the reference collision, B observed A start closing in.
- 13.40 s before the reference collision, A observed B start closing in.
- 13.35 s before the reference collision, B's time-to-contact with A became critical.
- 12.70 s before the reference collision, B's time-to-contact with A stopped being critical.
- 12.70 s before the reference collision, A observed B stop closing in.
- 12.70 s before the reference collision, B observed A stop closing in.
- 10.65 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared behind it.
- 10.65 s before the reference collision, C observed unidentified object C:track_001 start closing in (already the case when first observed).
- 10.15 s before the reference collision, A started braking.
- 9.90 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its right.
- 9.90 s before the reference collision, A observed B start closing in.
- 9.90 s before the reference collision, B observed A start closing in.
- 9.90 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 9.70 s before the reference collision, B's time-to-contact with A became critical.
- 9.35 s before the reference collision, B started braking.
- 8.95 s before the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 8.95 s before the reference collision, A observed B stop closing in.
- 8.90 s before the reference collision, B's time-to-contact with A stopped being critical.
- 8.90 s before the reference collision, B observed A stop closing in.
- 8.85 s before the reference collision, C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- 8.50 s before the reference collision, C observed unidentified object C:track_001 stop closing in.
- 8.50 s before the reference collision, B stopped moving.
- 8.50 s before the reference collision, B came to a stop.
- 8.30 s before the reference collision, A stopped moving.
- 8.30 s before the reference collision, A came to a stop.
- 3.15 s before the reference collision, A released the brake.
- 2.70 s before the reference collision, A left its stop.
- 2.70 s before the reference collision, A started moving.
- 2.60 s before the reference collision, C's radar started tracking unidentified object C:track_003, which appeared on its right.
- 2.35 s before the reference collision, C observed unidentified object C:track_003 start closing in.
- 2.15 s before the reference collision, C left its stop.
- 2.15 s before the reference collision, C started moving.
- 2.15 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 1.85 s before the reference collision, C's radar lost unidentified object C:track_003 (its states are UNKNOWN from then on, not ended).
- 0.95 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 0.95 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.95 s before the reference collision, A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- 0.70 s before the reference collision, B observed A leave its forward path corridor.
- 0.70 s before the reference collision, C's camera established a STOP sign detection (unidentified object C:sign-3) (the detector judged it not relevant to its path).
- 0.50 s before the reference collision, C's camera stopped detecting STOP sign unidentified object C:sign-3.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and C both recorded this same collision (peak impulses A: 9090, C: 9090 N*s).
- At the reference collision, A's time-to-contact with unidentified object A:track_002 stopped being critical.
- At the reference collision, A observed unidentified object A:track_002 stop closing in.
- At the reference collision, C started braking.
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, C stopped moving.
- 0.55 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, C came to a stop.
- 3.70 s after the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 13.15, COLLISION 14.10 (+0.95 s) [local times; t_global: critical_ttc_start -0.95, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -13.35, collision -8.95]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B)
- MOVING_END(C); STOP_START(C)
- CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
- TRACK_APPEARED_REAR(C,C:track_001); CLOSING_START(C,C:track_001)
- TRACK_APPEARED_RIGHT(C,C:track_002); CLOSING_START(A,B); CLOSING_START(B,A); CLOSING_START(C,C:track_002)
- COLLISION(A,B); CLOSING_END(A,B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- CLOSING_END(C,C:track_001); MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)
- STOP_END(A); MOVING_START(A)
- STOP_END(C); MOVING_START(C); TRACK_APPEARED_LEFT(B,B:track_002)
- TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_002)
- EGO_PATH_EXIT(B,A); STOP_SIGN_DETECTED_START(C,C:sign-3)
- TRACK_LOST(B,A); TRACK_LOST(C,C:track_001)
- COLLISION(A,C); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002); BRAKE_START(C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### States still active when observation ended

A:
- STOP, since A:e21 (t = 14.65 s)
B:
- BRAKE, since B:e09 (t = 4.75 s)
- STOP, since B:e14 (t = 5.60 s)
C:
- CLOSING of track_002, since C:e07 (t = 4.20 s); the track was lost at 5.25 s
- CLOSING of track_003, since C:e11 (t = 11.75 s); the track was lost at 12.25 s
- BRAKE, since C:e19 (t = 14.10 s)
- STOP, since C:e21 (t = 14.65 s)

### Sign detection windows

A:
- none
B:
- none
C:
- STOP sign sign-3: detected 13.40 s -> 13.60 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- A A:e07 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING
- A A:e17 at 14.10 s (local): ego: MOVING; track_001: no active state; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e10 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- C C:e18 at 14.10 s (local): ego: MOVING; track lost, states UNKNOWN: track_001, track_002, track_003; sign-3: STOP sign known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_001
B:
- lost with no state active: track_001
C:
- track_002 at 5.25 s (C:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 12.25 s (C:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Uncertainty and limitations

- A:track_002 stays anonymous: collision_002 with C: tracked for 0.95 s before the matched collision (needs 1.00 s).
- B:track_002 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 6.80 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- C:track_001 stays anonymous: not approaching before the contact: clearance 24.0 m -> 25.1 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 6.46 m/s over 3.0 s (> 1.50).
- C:track_002 stays anonymous: lost 8.85 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- C:track_003 stays anonymous: lost 1.85 s before the matched collision (window 1.00 s).
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
