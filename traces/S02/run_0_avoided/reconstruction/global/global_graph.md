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
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g05 | - | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g06 | - | PREDICTED_PATH_CONFLICT_START | A | A:track_001 | A:e06 @ 1.90 |  |
| g07 | - | CUT_IN_FROM_LEFT_START | A | A:track_001 | A:e07 @ 2.35 |  |
| g08 | - | CRITICAL_TTC_START | A | A:track_001 | A:e08 @ 2.80 |  |
| g09 | - | BRAKE_START | A | - | A:e09 @ 2.85 |  |
| g10 | - | HARD_BRAKE_START | A | - | A:e10 @ 2.85 |  |
| g11 | - | CRITICAL_TTC_END | A | A:track_001 | A:e11 @ 3.10 |  |
| g12 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e12 @ 3.25 |  |
| g13 | - | PREDICTED_PATH_CONFLICT_END | A | A:track_001 | A:e13 @ 3.65 |  |
| g14 | - | HARD_BRAKE_END | A | - | A:e14 @ 3.70 |  |
| g15 | - | CLOSING_END | A | A:track_001 | A:e15 @ 4.05 |  |
| g16 | - | BRAKE_END | A | - | A:e16 @ 4.10 |  |
| g17 | - | CUT_IN_FROM_LEFT_END | A | A:track_001 | A:e17 @ 5.30 |  |
| g18 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g19 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 0.35 |  |
| g20 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.30 |  |
| g21 | - | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g22 | - | BRAKE_END | B | - | B:e05 @ 3.60 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g02 --SAME_TRACK--> g08
    g02 --SAME_TRACK--> g11
    g02 --SAME_TRACK--> g12
    g02 --SAME_TRACK--> g13
    g02 --SAME_TRACK--> g15
    g02 --SAME_TRACK--> g17
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| - | A | g04 STRONG_THROTTLE_START(A) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g05 STRONG_THROTTLE_END(A) (A:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING |
| - | A | g06 PREDICTED_PATH_CONFLICT_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g07 CUT_IN_FROM_LEFT_START(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT |
| - | A | g08 CRITICAL_TTC_START(A,A:track_001) (A:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| - | A | g09 BRAKE_START(A) (A:e09)<br>g10 HARD_BRAKE_START(A) (A:e10) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| - | A | g11 CRITICAL_TTC_END(A,A:track_001) (A:e11) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| - | A | g12 EGO_PATH_ENTRY(A,A:track_001) (A:e12) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| - | A | g13 PREDICTED_PATH_CONFLICT_END(A,A:track_001) (A:e13) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| - | A | g14 HARD_BRAKE_END(A) (A:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g15 CLOSING_END(A,A:track_001) (A:e15) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g16 BRAKE_END(A) (A:e16) | ego: MOVING, BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | A | g17 CUT_IN_FROM_LEFT_END(A,A:track_001) (A:e17) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| - | B | g18 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g19 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g20 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g21 BRAKE_START(B) (B:e04) | ego: MOVING |
| - | B | g22 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 1.15 s) A started applying strong throttle.
- (unaligned, A local time 1.35 s) A stopped applying strong throttle.
- (unaligned, A local time 1.90 s) A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- (unaligned, A local time 2.35 s) A observed unidentified object A:track_001 cutting in from the left.
- (unaligned, A local time 2.80 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 2.85 s) A started braking.
- (unaligned, A local time 2.85 s) A started braking hard.
- (unaligned, A local time 3.10 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 3.25 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 3.65 s) A stopped predicting a path conflict with unidentified object A:track_001.
- (unaligned, A local time 3.70 s) A stopped braking hard.
- (unaligned, A local time 4.05 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.10 s) A released the brake.
- (unaligned, A local time 5.30 s) A observed unidentified object A:track_001's cut-in from the left settle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.35 s) B started applying strong throttle.
- (unaligned, B local time 1.30 s) B stopped applying strong throttle.
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.60 s) B released the brake.
