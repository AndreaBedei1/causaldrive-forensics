# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 234.8135948292911 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 18 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 66; edges: 171 (PRECEDES 134, SAME_TRACK 37)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.95 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e06 | 2.95 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e07 | 3.40 | MOVING_END | A | - | ego |  |
| A:e08 | 3.40 | STOP_START | A | - | ego |  |
| A:e09 | 4.70 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 6.45 | BRAKE_END | A | - | controls |  |
| A:e11 | 6.80 | STOP_END | A | - | ego |  |
| A:e12 | 6.80 | MOVING_START | A | - | ego |  |
| A:e13 | 7.15 | CLOSING_START | A | track_001 | radar |  |
| A:e14 | 7.80 | TURN_LEFT_START | A | - | ego |  |
| A:e15 | 8.25 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e16 | 8.25 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e17 | 8.25 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e18 | 8.25 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e19 | 8.25 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e20 | 8.25 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e21 | 8.25 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e22 | 8.25 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e23 | 8.30 | TRACK_APPEARED_LEFT | A | track_004 | radar |  |
| A:e24 | 8.30 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e25 | 8.80 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e26 | 8.80 | TRACK_APPEARED_RIGHT | A | track_007 | radar |  |
| A:e27 | 8.80 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e28 | 8.85 | TRACK_APPEARED_LEFT | A | track_010 | radar |  |
| A:e29 | 8.85 | TRACK_APPEARED_LEFT | A | track_011 | radar |  |
| A:e30 | 8.85 | TRACK_APPEARED_RIGHT | A | track_009 | radar |  |
| A:e31 | 8.85 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e32 | 8.85 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e33 | 8.90 | TRACK_APPEARED_LEFT | A | track_012 | radar |  |
| A:e34 | 8.90 | TRACK_APPEARED_LEFT | A | track_017 | radar |  |
| A:e35 | 8.90 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e36 | 8.90 | CLOSING_START | A | track_017 | radar | active_at_first_observation=True |
| A:e37 | 9.00 | TRACK_APPEARED_LEFT | A | track_014 | radar |  |
| A:e38 | 9.00 | TRACK_APPEARED_RIGHT | A | track_013 | radar |  |
| A:e39 | 9.00 | CLOSING_START | A | track_014 | radar | active_at_first_observation=True |
| A:e40 | 9.00 | TRACK_LOST | A | track_007 | radar |  |
| A:e41 | 9.05 | TRACK_APPEARED_LEFT | A | track_015 | radar |  |
| A:e42 | 9.05 | CLOSING_START | A | track_015 | radar | active_at_first_observation=True |
| A:e43 | 9.10 | TRACK_APPEARED_RIGHT | A | track_016 | radar |  |
| A:e44 | 9.10 | CLOSING_START | A | track_016 | radar | active_at_first_observation=True |
| A:e45 | 9.20 | TRACK_LOST | A | track_009 | radar |  |
| A:e46 | 9.25 | TRACK_APPEARED_RIGHT | A | track_018 | radar |  |
| A:e47 | 9.25 | CLOSING_START | A | track_018 | radar | active_at_first_observation=True |
| A:e48 | 9.40 | CLOSING_END | A | track_016 | radar |  |
| A:e49 | 9.60 | CLOSING_START | A | track_016 | radar |  |
| A:e50 | 9.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e51 | 9.80 | CLOSING_START | A | track_013 | radar |  |
| A:e52 | 10.10 | TRACK_LOST | A | track_018 | radar |  |
| A:e53 | 10.40 | TRACK_LOST | A | track_016 | radar |  |
| A:e54 | 10.45 | TRACK_LOST | A | track_015 | radar |  |
| A:e55 | 10.60 | EGO_PATH_ENTRY | A | track_014 | radar |  |
| A:e56 | 10.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e57 | 10.70 | TRACK_LOST | A | track_010 | radar |  |
| A:e58 | 11.00 | TRACK_LOST | A | track_001 | radar |  |
| A:e59 | 11.05 | TURN_LEFT_END | A | - | ego |  |
| A:e60 | 11.20 | EGO_PATH_EXIT | A | track_014 | radar |  |
| A:e61 | 11.90 | EGO_PATH_ENTRY | A | track_008 | radar |  |
| A:e62 | 12.30 | TRACK_LOST | A | track_006 | radar |  |
| A:e63 | 13.50 | TRACK_LOST | A | track_013 | radar |  |
| A:e64 | 14.30 | TRACK_LOST | A | track_017 | radar |  |
| A:e65 | 14.35 | TRACK_LOST | A | track_012 | radar |  |
| A:e66 | 14.50 | TRACK_LOST | A | track_004 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e19
    A:e14 --PRECEDES--> A:e20
    A:e14 --PRECEDES--> A:e21
    A:e14 --PRECEDES--> A:e22
    A:e15 --PRECEDES--> A:e23
    A:e15 --PRECEDES--> A:e24
    A:e16 --PRECEDES--> A:e23
    A:e16 --PRECEDES--> A:e24
    A:e17 --PRECEDES--> A:e23
    A:e17 --PRECEDES--> A:e24
    A:e18 --PRECEDES--> A:e23
    A:e18 --PRECEDES--> A:e24
    A:e19 --PRECEDES--> A:e23
    A:e19 --PRECEDES--> A:e24
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e30
    A:e25 --PRECEDES--> A:e31
    A:e25 --PRECEDES--> A:e32
    A:e26 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e31
    A:e26 --PRECEDES--> A:e32
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e27 --PRECEDES--> A:e31
    A:e27 --PRECEDES--> A:e32
    A:e28 --PRECEDES--> A:e33
    A:e28 --PRECEDES--> A:e34
    A:e28 --PRECEDES--> A:e35
    A:e28 --PRECEDES--> A:e36
    A:e29 --PRECEDES--> A:e33
    A:e29 --PRECEDES--> A:e34
    A:e29 --PRECEDES--> A:e35
    A:e29 --PRECEDES--> A:e36
    A:e30 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e30 --PRECEDES--> A:e36
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e37
    A:e33 --PRECEDES--> A:e38
    A:e33 --PRECEDES--> A:e39
    A:e33 --PRECEDES--> A:e40
    A:e34 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e38
    A:e34 --PRECEDES--> A:e39
    A:e34 --PRECEDES--> A:e40
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e35 --PRECEDES--> A:e39
    A:e35 --PRECEDES--> A:e40
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e39
    A:e36 --PRECEDES--> A:e40
    A:e37 --PRECEDES--> A:e41
    A:e37 --PRECEDES--> A:e42
    A:e38 --PRECEDES--> A:e41
    A:e38 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e43
    A:e42 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e45
    A:e45 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e49 --PRECEDES--> A:e50
    A:e50 --PRECEDES--> A:e51
    A:e51 --PRECEDES--> A:e52
    A:e52 --PRECEDES--> A:e53
    A:e53 --PRECEDES--> A:e54
    A:e54 --PRECEDES--> A:e55
    A:e55 --PRECEDES--> A:e56
    A:e56 --PRECEDES--> A:e57
    A:e57 --PRECEDES--> A:e58
    A:e58 --PRECEDES--> A:e59
    A:e59 --PRECEDES--> A:e60
    A:e60 --PRECEDES--> A:e61
    A:e61 --PRECEDES--> A:e62
    A:e62 --PRECEDES--> A:e63
    A:e63 --PRECEDES--> A:e64
    A:e64 --PRECEDES--> A:e65
    A:e65 --PRECEDES--> A:e66
    A:e05 --SAME_TRACK--> A:e06
    A:e05 --SAME_TRACK--> A:e09
    A:e05 --SAME_TRACK--> A:e13
    A:e15 --SAME_TRACK--> A:e19
    A:e16 --SAME_TRACK--> A:e20
    A:e17 --SAME_TRACK--> A:e21
    A:e18 --SAME_TRACK--> A:e22
    A:e23 --SAME_TRACK--> A:e24
    A:e25 --SAME_TRACK--> A:e27
    A:e28 --SAME_TRACK--> A:e31
    A:e29 --SAME_TRACK--> A:e32
    A:e33 --SAME_TRACK--> A:e35
    A:e34 --SAME_TRACK--> A:e36
    A:e37 --SAME_TRACK--> A:e39
    A:e26 --SAME_TRACK--> A:e40
    A:e41 --SAME_TRACK--> A:e42
    A:e43 --SAME_TRACK--> A:e44
    A:e30 --SAME_TRACK--> A:e45
    A:e46 --SAME_TRACK--> A:e47
    A:e43 --SAME_TRACK--> A:e48
    A:e43 --SAME_TRACK--> A:e49
    A:e05 --SAME_TRACK--> A:e50
    A:e38 --SAME_TRACK--> A:e51
    A:e46 --SAME_TRACK--> A:e52
    A:e43 --SAME_TRACK--> A:e53
    A:e41 --SAME_TRACK--> A:e54
    A:e37 --SAME_TRACK--> A:e55
    A:e05 --SAME_TRACK--> A:e56
    A:e28 --SAME_TRACK--> A:e57
    A:e05 --SAME_TRACK--> A:e58
    A:e37 --SAME_TRACK--> A:e60
    A:e18 --SAME_TRACK--> A:e61
    A:e25 --SAME_TRACK--> A:e62
    A:e38 --SAME_TRACK--> A:e63
    A:e34 --SAME_TRACK--> A:e64
    A:e33 --SAME_TRACK--> A:e65
    A:e23 --SAME_TRACK--> A:e66
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.65 | A:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 2.95 | A:e05 TRACK_APPEARED_LEFT track_001<br>A:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 2.90 |
| 3.40 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 4.70 | A:e09 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.60 |
| 6.45 | A:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.40 |
| 6.80 | A:e11 STOP_END<br>A:e12 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.70 |
| 7.15 | A:e13 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 7.10 |
| 7.80 | A:e14 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 7.70 |
| 8.25 | A:e15 TRACK_APPEARED_LEFT track_002<br>A:e16 TRACK_APPEARED_LEFT track_003<br>A:e17 TRACK_APPEARED_LEFT track_005<br>A:e18 TRACK_APPEARED_LEFT track_008<br>A:e19 CLOSING_START track_002<br>A:e20 CLOSING_START track_003<br>A:e21 CLOSING_START track_005<br>A:e22 CLOSING_START track_008 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 8.30 | A:e23 TRACK_APPEARED_LEFT track_004<br>A:e24 CLOSING_START track_004 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 8.80 | A:e25 TRACK_APPEARED_LEFT track_006<br>A:e26 TRACK_APPEARED_RIGHT track_007<br>A:e27 CLOSING_START track_006 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.70 |
| 8.85 | A:e28 TRACK_APPEARED_LEFT track_010<br>A:e29 TRACK_APPEARED_LEFT track_011<br>A:e30 TRACK_APPEARED_RIGHT track_009<br>A:e31 CLOSING_START track_010<br>A:e32 CLOSING_START track_011 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.80 |
| 8.90 | A:e33 TRACK_APPEARED_LEFT track_012<br>A:e34 TRACK_APPEARED_LEFT track_017<br>A:e35 CLOSING_START track_012<br>A:e36 CLOSING_START track_017 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.80 |
| 9.00 | A:e37 TRACK_APPEARED_LEFT track_014<br>A:e38 TRACK_APPEARED_RIGHT track_013<br>A:e39 CLOSING_START track_014<br>A:e40 TRACK_LOST track_007 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_017: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.90 |
| 9.05 | A:e41 TRACK_APPEARED_LEFT track_015<br>A:e42 CLOSING_START track_015 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path | 9.00 |
| 9.10 | A:e43 TRACK_APPEARED_RIGHT track_016<br>A:e44 CLOSING_START track_016 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path | 9.00 |
| 9.20 | A:e45 TRACK_LOST track_009 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path | 9.10 |
| 9.25 | A:e46 TRACK_APPEARED_RIGHT track_018<br>A:e47 CLOSING_START track_018 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 9.20 |
| 9.40 | A:e48 CLOSING_END track_016 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 9.30 |
| 9.60 | A:e49 CLOSING_START track_016 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 9.75 | A:e50 CRITICAL_TTC_START track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 9.80 | A:e51 CLOSING_START track_013 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 10.10 | A:e52 TRACK_LOST track_018 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path | 10.00 |
| 10.40 | A:e53 TRACK_LOST track_016 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_018<br>sign-0: STOP sign known, relevant to the path | 10.30 |
| 10.45 | A:e54 TRACK_LOST track_015 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 10.40 |
| 10.60 | A:e55 EGO_PATH_ENTRY track_014 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 10.50 |
| 10.65 | A:e56 CRITICAL_TTC_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 10.60 |
| 10.70 | A:e57 TRACK_LOST track_010 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 10.60 |
| 11.00 | A:e58 TRACK_LOST track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 10.90 |
| 11.05 | A:e59 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 11.00 |
| 11.20 | A:e60 EGO_PATH_EXIT track_014 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 11.10 |
| 11.90 | A:e61 EGO_PATH_ENTRY track_008 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 11.80 |
| 12.30 | A:e62 TRACK_LOST track_006 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 12.20 |
| 13.50 | A:e63 TRACK_LOST track_013 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 13.40 |
| 14.30 | A:e64 TRACK_LOST track_017 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_013, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path | 14.20 |
| 14.35 | A:e65 TRACK_LOST track_012 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_013, track_015, track_016, track_017, track_018<br>sign-0: STOP sign known, relevant to the path | 14.30 |
| 14.50 | A:e66 TRACK_LOST track_004 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_012, track_013, track_015, track_016, track_017, track_018<br>sign-0: STOP sign known, relevant to the path | 14.40 |

