# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 349.14128875359893 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 12 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 50; edges: 125 (PRECEDES 100, SAME_TRACK 25)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.65 | HARD_BRAKE_START | A | - | controls |  |
| A:e06 | 3.40 | MOVING_END | A | - | ego |  |
| A:e07 | 3.40 | STOP_START | A | - | ego |  |
| A:e08 | 6.45 | HARD_BRAKE_END | A | - | controls |  |
| A:e09 | 6.45 | BRAKE_END | A | - | controls |  |
| A:e10 | 6.45 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e11 | 6.80 | STOP_END | A | - | ego |  |
| A:e12 | 6.80 | MOVING_START | A | - | ego |  |
| A:e13 | 7.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e14 | 8.85 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e15 | 8.85 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e16 | 8.85 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e17 | 8.85 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e18 | 8.95 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e19 | 8.95 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e20 | 9.00 | TRACK_APPEARED | A | track_004 | radar |  |
| A:e21 | 9.00 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e22 | 9.05 | TRACK_APPEARED | A | track_005 | radar |  |
| A:e23 | 9.05 | TRACK_APPEARED | A | track_007 | radar |  |
| A:e24 | 9.05 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e25 | 9.05 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e26 | 9.10 | TRACK_APPEARED | A | track_006 | radar |  |
| A:e27 | 9.10 | TRACK_APPEARED | A | track_008 | radar |  |
| A:e28 | 9.10 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e29 | 9.10 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e30 | 9.15 | TRACK_APPEARED | A | track_009 | radar |  |
| A:e31 | 9.15 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e32 | 9.20 | TRACK_APPEARED | A | track_010 | radar |  |
| A:e33 | 9.20 | TRACK_APPEARED | A | track_011 | radar |  |
| A:e34 | 9.20 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e35 | 9.20 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e36 | 9.25 | TRACK_APPEARED | A | track_012 | radar |  |
| A:e37 | 9.25 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e38 | 9.45 | CRITICAL_TTC_START | A | track_009 | radar |  |
| A:e39 | 10.05 | CRITICAL_TTC_START | A | track_004 | radar |  |
| A:e40 | 10.25 | TRACK_LOST | A | track_004 | radar |  |
| A:e41 | 10.70 | TRACK_LOST | A | track_009 | radar |  |
| A:e42 | 12.00 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e43 | 12.25 | TRACK_LOST | A | track_012 | radar |  |
| A:e44 | 12.75 | TRACK_LOST | A | track_011 | radar |  |
| A:e45 | 13.35 | TRACK_LOST | A | track_006 | radar |  |
| A:e46 | 14.50 | TRACK_LOST | A | track_008 | radar |  |
| A:e47 | 14.65 | TRACK_LOST | A | track_010 | radar |  |
| A:e48 | 15.55 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e49 | 15.75 | TRACK_LOST | A | track_005 | radar |  |
| A:e50 | 16.30 | TRACK_LOST | A | track_007 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e19
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e20 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e22 --PRECEDES--> A:e27
    A:e22 --PRECEDES--> A:e28
    A:e22 --PRECEDES--> A:e29
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e23 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e29
    A:e24 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e28
    A:e24 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e31
    A:e27 --PRECEDES--> A:e30
    A:e27 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e37
    A:e33 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e41 --PRECEDES--> A:e42
    A:e42 --PRECEDES--> A:e43
    A:e43 --PRECEDES--> A:e44
    A:e44 --PRECEDES--> A:e45
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e49 --PRECEDES--> A:e50
    A:e14 --SAME_TRACK--> A:e16
    A:e15 --SAME_TRACK--> A:e17
    A:e18 --SAME_TRACK--> A:e19
    A:e20 --SAME_TRACK--> A:e21
    A:e22 --SAME_TRACK--> A:e24
    A:e23 --SAME_TRACK--> A:e25
    A:e26 --SAME_TRACK--> A:e28
    A:e27 --SAME_TRACK--> A:e29
    A:e30 --SAME_TRACK--> A:e31
    A:e32 --SAME_TRACK--> A:e34
    A:e33 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e37
    A:e30 --SAME_TRACK--> A:e38
    A:e20 --SAME_TRACK--> A:e39
    A:e20 --SAME_TRACK--> A:e40
    A:e30 --SAME_TRACK--> A:e41
    A:e14 --SAME_TRACK--> A:e42
    A:e36 --SAME_TRACK--> A:e43
    A:e33 --SAME_TRACK--> A:e44
    A:e26 --SAME_TRACK--> A:e45
    A:e27 --SAME_TRACK--> A:e46
    A:e32 --SAME_TRACK--> A:e47
    A:e14 --SAME_TRACK--> A:e48
    A:e22 --SAME_TRACK--> A:e49
    A:e23 --SAME_TRACK--> A:e50
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign VISIBLE, known, relevant to the path | 2.20 |
| 2.65 | A:e04 BRAKE_START<br>A:e05 HARD_BRAKE_START | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path | 2.60 |
| 3.40 | A:e06 MOVING_END<br>A:e07 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path | 3.30 |
| 6.45 | A:e08 HARD_BRAKE_END<br>A:e09 BRAKE_END<br>A:e10 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path | 6.40 |
| 6.80 | A:e11 STOP_END<br>A:e12 MOVING_START | ego: STOP, STRONG_THROTTLE<br>sign-0: STOP sign not visible, known, relevant to the path | 6.70 |
| 7.80 | A:e13 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>sign-0: STOP sign not visible, known, relevant to the path | 7.70 |
| 8.85 | A:e14 TRACK_APPEARED track_001<br>A:e15 TRACK_APPEARED track_002<br>A:e16 CLOSING_START track_001<br>A:e17 CLOSING_START track_002 | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path | 8.80 |
| 8.95 | A:e18 TRACK_APPEARED track_003<br>A:e19 CLOSING_START track_003 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 8.90 |
| 9.00 | A:e20 TRACK_APPEARED track_004<br>A:e21 CLOSING_START track_004 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 8.90 |
| 9.05 | A:e22 TRACK_APPEARED track_005<br>A:e23 TRACK_APPEARED track_007<br>A:e24 CLOSING_START track_005<br>A:e25 CLOSING_START track_007 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.00 |
| 9.10 | A:e26 TRACK_APPEARED track_006<br>A:e27 TRACK_APPEARED track_008<br>A:e28 CLOSING_START track_006<br>A:e29 CLOSING_START track_008 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.00 |
| 9.15 | A:e30 TRACK_APPEARED track_009<br>A:e31 CLOSING_START track_009 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.10 |
| 9.20 | A:e32 TRACK_APPEARED track_010<br>A:e33 TRACK_APPEARED track_011<br>A:e34 CLOSING_START track_010<br>A:e35 CLOSING_START track_011 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.10 |
| 9.25 | A:e36 TRACK_APPEARED track_012<br>A:e37 CLOSING_START track_012 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.20 |
| 9.45 | A:e38 CRITICAL_TTC_START track_009 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 9.40 |
| 10.05 | A:e39 CRITICAL_TTC_START track_004 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 10.00 |
| 10.25 | A:e40 TRACK_LOST track_004 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING, CRITICAL_TTC<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 10.20 |
| 10.70 | A:e41 TRACK_LOST track_009 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004<br>sign-0: STOP sign not visible, known, relevant to the path | 10.60 |
| 12.00 | A:e42 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009<br>sign-0: STOP sign not visible, known, relevant to the path | 11.90 |
| 12.25 | A:e43 TRACK_LOST track_012 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009<br>sign-0: STOP sign not visible, known, relevant to the path | 12.20 |
| 12.75 | A:e44 TRACK_LOST track_011 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 12.70 |
| 13.35 | A:e45 TRACK_LOST track_006 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 13.30 |
| 14.50 | A:e46 TRACK_LOST track_008 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 14.40 |
| 14.65 | A:e47 TRACK_LOST track_010 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 14.60 |
| 15.55 | A:e48 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 15.50 |
| 15.75 | A:e49 TRACK_LOST track_005 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 15.70 |
| 16.30 | A:e50 TRACK_LOST track_007 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_005, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path | 16.20 |

