# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 142.39008847996593 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 42; edges: 69 (PRECEDES 44, SAME_TRACK 25)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_002 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_001#segment_1 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_003 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_LEFT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.05 | TRACK_APPEARED_FRONT | A | track_005#segment_1 | radar | initial_in_ego_path=True |
| A:e08 | 0.55 | CRITICAL_TTC_START | A | track_005#segment_1 | radar |  |
| A:e09 | 0.70 | TRACK_LOST | A | track_001#segment_1 | radar |  |
| A:e10 | 0.75 | TRACK_APPEARED_LEFT | A | track_001#segment_2 | radar | initial_in_ego_path=False |
| A:e11 | 2.30 | TRACK_LOST | A | track_002 | radar |  |
| A:e12 | 2.45 | TRACK_LOST | A | track_003 | radar |  |
| A:e13 | 6.25 | TRACK_LOST | A | track_005#segment_1 | radar |  |
| A:e14 | 6.30 | TRACK_APPEARED_FRONT | A | track_005#segment_2 | radar | initial_in_ego_path=False |
| A:e15 | 6.35 | CRITICAL_TTC_START | A | track_004 | radar |  |
| A:e16 | 6.55 | TRACK_APPEARED_FRONT | A | track_006 | radar | initial_in_ego_path=False |
| A:e17 | 6.65 | EGO_PATH_ENTRY | A | track_006 | radar | geometry=estimated_body |
| A:e18 | 6.95 | CLOSING_START | A | track_004 | radar |  |
| A:e19 | 7.40 | TRACK_APPEARED_RIGHT | A | track_007 | radar | initial_in_ego_path=False |
| A:e20 | 7.55 | EGO_PATH_EXIT | A | track_006 | radar | geometry=estimated_body |
| A:e21 | 7.70 | TRACK_LOST | A | track_006 | radar |  |
| A:e22 | 7.75 | COLLISION | A | - | collision_sensor | peak_impulse=255.03 |
| A:e23 | 7.75 | CRITICAL_TTC_END | A | track_004 | radar |  |
| A:e24 | 7.80 | THROTTLE_END | A | - | controls |  |
| A:e25 | 7.85 | TRACK_APPEARED_FRONT | A | track_008 | radar | initial_in_ego_path=True |
| A:e26 | 7.85 | EGO_PATH_ENTRY | A | track_004 | radar | geometry=estimated_body |
| A:e27 | 7.90 | CLOSING_END | A | track_004 | radar |  |
| A:e28 | 8.25 | TRACK_LOST | A | track_005#segment_2 | radar |  |
| A:e29 | 8.30 | TRACK_APPEARED_FRONT | A | track_005#segment_3 | radar | initial_in_ego_path=True |
| A:e30 | 8.35 | CRITICAL_TTC_START | A | track_008 | radar |  |
| A:e31 | 8.45 | TRACK_APPEARED_LEFT | A | track_009 | radar | initial_in_ego_path=False |
| A:e32 | 8.80 | CRITICAL_TTC_START | A | track_005#segment_3 | radar |  |
| A:e33 | 8.95 | CRITICAL_TTC_END | A | track_008 | radar |  |
| A:e34 | 8.95 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e35 | 9.10 | EGO_PATH_ENTRY | A | track_007 | radar | geometry=estimated_body |
| A:e36 | 9.50 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e37 | 9.75 | CRITICAL_TTC_START | A | track_008 | radar |  |
| A:e38 | 10.25 | EGO_PATH_ENTRY | A | track_008 | radar | geometry=estimated_body |
| A:e39 | 10.45 | CUT_IN_FROM_RIGHT_START | A | track_008 | radar | geometry=estimated_body |
| A:e40 | 11.15 | TRACK_LOST | A | track_010 | radar |  |
| A:e41 | 11.55 | EGO_PATH_EXIT | A | track_007 | radar | geometry=estimated_body |
| A:e42 | 11.60 | EGO_PATH_EXIT | A | track_005#segment_3 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e07
    A:e03 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e31 --PRECEDES--> A:e32
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e07 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e03 --SAME_TRACK--> A:e11
    A:e05 --SAME_TRACK--> A:e12
    A:e07 --SAME_TRACK--> A:e13
    A:e06 --SAME_TRACK--> A:e15
    A:e16 --SAME_TRACK--> A:e17
    A:e06 --SAME_TRACK--> A:e18
    A:e16 --SAME_TRACK--> A:e20
    A:e16 --SAME_TRACK--> A:e21
    A:e06 --SAME_TRACK--> A:e23
    A:e06 --SAME_TRACK--> A:e26
    A:e06 --SAME_TRACK--> A:e27
    A:e14 --SAME_TRACK--> A:e28
    A:e25 --SAME_TRACK--> A:e30
    A:e29 --SAME_TRACK--> A:e32
    A:e25 --SAME_TRACK--> A:e33
    A:e25 --SAME_TRACK--> A:e34
    A:e19 --SAME_TRACK--> A:e35
    A:e25 --SAME_TRACK--> A:e37
    A:e25 --SAME_TRACK--> A:e38
    A:e25 --SAME_TRACK--> A:e39
    A:e36 --SAME_TRACK--> A:e40
    A:e19 --SAME_TRACK--> A:e41
    A:e29 --SAME_TRACK--> A:e42
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_002<br>A:e04 TRACK_APPEARED_LEFT track_001#segment_1<br>A:e05 TRACK_APPEARED_LEFT track_003<br>A:e06 TRACK_APPEARED_LEFT track_004 | ego: not yet observed | - |
| 0.05 | A:e07 TRACK_APPEARED_FRONT track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.00 |
| 0.55 | A:e08 CRITICAL_TTC_START track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: IN_EGO_PATH, CRITICAL_TTC? | 0.50 |
| 0.70 | A:e09 TRACK_LOST track_001#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH | 0.60 |
| 0.75 | A:e10 TRACK_APPEARED_LEFT track_001#segment_2 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 0.70 |
| 2.30 | A:e11 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 2.20 |
| 2.45 | A:e12 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002 | 2.40 |
| 6.25 | A:e13 TRACK_LOST track_005#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003 | 6.20 |
| 6.30 | A:e14 TRACK_APPEARED_FRONT track_005#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 6.20 |
| 6.35 | A:e15 CRITICAL_TTC_START track_004 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 6.30 |
| 6.55 | A:e16 TRACK_APPEARED_FRONT track_006 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 6.50 |
| 6.65 | A:e17 EGO_PATH_ENTRY track_006 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 6.60 |
| 6.95 | A:e18 CLOSING_START track_004 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 6.90 |
| 7.40 | A:e19 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 7.30 |
| 7.55 | A:e20 EGO_PATH_EXIT track_006 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 7.50 |
| 7.70 | A:e21 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 | 7.60 |
| 7.75 | A:e22 COLLISION<br>A:e23 CRITICAL_TTC_END track_004 | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 | 7.70 |
| 7.80 | A:e24 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 | 7.70 |
| 7.85 | A:e25 TRACK_APPEARED_FRONT track_008<br>A:e26 EGO_PATH_ENTRY track_004 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: CLOSING<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 | 7.80 |
| 7.90 | A:e27 CLOSING_END track_004 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 | 7.80 |
| 8.25 | A:e28 TRACK_LOST track_005#segment_2 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 | 8.20 |
| 8.30 | A:e29 TRACK_APPEARED_FRONT track_005#segment_3 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 8.20 |
| 8.35 | A:e30 CRITICAL_TTC_START track_008 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 8.30 |
| 8.45 | A:e31 TRACK_APPEARED_LEFT track_009 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 8.40 |
| 8.80 | A:e32 CRITICAL_TTC_START track_005#segment_3 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 8.70 |
| 8.95 | A:e33 CRITICAL_TTC_END track_008<br>A:e34 EGO_PATH_EXIT track_008 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 8.90 |
| 9.10 | A:e35 EGO_PATH_ENTRY track_007 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 9.00 |
| 9.50 | A:e36 TRACK_APPEARED_LEFT track_010 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 9.40 |
| 9.75 | A:e37 CRITICAL_TTC_START track_008 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 9.70 |
| 10.25 | A:e38 EGO_PATH_ENTRY track_008 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 10.20 |
| 10.45 | A:e39 CUT_IN_FROM_RIGHT_START track_008 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 10.40 |
| 11.15 | A:e40 TRACK_LOST track_010 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 | 11.10 |
| 11.55 | A:e41 EGO_PATH_EXIT track_007 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006, track_010 | 11.50 |
| 11.60 | A:e42 EGO_PATH_EXIT track_005#segment_3 | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006, track_010 | 11.50 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CRITICAL_TTC of track_005#segment_1, since A:e08 (t = 0.55 s); the track was lost at 6.25 s
- EGO_PATH of track_004, since A:e26 (t = 7.85 s)
- CRITICAL_TTC of track_005#segment_3, since A:e32 (t = 8.80 s)
- CRITICAL_TTC of track_008, since A:e37 (t = 9.75 s)
- EGO_PATH of track_008, since A:e38 (t = 10.25 s)
- CUT_IN_FROM_RIGHT of track_008, since A:e39 (t = 10.45 s)

