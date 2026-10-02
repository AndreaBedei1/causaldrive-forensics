# Global graph - S10/run_0_stops_safely

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
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.85 | relevant_to_ego_path=False |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.15 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.55 |  |
| g05 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e05 @ 2.65 |  |
| g06 | - | CLOSING_START | A | A:track_001 | A:e06 @ 2.65 | active_at_first_observation=True |
| g07 | - | MOVING_END | A | - | A:e07 @ 3.35 |  |
| g08 | - | STOP_START | A | - | A:e08 @ 3.35 |  |
| g09 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e09 @ 5.80 |  |
| g10 | - | CLOSING_END | A | A:track_001 | A:e10 @ 6.15 |  |
| g11 | - | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 6.25 |  |
| g12 | - | TRACK_LOST | A | A:track_001 | A:e12 @ 9.45 |  |
| g13 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g14 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 2.60 |  |
| g15 | - | CLOSING_START | B | B:track_001 | B:e03 @ 2.60 | active_at_first_observation=True |
| g16 | - | CRITICAL_TTC_START | B | B:track_001 | B:e04 @ 4.25 |  |
| g17 | - | CRITICAL_TTC_END | B | B:track_001 | B:e05 @ 5.95 |  |
| g18 | - | CLOSING_END | B | B:track_001 | B:e06 @ 6.15 |  |
| g19 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e07 @ 7.60 | relevant_to_ego_path=False |
| g20 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e08 @ 7.80 |  |

## Edges

```
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g12
    g14 --SAME_TRACK--> g15
    g14 --SAME_TRACK--> g16
    g14 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g18
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): EGO_PATH_ENTRY 5.80, no critical TTC [local times]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 4.25 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| - | A | g02 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| - | A | g03 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known |
| - | A | g04 BRAKE_START(A) (A:e04) | ego: MOVING<br>sign-0: STOP sign known |
| - | A | g05 TRACK_APPEARED_LEFT(A,A:track_001) (A:e05)<br>g06 CLOSING_START(A,A:track_001) (A:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| - | A | g07 MOVING_END(A) (A:e07)<br>g08 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | A | g09 EGO_PATH_ENTRY(A,A:track_001) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | A | g10 CLOSING_END(A,A:track_001) (A:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known |
| - | A | g11 EGO_PATH_EXIT(A,A:track_001) (A:e11) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known |
| - | A | g12 TRACK_LOST(A,A:track_001) (A:e12) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known |
| - | B | g13 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g14 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g15 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| - | B | g16 CRITICAL_TTC_START(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g17 CRITICAL_TTC_END(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | B | g18 CLOSING_END(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING |
| - | B | g19 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e07) | ego: MOVING<br>track_001: no active state |
| - | B | g20 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e08) | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.85 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 2.15 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.55 s) A started braking.
- (unaligned, A local time 2.65 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 2.65 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.35 s) A stopped moving.
- (unaligned, A local time 3.35 s) A came to a stop.
- (unaligned, A local time 5.80 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 6.15 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.25 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 9.45 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 2.60 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 2.60 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.25 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.95 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 6.15 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 7.60 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 7.80 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