## States still active when observation ended

- MOVING, since A:e12 (t = 6.80 s)
- CLOSING of track_001, since A:e13 (t = 7.15 s); the track was lost at 11.00 s
- CLOSING of track_002, since A:e19 (t = 8.25 s)
- CLOSING of track_003, since A:e20 (t = 8.25 s)
- CLOSING of track_005, since A:e21 (t = 8.25 s)
- CLOSING of track_008, since A:e22 (t = 8.25 s)
- CLOSING of track_004, since A:e24 (t = 8.30 s); the track was lost at 14.50 s
- CLOSING of track_006, since A:e27 (t = 8.80 s); the track was lost at 12.30 s
- CLOSING of track_010, since A:e31 (t = 8.85 s); the track was lost at 10.70 s
- CLOSING of track_011, since A:e32 (t = 8.85 s)
- CLOSING of track_012, since A:e35 (t = 8.90 s); the track was lost at 14.35 s
- CLOSING of track_017, since A:e36 (t = 8.90 s); the track was lost at 14.30 s
- CLOSING of track_014, since A:e39 (t = 9.00 s)
- CLOSING of track_015, since A:e42 (t = 9.05 s); the track was lost at 10.45 s
- CLOSING of track_018, since A:e47 (t = 9.25 s); the track was lost at 10.10 s
- CLOSING of track_016, since A:e49 (t = 9.60 s); the track was lost at 10.40 s
- CLOSING of track_013, since A:e51 (t = 9.80 s); the track was lost at 13.50 s
- EGO_PATH of track_008, since A:e61 (t = 11.90 s)

