# Reconstruction report - S07/run_0_occluded

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.15 s | 143 | 12 | 19 | 1 | A:e07 @ 5.70 s |
| B | 14.15 s | 143 | 12 | 19 | 1 | B:e12 @ 5.70 s |
| C | 14.15 s | 143 | 9 | 9 | 0 | none |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.70 | -5.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.70 | -5.70 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31406.82 vs 31406.82 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 13.5 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.29 m/s over 3.0 s<br>range at the contact 0.74 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.0 m -> 10.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 10.21 m/s over 3.0 s (> 1.50)<br>range at the contact 10.79 m (beyond 3.50 m: confidence factor 0.05) |

## Global graph

32 nodes, 45 edges; 1 merged node(s): g18 COLLISION(A,B) from A:e07 + B:e12.

### Event sequence (global time)

- `-5.70` MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001)
- `-5.65` TRACK_APPEARED_FRONT(A,B)
- `-5.25` CLOSING_START(A,B)
- `-4.60` CLOSING_START(B,B:track_001)
- `-4.10` CLOSING_END(A,B)
- `-3.60` CLOSING_END(B,B:track_001)
- `-2.45` CLOSING_START(B,B:track_001)
- `-2.05` BRAKE_START(B)
- `-1.80` CLOSING_START(A,B)
- `-1.75` CRITICAL_TTC_START(B,B:track_001)
- `-1.10` CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
- `-0.85` CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.05` BRAKE_START(A)
- `+0.15` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 5.70 s before the matched collision, A started moving (already the case when first observed).
- 5.70 s before the matched collision, B started moving (already the case when first observed).
- 5.70 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.65 s before the matched collision, A's radar started tracking B, which appeared in front of it.
- 5.25 s before the matched collision, A observed B start closing in.
- 4.60 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.10 s before the matched collision, A observed B stop closing in.
- 3.60 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.45 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.05 s before the matched collision, B started braking.
- 1.80 s before the matched collision, A observed B start closing in.
- 1.75 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.10 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.10 s before the matched collision, A's time-to-contact with B became critical.
- 0.85 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 0.85 s before the matched collision, B stopped moving.
- 0.85 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31407, B: 31407 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A started braking.
- 0.15 s after the matched collision, A stopped moving.
- 0.15 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 3.10 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 12.95 s) C released the brake.
- (unaligned, C local time 13.75 s) C left its stop.
- (unaligned, C local time 13.75 s) C started moving.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.60, COLLISION 5.70 (+1.10 s) [local times; t_global: critical_ttc_start -1.10, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.95, COLLISION 5.70 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001)
- CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
- CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e10 (t = 5.75 s)
- STOP, since A:e12 (t = 5.85 s)
B:
- BRAKE, since B:e06 (t = 3.65 s)
- STOP, since B:e11 (t = 4.85 s)
C:
- MOVING, since C:e09 (t = 13.75 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e07 at 5.70 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e12 at 5.70 s (local): ego: STOP, BRAKE; track_001: IN_EGO_PATH

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 10.21 m/s over 3.0 s (> 1.50).
- C is UNALIGNED: it recorded no collision to anchor on.
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
