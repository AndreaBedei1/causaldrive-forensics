# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 116.97939620912075 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 17 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 64; edges: 303 (PRECEDES 266, SAME_TRACK 37)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.85 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.20 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e04 | 1.20 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 1.60 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e06 | 1.65 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 2.40 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e08 | 2.85 | TRACK_LOST | B | track_001 | radar |  |
| B:e09 | 3.70 | COLLISION | B | - | collision_sensor | peak_impulse=6116.26 |
| B:e10 | 3.70 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e11 | 3.70 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e12 | 3.70 | TRACK_APPEARED | B | track_003 | radar |  |
| B:e13 | 3.70 | TRACK_APPEARED | B | track_004 | radar |  |
| B:e14 | 3.70 | TRACK_APPEARED | B | track_005 | radar |  |
| B:e15 | 3.70 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e16 | 3.70 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e17 | 3.70 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e18 | 3.70 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e19 | 3.75 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e20 | 3.75 | BRAKE_START | B | - | controls |  |
| B:e21 | 3.75 | HARD_BRAKE_START | B | - | controls |  |
| B:e22 | 3.75 | TRACK_APPEARED | B | track_006 | radar |  |
| B:e23 | 3.75 | TRACK_APPEARED | B | track_007 | radar |  |
| B:e24 | 3.75 | TRACK_APPEARED | B | track_008 | radar |  |
| B:e25 | 3.75 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e26 | 3.75 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e27 | 3.75 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e28 | 3.80 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e29 | 3.80 | TRACK_APPEARED | B | track_010 | radar |  |
| B:e30 | 3.80 | EGO_PATH_ENTRY | B | track_006 | radar |  |
| B:e31 | 3.85 | EGO_PATH_EXIT | B | track_006 | radar |  |
| B:e32 | 3.85 | TRACK_APPEARED | B | track_009 | radar |  |
| B:e33 | 3.85 | TRACK_APPEARED | B | track_011 | radar |  |
| B:e34 | 3.85 | TRACK_APPEARED | B | track_013 | radar |  |
| B:e35 | 3.85 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e36 | 3.90 | EGO_PATH_EXIT | B | track_003 | radar |  |
| B:e37 | 3.90 | TRACK_APPEARED | B | track_012 | radar |  |
| B:e38 | 3.95 | TRACK_APPEARED | B | track_014 | radar |  |
| B:e39 | 3.95 | TRACK_APPEARED | B | track_015 | radar |  |
| B:e40 | 3.95 | CLOSING_START | B | track_012 | radar |  |
| B:e41 | 3.95 | TRACK_LOST | B | track_002 | radar |  |
| B:e42 | 4.00 | CLOSING_END | B | track_003 | radar |  |
| B:e43 | 4.00 | CLOSING_END | B | track_004 | radar |  |
| B:e44 | 4.00 | CLOSING_END | B | track_005 | radar |  |
| B:e45 | 4.00 | TRACK_APPEARED | B | track_016 | radar |  |
| B:e46 | 4.00 | TRACK_APPEARED | B | track_017 | radar |  |
| B:e47 | 4.00 | CLOSING_START | B | track_014 | radar |  |
| B:e48 | 4.00 | CLOSING_START | B | track_015 | radar |  |
| B:e49 | 4.00 | TRACK_LOST | B | track_003 | radar |  |
| B:e50 | 4.00 | TRACK_LOST | B | track_006 | radar |  |
| B:e51 | 4.05 | CLOSING_END | B | track_007 | radar |  |
| B:e52 | 4.05 | CLOSING_END | B | track_008 | radar |  |
| B:e53 | 4.05 | EGO_PATH_ENTRY | B | track_013 | radar |  |
| B:e54 | 4.05 | TRACK_LOST | B | track_004 | radar |  |
| B:e55 | 4.05 | TRACK_LOST | B | track_005 | radar |  |
| B:e56 | 4.10 | EGO_PATH_EXIT | B | track_013 | radar |  |
| B:e57 | 4.20 | EGO_PATH_ENTRY | B | track_012 | radar |  |
| B:e58 | 4.25 | CLOSING_END | B | track_012 | radar |  |
| B:e59 | 4.30 | CLOSING_END | B | track_014 | radar |  |
| B:e60 | 4.30 | CLOSING_END | B | track_015 | radar |  |
| B:e61 | 4.30 | MOVING_END | B | - | ego |  |
| B:e62 | 4.30 | STOP_START | B | - | ego |  |
| B:e63 | 4.30 | TRACK_LOST | B | track_017 | radar |  |
| B:e64 | 4.45 | TRACK_LOST | B | track_008 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e08 --PRECEDES--> B:e13
    B:e08 --PRECEDES--> B:e14
    B:e08 --PRECEDES--> B:e15
    B:e08 --PRECEDES--> B:e16
    B:e08 --PRECEDES--> B:e17
    B:e08 --PRECEDES--> B:e18
    B:e09 --PRECEDES--> B:e19
    B:e09 --PRECEDES--> B:e20
    B:e09 --PRECEDES--> B:e21
    B:e09 --PRECEDES--> B:e22
    B:e09 --PRECEDES--> B:e23
    B:e09 --PRECEDES--> B:e24
    B:e09 --PRECEDES--> B:e25
    B:e09 --PRECEDES--> B:e26
    B:e09 --PRECEDES--> B:e27
    B:e10 --PRECEDES--> B:e19
    B:e10 --PRECEDES--> B:e20
    B:e10 --PRECEDES--> B:e21
    B:e10 --PRECEDES--> B:e22
    B:e10 --PRECEDES--> B:e23
    B:e10 --PRECEDES--> B:e24
    B:e10 --PRECEDES--> B:e25
    B:e10 --PRECEDES--> B:e26
    B:e10 --PRECEDES--> B:e27
    B:e11 --PRECEDES--> B:e19
    B:e11 --PRECEDES--> B:e20
    B:e11 --PRECEDES--> B:e21
    B:e11 --PRECEDES--> B:e22
    B:e11 --PRECEDES--> B:e23
    B:e11 --PRECEDES--> B:e24
    B:e11 --PRECEDES--> B:e25
    B:e11 --PRECEDES--> B:e26
    B:e11 --PRECEDES--> B:e27
    B:e12 --PRECEDES--> B:e19
    B:e12 --PRECEDES--> B:e20
    B:e12 --PRECEDES--> B:e21
    B:e12 --PRECEDES--> B:e22
    B:e12 --PRECEDES--> B:e23
    B:e12 --PRECEDES--> B:e24
    B:e12 --PRECEDES--> B:e25
    B:e12 --PRECEDES--> B:e26
    B:e12 --PRECEDES--> B:e27
    B:e13 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e20
    B:e13 --PRECEDES--> B:e21
    B:e13 --PRECEDES--> B:e22
    B:e13 --PRECEDES--> B:e23
    B:e13 --PRECEDES--> B:e24
    B:e13 --PRECEDES--> B:e25
    B:e13 --PRECEDES--> B:e26
    B:e13 --PRECEDES--> B:e27
    B:e14 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e20
    B:e14 --PRECEDES--> B:e21
    B:e14 --PRECEDES--> B:e22
    B:e14 --PRECEDES--> B:e23
    B:e14 --PRECEDES--> B:e24
    B:e14 --PRECEDES--> B:e25
    B:e14 --PRECEDES--> B:e26
    B:e14 --PRECEDES--> B:e27
    B:e15 --PRECEDES--> B:e19
    B:e15 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e22
    B:e15 --PRECEDES--> B:e23
    B:e15 --PRECEDES--> B:e24
    B:e15 --PRECEDES--> B:e25
    B:e15 --PRECEDES--> B:e26
    B:e15 --PRECEDES--> B:e27
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e23
    B:e16 --PRECEDES--> B:e24
    B:e16 --PRECEDES--> B:e25
    B:e16 --PRECEDES--> B:e26
    B:e16 --PRECEDES--> B:e27
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e17 --PRECEDES--> B:e23
    B:e17 --PRECEDES--> B:e24
    B:e17 --PRECEDES--> B:e25
    B:e17 --PRECEDES--> B:e26
    B:e17 --PRECEDES--> B:e27
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e23
    B:e18 --PRECEDES--> B:e24
    B:e18 --PRECEDES--> B:e25
    B:e18 --PRECEDES--> B:e26
    B:e18 --PRECEDES--> B:e27
    B:e19 --PRECEDES--> B:e28
    B:e19 --PRECEDES--> B:e29
    B:e19 --PRECEDES--> B:e30
    B:e20 --PRECEDES--> B:e28
    B:e20 --PRECEDES--> B:e29
    B:e20 --PRECEDES--> B:e30
    B:e21 --PRECEDES--> B:e28
    B:e21 --PRECEDES--> B:e29
    B:e21 --PRECEDES--> B:e30
    B:e22 --PRECEDES--> B:e28
    B:e22 --PRECEDES--> B:e29
    B:e22 --PRECEDES--> B:e30
    B:e23 --PRECEDES--> B:e28
    B:e23 --PRECEDES--> B:e29
    B:e23 --PRECEDES--> B:e30
    B:e24 --PRECEDES--> B:e28
    B:e24 --PRECEDES--> B:e29
    B:e24 --PRECEDES--> B:e30
    B:e25 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e29
    B:e25 --PRECEDES--> B:e30
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e28 --PRECEDES--> B:e32
    B:e28 --PRECEDES--> B:e33
    B:e28 --PRECEDES--> B:e34
    B:e28 --PRECEDES--> B:e35
    B:e29 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e32
    B:e29 --PRECEDES--> B:e33
    B:e29 --PRECEDES--> B:e34
    B:e29 --PRECEDES--> B:e35
    B:e30 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e33
    B:e30 --PRECEDES--> B:e34
    B:e30 --PRECEDES--> B:e35
    B:e31 --PRECEDES--> B:e36
    B:e31 --PRECEDES--> B:e37
    B:e32 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e37
    B:e33 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e37
    B:e34 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e38
    B:e36 --PRECEDES--> B:e39
    B:e36 --PRECEDES--> B:e40
    B:e36 --PRECEDES--> B:e41
    B:e37 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e37 --PRECEDES--> B:e40
    B:e37 --PRECEDES--> B:e41
    B:e38 --PRECEDES--> B:e42
    B:e38 --PRECEDES--> B:e43
    B:e38 --PRECEDES--> B:e44
    B:e38 --PRECEDES--> B:e45
    B:e38 --PRECEDES--> B:e46
    B:e38 --PRECEDES--> B:e47
    B:e38 --PRECEDES--> B:e48
    B:e38 --PRECEDES--> B:e49
    B:e38 --PRECEDES--> B:e50
    B:e39 --PRECEDES--> B:e42
    B:e39 --PRECEDES--> B:e43
    B:e39 --PRECEDES--> B:e44
    B:e39 --PRECEDES--> B:e45
    B:e39 --PRECEDES--> B:e46
    B:e39 --PRECEDES--> B:e47
    B:e39 --PRECEDES--> B:e48
    B:e39 --PRECEDES--> B:e49
    B:e39 --PRECEDES--> B:e50
    B:e40 --PRECEDES--> B:e42
    B:e40 --PRECEDES--> B:e43
    B:e40 --PRECEDES--> B:e44
    B:e40 --PRECEDES--> B:e45
    B:e40 --PRECEDES--> B:e46
    B:e40 --PRECEDES--> B:e47
    B:e40 --PRECEDES--> B:e48
    B:e40 --PRECEDES--> B:e49
    B:e40 --PRECEDES--> B:e50
    B:e41 --PRECEDES--> B:e42
    B:e41 --PRECEDES--> B:e43
    B:e41 --PRECEDES--> B:e44
    B:e41 --PRECEDES--> B:e45
    B:e41 --PRECEDES--> B:e46
    B:e41 --PRECEDES--> B:e47
    B:e41 --PRECEDES--> B:e48
    B:e41 --PRECEDES--> B:e49
    B:e41 --PRECEDES--> B:e50
    B:e42 --PRECEDES--> B:e51
    B:e42 --PRECEDES--> B:e52
    B:e42 --PRECEDES--> B:e53
    B:e42 --PRECEDES--> B:e54
    B:e42 --PRECEDES--> B:e55
    B:e43 --PRECEDES--> B:e51
    B:e43 --PRECEDES--> B:e52
    B:e43 --PRECEDES--> B:e53
    B:e43 --PRECEDES--> B:e54
    B:e43 --PRECEDES--> B:e55
    B:e44 --PRECEDES--> B:e51
    B:e44 --PRECEDES--> B:e52
    B:e44 --PRECEDES--> B:e53
    B:e44 --PRECEDES--> B:e54
    B:e44 --PRECEDES--> B:e55
    B:e45 --PRECEDES--> B:e51
    B:e45 --PRECEDES--> B:e52
    B:e45 --PRECEDES--> B:e53
    B:e45 --PRECEDES--> B:e54
    B:e45 --PRECEDES--> B:e55
    B:e46 --PRECEDES--> B:e51
    B:e46 --PRECEDES--> B:e52
    B:e46 --PRECEDES--> B:e53
    B:e46 --PRECEDES--> B:e54
    B:e46 --PRECEDES--> B:e55
    B:e47 --PRECEDES--> B:e51
    B:e47 --PRECEDES--> B:e52
    B:e47 --PRECEDES--> B:e53
    B:e47 --PRECEDES--> B:e54
    B:e47 --PRECEDES--> B:e55
    B:e48 --PRECEDES--> B:e51
    B:e48 --PRECEDES--> B:e52
    B:e48 --PRECEDES--> B:e53
    B:e48 --PRECEDES--> B:e54
    B:e48 --PRECEDES--> B:e55
    B:e49 --PRECEDES--> B:e51
    B:e49 --PRECEDES--> B:e52
    B:e49 --PRECEDES--> B:e53
    B:e49 --PRECEDES--> B:e54
    B:e49 --PRECEDES--> B:e55
    B:e50 --PRECEDES--> B:e51
    B:e50 --PRECEDES--> B:e52
    B:e50 --PRECEDES--> B:e53
    B:e50 --PRECEDES--> B:e54
    B:e50 --PRECEDES--> B:e55
    B:e51 --PRECEDES--> B:e56
    B:e52 --PRECEDES--> B:e56
    B:e53 --PRECEDES--> B:e56
    B:e54 --PRECEDES--> B:e56
    B:e55 --PRECEDES--> B:e56
    B:e56 --PRECEDES--> B:e57
    B:e57 --PRECEDES--> B:e58
    B:e58 --PRECEDES--> B:e59
    B:e58 --PRECEDES--> B:e60
    B:e58 --PRECEDES--> B:e61
    B:e58 --PRECEDES--> B:e62
    B:e58 --PRECEDES--> B:e63
    B:e59 --PRECEDES--> B:e64
    B:e60 --PRECEDES--> B:e64
    B:e61 --PRECEDES--> B:e64
    B:e62 --PRECEDES--> B:e64
    B:e63 --PRECEDES--> B:e64
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e08
    B:e11 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e13 --SAME_TRACK--> B:e17
    B:e14 --SAME_TRACK--> B:e18
    B:e11 --SAME_TRACK--> B:e25
    B:e23 --SAME_TRACK--> B:e26
    B:e24 --SAME_TRACK--> B:e27
    B:e11 --SAME_TRACK--> B:e28
    B:e22 --SAME_TRACK--> B:e30
    B:e22 --SAME_TRACK--> B:e31
    B:e12 --SAME_TRACK--> B:e35
    B:e12 --SAME_TRACK--> B:e36
    B:e37 --SAME_TRACK--> B:e40
    B:e11 --SAME_TRACK--> B:e41
    B:e12 --SAME_TRACK--> B:e42
    B:e13 --SAME_TRACK--> B:e43
    B:e14 --SAME_TRACK--> B:e44
    B:e38 --SAME_TRACK--> B:e47
    B:e39 --SAME_TRACK--> B:e48
    B:e12 --SAME_TRACK--> B:e49
    B:e22 --SAME_TRACK--> B:e50
    B:e23 --SAME_TRACK--> B:e51
    B:e24 --SAME_TRACK--> B:e52
    B:e34 --SAME_TRACK--> B:e53
    B:e13 --SAME_TRACK--> B:e54
    B:e14 --SAME_TRACK--> B:e55
    B:e34 --SAME_TRACK--> B:e56
    B:e37 --SAME_TRACK--> B:e57
    B:e37 --SAME_TRACK--> B:e58
    B:e38 --SAME_TRACK--> B:e59
    B:e39 --SAME_TRACK--> B:e60
    B:e46 --SAME_TRACK--> B:e63
    B:e24 --SAME_TRACK--> B:e64
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.85 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 0.80 |
| 1.20 | B:e03 TRACK_APPEARED track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE | 1.10 |
| 1.60 | B:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING | 1.50 |
| 1.65 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.60 |
| 2.40 | B:e07 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 2.30 |
| 2.85 | B:e08 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 2.80 |
| 3.70 | B:e09 COLLISION<br>B:e10 STRONG_THROTTLE_START<br>B:e11 TRACK_APPEARED track_002<br>B:e12 TRACK_APPEARED track_003<br>B:e13 TRACK_APPEARED track_004<br>B:e14 TRACK_APPEARED track_005<br>B:e15 CLOSING_START track_002<br>B:e16 CLOSING_START track_003<br>B:e17 CLOSING_START track_004<br>B:e18 CLOSING_START track_005 | ego: MOVING<br>lost (states UNKNOWN): track_001 | 3.60 |
| 3.75 | B:e19 STRONG_THROTTLE_END<br>B:e20 BRAKE_START<br>B:e21 HARD_BRAKE_START<br>B:e22 TRACK_APPEARED track_006<br>B:e23 TRACK_APPEARED track_007<br>B:e24 TRACK_APPEARED track_008<br>B:e25 EGO_PATH_ENTRY track_002<br>B:e26 CLOSING_START track_007<br>B:e27 CLOSING_START track_008 | ego: MOVING, STRONG_THROTTLE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>lost (states UNKNOWN): track_001 | 3.70 |
| 3.80 | B:e28 EGO_PATH_EXIT track_002<br>B:e29 TRACK_APPEARED track_010<br>B:e30 EGO_PATH_ENTRY track_006 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001 | 3.70 |
| 3.85 | B:e31 EGO_PATH_EXIT track_006<br>B:e32 TRACK_APPEARED track_009<br>B:e33 TRACK_APPEARED track_011<br>B:e34 TRACK_APPEARED track_013<br>B:e35 EGO_PATH_ENTRY track_003 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: VISIBLE, IN_EGO_PATH, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE<br>lost (states UNKNOWN): track_001 | 3.80 |
| 3.90 | B:e36 EGO_PATH_EXIT track_003<br>B:e37 TRACK_APPEARED track_012 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_013: VISIBLE<br>lost (states UNKNOWN): track_001 | 3.80 |
| 3.95 | B:e38 TRACK_APPEARED track_014<br>B:e39 TRACK_APPEARED track_015<br>B:e40 CLOSING_START track_012<br>B:e41 TRACK_LOST track_002 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE<br>lost (states UNKNOWN): track_001 | 3.90 |
| 4.00 | B:e42 CLOSING_END track_003<br>B:e43 CLOSING_END track_004<br>B:e44 CLOSING_END track_005<br>B:e45 TRACK_APPEARED track_016<br>B:e46 TRACK_APPEARED track_017<br>B:e47 CLOSING_START track_014<br>B:e48 CLOSING_START track_015<br>B:e49 TRACK_LOST track_003<br>B:e50 TRACK_LOST track_006 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE<br>track_014: VISIBLE<br>track_015: VISIBLE<br>lost (states UNKNOWN): track_001, track_002 | 3.90 |
| 4.05 | B:e51 CLOSING_END track_007<br>B:e52 CLOSING_END track_008<br>B:e53 EGO_PATH_ENTRY track_013<br>B:e54 TRACK_LOST track_004<br>B:e55 TRACK_LOST track_005 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_004: VISIBLE<br>track_005: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE<br>track_017: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_006 | 4.00 |
| 4.10 | B:e56 EGO_PATH_EXIT track_013 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE, IN_EGO_PATH<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE<br>track_017: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_004, track_005, track_006 | 4.00 |
| 4.20 | B:e57 EGO_PATH_ENTRY track_012 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE<br>track_017: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_004, track_005, track_006 | 4.10 |
| 4.25 | B:e58 CLOSING_END track_012 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, CLOSING, IN_EGO_PATH<br>track_013: VISIBLE<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE<br>track_017: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_004, track_005, track_006 | 4.20 |
| 4.30 | B:e59 CLOSING_END track_014<br>B:e60 CLOSING_END track_015<br>B:e61 MOVING_END<br>B:e62 STOP_START<br>B:e63 TRACK_LOST track_017 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, IN_EGO_PATH<br>track_013: VISIBLE<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE<br>track_017: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_004, track_005, track_006 | 4.20 |
| 4.45 | B:e64 TRACK_LOST track_008 | ego: STOP, BRAKE, HARD_BRAKE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_011: VISIBLE<br>track_012: VISIBLE, IN_EGO_PATH<br>track_013: VISIBLE<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>lost (states UNKNOWN): track_001, track_002, track_003, track_004, track_005, track_006, track_017 | 4.40 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 1.20 s); the track was lost at 2.85 s
- CRITICAL_TTC of track_001, since B:e06 (t = 1.65 s); the track was lost at 2.85 s
- PREDICTED_PATH_CONFLICT of track_001, since B:e07 (t = 2.40 s); the track was lost at 2.85 s
- CLOSING of track_002, since B:e15 (t = 3.70 s); the track was lost at 3.95 s
- BRAKE, since B:e20 (t = 3.75 s)
- HARD_BRAKE, since B:e21 (t = 3.75 s)
- EGO_PATH of track_012, since B:e57 (t = 4.20 s)
- STOP, since B:e62 (t = 4.30 s)

