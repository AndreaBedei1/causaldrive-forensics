# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 130.43641052767634 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 19 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 84; edges: 445 (PRECEDES 390, SAME_TRACK 55)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.85 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.20 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e04 | 1.20 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 1.60 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e06 | 1.65 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 3.35 | TRACK_LOST | B | track_001 | radar |  |
| B:e08 | 3.70 | COLLISION | B | - | collision_sensor | peak_impulse=6116.26 |
| B:e09 | 3.70 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e10 | 3.70 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e11 | 3.70 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e12 | 3.70 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e13 | 3.70 | TRACK_APPEARED_LEFT | B | track_005 | radar |  |
| B:e14 | 3.70 | TRACK_APPEARED_LEFT | B | track_007 | radar |  |
| B:e15 | 3.70 | TRACK_APPEARED_LEFT | B | track_018 | radar |  |
| B:e16 | 3.70 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e17 | 3.70 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e18 | 3.70 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e19 | 3.70 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e20 | 3.70 | CLOSING_START | B | track_018 | radar | active_at_first_observation=True |
| B:e21 | 3.75 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e22 | 3.75 | BRAKE_START | B | - | controls |  |
| B:e23 | 3.75 | HARD_BRAKE_START | B | - | controls |  |
| B:e24 | 3.75 | TRACK_APPEARED_LEFT | B | track_012 | radar |  |
| B:e25 | 3.75 | TRACK_APPEARED_RIGHT | B | track_006 | radar |  |
| B:e26 | 3.75 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e27 | 3.75 | CLOSING_START | B | track_012 | radar | active_at_first_observation=True |
| B:e28 | 3.80 | EGO_PATH_EXIT | B | track_003 | radar |  |
| B:e29 | 3.80 | TRACK_APPEARED_LEFT | B | track_008 | radar |  |
| B:e30 | 3.80 | TRACK_APPEARED_LEFT | B | track_009 | radar |  |
| B:e31 | 3.80 | TRACK_APPEARED_LEFT | B | track_010 | radar |  |
| B:e32 | 3.80 | TRACK_APPEARED_RIGHT | B | track_011 | radar |  |
| B:e33 | 3.80 | EGO_PATH_ENTRY | B | track_005 | radar |  |
| B:e34 | 3.80 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e35 | 3.85 | EGO_PATH_EXIT | B | track_005 | radar |  |
| B:e36 | 3.85 | TRACK_APPEARED_LEFT | B | track_013 | radar |  |
| B:e37 | 3.85 | TRACK_APPEARED_LEFT | B | track_014 | radar |  |
| B:e38 | 3.85 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e39 | 3.85 | CLOSING_START | B | track_008 | radar |  |
| B:e40 | 3.90 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e41 | 3.90 | TRACK_APPEARED_LEFT | B | track_015 | radar |  |
| B:e42 | 3.90 | TRACK_APPEARED_LEFT | B | track_016 | radar |  |
| B:e43 | 3.90 | TRACK_APPEARED_LEFT | B | track_017 | radar |  |
| B:e44 | 3.90 | EGO_PATH_ENTRY | B | track_018 | radar |  |
| B:e45 | 3.90 | CLOSING_START | B | track_013 | radar |  |
| B:e46 | 3.90 | CLOSING_START | B | track_014 | radar |  |
| B:e47 | 3.90 | CLOSING_START | B | track_015 | radar | active_at_first_observation=True |
| B:e48 | 3.90 | CRITICAL_TTC_START | B | track_015 | radar | active_at_first_observation=True |
| B:e49 | 3.95 | EGO_PATH_EXIT | B | track_018 | radar |  |
| B:e50 | 3.95 | CLOSING_START | B | track_016 | radar |  |
| B:e51 | 3.95 | CLOSING_START | B | track_017 | radar |  |
| B:e52 | 3.95 | TRACK_LOST | B | track_006 | radar |  |
| B:e53 | 4.00 | CLOSING_END | B | track_002 | radar |  |
| B:e54 | 4.00 | CLOSING_END | B | track_005 | radar |  |
| B:e55 | 4.00 | TRACK_APPEARED_LEFT | B | track_019 | radar |  |
| B:e56 | 4.00 | TRACK_LOST | B | track_011 | radar |  |
| B:e57 | 4.05 | CLOSING_END | B | track_004 | radar |  |
| B:e58 | 4.05 | CLOSING_END | B | track_007 | radar |  |
| B:e59 | 4.05 | CLOSING_END | B | track_012 | radar |  |
| B:e60 | 4.05 | EGO_PATH_ENTRY | B | track_009 | radar |  |
| B:e61 | 4.05 | TRACK_LOST | B | track_003 | radar |  |
| B:e62 | 4.10 | CLOSING_END | B | track_009 | radar |  |
| B:e63 | 4.10 | CLOSING_END | B | track_018 | radar |  |
| B:e64 | 4.10 | EGO_PATH_EXIT | B | track_009 | radar |  |
| B:e65 | 4.10 | EGO_PATH_ENTRY | B | track_010 | radar |  |
| B:e66 | 4.15 | CLOSING_END | B | track_008 | radar |  |
| B:e67 | 4.15 | EGO_PATH_EXIT | B | track_010 | radar |  |
| B:e68 | 4.15 | EGO_PATH_ENTRY | B | track_008 | radar |  |
| B:e69 | 4.15 | TRACK_LOST | B | track_005 | radar |  |
| B:e70 | 4.20 | CRITICAL_TTC_END | B | track_015 | radar |  |
| B:e71 | 4.25 | CLOSING_END | B | track_013 | radar |  |
| B:e72 | 4.25 | CLOSING_END | B | track_015 | radar |  |
| B:e73 | 4.25 | EGO_PATH_EXIT | B | track_008 | radar |  |
| B:e74 | 4.25 | EGO_PATH_ENTRY | B | track_013 | radar |  |
| B:e75 | 4.25 | TRACK_LOST | B | track_018 | radar |  |
| B:e76 | 4.30 | CLOSING_END | B | track_014 | radar |  |
| B:e77 | 4.30 | CLOSING_END | B | track_016 | radar |  |
| B:e78 | 4.30 | CLOSING_END | B | track_017 | radar |  |
| B:e79 | 4.30 | MOVING_END | B | - | ego |  |
| B:e80 | 4.30 | STOP_START | B | - | ego |  |
| B:e81 | 4.95 | EGO_PATH_ENTRY | B | track_008 | radar |  |
| B:e82 | 5.10 | EGO_PATH_EXIT | B | track_013 | radar |  |
| B:e83 | 7.45 | EGO_PATH_ENTRY | B | track_013 | radar |  |
| B:e84 | 14.40 | TRACK_LOST | B | track_004 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e07 --PRECEDES--> B:e11
    B:e07 --PRECEDES--> B:e12
    B:e07 --PRECEDES--> B:e13
    B:e07 --PRECEDES--> B:e14
    B:e07 --PRECEDES--> B:e15
    B:e07 --PRECEDES--> B:e16
    B:e07 --PRECEDES--> B:e17
    B:e07 --PRECEDES--> B:e18
    B:e07 --PRECEDES--> B:e19
    B:e07 --PRECEDES--> B:e20
    B:e08 --PRECEDES--> B:e21
    B:e08 --PRECEDES--> B:e22
    B:e08 --PRECEDES--> B:e23
    B:e08 --PRECEDES--> B:e24
    B:e08 --PRECEDES--> B:e25
    B:e08 --PRECEDES--> B:e26
    B:e08 --PRECEDES--> B:e27
    B:e09 --PRECEDES--> B:e21
    B:e09 --PRECEDES--> B:e22
    B:e09 --PRECEDES--> B:e23
    B:e09 --PRECEDES--> B:e24
    B:e09 --PRECEDES--> B:e25
    B:e09 --PRECEDES--> B:e26
    B:e09 --PRECEDES--> B:e27
    B:e10 --PRECEDES--> B:e21
    B:e10 --PRECEDES--> B:e22
    B:e10 --PRECEDES--> B:e23
    B:e10 --PRECEDES--> B:e24
    B:e10 --PRECEDES--> B:e25
    B:e10 --PRECEDES--> B:e26
    B:e10 --PRECEDES--> B:e27
    B:e11 --PRECEDES--> B:e21
    B:e11 --PRECEDES--> B:e22
    B:e11 --PRECEDES--> B:e23
    B:e11 --PRECEDES--> B:e24
    B:e11 --PRECEDES--> B:e25
    B:e11 --PRECEDES--> B:e26
    B:e11 --PRECEDES--> B:e27
    B:e12 --PRECEDES--> B:e21
    B:e12 --PRECEDES--> B:e22
    B:e12 --PRECEDES--> B:e23
    B:e12 --PRECEDES--> B:e24
    B:e12 --PRECEDES--> B:e25
    B:e12 --PRECEDES--> B:e26
    B:e12 --PRECEDES--> B:e27
    B:e13 --PRECEDES--> B:e21
    B:e13 --PRECEDES--> B:e22
    B:e13 --PRECEDES--> B:e23
    B:e13 --PRECEDES--> B:e24
    B:e13 --PRECEDES--> B:e25
    B:e13 --PRECEDES--> B:e26
    B:e13 --PRECEDES--> B:e27
    B:e14 --PRECEDES--> B:e21
    B:e14 --PRECEDES--> B:e22
    B:e14 --PRECEDES--> B:e23
    B:e14 --PRECEDES--> B:e24
    B:e14 --PRECEDES--> B:e25
    B:e14 --PRECEDES--> B:e26
    B:e14 --PRECEDES--> B:e27
    B:e15 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e22
    B:e15 --PRECEDES--> B:e23
    B:e15 --PRECEDES--> B:e24
    B:e15 --PRECEDES--> B:e25
    B:e15 --PRECEDES--> B:e26
    B:e15 --PRECEDES--> B:e27
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e23
    B:e16 --PRECEDES--> B:e24
    B:e16 --PRECEDES--> B:e25
    B:e16 --PRECEDES--> B:e26
    B:e16 --PRECEDES--> B:e27
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e17 --PRECEDES--> B:e23
    B:e17 --PRECEDES--> B:e24
    B:e17 --PRECEDES--> B:e25
    B:e17 --PRECEDES--> B:e26
    B:e17 --PRECEDES--> B:e27
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e23
    B:e18 --PRECEDES--> B:e24
    B:e18 --PRECEDES--> B:e25
    B:e18 --PRECEDES--> B:e26
    B:e18 --PRECEDES--> B:e27
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e19 --PRECEDES--> B:e24
    B:e19 --PRECEDES--> B:e25
    B:e19 --PRECEDES--> B:e26
    B:e19 --PRECEDES--> B:e27
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e24
    B:e20 --PRECEDES--> B:e25
    B:e20 --PRECEDES--> B:e26
    B:e20 --PRECEDES--> B:e27
    B:e21 --PRECEDES--> B:e28
    B:e21 --PRECEDES--> B:e29
    B:e21 --PRECEDES--> B:e30
    B:e21 --PRECEDES--> B:e31
    B:e21 --PRECEDES--> B:e32
    B:e21 --PRECEDES--> B:e33
    B:e21 --PRECEDES--> B:e34
    B:e22 --PRECEDES--> B:e28
    B:e22 --PRECEDES--> B:e29
    B:e22 --PRECEDES--> B:e30
    B:e22 --PRECEDES--> B:e31
    B:e22 --PRECEDES--> B:e32
    B:e22 --PRECEDES--> B:e33
    B:e22 --PRECEDES--> B:e34
    B:e23 --PRECEDES--> B:e28
    B:e23 --PRECEDES--> B:e29
    B:e23 --PRECEDES--> B:e30
    B:e23 --PRECEDES--> B:e31
    B:e23 --PRECEDES--> B:e32
    B:e23 --PRECEDES--> B:e33
    B:e23 --PRECEDES--> B:e34
    B:e24 --PRECEDES--> B:e28
    B:e24 --PRECEDES--> B:e29
    B:e24 --PRECEDES--> B:e30
    B:e24 --PRECEDES--> B:e31
    B:e24 --PRECEDES--> B:e32
    B:e24 --PRECEDES--> B:e33
    B:e24 --PRECEDES--> B:e34
    B:e25 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e29
    B:e25 --PRECEDES--> B:e30
    B:e25 --PRECEDES--> B:e31
    B:e25 --PRECEDES--> B:e32
    B:e25 --PRECEDES--> B:e33
    B:e25 --PRECEDES--> B:e34
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e30
    B:e26 --PRECEDES--> B:e31
    B:e26 --PRECEDES--> B:e32
    B:e26 --PRECEDES--> B:e33
    B:e26 --PRECEDES--> B:e34
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e31
    B:e27 --PRECEDES--> B:e32
    B:e27 --PRECEDES--> B:e33
    B:e27 --PRECEDES--> B:e34
    B:e28 --PRECEDES--> B:e35
    B:e28 --PRECEDES--> B:e36
    B:e28 --PRECEDES--> B:e37
    B:e28 --PRECEDES--> B:e38
    B:e28 --PRECEDES--> B:e39
    B:e29 --PRECEDES--> B:e35
    B:e29 --PRECEDES--> B:e36
    B:e29 --PRECEDES--> B:e37
    B:e29 --PRECEDES--> B:e38
    B:e29 --PRECEDES--> B:e39
    B:e30 --PRECEDES--> B:e35
    B:e30 --PRECEDES--> B:e36
    B:e30 --PRECEDES--> B:e37
    B:e30 --PRECEDES--> B:e38
    B:e30 --PRECEDES--> B:e39
    B:e31 --PRECEDES--> B:e35
    B:e31 --PRECEDES--> B:e36
    B:e31 --PRECEDES--> B:e37
    B:e31 --PRECEDES--> B:e38
    B:e31 --PRECEDES--> B:e39
    B:e32 --PRECEDES--> B:e35
    B:e32 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e37
    B:e32 --PRECEDES--> B:e38
    B:e32 --PRECEDES--> B:e39
    B:e33 --PRECEDES--> B:e35
    B:e33 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e37
    B:e33 --PRECEDES--> B:e38
    B:e33 --PRECEDES--> B:e39
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e34 --PRECEDES--> B:e38
    B:e34 --PRECEDES--> B:e39
    B:e35 --PRECEDES--> B:e40
    B:e35 --PRECEDES--> B:e41
    B:e35 --PRECEDES--> B:e42
    B:e35 --PRECEDES--> B:e43
    B:e35 --PRECEDES--> B:e44
    B:e35 --PRECEDES--> B:e45
    B:e35 --PRECEDES--> B:e46
    B:e35 --PRECEDES--> B:e47
    B:e35 --PRECEDES--> B:e48
    B:e36 --PRECEDES--> B:e40
    B:e36 --PRECEDES--> B:e41
    B:e36 --PRECEDES--> B:e42
    B:e36 --PRECEDES--> B:e43
    B:e36 --PRECEDES--> B:e44
    B:e36 --PRECEDES--> B:e45
    B:e36 --PRECEDES--> B:e46
    B:e36 --PRECEDES--> B:e47
    B:e36 --PRECEDES--> B:e48
    B:e37 --PRECEDES--> B:e40
    B:e37 --PRECEDES--> B:e41
    B:e37 --PRECEDES--> B:e42
    B:e37 --PRECEDES--> B:e43
    B:e37 --PRECEDES--> B:e44
    B:e37 --PRECEDES--> B:e45
    B:e37 --PRECEDES--> B:e46
    B:e37 --PRECEDES--> B:e47
    B:e37 --PRECEDES--> B:e48
    B:e38 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e41
    B:e38 --PRECEDES--> B:e42
    B:e38 --PRECEDES--> B:e43
    B:e38 --PRECEDES--> B:e44
    B:e38 --PRECEDES--> B:e45
    B:e38 --PRECEDES--> B:e46
    B:e38 --PRECEDES--> B:e47
    B:e38 --PRECEDES--> B:e48
    B:e39 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e41
    B:e39 --PRECEDES--> B:e42
    B:e39 --PRECEDES--> B:e43
    B:e39 --PRECEDES--> B:e44
    B:e39 --PRECEDES--> B:e45
    B:e39 --PRECEDES--> B:e46
    B:e39 --PRECEDES--> B:e47
    B:e39 --PRECEDES--> B:e48
    B:e40 --PRECEDES--> B:e49
    B:e40 --PRECEDES--> B:e50
    B:e40 --PRECEDES--> B:e51
    B:e40 --PRECEDES--> B:e52
    B:e41 --PRECEDES--> B:e49
    B:e41 --PRECEDES--> B:e50
    B:e41 --PRECEDES--> B:e51
    B:e41 --PRECEDES--> B:e52
    B:e42 --PRECEDES--> B:e49
    B:e42 --PRECEDES--> B:e50
    B:e42 --PRECEDES--> B:e51
    B:e42 --PRECEDES--> B:e52
    B:e43 --PRECEDES--> B:e49
    B:e43 --PRECEDES--> B:e50
    B:e43 --PRECEDES--> B:e51
    B:e43 --PRECEDES--> B:e52
    B:e44 --PRECEDES--> B:e49
    B:e44 --PRECEDES--> B:e50
    B:e44 --PRECEDES--> B:e51
    B:e44 --PRECEDES--> B:e52
    B:e45 --PRECEDES--> B:e49
    B:e45 --PRECEDES--> B:e50
    B:e45 --PRECEDES--> B:e51
    B:e45 --PRECEDES--> B:e52
    B:e46 --PRECEDES--> B:e49
    B:e46 --PRECEDES--> B:e50
    B:e46 --PRECEDES--> B:e51
    B:e46 --PRECEDES--> B:e52
    B:e47 --PRECEDES--> B:e49
    B:e47 --PRECEDES--> B:e50
    B:e47 --PRECEDES--> B:e51
    B:e47 --PRECEDES--> B:e52
    B:e48 --PRECEDES--> B:e49
    B:e48 --PRECEDES--> B:e50
    B:e48 --PRECEDES--> B:e51
    B:e48 --PRECEDES--> B:e52
    B:e49 --PRECEDES--> B:e53
    B:e49 --PRECEDES--> B:e54
    B:e49 --PRECEDES--> B:e55
    B:e49 --PRECEDES--> B:e56
    B:e50 --PRECEDES--> B:e53
    B:e50 --PRECEDES--> B:e54
    B:e50 --PRECEDES--> B:e55
    B:e50 --PRECEDES--> B:e56
    B:e51 --PRECEDES--> B:e53
    B:e51 --PRECEDES--> B:e54
    B:e51 --PRECEDES--> B:e55
    B:e51 --PRECEDES--> B:e56
    B:e52 --PRECEDES--> B:e53
    B:e52 --PRECEDES--> B:e54
    B:e52 --PRECEDES--> B:e55
    B:e52 --PRECEDES--> B:e56
    B:e53 --PRECEDES--> B:e57
    B:e53 --PRECEDES--> B:e58
    B:e53 --PRECEDES--> B:e59
    B:e53 --PRECEDES--> B:e60
    B:e53 --PRECEDES--> B:e61
    B:e54 --PRECEDES--> B:e57
    B:e54 --PRECEDES--> B:e58
    B:e54 --PRECEDES--> B:e59
    B:e54 --PRECEDES--> B:e60
    B:e54 --PRECEDES--> B:e61
    B:e55 --PRECEDES--> B:e57
    B:e55 --PRECEDES--> B:e58
    B:e55 --PRECEDES--> B:e59
    B:e55 --PRECEDES--> B:e60
    B:e55 --PRECEDES--> B:e61
    B:e56 --PRECEDES--> B:e57
    B:e56 --PRECEDES--> B:e58
    B:e56 --PRECEDES--> B:e59
    B:e56 --PRECEDES--> B:e60
    B:e56 --PRECEDES--> B:e61
    B:e57 --PRECEDES--> B:e62
    B:e57 --PRECEDES--> B:e63
    B:e57 --PRECEDES--> B:e64
    B:e57 --PRECEDES--> B:e65
    B:e58 --PRECEDES--> B:e62
    B:e58 --PRECEDES--> B:e63
    B:e58 --PRECEDES--> B:e64
    B:e58 --PRECEDES--> B:e65
    B:e59 --PRECEDES--> B:e62
    B:e59 --PRECEDES--> B:e63
    B:e59 --PRECEDES--> B:e64
    B:e59 --PRECEDES--> B:e65
    B:e60 --PRECEDES--> B:e62
    B:e60 --PRECEDES--> B:e63
    B:e60 --PRECEDES--> B:e64
    B:e60 --PRECEDES--> B:e65
    B:e61 --PRECEDES--> B:e62
    B:e61 --PRECEDES--> B:e63
    B:e61 --PRECEDES--> B:e64
    B:e61 --PRECEDES--> B:e65
    B:e62 --PRECEDES--> B:e66
    B:e62 --PRECEDES--> B:e67
    B:e62 --PRECEDES--> B:e68
    B:e62 --PRECEDES--> B:e69
    B:e63 --PRECEDES--> B:e66
    B:e63 --PRECEDES--> B:e67
    B:e63 --PRECEDES--> B:e68
    B:e63 --PRECEDES--> B:e69
    B:e64 --PRECEDES--> B:e66
    B:e64 --PRECEDES--> B:e67
    B:e64 --PRECEDES--> B:e68
    B:e64 --PRECEDES--> B:e69
    B:e65 --PRECEDES--> B:e66
    B:e65 --PRECEDES--> B:e67
    B:e65 --PRECEDES--> B:e68
    B:e65 --PRECEDES--> B:e69
    B:e66 --PRECEDES--> B:e70
    B:e67 --PRECEDES--> B:e70
    B:e68 --PRECEDES--> B:e70
    B:e69 --PRECEDES--> B:e70
    B:e70 --PRECEDES--> B:e71
    B:e70 --PRECEDES--> B:e72
    B:e70 --PRECEDES--> B:e73
    B:e70 --PRECEDES--> B:e74
    B:e70 --PRECEDES--> B:e75
    B:e71 --PRECEDES--> B:e76
    B:e71 --PRECEDES--> B:e77
    B:e71 --PRECEDES--> B:e78
    B:e71 --PRECEDES--> B:e79
    B:e71 --PRECEDES--> B:e80
    B:e72 --PRECEDES--> B:e76
    B:e72 --PRECEDES--> B:e77
    B:e72 --PRECEDES--> B:e78
    B:e72 --PRECEDES--> B:e79
    B:e72 --PRECEDES--> B:e80
    B:e73 --PRECEDES--> B:e76
    B:e73 --PRECEDES--> B:e77
    B:e73 --PRECEDES--> B:e78
    B:e73 --PRECEDES--> B:e79
    B:e73 --PRECEDES--> B:e80
    B:e74 --PRECEDES--> B:e76
    B:e74 --PRECEDES--> B:e77
    B:e74 --PRECEDES--> B:e78
    B:e74 --PRECEDES--> B:e79
    B:e74 --PRECEDES--> B:e80
    B:e75 --PRECEDES--> B:e76
    B:e75 --PRECEDES--> B:e77
    B:e75 --PRECEDES--> B:e78
    B:e75 --PRECEDES--> B:e79
    B:e75 --PRECEDES--> B:e80
    B:e76 --PRECEDES--> B:e81
    B:e77 --PRECEDES--> B:e81
    B:e78 --PRECEDES--> B:e81
    B:e79 --PRECEDES--> B:e81
    B:e80 --PRECEDES--> B:e81
    B:e81 --PRECEDES--> B:e82
    B:e82 --PRECEDES--> B:e83
    B:e83 --PRECEDES--> B:e84
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e07
    B:e10 --SAME_TRACK--> B:e16
    B:e12 --SAME_TRACK--> B:e17
    B:e13 --SAME_TRACK--> B:e18
    B:e14 --SAME_TRACK--> B:e19
    B:e15 --SAME_TRACK--> B:e20
    B:e11 --SAME_TRACK--> B:e26
    B:e24 --SAME_TRACK--> B:e27
    B:e11 --SAME_TRACK--> B:e28
    B:e13 --SAME_TRACK--> B:e33
    B:e30 --SAME_TRACK--> B:e34
    B:e13 --SAME_TRACK--> B:e35
    B:e10 --SAME_TRACK--> B:e38
    B:e29 --SAME_TRACK--> B:e39
    B:e10 --SAME_TRACK--> B:e40
    B:e15 --SAME_TRACK--> B:e44
    B:e36 --SAME_TRACK--> B:e45
    B:e37 --SAME_TRACK--> B:e46
    B:e41 --SAME_TRACK--> B:e47
    B:e41 --SAME_TRACK--> B:e48
    B:e15 --SAME_TRACK--> B:e49
    B:e42 --SAME_TRACK--> B:e50
    B:e43 --SAME_TRACK--> B:e51
    B:e25 --SAME_TRACK--> B:e52
    B:e10 --SAME_TRACK--> B:e53
    B:e13 --SAME_TRACK--> B:e54
    B:e32 --SAME_TRACK--> B:e56
    B:e12 --SAME_TRACK--> B:e57
    B:e14 --SAME_TRACK--> B:e58
    B:e24 --SAME_TRACK--> B:e59
    B:e30 --SAME_TRACK--> B:e60
    B:e11 --SAME_TRACK--> B:e61
    B:e30 --SAME_TRACK--> B:e62
    B:e15 --SAME_TRACK--> B:e63
    B:e30 --SAME_TRACK--> B:e64
    B:e31 --SAME_TRACK--> B:e65
    B:e29 --SAME_TRACK--> B:e66
    B:e31 --SAME_TRACK--> B:e67
    B:e29 --SAME_TRACK--> B:e68
    B:e13 --SAME_TRACK--> B:e69
    B:e41 --SAME_TRACK--> B:e70
    B:e36 --SAME_TRACK--> B:e71
    B:e41 --SAME_TRACK--> B:e72
    B:e29 --SAME_TRACK--> B:e73
    B:e36 --SAME_TRACK--> B:e74
    B:e15 --SAME_TRACK--> B:e75
    B:e37 --SAME_TRACK--> B:e76
    B:e42 --SAME_TRACK--> B:e77
    B:e43 --SAME_TRACK--> B:e78
    B:e29 --SAME_TRACK--> B:e81
    B:e36 --SAME_TRACK--> B:e82
    B:e36 --SAME_TRACK--> B:e83
    B:e12 --SAME_TRACK--> B:e84
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.85 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 0.80 |
| 1.20 | B:e03 TRACK_APPEARED_LEFT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE | 1.10 |
| 1.60 | B:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING | 1.50 |
| 1.65 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 1.60 |
| 3.35 | B:e07 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 3.30 |
| 3.70 | B:e08 COLLISION<br>B:e09 STRONG_THROTTLE_START<br>B:e10 TRACK_APPEARED_LEFT track_002<br>B:e11 TRACK_APPEARED_LEFT track_003<br>B:e12 TRACK_APPEARED_LEFT track_004<br>B:e13 TRACK_APPEARED_LEFT track_005<br>B:e14 TRACK_APPEARED_LEFT track_007<br>B:e15 TRACK_APPEARED_LEFT track_018<br>B:e16 CLOSING_START track_002<br>B:e17 CLOSING_START track_004<br>B:e18 CLOSING_START track_005<br>B:e19 CLOSING_START track_007<br>B:e20 CLOSING_START track_018 | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 3.60 |
| 3.75 | B:e21 STRONG_THROTTLE_END<br>B:e22 BRAKE_START<br>B:e23 HARD_BRAKE_START<br>B:e24 TRACK_APPEARED_LEFT track_012<br>B:e25 TRACK_APPEARED_RIGHT track_006<br>B:e26 EGO_PATH_ENTRY track_003<br>B:e27 CLOSING_START track_012 | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 | 3.70 |
| 3.80 | B:e28 EGO_PATH_EXIT track_003<br>B:e29 TRACK_APPEARED_LEFT track_008<br>B:e30 TRACK_APPEARED_LEFT track_009<br>B:e31 TRACK_APPEARED_LEFT track_010<br>B:e32 TRACK_APPEARED_RIGHT track_011<br>B:e33 EGO_PATH_ENTRY track_005<br>B:e34 CLOSING_START track_009 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: IN_EGO_PATH, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 | 3.70 |
| 3.85 | B:e35 EGO_PATH_EXIT track_005<br>B:e36 TRACK_APPEARED_LEFT track_013<br>B:e37 TRACK_APPEARED_LEFT track_014<br>B:e38 EGO_PATH_ENTRY track_002<br>B:e39 CLOSING_START track_008 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: no active state<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 | 3.80 |
| 3.90 | B:e40 EGO_PATH_EXIT track_002<br>B:e41 TRACK_APPEARED_LEFT track_015<br>B:e42 TRACK_APPEARED_LEFT track_016<br>B:e43 TRACK_APPEARED_LEFT track_017<br>B:e44 EGO_PATH_ENTRY track_018<br>B:e45 CLOSING_START track_013<br>B:e46 CLOSING_START track_014<br>B:e47 CLOSING_START track_015<br>B:e48 CRITICAL_TTC_START track_015 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: no active state<br>track_014: no active state<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 | 3.80 |
| 3.95 | B:e49 EGO_PATH_EXIT track_018<br>B:e50 CLOSING_START track_016<br>B:e51 CLOSING_START track_017<br>B:e52 TRACK_LOST track_006 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: no active state<br>track_017: no active state<br>track_018: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 3.90 |
| 4.00 | B:e53 CLOSING_END track_002<br>B:e54 CLOSING_END track_005<br>B:e55 TRACK_APPEARED_LEFT track_019<br>B:e56 TRACK_LOST track_011 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_006 | 3.90 |
| 4.05 | B:e57 CLOSING_END track_004<br>B:e58 CLOSING_END track_007<br>B:e59 CLOSING_END track_012<br>B:e60 EGO_PATH_ENTRY track_009<br>B:e61 TRACK_LOST track_003 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: no active state<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_011 | 4.00 |
| 4.10 | B:e62 CLOSING_END track_009<br>B:e63 CLOSING_END track_018<br>B:e64 EGO_PATH_EXIT track_009<br>B:e65 EGO_PATH_ENTRY track_010 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: CLOSING, IN_EGO_PATH<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 | 4.00 |
| 4.15 | B:e66 CLOSING_END track_008<br>B:e67 EGO_PATH_EXIT track_010<br>B:e68 EGO_PATH_ENTRY track_008<br>B:e69 TRACK_LOST track_005 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: no active state<br>track_010: IN_EGO_PATH<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 | 4.10 |
| 4.20 | B:e70 CRITICAL_TTC_END track_015 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 | 4.10 |
| 4.25 | B:e71 CLOSING_END track_013<br>B:e72 CLOSING_END track_015<br>B:e73 EGO_PATH_EXIT track_008<br>B:e74 EGO_PATH_ENTRY track_013<br>B:e75 TRACK_LOST track_018 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 | 4.20 |
| 4.30 | B:e76 CLOSING_END track_014<br>B:e77 CLOSING_END track_016<br>B:e78 CLOSING_END track_017<br>B:e79 MOVING_END<br>B:e80 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 | 4.20 |
| 4.95 | B:e81 EGO_PATH_ENTRY track_008 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 | 4.90 |
| 5.10 | B:e82 EGO_PATH_EXIT track_013 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 | 5.00 |
| 7.45 | B:e83 EGO_PATH_ENTRY track_013 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 | 7.40 |
| 14.40 | B:e84 TRACK_LOST track_004 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 | 14.30 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 1.20 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_001, since B:e06 (t = 1.65 s); the track was lost at 3.35 s
- BRAKE, since B:e22 (t = 3.75 s)
- HARD_BRAKE, since B:e23 (t = 3.75 s)
- STOP, since B:e80 (t = 4.30 s)
- EGO_PATH of track_008, since B:e81 (t = 4.95 s)
- EGO_PATH of track_013, since B:e83 (t = 7.45 s)

