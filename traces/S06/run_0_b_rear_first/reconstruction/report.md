# Reconstruction report - S06/run_0_b_rear_first

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.15 s | 143 | 16 | 26 | 2 | A:e10 @ 6.00 s |
| B | 14.15 s | 143 | 20 | 44 | 1 | B:e10 @ 4.60 s, B:e20 @ 6.00 s |
| C | 14.15 s | 143 | 10 | 11 | 0 | C:e10 @ 4.60 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 6.00 | -6.00 | reported the reference collision collision_001 |
| B | ALIGNED | B:e20 | 6.00 | -6.00 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31488.29 vs 31488.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 21812.15 vs 21812.15 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>not at the contact: last seen 1.45 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.04 m/s over 1.5 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 4.45 s before the matched collision<br>not at the contact: last seen 3.05 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>at the contact: minimum range 0.21 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed disagrees with A's own speed: RMSE 11.16 m/s (> 1.50) |

## Global graph

45 nodes, 71 edges; 1 merged node(s): g29 COLLISION(A,B) from A:e10 + B:e20.

### Event sequence (global time)

- `-6.00` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(B,B:track_001)
- `-5.65` STRONG_THROTTLE_START(B)
- `-5.55` CLOSING_START(A,A:track_001)
- `-4.90` CLOSING_START(B,B:track_001)
- `-4.85` STRONG_THROTTLE_START(A)
- `-4.65` STRONG_THROTTLE_END(A)
- `-4.45` TRACK_APPEARED(A,A:track_002)
- `-4.40` CLOSING_END(A,A:track_001)
- `-4.25` STRONG_THROTTLE_END(B)
- `-3.90` CLOSING_END(B,B:track_001)
- `-3.05` TRACK_LOST(A,A:track_002)
- `-2.80` CLOSING_START(B,B:track_001)
- `-2.55` PREDICTED_PATH_CONFLICT_START(B,B:track_001)
- `-2.30` CRITICAL_TTC_START(B,B:track_001)
- `-1.45` TRACK_LOST(A,A:track_001)
- `-1.40` COLLISION(B); STRONG_THROTTLE_START(B)
- `-1.35` PREDICTED_PATH_CONFLICT_END(B,B:track_001); CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- `-1.25` MOVING_END(B); STOP_START(B)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(A)
- `+0.05` STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
- `+0.20` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 6.00 s before the matched collision, A started moving (already the case when first observed).
- 6.00 s before the matched collision, B started moving (already the case when first observed).
- 6.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 6.00 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 5.65 s before the matched collision, B started applying strong throttle.
- 5.55 s before the matched collision, A observed unidentified object A:track_001 start closing in.
- 4.90 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.85 s before the matched collision, A started applying strong throttle.
- 4.65 s before the matched collision, A stopped applying strong throttle.
- 4.45 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 4.40 s before the matched collision, A observed unidentified object A:track_001 stop closing in.
- 4.25 s before the matched collision, B stopped applying strong throttle.
- 3.90 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 3.05 s before the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 2.80 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.55 s before the matched collision, B predicted a path conflict with unidentified object B:track_001 (close approach ahead if both keep their motion).
- 2.30 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.45 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, B's collision sensor recorded a contact (peak impulse 21812 N*s).
- 1.40 s before the matched collision, B started applying strong throttle.
- 1.35 s before the matched collision, B stopped predicting a path conflict with unidentified object B:track_001.
- 1.35 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.35 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.35 s before the matched collision, B stopped applying strong throttle.
- 1.35 s before the matched collision, B started braking.
- 1.35 s before the matched collision, B started braking hard.
- 1.25 s before the matched collision, B stopped moving.
- 1.25 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31488, B: 31488 N*s).
- At the matched collision, A started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.20 s after the matched collision, A stopped moving.
- 0.20 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.50 s) C started applying strong throttle.
- (unaligned, C local time 2.05 s) C stopped applying strong throttle.
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 2.95 s) C started braking hard.
- (unaligned, C local time 3.05 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 4.60 s) C's collision sensor recorded a contact (peak impulse 21812 N*s).

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(B,B:track_001)
- COLLISION(B); STRONG_THROTTLE_START(B)
- PREDICTED_PATH_CONFLICT_END(B,B:track_001); CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,B); STRONG_THROTTLE_START(A)
- STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e13 (t = 6.05 s)
- HARD_BRAKE, since A:e14 (t = 6.05 s)
- STOP, since A:e16 (t = 6.20 s)
B:
- BRAKE, since B:e16 (t = 4.65 s)
- HARD_BRAKE, since B:e17 (t = 4.65 s)
- STOP, since B:e19 (t = 4.75 s)
C:
- BRAKE, since C:e05 (t = 2.95 s)
- HARD_BRAKE, since C:e06 (t = 2.95 s)
- STOP, since C:e09 (t = 4.05 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e10 at 6.00 s (local): ego: MOVING; lost (states UNKNOWN): track_001, track_002
- B B:e10 at 4.60 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT
- B B:e20 at 6.00 s (local): ego: STOP, BRAKE, HARD_BRAKE; track_001: VISIBLE, IN_EGO_PATH
- C C:e10 at 4.60 s (local): ego: STOP, BRAKE, HARD_BRAKE

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 2.95 s (A:e08): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 4.55 s (A:e09): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_001 stays anonymous: not at the contact: last seen 1.45 s before the matched collision (window 0.50 s).
- A:track_002 stays anonymous: not at the contact: last seen 3.05 s before the matched collision (window 0.50 s); speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 11.16 m/s (> 1.50).
- C is UNALIGNED: shares only a non-reference collision (multi-hop alignment not implemented).
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
    "hard_brake_threshold": 0.9,
    "strong_throttle_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_ttc_s": 2.0,
    "path_half_width_m": 1.5,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "conflict_horizon_s": 4.0,
    "conflict_distance_m": 1.5,
    "conflict_release_horizon_s": 5.0,
    "conflict_release_distance_m": 2.5,
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
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
