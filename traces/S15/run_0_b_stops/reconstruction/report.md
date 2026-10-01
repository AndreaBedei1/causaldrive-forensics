# Reconstruction report - S15/run_0_b_stops

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 10.55 s | 107 | 9 | 20 | 2 | none |
| B | 10.55 s | 107 | 35 | 61 | 3 | none |
| C | 10.55 s | 107 | 14 | 22 | 2 | none |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

58 nodes, 30 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's radar started tracking unidentified object A:track_002, which appeared on its right.
- (unaligned, A local time 2.00 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- (unaligned, A local time 2.45 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 3.80 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 4.45 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.45 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 1.45 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 1.80 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 1.95 s) B's radar started tracking unidentified object B:track_002, which appeared on its left.
- (unaligned, B local time 1.95 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 2.00 s) B's time-to-contact with unidentified object B:track_002 became critical.
- (unaligned, B local time 2.10 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.35 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 2.70 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 2.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 3.40 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 3.70 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 3.90 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 3.95 s) B's radar started tracking unidentified object B:track_003, which appeared on its right.
- (unaligned, B local time 3.95 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 4.20 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 4.40 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 4.80 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- (unaligned, B local time 4.80 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 4.80 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.35 s) B observed unidentified object B:track_003 stop closing in.
- (unaligned, B local time 5.60 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- (unaligned, B local time 5.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.65 s) B observed unidentified object B:track_003 enter its forward path corridor.
- (unaligned, B local time 6.45 s) B observed unidentified object B:track_003 leave its forward path corridor.
- (unaligned, B local time 6.70 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- (unaligned, B local time 10.55 s) B started applying strong throttle.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 1.65 s) C started applying strong throttle.
- (unaligned, C local time 2.10 s) C stopped applying strong throttle.
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.45 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.95 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.00 s) C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 4.50 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.50 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 4.50 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 4.45 s
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.80 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.80 s
- CRITICAL_TTC of track_001, since A:e07 (t = 2.45 s); the track was lost at 4.45 s
B:
- CLOSING of track_001, since B:e04 (t = 1.45 s); the track was lost at 2.85 s
- BRAKE, since B:e12 (t = 2.55 s)
- HARD_BRAKE, since B:e13 (t = 2.55 s)
- STOP, since B:e17 (t = 3.40 s)
- STOP_SIGN_DETECTED of sign-1, since B:e34 (t = 6.70 s)
- STRONG_THROTTLE, since B:e35 (t = 10.55 s)
C:
- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_002, since C:e05 (t = 0.00 s); the track was lost at 4.00 s

### Sign detection windows

A:
- none
B:
- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 3.40 s -> 3.70 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 4.80 s -> 4.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 5.60 s -> 5.60 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 6.70 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
C:
- none

### Perceived state just before each collision report

- no collision was reported

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.80 s (A:e08): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 4.45 s (A:e09): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_001 at 2.85 s (B:e15): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_002
C:
- track_002 at 4.00 s (C:e11): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 4.50 s (C:e14): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_002 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- B:track_001 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_002 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_003 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- C:track_001 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_002 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- A is UNALIGNED: it recorded no collision to anchor on.
- B is UNALIGNED: it recorded no collision to anchor on.
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
    "hard_brake_threshold": 0.9,
    "strong_throttle_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_ttc_s": 2.0,
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
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
