# Global graph - S11/run_0_stops_then_proceeds

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| B:track_003 | anonymous_track | seen only by B; candidate: - |
| B:track_004 | anonymous_track | seen only by B; candidate: - |
| B:track_005 | anonymous_track | seen only by B; candidate: - |
| B:track_006 | anonymous_track | seen only by B; candidate: - |
| B:track_007 | anonymous_track | seen only by B; candidate: - |
| B:track_008 | anonymous_track | seen only by B; candidate: - |
| B:track_009 | anonymous_track | seen only by B; candidate: - |
| B:track_010 | anonymous_track | seen only by B; candidate: - |
| B:track_011 | anonymous_track | seen only by B; candidate: - |
| B:track_012 | anonymous_track | seen only by B; candidate: - |
| B:track_013 | anonymous_track | seen only by B; candidate: - |

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_004 | B:track_004 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_005 | B:track_005 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_006 | B:track_006 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_007 | B:track_007 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_008 | B:track_008 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_009 | B:track_009 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_010 | B:track_010 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_011 | B:track_011 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_012 | B:track_012 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_013 | B:track_013 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e02 @ 2.70 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.70 | active_at_first_observation=True |
| g04 | - | TRACK_LOST | A | A:track_001 | A:e04 @ 5.75 |  |
| g05 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g06 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e02 @ 2.05 | relevant_to_ego_path=False |
| g07 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e03 @ 2.40 |  |
| g08 | - | TRACK_APPEARED_LEFT | B | B:track_001 | B:e04 @ 2.50 |  |
| g09 | - | CLOSING_START | B | B:track_001 | B:e05 @ 2.50 | active_at_first_observation=True |
| g10 | - | BRAKE_START | B | - | B:e06 @ 2.55 |  |
| g11 | - | MOVING_END | B | - | B:e07 @ 3.25 |  |
| g12 | - | STOP_START | B | - | B:e08 @ 3.25 |  |
| g13 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e09 @ 5.80 |  |
| g14 | - | CLOSING_END | B | B:track_001 | B:e10 @ 6.10 |  |
| g15 | - | EGO_PATH_EXIT | B | B:track_001 | B:e11 @ 6.20 |  |
| g16 | - | BRAKE_END | B | - | B:e12 @ 6.75 |  |
| g17 | - | STOP_END | B | - | B:e13 @ 7.20 |  |
| g18 | - | MOVING_START | B | - | B:e14 @ 7.20 |  |
| g19 | - | TURN_LEFT_START | B | - | B:e15 @ 7.95 |  |
| g20 | - | TRACK_LOST | B | B:track_001 | B:e16 @ 7.95 |  |
| g21 | - | TRACK_APPEARED_LEFT | B | B:track_003 | B:e17 @ 8.40 |  |
| g22 | - | TRACK_APPEARED_LEFT | B | B:track_004 | B:e18 @ 8.40 |  |
| g23 | - | TRACK_APPEARED_LEFT | B | B:track_005 | B:e19 @ 8.40 |  |
| g24 | - | TRACK_APPEARED_LEFT | B | B:track_006 | B:e20 @ 8.40 |  |
| g25 | - | TRACK_APPEARED_LEFT | B | B:track_007 | B:e21 @ 8.40 |  |
| g26 | - | TRACK_APPEARED_LEFT | B | B:track_008 | B:e22 @ 8.40 |  |
| g27 | - | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e23 @ 8.40 |  |
| g28 | - | CLOSING_START | B | B:track_003 | B:e24 @ 8.40 | active_at_first_observation=True |
| g29 | - | CLOSING_START | B | B:track_004 | B:e25 @ 8.40 | active_at_first_observation=True |
| g30 | - | CLOSING_START | B | B:track_005 | B:e26 @ 8.40 | active_at_first_observation=True |
| g31 | - | CLOSING_START | B | B:track_006 | B:e27 @ 8.40 | active_at_first_observation=True |
| g32 | - | CLOSING_START | B | B:track_007 | B:e28 @ 8.40 | active_at_first_observation=True |
| g33 | - | CLOSING_START | B | B:track_008 | B:e29 @ 8.40 | active_at_first_observation=True |
| g34 | - | TRACK_APPEARED_LEFT | B | B:track_010 | B:e30 @ 8.45 |  |
| g35 | - | TRACK_APPEARED_RIGHT | B | B:track_009 | B:e31 @ 8.45 |  |
| g36 | - | TRACK_APPEARED_RIGHT | B | B:track_011 | B:e32 @ 8.45 |  |
| g37 | - | CLOSING_START | B | B:track_009 | B:e33 @ 8.45 | active_at_first_observation=True |
| g38 | - | CLOSING_START | B | B:track_010 | B:e34 @ 8.45 | active_at_first_observation=True |
| g39 | - | CLOSING_START | B | B:track_011 | B:e35 @ 8.45 | active_at_first_observation=True |
| g40 | - | TRACK_APPEARED_RIGHT | B | B:track_012 | B:e36 @ 8.60 |  |
| g41 | - | TRACK_APPEARED_RIGHT | B | B:track_013 | B:e37 @ 8.60 |  |
| g42 | - | CLOSING_START | B | B:track_012 | B:e38 @ 8.60 | active_at_first_observation=True |
| g43 | - | CLOSING_START | B | B:track_013 | B:e39 @ 8.60 | active_at_first_observation=True |
| g44 | - | TRACK_LOST | B | B:track_005 | B:e40 @ 8.65 |  |
| g45 | - | TRACK_LOST | B | B:track_002 | B:e41 @ 8.80 |  |
| g46 | - | TRACK_LOST | B | B:track_011 | B:e42 @ 8.80 |  |
| g47 | - | CLOSING_END | B | B:track_009 | B:e43 @ 8.90 |  |
| g48 | - | CRITICAL_TTC_START | B | B:track_004 | B:e44 @ 8.90 |  |
| g49 | - | TRACK_LOST | B | B:track_013 | B:e45 @ 8.95 |  |
| g50 | - | TRACK_LOST | B | B:track_009 | B:e46 @ 9.00 |  |
| g51 | - | TRACK_LOST | B | B:track_004 | B:e47 @ 9.50 |  |
| g52 | - | TRACK_LOST | B | B:track_010 | B:e48 @ 9.70 |  |
| g53 | - | TURN_LEFT_END | B | - | B:e49 @ 10.70 |  |
| g54 | - | TRACK_LOST | B | B:track_003 | B:e50 @ 10.70 |  |
| g55 | - | CLOSING_END | B | B:track_012 | B:e51 @ 12.05 |  |
| g56 | - | TRACK_LOST | B | B:track_008 | B:e52 @ 12.20 |  |
| g57 | - | CLOSING_START | B | B:track_012 | B:e53 @ 12.30 |  |
| g58 | - | CUT_IN_FROM_LEFT_START | B | B:track_007 | B:e54 @ 12.55 |  |
| g59 | - | CUT_IN_FROM_RIGHT_START | B | B:track_012 | B:e55 @ 12.75 |  |
| g60 | - | TRACK_LOST | B | B:track_007 | B:e56 @ 12.90 |  |
| g61 | - | TRACK_LOST | B | B:track_012 | B:e57 @ 13.05 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g14
    g08 --SAME_TRACK--> g15
    g08 --SAME_TRACK--> g20
    g21 --SAME_TRACK--> g28
    g22 --SAME_TRACK--> g29
    g23 --SAME_TRACK--> g30
    g24 --SAME_TRACK--> g31
    g25 --SAME_TRACK--> g32
    g26 --SAME_TRACK--> g33
    g35 --SAME_TRACK--> g37
    g34 --SAME_TRACK--> g38
    g36 --SAME_TRACK--> g39
    g40 --SAME_TRACK--> g42
    g41 --SAME_TRACK--> g43
    g23 --SAME_TRACK--> g44
    g27 --SAME_TRACK--> g45
    g36 --SAME_TRACK--> g46
    g35 --SAME_TRACK--> g47
    g22 --SAME_TRACK--> g48
    g41 --SAME_TRACK--> g49
    g35 --SAME_TRACK--> g50
    g22 --SAME_TRACK--> g51
    g34 --SAME_TRACK--> g52
    g21 --SAME_TRACK--> g54
    g40 --SAME_TRACK--> g55
    g26 --SAME_TRACK--> g56
    g40 --SAME_TRACK--> g57
    g25 --SAME_TRACK--> g58
    g40 --SAME_TRACK--> g59
    g25 --SAME_TRACK--> g60
    g40 --SAME_TRACK--> g61
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- B's track_001 (unidentified B:track_001): EGO_PATH_ENTRY 5.80, no critical TTC [local times]
- B's track_004 (unidentified B:track_004): CRITICAL_TTC_START 8.90 [local times]
- B's track_007 (unidentified B:track_007): CUT_IN_FROM_LEFT_START 12.55, no critical TTC after it [local times]
- B's track_012 (unidentified B:track_012): CUT_IN_FROM_RIGHT_START 12.75, no critical TTC after it [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 TRACK_LOST(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g05 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g06 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e02) | ego: MOVING |
| - | B | g07 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e03) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g08 TRACK_APPEARED_LEFT(B,B:track_001) (B:e04)<br>g09 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g10 BRAKE_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g11 MOVING_END(B) (B:e07)<br>g12 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g13 EGO_PATH_ENTRY(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g14 CLOSING_END(B,B:track_001) (B:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g15 EGO_PATH_EXIT(B,B:track_001) (B:e11) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g16 BRAKE_END(B) (B:e12) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g17 STOP_END(B) (B:e13)<br>g18 MOVING_START(B) (B:e14) | ego: STOP<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g19 TURN_LEFT_START(B) (B:e15)<br>g20 TRACK_LOST(B,B:track_001) (B:e16) | ego: MOVING<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g21 TRACK_APPEARED_LEFT(B,B:track_003) (B:e17)<br>g22 TRACK_APPEARED_LEFT(B,B:track_004) (B:e18)<br>g23 TRACK_APPEARED_LEFT(B,B:track_005) (B:e19)<br>g24 TRACK_APPEARED_LEFT(B,B:track_006) (B:e20)<br>g25 TRACK_APPEARED_LEFT(B,B:track_007) (B:e21)<br>g26 TRACK_APPEARED_LEFT(B,B:track_008) (B:e22)<br>g27 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e23)<br>g28 CLOSING_START(B,B:track_003) (B:e24)<br>g29 CLOSING_START(B,B:track_004) (B:e25)<br>g30 CLOSING_START(B,B:track_005) (B:e26)<br>g31 CLOSING_START(B,B:track_006) (B:e27)<br>g32 CLOSING_START(B,B:track_007) (B:e28)<br>g33 CLOSING_START(B,B:track_008) (B:e29) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g34 TRACK_APPEARED_LEFT(B,B:track_010) (B:e30)<br>g35 TRACK_APPEARED_RIGHT(B,B:track_009) (B:e31)<br>g36 TRACK_APPEARED_RIGHT(B,B:track_011) (B:e32)<br>g37 CLOSING_START(B,B:track_009) (B:e33)<br>g38 CLOSING_START(B,B:track_010) (B:e34)<br>g39 CLOSING_START(B,B:track_011) (B:e35) | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g40 TRACK_APPEARED_RIGHT(B,B:track_012) (B:e36)<br>g41 TRACK_APPEARED_RIGHT(B,B:track_013) (B:e37)<br>g42 CLOSING_START(B,B:track_012) (B:e38)<br>g43 CLOSING_START(B,B:track_013) (B:e39) | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g44 TRACK_LOST(B,B:track_005) (B:e40) | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g45 TRACK_LOST(B,B:track_002) (B:e41)<br>g46 TRACK_LOST(B,B:track_011) (B:e42) | ego: MOVING, TURN_LEFT<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known |
| - | B | g47 CLOSING_END(B,B:track_009) (B:e43)<br>g48 CRITICAL_TTC_START(B,B:track_004) (B:e44) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011<br>sign-1: STOP sign known |
| - | B | g49 TRACK_LOST(B,B:track_013) (B:e45) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: no active state<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011<br>sign-1: STOP sign known |
| - | B | g50 TRACK_LOST(B,B:track_009) (B:e46) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: no active state<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g51 TRACK_LOST(B,B:track_004) (B:e47) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_004: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_009, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g52 TRACK_LOST(B,B:track_010) (B:e48) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g53 TURN_LEFT_END(B) (B:e49)<br>g54 TRACK_LOST(B,B:track_003) (B:e50) | ego: MOVING, TURN_LEFT<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g55 CLOSING_END(B,B:track_012) (B:e51) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g56 TRACK_LOST(B,B:track_008) (B:e52) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g57 CLOSING_START(B,B:track_012) (B:e53) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g58 CUT_IN_FROM_LEFT_START(B,B:track_007) (B:e54) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g59 CUT_IN_FROM_RIGHT_START(B,B:track_012) (B:e55) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g60 TRACK_LOST(B,B:track_007) (B:e56) | ego: MOVING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT<br>track_012: CLOSING, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |
| - | B | g61 TRACK_LOST(B,B:track_012) (B:e57) | ego: MOVING<br>track_006: CLOSING<br>track_012: CLOSING, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009, track_010, track_011, track_013<br>sign-1: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.70 s) A's radar started tracking unidentified object A:track_001, which appeared on its right.
- (unaligned, A local time 2.70 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 5.75 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.05 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.40 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.50 s) B's radar started tracking unidentified object B:track_001, which appeared on its left.
- (unaligned, B local time 2.50 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 6.75 s) B released the brake.
- (unaligned, B local time 7.20 s) B left its stop.
- (unaligned, B local time 7.20 s) B started moving.
- (unaligned, B local time 7.95 s) B started turning left.
- (unaligned, B local time 7.95 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_003, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_004, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_005, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_006, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_007, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_008, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_002, which appeared on its right.
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_004 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_005 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_006 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_007 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_008 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_010, which appeared on its left.
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_009, which appeared on its right.
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_011, which appeared on its right.
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_009 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_010 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_011 start closing in (already the case when first observed).
- (unaligned, B local time 8.60 s) B's radar started tracking unidentified object B:track_012, which appeared on its right.
- (unaligned, B local time 8.60 s) B's radar started tracking unidentified object B:track_013, which appeared on its right.
- (unaligned, B local time 8.60 s) B observed unidentified object B:track_012 start closing in (already the case when first observed).
- (unaligned, B local time 8.60 s) B observed unidentified object B:track_013 start closing in (already the case when first observed).
- (unaligned, B local time 8.65 s) B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.80 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.80 s) B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.90 s) B observed unidentified object B:track_009 stop closing in.
- (unaligned, B local time 8.90 s) B's time-to-contact with unidentified object B:track_004 became critical.
- (unaligned, B local time 8.95 s) B's radar lost unidentified object B:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.00 s) B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.50 s) B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.70 s) B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 10.70 s) B stopped turning left.
- (unaligned, B local time 10.70 s) B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 12.05 s) B observed unidentified object B:track_012 stop closing in.
- (unaligned, B local time 12.20 s) B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 12.30 s) B observed unidentified object B:track_012 start closing in.
- (unaligned, B local time 12.55 s) B observed unidentified object B:track_007 cutting in from the left.
- (unaligned, B local time 12.75 s) B observed unidentified object B:track_012 cutting in from the right.
- (unaligned, B local time 12.90 s) B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 13.05 s) B's radar lost unidentified object B:track_012 (its states are UNKNOWN from then on, not ended).