## Tracks lost

- track_018 at 10.10 s (A:e52): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_016 at 10.40 s (A:e53): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_015 at 10.45 s (A:e54): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 10.70 s (A:e57): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 11.00 s (A:e58): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 12.30 s (A:e62): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 13.50 s (A:e63): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_017 at 14.30 s (A:e64): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 14.35 s (A:e65): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 14.50 s (A:e66): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_007, track_009

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 9.75
- track_008: EGO_PATH_ENTRY 11.90, no critical TTC
- track_014: EGO_PATH_ENTRY 10.60, no critical TTC

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.95 | 11.00 | 162 | 31.6 m / -69 deg | 5.03 m (11.00) | 5.0 m / -84 deg | 5.5 m/s |
| track_002 | 8.25 | 16.45 | 144 | 96.5 m / -77 deg | 33.79 m (16.45) | 33.8 m / -21 deg | 3.6 m/s |
| track_003 | 8.25 | 16.45 | 144 | 56.6 m / -79 deg | 10.08 m (16.45) | 10.1 m / -75 deg | 8.1 m/s |
| track_004 | 8.30 | 14.50 | 108 | 38.6 m / -80 deg | 9.95 m (14.50) | 9.9 m / -78 deg | 8.1 m/s |
| track_005 | 8.25 | 16.45 | 130 | 64.6 m / -79 deg | 10.83 m (16.45) | 10.8 m / -68 deg | 6.2 m/s |
| track_006 | 8.80 | 12.30 | 70 | 28.8 m / -77 deg | 11.02 m (12.30) | 11.0 m / -78 deg | 6.7 m/s |
| track_007 | 8.80 | 9.00 | 5 | 15.9 m / +78 deg | 15.93 m (8.80) | 16.2 m / +81 deg | 15.7 m/s |
| track_008 | 8.25 | 16.45 | 140 | 89.5 m / -70 deg | 24.58 m (16.45) | 24.6 m / -0 deg | 2.7 m/s |
| track_009 | 8.85 | 9.20 | 8 | 12.5 m / +67 deg | 12.53 m (8.90) | 13.2 m / +82 deg | 10.7 m/s |
| track_010 | 8.85 | 10.70 | 38 | 23.4 m / -79 deg | 12.68 m (10.70) | 12.7 m / -81 deg | 3.2 m/s |
| track_011 | 8.85 | 16.45 | 145 | 90.0 m / -61 deg | 29.01 m (16.45) | 29.0 m / -11 deg | 1.7 m/s |
| track_012 | 8.90 | 14.35 | 103 | 41.3 m / -70 deg | 10.06 m (14.35) | 10.1 m / -71 deg | 6.7 m/s |
| track_013 | 9.00 | 13.50 | 91 | 9.8 m / +62 deg | 6.00 m (13.50) | 6.0 m / +79 deg | 14.7 m/s |
| track_014 | 9.00 | 16.45 | 144 | 78.0 m / -47 deg | 18.12 m (16.45) | 18.1 m / +17 deg | 2.2 m/s |
| track_015 | 9.05 | 10.45 | 29 | 17.9 m / -80 deg | 11.27 m (10.45) | 11.3 m / -81 deg | 3.2 m/s |
| track_016 | 9.10 | 10.40 | 27 | 10.1 m / +50 deg | 7.78 m (10.40) | 7.8 m / +46 deg | 14.1 m/s |
| track_017 | 8.90 | 14.30 | 99 | 46.3 m / -68 deg | 11.20 m (14.30) | 11.2 m / -69 deg | 3.9 m/s |
| track_018 | 9.25 | 10.10 | 18 | 10.9 m / +43 deg | 8.33 m (10.10) | 8.3 m / +46 deg | 12.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: A started braking.
- t = 2.95 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.95 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 4.70 s: A observed track_001 stop closing in.
- t = 6.45 s: A released the brake.
- t = 6.80 s: A left its stop.
- t = 6.80 s: A started moving.
- t = 7.15 s: A observed track_001 start closing in.
- t = 7.80 s: A started turning left.
- t = 8.25 s: A's radar started tracking track_002, which appeared on its left.
- t = 8.25 s: A's radar started tracking track_003, which appeared on its left.
- t = 8.25 s: A's radar started tracking track_005, which appeared on its left.
- t = 8.25 s: A's radar started tracking track_008, which appeared on its left.
- t = 8.25 s: A observed track_002 start closing in (already the case when first observed).
- t = 8.25 s: A observed track_003 start closing in (already the case when first observed).
- t = 8.25 s: A observed track_005 start closing in (already the case when first observed).
- t = 8.25 s: A observed track_008 start closing in (already the case when first observed).
- t = 8.30 s: A's radar started tracking track_004, which appeared on its left.
- t = 8.30 s: A observed track_004 start closing in (already the case when first observed).
- t = 8.80 s: A's radar started tracking track_006, which appeared on its left.
- t = 8.80 s: A's radar started tracking track_007, which appeared on its right.
- t = 8.80 s: A observed track_006 start closing in (already the case when first observed).
- t = 8.85 s: A's radar started tracking track_010, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_011, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_009, which appeared on its right.
- t = 8.85 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_011 start closing in (already the case when first observed).
- t = 8.90 s: A's radar started tracking track_012, which appeared on its left.
- t = 8.90 s: A's radar started tracking track_017, which appeared on its left.
- t = 8.90 s: A observed track_012 start closing in (already the case when first observed).
- t = 8.90 s: A observed track_017 start closing in (already the case when first observed).
- t = 9.00 s: A's radar started tracking track_014, which appeared on its left.
- t = 9.00 s: A's radar started tracking track_013, which appeared on its right.
- t = 9.00 s: A observed track_014 start closing in (already the case when first observed).
- t = 9.00 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 9.05 s: A's radar started tracking track_015, which appeared on its left.
- t = 9.05 s: A observed track_015 start closing in (already the case when first observed).
- t = 9.10 s: A's radar started tracking track_016, which appeared on its right.
- t = 9.10 s: A observed track_016 start closing in (already the case when first observed).
- t = 9.20 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 9.25 s: A's radar started tracking track_018, which appeared on its right.
- t = 9.25 s: A observed track_018 start closing in (already the case when first observed).
- t = 9.40 s: A observed track_016 stop closing in.
- t = 9.60 s: A observed track_016 start closing in.
- t = 9.75 s: A's time-to-contact with track_001 became critical.
- t = 9.80 s: A observed track_013 start closing in.
- t = 10.10 s: A's radar lost track_018 (its states are UNKNOWN from then on, not ended).
- t = 10.40 s: A's radar lost track_016 (its states are UNKNOWN from then on, not ended).
- t = 10.45 s: A's radar lost track_015 (its states are UNKNOWN from then on, not ended).
- t = 10.60 s: A observed track_014 enter its forward path corridor.
- t = 10.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 10.70 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 11.00 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 11.05 s: A stopped turning left.
- t = 11.20 s: A observed track_014 leave its forward path corridor.
- t = 11.90 s: A observed track_008 enter its forward path corridor.
- t = 12.30 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 13.50 s: A's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 14.30 s: A's radar lost track_017 (its states are UNKNOWN from then on, not ended).
- t = 14.35 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 14.50 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
