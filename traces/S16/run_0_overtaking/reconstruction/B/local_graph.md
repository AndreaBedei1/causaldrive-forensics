# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 318.1770825125277 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 9 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 49; edges: 89 (PRECEDES 56, SAME_TRACK 33)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 0.00 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e08 | 0.10 | TRACK_APPEARED_FRONT | B | track_004 | radar | initial_in_ego_path=True |
| B:e09 | 0.60 | CRITICAL_TTC_START | B | track_004 | radar |  |
| B:e10 | 0.80 | TRACK_APPEARED_FRONT | B | track_005 | radar | initial_in_ego_path=False |
| B:e11 | 0.80 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e12 | 3.10 | TRACK_LOST | B | track_005 | radar |  |
| B:e13 | 3.40 | CUT_IN_FROM_RIGHT_START | B | track_001 | radar | geometry=estimated_body |
| B:e14 | 4.20 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 4.45 | CUT_IN_FROM_RIGHT_END | B | track_001 | radar | geometry=estimated_body |
| B:e16 | 5.20 | TRACK_LOST | B | track_003 | radar |  |
| B:e17 | 5.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e18 | 5.65 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e19 | 5.65 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e20 | 5.85 | CLOSING_START | B | track_001 | radar |  |
| B:e21 | 5.90 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e22 | 5.90 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e23 | 6.25 | EGO_PATH_ENTRY | B | track_001 | radar | geometry=estimated_body |
| B:e24 | 6.55 | CLOSING_END | B | track_001 | radar |  |
| B:e25 | 6.75 | COLLISION | B | - | collision_sensor | peak_impulse=191.84; merged_bursts=[[8.25, 12.44]] |
| B:e26 | 6.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e27 | 6.80 | THROTTLE_END | B | - | controls |  |
| B:e28 | 6.80 | BRAKE_START | B | - | controls |  |
| B:e29 | 6.90 | EGO_PATH_ENTRY | B | track_007 | radar | geometry=estimated_body |
| B:e30 | 6.95 | CLOSING_START | B | track_001 | radar |  |
| B:e31 | 7.05 | CLOSING_END | B | track_007 | radar |  |
| B:e32 | 7.10 | CLOSING_END | B | track_002 | radar |  |
| B:e33 | 7.20 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e34 | 7.35 | CLOSING_END | B | track_001 | radar |  |
| B:e35 | 7.35 | CLOSING_END | B | track_006 | radar |  |
| B:e36 | 7.40 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e37 | 7.55 | CRITICAL_TTC_END | B | track_004 | radar |  |
| B:e38 | 7.90 | MOVING_END | B | - | ego |  |
| B:e39 | 7.90 | STOP_START | B | - | ego |  |
| B:e40 | 8.55 | TRACK_APPEARED_LEFT | B | track_008 | radar | initial_in_ego_path=False |
| B:e41 | 8.60 | EGO_PATH_EXIT | B | track_004 | radar | geometry=estimated_body |
| B:e42 | 9.00 | EGO_PATH_EXIT | B | track_007 | radar | geometry=estimated_body |
| B:e43 | 9.10 | EGO_PATH_ENTRY | B | track_006 | radar | geometry=estimated_body |
| B:e44 | 9.70 | TRACK_LOST | B | track_008 | radar |  |
| B:e45 | 10.20 | TRACK_APPEARED_RIGHT | B | track_009 | radar | initial_in_ego_path=False |
| B:e46 | 10.35 | EGO_PATH_EXIT | B | track_002 | radar | geometry=estimated_body |
| B:e47 | 11.10 | TRACK_LOST | B | track_004 | radar |  |
| B:e48 | 11.50 | EGO_PATH_EXIT | B | track_006 | radar | geometry=estimated_body |
| B:e49 | 11.55 | TRACK_LOST | B | track_007 | radar |  |

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
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e33 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e36
    B:e36 --PRECEDES--> B:e37
    B:e37 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e40
    B:e40 --PRECEDES--> B:e41
    B:e41 --PRECEDES--> B:e42
    B:e42 --PRECEDES--> B:e43
    B:e43 --PRECEDES--> B:e44
    B:e44 --PRECEDES--> B:e45
    B:e45 --PRECEDES--> B:e46
    B:e46 --PRECEDES--> B:e47
    B:e47 --PRECEDES--> B:e48
    B:e48 --PRECEDES--> B:e49
    B:e03 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e07
    B:e08 --SAME_TRACK--> B:e09
    B:e10 --SAME_TRACK--> B:e11
    B:e10 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e13
    B:e03 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e16
    B:e03 --SAME_TRACK--> B:e17
    B:e18 --SAME_TRACK--> B:e19
    B:e03 --SAME_TRACK--> B:e20
    B:e21 --SAME_TRACK--> B:e22
    B:e03 --SAME_TRACK--> B:e23
    B:e03 --SAME_TRACK--> B:e24
    B:e03 --SAME_TRACK--> B:e26
    B:e21 --SAME_TRACK--> B:e29
    B:e03 --SAME_TRACK--> B:e30
    B:e21 --SAME_TRACK--> B:e31
    B:e04 --SAME_TRACK--> B:e32
    B:e04 --SAME_TRACK--> B:e33
    B:e03 --SAME_TRACK--> B:e34
    B:e18 --SAME_TRACK--> B:e35
    B:e03 --SAME_TRACK--> B:e36
    B:e08 --SAME_TRACK--> B:e37
    B:e08 --SAME_TRACK--> B:e41
    B:e21 --SAME_TRACK--> B:e42
    B:e18 --SAME_TRACK--> B:e43
    B:e40 --SAME_TRACK--> B:e44
    B:e04 --SAME_TRACK--> B:e46
    B:e08 --SAME_TRACK--> B:e47
    B:e18 --SAME_TRACK--> B:e48
    B:e21 --SAME_TRACK--> B:e49
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 TRACK_APPEARED_RIGHT track_003<br>B:e06 CLOSING_START track_001<br>B:e07 CLOSING_START track_002 | ego: not yet observed | - |
| 0.10 | B:e08 TRACK_APPEARED_FRONT track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.00 |
| 0.60 | B:e09 CRITICAL_TTC_START track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: IN_EGO_PATH, CRITICAL_TTC? | 0.50 |
| 0.80 | B:e10 TRACK_APPEARED_FRONT track_005<br>B:e11 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH | 0.70 |
| 3.10 | B:e12 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING | 3.00 |
| 3.40 | B:e13 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 | 3.30 |
| 4.20 | B:e14 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_RIGHT<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 | 4.10 |
| 4.45 | B:e15 CUT_IN_FROM_RIGHT_END track_001 | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 | 4.40 |
| 5.20 | B:e16 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 | 5.10 |
| 5.40 | B:e17 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 5.30 |
| 5.65 | B:e18 TRACK_APPEARED_RIGHT track_006<br>B:e19 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 5.60 |
| 5.85 | B:e20 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 5.80 |
| 5.90 | B:e21 TRACK_APPEARED_RIGHT track_007<br>B:e22 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 5.80 |
| 6.25 | B:e23 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 6.20 |
| 6.55 | B:e24 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 | 6.50 |
| 6.75 | B:e25 COLLISION<br>B:e26 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 | 6.70 |
| 6.80 | B:e27 THROTTLE_END<br>B:e28 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 | 6.70 |
| 6.90 | B:e29 EGO_PATH_ENTRY track_007 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 | 6.80 |
| 6.95 | B:e30 CLOSING_START track_001 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 6.90 |
| 7.05 | B:e31 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.00 |
| 7.10 | B:e32 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.00 |
| 7.20 | B:e33 EGO_PATH_ENTRY track_002 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.10 |
| 7.35 | B:e34 CLOSING_END track_001<br>B:e35 CLOSING_END track_006 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.30 |
| 7.40 | B:e36 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.30 |
| 7.55 | B:e37 CRITICAL_TTC_END track_004 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.50 |
| 7.90 | B:e38 MOVING_END<br>B:e39 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 7.80 |
| 8.55 | B:e40 TRACK_APPEARED_LEFT track_008 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 | 8.50 |
| 8.60 | B:e41 EGO_PATH_EXIT track_004 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 8.50 |
| 9.00 | B:e42 EGO_PATH_EXIT track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 | 8.90 |
| 9.10 | B:e43 EGO_PATH_ENTRY track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_003, track_005 | 9.00 |
| 9.70 | B:e44 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_003, track_005 | 9.60 |
| 10.20 | B:e45 TRACK_APPEARED_RIGHT track_009 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_005, track_008 | 10.10 |
| 10.35 | B:e46 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005, track_008 | 10.30 |
| 11.10 | B:e47 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_003, track_005, track_008 | 11.00 |
| 11.50 | B:e48 EGO_PATH_EXIT track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_005, track_008 | 11.40 |
| 11.55 | B:e49 TRACK_LOST track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_006: no active state<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_005, track_008 | 11.50 |

