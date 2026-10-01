# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 77.64883407205343 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 42 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 153; edges: 753 (PRECEDES 649, SAME_TRACK 104)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.80 | BRAKE_START | B | - | controls |  |
| B:e03 | 5.65 | COLLISION | B | - | collision_sensor | peak_impulse=5215.85 |
| B:e04 | 5.75 | TURN_RIGHT_START | B | - | ego |  |
| B:e05 | 5.90 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e06 | 5.90 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e07 | 5.90 | TRACK_APPEARED_RIGHT | B | track_003 | radar |  |
| B:e08 | 5.90 | TRACK_APPEARED_RIGHT | B | track_022 | radar |  |
| B:e09 | 5.90 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e10 | 5.90 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e100 | 6.50 | CLOSING_START | B | track_042 | radar | active_at_first_observation=True |
| B:e101 | 6.50 | TRACK_LOST | B | track_016 | radar |  |
| B:e102 | 6.50 | TRACK_LOST | B | track_018 | radar |  |
| B:e103 | 6.55 | TRACK_LOST | B | track_019 | radar |  |
| B:e104 | 6.55 | TRACK_LOST | B | track_026 | radar |  |
| B:e105 | 6.60 | TRACK_LOST | B | track_017 | radar |  |
| B:e106 | 6.60 | TRACK_LOST | B | track_023 | radar |  |
| B:e107 | 6.60 | TRACK_LOST | B | track_027 | radar |  |
| B:e108 | 6.65 | CRITICAL_TTC_END | B | track_013 | radar |  |
| B:e109 | 6.65 | EGO_PATH_ENTRY | B | track_012 | radar |  |
| B:e11 | 5.90 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e110 | 6.65 | EGO_PATH_ENTRY | B | track_013 | radar |  |
| B:e111 | 6.65 | TRACK_LOST | B | track_033 | radar |  |
| B:e112 | 6.70 | CLOSING_END | B | track_024 | radar |  |
| B:e113 | 6.70 | CLOSING_END | B | track_031 | radar |  |
| B:e114 | 6.70 | CLOSING_END | B | track_034 | radar |  |
| B:e115 | 6.70 | TRACK_LOST | B | track_024 | radar |  |
| B:e116 | 6.70 | TRACK_LOST | B | track_031 | radar |  |
| B:e117 | 6.70 | TRACK_LOST | B | track_034 | radar |  |
| B:e118 | 6.75 | CRITICAL_TTC_END | B | track_012 | radar |  |
| B:e119 | 6.75 | CLOSING_END | B | track_030 | radar |  |
| B:e12 | 5.90 | CLOSING_START | B | track_022 | radar | active_at_first_observation=True |
| B:e120 | 6.80 | CLOSING_END | B | track_028 | radar |  |
| B:e121 | 6.80 | CLOSING_END | B | track_032 | radar |  |
| B:e122 | 6.80 | CLOSING_END | B | track_036 | radar |  |
| B:e123 | 6.80 | CLOSING_END | B | track_040 | radar |  |
| B:e124 | 6.80 | CLOSING_END | B | track_041 | radar |  |
| B:e125 | 6.80 | EGO_PATH_ENTRY | B | track_005 | radar |  |
| B:e126 | 6.80 | TRACK_LOST | B | track_028 | radar |  |
| B:e127 | 6.85 | CLOSING_END | B | track_025 | radar |  |
| B:e128 | 6.85 | CLOSING_END | B | track_037 | radar |  |
| B:e129 | 6.85 | CLOSING_END | B | track_038 | radar |  |
| B:e13 | 5.95 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e130 | 6.85 | CLOSING_END | B | track_039 | radar |  |
| B:e131 | 6.85 | CLOSING_END | B | track_042 | radar |  |
| B:e132 | 6.85 | TRACK_LOST | B | track_041 | radar |  |
| B:e133 | 6.90 | CLOSING_END | B | track_001 | radar |  |
| B:e134 | 6.90 | CLOSING_END | B | track_003 | radar |  |
| B:e135 | 6.90 | CLOSING_END | B | track_005 | radar |  |
| B:e136 | 6.90 | CLOSING_END | B | track_006 | radar |  |
| B:e137 | 6.90 | CLOSING_END | B | track_012 | radar |  |
| B:e138 | 6.90 | CLOSING_END | B | track_013 | radar |  |
| B:e139 | 6.90 | CLOSING_END | B | track_020 | radar |  |
| B:e14 | 5.95 | TRACK_APPEARED_RIGHT | B | track_005 | radar |  |
| B:e140 | 6.90 | CLOSING_END | B | track_029 | radar |  |
| B:e141 | 6.90 | CLOSING_END | B | track_035 | radar |  |
| B:e142 | 6.90 | TURN_RIGHT_END | B | - | ego |  |
| B:e143 | 6.90 | MOVING_END | B | - | ego |  |
| B:e144 | 6.90 | STOP_START | B | - | ego |  |
| B:e145 | 7.00 | CLOSING_END | B | track_022 | radar |  |
| B:e146 | 7.35 | TRACK_LOST | B | track_022 | radar |  |
| B:e147 | 7.65 | TRACK_LOST | B | track_025 | radar |  |
| B:e148 | 7.70 | EGO_PATH_ENTRY | B | track_006 | radar |  |
| B:e149 | 8.35 | EGO_PATH_EXIT | B | track_013 | radar |  |
| B:e15 | 5.95 | TRACK_APPEARED_RIGHT | B | track_006 | radar |  |
| B:e150 | 8.65 | TRACK_LOST | B | track_029 | radar |  |
| B:e151 | 9.70 | TRACK_LOST | B | track_037 | radar |  |
| B:e152 | 9.90 | TRACK_LOST | B | track_005 | radar |  |
| B:e153 | 9.90 | TRACK_LOST | B | track_035 | radar |  |
| B:e16 | 5.95 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e17 | 5.95 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e18 | 5.95 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e19 | 6.05 | TRACK_APPEARED_LEFT | B | track_007 | radar |  |
| B:e20 | 6.05 | TRACK_APPEARED_LEFT | B | track_009 | radar |  |
| B:e21 | 6.05 | TRACK_APPEARED_RIGHT | B | track_008 | radar |  |
| B:e22 | 6.05 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e23 | 6.05 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e24 | 6.05 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e25 | 6.10 | TRACK_APPEARED_LEFT | B | track_010 | radar |  |
| B:e26 | 6.10 | TRACK_APPEARED_LEFT | B | track_011 | radar |  |
| B:e27 | 6.10 | TRACK_APPEARED_LEFT | B | track_015 | radar |  |
| B:e28 | 6.10 | TRACK_APPEARED_RIGHT | B | track_020 | radar |  |
| B:e29 | 6.10 | TRACK_APPEARED_RIGHT | B | track_029 | radar |  |
| B:e30 | 6.10 | CLOSING_START | B | track_010 | radar | active_at_first_observation=True |
| B:e31 | 6.10 | CLOSING_START | B | track_011 | radar | active_at_first_observation=True |
| B:e32 | 6.10 | CLOSING_START | B | track_015 | radar | active_at_first_observation=True |
| B:e33 | 6.10 | CLOSING_START | B | track_020 | radar | active_at_first_observation=True |
| B:e34 | 6.10 | CLOSING_START | B | track_029 | radar | active_at_first_observation=True |
| B:e35 | 6.15 | TRACK_APPEARED_LEFT | B | track_014 | radar |  |
| B:e36 | 6.15 | TRACK_APPEARED_LEFT | B | track_016 | radar |  |
| B:e37 | 6.15 | TRACK_APPEARED_LEFT | B | track_021 | radar |  |
| B:e38 | 6.15 | TRACK_APPEARED_RIGHT | B | track_012 | radar |  |
| B:e39 | 6.15 | TRACK_APPEARED_RIGHT | B | track_013 | radar |  |
| B:e40 | 6.15 | CLOSING_START | B | track_012 | radar | active_at_first_observation=True |
| B:e41 | 6.15 | CLOSING_START | B | track_013 | radar | active_at_first_observation=True |
| B:e42 | 6.15 | CLOSING_START | B | track_014 | radar | active_at_first_observation=True |
| B:e43 | 6.15 | CLOSING_START | B | track_016 | radar | active_at_first_observation=True |
| B:e44 | 6.15 | CLOSING_START | B | track_021 | radar | active_at_first_observation=True |
| B:e45 | 6.15 | CRITICAL_TTC_START | B | track_012 | radar | active_at_first_observation=True |
| B:e46 | 6.15 | CRITICAL_TTC_START | B | track_013 | radar | active_at_first_observation=True |
| B:e47 | 6.20 | TRACK_APPEARED_LEFT | B | track_017 | radar |  |
| B:e48 | 6.20 | TRACK_APPEARED_LEFT | B | track_018 | radar |  |
| B:e49 | 6.20 | TRACK_APPEARED_LEFT | B | track_019 | radar |  |
| B:e50 | 6.20 | TRACK_APPEARED_LEFT | B | track_026 | radar |  |
| B:e51 | 6.20 | CLOSING_START | B | track_017 | radar | active_at_first_observation=True |
| B:e52 | 6.20 | CLOSING_START | B | track_018 | radar | active_at_first_observation=True |
| B:e53 | 6.20 | CLOSING_START | B | track_019 | radar | active_at_first_observation=True |
| B:e54 | 6.20 | CLOSING_START | B | track_026 | radar | active_at_first_observation=True |
| B:e55 | 6.25 | TRACK_LOST | B | track_004 | radar |  |
| B:e56 | 6.30 | TRACK_APPEARED_LEFT | B | track_023 | radar |  |
| B:e57 | 6.30 | TRACK_APPEARED_LEFT | B | track_024 | radar |  |
| B:e58 | 6.30 | TRACK_APPEARED_LEFT | B | track_025 | radar |  |
| B:e59 | 6.30 | TRACK_APPEARED_LEFT | B | track_027 | radar |  |
| B:e60 | 6.30 | TRACK_APPEARED_LEFT | B | track_030 | radar |  |
| B:e61 | 6.30 | TRACK_APPEARED_LEFT | B | track_031 | radar |  |
| B:e62 | 6.30 | CLOSING_START | B | track_023 | radar | active_at_first_observation=True |
| B:e63 | 6.30 | CLOSING_START | B | track_024 | radar | active_at_first_observation=True |
| B:e64 | 6.30 | CLOSING_START | B | track_025 | radar | active_at_first_observation=True |
| B:e65 | 6.30 | CLOSING_START | B | track_027 | radar | active_at_first_observation=True |
| B:e66 | 6.30 | CLOSING_START | B | track_030 | radar | active_at_first_observation=True |
| B:e67 | 6.30 | CLOSING_START | B | track_031 | radar | active_at_first_observation=True |
| B:e68 | 6.30 | TRACK_LOST | B | track_002 | radar |  |
| B:e69 | 6.30 | TRACK_LOST | B | track_007 | radar |  |
| B:e70 | 6.30 | TRACK_LOST | B | track_008 | radar |  |
| B:e71 | 6.30 | TRACK_LOST | B | track_009 | radar |  |
| B:e72 | 6.35 | TRACK_APPEARED_LEFT | B | track_028 | radar |  |
| B:e73 | 6.35 | CLOSING_START | B | track_028 | radar | active_at_first_observation=True |
| B:e74 | 6.40 | TRACK_APPEARED_LEFT | B | track_032 | radar |  |
| B:e75 | 6.40 | TRACK_APPEARED_LEFT | B | track_033 | radar |  |
| B:e76 | 6.40 | TRACK_APPEARED_LEFT | B | track_034 | radar |  |
| B:e77 | 6.40 | TRACK_APPEARED_LEFT | B | track_036 | radar |  |
| B:e78 | 6.40 | TRACK_APPEARED_LEFT | B | track_037 | radar |  |
| B:e79 | 6.40 | TRACK_APPEARED_LEFT | B | track_040 | radar |  |
| B:e80 | 6.40 | TRACK_APPEARED_RIGHT | B | track_035 | radar |  |
| B:e81 | 6.40 | CLOSING_START | B | track_032 | radar | active_at_first_observation=True |
| B:e82 | 6.40 | CLOSING_START | B | track_033 | radar | active_at_first_observation=True |
| B:e83 | 6.40 | CLOSING_START | B | track_034 | radar | active_at_first_observation=True |
| B:e84 | 6.40 | CLOSING_START | B | track_035 | radar | active_at_first_observation=True |
| B:e85 | 6.40 | CLOSING_START | B | track_036 | radar | active_at_first_observation=True |
| B:e86 | 6.40 | CLOSING_START | B | track_037 | radar | active_at_first_observation=True |
| B:e87 | 6.40 | CLOSING_START | B | track_040 | radar | active_at_first_observation=True |
| B:e88 | 6.40 | TRACK_LOST | B | track_010 | radar |  |
| B:e89 | 6.40 | TRACK_LOST | B | track_011 | radar |  |
| B:e90 | 6.45 | TRACK_APPEARED_LEFT | B | track_041 | radar |  |
| B:e91 | 6.45 | CLOSING_START | B | track_041 | radar | active_at_first_observation=True |
| B:e92 | 6.45 | TRACK_LOST | B | track_014 | radar |  |
| B:e93 | 6.45 | TRACK_LOST | B | track_015 | radar |  |
| B:e94 | 6.45 | TRACK_LOST | B | track_021 | radar |  |
| B:e95 | 6.50 | TRACK_APPEARED_LEFT | B | track_038 | radar |  |
| B:e96 | 6.50 | TRACK_APPEARED_LEFT | B | track_039 | radar |  |
| B:e97 | 6.50 | TRACK_APPEARED_LEFT | B | track_042 | radar |  |
| B:e98 | 6.50 | CLOSING_START | B | track_038 | radar | active_at_first_observation=True |
| B:e99 | 6.50 | CLOSING_START | B | track_039 | radar | active_at_first_observation=True |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e10
    B:e05 --PRECEDES--> B:e100
    B:e05 --PRECEDES--> B:e101
    B:e05 --PRECEDES--> B:e102
    B:e06 --PRECEDES--> B:e100
    B:e06 --PRECEDES--> B:e101
    B:e06 --PRECEDES--> B:e102
    B:e07 --PRECEDES--> B:e100
    B:e07 --PRECEDES--> B:e101
    B:e07 --PRECEDES--> B:e102
    B:e08 --PRECEDES--> B:e100
    B:e08 --PRECEDES--> B:e101
    B:e08 --PRECEDES--> B:e102
    B:e09 --PRECEDES--> B:e100
    B:e09 --PRECEDES--> B:e101
    B:e09 --PRECEDES--> B:e102
    B:e10 --PRECEDES--> B:e100
    B:e10 --PRECEDES--> B:e101
    B:e10 --PRECEDES--> B:e102
    B:e100 --PRECEDES--> B:e103
    B:e100 --PRECEDES--> B:e104
    B:e101 --PRECEDES--> B:e103
    B:e101 --PRECEDES--> B:e104
    B:e102 --PRECEDES--> B:e103
    B:e102 --PRECEDES--> B:e104
    B:e103 --PRECEDES--> B:e105
    B:e103 --PRECEDES--> B:e106
    B:e103 --PRECEDES--> B:e107
    B:e104 --PRECEDES--> B:e105
    B:e104 --PRECEDES--> B:e106
    B:e104 --PRECEDES--> B:e107
    B:e105 --PRECEDES--> B:e108
    B:e105 --PRECEDES--> B:e109
    B:e106 --PRECEDES--> B:e108
    B:e106 --PRECEDES--> B:e109
    B:e107 --PRECEDES--> B:e108
    B:e107 --PRECEDES--> B:e109
    B:e108 --PRECEDES--> B:e11
    B:e109 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e110
    B:e11 --PRECEDES--> B:e111
    B:e110 --PRECEDES--> B:e112
    B:e110 --PRECEDES--> B:e113
    B:e110 --PRECEDES--> B:e114
    B:e110 --PRECEDES--> B:e115
    B:e110 --PRECEDES--> B:e116
    B:e110 --PRECEDES--> B:e117
    B:e111 --PRECEDES--> B:e112
    B:e111 --PRECEDES--> B:e113
    B:e111 --PRECEDES--> B:e114
    B:e111 --PRECEDES--> B:e115
    B:e111 --PRECEDES--> B:e116
    B:e111 --PRECEDES--> B:e117
    B:e112 --PRECEDES--> B:e118
    B:e112 --PRECEDES--> B:e119
    B:e113 --PRECEDES--> B:e118
    B:e113 --PRECEDES--> B:e119
    B:e114 --PRECEDES--> B:e118
    B:e114 --PRECEDES--> B:e119
    B:e115 --PRECEDES--> B:e118
    B:e115 --PRECEDES--> B:e119
    B:e116 --PRECEDES--> B:e118
    B:e116 --PRECEDES--> B:e119
    B:e117 --PRECEDES--> B:e118
    B:e117 --PRECEDES--> B:e119
    B:e118 --PRECEDES--> B:e12
    B:e119 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e120
    B:e12 --PRECEDES--> B:e121
    B:e12 --PRECEDES--> B:e122
    B:e12 --PRECEDES--> B:e123
    B:e12 --PRECEDES--> B:e124
    B:e12 --PRECEDES--> B:e125
    B:e12 --PRECEDES--> B:e126
    B:e120 --PRECEDES--> B:e127
    B:e120 --PRECEDES--> B:e128
    B:e120 --PRECEDES--> B:e129
    B:e121 --PRECEDES--> B:e127
    B:e121 --PRECEDES--> B:e128
    B:e121 --PRECEDES--> B:e129
    B:e122 --PRECEDES--> B:e127
    B:e122 --PRECEDES--> B:e128
    B:e122 --PRECEDES--> B:e129
    B:e123 --PRECEDES--> B:e127
    B:e123 --PRECEDES--> B:e128
    B:e123 --PRECEDES--> B:e129
    B:e124 --PRECEDES--> B:e127
    B:e124 --PRECEDES--> B:e128
    B:e124 --PRECEDES--> B:e129
    B:e125 --PRECEDES--> B:e127
    B:e125 --PRECEDES--> B:e128
    B:e125 --PRECEDES--> B:e129
    B:e126 --PRECEDES--> B:e127
    B:e126 --PRECEDES--> B:e128
    B:e126 --PRECEDES--> B:e129
    B:e127 --PRECEDES--> B:e13
    B:e128 --PRECEDES--> B:e13
    B:e129 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e130
    B:e13 --PRECEDES--> B:e131
    B:e13 --PRECEDES--> B:e132
    B:e130 --PRECEDES--> B:e133
    B:e130 --PRECEDES--> B:e134
    B:e130 --PRECEDES--> B:e135
    B:e130 --PRECEDES--> B:e136
    B:e130 --PRECEDES--> B:e137
    B:e130 --PRECEDES--> B:e138
    B:e130 --PRECEDES--> B:e139
    B:e131 --PRECEDES--> B:e133
    B:e131 --PRECEDES--> B:e134
    B:e131 --PRECEDES--> B:e135
    B:e131 --PRECEDES--> B:e136
    B:e131 --PRECEDES--> B:e137
    B:e131 --PRECEDES--> B:e138
    B:e131 --PRECEDES--> B:e139
    B:e132 --PRECEDES--> B:e133
    B:e132 --PRECEDES--> B:e134
    B:e132 --PRECEDES--> B:e135
    B:e132 --PRECEDES--> B:e136
    B:e132 --PRECEDES--> B:e137
    B:e132 --PRECEDES--> B:e138
    B:e132 --PRECEDES--> B:e139
    B:e133 --PRECEDES--> B:e14
    B:e134 --PRECEDES--> B:e14
    B:e135 --PRECEDES--> B:e14
    B:e136 --PRECEDES--> B:e14
    B:e137 --PRECEDES--> B:e14
    B:e138 --PRECEDES--> B:e14
    B:e139 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e140
    B:e14 --PRECEDES--> B:e141
    B:e14 --PRECEDES--> B:e142
    B:e14 --PRECEDES--> B:e143
    B:e14 --PRECEDES--> B:e144
    B:e140 --PRECEDES--> B:e145
    B:e141 --PRECEDES--> B:e145
    B:e142 --PRECEDES--> B:e145
    B:e143 --PRECEDES--> B:e145
    B:e144 --PRECEDES--> B:e145
    B:e145 --PRECEDES--> B:e146
    B:e146 --PRECEDES--> B:e147
    B:e147 --PRECEDES--> B:e148
    B:e148 --PRECEDES--> B:e149
    B:e149 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e150
    B:e150 --PRECEDES--> B:e151
    B:e151 --PRECEDES--> B:e152
    B:e151 --PRECEDES--> B:e153
    B:e152 --PRECEDES--> B:e16
    B:e152 --PRECEDES--> B:e17
    B:e152 --PRECEDES--> B:e18
    B:e153 --PRECEDES--> B:e16
    B:e153 --PRECEDES--> B:e17
    B:e153 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e23
    B:e16 --PRECEDES--> B:e24
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e17 --PRECEDES--> B:e23
    B:e17 --PRECEDES--> B:e24
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e23
    B:e18 --PRECEDES--> B:e24
    B:e19 --PRECEDES--> B:e25
    B:e19 --PRECEDES--> B:e26
    B:e19 --PRECEDES--> B:e27
    B:e19 --PRECEDES--> B:e28
    B:e19 --PRECEDES--> B:e29
    B:e19 --PRECEDES--> B:e30
    B:e19 --PRECEDES--> B:e31
    B:e19 --PRECEDES--> B:e32
    B:e19 --PRECEDES--> B:e33
    B:e19 --PRECEDES--> B:e34
    B:e20 --PRECEDES--> B:e25
    B:e20 --PRECEDES--> B:e26
    B:e20 --PRECEDES--> B:e27
    B:e20 --PRECEDES--> B:e28
    B:e20 --PRECEDES--> B:e29
    B:e20 --PRECEDES--> B:e30
    B:e20 --PRECEDES--> B:e31
    B:e20 --PRECEDES--> B:e32
    B:e20 --PRECEDES--> B:e33
    B:e20 --PRECEDES--> B:e34
    B:e21 --PRECEDES--> B:e25
    B:e21 --PRECEDES--> B:e26
    B:e21 --PRECEDES--> B:e27
    B:e21 --PRECEDES--> B:e28
    B:e21 --PRECEDES--> B:e29
    B:e21 --PRECEDES--> B:e30
    B:e21 --PRECEDES--> B:e31
    B:e21 --PRECEDES--> B:e32
    B:e21 --PRECEDES--> B:e33
    B:e21 --PRECEDES--> B:e34
    B:e22 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e26
    B:e22 --PRECEDES--> B:e27
    B:e22 --PRECEDES--> B:e28
    B:e22 --PRECEDES--> B:e29
    B:e22 --PRECEDES--> B:e30
    B:e22 --PRECEDES--> B:e31
    B:e22 --PRECEDES--> B:e32
    B:e22 --PRECEDES--> B:e33
    B:e22 --PRECEDES--> B:e34
    B:e23 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e26
    B:e23 --PRECEDES--> B:e27
    B:e23 --PRECEDES--> B:e28
    B:e23 --PRECEDES--> B:e29
    B:e23 --PRECEDES--> B:e30
    B:e23 --PRECEDES--> B:e31
    B:e23 --PRECEDES--> B:e32
    B:e23 --PRECEDES--> B:e33
    B:e23 --PRECEDES--> B:e34
    B:e24 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e24 --PRECEDES--> B:e28
    B:e24 --PRECEDES--> B:e29
    B:e24 --PRECEDES--> B:e30
    B:e24 --PRECEDES--> B:e31
    B:e24 --PRECEDES--> B:e32
    B:e24 --PRECEDES--> B:e33
    B:e24 --PRECEDES--> B:e34
    B:e25 --PRECEDES--> B:e35
    B:e25 --PRECEDES--> B:e36
    B:e25 --PRECEDES--> B:e37
    B:e25 --PRECEDES--> B:e38
    B:e25 --PRECEDES--> B:e39
    B:e25 --PRECEDES--> B:e40
    B:e25 --PRECEDES--> B:e41
    B:e25 --PRECEDES--> B:e42
    B:e25 --PRECEDES--> B:e43
    B:e25 --PRECEDES--> B:e44
    B:e25 --PRECEDES--> B:e45
    B:e25 --PRECEDES--> B:e46
    B:e26 --PRECEDES--> B:e35
    B:e26 --PRECEDES--> B:e36
    B:e26 --PRECEDES--> B:e37
    B:e26 --PRECEDES--> B:e38
    B:e26 --PRECEDES--> B:e39
    B:e26 --PRECEDES--> B:e40
    B:e26 --PRECEDES--> B:e41
    B:e26 --PRECEDES--> B:e42
    B:e26 --PRECEDES--> B:e43
    B:e26 --PRECEDES--> B:e44
    B:e26 --PRECEDES--> B:e45
    B:e26 --PRECEDES--> B:e46
    B:e27 --PRECEDES--> B:e35
    B:e27 --PRECEDES--> B:e36
    B:e27 --PRECEDES--> B:e37
    B:e27 --PRECEDES--> B:e38
    B:e27 --PRECEDES--> B:e39
    B:e27 --PRECEDES--> B:e40
    B:e27 --PRECEDES--> B:e41
    B:e27 --PRECEDES--> B:e42
    B:e27 --PRECEDES--> B:e43
    B:e27 --PRECEDES--> B:e44
    B:e27 --PRECEDES--> B:e45
    B:e27 --PRECEDES--> B:e46
    B:e28 --PRECEDES--> B:e35
    B:e28 --PRECEDES--> B:e36
    B:e28 --PRECEDES--> B:e37
    B:e28 --PRECEDES--> B:e38
    B:e28 --PRECEDES--> B:e39
    B:e28 --PRECEDES--> B:e40
    B:e28 --PRECEDES--> B:e41
    B:e28 --PRECEDES--> B:e42
    B:e28 --PRECEDES--> B:e43
    B:e28 --PRECEDES--> B:e44
    B:e28 --PRECEDES--> B:e45
    B:e28 --PRECEDES--> B:e46
    B:e29 --PRECEDES--> B:e35
    B:e29 --PRECEDES--> B:e36
    B:e29 --PRECEDES--> B:e37
    B:e29 --PRECEDES--> B:e38
    B:e29 --PRECEDES--> B:e39
    B:e29 --PRECEDES--> B:e40
    B:e29 --PRECEDES--> B:e41
    B:e29 --PRECEDES--> B:e42
    B:e29 --PRECEDES--> B:e43
    B:e29 --PRECEDES--> B:e44
    B:e29 --PRECEDES--> B:e45
    B:e29 --PRECEDES--> B:e46
    B:e30 --PRECEDES--> B:e35
    B:e30 --PRECEDES--> B:e36
    B:e30 --PRECEDES--> B:e37
    B:e30 --PRECEDES--> B:e38
    B:e30 --PRECEDES--> B:e39
    B:e30 --PRECEDES--> B:e40
    B:e30 --PRECEDES--> B:e41
    B:e30 --PRECEDES--> B:e42
    B:e30 --PRECEDES--> B:e43
    B:e30 --PRECEDES--> B:e44
    B:e30 --PRECEDES--> B:e45
    B:e30 --PRECEDES--> B:e46
    B:e31 --PRECEDES--> B:e35
    B:e31 --PRECEDES--> B:e36
    B:e31 --PRECEDES--> B:e37
    B:e31 --PRECEDES--> B:e38
    B:e31 --PRECEDES--> B:e39
    B:e31 --PRECEDES--> B:e40
    B:e31 --PRECEDES--> B:e41
    B:e31 --PRECEDES--> B:e42
    B:e31 --PRECEDES--> B:e43
    B:e31 --PRECEDES--> B:e44
    B:e31 --PRECEDES--> B:e45
    B:e31 --PRECEDES--> B:e46
    B:e32 --PRECEDES--> B:e35
    B:e32 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e37
    B:e32 --PRECEDES--> B:e38
    B:e32 --PRECEDES--> B:e39
    B:e32 --PRECEDES--> B:e40
    B:e32 --PRECEDES--> B:e41
    B:e32 --PRECEDES--> B:e42
    B:e32 --PRECEDES--> B:e43
    B:e32 --PRECEDES--> B:e44
    B:e32 --PRECEDES--> B:e45
    B:e32 --PRECEDES--> B:e46
    B:e33 --PRECEDES--> B:e35
    B:e33 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e37
    B:e33 --PRECEDES--> B:e38
    B:e33 --PRECEDES--> B:e39
    B:e33 --PRECEDES--> B:e40
    B:e33 --PRECEDES--> B:e41
    B:e33 --PRECEDES--> B:e42
    B:e33 --PRECEDES--> B:e43
    B:e33 --PRECEDES--> B:e44
    B:e33 --PRECEDES--> B:e45
    B:e33 --PRECEDES--> B:e46
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e34 --PRECEDES--> B:e38
    B:e34 --PRECEDES--> B:e39
    B:e34 --PRECEDES--> B:e40
    B:e34 --PRECEDES--> B:e41
    B:e34 --PRECEDES--> B:e42
    B:e34 --PRECEDES--> B:e43
    B:e34 --PRECEDES--> B:e44
    B:e34 --PRECEDES--> B:e45
    B:e34 --PRECEDES--> B:e46
    B:e35 --PRECEDES--> B:e47
    B:e35 --PRECEDES--> B:e48
    B:e35 --PRECEDES--> B:e49
    B:e35 --PRECEDES--> B:e50
    B:e35 --PRECEDES--> B:e51
    B:e35 --PRECEDES--> B:e52
    B:e35 --PRECEDES--> B:e53
    B:e35 --PRECEDES--> B:e54
    B:e36 --PRECEDES--> B:e47
    B:e36 --PRECEDES--> B:e48
    B:e36 --PRECEDES--> B:e49
    B:e36 --PRECEDES--> B:e50
    B:e36 --PRECEDES--> B:e51
    B:e36 --PRECEDES--> B:e52
    B:e36 --PRECEDES--> B:e53
    B:e36 --PRECEDES--> B:e54
    B:e37 --PRECEDES--> B:e47
    B:e37 --PRECEDES--> B:e48
    B:e37 --PRECEDES--> B:e49
    B:e37 --PRECEDES--> B:e50
    B:e37 --PRECEDES--> B:e51
    B:e37 --PRECEDES--> B:e52
    B:e37 --PRECEDES--> B:e53
    B:e37 --PRECEDES--> B:e54
    B:e38 --PRECEDES--> B:e47
    B:e38 --PRECEDES--> B:e48
    B:e38 --PRECEDES--> B:e49
    B:e38 --PRECEDES--> B:e50
    B:e38 --PRECEDES--> B:e51
    B:e38 --PRECEDES--> B:e52
    B:e38 --PRECEDES--> B:e53
    B:e38 --PRECEDES--> B:e54
    B:e39 --PRECEDES--> B:e47
    B:e39 --PRECEDES--> B:e48
    B:e39 --PRECEDES--> B:e49
    B:e39 --PRECEDES--> B:e50
    B:e39 --PRECEDES--> B:e51
    B:e39 --PRECEDES--> B:e52
    B:e39 --PRECEDES--> B:e53
    B:e39 --PRECEDES--> B:e54
    B:e40 --PRECEDES--> B:e47
    B:e40 --PRECEDES--> B:e48
    B:e40 --PRECEDES--> B:e49
    B:e40 --PRECEDES--> B:e50
    B:e40 --PRECEDES--> B:e51
    B:e40 --PRECEDES--> B:e52
    B:e40 --PRECEDES--> B:e53
    B:e40 --PRECEDES--> B:e54
    B:e41 --PRECEDES--> B:e47
    B:e41 --PRECEDES--> B:e48
    B:e41 --PRECEDES--> B:e49
    B:e41 --PRECEDES--> B:e50
    B:e41 --PRECEDES--> B:e51
    B:e41 --PRECEDES--> B:e52
    B:e41 --PRECEDES--> B:e53
    B:e41 --PRECEDES--> B:e54
    B:e42 --PRECEDES--> B:e47
    B:e42 --PRECEDES--> B:e48
    B:e42 --PRECEDES--> B:e49
    B:e42 --PRECEDES--> B:e50
    B:e42 --PRECEDES--> B:e51
    B:e42 --PRECEDES--> B:e52
    B:e42 --PRECEDES--> B:e53
    B:e42 --PRECEDES--> B:e54
    B:e43 --PRECEDES--> B:e47
    B:e43 --PRECEDES--> B:e48
    B:e43 --PRECEDES--> B:e49
    B:e43 --PRECEDES--> B:e50
    B:e43 --PRECEDES--> B:e51
    B:e43 --PRECEDES--> B:e52
    B:e43 --PRECEDES--> B:e53
    B:e43 --PRECEDES--> B:e54
    B:e44 --PRECEDES--> B:e47
    B:e44 --PRECEDES--> B:e48
    B:e44 --PRECEDES--> B:e49
    B:e44 --PRECEDES--> B:e50
    B:e44 --PRECEDES--> B:e51
    B:e44 --PRECEDES--> B:e52
    B:e44 --PRECEDES--> B:e53
    B:e44 --PRECEDES--> B:e54
    B:e45 --PRECEDES--> B:e47
    B:e45 --PRECEDES--> B:e48
    B:e45 --PRECEDES--> B:e49
    B:e45 --PRECEDES--> B:e50
    B:e45 --PRECEDES--> B:e51
    B:e45 --PRECEDES--> B:e52
    B:e45 --PRECEDES--> B:e53
    B:e45 --PRECEDES--> B:e54
    B:e46 --PRECEDES--> B:e47
    B:e46 --PRECEDES--> B:e48
    B:e46 --PRECEDES--> B:e49
    B:e46 --PRECEDES--> B:e50
    B:e46 --PRECEDES--> B:e51
    B:e46 --PRECEDES--> B:e52
    B:e46 --PRECEDES--> B:e53
    B:e46 --PRECEDES--> B:e54
    B:e47 --PRECEDES--> B:e55
    B:e48 --PRECEDES--> B:e55
    B:e49 --PRECEDES--> B:e55
    B:e50 --PRECEDES--> B:e55
    B:e51 --PRECEDES--> B:e55
    B:e52 --PRECEDES--> B:e55
    B:e53 --PRECEDES--> B:e55
    B:e54 --PRECEDES--> B:e55
    B:e55 --PRECEDES--> B:e56
    B:e55 --PRECEDES--> B:e57
    B:e55 --PRECEDES--> B:e58
    B:e55 --PRECEDES--> B:e59
    B:e55 --PRECEDES--> B:e60
    B:e55 --PRECEDES--> B:e61
    B:e55 --PRECEDES--> B:e62
    B:e55 --PRECEDES--> B:e63
    B:e55 --PRECEDES--> B:e64
    B:e55 --PRECEDES--> B:e65
    B:e55 --PRECEDES--> B:e66
    B:e55 --PRECEDES--> B:e67
    B:e55 --PRECEDES--> B:e68
    B:e55 --PRECEDES--> B:e69
    B:e55 --PRECEDES--> B:e70
    B:e55 --PRECEDES--> B:e71
    B:e56 --PRECEDES--> B:e72
    B:e56 --PRECEDES--> B:e73
    B:e57 --PRECEDES--> B:e72
    B:e57 --PRECEDES--> B:e73
    B:e58 --PRECEDES--> B:e72
    B:e58 --PRECEDES--> B:e73
    B:e59 --PRECEDES--> B:e72
    B:e59 --PRECEDES--> B:e73
    B:e60 --PRECEDES--> B:e72
    B:e60 --PRECEDES--> B:e73
    B:e61 --PRECEDES--> B:e72
    B:e61 --PRECEDES--> B:e73
    B:e62 --PRECEDES--> B:e72
    B:e62 --PRECEDES--> B:e73
    B:e63 --PRECEDES--> B:e72
    B:e63 --PRECEDES--> B:e73
    B:e64 --PRECEDES--> B:e72
    B:e64 --PRECEDES--> B:e73
    B:e65 --PRECEDES--> B:e72
    B:e65 --PRECEDES--> B:e73
    B:e66 --PRECEDES--> B:e72
    B:e66 --PRECEDES--> B:e73
    B:e67 --PRECEDES--> B:e72
    B:e67 --PRECEDES--> B:e73
    B:e68 --PRECEDES--> B:e72
    B:e68 --PRECEDES--> B:e73
    B:e69 --PRECEDES--> B:e72
    B:e69 --PRECEDES--> B:e73
    B:e70 --PRECEDES--> B:e72
    B:e70 --PRECEDES--> B:e73
    B:e71 --PRECEDES--> B:e72
    B:e71 --PRECEDES--> B:e73
    B:e72 --PRECEDES--> B:e74
    B:e72 --PRECEDES--> B:e75
    B:e72 --PRECEDES--> B:e76
    B:e72 --PRECEDES--> B:e77
    B:e72 --PRECEDES--> B:e78
    B:e72 --PRECEDES--> B:e79
    B:e72 --PRECEDES--> B:e80
    B:e72 --PRECEDES--> B:e81
    B:e72 --PRECEDES--> B:e82
    B:e72 --PRECEDES--> B:e83
    B:e72 --PRECEDES--> B:e84
    B:e72 --PRECEDES--> B:e85
    B:e72 --PRECEDES--> B:e86
    B:e72 --PRECEDES--> B:e87
    B:e72 --PRECEDES--> B:e88
    B:e72 --PRECEDES--> B:e89
    B:e73 --PRECEDES--> B:e74
    B:e73 --PRECEDES--> B:e75
    B:e73 --PRECEDES--> B:e76
    B:e73 --PRECEDES--> B:e77
    B:e73 --PRECEDES--> B:e78
    B:e73 --PRECEDES--> B:e79
    B:e73 --PRECEDES--> B:e80
    B:e73 --PRECEDES--> B:e81
    B:e73 --PRECEDES--> B:e82
    B:e73 --PRECEDES--> B:e83
    B:e73 --PRECEDES--> B:e84
    B:e73 --PRECEDES--> B:e85
    B:e73 --PRECEDES--> B:e86
    B:e73 --PRECEDES--> B:e87
    B:e73 --PRECEDES--> B:e88
    B:e73 --PRECEDES--> B:e89
    B:e74 --PRECEDES--> B:e90
    B:e74 --PRECEDES--> B:e91
    B:e74 --PRECEDES--> B:e92
    B:e74 --PRECEDES--> B:e93
    B:e74 --PRECEDES--> B:e94
    B:e75 --PRECEDES--> B:e90
    B:e75 --PRECEDES--> B:e91
    B:e75 --PRECEDES--> B:e92
    B:e75 --PRECEDES--> B:e93
    B:e75 --PRECEDES--> B:e94
    B:e76 --PRECEDES--> B:e90
    B:e76 --PRECEDES--> B:e91
    B:e76 --PRECEDES--> B:e92
    B:e76 --PRECEDES--> B:e93
    B:e76 --PRECEDES--> B:e94
    B:e77 --PRECEDES--> B:e90
    B:e77 --PRECEDES--> B:e91
    B:e77 --PRECEDES--> B:e92
    B:e77 --PRECEDES--> B:e93
    B:e77 --PRECEDES--> B:e94
    B:e78 --PRECEDES--> B:e90
    B:e78 --PRECEDES--> B:e91
    B:e78 --PRECEDES--> B:e92
    B:e78 --PRECEDES--> B:e93
    B:e78 --PRECEDES--> B:e94
    B:e79 --PRECEDES--> B:e90
    B:e79 --PRECEDES--> B:e91
    B:e79 --PRECEDES--> B:e92
    B:e79 --PRECEDES--> B:e93
    B:e79 --PRECEDES--> B:e94
    B:e80 --PRECEDES--> B:e90
    B:e80 --PRECEDES--> B:e91
    B:e80 --PRECEDES--> B:e92
    B:e80 --PRECEDES--> B:e93
    B:e80 --PRECEDES--> B:e94
    B:e81 --PRECEDES--> B:e90
    B:e81 --PRECEDES--> B:e91
    B:e81 --PRECEDES--> B:e92
    B:e81 --PRECEDES--> B:e93
    B:e81 --PRECEDES--> B:e94
    B:e82 --PRECEDES--> B:e90
    B:e82 --PRECEDES--> B:e91
    B:e82 --PRECEDES--> B:e92
    B:e82 --PRECEDES--> B:e93
    B:e82 --PRECEDES--> B:e94
    B:e83 --PRECEDES--> B:e90
    B:e83 --PRECEDES--> B:e91
    B:e83 --PRECEDES--> B:e92
    B:e83 --PRECEDES--> B:e93
    B:e83 --PRECEDES--> B:e94
    B:e84 --PRECEDES--> B:e90
    B:e84 --PRECEDES--> B:e91
    B:e84 --PRECEDES--> B:e92
    B:e84 --PRECEDES--> B:e93
    B:e84 --PRECEDES--> B:e94
    B:e85 --PRECEDES--> B:e90
    B:e85 --PRECEDES--> B:e91
    B:e85 --PRECEDES--> B:e92
    B:e85 --PRECEDES--> B:e93
    B:e85 --PRECEDES--> B:e94
    B:e86 --PRECEDES--> B:e90
    B:e86 --PRECEDES--> B:e91
    B:e86 --PRECEDES--> B:e92
    B:e86 --PRECEDES--> B:e93
    B:e86 --PRECEDES--> B:e94
    B:e87 --PRECEDES--> B:e90
    B:e87 --PRECEDES--> B:e91
    B:e87 --PRECEDES--> B:e92
    B:e87 --PRECEDES--> B:e93
    B:e87 --PRECEDES--> B:e94
    B:e88 --PRECEDES--> B:e90
    B:e88 --PRECEDES--> B:e91
    B:e88 --PRECEDES--> B:e92
    B:e88 --PRECEDES--> B:e93
    B:e88 --PRECEDES--> B:e94
    B:e89 --PRECEDES--> B:e90
    B:e89 --PRECEDES--> B:e91
    B:e89 --PRECEDES--> B:e92
    B:e89 --PRECEDES--> B:e93
    B:e89 --PRECEDES--> B:e94
    B:e90 --PRECEDES--> B:e95
    B:e90 --PRECEDES--> B:e96
    B:e90 --PRECEDES--> B:e97
    B:e90 --PRECEDES--> B:e98
    B:e90 --PRECEDES--> B:e99
    B:e91 --PRECEDES--> B:e95
    B:e91 --PRECEDES--> B:e96
    B:e91 --PRECEDES--> B:e97
    B:e91 --PRECEDES--> B:e98
    B:e91 --PRECEDES--> B:e99
    B:e92 --PRECEDES--> B:e95
    B:e92 --PRECEDES--> B:e96
    B:e92 --PRECEDES--> B:e97
    B:e92 --PRECEDES--> B:e98
    B:e92 --PRECEDES--> B:e99
    B:e93 --PRECEDES--> B:e95
    B:e93 --PRECEDES--> B:e96
    B:e93 --PRECEDES--> B:e97
    B:e93 --PRECEDES--> B:e98
    B:e93 --PRECEDES--> B:e99
    B:e94 --PRECEDES--> B:e95
    B:e94 --PRECEDES--> B:e96
    B:e94 --PRECEDES--> B:e97
    B:e94 --PRECEDES--> B:e98
    B:e94 --PRECEDES--> B:e99
    B:e05 --SAME_TRACK--> B:e09
    B:e06 --SAME_TRACK--> B:e10
    B:e97 --SAME_TRACK--> B:e100
    B:e36 --SAME_TRACK--> B:e101
    B:e48 --SAME_TRACK--> B:e102
    B:e49 --SAME_TRACK--> B:e103
    B:e50 --SAME_TRACK--> B:e104
    B:e47 --SAME_TRACK--> B:e105
    B:e56 --SAME_TRACK--> B:e106
    B:e59 --SAME_TRACK--> B:e107
    B:e39 --SAME_TRACK--> B:e108
    B:e38 --SAME_TRACK--> B:e109
    B:e07 --SAME_TRACK--> B:e11
    B:e39 --SAME_TRACK--> B:e110
    B:e75 --SAME_TRACK--> B:e111
    B:e57 --SAME_TRACK--> B:e112
    B:e61 --SAME_TRACK--> B:e113
    B:e76 --SAME_TRACK--> B:e114
    B:e57 --SAME_TRACK--> B:e115
    B:e61 --SAME_TRACK--> B:e116
    B:e76 --SAME_TRACK--> B:e117
    B:e38 --SAME_TRACK--> B:e118
    B:e60 --SAME_TRACK--> B:e119
    B:e08 --SAME_TRACK--> B:e12
    B:e72 --SAME_TRACK--> B:e120
    B:e74 --SAME_TRACK--> B:e121
    B:e77 --SAME_TRACK--> B:e122
    B:e79 --SAME_TRACK--> B:e123
    B:e90 --SAME_TRACK--> B:e124
    B:e14 --SAME_TRACK--> B:e125
    B:e72 --SAME_TRACK--> B:e126
    B:e58 --SAME_TRACK--> B:e127
    B:e78 --SAME_TRACK--> B:e128
    B:e95 --SAME_TRACK--> B:e129
    B:e96 --SAME_TRACK--> B:e130
    B:e97 --SAME_TRACK--> B:e131
    B:e90 --SAME_TRACK--> B:e132
    B:e05 --SAME_TRACK--> B:e133
    B:e07 --SAME_TRACK--> B:e134
    B:e14 --SAME_TRACK--> B:e135
    B:e15 --SAME_TRACK--> B:e136
    B:e38 --SAME_TRACK--> B:e137
    B:e39 --SAME_TRACK--> B:e138
    B:e28 --SAME_TRACK--> B:e139
    B:e29 --SAME_TRACK--> B:e140
    B:e80 --SAME_TRACK--> B:e141
    B:e08 --SAME_TRACK--> B:e145
    B:e08 --SAME_TRACK--> B:e146
    B:e58 --SAME_TRACK--> B:e147
    B:e15 --SAME_TRACK--> B:e148
    B:e39 --SAME_TRACK--> B:e149
    B:e29 --SAME_TRACK--> B:e150
    B:e78 --SAME_TRACK--> B:e151
    B:e14 --SAME_TRACK--> B:e152
    B:e80 --SAME_TRACK--> B:e153
    B:e13 --SAME_TRACK--> B:e16
    B:e14 --SAME_TRACK--> B:e17
    B:e15 --SAME_TRACK--> B:e18
    B:e19 --SAME_TRACK--> B:e22
    B:e21 --SAME_TRACK--> B:e23
    B:e20 --SAME_TRACK--> B:e24
    B:e25 --SAME_TRACK--> B:e30
    B:e26 --SAME_TRACK--> B:e31
    B:e27 --SAME_TRACK--> B:e32
    B:e28 --SAME_TRACK--> B:e33
    B:e29 --SAME_TRACK--> B:e34
    B:e38 --SAME_TRACK--> B:e40
    B:e39 --SAME_TRACK--> B:e41
    B:e35 --SAME_TRACK--> B:e42
    B:e36 --SAME_TRACK--> B:e43
    B:e37 --SAME_TRACK--> B:e44
    B:e38 --SAME_TRACK--> B:e45
    B:e39 --SAME_TRACK--> B:e46
    B:e47 --SAME_TRACK--> B:e51
    B:e48 --SAME_TRACK--> B:e52
    B:e49 --SAME_TRACK--> B:e53
    B:e50 --SAME_TRACK--> B:e54
    B:e13 --SAME_TRACK--> B:e55
    B:e56 --SAME_TRACK--> B:e62
    B:e57 --SAME_TRACK--> B:e63
    B:e58 --SAME_TRACK--> B:e64
    B:e59 --SAME_TRACK--> B:e65
    B:e60 --SAME_TRACK--> B:e66
    B:e61 --SAME_TRACK--> B:e67
    B:e06 --SAME_TRACK--> B:e68
    B:e19 --SAME_TRACK--> B:e69
    B:e21 --SAME_TRACK--> B:e70
    B:e20 --SAME_TRACK--> B:e71
    B:e72 --SAME_TRACK--> B:e73
    B:e74 --SAME_TRACK--> B:e81
    B:e75 --SAME_TRACK--> B:e82
    B:e76 --SAME_TRACK--> B:e83
    B:e80 --SAME_TRACK--> B:e84
    B:e77 --SAME_TRACK--> B:e85
    B:e78 --SAME_TRACK--> B:e86
    B:e79 --SAME_TRACK--> B:e87
    B:e25 --SAME_TRACK--> B:e88
    B:e26 --SAME_TRACK--> B:e89
    B:e90 --SAME_TRACK--> B:e91
    B:e35 --SAME_TRACK--> B:e92
    B:e27 --SAME_TRACK--> B:e93
    B:e37 --SAME_TRACK--> B:e94
    B:e95 --SAME_TRACK--> B:e98
    B:e96 --SAME_TRACK--> B:e99
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | B:e02 BRAKE_START | ego: MOVING | 0.70 |
| 5.65 | B:e03 COLLISION | ego: MOVING, BRAKE | 5.60 |
| 5.75 | B:e04 TURN_RIGHT_START | ego: MOVING, BRAKE | 5.70 |
| 5.90 | B:e05 TRACK_APPEARED_RIGHT track_001<br>B:e06 TRACK_APPEARED_RIGHT track_002<br>B:e07 TRACK_APPEARED_RIGHT track_003<br>B:e08 TRACK_APPEARED_RIGHT track_022<br>B:e09 CLOSING_START track_001<br>B:e10 CLOSING_START track_002 | ego: MOVING, BRAKE, TURN_RIGHT | 5.80 |
| 6.50 | B:e100 CLOSING_START track_042<br>B:e101 TRACK_LOST track_016<br>B:e102 TRACK_LOST track_018 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_021 | 6.40 |
| 6.55 | B:e103 TRACK_LOST track_019<br>B:e104 TRACK_LOST track_026 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_017: CLOSING<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_018, track_021 | 6.50 |
| 6.60 | B:e105 TRACK_LOST track_017<br>B:e106 TRACK_LOST track_023<br>B:e107 TRACK_LOST track_027 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_017: CLOSING<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_018, track_019, track_021, track_026 | 6.50 |
| 6.65 | B:e108 CRITICAL_TTC_END track_013<br>B:e109 EGO_PATH_ENTRY track_012 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_020: CLOSING<br>track_022: CLOSING<br>track_024: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_026, track_027 | 6.60 |
| 5.90 | B:e11 CLOSING_START track_003 | ego: MOVING, BRAKE, TURN_RIGHT | 5.80 |
| 6.65 | B:e110 EGO_PATH_ENTRY track_013<br>B:e111 TRACK_LOST track_033 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_020: CLOSING<br>track_022: CLOSING<br>track_024: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_026, track_027 | 6.60 |
| 6.70 | B:e112 CLOSING_END track_024<br>B:e113 CLOSING_END track_031<br>B:e114 CLOSING_END track_034<br>B:e115 TRACK_LOST track_024<br>B:e116 TRACK_LOST track_031<br>B:e117 TRACK_LOST track_034 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_024: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_026, track_027, track_033 | 6.60 |
| 6.75 | B:e118 CRITICAL_TTC_END track_012<br>B:e119 CLOSING_END track_030 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_032: CLOSING<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_031, track_033, track_034 | 6.70 |
| 5.90 | B:e12 CLOSING_START track_022 | ego: MOVING, BRAKE, TURN_RIGHT | 5.80 |
| 6.80 | B:e120 CLOSING_END track_028<br>B:e121 CLOSING_END track_032<br>B:e122 CLOSING_END track_036<br>B:e123 CLOSING_END track_040<br>B:e124 CLOSING_END track_041<br>B:e125 EGO_PATH_ENTRY track_005<br>B:e126 TRACK_LOST track_028 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: no active state<br>track_032: CLOSING<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_031, track_033, track_034 | 6.70 |
| 6.85 | B:e127 CLOSING_END track_025<br>B:e128 CLOSING_END track_037<br>B:e129 CLOSING_END track_038 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: no active state<br>track_041: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034 | 6.80 |
| 5.95 | B:e13 TRACK_APPEARED_LEFT track_004 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_022: CLOSING | 5.90 |
| 6.85 | B:e130 CLOSING_END track_039<br>B:e131 CLOSING_END track_042<br>B:e132 TRACK_LOST track_041 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: no active state<br>track_041: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034 | 6.80 |
| 6.90 | B:e133 CLOSING_END track_001<br>B:e134 CLOSING_END track_003<br>B:e135 CLOSING_END track_005<br>B:e136 CLOSING_END track_006<br>B:e137 CLOSING_END track_012<br>B:e138 CLOSING_END track_013<br>B:e139 CLOSING_END track_020 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: no active state<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 6.80 |
| 5.95 | B:e14 TRACK_APPEARED_RIGHT track_005 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_022: CLOSING | 5.90 |
| 6.90 | B:e140 CLOSING_END track_029<br>B:e141 CLOSING_END track_035<br>B:e142 TURN_RIGHT_END<br>B:e143 MOVING_END<br>B:e144 STOP_START | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: no active state<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 6.80 |
| 7.00 | B:e145 CLOSING_END track_022 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_022: CLOSING<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 6.90 |
| 7.35 | B:e146 TRACK_LOST track_022 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_022: no active state<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 7.30 |
| 7.65 | B:e147 TRACK_LOST track_025 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 7.60 |
| 7.70 | B:e148 EGO_PATH_ENTRY track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 7.60 |
| 8.35 | B:e149 EGO_PATH_EXIT track_013 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 8.30 |
| 5.95 | B:e15 TRACK_APPEARED_RIGHT track_006 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_022: CLOSING | 5.90 |
| 8.65 | B:e150 TRACK_LOST track_029 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 | 8.60 |
| 9.70 | B:e151 TRACK_LOST track_037 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_029, track_031, track_033, track_034, track_041 | 9.60 |
| 9.90 | B:e152 TRACK_LOST track_005<br>B:e153 TRACK_LOST track_035 | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_029, track_031, track_033, track_034, track_037, track_041 | 9.80 |
| 5.95 | B:e16 CLOSING_START track_004<br>B:e17 CLOSING_START track_005<br>B:e18 CLOSING_START track_006 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_022: CLOSING | 5.90 |
| 6.05 | B:e19 TRACK_APPEARED_LEFT track_007<br>B:e20 TRACK_APPEARED_LEFT track_009<br>B:e21 TRACK_APPEARED_RIGHT track_008<br>B:e22 CLOSING_START track_007<br>B:e23 CLOSING_START track_008<br>B:e24 CLOSING_START track_009 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_022: CLOSING | 6.00 |
| 6.10 | B:e25 TRACK_APPEARED_LEFT track_010<br>B:e26 TRACK_APPEARED_LEFT track_011<br>B:e27 TRACK_APPEARED_LEFT track_015<br>B:e28 TRACK_APPEARED_RIGHT track_020<br>B:e29 TRACK_APPEARED_RIGHT track_029<br>B:e30 CLOSING_START track_010<br>B:e31 CLOSING_START track_011<br>B:e32 CLOSING_START track_015<br>B:e33 CLOSING_START track_020<br>B:e34 CLOSING_START track_029 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING | 6.00 |
| 6.15 | B:e35 TRACK_APPEARED_LEFT track_014<br>B:e36 TRACK_APPEARED_LEFT track_016<br>B:e37 TRACK_APPEARED_LEFT track_021<br>B:e38 TRACK_APPEARED_RIGHT track_012<br>B:e39 TRACK_APPEARED_RIGHT track_013<br>B:e40 CLOSING_START track_012<br>B:e41 CLOSING_START track_013<br>B:e42 CLOSING_START track_014<br>B:e43 CLOSING_START track_016<br>B:e44 CLOSING_START track_021<br>B:e45 CRITICAL_TTC_START track_012<br>B:e46 CRITICAL_TTC_START track_013 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_029: CLOSING | 6.10 |
| 6.20 | B:e47 TRACK_APPEARED_LEFT track_017<br>B:e48 TRACK_APPEARED_LEFT track_018<br>B:e49 TRACK_APPEARED_LEFT track_019<br>B:e50 TRACK_APPEARED_LEFT track_026<br>B:e51 CLOSING_START track_017<br>B:e52 CLOSING_START track_018<br>B:e53 CLOSING_START track_019<br>B:e54 CLOSING_START track_026 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_029: CLOSING | 6.10 |
| 6.25 | B:e55 TRACK_LOST track_004 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING | 6.20 |
| 6.30 | B:e56 TRACK_APPEARED_LEFT track_023<br>B:e57 TRACK_APPEARED_LEFT track_024<br>B:e58 TRACK_APPEARED_LEFT track_025<br>B:e59 TRACK_APPEARED_LEFT track_027<br>B:e60 TRACK_APPEARED_LEFT track_030<br>B:e61 TRACK_APPEARED_LEFT track_031<br>B:e62 CLOSING_START track_023<br>B:e63 CLOSING_START track_024<br>B:e64 CLOSING_START track_025<br>B:e65 CLOSING_START track_027<br>B:e66 CLOSING_START track_030<br>B:e67 CLOSING_START track_031<br>B:e68 TRACK_LOST track_002<br>B:e69 TRACK_LOST track_007<br>B:e70 TRACK_LOST track_008<br>B:e71 TRACK_LOST track_009 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING<br>track lost, states UNKNOWN: track_004 | 6.20 |
| 6.35 | B:e72 TRACK_APPEARED_LEFT track_028<br>B:e73 CLOSING_START track_028 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009 | 6.30 |
| 6.40 | B:e74 TRACK_APPEARED_LEFT track_032<br>B:e75 TRACK_APPEARED_LEFT track_033<br>B:e76 TRACK_APPEARED_LEFT track_034<br>B:e77 TRACK_APPEARED_LEFT track_036<br>B:e78 TRACK_APPEARED_LEFT track_037<br>B:e79 TRACK_APPEARED_LEFT track_040<br>B:e80 TRACK_APPEARED_RIGHT track_035<br>B:e81 CLOSING_START track_032<br>B:e82 CLOSING_START track_033<br>B:e83 CLOSING_START track_034<br>B:e84 CLOSING_START track_035<br>B:e85 CLOSING_START track_036<br>B:e86 CLOSING_START track_037<br>B:e87 CLOSING_START track_040<br>B:e88 TRACK_LOST track_010<br>B:e89 TRACK_LOST track_011 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009 | 6.30 |
| 6.45 | B:e90 TRACK_APPEARED_LEFT track_041<br>B:e91 CLOSING_START track_041<br>B:e92 TRACK_LOST track_014<br>B:e93 TRACK_LOST track_015<br>B:e94 TRACK_LOST track_021 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_040: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011 | 6.40 |
| 6.50 | B:e95 TRACK_APPEARED_LEFT track_038<br>B:e96 TRACK_APPEARED_LEFT track_039<br>B:e97 TRACK_APPEARED_LEFT track_042<br>B:e98 CLOSING_START track_038<br>B:e99 CLOSING_START track_039 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_021 | 6.40 |

