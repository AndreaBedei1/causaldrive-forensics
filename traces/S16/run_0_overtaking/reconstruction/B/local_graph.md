# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 318.1770825125277 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 10 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 55; edges: 117 (PRECEDES 79, SAME_TRACK 38)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e07 | 0.00 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e08 | 0.00 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e09 | 0.20 | TRACK_APPEARED_FRONT | B | track_005 | radar | initial_in_ego_path=False |
| B:e10 | 0.20 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e11 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e12 | 3.10 | TRACK_LOST | B | track_005 | radar |  |
| B:e13 | 3.50 | CUT_IN_FROM_RIGHT_START | B | track_002 | radar | geometry=estimated_body |
| B:e14 | 4.15 | CLOSING_END | B | track_002 | radar |  |
| B:e15 | 4.30 | CUT_IN_FROM_RIGHT_END | B | track_002 | radar | geometry=estimated_body |
| B:e16 | 5.20 | TRACK_LOST | B | track_004 | radar |  |
| B:e17 | 5.55 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e18 | 5.65 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e19 | 5.65 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e20 | 5.90 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e21 | 5.90 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e22 | 6.20 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e23 | 6.20 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e24 | 6.30 | CLOSING_START | B | track_002 | radar |  |
| B:e25 | 6.75 | COLLISION | B | - | collision_sensor | peak_impulse=191.84; merged_bursts=[[8.25, 12.44]] |
| B:e26 | 6.75 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e27 | 6.80 | CLOSING_END | B | track_002 | radar |  |
| B:e28 | 6.80 | THROTTLE_END | B | - | controls |  |
| B:e29 | 6.80 | BRAKE_START | B | - | controls |  |
| B:e30 | 6.95 | EGO_PATH_ENTRY | B | track_007 | radar | geometry=estimated_body |
| B:e31 | 7.05 | CLOSING_END | B | track_007 | radar |  |
| B:e32 | 7.10 | CLOSING_END | B | track_003 | radar |  |
| B:e33 | 7.25 | EGO_PATH_ENTRY | B | track_003 | radar | geometry=estimated_body |
| B:e34 | 7.35 | CLOSING_END | B | track_006 | radar |  |
| B:e35 | 7.35 | CLOSING_END | B | track_008 | radar |  |
| B:e36 | 7.35 | EGO_PATH_ENTRY | B | track_008 | radar | geometry=estimated_body |
| B:e37 | 7.40 | CRITICAL_TTC_START | B | track_003 | radar |  |
| B:e38 | 7.55 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e39 | 7.55 | TRACK_LOST | B | track_008 | radar |  |
| B:e40 | 7.90 | MOVING_END | B | - | ego |  |
| B:e41 | 7.90 | STOP_START | B | - | ego |  |
| B:e42 | 7.90 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e43 | 8.25 | TRACK_APPEARED_LEFT | B | track_009 | radar | initial_in_ego_path=False |
| B:e44 | 8.50 | CRITICAL_TTC_END | B | track_003 | radar |  |
| B:e45 | 8.65 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e46 | 9.05 | EGO_PATH_EXIT | B | track_007 | radar | geometry=estimated_body |
| B:e47 | 9.15 | EGO_PATH_ENTRY | B | track_006 | radar | geometry=estimated_body |
| B:e48 | 9.65 | CUT_IN_FROM_RIGHT_START | B | track_003 | radar | geometry=estimated_body |
| B:e49 | 9.70 | TRACK_LOST | B | track_009 | radar |  |
| B:e50 | 10.20 | TRACK_APPEARED_RIGHT | B | track_010 | radar | initial_in_ego_path=False |
| B:e51 | 10.35 | EGO_PATH_EXIT | B | track_003 | radar | geometry=estimated_body |
| B:e52 | 10.90 | CUT_IN_FROM_RIGHT_START | B | track_006 | radar | geometry=estimated_body |
| B:e53 | 11.10 | TRACK_LOST | B | track_001 | radar |  |
| B:e54 | 11.55 | EGO_PATH_EXIT | B | track_006 | radar | geometry=estimated_body |
| B:e55 | 11.55 | TRACK_LOST | B | track_007 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e09
    B:e01 --PRECEDES--> B:e10
    B:e02 --PRECEDES--> B:e09
    B:e02 --PRECEDES--> B:e10
    B:e03 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e10
    B:e04 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e10
    B:e05 --PRECEDES--> B:e09
    B:e05 --PRECEDES--> B:e10
    B:e06 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e10
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e33 --PRECEDES--> B:e35
    B:e33 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e37
    B:e37 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e41
    B:e38 --PRECEDES--> B:e42
    B:e39 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e41
    B:e39 --PRECEDES--> B:e42
    B:e40 --PRECEDES--> B:e43
    B:e41 --PRECEDES--> B:e43
    B:e42 --PRECEDES--> B:e43
    B:e43 --PRECEDES--> B:e44
    B:e44 --PRECEDES--> B:e45
    B:e45 --PRECEDES--> B:e46
    B:e46 --PRECEDES--> B:e47
    B:e47 --PRECEDES--> B:e48
    B:e48 --PRECEDES--> B:e49
    B:e49 --PRECEDES--> B:e50
    B:e50 --PRECEDES--> B:e51
    B:e51 --PRECEDES--> B:e52
    B:e52 --PRECEDES--> B:e53
    B:e53 --PRECEDES--> B:e54
    B:e53 --PRECEDES--> B:e55
    B:e04 --SAME_TRACK--> B:e07
    B:e05 --SAME_TRACK--> B:e08
    B:e09 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e11
    B:e09 --SAME_TRACK--> B:e12
    B:e04 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e04 --SAME_TRACK--> B:e15
    B:e06 --SAME_TRACK--> B:e16
    B:e04 --SAME_TRACK--> B:e17
    B:e18 --SAME_TRACK--> B:e19
    B:e20 --SAME_TRACK--> B:e21
    B:e22 --SAME_TRACK--> B:e23
    B:e04 --SAME_TRACK--> B:e24
    B:e04 --SAME_TRACK--> B:e26
    B:e04 --SAME_TRACK--> B:e27
    B:e20 --SAME_TRACK--> B:e30
    B:e20 --SAME_TRACK--> B:e31
    B:e05 --SAME_TRACK--> B:e32
    B:e05 --SAME_TRACK--> B:e33
    B:e18 --SAME_TRACK--> B:e34
    B:e22 --SAME_TRACK--> B:e35
    B:e22 --SAME_TRACK--> B:e36
    B:e05 --SAME_TRACK--> B:e37
    B:e03 --SAME_TRACK--> B:e38
    B:e22 --SAME_TRACK--> B:e39
    B:e04 --SAME_TRACK--> B:e42
    B:e05 --SAME_TRACK--> B:e44
    B:e03 --SAME_TRACK--> B:e45
    B:e20 --SAME_TRACK--> B:e46
    B:e18 --SAME_TRACK--> B:e47
    B:e05 --SAME_TRACK--> B:e48
    B:e43 --SAME_TRACK--> B:e49
    B:e05 --SAME_TRACK--> B:e51
    B:e18 --SAME_TRACK--> B:e52
    B:e03 --SAME_TRACK--> B:e53
    B:e18 --SAME_TRACK--> B:e54
    B:e20 --SAME_TRACK--> B:e55
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 TRACK_APPEARED_RIGHT track_003<br>B:e06 TRACK_APPEARED_RIGHT track_004<br>B:e07 CLOSING_START track_002<br>B:e08 CLOSING_START track_003 | ego: not yet observed | - |
| 0.20 | B:e09 TRACK_APPEARED_FRONT track_005<br>B:e10 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.10 |
| 0.50 | B:e11 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC? | 0.40 |
| 3.10 | B:e12 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_005: CLOSING | 3.00 |
| 3.50 | B:e13 CUT_IN_FROM_RIGHT_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 | 3.40 |
| 4.15 | B:e14 CLOSING_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 | 4.10 |
| 4.30 | B:e15 CUT_IN_FROM_RIGHT_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 | 4.20 |
| 5.20 | B:e16 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 | 5.10 |
| 5.55 | B:e17 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 5.50 |
| 5.65 | B:e18 TRACK_APPEARED_RIGHT track_006<br>B:e19 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 5.60 |
| 5.90 | B:e20 TRACK_APPEARED_RIGHT track_007<br>B:e21 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 | 5.80 |
| 6.20 | B:e22 TRACK_APPEARED_RIGHT track_008<br>B:e23 CLOSING_START track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 | 6.10 |
| 6.30 | B:e24 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 | 6.20 |
| 6.75 | B:e25 COLLISION<br>B:e26 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 6.70 |
| 6.80 | B:e27 CLOSING_END track_002<br>B:e28 THROTTLE_END<br>B:e29 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 6.70 |
| 6.95 | B:e30 EGO_PATH_ENTRY track_007 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 6.90 |
| 7.05 | B:e31 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 7.00 |
| 7.10 | B:e32 CLOSING_END track_003 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 7.00 |
| 7.25 | B:e33 EGO_PATH_ENTRY track_003 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 7.20 |
| 7.35 | B:e34 CLOSING_END track_006<br>B:e35 CLOSING_END track_008<br>B:e36 EGO_PATH_ENTRY track_008 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 | 7.30 |
| 7.40 | B:e37 CRITICAL_TTC_START track_003 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005 | 7.30 |
| 7.55 | B:e38 CRITICAL_TTC_END track_001<br>B:e39 TRACK_LOST track_008 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005 | 7.50 |
| 7.90 | B:e40 MOVING_END<br>B:e41 STOP_START<br>B:e42 EGO_PATH_ENTRY track_002 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 7.80 |
| 8.25 | B:e43 TRACK_APPEARED_LEFT track_009 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 8.20 |
| 8.50 | B:e44 CRITICAL_TTC_END track_003 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 8.40 |
| 8.65 | B:e45 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 8.60 |
| 9.05 | B:e46 EGO_PATH_EXIT track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 9.00 |
| 9.15 | B:e47 EGO_PATH_ENTRY track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 9.10 |
| 9.65 | B:e48 CUT_IN_FROM_RIGHT_START track_003 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 9.60 |
| 9.70 | B:e49 TRACK_LOST track_009 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 | 9.60 |
| 10.20 | B:e50 TRACK_APPEARED_RIGHT track_010 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 | 10.10 |
| 10.35 | B:e51 EGO_PATH_EXIT track_003 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 | 10.30 |
| 10.90 | B:e52 CUT_IN_FROM_RIGHT_START track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 | 10.80 |
| 11.10 | B:e53 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 | 11.00 |
| 11.55 | B:e54 EGO_PATH_EXIT track_006<br>B:e55 TRACK_LOST track_007 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_003: CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_008, track_009 | 11.50 |

