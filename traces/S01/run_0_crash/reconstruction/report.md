# Reconstruction report - S01/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 12 | 21 | 1 | A:e08 @ 6.50 s |
| B | 11.95 s | 121 | 10 | 14 | 1 | B:e10 @ 6.50 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 0.32 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.13 m/s over 3.0 s<br>clearance at the contact 0.58 m<br>the only track of B compatible with the contact |

## Global graph

21 nodes, 36 edges; 1 merged node(s): g17 COLLISION(A,B) from A:e08 + B:e10.

### Event sequence (global time)

- `-6.50` MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_REAR(B,A)
- `-6.05` CLOSING_START(A,B)
- `-6.00` CLOSING_START(B,A)
- `-4.85` CLOSING_END(A,B); CLOSING_END(B,A)
- `-2.55` BRAKE_START(B)
- `-2.30` CLOSING_START(A,B)
- `-2.25` CLOSING_START(B,A)
- `-1.50` CRITICAL_TTC_START(A,B)
- `-1.35` MOVING_END(B); STOP_START(B)
- `-0.95` BRAKE_START(A)
- `-0.05` TRACK_LOST(B,A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.05` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 6.50 s before the reference collision, A started moving (already the case when first observed).
- 6.50 s before the reference collision, B started moving (already the case when first observed).
- 6.50 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.50 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 6.05 s before the reference collision, A observed B start closing in.
- 6.00 s before the reference collision, B observed A start closing in.
- 4.85 s before the reference collision, A observed B stop closing in.
- 4.85 s before the reference collision, B observed A stop closing in.
- 2.55 s before the reference collision, B started braking.
- 2.30 s before the reference collision, A observed B start closing in.
- 2.25 s before the reference collision, B observed A start closing in.
- 1.50 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B stopped moving.
- 1.35 s before the reference collision, B came to a stop.
- 0.95 s before the reference collision, A started braking.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A stopped moving.
- 0.05 s after the reference collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 5.00, COLLISION with B 6.50 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_REAR(B,A)
- CLOSING_END(A,B); CLOSING_END(B,A)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e07 (t = 5.55 s)
- STOP, since A:e12 (t = 6.55 s)
B:
- BRAKE, since B:e05 (t = 3.95 s)
- CLOSING of track_001, since B:e06 (t = 4.25 s); the track was lost at 6.45 s
- STOP, since B:e08 (t = 5.15 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e08 at 6.50 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e10 at 6.50 s (local): ego: STOP, BRAKE; track lost, states UNKNOWN: track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- track_001 at 6.45 s (B:e09): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

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
