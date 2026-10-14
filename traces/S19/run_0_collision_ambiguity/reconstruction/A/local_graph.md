# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 568.7781397588551 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 15 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 58; edges: 132 (PRECEDES 96, SAME_TRACK 36)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_003 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001#segment_1 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | CLOSING_START | A | track_001#segment_1 | radar | active_at_first_observation=True |
| A:e08 | 0.00 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e09 | 0.05 | TRACK_APPEARED_LEFT | A | track_005#segment_1 | radar | initial_in_ego_path=False |
| A:e10 | 0.05 | CLOSING_START | A | track_005#segment_1 | radar | active_at_first_observation=True |
| A:e11 | 0.35 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e12 | 0.35 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e13 | 0.75 | TRACK_LOST | A | track_001#segment_1 | radar |  |
| A:e14 | 0.80 | TRACK_APPEARED_RIGHT | A | track_001#segment_2 | radar | initial_in_ego_path=False |
| A:e15 | 0.80 | CLOSING_START | A | track_001#segment_2 | radar | active_at_first_observation=True |
| A:e16 | 0.90 | TRACK_LOST | A | track_005#segment_1 | radar |  |
| A:e17 | 0.95 | TRACK_APPEARED_FRONT | A | track_005#segment_2 | radar | initial_in_ego_path=True |
| A:e18 | 0.95 | CLOSING_START | A | track_005#segment_2 | radar | active_at_first_observation=True |
| A:e19 | 1.45 | CRITICAL_TTC_START | A | track_005#segment_2 | radar |  |
| A:e20 | 1.50 | CUT_IN_FROM_RIGHT_START | A | track_001#segment_2 | radar | geometry=estimated_body |
| A:e21 | 1.75 | CUT_IN_FROM_RIGHT_END | A | track_001#segment_2 | radar | geometry=estimated_body |
| A:e22 | 3.65 | TRACK_LOST | A | track_003 | radar |  |
| A:e23 | 5.65 | TRACK_LOST | A | track_004 | radar |  |
| A:e24 | 5.95 | TRACK_LOST | A | track_002 | radar |  |
| A:e25 | 6.95 | CUT_IN_FROM_RIGHT_START | A | track_001#segment_2 | radar | geometry=estimated_body |
| A:e26 | 7.55 | CLOSING_END | A | track_001#segment_2 | radar |  |
| A:e27 | 7.70 | CUT_IN_FROM_RIGHT_END | A | track_001#segment_2 | radar | geometry=estimated_body |
| A:e28 | 7.70 | TRACK_APPEARED_FRONT | A | track_007 | radar | initial_in_ego_path=True |
| A:e29 | 7.70 | TRACK_APPEARED_LEFT | A | track_008 | radar | initial_in_ego_path=False |
| A:e30 | 7.75 | COLLISION | A | - | collision_sensor | peak_impulse=1897.70 |
| A:e31 | 7.75 | CRITICAL_TTC_END | A | track_005#segment_2 | radar |  |
| A:e32 | 7.75 | CLOSING_END | A | track_006 | radar |  |
| A:e33 | 7.80 | THROTTLE_END | A | - | controls |  |
| A:e34 | 7.80 | BRAKE_START | A | - | controls |  |
| A:e35 | 7.80 | TRACK_LOST | A | track_005#segment_2 | radar |  |
| A:e36 | 7.85 | TRACK_APPEARED_LEFT | A | track_005#segment_3 | radar | initial_in_ego_path=False |
| A:e37 | 7.85 | CLOSING_START | A | track_005#segment_3 | radar | active_at_first_observation=True |
| A:e38 | 8.15 | CLOSING_END | A | track_005#segment_3 | radar |  |
| A:e39 | 8.20 | EGO_PATH_ENTRY | A | track_001#segment_2 | radar | geometry=estimated_body |
| A:e40 | 8.20 | CRITICAL_TTC_START | A | track_001#segment_2 | radar |  |
| A:e41 | 8.45 | TRACK_LOST | A | track_007 | radar |  |
| A:e42 | 8.45 | TRACK_LOST | A | track_008 | radar |  |
| A:e43 | 8.55 | TRACK_APPEARED_RIGHT | A | track_009 | radar | initial_in_ego_path=False |
| A:e44 | 8.75 | TRACK_LOST | A | track_001#segment_2 | radar |  |
| A:e45 | 8.90 | MOVING_END | A | - | ego |  |
| A:e46 | 8.90 | STOP_START | A | - | ego |  |
| A:e47 | 8.95 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e48 | 8.95 | TRACK_APPEARED_RIGHT | A | track_011 | radar | initial_in_ego_path=False |
| A:e49 | 8.95 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e50 | 8.95 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e51 | 9.05 | TRACK_LOST | A | track_006 | radar |  |
| A:e52 | 9.20 | TRACK_LOST | A | track_009 | radar |  |
| A:e53 | 9.25 | TRACK_LOST | A | track_005#segment_3 | radar |  |
| A:e54 | 9.30 | TRACK_APPEARED_FRONT | A | track_005#segment_4 | radar | initial_in_ego_path=True |
| A:e55 | 9.95 | CLOSING_END | A | track_011 | radar |  |
| A:e56 | 10.00 | CLOSING_END | A | track_010 | radar |  |
| A:e57 | 10.85 | TRACK_LOST | A | track_010 | radar |  |
| A:e58 | 10.85 | TRACK_LOST | A | track_011 | radar |  |

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
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
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
    A:e26 --PRECEDES--> A:e29
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
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e43
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e44 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e47
    A:e45 --PRECEDES--> A:e48
    A:e45 --PRECEDES--> A:e49
    A:e45 --PRECEDES--> A:e50
    A:e46 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e46 --PRECEDES--> A:e49
    A:e46 --PRECEDES--> A:e50
    A:e47 --PRECEDES--> A:e51
    A:e48 --PRECEDES--> A:e51
    A:e49 --PRECEDES--> A:e51
    A:e50 --PRECEDES--> A:e51
    A:e51 --PRECEDES--> A:e52
    A:e52 --PRECEDES--> A:e53
    A:e53 --PRECEDES--> A:e54
    A:e54 --PRECEDES--> A:e55
    A:e55 --PRECEDES--> A:e56
    A:e56 --PRECEDES--> A:e57
    A:e56 --PRECEDES--> A:e58
    A:e05 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e11 --SAME_TRACK--> A:e12
    A:e05 --SAME_TRACK--> A:e13
    A:e14 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e17 --SAME_TRACK--> A:e18
    A:e17 --SAME_TRACK--> A:e19
    A:e14 --SAME_TRACK--> A:e20
    A:e14 --SAME_TRACK--> A:e21
    A:e03 --SAME_TRACK--> A:e22
    A:e06 --SAME_TRACK--> A:e23
    A:e04 --SAME_TRACK--> A:e24
    A:e14 --SAME_TRACK--> A:e25
    A:e14 --SAME_TRACK--> A:e26
    A:e14 --SAME_TRACK--> A:e27
    A:e17 --SAME_TRACK--> A:e31
    A:e11 --SAME_TRACK--> A:e32
    A:e17 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e37
    A:e36 --SAME_TRACK--> A:e38
    A:e14 --SAME_TRACK--> A:e39
    A:e14 --SAME_TRACK--> A:e40
    A:e28 --SAME_TRACK--> A:e41
    A:e29 --SAME_TRACK--> A:e42
    A:e14 --SAME_TRACK--> A:e44
    A:e47 --SAME_TRACK--> A:e49
    A:e48 --SAME_TRACK--> A:e50
    A:e11 --SAME_TRACK--> A:e51
    A:e43 --SAME_TRACK--> A:e52
    A:e36 --SAME_TRACK--> A:e53
    A:e48 --SAME_TRACK--> A:e55
    A:e47 --SAME_TRACK--> A:e56
    A:e47 --SAME_TRACK--> A:e57
    A:e48 --SAME_TRACK--> A:e58
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_003<br>A:e04 TRACK_APPEARED_LEFT track_002<br>A:e05 TRACK_APPEARED_RIGHT track_001#segment_1<br>A:e06 TRACK_APPEARED_RIGHT track_004<br>A:e07 CLOSING_START track_001#segment_1<br>A:e08 CLOSING_START track_003 | ego: not yet observed | - |
| 0.05 | A:e09 TRACK_APPEARED_LEFT track_005#segment_1<br>A:e10 CLOSING_START track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.00 |
| 0.35 | A:e11 TRACK_APPEARED_LEFT track_006<br>A:e12 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.30 |
| 0.75 | A:e13 TRACK_LOST track_001#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC? | 0.70 |
| 0.80 | A:e14 TRACK_APPEARED_RIGHT track_001#segment_2<br>A:e15 CLOSING_START track_001#segment_2 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 | 0.70 |
| 0.90 | A:e16 TRACK_LOST track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 | 0.80 |
| 0.95 | A:e17 TRACK_APPEARED_FRONT track_005#segment_2<br>A:e18 CLOSING_START track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 | 0.90 |
| 1.45 | A:e19 CRITICAL_TTC_START track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 | 1.40 |
| 1.50 | A:e20 CUT_IN_FROM_RIGHT_START track_001#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 | 1.40 |
| 1.75 | A:e21 CUT_IN_FROM_RIGHT_END track_001#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 | 1.70 |
| 3.65 | A:e22 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 | 3.60 |
| 5.65 | A:e23 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_003, track_005#segment_1 | 5.60 |
| 5.95 | A:e24 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_003, track_004, track_005#segment_1 | 5.90 |
| 6.95 | A:e25 CUT_IN_FROM_RIGHT_START track_001#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 | 6.90 |
| 7.55 | A:e26 CLOSING_END track_001#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 | 7.50 |
| 7.70 | A:e27 CUT_IN_FROM_RIGHT_END track_001#segment_2<br>A:e28 TRACK_APPEARED_FRONT track_007<br>A:e29 TRACK_APPEARED_LEFT track_008 | ego: MOVING, THROTTLE<br>track_001#segment_2: CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 | 7.60 |
| 7.75 | A:e30 COLLISION<br>A:e31 CRITICAL_TTC_END track_005#segment_2<br>A:e32 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 | 7.70 |
| 7.80 | A:e33 THROTTLE_END<br>A:e34 BRAKE_START<br>A:e35 TRACK_LOST track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_005#segment_2: CLOSING, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 | 7.70 |
| 7.85 | A:e36 TRACK_APPEARED_LEFT track_005#segment_3<br>A:e37 CLOSING_START track_005#segment_3 | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 | 7.80 |
| 8.15 | A:e38 CLOSING_END track_005#segment_3 | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_005#segment_3: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 | 8.10 |
| 8.20 | A:e39 EGO_PATH_ENTRY track_001#segment_2<br>A:e40 CRITICAL_TTC_START track_001#segment_2 | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 | 8.10 |
| 8.45 | A:e41 TRACK_LOST track_007<br>A:e42 TRACK_LOST track_008 | ego: MOVING, BRAKE<br>track_001#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 | 8.40 |
| 8.55 | A:e43 TRACK_APPEARED_RIGHT track_009 | ego: MOVING, BRAKE<br>track_001#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 | 8.50 |
| 8.75 | A:e44 TRACK_LOST track_001#segment_2 | ego: MOVING, BRAKE<br>track_001#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 | 8.70 |
| 8.90 | A:e45 MOVING_END<br>A:e46 STOP_START | ego: MOVING, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 | 8.80 |
| 8.95 | A:e47 TRACK_APPEARED_LEFT track_010<br>A:e48 TRACK_APPEARED_RIGHT track_011<br>A:e49 CLOSING_START track_010<br>A:e50 CLOSING_START track_011 | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 | 8.90 |
| 9.05 | A:e51 TRACK_LOST track_006 | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 | 9.00 |
| 9.20 | A:e52 TRACK_LOST track_009 | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007, track_008 | 9.10 |
| 9.25 | A:e53 TRACK_LOST track_005#segment_3 | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007, track_008, track_009 | 9.20 |
| 9.30 | A:e54 TRACK_APPEARED_FRONT track_005#segment_4 | ego: STOP, BRAKE<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_005#segment_3, track_006, track_007, track_008, track_009 | 9.20 |
| 9.95 | A:e55 CLOSING_END track_011 | ego: STOP, BRAKE<br>track_005#segment_4: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_005#segment_3, track_006, track_007, track_008, track_009 | 9.90 |
| 10.00 | A:e56 CLOSING_END track_010 | ego: STOP, BRAKE<br>track_005#segment_4: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_005#segment_3, track_006, track_007, track_008, track_009 | 9.90 |
| 10.85 | A:e57 TRACK_LOST track_010<br>A:e58 TRACK_LOST track_011 | ego: STOP, BRAKE<br>track_005#segment_4: IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_005#segment_3, track_006, track_007, track_008, track_009 | 10.80 |

