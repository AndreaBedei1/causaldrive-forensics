# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 63.627261225134134 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 14 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 43; edges: 78 (PRECEDES 53, SAME_TRACK 25)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_004 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_LEFT | B | track_005 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e07 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e08 | 0.05 | TRACK_APPEARED_LEFT | B | track_006 | radar | initial_in_ego_path=False |
| B:e09 | 0.05 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e10 | 0.15 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e11 | 0.20 | TRACK_APPEARED_FRONT | B | track_009 | radar | initial_in_ego_path=False |
| B:e12 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e13 | 2.20 | TRACK_LOST | B | track_009 | radar |  |
| B:e14 | 3.65 | TRACK_LOST | B | track_004 | radar |  |
| B:e15 | 3.80 | TRACK_LOST | B | track_008 | radar |  |
| B:e16 | 6.40 | TRACK_APPEARED_LEFT | B | track_010 | radar | initial_in_ego_path=False |
| B:e17 | 6.50 | TRACK_APPEARED_RIGHT | B | track_011 | radar | initial_in_ego_path=False |
| B:e18 | 6.60 | TRACK_APPEARED_FRONT | B | track_012 | radar | initial_in_ego_path=False |
| B:e19 | 6.70 | TRACK_LOST | B | track_005 | radar |  |
| B:e20 | 7.00 | TRACK_LOST | B | track_012 | radar |  |
| B:e21 | 7.05 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e22 | 7.15 | CLOSING_START | B | track_002 | radar |  |
| B:e23 | 7.75 | COLLISION | B | - | collision_sensor | peak_impulse=254.40 |
| B:e24 | 7.75 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e25 | 7.80 | THROTTLE_END | B | - | controls |  |
| B:e26 | 7.85 | CLOSING_END | B | track_002 | radar |  |
| B:e27 | 7.85 | TRACK_APPEARED_LEFT | B | track_013 | radar | initial_in_ego_path=False |
| B:e28 | 8.00 | EGO_PATH_ENTRY | B | track_010 | radar | geometry=estimated_body |
| B:e29 | 8.15 | TRACK_APPEARED_FRONT | B | track_014 | radar | initial_in_ego_path=True |
| B:e30 | 8.70 | EGO_PATH_ENTRY | B | track_006 | radar | geometry=estimated_body |
| B:e31 | 8.70 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e32 | 8.85 | TRACK_LOST | B | track_011 | radar |  |
| B:e33 | 9.00 | TRACK_LOST | B | track_013 | radar |  |
| B:e34 | 9.35 | TRACK_LOST | B | track_010 | radar |  |
| B:e35 | 9.55 | EGO_PATH_EXIT | B | track_014 | radar | geometry=estimated_body |
| B:e36 | 10.55 | CRITICAL_TTC_START | B | track_007 | radar |  |
| B:e37 | 10.60 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e38 | 10.60 | EGO_PATH_EXIT | B | track_006 | radar | geometry=estimated_body |
| B:e39 | 11.05 | EGO_PATH_ENTRY | B | track_007 | radar | geometry=estimated_body |
| B:e40 | 11.10 | CLOSING_START | B | track_003 | radar |  |
| B:e41 | 11.30 | CRITICAL_TTC_START | B | track_003 | radar |  |
| B:e42 | 11.60 | CLOSING_START | B | track_002 | radar |  |
| B:e43 | 11.80 | EGO_PATH_ENTRY | B | track_003 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e08
    B:e01 --PRECEDES--> B:e09
    B:e02 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e05 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e36 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e39
    B:e39 --PRECEDES--> B:e40
    B:e40 --PRECEDES--> B:e41
    B:e41 --PRECEDES--> B:e42
    B:e42 --PRECEDES--> B:e43
    B:e03 --SAME_TRACK--> B:e12
    B:e11 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e10 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e19
    B:e18 --SAME_TRACK--> B:e20
    B:e06 --SAME_TRACK--> B:e21
    B:e06 --SAME_TRACK--> B:e22
    B:e06 --SAME_TRACK--> B:e24
    B:e06 --SAME_TRACK--> B:e26
    B:e16 --SAME_TRACK--> B:e28
    B:e08 --SAME_TRACK--> B:e30
    B:e08 --SAME_TRACK--> B:e31
    B:e17 --SAME_TRACK--> B:e32
    B:e27 --SAME_TRACK--> B:e33
    B:e16 --SAME_TRACK--> B:e34
    B:e29 --SAME_TRACK--> B:e35
    B:e09 --SAME_TRACK--> B:e36
    B:e08 --SAME_TRACK--> B:e37
    B:e08 --SAME_TRACK--> B:e38
    B:e09 --SAME_TRACK--> B:e39
    B:e07 --SAME_TRACK--> B:e40
    B:e07 --SAME_TRACK--> B:e41
    B:e06 --SAME_TRACK--> B:e42
    B:e07 --SAME_TRACK--> B:e43
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_LEFT track_004<br>B:e05 TRACK_APPEARED_LEFT track_005<br>B:e06 TRACK_APPEARED_RIGHT track_002<br>B:e07 TRACK_APPEARED_RIGHT track_003 | ego: not yet observed | - |
| 0.05 | B:e08 TRACK_APPEARED_LEFT track_006<br>B:e09 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.00 |
| 0.15 | B:e10 TRACK_APPEARED_RIGHT track_008 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? | 0.10 |
| 0.20 | B:e11 TRACK_APPEARED_FRONT track_009 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC? | 0.10 |
| 0.50 | B:e12 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC? | 0.40 |
| 2.20 | B:e13 TRACK_LOST track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state | 2.10 |
| 3.65 | B:e14 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_009 | 3.60 |
| 3.80 | B:e15 TRACK_LOST track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_004, track_009 | 3.70 |
| 6.40 | B:e16 TRACK_APPEARED_LEFT track_010 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_008, track_009 | 6.30 |
| 6.50 | B:e17 TRACK_APPEARED_RIGHT track_011 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 | 6.40 |
| 6.60 | B:e18 TRACK_APPEARED_FRONT track_012 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 | 6.50 |
| 6.70 | B:e19 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track_011: CRITICAL_TTC?<br>track_012: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_008, track_009 | 6.60 |
| 7.00 | B:e20 TRACK_LOST track_012 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: CRITICAL_TTC?<br>track_012: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 | 6.90 |
| 7.05 | B:e21 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.00 |
| 7.15 | B:e22 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.10 |
| 7.75 | B:e23 COLLISION<br>B:e24 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.70 |
| 7.80 | B:e25 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.70 |
| 7.85 | B:e26 CLOSING_END track_002<br>B:e27 TRACK_APPEARED_LEFT track_013 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.80 |
| 8.00 | B:e28 EGO_PATH_ENTRY track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 7.90 |
| 8.15 | B:e29 TRACK_APPEARED_FRONT track_014 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 8.10 |
| 8.70 | B:e30 EGO_PATH_ENTRY track_006<br>B:e31 CRITICAL_TTC_START track_006 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 8.60 |
| 8.85 | B:e32 TRACK_LOST track_011 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 | 8.80 |
| 9.00 | B:e33 TRACK_LOST track_013 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_013: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_011, track_012 | 8.90 |
| 9.35 | B:e34 TRACK_LOST track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_011, track_012, track_013 | 9.30 |
| 9.55 | B:e35 EGO_PATH_EXIT track_014 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 9.50 |
| 10.55 | B:e36 CRITICAL_TTC_START track_007 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 10.50 |
| 10.60 | B:e37 CRITICAL_TTC_END track_006<br>B:e38 EGO_PATH_EXIT track_006 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 10.50 |
| 11.05 | B:e39 EGO_PATH_ENTRY track_007 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: CRITICAL_TTC<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 11.00 |
| 11.10 | B:e40 CLOSING_START track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 11.00 |
| 11.30 | B:e41 CRITICAL_TTC_START track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 11.20 |
| 11.60 | B:e42 CLOSING_START track_002 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 11.50 |
| 11.80 | B:e43 EGO_PATH_ENTRY track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 | 11.70 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)
- CRITICAL_TTC of track_001, since B:e12 (t = 0.50 s)
- EGO_PATH of track_010, since B:e28 (t = 8.00 s); the track was lost at 9.35 s
- CRITICAL_TTC of track_007, since B:e36 (t = 10.55 s)
- EGO_PATH of track_007, since B:e39 (t = 11.05 s)
- CLOSING of track_003, since B:e40 (t = 11.10 s)
- CRITICAL_TTC of track_003, since B:e41 (t = 11.30 s)
- CLOSING of track_002, since B:e42 (t = 11.60 s)
- EGO_PATH of track_003, since B:e43 (t = 11.80 s)

