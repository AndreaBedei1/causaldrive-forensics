# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 57.063893526792526 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 19 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 81; edges: 353 (PRECEDES 307, SAME_TRACK 46)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.30 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.45 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 2.45 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e07 | 3.40 | MOVING_END | A | - | ego |  |
| A:e08 | 3.40 | STOP_START | A | - | ego |  |
| A:e09 | 3.50 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 6.95 | BRAKE_END | A | - | controls |  |
| A:e11 | 7.30 | STOP_END | A | - | ego |  |
| A:e12 | 7.30 | MOVING_START | A | - | ego |  |
| A:e13 | 7.30 | CLOSING_START | A | track_001 | radar |  |
| A:e14 | 8.30 | TURN_LEFT_START | A | - | ego |  |
| A:e15 | 8.30 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e16 | 8.80 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e17 | 8.80 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e18 | 8.80 | TRACK_APPEARED_LEFT | A | track_010 | radar |  |
| A:e19 | 8.80 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e20 | 8.80 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e21 | 8.80 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e22 | 8.85 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e23 | 8.85 | TRACK_APPEARED_LEFT | A | track_004 | radar |  |
| A:e24 | 8.85 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e25 | 8.85 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e26 | 8.85 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e27 | 8.85 | TRACK_APPEARED_LEFT | A | track_013 | radar |  |
| A:e28 | 8.85 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e29 | 8.85 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e30 | 8.85 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e31 | 8.85 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e32 | 8.85 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e33 | 8.85 | CLOSING_START | A | track_013 | radar | active_at_first_observation=True |
| A:e34 | 8.90 | TRACK_APPEARED_LEFT | A | track_009 | radar |  |
| A:e35 | 8.90 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e36 | 9.15 | TRACK_LOST | A | track_001 | radar |  |
| A:e37 | 9.30 | TRACK_APPEARED_LEFT | A | track_011 | radar |  |
| A:e38 | 9.30 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e39 | 9.35 | TRACK_APPEARED_RIGHT | A | track_012 | radar |  |
| A:e40 | 9.40 | TRACK_APPEARED_LEFT | A | track_014 | radar |  |
| A:e41 | 9.40 | CLOSING_START | A | track_014 | radar | active_at_first_observation=True |
| A:e42 | 9.45 | TRACK_APPEARED_LEFT | A | track_016 | radar |  |
| A:e43 | 9.45 | CLOSING_START | A | track_016 | radar | active_at_first_observation=True |
| A:e44 | 9.50 | COLLISION | A | - | collision_sensor | peak_impulse=4032.49 |
| A:e45 | 9.50 | TRACK_APPEARED_FRONT | A | track_017 | radar |  |
| A:e46 | 9.50 | TRACK_APPEARED_RIGHT | A | track_015 | radar |  |
| A:e47 | 9.50 | CLOSING_START | A | track_017 | radar | active_at_first_observation=True |
| A:e48 | 9.55 | EGO_PATH_EXIT | A | track_017 | radar |  |
| A:e49 | 9.55 | BRAKE_START | A | - | controls |  |
| A:e50 | 9.55 | TRACK_APPEARED_LEFT | A | track_018 | radar |  |
| A:e51 | 9.55 | TRACK_APPEARED_RIGHT | A | track_019 | radar |  |
| A:e52 | 9.55 | CLOSING_START | A | track_018 | radar | active_at_first_observation=True |
| A:e53 | 9.55 | CLOSING_START | A | track_019 | radar | active_at_first_observation=True |
| A:e54 | 9.55 | TRACK_LOST | A | track_012 | radar |  |
| A:e55 | 9.70 | CLOSING_START | A | track_015 | radar |  |
| A:e56 | 10.00 | CLOSING_END | A | track_002 | radar |  |
| A:e57 | 10.00 | CLOSING_END | A | track_005 | radar |  |
| A:e58 | 10.00 | CLOSING_END | A | track_008 | radar |  |
| A:e59 | 10.00 | CLOSING_END | A | track_015 | radar |  |
| A:e60 | 10.00 | CLOSING_END | A | track_017 | radar |  |
| A:e61 | 10.00 | CLOSING_END | A | track_018 | radar |  |
| A:e62 | 10.00 | CLOSING_END | A | track_019 | radar |  |
| A:e63 | 10.00 | TURN_LEFT_END | A | - | ego |  |
| A:e64 | 10.00 | MOVING_END | A | - | ego |  |
| A:e65 | 10.00 | STOP_START | A | - | ego |  |
| A:e66 | 10.00 | TRACK_LOST | A | track_019 | radar |  |
| A:e67 | 10.05 | CLOSING_END | A | track_003 | radar |  |
| A:e68 | 10.05 | CLOSING_END | A | track_004 | radar |  |
| A:e69 | 10.05 | CLOSING_END | A | track_007 | radar |  |
| A:e70 | 10.05 | CLOSING_END | A | track_009 | radar |  |
| A:e71 | 10.05 | CLOSING_END | A | track_010 | radar |  |
| A:e72 | 10.05 | CLOSING_END | A | track_011 | radar |  |
| A:e73 | 10.05 | CLOSING_END | A | track_013 | radar |  |
| A:e74 | 10.05 | CLOSING_END | A | track_014 | radar |  |
| A:e75 | 10.05 | CLOSING_END | A | track_016 | radar |  |
| A:e76 | 10.10 | CLOSING_END | A | track_006 | radar |  |
| A:e77 | 11.00 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False |
| A:e78 | 12.60 | TRACK_LOST | A | track_006 | radar |  |
| A:e79 | 14.35 | TRACK_LOST | A | track_018 | radar |  |
| A:e80 | 14.85 | TRACK_LOST | A | track_005 | radar |  |
| A:e81 | 14.90 | TRACK_LOST | A | track_008 | radar |  |

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
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e19
    A:e14 --PRECEDES--> A:e20
    A:e14 --PRECEDES--> A:e21
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e15 --PRECEDES--> A:e20
    A:e15 --PRECEDES--> A:e21
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
    A:e17 --PRECEDES--> A:e22
    A:e17 --PRECEDES--> A:e23
    A:e17 --PRECEDES--> A:e24
    A:e17 --PRECEDES--> A:e25
    A:e17 --PRECEDES--> A:e26
    A:e17 --PRECEDES--> A:e27
    A:e17 --PRECEDES--> A:e28
    A:e17 --PRECEDES--> A:e29
    A:e17 --PRECEDES--> A:e30
    A:e17 --PRECEDES--> A:e31
    A:e17 --PRECEDES--> A:e32
    A:e17 --PRECEDES--> A:e33
    A:e18 --PRECEDES--> A:e22
    A:e18 --PRECEDES--> A:e23
    A:e18 --PRECEDES--> A:e24
    A:e18 --PRECEDES--> A:e25
    A:e18 --PRECEDES--> A:e26
    A:e18 --PRECEDES--> A:e27
    A:e18 --PRECEDES--> A:e28
    A:e18 --PRECEDES--> A:e29
    A:e18 --PRECEDES--> A:e30
    A:e18 --PRECEDES--> A:e31
    A:e18 --PRECEDES--> A:e32
    A:e18 --PRECEDES--> A:e33
    A:e19 --PRECEDES--> A:e22
    A:e19 --PRECEDES--> A:e23
    A:e19 --PRECEDES--> A:e24
    A:e19 --PRECEDES--> A:e25
    A:e19 --PRECEDES--> A:e26
    A:e19 --PRECEDES--> A:e27
    A:e19 --PRECEDES--> A:e28
    A:e19 --PRECEDES--> A:e29
    A:e19 --PRECEDES--> A:e30
    A:e19 --PRECEDES--> A:e31
    A:e19 --PRECEDES--> A:e32
    A:e19 --PRECEDES--> A:e33
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e20 --PRECEDES--> A:e25
    A:e20 --PRECEDES--> A:e26
    A:e20 --PRECEDES--> A:e27
    A:e20 --PRECEDES--> A:e28
    A:e20 --PRECEDES--> A:e29
    A:e20 --PRECEDES--> A:e30
    A:e20 --PRECEDES--> A:e31
    A:e20 --PRECEDES--> A:e32
    A:e20 --PRECEDES--> A:e33
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e26
    A:e21 --PRECEDES--> A:e27
    A:e21 --PRECEDES--> A:e28
    A:e21 --PRECEDES--> A:e29
    A:e21 --PRECEDES--> A:e30
    A:e21 --PRECEDES--> A:e31
    A:e21 --PRECEDES--> A:e32
    A:e21 --PRECEDES--> A:e33
    A:e22 --PRECEDES--> A:e34
    A:e22 --PRECEDES--> A:e35
    A:e23 --PRECEDES--> A:e34
    A:e23 --PRECEDES--> A:e35
    A:e24 --PRECEDES--> A:e34
    A:e24 --PRECEDES--> A:e35
    A:e25 --PRECEDES--> A:e34
    A:e25 --PRECEDES--> A:e35
    A:e26 --PRECEDES--> A:e34
    A:e26 --PRECEDES--> A:e35
    A:e27 --PRECEDES--> A:e34
    A:e27 --PRECEDES--> A:e35
    A:e28 --PRECEDES--> A:e34
    A:e28 --PRECEDES--> A:e35
    A:e29 --PRECEDES--> A:e34
    A:e29 --PRECEDES--> A:e35
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e43
    A:e41 --PRECEDES--> A:e42
    A:e41 --PRECEDES--> A:e43
    A:e42 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e45
    A:e42 --PRECEDES--> A:e46
    A:e42 --PRECEDES--> A:e47
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e46
    A:e43 --PRECEDES--> A:e47
    A:e44 --PRECEDES--> A:e48
    A:e44 --PRECEDES--> A:e49
    A:e44 --PRECEDES--> A:e50
    A:e44 --PRECEDES--> A:e51
    A:e44 --PRECEDES--> A:e52
    A:e44 --PRECEDES--> A:e53
    A:e44 --PRECEDES--> A:e54
    A:e45 --PRECEDES--> A:e48
    A:e45 --PRECEDES--> A:e49
    A:e45 --PRECEDES--> A:e50
    A:e45 --PRECEDES--> A:e51
    A:e45 --PRECEDES--> A:e52
    A:e45 --PRECEDES--> A:e53
    A:e45 --PRECEDES--> A:e54
    A:e46 --PRECEDES--> A:e48
    A:e46 --PRECEDES--> A:e49
    A:e46 --PRECEDES--> A:e50
    A:e46 --PRECEDES--> A:e51
    A:e46 --PRECEDES--> A:e52
    A:e46 --PRECEDES--> A:e53
    A:e46 --PRECEDES--> A:e54
    A:e47 --PRECEDES--> A:e48
    A:e47 --PRECEDES--> A:e49
    A:e47 --PRECEDES--> A:e50
    A:e47 --PRECEDES--> A:e51
    A:e47 --PRECEDES--> A:e52
    A:e47 --PRECEDES--> A:e53
    A:e47 --PRECEDES--> A:e54
    A:e48 --PRECEDES--> A:e55
    A:e49 --PRECEDES--> A:e55
    A:e50 --PRECEDES--> A:e55
    A:e51 --PRECEDES--> A:e55
    A:e52 --PRECEDES--> A:e55
    A:e53 --PRECEDES--> A:e55
    A:e54 --PRECEDES--> A:e55
    A:e55 --PRECEDES--> A:e56
    A:e55 --PRECEDES--> A:e57
    A:e55 --PRECEDES--> A:e58
    A:e55 --PRECEDES--> A:e59
    A:e55 --PRECEDES--> A:e60
    A:e55 --PRECEDES--> A:e61
    A:e55 --PRECEDES--> A:e62
    A:e55 --PRECEDES--> A:e63
    A:e55 --PRECEDES--> A:e64
    A:e55 --PRECEDES--> A:e65
    A:e55 --PRECEDES--> A:e66
    A:e56 --PRECEDES--> A:e67
    A:e56 --PRECEDES--> A:e68
    A:e56 --PRECEDES--> A:e69
    A:e56 --PRECEDES--> A:e70
    A:e56 --PRECEDES--> A:e71
    A:e56 --PRECEDES--> A:e72
    A:e56 --PRECEDES--> A:e73
    A:e56 --PRECEDES--> A:e74
    A:e56 --PRECEDES--> A:e75
    A:e57 --PRECEDES--> A:e67
    A:e57 --PRECEDES--> A:e68
    A:e57 --PRECEDES--> A:e69
    A:e57 --PRECEDES--> A:e70
    A:e57 --PRECEDES--> A:e71
    A:e57 --PRECEDES--> A:e72
    A:e57 --PRECEDES--> A:e73
    A:e57 --PRECEDES--> A:e74
    A:e57 --PRECEDES--> A:e75
    A:e58 --PRECEDES--> A:e67
    A:e58 --PRECEDES--> A:e68
    A:e58 --PRECEDES--> A:e69
    A:e58 --PRECEDES--> A:e70
    A:e58 --PRECEDES--> A:e71
    A:e58 --PRECEDES--> A:e72
    A:e58 --PRECEDES--> A:e73
    A:e58 --PRECEDES--> A:e74
    A:e58 --PRECEDES--> A:e75
    A:e59 --PRECEDES--> A:e67
    A:e59 --PRECEDES--> A:e68
    A:e59 --PRECEDES--> A:e69
    A:e59 --PRECEDES--> A:e70
    A:e59 --PRECEDES--> A:e71
    A:e59 --PRECEDES--> A:e72
    A:e59 --PRECEDES--> A:e73
    A:e59 --PRECEDES--> A:e74
    A:e59 --PRECEDES--> A:e75
    A:e60 --PRECEDES--> A:e67
    A:e60 --PRECEDES--> A:e68
    A:e60 --PRECEDES--> A:e69
    A:e60 --PRECEDES--> A:e70
    A:e60 --PRECEDES--> A:e71
    A:e60 --PRECEDES--> A:e72
    A:e60 --PRECEDES--> A:e73
    A:e60 --PRECEDES--> A:e74
    A:e60 --PRECEDES--> A:e75
    A:e61 --PRECEDES--> A:e67
    A:e61 --PRECEDES--> A:e68
    A:e61 --PRECEDES--> A:e69
    A:e61 --PRECEDES--> A:e70
    A:e61 --PRECEDES--> A:e71
    A:e61 --PRECEDES--> A:e72
    A:e61 --PRECEDES--> A:e73
    A:e61 --PRECEDES--> A:e74
    A:e61 --PRECEDES--> A:e75
    A:e62 --PRECEDES--> A:e67
    A:e62 --PRECEDES--> A:e68
    A:e62 --PRECEDES--> A:e69
    A:e62 --PRECEDES--> A:e70
    A:e62 --PRECEDES--> A:e71
    A:e62 --PRECEDES--> A:e72
    A:e62 --PRECEDES--> A:e73
    A:e62 --PRECEDES--> A:e74
    A:e62 --PRECEDES--> A:e75
    A:e63 --PRECEDES--> A:e67
    A:e63 --PRECEDES--> A:e68
    A:e63 --PRECEDES--> A:e69
    A:e63 --PRECEDES--> A:e70
    A:e63 --PRECEDES--> A:e71
    A:e63 --PRECEDES--> A:e72
    A:e63 --PRECEDES--> A:e73
    A:e63 --PRECEDES--> A:e74
    A:e63 --PRECEDES--> A:e75
    A:e64 --PRECEDES--> A:e67
    A:e64 --PRECEDES--> A:e68
    A:e64 --PRECEDES--> A:e69
    A:e64 --PRECEDES--> A:e70
    A:e64 --PRECEDES--> A:e71
    A:e64 --PRECEDES--> A:e72
    A:e64 --PRECEDES--> A:e73
    A:e64 --PRECEDES--> A:e74
    A:e64 --PRECEDES--> A:e75
    A:e65 --PRECEDES--> A:e67
    A:e65 --PRECEDES--> A:e68
    A:e65 --PRECEDES--> A:e69
    A:e65 --PRECEDES--> A:e70
    A:e65 --PRECEDES--> A:e71
    A:e65 --PRECEDES--> A:e72
    A:e65 --PRECEDES--> A:e73
    A:e65 --PRECEDES--> A:e74
    A:e65 --PRECEDES--> A:e75
    A:e66 --PRECEDES--> A:e67
    A:e66 --PRECEDES--> A:e68
    A:e66 --PRECEDES--> A:e69
    A:e66 --PRECEDES--> A:e70
    A:e66 --PRECEDES--> A:e71
    A:e66 --PRECEDES--> A:e72
    A:e66 --PRECEDES--> A:e73
    A:e66 --PRECEDES--> A:e74
    A:e66 --PRECEDES--> A:e75
    A:e67 --PRECEDES--> A:e76
    A:e68 --PRECEDES--> A:e76
    A:e69 --PRECEDES--> A:e76
    A:e70 --PRECEDES--> A:e76
    A:e71 --PRECEDES--> A:e76
    A:e72 --PRECEDES--> A:e76
    A:e73 --PRECEDES--> A:e76
    A:e74 --PRECEDES--> A:e76
    A:e75 --PRECEDES--> A:e76
    A:e76 --PRECEDES--> A:e77
    A:e77 --PRECEDES--> A:e78
    A:e78 --PRECEDES--> A:e79
    A:e79 --PRECEDES--> A:e80
    A:e80 --PRECEDES--> A:e81
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e13
    A:e04 --SAME_TRACK--> A:e15
    A:e16 --SAME_TRACK--> A:e19
    A:e17 --SAME_TRACK--> A:e20
    A:e18 --SAME_TRACK--> A:e21
    A:e22 --SAME_TRACK--> A:e28
    A:e23 --SAME_TRACK--> A:e29
    A:e24 --SAME_TRACK--> A:e30
    A:e25 --SAME_TRACK--> A:e31
    A:e26 --SAME_TRACK--> A:e32
    A:e27 --SAME_TRACK--> A:e33
    A:e34 --SAME_TRACK--> A:e35
    A:e04 --SAME_TRACK--> A:e36
    A:e37 --SAME_TRACK--> A:e38
    A:e40 --SAME_TRACK--> A:e41
    A:e42 --SAME_TRACK--> A:e43
    A:e45 --SAME_TRACK--> A:e47
    A:e45 --SAME_TRACK--> A:e48
    A:e50 --SAME_TRACK--> A:e52
    A:e51 --SAME_TRACK--> A:e53
    A:e39 --SAME_TRACK--> A:e54
    A:e46 --SAME_TRACK--> A:e55
    A:e16 --SAME_TRACK--> A:e56
    A:e17 --SAME_TRACK--> A:e57
    A:e26 --SAME_TRACK--> A:e58
    A:e46 --SAME_TRACK--> A:e59
    A:e45 --SAME_TRACK--> A:e60
    A:e50 --SAME_TRACK--> A:e61
    A:e51 --SAME_TRACK--> A:e62
    A:e51 --SAME_TRACK--> A:e66
    A:e22 --SAME_TRACK--> A:e67
    A:e23 --SAME_TRACK--> A:e68
    A:e25 --SAME_TRACK--> A:e69
    A:e34 --SAME_TRACK--> A:e70
    A:e18 --SAME_TRACK--> A:e71
    A:e37 --SAME_TRACK--> A:e72
    A:e27 --SAME_TRACK--> A:e73
    A:e40 --SAME_TRACK--> A:e74
    A:e42 --SAME_TRACK--> A:e75
    A:e24 --SAME_TRACK--> A:e76
    A:e24 --SAME_TRACK--> A:e78
    A:e50 --SAME_TRACK--> A:e79
    A:e17 --SAME_TRACK--> A:e80
    A:e26 --SAME_TRACK--> A:e81
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.70 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.30 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.45 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.40 |
| 2.65 | A:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 3.40 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 3.50 | A:e09 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.40 |
| 6.95 | A:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 7.30 | A:e11 STOP_END<br>A:e12 MOVING_START<br>A:e13 CLOSING_START track_001 | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 7.20 |
| 8.30 | A:e14 TURN_LEFT_START<br>A:e15 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 8.80 | A:e16 TRACK_APPEARED_LEFT track_002<br>A:e17 TRACK_APPEARED_LEFT track_005<br>A:e18 TRACK_APPEARED_LEFT track_010<br>A:e19 CLOSING_START track_002<br>A:e20 CLOSING_START track_005<br>A:e21 CLOSING_START track_010 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 8.70 |
| 8.85 | A:e22 TRACK_APPEARED_LEFT track_003<br>A:e23 TRACK_APPEARED_LEFT track_004<br>A:e24 TRACK_APPEARED_LEFT track_006<br>A:e25 TRACK_APPEARED_LEFT track_007<br>A:e26 TRACK_APPEARED_LEFT track_008<br>A:e27 TRACK_APPEARED_LEFT track_013<br>A:e28 CLOSING_START track_003<br>A:e29 CLOSING_START track_004<br>A:e30 CLOSING_START track_006<br>A:e31 CLOSING_START track_007<br>A:e32 CLOSING_START track_008<br>A:e33 CLOSING_START track_013 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_005: CLOSING<br>track_010: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.80 |
| 8.90 | A:e34 TRACK_APPEARED_LEFT track_009<br>A:e35 CLOSING_START track_009 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.80 |
| 9.15 | A:e36 TRACK_LOST track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>sign-0: STOP sign known, relevant to the path | 9.10 |
| 9.30 | A:e37 TRACK_APPEARED_LEFT track_011<br>A:e38 CLOSING_START track_011 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.20 |
| 9.35 | A:e39 TRACK_APPEARED_RIGHT track_012 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.30 |
| 9.40 | A:e40 TRACK_APPEARED_LEFT track_014<br>A:e41 CLOSING_START track_014 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.30 |
| 9.45 | A:e42 TRACK_APPEARED_LEFT track_016<br>A:e43 CLOSING_START track_016 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.40 |
| 9.50 | A:e44 COLLISION<br>A:e45 TRACK_APPEARED_FRONT track_017<br>A:e46 TRACK_APPEARED_RIGHT track_015<br>A:e47 CLOSING_START track_017 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.40 |
| 9.55 | A:e48 EGO_PATH_EXIT track_017<br>A:e49 BRAKE_START<br>A:e50 TRACK_APPEARED_LEFT track_018<br>A:e51 TRACK_APPEARED_RIGHT track_019<br>A:e52 CLOSING_START track_018<br>A:e53 CLOSING_START track_019<br>A:e54 TRACK_LOST track_012 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 9.70 | A:e55 CLOSING_START track_015 | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_012<br>sign-0: STOP sign known, relevant to the path | 9.60 |
| 10.00 | A:e56 CLOSING_END track_002<br>A:e57 CLOSING_END track_005<br>A:e58 CLOSING_END track_008<br>A:e59 CLOSING_END track_015<br>A:e60 CLOSING_END track_017<br>A:e61 CLOSING_END track_018<br>A:e62 CLOSING_END track_019<br>A:e63 TURN_LEFT_END<br>A:e64 MOVING_END<br>A:e65 STOP_START<br>A:e66 TRACK_LOST track_019 | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_012<br>sign-0: STOP sign known, relevant to the path | 9.90 |
| 10.05 | A:e67 CLOSING_END track_003<br>A:e68 CLOSING_END track_004<br>A:e69 CLOSING_END track_007<br>A:e70 CLOSING_END track_009<br>A:e71 CLOSING_END track_010<br>A:e72 CLOSING_END track_011<br>A:e73 CLOSING_END track_013<br>A:e74 CLOSING_END track_014<br>A:e75 CLOSING_END track_016 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: no active state<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path | 10.00 |
| 10.10 | A:e76 CLOSING_END track_006 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path | 10.00 |
| 11.00 | A:e77 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path | 10.90 |
| 12.60 | A:e78 TRACK_LOST track_006 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 12.50 |
| 14.35 | A:e79 TRACK_LOST track_018 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_012, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 14.30 |
| 14.85 | A:e80 TRACK_LOST track_005 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_012, track_018, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 14.80 |
| 14.90 | A:e81 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track lost, states UNKNOWN: track_001, track_005, track_006, track_012, track_018, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 14.80 |

