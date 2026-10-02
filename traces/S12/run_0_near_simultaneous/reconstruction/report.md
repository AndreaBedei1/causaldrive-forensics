# Reconstruction report - S12/run_0_near_simultaneous

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.95 s | 151 | 23 | 36 | 1 | A:e16 @ 9.50 s |
| B | 14.95 s | 151 | 22 | 39 | 1 | B:e16 @ 9.50 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.5 m -> 1.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.33 m/s over 3.0 s<br>clearance at the contact 1.00 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.9 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.64 m/s over 3.0 s<br>clearance at the contact 0.07 m<br>the only track of B compatible with the contact |

## Global graph

44 nodes, 101 edges; 1 merged node(s): g31 COLLISION(A,B) from A:e16 + B:e16.

### Event sequence (global time)

- `-9.50` MOVING_START(A); MOVING_START(B)
- `-8.85` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-7.70` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-7.25` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-6.90` STOP_SIGN_DETECTED_END(B,B:sign-0); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-6.85` BRAKE_START(A)
- `-6.75` BRAKE_START(B)
- `-6.70` TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- `-6.10` MOVING_END(A); STOP_START(A)
- `-6.05` CLOSING_END(B,A)
- `-6.00` CLOSING_END(A,B); MOVING_END(B); STOP_START(B)
- `-2.55` BRAKE_END(A); BRAKE_END(B)
- `-2.20` STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
- `-2.15` STOP_END(B); MOVING_START(B)
- `-1.25` CRITICAL_TTC_START(A,B)
- `-1.20` TURN_LEFT_START(A); CRITICAL_TTC_START(B,A)
- `-0.55` EGO_PATH_ENTRY(B,A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); EGO_PATH_EXIT(B,A)
- `+0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B)
- `+0.45` MOVING_END(B); STOP_START(B)
- `+0.50` TURN_LEFT_END(A); MOVING_END(A); STOP_START(A)
- `+1.45` STOP_SIGN_DETECTED_START(A,A:sign-1)

### What happened, in plain language

- 9.50 s before the reference collision, A started moving (already the case when first observed).
- 9.50 s before the reference collision, B started moving (already the case when first observed).
- 8.85 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 7.25 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 6.90 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 6.90 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.90 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.85 s before the reference collision, A started braking.
- 6.75 s before the reference collision, B started braking.
- 6.70 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 6.10 s before the reference collision, A stopped moving.
- 6.10 s before the reference collision, A came to a stop.
- 6.05 s before the reference collision, B observed A stop closing in.
- 6.00 s before the reference collision, A observed B stop closing in.
- 6.00 s before the reference collision, B stopped moving.
- 6.00 s before the reference collision, B came to a stop.
- 2.55 s before the reference collision, A released the brake.
- 2.55 s before the reference collision, B released the brake.
- 2.20 s before the reference collision, A left its stop.
- 2.20 s before the reference collision, A started moving.
- 2.20 s before the reference collision, A observed B start closing in.
- 2.20 s before the reference collision, B observed A start closing in.
- 2.15 s before the reference collision, B left its stop.
- 2.15 s before the reference collision, B started moving.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 1.20 s before the reference collision, A started turning left.
- 1.20 s before the reference collision, B's time-to-contact with A became critical.
- 0.55 s before the reference collision, B observed A enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A leave its forward path corridor.
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A stopped turning left.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.
- 1.45 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.25, COLLISION with B 9.50 (+1.25 s) [local times; t_global: critical_ttc_start -1.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.30, COLLISION with A 9.50 (+1.20 s); EGO_PATH_ENTRY 8.95 after critical TTC (+0.65 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -0.55, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- STOP_SIGN_DETECTED_END(B,B:sign-0); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- MOVING_END(A); STOP_START(A)
- CLOSING_END(A,B); MOVING_END(B); STOP_START(B)
- BRAKE_END(A); BRAKE_END(B)
- STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
- STOP_END(B); MOVING_START(B)
- TURN_LEFT_START(A); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); EGO_PATH_EXIT(B,A)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- TURN_LEFT_END(A); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e19 (t = 9.55 s)
- STOP, since A:e22 (t = 10.00 s)
- STOP_SIGN_DETECTED of sign-1, since A:e23 (t = 10.95 s)
B:
- BRAKE, since B:e20 (t = 9.55 s)
- STOP, since B:e22 (t = 9.95 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 10.95 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-0: detected 1.80 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

### Perceived state just before each collision report

- A A:e16 at 9.50 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC; sign-0: STOP sign known, relevant to the path
- B B:e16 at 9.50 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; sign-0: STOP sign known, relevant to the path

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost

## Uncertainty and limitations

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
