# Global graph - S04/run_0_yield

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
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 2.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.00 | active_at_first_observation=True |
| g04 | - | PREDICTED_PATH_CONFLICT_START | A | A:track_001 | A:e04 @ 2.35 |  |
| g05 | - | PREDICTED_PATH_CONFLICT_END | A | A:track_001 | A:e05 @ 2.65 |  |
| g06 | - | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 3.00 |  |
| g07 | - | CRITICAL_TTC_END | A | A:track_001 | A:e07 @ 4.95 |  |
| g08 | - | TRACK_LOST | A | A:track_001 | A:e08 @ 5.25 |  |
| g09 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e09 @ 8.20 | relevant_to_ego_path=False |
| g10 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e10 @ 8.45 |  |
| g11 | - | TRACK_APPEARED | A | A:track_002 | A:e11 @ 9.35 |  |
| g12 | - | TRACK_APPEARED | A | A:track_003 | A:e12 @ 9.35 |  |
| g13 | - | TRACK_APPEARED | A | A:track_004 | A:e13 @ 9.35 |  |
| g14 | - | TRACK_APPEARED | A | A:track_005 | A:e14 @ 9.35 |  |
| g15 | - | TRACK_APPEARED | A | A:track_006 | A:e15 @ 9.35 |  |
| g16 | - | TRACK_APPEARED | A | A:track_010 | A:e16 @ 9.35 |  |
| g17 | - | CLOSING_START | A | A:track_002 | A:e17 @ 9.35 | active_at_first_observation=True |
| g18 | - | CLOSING_START | A | A:track_003 | A:e18 @ 9.35 | active_at_first_observation=True |
| g19 | - | CLOSING_START | A | A:track_004 | A:e19 @ 9.35 | active_at_first_observation=True |
| g20 | - | CLOSING_START | A | A:track_005 | A:e20 @ 9.35 | active_at_first_observation=True |
| g21 | - | CLOSING_START | A | A:track_006 | A:e21 @ 9.35 | active_at_first_observation=True |
| g22 | - | CLOSING_START | A | A:track_010 | A:e22 @ 9.35 | active_at_first_observation=True |
| g23 | - | TRACK_APPEARED | A | A:track_007 | A:e23 @ 9.45 |  |
| g24 | - | TRACK_APPEARED | A | A:track_011 | A:e24 @ 9.45 |  |
| g25 | - | CLOSING_START | A | A:track_007 | A:e25 @ 9.45 | active_at_first_observation=True |
| g26 | - | CLOSING_START | A | A:track_011 | A:e26 @ 9.45 | active_at_first_observation=True |
| g27 | - | TRACK_APPEARED | A | A:track_008 | A:e27 @ 9.50 |  |
| g28 | - | TRACK_APPEARED | A | A:track_009 | A:e28 @ 9.50 |  |
| g29 | - | TRACK_APPEARED | A | A:track_012 | A:e29 @ 9.50 |  |
| g30 | - | TRACK_APPEARED | A | A:track_014 | A:e30 @ 9.50 |  |
| g31 | - | TRACK_APPEARED | A | A:track_015 | A:e31 @ 9.50 |  |
| g32 | - | CLOSING_START | A | A:track_009 | A:e32 @ 9.50 | active_at_first_observation=True |
| g33 | - | CLOSING_START | A | A:track_012 | A:e33 @ 9.50 | active_at_first_observation=True |
| g34 | - | CLOSING_START | A | A:track_014 | A:e34 @ 9.50 | active_at_first_observation=True |
| g35 | - | CLOSING_START | A | A:track_015 | A:e35 @ 9.50 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED | A | A:track_013 | A:e36 @ 9.70 |  |
| g37 | - | TRACK_LOST | A | A:track_008 | A:e37 @ 9.75 |  |
| g38 | - | CLOSING_END | A | A:track_009 | A:e38 @ 9.85 |  |
| g39 | - | TRACK_LOST | A | A:track_011 | A:e39 @ 9.85 |  |
| g40 | - | TRACK_LOST | A | A:track_012 | A:e40 @ 9.85 |  |
| g41 | - | CRITICAL_TTC_START | A | A:track_006 | A:e41 @ 9.90 |  |
| g42 | - | TRACK_LOST | A | A:track_009 | A:e42 @ 9.90 |  |
| g43 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g44 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g45 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g46 | - | TRACK_APPEARED | B | B:track_001 | B:e04 @ 1.95 |  |
| g47 | - | CLOSING_START | B | B:track_001 | B:e05 @ 1.95 | active_at_first_observation=True |
| g48 | - | BRAKE_START | B | - | B:e06 @ 3.15 |  |
| g49 | - | HARD_BRAKE_START | B | - | B:e07 @ 3.15 |  |
| g50 | - | CRITICAL_TTC_START | B | B:track_001 | B:e08 @ 3.15 |  |
| g51 | - | MOVING_END | B | - | B:e09 @ 3.90 |  |
| g52 | - | STOP_START | B | - | B:e10 @ 3.90 |  |
| g53 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e11 @ 5.40 |  |
| g54 | - | CRITICAL_TTC_END | B | B:track_001 | B:e12 @ 5.45 |  |
| g55 | - | CLOSING_END | B | B:track_001 | B:e13 @ 5.55 |  |
| g56 | - | EGO_PATH_EXIT | B | B:track_001 | B:e14 @ 5.90 |  |
| g57 | - | HARD_BRAKE_END | B | - | B:e15 @ 7.15 |  |
| g58 | - | BRAKE_END | B | - | B:e16 @ 7.15 |  |
| g59 | - | STRONG_THROTTLE_START | B | - | B:e17 @ 7.15 |  |
| g60 | - | STOP_END | B | - | B:e18 @ 7.55 |  |
| g61 | - | MOVING_START | B | - | B:e19 @ 7.55 |  |
| g62 | - | TRACK_LOST | B | B:track_001 | B:e20 @ 8.30 |  |
| g63 | - | STRONG_THROTTLE_END | B | - | B:e21 @ 8.55 |  |
| g64 | - | BRAKE_START | B | - | B:e22 @ 8.75 |  |
| g65 | - | BRAKE_END | B | - | B:e23 @ 9.00 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g02 --SAME_TRACK--> g08
    g11 --SAME_TRACK--> g17
    g12 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g19
    g14 --SAME_TRACK--> g20
    g15 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g25
    g24 --SAME_TRACK--> g26
    g28 --SAME_TRACK--> g32
    g29 --SAME_TRACK--> g33
    g30 --SAME_TRACK--> g34
    g31 --SAME_TRACK--> g35
    g27 --SAME_TRACK--> g37
    g28 --SAME_TRACK--> g38
    g24 --SAME_TRACK--> g39
    g29 --SAME_TRACK--> g40
    g15 --SAME_TRACK--> g41
    g28 --SAME_TRACK--> g42
    g46 --SAME_TRACK--> g47
    g46 --SAME_TRACK--> g50
    g46 --SAME_TRACK--> g53
    g46 --SAME_TRACK--> g54
    g46 --SAME_TRACK--> g55
    g46 --SAME_TRACK--> g56
    g46 --SAME_TRACK--> g62
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
| - | A | g02 TRACK_APPEARED(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 PREDICTED_PATH_CONFLICT_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g05 PREDICTED_PATH_CONFLICT_END(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT |
| - | A | g06 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g07 CRITICAL_TTC_END(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g08 TRACK_LOST(A,A:track_001) (A:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g09 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e09) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| - | A | g10 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e10) | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign VISIBLE, known |
| - | A | g11 TRACK_APPEARED(A,A:track_002) (A:e11)<br>g12 TRACK_APPEARED(A,A:track_003) (A:e12)<br>g13 TRACK_APPEARED(A,A:track_004) (A:e13)<br>g14 TRACK_APPEARED(A,A:track_005) (A:e14)<br>g15 TRACK_APPEARED(A,A:track_006) (A:e15)<br>g16 TRACK_APPEARED(A,A:track_010) (A:e16)<br>g17 CLOSING_START(A,A:track_002) (A:e17)<br>g18 CLOSING_START(A,A:track_003) (A:e18)<br>g19 CLOSING_START(A,A:track_004) (A:e19)<br>g20 CLOSING_START(A,A:track_005) (A:e20)<br>g21 CLOSING_START(A,A:track_006) (A:e21)<br>g22 CLOSING_START(A,A:track_010) (A:e22) | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | A | g23 TRACK_APPEARED(A,A:track_007) (A:e23)<br>g24 TRACK_APPEARED(A,A:track_011) (A:e24)<br>g25 CLOSING_START(A,A:track_007) (A:e25)<br>g26 CLOSING_START(A,A:track_011) (A:e26) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | A | g27 TRACK_APPEARED(A,A:track_008) (A:e27)<br>g28 TRACK_APPEARED(A,A:track_009) (A:e28)<br>g29 TRACK_APPEARED(A,A:track_012) (A:e29)<br>g30 TRACK_APPEARED(A,A:track_014) (A:e30)<br>g31 TRACK_APPEARED(A,A:track_015) (A:e31)<br>g32 CLOSING_START(A,A:track_009) (A:e32)<br>g33 CLOSING_START(A,A:track_012) (A:e33)<br>g34 CLOSING_START(A,A:track_014) (A:e34)<br>g35 CLOSING_START(A,A:track_015) (A:e35) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | A | g36 TRACK_APPEARED(A,A:track_013) (A:e36) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | A | g37 TRACK_LOST(A,A:track_008) (A:e37) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | A | g38 CLOSING_END(A,A:track_009) (A:e38)<br>g39 TRACK_LOST(A,A:track_011) (A:e39)<br>g40 TRACK_LOST(A,A:track_012) (A:e40) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_008<br>sign-0: STOP sign not visible, known |
| - | A | g41 CRITICAL_TTC_START(A,A:track_006) (A:e41)<br>g42 TRACK_LOST(A,A:track_009) (A:e42) | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE, CLOSING<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_008, track_011, track_012<br>sign-0: STOP sign not visible, known |
| - | B | g43 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g44 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g45 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g46 TRACK_APPEARED(B,B:track_001) (B:e04)<br>g47 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING |
| - | B | g48 BRAKE_START(B) (B:e06)<br>g49 HARD_BRAKE_START(B) (B:e07)<br>g50 CRITICAL_TTC_START(B,B:track_001) (B:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | B | g51 MOVING_END(B) (B:e09)<br>g52 STOP_START(B) (B:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | B | g53 EGO_PATH_ENTRY(B,B:track_001) (B:e11) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | B | g54 CRITICAL_TTC_END(B,B:track_001) (B:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | B | g55 CLOSING_END(B,B:track_001) (B:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| - | B | g56 EGO_PATH_EXIT(B,B:track_001) (B:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| - | B | g57 HARD_BRAKE_END(B) (B:e15)<br>g58 BRAKE_END(B) (B:e16)<br>g59 STRONG_THROTTLE_START(B) (B:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE |
| - | B | g60 STOP_END(B) (B:e18)<br>g61 MOVING_START(B) (B:e19) | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE |
| - | B | g62 TRACK_LOST(B,B:track_001) (B:e20) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE |
| - | B | g63 STRONG_THROTTLE_END(B) (B:e21) | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001 |
| - | B | g64 BRAKE_START(B) (B:e22) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| - | B | g65 BRAKE_END(B) (B:e23) | ego: MOVING, BRAKE<br>lost (states UNKNOWN): track_001 |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 2.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.35 s) A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- (unaligned, A local time 2.65 s) A stopped predicting a path conflict with unidentified object A:track_001.
- (unaligned, A local time 3.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 4.95 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 5.25 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.20 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 8.45 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_003.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_004.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_005.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_006.
- (unaligned, A local time 9.35 s) A's radar started tracking unidentified object A:track_010.
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 9.35 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 9.45 s) A's radar started tracking unidentified object A:track_007.
- (unaligned, A local time 9.45 s) A's radar started tracking unidentified object A:track_011.
- (unaligned, A local time 9.45 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 9.45 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_008.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_009.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_012.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_014.
- (unaligned, A local time 9.50 s) A's radar started tracking unidentified object A:track_015.
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_014 start closing in (already the case when first observed).
- (unaligned, A local time 9.50 s) A observed unidentified object A:track_015 start closing in (already the case when first observed).
- (unaligned, A local time 9.70 s) A's radar started tracking unidentified object A:track_013.
- (unaligned, A local time 9.75 s) A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.85 s) A observed unidentified object A:track_009 stop closing in.
- (unaligned, A local time 9.85 s) A's radar lost unidentified object A:track_011 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.85 s) A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 9.90 s) A's time-to-contact with unidentified object A:track_006 became critical.
- (unaligned, A local time 9.90 s) A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 1.95 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 1.95 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.15 s) B started braking hard.
- (unaligned, B local time 3.15 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 3.90 s) B stopped moving.
- (unaligned, B local time 3.90 s) B came to a stop.
- (unaligned, B local time 5.40 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 5.45 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.55 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.90 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 7.15 s) B stopped braking hard.
- (unaligned, B local time 7.15 s) B released the brake.
- (unaligned, B local time 7.15 s) B started applying strong throttle.
- (unaligned, B local time 7.55 s) B left its stop.
- (unaligned, B local time 7.55 s) B started moving.
- (unaligned, B local time 8.30 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.55 s) B stopped applying strong throttle.
- (unaligned, B local time 8.75 s) B started braking.
- (unaligned, B local time 9.00 s) B released the brake.
