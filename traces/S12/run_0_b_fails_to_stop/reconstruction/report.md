# Reconstruction report - S12/run_0_b_fails_to_stop

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.95 s | 161 | 19 | 25 | 1 | A:e15 @ 9.70 s |
| B | 15.95 s | 161 | 15 | 24 | 1 | B:e09 @ 9.70 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e15 | 9.70 | -9.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 9.70 | -9.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 7339.57 vs 7339.57 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 5.45 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.3 m -> 1.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.22 m/s over 3.0 s<br>clearance at the contact 1.41 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.80 | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 1.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.8 m -> 0.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.02 m/s over 1.5 s<br>clearance at the contact 0.91 m<br>the only track of B compatible with the contact |

## Global graph

33 nodes, 56 edges; 1 merged node(s): g23 COLLISION(A,B) from A:e15 + B:e09.

### Event sequence (global time)

- `-9.70` MOVING_START(A); MOVING_START(B)
- `-9.05` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-7.75` BRAKE_START(B)
- `-7.45` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-7.05` BRAKE_END(B); BRAKE_START(A)
- `-6.30` MOVING_END(A); STOP_START(A)
- `-6.20` STOP_SIGN_DETECTED_START(B,B:sign-1)
- `-5.45` TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-4.40` STOP_SIGN_DETECTED_END(B,B:sign-1)
- `-1.95` BRAKE_END(A)
- `-1.60` STOP_END(A); MOVING_START(A)
- `-1.55` TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- `-1.10` CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-0.60` TURN_LEFT_START(A)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B)
- `+0.05` BRAKE_START(A); BRAKE_START(B)
- `+0.10` TURN_LEFT_END(A)
- `+0.35` CRITICAL_TTC_END(B,A); MOVING_END(B); STOP_START(B)
- `+0.45` CLOSING_END(B,A); EGO_PATH_ENTRY(B,A)
- `+0.50` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 9.70 s before the reference collision, A started moving (already the case when first observed).
- 9.70 s before the reference collision, B started moving (already the case when first observed).
- 9.05 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.75 s before the reference collision, B started braking.
- 7.45 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.05 s before the reference collision, B released the brake.
- 7.05 s before the reference collision, A started braking.
- 6.30 s before the reference collision, A stopped moving.
- 6.30 s before the reference collision, A came to a stop.
- 6.20 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-1).
- 5.45 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 5.45 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.40 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 1.95 s before the reference collision, A released the brake.
- 1.60 s before the reference collision, A left its stop.
- 1.60 s before the reference collision, A started moving.
- 1.55 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 1.55 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.10 s before the reference collision, A's time-to-contact with B became critical.
- 1.10 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A started turning left.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 7340, B: 7340 N*s).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A stopped turning left.
- 0.35 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B stopped moving.
- 0.35 s after the reference collision, B came to a stop.
- 0.45 s after the reference collision, B observed A stop closing in.
- 0.45 s after the reference collision, B observed A enter its forward path corridor.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.60, COLLISION with B 9.70 (+1.10 s) [local times; t_global: critical_ttc_start -1.10, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.60, COLLISION with A 9.70 (+1.10 s); EGO_PATH_ENTRY 10.15 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.10, ego_path_entry +0.45, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- BRAKE_END(B); BRAKE_START(A)
- MOVING_END(A); STOP_START(A)
- TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- STOP_END(A); MOVING_START(A)
- TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- BRAKE_START(A); BRAKE_START(B)
- CRITICAL_TTC_END(B,A); MOVING_END(B); STOP_START(B)
- CLOSING_END(B,A); EGO_PATH_ENTRY(B,A)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e08 (t = 4.25 s); the track was lost at 9.65 s
- CRITICAL_TTC of track_001, since A:e12 (t = 8.60 s); the track was lost at 9.65 s
- BRAKE, since A:e16 (t = 9.75 s)
- STOP, since A:e19 (t = 10.20 s)
B:
- BRAKE, since B:e10 (t = 9.75 s)
- STOP, since B:e13 (t = 10.05 s)
- EGO_PATH of track_001, since B:e15 (t = 10.15 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
B:
- STOP sign sign-1: detected 3.50 s -> 5.30 s; relevant to the path: True; STOP_START inside: none

### Perceived state just before each collision report

- A A:e15 at 9.70 s (local): ego: MOVING, TURN_LEFT; track lost, states UNKNOWN: track_001; sign-0: STOP sign known, relevant to the path
- B B:e09 at 9.70 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; sign-1: STOP sign known, relevant to the path

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 9.65 s (A:e14): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
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
