# Reconstruction report - S13/run_0_cut_in

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 13 | 22 | 1 | A:e08 @ 5.25 s |
| B | 9.95 s | 101 | 22 | 95 | 5 | B:e03 @ 5.25 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 3184.37 vs 3184.37 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 5.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 5.6 m -> 1.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.33 m/s over 3.0 s<br>range at the contact 1.28 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Global graph

34 nodes, 138 edges; 1 merged node(s): g10 COLLISION(A,B) from A:e08 + B:e03.

### Event sequence (global time)

- `-5.25` MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-4.45` BRAKE_START(B)
- `-2.40` BRAKE_START(A)
- `-1.70` CUT_IN_FROM_LEFT_START(A,B)
- `-1.30` CRITICAL_TTC_START(A,B)
- `-0.35` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B)
- `+0.05` CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.20` TURN_RIGHT_START(B)
- `+0.70` TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- `+1.15` CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A)
- `+1.20` MOVING_END(B); STOP_START(B)
- `+1.40` CUT_IN_FROM_LEFT_END(A,B)

### What happened, in plain language

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 5.25 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 5.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 4.45 s before the matched collision, B started braking.
- 2.40 s before the matched collision, A started braking.
- 1.70 s before the matched collision, A observed B cutting in from the left.
- 1.30 s before the matched collision, A's time-to-contact with B became critical.
- 0.35 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 3184, B: 3184 N*s).
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.20 s after the matched collision, B started turning right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 0.70 s after the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 1.15 s after the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 1.15 s after the matched collision, B stopped turning right.
- 1.15 s after the matched collision, A stopped moving.
- 1.15 s after the matched collision, A came to a stop.
- 1.20 s after the matched collision, B stopped moving.
- 1.20 s after the matched collision, B came to a stop.
- 1.40 s after the matched collision, A observed B's cut-in from the left settle.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 3.55 < CRITICAL_TTC_START 3.95 (+0.40 s) < COLLISION 5.25 (+1.30 s); EGO_PATH_ENTRY 4.90 after critical TTC (+0.95 s) [local times; t_global: cut_in -1.70, critical_ttc_start -1.30, ego_path_entry -0.35, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A)
- MOVING_END(B); STOP_START(B)

### States still active when observation ended

A:
- BRAKE, since A:e04 (t = 2.85 s)
- EGO_PATH of track_001, since A:e07 (t = 4.90 s)
- STOP, since A:e12 (t = 6.40 s)
B:
- BRAKE, since B:e02 (t = 0.80 s)
- STOP, since B:e22 (t = 6.45 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e08 at 5.25 s (local): ego: MOVING, BRAKE; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT
- B B:e03 at 5.25 s (local): ego: MOVING, BRAKE

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- no track was lost

## Uncertainty and limitations

- B:track_001 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_002 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
