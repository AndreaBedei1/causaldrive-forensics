# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 534.8805473558605 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 11 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 55; edges: 116 (PRECEDES 79, SAME_TRACK 37)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_RIGHT | A | track_003 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e07 | 0.85 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e08 | 0.85 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e09 | 0.90 | TRACK_APPEARED_FRONT | A | track_005#segment_1 | radar | initial_in_ego_path=False |
| A:e10 | 0.90 | CLOSING_START | A | track_005#segment_1 | radar | active_at_first_observation=True |
| A:e11 | 1.25 | TRACK_LOST | A | track_003 | radar |  |
| A:e12 | 1.60 | TRACK_APPEARED_FRONT | A | track_006 | radar | initial_in_ego_path=False |
| A:e13 | 1.60 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e14 | 1.80 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e15 | 1.95 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar | geometry=estimated_body |
| A:e16 | 2.20 | TRACK_LOST | A | track_005#segment_1 | radar |  |
| A:e17 | 2.25 | TRACK_APPEARED_FRONT | A | track_005#segment_2 | radar | initial_in_ego_path=True |
| A:e18 | 2.25 | CLOSING_START | A | track_005#segment_2 | radar | active_at_first_observation=True |
| A:e19 | 2.60 | CLOSING_END | A | track_001 | radar |  |
| A:e20 | 2.65 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar | geometry=estimated_body |
| A:e21 | 2.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e22 | 3.65 | TRACK_LOST | A | track_006 | radar |  |
| A:e23 | 3.80 | TRACK_LOST | A | track_005#segment_2 | radar |  |
| A:e24 | 4.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e25 | 5.45 | CRITICAL_TTC_START | A | track_004 | radar |  |
| A:e26 | 5.60 | CUT_IN_FROM_RIGHT_START | A | track_004 | radar | geometry=estimated_body |
| A:e27 | 6.10 | CLOSING_END | A | track_004 | radar |  |
| A:e28 | 6.15 | CRITICAL_TTC_END | A | track_004 | radar |  |
| A:e29 | 6.20 | CUT_IN_FROM_RIGHT_END | A | track_004 | radar | geometry=estimated_body |
| A:e30 | 6.60 | TRACK_APPEARED_FRONT | A | track_007#segment_1 | radar | initial_in_ego_path=False |
| A:e31 | 6.60 | CLOSING_START | A | track_007#segment_1 | radar | active_at_first_observation=True |
| A:e32 | 6.85 | TRACK_APPEARED_RIGHT | A | track_008 | radar | initial_in_ego_path=False |
| A:e33 | 6.85 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e34 | 7.15 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e35 | 7.50 | TRACK_LOST | A | track_007#segment_1 | radar |  |
| A:e36 | 7.55 | TRACK_APPEARED_FRONT | A | track_007#segment_2 | radar | initial_in_ego_path=True |
| A:e37 | 7.55 | CLOSING_START | A | track_007#segment_2 | radar | active_at_first_observation=True |
| A:e38 | 7.60 | TRACK_LOST | A | track_004 | radar |  |
| A:e39 | 7.65 | CLOSING_START | A | track_002 | radar |  |
| A:e40 | 8.05 | CRITICAL_TTC_START | A | track_007#segment_2 | radar |  |
| A:e41 | 8.45 | CRITICAL_TTC_START | A | track_008 | radar |  |
| A:e42 | 8.50 | COLLISION | A | - | collision_sensor | peak_impulse=745.29 |
| A:e43 | 8.50 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e44 | 8.50 | EGO_PATH_ENTRY | A | track_002 | radar | geometry=estimated_body |
| A:e45 | 8.55 | CLOSING_END | A | track_002 | radar |  |
| A:e46 | 8.55 | THROTTLE_END | A | - | controls |  |
| A:e47 | 8.55 | BRAKE_START | A | - | controls |  |
| A:e48 | 8.80 | CRITICAL_TTC_END | A | track_008 | radar |  |
| A:e49 | 9.40 | CLOSING_END | A | track_008 | radar |  |
| A:e50 | 9.45 | CLOSING_END | A | track_007#segment_2 | radar |  |
| A:e51 | 9.60 | CRITICAL_TTC_END | A | track_007#segment_2 | radar |  |
| A:e52 | 9.70 | MOVING_END | A | - | ego |  |
| A:e53 | 9.70 | STOP_START | A | - | ego |  |
| A:e54 | 10.55 | TRACK_APPEARED_RIGHT | A | track_009 | radar | initial_in_ego_path=False |
| A:e55 | 10.55 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |

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
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e34
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e45
    A:e42 --PRECEDES--> A:e46
    A:e42 --PRECEDES--> A:e47
    A:e43 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e46
    A:e43 --PRECEDES--> A:e47
    A:e44 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e44 --PRECEDES--> A:e47
    A:e45 --PRECEDES--> A:e48
    A:e46 --PRECEDES--> A:e48
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e49 --PRECEDES--> A:e50
    A:e50 --PRECEDES--> A:e51
    A:e51 --PRECEDES--> A:e52
    A:e51 --PRECEDES--> A:e53
    A:e52 --PRECEDES--> A:e54
    A:e52 --PRECEDES--> A:e55
    A:e53 --PRECEDES--> A:e54
    A:e53 --PRECEDES--> A:e55
    A:e04 --SAME_TRACK--> A:e06
    A:e07 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e05 --SAME_TRACK--> A:e11
    A:e12 --SAME_TRACK--> A:e13
    A:e04 --SAME_TRACK--> A:e14
    A:e04 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e17 --SAME_TRACK--> A:e18
    A:e04 --SAME_TRACK--> A:e19
    A:e04 --SAME_TRACK--> A:e20
    A:e04 --SAME_TRACK--> A:e21
    A:e12 --SAME_TRACK--> A:e22
    A:e17 --SAME_TRACK--> A:e23
    A:e04 --SAME_TRACK--> A:e24
    A:e07 --SAME_TRACK--> A:e25
    A:e07 --SAME_TRACK--> A:e26
    A:e07 --SAME_TRACK--> A:e27
    A:e07 --SAME_TRACK--> A:e28
    A:e07 --SAME_TRACK--> A:e29
    A:e30 --SAME_TRACK--> A:e31
    A:e32 --SAME_TRACK--> A:e33
    A:e03 --SAME_TRACK--> A:e34
    A:e30 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e37
    A:e07 --SAME_TRACK--> A:e38
    A:e03 --SAME_TRACK--> A:e39
    A:e36 --SAME_TRACK--> A:e40
    A:e32 --SAME_TRACK--> A:e41
    A:e03 --SAME_TRACK--> A:e43
    A:e03 --SAME_TRACK--> A:e44
    A:e03 --SAME_TRACK--> A:e45
    A:e32 --SAME_TRACK--> A:e48
    A:e32 --SAME_TRACK--> A:e49
    A:e36 --SAME_TRACK--> A:e50
    A:e36 --SAME_TRACK--> A:e51
    A:e54 --SAME_TRACK--> A:e55
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_002<br>A:e04 TRACK_APPEARED_RIGHT track_001<br>A:e05 TRACK_APPEARED_RIGHT track_003<br>A:e06 CLOSING_START track_001 | ego: not yet observed | - |
| 0.85 | A:e07 TRACK_APPEARED_RIGHT track_004<br>A:e08 CLOSING_START track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state | 0.80 |
| 0.90 | A:e09 TRACK_APPEARED_FRONT track_005#segment_1<br>A:e10 CLOSING_START track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, CRITICAL_TTC? | 0.80 |
| 1.25 | A:e11 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 1.20 |
| 1.60 | A:e12 TRACK_APPEARED_FRONT track_006<br>A:e13 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 | 1.50 |
| 1.80 | A:e14 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 | 1.70 |
| 1.95 | A:e15 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 | 1.90 |
| 2.20 | A:e16 TRACK_LOST track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003 | 2.10 |
| 2.25 | A:e17 TRACK_APPEARED_FRONT track_005#segment_2<br>A:e18 CLOSING_START track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 | 2.20 |
| 2.60 | A:e19 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 | 2.50 |
| 2.65 | A:e20 CUT_IN_FROM_RIGHT_END track_001<br>A:e21 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 | 2.60 |
| 3.65 | A:e22 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_2: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 | 3.60 |
| 3.80 | A:e23 TRACK_LOST track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_2: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005#segment_1, track_006 | 3.70 |
| 4.20 | A:e24 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1, track_005#segment_2, track_006 | 4.10 |
| 5.45 | A:e25 CRITICAL_TTC_START track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 5.40 |
| 5.60 | A:e26 CUT_IN_FROM_RIGHT_START track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 5.50 |
| 6.10 | A:e27 CLOSING_END track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 6.00 |
| 6.15 | A:e28 CRITICAL_TTC_END track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 6.10 |
| 6.20 | A:e29 CUT_IN_FROM_RIGHT_END track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 6.10 |
| 6.60 | A:e30 TRACK_APPEARED_FRONT track_007#segment_1<br>A:e31 CLOSING_START track_007#segment_1 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 6.50 |
| 6.85 | A:e32 TRACK_APPEARED_RIGHT track_008<br>A:e33 CLOSING_START track_008 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 6.80 |
| 7.15 | A:e34 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 7.10 |
| 7.50 | A:e35 TRACK_LOST track_007#segment_1 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 | 7.40 |
| 7.55 | A:e36 TRACK_APPEARED_FRONT track_007#segment_2<br>A:e37 CLOSING_START track_007#segment_2 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 7.50 |
| 7.60 | A:e38 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 7.50 |
| 7.65 | A:e39 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 7.60 |
| 8.05 | A:e40 CRITICAL_TTC_START track_007#segment_2 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 8.00 |
| 8.45 | A:e41 CRITICAL_TTC_START track_008 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 8.40 |
| 8.50 | A:e42 COLLISION<br>A:e43 CRITICAL_TTC_END track_002<br>A:e44 EGO_PATH_ENTRY track_002 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 8.40 |
| 8.55 | A:e45 CLOSING_END track_002<br>A:e46 THROTTLE_END<br>A:e47 BRAKE_START | ego: MOVING, THROTTLE<br>track_002: CLOSING, IN_EGO_PATH<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 8.50 |
| 8.80 | A:e48 CRITICAL_TTC_END track_008 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 8.70 |
| 9.40 | A:e49 CLOSING_END track_008 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 9.30 |
| 9.45 | A:e50 CLOSING_END track_007#segment_2 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 9.40 |
| 9.60 | A:e51 CRITICAL_TTC_END track_007#segment_2 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 9.50 |
| 9.70 | A:e52 MOVING_END<br>A:e53 STOP_START | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 9.60 |
| 10.55 | A:e54 TRACK_APPEARED_RIGHT track_009<br>A:e55 CLOSING_START track_009 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 | 10.50 |

