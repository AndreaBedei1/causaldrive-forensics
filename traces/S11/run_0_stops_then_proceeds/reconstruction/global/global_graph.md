# Global graph - S11/run_0_stops_then_proceeds

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
| g02 | - | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e02 @ 2.65 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.65 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 4.40 |  |
| g05 | - | CRITICAL_TTC_END | A | A:track_001 | A:e05 @ 5.65 |  |
| g06 | - | CLOSING_END | A | A:track_001 | A:e06 @ 6.10 |  |
| g07 | - | TRACK_LOST | A | A:track_001 | A:e07 @ 12.10 |  |
| g08 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g09 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e02 @ 2.00 | relevant_to_ego_path=False |
| g10 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e03 @ 2.35 |  |
| g11 | - | BRAKE_START | B | - | B:e04 @ 2.55 |  |
| g12 | - | TRACK_APPEARED_LEFT | B | B:track_001 | B:e05 @ 2.75 |  |
| g13 | - | CLOSING_START | B | B:track_001 | B:e06 @ 2.75 | active_at_first_observation=True |
| g14 | - | MOVING_END | B | - | B:e07 @ 3.25 |  |
| g15 | - | STOP_START | B | - | B:e08 @ 3.25 |  |
| g16 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e09 @ 5.80 |  |
| g17 | - | CLOSING_END | B | B:track_001 | B:e10 @ 6.10 |  |
| g18 | - | EGO_PATH_EXIT | B | B:track_001 | B:e11 @ 6.20 |  |
| g19 | - | BRAKE_END | B | - | B:e12 @ 6.75 |  |
| g20 | - | STOP_END | B | - | B:e13 @ 7.20 |  |
| g21 | - | MOVING_START | B | - | B:e14 @ 7.20 |  |
| g22 | - | TURN_LEFT_START | B | - | B:e15 @ 7.95 |  |
| g23 | - | TURN_LEFT_END | B | - | B:e16 @ 10.70 |  |
| g24 | - | TRACK_LOST | B | B:track_001 | B:e17 @ 12.05 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g12 --SAME_TRACK--> g13
    g12 --SAME_TRACK--> g16
    g12 --SAME_TRACK--> g17
    g12 --SAME_TRACK--> g18
    g12 --SAME_TRACK--> g24
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 4.40 [local times]
- B's track_001 (unidentified B:track_001): EGO_PATH_ENTRY 5.80, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | A | g05 CRITICAL_TTC_END(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | A | g06 CLOSING_END(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | A | g07 TRACK_LOST(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: no active state |
| - | B | g08 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g09 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e02) | ego: MOVING |
| - | B | g10 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e03) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g11 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g12 TRACK_APPEARED_LEFT(B,B:track_001) (B:e05)<br>g13 CLOSING_START(B,B:track_001) (B:e06) | ego: MOVING, BRAKE<br>sign-1: STOP sign known |
| - | B | g14 MOVING_END(B) (B:e07)<br>g15 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g16 EGO_PATH_ENTRY(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g17 CLOSING_END(B,B:track_001) (B:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g18 EGO_PATH_EXIT(B,B:track_001) (B:e11) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g19 BRAKE_END(B) (B:e12) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g20 STOP_END(B) (B:e13)<br>g21 MOVING_START(B) (B:e14) | ego: STOP<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g22 TURN_LEFT_START(B) (B:e15) | ego: MOVING<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g23 TURN_LEFT_END(B) (B:e16) | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g24 TRACK_LOST(B,B:track_001) (B:e17) | ego: MOVING<br>track_001: no active state<br>sign-1: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.65 s) A's radar started tracking unidentified object A:track_001, which appeared on its right.
- (unaligned, A local time 2.65 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.40 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.65 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.10 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 12.10 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.00 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.35 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.75 s) B's radar started tracking unidentified object B:track_001, which appeared on its left.
- (unaligned, B local time 2.75 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 6.75 s) B released the brake.
- (unaligned, B local time 7.20 s) B left its stop.
- (unaligned, B local time 7.20 s) B started moving.
- (unaligned, B local time 7.95 s) B started turning left.
- (unaligned, B local time 10.70 s) B stopped turning left.
- (unaligned, B local time 12.05 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
