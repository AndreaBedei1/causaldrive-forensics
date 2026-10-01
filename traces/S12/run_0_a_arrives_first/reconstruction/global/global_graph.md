# Global graph - S12/run_0_a_arrives_first

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| A:track_003 | anonymous_track | seen only by A; candidate: - |
| A:track_004 | anonymous_track | seen only by A; candidate: - |
| A:track_005 | anonymous_track | seen only by A; candidate: - |
| A:track_006 | anonymous_track | seen only by A; candidate: - |
| A:track_007 | anonymous_track | seen only by A; candidate: - |
| A:track_008 | anonymous_track | seen only by A; candidate: - |
| A:track_009 | anonymous_track | seen only by A; candidate: - |
| A:track_010 | anonymous_track | seen only by A; candidate: - |
| A:track_011 | anonymous_track | seen only by A; candidate: - |
| A:track_012 | anonymous_track | seen only by A; candidate: - |
| A:track_013 | anonymous_track | seen only by A; candidate: - |
| A:track_014 | anonymous_track | seen only by A; candidate: - |
| A:track_015 | anonymous_track | seen only by A; candidate: - |
| A:track_016 | anonymous_track | seen only by A; candidate: - |
| A:track_017 | anonymous_track | seen only by A; candidate: - |
| A:track_018 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_003 | A:track_003 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_004 | A:track_004 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_005 | A:track_005 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_006 | A:track_006 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_007 | A:track_007 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_008 | A:track_008 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_009 | A:track_009 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_010 | A:track_010 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_011 | A:track_011 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_012 | A:track_012 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_013 | A:track_013 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_014 | A:track_014 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_015 | A:track_015 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_016 | A:track_016 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_017 | A:track_017 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_018 | A:track_018 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.65 |  |
| g05 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e05 @ 2.95 |  |
| g06 | - | CLOSING_START | A | A:track_001 | A:e06 @ 2.95 | active_at_first_observation=True |
| g07 | - | MOVING_END | A | - | A:e07 @ 3.40 |  |
| g08 | - | STOP_START | A | - | A:e08 @ 3.40 |  |
| g09 | - | CLOSING_END | A | A:track_001 | A:e09 @ 4.70 |  |
| g10 | - | BRAKE_END | A | - | A:e10 @ 6.45 |  |
| g11 | - | STOP_END | A | - | A:e11 @ 6.80 |  |
| g12 | - | MOVING_START | A | - | A:e12 @ 6.80 |  |
| g13 | - | CLOSING_START | A | A:track_001 | A:e13 @ 7.15 |  |
| g14 | - | TURN_LEFT_START | A | - | A:e14 @ 7.80 |  |
| g15 | - | TRACK_APPEARED_LEFT | A | A:track_002 | A:e15 @ 8.25 |  |
| g16 | - | TRACK_APPEARED_LEFT | A | A:track_003 | A:e16 @ 8.25 |  |
| g17 | - | TRACK_APPEARED_LEFT | A | A:track_005 | A:e17 @ 8.25 |  |
| g18 | - | TRACK_APPEARED_LEFT | A | A:track_008 | A:e18 @ 8.25 |  |
| g19 | - | CLOSING_START | A | A:track_002 | A:e19 @ 8.25 | active_at_first_observation=True |
| g20 | - | CLOSING_START | A | A:track_003 | A:e20 @ 8.25 | active_at_first_observation=True |
| g21 | - | CLOSING_START | A | A:track_005 | A:e21 @ 8.25 | active_at_first_observation=True |
| g22 | - | CLOSING_START | A | A:track_008 | A:e22 @ 8.25 | active_at_first_observation=True |
| g23 | - | TRACK_APPEARED_LEFT | A | A:track_004 | A:e23 @ 8.30 |  |
| g24 | - | CLOSING_START | A | A:track_004 | A:e24 @ 8.30 | active_at_first_observation=True |
| g25 | - | TRACK_APPEARED_LEFT | A | A:track_006 | A:e25 @ 8.80 |  |
| g26 | - | TRACK_APPEARED_RIGHT | A | A:track_007 | A:e26 @ 8.80 |  |
| g27 | - | CLOSING_START | A | A:track_006 | A:e27 @ 8.80 | active_at_first_observation=True |
| g28 | - | TRACK_APPEARED_LEFT | A | A:track_010 | A:e28 @ 8.85 |  |
| g29 | - | TRACK_APPEARED_LEFT | A | A:track_011 | A:e29 @ 8.85 |  |
| g30 | - | TRACK_APPEARED_RIGHT | A | A:track_009 | A:e30 @ 8.85 |  |
| g31 | - | CLOSING_START | A | A:track_010 | A:e31 @ 8.85 | active_at_first_observation=True |
| g32 | - | CLOSING_START | A | A:track_011 | A:e32 @ 8.85 | active_at_first_observation=True |
| g33 | - | TRACK_APPEARED_LEFT | A | A:track_012 | A:e33 @ 8.90 |  |
| g34 | - | TRACK_APPEARED_LEFT | A | A:track_017 | A:e34 @ 8.90 |  |
| g35 | - | CLOSING_START | A | A:track_012 | A:e35 @ 8.90 | active_at_first_observation=True |
| g36 | - | CLOSING_START | A | A:track_017 | A:e36 @ 8.90 | active_at_first_observation=True |
| g37 | - | TRACK_APPEARED_LEFT | A | A:track_014 | A:e37 @ 9.00 |  |
| g38 | - | TRACK_APPEARED_RIGHT | A | A:track_013 | A:e38 @ 9.00 |  |
| g39 | - | CLOSING_START | A | A:track_014 | A:e39 @ 9.00 | active_at_first_observation=True |
| g40 | - | TRACK_LOST | A | A:track_007 | A:e40 @ 9.00 |  |
| g41 | - | TRACK_APPEARED_LEFT | A | A:track_015 | A:e41 @ 9.05 |  |
| g42 | - | CLOSING_START | A | A:track_015 | A:e42 @ 9.05 | active_at_first_observation=True |
| g43 | - | TRACK_APPEARED_RIGHT | A | A:track_016 | A:e43 @ 9.10 |  |
| g44 | - | CLOSING_START | A | A:track_016 | A:e44 @ 9.10 | active_at_first_observation=True |
| g45 | - | TRACK_LOST | A | A:track_009 | A:e45 @ 9.20 |  |
| g46 | - | TRACK_APPEARED_RIGHT | A | A:track_018 | A:e46 @ 9.25 |  |
| g47 | - | CLOSING_START | A | A:track_018 | A:e47 @ 9.25 | active_at_first_observation=True |
| g48 | - | CLOSING_END | A | A:track_016 | A:e48 @ 9.40 |  |
| g49 | - | CLOSING_START | A | A:track_016 | A:e49 @ 9.60 |  |
| g50 | - | CRITICAL_TTC_START | A | A:track_001 | A:e50 @ 9.75 |  |
| g51 | - | CLOSING_START | A | A:track_013 | A:e51 @ 9.80 |  |
| g52 | - | TRACK_LOST | A | A:track_018 | A:e52 @ 10.10 |  |
| g53 | - | TRACK_LOST | A | A:track_016 | A:e53 @ 10.40 |  |
| g54 | - | TRACK_LOST | A | A:track_015 | A:e54 @ 10.45 |  |
| g55 | - | EGO_PATH_ENTRY | A | A:track_014 | A:e55 @ 10.60 |  |
| g56 | - | CRITICAL_TTC_END | A | A:track_001 | A:e56 @ 10.65 |  |
| g57 | - | TRACK_LOST | A | A:track_010 | A:e57 @ 10.70 |  |
| g58 | - | TRACK_LOST | A | A:track_001 | A:e58 @ 11.00 |  |
| g59 | - | TURN_LEFT_END | A | - | A:e59 @ 11.05 |  |
| g60 | - | EGO_PATH_EXIT | A | A:track_014 | A:e60 @ 11.20 |  |
| g61 | - | EGO_PATH_ENTRY | A | A:track_008 | A:e61 @ 11.90 |  |
| g62 | - | TRACK_LOST | A | A:track_006 | A:e62 @ 12.30 |  |
| g63 | - | TRACK_LOST | A | A:track_013 | A:e63 @ 13.50 |  |
| g64 | - | TRACK_LOST | A | A:track_017 | A:e64 @ 14.30 |  |
| g65 | - | TRACK_LOST | A | A:track_012 | A:e65 @ 14.35 |  |
| g66 | - | TRACK_LOST | A | A:track_004 | A:e66 @ 14.50 |  |
| g67 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g68 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 2.10 | relevant_to_ego_path=False |
| g69 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 4.00 |  |
| g70 | - | BRAKE_START | B | - | B:e04 @ 4.35 |  |
| g71 | - | MOVING_END | B | - | B:e05 @ 4.70 |  |
| g72 | - | STOP_START | B | - | B:e06 @ 4.70 |  |
| g73 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e07 @ 6.90 |  |
| g74 | - | CLOSING_START | B | B:track_001 | B:e08 @ 6.90 | active_at_first_observation=True |
| g75 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e09 @ 8.50 |  |
| g76 | - | EGO_PATH_EXIT | B | B:track_001 | B:e10 @ 9.05 |  |
| g77 | - | BRAKE_END | B | - | B:e11 @ 10.45 |  |
| g78 | - | CRITICAL_TTC_START | B | B:track_001 | B:e12 @ 10.55 |  |
| g79 | - | CRITICAL_TTC_END | B | B:track_001 | B:e13 @ 10.85 |  |
| g80 | - | STOP_END | B | - | B:e14 @ 10.85 |  |
| g81 | - | MOVING_START | B | - | B:e15 @ 10.85 |  |
| g82 | - | TRACK_LOST | B | B:track_001 | B:e16 @ 11.15 |  |

