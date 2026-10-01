# Global graph - S11/run_0_stops_safely

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

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
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 2.60 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.60 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 4.65 |  |
| g05 | - | CRITICAL_TTC_END | A | A:track_001 | A:e05 @ 5.25 |  |
| g06 | - | TRACK_LOST | A | A:track_001 | A:e06 @ 5.35 |  |
| g07 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g08 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g09 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g10 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e04 @ 2.10 | relevant_to_ego_path=False |
| g11 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e05 @ 2.35 |  |
| g12 | - | BRAKE_START | B | - | B:e06 @ 2.55 |  |
| g13 | - | HARD_BRAKE_START | B | - | B:e07 @ 2.55 |  |
| g14 | - | MOVING_END | B | - | B:e08 @ 3.25 |  |
| g15 | - | STOP_START | B | - | B:e09 @ 3.25 |  |
| g16 | - | TRACK_APPEARED | B | B:track_001 | B:e10 @ 3.50 |  |
| g17 | - | CLOSING_START | B | B:track_001 | B:e11 @ 3.50 | active_at_first_observation=True |
| g18 | - | CRITICAL_TTC_START | B | B:track_001 | B:e12 @ 4.40 |  |
| g19 | - | CRITICAL_TTC_END | B | B:track_001 | B:e13 @ 5.75 |  |
| g20 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e14 @ 5.80 |  |
| g21 | - | CLOSING_END | B | B:track_001 | B:e15 @ 6.10 |  |
| g22 | - | EGO_PATH_EXIT | B | B:track_001 | B:e16 @ 6.20 |  |
| g23 | - | TRACK_LOST | B | B:track_001 | B:e17 @ 7.30 |  |
| g24 | - | STRONG_THROTTLE_START | B | - | B:e18 @ 9.55 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g16 --SAME_TRACK--> g17
    g16 --SAME_TRACK--> g18
    g16 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g20
    g16 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g22
    g16 --SAME_TRACK--> g23
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
| - | A | g04 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g05 CRITICAL_TTC_END(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g06 TRACK_LOST(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | B | g07 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g08 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g09 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g10 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e04) | ego: MOVING |
| - | B | g11 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e05) | ego: MOVING<br>sign-1: STOP sign VISIBLE, known |
| - | B | g12 BRAKE_START(B) (B:e06)<br>g13 HARD_BRAKE_START(B) (B:e07) | ego: MOVING<br>sign-1: STOP sign not visible, known |
| - | B | g14 MOVING_END(B) (B:e08)<br>g15 STOP_START(B) (B:e09) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign not visible, known |
| - | B | g16 TRACK_APPEARED(B,B:track_001) (B:e10)<br>g17 CLOSING_START(B,B:track_001) (B:e11) | ego: STOP, BRAKE, HARD_BRAKE<br>sign-1: STOP sign not visible, known |
| - | B | g18 CRITICAL_TTC_START(B,B:track_001) (B:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known |
| - | B | g19 CRITICAL_TTC_END(B,B:track_001) (B:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-1: STOP sign not visible, known |
| - | B | g20 EGO_PATH_ENTRY(B,B:track_001) (B:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known |
| - | B | g21 CLOSING_END(B,B:track_001) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>sign-1: STOP sign not visible, known |
| - | B | g22 EGO_PATH_EXIT(B,B:track_001) (B:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>sign-1: STOP sign not visible, known |
| - | B | g23 TRACK_LOST(B,B:track_001) (B:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE<br>sign-1: STOP sign not visible, known |
| - | B | g24 STRONG_THROTTLE_START(B) (B:e18) | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-1: STOP sign not visible, known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.60 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 2.60 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.65 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 5.35 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.35 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 3.50 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 3.50 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.75 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 7.30 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.55 s) B started applying strong throttle.
