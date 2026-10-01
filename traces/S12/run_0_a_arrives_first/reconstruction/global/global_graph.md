# Global graph - S12/run_0_a_arrives_first

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.65 |  |
| g05 | - | HARD_BRAKE_START | A | - | A:e05 @ 2.65 |  |
| g06 | - | MOVING_END | A | - | A:e06 @ 3.40 |  |
| g07 | - | STOP_START | A | - | A:e07 @ 3.40 |  |
| g08 | - | HARD_BRAKE_END | A | - | A:e08 @ 6.45 |  |
| g09 | - | BRAKE_END | A | - | A:e09 @ 6.45 |  |
| g10 | - | STRONG_THROTTLE_START | A | - | A:e10 @ 6.45 |  |
| g11 | - | STOP_END | A | - | A:e11 @ 6.80 |  |
| g12 | - | MOVING_START | A | - | A:e12 @ 6.80 |  |
| g13 | - | STRONG_THROTTLE_END | A | - | A:e13 @ 7.80 |  |
| g14 | - | TRACK_APPEARED | A | A:track_001 | A:e14 @ 8.85 |  |
| g15 | - | TRACK_APPEARED | A | A:track_002 | A:e15 @ 8.85 |  |
| g16 | - | CLOSING_START | A | A:track_001 | A:e16 @ 8.85 | active_at_first_observation=True |
| g17 | - | CLOSING_START | A | A:track_002 | A:e17 @ 8.85 | active_at_first_observation=True |
| g18 | - | TRACK_APPEARED | A | A:track_003 | A:e18 @ 8.95 |  |
| g19 | - | CLOSING_START | A | A:track_003 | A:e19 @ 8.95 | active_at_first_observation=True |
| g20 | - | TRACK_APPEARED | A | A:track_004 | A:e20 @ 9.00 |  |
| g21 | - | CLOSING_START | A | A:track_004 | A:e21 @ 9.00 | active_at_first_observation=True |
| g22 | - | TRACK_APPEARED | A | A:track_005 | A:e22 @ 9.05 |  |
| g23 | - | TRACK_APPEARED | A | A:track_007 | A:e23 @ 9.05 |  |
| g24 | - | CLOSING_START | A | A:track_005 | A:e24 @ 9.05 | active_at_first_observation=True |
| g25 | - | CLOSING_START | A | A:track_007 | A:e25 @ 9.05 | active_at_first_observation=True |
| g26 | - | TRACK_APPEARED | A | A:track_006 | A:e26 @ 9.10 |  |
| g27 | - | TRACK_APPEARED | A | A:track_008 | A:e27 @ 9.10 |  |
| g28 | - | CLOSING_START | A | A:track_006 | A:e28 @ 9.10 | active_at_first_observation=True |
| g29 | - | CLOSING_START | A | A:track_008 | A:e29 @ 9.10 | active_at_first_observation=True |
| g30 | - | TRACK_APPEARED | A | A:track_009 | A:e30 @ 9.15 |  |
| g31 | - | CLOSING_START | A | A:track_009 | A:e31 @ 9.15 | active_at_first_observation=True |
| g32 | - | TRACK_APPEARED | A | A:track_010 | A:e32 @ 9.20 |  |
| g33 | - | TRACK_APPEARED | A | A:track_011 | A:e33 @ 9.20 |  |
| g34 | - | CLOSING_START | A | A:track_010 | A:e34 @ 9.20 | active_at_first_observation=True |
| g35 | - | CLOSING_START | A | A:track_011 | A:e35 @ 9.20 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED | A | A:track_012 | A:e36 @ 9.25 |  |
| g37 | - | CLOSING_START | A | A:track_012 | A:e37 @ 9.25 | active_at_first_observation=True |
| g38 | - | CRITICAL_TTC_START | A | A:track_009 | A:e38 @ 9.45 |  |
| g39 | - | CRITICAL_TTC_START | A | A:track_004 | A:e39 @ 10.05 |  |
| g40 | - | TRACK_LOST | A | A:track_004 | A:e40 @ 10.25 |  |
| g41 | - | TRACK_LOST | A | A:track_009 | A:e41 @ 10.70 |  |
| g42 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e42 @ 12.00 |  |
| g43 | - | TRACK_LOST | A | A:track_012 | A:e43 @ 12.25 |  |
| g44 | - | TRACK_LOST | A | A:track_011 | A:e44 @ 12.75 |  |
| g45 | - | TRACK_LOST | A | A:track_006 | A:e45 @ 13.35 |  |
| g46 | - | TRACK_LOST | A | A:track_008 | A:e46 @ 14.50 |  |
| g47 | - | TRACK_LOST | A | A:track_010 | A:e47 @ 14.65 |  |
| g48 | - | PREDICTED_PATH_CONFLICT_START | A | A:track_001 | A:e48 @ 15.55 |  |
| g49 | - | TRACK_LOST | A | A:track_005 | A:e49 @ 15.75 |  |
| g50 | - | TRACK_LOST | A | A:track_007 | A:e50 @ 16.30 |  |
| g51 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g52 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.65 |  |
| g53 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 2.10 |  |
| g54 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e04 @ 2.10 | relevant_to_ego_path=False |
| g55 | - | TRACK_APPEARED | B | B:track_001 | B:e05 @ 3.00 |  |
| g56 | - | CLOSING_START | B | B:track_001 | B:e06 @ 3.00 | active_at_first_observation=True |
| g57 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e07 @ 4.00 |  |
| g58 | - | BRAKE_START | B | - | B:e08 @ 4.35 |  |
| g59 | - | HARD_BRAKE_START | B | - | B:e09 @ 4.35 |  |
| g60 | - | CLOSING_END | B | B:track_001 | B:e10 @ 4.70 |  |
| g61 | - | MOVING_END | B | - | B:e11 @ 4.70 |  |
| g62 | - | STOP_START | B | - | B:e12 @ 4.70 |  |
| g63 | - | CLOSING_START | B | B:track_001 | B:e13 @ 6.95 |  |
| g64 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e14 @ 8.50 |  |
| g65 | - | EGO_PATH_EXIT | B | B:track_001 | B:e15 @ 9.05 |  |
| g66 | - | CRITICAL_TTC_START | B | B:track_001 | B:e16 @ 9.55 |  |
| g67 | - | HARD_BRAKE_END | B | - | B:e17 @ 10.45 |  |
| g68 | - | BRAKE_END | B | - | B:e18 @ 10.45 |  |
| g69 | - | STRONG_THROTTLE_START | B | - | B:e19 @ 10.45 |  |
| g70 | - | STOP_END | B | - | B:e20 @ 10.85 |  |
| g71 | - | MOVING_START | B | - | B:e21 @ 10.85 |  |
| g72 | - | TRACK_LOST | B | B:track_001 | B:e22 @ 10.85 |  |
| g73 | - | STRONG_THROTTLE_END | B | - | B:e23 @ 11.95 |  |

