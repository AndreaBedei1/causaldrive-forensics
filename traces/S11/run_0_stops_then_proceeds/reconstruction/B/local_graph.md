# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 216.8642254061997 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 57; edges: 205 (PRECEDES 172, SAME_TRACK 33)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.05 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e03 | 2.40 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e04 | 2.50 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e05 | 2.50 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e07 | 3.25 | MOVING_END | B | - | ego |  |
| B:e08 | 3.25 | STOP_START | B | - | ego |  |
| B:e09 | 5.80 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e10 | 6.10 | CLOSING_END | B | track_001 | radar |  |
| B:e11 | 6.20 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e12 | 6.75 | BRAKE_END | B | - | controls |  |
| B:e13 | 7.20 | STOP_END | B | - | ego |  |
| B:e14 | 7.20 | MOVING_START | B | - | ego |  |
| B:e15 | 7.95 | TURN_LEFT_START | B | - | ego |  |
| B:e16 | 7.95 | TRACK_LOST | B | track_001 | radar |  |
| B:e17 | 8.40 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e18 | 8.40 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e19 | 8.40 | TRACK_APPEARED_LEFT | B | track_005 | radar |  |
| B:e20 | 8.40 | TRACK_APPEARED_LEFT | B | track_006 | radar |  |
| B:e21 | 8.40 | TRACK_APPEARED_LEFT | B | track_007 | radar |  |
| B:e22 | 8.40 | TRACK_APPEARED_LEFT | B | track_008 | radar |  |
| B:e23 | 8.40 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e24 | 8.40 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e25 | 8.40 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e26 | 8.40 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e27 | 8.40 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e28 | 8.40 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e29 | 8.40 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e30 | 8.45 | TRACK_APPEARED_LEFT | B | track_010 | radar |  |
| B:e31 | 8.45 | TRACK_APPEARED_RIGHT | B | track_009 | radar |  |
| B:e32 | 8.45 | TRACK_APPEARED_RIGHT | B | track_011 | radar |  |
| B:e33 | 8.45 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e34 | 8.45 | CLOSING_START | B | track_010 | radar | active_at_first_observation=True |
| B:e35 | 8.45 | CLOSING_START | B | track_011 | radar | active_at_first_observation=True |
| B:e36 | 8.60 | TRACK_APPEARED_RIGHT | B | track_012 | radar |  |
| B:e37 | 8.60 | TRACK_APPEARED_RIGHT | B | track_013 | radar |  |
| B:e38 | 8.60 | CLOSING_START | B | track_012 | radar | active_at_first_observation=True |
| B:e39 | 8.60 | CLOSING_START | B | track_013 | radar | active_at_first_observation=True |
| B:e40 | 8.65 | TRACK_LOST | B | track_005 | radar |  |
| B:e41 | 8.80 | TRACK_LOST | B | track_002 | radar |  |
| B:e42 | 8.80 | TRACK_LOST | B | track_011 | radar |  |
| B:e43 | 8.90 | CLOSING_END | B | track_009 | radar |  |
| B:e44 | 8.90 | CRITICAL_TTC_START | B | track_004 | radar |  |
| B:e45 | 8.95 | TRACK_LOST | B | track_013 | radar |  |
| B:e46 | 9.00 | TRACK_LOST | B | track_009 | radar |  |
| B:e47 | 9.50 | TRACK_LOST | B | track_004 | radar |  |
| B:e48 | 9.70 | TRACK_LOST | B | track_010 | radar |  |
| B:e49 | 10.70 | TURN_LEFT_END | B | - | ego |  |
| B:e50 | 10.70 | TRACK_LOST | B | track_003 | radar |  |
| B:e51 | 12.05 | CLOSING_END | B | track_012 | radar |  |
| B:e52 | 12.20 | TRACK_LOST | B | track_008 | radar |  |
| B:e53 | 12.30 | CLOSING_START | B | track_012 | radar |  |
| B:e54 | 12.55 | CUT_IN_FROM_LEFT_START | B | track_007 | radar |  |
| B:e55 | 12.75 | CUT_IN_FROM_RIGHT_START | B | track_012 | radar |  |
| B:e56 | 12.90 | TRACK_LOST | B | track_007 | radar |  |
| B:e57 | 13.05 | TRACK_LOST | B | track_012 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e19
    B:e15 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e22
    B:e15 --PRECEDES--> B:e23
    B:e15 --PRECEDES--> B:e24
    B:e15 --PRECEDES--> B:e25
    B:e15 --PRECEDES--> B:e26
    B:e15 --PRECEDES--> B:e27
    B:e15 --PRECEDES--> B:e28
    B:e15 --PRECEDES--> B:e29
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e23
    B:e16 --PRECEDES--> B:e24
    B:e16 --PRECEDES--> B:e25
    B:e16 --PRECEDES--> B:e26
    B:e16 --PRECEDES--> B:e27
    B:e16 --PRECEDES--> B:e28
    B:e16 --PRECEDES--> B:e29
    B:e17 --PRECEDES--> B:e30
    B:e17 --PRECEDES--> B:e31
    B:e17 --PRECEDES--> B:e32
    B:e17 --PRECEDES--> B:e33
    B:e17 --PRECEDES--> B:e34
    B:e17 --PRECEDES--> B:e35
    B:e18 --PRECEDES--> B:e30
    B:e18 --PRECEDES--> B:e31
    B:e18 --PRECEDES--> B:e32
    B:e18 --PRECEDES--> B:e33
    B:e18 --PRECEDES--> B:e34
    B:e18 --PRECEDES--> B:e35
    B:e19 --PRECEDES--> B:e30
    B:e19 --PRECEDES--> B:e31
    B:e19 --PRECEDES--> B:e32
    B:e19 --PRECEDES--> B:e33
    B:e19 --PRECEDES--> B:e34
    B:e19 --PRECEDES--> B:e35
    B:e20 --PRECEDES--> B:e30
    B:e20 --PRECEDES--> B:e31
    B:e20 --PRECEDES--> B:e32
    B:e20 --PRECEDES--> B:e33
    B:e20 --PRECEDES--> B:e34
    B:e20 --PRECEDES--> B:e35
    B:e21 --PRECEDES--> B:e30
    B:e21 --PRECEDES--> B:e31
    B:e21 --PRECEDES--> B:e32
    B:e21 --PRECEDES--> B:e33
    B:e21 --PRECEDES--> B:e34
    B:e21 --PRECEDES--> B:e35
    B:e22 --PRECEDES--> B:e30
    B:e22 --PRECEDES--> B:e31
    B:e22 --PRECEDES--> B:e32
    B:e22 --PRECEDES--> B:e33
    B:e22 --PRECEDES--> B:e34
    B:e22 --PRECEDES--> B:e35
    B:e23 --PRECEDES--> B:e30
    B:e23 --PRECEDES--> B:e31
    B:e23 --PRECEDES--> B:e32
    B:e23 --PRECEDES--> B:e33
    B:e23 --PRECEDES--> B:e34
    B:e23 --PRECEDES--> B:e35
    B:e24 --PRECEDES--> B:e30
    B:e24 --PRECEDES--> B:e31
    B:e24 --PRECEDES--> B:e32
    B:e24 --PRECEDES--> B:e33
    B:e24 --PRECEDES--> B:e34
    B:e24 --PRECEDES--> B:e35
    B:e25 --PRECEDES--> B:e30
    B:e25 --PRECEDES--> B:e31
    B:e25 --PRECEDES--> B:e32
    B:e25 --PRECEDES--> B:e33
    B:e25 --PRECEDES--> B:e34
    B:e25 --PRECEDES--> B:e35
    B:e26 --PRECEDES--> B:e30
    B:e26 --PRECEDES--> B:e31
    B:e26 --PRECEDES--> B:e32
    B:e26 --PRECEDES--> B:e33
    B:e26 --PRECEDES--> B:e34
    B:e26 --PRECEDES--> B:e35
    B:e27 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e31
    B:e27 --PRECEDES--> B:e32
    B:e27 --PRECEDES--> B:e33
    B:e27 --PRECEDES--> B:e34
    B:e27 --PRECEDES--> B:e35
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e28 --PRECEDES--> B:e32
    B:e28 --PRECEDES--> B:e33
    B:e28 --PRECEDES--> B:e34
    B:e28 --PRECEDES--> B:e35
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e32
    B:e29 --PRECEDES--> B:e33
    B:e29 --PRECEDES--> B:e34
    B:e29 --PRECEDES--> B:e35
    B:e30 --PRECEDES--> B:e36
    B:e30 --PRECEDES--> B:e37
    B:e30 --PRECEDES--> B:e38
    B:e30 --PRECEDES--> B:e39
    B:e31 --PRECEDES--> B:e36
    B:e31 --PRECEDES--> B:e37
    B:e31 --PRECEDES--> B:e38
    B:e31 --PRECEDES--> B:e39
    B:e32 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e37
    B:e32 --PRECEDES--> B:e38
    B:e32 --PRECEDES--> B:e39
    B:e33 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e37
    B:e33 --PRECEDES--> B:e38
    B:e33 --PRECEDES--> B:e39
    B:e34 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e34 --PRECEDES--> B:e38
    B:e34 --PRECEDES--> B:e39
    B:e35 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e38
    B:e35 --PRECEDES--> B:e39
    B:e36 --PRECEDES--> B:e40
    B:e37 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e40
    B:e40 --PRECEDES--> B:e41
    B:e40 --PRECEDES--> B:e42
    B:e41 --PRECEDES--> B:e43
    B:e41 --PRECEDES--> B:e44
    B:e42 --PRECEDES--> B:e43
    B:e42 --PRECEDES--> B:e44
    B:e43 --PRECEDES--> B:e45
    B:e44 --PRECEDES--> B:e45
    B:e45 --PRECEDES--> B:e46
    B:e46 --PRECEDES--> B:e47
    B:e47 --PRECEDES--> B:e48
    B:e48 --PRECEDES--> B:e49
    B:e48 --PRECEDES--> B:e50
    B:e49 --PRECEDES--> B:e51
    B:e50 --PRECEDES--> B:e51
    B:e51 --PRECEDES--> B:e52
    B:e52 --PRECEDES--> B:e53
    B:e53 --PRECEDES--> B:e54
    B:e54 --PRECEDES--> B:e55
    B:e55 --PRECEDES--> B:e56
    B:e56 --PRECEDES--> B:e57
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e09
    B:e04 --SAME_TRACK--> B:e10
    B:e04 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e16
    B:e17 --SAME_TRACK--> B:e24
    B:e18 --SAME_TRACK--> B:e25
    B:e19 --SAME_TRACK--> B:e26
    B:e20 --SAME_TRACK--> B:e27
    B:e21 --SAME_TRACK--> B:e28
    B:e22 --SAME_TRACK--> B:e29
    B:e31 --SAME_TRACK--> B:e33
    B:e30 --SAME_TRACK--> B:e34
    B:e32 --SAME_TRACK--> B:e35
    B:e36 --SAME_TRACK--> B:e38
    B:e37 --SAME_TRACK--> B:e39
    B:e19 --SAME_TRACK--> B:e40
    B:e23 --SAME_TRACK--> B:e41
    B:e32 --SAME_TRACK--> B:e42
    B:e31 --SAME_TRACK--> B:e43
    B:e18 --SAME_TRACK--> B:e44
    B:e37 --SAME_TRACK--> B:e45
    B:e31 --SAME_TRACK--> B:e46
    B:e18 --SAME_TRACK--> B:e47
    B:e30 --SAME_TRACK--> B:e48
    B:e17 --SAME_TRACK--> B:e50
    B:e36 --SAME_TRACK--> B:e51
    B:e22 --SAME_TRACK--> B:e52
    B:e36 --SAME_TRACK--> B:e53
    B:e21 --SAME_TRACK--> B:e54
    B:e36 --SAME_TRACK--> B:e55
    B:e21 --SAME_TRACK--> B:e56
    B:e36 --SAME_TRACK--> B:e57
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.05 | B:e02 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 2.00 |
| 2.40 | B:e03 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign known | 2.30 |
| 2.50 | B:e04 TRACK_APPEARED_LEFT track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING<br>sign-1: STOP sign known | 2.40 |
| 2.55 | B:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known | 2.50 |
| 3.25 | B:e07 MOVING_END<br>B:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 3.20 |
| 5.80 | B:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 5.70 |
| 6.10 | B:e10 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known | 6.00 |
| 6.20 | B:e11 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known | 6.10 |
| 6.75 | B:e12 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-1: STOP sign known | 6.70 |
| 7.20 | B:e13 STOP_END<br>B:e14 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-1: STOP sign known | 7.10 |
| 7.95 | B:e15 TURN_LEFT_START<br>B:e16 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-1: STOP sign known | 7.90 |
| 8.40 | B:e17 TRACK_APPEARED_LEFT track_003<br>B:e18 TRACK_APPEARED_LEFT track_004<br>B:e19 TRACK_APPEARED_LEFT track_005<br>B:e20 TRACK_APPEARED_LEFT track_006<br>B:e21 TRACK_APPEARED_LEFT track_007<br>B:e22 TRACK_APPEARED_LEFT track_008<br>B:e23 TRACK_APPEARED_RIGHT track_002<br>B:e24 CLOSING_START track_003<br>B:e25 CLOSING_START track_004<br>B:e26 CLOSING_START track_005<br>B:e27 CLOSING_START track_006<br>B:e28 CLOSING_START track_007<br>B:e29 CLOSING_START track_008 | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.30 |
| 8.45 | B:e30 TRACK_APPEARED_LEFT track_010<br>B:e31 TRACK_APPEARED_RIGHT track_009<br>B:e32 TRACK_APPEARED_RIGHT track_011<br>B:e33 CLOSING_START track_009<br>B:e34 CLOSING_START track_010<br>B:e35 CLOSING_START track_011 | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.40 |
| 8.60 | B:e36 TRACK_APPEARED_RIGHT track_012<br>B:e37 TRACK_APPEARED_RIGHT track_013<br>B:e38 CLOSING_START track_012<br>B:e39 CLOSING_START track_013 | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.50 |
| 8.65 | B:e40 TRACK_LOST track_005 | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.60 |
| 8.80 | B:e41 TRACK_LOST track_002<br>B:e42 TRACK_LOST track_011 | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known | 8.70 |
| 8.90 | B:e43 CLOSING_END track_009<br>B:e44 CRITICAL_TTC_START track_004 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011<br>sign-1: STOP sign known | 8.80 |
| 8.95 | B:e45 TRACK_LOST track_013 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: no active state<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011<br>sign-1: STOP sign known | 8.90 |
| 9.00 | B:e46 TRACK_LOST track_009 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: no active state<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011, track_013<br>sign-1: STOP sign known | 8.90 |
| 9.50 | B:e47 TRACK_LOST track_004 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_009, track_011, track_013<br>sign-1: STOP sign known | 9.40 |
| 9.70 | B:e48 TRACK_LOST track_010 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_011, track_013<br>sign-1: STOP sign known | 9.60 |
| 10.70 | B:e49 TURN_LEFT_END<br>B:e50 TRACK_LOST track_003 | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 10.60 |
| 12.05 | B:e51 CLOSING_END track_012 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.00 |
| 12.20 | B:e52 TRACK_LOST track_008 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.10 |
| 12.30 | B:e53 CLOSING_START track_012 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.20 |
| 12.55 | B:e54 CUT_IN_FROM_LEFT_START track_007 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.50 |
| 12.75 | B:e55 CUT_IN_FROM_RIGHT_START track_012 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.70 |
| 12.90 | B:e56 TRACK_LOST track_007 | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT<br>track_012: CLOSING, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 12.80 |
| 13.05 | B:e57 TRACK_LOST track_012 | ego: MOVING<br>track_006: CLOSING<br>track_012: CLOSING, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known | 13.00 |

