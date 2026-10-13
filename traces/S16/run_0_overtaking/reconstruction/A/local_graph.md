# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 318.1770825125277 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 55; edges: 119 (PRECEDES 84, SAME_TRACK 35)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_003#segment_1 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | TRACK_APPEARED_RIGHT | A | track_005 | radar | initial_in_ego_path=False |
| A:e08 | 0.00 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e09 | 0.40 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e10 | 0.40 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e11 | 0.50 | CRITICAL_TTC_START | A | track_003#segment_1 | radar |  |
| A:e12 | 0.50 | TRACK_LOST | A | track_005 | radar |  |
| A:e13 | 3.60 | TRACK_LOST | A | track_002 | radar |  |
| A:e14 | 3.60 | TRACK_LOST | A | track_004 | radar |  |
| A:e15 | 3.85 | CLOSING_END | A | track_006 | radar |  |
| A:e16 | 4.75 | TRACK_LOST | A | track_003#segment_1 | radar |  |
| A:e17 | 4.80 | TRACK_APPEARED_FRONT | A | track_003#segment_2 | radar | initial_in_ego_path=False |
| A:e18 | 5.10 | CRITICAL_TTC_START | A | track_006 | radar |  |
| A:e19 | 5.30 | TRACK_APPEARED_RIGHT | A | track_007 | radar | initial_in_ego_path=False |
| A:e20 | 5.30 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e21 | 5.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e22 | 5.70 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e23 | 5.90 | TRACK_APPEARED_FRONT | A | track_008 | radar | initial_in_ego_path=True |
| A:e24 | 6.20 | CLOSING_START | A | track_006 | radar |  |
| A:e25 | 6.20 | TRACK_LOST | A | track_003#segment_2 | radar |  |
| A:e26 | 6.25 | TRACK_APPEARED_RIGHT | A | track_003#segment_3 | radar | initial_in_ego_path=True |
| A:e27 | 6.40 | EGO_PATH_ENTRY | A | track_006 | radar | geometry=estimated_body |
| A:e28 | 6.75 | COLLISION | A | - | collision_sensor | peak_impulse=191.84; merged_bursts=[[8.25, 12.44]] |
| A:e29 | 6.75 | CRITICAL_TTC_END | A | track_006 | radar |  |
| A:e30 | 6.75 | EGO_PATH_EXIT | A | track_003#segment_3 | radar | geometry=estimated_body |
| A:e31 | 6.80 | CLOSING_END | A | track_006 | radar |  |
| A:e32 | 6.80 | THROTTLE_END | A | - | controls |  |
| A:e33 | 6.80 | BRAKE_START | A | - | controls |  |
| A:e34 | 6.85 | EGO_PATH_ENTRY | A | track_003#segment_3 | radar | geometry=estimated_body |
| A:e35 | 6.85 | CRITICAL_TTC_START | A | track_003#segment_3 | radar |  |
| A:e36 | 7.20 | CLOSING_END | A | track_007 | radar |  |
| A:e37 | 7.45 | CRITICAL_TTC_END | A | track_003#segment_3 | radar |  |
| A:e38 | 7.55 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e39 | 7.55 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e40 | 7.90 | TRACK_APPEARED_FRONT | A | track_009 | radar | initial_in_ego_path=True |
| A:e41 | 7.95 | EGO_PATH_EXIT | A | track_006 | radar | geometry=estimated_body |
| A:e42 | 7.95 | MOVING_END | A | - | ego |  |
| A:e43 | 7.95 | STOP_START | A | - | ego |  |
| A:e44 | 8.05 | EGO_PATH_ENTRY | A | track_006 | radar | geometry=estimated_body |
| A:e45 | 8.30 | TRACK_APPEARED_RIGHT | A | track_010 | radar | initial_in_ego_path=False |
| A:e46 | 8.30 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e47 | 8.35 | EGO_PATH_ENTRY | A | track_007 | radar | geometry=estimated_body |
| A:e48 | 8.55 | TRACK_APPEARED_LEFT | A | track_011 | radar | initial_in_ego_path=False |
| A:e49 | 9.95 | EGO_PATH_EXIT | A | track_003#segment_3 | radar | geometry=estimated_body |
| A:e50 | 9.95 | TRACK_LOST | A | track_011 | radar |  |
| A:e51 | 10.10 | EGO_PATH_EXIT | A | track_009 | radar | geometry=estimated_body |
| A:e52 | 10.15 | CLOSING_END | A | track_010 | radar |  |
| A:e53 | 11.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e54 | 11.35 | EGO_PATH_EXIT | A | track_007 | radar | geometry=estimated_body |
| A:e55 | 11.85 | TRACK_LOST | A | track_008 | radar |  |

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
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e32
    A:e28 --PRECEDES--> A:e33
    A:e29 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e32
    A:e29 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e44
    A:e44 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e47
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e48 --PRECEDES--> A:e50
    A:e49 --PRECEDES--> A:e51
    A:e50 --PRECEDES--> A:e51
    A:e51 --PRECEDES--> A:e52
    A:e52 --PRECEDES--> A:e53
    A:e53 --PRECEDES--> A:e54
    A:e54 --PRECEDES--> A:e55
    A:e06 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e11
    A:e07 --SAME_TRACK--> A:e12
    A:e05 --SAME_TRACK--> A:e13
    A:e06 --SAME_TRACK--> A:e14
    A:e09 --SAME_TRACK--> A:e15
    A:e03 --SAME_TRACK--> A:e16
    A:e09 --SAME_TRACK--> A:e18
    A:e19 --SAME_TRACK--> A:e20
    A:e04 --SAME_TRACK--> A:e21
    A:e04 --SAME_TRACK--> A:e22
    A:e09 --SAME_TRACK--> A:e24
    A:e17 --SAME_TRACK--> A:e25
    A:e09 --SAME_TRACK--> A:e27
    A:e09 --SAME_TRACK--> A:e29
    A:e26 --SAME_TRACK--> A:e30
    A:e09 --SAME_TRACK--> A:e31
    A:e26 --SAME_TRACK--> A:e34
    A:e26 --SAME_TRACK--> A:e35
    A:e19 --SAME_TRACK--> A:e36
    A:e26 --SAME_TRACK--> A:e37
    A:e04 --SAME_TRACK--> A:e38
    A:e23 --SAME_TRACK--> A:e39
    A:e09 --SAME_TRACK--> A:e41
    A:e09 --SAME_TRACK--> A:e44
    A:e45 --SAME_TRACK--> A:e46
    A:e19 --SAME_TRACK--> A:e47
    A:e26 --SAME_TRACK--> A:e49
    A:e48 --SAME_TRACK--> A:e50
    A:e40 --SAME_TRACK--> A:e51
    A:e45 --SAME_TRACK--> A:e52
    A:e04 --SAME_TRACK--> A:e53
    A:e19 --SAME_TRACK--> A:e54
    A:e23 --SAME_TRACK--> A:e55
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_003#segment_1<br>A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 TRACK_APPEARED_LEFT track_002<br>A:e06 TRACK_APPEARED_RIGHT track_004<br>A:e07 TRACK_APPEARED_RIGHT track_005<br>A:e08 CLOSING_START track_004 | ego: not yet observed | - |
| 0.40 | A:e09 TRACK_APPEARED_LEFT track_006<br>A:e10 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003#segment_1: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.30 |
| 0.50 | A:e11 CRITICAL_TTC_START track_003#segment_1<br>A:e12 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003#segment_1: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? | 0.40 |
| 3.60 | A:e13 TRACK_LOST track_002<br>A:e14 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005 | 3.50 |
| 3.85 | A:e15 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 3.80 |
| 4.75 | A:e16 TRACK_LOST track_003#segment_1 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 4.70 |
| 4.80 | A:e17 TRACK_APPEARED_FRONT track_003#segment_2 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 4.70 |
| 5.10 | A:e18 CRITICAL_TTC_START track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 5.00 |
| 5.30 | A:e19 TRACK_APPEARED_RIGHT track_007<br>A:e20 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 5.20 |
| 5.60 | A:e21 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 5.50 |
| 5.70 | A:e22 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 5.60 |
| 5.90 | A:e23 TRACK_APPEARED_FRONT track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 5.80 |
| 6.20 | A:e24 CLOSING_START track_006<br>A:e25 TRACK_LOST track_003#segment_2 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 | 6.10 |
| 6.25 | A:e26 TRACK_APPEARED_RIGHT track_003#segment_3 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 6.20 |
| 6.40 | A:e27 EGO_PATH_ENTRY track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 6.30 |
| 6.75 | A:e28 COLLISION<br>A:e29 CRITICAL_TTC_END track_006<br>A:e30 EGO_PATH_EXIT track_003#segment_3 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 6.70 |
| 6.80 | A:e31 CLOSING_END track_006<br>A:e32 THROTTLE_END<br>A:e33 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: no active state<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 6.70 |
| 6.85 | A:e34 EGO_PATH_ENTRY track_003#segment_3<br>A:e35 CRITICAL_TTC_START track_003#segment_3 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 6.80 |
| 7.20 | A:e36 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 7.10 |
| 7.45 | A:e37 CRITICAL_TTC_END track_003#segment_3 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 7.40 |
| 7.55 | A:e38 EGO_PATH_EXIT track_001<br>A:e39 EGO_PATH_EXIT track_008 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 7.50 |
| 7.90 | A:e40 TRACK_APPEARED_FRONT track_009 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 7.80 |
| 7.95 | A:e41 EGO_PATH_EXIT track_006<br>A:e42 MOVING_END<br>A:e43 STOP_START | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 7.90 |
| 8.05 | A:e44 EGO_PATH_ENTRY track_006 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 8.00 |
| 8.30 | A:e45 TRACK_APPEARED_RIGHT track_010<br>A:e46 CLOSING_START track_010 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 8.20 |
| 8.35 | A:e47 EGO_PATH_ENTRY track_007 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 8.30 |
| 8.55 | A:e48 TRACK_APPEARED_LEFT track_011 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 8.50 |
| 9.95 | A:e49 EGO_PATH_EXIT track_003#segment_3<br>A:e50 TRACK_LOST track_011 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 | 9.90 |
| 10.10 | A:e51 EGO_PATH_EXIT track_009 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 | 10.00 |
| 10.15 | A:e52 CLOSING_END track_010 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 | 10.10 |
| 11.20 | A:e53 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 | 11.10 |
| 11.35 | A:e54 EGO_PATH_EXIT track_007 | ego: STOP, BRAKE<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 | 11.30 |
| 11.85 | A:e55 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 | 11.80 |

