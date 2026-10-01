# Reconstruction report - S02/run_0_critical_before_cut_in

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.45 s | 116 | 15 | 21 | 1 | A:e12 @ 3.85 s |
| B | 11.45 s | 116 | 7 | 6 | 0 | B:e04 @ 3.85 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 3.85 | -3.85 | reported the reference collision collision_001 |
| B | ALIGNED | B:e04 | 3.85 | -3.85 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 241.17 vs 241.17 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.67 | A and B both reported collision_001 (peak impulse 241.17 vs 241.17 N*s)<br>tracked for 3.85 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 0.50 s)<br>approaching before the contact: range 3.3 m -> 0.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.34 m/s over 2.9 s<br>range at the contact 0.92 m<br>the only track of A compatible with the contact |

## Global graph

21 nodes, 32 edges; 1 merged node(s): g15 COLLISION(A,B) from A:e12 + B:e04.

### Event sequence (global time)

- `-3.85` MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-3.10` CRITICAL_TTC_START(A,B)
- `-2.60` CRITICAL_TTC_END(A,B)
- `-2.45` BRAKE_START(B)
- `-2.30` BRAKE_END(B); CRITICAL_TTC_START(A,B)
- `-1.40` BRAKE_START(A)
- `-1.15` CUT_IN_FROM_LEFT_START(A,B)
- `-0.65` BRAKE_END(A)
- `-0.45` EGO_PATH_ENTRY(A,B)
- `-0.15` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B)
- `+0.05` BRAKE_START(A); BRAKE_START(B)
- `+0.50` MOVING_END(B); STOP_START(B)
- `+0.60` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 3.85 s before the reference collision, A started moving (already the case when first observed).
- 3.85 s before the reference collision, B started moving (already the case when first observed).
- 3.85 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 3.85 s before the reference collision, A observed B start closing in (already the case when first observed).
- 3.10 s before the reference collision, A's time-to-contact with B became critical.
- 2.60 s before the reference collision, A's time-to-contact with B stopped being critical.
- 2.45 s before the reference collision, B started braking.
- 2.30 s before the reference collision, B released the brake.
- 2.30 s before the reference collision, A's time-to-contact with B became critical.
- 1.40 s before the reference collision, A started braking.
- 1.15 s before the reference collision, A observed B cutting in from the left.
- 0.65 s before the reference collision, A released the brake.
- 0.45 s before the reference collision, A observed B enter its forward path corridor.
- 0.15 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 241, B: 241 N*s).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.60 s after the reference collision, A stopped moving.
- 0.60 s after the reference collision, A came to a stop.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 1.55 <= CUT_IN_FROM_LEFT_START 2.70 (+1.15 s); EGO_PATH_ENTRY 3.40 after critical TTC (+1.85 s) [local times; t_global: cut_in -1.15, critical_ttc_start -2.30, ego_path_entry -0.45, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- BRAKE_END(B); CRITICAL_TTC_START(A,B)
- BRAKE_START(A); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 3.70 s
- CRITICAL_TTC of track_001, since A:e06 (t = 1.55 s); the track was lost at 3.70 s
- CUT_IN_FROM_LEFT of track_001, since A:e08 (t = 2.70 s); the track was lost at 3.70 s
- EGO_PATH of track_001, since A:e10 (t = 3.40 s); the track was lost at 3.70 s
- BRAKE, since A:e13 (t = 3.90 s)
- STOP, since A:e15 (t = 4.45 s)
B:
- BRAKE, since B:e05 (t = 3.90 s)
- STOP, since B:e07 (t = 4.35 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e12 at 3.85 s (local): ego: MOVING; track lost, states UNKNOWN: track_001
- B B:e04 at 3.85 s (local): ego: MOVING

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 3.70 s (A:e11): CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost

## Uncertainty and limitations

- B built no radar track: nothing moving stayed in its forward radar view long enough, so B has no perception of the others.
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
