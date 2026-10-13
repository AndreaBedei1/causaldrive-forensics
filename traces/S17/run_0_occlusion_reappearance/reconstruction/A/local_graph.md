# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 415.1301955282688 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 10 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 48; edges: 92 (PRECEDES 63, SAME_TRACK 29)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_002 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_FRONT | A | track_003 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_LEFT | A | track_004 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e08 | 0.00 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e09 | 0.05 | TRACK_APPEARED_LEFT | A | track_005 | radar | initial_in_ego_path=False |
| A:e10 | 0.90 | TRACK_APPEARED_LEFT | A | track_007 | radar | initial_in_ego_path=False |
| A:e11 | 0.90 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e12 | 3.30 | TRACK_LOST | A | track_003 | radar |  |
| A:e13 | 4.30 | CLOSING_END | A | track_007 | radar |  |
| A:e14 | 4.55 | TRACK_LOST | A | track_006 | radar |  |
| A:e15 | 4.80 | TRACK_LOST | A | track_002 | radar |  |
| A:e16 | 5.45 | EGO_PATH_ENTRY | A | track_005 | radar | geometry=estimated_body |
| A:e17 | 5.45 | CLOSING_START | A | track_007 | radar |  |
| A:e18 | 5.45 | CRITICAL_TTC_START | A | track_005 | radar |  |
| A:e19 | 5.45 | CRITICAL_TTC_START | A | track_007 | radar |  |
| A:e20 | 5.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e21 | 5.85 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e22 | 6.15 | TRACK_APPEARED_RIGHT | A | track_008 | radar | initial_in_ego_path=False |
| A:e23 | 6.35 | TRACK_APPEARED_LEFT | A | track_009 | radar | initial_in_ego_path=False |
| A:e24 | 6.35 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e25 | 6.75 | TRACK_LOST | A | track_004 | radar |  |
| A:e26 | 6.85 | CRITICAL_TTC_START | A | track_009 | radar |  |
| A:e27 | 7.05 | CUT_IN_FROM_LEFT_START | A | track_009 | radar | geometry=estimated_body |
| A:e28 | 7.30 | COLLISION | A | - | collision_sensor | peak_impulse=389.26 |
| A:e29 | 7.30 | CRITICAL_TTC_END | A | track_007 | radar |  |
| A:e30 | 7.30 | CLOSING_END | A | track_007 | radar |  |
| A:e31 | 7.35 | THROTTLE_END | A | - | controls |  |
| A:e32 | 7.35 | BRAKE_START | A | - | controls |  |
| A:e33 | 7.40 | TURN_LEFT_START | A | - | ego |  |
| A:e34 | 7.40 | EGO_PATH_ENTRY | A | track_009 | radar | geometry=estimated_body |
| A:e35 | 7.50 | CLOSING_END | A | track_009 | radar |  |
| A:e36 | 7.55 | EGO_PATH_EXIT | A | track_005 | radar | geometry=estimated_body |
| A:e37 | 7.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e38 | 7.65 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e39 | 7.85 | CRITICAL_TTC_END | A | track_009 | radar |  |
| A:e40 | 7.95 | EGO_PATH_EXIT | A | track_009 | radar | geometry=estimated_body |
| A:e41 | 8.10 | TRACK_APPEARED_RIGHT | A | track_010 | radar | initial_in_ego_path=False |
| A:e42 | 8.25 | TURN_LEFT_END | A | - | ego |  |
| A:e43 | 8.25 | EGO_PATH_ENTRY | A | track_007 | radar | geometry=estimated_body |
| A:e44 | 8.30 | MOVING_END | A | - | ego |  |
| A:e45 | 8.30 | STOP_START | A | - | ego |  |
| A:e46 | 10.90 | CUT_IN_FROM_LEFT_END | A | track_009 | radar | geometry=estimated_body |
| A:e47 | 11.90 | TRACK_LOST | A | track_001 | radar |  |
| A:e48 | 11.90 | TRACK_LOST | A | track_010 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e09
    A:e02 --PRECEDES--> A:e09
    A:e03 --PRECEDES--> A:e09
    A:e04 --PRECEDES--> A:e09
    A:e05 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e32
    A:e29 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e43
    A:e42 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e07 --SAME_TRACK--> A:e08
    A:e10 --SAME_TRACK--> A:e11
    A:e04 --SAME_TRACK--> A:e12
    A:e10 --SAME_TRACK--> A:e13
    A:e07 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e10 --SAME_TRACK--> A:e17
    A:e09 --SAME_TRACK--> A:e18
    A:e10 --SAME_TRACK--> A:e19
    A:e05 --SAME_TRACK--> A:e20
    A:e05 --SAME_TRACK--> A:e21
    A:e23 --SAME_TRACK--> A:e24
    A:e06 --SAME_TRACK--> A:e25
    A:e23 --SAME_TRACK--> A:e26
    A:e23 --SAME_TRACK--> A:e27
    A:e10 --SAME_TRACK--> A:e29
    A:e10 --SAME_TRACK--> A:e30
    A:e23 --SAME_TRACK--> A:e34
    A:e23 --SAME_TRACK--> A:e35
    A:e09 --SAME_TRACK--> A:e36
    A:e05 --SAME_TRACK--> A:e37
    A:e05 --SAME_TRACK--> A:e38
    A:e23 --SAME_TRACK--> A:e39
    A:e23 --SAME_TRACK--> A:e40
    A:e10 --SAME_TRACK--> A:e43
    A:e23 --SAME_TRACK--> A:e46
    A:e05 --SAME_TRACK--> A:e47
    A:e41 --SAME_TRACK--> A:e48
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_002<br>A:e04 TRACK_APPEARED_FRONT track_003<br>A:e05 TRACK_APPEARED_LEFT track_001<br>A:e06 TRACK_APPEARED_LEFT track_004<br>A:e07 TRACK_APPEARED_LEFT track_006<br>A:e08 CLOSING_START track_006 | ego: not yet observed | - |
| 0.05 | A:e09 TRACK_APPEARED_LEFT track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? | 0.00 |
| 0.90 | A:e10 TRACK_APPEARED_LEFT track_007<br>A:e11 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING | 0.80 |
| 3.30 | A:e12 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING | 3.20 |
| 4.30 | A:e13 CLOSING_END track_007 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003 | 4.20 |
| 4.55 | A:e14 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 | 4.50 |
| 4.80 | A:e15 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_006 | 4.70 |
| 5.45 | A:e16 EGO_PATH_ENTRY track_005<br>A:e17 CLOSING_START track_007<br>A:e18 CRITICAL_TTC_START track_005<br>A:e19 CRITICAL_TTC_START track_007 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 5.40 |
| 5.55 | A:e20 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 5.50 |
| 5.85 | A:e21 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 5.80 |
| 6.15 | A:e22 TRACK_APPEARED_RIGHT track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 6.10 |
| 6.35 | A:e23 TRACK_APPEARED_LEFT track_009<br>A:e24 CLOSING_START track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 6.30 |
| 6.75 | A:e25 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_006 | 6.70 |
| 6.85 | A:e26 CRITICAL_TTC_START track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 6.80 |
| 7.05 | A:e27 CUT_IN_FROM_LEFT_START track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.00 |
| 7.30 | A:e28 COLLISION<br>A:e29 CRITICAL_TTC_END track_007<br>A:e30 CLOSING_END track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.20 |
| 7.35 | A:e31 THROTTLE_END<br>A:e32 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.30 |
| 7.40 | A:e33 TURN_LEFT_START<br>A:e34 EGO_PATH_ENTRY track_009 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.30 |
| 7.50 | A:e35 CLOSING_END track_009 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.40 |
| 7.55 | A:e36 EGO_PATH_EXIT track_005 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.50 |
| 7.65 | A:e37 CRITICAL_TTC_END track_001<br>A:e38 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.60 |
| 7.85 | A:e39 CRITICAL_TTC_END track_009 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.80 |
| 7.95 | A:e40 EGO_PATH_EXIT track_009 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.90 |
| 8.10 | A:e41 TRACK_APPEARED_RIGHT track_010 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 8.00 |
| 8.25 | A:e42 TURN_LEFT_END<br>A:e43 EGO_PATH_ENTRY track_007 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 8.20 |
| 8.30 | A:e44 MOVING_END<br>A:e45 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 8.20 |
| 10.90 | A:e46 CUT_IN_FROM_LEFT_END track_009 | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 10.80 |
| 11.90 | A:e47 TRACK_LOST track_001<br>A:e48 TRACK_LOST track_010 | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 11.80 |