## States still active when observation ended

- MOVING, since B:e14 (t = 7.20 s)
- CLOSING of track_003, since B:e24 (t = 8.40 s); the track was lost at 10.70 s
- CLOSING of track_004, since B:e25 (t = 8.40 s); the track was lost at 9.50 s
- CLOSING of track_005, since B:e26 (t = 8.40 s); the track was lost at 8.65 s
- CLOSING of track_006, since B:e27 (t = 8.40 s)
- CLOSING of track_007, since B:e28 (t = 8.40 s); the track was lost at 12.90 s
- CLOSING of track_008, since B:e29 (t = 8.40 s); the track was lost at 12.20 s
- CLOSING of track_010, since B:e34 (t = 8.45 s); the track was lost at 9.70 s
- CLOSING of track_011, since B:e35 (t = 8.45 s); the track was lost at 8.80 s
- CLOSING of track_013, since B:e39 (t = 8.60 s); the track was lost at 8.95 s
- CRITICAL_TTC of track_004, since B:e44 (t = 8.90 s); the track was lost at 9.50 s
- CLOSING of track_012, since B:e53 (t = 12.30 s); the track was lost at 13.05 s
- CUT_IN_FROM_LEFT of track_007, since B:e54 (t = 12.55 s); the track was lost at 12.90 s
- CUT_IN_FROM_RIGHT of track_012, since B:e55 (t = 12.75 s); the track was lost at 13.05 s

