# Reconstruction report - S16/run_0_independent

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 17.95 s | 181 | 20 | 30 | 2 | A:e03 @ 5.15 s, A:e16 @ 14.10 s |
| B | 17.95 s | 181 | 19 | 34 | 3 | B:e10 @ 5.15 s |
| C | 17.95 s | 181 | 13 | 19 | 0 | C:e10 @ 14.10 s |

## Graph alignment

Reference event: `collision_002` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | ALIGNED | B:e10 | 5.15 | -14.10 | shares collision_001 with A, aligned through collision_002 -> collision_001 |
| C | ALIGNED | C:e10 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9095.53 vs 9095.53 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and C both reported collision_002 at 14.10 s (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>lost 2.20 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 14.9 m -> 14.7 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.26 m/s over 0.8 s<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 6.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_002 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 at 14.10 s (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 8.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.15 m/s over 2.9 s<br>range at the contact 0.18 m<br>the only track of A compatible with the contact<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 6.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 3.9 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.52 m/s over 3.0 s<br>range at the contact 0.55 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 8.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 8.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Global graph

50 nodes, 85 edges; 2 merged node(s): g15 COLLISION(A,B) from A:e03 + B:e10, g42 COLLISION(A,C) from A:e16 + C:e10.

### Event sequence (global time)

- `-14.10` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
- `-13.60` MOVING_END(C); STOP_START(C)
- `-13.40` CLOSING_START(B,A)
- `-13.35` CRITICAL_TTC_START(B,A)
- `-12.70` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-10.15` BRAKE_START(A)
- `-9.85` CLOSING_START(B,A)
- `-9.65` CRITICAL_TTC_START(B,A)
- `-9.35` BRAKE_START(B)
- `-8.95` COLLISION(A,B)
- `-8.90` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-8.50` MOVING_END(B); STOP_START(B)
- `-8.30` MOVING_END(A); STOP_START(A)
- `-5.00` YIELD_SIGN_DETECTED_START(C,C:sign-1)
- `-4.50` YIELD_SIGN_DETECTED_END(C,C:sign-1)
- `-3.15` BRAKE_END(A)
- `-2.95` TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_LEFT(A,C)
- `-2.70` STOP_END(A); MOVING_START(A)
- `-2.35` CLOSING_START(A,C)
- `-2.30` CLOSING_START(A,A:track_001)
- `-2.20` TRACK_LOST(A,A:track_001)
- `-2.15` STOP_END(C); MOVING_START(C)
- `-2.00` EGO_PATH_ENTRY(A,C)
- `-1.45` CRITICAL_TTC_START(A,C)
- `-0.65` EGO_PATH_EXIT(B,A)
- `-0.55` TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003)
- `-0.30` STOP_SIGN_DETECTED_START(C,C:sign-3); STOP_SIGN_DETECTED_END(C,C:sign-3)
- `-0.10` TRACK_LOST(B,A)
- `+0.00` COLLISION(A,C); BRAKE_START(C)
- `+0.20` CLOSING_END(A,C)
- `+0.25` TRACK_LOST(A,C)
- `+0.40` TRACK_LOST(B,B:track_003)
- `+0.55` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### What happened, in plain language

- 14.10 s before the reference collision, A started moving (already the case when first observed).
- 14.10 s before the reference collision, B started moving (already the case when first observed).
- 14.10 s before the reference collision, C started moving (already the case when first observed).
- 14.10 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 13.60 s before the reference collision, C stopped moving.
- 13.60 s before the reference collision, C came to a stop.
- 13.40 s before the reference collision, B observed A start closing in.
- 13.35 s before the reference collision, B's time-to-contact with A became critical.
- 12.70 s before the reference collision, B's time-to-contact with A stopped being critical.
- 12.70 s before the reference collision, B observed A stop closing in.
- 10.15 s before the reference collision, A started braking.
- 9.85 s before the reference collision, B observed A start closing in.
- 9.65 s before the reference collision, B's time-to-contact with A became critical.
- 9.35 s before the reference collision, B started braking.
- 8.95 s before the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 8.90 s before the reference collision, B's time-to-contact with A stopped being critical.
- 8.90 s before the reference collision, B observed A stop closing in.
- 8.50 s before the reference collision, B stopped moving.
- 8.50 s before the reference collision, B came to a stop.
- 8.30 s before the reference collision, A stopped moving.
- 8.30 s before the reference collision, A came to a stop.
- 5.00 s before the reference collision, C's camera established a YIELD sign detection (unidentified object C:sign-1) (the detector judged it not relevant to its path).
- 4.50 s before the reference collision, C's camera stopped detecting YIELD sign unidentified object C:sign-1.
- 3.15 s before the reference collision, A released the brake.
- 2.95 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 2.95 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 2.70 s before the reference collision, A left its stop.
- 2.70 s before the reference collision, A started moving.
- 2.35 s before the reference collision, A observed C start closing in.
- 2.30 s before the reference collision, A observed unidentified object A:track_001 start closing in.
- 2.20 s before the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 2.15 s before the reference collision, C left its stop.
- 2.15 s before the reference collision, C started moving.
- 2.00 s before the reference collision, A observed C enter its forward path corridor.
- 1.45 s before the reference collision, A's time-to-contact with C became critical.
- 0.65 s before the reference collision, B observed A leave its forward path corridor.
- 0.55 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 0.55 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.30 s before the reference collision, C's camera established a STOP sign detection (unidentified object C:sign-3) (the detector judged it not relevant to its path).
- 0.30 s before the reference collision, C's camera stopped detecting STOP sign unidentified object C:sign-3.
- 0.10 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and C both recorded this same collision (peak impulses A: 9096, C: 9096 N*s).
- At the reference collision, C started braking.
- 0.20 s after the reference collision, A observed C stop closing in.
- 0.25 s after the reference collision, A's radar lost C (its states are UNKNOWN from then on, not ended).
- 0.40 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, C stopped moving.
- 0.55 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, C came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_002 (C): CRITICAL_TTC_START 12.65, COLLISION with C 14.10 (+1.45 s); EGO_PATH_ENTRY 12.10 before critical TTC (-0.55 s) [local times; t_global: critical_ttc_start -1.45, ego_path_entry -2.00, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -13.35, collision -8.95]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
- MOVING_END(C); STOP_START(C)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)
- TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_LEFT(A,C)
- STOP_END(A); MOVING_START(A)
- STOP_END(C); MOVING_START(C)
- TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003)
- STOP_SIGN_DETECTED_START(C,C:sign-3); STOP_SIGN_DETECTED_END(C,C:sign-3)
- COLLISION(A,C); BRAKE_START(C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e12 (t = 11.80 s); the track was lost at 11.90 s
- EGO_PATH of track_002, since A:e14 (t = 12.10 s); the track was lost at 14.35 s
- CRITICAL_TTC of track_002, since A:e15 (t = 12.65 s); the track was lost at 14.35 s
- STOP, since A:e20 (t = 14.65 s)
B:
- BRAKE, since B:e09 (t = 4.75 s)
- STOP, since B:e14 (t = 5.60 s)
C:
- BRAKE, since C:e11 (t = 14.10 s)
- STOP, since C:e13 (t = 14.65 s)

### Sign detection windows

A:
- none
B:
- none
C:
- STOP sign sign-3: detected 13.80 s -> 13.80 s; relevant to the path: False; STOP_START inside: none
- YIELD sign sign-1: detected 9.10 s -> 9.60 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened

### Perceived state just before each collision report

- A A:e03 at 5.15 s (local): ego: MOVING, BRAKE
- A A:e16 at 14.10 s (local): ego: MOVING; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track lost, states UNKNOWN: track_001
- B B:e10 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- C C:e10 at 14.10 s (local): ego: MOVING; sign-1: YIELD sign known; sign-3: STOP sign known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 11.90 s (A:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 14.35 s (A:e18): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
B:
- lost with no state active: track_001, track_003
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_001 stays anonymous: collision_002 with C: lost 2.20 s before the matched collision (window 0.50 s).
- B:track_002 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 8.40 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 8.40 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
    "new_impact_ratio": 0.5,
    "reversal_impact_ratio": 0.25,
    "impact_acceleration_mps2": 20.0,
    "reversal_angle_deg": 90.0
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
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