## States still active when observation ended

- CLOSING of track_005, since B:e11 (t = 0.80 s); the track was lost at 3.10 s
- BRAKE, since B:e28 (t = 6.80 s)
- STOP, since B:e39 (t = 7.90 s)

## Tracks lost

- track_005 at 3.10 s (B:e12): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_008, track_004, track_007

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.40 < CRITICAL_TTC_START 5.40 (+2.00 s) < COLLISION 6.75 (+1.35 s); EGO_PATH_ENTRY 6.25 after critical TTC (+0.85 s)
- track_002: EGO_PATH_ENTRY 7.20, no critical TTC
- track_004: CRITICAL_TTC_START 0.60, COLLISION 6.75 (+6.15 s)
- track_006: EGO_PATH_ENTRY 9.10, no critical TTC
- track_007: EGO_PATH_ENTRY 6.90, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 8.2 m / +16 deg | 0.42 m (6.25) | 1.7 m / -104 deg | 15.4 m/s |
| track_002 | 0.00 | 11.95 | 238 | 23.9 m / +8 deg | 10.55 m (7.15) | 61.7 m / -10 deg | 12.1 m/s |
| track_003 | 0.00 | 5.20 | 105 | 5.2 m / +76 deg | 4.86 m (0.50) | 18.3 m / +156 deg | 11.0 m/s |
| track_004 | 0.10 | 11.10 | 214 | 11.3 m / -0 deg | 10.31 m (6.75) | 60.4 m / -12 deg | 14.2 m/s |
| track_005 | 0.80 | 3.10 | 44 | 37.9 m / +5 deg | 33.12 m (3.10) | 33.1 m / +5 deg | 11.8 m/s |
| track_006 | 5.65 | 11.95 | 124 | 22.4 m / +17 deg | 16.91 m (7.40) | 58.0 m / -6 deg | 10.4 m/s |
| track_007 | 5.90 | 11.55 | 109 | 28.1 m / +6 deg | 25.93 m (7.15) | 71.9 m / -12 deg | 12.1 m/s |
| track_008 | 8.55 | 9.70 | 21 | 42.9 m / -9 deg | 42.90 m (8.55) | 58.7 m / -12 deg | 14.0 m/s |
| track_009 | 10.20 | 11.95 | 36 | 4.1 m / +88 deg | 4.09 m (10.20) | 13.9 m / +18 deg | 9.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: B observed track_002 start closing in (already the case when first observed).
- t = 0.10 s: B's radar started tracking track_004, which appeared in front of it.
- t = 0.60 s: B's time-to-contact with track_004 became critical.
- t = 0.80 s: B's radar started tracking track_005, which appeared in front of it.
- t = 0.80 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.10 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.40 s: B observed track_001 cutting in from the right.
- t = 4.20 s: B observed track_001 stop closing in.
- t = 4.45 s: B observed track_001's cut-in from the right settle.
- t = 5.20 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.40 s: B's time-to-contact with track_001 became critical.
- t = 5.65 s: B's radar started tracking track_006, which appeared on its right.
- t = 5.65 s: B observed track_006 start closing in (already the case when first observed).
- t = 5.85 s: B observed track_001 start closing in.
- t = 5.90 s: B's radar started tracking track_007, which appeared on its right.
- t = 5.90 s: B observed track_007 start closing in (already the case when first observed).
- t = 6.25 s: B observed track_001 enter its forward path corridor.
- t = 6.55 s: B observed track_001 stop closing in.
- t = 6.75 s: B's collision sensor recorded a contact (peak impulse 192 N*s).
- t = 6.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.80 s: B released the accelerator.
- t = 6.80 s: B started braking.
- t = 6.90 s: B observed track_007 enter its forward path corridor.
- t = 6.95 s: B observed track_001 start closing in.
- t = 7.05 s: B observed track_007 stop closing in.
- t = 7.10 s: B observed track_002 stop closing in.
- t = 7.20 s: B observed track_002 enter its forward path corridor.
- t = 7.35 s: B observed track_001 stop closing in.
- t = 7.35 s: B observed track_006 stop closing in.
- t = 7.40 s: B observed track_001 leave its forward path corridor.
- t = 7.55 s: B's time-to-contact with track_004 stopped being critical.
- t = 7.90 s: B stopped moving.
- t = 7.90 s: B came to a stop.
- t = 8.55 s: B's radar started tracking track_008, which appeared on its left.
- t = 8.60 s: B observed track_004 leave its forward path corridor.
- t = 9.00 s: B observed track_007 leave its forward path corridor.
- t = 9.10 s: B observed track_006 enter its forward path corridor.
- t = 9.70 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 10.20 s: B's radar started tracking track_009, which appeared on its right.
- t = 10.35 s: B observed track_002 leave its forward path corridor.
- t = 11.10 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 11.50 s: B observed track_006 leave its forward path corridor.
- t = 11.55 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