## States still active when observation ended

- CLOSING of track_004, since A:e08 (t = 0.00 s); the track was lost at 3.60 s
- CRITICAL_TTC of track_003#segment_1, since A:e11 (t = 0.50 s); the track was lost at 4.75 s
- CRITICAL_TTC of track_001, since A:e21 (t = 5.60 s); the track was lost at 11.20 s
- BRAKE, since A:e33 (t = 6.80 s)
- STOP, since A:e43 (t = 7.95 s)
- EGO_PATH of track_006, since A:e44 (t = 8.05 s)

## Tracks lost

- track_004 at 3.60 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003#segment_1 at 4.75 s (A:e16): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 11.20 s (A:e53): CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_002, track_003#segment_2, track_011, track_008

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.60, COLLISION 6.75 (+1.15 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.10 s)
- track_003#segment_1: CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s)
- track_003#segment_3: CRITICAL_TTC_START 6.85; EGO_PATH_ENTRY 6.85 together with critical TTC (+0.00 s)
- track_006: CRITICAL_TTC_START 5.10, COLLISION 6.75 (+1.65 s); EGO_PATH_ENTRY 6.40 after critical TTC (+1.30 s)
- track_007: EGO_PATH_ENTRY 8.35, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.20 | 215 | 2.5 m / -45 deg | 2.55 m (0.00) | 64.2 m / -13 deg | 14.1 m/s |
| track_002 | 0.00 | 3.60 | 70 | 16.4 m / -10 deg | 16.43 m (0.00) | 23.6 m / -8 deg | 13.9 m/s |
| track_003#segment_1 | 0.00 | 4.75 | 96 | 11.9 m / +0 deg | 11.93 m (0.50) | 12.3 m / +0 deg | 12.0 m/s |
| track_003#segment_2 | 4.80 | 6.20 | 29 | 12.5 m / -0 deg | 12.52 m (4.80) | 12.7 m / +8 deg | 12.1 m/s |
| track_003#segment_3 | 6.25 | 11.95 | 110 | 12.3 m / +8 deg | 12.30 m (7.00) | 64.0 m / -10 deg | 12.2 m/s |
| track_004 | 0.00 | 3.60 | 72 | 32.1 m / +5 deg | 24.86 m (3.60) | 24.9 m / +8 deg | 9.9 m/s |
| track_005 | 0.00 | 0.50 | 11 | 8.4 m / +152 deg | 8.40 m (0.00) | 9.3 m / +154 deg | 9.9 m/s |
| track_006 | 0.40 | 11.95 | 232 | 9.2 m / -153 deg | 0.43 m (7.80) | 0.6 m / -64 deg | 13.8 m/s |
| track_007 | 5.30 | 11.95 | 129 | 22.1 m / +9 deg | 18.72 m (7.30) | 60.1 m / -6 deg | 10.3 m/s |
| track_008 | 5.90 | 11.85 | 91 | 28.0 m / -2 deg | 28.04 m (5.90) | 78.1 m / -13 deg | 14.0 m/s |
| track_009 | 7.90 | 11.95 | 41 | 34.7 m / +4 deg | 34.71 m (7.90) | 73.6 m / -9 deg | 10.2 m/s |
| track_010 | 8.30 | 11.95 | 74 | 16.7 m / +156 deg | 2.51 m (10.10) | 15.1 m / +11 deg | 10.0 m/s |
| track_011 | 8.55 | 9.95 | 18 | 45.1 m / -11 deg | 45.14 m (8.55) | 64.3 m / -13 deg | 13.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_003#segment_1, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_005, which appeared on its right.
- t = 0.00 s: A observed track_004 start closing in (already the case when first observed).
- t = 0.40 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.40 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.50 s: A's time-to-contact with track_003#segment_1 became critical.
- t = 0.50 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.60 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.60 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.85 s: A observed track_006 stop closing in.
- t = 4.75 s: A's radar lost track_003#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 4.80 s: A's radar started tracking track_003#segment_2, which appeared in front of it.
- t = 5.10 s: A's time-to-contact with track_006 became critical.
- t = 5.30 s: A's radar started tracking track_007, which appeared on its right.
- t = 5.30 s: A observed track_007 start closing in (already the case when first observed).
- t = 5.60 s: A's time-to-contact with track_001 became critical.
- t = 5.70 s: A observed track_001 enter its forward path corridor.
- t = 5.90 s: A's radar started tracking track_008, which appeared in front of it.
- t = 6.20 s: A observed track_006 start closing in.
- t = 6.20 s: A's radar lost track_003#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 6.25 s: A's radar started tracking track_003#segment_3, which appeared on its right.
- t = 6.40 s: A observed track_006 enter its forward path corridor.
- t = 6.75 s: A's collision sensor recorded a contact (peak impulse 192 N*s).
- t = 6.75 s: A's time-to-contact with track_006 stopped being critical.
- t = 6.75 s: A observed track_003#segment_3 leave its forward path corridor.
- t = 6.80 s: A observed track_006 stop closing in.
- t = 6.80 s: A released the accelerator.
- t = 6.80 s: A started braking.
- t = 6.85 s: A observed track_003#segment_3 enter its forward path corridor.
- t = 6.85 s: A's time-to-contact with track_003#segment_3 became critical.
- t = 7.20 s: A observed track_007 stop closing in.
- t = 7.45 s: A's time-to-contact with track_003#segment_3 stopped being critical.
- t = 7.55 s: A observed track_001 leave its forward path corridor.
- t = 7.55 s: A observed track_008 leave its forward path corridor.
- t = 7.90 s: A's radar started tracking track_009, which appeared in front of it.
- t = 7.95 s: A observed track_006 leave its forward path corridor.
- t = 7.95 s: A stopped moving.
- t = 7.95 s: A came to a stop.
- t = 8.05 s: A observed track_006 enter its forward path corridor.
- t = 8.30 s: A's radar started tracking track_010, which appeared on its right.
- t = 8.30 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.35 s: A observed track_007 enter its forward path corridor.
- t = 8.55 s: A's radar started tracking track_011, which appeared on its left.
- t = 9.95 s: A observed track_003#segment_3 leave its forward path corridor.
- t = 9.95 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 10.10 s: A observed track_009 leave its forward path corridor.
- t = 10.15 s: A observed track_010 stop closing in.
- t = 11.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 11.35 s: A observed track_007 leave its forward path corridor.
- t = 11.85 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
