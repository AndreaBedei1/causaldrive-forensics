# Reconstruction report - S01/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 12 | 21 | 1 | A:e08 @ 6.50 s |
| B | 11.95 s | 121 | 5 | 5 | 0 | B:e05 @ 6.50 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e05 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.5 m -> 0.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.24 m/s over 3.0 s<br>range at the contact 0.77 m<br>the only track of A compatible with the contact |

## Global graph

16 nodes, 26 edges; 1 merged node(s): g12 COLLISION(A,B) from A:e08 + B:e05.

### Event sequence (global time)

- `-6.50` MOVING_START(A); MOVING_START(B)
- `-6.40` TRACK_APPEARED_FRONT(A,B)
- `-6.05` CLOSING_START(A,B)
- `-4.90` CLOSING_END(A,B)
- `-2.55` BRAKE_START(B)
- `-2.25` CLOSING_START(A,B)
- `-1.50` CRITICAL_TTC_START(A,B)
- `-1.35` MOVING_END(B); STOP_START(B)
- `-0.95` BRAKE_START(A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.05` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 6.50 s before the matched collision, A started moving (already the case when first observed).
- 6.50 s before the matched collision, B started moving (already the case when first observed).
- 6.40 s before the matched collision, A's radar started tracking B, which appeared in front of it.
- 6.05 s before the matched collision, A observed B start closing in.
- 4.90 s before the matched collision, A observed B stop closing in.
- 2.55 s before the matched collision, B started braking.
- 2.25 s before the matched collision, A observed B start closing in.
- 1.50 s before the matched collision, A's time-to-contact with B became critical.
- 1.35 s before the matched collision, B stopped moving.
- 1.35 s before the matched collision, B came to a stop.
- 0.95 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A stopped moving.
- 0.05 s after the matched collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 5.00, COLLISION 6.50 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e07 (t = 5.55 s)
- STOP, since A:e12 (t = 6.55 s)
B:
- BRAKE, since B:e02 (t = 3.95 s)
- STOP, since B:e04 (t = 5.15 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e08 at 6.50 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e05 at 6.50 s (local): ego: STOP, BRAKE

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost

## Uncertainty and limitations

- B built no radar track: nothing moving stayed in its forward radar view long enough, so B has no perception of the others.
- Global time rests on one collision anchor and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from t_global = 0.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5
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
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
