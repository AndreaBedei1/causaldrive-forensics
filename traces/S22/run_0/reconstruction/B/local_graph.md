# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 415.1301955282688 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 10 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 48; edges: 90 (PRECEDES 61, SAME_TRACK 29)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_FRONT | B | track_005 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e07 | 0.00 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e08 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 3.00 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e10 | 3.00 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e11 | 3.20 | TRACK_LOST | B | track_003 | radar |  |
| B:e12 | 3.40 | TRACK_LOST | B | track_005 | radar |  |
| B:e13 | 3.55 | CLOSING_END | B | track_006 | radar |  |
| B:e14 | 3.80 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e15 | 4.80 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e16 | 4.80 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e17 | 5.05 | TRACK_LOST | B | track_002 | radar |  |
| B:e18 | 5.45 | CLOSING_START | B | track_006 | radar |  |
| B:e19 | 5.50 | EGO_PATH_ENTRY | B | track_007 | radar | geometry=estimated_body |
| B:e20 | 5.55 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e21 | 5.55 | CRITICAL_TTC_START | B | track_007 | radar |  |
| B:e22 | 5.60 | CRITICAL_TTC_START | B | track_004 | radar |  |
| B:e23 | 5.85 | EGO_PATH_ENTRY | B | track_004 | radar | geometry=estimated_body |
| B:e24 | 6.15 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e25 | 6.15 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e26 | 6.80 | TRACK_APPEARED_FRONT | B | track_009 | radar | initial_in_ego_path=True |
| B:e27 | 6.95 | EGO_PATH_ENTRY | B | track_006 | radar | geometry=estimated_body |
| B:e28 | 7.20 | CLOSING_END | B | track_006 | radar |  |
| B:e29 | 7.30 | COLLISION | B | - | collision_sensor | peak_impulse=389.26 |
| B:e30 | 7.35 | THROTTLE_END | B | - | controls |  |
| B:e31 | 7.35 | BRAKE_START | B | - | controls |  |
| B:e32 | 7.35 | TURN_LEFT_START | B | - | ego |  |
| B:e33 | 7.40 | TRACK_LOST | B | track_008 | radar |  |
| B:e34 | 7.45 | CUT_IN_FROM_RIGHT_START | B | track_006 | radar | geometry=estimated_body |
| B:e35 | 7.50 | EGO_PATH_EXIT | B | track_009 | radar | geometry=estimated_body |
| B:e36 | 7.60 | TRACK_LOST | B | track_009 | radar |  |
| B:e37 | 7.65 | EGO_PATH_ENTRY | B | track_001 | radar | geometry=estimated_body |
| B:e38 | 7.80 | TRACK_LOST | B | track_004 | radar |  |
| B:e39 | 7.90 | TRACK_LOST | B | track_007 | radar |  |
| B:e40 | 8.00 | TRACK_LOST | B | track_001 | radar |  |
| B:e41 | 8.25 | TURN_LEFT_END | B | - | ego |  |
| B:e42 | 8.25 | MOVING_END | B | - | ego |  |
| B:e43 | 8.25 | STOP_START | B | - | ego |  |
| B:e44 | 8.30 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e45 | 8.30 | TRACK_APPEARED_RIGHT | B | track_010 | radar | initial_in_ego_path=False |
| B:e46 | 8.30 | CLOSING_START | B | track_010 | radar | active_at_first_observation=True |
| B:e47 | 8.55 | CUT_IN_FROM_RIGHT_END | B | track_006 | radar | geometry=estimated_body |
| B:e48 | 9.30 | CLOSING_END | B | track_010 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e33
    B:e31 --PRECEDES--> B:e33
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e36 --PRECEDES--> B:e37
    B:e37 --PRECEDES--> B:e38
    B:e38 --PRECEDES--> B:e39
    B:e39 --PRECEDES--> B:e40
    B:e40 --PRECEDES--> B:e41
    B:e40 --PRECEDES--> B:e42
    B:e40 --PRECEDES--> B:e43
    B:e41 --PRECEDES--> B:e44
    B:e41 --PRECEDES--> B:e45
    B:e41 --PRECEDES--> B:e46
    B:e42 --PRECEDES--> B:e44
    B:e42 --PRECEDES--> B:e45
    B:e42 --PRECEDES--> B:e46
    B:e43 --PRECEDES--> B:e44
    B:e43 --PRECEDES--> B:e45
    B:e43 --PRECEDES--> B:e46
    B:e44 --PRECEDES--> B:e47
    B:e45 --PRECEDES--> B:e47
    B:e46 --PRECEDES--> B:e47
    B:e47 --PRECEDES--> B:e48
    B:e03 --SAME_TRACK--> B:e08
    B:e09 --SAME_TRACK--> B:e10
    B:e06 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e09 --SAME_TRACK--> B:e13
    B:e15 --SAME_TRACK--> B:e16
    B:e05 --SAME_TRACK--> B:e17
    B:e09 --SAME_TRACK--> B:e18
    B:e14 --SAME_TRACK--> B:e19
    B:e09 --SAME_TRACK--> B:e20
    B:e14 --SAME_TRACK--> B:e21
    B:e07 --SAME_TRACK--> B:e22
    B:e07 --SAME_TRACK--> B:e23
    B:e03 --SAME_TRACK--> B:e24
    B:e03 --SAME_TRACK--> B:e25
    B:e09 --SAME_TRACK--> B:e27
    B:e09 --SAME_TRACK--> B:e28
    B:e15 --SAME_TRACK--> B:e33
    B:e09 --SAME_TRACK--> B:e34
    B:e26 --SAME_TRACK--> B:e35
    B:e26 --SAME_TRACK--> B:e36
    B:e03 --SAME_TRACK--> B:e37
    B:e07 --SAME_TRACK--> B:e38
    B:e14 --SAME_TRACK--> B:e39
    B:e03 --SAME_TRACK--> B:e40
    B:e09 --SAME_TRACK--> B:e44
    B:e45 --SAME_TRACK--> B:e46
    B:e09 --SAME_TRACK--> B:e47
    B:e45 --SAME_TRACK--> B:e48
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_FRONT track_005<br>B:e05 TRACK_APPEARED_RIGHT track_002<br>B:e06 TRACK_APPEARED_RIGHT track_003<br>B:e07 TRACK_APPEARED_RIGHT track_004 | ego: not yet observed | - |
| 0.50 | B:e08 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.40 |
| 3.00 | B:e09 TRACK_APPEARED_RIGHT track_006<br>B:e10 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 2.90 |
| 3.20 | B:e11 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC? | 3.10 |
| 3.40 | B:e12 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 | 3.30 |
| 3.55 | B:e13 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 | 3.50 |
| 3.80 | B:e14 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_003, track_005 | 3.70 |
| 4.80 | B:e15 TRACK_APPEARED_RIGHT track_008<br>B:e16 CLOSING_START track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_005 | 4.70 |
| 5.05 | B:e17 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 5.00 |
| 5.45 | B:e18 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 5.40 |
| 5.50 | B:e19 EGO_PATH_ENTRY track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 5.40 |
| 5.55 | B:e20 CRITICAL_TTC_START track_006<br>B:e21 CRITICAL_TTC_START track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 5.50 |
| 5.60 | B:e22 CRITICAL_TTC_START track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 5.50 |
| 5.85 | B:e23 EGO_PATH_ENTRY track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: CRITICAL_TTC<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 5.80 |
| 6.15 | B:e24 CRITICAL_TTC_END track_001<br>B:e25 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 6.10 |
| 6.80 | B:e26 TRACK_APPEARED_FRONT track_009 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 6.70 |
| 6.95 | B:e27 EGO_PATH_ENTRY track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 6.90 |
| 7.20 | B:e28 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 7.10 |
| 7.30 | B:e29 COLLISION | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 7.20 |
| 7.35 | B:e30 THROTTLE_END<br>B:e31 BRAKE_START<br>B:e32 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 7.30 |
| 7.40 | B:e33 TRACK_LOST track_008 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 7.30 |
| 7.45 | B:e34 CUT_IN_FROM_RIGHT_START track_006 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 | 7.40 |
| 7.50 | B:e35 EGO_PATH_EXIT track_009 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 | 7.40 |
| 7.60 | B:e36 TRACK_LOST track_009 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 | 7.50 |
| 7.65 | B:e37 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008, track_009 | 7.60 |
| 7.80 | B:e38 TRACK_LOST track_004 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008, track_009 | 7.70 |
| 7.90 | B:e39 TRACK_LOST track_007 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_008, track_009 | 7.80 |
| 8.00 | B:e40 TRACK_LOST track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_007, track_008, track_009 | 7.90 |
| 8.25 | B:e41 TURN_LEFT_END<br>B:e42 MOVING_END<br>B:e43 STOP_START | ego: MOVING, BRAKE, TURN_LEFT<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 | 8.20 |
| 8.30 | B:e44 CRITICAL_TTC_END track_006<br>B:e45 TRACK_APPEARED_RIGHT track_010<br>B:e46 CLOSING_START track_010 | ego: STOP, BRAKE<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 | 8.20 |
| 8.55 | B:e47 CUT_IN_FROM_RIGHT_END track_006 | ego: STOP, BRAKE<br>track_006: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 | 8.50 |
| 9.30 | B:e48 CLOSING_END track_010 | ego: STOP, BRAKE<br>track_006: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 | 9.20 |

