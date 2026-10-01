# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 432.100672993809 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 16 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 64; edges: 238 (PRECEDES 196, SAME_TRACK 42)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.80 | BRAKE_START | B | - | controls |  |
| B:e03 | 5.65 | COLLISION | B | - | collision_sensor | peak_impulse=5215.85 |
| B:e04 | 5.65 | HARD_BRAKE_START | B | - | controls |  |
| B:e05 | 5.95 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e06 | 5.95 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e07 | 5.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e08 | 5.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e09 | 5.95 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e10 | 5.95 | CRITICAL_TTC_START | B | track_002 | radar | active_at_first_observation=True |
| B:e11 | 6.00 | TRACK_APPEARED | B | track_003 | radar |  |
| B:e12 | 6.00 | TRACK_APPEARED | B | track_004 | radar |  |
| B:e13 | 6.00 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e14 | 6.00 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e15 | 6.20 | TRACK_APPEARED | B | track_005 | radar |  |
| B:e16 | 6.20 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e17 | 6.25 | TRACK_APPEARED | B | track_006 | radar |  |
| B:e18 | 6.25 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e19 | 6.30 | TRACK_APPEARED | B | track_007 | radar |  |
| B:e20 | 6.30 | TRACK_APPEARED | B | track_008 | radar |  |
| B:e21 | 6.30 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e22 | 6.30 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e23 | 6.35 | TRACK_APPEARED | B | track_009 | radar |  |
| B:e24 | 6.35 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e25 | 6.40 | TRACK_APPEARED | B | track_010 | radar |  |
| B:e26 | 6.40 | CLOSING_START | B | track_010 | radar | active_at_first_observation=True |
| B:e27 | 6.45 | TRACK_APPEARED | B | track_011 | radar |  |
| B:e28 | 6.45 | CLOSING_START | B | track_011 | radar | active_at_first_observation=True |
| B:e29 | 6.45 | TRACK_LOST | B | track_006 | radar |  |
| B:e30 | 6.50 | TRACK_APPEARED | B | track_012 | radar |  |
| B:e31 | 6.50 | CLOSING_START | B | track_012 | radar | active_at_first_observation=True |
| B:e32 | 6.55 | TRACK_APPEARED | B | track_013 | radar |  |
| B:e33 | 6.55 | TRACK_APPEARED | B | track_014 | radar |  |
| B:e34 | 6.55 | CLOSING_START | B | track_013 | radar | active_at_first_observation=True |
| B:e35 | 6.55 | CLOSING_START | B | track_014 | radar | active_at_first_observation=True |
| B:e36 | 6.55 | TRACK_LOST | B | track_008 | radar |  |
| B:e37 | 6.60 | TRACK_APPEARED | B | track_015 | radar |  |
| B:e38 | 6.60 | TRACK_APPEARED | B | track_016 | radar |  |
| B:e39 | 6.60 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e40 | 6.60 | EGO_PATH_ENTRY | B | track_004 | radar |  |
| B:e41 | 6.60 | CLOSING_START | B | track_015 | radar | active_at_first_observation=True |
| B:e42 | 6.60 | CLOSING_START | B | track_016 | radar | active_at_first_observation=True |
| B:e43 | 6.60 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e44 | 6.60 | TRACK_LOST | B | track_007 | radar |  |
| B:e45 | 6.60 | TRACK_LOST | B | track_009 | radar |  |
| B:e46 | 6.65 | TRACK_LOST | B | track_010 | radar |  |
| B:e47 | 6.70 | EGO_PATH_EXIT | B | track_004 | radar |  |
| B:e48 | 6.70 | TRACK_LOST | B | track_011 | radar |  |
| B:e49 | 6.75 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e50 | 6.75 | TRACK_LOST | B | track_012 | radar |  |
| B:e51 | 6.80 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e52 | 6.80 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e53 | 6.80 | TRACK_LOST | B | track_013 | radar |  |
| B:e54 | 6.90 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e55 | 6.90 | CLOSING_END | B | track_001 | radar |  |
| B:e56 | 6.90 | CLOSING_END | B | track_003 | radar |  |
| B:e57 | 6.90 | CLOSING_END | B | track_004 | radar |  |
| B:e58 | 6.90 | CLOSING_END | B | track_005 | radar |  |
| B:e59 | 6.90 | CLOSING_END | B | track_014 | radar |  |
| B:e60 | 6.90 | CLOSING_END | B | track_015 | radar |  |
| B:e61 | 6.90 | MOVING_END | B | - | ego |  |
| B:e62 | 6.90 | STOP_START | B | - | ego |  |
| B:e63 | 6.95 | CLOSING_END | B | track_016 | radar |  |
| B:e64 | 7.00 | CLOSING_END | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e10
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e10
    B:e05 --PRECEDES--> B:e11
    B:e05 --PRECEDES--> B:e12
    B:e05 --PRECEDES--> B:e13
    B:e05 --PRECEDES--> B:e14
    B:e06 --PRECEDES--> B:e11
    B:e06 --PRECEDES--> B:e12
    B:e06 --PRECEDES--> B:e13
    B:e06 --PRECEDES--> B:e14
    B:e07 --PRECEDES--> B:e11
    B:e07 --PRECEDES--> B:e12
    B:e07 --PRECEDES--> B:e13
    B:e07 --PRECEDES--> B:e14
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e08 --PRECEDES--> B:e13
    B:e08 --PRECEDES--> B:e14
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e09 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e19 --PRECEDES--> B:e24
    B:e20 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e24
    B:e21 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e31
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e33
    B:e30 --PRECEDES--> B:e34
    B:e30 --PRECEDES--> B:e35
    B:e30 --PRECEDES--> B:e36
    B:e31 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e33
    B:e31 --PRECEDES--> B:e34
    B:e31 --PRECEDES--> B:e35
    B:e31 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e37
    B:e32 --PRECEDES--> B:e38
    B:e32 --PRECEDES--> B:e39
    B:e32 --PRECEDES--> B:e40
    B:e32 --PRECEDES--> B:e41
    B:e32 --PRECEDES--> B:e42
    B:e32 --PRECEDES--> B:e43
    B:e32 --PRECEDES--> B:e44
    B:e32 --PRECEDES--> B:e45
    B:e33 --PRECEDES--> B:e37
    B:e33 --PRECEDES--> B:e38
    B:e33 --PRECEDES--> B:e39
    B:e33 --PRECEDES--> B:e40
    B:e33 --PRECEDES--> B:e41
    B:e33 --PRECEDES--> B:e42
    B:e33 --PRECEDES--> B:e43
    B:e33 --PRECEDES--> B:e44
    B:e33 --PRECEDES--> B:e45
    B:e34 --PRECEDES--> B:e37
    B:e34 --PRECEDES--> B:e38
    B:e34 --PRECEDES--> B:e39
    B:e34 --PRECEDES--> B:e40
    B:e34 --PRECEDES--> B:e41
    B:e34 --PRECEDES--> B:e42
    B:e34 --PRECEDES--> B:e43
    B:e34 --PRECEDES--> B:e44
    B:e34 --PRECEDES--> B:e45
    B:e35 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e38
    B:e35 --PRECEDES--> B:e39
    B:e35 --PRECEDES--> B:e40
    B:e35 --PRECEDES--> B:e41
    B:e35 --PRECEDES--> B:e42
    B:e35 --PRECEDES--> B:e43
    B:e35 --PRECEDES--> B:e44
    B:e35 --PRECEDES--> B:e45
    B:e36 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e38
    B:e36 --PRECEDES--> B:e39
    B:e36 --PRECEDES--> B:e40
    B:e36 --PRECEDES--> B:e41
    B:e36 --PRECEDES--> B:e42
    B:e36 --PRECEDES--> B:e43
    B:e36 --PRECEDES--> B:e44
    B:e36 --PRECEDES--> B:e45
    B:e37 --PRECEDES--> B:e46
    B:e38 --PRECEDES--> B:e46
    B:e39 --PRECEDES--> B:e46
    B:e40 --PRECEDES--> B:e46
    B:e41 --PRECEDES--> B:e46
    B:e42 --PRECEDES--> B:e46
    B:e43 --PRECEDES--> B:e46
    B:e44 --PRECEDES--> B:e46
    B:e45 --PRECEDES--> B:e46
    B:e46 --PRECEDES--> B:e47
    B:e46 --PRECEDES--> B:e48
    B:e47 --PRECEDES--> B:e49
    B:e47 --PRECEDES--> B:e50
    B:e48 --PRECEDES--> B:e49
    B:e48 --PRECEDES--> B:e50
    B:e49 --PRECEDES--> B:e51
    B:e49 --PRECEDES--> B:e52
    B:e49 --PRECEDES--> B:e53
    B:e50 --PRECEDES--> B:e51
    B:e50 --PRECEDES--> B:e52
    B:e50 --PRECEDES--> B:e53
    B:e51 --PRECEDES--> B:e54
    B:e51 --PRECEDES--> B:e55
    B:e51 --PRECEDES--> B:e56
    B:e51 --PRECEDES--> B:e57
    B:e51 --PRECEDES--> B:e58
    B:e51 --PRECEDES--> B:e59
    B:e51 --PRECEDES--> B:e60
    B:e51 --PRECEDES--> B:e61
    B:e51 --PRECEDES--> B:e62
    B:e52 --PRECEDES--> B:e54
    B:e52 --PRECEDES--> B:e55
    B:e52 --PRECEDES--> B:e56
    B:e52 --PRECEDES--> B:e57
    B:e52 --PRECEDES--> B:e58
    B:e52 --PRECEDES--> B:e59
    B:e52 --PRECEDES--> B:e60
    B:e52 --PRECEDES--> B:e61
    B:e52 --PRECEDES--> B:e62
    B:e53 --PRECEDES--> B:e54
    B:e53 --PRECEDES--> B:e55
    B:e53 --PRECEDES--> B:e56
    B:e53 --PRECEDES--> B:e57
    B:e53 --PRECEDES--> B:e58
    B:e53 --PRECEDES--> B:e59
    B:e53 --PRECEDES--> B:e60
    B:e53 --PRECEDES--> B:e61
    B:e53 --PRECEDES--> B:e62
    B:e54 --PRECEDES--> B:e63
    B:e55 --PRECEDES--> B:e63
    B:e56 --PRECEDES--> B:e63
    B:e57 --PRECEDES--> B:e63
    B:e58 --PRECEDES--> B:e63
    B:e59 --PRECEDES--> B:e63
    B:e60 --PRECEDES--> B:e63
    B:e61 --PRECEDES--> B:e63
    B:e62 --PRECEDES--> B:e63
    B:e63 --PRECEDES--> B:e64
    B:e05 --SAME_TRACK--> B:e07
    B:e06 --SAME_TRACK--> B:e08
    B:e05 --SAME_TRACK--> B:e09
    B:e06 --SAME_TRACK--> B:e10
    B:e11 --SAME_TRACK--> B:e13
    B:e12 --SAME_TRACK--> B:e14
    B:e15 --SAME_TRACK--> B:e16
    B:e17 --SAME_TRACK--> B:e18
    B:e19 --SAME_TRACK--> B:e21
    B:e20 --SAME_TRACK--> B:e22
    B:e23 --SAME_TRACK--> B:e24
    B:e25 --SAME_TRACK--> B:e26
    B:e27 --SAME_TRACK--> B:e28
    B:e17 --SAME_TRACK--> B:e29
    B:e30 --SAME_TRACK--> B:e31
    B:e32 --SAME_TRACK--> B:e34
    B:e33 --SAME_TRACK--> B:e35
    B:e20 --SAME_TRACK--> B:e36
    B:e05 --SAME_TRACK--> B:e39
    B:e12 --SAME_TRACK--> B:e40
    B:e37 --SAME_TRACK--> B:e41
    B:e38 --SAME_TRACK--> B:e42
    B:e05 --SAME_TRACK--> B:e43
    B:e19 --SAME_TRACK--> B:e44
    B:e23 --SAME_TRACK--> B:e45
    B:e25 --SAME_TRACK--> B:e46
    B:e12 --SAME_TRACK--> B:e47
    B:e27 --SAME_TRACK--> B:e48
    B:e06 --SAME_TRACK--> B:e49
    B:e30 --SAME_TRACK--> B:e50
    B:e05 --SAME_TRACK--> B:e51
    B:e11 --SAME_TRACK--> B:e52
    B:e32 --SAME_TRACK--> B:e53
    B:e05 --SAME_TRACK--> B:e54
    B:e05 --SAME_TRACK--> B:e55
    B:e11 --SAME_TRACK--> B:e56
    B:e12 --SAME_TRACK--> B:e57
    B:e15 --SAME_TRACK--> B:e58
    B:e33 --SAME_TRACK--> B:e59
    B:e37 --SAME_TRACK--> B:e60
    B:e38 --SAME_TRACK--> B:e63
    B:e06 --SAME_TRACK--> B:e64
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | B:e02 BRAKE_START | ego: MOVING | 0.70 |
| 5.65 | B:e03 COLLISION<br>B:e04 HARD_BRAKE_START | ego: MOVING, BRAKE | 5.60 |
| 5.95 | B:e05 TRACK_APPEARED track_001<br>B:e06 TRACK_APPEARED track_002<br>B:e07 CLOSING_START track_001<br>B:e08 CLOSING_START track_002<br>B:e09 CRITICAL_TTC_START track_001<br>B:e10 CRITICAL_TTC_START track_002 | ego: MOVING, BRAKE, HARD_BRAKE | 5.90 |
| 6.00 | B:e11 TRACK_APPEARED track_003<br>B:e12 TRACK_APPEARED track_004<br>B:e13 CLOSING_START track_003<br>B:e14 CLOSING_START track_004 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 5.90 |
| 6.20 | B:e15 TRACK_APPEARED track_005<br>B:e16 CLOSING_START track_005 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING | 6.10 |
| 6.25 | B:e17 TRACK_APPEARED track_006<br>B:e18 CLOSING_START track_006 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING | 6.20 |
| 6.30 | B:e19 TRACK_APPEARED track_007<br>B:e20 TRACK_APPEARED track_008<br>B:e21 CLOSING_START track_007<br>B:e22 CLOSING_START track_008 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 6.20 |
| 6.35 | B:e23 TRACK_APPEARED track_009<br>B:e24 CLOSING_START track_009 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 6.30 |
| 6.40 | B:e25 TRACK_APPEARED track_010<br>B:e26 CLOSING_START track_010 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 6.30 |
| 6.45 | B:e27 TRACK_APPEARED track_011<br>B:e28 CLOSING_START track_011<br>B:e29 TRACK_LOST track_006 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 6.40 |
| 6.50 | B:e30 TRACK_APPEARED track_012<br>B:e31 CLOSING_START track_012 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>lost (states UNKNOWN): track_006 | 6.40 |
| 6.55 | B:e32 TRACK_APPEARED track_013<br>B:e33 TRACK_APPEARED track_014<br>B:e34 CLOSING_START track_013<br>B:e35 CLOSING_START track_014<br>B:e36 TRACK_LOST track_008 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>lost (states UNKNOWN): track_006 | 6.50 |
| 6.60 | B:e37 TRACK_APPEARED track_015<br>B:e38 TRACK_APPEARED track_016<br>B:e39 EGO_PATH_ENTRY track_001<br>B:e40 EGO_PATH_ENTRY track_004<br>B:e41 CLOSING_START track_015<br>B:e42 CLOSING_START track_016<br>B:e43 PREDICTED_PATH_CONFLICT_START track_001<br>B:e44 TRACK_LOST track_007<br>B:e45 TRACK_LOST track_009 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_008 | 6.50 |
| 6.65 | B:e46 TRACK_LOST track_010 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING, IN_EGO_PATH<br>track_005: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009 | 6.60 |
| 6.70 | B:e47 EGO_PATH_EXIT track_004<br>B:e48 TRACK_LOST track_011 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING, IN_EGO_PATH<br>track_005: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010 | 6.60 |
| 6.75 | B:e49 CRITICAL_TTC_END track_002<br>B:e50 TRACK_LOST track_012 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010, track_011 | 6.70 |
| 6.80 | B:e51 CRITICAL_TTC_END track_001<br>B:e52 EGO_PATH_ENTRY track_003<br>B:e53 TRACK_LOST track_013 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_013: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010, track_011, track_012 | 6.70 |
| 6.90 | B:e54 PREDICTED_PATH_CONFLICT_END track_001<br>B:e55 CLOSING_END track_001<br>B:e56 CLOSING_END track_003<br>B:e57 CLOSING_END track_004<br>B:e58 CLOSING_END track_005<br>B:e59 CLOSING_END track_014<br>B:e60 CLOSING_END track_015<br>B:e61 MOVING_END<br>B:e62 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING, IN_EGO_PATH<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 6.80 |
| 6.95 | B:e63 CLOSING_END track_016 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, IN_EGO_PATH<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 6.90 |
| 7.00 | B:e64 CLOSING_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, IN_EGO_PATH<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>lost (states UNKNOWN): track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 | 6.90 |

