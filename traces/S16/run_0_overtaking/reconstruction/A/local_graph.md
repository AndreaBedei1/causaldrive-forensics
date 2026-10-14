# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 318.1770825125277 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 12 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 51; edges: 106 (PRECEDES 74, SAME_TRACK 32)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_003 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | TRACK_APPEARED_RIGHT | A | track_005 | radar | initial_in_ego_path=False |
| A:e08 | 0.00 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e09 | 0.40 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e10 | 0.40 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e11 | 0.50 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e12 | 0.50 | TRACK_LOST | A | track_005 | radar |  |
| A:e13 | 3.60 | TRACK_LOST | A | track_002 | radar |  |
| A:e14 | 3.60 | TRACK_LOST | A | track_004 | radar |  |
| A:e15 | 3.90 | CLOSING_END | A | track_006 | radar |  |
| A:e16 | 5.10 | CRITICAL_TTC_START | A | track_006 | radar |  |
| A:e17 | 5.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e18 | 5.60 | TRACK_APPEARED_RIGHT | A | track_007 | radar | initial_in_ego_path=False |
| A:e19 | 5.60 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e20 | 5.65 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e21 | 6.00 | TRACK_APPEARED_FRONT | A | track_008 | radar | initial_in_ego_path=True |
| A:e22 | 6.15 | CLOSING_START | A | track_006 | radar |  |
| A:e23 | 6.35 | EGO_PATH_ENTRY | A | track_006 | radar | geometry=estimated_body |
| A:e24 | 6.75 | COLLISION | A | - | collision_sensor | peak_impulse=191.84; merged_bursts=[[8.25, 12.44]] |
| A:e25 | 6.75 | CRITICAL_TTC_END | A | track_006 | radar |  |
| A:e26 | 6.75 | EGO_PATH_EXIT | A | track_003 | radar | geometry=estimated_body |
| A:e27 | 6.80 | CLOSING_END | A | track_006 | radar |  |
| A:e28 | 6.80 | THROTTLE_END | A | - | controls |  |
| A:e29 | 6.80 | BRAKE_START | A | - | controls |  |
| A:e30 | 6.85 | EGO_PATH_ENTRY | A | track_003 | radar | geometry=estimated_body |
| A:e31 | 7.20 | CLOSING_END | A | track_007 | radar |  |
| A:e32 | 7.35 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e33 | 7.45 | CRITICAL_TTC_END | A | track_003 | radar |  |
| A:e34 | 7.55 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e35 | 7.95 | MOVING_END | A | - | ego |  |
| A:e36 | 7.95 | STOP_START | A | - | ego |  |
| A:e37 | 8.05 | TRACK_APPEARED_FRONT | A | track_009 | radar | initial_in_ego_path=True |
| A:e38 | 8.25 | EGO_PATH_ENTRY | A | track_007 | radar | geometry=estimated_body |
| A:e39 | 8.30 | TRACK_APPEARED_RIGHT | A | track_010 | radar | initial_in_ego_path=False |
| A:e40 | 8.30 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e41 | 8.55 | TRACK_APPEARED_LEFT | A | track_011 | radar | initial_in_ego_path=False |
| A:e42 | 8.85 | TRACK_LOST | A | track_011 | radar |  |
| A:e43 | 9.05 | TRACK_APPEARED_LEFT | A | track_012 | radar | initial_in_ego_path=False |
| A:e44 | 9.95 | EGO_PATH_EXIT | A | track_003 | radar | geometry=estimated_body |
| A:e45 | 9.95 | TRACK_LOST | A | track_012 | radar |  |
| A:e46 | 10.10 | EGO_PATH_EXIT | A | track_009 | radar | geometry=estimated_body |
| A:e47 | 10.15 | CLOSING_END | A | track_010 | radar |  |
| A:e48 | 10.75 | TRACK_LOST | A | track_009 | radar |  |
| A:e49 | 11.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e50 | 11.30 | EGO_PATH_EXIT | A | track_007 | radar | geometry=estimated_body |
| A:e51 | 11.85 | TRACK_LOST | A | track_008 | radar |  |

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
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e28
    A:e24 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e31 --PRECEDES--> A:e32
    A:e32 --PRECEDES--> A:e33
    A:e33 --PRECEDES--> A:e34
    A:e34 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e49 --PRECEDES--> A:e50
    A:e50 --PRECEDES--> A:e51
    A:e06 --SAME_TRACK--> A:e08
    A:e09 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e11
    A:e07 --SAME_TRACK--> A:e12
    A:e05 --SAME_TRACK--> A:e13
    A:e06 --SAME_TRACK--> A:e14
    A:e09 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e04 --SAME_TRACK--> A:e17
    A:e18 --SAME_TRACK--> A:e19
    A:e04 --SAME_TRACK--> A:e20
    A:e09 --SAME_TRACK--> A:e22
    A:e09 --SAME_TRACK--> A:e23
    A:e09 --SAME_TRACK--> A:e25
    A:e03 --SAME_TRACK--> A:e26
    A:e09 --SAME_TRACK--> A:e27
    A:e03 --SAME_TRACK--> A:e30
    A:e18 --SAME_TRACK--> A:e31
    A:e21 --SAME_TRACK--> A:e32
    A:e03 --SAME_TRACK--> A:e33
    A:e04 --SAME_TRACK--> A:e34
    A:e18 --SAME_TRACK--> A:e38
    A:e39 --SAME_TRACK--> A:e40
    A:e41 --SAME_TRACK--> A:e42
    A:e03 --SAME_TRACK--> A:e44
    A:e43 --SAME_TRACK--> A:e45
    A:e37 --SAME_TRACK--> A:e46
    A:e39 --SAME_TRACK--> A:e47
    A:e37 --SAME_TRACK--> A:e48
    A:e04 --SAME_TRACK--> A:e49
    A:e18 --SAME_TRACK--> A:e50
    A:e21 --SAME_TRACK--> A:e51
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_003<br>A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 TRACK_APPEARED_LEFT track_002<br>A:e06 TRACK_APPEARED_RIGHT track_004<br>A:e07 TRACK_APPEARED_RIGHT track_005<br>A:e08 CLOSING_START track_004 | ego: not yet observed | - |
| 0.40 | A:e09 TRACK_APPEARED_LEFT track_006<br>A:e10 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.30 |
| 0.50 | A:e11 CRITICAL_TTC_START track_003<br>A:e12 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? | 0.40 |
| 3.60 | A:e13 TRACK_LOST track_002<br>A:e14 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005 | 3.50 |
| 3.90 | A:e15 CLOSING_END track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 3.80 |
| 5.10 | A:e16 CRITICAL_TTC_START track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 5.00 |
| 5.55 | A:e17 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 5.50 |
| 5.60 | A:e18 TRACK_APPEARED_RIGHT track_007<br>A:e19 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 5.50 |
| 5.65 | A:e20 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 5.60 |
| 6.00 | A:e21 TRACK_APPEARED_FRONT track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 5.90 |
| 6.15 | A:e22 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 6.10 |
| 6.35 | A:e23 EGO_PATH_ENTRY track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 6.30 |
| 6.75 | A:e24 COLLISION<br>A:e25 CRITICAL_TTC_END track_006<br>A:e26 EGO_PATH_EXIT track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 6.70 |
| 6.80 | A:e27 CLOSING_END track_006<br>A:e28 THROTTLE_END<br>A:e29 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 6.70 |
| 6.85 | A:e30 EGO_PATH_ENTRY track_003 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 6.80 |
| 7.20 | A:e31 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 7.10 |
| 7.35 | A:e32 EGO_PATH_EXIT track_008 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 7.30 |
| 7.45 | A:e33 CRITICAL_TTC_END track_003 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 7.40 |
| 7.55 | A:e34 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 7.50 |
| 7.95 | A:e35 MOVING_END<br>A:e36 STOP_START | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 7.90 |
| 8.05 | A:e37 TRACK_APPEARED_FRONT track_009 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 8.00 |
| 8.25 | A:e38 EGO_PATH_ENTRY track_007 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 8.20 |
| 8.30 | A:e39 TRACK_APPEARED_RIGHT track_010<br>A:e40 CLOSING_START track_010 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 8.20 |
| 8.55 | A:e41 TRACK_APPEARED_LEFT track_011 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 8.50 |
| 8.85 | A:e42 TRACK_LOST track_011 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_005 | 8.80 |
| 9.05 | A:e43 TRACK_APPEARED_LEFT track_012 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011 | 9.00 |
| 9.95 | A:e44 EGO_PATH_EXIT track_003<br>A:e45 TRACK_LOST track_012 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011 | 9.90 |
| 10.10 | A:e46 EGO_PATH_EXIT track_009 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011, track_012 | 10.00 |
| 10.15 | A:e47 CLOSING_END track_010 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011, track_012 | 10.10 |
| 10.75 | A:e48 TRACK_LOST track_009 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011, track_012 | 10.70 |
| 11.20 | A:e49 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_009, track_011, track_012 | 11.10 |
| 11.30 | A:e50 EGO_PATH_EXIT track_007 | ego: STOP, BRAKE<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_011, track_012 | 11.20 |
| 11.85 | A:e51 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_011, track_012 | 11.80 |