## Edges

```
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g13
    g15 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g24
    g25 --SAME_TRACK--> g27
    g28 --SAME_TRACK--> g31
    g29 --SAME_TRACK--> g32
    g33 --SAME_TRACK--> g35
    g34 --SAME_TRACK--> g36
    g37 --SAME_TRACK--> g39
    g26 --SAME_TRACK--> g40
    g41 --SAME_TRACK--> g42
    g43 --SAME_TRACK--> g44
    g30 --SAME_TRACK--> g45
    g46 --SAME_TRACK--> g47
    g43 --SAME_TRACK--> g48
    g43 --SAME_TRACK--> g49
    g05 --SAME_TRACK--> g50
    g38 --SAME_TRACK--> g51
    g46 --SAME_TRACK--> g52
    g43 --SAME_TRACK--> g53
    g41 --SAME_TRACK--> g54
    g37 --SAME_TRACK--> g55
    g05 --SAME_TRACK--> g56
    g28 --SAME_TRACK--> g57
    g05 --SAME_TRACK--> g58
    g37 --SAME_TRACK--> g60
    g18 --SAME_TRACK--> g61
    g25 --SAME_TRACK--> g62
    g38 --SAME_TRACK--> g63
    g34 --SAME_TRACK--> g64
    g33 --SAME_TRACK--> g65
    g23 --SAME_TRACK--> g66
    g73 --SAME_TRACK--> g74
    g73 --SAME_TRACK--> g75
    g73 --SAME_TRACK--> g76
    g73 --SAME_TRACK--> g78
    g73 --SAME_TRACK--> g79
    g73 --SAME_TRACK--> g82
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 9.75 [local times]
- A's track_008 (unidentified A:track_008): EGO_PATH_ENTRY 11.90, no critical TTC [local times]
- A's track_014 (unidentified A:track_014): EGO_PATH_ENTRY 10.60, no critical TTC [local times]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 10.55; EGO_PATH_ENTRY 8.50 before critical TTC (-2.05 s) [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g04 BRAKE_START(A) (A:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g05 TRACK_APPEARED_LEFT(A,A:track_001) (A:e05)<br>g06 CLOSING_START(A,A:track_001) (A:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| - | A | g07 MOVING_END(A) (A:e07)<br>g08 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g09 CLOSING_END(A,A:track_001) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g10 BRAKE_END(A) (A:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g11 STOP_END(A) (A:e11)<br>g12 MOVING_START(A) (A:e12) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g13 CLOSING_START(A,A:track_001) (A:e13) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g14 TURN_LEFT_START(A) (A:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g15 TRACK_APPEARED_LEFT(A,A:track_002) (A:e15)<br>g16 TRACK_APPEARED_LEFT(A,A:track_003) (A:e16)<br>g17 TRACK_APPEARED_LEFT(A,A:track_005) (A:e17)<br>g18 TRACK_APPEARED_LEFT(A,A:track_008) (A:e18)<br>g19 CLOSING_START(A,A:track_002) (A:e19)<br>g20 CLOSING_START(A,A:track_003) (A:e20)<br>g21 CLOSING_START(A,A:track_005) (A:e21)<br>g22 CLOSING_START(A,A:track_008) (A:e22) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g23 TRACK_APPEARED_LEFT(A,A:track_004) (A:e23)<br>g24 CLOSING_START(A,A:track_004) (A:e24) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g25 TRACK_APPEARED_LEFT(A,A:track_006) (A:e25)<br>g26 TRACK_APPEARED_RIGHT(A,A:track_007) (A:e26)<br>g27 CLOSING_START(A,A:track_006) (A:e27) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g28 TRACK_APPEARED_LEFT(A,A:track_010) (A:e28)<br>g29 TRACK_APPEARED_LEFT(A,A:track_011) (A:e29)<br>g30 TRACK_APPEARED_RIGHT(A,A:track_009) (A:e30)<br>g31 CLOSING_START(A,A:track_010) (A:e31)<br>g32 CLOSING_START(A,A:track_011) (A:e32) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g33 TRACK_APPEARED_LEFT(A,A:track_012) (A:e33)<br>g34 TRACK_APPEARED_LEFT(A,A:track_017) (A:e34)<br>g35 CLOSING_START(A,A:track_012) (A:e35)<br>g36 CLOSING_START(A,A:track_017) (A:e36) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g37 TRACK_APPEARED_LEFT(A,A:track_014) (A:e37)<br>g38 TRACK_APPEARED_RIGHT(A,A:track_013) (A:e38)<br>g39 CLOSING_START(A,A:track_014) (A:e39)<br>g40 TRACK_LOST(A,A:track_007) (A:e40) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_017: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g41 TRACK_APPEARED_LEFT(A,A:track_015) (A:e41)<br>g42 CLOSING_START(A,A:track_015) (A:e42) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g43 TRACK_APPEARED_RIGHT(A,A:track_016) (A:e43)<br>g44 CLOSING_START(A,A:track_016) (A:e44) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g45 TRACK_LOST(A,A:track_009) (A:e45) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g46 TRACK_APPEARED_RIGHT(A,A:track_018) (A:e46)<br>g47 CLOSING_START(A,A:track_018) (A:e47) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g48 CLOSING_END(A,A:track_016) (A:e48) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g49 CLOSING_START(A,A:track_016) (A:e49) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g50 CRITICAL_TTC_START(A,A:track_001) (A:e50) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g51 CLOSING_START(A,A:track_013) (A:e51) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: no active state<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g52 TRACK_LOST(A,A:track_018) (A:e52) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_007, track_009<br>sign-0: STOP sign known, relevant to the path |
| - | A | g53 TRACK_LOST(A,A:track_016) (A:e53) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g54 TRACK_LOST(A,A:track_015) (A:e54) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g55 EGO_PATH_ENTRY(A,A:track_014) (A:e55) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g56 CRITICAL_TTC_END(A,A:track_001) (A:e56) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g57 TRACK_LOST(A,A:track_010) (A:e57) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g58 TRACK_LOST(A,A:track_001) (A:e58) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g59 TURN_LEFT_END(A) (A:e59) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g60 EGO_PATH_EXIT(A,A:track_014) (A:e60) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING, IN_EGO_PATH<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g61 EGO_PATH_ENTRY(A,A:track_008) (A:e61) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g62 TRACK_LOST(A,A:track_006) (A:e62) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g63 TRACK_LOST(A,A:track_013) (A:e63) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g64 TRACK_LOST(A,A:track_017) (A:e64) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_014: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_013, track_015, track_016, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g65 TRACK_LOST(A,A:track_012) (A:e65) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_012: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_013, track_015, track_016, track_017, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | A | g66 TRACK_LOST(A,A:track_004) (A:e66) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING, IN_EGO_PATH<br>track_011: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_006, track_007, track_009, track_010, track_012, track_013, track_015, track_016, track_017, track_018<br>sign-0: STOP sign known, relevant to the path |
| - | B | g67 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g68 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| - | B | g69 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known |
| - | B | g70 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-0: STOP sign known |
| - | B | g71 MOVING_END(B) (B:e05)<br>g72 STOP_START(B) (B:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| - | B | g73 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e07)<br>g74 CLOSING_START(B,B:track_001) (B:e08) | ego: STOP, BRAKE<br>sign-0: STOP sign known |
| - | B | g75 EGO_PATH_ENTRY(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g76 EGO_PATH_EXIT(B,B:track_001) (B:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known |
| - | B | g77 BRAKE_END(B) (B:e11) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g78 CRITICAL_TTC_START(B,B:track_001) (B:e12) | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g79 CRITICAL_TTC_END(B,B:track_001) (B:e13)<br>g80 STOP_END(B) (B:e14)<br>g81 MOVING_START(B) (B:e15) | ego: STOP<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g82 TRACK_LOST(B,B:track_001) (B:e16) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.65 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 2.25 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.65 s) A started braking.
- (unaligned, A local time 2.95 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 2.95 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.40 s) A stopped moving.
- (unaligned, A local time 3.40 s) A came to a stop.
- (unaligned, A local time 4.70 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.45 s) A released the brake.
- (unaligned, A local time 6.80 s) A left its stop.
- (unaligned, A local time 6.80 s) A started moving.
- (unaligned, A local time 7.15 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 7.80 s) A started turning left.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_003, which appeared on its left.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_008, which appeared on its left.
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 8.30 s) A's radar started tracking unidentified object A:track_004, which appeared on its left.
- (unaligned, A local time 8.30 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 8.80 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 8.80 s) A's radar started tracking unidentified object A:track_007, which appeared on its right.
- (unaligned, A local time 8.80 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 8.85 s) A's radar started tracking unidentified object A:track_010, which appeared on its left.
- (unaligned, A local time 8.85 s) A's radar started tracking unidentified object A:track_011, which appeared on its left.
- (unaligned, A local time 8.85 s) A's radar started tracking unidentified object A:track_009, which appeared on its right.
- (unaligned, A local time 8.85 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 8.85 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 8.90 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 8.90 s) A's radar started tracking unidentified object A:track_017, which appeared on its left.
- (unaligned, A local time 8.90 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 8.90 s) A observed unidentified object A:track_017 start closing in (already the case when first observed).
- (unaligned, A local time 9.00 s) A's radar started tracking unidentified object A:track_014, which appeared on its left.
- (unaligned, A local time 9.00 s) A's radar started tracking unidentified object A:track_013, which appeared on its right.
- (unaligned, A local time 9.00 s) A observed unidentified object A:track_014 start closing in (already the case when first observed).
- (unaligned, A local time 9.00 s) A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.05 s) A's radar started tracking unidentified object A:track_015, which appeared on its left.
- (unaligned, A local time 9.05 s) A observed unidentified object A:track_015 start closing in (already the case when first observed).
- (unaligned, A local time 9.10 s) A's radar started tracking unidentified object A:track_016, which appeared on its right.
- (unaligned, A local time 9.10 s) A observed unidentified object A:track_016 start closing in (already the case when first observed).
- (unaligned, A local time 9.20 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.25 s) A's radar started tracking unidentified object A:track_018, which appeared on its right.
- (unaligned, A local time 9.25 s) A observed unidentified object A:track_018 start closing in (already the case when first observed).
- (unaligned, A local time 9.40 s) A observed unidentified object A:track_016 stop closing in.
- (unaligned, A local time 9.60 s) A observed unidentified object A:track_016 start closing in.
- (unaligned, A local time 9.75 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 9.80 s) A observed unidentified object A:track_013 start closing in.
- (unaligned, A local time 10.10 s) A's radar lost unidentified object A:track_018 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.40 s) A's radar lost unidentified object A:track_016 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.45 s) A's radar lost unidentified object A:track_015 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.60 s) A observed unidentified object A:track_014 enter its forward path corridor.
- (unaligned, A local time 10.65 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 10.70 s) A's radar lost unidentified object A:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.00 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.05 s) A stopped turning left.
- (unaligned, A local time 11.20 s) A observed unidentified object A:track_014 leave its forward path corridor.
- (unaligned, A local time 11.90 s) A observed unidentified object A:track_008 enter its forward path corridor.
- (unaligned, A local time 12.30 s) A's radar lost unidentified object A:track_006 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 13.50 s) A's radar lost unidentified object A:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.30 s) A's radar lost unidentified object A:track_017 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.35 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.50 s) A's radar lost unidentified object A:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 4.00 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 4.35 s) B started braking.
- (unaligned, B local time 4.70 s) B stopped moving.
- (unaligned, B local time 4.70 s) B came to a stop.
- (unaligned, B local time 6.90 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 6.90 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 8.50 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 9.05 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 10.45 s) B released the brake.
- (unaligned, B local time 10.55 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 10.85 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 10.85 s) B left its stop.
- (unaligned, B local time 10.85 s) B started moving.
- (unaligned, B local time 11.15 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
