# Reconstruction report - S16/run_0_consequential

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 27 | 55 | 6 | A:e03 @ 5.15 s, A:e21 @ 5.90 s |
| B | 9.95 s | 101 | 14 | 24 | 1 | B:e10 @ 5.15 s |
| C | 9.95 s | 101 | 9 | 13 | 0 | C:e04 @ 5.90 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e03 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | ALIGNED | C:e04 | 5.90 | -5.15 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 4.7 m -> 0.6 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 1.66 m/s over 0.8 s (> 1.50)<br>range at the contact 0.56 m<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 15.89 m (beyond 3.50 m: confidence factor 0.00)<br>collision_002 with C at 5.90 s: not compatible (tracked for 0.75 s before the matched collision (needs 1.00 s); not approaching before the contact: range 15.9 m -> 16.6 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 7.92 m/s over 0.8 s (> 1.50)) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 13.50 m (beyond 3.50 m: confidence factor 0.00)<br>collision_002 with C at 5.90 s: not compatible (tracked for 0.75 s before the matched collision (needs 1.00 s); not approaching before the contact: range 13.5 m -> 14.4 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 6.03 m/s over 0.8 s (> 1.50)) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 21.7 m -> 19.7 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.45 m/s over 0.8 s<br>range at the contact 19.42 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 14.2 m -> 15.1 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 5.31 m/s over 0.4 s (> 1.50)<br>range at the contact 14.23 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.35 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 19.0 m -> 19.9 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 2.83 m/s over 0.4 s (> 1.50)<br>range at the contact 19.02 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.35 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 4.0 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.51 m/s over 3.0 s<br>range at the contact 0.59 m<br>the only track of B compatible with the contact |

## Global graph

48 nodes, 121 edges; 2 merged node(s): g15 COLLISION(A,B) from A:e03 + B:e10, g37 COLLISION(A,C) from A:e21 + C:e04.

### Event sequence (global time)

- `-5.15` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
- `-4.85` MOVING_END(C); STOP_START(C)
- `-4.45` CLOSING_START(B,A)
- `-4.40` CRITICAL_TTC_START(B,A)
- `-3.75` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-1.20` BRAKE_START(A)
- `-0.90` CLOSING_START(B,A)
- `-0.70` CRITICAL_TTC_START(B,A)
- `-0.40` BRAKE_START(B)
- `+0.00` COLLISION(A,B); TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_RIGHT(A,A:track_002); TRACK_APPEARED_RIGHT(A,A:track_003); TRACK_APPEARED_RIGHT(A,A:track_004); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CRITICAL_TTC_START(A,A:track_001)
- `+0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
- `+0.25` TURN_LEFT_START(A)
- `+0.30` CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003)
- `+0.35` TRACK_APPEARED_RIGHT(A,A:track_005); TRACK_APPEARED_RIGHT(A,A:track_006)
- `+0.45` MOVING_END(B); STOP_START(B)
- `+0.55` CLOSING_END(A,A:track_004); EGO_PATH_ENTRY(A,A:track_001)
- `+0.75` COLLISION(A,C); STOP_END(C); MOVING_START(C)
- `+0.80` BRAKE_START(C); TRACK_LOST(A,A:track_005)
- `+0.85` CRITICAL_TTC_END(A,A:track_001); TURN_LEFT_END(A)
- `+0.90` CLOSING_END(A,A:track_001); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### What happened, in plain language