## States still active when observation ended

- CLOSING of track_005, since B:e10 (t = 0.20 s); the track was lost at 3.10 s
- BRAKE, since B:e29 (t = 6.80 s)
- EGO_PATH of track_008, since B:e36 (t = 7.35 s); the track was lost at 7.55 s
- STOP, since B:e41 (t = 7.90 s)
- EGO_PATH of track_002, since B:e42 (t = 7.90 s)
- CUT_IN_FROM_RIGHT of track_003, since B:e48 (t = 9.65 s)
- CUT_IN_FROM_RIGHT of track_006, since B:e52 (t = 10.90 s)

## Tracks lost

- track_005 at 3.10 s (B:e12): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 7.55 s (B:e39): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_009, track_001, track_007

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s)
- track_002: cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.50 < CRITICAL_TTC_START 5.55 (+2.05 s) < COLLISION 6.75 (+1.20 s); EGO_PATH_ENTRY 7.90 after critical TTC (+2.35 s)
- track_003: CUT_IN_FROM_RIGHT_START 9.65, no critical TTC after it; EGO_PATH_ENTRY 7.25 before critical TTC (-0.15 s)
- track_006: CUT_IN_FROM_RIGHT_START 10.90, no critical TTC after it; EGO_PATH_ENTRY 9.15, no critical TTC
- track_007: EGO_PATH_ENTRY 6.95, no critical TTC
- track_008: EGO_PATH_ENTRY 7.35, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.10 | 216 | 11.3 m / +1 deg | 10.29 m (6.75) | 60.3 m / -12 deg | 14.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 8.2 m / +17 deg | 0.06 m (8.00) | 0.1 m / +95 deg | 14.2 m/s |
| track_003 | 0.00 | 11.95 | 237 | 23.9 m / +8 deg | 10.52 m (7.15) | 61.6 m / -9 deg | 12.1 m/s |
| track_004 | 0.00 | 5.20 | 105 | 5.2 m / +76 deg | 4.89 m (0.50) | 18.3 m / +156 deg | 11.1 m/s |
| track_005 | 0.20 | 3.10 | 52 | 39.2 m / +5 deg | 33.14 m (3.10) | 33.1 m / +5 deg | 11.8 m/s |
| track_006 | 5.65 | 11.95 | 124 | 22.4 m / +17 deg | 16.86 m (7.40) | 57.8 m / -6 deg | 10.3 m/s |
| track_007 | 5.90 | 11.55 | 109 | 28.0 m / +6 deg | 25.85 m (7.15) | 71.8 m / -12 deg | 12.1 m/s |
| track_008 | 6.20 | 7.55 | 18 | 36.5 m / +9 deg | 32.89 m (7.40) | 33.0 m / +3 deg | 10.2 m/s |
| track_009 | 8.25 | 9.70 | 24 | 38.7 m / -9 deg | 38.70 m (8.25) | 58.7 m / -12 deg | 14.1 m/s |
| track_010 | 10.20 | 11.95 | 36 | 4.1 m / +88 deg | 4.10 m (10.20) | 13.9 m / +19 deg | 9.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: B observed track_002 start closing in (already the case when first observed).
- t = 0.00 s: B observed track_003 start closing in (already the case when first observed).
- t = 0.20 s: B's radar started tracking track_005, which appeared in front of it.
- t = 0.20 s: B observed track_005 start closing in (already the case when first observed).
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 3.10 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.50 s: B observed track_002 cutting in from the right.
- t = 4.15 s: B observed track_002 stop closing in.
- t = 4.30 s: B observed track_002's cut-in from the right settle.
- t = 5.20 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 5.55 s: B's time-to-contact with track_002 became critical.
- t = 5.65 s: B's radar started tracking track_006, which appeared on its right.
- t = 5.65 s: B observed track_006 start closing in (already the case when first observed).
- t = 5.90 s: B's radar started tracking track_007, which appeared on its right.
- t = 5.90 s: B observed track_007 start closing in (already the case when first observed).
- t = 6.20 s: B's radar started tracking track_008, which appeared on its right.
- t = 6.20 s: B observed track_008 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_002 start closing in.
- t = 6.75 s: B's collision sensor recorded a contact (peak impulse 192 N*s).
- t = 6.75 s: B's time-to-contact with track_002 stopped being critical.
- t = 6.80 s: B observed track_002 stop closing in.
- t = 6.80 s: B released the accelerator.
- t = 6.80 s: B started braking.
- t = 6.95 s: B observed track_007 enter its forward path corridor.
- t = 7.05 s: B observed track_007 stop closing in.
- t = 7.10 s: B observed track_003 stop closing in.
- t = 7.25 s: B observed track_003 enter its forward path corridor.
- t = 7.35 s: B observed track_006 stop closing in.
- t = 7.35 s: B observed track_008 stop closing in.
- t = 7.35 s: B observed track_008 enter its forward path corridor.
- t = 7.40 s: B's time-to-contact with track_003 became critical.
- t = 7.55 s: B's time-to-contact with track_001 stopped being critical.
- t = 7.55 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 7.90 s: B stopped moving.
- t = 7.90 s: B came to a stop.
- t = 7.90 s: B observed track_002 enter its forward path corridor.
- t = 8.25 s: B's radar started tracking track_009, which appeared on its left.
- t = 8.50 s: B's time-to-contact with track_003 stopped being critical.
- t = 8.65 s: B observed track_001 leave its forward path corridor.
- t = 9.05 s: B observed track_007 leave its forward path corridor.
- t = 9.15 s: B observed track_006 enter its forward path corridor.
- t = 9.65 s: B observed track_003 cutting in from the right.
- t = 9.70 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 10.20 s: B's radar started tracking track_010, which appeared on its right.
- t = 10.35 s: B observed track_003 leave its forward path corridor.
- t = 10.90 s: B observed track_006 cutting in from the right.
- t = 11.10 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 11.55 s: B observed track_006 leave its forward path corridor.
- t = 11.55 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
