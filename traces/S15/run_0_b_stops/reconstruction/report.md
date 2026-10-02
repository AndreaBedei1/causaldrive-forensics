# Reconstruction report - S15/run_0_b_stops

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 10.55 s | 107 | 13 | 28 | 2 | none |
| B | 10.55 s | 107 | 26 | 42 | 2 | none |
| C | 10.55 s | 107 | 10 | 20 | 2 | none |

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
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

49 nodes, 30 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.20 s) A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- (unaligned, A local time 0.20 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.10 s) A's radar started tracking unidentified object A:track_002, which appeared on its right.
- (unaligned, A local time 2.10 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 2.10 s) A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- (unaligned, A local time 2.50 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 4.20 s) A's time-to-contact with unidentified object A:track_002 stopped being critical.
- (unaligned, A local time 4.25 s) A observed unidentified object A:track_002 stop closing in.
- (unaligned, A local time 4.65 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 4.65 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 9.55 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.40 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.45 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 1.75 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 1.75 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.05 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.10 s) B's radar started tracking unidentified object B:track_002, which appeared on its left.
- (unaligned, B local time 2.10 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 2.10 s) B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- (unaligned, B local time 2.25 s) B started turning left.
- (unaligned, B local time 2.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.80 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 3.35 s) B stopped turning left.
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 3.55 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 3.90 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 4.00 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 4.30 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 4.35 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 5.25 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.75 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.40 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 7.90 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 9.25 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- (unaligned, B local time 9.85 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.05 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.05 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.35 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.35 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.85 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 4.70 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.70 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 5.20 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 10.20 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 2.50 [local times]
- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 2.10 [local times]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 2.40; EGO_PATH_ENTRY 5.75 after critical TTC (+3.35 s) [local times]
- B's track_002 (unidentified B:track_002): CRITICAL_TTC_START 2.10; EGO_PATH_ENTRY 3.90 after critical TTC (+1.80 s) [local times]
- C's track_001 (unidentified C:track_001): CRITICAL_TTC_START 2.85 [local times]

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
B:
- BRAKE, since B:e11 (t = 2.55 s)
- STOP, since B:e15 (t = 3.40 s)
- STOP_SIGN_DETECTED of sign-1, since B:e25 (t = 9.25 s)
C:
- MOVING, since C:e01 (t = 0.00 s)

### Sign detection windows

A:
- none
B:
- STOP sign sign-0: detected 1.45 s -> 2.05 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 4.00 s -> 7.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 9.25 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
C:
- none

### Perceived state just before each collision report

- no collision was reported

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_001, track_002
B:
- lost with no state active: track_002
C:
- lost with no state active: track_001

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_002 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- B:track_001 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_002 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- C:track_001 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_002 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- A is UNALIGNED: it recorded no collision to anchor on.
- B is UNALIGNED: it recorded no collision to anchor on.
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
