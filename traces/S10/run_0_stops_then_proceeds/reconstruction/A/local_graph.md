# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 163.75191905722022 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 15 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 67; edges: 176 (PRECEDES 135, SAME_TRACK 41)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.85 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.40 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 2.40 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 2.55 | BRAKE_START | A | - | controls |  |
| A:e07 | 3.35 | MOVING_END | A | - | ego |  |
| A:e08 | 3.35 | STOP_START | A | - | ego |  |
| A:e09 | 5.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e10 | 6.10 | CLOSING_END | A | track_001 | radar |  |
| A:e11 | 6.25 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e12 | 6.75 | BRAKE_END | A | - | controls |  |
| A:e13 | 7.10 | STOP_END | A | - | ego |  |
| A:e14 | 7.10 | MOVING_START | A | - | ego |  |
| A:e15 | 7.50 | TRACK_LOST | A | track_001 | radar |  |
| A:e16 | 7.65 | TURN_LEFT_START | A | - | ego |  |
| A:e17 | 8.20 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e18 | 8.20 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e19 | 8.20 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e20 | 8.20 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e21 | 8.20 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e22 | 8.20 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e23 | 8.20 | TRACK_APPEARED_LEFT | A | track_012 | radar |  |
| A:e24 | 8.20 | TRACK_APPEARED_LEFT | A | track_013 | radar |  |
| A:e25 | 8.20 | TRACK_APPEARED_RIGHT | A | track_004 | radar |  |
| A:e26 | 8.20 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e27 | 8.20 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e28 | 8.20 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e29 | 8.20 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e30 | 8.20 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e31 | 8.20 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e32 | 8.20 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e33 | 8.20 | CLOSING_START | A | track_013 | radar | active_at_first_observation=True |
| A:e34 | 8.25 | TRACK_APPEARED_RIGHT | A | track_009 | radar |  |
| A:e35 | 8.25 | TRACK_APPEARED_RIGHT | A | track_010 | radar |  |
| A:e36 | 8.25 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e37 | 8.30 | TRACK_APPEARED_RIGHT | A | track_011 | radar |  |
| A:e38 | 8.30 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e39 | 8.45 | TRACK_APPEARED_LEFT | A | track_014 | radar |  |
| A:e40 | 8.45 | CLOSING_START | A | track_014 | radar | active_at_first_observation=True |
| A:e41 | 8.50 | TRACK_APPEARED_RIGHT | A | track_015 | radar |  |
| A:e42 | 8.50 | CLOSING_START | A | track_015 | radar | active_at_first_observation=True |
| A:e43 | 8.50 | CRITICAL_TTC_START | A | track_006 | radar |  |
| A:e44 | 8.55 | CLOSING_END | A | track_010 | radar |  |
| A:e45 | 8.55 | TRACK_LOST | A | track_010 | radar |  |
| A:e46 | 8.60 | TRACK_LOST | A | track_004 | radar |  |
| A:e47 | 8.60 | TRACK_LOST | A | track_008 | radar |  |
| A:e48 | 8.65 | TRACK_LOST | A | track_009 | radar |  |
| A:e49 | 8.70 | CLOSING_END | A | track_011 | radar |  |
| A:e50 | 9.10 | TRACK_LOST | A | track_006 | radar |  |
| A:e51 | 9.15 | TRACK_LOST | A | track_015 | radar |  |
| A:e52 | 9.30 | CLOSING_START | A | track_011 | radar |  |
| A:e53 | 10.20 | TRACK_LOST | A | track_014 | radar |  |
| A:e54 | 10.30 | TURN_LEFT_END | A | - | ego |  |
| A:e55 | 11.00 | CUT_IN_FROM_LEFT_START | A | track_002 | radar |  |
| A:e56 | 11.20 | TRACK_LOST | A | track_002 | radar |  |
| A:e57 | 11.65 | CLOSING_END | A | track_011 | radar |  |
| A:e58 | 11.75 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e59 | 11.75 | TRACK_LOST | A | track_007 | radar |  |
| A:e60 | 11.95 | CLOSING_START | A | track_011 | radar |  |
| A:e61 | 12.00 | TRACK_LOST | A | track_012 | radar |  |
| A:e62 | 12.15 | CRITICAL_TTC_START | A | track_011 | radar |  |
| A:e63 | 12.20 | CRITICAL_TTC_END | A | track_003 | radar |  |
| A:e64 | 12.20 | CUT_IN_FROM_LEFT_START | A | track_003 | radar |  |
| A:e65 | 12.45 | CUT_IN_FROM_RIGHT_START | A | track_011 | radar |  |
| A:e66 | 12.50 | TRACK_LOST | A | track_003 | radar |  |
| A:e67 | 13.15 | TRACK_LOST | A | track_013 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e20
    A:e16 --PRECEDES--> A:e21
    A:e16 --PRECEDES--> A:e22
    A:e16 --PRECEDES--> A:e23
    A:e16 --PRECEDES--> A:e24
    A:e16 --PRECEDES--> A:e25
    A:e16 --PRECEDES--> A:e26
    A:e16 --PRECEDES--> A:e27
    A:e16 --PRECEDES--> A:e28
    A:e16 --PRECEDES--> A:e29
    A:e16 --PRECEDES--> A:e30
    A:e16 --PRECEDES--> A:e31
    A:e16 --PRECEDES--> A:e32
    A:e16 --PRECEDES--> A:e33
    A:e17 --PRECEDES--> A:e34
    A:e17 --PRECEDES--> A:e35
    A:e17 --PRECEDES--> A:e36
    A:e18 --PRECEDES--> A:e34
    A:e18 --PRECEDES--> A:e35
    A:e18 --PRECEDES--> A:e36
    A:e19 --PRECEDES--> A:e34
    A:e19 --PRECEDES--> A:e35
    A:e19 --PRECEDES--> A:e36
    A:e20 --PRECEDES--> A:e34
    A:e20 --PRECEDES--> A:e35
    A:e20 --PRECEDES--> A:e36
    A:e21 --PRECEDES--> A:e34
    A:e21 --PRECEDES--> A:e35
    A:e21 --PRECEDES--> A:e36
    A:e22 --PRECEDES--> A:e34
    A:e22 --PRECEDES--> A:e35
    A:e22 --PRECEDES--> A:e36
    A:e23 --PRECEDES--> A:e34
    A:e23 --PRECEDES--> A:e35
    A:e23 --PRECEDES--> A:e36
    A:e24 --PRECEDES--> A:e34
    A:e24 --PRECEDES--> A:e35
    A:e24 --PRECEDES--> A:e36
    A:e25 --PRECEDES--> A:e34
    A:e25 --PRECEDES--> A:e35
    A:e25 --PRECEDES--> A:e36
    A:e26 --PRECEDES--> A:e34
    A:e26 --PRECEDES--> A:e35
    A:e26 --PRECEDES--> A:e36
    A:e27 --PRECEDES--> A:e34
    A:e27 --PRECEDES--> A:e35
    A:e27 --PRECEDES--> A:e36
    A:e28 --PRECEDES--> A:e34
    A:e28 --PRECEDES--> A:e35
    A:e28 --PRECEDES--> A:e36
    A:e29 --PRECEDES--> A:e34
    A:e29 --PRECEDES--> A:e35
    A:e29 --PRECEDES--> A:e36
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e30 --PRECEDES--> A:e36
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e38
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e37 --PRECEDES--> A:e40
    A:e38 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e43
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e44
    A:e41 --PRECEDES--> A:e45
    A:e42 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e44 --PRECEDES--> A:e47
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
    A:e57 --PRECEDES--> A:e59
    A:e58 --PRECEDES--> A:e60
    A:e59 --PRECEDES--> A:e60
    A:e60 --PRECEDES--> A:e61
    A:e61 --PRECEDES--> A:e62
    A:e62 --PRECEDES--> A:e63
    A:e62 --PRECEDES--> A:e64
    A:e63 --PRECEDES--> A:e65
    A:e64 --PRECEDES--> A:e65
    A:e65 --PRECEDES--> A:e66
    A:e66 --PRECEDES--> A:e67
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e04 --SAME_TRACK--> A:e11
    A:e04 --SAME_TRACK--> A:e15
    A:e17 --SAME_TRACK--> A:e26
    A:e18 --SAME_TRACK--> A:e27
    A:e19 --SAME_TRACK--> A:e28
    A:e20 --SAME_TRACK--> A:e29
    A:e21 --SAME_TRACK--> A:e30
    A:e22 --SAME_TRACK--> A:e31
    A:e23 --SAME_TRACK--> A:e32
    A:e24 --SAME_TRACK--> A:e33
    A:e35 --SAME_TRACK--> A:e36
    A:e37 --SAME_TRACK--> A:e38
    A:e39 --SAME_TRACK--> A:e40
    A:e41 --SAME_TRACK--> A:e42
    A:e20 --SAME_TRACK--> A:e43
    A:e35 --SAME_TRACK--> A:e44
    A:e35 --SAME_TRACK--> A:e45
    A:e25 --SAME_TRACK--> A:e46
    A:e22 --SAME_TRACK--> A:e47
    A:e34 --SAME_TRACK--> A:e48
    A:e37 --SAME_TRACK--> A:e49
    A:e20 --SAME_TRACK--> A:e50
    A:e41 --SAME_TRACK--> A:e51
    A:e37 --SAME_TRACK--> A:e52
    A:e39 --SAME_TRACK--> A:e53
    A:e17 --SAME_TRACK--> A:e55
    A:e17 --SAME_TRACK--> A:e56
    A:e37 --SAME_TRACK--> A:e57
    A:e18 --SAME_TRACK--> A:e58
    A:e21 --SAME_TRACK--> A:e59
    A:e37 --SAME_TRACK--> A:e60
    A:e23 --SAME_TRACK--> A:e61
    A:e37 --SAME_TRACK--> A:e62
    A:e18 --SAME_TRACK--> A:e63
    A:e18 --SAME_TRACK--> A:e64
    A:e37 --SAME_TRACK--> A:e65
    A:e18 --SAME_TRACK--> A:e66
    A:e24 --SAME_TRACK--> A:e67
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.85 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.80 |
| 2.15 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known | 2.10 |
| 2.40 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known | 2.30 |
| 2.55 | A:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 2.50 |
| 3.35 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 3.30 |
| 5.80 | A:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 5.70 |
| 6.10 | A:e10 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known | 6.00 |
| 6.25 | A:e11 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known | 6.20 |
| 6.75 | A:e12 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known | 6.70 |
| 7.10 | A:e13 STOP_END<br>A:e14 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known | 7.00 |
| 7.50 | A:e15 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known | 7.40 |
| 7.65 | A:e16 TURN_LEFT_START | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 7.60 |
| 8.20 | A:e17 TRACK_APPEARED_LEFT track_002<br>A:e18 TRACK_APPEARED_LEFT track_003<br>A:e19 TRACK_APPEARED_LEFT track_005<br>A:e20 TRACK_APPEARED_LEFT track_006<br>A:e21 TRACK_APPEARED_LEFT track_007<br>A:e22 TRACK_APPEARED_LEFT track_008<br>A:e23 TRACK_APPEARED_LEFT track_012<br>A:e24 TRACK_APPEARED_LEFT track_013<br>A:e25 TRACK_APPEARED_RIGHT track_004<br>A:e26 CLOSING_START track_002<br>A:e27 CLOSING_START track_003<br>A:e28 CLOSING_START track_005<br>A:e29 CLOSING_START track_006<br>A:e30 CLOSING_START track_007<br>A:e31 CLOSING_START track_008<br>A:e32 CLOSING_START track_012<br>A:e33 CLOSING_START track_013 | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.10 |
| 8.25 | A:e34 TRACK_APPEARED_RIGHT track_009<br>A:e35 TRACK_APPEARED_RIGHT track_010<br>A:e36 CLOSING_START track_010 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.20 |
| 8.30 | A:e37 TRACK_APPEARED_RIGHT track_011<br>A:e38 CLOSING_START track_011 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.20 |
| 8.45 | A:e39 TRACK_APPEARED_LEFT track_014<br>A:e40 CLOSING_START track_014 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.40 |
| 8.50 | A:e41 TRACK_APPEARED_RIGHT track_015<br>A:e42 CLOSING_START track_015<br>A:e43 CRITICAL_TTC_START track_006 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.40 |
| 8.55 | A:e44 CLOSING_END track_010<br>A:e45 TRACK_LOST track_010 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.50 |
| 8.60 | A:e46 TRACK_LOST track_004<br>A:e47 TRACK_LOST track_008 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_010<br>sign-0: STOP sign known | 8.50 |
| 8.65 | A:e48 TRACK_LOST track_009 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_009: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_010<br>sign-0: STOP sign known | 8.60 |
| 8.70 | A:e49 CLOSING_END track_011 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_009, track_010<br>sign-0: STOP sign known | 8.60 |
| 9.10 | A:e50 TRACK_LOST track_006 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_009, track_010<br>sign-0: STOP sign known | 9.00 |
| 9.15 | A:e51 TRACK_LOST track_015 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010<br>sign-0: STOP sign known | 9.10 |
| 9.30 | A:e52 CLOSING_START track_011 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_015<br>sign-0: STOP sign known | 9.20 |
| 10.20 | A:e53 TRACK_LOST track_014 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_015<br>sign-0: STOP sign known | 10.10 |
| 10.30 | A:e54 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 10.20 |
| 11.00 | A:e55 CUT_IN_FROM_LEFT_START track_002 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 10.90 |
| 11.20 | A:e56 TRACK_LOST track_002 | ego: MOVING<br>track_002: CLOSING, CUT_IN_FROM_LEFT<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 11.10 |
| 11.65 | A:e57 CLOSING_END track_011 | ego: MOVING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 11.60 |
| 11.75 | A:e58 CRITICAL_TTC_START track_003<br>A:e59 TRACK_LOST track_007 | ego: MOVING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 11.70 |
| 11.95 | A:e60 CLOSING_START track_011 | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 11.90 |
| 12.00 | A:e61 TRACK_LOST track_012 | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known | 11.90 |
| 12.15 | A:e62 CRITICAL_TTC_START track_011 | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known | 12.10 |
| 12.20 | A:e63 CRITICAL_TTC_END track_003<br>A:e64 CUT_IN_FROM_LEFT_START track_003 | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known | 12.10 |
| 12.45 | A:e65 CUT_IN_FROM_RIGHT_START track_011 | ego: MOVING<br>track_003: CLOSING, CUT_IN_FROM_LEFT<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known | 12.40 |
| 12.50 | A:e66 TRACK_LOST track_003 | ego: MOVING<br>track_003: CLOSING, CUT_IN_FROM_LEFT<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known | 12.40 |
| 13.15 | A:e67 TRACK_LOST track_013 | ego: MOVING<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known | 13.10 |

