# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 25.013249535113573 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 14 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 46; edges: 195 (PRECEDES 172, SAME_TRACK 23)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TURN_RIGHT_START | B | - | ego | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e04 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 0.00 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 0.20 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e07 | 0.20 | TRACK_APPEARED_LEFT | B | track_007 | radar |  |
| B:e08 | 0.20 | TRACK_APPEARED_LEFT | B | track_008 | radar |  |
| B:e09 | 0.20 | TRACK_APPEARED_RIGHT | B | track_003 | radar |  |
| B:e10 | 0.20 | TRACK_APPEARED_RIGHT | B | track_004 | radar |  |
| B:e11 | 0.20 | TRACK_APPEARED_RIGHT | B | track_005 | radar |  |
| B:e12 | 0.20 | TRACK_APPEARED_RIGHT | B | track_006 | radar |  |
| B:e13 | 0.20 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e14 | 0.20 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e15 | 0.20 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e16 | 0.20 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e17 | 0.25 | TRACK_APPEARED_LEFT | B | track_009 | radar |  |
| B:e18 | 0.25 | TRACK_APPEARED_LEFT | B | track_010 | radar |  |
| B:e19 | 0.25 | TRACK_APPEARED_LEFT | B | track_011 | radar |  |
| B:e20 | 0.25 | TRACK_APPEARED_LEFT | B | track_012 | radar |  |
| B:e21 | 0.25 | TRACK_APPEARED_LEFT | B | track_013 | radar |  |
| B:e22 | 0.25 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e23 | 0.25 | TRACK_LOST | B | track_001 | radar |  |
| B:e24 | 0.30 | TRACK_APPEARED_LEFT | B | track_014 | radar |  |
| B:e25 | 0.30 | CLOSING_START | B | track_014 | radar | active_at_first_observation=True |
| B:e26 | 0.40 | TRACK_LOST | B | track_002 | radar |  |
| B:e27 | 0.40 | TRACK_LOST | B | track_007 | radar |  |
| B:e28 | 0.45 | TRACK_LOST | B | track_008 | radar |  |
| B:e29 | 0.50 | TRACK_LOST | B | track_011 | radar |  |
| B:e30 | 0.55 | TRACK_LOST | B | track_012 | radar |  |
| B:e31 | 0.60 | TRACK_LOST | B | track_013 | radar |  |
| B:e32 | 0.65 | TRACK_LOST | B | track_010 | radar |  |
| B:e33 | 0.80 | CLOSING_END | B | track_009 | radar |  |
| B:e34 | 0.90 | TRACK_LOST | B | track_009 | radar |  |
| B:e35 | 1.20 | TURN_RIGHT_END | B | - | ego |  |
| B:e36 | 1.50 | TRACK_LOST | B | track_006 | radar |  |
| B:e37 | 1.80 | COLLISION | B | - | collision_sensor | peak_impulse=1247.19 |
| B:e38 | 1.85 | BRAKE_START | B | - | controls |  |
| B:e39 | 1.85 | TURN_LEFT_START | B | - | ego |  |
| B:e40 | 1.85 | TRACK_LOST | B | track_003 | radar |  |
| B:e41 | 1.90 | TRACK_LOST | B | track_005 | radar |  |
| B:e42 | 1.95 | TRACK_LOST | B | track_004 | radar |  |
| B:e43 | 2.15 | CLOSING_END | B | track_014 | radar |  |
| B:e44 | 2.50 | TURN_LEFT_END | B | - | ego |  |
| B:e45 | 2.55 | MOVING_END | B | - | ego |  |
| B:e46 | 2.55 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e01 --PRECEDES--> B:e07
    B:e01 --PRECEDES--> B:e08
    B:e01 --PRECEDES--> B:e09
    B:e01 --PRECEDES--> B:e10
    B:e01 --PRECEDES--> B:e11
    B:e01 --PRECEDES--> B:e12
    B:e01 --PRECEDES--> B:e13
    B:e01 --PRECEDES--> B:e14
    B:e01 --PRECEDES--> B:e15
    B:e01 --PRECEDES--> B:e16
    B:e02 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e07
    B:e02 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e09
    B:e02 --PRECEDES--> B:e10
    B:e02 --PRECEDES--> B:e11
    B:e02 --PRECEDES--> B:e12
    B:e02 --PRECEDES--> B:e13
    B:e02 --PRECEDES--> B:e14
    B:e02 --PRECEDES--> B:e15
    B:e02 --PRECEDES--> B:e16
    B:e03 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e10
    B:e03 --PRECEDES--> B:e11
    B:e03 --PRECEDES--> B:e12
    B:e03 --PRECEDES--> B:e13
    B:e03 --PRECEDES--> B:e14
    B:e03 --PRECEDES--> B:e15
    B:e03 --PRECEDES--> B:e16
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e10
    B:e04 --PRECEDES--> B:e11
    B:e04 --PRECEDES--> B:e12
    B:e04 --PRECEDES--> B:e13
    B:e04 --PRECEDES--> B:e14
    B:e04 --PRECEDES--> B:e15
    B:e04 --PRECEDES--> B:e16
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e09
    B:e05 --PRECEDES--> B:e10
    B:e05 --PRECEDES--> B:e11
    B:e05 --PRECEDES--> B:e12
    B:e05 --PRECEDES--> B:e13
    B:e05 --PRECEDES--> B:e14
    B:e05 --PRECEDES--> B:e15
    B:e05 --PRECEDES--> B:e16
    B:e06 --PRECEDES--> B:e17
    B:e06 --PRECEDES--> B:e18
    B:e06 --PRECEDES--> B:e19
    B:e06 --PRECEDES--> B:e20
    B:e06 --PRECEDES--> B:e21
    B:e06 --PRECEDES--> B:e22
    B:e06 --PRECEDES--> B:e23
    B:e07 --PRECEDES--> B:e17
    B:e07 --PRECEDES--> B:e18
    B:e07 --PRECEDES--> B:e19
    B:e07 --PRECEDES--> B:e20
    B:e07 --PRECEDES--> B:e21
    B:e07 --PRECEDES--> B:e22
    B:e07 --PRECEDES--> B:e23
    B:e08 --PRECEDES--> B:e17
    B:e08 --PRECEDES--> B:e18
    B:e08 --PRECEDES--> B:e19
    B:e08 --PRECEDES--> B:e20
    B:e08 --PRECEDES--> B:e21
    B:e08 --PRECEDES--> B:e22
    B:e08 --PRECEDES--> B:e23
    B:e09 --PRECEDES--> B:e17
    B:e09 --PRECEDES--> B:e18
    B:e09 --PRECEDES--> B:e19
    B:e09 --PRECEDES--> B:e20
    B:e09 --PRECEDES--> B:e21
    B:e09 --PRECEDES--> B:e22
    B:e09 --PRECEDES--> B:e23
    B:e10 --PRECEDES--> B:e17
    B:e10 --PRECEDES--> B:e18
    B:e10 --PRECEDES--> B:e19
    B:e10 --PRECEDES--> B:e20
    B:e10 --PRECEDES--> B:e21
    B:e10 --PRECEDES--> B:e22
    B:e10 --PRECEDES--> B:e23
    B:e11 --PRECEDES--> B:e17
    B:e11 --PRECEDES--> B:e18
    B:e11 --PRECEDES--> B:e19
    B:e11 --PRECEDES--> B:e20
    B:e11 --PRECEDES--> B:e21
    B:e11 --PRECEDES--> B:e22
    B:e11 --PRECEDES--> B:e23
    B:e12 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e12 --PRECEDES--> B:e19
    B:e12 --PRECEDES--> B:e20
    B:e12 --PRECEDES--> B:e21
    B:e12 --PRECEDES--> B:e22
    B:e12 --PRECEDES--> B:e23
    B:e13 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e20
    B:e13 --PRECEDES--> B:e21
    B:e13 --PRECEDES--> B:e22
    B:e13 --PRECEDES--> B:e23
    B:e14 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e20
    B:e14 --PRECEDES--> B:e21
    B:e14 --PRECEDES--> B:e22
    B:e14 --PRECEDES--> B:e23
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e19
    B:e15 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e22
    B:e15 --PRECEDES--> B:e23
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e23
    B:e17 --PRECEDES--> B:e24
    B:e17 --PRECEDES--> B:e25
    B:e18 --PRECEDES--> B:e24
    B:e18 --PRECEDES--> B:e25
    B:e19 --PRECEDES--> B:e24
    B:e19 --PRECEDES--> B:e25
    B:e20 --PRECEDES--> B:e24
    B:e20 --PRECEDES--> B:e25
    B:e21 --PRECEDES--> B:e24
    B:e21 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e36 --PRECEDES--> B:e37
    B:e37 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e37 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e41
    B:e39 --PRECEDES--> B:e41
    B:e40 --PRECEDES--> B:e41
    B:e41 --PRECEDES--> B:e42
    B:e42 --PRECEDES--> B:e43
    B:e43 --PRECEDES--> B:e44
    B:e44 --PRECEDES--> B:e45
    B:e44 --PRECEDES--> B:e46
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e05
    B:e09 --SAME_TRACK--> B:e13
    B:e10 --SAME_TRACK--> B:e14
    B:e11 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e17 --SAME_TRACK--> B:e22
    B:e03 --SAME_TRACK--> B:e23
    B:e24 --SAME_TRACK--> B:e25
    B:e06 --SAME_TRACK--> B:e26
    B:e07 --SAME_TRACK--> B:e27
    B:e08 --SAME_TRACK--> B:e28
    B:e19 --SAME_TRACK--> B:e29
    B:e20 --SAME_TRACK--> B:e30
    B:e21 --SAME_TRACK--> B:e31
    B:e18 --SAME_TRACK--> B:e32
    B:e17 --SAME_TRACK--> B:e33
    B:e17 --SAME_TRACK--> B:e34
    B:e12 --SAME_TRACK--> B:e36
    B:e09 --SAME_TRACK--> B:e40
    B:e11 --SAME_TRACK--> B:e41
    B:e10 --SAME_TRACK--> B:e42
    B:e24 --SAME_TRACK--> B:e43
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TURN_RIGHT_START<br>B:e03 TRACK_APPEARED_LEFT track_001<br>B:e04 CLOSING_START track_001<br>B:e05 CRITICAL_TTC_START track_001 | ego: not yet observed | - |
| 0.20 | B:e06 TRACK_APPEARED_LEFT track_002<br>B:e07 TRACK_APPEARED_LEFT track_007<br>B:e08 TRACK_APPEARED_LEFT track_008<br>B:e09 TRACK_APPEARED_RIGHT track_003<br>B:e10 TRACK_APPEARED_RIGHT track_004<br>B:e11 TRACK_APPEARED_RIGHT track_005<br>B:e12 TRACK_APPEARED_RIGHT track_006<br>B:e13 CLOSING_START track_003<br>B:e14 CLOSING_START track_004<br>B:e15 CLOSING_START track_005<br>B:e16 CLOSING_START track_006 | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.10 |
| 0.25 | B:e17 TRACK_APPEARED_LEFT track_009<br>B:e18 TRACK_APPEARED_LEFT track_010<br>B:e19 TRACK_APPEARED_LEFT track_011<br>B:e20 TRACK_APPEARED_LEFT track_012<br>B:e21 TRACK_APPEARED_LEFT track_013<br>B:e22 CLOSING_START track_009<br>B:e23 TRACK_LOST track_001 | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.20 |
| 0.30 | B:e24 TRACK_APPEARED_LEFT track_014<br>B:e25 CLOSING_START track_014 | ego: MOVING, TURN_RIGHT<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001 | 0.20 |
| 0.40 | B:e26 TRACK_LOST track_002<br>B:e27 TRACK_LOST track_007 | ego: MOVING, TURN_RIGHT<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001 | 0.30 |
| 0.45 | B:e28 TRACK_LOST track_008 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007 | 0.40 |
| 0.50 | B:e29 TRACK_LOST track_011 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008 | 0.40 |
| 0.55 | B:e30 TRACK_LOST track_012 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011 | 0.50 |
| 0.60 | B:e31 TRACK_LOST track_013 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011, track_012 | 0.50 |
| 0.65 | B:e32 TRACK_LOST track_010 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011, track_012, track_013 | 0.60 |
| 0.80 | B:e33 CLOSING_END track_009 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_010, track_011, track_012, track_013 | 0.70 |
| 0.90 | B:e34 TRACK_LOST track_009 | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: no active state<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_010, track_011, track_012, track_013 | 0.80 |
| 1.20 | B:e35 TURN_RIGHT_END | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.10 |
| 1.50 | B:e36 TRACK_LOST track_006 | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.40 |
| 1.80 | B:e37 COLLISION | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.70 |
| 1.85 | B:e38 BRAKE_START<br>B:e39 TURN_LEFT_START<br>B:e40 TRACK_LOST track_003 | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.80 |
| 1.90 | B:e41 TRACK_LOST track_005 | ego: MOVING, BRAKE, TURN_LEFT<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.80 |
| 1.95 | B:e42 TRACK_LOST track_004 | ego: MOVING, BRAKE, TURN_LEFT<br>track_004: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 1.90 |
| 2.15 | B:e43 CLOSING_END track_014 | ego: MOVING, BRAKE, TURN_LEFT<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 2.10 |
| 2.50 | B:e44 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_014: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 2.40 |
| 2.55 | B:e45 MOVING_END<br>B:e46 STOP_START | ego: MOVING, BRAKE<br>track_014: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 2.50 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 0.00 s); the track was lost at 0.25 s
- CRITICAL_TTC of track_001, since B:e05 (t = 0.00 s); the track was lost at 0.25 s
- CLOSING of track_003, since B:e13 (t = 0.20 s); the track was lost at 1.85 s
- CLOSING of track_004, since B:e14 (t = 0.20 s); the track was lost at 1.95 s
- CLOSING of track_005, since B:e15 (t = 0.20 s); the track was lost at 1.90 s
- CLOSING of track_006, since B:e16 (t = 0.20 s); the track was lost at 1.50 s
- BRAKE, since B:e38 (t = 1.85 s)
- STOP, since B:e46 (t = 2.55 s)