## States still active when observation ended

- CLOSING of track_001, since A:e13 (t = 7.30 s); the track was lost at 9.15 s
- CRITICAL_TTC of track_001, since A:e15 (t = 8.30 s); the track was lost at 9.15 s
- BRAKE, since A:e49 (t = 9.55 s)
- STOP, since A:e65 (t = 10.00 s)
- STOP_SIGN_DETECTED of sign-1, since A:e77 (t = 11.00 s)

## Tracks lost

- track_001 at 9.15 s (A:e36): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_019 at 10.00 s (A:e66): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_012, track_006, track_018, track_005, track_008

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.30, COLLISION 9.50 (+1.20 s)

## Sign detection windows

- STOP sign sign-0: detected 0.70 s -> 2.30 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 11.00 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.45 | 9.15 | 134 | 29.1 m / -57 deg | 4.63 m (9.15) | 4.6 m / -86 deg | 10.8 m/s |
| track_002 | 8.80 | 14.95 | 47 | 68.5 m / -79 deg | 61.77 m (13.20) | 62.2 m / -26 deg | 4.0 m/s |
| track_003 | 8.85 | 14.95 | 90 | 45.3 m / -79 deg | 38.40 m (14.10) | 38.5 m / -32 deg | 3.7 m/s |
| track_004 | 8.85 | 14.95 | 91 | 40.8 m / -80 deg | 34.29 m (14.95) | 34.3 m / -34 deg | 4.2 m/s |
| track_005 | 8.80 | 14.85 | 90 | 96.6 m / -78 deg | 90.74 m (10.05) | 90.8 m / -25 deg | 3.9 m/s |
| track_006 | 8.85 | 12.60 | 32 | 57.8 m / -78 deg | 51.61 m (12.60) | 51.6 m / -28 deg | 3.3 m/s |
| track_007 | 8.85 | 14.95 | 78 | 50.0 m / -79 deg | 43.87 m (13.15) | 44.0 m / -30 deg | 3.3 m/s |
| track_008 | 8.85 | 14.90 | 53 | 53.6 m / -78 deg | 47.64 m (10.05) | 48.3 m / -29 deg | 3.9 m/s |
| track_009 | 8.90 | 14.95 | 105 | 35.9 m / -79 deg | 29.67 m (14.95) | 29.7 m / -36 deg | 3.0 m/s |
| track_010 | 8.80 | 14.95 | 84 | 93.2 m / -76 deg | 85.44 m (14.95) | 85.4 m / -18 deg | 5.5 m/s |
| track_011 | 9.30 | 14.95 | 114 | 25.8 m / -78 deg | 20.88 m (14.95) | 20.9 m / -45 deg | 4.6 m/s |
| track_012 | 9.35 | 9.55 | 5 | 12.9 m / +66 deg | 12.91 m (9.35) | 13.5 m / +80 deg | 14.2 m/s |
| track_013 | 8.85 | 14.95 | 88 | 87.1 m / -68 deg | 79.59 m (14.95) | 79.6 m / -14 deg | 3.5 m/s |
| track_014 | 9.40 | 14.95 | 77 | 87.4 m / -58 deg | 83.02 m (14.95) | 83.0 m / -16 deg | 5.5 m/s |
| track_015 | 9.50 | 14.95 | 110 | 9.8 m / +44 deg | 9.78 m (9.50) | 10.2 m / +70 deg | 6.6 m/s |
| track_016 | 9.45 | 14.95 | 109 | 18.6 m / -80 deg | 13.89 m (14.85) | 13.9 m / -76 deg | 4.4 m/s |
| track_017 | 9.50 | 14.95 | 109 | 12.7 m / +3 deg | 11.23 m (13.10) | 11.2 m / +48 deg | 2.9 m/s |
| track_018 | 9.55 | 14.35 | 97 | 14.5 m / -84 deg | 13.08 m (10.20) | 13.1 m / -79 deg | 5.4 m/s |
| track_019 | 9.55 | 10.00 | 10 | 10.8 m / +35 deg | 10.41 m (10.00) | 10.4 m / +63 deg | 3.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A's camera established a STOP sign detection (sign-0).
- t = 2.30 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.45 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.45 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.65 s: A started braking.
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 3.50 s: A observed track_001 stop closing in.
- t = 6.95 s: A released the brake.
- t = 7.30 s: A left its stop.
- t = 7.30 s: A started moving.
- t = 7.30 s: A observed track_001 start closing in.
- t = 8.30 s: A started turning left.
- t = 8.30 s: A's time-to-contact with track_001 became critical.
- t = 8.80 s: A's radar started tracking track_002, which appeared on its left.
- t = 8.80 s: A's radar started tracking track_005, which appeared on its left.
- t = 8.80 s: A's radar started tracking track_010, which appeared on its left.
- t = 8.80 s: A observed track_002 start closing in (already the case when first observed).
- t = 8.80 s: A observed track_005 start closing in (already the case when first observed).
- t = 8.80 s: A observed track_010 start closing in (already the case when first observed).
- t = 8.85 s: A's radar started tracking track_003, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_004, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_006, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_007, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_008, which appeared on its left.
- t = 8.85 s: A's radar started tracking track_013, which appeared on its left.
- t = 8.85 s: A observed track_003 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_004 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_006 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_007 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_008 start closing in (already the case when first observed).
- t = 8.85 s: A observed track_013 start closing in (already the case when first observed).
- t = 8.90 s: A's radar started tracking track_009, which appeared on its left.
- t = 8.90 s: A observed track_009 start closing in (already the case when first observed).
- t = 9.15 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.30 s: A's radar started tracking track_011, which appeared on its left.
- t = 9.30 s: A observed track_011 start closing in (already the case when first observed).
- t = 9.35 s: A's radar started tracking track_012, which appeared on its right.
- t = 9.40 s: A's radar started tracking track_014, which appeared on its left.
- t = 9.40 s: A observed track_014 start closing in (already the case when first observed).
- t = 9.45 s: A's radar started tracking track_016, which appeared on its left.
- t = 9.45 s: A observed track_016 start closing in (already the case when first observed).
- t = 9.50 s: A's collision sensor recorded a contact (peak impulse 4032 N*s).
- t = 9.50 s: A's radar started tracking track_017, which appeared in front of it.
- t = 9.50 s: A's radar started tracking track_015, which appeared on its right.
- t = 9.50 s: A observed track_017 start closing in (already the case when first observed).
- t = 9.55 s: A observed track_017 leave its forward path corridor.
- t = 9.55 s: A started braking.
- t = 9.55 s: A's radar started tracking track_018, which appeared on its left.
- t = 9.55 s: A's radar started tracking track_019, which appeared on its right.
- t = 9.55 s: A observed track_018 start closing in (already the case when first observed).
- t = 9.55 s: A observed track_019 start closing in (already the case when first observed).
- t = 9.55 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 9.70 s: A observed track_015 start closing in.
- t = 10.00 s: A observed track_002 stop closing in.
- t = 10.00 s: A observed track_005 stop closing in.
- t = 10.00 s: A observed track_008 stop closing in.
- t = 10.00 s: A observed track_015 stop closing in.
- t = 10.00 s: A observed track_017 stop closing in.
- t = 10.00 s: A observed track_018 stop closing in.
- t = 10.00 s: A observed track_019 stop closing in.
- t = 10.00 s: A stopped turning left.
- t = 10.00 s: A stopped moving.
- t = 10.00 s: A came to a stop.
- t = 10.00 s: A's radar lost track_019 (its states are UNKNOWN from then on, not ended).
- t = 10.05 s: A observed track_003 stop closing in.
- t = 10.05 s: A observed track_004 stop closing in.
- t = 10.05 s: A observed track_007 stop closing in.
- t = 10.05 s: A observed track_009 stop closing in.
- t = 10.05 s: A observed track_010 stop closing in.
- t = 10.05 s: A observed track_011 stop closing in.
- t = 10.05 s: A observed track_013 stop closing in.
- t = 10.05 s: A observed track_014 stop closing in.
- t = 10.05 s: A observed track_016 stop closing in.
- t = 10.10 s: A observed track_006 stop closing in.
- t = 11.00 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 12.60 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 14.35 s: A's radar lost track_018 (its states are UNKNOWN from then on, not ended).
- t = 14.85 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 14.90 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