## States still active when observation ended

- CLOSING of track_005#segment_1, since A:e10 (t = 0.90 s); the track was lost at 2.20 s
- CLOSING of track_006, since A:e13 (t = 1.60 s); the track was lost at 3.65 s
- CLOSING of track_005#segment_2, since A:e18 (t = 2.25 s); the track was lost at 3.80 s
- CLOSING of track_007#segment_1, since A:e31 (t = 6.60 s); the track was lost at 7.50 s
- EGO_PATH of track_002, since A:e44 (t = 8.50 s)
- BRAKE, since A:e47 (t = 8.55 s)
- STOP, since A:e53 (t = 9.70 s)
- CLOSING of track_009, since A:e55 (t = 10.55 s)

## Tracks lost

- track_005#segment_1 at 2.20 s (A:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.65 s (A:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005#segment_2 at 3.80 s (A:e23): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_007#segment_1 at 7.50 s (A:e35): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_001, track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 1.80 <= CUT_IN_FROM_RIGHT_START 1.95 (+0.15 s)
- track_002: CRITICAL_TTC_START 7.15, COLLISION 8.50 (+1.35 s); EGO_PATH_ENTRY 8.50 after critical TTC (+1.35 s)
- track_004: critical TTC already active before the cut-in: CRITICAL_TTC_START 5.45 <= CUT_IN_FROM_RIGHT_START 5.60 (+0.15 s)
- track_007#segment_2: CRITICAL_TTC_START 8.05, COLLISION 8.50 (+0.45 s)
- track_008: CRITICAL_TTC_START 8.45, COLLISION 8.50 (+0.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.20 | 85 | 15.6 m / +10 deg | 1.21 m (2.70) | 9.0 m / +153 deg | 9.3 m/s |
| track_002 | 0.00 | 11.95 | 240 | 1.6 m / -84 deg | 0.07 m (11.95) | 0.1 m / -89 deg | 13.3 m/s |
| track_003 | 0.00 | 1.25 | 26 | 1.7 m / +110 deg | 1.68 m (0.00) | 9.0 m / +153 deg | 7.6 m/s |
| track_004 | 0.85 | 7.60 | 135 | 33.4 m / +6 deg | 1.24 m (6.20) | 8.0 m / +152 deg | 9.9 m/s |
| track_005#segment_1 | 0.90 | 2.20 | 27 | 59.4 m / +2 deg | 50.50 m (2.20) | 50.5 m / -0 deg | 6.3 m/s |
| track_005#segment_2 | 2.25 | 3.80 | 31 | 50.1 m / -0 deg | 39.70 m (3.80) | 39.7 m / -0 deg | 6.1 m/s |
| track_006 | 1.60 | 3.65 | 35 | 55.1 m / +4 deg | 41.28 m (3.65) | 41.3 m / +4 deg | 6.1 m/s |
| track_007#segment_1 | 6.60 | 7.50 | 19 | 20.7 m / +2 deg | 14.46 m (7.50) | 14.5 m / +1 deg | 6.4 m/s |
| track_007#segment_2 | 7.55 | 11.95 | 89 | 13.7 m / +3 deg | 3.44 m (9.45) | 17.6 m / +7 deg | 6.2 m/s |
| track_008 | 6.85 | 11.95 | 103 | 19.5 m / +9 deg | 6.53 m (9.10) | 18.9 m / +16 deg | 6.3 m/s |
| track_009 | 10.55 | 11.95 | 29 | 12.3 m / +155 deg | 4.84 m (11.95) | 4.8 m / +134 deg | 5.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.85 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.85 s: A observed track_004 start closing in (already the case when first observed).
- t = 0.90 s: A's radar started tracking track_005#segment_1, which appeared in front of it.
- t = 0.90 s: A observed track_005#segment_1 start closing in (already the case when first observed).
- t = 1.25 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 1.60 s: A's radar started tracking track_006, which appeared in front of it.
- t = 1.60 s: A observed track_006 start closing in (already the case when first observed).
- t = 1.80 s: A's time-to-contact with track_001 became critical.
- t = 1.95 s: A observed track_001 cutting in from the right.
- t = 2.20 s: A's radar lost track_005#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 2.25 s: A's radar started tracking track_005#segment_2, which appeared in front of it.
- t = 2.25 s: A observed track_005#segment_2 start closing in (already the case when first observed).
- t = 2.60 s: A observed track_001 stop closing in.
- t = 2.65 s: A observed track_001's cut-in from the right settle.
- t = 2.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.65 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: A's radar lost track_005#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 4.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.45 s: A's time-to-contact with track_004 became critical.
- t = 5.60 s: A observed track_004 cutting in from the right.
- t = 6.10 s: A observed track_004 stop closing in.
- t = 6.15 s: A's time-to-contact with track_004 stopped being critical.
- t = 6.20 s: A observed track_004's cut-in from the right settle.
- t = 6.60 s: A's radar started tracking track_007#segment_1, which appeared in front of it.
- t = 6.60 s: A observed track_007#segment_1 start closing in (already the case when first observed).
- t = 6.85 s: A's radar started tracking track_008, which appeared on its right.
- t = 6.85 s: A observed track_008 start closing in (already the case when first observed).
- t = 7.15 s: A's time-to-contact with track_002 became critical.
- t = 7.50 s: A's radar lost track_007#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 7.55 s: A's radar started tracking track_007#segment_2, which appeared in front of it.
- t = 7.55 s: A observed track_007#segment_2 start closing in (already the case when first observed).
- t = 7.60 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 7.65 s: A observed track_002 start closing in.
- t = 8.05 s: A's time-to-contact with track_007#segment_2 became critical.
- t = 8.45 s: A's time-to-contact with track_008 became critical.
- t = 8.50 s: A's collision sensor recorded a contact (peak impulse 745 N*s).
- t = 8.50 s: A's time-to-contact with track_002 stopped being critical.
- t = 8.50 s: A observed track_002 enter its forward path corridor.
- t = 8.55 s: A observed track_002 stop closing in.
- t = 8.55 s: A released the accelerator.
- t = 8.55 s: A started braking.
- t = 8.80 s: A's time-to-contact with track_008 stopped being critical.
- t = 9.40 s: A observed track_008 stop closing in.
- t = 9.45 s: A observed track_007#segment_2 stop closing in.
- t = 9.60 s: A's time-to-contact with track_007#segment_2 stopped being critical.
- t = 9.70 s: A stopped moving.
- t = 9.70 s: A came to a stop.
- t = 10.55 s: A's radar started tracking track_009, which appeared on its right.
- t = 10.55 s: A observed track_009 start closing in (already the case when first observed).