## Tracks lost

- track_001 at 2.85 s (B:e08): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 3.95 s (B:e41): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 4.00 s (B:e49): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_006, track_004, track_005, track_017, track_008

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.20 | 2.85 | 34 | 37.0 m / -52 deg | 12.25 m (2.85) | 12.2 m / -59 deg | 12.4 m/s |
| track_002 | 3.70 | 3.95 | 6 | 30.5 m / -17 deg | 29.83 m (3.85) | 30.2 m / +55 deg | 5.1 m/s |
| track_003 | 3.70 | 4.00 | 7 | 29.6 m / -50 deg | 28.08 m (3.90) | 28.4 m / +45 deg | 21.7 m/s |
| track_004 | 3.70 | 4.05 | 8 | 19.9 m / -61 deg | 18.14 m (3.90) | 18.6 m / +57 deg | 24.5 m/s |
| track_005 | 3.70 | 4.05 | 7 | 30.4 m / -54 deg | 28.66 m (3.95) | 29.1 m / +50 deg | 18.4 m/s |
| track_006 | 3.75 | 4.00 | 6 | 23.5 m / -16 deg | 23.03 m (3.85) | 23.6 m / +60 deg | 13.5 m/s |
| track_007 | 3.75 | 14.45 | 210 | 36.0 m / -46 deg | 34.78 m (3.95) | 36.1 m / +53 deg | 3.9 m/s |
| track_008 | 3.75 | 4.45 | 11 | 37.4 m / -46 deg | 36.31 m (3.95) | 37.0 m / +50 deg | 3.5 m/s |
| track_009 | 3.85 | 14.45 | 212 | 33.1 m / -59 deg | 31.85 m (4.25) | 32.7 m / +12 deg | 5.1 m/s |
| track_010 | 3.80 | 14.45 | 142 | 60.2 m / -37 deg | 59.64 m (4.00) | 60.2 m / +47 deg | 2.0 m/s |
| track_011 | 3.85 | 14.45 | 210 | 52.1 m / -21 deg | 51.83 m (3.95) | 52.4 m / +50 deg | 2.1 m/s |
| track_012 | 3.90 | 14.45 | 212 | 31.6 m / -55 deg | 30.43 m (8.00) | 30.5 m / +2 deg | 4.4 m/s |
| track_013 | 3.85 | 14.45 | 169 | 57.4 m / -47 deg | 56.51 m (4.10) | 57.1 m / +24 deg | 3.9 m/s |
| track_014 | 3.95 | 14.45 | 211 | 21.9 m / -52 deg | 20.87 m (8.25) | 20.9 m / -8 deg | 3.8 m/s |
| track_015 | 3.95 | 14.45 | 202 | 33.9 m / -58 deg | 32.69 m (6.05) | 32.7 m / -12 deg | 4.6 m/s |
| track_016 | 4.00 | 14.45 | 210 | 30.3 m / -54 deg | 28.21 m (14.45) | 28.2 m / -20 deg | 3.5 m/s |
| track_017 | 4.00 | 4.30 | 7 | 4.1 m / -51 deg | 2.40 m (4.25) | 2.6 m / -88 deg | 13.7 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.85 s: B started applying strong throttle.
- t = 1.20 s: B's radar started tracking track_001.
- t = 1.20 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.60 s: B stopped applying strong throttle.
- t = 1.65 s: B's time-to-contact with track_001 became critical.
- t = 2.40 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 2.85 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.70 s: B's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: B started applying strong throttle.
- t = 3.70 s: B's radar started tracking track_002.
- t = 3.70 s: B's radar started tracking track_003.
- t = 3.70 s: B's radar started tracking track_004.
- t = 3.70 s: B's radar started tracking track_005.
- t = 3.70 s: B observed track_002 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_003 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_004 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.75 s: B stopped applying strong throttle.
- t = 3.75 s: B started braking.
- t = 3.75 s: B started braking hard.
- t = 3.75 s: B's radar started tracking track_006.
- t = 3.75 s: B's radar started tracking track_007.
- t = 3.75 s: B's radar started tracking track_008.
- t = 3.75 s: B observed track_002 enter its forward path corridor.
- t = 3.75 s: B observed track_007 start closing in (already the case when first observed).
- t = 3.75 s: B observed track_008 start closing in (already the case when first observed).
- t = 3.80 s: B observed track_002 leave its forward path corridor.
- t = 3.80 s: B's radar started tracking track_010.
- t = 3.80 s: B observed track_006 enter its forward path corridor.
- t = 3.85 s: B observed track_006 leave its forward path corridor.
- t = 3.85 s: B's radar started tracking track_009.
- t = 3.85 s: B's radar started tracking track_011.
- t = 3.85 s: B's radar started tracking track_013.
- t = 3.85 s: B observed track_003 enter its forward path corridor.
- t = 3.90 s: B observed track_003 leave its forward path corridor.
- t = 3.90 s: B's radar started tracking track_012.
- t = 3.95 s: B's radar started tracking track_014.
- t = 3.95 s: B's radar started tracking track_015.
- t = 3.95 s: B observed track_012 start closing in.
- t = 3.95 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.00 s: B observed track_003 stop closing in.
- t = 4.00 s: B observed track_004 stop closing in.
- t = 4.00 s: B observed track_005 stop closing in.
- t = 4.00 s: B's radar started tracking track_016.
- t = 4.00 s: B's radar started tracking track_017.
- t = 4.00 s: B observed track_014 start closing in.
- t = 4.00 s: B observed track_015 start closing in.
- t = 4.00 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 4.00 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 4.05 s: B observed track_007 stop closing in.
- t = 4.05 s: B observed track_008 stop closing in.
- t = 4.05 s: B observed track_013 enter its forward path corridor.
- t = 4.05 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 4.05 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 4.10 s: B observed track_013 leave its forward path corridor.
- t = 4.20 s: B observed track_012 enter its forward path corridor.
- t = 4.25 s: B observed track_012 stop closing in.
- t = 4.30 s: B observed track_014 stop closing in.
- t = 4.30 s: B observed track_015 stop closing in.
- t = 4.30 s: B stopped moving.
- t = 4.30 s: B came to a stop.
- t = 4.30 s: B's radar lost track_017 (its states are UNKNOWN from then on, not ended).
- t = 4.45 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
