# Global graph - S12/run_0_b_arrives_first

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.05 | relevant_to_ego_path=True |
| g03 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e03 @ 3.00 |  |
| g04 | - | CLOSING_START | A | A:track_001 | A:e04 @ 3.00 | active_at_first_observation=True |
| g05 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e05 @ 3.55 |  |
| g06 | - | BRAKE_START | A | - | A:e06 @ 4.35 |  |
| g07 | - | HARD_BRAKE_START | A | - | A:e07 @ 4.35 |  |
| g08 | - | CLOSING_END | A | A:track_001 | A:e08 @ 4.70 |  |
| g09 | - | MOVING_END | A | - | A:e09 @ 4.75 |  |
| g10 | - | STOP_START | A | - | A:e10 @ 4.75 |  |
| g11 | - | CLOSING_START | A | A:track_001 | A:e11 @ 7.00 |  |
| g12 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e12 @ 9.70 |  |
| g13 | - | CLOSING_END | A | A:track_001 | A:e13 @ 9.85 |  |
| g14 | - | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 10.20 |  |
| g15 | - | HARD_BRAKE_END | A | - | A:e15 @ 10.45 |  |
| g16 | - | BRAKE_END | A | - | A:e16 @ 10.45 |  |
| g17 | - | STRONG_THROTTLE_START | A | - | A:e17 @ 10.45 |  |
| g18 | - | STOP_END | A | - | A:e18 @ 10.80 |  |
| g19 | - | MOVING_START | A | - | A:e19 @ 10.80 |  |
| g20 | - | TRACK_LOST | A | A:track_001 | A:e20 @ 11.65 |  |
| g21 | - | STRONG_THROTTLE_END | A | - | A:e21 @ 11.80 |  |
| g22 | - | TRACK_APPEARED_LEFT | A | A:track_002 | A:e22 @ 13.10 |  |
| g23 | - | TRACK_APPEARED_LEFT | A | A:track_004 | A:e23 @ 13.10 |  |
| g24 | - | TRACK_APPEARED_LEFT | A | A:track_006 | A:e24 @ 13.10 |  |
| g25 | - | TRACK_APPEARED_RIGHT | A | A:track_003 | A:e25 @ 13.10 |  |
| g26 | - | CLOSING_START | A | A:track_002 | A:e26 @ 13.10 | active_at_first_observation=True |
| g27 | - | CLOSING_START | A | A:track_003 | A:e27 @ 13.10 | active_at_first_observation=True |
| g28 | - | CLOSING_START | A | A:track_004 | A:e28 @ 13.10 | active_at_first_observation=True |
| g29 | - | CLOSING_START | A | A:track_006 | A:e29 @ 13.10 | active_at_first_observation=True |
| g30 | - | TRACK_APPEARED_LEFT | A | A:track_005 | A:e30 @ 13.25 |  |
| g31 | - | CLOSING_START | A | A:track_005 | A:e31 @ 13.25 | active_at_first_observation=True |
| g32 | - | TRACK_APPEARED_LEFT | A | A:track_009 | A:e32 @ 13.30 |  |
| g33 | - | TRACK_APPEARED_RIGHT | A | A:track_007 | A:e33 @ 13.30 |  |
| g34 | - | CLOSING_START | A | A:track_007 | A:e34 @ 13.30 | active_at_first_observation=True |
| g35 | - | CLOSING_START | A | A:track_009 | A:e35 @ 13.30 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED_LEFT | A | A:track_008 | A:e36 @ 13.35 |  |
| g37 | - | TRACK_APPEARED_LEFT | A | A:track_010 | A:e37 @ 13.35 |  |
| g38 | - | CLOSING_START | A | A:track_008 | A:e38 @ 13.35 | active_at_first_observation=True |
| g39 | - | CLOSING_START | A | A:track_010 | A:e39 @ 13.35 | active_at_first_observation=True |
| g40 | - | TRACK_APPEARED_LEFT | A | A:track_011 | A:e40 @ 13.45 |  |
| g41 | - | TRACK_APPEARED_LEFT | A | A:track_012 | A:e41 @ 13.45 |  |
| g42 | - | CLOSING_START | A | A:track_011 | A:e42 @ 13.45 | active_at_first_observation=True |
| g43 | - | CLOSING_START | A | A:track_012 | A:e43 @ 13.45 | active_at_first_observation=True |
| g44 | - | TRACK_APPEARED_LEFT | A | A:track_013 | A:e44 @ 13.50 |  |
| g45 | - | CLOSING_START | A | A:track_013 | A:e45 @ 13.50 | active_at_first_observation=True |
| g46 | - | CRITICAL_TTC_START | A | A:track_007 | A:e46 @ 13.80 |  |
| g47 | - | TRACK_LOST | A | A:track_007 | A:e47 @ 14.00 |  |
| g48 | - | TRACK_LOST | A | A:track_003 | A:e48 @ 14.40 |  |
| g49 | - | EGO_PATH_ENTRY | A | A:track_006 | A:e49 @ 15.00 |  |
| g50 | - | TRACK_LOST | A | A:track_013 | A:e50 @ 15.60 |  |
| g51 | - | EGO_PATH_EXIT | A | A:track_006 | A:e51 @ 15.95 |  |
| g52 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g53 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g54 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g55 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e04 @ 2.10 | relevant_to_ego_path=True |
| g56 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e05 @ 2.60 |  |
| g57 | - | BRAKE_START | B | - | B:e06 @ 2.65 |  |
| g58 | - | HARD_BRAKE_START | B | - | B:e07 @ 2.65 |  |
| g59 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e08 @ 3.00 |  |
| g60 | - | CLOSING_START | B | B:track_001 | B:e09 @ 3.00 | active_at_first_observation=True |
| g61 | - | MOVING_END | B | - | B:e10 @ 3.40 |  |
| g62 | - | STOP_START | B | - | B:e11 @ 3.40 |  |
| g63 | - | CLOSING_END | B | B:track_001 | B:e12 @ 4.70 |  |
| g64 | - | HARD_BRAKE_END | B | - | B:e13 @ 6.45 |  |
| g65 | - | BRAKE_END | B | - | B:e14 @ 6.45 |  |
| g66 | - | STRONG_THROTTLE_START | B | - | B:e15 @ 6.45 |  |
| g67 | - | STOP_END | B | - | B:e16 @ 6.85 |  |
| g68 | - | MOVING_START | B | - | B:e17 @ 6.85 |  |
| g69 | - | CLOSING_START | B | B:track_001 | B:e18 @ 7.00 |  |
| g70 | - | STRONG_THROTTLE_END | B | - | B:e19 @ 7.90 |  |
| g71 | - | TRACK_LOST | B | B:track_001 | B:e20 @ 8.75 |  |

