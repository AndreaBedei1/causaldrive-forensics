# Global graph - S02/run_0_avoided

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |

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

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED_LEFT | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g05 | - | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g06 | - | CUT_IN_FROM_LEFT_START | A | A:track_001 | A:e06 @ 2.35 |  |
| g07 | - | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 2.80 |  |
| g08 | - | BRAKE_START | A | - | A:e08 @ 2.85 |  |
| g09 | - | HARD_BRAKE_START | A | - | A:e09 @ 2.85 |  |
| g10 | - | CRITICAL_TTC_END | A | A:track_001 | A:e10 @ 3.10 |  |
| g11 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e11 @ 3.25 |  |
| g12 | - | HARD_BRAKE_END | A | - | A:e12 @ 3.70 |  |
| g13 | - | CLOSING_END | A | A:track_001 | A:e13 @ 4.05 |  |
| g14 | - | BRAKE_END | A | - | A:e14 @ 4.10 |  |
| g15 | - | CUT_IN_FROM_LEFT_END | A | A:track_001 | A:e15 @ 5.30 |  |
| g16 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g17 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 0.35 |  |
| g18 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.30 |  |
| g19 | - | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g20 | - | BRAKE_END | B | - | B:e05 @ 3.60 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g02 --SAME_TRACK--> g10
    g02 --SAME_TRACK--> g11
    g02 --SAME_TRACK--> g13
    g02 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED_LEFT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| - | A | g04 STRONG_THROTTLE_START(A) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | A | g05 STRONG_THROTTLE_END(A) (A:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| - | A | g06 CUT_IN_FROM_LEFT_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | A | g07 CRITICAL_TTC_START(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| - | A | g08 BRAKE_START(A) (A:e08)<br>g09 HARD_BRAKE_START(A) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| - | A | g10 CRITICAL_TTC_END(A,A:track_001) (A:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| - | A | g11 EGO_PATH_ENTRY(A,A:track_001) (A:e11) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| - | A | g12 HARD_BRAKE_END(A) (A:e12) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g13 CLOSING_END(A,A:track_001) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g14 BRAKE_END(A) (A:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g15 CUT_IN_FROM_LEFT_END(A,A:track_001) (A:e15) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | B | g16 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g17 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g18 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g19 BRAKE_START(B) (B:e04) | ego: MOVING |
| - | B | g20 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 1.15 s) A started applying strong throttle.
- (unaligned, A local time 1.35 s) A stopped applying strong throttle.
- (unaligned, A local time 2.35 s) A observed unidentified object A:track_001 cutting in from the left.
- (unaligned, A local time 2.80 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 2.85 s) A started braking.
- (unaligned, A local time 2.85 s) A started braking hard.
- (unaligned, A local time 3.10 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 3.25 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 3.70 s) A stopped braking hard.
- (unaligned, A local time 4.05 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.10 s) A released the brake.
- (unaligned, A local time 5.30 s) A observed unidentified object A:track_001's cut-in from the left settle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.35 s) B started applying strong throttle.
- (unaligned, B local time 1.30 s) B stopped applying strong throttle.
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.60 s) B released the brake.
