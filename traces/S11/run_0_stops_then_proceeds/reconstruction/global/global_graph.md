# Global graph - S11/run_0_stops_then_proceeds

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| B:track_003 | anonymous_track | seen only by B; candidate: - |
| B:track_004 | anonymous_track | seen only by B; candidate: - |
| B:track_005 | anonymous_track | seen only by B; candidate: - |

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
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_004 | B:track_004 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_005 | B:track_005 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e02 @ 2.60 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.60 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 4.65 |  |
| g05 | - | CRITICAL_TTC_END | A | A:track_001 | A:e05 @ 5.25 |  |
| g06 | - | TRACK_LOST | A | A:track_001 | A:e06 @ 5.35 |  |
| g07 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g08 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g09 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g10 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e04 @ 2.10 | relevant_to_ego_path=False |
| g11 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e05 @ 2.40 |  |
| g12 | - | BRAKE_START | B | - | B:e06 @ 2.55 |  |
| g13 | - | HARD_BRAKE_START | B | - | B:e07 @ 2.55 |  |
| g14 | - | MOVING_END | B | - | B:e08 @ 3.25 |  |
| g15 | - | STOP_START | B | - | B:e09 @ 3.25 |  |
| g16 | - | TRACK_APPEARED_LEFT | B | B:track_001 | B:e10 @ 3.50 |  |
| g17 | - | CLOSING_START | B | B:track_001 | B:e11 @ 3.50 | active_at_first_observation=True |
| g18 | - | CRITICAL_TTC_START | B | B:track_001 | B:e12 @ 4.40 |  |
| g19 | - | CRITICAL_TTC_END | B | B:track_001 | B:e13 @ 5.75 |  |
| g20 | - | EGO_PATH_ENTRY | B | B:track_001 | B:e14 @ 5.80 |  |
| g21 | - | CLOSING_END | B | B:track_001 | B:e15 @ 6.10 |  |
| g22 | - | EGO_PATH_EXIT | B | B:track_001 | B:e16 @ 6.20 |  |
| g23 | - | HARD_BRAKE_END | B | - | B:e17 @ 6.75 |  |
| g24 | - | BRAKE_END | B | - | B:e18 @ 6.75 |  |
| g25 | - | STRONG_THROTTLE_START | B | - | B:e19 @ 6.75 |  |
| g26 | - | STOP_END | B | - | B:e20 @ 7.20 |  |
| g27 | - | MOVING_START | B | - | B:e21 @ 7.20 |  |
| g28 | - | TRACK_LOST | B | B:track_001 | B:e22 @ 7.30 |  |
| g29 | - | STRONG_THROTTLE_END | B | - | B:e23 @ 8.40 |  |
| g30 | - | TRACK_APPEARED_LEFT | B | B:track_003 | B:e24 @ 8.40 |  |
| g31 | - | TRACK_APPEARED_LEFT | B | B:track_004 | B:e25 @ 8.40 |  |
| g32 | - | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e26 @ 8.40 |  |
| g33 | - | CLOSING_START | B | B:track_002 | B:e27 @ 8.40 | active_at_first_observation=True |
| g34 | - | CLOSING_START | B | B:track_003 | B:e28 @ 8.40 | active_at_first_observation=True |
| g35 | - | CLOSING_START | B | B:track_004 | B:e29 @ 8.40 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED_RIGHT | B | B:track_005 | B:e30 @ 8.45 |  |
| g37 | - | CLOSING_START | B | B:track_005 | B:e31 @ 8.45 | active_at_first_observation=True |
| g38 | - | TRACK_LOST | B | B:track_005 | B:e32 @ 8.65 |  |
| g39 | - | EGO_PATH_ENTRY | B | B:track_004 | B:e33 @ 9.60 |  |
| g40 | - | EGO_PATH_ENTRY | B | B:track_003 | B:e34 @ 9.70 |  |
| g41 | - | EGO_PATH_EXIT | B | B:track_004 | B:e35 @ 9.85 |  |
| g42 | - | EGO_PATH_EXIT | B | B:track_003 | B:e36 @ 9.90 |  |
| g43 | - | TRACK_LOST | B | B:track_002 | B:e37 @ 9.90 |  |

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
    g16 --SAME_TRACK--> g28
    g32 --SAME_TRACK--> g33
    g30 --SAME_TRACK--> g34
    g31 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g37
    g36 --SAME_TRACK--> g38
    g31 --SAME_TRACK--> g39
    g30 --SAME_TRACK--> g40
    g31 --SAME_TRACK--> g41
    g30 --SAME_TRACK--> g42
    g32 --SAME_TRACK--> g43
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
| - | A | g02 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| - | A | g04 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| - | A | g05 CRITICAL_TTC_END(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | A | g06 TRACK_LOST(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | B | g07 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g08 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g09 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| - | B | g10 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e04) | ego: MOVING |
| - | B | g11 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e05) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g12 BRAKE_START(B) (B:e06)<br>g13 HARD_BRAKE_START(B) (B:e07) | ego: MOVING<br>sign-1: STOP sign known |
| - | B | g14 MOVING_END(B) (B:e08)<br>g15 STOP_START(B) (B:e09) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known |
| - | B | g16 TRACK_APPEARED_LEFT(B,B:track_001) (B:e10)<br>g17 CLOSING_START(B,B:track_001) (B:e11) | ego: STOP, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known |
| - | B | g18 CRITICAL_TTC_START(B,B:track_001) (B:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g19 CRITICAL_TTC_END(B,B:track_001) (B:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known |
| - | B | g20 EGO_PATH_ENTRY(B,B:track_001) (B:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known |
| - | B | g21 CLOSING_END(B,B:track_001) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g22 EGO_PATH_EXIT(B,B:track_001) (B:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known |
| - | B | g23 HARD_BRAKE_END(B) (B:e17)<br>g24 BRAKE_END(B) (B:e18)<br>g25 STRONG_THROTTLE_START(B) (B:e19) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g26 STOP_END(B) (B:e20)<br>g27 MOVING_START(B) (B:e21) | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g28 TRACK_LOST(B,B:track_001) (B:e22) | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known |
| - | B | g29 STRONG_THROTTLE_END(B) (B:e23)<br>g30 TRACK_APPEARED_LEFT(B,B:track_003) (B:e24)<br>g31 TRACK_APPEARED_LEFT(B,B:track_004) (B:e25)<br>g32 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e26)<br>g33 CLOSING_START(B,B:track_002) (B:e27)<br>g34 CLOSING_START(B,B:track_003) (B:e28)<br>g35 CLOSING_START(B,B:track_004) (B:e29) | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g36 TRACK_APPEARED_RIGHT(B,B:track_005) (B:e30)<br>g37 CLOSING_START(B,B:track_005) (B:e31) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g38 TRACK_LOST(B,B:track_005) (B:e32) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known |
| - | B | g39 EGO_PATH_ENTRY(B,B:track_004) (B:e33) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known |
| - | B | g40 EGO_PATH_ENTRY(B,B:track_003) (B:e34) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known |
| - | B | g41 EGO_PATH_EXIT(B,B:track_004) (B:e35) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING, IN_EGO_PATH<br>track_004: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known |
| - | B | g42 EGO_PATH_EXIT(B,B:track_003) (B:e36)<br>g43 TRACK_LOST(B,B:track_002) (B:e37) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING, IN_EGO_PATH<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.60 s) A's radar started tracking unidentified object A:track_001, which appeared on its right.
- (unaligned, A local time 2.60 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.65 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 5.35 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.40 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 3.50 s) B's radar started tracking unidentified object B:track_001, which appeared on its left.
- (unaligned, B local time 3.50 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.75 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 6.75 s) B stopped braking hard.
- (unaligned, B local time 6.75 s) B released the brake.
- (unaligned, B local time 6.75 s) B started applying strong throttle.
- (unaligned, B local time 7.20 s) B left its stop.
- (unaligned, B local time 7.20 s) B started moving.
- (unaligned, B local time 7.30 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.40 s) B stopped applying strong throttle.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_003, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_004, which appeared on its left.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_002, which appeared on its right.
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_004 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_005, which appeared on its right.
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_005 start closing in (already the case when first observed).
- (unaligned, B local time 8.65 s) B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.60 s) B observed unidentified object B:track_004 enter its forward path corridor.
- (unaligned, B local time 9.70 s) B observed unidentified object B:track_003 enter its forward path corridor.
- (unaligned, B local time 9.85 s) B observed unidentified object B:track_004 leave its forward path corridor.
- (unaligned, B local time 9.90 s) B observed unidentified object B:track_003 leave its forward path corridor.
- (unaligned, B local time 9.90 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
