# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 568.7781397588551 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 12 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 48; edges: 117 (PRECEDES 88, SAME_TRACK 29)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_003 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e08 | 0.00 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e09 | 0.05 | TRACK_APPEARED_LEFT | A | track_005#segment_1 | radar | initial_in_ego_path=False |
| A:e10 | 0.05 | CLOSING_START | A | track_005#segment_1 | radar | active_at_first_observation=True |
| A:e11 | 0.40 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=True |
| A:e12 | 0.40 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e13 | 0.85 | EGO_PATH_EXIT | A | track_006 | radar | geometry=estimated_body |
| A:e14 | 1.30 | TRACK_LOST | A | track_005#segment_1 | radar |  |
| A:e15 | 1.35 | TRACK_APPEARED_FRONT | A | track_005#segment_2 | radar | initial_in_ego_path=True |
| A:e16 | 1.35 | CLOSING_START | A | track_005#segment_2 | radar | active_at_first_observation=True |
| A:e17 | 1.85 | CRITICAL_TTC_START | A | track_005#segment_2 | radar |  |
| A:e18 | 3.65 | TRACK_LOST | A | track_003 | radar |  |
| A:e19 | 5.65 | TRACK_LOST | A | track_004 | radar |  |
| A:e20 | 5.95 | TRACK_LOST | A | track_002 | radar |  |
| A:e21 | 6.95 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar | geometry=estimated_body |
| A:e22 | 7.50 | CLOSING_END | A | track_001 | radar |  |
| A:e23 | 7.70 | TRACK_APPEARED_FRONT | A | track_007 | radar | initial_in_ego_path=True |
| A:e24 | 7.70 | TRACK_APPEARED_FRONT | A | track_008 | radar | initial_in_ego_path=True |
| A:e25 | 7.70 | TRACK_APPEARED_LEFT | A | track_009 | radar | initial_in_ego_path=False |
| A:e26 | 7.75 | COLLISION | A | - | collision_sensor | peak_impulse=1897.70 |
| A:e27 | 7.75 | CRITICAL_TTC_END | A | track_005#segment_2 | radar |  |
| A:e28 | 7.75 | CLOSING_END | A | track_005#segment_2 | radar |  |
| A:e29 | 7.75 | CLOSING_END | A | track_006 | radar |  |
| A:e30 | 7.80 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar | geometry=estimated_body |
| A:e31 | 7.80 | THROTTLE_END | A | - | controls |  |
| A:e32 | 7.80 | BRAKE_START | A | - | controls |  |
| A:e33 | 8.20 | CRITICAL_TTC_START | A | track_008 | radar |  |
| A:e34 | 8.45 | TRACK_LOST | A | track_007 | radar |  |
| A:e35 | 8.45 | TRACK_LOST | A | track_008 | radar |  |
| A:e36 | 8.45 | TRACK_LOST | A | track_009 | radar |  |
| A:e37 | 8.90 | MOVING_END | A | - | ego |  |
| A:e38 | 8.90 | STOP_START | A | - | ego |  |
| A:e39 | 8.95 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e40 | 8.95 | TRACK_APPEARED_RIGHT | A | track_011 | radar | initial_in_ego_path=False |
| A:e41 | 8.95 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e42 | 8.95 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e43 | 9.05 | TRACK_LOST | A | track_006 | radar |  |
| A:e44 | 9.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e45 | 9.85 | CLOSING_END | A | track_010 | radar |  |
| A:e46 | 9.90 | CLOSING_END | A | track_011 | radar |  |
| A:e47 | 10.85 | TRACK_LOST | A | track_010 | radar |  |
| A:e48 | 10.85 | TRACK_LOST | A | track_011 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e09
    A:e01 --PRECEDES--> A:e10
    A:e02 --PRECEDES--> A:e09
    A:e02 --PRECEDES--> A:e10
    A:e03 --PRECEDES--> A:e09
    A:e03 --PRECEDES--> A:e10
    A:e04 --PRECEDES--> A:e09
    A:e04 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e09
    A:e05 --PRECEDES--> A:e10
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e23 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e29
    A:e24 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e28
    A:e24 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e31
    A:e26 --PRECEDES--> A:e32
    A:e27 --PRECEDES--> A:e30
    A:e27 --PRECEDES--> A:e31
    A:e27 --PRECEDES--> A:e32
    A:e28 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e32
    A:e29 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e33
    A:e33 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e38
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e37 --PRECEDES--> A:e40
    A:e37 --PRECEDES--> A:e41
    A:e37 --PRECEDES--> A:e42
    A:e38 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e38 --PRECEDES--> A:e41
    A:e38 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e43
    A:e40 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e43
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e44 --PRECEDES--> A:e45
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e05 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e11 --SAME_TRACK--> A:e12
    A:e11 --SAME_TRACK--> A:e13
    A:e09 --SAME_TRACK--> A:e14
    A:e15 --SAME_TRACK--> A:e16
    A:e15 --SAME_TRACK--> A:e17
    A:e03 --SAME_TRACK--> A:e18
    A:e06 --SAME_TRACK--> A:e19
    A:e04 --SAME_TRACK--> A:e20
    A:e05 --SAME_TRACK--> A:e21
    A:e05 --SAME_TRACK--> A:e22
    A:e15 --SAME_TRACK--> A:e27
    A:e15 --SAME_TRACK--> A:e28
    A:e11 --SAME_TRACK--> A:e29
    A:e05 --SAME_TRACK--> A:e30
    A:e24 --SAME_TRACK--> A:e33
    A:e23 --SAME_TRACK--> A:e34
    A:e24 --SAME_TRACK--> A:e35
    A:e25 --SAME_TRACK--> A:e36
    A:e39 --SAME_TRACK--> A:e41
    A:e40 --SAME_TRACK--> A:e42
    A:e11 --SAME_TRACK--> A:e43
    A:e05 --SAME_TRACK--> A:e44
    A:e39 --SAME_TRACK--> A:e45
    A:e40 --SAME_TRACK--> A:e46
    A:e39 --SAME_TRACK--> A:e47
    A:e40 --SAME_TRACK--> A:e48
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_003<br>A:e04 TRACK_APPEARED_LEFT track_002<br>A:e05 TRACK_APPEARED_RIGHT track_001<br>A:e06 TRACK_APPEARED_RIGHT track_004<br>A:e07 CLOSING_START track_001<br>A:e08 CLOSING_START track_003 | ego: not yet observed | - |
| 0.05 | A:e09 TRACK_APPEARED_LEFT track_005#segment_1<br>A:e10 CLOSING_START track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.00 |
| 0.40 | A:e11 TRACK_APPEARED_LEFT track_006<br>A:e12 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.30 |
| 0.85 | A:e13 EGO_PATH_EXIT track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? | 0.80 |
| 1.30 | A:e14 TRACK_LOST track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING | 1.20 |
| 1.35 | A:e15 TRACK_APPEARED_FRONT track_005#segment_2<br>A:e16 CLOSING_START track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 | 1.30 |
| 1.85 | A:e17 CRITICAL_TTC_START track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 | 1.80 |
| 3.65 | A:e18 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 | 3.60 |
| 5.65 | A:e19 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 | 5.60 |
| 5.95 | A:e20 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_004, track_005#segment_1 | 5.90 |
| 6.95 | A:e21 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 6.90 |
| 7.50 | A:e22 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 7.40 |
| 7.70 | A:e23 TRACK_APPEARED_FRONT track_007<br>A:e24 TRACK_APPEARED_FRONT track_008<br>A:e25 TRACK_APPEARED_LEFT track_009 | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 7.60 |
| 7.75 | A:e26 COLLISION<br>A:e27 CRITICAL_TTC_END track_005#segment_2<br>A:e28 CLOSING_END track_005#segment_2<br>A:e29 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 7.70 |
| 7.80 | A:e30 CUT_IN_FROM_RIGHT_END track_001<br>A:e31 THROTTLE_END<br>A:e32 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 7.70 |
| 8.20 | A:e33 CRITICAL_TTC_START track_008 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 8.10 |
| 8.45 | A:e34 TRACK_LOST track_007<br>A:e35 TRACK_LOST track_008<br>A:e36 TRACK_LOST track_009 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 | 8.40 |
| 8.90 | A:e37 MOVING_END<br>A:e38 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 | 8.80 |
| 8.95 | A:e39 TRACK_APPEARED_LEFT track_010<br>A:e40 TRACK_APPEARED_RIGHT track_011<br>A:e41 CLOSING_START track_010<br>A:e42 CLOSING_START track_011 | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 | 8.90 |
| 9.05 | A:e43 TRACK_LOST track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 | 9.00 |
| 9.20 | A:e44 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_006, track_007, track_008, track_009 | 9.10 |
| 9.85 | A:e45 CLOSING_END track_010 | ego: STOP, BRAKE<br>track_005#segment_2: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005#segment_1, track_006, track_007, track_008, track_009 | 9.80 |
| 9.90 | A:e46 CLOSING_END track_011 | ego: STOP, BRAKE<br>track_005#segment_2: IN_EGO_PATH<br>track_010: no active state<br>track_011: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005#segment_1, track_006, track_007, track_008, track_009 | 9.80 |
| 10.85 | A:e47 TRACK_LOST track_010<br>A:e48 TRACK_LOST track_011 | ego: STOP, BRAKE<br>track_005#segment_2: IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005#segment_1, track_006, track_007, track_008, track_009 | 10.80 |

