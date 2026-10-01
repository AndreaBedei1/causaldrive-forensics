# Global graph - S12/run_0_b_arrives_first

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
| A:track_019 | anonymous_track | seen only by A; candidate: - |
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
| A:track_019 | A:track_019 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.95 | relevant_to_ego_path=True |
| g03 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e03 @ 3.10 |  |
| g04 | - | CLOSING_START | A | A:track_001 | A:e04 @ 3.10 | active_at_first_observation=True |
| g05 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e05 @ 3.60 |  |
| g06 | - | BRAKE_START | A | - | A:e06 @ 4.35 |  |
| g07 | - | CLOSING_END | A | A:track_001 | A:e07 @ 4.70 |  |
| g08 | - | MOVING_END | A | - | A:e08 @ 4.75 |  |
| g09 | - | STOP_START | A | - | A:e09 @ 4.75 |  |
| g10 | - | CLOSING_START | A | A:track_001 | A:e10 @ 6.95 |  |
| g11 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e11 @ 9.75 |  |
| g12 | - | CLOSING_END | A | A:track_001 | A:e12 @ 9.90 |  |
| g13 | - | EGO_PATH_EXIT | A | A:track_001 | A:e13 @ 10.20 |  |
| g14 | - | BRAKE_END | A | - | A:e14 @ 10.45 |  |
| g15 | - | STOP_END | A | - | A:e15 @ 10.80 |  |
| g16 | - | MOVING_START | A | - | A:e16 @ 10.80 |  |
| g17 | - | TURN_LEFT_START | A | - | A:e17 @ 12.10 |  |
| g18 | - | TRACK_LOST | A | A:track_001 | A:e18 @ 12.10 |  |
| g19 | - | TRACK_APPEARED_LEFT | A | A:track_006 | A:e19 @ 12.55 |  |
| g20 | - | TRACK_APPEARED_LEFT | A | A:track_007 | A:e20 @ 12.55 |  |
| g21 | - | CLOSING_START | A | A:track_006 | A:e21 @ 12.55 | active_at_first_observation=True |
| g22 | - | CLOSING_START | A | A:track_007 | A:e22 @ 12.55 | active_at_first_observation=True |
| g23 | - | TRACK_APPEARED_LEFT | A | A:track_002 | A:e23 @ 12.60 |  |
| g24 | - | TRACK_APPEARED_LEFT | A | A:track_003 | A:e24 @ 12.60 |  |
| g25 | - | TRACK_APPEARED_LEFT | A | A:track_004 | A:e25 @ 12.60 |  |
| g26 | - | CLOSING_START | A | A:track_002 | A:e26 @ 12.60 | active_at_first_observation=True |
| g27 | - | CLOSING_START | A | A:track_003 | A:e27 @ 12.60 | active_at_first_observation=True |
| g28 | - | CLOSING_START | A | A:track_004 | A:e28 @ 12.60 | active_at_first_observation=True |
| g29 | - | TRACK_APPEARED_LEFT | A | A:track_005 | A:e29 @ 12.65 |  |
| g30 | - | CLOSING_START | A | A:track_005 | A:e30 @ 12.65 | active_at_first_observation=True |
| g31 | - | TRACK_APPEARED_LEFT | A | A:track_009 | A:e31 @ 13.05 |  |
| g32 | - | TRACK_APPEARED_LEFT | A | A:track_013 | A:e32 @ 13.05 |  |
| g33 | - | TRACK_APPEARED_RIGHT | A | A:track_008 | A:e33 @ 13.05 |  |
| g34 | - | CLOSING_START | A | A:track_009 | A:e34 @ 13.05 | active_at_first_observation=True |
| g35 | - | CLOSING_START | A | A:track_013 | A:e35 @ 13.05 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED_LEFT | A | A:track_011 | A:e36 @ 13.10 |  |
| g37 | - | TRACK_APPEARED_LEFT | A | A:track_015 | A:e37 @ 13.10 |  |
| g38 | - | TRACK_APPEARED_RIGHT | A | A:track_010 | A:e38 @ 13.10 |  |
| g39 | - | CLOSING_START | A | A:track_011 | A:e39 @ 13.10 | active_at_first_observation=True |
| g40 | - | CLOSING_START | A | A:track_015 | A:e40 @ 13.10 | active_at_first_observation=True |
| g41 | - | TRACK_APPEARED_LEFT | A | A:track_012 | A:e41 @ 13.15 |  |
| g42 | - | CLOSING_START | A | A:track_012 | A:e42 @ 13.15 | active_at_first_observation=True |
| g43 | - | TRACK_APPEARED_LEFT | A | A:track_014 | A:e43 @ 13.20 |  |
| g44 | - | CLOSING_START | A | A:track_014 | A:e44 @ 13.20 | active_at_first_observation=True |
| g45 | - | TRACK_APPEARED_LEFT | A | A:track_017 | A:e45 @ 13.25 |  |
| g46 | - | TRACK_APPEARED_RIGHT | A | A:track_016 | A:e46 @ 13.25 |  |
| g47 | - | CLOSING_START | A | A:track_017 | A:e47 @ 13.25 | active_at_first_observation=True |
| g48 | - | TRACK_LOST | A | A:track_008 | A:e48 @ 13.30 |  |
| g49 | - | TRACK_APPEARED_RIGHT | A | A:track_018 | A:e49 @ 13.35 |  |
| g50 | - | CLOSING_START | A | A:track_018 | A:e50 @ 13.35 | active_at_first_observation=True |
| g51 | - | TRACK_APPEARED_LEFT | A | A:track_019 | A:e51 @ 13.40 |  |
| g52 | - | CLOSING_START | A | A:track_019 | A:e52 @ 13.40 | active_at_first_observation=True |
| g53 | - | TRACK_LOST | A | A:track_010 | A:e53 @ 13.50 |  |
| g54 | - | CLOSING_START | A | A:track_016 | A:e54 @ 14.00 |  |
| g55 | - | TRACK_LOST | A | A:track_019 | A:e55 @ 14.45 |  |
| g56 | - | TRACK_LOST | A | A:track_018 | A:e56 @ 14.60 |  |
| g57 | - | EGO_PATH_ENTRY | A | A:track_017 | A:e57 @ 14.90 |  |
| g58 | - | TRACK_LOST | A | A:track_014 | A:e58 @ 15.15 |  |
| g59 | - | TURN_LEFT_END | A | - | A:e59 @ 15.30 |  |
| g60 | - | EGO_PATH_ENTRY | A | A:track_006 | A:e60 @ 15.35 |  |
| g61 | - | EGO_PATH_EXIT | A | A:track_017 | A:e61 @ 15.55 |  |
| g62 | - | CUT_IN_FROM_RIGHT_START | A | A:track_016 | A:e62 @ 15.90 |  |
| g63 | - | TRACK_LOST | A | A:track_012 | A:e63 @ 16.05 |  |
| g64 | - | TRACK_LOST | A | A:track_009 | A:e64 @ 16.35 |  |
| g65 | - | TRACK_LOST | A | A:track_004 | A:e65 @ 16.40 |  |
| g66 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g67 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.80 | relevant_to_ego_path=True |
| g68 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 2.60 |  |
| g69 | - | BRAKE_START | B | - | B:e04 @ 2.65 |  |
| g70 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e05 @ 3.05 |  |
| g71 | - | CLOSING_START | B | B:track_001 | B:e06 @ 3.05 | active_at_first_observation=True |
| g72 | - | MOVING_END | B | - | B:e07 @ 3.40 |  |
| g73 | - | STOP_START | B | - | B:e08 @ 3.40 |  |
| g74 | - | CLOSING_END | B | B:track_001 | B:e09 @ 4.70 |  |
| g75 | - | BRAKE_END | B | - | B:e10 @ 6.45 |  |
| g76 | - | STOP_END | B | - | B:e11 @ 6.85 |  |
| g77 | - | MOVING_START | B | - | B:e12 @ 6.85 |  |
| g78 | - | CLOSING_START | B | B:track_001 | B:e13 @ 7.00 |  |
| g79 | - | TRACK_LOST | B | B:track_001 | B:e14 @ 9.45 |  |