## Tracks lost

- track_001 at 3.35 s (B:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_006, track_011, track_003, track_005, track_018, track_004

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.20 | 3.35 | 42 | 37.0 m / -51 deg | 5.59 m (3.35) | 5.6 m / -84 deg | 11.8 m/s |
| track_002 | 3.70 | 14.45 | 216 | 18.9 m / -43 deg | 17.46 m (3.90) | 18.6 m / +74 deg | 4.2 m/s |
| track_003 | 3.70 | 4.05 | 8 | 32.4 m / -15 deg | 31.74 m (3.85) | 32.9 m / +79 deg | 6.4 m/s |
| track_004 | 3.70 | 14.40 | 208 | 37.3 m / -61 deg | 35.30 m (3.95) | 35.8 m / +53 deg | 6.0 m/s |
| track_005 | 3.70 | 4.15 | 9 | 22.8 m / -27 deg | 21.76 m (3.90) | 23.1 m / +77 deg | 5.7 m/s |
| track_006 | 3.75 | 3.95 | 5 | 87.4 m / +20 deg | 87.38 m (3.75) | 88.2 m / +75 deg | 6.5 m/s |
| track_007 | 3.70 | 14.45 | 214 | 30.0 m / -51 deg | 28.46 m (3.95) | 29.6 m / +61 deg | 4.9 m/s |
| track_008 | 3.80 | 14.45 | 214 | 31.7 m / -77 deg | 29.73 m (4.25) | 30.4 m / +3 deg | 6.9 m/s |
| track_009 | 3.80 | 14.45 | 208 | 53.3 m / -63 deg | 51.77 m (4.10) | 52.1 m / +19 deg | 5.7 m/s |
| track_010 | 3.80 | 14.45 | 205 | 35.3 m / -71 deg | 33.27 m (14.45) | 33.3 m / +12 deg | 6.4 m/s |
| track_011 | 3.80 | 4.00 | 5 | 98.9 m / +28 deg | 98.87 m (3.80) | 100.0 m / +79 deg | 6.8 m/s |
| track_012 | 3.75 | 14.45 | 213 | 52.9 m / -48 deg | 51.80 m (3.95) | 52.4 m / +50 deg | 3.1 m/s |
| track_013 | 3.85 | 14.45 | 189 | 30.6 m / -72 deg | 28.23 m (11.50) | 28.3 m / -4 deg | 6.3 m/s |
| track_014 | 3.85 | 14.45 | 213 | 22.7 m / -77 deg | 20.80 m (4.40) | 21.1 m / -7 deg | 6.4 m/s |
| track_015 | 3.90 | 14.45 | 212 | 5.1 m / -90 deg | 2.45 m (4.25) | 2.8 m / -76 deg | 10.6 m/s |
| track_016 | 3.90 | 14.45 | 134 | 33.9 m / -68 deg | 32.22 m (8.15) | 32.3 m / -11 deg | 5.5 m/s |
| track_017 | 3.90 | 14.45 | 212 | 25.8 m / -73 deg | 24.10 m (6.95) | 24.5 m / -15 deg | 5.8 m/s |
| track_018 | 3.70 | 4.25 | 7 | 27.4 m / -64 deg | 25.33 m (4.00) | 26.1 m / +72 deg | 19.0 m/s |
| track_019 | 4.00 | 14.45 | 198 | 30.4 m / -55 deg | 28.52 m (10.90) | 28.6 m / -21 deg | 3.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.85 s: B started applying strong throttle.
- t = 1.20 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.20 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.60 s: B stopped applying strong throttle.
- t = 1.65 s: B's time-to-contact with track_001 became critical.
- t = 3.35 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.70 s: B's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: B started applying strong throttle.
- t = 3.70 s: B's radar started tracking track_002, which appeared on its left.
- t = 3.70 s: B's radar started tracking track_003, which appeared on its left.
- t = 3.70 s: B's radar started tracking track_004, which appeared on its left.
- t = 3.70 s: B's radar started tracking track_005, which appeared on its left.
- t = 3.70 s: B's radar started tracking track_007, which appeared on its left.
- t = 3.70 s: B's radar started tracking track_018, which appeared on its left.
- t = 3.70 s: B observed track_002 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_004 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_007 start closing in (already the case when first observed).
- t = 3.70 s: B observed track_018 start closing in (already the case when first observed).
- t = 3.75 s: B stopped applying strong throttle.
- t = 3.75 s: B started braking.
- t = 3.75 s: B started braking hard.
- t = 3.75 s: B's radar started tracking track_012, which appeared on its left.
- t = 3.75 s: B's radar started tracking track_006, which appeared on its right.
- t = 3.75 s: B observed track_003 enter its forward path corridor.
- t = 3.75 s: B observed track_012 start closing in (already the case when first observed).
- t = 3.80 s: B observed track_003 leave its forward path corridor.
- t = 3.80 s: B's radar started tracking track_008, which appeared on its left.
- t = 3.80 s: B's radar started tracking track_009, which appeared on its left.
- t = 3.80 s: B's radar started tracking track_010, which appeared on its left.
- t = 3.80 s: B's radar started tracking track_011, which appeared on its right.
- t = 3.80 s: B observed track_005 enter its forward path corridor.
- t = 3.80 s: B observed track_009 start closing in (already the case when first observed).
- t = 3.85 s: B observed track_005 leave its forward path corridor.
- t = 3.85 s: B's radar started tracking track_013, which appeared on its left.
- t = 3.85 s: B's radar started tracking track_014, which appeared on its left.
- t = 3.85 s: B observed track_002 enter its forward path corridor.
- t = 3.85 s: B observed track_008 start closing in.
- t = 3.90 s: B observed track_002 leave its forward path corridor.
- t = 3.90 s: B's radar started tracking track_015, which appeared on its left.
- t = 3.90 s: B's radar started tracking track_016, which appeared on its left.
- t = 3.90 s: B's radar started tracking track_017, which appeared on its left.
- t = 3.90 s: B observed track_018 enter its forward path corridor.
- t = 3.90 s: B observed track_013 start closing in.
- t = 3.90 s: B observed track_014 start closing in.
- t = 3.90 s: B observed track_015 start closing in (already the case when first observed).
- t = 3.90 s: B's time-to-contact with track_015 became critical (already the case when first observed).
- t = 3.95 s: B observed track_018 leave its forward path corridor.
- t = 3.95 s: B observed track_016 start closing in.
- t = 3.95 s: B observed track_017 start closing in.
- t = 3.95 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 4.00 s: B observed track_002 stop closing in.
- t = 4.00 s: B observed track_005 stop closing in.
- t = 4.00 s: B's radar started tracking track_019, which appeared on its left.
- t = 4.00 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 4.05 s: B observed track_004 stop closing in.
- t = 4.05 s: B observed track_007 stop closing in.
- t = 4.05 s: B observed track_012 stop closing in.
- t = 4.05 s: B observed track_009 enter its forward path corridor.
- t = 4.05 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 4.10 s: B observed track_009 stop closing in.
- t = 4.10 s: B observed track_018 stop closing in.
- t = 4.10 s: B observed track_009 leave its forward path corridor.
- t = 4.10 s: B observed track_010 enter its forward path corridor.
- t = 4.15 s: B observed track_008 stop closing in.
- t = 4.15 s: B observed track_010 leave its forward path corridor.
- t = 4.15 s: B observed track_008 enter its forward path corridor.
- t = 4.15 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 4.20 s: B's time-to-contact with track_015 stopped being critical.
- t = 4.25 s: B observed track_013 stop closing in.
- t = 4.25 s: B observed track_015 stop closing in.
- t = 4.25 s: B observed track_008 leave its forward path corridor.
- t = 4.25 s: B observed track_013 enter its forward path corridor.
- t = 4.25 s: B's radar lost track_018 (its states are UNKNOWN from then on, not ended).
- t = 4.30 s: B observed track_014 stop closing in.
- t = 4.30 s: B observed track_016 stop closing in.
- t = 4.30 s: B observed track_017 stop closing in.
- t = 4.30 s: B stopped moving.
- t = 4.30 s: B came to a stop.
- t = 4.95 s: B observed track_008 enter its forward path corridor.
- t = 5.10 s: B observed track_013 leave its forward path corridor.
- t = 7.45 s: B observed track_013 enter its forward path corridor.
- t = 14.40 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