## Tracks lost

- track_005#segment_1 at 6.25 s (A:e13): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_1, track_002, track_003, track_006, track_005#segment_2, track_010

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_004: CRITICAL_TTC_START 6.35, COLLISION 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s)
- track_005#segment_1: CRITICAL_TTC_START 0.55, COLLISION 7.75 (+7.20 s)
- track_005#segment_3: CRITICAL_TTC_START 8.80
- track_006: EGO_PATH_ENTRY 6.65, no critical TTC
- track_007: EGO_PATH_ENTRY 9.10, no critical TTC
- track_008: critical TTC already active before the cut-in: CRITICAL_TTC_START 9.75 <= CUT_IN_FROM_RIGHT_START 10.45 (+0.70 s); EGO_PATH_ENTRY 10.25 after critical TTC (+0.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001#segment_1 | 0.00 | 0.70 | 15 | 12.2 m / -24 deg | 12.22 m (0.00) | 13.7 m / -28 deg | 11.4 m/s |
| track_001#segment_2 | 0.75 | 11.95 | 225 | 13.7 m / -27 deg | 10.85 m (9.85) | 12.4 m / -31 deg | 12.4 m/s |
| track_002 | 0.00 | 2.30 | 38 | 41.4 m / -5 deg | 41.38 m (0.45) | 41.6 m / -5 deg | 12.0 m/s |
| track_003 | 0.00 | 2.45 | 45 | 42.0 m / -9 deg | 41.95 m (0.40) | 42.1 m / -9 deg | 12.0 m/s |
| track_004 | 0.00 | 11.95 | 240 | 2.9 m / -129 deg | 0.00 m (11.65) | 0.0 m / -90 deg | 12.4 m/s |
| track_005#segment_1 | 0.05 | 6.25 | 125 | 10.9 m / +0 deg | 10.85 m (3.20) | 11.0 m / -0 deg | 12.0 m/s |
| track_005#segment_2 | 6.30 | 8.25 | 40 | 10.7 m / +1 deg | 10.35 m (8.25) | 10.3 m / -6 deg | 12.3 m/s |
| track_005#segment_3 | 8.30 | 11.95 | 74 | 9.9 m / -2 deg | 9.54 m (10.60) | 10.0 m / -18 deg | 12.1 m/s |
| track_006 | 6.55 | 7.70 | 23 | 42.1 m / -3 deg | 42.00 m (7.70) | 42.0 m / +4 deg | 12.0 m/s |
| track_007 | 7.40 | 11.95 | 89 | 26.4 m / +8 deg | 24.88 m (11.75) | 24.9 m / -11 deg | 12.1 m/s |
| track_008 | 7.85 | 11.95 | 83 | 11.6 m / +5 deg | 9.84 m (11.95) | 9.8 m / -2 deg | 12.0 m/s |
| track_009 | 8.45 | 11.95 | 66 | 27.0 m / -9 deg | 26.91 m (9.20) | 28.4 m / -26 deg | 12.1 m/s |
| track_010 | 9.50 | 11.15 | 26 | 41.9 m / -7 deg | 41.70 m (10.50) | 41.8 m / -16 deg | 12.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_001#segment_1, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its left.
- t = 0.05 s: A's radar started tracking track_005#segment_1, which appeared in front of it.
- t = 0.55 s: A's time-to-contact with track_005#segment_1 became critical.
- t = 0.70 s: A's radar lost track_001#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 0.75 s: A's radar started tracking track_001#segment_2, which appeared on its left.
- t = 2.30 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 2.45 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 6.25 s: A's radar lost track_005#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: A's radar started tracking track_005#segment_2, which appeared in front of it.
- t = 6.35 s: A's time-to-contact with track_004 became critical.
- t = 6.55 s: A's radar started tracking track_006, which appeared in front of it.
- t = 6.65 s: A observed track_006 enter its forward path corridor.
- t = 6.95 s: A observed track_004 start closing in.
- t = 7.40 s: A's radar started tracking track_007, which appeared on its right.
- t = 7.55 s: A observed track_006 leave its forward path corridor.
- t = 7.70 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 7.75 s: A's collision sensor recorded a contact (peak impulse 255 N*s).
- t = 7.75 s: A's time-to-contact with track_004 stopped being critical.
- t = 7.80 s: A released the accelerator.
- t = 7.85 s: A's radar started tracking track_008, which appeared in front of it.
- t = 7.85 s: A observed track_004 enter its forward path corridor.
- t = 7.90 s: A observed track_004 stop closing in.
- t = 8.25 s: A's radar lost track_005#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 8.30 s: A's radar started tracking track_005#segment_3, which appeared in front of it.
- t = 8.35 s: A's time-to-contact with track_008 became critical.
- t = 8.45 s: A's radar started tracking track_009, which appeared on its left.
- t = 8.80 s: A's time-to-contact with track_005#segment_3 became critical.
- t = 8.95 s: A's time-to-contact with track_008 stopped being critical.
- t = 8.95 s: A observed track_008 leave its forward path corridor.
- t = 9.10 s: A observed track_007 enter its forward path corridor.
- t = 9.50 s: A's radar started tracking track_010, which appeared on its left.
- t = 9.75 s: A's time-to-contact with track_008 became critical.
- t = 10.25 s: A observed track_008 enter its forward path corridor.
- t = 10.45 s: A observed track_008 cutting in from the right.
- t = 11.15 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 11.55 s: A observed track_007 leave its forward path corridor.
- t = 11.60 s: A observed track_005#segment_3 leave its forward path corridor.
