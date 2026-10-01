# Global graph - S10/run_0_stops_then_proceeds

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.85 | relevant_to_ego_path=False |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.15 |  |
| g04 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e04 @ 2.40 |  |
| g05 | - | CLOSING_START | A | A:track_001 | A:e05 @ 2.40 | active_at_first_observation=True |
| g06 | - | BRAKE_START | A | - | A:e06 @ 2.55 |  |
| g07 | - | MOVING_END | A | - | A:e07 @ 3.35 |  |
| g08 | - | STOP_START | A | - | A:e08 @ 3.35 |  |
| g09 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e09 @ 5.80 |  |
| g10 | - | CLOSING_END | A | A:track_001 | A:e10 @ 6.10 |  |
| g11 | - | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 6.25 |  |
| g12 | - | BRAKE_END | A | - | A:e12 @ 6.75 |  |
| g13 | - | STOP_END | A | - | A:e13 @ 7.10 |  |
| g14 | - | MOVING_START | A | - | A:e14 @ 7.10 |  |
| g15 | - | TRACK_LOST | A | A:track_001 | A:e15 @ 7.50 |  |
| g16 | - | TURN_LEFT_START | A | - | A:e16 @ 7.65 |  |
| g17 | - | TRACK_APPEARED_LEFT | A | A:track_002 | A:e17 @ 8.20 |  |
| g18 | - | TRACK_APPEARED_LEFT | A | A:track_003 | A:e18 @ 8.20 |  |
| g19 | - | TRACK_APPEARED_LEFT | A | A:track_005 | A:e19 @ 8.20 |  |
| g20 | - | TRACK_APPEARED_LEFT | A | A:track_006 | A:e20 @ 8.20 |  |
| g21 | - | TRACK_APPEARED_LEFT | A | A:track_007 | A:e21 @ 8.20 |  |
| g22 | - | TRACK_APPEARED_LEFT | A | A:track_008 | A:e22 @ 8.20 |  |
| g23 | - | TRACK_APPEARED_LEFT | A | A:track_012 | A:e23 @ 8.20 |  |
| g24 | - | TRACK_APPEARED_LEFT | A | A:track_013 | A:e24 @ 8.20 |  |
| g25 | - | TRACK_APPEARED_RIGHT | A | A:track_004 | A:e25 @ 8.20 |  |
| g26 | - | CLOSING_START | A | A:track_002 | A:e26 @ 8.20 | active_at_first_observation=True |
| g27 | - | CLOSING_START | A | A:track_003 | A:e27 @ 8.20 | active_at_first_observation=True |
| g28 | - | CLOSING_START | A | A:track_005 | A:e28 @ 8.20 | active_at_first_observation=True |
| g29 | - | CLOSING_START | A | A:track_006 | A:e29 @ 8.20 | active_at_first_observation=True |
| g30 | - | CLOSING_START | A | A:track_007 | A:e30 @ 8.20 | active_at_first_observation=True |
| g31 | - | CLOSING_START | A | A:track_008 | A:e31 @ 8.20 | active_at_first_observation=True |
| g32 | - | CLOSING_START | A | A:track_012 | A:e32 @ 8.20 | active_at_first_observation=True |
| g33 | - | CLOSING_START | A | A:track_013 | A:e33 @ 8.20 | active_at_first_observation=True |
| g34 | - | TRACK_APPEARED_RIGHT | A | A:track_009 | A:e34 @ 8.25 |  |
| g35 | - | TRACK_APPEARED_RIGHT | A | A:track_010 | A:e35 @ 8.25 |  |
| g36 | - | CLOSING_START | A | A:track_010 | A:e36 @ 8.25 | active_at_first_observation=True |
| g37 | - | TRACK_APPEARED_RIGHT | A | A:track_011 | A:e37 @ 8.30 |  |
| g38 | - | CLOSING_START | A | A:track_011 | A:e38 @ 8.30 | active_at_first_observation=True |
| g39 | - | TRACK_APPEARED_LEFT | A | A:track_014 | A:e39 @ 8.45 |  |
| g40 | - | CLOSING_START | A | A:track_014 | A:e40 @ 8.45 | active_at_first_observation=True |
| g41 | - | TRACK_APPEARED_RIGHT | A | A:track_015 | A:e41 @ 8.50 |  |
| g42 | - | CLOSING_START | A | A:track_015 | A:e42 @ 8.50 | active_at_first_observation=True |
| g43 | - | CRITICAL_TTC_START | A | A:track_006 | A:e43 @ 8.50 |  |
| g44 | - | CLOSING_END | A | A:track_010 | A:e44 @ 8.55 |  |
| g45 | - | TRACK_LOST | A | A:track_010 | A:e45 @ 8.55 |  |
| g46 | - | TRACK_LOST | A | A:track_004 | A:e46 @ 8.60 |  |
| g47 | - | TRACK_LOST | A | A:track_008 | A:e47 @ 8.60 |  |
| g48 | - | TRACK_LOST | A | A:track_009 | A:e48 @ 8.65 |  |
| g49 | - | CLOSING_END | A | A:track_011 | A:e49 @ 8.70 |  |
| g50 | - | TRACK_LOST | A | A:track_006 | A:e50 @ 9.10 |  |
| g51 | - | TRACK_LOST | A | A:track_015 | A:e51 @ 9.15 |  |
| g52 | - | CLOSING_START | A | A:track_011 | A:e52 @ 9.30 |  |
| g53 | - | TRACK_LOST | A | A:track_014 | A:e53 @ 10.20 |  |
| g54 | - | TURN_LEFT_END | A | - | A:e54 @ 10.30 |  |
| g55 | - | CUT_IN_FROM_LEFT_START | A | A:track_002 | A:e55 @ 11.00 |  |
| g56 | - | TRACK_LOST | A | A:track_002 | A:e56 @ 11.20 |  |
| g57 | - | CLOSING_END | A | A:track_011 | A:e57 @ 11.65 |  |
| g58 | - | CRITICAL_TTC_START | A | A:track_003 | A:e58 @ 11.75 |  |
| g59 | - | TRACK_LOST | A | A:track_007 | A:e59 @ 11.75 |  |
| g60 | - | CLOSING_START | A | A:track_011 | A:e60 @ 11.95 |  |
| g61 | - | TRACK_LOST | A | A:track_012 | A:e61 @ 12.00 |  |
| g62 | - | CRITICAL_TTC_START | A | A:track_011 | A:e62 @ 12.15 |  |
| g63 | - | CRITICAL_TTC_END | A | A:track_003 | A:e63 @ 12.20 |  |
| g64 | - | CUT_IN_FROM_LEFT_START | A | A:track_003 | A:e64 @ 12.20 |  |
| g65 | - | CUT_IN_FROM_RIGHT_START | A | A:track_011 | A:e65 @ 12.45 |  |
| g66 | - | TRACK_LOST | A | A:track_003 | A:e66 @ 12.50 |  |
| g67 | - | TRACK_LOST | A | A:track_013 | A:e67 @ 13.15 |  |
| g68 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g69 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 2.60 |  |
| g70 | - | CLOSING_START | B | B:track_001 | B:e03 @ 2.60 | active_at_first_observation=True |
| g71 | - | CRITICAL_TTC_START | B | B:track_001 | B:e04 @ 4.40 |  |
| g72 | - | CRITICAL_TTC_END | B | B:track_001 | B:e05 @ 5.60 |  |
| g73 | - | TRACK_LOST | B | B:track_001 | B:e06 @ 5.85 |  |

