# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 534.8805473558605 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 9 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 49; edges: 100 (PRECEDES 67, SAME_TRACK 33)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_RIGHT | A | track_003 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e07 | 0.90 | TRACK_APPEARED_FRONT | A | track_004 | radar | initial_in_ego_path=True |
| A:e08 | 0.90 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e09 | 1.00 | TRACK_APPEARED_FRONT | A | track_006 | radar | initial_in_ego_path=True |
| A:e10 | 1.00 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e11 | 1.10 | TRACK_APPEARED_RIGHT | A | track_005 | radar | initial_in_ego_path=False |
| A:e12 | 1.10 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e13 | 1.25 | TRACK_LOST | A | track_003 | radar |  |
| A:e14 | 1.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e15 | 1.85 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar | geometry=estimated_body |
| A:e16 | 2.10 | TRACK_LOST | A | track_006 | radar |  |
| A:e17 | 2.60 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e18 | 2.60 | CLOSING_END | A | track_001 | radar |  |
| A:e19 | 2.65 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar | geometry=estimated_body |
| A:e20 | 3.80 | TRACK_LOST | A | track_004 | radar |  |
| A:e21 | 4.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e22 | 5.30 | CRITICAL_TTC_START | A | track_005 | radar |  |
| A:e23 | 5.40 | CUT_IN_FROM_RIGHT_START | A | track_005 | radar | geometry=estimated_body |
| A:e24 | 6.05 | CLOSING_END | A | track_005 | radar |  |
| A:e25 | 6.10 | CRITICAL_TTC_END | A | track_005 | radar |  |
| A:e26 | 6.15 | CUT_IN_FROM_RIGHT_END | A | track_005 | radar | geometry=estimated_body |
| A:e27 | 6.60 | TRACK_APPEARED_FRONT | A | track_007 | radar | initial_in_ego_path=True |
| A:e28 | 6.60 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e29 | 7.10 | CRITICAL_TTC_START | A | track_007 | radar |  |
| A:e30 | 7.15 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e31 | 7.60 | TRACK_APPEARED_RIGHT | A | track_008 | radar | initial_in_ego_path=False |
| A:e32 | 7.60 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e33 | 7.60 | TRACK_LOST | A | track_005 | radar |  |
| A:e34 | 7.80 | CLOSING_START | A | track_002 | radar |  |
| A:e35 | 8.45 | CRITICAL_TTC_START | A | track_008 | radar |  |
| A:e36 | 8.50 | COLLISION | A | - | collision_sensor | peak_impulse=745.29 |
| A:e37 | 8.50 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e38 | 8.55 | THROTTLE_END | A | - | controls |  |
| A:e39 | 8.55 | BRAKE_START | A | - | controls |  |
| A:e40 | 8.60 | CLOSING_END | A | track_002 | radar |  |
| A:e41 | 8.80 | CRITICAL_TTC_END | A | track_008 | radar |  |
| A:e42 | 8.85 | EGO_PATH_ENTRY | A | track_002 | radar | geometry=estimated_body |
| A:e43 | 9.40 | CLOSING_END | A | track_008 | radar |  |
| A:e44 | 9.45 | CLOSING_END | A | track_007 | radar |  |
| A:e45 | 9.60 | CRITICAL_TTC_END | A | track_007 | radar |  |
| A:e46 | 9.70 | MOVING_END | A | - | ego |  |
| A:e47 | 9.70 | STOP_START | A | - | ego |  |
| A:e48 | 10.55 | TRACK_APPEARED_RIGHT | A | track_009 | radar | initial_in_ego_path=False |
| A:e49 | 10.55 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e07
    A:e01 --PRECEDES--> A:e08
    A:e02 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e08
    A:e03 --PRECEDES--> A:e07
    A:e03 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
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
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e34
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e39
    A:e37 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e44 --PRECEDES--> A:e45
    A:e45 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e46 --PRECEDES--> A:e49
    A:e47 --PRECEDES--> A:e48
    A:e47 --PRECEDES--> A:e49
    A:e04 --SAME_TRACK--> A:e06
    A:e07 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e11 --SAME_TRACK--> A:e12
    A:e05 --SAME_TRACK--> A:e13
    A:e04 --SAME_TRACK--> A:e14
    A:e04 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e04 --SAME_TRACK--> A:e17
    A:e04 --SAME_TRACK--> A:e18
    A:e04 --SAME_TRACK--> A:e19
    A:e07 --SAME_TRACK--> A:e20
    A:e04 --SAME_TRACK--> A:e21
    A:e11 --SAME_TRACK--> A:e22
    A:e11 --SAME_TRACK--> A:e23
    A:e11 --SAME_TRACK--> A:e24
    A:e11 --SAME_TRACK--> A:e25
    A:e11 --SAME_TRACK--> A:e26
    A:e27 --SAME_TRACK--> A:e28
    A:e27 --SAME_TRACK--> A:e29
    A:e03 --SAME_TRACK--> A:e30
    A:e31 --SAME_TRACK--> A:e32
    A:e11 --SAME_TRACK--> A:e33
    A:e03 --SAME_TRACK--> A:e34
    A:e31 --SAME_TRACK--> A:e35
    A:e03 --SAME_TRACK--> A:e37
    A:e03 --SAME_TRACK--> A:e40
    A:e31 --SAME_TRACK--> A:e41
    A:e03 --SAME_TRACK--> A:e42
    A:e31 --SAME_TRACK--> A:e43
    A:e27 --SAME_TRACK--> A:e44
    A:e27 --SAME_TRACK--> A:e45
    A:e48 --SAME_TRACK--> A:e49
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_002<br>A:e04 TRACK_APPEARED_RIGHT track_001<br>A:e05 TRACK_APPEARED_RIGHT track_003<br>A:e06 CLOSING_START track_001 | ego: not yet observed | - |
| 0.90 | A:e07 TRACK_APPEARED_FRONT track_004<br>A:e08 CLOSING_START track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state | 0.80 |
| 1.00 | A:e09 TRACK_APPEARED_FRONT track_006<br>A:e10 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC? | 0.90 |
| 1.10 | A:e11 TRACK_APPEARED_RIGHT track_005<br>A:e12 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? | 1.00 |
| 1.25 | A:e13 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? | 1.20 |
| 1.75 | A:e14 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 | 1.70 |
| 1.85 | A:e15 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 | 1.80 |
| 2.10 | A:e16 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 | 2.00 |
| 2.60 | A:e17 CRITICAL_TTC_END track_001<br>A:e18 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_003, track_006 | 2.50 |
| 2.65 | A:e19 CUT_IN_FROM_RIGHT_END track_001 | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_003, track_006 | 2.60 |
| 3.80 | A:e20 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_003, track_006 | 3.70 |
| 4.20 | A:e21 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_003, track_004, track_006 | 4.10 |
| 5.30 | A:e22 CRITICAL_TTC_START track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 5.20 |
| 5.40 | A:e23 CUT_IN_FROM_RIGHT_START track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 5.30 |
| 6.05 | A:e24 CLOSING_END track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 6.00 |
| 6.10 | A:e25 CRITICAL_TTC_END track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 6.00 |
| 6.15 | A:e26 CUT_IN_FROM_RIGHT_END track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 6.10 |
| 6.60 | A:e27 TRACK_APPEARED_FRONT track_007<br>A:e28 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 6.50 |
| 7.10 | A:e29 CRITICAL_TTC_START track_007 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 7.00 |
| 7.15 | A:e30 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 7.10 |
| 7.60 | A:e31 TRACK_APPEARED_RIGHT track_008<br>A:e32 CLOSING_START track_008<br>A:e33 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_005: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 | 7.50 |
| 7.80 | A:e34 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 7.70 |
| 8.45 | A:e35 CRITICAL_TTC_START track_008 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.40 |
| 8.50 | A:e36 COLLISION<br>A:e37 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.40 |
| 8.55 | A:e38 THROTTLE_END<br>A:e39 BRAKE_START | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.50 |
| 8.60 | A:e40 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.50 |
| 8.80 | A:e41 CRITICAL_TTC_END track_008 | ego: MOVING, BRAKE<br>track_002: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.70 |
| 8.85 | A:e42 EGO_PATH_ENTRY track_002 | ego: MOVING, BRAKE<br>track_002: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 8.80 |
| 9.40 | A:e43 CLOSING_END track_008 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 9.30 |
| 9.45 | A:e44 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 9.40 |
| 9.60 | A:e45 CRITICAL_TTC_END track_007 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 9.50 |
| 9.70 | A:e46 MOVING_END<br>A:e47 STOP_START | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 9.60 |
| 10.55 | A:e48 TRACK_APPEARED_RIGHT track_009<br>A:e49 CLOSING_START track_009 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 | 10.50 |

