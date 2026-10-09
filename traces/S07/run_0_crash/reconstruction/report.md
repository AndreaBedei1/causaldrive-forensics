# Reconstruction report - S07/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.65 s | 138 | 12 | 22 | 1 | A:e08 @ 5.90 s |
| B | 13.65 s | 138 | 12 | 18 | 1 | B:e12 @ 5.90 s |
| C | 13.65 s | 138 | 6 | 8 | 0 | none |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 22183.35 vs 22183.35 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 22183.35 vs 22183.35 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 22183.35 vs 22183.35 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.2 m -> 14.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.87 m/s over 3.0 s (> 1.50)<br>clearance at the contact 14.08 m (beyond 3.50 m: confidence factor 0.00) |

## Global graph

29 nodes, 42 edges; 1 merged node(s): g19 COLLISION(A,B) from A:e08 + B:e12.

### Event sequence (global time)

- `-5.90` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001)
- `-5.40` CRITICAL_TTC_START(A,B)
- `-2.70` CLOSING_START(B,B:track_001)
- `-2.50` CRITICAL_TTC_START(B,B:track_001)
- `-2.25` THROTTLE_END(B); BRAKE_START(B)
- `-2.05` CLOSING_START(A,B)
- `-1.55` CRITICAL_TTC_END(B,B:track_001)
- `-1.05` CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
- `-0.65` THROTTLE_END(A); BRAKE_START(A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.10` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 5.90 s before the reference collision, A started moving (already the case when first observed).
- 5.90 s before the reference collision, B started moving (already the case when first observed).
- 5.90 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.90 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.90 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.40 s before the reference collision, A's time-to-contact with B became critical.
- 2.70 s before the reference collision, B observed unidentified object B:track_001 start closing in.
- 2.50 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 2.25 s before the reference collision, B released the accelerator.
- 2.25 s before the reference collision, B started braking.
- 2.05 s before the reference collision, A observed B start closing in.
- 1.55 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.05 s before the reference collision, B observed unidentified object B:track_001 stop closing in.
- 1.05 s before the reference collision, B stopped moving.
- 1.05 s before the reference collision, B came to a stop.
- 0.65 s before the reference collision, A released the accelerator.
- 0.65 s before the reference collision, A started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 22183, B: 22183 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.10 s after the reference collision, A stopped moving.
- 0.10 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C pressed the accelerator (already the case when first observed).
- (unaligned, C local time 2.95 s) C released the accelerator.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 4.35 s) C stopped moving.
- (unaligned, C local time 4.35 s) C came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 0.50, COLLISION with B 5.90 (+5.40 s) [local times; t_global: critical_ttc_start -5.40, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.40, COLLISION 5.90 (+2.50 s) [local times; t_global: critical_ttc_start -2.50, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001)
- THROTTLE_END(B); BRAKE_START(B)
- CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
- THROTTLE_END(A); BRAKE_START(A)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e07 (t = 5.25 s)
- STOP, since A:e12 (t = 6.00 s)
B:
- BRAKE, since B:e07 (t = 3.65 s)
- STOP, since B:e11 (t = 4.85 s)
C:
- BRAKE, since C:e04 (t = 2.95 s)
- STOP, since C:e06 (t = 4.35 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e08 at 5.90 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e12 at 5.90 s (local): ego: STOP, BRAKE; track_001: IN_EGO_PATH

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its radar view long enough, so C has no perception of the others.
- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 9.87 m/s over 3.0 s (> 1.50).
- C is UNALIGNED: it recorded no collision to anchor on.
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
    "min_new_impact_impulse": 1000.0,
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
    "acceleration_std_mps2": 6.0,
    "min_slowdown_returns": 3
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "throttle_on_threshold": 0.1,
    "throttle_off_threshold": 0.05,
    "throttle_release_debounce_s": 0.2,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_lateral_margin_m": 0.3,
    "critical_release_ratio": 0.75,
    "prediction_horizon_s": 6.0,
    "prediction_time_step_s": 0.05,
    "target_length_m": 4.6,
    "target_width_m": 1.9,
    "target_braking_min_mps2": 1.0,
    "critical_min_track_age_s": 0.5,
    "critical_time_gap_table": [
      [
        7.2,
        1.0
      ],
      [
        10.0,
        1.1
      ],
      [
        20.0,
        1.2
      ],
      [
        30.0,
        1.3
      ],
      [
        40.0,
        1.4
      ],
      [
        50.0,
        1.5
      ],
      [
        60.0,
        1.6
      ]
    ],
    "critical_min_following_distance_m": 2.0,
    "critical_lead_deceleration_mps2": 6.0,
    "critical_forward_min_speed_mps": 1.0,
    "critical_front_lateral_margin_m": 1.0,
    "critical_front_lateral_speed_mps": 0.3,
    "critical_forward_release_factor": 1.1,
    "occlusion_margin_m": 0.5,
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
    "cut_in_preentry_margin_m": 1.0,
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
    "speed_consistency_mps": 1.5,
    "touching_clearance_m": 1.0,
    "rival_clearance_m": 2.0
  }
}
```
