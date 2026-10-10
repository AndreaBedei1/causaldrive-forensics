# Reconstruction report - S17/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 10.95 s | 111 | 22 | 40 | 2 | A:e14 @ 4.95 s |
| B | 10.95 s | 111 | 19 | 31 | 3 | B:e09 @ 4.95 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e14 | 4.95 | -4.95 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 4.95 | -4.95 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1576.92 vs 1576.92 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.9 m -> 1.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.90 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.03 m |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s<br>clearance at the contact 0.10 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.93 | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.2 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 0.23 m<br>the only compatible track of B touching it at the contact (clearance 0.23 m; track_002 at 4.94 m) |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 6.8 m -> 4.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.23 m/s over 3.0 s<br>clearance at the contact 4.94 m (beyond 3.50 m: confidence factor 0.89)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Global graph

40 nodes, 79 edges; 1 merged node(s): g22 COLLISION(A,B) from A:e14 + B:e09.

### Event sequence (global time)

- `-4.95` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_001); CLOSING_START(B,B:track_002)
- `-2.35` CRITICAL_TTC_START(A,A:track_001)
- `-2.20` CUT_IN_FROM_RIGHT_START(A,A:track_001)
- `-1.60` EGO_PATH_ENTRY(A,A:track_001)
- `-1.15` CRITICAL_TTC_START(A,B)
- `-0.85` CUT_IN_FROM_RIGHT_END(A,A:track_001)
- `-0.80` CRITICAL_TTC_START(B,A)
- `-0.75` CLOSING_START(A,B)
- `-0.70` CLOSING_START(B,A)
- `-0.40` CLOSING_END(A,A:track_001)
- `-0.30` CRITICAL_TTC_END(A,A:track_001)
- `-0.05` CRITICAL_TTC_END(B,A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- `+0.20` CLOSING_END(B,B:track_002)
- `+0.25` EGO_PATH_EXIT(A,A:track_001)
- `+0.75` TRACK_LOST(B,B:track_002)
- `+1.00` MOVING_END(B); STOP_START(B)
- `+1.10` MOVING_END(A); STOP_START(A)
- `+1.30` EGO_PATH_ENTRY(B,A)
- `+1.45` TRACK_APPEARED_RIGHT(B,B:track_003)
- `+2.05` TRACK_LOST(B,B:track_003)
- `+2.50` TRACK_LOST(A,A:track_001)

### What happened, in plain language

- 4.95 s before the reference collision, A started moving (already the case when first observed).
- 4.95 s before the reference collision, B started moving (already the case when first observed).
- 4.95 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.95 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 4.95 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.95 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 2.35 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 2.20 s before the reference collision, A observed unidentified object A:track_001 cutting in from the right.
- 1.60 s before the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 1.15 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, A observed unidentified object A:track_001's cut-in from the right settle.
- 0.80 s before the reference collision, B's time-to-contact with A became critical.
- 0.75 s before the reference collision, A observed B start closing in.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.40 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.30 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.05 s before the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1577, B: 1577 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.25 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.75 s after the reference collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, B stopped moving.
- 1.00 s after the reference collision, B came to a stop.
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, B observed A enter its forward path corridor.
- 1.45 s after the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 2.05 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 2.50 s after the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): critical TTC already active before the cut-in: CRITICAL_TTC_START 2.60 <= CUT_IN_FROM_RIGHT_START 2.75 (+0.15 s); EGO_PATH_ENTRY 3.35 after critical TTC (+0.75 s) [local times; t_global: cut_in -2.20, critical_ttc_start -2.35, ego_path_entry -1.60, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 3.80, COLLISION with B 4.95 (+1.15 s) [local times; t_global: critical_ttc_start -1.15, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.15, COLLISION with A 4.95 (+0.80 s); EGO_PATH_ENTRY 6.25 after critical TTC (+2.10 s) [local times; t_global: critical_ttc_start -0.80, ego_path_entry +1.30, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_001); CLOSING_START(B,B:track_002)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A)
- THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e18 (t = 5.00 s)
- STOP, since A:e21 (t = 6.05 s)
B:
- BRAKE, since B:e12 (t = 5.00 s)
- STOP, since B:e16 (t = 5.95 s)
- EGO_PATH of track_001, since B:e17 (t = 6.25 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e14 at 4.95 s (local): ego: MOVING, THROTTLE; track_001: IN_EGO_PATH; track_002: CLOSING, CRITICAL_TTC
- B B:e09 at 4.95 s (local): ego: MOVING, THROTTLE; track_001: CLOSING; track_002: CLOSING

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_001
B:
- lost with no state active: track_002, track_003

## Uncertainty and limitations

- A:track_001 stays anonymous: track speed disagrees with B's own speed: RMSE 1.90 m/s over 3.0 s (> 1.50).
- B:track_002 stays anonymous: ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002).
- B:track_003 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
