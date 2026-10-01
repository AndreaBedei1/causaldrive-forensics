# Global graph - S04/run_0_yield

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
| g02 | - | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e02 @ 2.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.00 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 3.15 |  |
| g05 | - | CRITICAL_TTC_END | A | A:track_001 | A:e05 @ 4.95 |  |
| g06 | - | TRACK_LOST | A | A:track_001 | A:e06 @ 5.25 |  |
| g07 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e07 @ 8.20 | relevant_to_ego_path=False |
| g08 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e08 @ 8.45 |  |
| g09 | - | TURN_LEFT_START | A | - | A:e09 @ 8.65 |  |
| g10 | - | TRACK_APPEARED_LEFT | A | A:track_002 | A:e10 @ 9.35 |  |
| g11 | - | TRACK_APPEARED_LEFT | A | A:track_003 | A:e11 @ 9.35 |  |
| g12 | - | TRACK_APPEARED_LEFT | A | A:track_004 | A:e12 @ 9.35 |  |
| g13 | - | TRACK_APPEARED_LEFT | A | A:track_005 | A:e13 @ 9.35 |  |
| g14 | - | TRACK_APPEARED_LEFT | A | A:track_006 | A:e14 @ 9.35 |  |
| g15 | - | TRACK_APPEARED_LEFT | A | A:track_010 | A:e15 @ 9.35 |  |
| g16 | - | CLOSING_START | A | A:track_002 | A:e16 @ 9.35 | active_at_first_observation=True |
| g17 | - | CLOSING_START | A | A:track_003 | A:e17 @ 9.35 | active_at_first_observation=True |
| g18 | - | CLOSING_START | A | A:track_004 | A:e18 @ 9.35 | active_at_first_observation=True |
| g19 | - | CLOSING_START | A | A:track_005 | A:e19 @ 9.35 | active_at_first_observation=True |
| g20 | - | CLOSING_START | A | A:track_006 | A:e20 @ 9.35 | active_at_first_observation=True |
| g21 | - | CLOSING_START | A | A:track_010 | A:e21 @ 9.35 | active_at_first_observation=True |
| g22 | - | TRACK_APPEARED_LEFT | A | A:track_007 | A:e22 @ 9.45 |  |
| g23 | - | TRACK_APPEARED_LEFT | A | A:track_011 | A:e23 @ 9.45 |  |
| g24 | - | CLOSING_START | A | A:track_007 | A:e24 @ 9.45 | active_at_first_observation=True |
| g25 | - | CLOSING_START | A | A:track_011 | A:e25 @ 9.45 | active_at_first_observation=True |
| g26 | - | TRACK_APPEARED_LEFT | A | A:track_012 | A:e26 @ 9.50 |  |
| g27 | - | TRACK_APPEARED_LEFT | A | A:track_014 | A:e27 @ 9.50 |  |
| g28 | - | TRACK_APPEARED_LEFT | A | A:track_015 | A:e28 @ 9.50 |  |
| g29 | - | TRACK_APPEARED_RIGHT | A | A:track_008 | A:e29 @ 9.50 |  |
| g30 | - | TRACK_APPEARED_RIGHT | A | A:track_009 | A:e30 @ 9.50 |  |
| g31 | - | CLOSING_START | A | A:track_009 | A:e31 @ 9.50 | active_at_first_observation=True |
| g32 | - | CLOSING_START | A | A:track_012 | A:e32 @ 9.50 | active_at_first_observation=True |
| g33 | - | CLOSING_START | A | A:track_014 | A:e33 @ 9.50 | active_at_first_observation=True |
| g34 | - | CLOSING_START | A | A:track_015 | A:e34 @ 9.50 | active_at_first_observation=True |
| g35 | - | TRACK_APPEARED_RIGHT | A | A:track_013 | A:e35 @ 9.70 |  |
| g36 | - | TRACK_LOST | A | A:track_008 | A:e36 @ 9.75 |  |
| g37 | - | CLOSING_END | A | A:track_009 | A:e37 @ 9.85 |  |
| g38 | - | TRACK_LOST | A | A:track_011 | A:e38 @ 9.85 |  |
| g39 | - | TRACK_LOST | A | A:track_012 | A:e39 @ 9.85 |  |
| g40 | - | CRITICAL_TTC_START | A | A:track_006 | A:e40 @ 9.90 |  |
| g41 | - | TRACK_LOST | A | A:track_009 | A:e41 @ 9.90 |  |
| g42 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g43 | - | TRACK_APPEARED_LEFT | B | B:track_001 | B:e02 @ 1.95 |  |
| g44 | - | CLOSING_START | B | B:track_001 | B:e03 @ 1.95 | active_at_first_observation=True |
| g45 | - | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g46 | - | MOVING_END | B | - | B:e05 @ 3.90 |  |
| g47 | - | STOP_START | B | - | B:e06 @ 3.90 |  |
| g48 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e07 @ 5.40 |  |
| g49 | - | CLOSING_END | B | B:track_001 | B:e08 @ 5.55 |  |
| g50 | - | EGO_PATH_EXIT | B | B:track_001 | B:e09 @ 5.90 |  |
| g51 | - | BRAKE_END | B | - | B:e10 @ 7.15 |  |
| g52 | - | STOP_END | B | - | B:e11 @ 7.55 |  |
| g53 | - | MOVING_START | B | - | B:e12 @ 7.55 |  |
| g54 | - | TRACK_LOST | B | B:track_001 | B:e13 @ 8.30 |  |
| g55 | - | BRAKE_START | B | - | B:e14 @ 8.75 |  |
| g56 | - | BRAKE_END | B | - | B:e15 @ 9.00 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g10 --SAME_TRACK--> g16
    g11 --SAME_TRACK--> g17
    g12 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g19
    g14 --SAME_TRACK--> g20
    g15 --SAME_TRACK--> g21
    g22 --SAME_TRACK--> g24
    g23 --SAME_TRACK--> g25
    g30 --SAME_TRACK--> g31
    g26 --SAME_TRACK--> g32
    g27 --SAME_TRACK--> g33
    g28 --SAME_TRACK--> g34
    g29 --SAME_TRACK--> g36
    g30 --SAME_TRACK--> g37
    g23 --SAME_TRACK--> g38
    g26 --SAME_TRACK--> g39
    g14 --SAME_TRACK--> g40
    g30 --SAME_TRACK--> g41
    g43 --SAME_TRACK--> g44
    g43 --SAME_TRACK--> g48
    g43 --SAME_TRACK--> g49
    g43 --SAME_TRACK--> g50
    g43 --SAME_TRACK--> g54
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 3.15 [local times]
- A's track_006 (unidentified A:track_006): CRITICAL_TTC_START 9.90 [local times]
- B's track_001 (unidentified B:track_001): EGO_PATH_ENTRY 5.40, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | A | g05 CRITICAL_TTC_END(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | A | g06 TRACK_LOST(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | A | g07 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e07) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| - | A | g08 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e08) | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g09 TURN_LEFT_START(A) (A:e09) | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g10 TRACK_APPEARED_LEFT(A,A:track_002) (A:e10)<br>g11 TRACK_APPEARED_LEFT(A,A:track_003) (A:e11)<br>g12 TRACK_APPEARED_LEFT(A,A:track_004) (A:e12)<br>g13 TRACK_APPEARED_LEFT(A,A:track_005) (A:e13)<br>g14 TRACK_APPEARED_LEFT(A,A:track_006) (A:e14)<br>g15 TRACK_APPEARED_LEFT(A,A:track_010) (A:e15)<br>g16 CLOSING_START(A,A:track_002) (A:e16)<br>g17 CLOSING_START(A,A:track_003) (A:e17)<br>g18 CLOSING_START(A,A:track_004) (A:e18)<br>g19 CLOSING_START(A,A:track_005) (A:e19)<br>g20 CLOSING_START(A,A:track_006) (A:e20)<br>g21 CLOSING_START(A,A:track_010) (A:e21) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g22 TRACK_APPEARED_LEFT(A,A:track_007) (A:e22)<br>g23 TRACK_APPEARED_LEFT(A,A:track_011) (A:e23)<br>g24 CLOSING_START(A,A:track_007) (A:e24)<br>g25 CLOSING_START(A,A:track_011) (A:e25) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g26 TRACK_APPEARED_LEFT(A,A:track_012) (A:e26)<br>g27 TRACK_APPEARED_LEFT(A,A:track_014) (A:e27)<br>g28 TRACK_APPEARED_LEFT(A,A:track_015) (A:e28)<br>g29 TRACK_APPEARED_RIGHT(A,A:track_008) (A:e29)<br>g30 TRACK_APPEARED_RIGHT(A,A:track_009) (A:e30)<br>g31 CLOSING_START(A,A:track_009) (A:e31)<br>g32 CLOSING_START(A,A:track_012) (A:e32)<br>g33 CLOSING_START(A,A:track_014) (A:e33)<br>g34 CLOSING_START(A,A:track_015) (A:e34) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g35 TRACK_APPEARED_RIGHT(A,A:track_013) (A:e35) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g36 TRACK_LOST(A,A:track_008) (A:e36) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | A | g37 CLOSING_END(A,A:track_009) (A:e37)<br>g38 TRACK_LOST(A,A:track_011) (A:e38)<br>g39 TRACK_LOST(A,A:track_012) (A:e39) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_008<br>sign-0: STOP sign known |
| - | A | g40 CRITICAL_TTC_START(A,A:track_006) (A:e40)<br>g41 TRACK_LOST(A,A:track_009) (A:e41) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_009: no active state<br>track_010: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track lost, states UNKNOWN: track_001, track_008, track_011, track_012<br>sign-0: STOP sign known |
| - | B | g42 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g43 TRACK_APPEARED_LEFT(B,B:track_001) (B:e02)<br>g44 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| - | B | g45 BRAKE_START(B) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g46 MOVING_END(B) (B:e05)<br>g47 STOP_START(B) (B:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| - | B | g48 EGO_PATH_ENTRY(B,B:track_001) (B:e07) | ego: STOP, BRAKE<br>track_001: CLOSING |
| - | B | g49 CLOSING_END(B,B:track_001) (B:e08) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| - | B | g50 EGO_PATH_EXIT(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| - | B | g51 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state |
| - | B | g52 STOP_END(B) (B:e11)<br>g53 MOVING_START(B) (B:e12) | ego: STOP<br>track_001: no active state |
| - | B | g54 TRACK_LOST(B,B:track_001) (B:e13) | ego: MOVING<br>track_001: no active state |
| - | B | g55 BRAKE_START(B) (B:e14) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| - | B | g56 BRAKE_END(B) (B:e15) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.00 s) A's radar started tracking unidentified object A:track_001, which appeared on its right.
- (unaligned, A local time 2.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.15 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 4.95 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 5.25 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.20 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 8.45 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 8.65 s) A started turning left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_003, which appeared on its left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_004, which appeared on its left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_010, which appeared on its left.
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 9.45 s) A's radar started tracking unidentified object A:track_007, which appeared on its left.
- (unaligned, A local time 9.45 s) A's radar started tracking unidentified object A:track_011, which appeared on its left.
- (unaligned, A local time 9.45 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 9.45 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_014, which appeared on its left.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_015, which appeared on its left.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_008, which appeared on its right.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_009, which appeared on its right.
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_014 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_015 start closing in (already the case when first observed).
- (unaligned, A local time 9.70 s) A's radar started tracking unidentified object A:track_013, which appeared on its right.
- (unaligned, A local time 9.75 s) A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.85 s) A observed unidentified object A:track_009 stop closing in.
- (unaligned, A local time 9.85 s) A's radar lost unidentified object A:track_011 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.85 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.90 s) A's time-to-contact with unidentified object A:track_006 became critical.
- (unaligned, A local time 9.90 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.95 s) B's radar started tracking unidentified object B:track_001, which appeared on its left.
- (unaligned, B local time 1.95 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.90 s) B stopped moving.
- (unaligned, B local time 3.90 s) B came to a stop.
- (unaligned, B local time 5.40 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 5.55 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.90 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 7.15 s) B released the brake.
- (unaligned, B local time 7.55 s) B left its stop.
- (unaligned, B local time 7.55 s) B started moving.
- (unaligned, B local time 8.30 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.75 s) B started braking.
- (unaligned, B local time 9.00 s) B released the brake.