- 5.15 s before the reference collision, A started moving (already the case when first observed).
- 5.15 s before the reference collision, B started moving (already the case when first observed).
- 5.15 s before the reference collision, C started moving (already the case when first observed).
- 5.15 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 4.85 s before the reference collision, C stopped moving.
- 4.85 s before the reference collision, C came to a stop.
- 4.45 s before the reference collision, B observed A start closing in.
- 4.40 s before the reference collision, B's time-to-contact with A became critical.
- 3.75 s before the reference collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the reference collision, B observed A stop closing in.
- 1.20 s before the reference collision, A started braking.
- 0.90 s before the reference collision, B observed A start closing in.
- 0.70 s before the reference collision, B's time-to-contact with A became critical.
- 0.40 s before the reference collision, B started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- At the reference collision, A's radar started tracking unidentified object A:track_002, which appeared on its right.
- At the reference collision, A's radar started tracking unidentified object A:track_003, which appeared on its right.
- At the reference collision, A's radar started tracking unidentified object A:track_004, which appeared on its right.
- At the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- At the reference collision, A's time-to-contact with unidentified object A:track_001 became critical (already the case when first observed).
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the brake.
- 0.25 s after the reference collision, A started turning left.
- 0.30 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.30 s after the reference collision, A observed unidentified object A:track_003 stop closing in.
- 0.35 s after the reference collision, A's radar started tracking unidentified object A:track_005, which appeared on its right.
- 0.35 s after the reference collision, A's radar started tracking unidentified object A:track_006, which appeared on its right.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.75 s after the reference collision, A and C both recorded this same collision (peak impulses A: 2696, C: 2696 N*s).
- 0.75 s after the reference collision, C left its stop.
- 0.75 s after the reference collision, C started moving.
- 0.80 s after the reference collision, C started braking.
- 0.80 s after the reference collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s after the reference collision, A stopped turning left.
- 0.90 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.90 s after the reference collision, A stopped moving.
- 0.90 s after the reference collision, C stopped moving.
- 0.90 s after the reference collision, A came to a stop.
- 0.90 s after the reference collision, C came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 5.15, COLLISION 5.15 (+0.00 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.55 s) [local times; t_global: critical_ttc_start +0.00, ego_path_entry +0.55, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
- MOVING_END(C); STOP_START(C)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- COLLISION(A,B); TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_RIGHT(A,A:track_002); TRACK_APPEARED_RIGHT(A,A:track_003); TRACK_APPEARED_RIGHT(A,A:track_004); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CRITICAL_TTC_START(A,A:track_001)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
- CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003)
- TRACK_APPEARED_RIGHT(A,A:track_005); TRACK_APPEARED_RIGHT(A,A:track_006)
- MOVING_END(B); STOP_START(B)
- CLOSING_END(A,A:track_004); EGO_PATH_ENTRY(A,A:track_001)
- COLLISION(A,C); STOP_END(C); MOVING_START(C)
- BRAKE_START(C); TRACK_LOST(A,A:track_005)
- CRITICAL_TTC_END(A,A:track_001); TURN_LEFT_END(A)
- CLOSING_END(A,A:track_001); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### States still active when observation ended

A:
- EGO_PATH of track_001, since A:e20 (t = 5.70 s)
- STOP, since A:e27 (t = 6.05 s)
B:
- BRAKE, since B:e09 (t = 4.75 s)
- STOP, since B:e14 (t = 5.60 s)
C:
- BRAKE, since C:e07 (t = 5.95 s)
- STOP, since C:e09 (t = 6.05 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e03 at 5.15 s (local): ego: MOVING, BRAKE
- A A:e21 at 5.90 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_002: no active state; track_003: no active state; track_004: no active state; track_005: no active state; track_006: no active state
- B B:e10 at 5.15 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- C C:e04 at 5.90 s (local): ego: STOP

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_005
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_001 stays anonymous: collision_002 with C: tracked for 0.75 s before the matched collision (needs 1.00 s); collision_002 with C: track speed disagrees with C's own speed: RMSE 1.66 m/s over 0.8 s (> 1.50).
- A:track_002 stays anonymous: collision_001 with B: tracked for 0.00 s before the matched collision (needs 1.00 s); collision_001 with B: range trend before the contact not measurable; collision_001 with B: speed not comparable with B's own speed before the collision.
- A:track_003 stays anonymous: collision_001 with B: tracked for 0.00 s before the matched collision (needs 1.00 s); collision_001 with B: range trend before the contact not measurable; collision_001 with B: speed not comparable with B's own speed before the collision.
- A:track_004 stays anonymous: collision_002 with C: tracked for 0.75 s before the matched collision (needs 1.00 s).
- A:track_005 stays anonymous: collision_002 with C: tracked for 0.40 s before the matched collision (needs 1.00 s); collision_002 with C: not approaching before the contact: range 14.2 m -> 15.1 m over the last 1.0 s; collision_002 with C: track speed disagrees with C's own speed: RMSE 5.31 m/s over 0.4 s (> 1.50).
- A:track_006 stays anonymous: collision_002 with C: tracked for 0.40 s before the matched collision (needs 1.00 s); collision_002 with C: not approaching before the contact: range 19.0 m -> 19.9 m over the last 1.0 s; collision_002 with C: track speed disagrees with C's own speed: RMSE 2.83 m/s over 0.4 s (> 1.50).
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
