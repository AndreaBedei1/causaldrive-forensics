# Reconstruction report - S15/run_0_deflected_into_c

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 26 | 45 | 2 | A:e09 @ 3.80 s, A:e15 @ 4.75 s |
| B | 13.95 s | 141 | 25 | 47 | 2 | B:e17 @ 3.80 s |
| C | 13.95 s | 141 | 21 | 34 | 2 | C:e12 @ 4.75 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e17 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 3.80 s before the matched collision<br>not at the contact: minimum range 11.09 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 3.70 m/s (> 1.50) |
| A:track_002 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.67 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 1.8 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.35 s before the matched collision<br>not at the contact: last seen 1.00 s before the matched collision (window 0.50 s)<br>track speed disagrees with A's own speed: RMSE 5.84 m/s (> 1.50) |
| B:track_002 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>at the contact: minimum range 0.40 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.68 m/s over 1.8 s |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |

## Global graph

71 nodes, 109 edges; 1 merged node(s): g25 COLLISION(A,B) from A:e09 + B:e17.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.60` STRONG_THROTTLE_START(B)
- `-2.35` TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
- `-2.00` STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.85` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-1.80` TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-1.70` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.45` CRITICAL_TTC_START(B,B:track_001)
- `-1.30` CRITICAL_TTC_START(A,A:track_001)
- `-1.05` CRITICAL_TTC_END(B,B:track_001)
- `-1.00` TRACK_LOST(B,B:track_001)
- `-0.85` BRAKE_START(B)
- `-0.30` BRAKE_END(B)
- `-0.20` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- `+0.05` STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.25` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.75` STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+0.80` EGO_PATH_ENTRY(A,A:track_001)
- `+0.95` COLLISION(A)
- `+1.15` CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
- `+1.25` MOVING_END(A); STOP_START(A)
- `+1.50` STOP_SIGN_DETECTED_START(A,A:sign-2)
- `+4.00` STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+4.90` STOP_SIGN_DETECTED_START(A,A:sign-3); STOP_SIGN_DETECTED_END(A,A:sign-3)
- `+5.95` STOP_SIGN_DETECTED_START(A,A:sign-4)
- `+6.10` STOP_SIGN_DETECTED_END(A,A:sign-4)
- `+7.10` STOP_SIGN_DETECTED_START(A,A:sign-5)

### What happened, in plain language

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 3.80 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 3.80 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.60 s before the matched collision, B started applying strong throttle.
- 2.35 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 2.35 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.00 s before the matched collision, B stopped applying strong throttle.
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the matched collision, B's time-to-contact with A became critical.
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.45 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.30 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.00 s before the matched collision, B's radar lost unidentified object B:track_001.
- 0.85 s before the matched collision, B started braking.
- 0.30 s before the matched collision, B released the brake.
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.75 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.75 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.80 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.95 s after the matched collision, A's collision sensor recorded a contact (peak impulse 1638 N*s).
- 1.15 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 1.15 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 1.25 s after the matched collision, A stopped moving.
- 1.25 s after the matched collision, A came to a stop.
- 1.50 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 4.00 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.90 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-3) (the detector judged it not relevant to its path).
- 4.90 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-3.
- 5.95 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-4) (the detector judged it not relevant to its path).
- 6.10 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-4.
- 7.10 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-5) (the detector judged it not relevant to its path).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 1.65 s) C started applying strong throttle.
- (unaligned, C local time 2.10 s) C stopped applying strong throttle.
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.50 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 3.15 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.45 s) C's radar lost unidentified object C:track_002.
- (unaligned, C local time 4.75 s) C's collision sensor recorded a contact (peak impulse 1638 N*s).
- (unaligned, C local time 4.75 s) C started applying strong throttle.
- (unaligned, C local time 4.80 s) C stopped applying strong throttle.
- (unaligned, C local time 4.80 s) C started braking.
- (unaligned, C local time 4.80 s) C started braking hard.
- (unaligned, C local time 5.00 s) C observed unidentified object C:track_001 enter its forward path corridor.
- (unaligned, C local time 5.05 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 5.05 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 5.05 s) C stopped moving.
- (unaligned, C local time 5.05 s) C came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
- STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
- MOVING_END(A); STOP_START(A)
- STOP_SIGN_DETECTED_START(A,A:sign-3); STOP_SIGN_DETECTED_END(A,A:sign-3)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- EGO_PATH of track_001, since A:e14 (t = 4.60 s)
- STOP, since A:e19 (t = 5.05 s)
- STOP_SIGN_DETECTED of sign-5, since A:e26 (t = 10.90 s)
B:
- CLOSING of track_001, since B:e04 (t = 1.45 s); the track was lost at 2.80 s
- EGO_PATH of track_002, since B:e16 (t = 3.60 s)
- BRAKE, since B:e20 (t = 3.85 s)
- HARD_BRAKE, since B:e21 (t = 3.85 s)
- STOP, since B:e23 (t = 4.00 s)
C:
- CLOSING of track_002, since C:e05 (t = 0.00 s); the track was lost at 4.45 s
- BRAKE, since C:e15 (t = 4.80 s)
- HARD_BRAKE, since C:e16 (t = 4.80 s)
- EGO_PATH of track_001, since C:e17 (t = 5.00 s)
- STOP, since C:e21 (t = 5.05 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.55 s -> 4.55 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 5.30 s -> 7.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-3: detected 8.70 s -> 8.70 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-4: detected 9.75 s -> 9.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-5: detected 10.90 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
C:
- none

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: minimum range 11.09 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with B's own speed: RMSE 3.70 m/s (> 1.50).
- B:track_001 stays anonymous: not at the contact: last seen 1.00 s before the matched collision (window 0.50 s); track speed disagrees with A's own speed: RMSE 5.84 m/s (> 1.50).
- C:track_001 stays anonymous: graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented).
- C:track_002 stays anonymous: graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented).
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
    "path_half_width_m": 1.5
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
