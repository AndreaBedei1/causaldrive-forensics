# Global graph - S04/run_0_yield

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |

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
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 2.10 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.10 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 3.00 |  |
| g05 | - | PREDICTED_PATH_CONFLICT_START | A | A:track_001 | A:e05 @ 3.45 |  |
| g06 | - | PREDICTED_PATH_CONFLICT_END | A | A:track_001 | A:e06 @ 3.75 |  |
| g07 | - | TRACK_LOST | A | A:track_001 | A:e07 @ 4.95 |  |
| g08 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e08 @ 8.15 | relevant_to_ego_path=False |
| g09 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e09 @ 8.45 |  |
| g10 | - | TRACK_APPEARED | A | A:track_002 | A:e10 @ 9.70 |  |
| g11 | - | CLOSING_START | A | A:track_002 | A:e11 @ 9.70 | active_at_first_observation=True |
| g12 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g13 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g14 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g15 | - | TRACK_APPEARED | B | B:track_001 | B:e04 @ 2.00 |  |
| g16 | - | CLOSING_START | B | B:track_001 | B:e05 @ 2.00 | active_at_first_observation=True |
| g17 | - | TRACK_LOST | B | B:track_001 | B:e06 @ 2.35 |  |
| g18 | - | BRAKE_START | B | - | B:e07 @ 3.15 |  |
| g19 | - | HARD_BRAKE_START | B | - | B:e08 @ 3.15 |  |
| g20 | - | MOVING_END | B | - | B:e09 @ 3.90 |  |
| g21 | - | STOP_START | B | - | B:e10 @ 3.90 |  |
| g22 | - | TRACK_APPEARED | B | B:track_002 | B:e11 @ 4.35 |  |
| g23 | - | CLOSING_START | B | B:track_002 | B:e12 @ 4.35 | active_at_first_observation=True |
| g24 | - | CRITICAL_TTC_START | B | B:track_002 | B:e13 @ 4.35 | active_at_first_observation=True |
| g25 | - | EGO_PATH_ENTRY | B | B:track_002 | B:e14 @ 5.40 |  |
| g26 | - | CRITICAL_TTC_END | B | B:track_002 | B:e15 @ 5.45 |  |
| g27 | - | CLOSING_END | B | B:track_002 | B:e16 @ 5.55 |  |
| g28 | - | EGO_PATH_EXIT | B | B:track_002 | B:e17 @ 5.90 |  |
| g29 | - | TRACK_LOST | B | B:track_002 | B:e18 @ 6.90 |  |
| g30 | - | HARD_BRAKE_END | B | - | B:e19 @ 7.15 |  |
| g31 | - | BRAKE_END | B | - | B:e20 @ 7.15 |  |
| g32 | - | STRONG_THROTTLE_START | B | - | B:e21 @ 7.15 |  |
| g33 | - | STOP_END | B | - | B:e22 @ 7.55 |  |
| g34 | - | MOVING_START | B | - | B:e23 @ 7.55 |  |
| g35 | - | STRONG_THROTTLE_END | B | - | B:e24 @ 8.55 |  |
| g36 | - | BRAKE_START | B | - | B:e25 @ 8.75 |  |
| g37 | - | BRAKE_END | B | - | B:e26 @ 9.00 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g10 --SAME_TRACK--> g11
    g15 --SAME_TRACK--> g16
    g15 --SAME_TRACK--> g17
    g22 --SAME_TRACK--> g23
    g22 --SAME_TRACK--> g24
    g22 --SAME_TRACK--> g25
    g22 --SAME_TRACK--> g26
    g22 --SAME_TRACK--> g27
    g22 --SAME_TRACK--> g28
    g22 --SAME_TRACK--> g29
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
| - | A | g05 PREDICTED_PATH_CONFLICT_START(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g06 PREDICTED_PATH_CONFLICT_END(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| - | A | g07 TRACK_LOST(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g08 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e08) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| - | A | g09 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e09) | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign VISIBLE, known |
| - | A | g10 TRACK_APPEARED(A,A:track_002) (A:e10)<br>g11 CLOSING_START(A,A:track_002) (A:e11) | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | B | g12 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g13 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g14 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g15 TRACK_APPEARED(B,B:track_001) (B:e04)<br>g16 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING |
| - | B | g17 TRACK_LOST(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| - | B | g18 BRAKE_START(B) (B:e07)<br>g19 HARD_BRAKE_START(B) (B:e08) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| - | B | g20 MOVING_END(B) (B:e09)<br>g21 STOP_START(B) (B:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 |
| - | B | g22 TRACK_APPEARED(B,B:track_002) (B:e11)<br>g23 CLOSING_START(B,B:track_002) (B:e12)<br>g24 CRITICAL_TTC_START(B,B:track_002) (B:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 |
| - | B | g25 EGO_PATH_ENTRY(B,B:track_002) (B:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001 |
| - | B | g26 CRITICAL_TTC_END(B,B:track_002) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 |
| - | B | g27 CLOSING_END(B,B:track_002) (B:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 |
| - | B | g28 EGO_PATH_EXIT(B,B:track_002) (B:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 |
| - | B | g29 TRACK_LOST(B,B:track_002) (B:e18) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>lost (states UNKNOWN): track_001 |
| - | B | g30 HARD_BRAKE_END(B) (B:e19)<br>g31 BRAKE_END(B) (B:e20)<br>g32 STRONG_THROTTLE_START(B) (B:e21) | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001, track_002 |
| - | B | g33 STOP_END(B) (B:e22)<br>g34 MOVING_START(B) (B:e23) | ego: STOP, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 |
| - | B | g35 STRONG_THROTTLE_END(B) (B:e24) | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 |
| - | B | g36 BRAKE_START(B) (B:e25) | ego: MOVING<br>lost (states UNKNOWN): track_001, track_002 |
| - | B | g37 BRAKE_END(B) (B:e26) | ego: MOVING, BRAKE<br>lost (states UNKNOWN): track_001, track_002 |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.10 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 2.10 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 3.45 s) A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- (unaligned, A local time 3.75 s) A stopped predicting a path conflict with unidentified object A:track_001.
- (unaligned, A local time 4.95 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 8.15 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 8.45 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 9.70 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 9.70 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.00 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 2.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.35 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.15 s) B started braking hard.
- (unaligned, B local time 3.90 s) B stopped moving.
- (unaligned, B local time 3.90 s) B came to a stop.
- (unaligned, B local time 4.35 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 4.35 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 4.35 s) B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- (unaligned, B local time 5.40 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 5.45 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 5.55 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 5.90 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 6.90 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 7.15 s) B stopped braking hard.
- (unaligned, B local time 7.15 s) B released the brake.
- (unaligned, B local time 7.15 s) B started applying strong throttle.
- (unaligned, B local time 7.55 s) B left its stop.
- (unaligned, B local time 7.55 s) B started moving.
- (unaligned, B local time 8.55 s) B stopped applying strong throttle.
- (unaligned, B local time 8.75 s) B started braking.
- (unaligned, B local time 9.00 s) B released the brake.
