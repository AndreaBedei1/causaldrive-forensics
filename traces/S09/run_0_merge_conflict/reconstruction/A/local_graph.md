# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 25.013249535113573 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 14 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 51; edges: 194 (PRECEDES 164, SAME_TRACK 30)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TURN_LEFT_START | A | - | ego | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e04 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.00 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 0.20 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e07 | 0.20 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e08 | 0.20 | TRACK_APPEARED_LEFT | A | track_004 | radar |  |
| A:e09 | 0.20 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e10 | 0.20 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e11 | 0.20 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e12 | 0.20 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e13 | 0.20 | TRACK_APPEARED_LEFT | A | track_009 | radar |  |
| A:e14 | 0.20 | TRACK_APPEARED_LEFT | A | track_010 | radar |  |
| A:e15 | 0.20 | TRACK_APPEARED_LEFT | A | track_012 | radar |  |
| A:e16 | 0.20 | TRACK_APPEARED_RIGHT | A | track_011 | radar |  |
| A:e17 | 0.20 | TRACK_APPEARED_RIGHT | A | track_013 | radar |  |
| A:e18 | 0.20 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e19 | 0.20 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e20 | 0.20 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e21 | 0.20 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e22 | 0.20 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e23 | 0.20 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e24 | 0.20 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e25 | 0.20 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e26 | 0.20 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e27 | 0.20 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e28 | 0.25 | TRACK_APPEARED_RIGHT | A | track_014 | radar |  |
| A:e29 | 0.40 | TRACK_LOST | A | track_007 | radar |  |
| A:e30 | 0.40 | TRACK_LOST | A | track_011 | radar |  |
| A:e31 | 0.45 | TRACK_LOST | A | track_013 | radar |  |
| A:e32 | 0.60 | TRACK_LOST | A | track_014 | radar |  |
| A:e33 | 1.45 | TRACK_LOST | A | track_002 | radar |  |
| A:e34 | 1.55 | TRACK_LOST | A | track_009 | radar |  |
| A:e35 | 1.60 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e36 | 1.65 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar |  |
| A:e37 | 1.65 | TRACK_LOST | A | track_005 | radar |  |
| A:e38 | 1.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e39 | 1.80 | COLLISION | A | - | collision_sensor | peak_impulse=1247.19 |
| A:e40 | 1.85 | BRAKE_START | A | - | controls |  |
| A:e41 | 1.85 | TRACK_LOST | A | track_012 | radar |  |
| A:e42 | 1.90 | CLOSING_END | A | track_001 | radar |  |
| A:e43 | 1.95 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar |  |
| A:e44 | 2.45 | CLOSING_END | A | track_010 | radar |  |
| A:e45 | 2.45 | TURN_LEFT_END | A | - | ego |  |
| A:e46 | 2.50 | CLOSING_END | A | track_003 | radar |  |
| A:e47 | 2.50 | CLOSING_END | A | track_004 | radar |  |
| A:e48 | 2.50 | CLOSING_END | A | track_006 | radar |  |
| A:e49 | 2.50 | CLOSING_END | A | track_008 | radar |  |
| A:e50 | 2.50 | MOVING_END | A | - | ego |  |
| A:e51 | 2.50 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e06
    A:e01 --PRECEDES--> A:e07
    A:e01 --PRECEDES--> A:e08
    A:e01 --PRECEDES--> A:e09
    A:e01 --PRECEDES--> A:e10
    A:e01 --PRECEDES--> A:e11
    A:e01 --PRECEDES--> A:e12
    A:e01 --PRECEDES--> A:e13
    A:e01 --PRECEDES--> A:e14
    A:e01 --PRECEDES--> A:e15
    A:e01 --PRECEDES--> A:e16
    A:e01 --PRECEDES--> A:e17
    A:e01 --PRECEDES--> A:e18
    A:e01 --PRECEDES--> A:e19
    A:e01 --PRECEDES--> A:e20
    A:e01 --PRECEDES--> A:e21
    A:e01 --PRECEDES--> A:e22
    A:e01 --PRECEDES--> A:e23
    A:e01 --PRECEDES--> A:e24
    A:e01 --PRECEDES--> A:e25
    A:e01 --PRECEDES--> A:e26
    A:e01 --PRECEDES--> A:e27
    A:e02 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e08
    A:e02 --PRECEDES--> A:e09
    A:e02 --PRECEDES--> A:e10
    A:e02 --PRECEDES--> A:e11
    A:e02 --PRECEDES--> A:e12
    A:e02 --PRECEDES--> A:e13
    A:e02 --PRECEDES--> A:e14
    A:e02 --PRECEDES--> A:e15
    A:e02 --PRECEDES--> A:e16
    A:e02 --PRECEDES--> A:e17
    A:e02 --PRECEDES--> A:e18
    A:e02 --PRECEDES--> A:e19
    A:e02 --PRECEDES--> A:e20
    A:e02 --PRECEDES--> A:e21
    A:e02 --PRECEDES--> A:e22
    A:e02 --PRECEDES--> A:e23
    A:e02 --PRECEDES--> A:e24
    A:e02 --PRECEDES--> A:e25
    A:e02 --PRECEDES--> A:e26
    A:e02 --PRECEDES--> A:e27
    A:e03 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e07
    A:e03 --PRECEDES--> A:e08
    A:e03 --PRECEDES--> A:e09
    A:e03 --PRECEDES--> A:e10
    A:e03 --PRECEDES--> A:e11
    A:e03 --PRECEDES--> A:e12
    A:e03 --PRECEDES--> A:e13
    A:e03 --PRECEDES--> A:e14
    A:e03 --PRECEDES--> A:e15
    A:e03 --PRECEDES--> A:e16
    A:e03 --PRECEDES--> A:e17
    A:e03 --PRECEDES--> A:e18
    A:e03 --PRECEDES--> A:e19
    A:e03 --PRECEDES--> A:e20
    A:e03 --PRECEDES--> A:e21
    A:e03 --PRECEDES--> A:e22
    A:e03 --PRECEDES--> A:e23
    A:e03 --PRECEDES--> A:e24
    A:e03 --PRECEDES--> A:e25
    A:e03 --PRECEDES--> A:e26
    A:e03 --PRECEDES--> A:e27
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e09
    A:e04 --PRECEDES--> A:e10
    A:e04 --PRECEDES--> A:e11
    A:e04 --PRECEDES--> A:e12
    A:e04 --PRECEDES--> A:e13
    A:e04 --PRECEDES--> A:e14
    A:e04 --PRECEDES--> A:e15
    A:e04 --PRECEDES--> A:e16
    A:e04 --PRECEDES--> A:e17
    A:e04 --PRECEDES--> A:e18
    A:e04 --PRECEDES--> A:e19
    A:e04 --PRECEDES--> A:e20
    A:e04 --PRECEDES--> A:e21
    A:e04 --PRECEDES--> A:e22
    A:e04 --PRECEDES--> A:e23
    A:e04 --PRECEDES--> A:e24
    A:e04 --PRECEDES--> A:e25
    A:e04 --PRECEDES--> A:e26
    A:e04 --PRECEDES--> A:e27
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e05 --PRECEDES--> A:e09
    A:e05 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e11
    A:e05 --PRECEDES--> A:e12
    A:e05 --PRECEDES--> A:e13
    A:e05 --PRECEDES--> A:e14
    A:e05 --PRECEDES--> A:e15
    A:e05 --PRECEDES--> A:e16
    A:e05 --PRECEDES--> A:e17
    A:e05 --PRECEDES--> A:e18
    A:e05 --PRECEDES--> A:e19
    A:e05 --PRECEDES--> A:e20
    A:e05 --PRECEDES--> A:e21
    A:e05 --PRECEDES--> A:e22
    A:e05 --PRECEDES--> A:e23
    A:e05 --PRECEDES--> A:e24
    A:e05 --PRECEDES--> A:e25
    A:e05 --PRECEDES--> A:e26
    A:e05 --PRECEDES--> A:e27
    A:e06 --PRECEDES--> A:e28
    A:e07 --PRECEDES--> A:e28
    A:e08 --PRECEDES--> A:e28
    A:e09 --PRECEDES--> A:e28
    A:e10 --PRECEDES--> A:e28
    A:e11 --PRECEDES--> A:e28
    A:e12 --PRECEDES--> A:e28
    A:e13 --PRECEDES--> A:e28
    A:e14 --PRECEDES--> A:e28
    A:e15 --PRECEDES--> A:e28
    A:e16 --PRECEDES--> A:e28
    A:e17 --PRECEDES--> A:e28
    A:e18 --PRECEDES--> A:e28
    A:e19 --PRECEDES--> A:e28
    A:e20 --PRECEDES--> A:e28
    A:e21 --PRECEDES--> A:e28
    A:e22 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e28
    A:e24 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e31
    A:e31 --PRECEDES--> A:e32
    A:e32 --PRECEDES--> A:e33
    A:e33 --PRECEDES--> A:e34
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e42
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e44 --PRECEDES--> A:e47
    A:e44 --PRECEDES--> A:e48
    A:e44 --PRECEDES--> A:e49
    A:e44 --PRECEDES--> A:e50
    A:e44 --PRECEDES--> A:e51
    A:e45 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e47
    A:e45 --PRECEDES--> A:e48
    A:e45 --PRECEDES--> A:e49
    A:e45 --PRECEDES--> A:e50
    A:e45 --PRECEDES--> A:e51
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e06 --SAME_TRACK--> A:e18
    A:e07 --SAME_TRACK--> A:e19
    A:e08 --SAME_TRACK--> A:e20
    A:e09 --SAME_TRACK--> A:e21
    A:e10 --SAME_TRACK--> A:e22
    A:e11 --SAME_TRACK--> A:e23
    A:e12 --SAME_TRACK--> A:e24
    A:e13 --SAME_TRACK--> A:e25
    A:e14 --SAME_TRACK--> A:e26
    A:e15 --SAME_TRACK--> A:e27
    A:e11 --SAME_TRACK--> A:e29
    A:e16 --SAME_TRACK--> A:e30
    A:e17 --SAME_TRACK--> A:e31
    A:e28 --SAME_TRACK--> A:e32
    A:e06 --SAME_TRACK--> A:e33
    A:e13 --SAME_TRACK--> A:e34
    A:e03 --SAME_TRACK--> A:e35
    A:e03 --SAME_TRACK--> A:e36
    A:e09 --SAME_TRACK--> A:e37
    A:e03 --SAME_TRACK--> A:e38
    A:e15 --SAME_TRACK--> A:e41
    A:e03 --SAME_TRACK--> A:e42
    A:e03 --SAME_TRACK--> A:e43
    A:e14 --SAME_TRACK--> A:e44
    A:e07 --SAME_TRACK--> A:e46
    A:e08 --SAME_TRACK--> A:e47
    A:e10 --SAME_TRACK--> A:e48
    A:e12 --SAME_TRACK--> A:e49
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TURN_LEFT_START<br>A:e03 TRACK_APPEARED_RIGHT track_001<br>A:e04 CLOSING_START track_001<br>A:e05 CRITICAL_TTC_START track_001 | ego: not yet observed | - |
| 0.20 | A:e06 TRACK_APPEARED_LEFT track_002<br>A:e07 TRACK_APPEARED_LEFT track_003<br>A:e08 TRACK_APPEARED_LEFT track_004<br>A:e09 TRACK_APPEARED_LEFT track_005<br>A:e10 TRACK_APPEARED_LEFT track_006<br>A:e11 TRACK_APPEARED_LEFT track_007<br>A:e12 TRACK_APPEARED_LEFT track_008<br>A:e13 TRACK_APPEARED_LEFT track_009<br>A:e14 TRACK_APPEARED_LEFT track_010<br>A:e15 TRACK_APPEARED_LEFT track_012<br>A:e16 TRACK_APPEARED_RIGHT track_011<br>A:e17 TRACK_APPEARED_RIGHT track_013<br>A:e18 CLOSING_START track_002<br>A:e19 CLOSING_START track_003<br>A:e20 CLOSING_START track_004<br>A:e21 CLOSING_START track_005<br>A:e22 CLOSING_START track_006<br>A:e23 CLOSING_START track_007<br>A:e24 CLOSING_START track_008<br>A:e25 CLOSING_START track_009<br>A:e26 CLOSING_START track_010<br>A:e27 CLOSING_START track_012 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 0.10 |
| 0.25 | A:e28 TRACK_APPEARED_RIGHT track_014 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.20 |
| 0.40 | A:e29 TRACK_LOST track_007<br>A:e30 TRACK_LOST track_011 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.30 |
| 0.45 | A:e31 TRACK_LOST track_013 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_007, track_011 | 0.40 |
| 0.60 | A:e32 TRACK_LOST track_014 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_007, track_011, track_013 | 0.50 |
| 1.45 | A:e33 TRACK_LOST track_002 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_007, track_011, track_013, track_014 | 1.40 |
| 1.55 | A:e34 TRACK_LOST track_009 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_011, track_013, track_014 | 1.50 |
| 1.60 | A:e35 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_009, track_011, track_013, track_014 | 1.50 |
| 1.65 | A:e36 CUT_IN_FROM_RIGHT_START track_001<br>A:e37 TRACK_LOST track_005 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_009, track_011, track_013, track_014 | 1.60 |
| 1.75 | A:e38 CRITICAL_TTC_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 | 1.70 |
| 1.80 | A:e39 COLLISION | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 | 1.70 |
| 1.85 | A:e40 BRAKE_START<br>A:e41 TRACK_LOST track_012 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 | 1.80 |
| 1.90 | A:e42 CLOSING_END track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 | 1.80 |
| 1.95 | A:e43 CUT_IN_FROM_RIGHT_END track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 | 1.90 |
| 2.45 | A:e44 CLOSING_END track_010<br>A:e45 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 | 2.40 |
| 2.50 | A:e46 CLOSING_END track_003<br>A:e47 CLOSING_END track_004<br>A:e48 CLOSING_END track_006<br>A:e49 CLOSING_END track_008<br>A:e50 MOVING_END<br>A:e51 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 | 2.40 |

