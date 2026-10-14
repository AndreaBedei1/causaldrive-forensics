# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 63.627261225134134 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 42; edges: 77 (PRECEDES 52, SAME_TRACK 25)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_003 | radar | initial_in_ego_path=False |
| A:e06 | 0.05 | TRACK_APPEARED_LEFT | A | track_004#segment_1 | radar | initial_in_ego_path=False |
| A:e07 | 0.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 4.80 | TRACK_APPEARED_LEFT | A | track_005 | radar | initial_in_ego_path=False |
| A:e09 | 6.35 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e10 | 6.70 | CRITICAL_TTC_START | A | track_004#segment_1 | radar |  |
| A:e11 | 6.80 | TRACK_LOST | A | track_004#segment_1 | radar |  |
| A:e12 | 6.85 | TRACK_APPEARED_LEFT | A | track_004#segment_2 | radar | initial_in_ego_path=False |
| A:e13 | 6.95 | CLOSING_START | A | track_003 | radar |  |
| A:e14 | 7.05 | TRACK_APPEARED_FRONT | A | track_006 | radar | initial_in_ego_path=True |
| A:e15 | 7.05 | TRACK_APPEARED_LEFT | A | track_007 | radar | initial_in_ego_path=False |
| A:e16 | 7.25 | TRACK_LOST | A | track_005 | radar |  |
| A:e17 | 7.45 | TRACK_LOST | A | track_007 | radar |  |
| A:e18 | 7.60 | EGO_PATH_EXIT | A | track_006 | radar | geometry=estimated_body |
| A:e19 | 7.60 | TRACK_APPEARED_RIGHT | A | track_008 | radar | initial_in_ego_path=False |
| A:e20 | 7.60 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e21 | 7.70 | TRACK_LOST | A | track_006 | radar |  |
| A:e22 | 7.75 | COLLISION | A | - | collision_sensor | peak_impulse=254.40 |
| A:e23 | 7.75 | CRITICAL_TTC_END | A | track_003 | radar |  |
| A:e24 | 7.75 | TRACK_APPEARED_RIGHT | A | track_009 | radar | initial_in_ego_path=False |
| A:e25 | 7.80 | THROTTLE_END | A | - | controls |  |
| A:e26 | 7.80 | EGO_PATH_ENTRY | A | track_009 | radar | geometry=estimated_body |
| A:e27 | 7.85 | EGO_PATH_ENTRY | A | track_003 | radar | geometry=estimated_body |
| A:e28 | 7.90 | CLOSING_END | A | track_003 | radar |  |
| A:e29 | 8.45 | TRACK_LOST | A | track_004#segment_2 | radar |  |
| A:e30 | 8.50 | TRACK_APPEARED_FRONT | A | track_004#segment_3 | radar | initial_in_ego_path=True |
| A:e31 | 8.55 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e32 | 9.00 | EGO_PATH_ENTRY | A | track_008 | radar | geometry=estimated_body |
| A:e33 | 9.00 | CRITICAL_TTC_START | A | track_004#segment_3 | radar |  |
| A:e34 | 9.15 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e35 | 9.15 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e36 | 9.95 | TRACK_APPEARED_LEFT | A | track_011 | radar | initial_in_ego_path=False |
| A:e37 | 10.15 | CRITICAL_TTC_START | A | track_009 | radar |  |
| A:e38 | 10.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e39 | 10.95 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e40 | 11.15 | TRACK_LOST | A | track_011 | radar |  |
| A:e41 | 11.55 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e42 | 11.60 | EGO_PATH_EXIT | A | track_004#segment_3 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e31 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e03 --SAME_TRACK--> A:e07
    A:e05 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
    A:e06 --SAME_TRACK--> A:e11
    A:e05 --SAME_TRACK--> A:e13
    A:e08 --SAME_TRACK--> A:e16
    A:e15 --SAME_TRACK--> A:e17
    A:e14 --SAME_TRACK--> A:e18
    A:e04 --SAME_TRACK--> A:e20
    A:e14 --SAME_TRACK--> A:e21
    A:e05 --SAME_TRACK--> A:e23
    A:e24 --SAME_TRACK--> A:e26
    A:e05 --SAME_TRACK--> A:e27
    A:e05 --SAME_TRACK--> A:e28
    A:e12 --SAME_TRACK--> A:e29
    A:e19 --SAME_TRACK--> A:e32
    A:e30 --SAME_TRACK--> A:e33
    A:e03 --SAME_TRACK--> A:e34
    A:e03 --SAME_TRACK--> A:e35
    A:e24 --SAME_TRACK--> A:e37
    A:e03 --SAME_TRACK--> A:e38
    A:e03 --SAME_TRACK--> A:e39
    A:e36 --SAME_TRACK--> A:e40
    A:e19 --SAME_TRACK--> A:e41
    A:e30 --SAME_TRACK--> A:e42
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_001<br>A:e04 TRACK_APPEARED_LEFT track_002<br>A:e05 TRACK_APPEARED_LEFT track_003 | ego: not yet observed | - |
| 0.05 | A:e06 TRACK_APPEARED_LEFT track_004#segment_1 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.00 |
| 0.50 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004#segment_1: CRITICAL_TTC? | 0.40 |
| 4.80 | A:e08 TRACK_APPEARED_LEFT track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state | 4.70 |
| 6.35 | A:e09 CRITICAL_TTC_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state<br>track_005: no active state | 6.30 |
| 6.70 | A:e10 CRITICAL_TTC_START track_004#segment_1 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_1: no active state<br>track_005: no active state | 6.60 |
| 6.80 | A:e11 TRACK_LOST track_004#segment_1 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_1: CRITICAL_TTC<br>track_005: no active state | 6.70 |
| 6.85 | A:e12 TRACK_APPEARED_LEFT track_004#segment_2 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 | 6.80 |
| 6.95 | A:e13 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 | 6.90 |
| 7.05 | A:e14 TRACK_APPEARED_FRONT track_006<br>A:e15 TRACK_APPEARED_LEFT track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 | 7.00 |
| 7.25 | A:e16 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1 | 7.20 |
| 7.45 | A:e17 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005 | 7.40 |
| 7.60 | A:e18 EGO_PATH_EXIT track_006<br>A:e19 TRACK_APPEARED_RIGHT track_008<br>A:e20 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_007 | 7.50 |
| 7.70 | A:e21 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_007 | 7.60 |
| 7.75 | A:e22 COLLISION<br>A:e23 CRITICAL_TTC_END track_003<br>A:e24 TRACK_APPEARED_RIGHT track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 | 7.70 |
| 7.80 | A:e25 THROTTLE_END<br>A:e26 EGO_PATH_ENTRY track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 | 7.70 |
| 7.85 | A:e27 EGO_PATH_ENTRY track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 | 7.80 |
| 7.90 | A:e28 CLOSING_END track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING, IN_EGO_PATH<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 | 7.80 |
| 8.45 | A:e29 TRACK_LOST track_004#segment_2 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 | 8.40 |
| 8.50 | A:e30 TRACK_APPEARED_FRONT track_004#segment_3 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 8.40 |
| 8.55 | A:e31 TRACK_APPEARED_LEFT track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 8.50 |
| 9.00 | A:e32 EGO_PATH_ENTRY track_008<br>A:e33 CRITICAL_TTC_START track_004#segment_3 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 8.90 |
| 9.15 | A:e34 CRITICAL_TTC_END track_001<br>A:e35 EGO_PATH_EXIT track_001 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 9.10 |
| 9.95 | A:e36 TRACK_APPEARED_LEFT track_011 | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 9.90 |
| 10.15 | A:e37 CRITICAL_TTC_START track_009 | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 10.10 |
| 10.55 | A:e38 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 10.50 |
| 10.95 | A:e39 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CRITICAL_TTC<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 10.90 |
| 11.15 | A:e40 TRACK_LOST track_011 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 | 11.10 |
| 11.55 | A:e41 EGO_PATH_EXIT track_008 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007, track_011 | 11.50 |
| 11.60 | A:e42 EGO_PATH_EXIT track_004#segment_3 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007, track_011 | 11.50 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CRITICAL_TTC of track_004#segment_1, since A:e10 (t = 6.70 s); the track was lost at 6.80 s
- CRITICAL_TTC of track_002, since A:e20 (t = 7.60 s)
- EGO_PATH of track_009, since A:e26 (t = 7.80 s)
- EGO_PATH of track_003, since A:e27 (t = 7.85 s)
- CRITICAL_TTC of track_004#segment_3, since A:e33 (t = 9.00 s)
- CRITICAL_TTC of track_009, since A:e37 (t = 10.15 s)
- CRITICAL_TTC of track_001, since A:e38 (t = 10.55 s)
- EGO_PATH of track_001, since A:e39 (t = 10.95 s)

