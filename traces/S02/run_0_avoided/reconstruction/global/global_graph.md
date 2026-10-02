# Global graph - S02/run_0_avoided

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
| g02 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | CUT_IN_FROM_LEFT_START | A | A:track_001 | A:e04 @ 2.40 |  |
| g05 | - | BRAKE_START | A | - | A:e05 @ 2.85 |  |
| g06 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e06 @ 3.30 |  |
| g07 | - | CLOSING_END | A | A:track_001 | A:e07 @ 4.05 |  |
| g08 | - | BRAKE_END | A | - | A:e08 @ 4.10 |  |
| g09 | - | CUT_IN_FROM_LEFT_END | A | A:track_001 | A:e09 @ 5.25 |  |
| g10 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g11 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 0.00 |  |
| g12 | - | CLOSING_START | B | B:track_001 | B:e03 @ 0.00 | active_at_first_observation=True |
| g13 | - | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g14 | - | BRAKE_END | B | - | B:e05 @ 3.60 |  |
| g15 | - | CLOSING_END | B | B:track_001 | B:e06 @ 4.05 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g02 --SAME_TRACK--> g09
    g11 --SAME_TRACK--> g12
    g11 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CUT_IN_FROM_LEFT_START 2.40, no critical TTC after it; EGO_PATH_ENTRY 3.30, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED_LEFT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| - | A | g04 CUT_IN_FROM_LEFT_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | A | g05 BRAKE_START(A) (A:e05) | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| - | A | g06 EGO_PATH_ENTRY(A,A:track_001) (A:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| - | A | g07 CLOSING_END(A,A:track_001) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g08 BRAKE_END(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g09 CUT_IN_FROM_LEFT_END(A,A:track_001) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | B | g10 MOVING_START(B) (B:e01)<br>g11 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g12 CLOSING_START(B,B:track_001) (B:e03) | ego: not yet observed |
| - | B | g13 BRAKE_START(B) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g14 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| - | B | g15 CLOSING_END(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.40 s) A observed unidentified object A:track_001 cutting in from the left.
- (unaligned, A local time 2.85 s) A started braking.
- (unaligned, A local time 3.30 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 4.05 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.10 s) A released the brake.
- (unaligned, A local time 5.25 s) A observed unidentified object A:track_001's cut-in from the left settle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.00 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 0.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.60 s) B released the brake.
- (unaligned, B local time 4.05 s) B observed unidentified object B:track_001 stop closing in.