## States still active when observation ended

- MOVING, since A:e14 (t = 7.10 s)
- CLOSING of track_002, since A:e26 (t = 8.20 s); the track was lost at 11.20 s
- CLOSING of track_003, since A:e27 (t = 8.20 s); the track was lost at 12.50 s
- CLOSING of track_005, since A:e28 (t = 8.20 s)
- CLOSING of track_006, since A:e29 (t = 8.20 s); the track was lost at 9.10 s
- CLOSING of track_007, since A:e30 (t = 8.20 s); the track was lost at 11.75 s
- CLOSING of track_008, since A:e31 (t = 8.20 s); the track was lost at 8.60 s
- CLOSING of track_012, since A:e32 (t = 8.20 s); the track was lost at 12.00 s
- CLOSING of track_013, since A:e33 (t = 8.20 s); the track was lost at 13.15 s
- CLOSING of track_014, since A:e40 (t = 8.45 s); the track was lost at 10.20 s
- CLOSING of track_015, since A:e42 (t = 8.50 s); the track was lost at 9.15 s
- CRITICAL_TTC of track_006, since A:e43 (t = 8.50 s); the track was lost at 9.10 s
- CUT_IN_FROM_LEFT of track_002, since A:e55 (t = 11.00 s); the track was lost at 11.20 s
- CLOSING of track_011, since A:e60 (t = 11.95 s)
- CRITICAL_TTC of track_011, since A:e62 (t = 12.15 s)
- CUT_IN_FROM_LEFT of track_003, since A:e64 (t = 12.20 s); the track was lost at 12.50 s
- CUT_IN_FROM_RIGHT of track_011, since A:e65 (t = 12.45 s)