## States still active when observation ended

- MOVING, since A:e12 (t = 6.80 s)
- CLOSING of track_001, since A:e16 (t = 8.85 s)
- CLOSING of track_002, since A:e17 (t = 8.85 s)
- CLOSING of track_003, since A:e19 (t = 8.95 s)
- CLOSING of track_004, since A:e21 (t = 9.00 s); the track was lost at 10.25 s
- CLOSING of track_005, since A:e24 (t = 9.05 s); the track was lost at 15.75 s
- CLOSING of track_007, since A:e25 (t = 9.05 s); the track was lost at 16.30 s
- CLOSING of track_006, since A:e28 (t = 9.10 s); the track was lost at 13.35 s
- CLOSING of track_008, since A:e29 (t = 9.10 s); the track was lost at 14.50 s
- CLOSING of track_009, since A:e31 (t = 9.15 s); the track was lost at 10.70 s
- CLOSING of track_010, since A:e34 (t = 9.20 s); the track was lost at 14.65 s
- CLOSING of track_011, since A:e35 (t = 9.20 s); the track was lost at 12.75 s
- CLOSING of track_012, since A:e37 (t = 9.25 s); the track was lost at 12.25 s
- CRITICAL_TTC of track_009, since A:e38 (t = 9.45 s); the track was lost at 10.70 s
- CRITICAL_TTC of track_004, since A:e39 (t = 10.05 s); the track was lost at 10.25 s
- EGO_PATH of track_001, since A:e42 (t = 12.00 s)
- PREDICTED_PATH_CONFLICT of track_001, since A:e48 (t = 15.55 s)