## Tracks lost

- track_001 at 0.25 s (B:e23): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 1.50 s (B:e36): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 1.85 s (B:e40): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 1.90 s (B:e41): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 1.95 s (B:e42): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_002, track_007, track_008, track_011, track_012, track_013, track_010, track_009

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.00, COLLISION 1.80 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 0.25 | 6 | 8.8 m / -74 deg | 7.12 m (0.25) | 7.1 m / -78 deg | 11.7 m/s |
| track_002 | 0.20 | 0.40 | 5 | 43.7 m / -66 deg | 43.66 m (0.20) | 44.0 m / -78 deg | 1.4 m/s |
| track_003 | 0.20 | 1.85 | 33 | 27.6 m / +77 deg | 22.40 m (1.85) | 22.4 m / +83 deg | 5.5 m/s |
| track_004 | 0.20 | 1.95 | 33 | 19.4 m / +61 deg | 11.12 m (1.95) | 11.1 m / +80 deg | 1.2 m/s |
| track_005 | 0.20 | 1.90 | 34 | 29.7 m / +67 deg | 23.15 m (1.90) | 23.1 m / +83 deg | 5.1 m/s |
| track_006 | 0.20 | 1.50 | 27 | 14.2 m / +71 deg | 9.27 m (1.50) | 9.3 m / +81 deg | 1.3 m/s |
| track_007 | 0.20 | 0.40 | 5 | 68.5 m / -68 deg | 68.53 m (0.20) | 68.9 m / -78 deg | 1.4 m/s |
| track_008 | 0.20 | 0.45 | 6 | 64.5 m / -65 deg | 64.47 m (0.20) | 64.8 m / -79 deg | 1.5 m/s |
| track_009 | 0.25 | 0.90 | 14 | 21.2 m / -52 deg | 21.06 m (0.90) | 21.1 m / -81 deg | 2.8 m/s |
| track_010 | 0.25 | 0.65 | 9 | 55.8 m / -61 deg | 55.84 m (0.25) | 56.1 m / -81 deg | 3.3 m/s |
| track_011 | 0.25 | 0.50 | 6 | 17.7 m / -58 deg | 17.70 m (0.25) | 17.8 m / -74 deg | 1.7 m/s |
| track_012 | 0.25 | 0.55 | 7 | 59.4 m / -65 deg | 59.39 m (0.25) | 59.7 m / -79 deg | 1.7 m/s |
| track_013 | 0.25 | 0.60 | 8 | 28.9 m / -60 deg | 28.93 m (0.25) | 29.1 m / -78 deg | 2.3 m/s |
| track_014 | 0.30 | 14.95 | 294 | 14.7 m / -56 deg | 11.99 m (2.50) | 12.6 m / -78 deg | 9.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B started turning right (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.20 s: B's radar started tracking track_002, which appeared on its left.
- t = 0.20 s: B's radar started tracking track_007, which appeared on its left.
- t = 0.20 s: B's radar started tracking track_008, which appeared on its left.
- t = 0.20 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.20 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.20 s: B's radar started tracking track_005, which appeared on its right.
- t = 0.20 s: B's radar started tracking track_006, which appeared on its right.
- t = 0.20 s: B observed track_003 start closing in (already the case when first observed).
- t = 0.20 s: B observed track_004 start closing in (already the case when first observed).
- t = 0.20 s: B observed track_005 start closing in (already the case when first observed).
- t = 0.20 s: B observed track_006 start closing in (already the case when first observed).
- t = 0.25 s: B's radar started tracking track_009, which appeared on its left.
- t = 0.25 s: B's radar started tracking track_010, which appeared on its left.
- t = 0.25 s: B's radar started tracking track_011, which appeared on its left.
- t = 0.25 s: B's radar started tracking track_012, which appeared on its left.
- t = 0.25 s: B's radar started tracking track_013, which appeared on its left.
- t = 0.25 s: B observed track_009 start closing in (already the case when first observed).
- t = 0.25 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 0.30 s: B's radar started tracking track_014, which appeared on its left.
- t = 0.30 s: B observed track_014 start closing in (already the case when first observed).
- t = 0.40 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 0.40 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 0.45 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 0.50 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 0.55 s: B's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 0.60 s: B's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 0.65 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 0.80 s: B observed track_009 stop closing in.
- t = 0.90 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 1.20 s: B stopped turning right.
- t = 1.50 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 1.80 s: B's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.85 s: B started braking.
- t = 1.85 s: B started turning left.
- t = 1.85 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 1.90 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 1.95 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 2.15 s: B observed track_014 stop closing in.
- t = 2.50 s: B stopped turning left.
- t = 2.55 s: B stopped moving.
- t = 2.55 s: B came to a stop.