## States still active when observation ended

- BRAKE, since B:e02 (t = 0.80 s)
- HARD_BRAKE, since B:e04 (t = 5.65 s)
- CLOSING of track_006, since B:e18 (t = 6.25 s); the track was lost at 6.45 s
- CLOSING of track_007, since B:e21 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_008, since B:e22 (t = 6.30 s); the track was lost at 6.55 s
- CLOSING of track_009, since B:e24 (t = 6.35 s); the track was lost at 6.60 s
- CLOSING of track_010, since B:e26 (t = 6.40 s); the track was lost at 6.65 s
- CLOSING of track_011, since B:e28 (t = 6.45 s); the track was lost at 6.70 s
- CLOSING of track_012, since B:e31 (t = 6.50 s); the track was lost at 6.75 s
- CLOSING of track_013, since B:e34 (t = 6.55 s); the track was lost at 6.80 s
- EGO_PATH of track_001, since B:e39 (t = 6.60 s)
- EGO_PATH of track_003, since B:e52 (t = 6.80 s)
- STOP, since B:e62 (t = 6.90 s)

## Tracks lost

- track_006 at 6.45 s (B:e29): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 6.55 s (B:e36): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 6.60 s (B:e44): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 6.60 s (B:e45): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 6.65 s (B:e46): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 6.70 s (B:e48): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 6.75 s (B:e50): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 6.80 s (B:e53): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.95 | 9.95 | 81 | 12.2 m / +49 deg | 6.00 m (6.95) | 6.0 m / -0 deg | 4.5 m/s |
| track_002 | 5.95 | 9.95 | 81 | 13.3 m / +53 deg | 6.76 m (9.95) | 6.8 m / +42 deg | 2.6 m/s |
| track_003 | 6.00 | 9.95 | 80 | 27.5 m / +56 deg | 21.96 m (6.90) | 22.2 m / -1 deg | 4.0 m/s |
| track_004 | 6.00 | 9.95 | 50 | 22.5 m / +45 deg | 16.56 m (7.00) | 16.8 m / -23 deg | 5.7 m/s |
| track_005 | 6.20 | 9.95 | 74 | 26.6 m / +59 deg | 22.62 m (7.00) | 22.7 m / +13 deg | 3.3 m/s |
| track_006 | 6.25 | 6.45 | 5 | 37.2 m / -44 deg | 36.55 m (6.45) | 36.5 m / -59 deg | 5.2 m/s |
| track_007 | 6.30 | 6.60 | 7 | 33.7 m / -39 deg | 32.78 m (6.60) | 32.8 m / -58 deg | 13.8 m/s |
| track_008 | 6.30 | 6.55 | 6 | 44.0 m / -42 deg | 43.25 m (6.55) | 43.2 m / -59 deg | 12.3 m/s |
| track_009 | 6.35 | 6.60 | 6 | 38.2 m / -39 deg | 37.54 m (6.60) | 37.5 m / -59 deg | 6.0 m/s |
| track_010 | 6.40 | 6.65 | 6 | 46.0 m / -36 deg | 45.39 m (6.65) | 45.4 m / -57 deg | 4.2 m/s |
| track_011 | 6.45 | 6.70 | 5 | 32.1 m / -34 deg | 31.60 m (6.70) | 31.6 m / -56 deg | 2.4 m/s |
| track_012 | 6.50 | 6.75 | 6 | 28.2 m / -36 deg | 27.82 m (6.70) | 27.8 m / -59 deg | 1.7 m/s |
| track_013 | 6.55 | 6.80 | 5 | 23.3 m / -38 deg | 23.08 m (6.75) | 23.1 m / -59 deg | 1.6 m/s |
| track_014 | 6.55 | 9.95 | 55 | 20.9 m / +46 deg | 19.43 m (7.05) | 19.5 m / +26 deg | 1.7 m/s |
| track_015 | 6.60 | 9.95 | 68 | 15.0 m / -35 deg | 14.31 m (9.95) | 14.3 m / -52 deg | 1.2 m/s |
| track_016 | 6.60 | 9.95 | 56 | 10.0 m / +58 deg | 8.51 m (9.95) | 8.5 m / +58 deg | 3.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.80 s: B started braking.
- t = 5.65 s: B's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.65 s: B started braking hard.
- t = 5.95 s: B's radar started tracking track_001.
- t = 5.95 s: B's radar started tracking track_002.
- t = 5.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 5.95 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 5.95 s: B's time-to-contact with track_002 became critical (already the case when first observed).
- t = 6.00 s: B's radar started tracking track_003.
- t = 6.00 s: B's radar started tracking track_004.
- t = 6.00 s: B observed track_003 start closing in (already the case when first observed).
- t = 6.00 s: B observed track_004 start closing in (already the case when first observed).
- t = 6.20 s: B's radar started tracking track_005.
- t = 6.20 s: B observed track_005 start closing in (already the case when first observed).
- t = 6.25 s: B's radar started tracking track_006.
- t = 6.25 s: B observed track_006 start closing in (already the case when first observed).
- t = 6.30 s: B's radar started tracking track_007.
- t = 6.30 s: B's radar started tracking track_008.
- t = 6.30 s: B observed track_007 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_008 start closing in (already the case when first observed).
- t = 6.35 s: B's radar started tracking track_009.
- t = 6.35 s: B observed track_009 start closing in (already the case when first observed).
- t = 6.40 s: B's radar started tracking track_010.
- t = 6.40 s: B observed track_010 start closing in (already the case when first observed).
- t = 6.45 s: B's radar started tracking track_011.
- t = 6.45 s: B observed track_011 start closing in (already the case when first observed).
- t = 6.45 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 6.50 s: B's radar started tracking track_012.
- t = 6.50 s: B observed track_012 start closing in (already the case when first observed).
- t = 6.55 s: B's radar started tracking track_013.
- t = 6.55 s: B's radar started tracking track_014.
- t = 6.55 s: B observed track_013 start closing in (already the case when first observed).
- t = 6.55 s: B observed track_014 start closing in (already the case when first observed).
- t = 6.55 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 6.60 s: B's radar started tracking track_015.
- t = 6.60 s: B's radar started tracking track_016.
- t = 6.60 s: B observed track_001 enter its forward path corridor.
- t = 6.60 s: B observed track_004 enter its forward path corridor.
- t = 6.60 s: B observed track_015 start closing in (already the case when first observed).
- t = 6.60 s: B observed track_016 start closing in (already the case when first observed).
- t = 6.60 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 6.60 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 6.60 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 6.65 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 6.70 s: B observed track_004 leave its forward path corridor.
- t = 6.70 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 6.75 s: B's time-to-contact with track_002 stopped being critical.
- t = 6.75 s: B's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 6.80 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.80 s: B observed track_003 enter its forward path corridor.
- t = 6.80 s: B's radar lost track_013 (its states are UNKNOWN from then on, not ended).
- t = 6.90 s: B stopped predicting a path conflict with track_001.
- t = 6.90 s: B observed track_001 stop closing in.
- t = 6.90 s: B observed track_003 stop closing in.
- t = 6.90 s: B observed track_004 stop closing in.
- t = 6.90 s: B observed track_005 stop closing in.
- t = 6.90 s: B observed track_014 stop closing in.
- t = 6.90 s: B observed track_015 stop closing in.
- t = 6.90 s: B stopped moving.
- t = 6.90 s: B came to a stop.
- t = 6.95 s: B observed track_016 stop closing in.
- t = 7.00 s: B observed track_002 stop closing in.
