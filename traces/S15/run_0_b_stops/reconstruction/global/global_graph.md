# Global graph - S15/run_0_b_stops

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| B:track_003 | anonymous_track | seen only by B; candidate: - |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | TRACK_APPEARED_RIGHT | A | A:track_002 | A:e04 @ 2.00 |  |
| g05 | - | CLOSING_START | A | A:track_002 | A:e05 @ 2.00 | active_at_first_observation=True |
| g06 | - | CRITICAL_TTC_START | A | A:track_002 | A:e06 @ 2.00 | active_at_first_observation=True |
| g07 | - | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 2.45 |  |
| g08 | - | TRACK_LOST | A | A:track_002 | A:e08 @ 3.80 |  |
| g09 | - | TRACK_LOST | A | A:track_001 | A:e09 @ 4.45 |  |
| g10 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g11 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g12 | - | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e03 @ 1.45 |  |
| g13 | - | CLOSING_START | B | B:track_001 | B:e04 @ 1.45 | active_at_first_observation=True |
| g14 | - | STRONG_THROTTLE_END | B | - | B:e05 @ 1.80 |  |
| g15 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e06 @ 1.80 | relevant_to_ego_path=False |
| g16 | - | TRACK_APPEARED_LEFT | B | B:track_002 | B:e07 @ 1.95 |  |
| g17 | - | CLOSING_START | B | B:track_002 | B:e08 @ 1.95 | active_at_first_observation=True |
| g18 | - | CRITICAL_TTC_START | B | B:track_002 | B:e09 @ 2.00 |  |
| g19 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e10 @ 2.10 |  |
| g20 | - | CRITICAL_TTC_START | B | B:track_001 | B:e11 @ 2.35 |  |
| g21 | - | BRAKE_START | B | - | B:e12 @ 2.55 |  |
| g22 | - | HARD_BRAKE_START | B | - | B:e13 @ 2.55 |  |
| g23 | - | CRITICAL_TTC_END | B | B:track_001 | B:e14 @ 2.70 |  |
| g24 | - | TRACK_LOST | B | B:track_001 | B:e15 @ 2.85 |  |
| g25 | - | MOVING_END | B | - | B:e16 @ 3.40 |  |
| g26 | - | STOP_START | B | - | B:e17 @ 3.40 |  |
| g27 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e18 @ 3.40 | relevant_to_ego_path=False |
| g28 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e19 @ 3.70 |  |
| g29 | - | EGO_PATH_ENTRY | B | B:track_002 | B:e20 @ 3.90 |  |
| g30 | - | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e21 @ 3.95 |  |
| g31 | - | CLOSING_START | B | B:track_003 | B:e22 @ 3.95 | active_at_first_observation=True |
| g32 | - | CRITICAL_TTC_END | B | B:track_002 | B:e23 @ 4.20 |  |
| g33 | - | CLOSING_END | B | B:track_002 | B:e24 @ 4.25 |  |
| g34 | - | EGO_PATH_EXIT | B | B:track_002 | B:e25 @ 4.40 |  |
| g35 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e26 @ 4.80 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-2 |
| g36 | - | TRACK_LOST | B | B:track_002 | B:e27 @ 4.80 |  |
| g37 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e28 @ 4.80 | sign_track=sign-2 |
| g38 | - | CLOSING_END | B | B:track_003 | B:e29 @ 5.35 |  |
| g39 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e30 @ 5.60 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| g40 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e31 @ 5.60 | sign_track=sign-3 |
| g41 | - | EGO_PATH_ENTRY | B | B:track_003 | B:e32 @ 5.65 |  |
| g42 | - | EGO_PATH_EXIT | B | B:track_003 | B:e33 @ 6.45 |  |
| g43 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e34 @ 6.70 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| g44 | - | STRONG_THROTTLE_START | B | - | B:e35 @ 10.55 |  |
| g45 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g46 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e02 @ 0.00 |  |
| g47 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e03 @ 0.00 |  |
| g48 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.00 | active_at_first_observation=True |
| g49 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.00 | active_at_first_observation=True |
| g50 | - | STRONG_THROTTLE_START | C | - | C:e06 @ 1.65 |  |
| g51 | - | STRONG_THROTTLE_END | C | - | C:e07 @ 2.10 |  |
| g52 | - | CRITICAL_TTC_START | C | C:track_002 | C:e08 @ 2.25 |  |
| g53 | - | CRITICAL_TTC_START | C | C:track_001 | C:e09 @ 2.45 |  |
| g54 | - | CRITICAL_TTC_END | C | C:track_002 | C:e10 @ 2.95 |  |
| g55 | - | TRACK_LOST | C | C:track_002 | C:e11 @ 4.00 |  |
| g56 | - | CRITICAL_TTC_END | C | C:track_001 | C:e12 @ 4.50 |  |
| g57 | - | CLOSING_END | C | C:track_001 | C:e13 @ 4.50 |  |
| g58 | - | TRACK_LOST | C | C:track_001 | C:e14 @ 4.50 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g08
    g02 --SAME_TRACK--> g09
    g12 --SAME_TRACK--> g13
    g16 --SAME_TRACK--> g17
    g16 --SAME_TRACK--> g18
    g12 --SAME_TRACK--> g20
    g12 --SAME_TRACK--> g23
    g12 --SAME_TRACK--> g24
    g16 --SAME_TRACK--> g29
    g30 --SAME_TRACK--> g31
    g16 --SAME_TRACK--> g32
    g16 --SAME_TRACK--> g33
    g16 --SAME_TRACK--> g34
    g16 --SAME_TRACK--> g36
    g30 --SAME_TRACK--> g38
    g30 --SAME_TRACK--> g41
    g30 --SAME_TRACK--> g42
    g46 --SAME_TRACK--> g48
    g47 --SAME_TRACK--> g49
    g47 --SAME_TRACK--> g52
    g46 --SAME_TRACK--> g53
    g47 --SAME_TRACK--> g54
    g47 --SAME_TRACK--> g55
    g46 --SAME_TRACK--> g56
    g46 --SAME_TRACK--> g57
    g46 --SAME_TRACK--> g58
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| - | A | g04 TRACK_APPEARED_RIGHT(A,A:track_002) (A:e04)<br>g05 CLOSING_START(A,A:track_002) (A:e05)<br>g06 CRITICAL_TTC_START(A,A:track_002) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| - | A | g07 CRITICAL_TTC_START(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| - | A | g08 TRACK_LOST(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | A | g09 TRACK_LOST(A,A:track_001) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| - | B | g10 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g11 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g12 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e03)<br>g13 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| - | B | g14 STRONG_THROTTLE_END(B) (B:e05)<br>g15 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e06) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| - | B | g16 TRACK_APPEARED_LEFT(B,B:track_002) (B:e07)<br>g17 CLOSING_START(B,B:track_002) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| - | B | g18 CRITICAL_TTC_START(B,B:track_002) (B:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |
| - | B | g19 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e10) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g20 CRITICAL_TTC_START(B,B:track_001) (B:e11) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g21 BRAKE_START(B) (B:e12)<br>g22 HARD_BRAKE_START(B) (B:e13) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g23 CRITICAL_TTC_END(B,B:track_001) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g24 TRACK_LOST(B,B:track_001) (B:e15) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| - | B | g25 MOVING_END(B) (B:e16)<br>g26 STOP_START(B) (B:e17)<br>g27 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e18) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | B | g28 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e19) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g29 EGO_PATH_ENTRY(B,B:track_002) (B:e20) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g30 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e21)<br>g31 CLOSING_START(B,B:track_003) (B:e22) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g32 CRITICAL_TTC_END(B,B:track_002) (B:e23) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g33 CLOSING_END(B,B:track_002) (B:e24) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g34 EGO_PATH_EXIT(B,B:track_002) (B:e25) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: IN_EGO_PATH<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g35 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e26)<br>g36 TRACK_LOST(B,B:track_002) (B:e27)<br>g37 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e28) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g38 CLOSING_END(B,B:track_003) (B:e29) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g39 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e30)<br>g40 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e31) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g41 EGO_PATH_ENTRY(B,B:track_003) (B:e32) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g42 EGO_PATH_EXIT(B,B:track_003) (B:e33) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g43 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e34) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | B | g44 STRONG_THROTTLE_START(B) (B:e35) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | C | g45 MOVING_START(C) (C:e01)<br>g46 TRACK_APPEARED_FRONT(C,C:track_001) (C:e02)<br>g47 TRACK_APPEARED_LEFT(C,C:track_002) (C:e03)<br>g48 CLOSING_START(C,C:track_001) (C:e04)<br>g49 CLOSING_START(C,C:track_002) (C:e05) | ego: not yet observed |
| - | C | g50 STRONG_THROTTLE_START(C) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g51 STRONG_THROTTLE_END(C) (C:e07) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g52 CRITICAL_TTC_START(C,C:track_002) (C:e08) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g53 CRITICAL_TTC_START(C,C:track_001) (C:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g54 CRITICAL_TTC_END(C,C:track_002) (C:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g55 TRACK_LOST(C,C:track_002) (C:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g56 CRITICAL_TTC_END(C,C:track_001) (C:e12)<br>g57 CLOSING_END(C,C:track_001) (C:e13)<br>g58 TRACK_LOST(C,C:track_001) (C:e14) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's radar started tracking unidentified object A:track_002, which appeared on its right.
- (unaligned, A local time 2.00 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- (unaligned, A local time 2.45 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 3.80 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 4.45 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.45 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 1.45 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 1.80 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 1.95 s) B's radar started tracking unidentified object B:track_002, which appeared on its left.
- (unaligned, B local time 1.95 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 2.00 s) B's time-to-contact with unidentified object B:track_002 became critical.
- (unaligned, B local time 2.10 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.35 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 2.70 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 2.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 3.40 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 3.70 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 3.90 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 3.95 s) B's radar started tracking unidentified object B:track_003, which appeared on its right.
- (unaligned, B local time 3.95 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 4.20 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 4.40 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 4.80 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- (unaligned, B local time 4.80 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 4.80 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.35 s) B observed unidentified object B:track_003 stop closing in.
- (unaligned, B local time 5.60 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- (unaligned, B local time 5.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.65 s) B observed unidentified object B:track_003 enter its forward path corridor.
- (unaligned, B local time 6.45 s) B observed unidentified object B:track_003 leave its forward path corridor.
- (unaligned, B local time 6.70 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- (unaligned, B local time 10.55 s) B started applying strong throttle.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 1.65 s) C started applying strong throttle.
- (unaligned, C local time 2.10 s) C stopped applying strong throttle.
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.45 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.95 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.00 s) C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 4.50 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.50 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 4.50 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