## States still active when observation ended

- CLOSING of track_004, since A:e08 (t = 0.00 s); the track was lost at 3.60 s
- CRITICAL_TTC of track_001, since A:e17 (t = 5.55 s); the track was lost at 11.20 s
- EGO_PATH of track_006, since A:e23 (t = 6.35 s)
- BRAKE, since A:e29 (t = 6.80 s)
- STOP, since A:e36 (t = 7.95 s)

## Tracks lost

- track_004 at 3.60 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 11.20 s (A:e49): CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_002, track_011, track_012, track_009, track_008

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.55, COLLISION 6.75 (+1.20 s); EGO_PATH_ENTRY 5.65 after critical TTC (+0.10 s)
- track_003: CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s); EGO_PATH_ENTRY 6.85 after critical TTC (+6.35 s)
- track_006: CRITICAL_TTC_START 5.10, COLLISION 6.75 (+1.65 s); EGO_PATH_ENTRY 6.35 after critical TTC (+1.25 s)
- track_007: EGO_PATH_ENTRY 8.25, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.20 | 215 | 2.5 m / -45 deg | 2.52 m (0.00) | 64.3 m / -13 deg | 14.1 m/s |
| track_002 | 0.00 | 3.60 | 70 | 16.4 m / -10 deg | 16.44 m (0.00) | 23.6 m / -8 deg | 13.9 m/s |
| track_003 | 0.00 | 11.95 | 237 | 11.9 m / +0 deg | 11.94 m (0.50) | 64.2 m / -10 deg | 12.2 m/s |
| track_004 | 0.00 | 3.60 | 72 | 32.1 m / +5 deg | 24.86 m (3.60) | 24.9 m / +8 deg | 9.9 m/s |
| track_005 | 0.00 | 0.50 | 11 | 8.4 m / +152 deg | 8.40 m (0.00) | 9.3 m / +154 deg | 9.9 m/s |
| track_006 | 0.40 | 11.95 | 232 | 9.2 m / -153 deg | 0.54 m (11.95) | 0.5 m / -71 deg | 13.8 m/s |
| track_007 | 5.60 | 11.95 | 127 | 21.5 m / +11 deg | 18.76 m (7.30) | 60.2 m / -6 deg | 10.2 m/s |
| track_008 | 6.00 | 11.85 | 100 | 27.9 m / -1 deg | 27.87 m (6.00) | 78.0 m / -13 deg | 14.0 m/s |
| track_009 | 8.05 | 10.75 | 34 | 36.1 m / +3 deg | 36.11 m (8.05) | 62.1 m / -5 deg | 10.1 m/s |
| track_010 | 8.30 | 11.95 | 74 | 16.8 m / +156 deg | 2.49 m (10.10) | 15.2 m / +11 deg | 10.0 m/s |
| track_011 | 8.55 | 8.85 | 7 | 45.5 m / -11 deg | 45.46 m (8.55) | 49.6 m / -11 deg | 13.9 m/s |
| track_012 | 9.05 | 9.95 | 12 | 51.7 m / -11 deg | 51.73 m (9.05) | 64.1 m / -13 deg | 14.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_005, which appeared on its right.
- t = 0.00 s: A observed track_004 start closing in (already the case when first observed).
- t = 0.40 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.40 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.50 s: A's time-to-contact with track_003 became critical.
- t = 0.50 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.60 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.60 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.90 s: A observed track_006 stop closing in.
- t = 5.10 s: A's time-to-contact with track_006 became critical.
- t = 5.55 s: A's time-to-contact with track_001 became critical.
- t = 5.60 s: A's radar started tracking track_007, which appeared on its right.
- t = 5.60 s: A observed track_007 start closing in (already the case when first observed).
- t = 5.65 s: A observed track_001 enter its forward path corridor.
- t = 6.00 s: A's radar started tracking track_008, which appeared in front of it.
- t = 6.15 s: A observed track_006 start closing in.
- t = 6.35 s: A observed track_006 enter its forward path corridor.
- t = 6.75 s: A's collision sensor recorded a contact (peak impulse 192 N*s).
- t = 6.75 s: A's time-to-contact with track_006 stopped being critical.
- t = 6.75 s: A observed track_003 leave its forward path corridor.
- t = 6.80 s: A observed track_006 stop closing in.
- t = 6.80 s: A released the accelerator.
- t = 6.80 s: A started braking.
- t = 6.85 s: A observed track_003 enter its forward path corridor.
- t = 7.20 s: A observed track_007 stop closing in.
- t = 7.35 s: A observed track_008 leave its forward path corridor.
- t = 7.45 s: A's time-to-contact with track_003 stopped being critical.
- t = 7.55 s: A observed track_001 leave its forward path corridor.
- t = 7.95 s: A stopped moving.
- t = 7.95 s: A came to a stop.
- t = 8.05 s: A's radar started tracking track_009, which appeared in front of it.
- t = 8.25 s: A observed track_007 enter its forward path corridor.
- t = 8.30 s: A's radar started tracking track_010, which appeared on its right.
- t = 8.30 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.55 s: A's radar started tracking track_011, which appeared on its left.
- t = 8.85 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 9.05 s: A's radar started tracking track_012, which appeared on its left.
- t = 9.95 s: A observed track_003 leave its forward path corridor.
- t = 9.95 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 10.10 s: A observed track_009 leave its forward path corridor.
- t = 10.15 s: A observed track_010 stop closing in.
- t = 10.75 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 11.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 11.30 s: A observed track_007 leave its forward path corridor.
- t = 11.85 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