## Edges

```
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g18
    g19 --SAME_TRACK--> g21
    g20 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g26
    g24 --SAME_TRACK--> g27
    g25 --SAME_TRACK--> g28
    g29 --SAME_TRACK--> g30
    g31 --SAME_TRACK--> g34
    g32 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g39
    g37 --SAME_TRACK--> g40
    g41 --SAME_TRACK--> g42
    g43 --SAME_TRACK--> g44
    g45 --SAME_TRACK--> g47
    g33 --SAME_TRACK--> g48
    g49 --SAME_TRACK--> g50
    g51 --SAME_TRACK--> g52
    g38 --SAME_TRACK--> g53
    g46 --SAME_TRACK--> g54
    g51 --SAME_TRACK--> g55
    g49 --SAME_TRACK--> g56
    g45 --SAME_TRACK--> g57
    g43 --SAME_TRACK--> g58
    g19 --SAME_TRACK--> g60
    g45 --SAME_TRACK--> g61
    g46 --SAME_TRACK--> g62
    g41 --SAME_TRACK--> g63
    g31 --SAME_TRACK--> g64
    g25 --SAME_TRACK--> g65
    g70 --SAME_TRACK--> g71
    g70 --SAME_TRACK--> g74
    g70 --SAME_TRACK--> g78
    g70 --SAME_TRACK--> g79
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): EGO_PATH_ENTRY 9.75, no critical TTC [local times]
- A's track_006 (unidentified A:track_006): EGO_PATH_ENTRY 15.35, no critical TTC [local times]
- A's track_016 (unidentified A:track_016): CUT_IN_FROM_RIGHT_START 15.90, no critical TTC after it [local times]
- A's track_017 (unidentified A:track_017): EGO_PATH_ENTRY 14.90, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 TRACK_APPEARED_LEFT(A,A:track_001) (A:e03)<br>g04 CLOSING_START(A,A:track_001) (A:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g06 BRAKE_START(A) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g07 CLOSING_END(A,A:track_001) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g08 MOVING_END(A) (A:e08)<br>g09 STOP_START(A) (A:e09) | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g10 CLOSING_START(A,A:track_001) (A:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g11 EGO_PATH_ENTRY(A,A:track_001) (A:e11) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g12 CLOSING_END(A,A:track_001) (A:e12) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g13 EGO_PATH_EXIT(A,A:track_001) (A:e13) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g14 BRAKE_END(A) (A:e14) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g15 STOP_END(A) (A:e15)<br>g16 MOVING_START(A) (A:e16) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g17 TURN_LEFT_START(A) (A:e17)<br>g18 TRACK_LOST(A,A:track_001) (A:e18) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g19 TRACK_APPEARED_LEFT(A,A:track_006) (A:e19)<br>g20 TRACK_APPEARED_LEFT(A,A:track_007) (A:e20)<br>g21 CLOSING_START(A,A:track_006) (A:e21)<br>g22 CLOSING_START(A,A:track_007) (A:e22) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g23 TRACK_APPEARED_LEFT(A,A:track_002) (A:e23)<br>g24 TRACK_APPEARED_LEFT(A,A:track_003) (A:e24)<br>g25 TRACK_APPEARED_LEFT(A,A:track_004) (A:e25)<br>g26 CLOSING_START(A,A:track_002) (A:e26)<br>g27 CLOSING_START(A,A:track_003) (A:e27)<br>g28 CLOSING_START(A,A:track_004) (A:e28) | ego: MOVING, TURN_LEFT<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g29 TRACK_APPEARED_LEFT(A,A:track_005) (A:e29)<br>g30 CLOSING_START(A,A:track_005) (A:e30) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g31 TRACK_APPEARED_LEFT(A,A:track_009) (A:e31)<br>g32 TRACK_APPEARED_LEFT(A,A:track_013) (A:e32)<br>g33 TRACK_APPEARED_RIGHT(A,A:track_008) (A:e33)<br>g34 CLOSING_START(A,A:track_009) (A:e34)<br>g35 CLOSING_START(A,A:track_013) (A:e35) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g36 TRACK_APPEARED_LEFT(A,A:track_011) (A:e36)<br>g37 TRACK_APPEARED_LEFT(A,A:track_015) (A:e37)<br>g38 TRACK_APPEARED_RIGHT(A,A:track_010) (A:e38)<br>g39 CLOSING_START(A,A:track_011) (A:e39)<br>g40 CLOSING_START(A,A:track_015) (A:e40) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g41 TRACK_APPEARED_LEFT(A,A:track_012) (A:e41)<br>g42 CLOSING_START(A,A:track_012) (A:e42) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g43 TRACK_APPEARED_LEFT(A,A:track_014) (A:e43)<br>g44 CLOSING_START(A,A:track_014) (A:e44) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g45 TRACK_APPEARED_LEFT(A,A:track_017) (A:e45)<br>g46 TRACK_APPEARED_RIGHT(A,A:track_016) (A:e46)<br>g47 CLOSING_START(A,A:track_017) (A:e47) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g48 TRACK_LOST(A,A:track_008) (A:e48) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g49 TRACK_APPEARED_RIGHT(A,A:track_018) (A:e49)<br>g50 CLOSING_START(A,A:track_018) (A:e50) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path |
| - | A | g51 TRACK_APPEARED_LEFT(A,A:track_019) (A:e51)<br>g52 CLOSING_START(A,A:track_019) (A:e52) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path |
| - | A | g53 TRACK_LOST(A,A:track_010) (A:e53) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known, relevant to the path |
| - | A | g54 CLOSING_START(A,A:track_016) (A:e54) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: no active state<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010<br>sign-0: STOP sign known, relevant to the path |
| - | A | g55 TRACK_LOST(A,A:track_019) (A:e55) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010<br>sign-0: STOP sign known, relevant to the path |
| - | A | g56 TRACK_LOST(A,A:track_018) (A:e56) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g57 EGO_PATH_ENTRY(A,A:track_017) (A:e57) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g58 TRACK_LOST(A,A:track_014) (A:e58) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g59 TURN_LEFT_END(A) (A:e59) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g60 EGO_PATH_ENTRY(A,A:track_006) (A:e60) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g61 EGO_PATH_EXIT(A,A:track_017) (A:e61) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g62 CUT_IN_FROM_RIGHT_START(A,A:track_016) (A:e62) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g63 TRACK_LOST(A,A:track_012) (A:e63) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g64 TRACK_LOST(A,A:track_009) (A:e64) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_009: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_010, track_012, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | A | g65 TRACK_LOST(A,A:track_004) (A:e65) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_007: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING, CUT_IN_FROM_RIGHT<br>track_017: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_009, track_010, track_012, track_014, track_018, track_019<br>sign-0: STOP sign known, relevant to the path |
| - | B | g66 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g67 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| - | B | g68 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g69 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g70 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e05)<br>g71 CLOSING_START(B,B:track_001) (B:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| - | B | g72 MOVING_END(B) (B:e07)<br>g73 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g74 CLOSING_END(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g75 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g76 STOP_END(B) (B:e11)<br>g77 MOVING_START(B) (B:e12) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g78 CLOSING_START(B,B:track_001) (B:e13) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g79 TRACK_LOST(B,B:track_001) (B:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.95 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 3.10 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 3.10 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.60 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 4.35 s) A started braking.
- (unaligned, A local time 4.70 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.75 s) A stopped moving.
- (unaligned, A local time 4.75 s) A came to a stop.
- (unaligned, A local time 6.95 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 9.75 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 9.90 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 10.20 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 10.45 s) A released the brake.
- (unaligned, A local time 10.80 s) A left its stop.
- (unaligned, A local time 10.80 s) A started moving.
- (unaligned, A local time 12.10 s) A started turning left.
- (unaligned, A local time 12.10 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 12.55 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 12.55 s) A's radar started tracking unidentified object A:track_007, which appeared on its left.
- (unaligned, A local time 12.55 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 12.55 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 12.60 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 12.60 s) A's radar started tracking unidentified object A:track_003, which appeared on its left.
- (unaligned, A local time 12.60 s) A's radar started tracking unidentified object A:track_004, which appeared on its left.
- (unaligned, A local time 12.60 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 12.60 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 12.60 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 12.65 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 12.65 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 13.05 s) A's radar started tracking unidentified object A:track_009, which appeared on its left.
- (unaligned, A local time 13.05 s) A's radar started tracking unidentified object A:track_013, which appeared on its left.
- (unaligned, A local time 13.05 s) A's radar started tracking unidentified object A:track_008, which appeared on its right.
- (unaligned, A local time 13.05 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 13.05 s) A observed unidentified object A:track_013 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_011, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_015, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_010, which appeared on its right.
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_015 start closing in (already the case when first observed).
- (unaligned, A local time 13.15 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 13.15 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 13.20 s) A's radar started tracking unidentified object A:track_014, which appeared on its left.
- (unaligned, A local time 13.20 s) A observed unidentified object A:track_014 start closing in (already the case when first observed).
- (unaligned, A local time 13.25 s) A's radar started tracking unidentified object A:track_017, which appeared on its left.
- (unaligned, A local time 13.25 s) A's radar started tracking unidentified object A:track_016, which appeared on its right.
- (unaligned, A local time 13.25 s) A observed unidentified object A:track_017 start closing in (already the case when first observed).
- (unaligned, A local time 13.30 s) A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 13.35 s) A's radar started tracking unidentified object A:track_018, which appeared on its right.
- (unaligned, A local time 13.35 s) A observed unidentified object A:track_018 start closing in (already the case when first observed).
- (unaligned, A local time 13.40 s) A's radar started tracking unidentified object A:track_019, which appeared on its left.
- (unaligned, A local time 13.40 s) A observed unidentified object A:track_019 start closing in (already the case when first observed).
- (unaligned, A local time 13.50 s) A's radar lost unidentified object A:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.00 s) A observed unidentified object A:track_016 start closing in.
- (unaligned, A local time 14.45 s) A's radar lost unidentified object A:track_019 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.60 s) A's radar lost unidentified object A:track_018 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.90 s) A observed unidentified object A:track_017 enter its forward path corridor.
- (unaligned, A local time 15.15 s) A's radar lost unidentified object A:track_014 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.30 s) A stopped turning left.
- (unaligned, A local time 15.35 s) A observed unidentified object A:track_006 enter its forward path corridor.
- (unaligned, A local time 15.55 s) A observed unidentified object A:track_017 leave its forward path corridor.
- (unaligned, A local time 15.90 s) A observed unidentified object A:track_016 cutting in from the right.
- (unaligned, A local time 16.05 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 16.35 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 16.40 s) A's radar lost unidentified object A:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.80 s) B's camera established a STOP sign detection (unidentified object B:sign-0).
- (unaligned, B local time 2.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.65 s) B started braking.
- (unaligned, B local time 3.05 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 3.05 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 4.70 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.45 s) B released the brake.
- (unaligned, B local time 6.85 s) B left its stop.
- (unaligned, B local time 6.85 s) B started moving.
- (unaligned, B local time 7.00 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 9.45 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
