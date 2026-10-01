# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 14.042597696185112 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 19 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 65; edges: 178 (PRECEDES 143, SAME_TRACK 35)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.95 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 3.10 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e04 | 3.10 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 3.60 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e06 | 4.35 | BRAKE_START | A | - | controls |  |
| A:e07 | 4.70 | CLOSING_END | A | track_001 | radar |  |
| A:e08 | 4.75 | MOVING_END | A | - | ego |  |
| A:e09 | 4.75 | STOP_START | A | - | ego |  |
| A:e10 | 6.95 | CLOSING_START | A | track_001 | radar |  |
| A:e11 | 9.75 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 9.90 | CLOSING_END | A | track_001 | radar |  |
| A:e13 | 10.20 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e14 | 10.45 | BRAKE_END | A | - | controls |  |
| A:e15 | 10.80 | STOP_END | A | - | ego |  |
| A:e16 | 10.80 | MOVING_START | A | - | ego |  |
| A:e17 | 12.10 | TURN_LEFT_START | A | - | ego |  |
| A:e18 | 12.10 | TRACK_LOST | A | track_001 | radar |  |
| A:e19 | 12.55 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e20 | 12.55 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e21 | 12.55 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e22 | 12.55 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e23 | 12.60 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e24 | 12.60 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e25 | 12.60 | TRACK_APPEARED_LEFT | A | track_004 | radar |  |
| A:e26 | 12.60 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e27 | 12.60 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e28 | 12.60 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e29 | 12.65 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e30 | 12.65 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e31 | 13.05 | TRACK_APPEARED_LEFT | A | track_009 | radar |  |
| A:e32 | 13.05 | TRACK_APPEARED_LEFT | A | track_013 | radar |  |
| A:e33 | 13.05 | TRACK_APPEARED_RIGHT | A | track_008 | radar |  |
| A:e34 | 13.05 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e35 | 13.05 | CLOSING_START | A | track_013 | radar | active_at_first_observation=True |
| A:e36 | 13.10 | TRACK_APPEARED_LEFT | A | track_011 | radar |  |
| A:e37 | 13.10 | TRACK_APPEARED_LEFT | A | track_015 | radar |  |
| A:e38 | 13.10 | TRACK_APPEARED_RIGHT | A | track_010 | radar |  |
| A:e39 | 13.10 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e40 | 13.10 | CLOSING_START | A | track_015 | radar | active_at_first_observation=True |
| A:e41 | 13.15 | TRACK_APPEARED_LEFT | A | track_012 | radar |  |
| A:e42 | 13.15 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e43 | 13.20 | TRACK_APPEARED_LEFT | A | track_014 | radar |  |
| A:e44 | 13.20 | CLOSING_START | A | track_014 | radar | active_at_first_observation=True |
| A:e45 | 13.25 | TRACK_APPEARED_LEFT | A | track_017 | radar |  |
| A:e46 | 13.25 | TRACK_APPEARED_RIGHT | A | track_016 | radar |  |
| A:e47 | 13.25 | CLOSING_START | A | track_017 | radar | active_at_first_observation=True |
| A:e48 | 13.30 | TRACK_LOST | A | track_008 | radar |  |
| A:e49 | 13.35 | TRACK_APPEARED_RIGHT | A | track_018 | radar |  |
| A:e50 | 13.35 | CLOSING_START | A | track_018 | radar | active_at_first_observation=True |
| A:e51 | 13.40 | TRACK_APPEARED_LEFT | A | track_019 | radar |  |
| A:e52 | 13.40 | CLOSING_START | A | track_019 | radar | active_at_first_observation=True |
| A:e53 | 13.50 | TRACK_LOST | A | track_010 | radar |  |
| A:e54 | 14.00 | CLOSING_START | A | track_016 | radar |  |
| A:e55 | 14.45 | TRACK_LOST | A | track_019 | radar |  |
| A:e56 | 14.60 | TRACK_LOST | A | track_018 | radar |  |
| A:e57 | 14.90 | EGO_PATH_ENTRY | A | track_017 | radar |  |
| A:e58 | 15.15 | TRACK_LOST | A | track_014 | radar |  |
| A:e59 | 15.30 | TURN_LEFT_END | A | - | ego |  |
| A:e60 | 15.35 | EGO_PATH_ENTRY | A | track_006 | radar |  |
| A:e61 | 15.55 | EGO_PATH_EXIT | A | track_017 | radar |  |
| A:e62 | 15.90 | CUT_IN_FROM_RIGHT_START | A | track_016 | radar |  |
| A:e63 | 16.05 | TRACK_LOST | A | track_012 | radar |  |
| A:e64 | 16.35 | TRACK_LOST | A | track_009 | radar |  |
| A:e65 | 16.40 | TRACK_LOST | A | track_004 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e21
    A:e17 --PRECEDES--> A:e22
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e22
    A:e19 --PRECEDES--> A:e23
    A:e19 --PRECEDES--> A:e24
    A:e19 --PRECEDES--> A:e25
    A:e19 --PRECEDES--> A:e26
    A:e19 --PRECEDES--> A:e27
    A:e19 --PRECEDES--> A:e28
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e20 --PRECEDES--> A:e25
    A:e20 --PRECEDES--> A:e26
    A:e20 --PRECEDES--> A:e27
    A:e20 --PRECEDES--> A:e28
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e26
    A:e21 --PRECEDES--> A:e27
    A:e21 --PRECEDES--> A:e28
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e22 --PRECEDES--> A:e27
    A:e22 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e29
    A:e23 --PRECEDES--> A:e30
    A:e24 --PRECEDES--> A:e29
    A:e24 --PRECEDES--> A:e30
    A:e25 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e30
    A:e27 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e32
    A:e29 --PRECEDES--> A:e33
    A:e29 --PRECEDES--> A:e34
    A:e29 --PRECEDES--> A:e35
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e36
    A:e31 --PRECEDES--> A:e37
    A:e31 --PRECEDES--> A:e38
    A:e31 --PRECEDES--> A:e39
    A:e31 --PRECEDES--> A:e40
    A:e32 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e37
    A:e32 --PRECEDES--> A:e38
    A:e32 --PRECEDES--> A:e39
    A:e32 --PRECEDES--> A:e40
    A:e33 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e37
    A:e33 --PRECEDES--> A:e38
    A:e33 --PRECEDES--> A:e39
    A:e33 --PRECEDES--> A:e40
    A:e34 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e38
    A:e34 --PRECEDES--> A:e39
    A:e34 --PRECEDES--> A:e40
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e35 --PRECEDES--> A:e39
    A:e35 --PRECEDES--> A:e40
    A:e36 --PRECEDES--> A:e41
    A:e36 --PRECEDES--> A:e42
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
    A:e43 --PRECEDES--> A:e46
    A:e43 --PRECEDES--> A:e47
    A:e44 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e44 --PRECEDES--> A:e47
    A:e45 --PRECEDES--> A:e48
    A:e46 --PRECEDES--> A:e48
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e48 --PRECEDES--> A:e50
    A:e49 --PRECEDES--> A:e51
    A:e49 --PRECEDES--> A:e52
    A:e50 --PRECEDES--> A:e51
    A:e50 --PRECEDES--> A:e52
    A:e51 --PRECEDES--> A:e53
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
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e18
    A:e19 --SAME_TRACK--> A:e21
    A:e20 --SAME_TRACK--> A:e22
    A:e23 --SAME_TRACK--> A:e26
    A:e24 --SAME_TRACK--> A:e27
    A:e25 --SAME_TRACK--> A:e28
    A:e29 --SAME_TRACK--> A:e30
    A:e31 --SAME_TRACK--> A:e34
    A:e32 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e39
    A:e37 --SAME_TRACK--> A:e40
    A:e41 --SAME_TRACK--> A:e42
    A:e43 --SAME_TRACK--> A:e44
    A:e45 --SAME_TRACK--> A:e47
    A:e33 --SAME_TRACK--> A:e48
    A:e49 --SAME_TRACK--> A:e50
    A:e51 --SAME_TRACK--> A:e52
    A:e38 --SAME_TRACK--> A:e53
    A:e46 --SAME_TRACK--> A:e54
    A:e51 --SAME_TRACK--> A:e55
    A:e49 --SAME_TRACK--> A:e56
    A:e45 --SAME_TRACK--> A:e57
    A:e43 --SAME_TRACK--> A:e58
    A:e19 --SAME_TRACK--> A:e60
    A:e45 --SAME_TRACK--> A:e61
    A:e46 --SAME_TRACK--> A:e62
    A:e41 --SAME_TRACK--> A:e63
    A:e31 --SAME_TRACK--> A:e64
    A:e25 --SAME_TRACK--> A:e65
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.95 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.90 |
| 3.10 | A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 3.00 |
| 3.60 | A:e05 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.50 |
| 4.35 | A:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.30 |
| 4.70 | A:e07 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.60 |
| 4.75 | A:e08 MOVING_END<br>A:e09 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 4.70 |
| 6.95 | A:e10 CLOSING_START track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 9.75 | A:e11 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 9.90 | A:e12 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 9.80 |
| 10.20 | A:e13 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 10.10 |
| 10.45 | A:e14 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 10.40 |
| 10.80 | A:e15 STOP_END<br>A:e16 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 10.70 |
| 12.10 | A:e17 TURN_LEFT_START<br>A:e18 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 12.00 |
| 12.55 | A:e19 TRACK_APPEARED_LEFT track_006<br>A:e20 TRACK_APPEARED_LEFT track_007<br>A:e21 CLOSING_START track_006<br>A:e22 CLOSING_START track_007 | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 12.50 |
| 12.60 | A:e23 TRACK_APPEARED_LEFT track_002<br>A:e24 TRACK_APPEARED_LEFT track_003<br>A:e25 TRACK_APPEARED_LEFT track_004<br>A:e26 CLOSING_START track_002<br>A:e27 CLOSING_START track_003<br>A:e28 CLOSING_START track_004 | ego: MOVING, TURN_LEFT<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 12.50 |
| 12.65 | A:e29 TRACK_APPEARED_LEFT track_005<br>A:e30 CLOSING_START track_005 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 12.60 |
| 13.05 | A:e31 TRACK_APPEARED_LEFT track_009<br>A:e32 TRACK_APPEARED_LEFT track_013<br>A:e33 TRACK_APPEARED_RIGHT track_008<br>A:e34 CLOSING_START track_009<br>A:e35 CLOSING_START track_013 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.00 |
| 13.10 | A:e36 TRACK_APPEARED_LEFT track_011<br>A:e37 TRACK_APPEARED_LEFT track_015<br>A:e38 TRACK_APPEARED_RIGHT track_010<br>A:e39 CLOSING_START track_011<br>A:e40 CLOSING_START track_015 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.00 |
| 13.15 | A:e41 TRACK_APPEARED_LEFT track_012<br>A:e42 CLOSING_START track_012 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.10 |
| 13.20 | A:e43 TRACK_APPEARED_LEFT track_014<br>A:e44 CLOSING_START track_014 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.10 |
| 13.25 | A:e45 TRACK_APPEARED_LEFT track_017<br>A:e46 TRACK_APPEARED_RIGHT track_016<br>A:e47 CLOSING_START track_017 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.20 |
| 13.30 | A:e48 TRACK_LOST track_008 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 13.20 |
| 13.35 | A:e49 TRACK_APPEARED_RIGHT track_018<br>A:e50 CLOSING_START track_018 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path | 13.30 |
| 13.40 | A:e51 TRACK_APPEARED_LEFT track_019<br>A:e52 CLOSING_START track_019 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path | 13.30 |
| 13.50 | A:e53 TRACK_LOST track_010 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path | 13.40 |
| 14.00 | A:e54 CLOSING_START track_016 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010<br>sign-0: STOP sign known, relevant to the path | 13.90 |
| 14.45 | A:e55 TRACK_LOST track_019 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010<br>sign-0: STOP sign known, relevant to the path | 14.40 |
| 14.60 | A:e56 TRACK_LOST track_018 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_019<br>sign-0: STOP sign known, relevant to the path | 14.50 |
| 14.90 | A:e57 EGO_PATH_ENTRY track_017 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 14.80 |
| 15.15 | A:e58 TRACK_LOST track_014 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 15.10 |
| 15.30 | A:e59 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 15.20 |
| 15.35 | A:e60 EGO_PATH_ENTRY track_006 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 15.30 |
| 15.55 | A:e61 EGO_PATH_EXIT track_017 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 15.50 |
| 15.90 | A:e62 CUT_IN_FROM_RIGHT_START track_016 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 15.80 |
| 16.05 | A:e63 TRACK_LOST track_012 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 16.00 |
| 16.35 | A:e64 TRACK_LOST track_009 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_012, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 16.30 |
| 16.40 | A:e65 TRACK_LOST track_004 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_009, track_010, track_012, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path | 16.30 |