## States still active when observation ended

- BRAKE, since B:e02 (t = 0.80 s)
- CLOSING of track_002, since B:e10 (t = 5.90 s); the track was lost at 6.30 s
- EGO_PATH of track_012, since B:e109 (t = 6.65 s)
- EGO_PATH of track_005, since B:e125 (t = 6.80 s); the track was lost at 9.90 s
- STOP, since B:e144 (t = 6.90 s)
- EGO_PATH of track_006, since B:e148 (t = 7.70 s)
- CLOSING of track_004, since B:e16 (t = 5.95 s); the track was lost at 6.25 s
- CLOSING of track_005, since B:e17 (t = 5.95 s); the track was lost at 9.90 s
- CLOSING of track_006, since B:e18 (t = 5.95 s)
- CLOSING of track_007, since B:e22 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_008, since B:e23 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_009, since B:e24 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_010, since B:e30 (t = 6.10 s); the track was lost at 6.40 s
- CLOSING of track_011, since B:e31 (t = 6.10 s); the track was lost at 6.40 s
- CLOSING of track_015, since B:e32 (t = 6.10 s); the track was lost at 6.45 s
- CLOSING of track_020, since B:e33 (t = 6.10 s)
- CLOSING of track_029, since B:e34 (t = 6.10 s); the track was lost at 8.65 s
- CLOSING of track_012, since B:e40 (t = 6.15 s)
- CLOSING of track_013, since B:e41 (t = 6.15 s)
- CLOSING of track_014, since B:e42 (t = 6.15 s); the track was lost at 6.45 s
- CLOSING of track_016, since B:e43 (t = 6.15 s); the track was lost at 6.50 s
- CLOSING of track_021, since B:e44 (t = 6.15 s); the track was lost at 6.45 s
- CRITICAL_TTC of track_012, since B:e45 (t = 6.15 s)
- CRITICAL_TTC of track_013, since B:e46 (t = 6.15 s)
- CLOSING of track_017, since B:e51 (t = 6.20 s); the track was lost at 6.60 s
- CLOSING of track_018, since B:e52 (t = 6.20 s); the track was lost at 6.50 s
- CLOSING of track_019, since B:e53 (t = 6.20 s); the track was lost at 6.55 s
- CLOSING of track_026, since B:e54 (t = 6.20 s); the track was lost at 6.55 s
- CLOSING of track_023, since B:e62 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_024, since B:e63 (t = 6.30 s); the track was lost at 6.70 s
- CLOSING of track_025, since B:e64 (t = 6.30 s); the track was lost at 7.65 s
- CLOSING of track_027, since B:e65 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_030, since B:e66 (t = 6.30 s)
- CLOSING of track_031, since B:e67 (t = 6.30 s); the track was lost at 6.70 s
- CLOSING of track_028, since B:e73 (t = 6.35 s); the track was lost at 6.80 s
- CLOSING of track_032, since B:e81 (t = 6.40 s)
- CLOSING of track_033, since B:e82 (t = 6.40 s); the track was lost at 6.65 s
- CLOSING of track_034, since B:e83 (t = 6.40 s); the track was lost at 6.70 s
- CLOSING of track_035, since B:e84 (t = 6.40 s); the track was lost at 9.90 s
- CLOSING of track_036, since B:e85 (t = 6.40 s)
- CLOSING of track_037, since B:e86 (t = 6.40 s); the track was lost at 9.70 s
- CLOSING of track_040, since B:e87 (t = 6.40 s)
- CLOSING of track_041, since B:e91 (t = 6.45 s); the track was lost at 6.85 s
- CLOSING of track_038, since B:e98 (t = 6.50 s)
- CLOSING of track_039, since B:e99 (t = 6.50 s)