## States still active when observation ended

- CLOSING of track_008, since B:e16 (t = 4.80 s); the track was lost at 7.40 s
- EGO_PATH of track_007, since B:e19 (t = 5.50 s); the track was lost at 7.90 s
- CRITICAL_TTC of track_007, since B:e21 (t = 5.55 s); the track was lost at 7.90 s
- CRITICAL_TTC of track_004, since B:e22 (t = 5.60 s); the track was lost at 7.80 s
- EGO_PATH of track_004, since B:e23 (t = 5.85 s); the track was lost at 7.80 s
- EGO_PATH of track_006, since B:e27 (t = 6.95 s)
- BRAKE, since B:e31 (t = 7.35 s)
- EGO_PATH of track_001, since B:e37 (t = 7.65 s); the track was lost at 8.00 s
- STOP, since B:e43 (t = 8.25 s)

## Tracks lost

- track_008 at 7.40 s (B:e33): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 7.80 s (B:e38): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 7.90 s (B:e39): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 8.00 s (B:e40): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_005, track_002, track_009

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s); EGO_PATH_ENTRY 7.65 after critical TTC (+7.15 s)
- track_004: CRITICAL_TTC_START 5.60, COLLISION 7.30 (+1.70 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.25 s)
- track_006: critical TTC already active before the cut-in: CRITICAL_TTC_START 5.55 <= CUT_IN_FROM_RIGHT_START 7.45 (+1.90 s); EGO_PATH_ENTRY 6.95 after critical TTC (+1.40 s)
- track_007: CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.50 before critical TTC (-0.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 8.00 | 161 | 13.4 m / +0 deg | 13.37 m (0.00) | 14.9 m / -3 deg | 10.1 m/s |
| track_002 | 0.00 | 5.05 | 98 | 12.3 m / +30 deg | 12.28 m (0.00) | 19.9 m / +17 deg | 12.1 m/s |
| track_003 | 0.00 | 3.20 | 63 | 26.0 m / +6 deg | 25.97 m (0.00) | 31.9 m / +6 deg | 11.8 m/s |
| track_004 | 0.00 | 7.80 | 157 | 3.0 m / +129 deg | 1.28 m (2.30) | 15.5 m / +4 deg | 15.2 m/s |
| track_005 | 0.00 | 3.40 | 30 | 28.3 m / +5 deg | 28.32 m (0.00) | 34.1 m / +5 deg | 11.8 m/s |
| track_006 | 3.00 | 11.95 | 180 | 7.6 m / +139 deg | 0.56 m (8.65) | 0.6 m / +9 deg | 12.8 m/s |
| track_007 | 3.80 | 7.90 | 74 | 2.5 m / +40 deg | 2.47 m (3.80) | 17.0 m / -1 deg | 15.2 m/s |
| track_008 | 4.80 | 7.40 | 51 | 19.5 m / +156 deg | 13.87 m (7.40) | 13.9 m / +156 deg | 12.5 m/s |
| track_009 | 6.80 | 7.60 | 16 | 22.9 m / +3 deg | 22.94 m (6.80) | 24.4 m / +8 deg | 12.4 m/s |
| track_010 | 8.30 | 11.95 | 74 | 9.0 m / +152 deg | 2.99 m (9.50) | 3.1 m / +122 deg | 9.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_005, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 3.00 s: B's radar started tracking track_006, which appeared on its right.
- t = 3.00 s: B observed track_006 start closing in (already the case when first observed).
- t = 3.20 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.40 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.55 s: B observed track_006 stop closing in.
- t = 3.80 s: B's radar started tracking track_007, which appeared on its right.
- t = 4.80 s: B's radar started tracking track_008, which appeared on its right.
- t = 4.80 s: B observed track_008 start closing in (already the case when first observed).
- t = 5.05 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.45 s: B observed track_006 start closing in.
- t = 5.50 s: B observed track_007 enter its forward path corridor.
- t = 5.55 s: B's time-to-contact with track_006 became critical.
- t = 5.55 s: B's time-to-contact with track_007 became critical.
- t = 5.60 s: B's time-to-contact with track_004 became critical.
- t = 5.85 s: B observed track_004 enter its forward path corridor.
- t = 6.15 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.15 s: B observed track_001 leave its forward path corridor.
- t = 6.80 s: B's radar started tracking track_009, which appeared in front of it.
- t = 6.95 s: B observed track_006 enter its forward path corridor.
- t = 7.20 s: B observed track_006 stop closing in.
- t = 7.30 s: B's collision sensor recorded a contact (peak impulse 389 N*s).
- t = 7.35 s: B released the accelerator.
- t = 7.35 s: B started braking.
- t = 7.35 s: B started turning left.
- t = 7.40 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 7.45 s: B observed track_006 cutting in from the right.
- t = 7.50 s: B observed track_009 leave its forward path corridor.
- t = 7.60 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 7.65 s: B observed track_001 enter its forward path corridor.
- t = 7.80 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 7.90 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 8.00 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.25 s: B stopped turning left.
- t = 8.25 s: B stopped moving.
- t = 8.25 s: B came to a stop.
- t = 8.30 s: B's time-to-contact with track_006 stopped being critical.
- t = 8.30 s: B's radar started tracking track_010, which appeared on its right.
- t = 8.30 s: B observed track_010 start closing in (already the case when first observed).
- t = 8.55 s: B observed track_006's cut-in from the right settle.
- t = 9.30 s: B observed track_010 stop closing in.