## Tracks lost

- track_005 at 8.65 s (B:e40): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 8.80 s (B:e42): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 8.95 s (B:e45): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 9.50 s (B:e47): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 9.70 s (B:e48): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 10.70 s (B:e50): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 12.20 s (B:e52): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 12.90 s (B:e56): CLOSING, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 13.05 s (B:e57): CLOSING, CUT_IN_FROM_RIGHT were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001, track_002, track_009

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.80, no critical TTC
- track_004: CRITICAL_TTC_START 8.90
- track_007: CUT_IN_FROM_LEFT_START 12.55, no critical TTC after it
- track_012: CUT_IN_FROM_RIGHT_START 12.75, no critical TTC after it

## Sign detection windows

- STOP sign sign-1: detected 2.05 s -> 2.40 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.50 | 7.95 | 110 | 36.2 m / -68 deg | 6.86 m (6.10) | 18.0 m / +80 deg | 10.1 m/s |
| track_002 | 8.40 | 8.80 | 9 | 18.7 m / +59 deg | 18.71 m (8.45) | 19.1 m / +82 deg | 8.4 m/s |
| track_003 | 8.40 | 10.70 | 47 | 21.3 m / -77 deg | 10.14 m (10.70) | 10.1 m / -80 deg | 6.0 m/s |
| track_004 | 8.40 | 9.50 | 23 | 13.2 m / -73 deg | 6.57 m (9.50) | 6.6 m / -81 deg | 1.5 m/s |
| track_005 | 8.40 | 8.65 | 6 | 130.9 m / -64 deg | 128.70 m (8.65) | 128.7 m / -50 deg | 3.5 m/s |
| track_006 | 8.40 | 13.35 | 92 | 41.6 m / -72 deg | 10.40 m (13.35) | 10.4 m / -78 deg | 7.3 m/s |
| track_007 | 8.40 | 12.90 | 88 | 28.8 m / -75 deg | 8.27 m (12.90) | 8.3 m / -73 deg | 9.4 m/s |
| track_008 | 8.40 | 12.20 | 75 | 33.7 m / -74 deg | 10.36 m (12.20) | 10.4 m / -71 deg | 7.2 m/s |
| track_009 | 8.45 | 9.00 | 12 | 16.7 m / +46 deg | 16.31 m (8.80) | 16.5 m / +83 deg | 4.2 m/s |
| track_010 | 8.45 | 9.70 | 26 | 17.1 m / -80 deg | 10.79 m (9.70) | 10.8 m / -81 deg | 2.0 m/s |
| track_011 | 8.45 | 8.80 | 8 | 22.7 m / +37 deg | 21.75 m (8.80) | 21.8 m / +65 deg | 2.3 m/s |
| track_012 | 8.60 | 13.05 | 84 | 14.1 m / +49 deg | 7.50 m (13.05) | 7.5 m / +75 deg | 15.5 m/s |
| track_013 | 8.60 | 8.95 | 6 | 10.0 m / +43 deg | 9.40 m (8.90) | 9.4 m / +77 deg | 1.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.05 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.40 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.50 s: B's radar started tracking track_001, which appeared on its left.
- t = 2.50 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.55 s: B started braking.
- t = 3.25 s: B stopped moving.
- t = 3.25 s: B came to a stop.
- t = 5.80 s: B observed track_001 enter its forward path corridor.
- t = 6.10 s: B observed track_001 stop closing in.
- t = 6.20 s: B observed track_001 leave its forward path corridor.
- t = 6.75 s: B released the brake.
- t = 7.20 s: B left its stop.
- t = 7.20 s: B started moving.
- t = 7.95 s: B started turning left.
- t = 7.95 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.40 s: B's radar started tracking track_003, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_004, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_005, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_006, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_007, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_008, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_002, which appeared on its right.
- t = 8.40 s: B observed track_003 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_004 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_005 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_006 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_007 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_008 start closing in (already the case when first observed).
- t = 8.45 s: B's radar started tracking track_010, which appeared on its left.
- t = 8.45 s: B's radar started tracking track_009, which appeared on its right.
- t = 8.45 s: B's radar started tracking track_011, which appeared on its right.
- t = 8.45 s: B observed track_009 start closing in (already the case when first observed).
- t = 8.45 s: B observed track_010 start closing in (already the case when first observed).
- t = 8.45 s: B observed track_011 start closing in (already the case when first observed).
- t = 8.60 s: B's radar started tracking track_012, which appeared on its right.
- t = 8.60 s: B's radar started tracking track_013, which appeared on its right.
- t = 8.60 s: B observed track_012 start closing in (already the case when first observed).
- t = 8.60 s: B observed track_013 start closing in (already the case when first observed).
- t = 8.65 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 8.80 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 8.80 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 8.90 s: B observed track_009 stop closing in.
- t = 8.90 s: B's time-to-contact with track_004 became critical.
- t = 8.95 s: B's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 9.00 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 9.50 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 9.70 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 10.70 s: B stopped turning left.
- t = 10.70 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 12.05 s: B observed track_012 stop closing in.
- t = 12.20 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 12.30 s: B observed track_012 start closing in.
- t = 12.55 s: B observed track_007 cutting in from the left.
- t = 12.75 s: B observed track_012 cutting in from the right.
- t = 12.90 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 13.05 s: B's radar lost track_012 (its states are UNKNOWN from then on, not ended).