## States still active when observation ended

- CLOSING of track_001#segment_1, since A:e07 (t = 0.00 s); the track was lost at 0.75 s
- CLOSING of track_003, since A:e08 (t = 0.00 s); the track was lost at 3.65 s
- CLOSING of track_005#segment_1, since A:e10 (t = 0.05 s); the track was lost at 0.90 s
- CLOSING of track_005#segment_2, since A:e18 (t = 0.95 s); the track was lost at 7.80 s
- BRAKE, since A:e34 (t = 7.80 s)
- EGO_PATH of track_001#segment_2, since A:e39 (t = 8.20 s); the track was lost at 8.75 s
- CRITICAL_TTC of track_001#segment_2, since A:e40 (t = 8.20 s); the track was lost at 8.75 s
- STOP, since A:e46 (t = 8.90 s)

## Tracks lost

- track_001#segment_1 at 0.75 s (A:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005#segment_1 at 0.90 s (A:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.65 s (A:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005#segment_2 at 7.80 s (A:e35): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 8.45 s (A:e41): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001#segment_2 at 8.75 s (A:e44): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_008, track_006, track_009, track_005#segment_3, track_010, track_011

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001#segment_2: cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 1.50 < CRITICAL_TTC_START 8.20 (+6.70 s); EGO_PATH_ENTRY 8.20 together with critical TTC (+0.00 s)
- track_005#segment_2: CRITICAL_TTC_START 1.45, COLLISION 7.75 (+6.30 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001#segment_1 | 0.00 | 0.75 | 16 | 14.9 m / +9 deg | 13.44 m (0.75) | 13.4 m / +12 deg | 10.7 m/s |
| track_001#segment_2 | 0.80 | 8.75 | 160 | 13.1 m / +14 deg | 1.85 m (8.50) | 4.7 m / +11 deg | 13.3 m/s |
| track_002 | 0.00 | 5.95 | 117 | 2.0 m / -61 deg | 1.36 m (1.10) | 9.1 m / -154 deg | 12.1 m/s |
| track_003 | 0.00 | 3.65 | 68 | 36.0 m / -5 deg | 28.88 m (3.65) | 28.9 m / -6 deg | 10.9 m/s |
| track_004 | 0.00 | 5.65 | 111 | 1.4 m / +80 deg | 1.27 m (0.50) | 9.0 m / +154 deg | 12.1 m/s |
| track_005#segment_1 | 0.05 | 0.90 | 18 | 15.5 m / -7 deg | 13.71 m (0.90) | 13.7 m / +2 deg | 12.1 m/s |
| track_005#segment_2 | 0.95 | 7.80 | 138 | 13.3 m / +0 deg | 0.26 m (7.55) | 1.1 m / -31 deg | 11.1 m/s |
| track_005#segment_3 | 7.85 | 9.25 | 25 | 0.8 m / -8 deg | 0.56 m (8.50) | 1.5 m / +2 deg | 10.5 m/s |
| track_005#segment_4 | 9.30 | 11.95 | 54 | 0.8 m / +5 deg | 0.79 m (9.85) | 0.8 m / -0 deg | 1.3 m/s |
| track_006 | 0.35 | 9.05 | 175 | 16.0 m / -10 deg | 3.23 m (8.00) | 8.7 m / -25 deg | 11.1 m/s |
| track_007 | 7.70 | 8.45 | 16 | 18.3 m / +0 deg | 18.06 m (8.00) | 18.9 m / +0 deg | 11.1 m/s |
| track_008 | 7.70 | 8.45 | 15 | 21.3 m / -7 deg | 21.06 m (8.00) | 21.9 m / -7 deg | 11.1 m/s |
| track_009 | 8.55 | 9.20 | 14 | 3.5 m / +60 deg | 3.49 m (8.55) | 8.6 m / +25 deg | 11.1 m/s |
| track_010 | 8.95 | 10.85 | 39 | 9.4 m / -152 deg | 1.46 m (9.95) | 9.3 m / -21 deg | 10.6 m/s |
| track_011 | 8.95 | 10.85 | 39 | 9.9 m / +153 deg | 1.39 m (9.95) | 9.0 m / +21 deg | 10.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001#segment_1, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: A observed track_001#segment_1 start closing in (already the case when first observed).
- t = 0.00 s: A observed track_003 start closing in (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_005#segment_1, which appeared on its left.
- t = 0.05 s: A observed track_005#segment_1 start closing in (already the case when first observed).
- t = 0.35 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.35 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.75 s: A's radar lost track_001#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 0.80 s: A's radar started tracking track_001#segment_2, which appeared on its right.
- t = 0.80 s: A observed track_001#segment_2 start closing in (already the case when first observed).
- t = 0.90 s: A's radar lost track_005#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 0.95 s: A's radar started tracking track_005#segment_2, which appeared in front of it.
- t = 0.95 s: A observed track_005#segment_2 start closing in (already the case when first observed).
- t = 1.45 s: A's time-to-contact with track_005#segment_2 became critical.
- t = 1.50 s: A observed track_001#segment_2 cutting in from the right.
- t = 1.75 s: A observed track_001#segment_2's cut-in from the right settle.
- t = 3.65 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.65 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 5.95 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.95 s: A observed track_001#segment_2 cutting in from the right.
- t = 7.55 s: A observed track_001#segment_2 stop closing in.
- t = 7.70 s: A observed track_001#segment_2's cut-in from the right settle.
- t = 7.70 s: A's radar started tracking track_007, which appeared in front of it.
- t = 7.70 s: A's radar started tracking track_008, which appeared on its left.
- t = 7.75 s: A's collision sensor recorded a contact (peak impulse 1898 N*s).
- t = 7.75 s: A's time-to-contact with track_005#segment_2 stopped being critical.
- t = 7.75 s: A observed track_006 stop closing in.
- t = 7.80 s: A released the accelerator.
- t = 7.80 s: A started braking.
- t = 7.80 s: A's radar lost track_005#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 7.85 s: A's radar started tracking track_005#segment_3, which appeared on its left.
- t = 7.85 s: A observed track_005#segment_3 start closing in (already the case when first observed).
- t = 8.15 s: A observed track_005#segment_3 stop closing in.
- t = 8.20 s: A observed track_001#segment_2 enter its forward path corridor.
- t = 8.20 s: A's time-to-contact with track_001#segment_2 became critical.
- t = 8.45 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 8.45 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 8.55 s: A's radar started tracking track_009, which appeared on its right.
- t = 8.75 s: A's radar lost track_001#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 8.90 s: A stopped moving.
- t = 8.90 s: A came to a stop.
- t = 8.95 s: A's radar started tracking track_010, which appeared on its left.
- t = 8.95 s: A's radar started tracking track_011, which appeared on its right.
- t = 8.95 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.95 s: A observed track_011 start closing in (already the case when first observed).
- t = 9.05 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 9.20 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 9.25 s: A's radar lost track_005#segment_3 (its states are UNKNOWN from then on, not ended).
- t = 9.30 s: A's radar started tracking track_005#segment_4, which appeared in front of it.
- t = 9.95 s: A observed track_011 stop closing in.
- t = 10.00 s: A observed track_010 stop closing in.
- t = 10.85 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 10.85 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
