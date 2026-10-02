# Reconstruction report - S08/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 153 | 16 | 27 | 2 | A:e11 @ 4.25 s |
| B | 15.15 s | 153 | 16 | 32 | 2 | B:e08 @ 4.25 s |
| C | 15.15 s | 153 | 17 | 34 | 2 | none |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 4.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.0 m -> 10.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.95 m/s over 3.0 s (> 1.50)<br>clearance at the contact 10.47 m (beyond 3.50 m: confidence factor 0.07) |
| A:track_002 | B | ASSOCIATED | 0.88 | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 3.00 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.3 m -> 1.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 1.46 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.4 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.3 m -> 11.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.99 m/s over 2.1 s (> 1.50)<br>clearance at the contact 11.74 m (beyond 3.50 m: confidence factor 0.02) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

48 nodes, 78 edges; 1 merged node(s): g18 COLLISION(A,B) from A:e11 + B:e08.

### Event sequence (global time)

- `-4.25` MOVING_START(A); MOVING_START(B)
- `-4.20` TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- `-3.00` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- `-2.95` TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- `-2.10` TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_002)
- `-2.05` CRITICAL_TTC_START(A,A:track_001)
- `-1.90` CRITICAL_TTC_START(B,A)
- `-1.80` CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_002)
- `-1.50` CRITICAL_TTC_END(A,A:track_001)
- `-0.75` CRITICAL_TTC_START(A,A:track_001)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(B,B:track_002); EGO_PATH_ENTRY(B,A)
- `+0.05` BRAKE_START(A); BRAKE_START(B)
- `+0.25` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.30` CLOSING_END(B,B:track_002); MOVING_END(B); STOP_START(B)
- `+0.50` CRITICAL_TTC_END(A,A:track_001)
- `+0.65` CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 4.25 s before the reference collision, A started moving (already the case when first observed).
- 4.25 s before the reference collision, B started moving (already the case when first observed).
- 4.20 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 4.20 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 3.00 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 3.00 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.95 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.95 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.10 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 2.10 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.90 s before the reference collision, B's time-to-contact with A became critical.
- 1.80 s before the reference collision, A's time-to-contact with B became critical.
- 1.80 s before the reference collision, B's time-to-contact with unidentified object B:track_002 became critical.
- 1.50 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.75 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the reference collision, B's time-to-contact with unidentified object B:track_002 stopped being critical.
- At the reference collision, B observed A enter its forward path corridor.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.25 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the reference collision, B observed A stop closing in.
- 0.30 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.30 s after the reference collision, B stopped moving.
- 0.30 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.65 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 2.25 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.80 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.85 s) C stopped moving.
- (unaligned, C local time 2.85 s) C came to a stop.
- (unaligned, C local time 3.20 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 3.55 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.55 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 4.90 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 14.35 s) C released the brake.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 2.20, COLLISION 4.25 (+2.05 s) [local times; t_global: critical_ttc_start -2.05, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.45, COLLISION with B 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.35, COLLISION with A 4.25 (+1.90 s); EGO_PATH_ENTRY 4.25 after critical TTC (+1.90 s) [local times; t_global: critical_ttc_start -1.90, ego_path_entry +0.00, collision +0.00]
- B's track_002 (unidentified B:track_002): CRITICAL_TTC_START 2.45, COLLISION 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- C's track_001 (unidentified C:track_001): CRITICAL_TTC_START 2.25 [local times]
- C's track_002 (unidentified C:track_002): CRITICAL_TTC_START 2.80 [local times]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_002)
- CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_002)
- COLLISION(A,B); CRITICAL_TTC_END(B,B:track_002); EGO_PATH_ENTRY(B,A)
- BRAKE_START(A); BRAKE_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- CLOSING_END(B,B:track_002); MOVING_END(B); STOP_START(B)
- CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e05 (t = 1.25 s); the track was lost at 4.20 s
- CRITICAL_TTC of track_002, since A:e07 (t = 2.45 s); the track was lost at 4.20 s
- BRAKE, since A:e12 (t = 4.30 s)
- STOP, since A:e16 (t = 4.90 s)
B:
- EGO_PATH of track_001, since B:e10 (t = 4.25 s)
- BRAKE, since B:e11 (t = 4.30 s)
- STOP, since B:e16 (t = 4.55 s)
C:
- STOP, since C:e10 (t = 2.85 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e11 at 4.25 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; track lost, states UNKNOWN: track_002
- B B:e08 at 4.25 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; track_002: CLOSING, CRITICAL_TTC

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 4.20 s (A:e10): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- A:track_001 stays anonymous: track speed disagrees with B's own speed: RMSE 8.95 m/s over 3.0 s (> 1.50).
- B:track_002 stays anonymous: track speed disagrees with A's own speed: RMSE 7.99 m/s over 2.1 s (> 1.50).
- C:track_001 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_002 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
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