## Edges

```
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g11
    g04 --SAME_TRACK--> g15
    g17 --SAME_TRACK--> g26
    g18 --SAME_TRACK--> g27
    g19 --SAME_TRACK--> g28
    g20 --SAME_TRACK--> g29
    g21 --SAME_TRACK--> g30
    g22 --SAME_TRACK--> g31
    g23 --SAME_TRACK--> g32
    g24 --SAME_TRACK--> g33
    g35 --SAME_TRACK--> g36
    g37 --SAME_TRACK--> g38
    g39 --SAME_TRACK--> g40
    g41 --SAME_TRACK--> g42
    g20 --SAME_TRACK--> g43
    g35 --SAME_TRACK--> g44
    g35 --SAME_TRACK--> g45
    g25 --SAME_TRACK--> g46
    g22 --SAME_TRACK--> g47
    g34 --SAME_TRACK--> g48
    g37 --SAME_TRACK--> g49
    g20 --SAME_TRACK--> g50
    g41 --SAME_TRACK--> g51
    g37 --SAME_TRACK--> g52
    g39 --SAME_TRACK--> g53
    g17 --SAME_TRACK--> g55
    g17 --SAME_TRACK--> g56
    g37 --SAME_TRACK--> g57
    g18 --SAME_TRACK--> g58
    g21 --SAME_TRACK--> g59
    g37 --SAME_TRACK--> g60
    g23 --SAME_TRACK--> g61
    g37 --SAME_TRACK--> g62
    g18 --SAME_TRACK--> g63
    g18 --SAME_TRACK--> g64
    g37 --SAME_TRACK--> g65
    g18 --SAME_TRACK--> g66
    g24 --SAME_TRACK--> g67
    g69 --SAME_TRACK--> g70
    g69 --SAME_TRACK--> g71
    g69 --SAME_TRACK--> g72
    g69 --SAME_TRACK--> g73
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): EGO_PATH_ENTRY 5.80, no critical TTC [local times]
- A's track_002 (unidentified A:track_002): CUT_IN_FROM_LEFT_START 11.00, no critical TTC after it [local times]
- A's track_003 (unidentified A:track_003): CUT_IN_FROM_LEFT_START 12.20, no critical TTC after it [local times]
- A's track_006 (unidentified A:track_006): CRITICAL_TTC_START 8.50 [local times]
- A's track_011 (unidentified A:track_011): critical TTC already active before the cut-in: CRITICAL_TTC_START 12.15 <= CUT_IN_FROM_RIGHT_START 12.45 (+0.30 s) [local times]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 4.40 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known |
| - | A | g04 TRACK_APPEARED_LEFT(A,A:track_001) (A:e04)<br>g05 CLOSING_START(A,A:track_001) (A:e05) | ego: MOVING<br>sign-0: STOP sign known |
| - | A | g06 BRAKE_START(A) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | A | g07 MOVING_END(A) (A:e07)<br>g08 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | A | g09 EGO_PATH_ENTRY(A,A:track_001) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | A | g10 CLOSING_END(A,A:track_001) (A:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known |
| - | A | g11 EGO_PATH_EXIT(A,A:track_001) (A:e11) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known |
| - | A | g12 BRAKE_END(A) (A:e12) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known |
| - | A | g13 STOP_END(A) (A:e13)<br>g14 MOVING_START(A) (A:e14) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known |
| - | A | g15 TRACK_LOST(A,A:track_001) (A:e15) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known |
| - | A | g16 TURN_LEFT_START(A) (A:e16) | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g17 TRACK_APPEARED_LEFT(A,A:track_002) (A:e17)<br>g18 TRACK_APPEARED_LEFT(A,A:track_003) (A:e18)<br>g19 TRACK_APPEARED_LEFT(A,A:track_005) (A:e19)<br>g20 TRACK_APPEARED_LEFT(A,A:track_006) (A:e20)<br>g21 TRACK_APPEARED_LEFT(A,A:track_007) (A:e21)<br>g22 TRACK_APPEARED_LEFT(A,A:track_008) (A:e22)<br>g23 TRACK_APPEARED_LEFT(A,A:track_012) (A:e23)<br>g24 TRACK_APPEARED_LEFT(A,A:track_013) (A:e24)<br>g25 TRACK_APPEARED_RIGHT(A,A:track_004) (A:e25)<br>g26 CLOSING_START(A,A:track_002) (A:e26)<br>g27 CLOSING_START(A,A:track_003) (A:e27)<br>g28 CLOSING_START(A,A:track_005) (A:e28)<br>g29 CLOSING_START(A,A:track_006) (A:e29)<br>g30 CLOSING_START(A,A:track_007) (A:e30)<br>g31 CLOSING_START(A,A:track_008) (A:e31)<br>g32 CLOSING_START(A,A:track_012) (A:e32)<br>g33 CLOSING_START(A,A:track_013) (A:e33) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g34 TRACK_APPEARED_RIGHT(A,A:track_009) (A:e34)<br>g35 TRACK_APPEARED_RIGHT(A,A:track_010) (A:e35)<br>g36 CLOSING_START(A,A:track_010) (A:e36) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g37 TRACK_APPEARED_RIGHT(A,A:track_011) (A:e37)<br>g38 CLOSING_START(A,A:track_011) (A:e38) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g39 TRACK_APPEARED_LEFT(A,A:track_014) (A:e39)<br>g40 CLOSING_START(A,A:track_014) (A:e40) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g41 TRACK_APPEARED_RIGHT(A,A:track_015) (A:e41)<br>g42 CLOSING_START(A,A:track_015) (A:e42)<br>g43 CRITICAL_TTC_START(A,A:track_006) (A:e43) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g44 CLOSING_END(A,A:track_010) (A:e44)<br>g45 TRACK_LOST(A,A:track_010) (A:e45) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g46 TRACK_LOST(A,A:track_004) (A:e46)<br>g47 TRACK_LOST(A,A:track_008) (A:e47) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_010<br>sign-0: STOP sign known |
| - | A | g48 TRACK_LOST(A,A:track_009) (A:e48) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_009: no active state<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_010<br>sign-0: STOP sign known |
| - | A | g49 CLOSING_END(A,A:track_011) (A:e49) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_009, track_010<br>sign-0: STOP sign known |
| - | A | g50 TRACK_LOST(A,A:track_006) (A:e50) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_008, track_009, track_010<br>sign-0: STOP sign known |
| - | A | g51 TRACK_LOST(A,A:track_015) (A:e51) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010<br>sign-0: STOP sign known |
| - | A | g52 CLOSING_START(A,A:track_011) (A:e52) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_015<br>sign-0: STOP sign known |
| - | A | g53 TRACK_LOST(A,A:track_014) (A:e53) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_015<br>sign-0: STOP sign known |
| - | A | g54 TURN_LEFT_END(A) (A:e54) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g55 CUT_IN_FROM_LEFT_START(A,A:track_002) (A:e55) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g56 TRACK_LOST(A,A:track_002) (A:e56) | ego: MOVING<br>track_002: CLOSING, CUT_IN_FROM_LEFT<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g57 CLOSING_END(A,A:track_011) (A:e57) | ego: MOVING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g58 CRITICAL_TTC_START(A,A:track_003) (A:e58)<br>g59 TRACK_LOST(A,A:track_007) (A:e59) | ego: MOVING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g60 CLOSING_START(A,A:track_011) (A:e60) | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g61 TRACK_LOST(A,A:track_012) (A:e61) | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g62 CRITICAL_TTC_START(A,A:track_011) (A:e62) | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g63 CRITICAL_TTC_END(A,A:track_003) (A:e63)<br>g64 CUT_IN_FROM_LEFT_START(A,A:track_003) (A:e64) | ego: MOVING<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g65 CUT_IN_FROM_RIGHT_START(A,A:track_011) (A:e65) | ego: MOVING<br>track_003: CLOSING, CUT_IN_FROM_LEFT<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g66 TRACK_LOST(A,A:track_003) (A:e66) | ego: MOVING<br>track_003: CLOSING, CUT_IN_FROM_LEFT<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known |
| - | A | g67 TRACK_LOST(A,A:track_013) (A:e67) | ego: MOVING<br>track_005: CLOSING<br>track_011: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006, track_007, track_008, track_009, track_010, track_012, track_014, track_015<br>sign-0: STOP sign known |
| - | B | g68 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g69 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g70 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| - | B | g71 CRITICAL_TTC_START(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g72 CRITICAL_TTC_END(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | B | g73 TRACK_LOST(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.85 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 2.15 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.40 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 2.40 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.55 s) A started braking.
- (unaligned, A local time 3.35 s) A stopped moving.
- (unaligned, A local time 3.35 s) A came to a stop.
- (unaligned, A local time 5.80 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 6.10 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.25 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 6.75 s) A released the brake.
- (unaligned, A local time 7.10 s) A left its stop.
- (unaligned, A local time 7.10 s) A started moving.
- (unaligned, A local time 7.50 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 7.65 s) A started turning left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_003, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_007, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_008, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_013, which appeared on its left.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_004, which appeared on its right.
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_013 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_009, which appeared on its right.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_010, which appeared on its right.
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 8.30 s) A's radar started tracking unidentified object A:track_011, which appeared on its right.
- (unaligned, A local time 8.30 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 8.45 s) A's radar started tracking unidentified object A:track_014, which appeared on its left.
- (unaligned, A local time 8.45 s) A observed unidentified object A:track_014 start closing in (already the case when first observed).
- (unaligned, A local time 8.50 s) A's radar started tracking unidentified object A:track_015, which appeared on its right.
- (unaligned, A local time 8.50 s) A observed unidentified object A:track_015 start closing in (already the case when first observed).
- (unaligned, A local time 8.50 s) A's time-to-contact with unidentified object A:track_006 became critical.
- (unaligned, A local time 8.55 s) A observed unidentified object A:track_010 stop closing in.
- (unaligned, A local time 8.55 s) A's radar lost unidentified object A:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.60 s) A's radar lost unidentified object A:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.60 s) A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.65 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.70 s) A observed unidentified object A:track_011 stop closing in.
- (unaligned, A local time 9.10 s) A's radar lost unidentified object A:track_006 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.15 s) A's radar lost unidentified object A:track_015 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.30 s) A observed unidentified object A:track_011 start closing in.
- (unaligned, A local time 10.20 s) A's radar lost unidentified object A:track_014 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.30 s) A stopped turning left.
- (unaligned, A local time 11.00 s) A observed unidentified object A:track_002 cutting in from the left.
- (unaligned, A local time 11.20 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.65 s) A observed unidentified object A:track_011 stop closing in.
- (unaligned, A local time 11.75 s) A's time-to-contact with unidentified object A:track_003 became critical.
- (unaligned, A local time 11.75 s) A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.95 s) A observed unidentified object A:track_011 start closing in.
- (unaligned, A local time 12.00 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 12.15 s) A's time-to-contact with unidentified object A:track_011 became critical.
- (unaligned, A local time 12.20 s) A's time-to-contact with unidentified object A:track_003 stopped being critical.
- (unaligned, A local time 12.20 s) A observed unidentified object A:track_003 cutting in from the left.
- (unaligned, A local time 12.45 s) A observed unidentified object A:track_011 cutting in from the right.
- (unaligned, A local time 12.50 s) A's radar lost unidentified object A:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 13.15 s) A's radar lost unidentified object A:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.60 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 2.60 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.60 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
