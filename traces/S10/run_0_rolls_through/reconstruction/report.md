# Reconstruction report - S10/run_0_rolls_through

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.95 s | 161 | 16 | 26 | 1 | A:e10 @ 5.25 s |
| B | 15.95 s | 161 | 11 | 18 | 1 | B:e06 @ 5.25 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12489.77 vs 12489.77 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.9 m -> 1.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.55 m/s over 2.8 s (> 1.50)<br>range at the contact 1.44 m |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.6 m -> 1.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.66 m/s over 2.6 s<br>range at the contact 1.17 m<br>the only track of B compatible with the contact |

## Global graph

26 nodes, 51 edges; 1 merged node(s): g15 COLLISION(A,B) from A:e10 + B:e06.

### Event sequence (global time)

- `-5.25` MOVING_START(A); MOVING_START(B)
- `-3.45` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-3.30` BRAKE_START(A)
- `-3.10` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-2.80` TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.65` TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- `-2.55` TURN_LEFT_START(A)
- `-1.70` CRITICAL_TTC_START(B,A)
- `-1.45` BRAKE_END(A)
- `-1.40` CRITICAL_TTC_START(A,A:track_001)
- `-0.30` EGO_PATH_ENTRY(B,A)
- `+0.00` COLLISION(A,B); CLOSING_END(A,A:track_001); TRACK_LOST(A,A:track_001)
- `+0.05` TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B)
- `+0.10` MOVING_END(B); STOP_START(B)
- `+0.15` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 5.25 s before the reference collision, A started moving (already the case when first observed).
- 5.25 s before the reference collision, B started moving (already the case when first observed).
- 3.45 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 3.30 s before the reference collision, A started braking.
- 3.10 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 2.80 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 2.80 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.65 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 2.65 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.55 s before the reference collision, A started turning left.
- 1.70 s before the reference collision, B's time-to-contact with A became critical.
- 1.45 s before the reference collision, A released the brake.
- 1.40 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.30 s before the reference collision, B observed A enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12490, B: 12490 N*s).
- At the reference collision, A observed unidentified object A:track_001 stop closing in.
- At the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 0.05 s after the reference collision, A stopped turning left.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B stopped moving.
- 0.10 s after the reference collision, B came to a stop.
- 0.15 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.15 s after the reference collision, B observed A stop closing in.
- 0.15 s after the reference collision, A stopped moving.
- 0.15 s after the reference collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 3.85, COLLISION 5.25 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 3.55, COLLISION with A 5.25 (+1.70 s); EGO_PATH_ENTRY 4.95 after critical TTC (+1.40 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.30, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- COLLISION(A,B); CLOSING_END(A,A:track_001); TRACK_LOST(A,A:track_001)
- TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CRITICAL_TTC of track_001, since A:e09 (t = 3.85 s); the track was lost at 5.25 s
- BRAKE, since A:e14 (t = 5.30 s)
- STOP, since A:e16 (t = 5.40 s)
B:
- EGO_PATH of track_001, since B:e05 (t = 4.95 s)
- BRAKE, since B:e07 (t = 5.30 s)
- STOP, since B:e09 (t = 5.35 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 1.80 s -> 2.15 s; relevant to the path: False; STOP_START inside: none
B:
- none

### Perceived state just before each collision report

- A A:e10 at 5.25 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC; sign-0: STOP sign known
- B B:e06 at 5.25 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 5.25 s (A:e12): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost

## Uncertainty and limitations

- A:track_001 stays anonymous: track speed disagrees with B's own speed: RMSE 1.55 m/s over 2.8 s (> 1.50).
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
