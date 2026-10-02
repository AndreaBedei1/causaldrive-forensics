# Global graph - S12/run_0_b_arrives_first

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
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.95 | relevant_to_ego_path=True |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 3.55 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 4.35 |  |
| g05 | - | MOVING_END | A | - | A:e05 @ 4.75 |  |
| g06 | - | STOP_START | A | - | A:e06 @ 4.75 |  |
| g07 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e07 @ 6.90 |  |
| g08 | - | CLOSING_START | A | A:track_001 | A:e08 @ 6.90 | active_at_first_observation=True |
| g09 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e09 @ 9.75 |  |
| g10 | - | CLOSING_END | A | A:track_001 | A:e10 @ 9.90 |  |
| g11 | - | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 10.20 |  |
| g12 | - | BRAKE_END | A | - | A:e12 @ 10.45 |  |
| g13 | - | STOP_END | A | - | A:e13 @ 10.80 |  |
| g14 | - | MOVING_START | A | - | A:e14 @ 10.80 |  |
| g15 | - | TURN_LEFT_START | A | - | A:e15 @ 12.10 |  |
| g16 | - | TURN_LEFT_END | A | - | A:e16 @ 15.30 |  |
| g17 | - | TRACK_LOST | A | A:track_001 | A:e17 @ 16.20 |  |
| g18 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g19 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.80 | relevant_to_ego_path=True |
| g20 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 2.60 |  |
| g21 | - | BRAKE_START | B | - | B:e04 @ 2.65 |  |
| g22 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e05 @ 3.35 |  |
| g23 | - | CLOSING_START | B | B:track_001 | B:e06 @ 3.35 | active_at_first_observation=True |
| g24 | - | MOVING_END | B | - | B:e07 @ 3.40 |  |
| g25 | - | STOP_START | B | - | B:e08 @ 3.40 |  |
| g26 | - | CLOSING_END | B | B:track_001 | B:e09 @ 4.70 |  |
| g27 | - | BRAKE_END | B | - | B:e10 @ 6.45 |  |
| g28 | - | STOP_END | B | - | B:e11 @ 6.85 |  |
| g29 | - | MOVING_START | B | - | B:e12 @ 6.85 |  |
| g30 | - | CLOSING_START | B | B:track_001 | B:e13 @ 6.90 |  |
| g31 | - | CLOSING_END | B | B:track_001 | B:e14 @ 9.85 |  |
| g32 | - | TRACK_LOST | B | B:track_001 | B:e15 @ 15.85 |  |

## Edges

```
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g09
    g07 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g17
    g22 --SAME_TRACK--> g23
    g22 --SAME_TRACK--> g26
    g22 --SAME_TRACK--> g30
    g22 --SAME_TRACK--> g31
    g22 --SAME_TRACK--> g32
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): EGO_PATH_ENTRY 9.75, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g04 BRAKE_START(A) (A:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g05 MOVING_END(A) (A:e05)<br>g06 STOP_START(A) (A:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| - | A | g07 TRACK_APPEARED_LEFT(A,A:track_001) (A:e07)<br>g08 CLOSING_START(A,A:track_001) (A:e08) | ego: STOP, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| - | A | g09 EGO_PATH_ENTRY(A,A:track_001) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | A | g10 CLOSING_END(A,A:track_001) (A:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g11 EGO_PATH_EXIT(A,A:track_001) (A:e11) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| - | A | g12 BRAKE_END(A) (A:e12) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g13 STOP_END(A) (A:e13)<br>g14 MOVING_START(A) (A:e14) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g15 TURN_LEFT_START(A) (A:e15) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g16 TURN_LEFT_END(A) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | A | g17 TRACK_LOST(A,A:track_001) (A:e17) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g18 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g19 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| - | B | g20 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g21 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g22 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e05)<br>g23 CLOSING_START(B,B:track_001) (B:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| - | B | g24 MOVING_END(B) (B:e07)<br>g25 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g26 CLOSING_END(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g27 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g28 STOP_END(B) (B:e11)<br>g29 MOVING_START(B) (B:e12) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g30 CLOSING_START(B,B:track_001) (B:e13) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| - | B | g31 CLOSING_END(B,B:track_001) (B:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| - | B | g32 TRACK_LOST(B,B:track_001) (B:e15) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.95 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 3.55 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 4.35 s) A started braking.
- (unaligned, A local time 4.75 s) A stopped moving.
- (unaligned, A local time 4.75 s) A came to a stop.
- (unaligned, A local time 6.90 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 6.90 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 9.75 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 9.90 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 10.20 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 10.45 s) A released the brake.
- (unaligned, A local time 10.80 s) A left its stop.
- (unaligned, A local time 10.80 s) A started moving.
- (unaligned, A local time 12.10 s) A started turning left.
- (unaligned, A local time 15.30 s) A stopped turning left.
- (unaligned, A local time 16.20 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.80 s) B's camera established a STOP sign detection (unidentified object B:sign-0).
- (unaligned, B local time 2.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.65 s) B started braking.
- (unaligned, B local time 3.35 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 3.35 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 4.70 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.45 s) B released the brake.
- (unaligned, B local time 6.85 s) B left its stop.
- (unaligned, B local time 6.85 s) B started moving.
- (unaligned, B local time 6.90 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 9.85 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 15.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
