# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 534.8805473558605 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 49; edges: 101 (PRECEDES 72, SAME_TRACK 29)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 0.40 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e07 | 0.50 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e08 | 0.50 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e09 | 0.75 | TRACK_LOST | B | track_004 | radar |  |
| B:e10 | 0.90 | TRACK_APPEARED_RIGHT | B | track_005 | radar | initial_in_ego_path=False |
| B:e11 | 0.90 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e12 | 0.95 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e13 | 0.95 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e14 | 2.15 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e15 | 2.15 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e16 | 2.30 | CLOSING_END | B | track_001 | radar |  |
| B:e17 | 2.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e18 | 2.40 | TRACK_LOST | B | track_007 | radar |  |
| B:e19 | 2.55 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e20 | 2.55 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e21 | 2.55 | TRACK_LOST | B | track_003 | radar |  |
| B:e22 | 3.35 | TRACK_LOST | B | track_006 | radar |  |
| B:e23 | 3.40 | TRACK_LOST | B | track_008 | radar |  |
| B:e24 | 3.50 | TRACK_APPEARED_RIGHT | B | track_009 | radar | initial_in_ego_path=False |
| B:e25 | 5.40 | TRACK_LOST | B | track_009 | radar |  |
| B:e26 | 5.80 | CLOSING_END | B | track_005 | radar |  |
| B:e27 | 5.80 | TRACK_LOST | B | track_005 | radar |  |
| B:e28 | 6.65 | TRACK_APPEARED_RIGHT | B | track_010 | radar | initial_in_ego_path=False |
| B:e29 | 6.65 | CLOSING_START | B | track_010 | radar | active_at_first_observation=True |
| B:e30 | 6.70 | TRACK_APPEARED_RIGHT | B | track_011 | radar | initial_in_ego_path=False |
| B:e31 | 6.70 | CLOSING_START | B | track_011 | radar | active_at_first_observation=True |
| B:e32 | 6.95 | TRACK_APPEARED_RIGHT | B | track_012 | radar | initial_in_ego_path=False |
| B:e33 | 7.60 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e34 | 7.70 | CLOSING_START | B | track_002 | radar |  |
| B:e35 | 8.50 | COLLISION | B | - | collision_sensor | peak_impulse=745.29 |
| B:e36 | 8.50 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e37 | 8.55 | THROTTLE_END | B | - | controls |  |
| B:e38 | 8.55 | BRAKE_START | B | - | controls |  |
| B:e39 | 9.10 | CLOSING_END | B | track_002 | radar |  |
| B:e40 | 9.10 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e41 | 9.20 | TRACK_LOST | B | track_012 | radar |  |
| B:e42 | 9.30 | CLOSING_END | B | track_010 | radar |  |
| B:e43 | 9.30 | CLOSING_END | B | track_011 | radar |  |
| B:e44 | 9.50 | EGO_PATH_EXIT | B | track_002 | radar | geometry=estimated_body |
| B:e45 | 9.60 | MOVING_END | B | - | ego |  |
| B:e46 | 9.60 | STOP_START | B | - | ego |  |
| B:e47 | 9.85 | TRACK_APPEARED_RIGHT | B | track_013 | radar | initial_in_ego_path=False |
| B:e48 | 9.85 | CLOSING_START | B | track_013 | radar | active_at_first_observation=True |
| B:e49 | 10.55 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e38
    B:e36 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e37 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e41
    B:e40 --PRECEDES--> B:e41
    B:e41 --PRECEDES--> B:e42
    B:e41 --PRECEDES--> B:e43
    B:e42 --PRECEDES--> B:e44
    B:e43 --PRECEDES--> B:e44
    B:e44 --PRECEDES--> B:e45
    B:e44 --PRECEDES--> B:e46
    B:e45 --PRECEDES--> B:e47
    B:e45 --PRECEDES--> B:e48
    B:e46 --PRECEDES--> B:e47
    B:e46 --PRECEDES--> B:e48
    B:e47 --PRECEDES--> B:e49
    B:e48 --PRECEDES--> B:e49
    B:e03 --SAME_TRACK--> B:e05
    B:e07 --SAME_TRACK--> B:e08
    B:e07 --SAME_TRACK--> B:e09
    B:e10 --SAME_TRACK--> B:e11
    B:e12 --SAME_TRACK--> B:e13
    B:e14 --SAME_TRACK--> B:e15
    B:e03 --SAME_TRACK--> B:e16
    B:e03 --SAME_TRACK--> B:e17
    B:e14 --SAME_TRACK--> B:e18
    B:e19 --SAME_TRACK--> B:e20
    B:e06 --SAME_TRACK--> B:e21
    B:e12 --SAME_TRACK--> B:e22
    B:e19 --SAME_TRACK--> B:e23
    B:e24 --SAME_TRACK--> B:e25
    B:e10 --SAME_TRACK--> B:e26
    B:e10 --SAME_TRACK--> B:e27
    B:e28 --SAME_TRACK--> B:e29
    B:e30 --SAME_TRACK--> B:e31
    B:e04 --SAME_TRACK--> B:e33
    B:e04 --SAME_TRACK--> B:e34
    B:e04 --SAME_TRACK--> B:e36
    B:e04 --SAME_TRACK--> B:e39
    B:e04 --SAME_TRACK--> B:e40
    B:e32 --SAME_TRACK--> B:e41
    B:e28 --SAME_TRACK--> B:e42
    B:e30 --SAME_TRACK--> B:e43
    B:e04 --SAME_TRACK--> B:e44
    B:e47 --SAME_TRACK--> B:e48
    B:e04 --SAME_TRACK--> B:e49
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 CLOSING_START track_001 | ego: not yet observed | - |
| 0.40 | B:e06 TRACK_APPEARED_RIGHT track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? | 0.30 |
| 0.50 | B:e07 TRACK_APPEARED_RIGHT track_004<br>B:e08 CLOSING_START track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.40 |
| 0.75 | B:e09 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.70 |
| 0.90 | B:e10 TRACK_APPEARED_RIGHT track_005<br>B:e11 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 | 0.80 |
| 0.95 | B:e12 TRACK_APPEARED_RIGHT track_006<br>B:e13 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 | 0.90 |
| 2.15 | B:e14 TRACK_APPEARED_RIGHT track_007<br>B:e15 CLOSING_START track_007 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_004 | 2.10 |
| 2.30 | B:e16 CLOSING_END track_001<br>B:e17 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004 | 2.20 |
| 2.40 | B:e18 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_004 | 2.30 |
| 2.55 | B:e19 TRACK_APPEARED_RIGHT track_008<br>B:e20 CLOSING_START track_008<br>B:e21 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_007 | 2.50 |
| 3.35 | B:e22 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_007 | 3.30 |
| 3.40 | B:e23 TRACK_LOST track_008 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007 | 3.30 |
| 3.50 | B:e24 TRACK_APPEARED_RIGHT track_009 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007, track_008 | 3.40 |
| 5.40 | B:e25 TRACK_LOST track_009 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track_009: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007, track_008 | 5.30 |
| 5.80 | B:e26 CLOSING_END track_005<br>B:e27 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007, track_008, track_009 | 5.70 |
| 6.65 | B:e28 TRACK_APPEARED_RIGHT track_010<br>B:e29 CLOSING_START track_010 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 6.60 |
| 6.70 | B:e30 TRACK_APPEARED_RIGHT track_011<br>B:e31 CLOSING_START track_011 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 6.60 |
| 6.95 | B:e32 TRACK_APPEARED_RIGHT track_012 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 6.90 |
| 7.60 | B:e33 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 7.50 |
| 7.70 | B:e34 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 7.60 |
| 8.50 | B:e35 COLLISION<br>B:e36 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 8.40 |
| 8.55 | B:e37 THROTTLE_END<br>B:e38 BRAKE_START | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 8.50 |
| 9.10 | B:e39 CLOSING_END track_002<br>B:e40 EGO_PATH_ENTRY track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 9.00 |
| 9.20 | B:e41 TRACK_LOST track_012 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 | 9.10 |
| 9.30 | B:e42 CLOSING_END track_010<br>B:e43 CLOSING_END track_011 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_010: CLOSING<br>track_011: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 | 9.20 |
| 9.50 | B:e44 EGO_PATH_EXIT track_002 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 | 9.40 |
| 9.60 | B:e45 MOVING_END<br>B:e46 STOP_START | ego: MOVING, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 | 9.50 |
| 9.85 | B:e47 TRACK_APPEARED_RIGHT track_013<br>B:e48 CLOSING_START track_013 | ego: STOP, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 | 9.80 |
| 10.55 | B:e49 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 | 10.50 |