## States still active when observation ended

- CLOSING of track_002, since A:e18 (t = 0.20 s); the track was lost at 1.45 s
- CLOSING of track_005, since A:e21 (t = 0.20 s); the track was lost at 1.65 s
- CLOSING of track_007, since A:e23 (t = 0.20 s); the track was lost at 0.40 s
- CLOSING of track_009, since A:e25 (t = 0.20 s); the track was lost at 1.55 s
- CLOSING of track_012, since A:e27 (t = 0.20 s); the track was lost at 1.85 s
- EGO_PATH of track_001, since A:e35 (t = 1.60 s)
- BRAKE, since A:e40 (t = 1.85 s)
- STOP, since A:e51 (t = 2.50 s)

## Tracks lost

- track_007 at 0.40 s (A:e29): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 1.45 s (A:e33): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 1.55 s (A:e34): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 1.65 s (A:e37): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 1.85 s (A:e41): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_011, track_013, track_014

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 0.00 <= CUT_IN_FROM_RIGHT_START 1.65 (+1.65 s); EGO_PATH_ENTRY 1.60 after critical TTC (+1.60 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.95 | 300 | 7.5 m / +38 deg | 1.05 m (12.85) | 1.1 m / +68 deg | 7.9 m/s |
| track_002 | 0.20 | 1.45 | 17 | 28.1 m / -68 deg | 21.19 m (1.45) | 21.2 m / -57 deg | 2.5 m/s |
| track_003 | 0.20 | 14.95 | 296 | 21.2 m / -74 deg | 11.49 m (2.50) | 11.7 m / -69 deg | 1.4 m/s |
| track_004 | 0.20 | 14.95 | 296 | 48.1 m / -53 deg | 32.20 m (2.70) | 32.6 m / -12 deg | 3.3 m/s |
| track_005 | 0.20 | 1.65 | 30 | 15.8 m / -80 deg | 10.90 m (1.65) | 10.9 m / -81 deg | 3.2 m/s |
| track_006 | 0.20 | 14.95 | 290 | 46.0 m / -57 deg | 30.80 m (6.60) | 31.0 m / -19 deg | 6.6 m/s |
| track_007 | 0.20 | 0.40 | 5 | 69.0 m / -76 deg | 67.83 m (0.40) | 67.8 m / -69 deg | 8.8 m/s |
| track_008 | 0.20 | 14.95 | 296 | 48.4 m / -67 deg | 34.69 m (2.55) | 34.9 m / -28 deg | 1.9 m/s |
| track_009 | 0.20 | 1.55 | 20 | 45.2 m / -62 deg | 36.10 m (1.55) | 36.1 m / -35 deg | 1.9 m/s |
| track_010 | 0.20 | 14.95 | 172 | 52.2 m / -71 deg | 39.80 m (2.45) | 41.9 m / -32 deg | 1.4 m/s |
| track_011 | 0.20 | 0.40 | 5 | 32.0 m / +67 deg | 32.04 m (0.20) | 32.4 m / +79 deg | 2.1 m/s |
| track_012 | 0.20 | 1.85 | 29 | 15.8 m / -69 deg | 7.72 m (1.85) | 7.7 m / -67 deg | 3.2 m/s |
| track_013 | 0.20 | 0.45 | 5 | 150.9 m / +66 deg | 150.92 m (0.20) | 151.3 m / +79 deg | 1.5 m/s |
| track_014 | 0.25 | 0.60 | 8 | 20.7 m / +64 deg | 20.68 m (0.25) | 21.0 m / +80 deg | 6.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A started turning left (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.20 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_003, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_004, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_005, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_007, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_008, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_009, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_010, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_012, which appeared on its left.
- t = 0.20 s: A's radar started tracking track_011, which appeared on its right.
- t = 0.20 s: A's radar started tracking track_013, which appeared on its right.
- t = 0.20 s: A observed track_002 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_003 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_004 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_005 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_006 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_007 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_008 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_009 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_010 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_012 start closing in (already the case when first observed).
- t = 0.25 s: A's radar started tracking track_014, which appeared on its right.
- t = 0.40 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 0.40 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 0.45 s: A's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 0.60 s: A's radar lost track_014 (its states are UNKNOWN from then on, not ended).
- t = 1.45 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 1.55 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 1.60 s: A observed track_001 enter its forward path corridor.
- t = 1.65 s: A observed track_001 cutting in from the right.
- t = 1.65 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 1.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 1.80 s: A's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.85 s: A started braking.
- t = 1.85 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 1.90 s: A observed track_001 stop closing in.
- t = 1.95 s: A observed track_001's cut-in from the right settle.
- t = 2.45 s: A observed track_010 stop closing in.
- t = 2.45 s: A stopped turning left.
- t = 2.50 s: A observed track_003 stop closing in.
- t = 2.50 s: A observed track_004 stop closing in.
- t = 2.50 s: A observed track_006 stop closing in.
- t = 2.50 s: A observed track_008 stop closing in.
- t = 2.50 s: A stopped moving.
- t = 2.50 s: A came to a stop.