## Tracks lost

- track_004#segment_1 at 6.80 s (A:e11): CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_007, track_006, track_004#segment_2, track_011

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 10.95 after critical TTC (+10.45 s)
- track_002: CRITICAL_TTC_START 7.60, COLLISION 7.75 (+0.15 s)
- track_003: CRITICAL_TTC_START 6.35, COLLISION 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s)
- track_004#segment_1: CRITICAL_TTC_START 6.70, COLLISION 7.75 (+1.05 s)
- track_004#segment_3: CRITICAL_TTC_START 9.00
- track_008: EGO_PATH_ENTRY 9.00, no critical TTC
- track_009: CRITICAL_TTC_START 10.15; EGO_PATH_ENTRY 7.80 before critical TTC (-2.35 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 3.2 m / +0 deg | 1.42 m (11.95) | 1.4 m / +6 deg | 12.3 m/s |
| track_002 | 0.00 | 11.95 | 240 | 12.3 m / -27 deg | 10.91 m (9.85) | 12.5 m / -31 deg | 12.4 m/s |
| track_003 | 0.00 | 11.95 | 240 | 3.0 m / -129 deg | 0.01 m (11.60) | 0.0 m / -90 deg | 12.4 m/s |
| track_004#segment_1 | 0.05 | 6.80 | 136 | 11.1 m / -14 deg | 10.49 m (4.70) | 10.5 m / -11 deg | 12.3 m/s |
| track_004#segment_2 | 6.85 | 8.45 | 33 | 10.3 m / -9 deg | 9.92 m (8.45) | 9.9 m / -3 deg | 12.1 m/s |
| track_004#segment_3 | 8.50 | 11.95 | 70 | 9.9 m / -2 deg | 9.54 m (10.60) | 10.0 m / -18 deg | 12.2 m/s |
| track_005 | 4.80 | 7.25 | 50 | 12.8 m / -154 deg | 12.45 m (7.25) | 12.4 m / -149 deg | 12.2 m/s |
| track_006 | 7.05 | 7.70 | 14 | 42.0 m / -1 deg | 41.99 m (7.70) | 42.0 m / +5 deg | 12.4 m/s |
| track_007 | 7.05 | 7.45 | 9 | 20.7 m / -157 deg | 20.57 m (7.45) | 20.6 m / -156 deg | 11.8 m/s |
| track_008 | 7.60 | 11.95 | 87 | 26.4 m / +9 deg | 24.90 m (11.75) | 24.9 m / -11 deg | 12.1 m/s |
| track_009 | 7.75 | 11.95 | 85 | 11.3 m / +11 deg | 9.88 m (11.95) | 9.9 m / -5 deg | 12.0 m/s |
| track_010 | 8.55 | 11.95 | 65 | 27.0 m / -8 deg | 26.93 m (9.20) | 28.4 m / -26 deg | 12.1 m/s |
| track_011 | 9.95 | 11.15 | 21 | 41.5 m / -8 deg | 41.46 m (10.40) | 41.6 m / -16 deg | 12.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its left.
- t = 0.05 s: A's radar started tracking track_004#segment_1, which appeared on its left.
- t = 0.50 s: A's time-to-contact with track_001 became critical.
- t = 4.80 s: A's radar started tracking track_005, which appeared on its left.
- t = 6.35 s: A's time-to-contact with track_003 became critical.
- t = 6.70 s: A's time-to-contact with track_004#segment_1 became critical.
- t = 6.80 s: A's radar lost track_004#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 6.85 s: A's radar started tracking track_004#segment_2, which appeared on its left.
- t = 6.95 s: A observed track_003 start closing in.
- t = 7.05 s: A's radar started tracking track_006, which appeared in front of it.
- t = 7.05 s: A's radar started tracking track_007, which appeared on its left.
- t = 7.25 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 7.45 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 7.60 s: A observed track_006 leave its forward path corridor.
- t = 7.60 s: A's radar started tracking track_008, which appeared on its right.
- t = 7.60 s: A's time-to-contact with track_002 became critical.
- t = 7.70 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 7.75 s: A's collision sensor recorded a contact (peak impulse 254 N*s).
- t = 7.75 s: A's time-to-contact with track_003 stopped being critical.
- t = 7.75 s: A's radar started tracking track_009, which appeared on its right.
- t = 7.80 s: A released the accelerator.
- t = 7.80 s: A observed track_009 enter its forward path corridor.
- t = 7.85 s: A observed track_003 enter its forward path corridor.
- t = 7.90 s: A observed track_003 stop closing in.
- t = 8.45 s: A's radar lost track_004#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 8.50 s: A's radar started tracking track_004#segment_3, which appeared in front of it.
- t = 8.55 s: A's radar started tracking track_010, which appeared on its left.
- t = 9.00 s: A observed track_008 enter its forward path corridor.
- t = 9.00 s: A's time-to-contact with track_004#segment_3 became critical.
- t = 9.15 s: A's time-to-contact with track_001 stopped being critical.
- t = 9.15 s: A observed track_001 leave its forward path corridor.
- t = 9.95 s: A's radar started tracking track_011, which appeared on its left.
- t = 10.15 s: A's time-to-contact with track_009 became critical.
- t = 10.55 s: A's time-to-contact with track_001 became critical.
- t = 10.95 s: A observed track_001 enter its forward path corridor.
- t = 11.15 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 11.55 s: A observed track_008 leave its forward path corridor.
- t = 11.60 s: A observed track_004#segment_3 leave its forward path corridor.