## Edges

```
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g20
    g22 --SAME_TRACK--> g26
    g25 --SAME_TRACK--> g27
    g23 --SAME_TRACK--> g28
    g24 --SAME_TRACK--> g29
    g30 --SAME_TRACK--> g31
    g33 --SAME_TRACK--> g34
    g32 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g38
    g37 --SAME_TRACK--> g39
    g40 --SAME_TRACK--> g42
    g41 --SAME_TRACK--> g43
    g44 --SAME_TRACK--> g45
    g33 --SAME_TRACK--> g46
    g33 --SAME_TRACK--> g47
    g25 --SAME_TRACK--> g48
    g24 --SAME_TRACK--> g49
    g44 --SAME_TRACK--> g50
    g24 --SAME_TRACK--> g51
    g59 --SAME_TRACK--> g60
    g59 --SAME_TRACK--> g63
    g59 --SAME_TRACK--> g69
    g59 --SAME_TRACK--> g71
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 TRACK_APPEARED_LEFT(A,A:track_001) (A:e03)<br>g04 CLOSING_START(A,A:track_001) (A:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g06 BRAKE_START(A) (A:e06)<br>g07 HARD_BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g08 CLOSING_END(A,A:track_001) (A:e08) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g09 MOVING_END(A) (A:e09)<br>g10 STOP_START(A) (A:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g11 CLOSING_START(A,A:track_001) (A:e11) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g12 EGO_PATH_ENTRY(A,A:track_001) (A:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g13 CLOSING_END(A,A:track_001) (A:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g14 EGO_PATH_EXIT(A,A:track_001) (A:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g15 HARD_BRAKE_END(A) (A:e15)<br>g16 BRAKE_END(A) (A:e16)<br>g17 STRONG_THROTTLE_START(A) (A:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g18 STOP_END(A) (A:e18)<br>g19 MOVING_START(A) (A:e19) | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g20 TRACK_LOST(A,A:track_001) (A:e20) | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g21 STRONG_THROTTLE_END(A) (A:e21) | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g22 TRACK_APPEARED_LEFT(A,A:track_002) (A:e22)<br>g23 TRACK_APPEARED_LEFT(A,A:track_004) (A:e23)<br>g24 TRACK_APPEARED_LEFT(A,A:track_006) (A:e24)<br>g25 TRACK_APPEARED_RIGHT(A,A:track_003) (A:e25)<br>g26 CLOSING_START(A,A:track_002) (A:e26)<br>g27 CLOSING_START(A,A:track_003) (A:e27)<br>g28 CLOSING_START(A,A:track_004) (A:e28)<br>g29 CLOSING_START(A,A:track_006) (A:e29) | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g30 TRACK_APPEARED_LEFT(A,A:track_005) (A:e30)<br>g31 CLOSING_START(A,A:track_005) (A:e31) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g32 TRACK_APPEARED_LEFT(A,A:track_009) (A:e32)<br>g33 TRACK_APPEARED_RIGHT(A,A:track_007) (A:e33)<br>g34 CLOSING_START(A,A:track_007) (A:e34)<br>g35 CLOSING_START(A,A:track_009) (A:e35) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g36 TRACK_APPEARED_LEFT(A,A:track_008) (A:e36)<br>g37 TRACK_APPEARED_LEFT(A,A:track_010) (A:e37)<br>g38 CLOSING_START(A,A:track_008) (A:e38)<br>g39 CLOSING_START(A,A:track_010) (A:e39) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g40 TRACK_APPEARED_LEFT(A,A:track_011) (A:e40)<br>g41 TRACK_APPEARED_LEFT(A,A:track_012) (A:e41)<br>g42 CLOSING_START(A,A:track_011) (A:e42)<br>g43 CLOSING_START(A,A:track_012) (A:e43) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g44 TRACK_APPEARED_LEFT(A,A:track_013) (A:e44)<br>g45 CLOSING_START(A,A:track_013) (A:e45) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g46 CRITICAL_TTC_START(A,A:track_007) (A:e46) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g47 TRACK_LOST(A,A:track_007) (A:e47) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| - | A | g48 TRACK_LOST(A,A:track_003) (A:e48) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g49 EGO_PATH_ENTRY(A,A:track_006) (A:e49) | ego: MOVING<br>track_002: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g50 TRACK_LOST(A,A:track_013) (A:e50) | ego: MOVING<br>track_002: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_007<br>sign-0: STOP sign known, relevant to the path |
| - | A | g51 EGO_PATH_EXIT(A,A:track_006) (A:e51) | ego: MOVING<br>track_002: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_007, track_013<br>sign-0: STOP sign known, relevant to the path |
| - | B | g52 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g53 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g54 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g55 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e04) | ego: MOVING |
| - | B | g56 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e05) | ego: MOVING<br>sign-1: STOP sign known, relevant to the path |
| - | B | g57 BRAKE_START(B) (B:e06)<br>g58 HARD_BRAKE_START(B) (B:e07) | ego: MOVING<br>sign-1: STOP sign known, relevant to the path |
| - | B | g59 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e08)<br>g60 CLOSING_START(B,B:track_001) (B:e09) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known, relevant to the path |
| - | B | g61 MOVING_END(B) (B:e10)<br>g62 STOP_START(B) (B:e11) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| - | B | g63 CLOSING_END(B,B:track_001) (B:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| - | B | g64 HARD_BRAKE_END(B) (B:e13)<br>g65 BRAKE_END(B) (B:e14)<br>g66 STRONG_THROTTLE_START(B) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path |
| - | B | g67 STOP_END(B) (B:e16)<br>g68 MOVING_START(B) (B:e17) | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path |
| - | B | g69 CLOSING_START(B,B:track_001) (B:e18) | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path |
| - | B | g70 STRONG_THROTTLE_END(B) (B:e19) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| - | B | g71 TRACK_LOST(B,B:track_001) (B:e20) | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.05 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 3.00 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 3.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.55 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 4.35 s) A started braking.
- (unaligned, A local time 4.35 s) A started braking hard.
- (unaligned, A local time 4.70 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.75 s) A stopped moving.
- (unaligned, A local time 4.75 s) A came to a stop.
- (unaligned, A local time 7.00 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 9.70 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 9.85 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 10.20 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 10.45 s) A stopped braking hard.
- (unaligned, A local time 10.45 s) A released the brake.
- (unaligned, A local time 10.45 s) A started applying strong throttle.
- (unaligned, A local time 10.80 s) A left its stop.
- (unaligned, A local time 10.80 s) A started moving.
- (unaligned, A local time 11.65 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.80 s) A stopped applying strong throttle.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_004, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_003, which appeared on its right.
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 13.25 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 13.25 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 13.30 s) A's radar started tracking unidentified object A:track_009, which appeared on its left.
- (unaligned, A local time 13.30 s) A's radar started tracking unidentified object A:track_007, which appeared on its right.
- (unaligned, A local time 13.30 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 13.30 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 13.35 s) A's radar started tracking unidentified object A:track_008, which appeared on its left.
- (unaligned, A local time 13.35 s) A's radar started tracking unidentified object A:track_010, which appeared on its left.
- (unaligned, A local time 13.35 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 13.35 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 13.45 s) A's radar started tracking unidentified object A:track_011, which appeared on its left.
- (unaligned, A local time 13.45 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 13.45 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 13.45 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 13.50 s) A's radar started tracking unidentified object A:track_013, which appeared on its left.
- (unaligned, A local time 13.50 s) A observed unidentified object A:track_013 start closing in (already the case when first observed).
- (unaligned, A local time 13.80 s) A's time-to-contact with unidentified object A:track_007 became critical.
- (unaligned, A local time 14.00 s) A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.40 s) A's radar lost unidentified object A:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.00 s) A observed unidentified object A:track_006 enter its forward path corridor.
- (unaligned, A local time 15.60 s) A's radar lost unidentified object A:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.95 s) A observed unidentified object A:track_006 leave its forward path corridor.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-1).
- (unaligned, B local time 2.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.65 s) B started braking.
- (unaligned, B local time 2.65 s) B started braking hard.
- (unaligned, B local time 3.00 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 3.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 4.70 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.45 s) B stopped braking hard.
- (unaligned, B local time 6.45 s) B released the brake.
- (unaligned, B local time 6.45 s) B started applying strong throttle.
- (unaligned, B local time 6.85 s) B left its stop.
- (unaligned, B local time 6.85 s) B started moving.
- (unaligned, B local time 7.00 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 7.90 s) B stopped applying strong throttle.
- (unaligned, B local time 8.75 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
