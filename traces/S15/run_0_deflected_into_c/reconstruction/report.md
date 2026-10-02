# Reconstruction report - S15/run_0_deflected_into_c

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 24 | 43 | 2 | A:e09 @ 3.80 s, A:e14 @ 4.75 s |
| B | 13.95 s | 141 | 26 | 51 | 2 | B:e15 @ 3.80 s |
| C | 13.95 s | 141 | 13 | 25 | 2 | C:e07 @ 4.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e15 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e07 | 4.75 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.96 | A and C both reported collision_002 at 4.75 s (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.9 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.43 m/s over 3.0 s<br>clearance at the contact 0.21 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.64 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 at 3.80 s (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.64 m/s over 1.6 s<br>clearance at the contact 0.75 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.75 s: not compatible (track speed disagrees with C's own speed: RMSE 3.27 m/s over 1.6 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.4 m -> 9.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.98 m/s over 2.0 s (> 1.50)<br>clearance at the contact 9.17 m (beyond 3.50 m: confidence factor 0.17) |
| B:track_002 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 1.7 s<br>clearance at the contact 0.18 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.97 | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.36 m/s over 3.0 s<br>clearance at the contact 1.10 m<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.0 m -> 6.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.99 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.69 m (beyond 3.50 m: confidence factor 0.57) |

## Global graph

61 nodes, 130 edges; 2 merged node(s): g29 COLLISION(A,B) from A:e09 + B:e15, g43 COLLISION(A,C) from A:e14 + C:e07.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B); MOVING_START(C)
- `-3.75` TRACK_APPEARED_FRONT(C,A); CLOSING_START(C,A)
- `-3.60` TRACK_APPEARED_FRONT(A,C); CLOSING_START(A,C)
- `-3.45` TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
- `-2.05` TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- `-2.00` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.75` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.70` TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-1.55` TURN_LEFT_START(B); CRITICAL_TTC_START(B,B:track_001)
- `-1.30` CRITICAL_TTC_START(A,C)
- `-0.95` CRITICAL_TTC_START(C,A)
- `-0.85` BRAKE_START(B)
- `-0.70` CRITICAL_TTC_END(B,B:track_001)
- `-0.30` BRAKE_END(B)
- `-0.15` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
- `+0.05` BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.35` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.65` CRITICAL_TTC_END(B,B:track_001)
- `+0.75` STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+0.85` EGO_PATH_ENTRY(A,C)
- `+0.90` EGO_PATH_EXIT(B,A)
- `+0.95` COLLISION(A,C)
- `+1.00` CLOSING_END(C,C:track_002); BRAKE_START(C)
- `+1.10` CLOSING_END(B,B:track_001)
- `+1.15` CRITICAL_TTC_END(C,A); CLOSING_END(C,A); TURN_LEFT_END(A)
- `+1.20` CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
- `+1.25` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
- `+1.45` STOP_SIGN_DETECTED_START(A,A:sign-2)
- `+3.00` TRACK_LOST(B,A)
- `+3.95` STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+4.85` STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+5.85` STOP_SIGN_DETECTED_START(A,A:sign-2)

### What happened, in plain language

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.75 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.75 s before the reference collision, C observed A start closing in (already the case when first observed).
- 3.60 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.60 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.45 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its left.
- 3.45 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 2.05 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.05 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.75 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.70 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.70 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.70 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's time-to-contact with A became critical (already the case when first observed).
- 1.55 s before the reference collision, B started turning left.
- 1.55 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.30 s before the reference collision, A's time-to-contact with C became critical.
- 0.95 s before the reference collision, C's time-to-contact with A became critical.
- 0.85 s before the reference collision, B started braking.
- 0.70 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.35 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.75 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.85 s after the reference collision, A observed C enter its forward path corridor.
- 0.90 s after the reference collision, B observed A leave its forward path corridor.
- 0.95 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1638, C: 1638 N*s).
- 1.00 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.00 s after the reference collision, C started braking.
- 1.10 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
- 1.15 s after the reference collision, C's time-to-contact with A stopped being critical.
- 1.15 s after the reference collision, C observed A stop closing in.
- 1.15 s after the reference collision, A stopped turning left.
- 1.20 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.20 s after the reference collision, A observed C stop closing in.
- 1.25 s after the reference collision, A stopped moving.
- 1.25 s after the reference collision, C stopped moving.
- 1.25 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, C came to a stop.
- 1.45 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 3.00 s after the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 3.95 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.85 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- 4.85 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 5.85 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 2.50, COLLISION with C 4.75 (+2.25 s); EGO_PATH_ENTRY 4.65 after critical TTC (+2.15 s) [local times; t_global: critical_ttc_start -1.30, ego_path_entry +0.85, collision +0.95]
- A's track_002 (B): CRITICAL_TTC_START 2.10, COLLISION with B 3.80 (+1.70 s) [local times; t_global: critical_ttc_start -1.70, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 2.25, COLLISION 3.80 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.10, COLLISION with A 3.80 (+1.70 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.15, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 2.85, COLLISION with A 4.75 (+1.90 s) [local times; t_global: critical_ttc_start -0.95, collision +0.95]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C)
- TRACK_APPEARED_FRONT(C,A); CLOSING_START(C,A)
- TRACK_APPEARED_FRONT(A,C); CLOSING_START(A,C)
- TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
- TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- TURN_LEFT_START(B); CRITICAL_TTC_START(B,B:track_001)
- COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
- BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- CLOSING_END(C,C:track_002); BRAKE_START(C)
- CRITICAL_TTC_END(C,A); CLOSING_END(C,A); TURN_LEFT_END(A)
- CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
- STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e05 (t = 2.10 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.10 s); the track was lost at 3.75 s
- EGO_PATH of track_001, since A:e13 (t = 4.65 s)
- STOP, since A:e19 (t = 5.05 s)
- STOP_SIGN_DETECTED of sign-2, since A:e24 (t = 9.65 s)
B:
- BRAKE, since B:e17 (t = 3.85 s)
- STOP, since B:e20 (t = 4.00 s)
C:
- BRAKE, since C:e09 (t = 4.80 s)
- STOP, since C:e13 (t = 5.05 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.55 s -> 4.55 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 5.25 s -> 7.75 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 8.65 s -> 8.65 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 9.65 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-0: detected 1.80 s -> 2.05 s; relevant to the path: False; STOP_START inside: none
C:
- none

### Perceived state just before each collision report

- A A:e09 at 3.80 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; track lost, states UNKNOWN: track_002
- A A:e14 at 4.75 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track lost, states UNKNOWN: track_002; sign-0: STOP sign known
- B B:e15 at 3.80 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH; sign-0: STOP sign known
- C C:e07 at 4.75 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; track_002: CLOSING

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.75 s (A:e08): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- lost with no state active: track_002
C:
- no track was lost

## Uncertainty and limitations

- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 4.98 m/s over 2.0 s (> 1.50).
- C:track_002 stays anonymous: track speed disagrees with A's own speed: RMSE 3.99 m/s over 3.0 s (> 1.50).
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
