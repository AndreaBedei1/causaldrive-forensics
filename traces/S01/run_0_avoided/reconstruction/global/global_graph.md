# Global graph - S01/run_0_avoided

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
| g02 | - | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.45 |  |
| g04 | - | CLOSING_END | A | A:track_001 | A:e04 @ 1.65 |  |
| g05 | - | CLOSING_START | A | A:track_001 | A:e05 @ 4.20 |  |
| g06 | - | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 5.00 |  |
| g07 | - | BRAKE_START | A | - | A:e07 @ 5.05 |  |
| g08 | - | CRITICAL_TTC_END | A | A:track_001 | A:e08 @ 6.25 |  |
| g09 | - | CLOSING_END | A | A:track_001 | A:e09 @ 6.35 |  |
| g10 | - | MOVING_END | A | - | A:e10 @ 6.35 |  |
| g11 | - | STOP_START | A | - | A:e11 @ 6.35 |  |
| g12 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g13 | - | TRACK_APPEARED_REAR | B | B:track_001 | B:e02 @ 0.00 |  |
| g14 | - | CLOSING_START | B | B:track_001 | B:e03 @ 0.50 |  |
| g15 | - | CLOSING_END | B | B:track_001 | B:e04 @ 1.65 |  |
| g16 | - | BRAKE_START | B | - | B:e05 @ 3.95 |  |
| g17 | - | CLOSING_START | B | B:track_001 | B:e06 @ 4.25 |  |
| g18 | - | MOVING_END | B | - | B:e07 @ 5.15 |  |
| g19 | - | STOP_START | B | - | B:e08 @ 5.15 |  |
| g20 | - | CLOSING_END | B | B:track_001 | B:e09 @ 6.40 |  |
| g21 | - | BRAKE_END | B | - | B:e10 @ 11.95 |  |
| g22 | - | STOP_END | B | - | B:e11 @ 12.35 |  |
| g23 | - | MOVING_START | B | - | B:e12 @ 12.35 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g08
    g02 --SAME_TRACK--> g09
    g13 --SAME_TRACK--> g14
    g13 --SAME_TRACK--> g15
    g13 --SAME_TRACK--> g17
    g13 --SAME_TRACK--> g20
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 5.00 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02) | ego: not yet observed |
| - | A | g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| - | A | g04 CLOSING_END(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| - | A | g05 CLOSING_START(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| - | A | g06 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| - | A | g07 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | A | g08 CRITICAL_TTC_END(A,A:track_001) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | A | g09 CLOSING_END(A,A:track_001) (A:e09)<br>g10 MOVING_END(A) (A:e10)<br>g11 STOP_START(A) (A:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| - | B | g12 MOVING_START(B) (B:e01)<br>g13 TRACK_APPEARED_REAR(B,B:track_001) (B:e02) | ego: not yet observed |
| - | B | g14 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING<br>track_001: no active state |
| - | B | g15 CLOSING_END(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| - | B | g16 BRAKE_START(B) (B:e05) | ego: MOVING<br>track_001: no active state |
| - | B | g17 CLOSING_START(B,B:track_001) (B:e06) | ego: MOVING, BRAKE<br>track_001: no active state |
| - | B | g18 MOVING_END(B) (B:e07)<br>g19 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| - | B | g20 CLOSING_END(B,B:track_001) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING |
| - | B | g21 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state |
| - | B | g22 STOP_END(B) (B:e11)<br>g23 MOVING_START(B) (B:e12) | ego: STOP<br>track_001: no active state |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- (unaligned, A local time 0.45 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 1.65 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.20 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 5.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.05 s) A started braking.
- (unaligned, A local time 6.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.35 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.35 s) A stopped moving.
- (unaligned, A local time 6.35 s) A came to a stop.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.00 s) B's radar started tracking unidentified object B:track_001, which appeared behind it.
- (unaligned, B local time 0.50 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 1.65 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 3.95 s) B started braking.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 5.15 s) B stopped moving.
- (unaligned, B local time 5.15 s) B came to a stop.
- (unaligned, B local time 6.40 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 11.95 s) B released the brake.
- (unaligned, B local time 12.35 s) B left its stop.
- (unaligned, B local time 12.35 s) B started moving.