## Tracks lost

- track_004 at 10.25 s (A:e40): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 10.70 s (A:e41): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 12.25 s (A:e43): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 12.75 s (A:e44): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 13.35 s (A:e45): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 14.50 s (A:e46): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 14.65 s (A:e47): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 15.75 s (A:e49): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 16.30 s (A:e50): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 8.85 | 16.45 | 149 | 87.0 m / -58 deg | 24.68 m (16.45) | 24.7 m / +0 deg | 1.9 m/s |
| track_002 | 8.85 | 16.45 | 146 | 89.5 m / -60 deg | 27.70 m (16.45) | 27.7 m / -7 deg | 3.2 m/s |
| track_003 | 8.95 | 16.45 | 139 | 90.9 m / -59 deg | 30.83 m (16.45) | 30.8 m / -15 deg | 1.7 m/s |
| track_004 | 9.00 | 10.25 | 26 | 11.2 m / +43 deg | 7.75 m (10.25) | 7.8 m / +46 deg | 16.4 m/s |
| track_005 | 9.05 | 15.75 | 126 | 57.5 m / -60 deg | 11.32 m (15.75) | 11.3 m / -60 deg | 5.4 m/s |
| track_006 | 9.10 | 13.35 | 83 | 43.0 m / -59 deg | 13.15 m (13.35) | 13.2 m / -60 deg | 2.4 m/s |
| track_007 | 9.05 | 16.30 | 131 | 62.4 m / -59 deg | 11.56 m (16.30) | 11.6 m / -60 deg | 4.3 m/s |
| track_008 | 9.10 | 14.50 | 105 | 47.2 m / -58 deg | 11.23 m (14.50) | 11.2 m / -60 deg | 5.2 m/s |
| track_009 | 9.15 | 10.70 | 32 | 16.3 m / -60 deg | 6.03 m (10.70) | 6.0 m / -62 deg | 2.3 m/s |
| track_010 | 9.20 | 14.65 | 108 | 51.0 m / -51 deg | 12.70 m (14.65) | 12.7 m / -60 deg | 2.2 m/s |
| track_011 | 9.20 | 12.75 | 71 | 37.0 m / -55 deg | 13.10 m (12.75) | 13.1 m / -59 deg | 2.3 m/s |
| track_012 | 9.25 | 12.25 | 61 | 31.5 m / -56 deg | 12.46 m (12.25) | 12.5 m / -60 deg | 3.1 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: A started braking.
- t = 2.65 s: A started braking hard.
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 6.45 s: A stopped braking hard.
- t = 6.45 s: A released the brake.
- t = 6.45 s: A started applying strong throttle.
- t = 6.80 s: A left its stop.
- t = 6.80 s: A started moving.
- t = 7.80 s: A stopped applying strong throttle.
- t = 8.85 s: A's radar started tracking track_001.
- t = 8.85 s: A's radar started tracking track_002.
- t = 8.85 s: A observed track_001 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_002 start closing in (already the case when first observed).
- t = 8.95 s: A's radar started tracking track_003.
- t = 8.95 s: A observed track_003 start closing in (already the case when first observed).
- t = 9.00 s: A's radar started tracking track_004.
- t = 9.00 s: A observed track_004 start closing in (already the case when first observed).
- t = 9.05 s: A's radar started tracking track_005.
- t = 9.05 s: A's radar started tracking track_007.
- t = 9.05 s: A observed track_005 start closing in (already the case when first observed).
- t = 9.05 s: A observed track_007 start closing in (already the case when first observed).
- t = 9.10 s: A's radar started tracking track_006.
- t = 9.10 s: A's radar started tracking track_008.
- t = 9.10 s: A observed track_006 start closing in (already the case when first observed).
- t = 9.10 s: A observed track_008 start closing in (already the case when first observed).
- t = 9.15 s: A's radar started tracking track_009.
- t = 9.15 s: A observed track_009 start closing in (already the case when first observed).
- t = 9.20 s: A's radar started tracking track_010.
- t = 9.20 s: A's radar started tracking track_011.
- t = 9.20 s: A observed track_010 start closing in (already the case when first observed).
- t = 9.20 s: A observed track_011 start closing in (already the case when first observed).
- t = 9.25 s: A's radar started tracking track_012.
- t = 9.25 s: A observed track_012 start closing in (already the case when first observed).
- t = 9.45 s: A's time-to-contact with track_009 became critical.
- t = 10.05 s: A's time-to-contact with track_004 became critical.
- t = 10.25 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 10.70 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 12.00 s: A observed track_001 enter its forward path corridor.
- t = 12.25 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 12.75 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 13.35 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 14.50 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 14.65 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 15.55 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 15.75 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 16.30 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
