# Global graph - S15/run_0_b_stops

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.20 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.20 | active_at_first_observation=True |
| g04 | - | TRACK_APPEARED_RIGHT | A | A:track_002 | A:e04 @ 2.10 |  |
| g05 | - | CLOSING_START | A | A:track_002 | A:e05 @ 2.10 | active_at_first_observation=True |
| g06 | - | CRITICAL_TTC_START | A | A:track_002 | A:e06 @ 2.10 | active_at_first_observation=True |
| g07 | - | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 2.50 |  |
| g08 | - | CRITICAL_TTC_END | A | A:track_002 | A:e08 @ 4.20 |  |
| g09 | - | CLOSING_END | A | A:track_002 | A:e09 @ 4.25 |  |
| g10 | - | CRITICAL_TTC_END | A | A:track_001 | A:e10 @ 4.65 |  |
| g11 | - | CLOSING_END | A | A:track_001 | A:e11 @ 4.65 |  |
| g12 | - | TRACK_LOST | A | A:track_001 | A:e12 @ 9.55 |  |
| g13 | - | TRACK_LOST | A | A:track_002 | A:e13 @ 10.40 |  |
| g14 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g15 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.45 | relevant_to_ego_path=False |
| g16 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e03 @ 1.75 |  |
| g17 | - | CLOSING_START | B | B:track_001 | B:e04 @ 1.75 | active_at_first_observation=True |
| g18 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e05 @ 2.05 |  |
| g19 | - | TRACK_APPEARED_LEFT | B | B:track_002 | B:e06 @ 2.10 |  |
| g20 | - | CLOSING_START | B | B:track_002 | B:e07 @ 2.10 | active_at_first_observation=True |
| g21 | - | CRITICAL_TTC_START | B | B:track_002 | B:e08 @ 2.10 | active_at_first_observation=True |
| g22 | - | TURN_LEFT_START | B | - | B:e09 @ 2.25 |  |
| g23 | - | CRITICAL_TTC_START | B | B:track_001 | B:e10 @ 2.40 |  |
| g24 | - | BRAKE_START | B | - | B:e11 @ 2.55 |  |
| g25 | - | CRITICAL_TTC_END | B | B:track_001 | B:e12 @ 2.80 |  |
| g26 | - | TURN_LEFT_END | B | - | B:e13 @ 3.35 |  |
| g27 | - | MOVING_END | B | - | B:e14 @ 3.40 |  |
| g28 | - | STOP_START | B | - | B:e15 @ 3.40 |  |
| g29 | - | CRITICAL_TTC_END | B | B:track_002 | B:e16 @ 3.55 |  |
| g30 | - | EGO_PATH_ENTRY | B | B:track_002 | B:e17 @ 3.90 |  |
| g31 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e18 @ 4.00 | relevant_to_ego_path=False |
| g32 | - | CLOSING_END | B | B:track_002 | B:e19 @ 4.30 |  |
| g33 | - | EGO_PATH_EXIT | B | B:track_002 | B:e20 @ 4.35 |  |
| g34 | - | CLOSING_END | B | B:track_001 | B:e21 @ 5.25 |  |
| g35 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e22 @ 5.75 |  |
| g36 | - | EGO_PATH_EXIT | B | B:track_001 | B:e23 @ 6.40 |  |
| g37 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e24 @ 7.90 |  |
| g38 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e25 @ 9.25 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-2 |
| g39 | - | TRACK_LOST | B | B:track_002 | B:e26 @ 9.85 |  |
| g40 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g41 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e02 @ 0.05 |  |
| g42 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.05 | active_at_first_observation=True |
| g43 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e04 @ 0.35 |  |
| g44 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.35 | active_at_first_observation=True |
| g45 | - | CRITICAL_TTC_START | C | C:track_001 | C:e06 @ 2.85 |  |
| g46 | - | CRITICAL_TTC_END | C | C:track_001 | C:e07 @ 4.70 |  |
| g47 | - | CLOSING_END | C | C:track_001 | C:e08 @ 4.70 |  |
| g48 | - | CLOSING_END | C | C:track_002 | C:e09 @ 5.20 |  |
| g49 | - | TRACK_LOST | C | C:track_001 | C:e10 @ 10.20 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g09
    g02 --SAME_TRACK--> g10
    g02 --SAME_TRACK--> g11
    g02 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g16 --SAME_TRACK--> g17
    g19 --SAME_TRACK--> g20
    g19 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g23
    g16 --SAME_TRACK--> g25
    g19 --SAME_TRACK--> g29
    g19 --SAME_TRACK--> g30
    g19 --SAME_TRACK--> g32
    g19 --SAME_TRACK--> g33
    g16 --SAME_TRACK--> g34
    g16 --SAME_TRACK--> g35
    g16 --SAME_TRACK--> g36
    g19 --SAME_TRACK--> g39
    g41 --SAME_TRACK--> g42
    g43 --SAME_TRACK--> g44
    g41 --SAME_TRACK--> g45
    g41 --SAME_TRACK--> g46
    g41 --SAME_TRACK--> g47
    g43 --SAME_TRACK--> g48
    g41 --SAME_TRACK--> g49
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 2.50 [local times]
- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 2.10 [local times]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 2.40; EGO_PATH_ENTRY 5.75 after critical TTC (+3.35 s) [local times]
- B's track_002 (unidentified B:track_002): CRITICAL_TTC_START 2.10; EGO_PATH_ENTRY 3.90 after critical TTC (+1.80 s) [local times]
- C's track_001 (unidentified C:track_001): CRITICAL_TTC_START 2.85 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 TRACK_APPEARED_RIGHT(A,A:track_002) (A:e04)<br>g05 CLOSING_START(A,A:track_002) (A:e05)<br>g06 CRITICAL_TTC_START(A,A:track_002) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | A | g07 CRITICAL_TTC_START(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| - | A | g08 CRITICAL_TTC_END(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | A | g09 CLOSING_END(A,A:track_002) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | A | g10 CRITICAL_TTC_END(A,A:track_001) (A:e10)<br>g11 CLOSING_END(A,A:track_001) (A:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| - | A | g12 TRACK_LOST(A,A:track_001) (A:e12) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| - | A | g13 TRACK_LOST(A,A:track_002) (A:e13) | ego: MOVING<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| - | B | g14 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g15 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| - | B | g16 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e03)<br>g17 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING<br>sign-0: STOP sign known |
| - | B | g18 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g19 TRACK_APPEARED_LEFT(B,B:track_002) (B:e06)<br>g20 CLOSING_START(B,B:track_002) (B:e07)<br>g21 CRITICAL_TTC_START(B,B:track_002) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g22 TURN_LEFT_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g23 CRITICAL_TTC_START(B,B:track_001) (B:e10) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g24 BRAKE_START(B) (B:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g25 CRITICAL_TTC_END(B,B:track_001) (B:e12) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g26 TURN_LEFT_END(B) (B:e13) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g27 MOVING_END(B) (B:e14)<br>g28 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g29 CRITICAL_TTC_END(B,B:track_002) (B:e16) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g30 EGO_PATH_ENTRY(B,B:track_002) (B:e17) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |
| - | B | g31 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e18) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known |
| - | B | g32 CLOSING_END(B,B:track_002) (B:e19) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g33 EGO_PATH_EXIT(B,B:track_002) (B:e20) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g34 CLOSING_END(B,B:track_001) (B:e21) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g35 EGO_PATH_ENTRY(B,B:track_001) (B:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g36 EGO_PATH_EXIT(B,B:track_001) (B:e23) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g37 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e24) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g38 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e25) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g39 TRACK_LOST(B,B:track_002) (B:e26) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | C | g40 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g41 TRACK_APPEARED_FRONT(C,C:track_001) (C:e02)<br>g42 CLOSING_START(C,C:track_001) (C:e03) | ego: MOVING |
| - | C | g43 TRACK_APPEARED_LEFT(C,C:track_002) (C:e04)<br>g44 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| - | C | g45 CRITICAL_TTC_START(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g46 CRITICAL_TTC_END(C,C:track_001) (C:e07)<br>g47 CLOSING_END(C,C:track_001) (C:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g48 CLOSING_END(C,C:track_002) (C:e09) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| - | C | g49 TRACK_LOST(C,C:track_001) (C:e10) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.20 s) A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- (unaligned, A local time 0.20 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.10 s) A's radar started tracking unidentified object A:track_002, which appeared on its right.
- (unaligned, A local time 2.10 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 2.10 s) A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- (unaligned, A local time 2.50 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 4.20 s) A's time-to-contact with unidentified object A:track_002 stopped being critical.
- (unaligned, A local time 4.25 s) A observed unidentified object A:track_002 stop closing in.
- (unaligned, A local time 4.65 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 4.65 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 9.55 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 10.40 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.45 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 1.75 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 1.75 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.05 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.10 s) B's radar started tracking unidentified object B:track_002, which appeared on its left.
- (unaligned, B local time 2.10 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 2.10 s) B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- (unaligned, B local time 2.25 s) B started turning left.
- (unaligned, B local time 2.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.80 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 3.35 s) B stopped turning left.
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 3.55 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 3.90 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 4.00 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 4.30 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 4.35 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 5.25 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.75 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.40 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 7.90 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 9.25 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- (unaligned, B local time 9.85 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.05 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.05 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.35 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.35 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.85 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 4.70 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.70 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 5.20 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 10.20 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