## States still active when observation ended

- MOVING, since A:e16 (t = 10.80 s)
- CLOSING of track_006, since A:e21 (t = 12.55 s)
- CLOSING of track_007, since A:e22 (t = 12.55 s)
- CLOSING of track_002, since A:e26 (t = 12.60 s)
- CLOSING of track_003, since A:e27 (t = 12.60 s)
- CLOSING of track_004, since A:e28 (t = 12.60 s); the track was lost at 16.40 s
- CLOSING of track_005, since A:e30 (t = 12.65 s)
- CLOSING of track_009, since A:e34 (t = 13.05 s); the track was lost at 16.35 s
- CLOSING of track_013, since A:e35 (t = 13.05 s)
- CLOSING of track_011, since A:e39 (t = 13.10 s)
- CLOSING of track_015, since A:e40 (t = 13.10 s)
- CLOSING of track_012, since A:e42 (t = 13.15 s); the track was lost at 16.05 s
- CLOSING of track_014, since A:e44 (t = 13.20 s); the track was lost at 15.15 s
- CLOSING of track_017, since A:e47 (t = 13.25 s)
- CLOSING of track_018, since A:e50 (t = 13.35 s); the track was lost at 14.60 s
- CLOSING of track_019, since A:e52 (t = 13.40 s); the track was lost at 14.45 s
- CLOSING of track_016, since A:e54 (t = 14.00 s)
- EGO_PATH of track_006, since A:e60 (t = 15.35 s)
- CUT_IN_FROM_RIGHT of track_016, since A:e62 (t = 15.90 s)