## Edges

```
    g14 --SAME_TRACK--> g16
    g15 --SAME_TRACK--> g17
    g18 --SAME_TRACK--> g19
    g20 --SAME_TRACK--> g21
    g22 --SAME_TRACK--> g24
    g23 --SAME_TRACK--> g25
    g26 --SAME_TRACK--> g28
    g27 --SAME_TRACK--> g29
    g30 --SAME_TRACK--> g31
    g32 --SAME_TRACK--> g34
    g33 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g37
    g30 --SAME_TRACK--> g38
    g20 --SAME_TRACK--> g39
    g20 --SAME_TRACK--> g40
    g30 --SAME_TRACK--> g41
    g14 --SAME_TRACK--> g42
    g36 --SAME_TRACK--> g43
    g33 --SAME_TRACK--> g44
    g26 --SAME_TRACK--> g45
    g27 --SAME_TRACK--> g46
    g32 --SAME_TRACK--> g47
    g14 --SAME_TRACK--> g48
    g22 --SAME_TRACK--> g49
    g23 --SAME_TRACK--> g50
    g55 --SAME_TRACK--> g56
    g55 --SAME_TRACK--> g60
    g55 --SAME_TRACK--> g63
    g55 --SAME_TRACK--> g64
    g55 --SAME_TRACK--> g65
    g55 --SAME_TRACK--> g66
    g55 --SAME_TRACK--> g72
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
| - | A | g03 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign VISIBLE, known, relevant to the path |
| - | A | g04 BRAKE_START(A) (A:e04)<br>g05 HARD_BRAKE_START(A) (A:e05) | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g06 MOVING_END(A) (A:e06)<br>g07 STOP_START(A) (A:e07) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g08 HARD_BRAKE_END(A) (A:e08)<br>g09 BRAKE_END(A) (A:e09)<br>g10 STRONG_THROTTLE_START(A) (A:e10) | ego: STOP, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g11 STOP_END(A) (A:e11)<br>g12 MOVING_START(A) (A:e12) | ego: STOP, STRONG_THROTTLE<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g13 STRONG_THROTTLE_END(A) (A:e13) | ego: MOVING, STRONG_THROTTLE<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g14 TRACK_APPEARED(A,A:track_001) (A:e14)<br>g15 TRACK_APPEARED(A,A:track_002) (A:e15)<br>g16 CLOSING_START(A,A:track_001) (A:e16)<br>g17 CLOSING_START(A,A:track_002) (A:e17) | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g18 TRACK_APPEARED(A,A:track_003) (A:e18)<br>g19 CLOSING_START(A,A:track_003) (A:e19) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g20 TRACK_APPEARED(A,A:track_004) (A:e20)<br>g21 CLOSING_START(A,A:track_004) (A:e21) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g22 TRACK_APPEARED(A,A:track_005) (A:e22)<br>g23 TRACK_APPEARED(A,A:track_007) (A:e23)<br>g24 CLOSING_START(A,A:track_005) (A:e24)<br>g25 CLOSING_START(A,A:track_007) (A:e25) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g26 TRACK_APPEARED(A,A:track_006) (A:e26)<br>g27 TRACK_APPEARED(A,A:track_008) (A:e27)<br>g28 CLOSING_START(A,A:track_006) (A:e28)<br>g29 CLOSING_START(A,A:track_008) (A:e29) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g30 TRACK_APPEARED(A,A:track_009) (A:e30)<br>g31 CLOSING_START(A,A:track_009) (A:e31) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g32 TRACK_APPEARED(A,A:track_010) (A:e32)<br>g33 TRACK_APPEARED(A,A:track_011) (A:e33)<br>g34 CLOSING_START(A,A:track_010) (A:e34)<br>g35 CLOSING_START(A,A:track_011) (A:e35) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g36 TRACK_APPEARED(A,A:track_012) (A:e36)<br>g37 CLOSING_START(A,A:track_012) (A:e37) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g38 CRITICAL_TTC_START(A,A:track_009) (A:e38) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g39 CRITICAL_TTC_START(A,A:track_004) (A:e39) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g40 TRACK_LOST(A,A:track_004) (A:e40) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING, CRITICAL_TTC<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g41 TRACK_LOST(A,A:track_009) (A:e41) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, CRITICAL_TTC<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g42 EGO_PATH_ENTRY(A,A:track_001) (A:e42) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g43 TRACK_LOST(A,A:track_012) (A:e43) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g44 TRACK_LOST(A,A:track_011) (A:e44) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g45 TRACK_LOST(A,A:track_006) (A:e45) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g46 TRACK_LOST(A,A:track_008) (A:e46) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g47 TRACK_LOST(A,A:track_010) (A:e47) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g48 PREDICTED_PATH_CONFLICT_START(A,A:track_001) (A:e48) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g49 TRACK_LOST(A,A:track_005) (A:e49) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | A | g50 TRACK_LOST(A,A:track_007) (A:e50) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_004, track_005, track_006, track_008, track_009, track_010, track_011, track_012<br>sign-0: STOP sign not visible, known, relevant to the path |
| - | B | g51 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g52 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g53 STRONG_THROTTLE_END(B) (B:e03)<br>g54 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| - | B | g55 TRACK_APPEARED(B,B:track_001) (B:e05)<br>g56 CLOSING_START(B,B:track_001) (B:e06) | ego: MOVING<br>sign-0: STOP sign VISIBLE, known |
| - | B | g57 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign VISIBLE, known |
| - | B | g58 BRAKE_START(B) (B:e08)<br>g59 HARD_BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known |
| - | B | g60 CLOSING_END(B,B:track_001) (B:e10)<br>g61 MOVING_END(B) (B:e11)<br>g62 STOP_START(B) (B:e12) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known |
| - | B | g63 CLOSING_START(B,B:track_001) (B:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE<br>sign-0: STOP sign not visible, known |
| - | B | g64 EGO_PATH_ENTRY(B,B:track_001) (B:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known |
| - | B | g65 EGO_PATH_EXIT(B,B:track_001) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>sign-0: STOP sign not visible, known |
| - | B | g66 CRITICAL_TTC_START(B,B:track_001) (B:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known |
| - | B | g67 HARD_BRAKE_END(B) (B:e17)<br>g68 BRAKE_END(B) (B:e18)<br>g69 STRONG_THROTTLE_START(B) (B:e19) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g70 STOP_END(B) (B:e20)<br>g71 MOVING_START(B) (B:e21)<br>g72 TRACK_LOST(B,B:track_001) (B:e22) | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g73 STRONG_THROTTLE_END(B) (B:e23) | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.65 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 2.25 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.65 s) A started braking.
- (unaligned, A local time 2.65 s) A started braking hard.
- (unaligned, A local time 3.40 s) A stopped moving.
- (unaligned, A local time 3.40 s) A came to a stop.
- (unaligned, A local time 6.45 s) A stopped braking hard.
- (unaligned, A local time 6.45 s) A released the brake.
- (unaligned, A local time 6.45 s) A started applying strong throttle.
- (unaligned, A local time 6.80 s) A left its stop.
- (unaligned, A local time 6.80 s) A started moving.
- (unaligned, A local time 7.80 s) A stopped applying strong throttle.
- (unaligned, A local time 8.85 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 8.85 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 8.85 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 8.85 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 8.95 s) A's radar started tracking unidentified object A:track_003.
- (unaligned, A local time 8.95 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 9.00 s) A's radar started tracking unidentified object A:track_004.
- (unaligned, A local time 9.00 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 9.05 s) A's radar started tracking unidentified object A:track_005.
- (unaligned, A local time 9.05 s) A's radar started tracking unidentified object A:track_007.
- (unaligned, A local time 9.05 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 9.05 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 9.10 s) A's radar started tracking unidentified object A:track_006.
- (unaligned, A local time 9.10 s) A's radar started tracking unidentified object A:track_008.
- (unaligned, A local time 9.10 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 9.10 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 9.15 s) A's radar started tracking unidentified object A:track_009.
- (unaligned, A local time 9.15 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 9.20 s) A's radar started tracking unidentified object A:track_010.
- (unaligned, A local time 9.20 s) A's radar started tracking unidentified object A:track_011.
- (unaligned, A local time 9.20 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 9.20 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 9.25 s) A's radar started tracking unidentified object A:track_012.
- (unaligned, A local time 9.25 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 9.45 s) A's time-to-contact with unidentified object A:track_009 became critical.
- (unaligned, A local time 10.05 s) A's time-to-contact with unidentified object A:track_004 became critical.
- (unaligned, A local time 10.25 s) A's radar lost unidentified object A:track_004 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.70 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 12.00 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 12.25 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 12.75 s) A's radar lost unidentified object A:track_011 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 13.35 s) A's radar lost unidentified object A:track_006 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.50 s) A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.65 s) A's radar lost unidentified object A:track_010 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.55 s) A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- (unaligned, A local time 15.75 s) A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 16.30 s) A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.65 s) B started applying strong throttle.
- (unaligned, B local time 2.10 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 3.00 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 3.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.00 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 4.35 s) B started braking.
- (unaligned, B local time 4.35 s) B started braking hard.
- (unaligned, B local time 4.70 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 4.70 s) B stopped moving.
- (unaligned, B local time 4.70 s) B came to a stop.
- (unaligned, B local time 6.95 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 8.50 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 9.05 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 9.55 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 10.45 s) B stopped braking hard.
- (unaligned, B local time 10.45 s) B released the brake.
- (unaligned, B local time 10.45 s) B started applying strong throttle.
- (unaligned, B local time 10.85 s) B left its stop.
- (unaligned, B local time 10.85 s) B started moving.
- (unaligned, B local time 10.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 11.95 s) B stopped applying strong throttle.