## Tracks lost

- track_016 at 6.50 s (B:e101): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_018 at 6.50 s (B:e102): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_019 at 6.55 s (B:e103): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_026 at 6.55 s (B:e104): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_017 at 6.60 s (B:e105): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_023 at 6.60 s (B:e106): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_027 at 6.60 s (B:e107): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_033 at 6.65 s (B:e111): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_024 at 6.70 s (B:e115): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_031 at 6.70 s (B:e116): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_034 at 6.70 s (B:e117): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_028 at 6.80 s (B:e126): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 9.90 s (B:e152): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 6.25 s (B:e55): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 6.30 s (B:e68): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 6.30 s (B:e69): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 6.30 s (B:e70): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 6.30 s (B:e71): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 6.40 s (B:e88): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 6.40 s (B:e89): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_014 at 6.45 s (B:e92): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_015 at 6.45 s (B:e93): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_021 at 6.45 s (B:e94): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_041, track_022, track_025, track_029, track_037, track_035

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_005: EGO_PATH_ENTRY 6.80, no critical TTC
- track_006: EGO_PATH_ENTRY 7.70, no critical TTC
- track_012: CRITICAL_TTC_START 6.15; EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s)
- track_013: CRITICAL_TTC_START 6.15; EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.90 | 9.95 | 82 | 11.1 m / +71 deg | 6.31 m (7.00) | 6.5 m / +39 deg | 2.3 m/s |
| track_002 | 5.90 | 6.30 | 9 | 23.6 m / +73 deg | 21.36 m (6.30) | 21.4 m / +56 deg | 5.3 m/s |
| track_003 | 5.90 | 9.95 | 82 | 13.5 m / +73 deg | 9.65 m (6.95) | 9.8 m / +66 deg | 5.4 m/s |
| track_004 | 5.95 | 6.25 | 7 | 8.7 m / -71 deg | 8.36 m (6.25) | 8.4 m / -80 deg | 13.6 m/s |
| track_005 | 5.95 | 9.90 | 70 | 27.7 m / +58 deg | 21.90 m (6.85) | 22.2 m / -1 deg | 4.9 m/s |
| track_006 | 5.95 | 9.95 | 81 | 14.5 m / +57 deg | 8.71 m (6.95) | 8.9 m / +6 deg | 1.6 m/s |
| track_007 | 6.05 | 6.30 | 6 | 35.6 m / -64 deg | 35.28 m (6.30) | 35.3 m / -78 deg | 11.0 m/s |
| track_008 | 6.05 | 6.30 | 6 | 34.9 m / +80 deg | 33.83 m (6.30) | 33.8 m / +69 deg | 1.8 m/s |
| track_009 | 6.05 | 6.30 | 5 | 38.2 m / -59 deg | 37.66 m (6.30) | 37.7 m / -77 deg | 1.9 m/s |
| track_010 | 6.10 | 6.40 | 7 | 12.3 m / -59 deg | 11.89 m (6.30) | 11.9 m / -83 deg | 5.7 m/s |
| track_011 | 6.10 | 6.40 | 6 | 42.7 m / -58 deg | 42.24 m (6.35) | 42.3 m / -79 deg | 4.7 m/s |
| track_012 | 6.15 | 9.95 | 77 | 10.7 m / +40 deg | 6.06 m (6.95) | 6.1 m / -4 deg | 1.5 m/s |
| track_013 | 6.15 | 9.95 | 73 | 14.0 m / +37 deg | 9.15 m (9.50) | 9.2 m / -40 deg | 4.5 m/s |
| track_014 | 6.15 | 6.45 | 7 | 15.3 m / -53 deg | 14.83 m (6.40) | 14.9 m / -81 deg | 2.7 m/s |
| track_015 | 6.10 | 6.45 | 6 | 49.6 m / -53 deg | 48.93 m (6.40) | 49.0 m / -79 deg | 2.7 m/s |
| track_016 | 6.15 | 6.50 | 7 | 47.4 m / -49 deg | 46.61 m (6.45) | 46.6 m / -78 deg | 4.2 m/s |
| track_017 | 6.20 | 6.60 | 9 | 26.7 m / -45 deg | 25.94 m (6.50) | 26.1 m / -80 deg | 2.4 m/s |
| track_018 | 6.20 | 6.50 | 7 | 53.0 m / -51 deg | 52.43 m (6.45) | 52.4 m / -75 deg | 2.0 m/s |
| track_019 | 6.20 | 6.55 | 8 | 21.1 m / -49 deg | 20.50 m (6.45) | 20.6 m / -81 deg | 2.3 m/s |
| track_020 | 6.10 | 9.95 | 75 | 16.9 m / +80 deg | 13.33 m (9.95) | 13.3 m / +76 deg | 7.1 m/s |
| track_021 | 6.15 | 6.45 | 5 | 55.7 m / -53 deg | 55.07 m (6.45) | 55.1 m / -74 deg | 5.1 m/s |
| track_022 | 5.90 | 7.35 | 9 | 27.5 m / +76 deg | 22.57 m (7.35) | 22.6 m / +26 deg | 1.8 m/s |
| track_023 | 6.30 | 6.60 | 7 | 33.9 m / -42 deg | 33.31 m (6.55) | 33.4 m / -76 deg | 14.3 m/s |
| track_024 | 6.30 | 6.70 | 9 | 37.6 m / -48 deg | 37.12 m (6.55) | 37.4 m / -82 deg | 4.4 m/s |
| track_025 | 6.30 | 7.65 | 26 | 39.3 m / -38 deg | 38.38 m (6.60) | 38.6 m / -64 deg | 10.5 m/s |
| track_026 | 6.20 | 6.55 | 5 | 51.5 m / -47 deg | 50.70 m (6.50) | 50.7 m / -74 deg | 5.0 m/s |
| track_027 | 6.30 | 6.60 | 6 | 48.8 m / -40 deg | 47.88 m (6.60) | 47.9 m / -59 deg | 20.3 m/s |
| track_028 | 6.35 | 6.80 | 7 | 50.3 m / -38 deg | 49.43 m (6.70) | 49.5 m / -64 deg | 20.3 m/s |
| track_029 | 6.10 | 8.65 | 14 | 40.3 m / +76 deg | 36.75 m (6.90) | 37.3 m / +26 deg | 2.0 m/s |
| track_030 | 6.30 | 9.95 | 69 | 40.5 m / -44 deg | 39.79 m (6.55) | 40.1 m / -77 deg | 11.1 m/s |
| track_031 | 6.30 | 6.70 | 7 | 41.2 m / -47 deg | 40.68 m (6.55) | 40.9 m / -81 deg | 3.2 m/s |
| track_032 | 6.40 | 9.95 | 72 | 36.5 m / -36 deg | 35.92 m (6.65) | 36.1 m / -78 deg | 5.7 m/s |
| track_033 | 6.40 | 6.65 | 6 | 32.5 m / -44 deg | 32.07 m (6.60) | 32.1 m / -74 deg | 15.8 m/s |
| track_034 | 6.40 | 6.70 | 7 | 44.0 m / -44 deg | 43.57 m (6.60) | 43.7 m / -76 deg | 10.7 m/s |
| track_035 | 6.40 | 9.90 | 62 | 25.4 m / +44 deg | 22.74 m (9.05) | 22.8 m / +12 deg | 1.6 m/s |
| track_036 | 6.40 | 9.95 | 65 | 43.5 m / -40 deg | 43.02 m (6.65) | 43.3 m / -72 deg | 2.3 m/s |
| track_037 | 6.40 | 9.70 | 54 | 41.5 m / -36 deg | 40.30 m (9.70) | 40.3 m / -79 deg | 4.3 m/s |
| track_038 | 6.50 | 9.95 | 70 | 22.0 m / -32 deg | 21.53 m (6.75) | 21.8 m / -62 deg | 1.5 m/s |
| track_039 | 6.50 | 9.95 | 68 | 28.4 m / -37 deg | 28.00 m (9.15) | 28.0 m / -66 deg | 1.7 m/s |
| track_040 | 6.40 | 9.95 | 58 | 39.7 m / -40 deg | 38.58 m (9.95) | 38.6 m / -69 deg | 4.3 m/s |
| track_041 | 6.45 | 6.85 | 7 | 44.6 m / -38 deg | 44.18 m (6.65) | 44.3 m / -73 deg | 7.9 m/s |
| track_042 | 6.50 | 9.95 | 68 | 31.9 m / -42 deg | 31.69 m (6.65) | 31.7 m / -68 deg | 3.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.80 s: B started braking.
- t = 5.65 s: B's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.75 s: B started turning right.
- t = 5.90 s: B's radar started tracking track_001, which appeared on its right.
- t = 5.90 s: B's radar started tracking track_002, which appeared on its right.
- t = 5.90 s: B's radar started tracking track_003, which appeared on its right.
- t = 5.90 s: B's radar started tracking track_022, which appeared on its right.
- t = 5.90 s: B observed track_001 start closing in (already the case when first observed).
- t = 5.90 s: B observed track_002 start closing in (already the case when first observed).
- t = 6.50 s: B observed track_042 start closing in (already the case when first observed).
- t = 6.50 s: B's radar lost track_016 (its states are UNKNOWN from then on, not ended).
- t = 6.50 s: B's radar lost track_018 (its states are UNKNOWN from then on, not ended).
- t = 6.55 s: B's radar lost track_019 (its states are UNKNOWN from then on, not ended).
- t = 6.55 s: B's radar lost track_026 (its states are UNKNOWN from then on, not ended).
- t = 6.60 s: B's radar lost track_017 (its states are UNKNOWN from then on, not ended).
- t = 6.60 s: B's radar lost track_023 (its states are UNKNOWN from then on, not ended).
- t = 6.60 s: B's radar lost track_027 (its states are UNKNOWN from then on, not ended).
- t = 6.65 s: B's time-to-contact with track_013 stopped being critical.
- t = 6.65 s: B observed track_012 enter its forward path corridor.
- t = 5.90 s: B observed track_003 start closing in (already the case when first observed).
- t = 6.65 s: B observed track_013 enter its forward path corridor.
- t = 6.65 s: B's radar lost track_033 (its states are UNKNOWN from then on, not ended).
- t = 6.70 s: B observed track_024 stop closing in.
- t = 6.70 s: B observed track_031 stop closing in.
- t = 6.70 s: B observed track_034 stop closing in.
- t = 6.70 s: B's radar lost track_024 (its states are UNKNOWN from then on, not ended).
- t = 6.70 s: B's radar lost track_031 (its states are UNKNOWN from then on, not ended).
- t = 6.70 s: B's radar lost track_034 (its states are UNKNOWN from then on, not ended).
- t = 6.75 s: B's time-to-contact with track_012 stopped being critical.
- t = 6.75 s: B observed track_030 stop closing in.
- t = 5.90 s: B observed track_022 start closing in (already the case when first observed).
- t = 6.80 s: B observed track_028 stop closing in.
- t = 6.80 s: B observed track_032 stop closing in.
- t = 6.80 s: B observed track_036 stop closing in.
- t = 6.80 s: B observed track_040 stop closing in.
- t = 6.80 s: B observed track_041 stop closing in.
- t = 6.80 s: B observed track_005 enter its forward path corridor.
- t = 6.80 s: B's radar lost track_028 (its states are UNKNOWN from then on, not ended).
- t = 6.85 s: B observed track_025 stop closing in.
- t = 6.85 s: B observed track_037 stop closing in.
- t = 6.85 s: B observed track_038 stop closing in.
- t = 5.95 s: B's radar started tracking track_004, which appeared on its left.
- t = 6.85 s: B observed track_039 stop closing in.
- t = 6.85 s: B observed track_042 stop closing in.
- t = 6.85 s: B's radar lost track_041 (its states are UNKNOWN from then on, not ended).
- t = 6.90 s: B observed track_001 stop closing in.
- t = 6.90 s: B observed track_003 stop closing in.
- t = 6.90 s: B observed track_005 stop closing in.
- t = 6.90 s: B observed track_006 stop closing in.
- t = 6.90 s: B observed track_012 stop closing in.
- t = 6.90 s: B observed track_013 stop closing in.
- t = 6.90 s: B observed track_020 stop closing in.
- t = 5.95 s: B's radar started tracking track_005, which appeared on its right.
- t = 6.90 s: B observed track_029 stop closing in.
- t = 6.90 s: B observed track_035 stop closing in.
- t = 6.90 s: B stopped turning right.
- t = 6.90 s: B stopped moving.
- t = 6.90 s: B came to a stop.
- t = 7.00 s: B observed track_022 stop closing in.
- t = 7.35 s: B's radar lost track_022 (its states are UNKNOWN from then on, not ended).
- t = 7.65 s: B's radar lost track_025 (its states are UNKNOWN from then on, not ended).
- t = 7.70 s: B observed track_006 enter its forward path corridor.
- t = 8.35 s: B observed track_013 leave its forward path corridor.
- t = 5.95 s: B's radar started tracking track_006, which appeared on its right.
- t = 8.65 s: B's radar lost track_029 (its states are UNKNOWN from then on, not ended).
- t = 9.70 s: B's radar lost track_037 (its states are UNKNOWN from then on, not ended).
- t = 9.90 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 9.90 s: B's radar lost track_035 (its states are UNKNOWN from then on, not ended).
- t = 5.95 s: B observed track_004 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_005 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_006 start closing in (already the case when first observed).
- t = 6.05 s: B's radar started tracking track_007, which appeared on its left.
- t = 6.05 s: B's radar started tracking track_009, which appeared on its left.
- t = 6.05 s: B's radar started tracking track_008, which appeared on its right.
- t = 6.05 s: B observed track_007 start closing in (already the case when first observed).
- t = 6.05 s: B observed track_008 start closing in (already the case when first observed).
- t = 6.05 s: B observed track_009 start closing in (already the case when first observed).
- t = 6.10 s: B's radar started tracking track_010, which appeared on its left.
- t = 6.10 s: B's radar started tracking track_011, which appeared on its left.
- t = 6.10 s: B's radar started tracking track_015, which appeared on its left.
- t = 6.10 s: B's radar started tracking track_020, which appeared on its right.
- t = 6.10 s: B's radar started tracking track_029, which appeared on its right.
- t = 6.10 s: B observed track_010 start closing in (already the case when first observed).
- t = 6.10 s: B observed track_011 start closing in (already the case when first observed).
- t = 6.10 s: B observed track_015 start closing in (already the case when first observed).
- t = 6.10 s: B observed track_020 start closing in (already the case when first observed).
- t = 6.10 s: B observed track_029 start closing in (already the case when first observed).
- t = 6.15 s: B's radar started tracking track_014, which appeared on its left.
- t = 6.15 s: B's radar started tracking track_016, which appeared on its left.
- t = 6.15 s: B's radar started tracking track_021, which appeared on its left.
- t = 6.15 s: B's radar started tracking track_012, which appeared on its right.
- t = 6.15 s: B's radar started tracking track_013, which appeared on its right.
- t = 6.15 s: B observed track_012 start closing in (already the case when first observed).
- t = 6.15 s: B observed track_013 start closing in (already the case when first observed).
- t = 6.15 s: B observed track_014 start closing in (already the case when first observed).
- t = 6.15 s: B observed track_016 start closing in (already the case when first observed).
- t = 6.15 s: B observed track_021 start closing in (already the case when first observed).
- t = 6.15 s: B's time-to-contact with track_012 became critical (already the case when first observed).
- t = 6.15 s: B's time-to-contact with track_013 became critical (already the case when first observed).
- t = 6.20 s: B's radar started tracking track_017, which appeared on its left.
- t = 6.20 s: B's radar started tracking track_018, which appeared on its left.
- t = 6.20 s: B's radar started tracking track_019, which appeared on its left.
- t = 6.20 s: B's radar started tracking track_026, which appeared on its left.
- t = 6.20 s: B observed track_017 start closing in (already the case when first observed).
- t = 6.20 s: B observed track_018 start closing in (already the case when first observed).
- t = 6.20 s: B observed track_019 start closing in (already the case when first observed).
- t = 6.20 s: B observed track_026 start closing in (already the case when first observed).
- t = 6.25 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: B's radar started tracking track_023, which appeared on its left.
- t = 6.30 s: B's radar started tracking track_024, which appeared on its left.
- t = 6.30 s: B's radar started tracking track_025, which appeared on its left.
- t = 6.30 s: B's radar started tracking track_027, which appeared on its left.
- t = 6.30 s: B's radar started tracking track_030, which appeared on its left.
- t = 6.30 s: B's radar started tracking track_031, which appeared on its left.
- t = 6.30 s: B observed track_023 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_024 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_025 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_027 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_030 start closing in (already the case when first observed).
- t = 6.30 s: B observed track_031 start closing in (already the case when first observed).
- t = 6.30 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 6.35 s: B's radar started tracking track_028, which appeared on its left.
- t = 6.35 s: B observed track_028 start closing in (already the case when first observed).
- t = 6.40 s: B's radar started tracking track_032, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_033, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_034, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_036, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_037, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_040, which appeared on its left.
- t = 6.40 s: B's radar started tracking track_035, which appeared on its right.
- t = 6.40 s: B observed track_032 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_033 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_034 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_035 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_036 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_037 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_040 start closing in (already the case when first observed).
- t = 6.40 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 6.40 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 6.45 s: B's radar started tracking track_041, which appeared on its left.
- t = 6.45 s: B observed track_041 start closing in (already the case when first observed).
- t = 6.45 s: B's radar lost track_014 (its states are UNKNOWN from then on, not ended).
- t = 6.45 s: B's radar lost track_015 (its states are UNKNOWN from then on, not ended).
- t = 6.45 s: B's radar lost track_021 (its states are UNKNOWN from then on, not ended).
- t = 6.50 s: B's radar started tracking track_038, which appeared on its left.
- t = 6.50 s: B's radar started tracking track_039, which appeared on its left.
- t = 6.50 s: B's radar started tracking track_042, which appeared on its left.
- t = 6.50 s: B observed track_038 start closing in (already the case when first observed).
- t = 6.50 s: B observed track_039 start closing in (already the case when first observed).