## States still active when observation ended

- CLOSING of track_004, since B:e08 (t = 0.50 s); the track was lost at 0.75 s
- CLOSING of track_006, since B:e13 (t = 0.95 s); the track was lost at 3.35 s
- CLOSING of track_007, since B:e15 (t = 2.15 s); the track was lost at 2.40 s
- CLOSING of track_008, since B:e20 (t = 2.55 s); the track was lost at 3.40 s
- BRAKE, since B:e38 (t = 8.55 s)
- STOP, since B:e46 (t = 9.60 s)
- CLOSING of track_013, since B:e48 (t = 9.85 s)
- EGO_PATH of track_002, since B:e49 (t = 10.55 s)

## Tracks lost

- track_004 at 0.75 s (B:e09): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 2.30 s (B:e17): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 2.40 s (B:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.35 s (B:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 3.40 s (B:e23): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 5.80 s (B:e27): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_009, track_012

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 7.60, COLLISION 8.50 (+0.90 s); EGO_PATH_ENTRY 9.10 after critical TTC (+1.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 2.30 | 47 | 16.3 m / +22 deg | 5.52 m (2.30) | 5.5 m / +68 deg | 7.0 m/s |
| track_002 | 0.00 | 11.95 | 240 | 1.5 m / +96 deg | 0.03 m (8.50) | 0.6 m / -82 deg | 13.5 m/s |
| track_003 | 0.40 | 2.55 | 44 | 6.8 m / +138 deg | 6.76 m (0.40) | 19.7 m / +157 deg | 7.7 m/s |
| track_004 | 0.50 | 0.75 | 6 | 35.9 m / +10 deg | 34.12 m (0.75) | 34.1 m / +11 deg | 5.8 m/s |
| track_005 | 0.90 | 5.80 | 99 | 33.1 m / +12 deg | 5.44 m (5.80) | 5.4 m / +69 deg | 7.3 m/s |
| track_006 | 0.95 | 3.35 | 44 | 58.4 m / +5 deg | 42.13 m (3.35) | 42.1 m / +4 deg | 7.2 m/s |
| track_007 | 2.15 | 2.40 | 6 | 51.0 m / +7 deg | 49.28 m (2.40) | 49.3 m / +8 deg | 6.2 m/s |
| track_008 | 2.55 | 3.40 | 12 | 48.7 m / +8 deg | 42.97 m (3.40) | 43.0 m / +8 deg | 6.1 m/s |
| track_009 | 3.50 | 5.40 | 39 | 7.3 m / +139 deg | 7.29 m (3.50) | 19.1 m / +156 deg | 7.1 m/s |
| track_010 | 6.65 | 11.95 | 107 | 19.7 m / +8 deg | 4.01 m (9.30) | 17.6 m / +12 deg | 6.2 m/s |
| track_011 | 6.70 | 11.95 | 106 | 20.7 m / +17 deg | 7.35 m (9.30) | 19.2 m / +20 deg | 6.4 m/s |
| track_012 | 6.95 | 9.20 | 38 | 7.6 m / +139 deg | 7.56 m (6.95) | 20.0 m / +156 deg | 8.3 m/s |
| track_013 | 9.85 | 11.95 | 43 | 17.6 m / +156 deg | 6.67 m (11.95) | 6.7 m / +128 deg | 5.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.40 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.50 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.50 s: B observed track_004 start closing in (already the case when first observed).
- t = 0.75 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 0.90 s: B's radar started tracking track_005, which appeared on its right.
- t = 0.90 s: B observed track_005 start closing in (already the case when first observed).
- t = 0.95 s: B's radar started tracking track_006, which appeared on its right.
- t = 0.95 s: B observed track_006 start closing in (already the case when first observed).
- t = 2.15 s: B's radar started tracking track_007, which appeared on its right.
- t = 2.15 s: B observed track_007 start closing in (already the case when first observed).
- t = 2.30 s: B observed track_001 stop closing in.
- t = 2.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.40 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 2.55 s: B's radar started tracking track_008, which appeared on its right.
- t = 2.55 s: B observed track_008 start closing in (already the case when first observed).
- t = 2.55 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.35 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 3.40 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 3.50 s: B's radar started tracking track_009, which appeared on its right.
- t = 5.40 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 5.80 s: B observed track_005 stop closing in.
- t = 5.80 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 6.65 s: B's radar started tracking track_010, which appeared on its right.
- t = 6.65 s: B observed track_010 start closing in (already the case when first observed).
- t = 6.70 s: B's radar started tracking track_011, which appeared on its right.
- t = 6.70 s: B observed track_011 start closing in (already the case when first observed).
- t = 6.95 s: B's radar started tracking track_012, which appeared on its right.
- t = 7.60 s: B's time-to-contact with track_002 became critical.
- t = 7.70 s: B observed track_002 start closing in.
- t = 8.50 s: B's collision sensor recorded a contact (peak impulse 745 N*s).
- t = 8.50 s: B's time-to-contact with track_002 stopped being critical.
- t = 8.55 s: B released the accelerator.
- t = 8.55 s: B started braking.
- t = 9.10 s: B observed track_002 stop closing in.
- t = 9.10 s: B observed track_002 enter its forward path corridor.
- t = 9.20 s: B's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 9.30 s: B observed track_010 stop closing in.
- t = 9.30 s: B observed track_011 stop closing in.
- t = 9.50 s: B observed track_002 leave its forward path corridor.
- t = 9.60 s: B stopped moving.
- t = 9.60 s: B came to a stop.
- t = 9.85 s: B's radar started tracking track_013, which appeared on its right.
- t = 9.85 s: B observed track_013 start closing in (already the case when first observed).
- t = 10.55 s: B observed track_002 enter its forward path corridor.