## Tracks lost

- track_010 at 9.35 s (B:e34): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_009, track_004, track_008, track_005, track_012, track_011, track_013

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s)
- track_002: CRITICAL_TTC_START 7.05, COLLISION 7.75 (+0.70 s)
- track_003: CRITICAL_TTC_START 11.30; EGO_PATH_ENTRY 11.80 after critical TTC (+0.50 s)
- track_006: CRITICAL_TTC_START 8.70; EGO_PATH_ENTRY 8.70 together with critical TTC (+0.00 s)
- track_007: CRITICAL_TTC_START 10.55; EGO_PATH_ENTRY 11.05 after critical TTC (+0.50 s)
- track_010: EGO_PATH_ENTRY 8.00, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 14.4 m / +0 deg | 9.12 m (11.45) | 9.2 m / -11 deg | 12.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 2.6 m / +38 deg | 1.25 m (7.50) | 1.6 m / +72 deg | 14.3 m/s |
| track_003 | 0.00 | 11.95 | 240 | 7.5 m / +17 deg | 2.48 m (11.95) | 2.5 m / +29 deg | 12.3 m/s |
| track_004 | 0.00 | 3.65 | 70 | 30.2 m / -5 deg | 28.57 m (3.65) | 28.6 m / -6 deg | 12.1 m/s |
| track_005 | 0.00 | 6.70 | 131 | 6.0 m / -146 deg | 5.97 m (0.00) | 9.3 m / -154 deg | 12.0 m/s |
| track_006 | 0.05 | 11.95 | 239 | 14.6 m / -11 deg | 10.11 m (10.10) | 11.2 m / -28 deg | 12.1 m/s |
| track_007 | 0.05 | 11.95 | 239 | 15.4 m / +10 deg | 9.79 m (11.95) | 9.8 m / +2 deg | 12.1 m/s |
| track_008 | 0.15 | 3.80 | 73 | 30.3 m / +6 deg | 28.07 m (3.80) | 28.1 m / +6 deg | 11.8 m/s |
| track_009 | 0.20 | 2.20 | 35 | 45.2 m / -4 deg | 44.26 m (2.20) | 44.3 m / -4 deg | 11.9 m/s |
| track_010 | 6.40 | 9.35 | 58 | 27.6 m / -6 deg | 26.44 m (9.35) | 26.4 m / -5 deg | 12.1 m/s |
| track_011 | 6.50 | 8.85 | 47 | 27.0 m / +7 deg | 25.89 m (8.85) | 25.9 m / +10 deg | 12.1 m/s |
| track_012 | 6.60 | 7.00 | 7 | 42.8 m / -5 deg | 42.58 m (7.00) | 42.6 m / -4 deg | 12.1 m/s |
| track_013 | 7.85 | 9.00 | 24 | 8.1 m / -156 deg | 8.10 m (7.85) | 17.9 m / -155 deg | 14.6 m/s |
| track_014 | 8.15 | 11.95 | 62 | 41.7 m / -1 deg | 40.72 m (11.05) | 41.0 m / -21 deg | 12.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_005, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.05 s: B's radar started tracking track_006, which appeared on its left.
- t = 0.05 s: B's radar started tracking track_007, which appeared on its right.
- t = 0.15 s: B's radar started tracking track_008, which appeared on its right.
- t = 0.20 s: B's radar started tracking track_009, which appeared in front of it.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 2.20 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 3.65 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 6.40 s: B's radar started tracking track_010, which appeared on its left.
- t = 6.50 s: B's radar started tracking track_011, which appeared on its right.
- t = 6.60 s: B's radar started tracking track_012, which appeared in front of it.
- t = 6.70 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 7.00 s: B's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 7.05 s: B's time-to-contact with track_002 became critical.
- t = 7.15 s: B observed track_002 start closing in.
- t = 7.75 s: B's collision sensor recorded a contact (peak impulse 254 N*s).
- t = 7.75 s: B's time-to-contact with track_002 stopped being critical.
- t = 7.80 s: B released the accelerator.
- t = 7.85 s: B observed track_002 stop closing in.
- t = 7.85 s: B's radar started tracking track_013, which appeared on its left.
- t = 8.00 s: B observed track_010 enter its forward path corridor.
- t = 8.15 s: B's radar started tracking track_014, which appeared in front of it.
- t = 8.70 s: B observed track_006 enter its forward path corridor.
- t = 8.70 s: B's time-to-contact with track_006 became critical.
- t = 8.85 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 9.00 s: B's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 9.35 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 9.55 s: B observed track_014 leave its forward path corridor.
- t = 10.55 s: B's time-to-contact with track_007 became critical.
- t = 10.60 s: B's time-to-contact with track_006 stopped being critical.
- t = 10.60 s: B observed track_006 leave its forward path corridor.
- t = 11.05 s: B observed track_007 enter its forward path corridor.
- t = 11.10 s: B observed track_003 start closing in.
- t = 11.30 s: B's time-to-contact with track_003 became critical.
- t = 11.60 s: B observed track_002 start closing in.
- t = 11.80 s: B observed track_003 enter its forward path corridor.