## Tracks lost

- track_010 at 8.55 s (A:e45): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 8.60 s (A:e47): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 9.10 s (A:e50): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_015 at 9.15 s (A:e51): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_014 at 10.20 s (A:e53): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 11.20 s (A:e56): CLOSING, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 11.75 s (A:e59): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 12.00 s (A:e61): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 12.50 s (A:e66): CLOSING, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 13.15 s (A:e67): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001, track_004, track_009

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.80, no critical TTC
- track_002: CUT_IN_FROM_LEFT_START 11.00, no critical TTC after it
- track_003: CUT_IN_FROM_LEFT_START 12.20, no critical TTC after it
- track_006: CRITICAL_TTC_START 8.50
- track_011: critical TTC already active before the cut-in: CRITICAL_TTC_START 12.15 <= CUT_IN_FROM_RIGHT_START 12.45 (+0.30 s)

## Sign detection windows

- STOP sign sign-0: detected 1.85 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.40 | 7.50 | 103 | 38.4 m / -70 deg | 5.30 m (6.10) | 13.7 m / +80 deg | 10.1 m/s |
| track_002 | 8.20 | 11.20 | 61 | 19.1 m / -79 deg | 8.70 m (11.20) | 8.7 m / -76 deg | 8.8 m/s |
| track_003 | 8.20 | 12.50 | 84 | 27.9 m / -72 deg | 8.47 m (12.50) | 8.5 m / -74 deg | 9.3 m/s |
| track_004 | 8.20 | 8.60 | 7 | 17.7 m / +70 deg | 17.66 m (8.20) | 18.4 m / +82 deg | 16.5 m/s |
| track_005 | 8.20 | 13.35 | 91 | 40.9 m / -69 deg | 9.98 m (13.35) | 10.0 m / -75 deg | 8.7 m/s |
| track_006 | 8.20 | 9.10 | 19 | 12.3 m / -75 deg | 6.89 m (9.10) | 6.9 m / -81 deg | 1.5 m/s |
| track_007 | 8.20 | 11.75 | 72 | 32.9 m / -71 deg | 10.50 m (11.75) | 10.5 m / -71 deg | 6.8 m/s |
| track_008 | 8.20 | 8.60 | 7 | 48.5 m / -67 deg | 45.07 m (8.60) | 45.1 m / -44 deg | 8.6 m/s |
| track_009 | 8.25 | 8.65 | 9 | 15.4 m / +57 deg | 15.34 m (8.35) | 15.8 m / +83 deg | 6.8 m/s |
| track_010 | 8.25 | 8.55 | 7 | 20.0 m / +47 deg | 19.72 m (8.45) | 19.8 m / +74 deg | 3.8 m/s |
| track_011 | 8.30 | 13.35 | 88 | 13.3 m / +49 deg | 5.28 m (13.35) | 5.3 m / +71 deg | 15.3 m/s |
| track_012 | 8.20 | 12.00 | 55 | 36.4 m / -70 deg | 11.13 m (12.00) | 11.1 m / -80 deg | 2.2 m/s |
| track_013 | 8.20 | 13.15 | 83 | 41.9 m / -66 deg | 10.02 m (13.15) | 10.0 m / -71 deg | 6.7 m/s |
| track_014 | 8.45 | 10.20 | 36 | 20.4 m / -67 deg | 10.86 m (10.20) | 10.9 m / -75 deg | 3.5 m/s |
| track_015 | 8.50 | 9.15 | 14 | 12.8 m / +49 deg | 12.25 m (9.15) | 12.2 m / +81 deg | 7.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.85 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.40 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.40 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.55 s: A started braking.
- t = 3.35 s: A stopped moving.
- t = 3.35 s: A came to a stop.
- t = 5.80 s: A observed track_001 enter its forward path corridor.
- t = 6.10 s: A observed track_001 stop closing in.
- t = 6.25 s: A observed track_001 leave its forward path corridor.
- t = 6.75 s: A released the brake.
- t = 7.10 s: A left its stop.
- t = 7.10 s: A started moving.
- t = 7.50 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 7.65 s: A started turning left.
- t = 8.20 s: A's radar started tracking track_002, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_003, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_005, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_006, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_007, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_008, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_012, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_013, which appeared on its left.
- t = 8.20 s: A's radar started tracking track_004, which appeared on its right.
- t = 8.20 s: A observed track_002 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_003 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_005 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_006 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_007 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_008 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_012 start closing in (already the case when first observed).
- t = 8.20 s: A observed track_013 start closing in (already the case when first observed).
- t = 8.25 s: A's radar started tracking track_009, which appeared on its right.
- t = 8.25 s: A's radar started tracking track_010, which appeared on its right.
- t = 8.25 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.30 s: A's radar started tracking track_011, which appeared on its right.
- t = 8.30 s: A observed track_011 start closing in (already the case when first observed).
- t = 8.45 s: A's radar started tracking track_014, which appeared on its left.
- t = 8.45 s: A observed track_014 start closing in (already the case when first observed).
- t = 8.50 s: A's radar started tracking track_015, which appeared on its right.
- t = 8.50 s: A observed track_015 start closing in (already the case when first observed).
- t = 8.50 s: A's time-to-contact with track_006 became critical.
- t = 8.55 s: A observed track_010 stop closing in.
- t = 8.55 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 8.60 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 8.60 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 8.65 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 8.70 s: A observed track_011 stop closing in.
- t = 9.10 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 9.15 s: A's radar lost track_015 (its states are UNKNOWN from then on, not ended).
- t = 9.30 s: A observed track_011 start closing in.
- t = 10.20 s: A's radar lost track_014 (its states are UNKNOWN from then on, not ended).
- t = 10.30 s: A stopped turning left.
- t = 11.00 s: A observed track_002 cutting in from the left.
- t = 11.20 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 11.65 s: A observed track_011 stop closing in.
- t = 11.75 s: A's time-to-contact with track_003 became critical.
- t = 11.75 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 11.95 s: A observed track_011 start closing in.
- t = 12.00 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 12.15 s: A's time-to-contact with track_011 became critical.
- t = 12.20 s: A's time-to-contact with track_003 stopped being critical.
- t = 12.20 s: A observed track_003 cutting in from the left.
- t = 12.45 s: A observed track_011 cutting in from the right.
- t = 12.50 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 13.15 s: A's radar lost track_013 (its states are UNKNOWN from then on, not ended).