## Tracks lost

- track_019 at 14.45 s (A:e55): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_018 at 14.60 s (A:e56): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_014 at 15.15 s (A:e58): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 16.05 s (A:e63): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 16.35 s (A:e64): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 16.40 s (A:e65): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001, track_008, track_010

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 9.75, no critical TTC
- track_006: EGO_PATH_ENTRY 15.35, no critical TTC
- track_016: CUT_IN_FROM_RIGHT_START 15.90, no critical TTC after it
- track_017: EGO_PATH_ENTRY 14.90, no critical TTC

## Sign detection windows

- STOP sign sign-0: detected 0.95 s -> 3.60 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.10 | 12.10 | 180 | 27.6 m / -44 deg | 10.08 m (9.95) | 17.4 m / +81 deg | 8.2 m/s |
| track_002 | 12.60 | 16.45 | 57 | 51.6 m / -78 deg | 23.45 m (16.45) | 23.4 m / -31 deg | 1.6 m/s |
| track_003 | 12.60 | 16.45 | 69 | 43.0 m / -79 deg | 16.40 m (16.45) | 16.4 m / -48 deg | 1.6 m/s |
| track_004 | 12.60 | 16.40 | 47 | 57.5 m / -78 deg | 28.50 m (16.40) | 28.5 m / -25 deg | 1.9 m/s |
| track_005 | 12.65 | 16.45 | 70 | 36.8 m / -79 deg | 12.93 m (16.45) | 12.9 m / -74 deg | 2.2 m/s |
| track_006 | 12.55 | 16.45 | 63 | 87.2 m / -69 deg | 56.29 m (16.45) | 56.3 m / +1 deg | 1.2 m/s |
| track_007 | 12.55 | 16.45 | 53 | 62.5 m / -79 deg | 32.61 m (16.45) | 32.6 m / -22 deg | 2.6 m/s |
| track_008 | 13.05 | 13.30 | 6 | 15.0 m / +74 deg | 14.97 m (13.05) | 15.4 m / +81 deg | 13.8 m/s |
| track_009 | 13.05 | 16.35 | 67 | 26.4 m / -78 deg | 10.79 m (16.35) | 10.8 m / -78 deg | 6.7 m/s |
| track_010 | 13.10 | 13.50 | 9 | 12.2 m / +65 deg | 12.17 m (13.15) | 12.9 m / +82 deg | 10.8 m/s |
| track_011 | 13.10 | 16.45 | 59 | 89.8 m / -60 deg | 62.34 m (16.45) | 62.3 m / -5 deg | 4.3 m/s |
| track_012 | 13.15 | 16.05 | 59 | 29.9 m / -74 deg | 12.23 m (16.05) | 12.2 m / -71 deg | 2.4 m/s |
| track_013 | 13.05 | 16.45 | 59 | 93.0 m / -66 deg | 65.43 m (16.45) | 65.4 m / -10 deg | 2.6 m/s |
| track_014 | 13.20 | 15.15 | 40 | 20.8 m / -78 deg | 11.32 m (15.15) | 11.3 m / -81 deg | 3.2 m/s |
| track_015 | 13.10 | 16.45 | 54 | 44.7 m / -70 deg | 19.68 m (16.45) | 19.7 m / -38 deg | 1.6 m/s |
| track_016 | 13.25 | 16.45 | 65 | 9.8 m / +60 deg | 6.35 m (16.45) | 6.3 m / +75 deg | 13.9 m/s |
| track_017 | 13.25 | 16.45 | 59 | 78.7 m / -48 deg | 52.14 m (16.45) | 52.1 m / +4 deg | 1.4 m/s |
| track_018 | 13.35 | 14.60 | 26 | 10.6 m / +46 deg | 7.85 m (14.60) | 7.8 m / +47 deg | 13.2 m/s |
| track_019 | 13.40 | 14.45 | 22 | 16.1 m / -80 deg | 11.31 m (14.45) | 11.3 m / -82 deg | 2.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.95 s: A's camera established a STOP sign detection (sign-0).
- t = 3.10 s: A's radar started tracking track_001, which appeared on its left.
- t = 3.10 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.60 s: A's camera stopped detecting STOP sign sign-0.
- t = 4.35 s: A started braking.
- t = 4.70 s: A observed track_001 stop closing in.
- t = 4.75 s: A stopped moving.
- t = 4.75 s: A came to a stop.
- t = 6.95 s: A observed track_001 start closing in.
- t = 9.75 s: A observed track_001 enter its forward path corridor.
- t = 9.90 s: A observed track_001 stop closing in.
- t = 10.20 s: A observed track_001 leave its forward path corridor.
- t = 10.45 s: A released the brake.
- t = 10.80 s: A left its stop.
- t = 10.80 s: A started moving.
- t = 12.10 s: A started turning left.
- t = 12.10 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 12.55 s: A's radar started tracking track_006, which appeared on its left.
- t = 12.55 s: A's radar started tracking track_007, which appeared on its left.
- t = 12.55 s: A observed track_006 start closing in (already the case when first observed).
- t = 12.55 s: A observed track_007 start closing in (already the case when first observed).
- t = 12.60 s: A's radar started tracking track_002, which appeared on its left.
- t = 12.60 s: A's radar started tracking track_003, which appeared on its left.
- t = 12.60 s: A's radar started tracking track_004, which appeared on its left.
- t = 12.60 s: A observed track_002 start closing in (already the case when first observed).
- t = 12.60 s: A observed track_003 start closing in (already the case when first observed).
- t = 12.60 s: A observed track_004 start closing in (already the case when first observed).
- t = 12.65 s: A's radar started tracking track_005, which appeared on its left.
- t = 12.65 s: A observed track_005 start closing in (already the case when first observed).
- t = 13.05 s: A's radar started tracking track_009, which appeared on its left.
- t = 13.05 s: A's radar started tracking track_013, which appeared on its left.
- t = 13.05 s: A's radar started tracking track_008, which appeared on its right.
- t = 13.05 s: A observed track_009 start closing in (already the case when first observed).
- t = 13.05 s: A observed track_013 start closing in (already the case when first observed).
- t = 13.10 s: A's radar started tracking track_011, which appeared on its left.
- t = 13.10 s: A's radar started tracking track_015, which appeared on its left.
- t = 13.10 s: A's radar started tracking track_010, which appeared on its right.
- t = 13.10 s: A observed track_011 start closing in (already the case when first observed).
- t = 13.10 s: A observed track_015 start closing in (already the case when first observed).
- t = 13.15 s: A's radar started tracking track_012, which appeared on its left.
- t = 13.15 s: A observed track_012 start closing in (already the case when first observed).
- t = 13.20 s: A's radar started tracking track_014, which appeared on its left.
- t = 13.20 s: A observed track_014 start closing in (already the case when first observed).
- t = 13.25 s: A's radar started tracking track_017, which appeared on its left.
- t = 13.25 s: A's radar started tracking track_016, which appeared on its right.
- t = 13.25 s: A observed track_017 start closing in (already the case when first observed).
- t = 13.30 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 13.35 s: A's radar started tracking track_018, which appeared on its right.
- t = 13.35 s: A observed track_018 start closing in (already the case when first observed).
- t = 13.40 s: A's radar started tracking track_019, which appeared on its left.
- t = 13.40 s: A observed track_019 start closing in (already the case when first observed).
- t = 13.50 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 14.00 s: A observed track_016 start closing in.
- t = 14.45 s: A's radar lost track_019 (its states are UNKNOWN from then on, not ended).
- t = 14.60 s: A's radar lost track_018 (its states are UNKNOWN from then on, not ended).
- t = 14.90 s: A observed track_017 enter its forward path corridor.
- t = 15.15 s: A's radar lost track_014 (its states are UNKNOWN from then on, not ended).
- t = 15.30 s: A stopped turning left.
- t = 15.35 s: A observed track_006 enter its forward path corridor.
- t = 15.55 s: A observed track_017 leave its forward path corridor.
- t = 15.90 s: A observed track_016 cutting in from the right.
- t = 16.05 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 16.35 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 16.40 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
