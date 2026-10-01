# Reconstruction report - S16/run_0_consequential

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 23 | 44 | 3 | A:e05 @ 5.15 s, A:e17 @ 5.90 s |
| B | 9.95 s | 101 | 21 | 41 | 1 | B:e15 @ 5.15 s |
| C | 9.95 s | 101 | 10 | 18 | 0 | C:e04 @ 5.90 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e15 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 5.60 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 15.63 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.40 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>at the contact: minimum range 0.59 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.46 m/s over 3.0 s |

## Global graph

53 nodes, 108 edges; 1 merged node(s): g19 COLLISION(A,B) from A:e05 + B:e15.

### Event sequence (global time)

- `-5.15` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
- `-4.50` PREDICTED_PATH_CONFLICT_START(B,A)
- `-4.45` STRONG_THROTTLE_START(A); CLOSING_START(B,A)
- `-4.40` CRITICAL_TTC_START(B,A)
- `-3.80` STRONG_THROTTLE_START(B)
- `-3.75` PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-3.35` STRONG_THROTTLE_END(A)
- `-2.65` STRONG_THROTTLE_END(B)
- `-1.20` BRAKE_START(A)
- `-0.90` CLOSING_START(B,A); PREDICTED_PATH_CONFLICT_START(B,A)
- `-0.75` CRITICAL_TTC_START(B,A)
- `-0.40` BRAKE_START(B)
- `+0.00` COLLISION(A,B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_001)
- `+0.05` PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A); HARD_BRAKE_START(B)
- `+0.35` PREDICTED_PATH_CONFLICT_START(A,A:track_001)
- `+0.40` TRACK_APPEARED(A,A:track_003)
- `+0.45` CLOSING_END(A,A:track_002); MOVING_END(B); STOP_START(B)
- `+0.50` EGO_PATH_ENTRY(A,A:track_001); TRACK_LOST(A,A:track_002)
- `+0.75` COLLISION(A)
- `+0.85` CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
- `+0.90` PREDICTED_PATH_CONFLICT_END(A,A:track_001); MOVING_END(A); STOP_START(A)
- `+1.05` TRACK_LOST(A,A:track_003)

### What happened, in plain language

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A.
- 4.50 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 4.45 s before the matched collision, A started applying strong throttle.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.80 s before the matched collision, B started applying strong throttle.
- 3.75 s before the matched collision, B stopped predicting a path conflict with A.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 3.35 s before the matched collision, A stopped applying strong throttle.
- 2.65 s before the matched collision, B stopped applying strong throttle.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.90 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 0.75 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the matched collision, A's radar started tracking unidentified object A:track_001.
- At the matched collision, A's radar started tracking unidentified object A:track_002.
- At the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- At the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- At the matched collision, A's time-to-contact with unidentified object A:track_001 became critical (already the case when first observed).
- 0.05 s after the matched collision, B stopped predicting a path conflict with A.
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, A released the brake.
- 0.05 s after the matched collision, B started braking hard.
- 0.35 s after the matched collision, A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- 0.40 s after the matched collision, A's radar started tracking unidentified object A:track_003.
- 0.45 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the matched collision, A's collision sensor recorded a contact (peak impulse 2696 N*s).
- 0.85 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 0.90 s after the matched collision, A stopped predicting a path conflict with unidentified object A:track_001.
- 0.90 s after the matched collision, A stopped moving.
- 0.90 s after the matched collision, A came to a stop.
- 1.05 s after the matched collision, A's radar lost unidentified object A:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
- (unaligned, C local time 5.90 s) C's collision sensor recorded a contact (peak impulse 2696 N*s).
- (unaligned, C local time 5.90 s) C left its stop.
- (unaligned, C local time 5.90 s) C started moving.
- (unaligned, C local time 5.95 s) C started braking.
- (unaligned, C local time 5.95 s) C started braking hard.
- (unaligned, C local time 6.05 s) C stopped moving.
- (unaligned, C local time 6.05 s) C came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
- STRONG_THROTTLE_START(A); CLOSING_START(B,A)
- PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- CLOSING_START(B,A); PREDICTED_PATH_CONFLICT_START(B,A)
- COLLISION(A,B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_001)
- PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A); HARD_BRAKE_START(B)
- CLOSING_END(A,A:track_002); MOVING_END(B); STOP_START(B)
- EGO_PATH_ENTRY(A,A:track_001); TRACK_LOST(A,A:track_002)
- CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
- PREDICTED_PATH_CONFLICT_END(A,A:track_001); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- EGO_PATH of track_001, since A:e15 (t = 5.65 s)
- STOP, since A:e22 (t = 6.05 s)
B:
- BRAKE, since B:e14 (t = 4.75 s)
- HARD_BRAKE, since B:e19 (t = 5.20 s)
- STOP, since B:e21 (t = 5.60 s)
C:
- BRAKE, since C:e07 (t = 5.95 s)
- HARD_BRAKE, since C:e08 (t = 5.95 s)
- STOP, since C:e10 (t = 6.05 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e05 at 5.15 s (local): ego: MOVING, BRAKE
- A A:e17 at 5.90 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT; track_003: VISIBLE; lost (states UNKNOWN): track_002
- B B:e15 at 5.15 s (local): ego: MOVING, BRAKE; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT
- C C:e04 at 5.90 s (local): ego: STOP

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_002, track_003
B:
- no track was lost
C:
- no track was lost

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_001 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 5.60 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with B's own speed before the collision.
- A:track_002 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 15.63 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with B's own speed before the collision.
- A:track_003 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.40 s after the matched collision; speed not comparable with B's own speed before the collision.
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