## States still active when observation ended

- CLOSING of track_003, since A:e08 (t = 0.00 s); the track was lost at 3.65 s
- CLOSING of track_005#segment_1, since A:e10 (t = 0.05 s); the track was lost at 1.30 s
- BRAKE, since A:e32 (t = 7.80 s)
- CRITICAL_TTC of track_008, since A:e33 (t = 8.20 s); the track was lost at 8.45 s
- STOP, since A:e38 (t = 8.90 s)

## Tracks lost

- track_005#segment_1 at 1.30 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.65 s (A:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 8.45 s (A:e34): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 8.45 s (A:e35): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_009, track_006, track_001, track_010, track_011

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CUT_IN_FROM_RIGHT_START 6.95, no critical TTC after it
- track_005#segment_2: CRITICAL_TTC_START 1.85, COLLISION 7.75 (+5.90 s)
- track_008: CRITICAL_TTC_START 8.20

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 9.20 | 185 | 14.7 m / +10 deg | 2.37 m (7.75) | 8.6 m / +22 deg | 11.5 m/s |
| track_002 | 0.00 | 5.95 | 117 | 2.1 m / -60 deg | 1.38 m (1.10) | 9.1 m / -154 deg | 12.2 m/s |
| track_003 | 0.00 | 3.65 | 68 | 36.0 m / -5 deg | 28.90 m (3.65) | 28.9 m / -6 deg | 11.0 m/s |
| track_004 | 0.00 | 5.65 | 111 | 1.5 m / +78 deg | 1.30 m (0.50) | 9.1 m / +154 deg | 12.0 m/s |
| track_005#segment_1 | 0.05 | 1.30 | 26 | 15.4 m / -7 deg | 12.86 m (1.30) | 12.9 m / +1 deg | 12.1 m/s |
| track_005#segment_2 | 1.35 | 11.95 | 213 | 12.6 m / +0 deg | 0.02 m (8.80) | 0.7 m / -0 deg | 11.7 m/s |
| track_006 | 0.40 | 9.05 | 174 | 16.2 m / -7 deg | 3.24 m (7.85) | 8.7 m / -25 deg | 11.2 m/s |
| track_007 | 7.70 | 8.45 | 16 | 18.3 m / +0 deg | 18.06 m (8.00) | 18.9 m / -0 deg | 11.1 m/s |
| track_008 | 7.70 | 8.45 | 16 | 3.7 m / +1 deg | 3.65 m (8.10) | 3.7 m / -0 deg | 12.0 m/s |
| track_009 | 7.70 | 8.45 | 14 | 21.1 m / -7 deg | 20.83 m (8.00) | 21.6 m / -7 deg | 11.0 m/s |
| track_010 | 8.95 | 10.85 | 39 | 8.9 m / -152 deg | 1.39 m (9.85) | 9.5 m / -22 deg | 10.6 m/s |
| track_011 | 8.95 | 10.85 | 39 | 9.6 m / +153 deg | 1.41 m (9.95) | 9.0 m / +22 deg | 10.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: A observed track_003 start closing in (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_005#segment_1, which appeared on its left.
- t = 0.05 s: A observed track_005#segment_1 start closing in (already the case when first observed).
- t = 0.40 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.40 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.85 s: A observed track_006 leave its forward path corridor.
- t = 1.30 s: A's radar lost track_005#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 1.35 s: A's radar started tracking track_005#segment_2, which appeared in front of it.
- t = 1.35 s: A observed track_005#segment_2 start closing in (already the case when first observed).
- t = 1.85 s: A's time-to-contact with track_005#segment_2 became critical.
- t = 3.65 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.65 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 5.95 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.95 s: A observed track_001 cutting in from the right.
- t = 7.50 s: A observed track_001 stop closing in.
- t = 7.70 s: A's radar started tracking track_007, which appeared in front of it.
- t = 7.70 s: A's radar started tracking track_008, which appeared in front of it.
- t = 7.70 s: A's radar started tracking track_009, which appeared on its left.
- t = 7.75 s: A's collision sensor recorded a contact (peak impulse 1898 N*s).
- t = 7.75 s: A's time-to-contact with track_005#segment_2 stopped being critical.
- t = 7.75 s: A observed track_005#segment_2 stop closing in.
- t = 7.75 s: A observed track_006 stop closing in.
- t = 7.80 s: A observed track_001's cut-in from the right settle.
- t = 7.80 s: A released the accelerator.
- t = 7.80 s: A started braking.
- t = 8.20 s: A's time-to-contact with track_008 became critical.
- t = 8.45 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 8.45 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 8.45 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 8.90 s: A stopped moving.
- t = 8.90 s: A came to a stop.
- t = 8.95 s: A's radar started tracking track_010, which appeared on its left.
- t = 8.95 s: A's radar started tracking track_011, which appeared on its right.
- t = 8.95 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.95 s: A observed track_011 start closing in (already the case when first observed).
- t = 9.05 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 9.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.85 s: A observed track_010 stop closing in.
- t = 9.90 s: A observed track_011 stop closing in.
- t = 10.85 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 10.85 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
