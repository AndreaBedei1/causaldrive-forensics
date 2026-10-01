# Reconstruction report - S06/run_0_b_rear_first

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.15 s | 143 | 9 | 11 | 1 | A:e06 @ 6.00 s |
| B | 14.15 s | 143 | 13 | 23 | 1 | B:e07 @ 4.60 s, B:e13 @ 6.00 s |
| C | 14.15 s | 143 | 7 | 7 | 0 | C:e07 @ 4.60 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 6.00 | -6.00 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 6.00 | -6.00 | reported the reference collision collision_001 |
| C | ALIGNED | C:e07 | 4.60 | -6.00 | shares collision_002 with B, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31488.29 vs 31488.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 21812.15 vs 21812.15 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 5.95 s before the matched collision<br>lost 1.45 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 19.4 m -> 19.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.04 m/s over 1.5 s |
| B:track_001 | C | ASSOCIATED | 0.97 | B and C both reported collision_002 at 4.60 s (peak impulse 21812.15 vs 21812.15 N*s)<br>tracked for 4.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.39 m/s over 3.0 s<br>range at the contact 0.09 m<br>the only track of B compatible with the contact<br>collision_001 with A at 6.00 s: not compatible (track speed disagrees with A's own speed: RMSE 10.92 m/s over 3.0 s (> 1.50)) |

## Global graph

27 nodes, 41 edges; 2 merged node(s): g18 COLLISION(B,C) from B:e07 + C:e07, g24 COLLISION(A,B) from A:e06 + B:e13.

### Event sequence (global time)

- `-6.00` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,C)
- `-5.95` TRACK_APPEARED_FRONT(A,A:track_001)
- `-5.55` CLOSING_START(A,A:track_001)
- `-4.90` CLOSING_START(B,C)
- `-4.40` CLOSING_END(A,A:track_001)
- `-3.90` CLOSING_END(B,C)
- `-3.60` SPEED_LIMIT_EXCEEDED_START(C)
- `-3.05` BRAKE_START(C)
- `-2.95` SPEED_LIMIT_EXCEEDED_END(C)
- `-2.80` CLOSING_START(B,C)
- `-2.25` CRITICAL_TTC_START(B,C)
- `-1.95` MOVING_END(C); STOP_START(C)
- `-1.45` TRACK_LOST(A,A:track_001)
- `-1.40` COLLISION(B,C)
- `-1.35` CRITICAL_TTC_END(B,C); CLOSING_END(B,C); BRAKE_START(B)
- `-1.25` MOVING_END(B); STOP_START(B)
- `+0.00` COLLISION(A,B)
- `+0.05` BRAKE_START(A)
- `+0.20` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 6.00 s before the reference collision, A started moving (already the case when first observed).
- 6.00 s before the reference collision, B started moving (already the case when first observed).
- 6.00 s before the reference collision, C started moving (already the case when first observed).
- 6.00 s before the reference collision, B's radar started tracking C, which appeared in front of it.
- 5.95 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 5.55 s before the reference collision, A observed unidentified object A:track_001 start closing in.
- 4.90 s before the reference collision, B observed C start closing in.
- 4.40 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- 3.90 s before the reference collision, B observed C stop closing in.
- 3.60 s before the reference collision, C began exceeding the speed limit.
- 3.05 s before the reference collision, C started braking.
- 2.95 s before the reference collision, C returned within the speed limit.
- 2.80 s before the reference collision, B observed C start closing in.
- 2.25 s before the reference collision, B's time-to-contact with C became critical.
- 1.95 s before the reference collision, C stopped moving.
- 1.95 s before the reference collision, C came to a stop.
- 1.45 s before the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the reference collision, B and C both recorded this same collision (peak impulses B: 21812, C: 21812 N*s).
- 1.35 s before the reference collision, B's time-to-contact with C stopped being critical.
- 1.35 s before the reference collision, B observed C stop closing in.
- 1.35 s before the reference collision, B started braking.
- 1.25 s before the reference collision, B stopped moving.
- 1.25 s before the reference collision, B came to a stop.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 31488, B: 31488 N*s).
- 0.05 s after the reference collision, A started braking.
- 0.20 s after the reference collision, A stopped moving.
- 0.20 s after the reference collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- B's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 4.60 (+0.85 s) [local times; t_global: critical_ttc_start -2.25, collision -1.40]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,C)
- MOVING_END(C); STOP_START(C)
- CRITICAL_TTC_END(B,C); CLOSING_END(B,C); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e07 (t = 6.05 s)
- STOP, since A:e09 (t = 6.20 s)
B:
- BRAKE, since B:e10 (t = 4.65 s)
- STOP, since B:e12 (t = 4.75 s)
C:
- BRAKE, since C:e03 (t = 2.95 s)
- STOP, since C:e06 (t = 4.05 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e06 at 6.00 s (local): ego: MOVING; track lost, states UNKNOWN: track_001
- B B:e07 at 4.60 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e13 at 6.00 s (local): ego: STOP, BRAKE; track_001: IN_EGO_PATH
- C C:e07 at 4.60 s (local): ego: STOP, BRAKE

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 4.55 s (A:e05): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_001 stays anonymous: lost 1.45 s before the matched collision (window 0.50 s); not approaching before the contact: range 19.4 m -> 19.8 m over the last 1.0 s.
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