## States still active when observation ended

- CLOSING of track_004, since A:e08 (t = 0.90 s); the track was lost at 3.80 s
- CLOSING of track_006, since A:e10 (t = 1.00 s); the track was lost at 2.10 s
- BRAKE, since A:e39 (t = 8.55 s)
- EGO_PATH of track_002, since A:e42 (t = 8.85 s)
- STOP, since A:e47 (t = 9.70 s)
- CLOSING of track_009, since A:e49 (t = 10.55 s)

## Tracks lost

- track_006 at 2.10 s (A:e16): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 3.80 s (A:e20): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_001, track_005

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 1.75 <= CUT_IN_FROM_RIGHT_START 1.85 (+0.10 s)
- track_002: CRITICAL_TTC_START 7.15, COLLISION 8.50 (+1.35 s); EGO_PATH_ENTRY 8.85 after critical TTC (+1.70 s)
- track_005: critical TTC already active before the cut-in: CRITICAL_TTC_START 5.30 <= CUT_IN_FROM_RIGHT_START 5.40 (+0.10 s)
- track_007: CRITICAL_TTC_START 7.10, COLLISION 8.50 (+1.40 s)
- track_008: CRITICAL_TTC_START 8.45, COLLISION 8.50 (+0.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.20 | 85 | 15.5 m / +10 deg | 1.21 m (2.70) | 9.1 m / +153 deg | 9.3 m/s |
| track_002 | 0.00 | 11.95 | 240 | 1.6 m / -83 deg | 0.10 m (11.95) | 0.1 m / -89 deg | 13.0 m/s |
| track_003 | 0.00 | 1.25 | 26 | 1.7 m / +110 deg | 1.67 m (0.00) | 9.0 m / +153 deg | 7.6 m/s |
| track_004 | 0.90 | 3.80 | 54 | 59.3 m / +1 deg | 39.64 m (3.80) | 39.6 m / -0 deg | 6.1 m/s |
| track_005 | 1.10 | 7.60 | 130 | 31.6 m / +6 deg | 1.22 m (6.15) | 8.3 m / +153 deg | 9.9 m/s |
| track_006 | 1.00 | 2.10 | 5 | 61.9 m / +3 deg | 54.18 m (2.10) | 54.2 m / -2 deg | 7.8 m/s |
| track_007 | 6.60 | 11.95 | 108 | 20.4 m / +0 deg | 3.50 m (9.45) | 17.6 m / +8 deg | 6.1 m/s |
| track_008 | 7.60 | 11.95 | 88 | 14.3 m / +16 deg | 6.30 m (9.20) | 18.8 m / +17 deg | 6.3 m/s |
| track_009 | 10.55 | 11.95 | 29 | 12.3 m / +155 deg | 4.83 m (11.95) | 4.8 m / +133 deg | 5.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.90 s: A's radar started tracking track_004, which appeared in front of it.
- t = 0.90 s: A observed track_004 start closing in (already the case when first observed).
- t = 1.00 s: A's radar started tracking track_006, which appeared in front of it.
- t = 1.00 s: A observed track_006 start closing in (already the case when first observed).
- t = 1.10 s: A's radar started tracking track_005, which appeared on its right.
- t = 1.10 s: A observed track_005 start closing in (already the case when first observed).
- t = 1.25 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 1.75 s: A's time-to-contact with track_001 became critical.
- t = 1.85 s: A observed track_001 cutting in from the right.
- t = 2.10 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 2.60 s: A's time-to-contact with track_001 stopped being critical.
- t = 2.60 s: A observed track_001 stop closing in.
- t = 2.65 s: A observed track_001's cut-in from the right settle.
- t = 3.80 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 4.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.30 s: A's time-to-contact with track_005 became critical.
- t = 5.40 s: A observed track_005 cutting in from the right.
- t = 6.05 s: A observed track_005 stop closing in.
- t = 6.10 s: A's time-to-contact with track_005 stopped being critical.
- t = 6.15 s: A observed track_005's cut-in from the right settle.
- t = 6.60 s: A's radar started tracking track_007, which appeared in front of it.
- t = 6.60 s: A observed track_007 start closing in (already the case when first observed).
- t = 7.10 s: A's time-to-contact with track_007 became critical.
- t = 7.15 s: A's time-to-contact with track_002 became critical.
- t = 7.60 s: A's radar started tracking track_008, which appeared on its right.
- t = 7.60 s: A observed track_008 start closing in (already the case when first observed).
- t = 7.60 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 7.80 s: A observed track_002 start closing in.
- t = 8.45 s: A's time-to-contact with track_008 became critical.
- t = 8.50 s: A's collision sensor recorded a contact (peak impulse 745 N*s).
- t = 8.50 s: A's time-to-contact with track_002 stopped being critical.
- t = 8.55 s: A released the accelerator.
- t = 8.55 s: A started braking.
- t = 8.60 s: A observed track_002 stop closing in.
- t = 8.80 s: A's time-to-contact with track_008 stopped being critical.
- t = 8.85 s: A observed track_002 enter its forward path corridor.
- t = 9.40 s: A observed track_008 stop closing in.
- t = 9.45 s: A observed track_007 stop closing in.
- t = 9.60 s: A's time-to-contact with track_007 stopped being critical.
- t = 9.70 s: A stopped moving.
- t = 9.70 s: A came to a stop.
- t = 10.55 s: A's radar started tracking track_009, which appeared on its right.
- t = 10.55 s: A observed track_009 start closing in (already the case when first observed).
