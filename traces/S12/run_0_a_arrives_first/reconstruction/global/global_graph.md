# Global graph - S12/run_0_a_arrives_first

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.65 |  |
| g05 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e05 @ 3.20 |  |
| g06 | - | CLOSING_START | A | A:track_001 | A:e06 @ 3.20 | active_at_first_observation=True |
| g07 | - | MOVING_END | A | - | A:e07 @ 3.40 |  |
| g08 | - | STOP_START | A | - | A:e08 @ 3.40 |  |
| g09 | - | CLOSING_END | A | A:track_001 | A:e09 @ 4.70 |  |
| g10 | - | BRAKE_END | A | - | A:e10 @ 6.45 |  |
| g11 | - | STOP_END | A | - | A:e11 @ 6.80 |  |
| g12 | - | MOVING_START | A | - | A:e12 @ 6.80 |  |
| g13 | - | CLOSING_START | A | A:track_001 | A:e13 @ 6.95 |  |
| g14 | - | TURN_LEFT_START | A | - | A:e14 @ 7.80 |  |
| g15 | - | CRITICAL_TTC_START | A | A:track_001 | A:e15 @ 9.60 |  |
| g16 | - | TURN_LEFT_END | A | - | A:e16 @ 11.05 |  |
| g17 | - | CRITICAL_TTC_END | A | A:track_001 | A:e17 @ 11.10 |  |
| g18 | - | CLOSING_END | A | A:track_001 | A:e18 @ 11.25 |  |
| g19 | - | TRACK_LOST | A | A:track_001 | A:e19 @ 15.55 |  |
| g20 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g21 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 2.10 | relevant_to_ego_path=False |
| g22 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 4.00 |  |
| g23 | - | BRAKE_START | B | - | B:e04 @ 4.35 |  |
| g24 | - | MOVING_END | B | - | B:e05 @ 4.70 |  |
| g25 | - | STOP_START | B | - | B:e06 @ 4.70 |  |
| g26 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e07 @ 6.95 |  |
| g27 | - | CLOSING_START | B | B:track_001 | B:e08 @ 6.95 | active_at_first_observation=True |
| g28 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e09 @ 8.50 |  |
| g29 | - | EGO_PATH_EXIT | B | B:track_001 | B:e10 @ 9.05 |  |
| g30 | - | BRAKE_END | B | - | B:e11 @ 10.45 |  |
| g31 | - | CRITICAL_TTC_START | B | B:track_001 | B:e12 @ 10.55 |  |
| g32 | - | STOP_END | B | - | B:e13 @ 10.85 |  |
| g33 | - | MOVING_START | B | - | B:e14 @ 10.85 |  |
| g34 | - | CRITICAL_TTC_END | B | B:track_001 | B:e15 @ 11.10 |  |
| g35 | - | CLOSING_END | B | B:track_001 | B:e16 @ 11.30 |  |
| g36 | - | TRACK_LOST | B | B:track_001 | B:e17 @ 16.20 |  |

## Edges

```
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g17
    g05 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g19
    g26 --SAME_TRACK--> g27
    g26 --SAME_TRACK--> g28
    g26 --SAME_TRACK--> g29
    g26 --SAME_TRACK--> g31
    g26 --SAME_TRACK--> g34
    g26 --SAME_TRACK--> g35
    g26 --SAME_TRACK--> g36
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 9.60 [local times]
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
| - | A | g15 CRITICAL_TTC_START(A,A:track_001) (A:e15) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g16 TURN_LEFT_END(A) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| - | A | g17 CRITICAL_TTC_END(A,A:track_001) (A:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| - | A | g18 CLOSING_END(A,A:track_001) (A:e18) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g19 TRACK_LOST(A,A:track_001) (A:e19) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g20 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g21 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| - | B | g22 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known |
| - | B | g23 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-0: STOP sign known |
| - | B | g24 MOVING_END(B) (B:e05)<br>g25 STOP_START(B) (B:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| - | B | g26 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e07)<br>g27 CLOSING_START(B,B:track_001) (B:e08) | ego: STOP, BRAKE<br>sign-0: STOP sign known |
| - | B | g28 EGO_PATH_ENTRY(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g29 EGO_PATH_EXIT(B,B:track_001) (B:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known |
| - | B | g30 BRAKE_END(B) (B:e11) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g31 CRITICAL_TTC_START(B,B:track_001) (B:e12) | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g32 STOP_END(B) (B:e13)<br>g33 MOVING_START(B) (B:e14) | ego: STOP<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g34 CRITICAL_TTC_END(B,B:track_001) (B:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g35 CLOSING_END(B,B:track_001) (B:e16) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g36 TRACK_LOST(B,B:track_001) (B:e17) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.65 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 2.25 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.65 s) A started braking.
- (unaligned, A local time 3.20 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 3.20 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.40 s) A stopped moving.
- (unaligned, A local time 3.40 s) A came to a stop.
- (unaligned, A local time 4.70 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.45 s) A released the brake.
- (unaligned, A local time 6.80 s) A left its stop.
- (unaligned, A local time 6.80 s) A started moving.
- (unaligned, A local time 6.95 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 7.80 s) A started turning left.
- (unaligned, A local time 9.60 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 11.05 s) A stopped turning left.
- (unaligned, A local time 11.10 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 11.25 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 15.55 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 4.00 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 4.35 s) B started braking.
- (unaligned, B local time 4.70 s) B stopped moving.
- (unaligned, B local time 4.70 s) B came to a stop.
- (unaligned, B local time 6.95 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 6.95 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 8.50 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 9.05 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 10.45 s) B released the brake.
- (unaligned, B local time 10.55 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 10.85 s) B left its stop.
- (unaligned, B local time 10.85 s) B started moving.
- (unaligned, B local time 11.10 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 11.30 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 16.20 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
