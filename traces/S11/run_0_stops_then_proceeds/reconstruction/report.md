# Reconstruction report - S11/run_0_stops_then_proceeds

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.35 s | 135 | 4 | 6 | 1 | none |
| B | 13.35 s | 135 | 57 | 205 | 13 | none |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_004 | B:track_004 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_005 | B:track_005 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_006 | B:track_006 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_007 | B:track_007 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_008 | B:track_008 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_009 | B:track_009 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_010 | B:track_010 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_011 | B:track_011 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_012 | B:track_012 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_013 | B:track_013 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Global graph

61 nodes, 35 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.70 s) A's radar started tracking unidentified object A:track_001, which appeared on its right.
- (unaligned, A local time 2.70 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 5.75 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.05 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.40 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.50 s) B's radar started tracking unidentified object B:track_001, which appeared on its left.
- (unaligned, B local time 2.50 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 6.75 s) B released the brake.
- (unaligned, B local time 7.20 s) B left its stop.
- (unaligned, B local time 7.20 s) B started moving.
- (unaligned, B local time 7.95 s) B started turning left.
- (unaligned, B local time 7.95 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_003, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_004, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_005, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_006, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_007, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_008, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_002, which appeared on its right.
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_004 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_005 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_006 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_007 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_008 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_010, which appeared on its left.
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_009, which appeared on its right.
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_011, which appeared on its right.
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_009 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_010 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_011 start closing in (already the case when first observed).
- (unaligned, B local time 8.60 s) B's radar started tracking unidentified object B:track_012, which appeared on its right.
- (unaligned, B local time 8.60 s) B's radar started tracking unidentified object B:track_013, which appeared on its right.
- (unaligned, B local time 8.60 s) B observed unidentified object B:track_012 start closing in (already the case when first observed).
- (unaligned, B local time 8.60 s) B observed unidentified object B:track_013 start closing in (already the case when first observed).
- (unaligned, B local time 8.65 s) B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.80 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.80 s) B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.90 s) B observed unidentified object B:track_009 stop closing in.
- (unaligned, B local time 8.90 s) B's time-to-contact with unidentified object B:track_004 became critical.
- (unaligned, B local time 8.95 s) B's radar lost unidentified object B:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.00 s) B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.50 s) B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.70 s) B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 10.70 s) B stopped turning left.
- (unaligned, B local time 10.70 s) B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 12.05 s) B observed unidentified object B:track_012 stop closing in.
- (unaligned, B local time 12.20 s) B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 12.30 s) B observed unidentified object B:track_012 start closing in.
- (unaligned, B local time 12.55 s) B observed unidentified object B:track_007 cutting in from the left.
- (unaligned, B local time 12.75 s) B observed unidentified object B:track_012 cutting in from the right.
- (unaligned, B local time 12.90 s) B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 13.05 s) B's radar lost unidentified object B:track_012 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- B's track_001 (unidentified B:track_001): EGO_PATH_ENTRY 5.80, no critical TTC [local times]
- B's track_004 (unidentified B:track_004): CRITICAL_TTC_START 8.90 [local times]
- B's track_007 (unidentified B:track_007): CUT_IN_FROM_LEFT_START 12.55, no critical TTC after it [local times]
- B's track_012 (unidentified B:track_012): CUT_IN_FROM_RIGHT_START 12.75, no critical TTC after it [local times]

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 2.70 s); the track was lost at 5.75 s
B:
- MOVING, since B:e14 (t = 7.20 s)
- CLOSING of track_003, since B:e24 (t = 8.40 s); the track was lost at 10.70 s
- CLOSING of track_004, since B:e25 (t = 8.40 s); the track was lost at 9.50 s
- CLOSING of track_005, since B:e26 (t = 8.40 s); the track was lost at 8.65 s
- CLOSING of track_006, since B:e27 (t = 8.40 s)
- CLOSING of track_007, since B:e28 (t = 8.40 s); the track was lost at 12.90 s
- CLOSING of track_008, since B:e29 (t = 8.40 s); the track was lost at 12.20 s
- CLOSING of track_010, since B:e34 (t = 8.45 s); the track was lost at 9.70 s
- CLOSING of track_011, since B:e35 (t = 8.45 s); the track was lost at 8.80 s
- CLOSING of track_013, since B:e39 (t = 8.60 s); the track was lost at 8.95 s
- CRITICAL_TTC of track_004, since B:e44 (t = 8.90 s); the track was lost at 9.50 s
- CLOSING of track_012, since B:e53 (t = 12.30 s); the track was lost at 13.05 s
- CUT_IN_FROM_LEFT of track_007, since B:e54 (t = 12.55 s); the track was lost at 12.90 s
- CUT_IN_FROM_RIGHT of track_012, since B:e55 (t = 12.75 s); the track was lost at 13.05 s

### Sign detection windows

A:
- none
B:
- STOP sign sign-1: detected 2.05 s -> 2.40 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- no collision was reported

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 5.75 s (A:e04): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_005 at 8.65 s (B:e40): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 8.80 s (B:e42): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 8.95 s (B:e45): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 9.50 s (B:e47): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 9.70 s (B:e48): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 10.70 s (B:e50): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 12.20 s (B:e52): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 12.90 s (B:e56): CLOSING, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 13.05 s (B:e57): CLOSING, CUT_IN_FROM_RIGHT were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001, track_002, track_009

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- B:track_001 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_002 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_003 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_004 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_005 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_006 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_007 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_008 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_009 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_010 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_011 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_012 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_013 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- A is UNALIGNED: it recorded no collision to anchor on.
- B is UNALIGNED: it recorded no collision to anchor on.
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