## States still active when observation ended

- CLOSING of track_006, since A:e08 (t = 0.00 s); the track was lost at 4.55 s
- CRITICAL_TTC of track_005, since A:e18 (t = 5.45 s)
- BRAKE, since A:e32 (t = 7.35 s)
- EGO_PATH of track_007, since A:e43 (t = 8.25 s)
- STOP, since A:e45 (t = 8.30 s)

## Tracks lost

- track_006 at 4.55 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 4.80 s (A:e15): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_004, track_001, track_010

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.30 s)
- track_005: CRITICAL_TTC_START 5.45, COLLISION 7.30 (+1.85 s); EGO_PATH_ENTRY 5.45 together with critical TTC (+0.00 s)
- track_007: CRITICAL_TTC_START 5.45, COLLISION 7.30 (+1.85 s); EGO_PATH_ENTRY 8.25 after critical TTC (+2.80 s)
- track_009: critical TTC already active before the cut-in: CRITICAL_TTC_START 6.85 <= CUT_IN_FROM_LEFT_START 7.05 (+0.20 s); EGO_PATH_ENTRY 7.40 after critical TTC (+0.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.90 | 237 | 3.5 m / -36 deg | 3.36 m (3.25) | 73.0 m / +30 deg | 15.2 m/s |
| track_002 | 0.00 | 4.80 | 96 | 20.4 m / +0 deg | 20.34 m (1.70) | 20.5 m / +0 deg | 11.9 m/s |
| track_003 | 0.00 | 3.30 | 62 | 38.0 m / -4 deg | 37.53 m (2.85) | 37.5 m / -5 deg | 11.8 m/s |
| track_004 | 0.00 | 6.75 | 136 | 8.3 m / -138 deg | 8.29 m (0.00) | 20.2 m / -157 deg | 10.2 m/s |
| track_005 | 0.05 | 11.95 | 175 | 5.3 m / -18 deg | 4.82 m (3.30) | 76.5 m / +28 deg | 15.4 m/s |
| track_006 | 0.00 | 4.55 | 88 | 26.5 m / -14 deg | 18.38 m (4.55) | 18.4 m / -16 deg | 10.3 m/s |
| track_007 | 0.90 | 11.95 | 222 | 9.7 m / -45 deg | 0.48 m (7.95) | 0.5 m / -102 deg | 12.1 m/s |
| track_008 | 6.15 | 11.95 | 111 | 20.9 m / +9 deg | 20.92 m (6.15) | 68.8 m / +33 deg | 12.1 m/s |
| track_009 | 6.35 | 11.95 | 113 | 14.3 m / -12 deg | 11.74 m (7.65) | 52.3 m / +30 deg | 10.4 m/s |
| track_010 | 8.10 | 11.90 | 51 | 41.0 m / +33 deg | 41.02 m (8.10) | 86.4 m / +27 deg | 12.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.00 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_005, which appeared on its left.
- t = 0.90 s: A's radar started tracking track_007, which appeared on its left.
- t = 0.90 s: A observed track_007 start closing in (already the case when first observed).
- t = 3.30 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 4.30 s: A observed track_007 stop closing in.
- t = 4.55 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 4.80 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.45 s: A observed track_005 enter its forward path corridor.
- t = 5.45 s: A observed track_007 start closing in.
- t = 5.45 s: A's time-to-contact with track_005 became critical.
- t = 5.45 s: A's time-to-contact with track_007 became critical.
- t = 5.55 s: A's time-to-contact with track_001 became critical.
- t = 5.85 s: A observed track_001 enter its forward path corridor.
- t = 6.15 s: A's radar started tracking track_008, which appeared on its right.
- t = 6.35 s: A's radar started tracking track_009, which appeared on its left.
- t = 6.35 s: A observed track_009 start closing in (already the case when first observed).
- t = 6.75 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 6.85 s: A's time-to-contact with track_009 became critical.
- t = 7.05 s: A observed track_009 cutting in from the left.
- t = 7.30 s: A's collision sensor recorded a contact (peak impulse 389 N*s).
- t = 7.30 s: A's time-to-contact with track_007 stopped being critical.
- t = 7.30 s: A observed track_007 stop closing in.
- t = 7.35 s: A released the accelerator.
- t = 7.35 s: A started braking.
- t = 7.40 s: A started turning left.
- t = 7.40 s: A observed track_009 enter its forward path corridor.
- t = 7.50 s: A observed track_009 stop closing in.
- t = 7.55 s: A observed track_005 leave its forward path corridor.
- t = 7.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 7.65 s: A observed track_001 leave its forward path corridor.
- t = 7.85 s: A's time-to-contact with track_009 stopped being critical.
- t = 7.95 s: A observed track_009 leave its forward path corridor.
- t = 8.10 s: A's radar started tracking track_010, which appeared on its right.
- t = 8.25 s: A stopped turning left.
- t = 8.25 s: A observed track_007 enter its forward path corridor.
- t = 8.30 s: A stopped moving.
- t = 8.30 s: A came to a stop.
- t = 10.90 s: A observed track_009's cut-in from the left settle.
- t = 11.90 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 11.90 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
