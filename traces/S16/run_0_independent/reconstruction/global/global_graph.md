# Global graph - S16/run_0_independent

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: A:track_002 |
| A:track_001 | anonymous_track | seen only by A; candidate: C |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| B:track_003 | anonymous_track | seen only by B; candidate: - |

## Graph alignment

Reference event: `collision_002`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |
| C | ALIGNED | C:e10 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: C - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9095.53 vs 9095.53 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and C both reported collision_002 (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>lost 2.20 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 14.9 m -> 14.7 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.26 m/s over 0.8 s |
| A:track_002 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 8.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.15 m/s over 2.9 s<br>range at the contact 0.18 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -14.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -14.10 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -13.60 | MOVING_END | C | - | C:e02 @ 0.50 |  |
| g04 | -13.60 | STOP_START | C | - | C:e03 @ 0.50 |  |
| g05 | -10.15 | BRAKE_START | A | - | A:e02 @ 3.95 |  |
| g06 | -8.95 | COLLISION | A | - | A:e03 @ 5.15 | peak_impulse=6073.81 |
| g07 | -8.30 | MOVING_END | A | - | A:e04 @ 5.80 |  |
| g08 | -8.30 | STOP_START | A | - | A:e05 @ 5.80 |  |
| g09 | -5.00 | YIELD_SIGN_DETECTED_START | C | C:sign-1 | C:e04 @ 9.10 | relevant_to_ego_path=False |
| g10 | -4.50 | YIELD_SIGN_DETECTED_END | C | C:sign-1 | C:e05 @ 9.60 |  |
| g11 | -3.15 | BRAKE_END | A | - | A:e06 @ 10.95 |  |
| g12 | -2.95 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e07 @ 11.15 |  |
| g13 | -2.95 | TRACK_APPEARED_LEFT | A | C | A:e08 @ 11.15 |  |
| g14 | -2.70 | STOP_END | A | - | A:e09 @ 11.40 |  |
| g15 | -2.70 | MOVING_START | A | - | A:e10 @ 11.40 |  |
| g16 | -2.35 | CLOSING_START | A | C | A:e11 @ 11.75 |  |
| g17 | -2.30 | CLOSING_START | A | A:track_001 | A:e12 @ 11.80 |  |
| g18 | -2.20 | TRACK_LOST | A | A:track_001 | A:e13 @ 11.90 |  |
| g19 | -2.15 | STOP_END | C | - | C:e06 @ 11.95 |  |
| g20 | -2.15 | MOVING_START | C | - | C:e07 @ 11.95 |  |
| g21 | -2.00 | EGO_PATH_ENTRY | A | C | A:e14 @ 12.10 |  |
| g22 | -1.45 | CRITICAL_TTC_START | A | C | A:e15 @ 12.65 |  |
| g23 | -0.30 | STOP_SIGN_DETECTED_START | C | C:sign-3 | C:e08 @ 13.80 | relevant_to_ego_path=False |
| g24 | -0.30 | STOP_SIGN_DETECTED_END | C | C:sign-3 | C:e09 @ 13.80 |  |
| g25 | 0.00 | COLLISION | - | A, C | A:e16 @ 14.10, C:e10 @ 14.10 | matched_event=collision_002; reference_event=True; peak_impulse=A 9095.53, C 9095.53 |
| g26 | 0.00 | BRAKE_START | C | - | C:e11 @ 14.10 |  |
| g27 | 0.20 | CLOSING_END | A | C | A:e17 @ 14.30 |  |
| g28 | 0.25 | TRACK_LOST | A | C | A:e18 @ 14.35 |  |
| g29 | 0.55 | MOVING_END | A | - | A:e19 @ 14.65 |  |
| g30 | 0.55 | MOVING_END | C | - | C:e12 @ 14.65 |  |
| g31 | 0.55 | STOP_START | A | - | A:e20 @ 14.65 |  |
| g32 | 0.55 | STOP_START | C | - | C:e13 @ 14.65 |  |
| g33 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g34 | - | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g35 | - | CLOSING_START | B | B:track_001 | B:e03 @ 0.70 |  |
| g36 | - | CRITICAL_TTC_START | B | B:track_001 | B:e04 @ 0.75 |  |
| g37 | - | CRITICAL_TTC_END | B | B:track_001 | B:e05 @ 1.40 |  |
| g38 | - | CLOSING_END | B | B:track_001 | B:e06 @ 1.40 |  |
| g39 | - | CLOSING_START | B | B:track_001 | B:e07 @ 4.25 |  |
| g40 | - | CRITICAL_TTC_START | B | B:track_001 | B:e08 @ 4.45 |  |
| g41 | - | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g42 | - | COLLISION | B | - | B:e10 @ 5.15 | peak_impulse=6073.81 |
| g43 | - | CRITICAL_TTC_END | B | B:track_001 | B:e11 @ 5.20 |  |
| g44 | - | CLOSING_END | B | B:track_001 | B:e12 @ 5.20 |  |
| g45 | - | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g46 | - | STOP_START | B | - | B:e14 @ 5.60 |  |
| g47 | - | EGO_PATH_EXIT | B | B:track_001 | B:e15 @ 13.45 |  |
| g48 | - | TRACK_APPEARED_LEFT | B | B:track_002 | B:e16 @ 13.55 |  |
| g49 | - | TRACK_APPEARED_LEFT | B | B:track_003 | B:e17 @ 13.55 |  |
| g50 | - | TRACK_LOST | B | B:track_001 | B:e18 @ 14.00 |  |
| g51 | - | TRACK_LOST | B | B:track_003 | B:e19 @ 14.50 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g13 --SAME_TRACK--> g16
    g12 --SAME_TRACK--> g17
    g12 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g21
    g13 --SAME_TRACK--> g22
    g13 --SAME_TRACK--> g27
    g13 --SAME_TRACK--> g28
    g34 --SAME_TRACK--> g35
    g34 --SAME_TRACK--> g36
    g34 --SAME_TRACK--> g37
    g34 --SAME_TRACK--> g38
    g34 --SAME_TRACK--> g39
    g34 --SAME_TRACK--> g40
    g34 --SAME_TRACK--> g43
    g34 --SAME_TRACK--> g44
    g34 --SAME_TRACK--> g47
    g34 --SAME_TRACK--> g50
    g49 --SAME_TRACK--> g51
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -14.10 | MOVING_START(A); MOVING_START(C) |
| -13.60 | MOVING_END(C); STOP_START(C) |
| -10.15 | BRAKE_START(A) |
| -8.95 | COLLISION(A) |
| -8.30 | MOVING_END(A); STOP_START(A) |
| -5.00 | YIELD_SIGN_DETECTED_START(C,C:sign-1) |
| -4.50 | YIELD_SIGN_DETECTED_END(C,C:sign-1) |
| -3.15 | BRAKE_END(A) |
| -2.95 | TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_LEFT(A,C) |
| -2.70 | STOP_END(A); MOVING_START(A) |
| -2.35 | CLOSING_START(A,C) |
| -2.30 | CLOSING_START(A,A:track_001) |
| -2.20 | TRACK_LOST(A,A:track_001) |
| -2.15 | STOP_END(C); MOVING_START(C) |
| -2.00 | EGO_PATH_ENTRY(A,C) |
| -1.45 | CRITICAL_TTC_START(A,C) |
| -0.30 | STOP_SIGN_DETECTED_START(C,C:sign-3); STOP_SIGN_DETECTED_END(C,C:sign-3) |
| +0.00 | COLLISION(A,C); BRAKE_START(C) |
| +0.20 | CLOSING_END(A,C) |
| +0.25 | TRACK_LOST(A,C) |
| +0.55 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (C): CRITICAL_TTC_START 12.65, COLLISION 5.15 (+-7.50 s); EGO_PATH_ENTRY 12.10 before critical TTC (-0.55 s) [local times; t_global: critical_ttc_start -1.45, ego_path_entry -2.00, collision -8.95]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 0.75, COLLISION 5.15 (+4.40 s) [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -14.10 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -14.10 | C | g02 MOVING_START(C) (C:e01) | ego: not yet observed |
| -13.60 | C | g03 MOVING_END(C) (C:e02)<br>g04 STOP_START(C) (C:e03) | ego: MOVING |
| -10.15 | A | g05 BRAKE_START(A) (A:e02) | ego: MOVING |
| -8.95 | A | g06 COLLISION(A) (A:e03) | ego: MOVING, BRAKE |
| -8.30 | A | g07 MOVING_END(A) (A:e04)<br>g08 STOP_START(A) (A:e05) | ego: MOVING, BRAKE |
| -5.00 | C | g09 YIELD_SIGN_DETECTED_START(C,C:sign-1) (C:e04) | ego: STOP |
| -4.50 | C | g10 YIELD_SIGN_DETECTED_END(C,C:sign-1) (C:e05) | ego: STOP<br>sign-1: YIELD sign known |
| -3.15 | A | g11 BRAKE_END(A) (A:e06) | ego: STOP, BRAKE |
| -2.95 | A | g12 TRACK_APPEARED_LEFT(A,A:track_001) (A:e07)<br>g13 TRACK_APPEARED_LEFT(A,C) (A:e08) | ego: STOP |
| -2.70 | A | g14 STOP_END(A) (A:e09)<br>g15 MOVING_START(A) (A:e10) | ego: STOP<br>track_001: no active state<br>track_002: no active state |
| -2.35 | A | g16 CLOSING_START(A,C) (A:e11) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -2.30 | A | g17 CLOSING_START(A,A:track_001) (A:e12) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| -2.20 | A | g18 TRACK_LOST(A,A:track_001) (A:e13) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -2.15 | C | g19 STOP_END(C) (C:e06)<br>g20 MOVING_START(C) (C:e07) | ego: STOP<br>sign-1: YIELD sign known |
| -2.00 | A | g21 EGO_PATH_ENTRY(A,C) (A:e14) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.45 | A | g22 CRITICAL_TTC_START(A,C) (A:e15) | ego: MOVING<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| -0.30 | C | g23 STOP_SIGN_DETECTED_START(C,C:sign-3) (C:e08)<br>g24 STOP_SIGN_DETECTED_END(C,C:sign-3) (C:e09) | ego: MOVING<br>sign-1: YIELD sign known |
| +0.00 | A | g25 COLLISION(A,C) (A:e16) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.00 | C | g25 COLLISION(A,C) (C:e10)<br>g26 BRAKE_START(C) (C:e11) | ego: MOVING<br>sign-1: YIELD sign known<br>sign-3: STOP sign known |
| +0.20 | A | g27 CLOSING_END(A,C) (A:e17) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.25 | A | g28 TRACK_LOST(A,C) (A:e18) | ego: MOVING<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.55 | A | g29 MOVING_END(A) (A:e19)<br>g31 STOP_START(A) (A:e20) | ego: MOVING<br>track lost, states UNKNOWN: track_001, track_002 |
| +0.55 | C | g30 MOVING_END(C) (C:e12)<br>g32 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>sign-1: YIELD sign known<br>sign-3: STOP sign known |
| - | B | g33 MOVING_START(B) (B:e01)<br>g34 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02) | ego: not yet observed |
| - | B | g35 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| - | B | g36 CRITICAL_TTC_START(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| - | B | g37 CRITICAL_TTC_END(B,B:track_001) (B:e05)<br>g38 CLOSING_END(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | B | g39 CLOSING_START(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| - | B | g40 CRITICAL_TTC_START(B,B:track_001) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| - | B | g41 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | B | g42 COLLISION(B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | B | g43 CRITICAL_TTC_END(B,B:track_001) (B:e11)<br>g44 CLOSING_END(B,B:track_001) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| - | B | g45 MOVING_END(B) (B:e13)<br>g46 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| - | B | g47 EGO_PATH_EXIT(B,B:track_001) (B:e15) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| - | B | g48 TRACK_APPEARED_LEFT(B,B:track_002) (B:e16)<br>g49 TRACK_APPEARED_LEFT(B,B:track_003) (B:e17) | ego: STOP, BRAKE<br>track_001: no active state |
| - | B | g50 TRACK_LOST(B,B:track_001) (B:e18) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state |
| - | B | g51 TRACK_LOST(B,B:track_003) (B:e19) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 14.10 s before the matched collision, A started moving (already the case when first observed).
- 14.10 s before the matched collision, C started moving (already the case when first observed).
- 13.60 s before the matched collision, C stopped moving.
- 13.60 s before the matched collision, C came to a stop.
- 10.15 s before the matched collision, A started braking.
- 8.95 s before the matched collision, A's collision sensor recorded a contact (peak impulse 6074 N*s).
- 8.30 s before the matched collision, A stopped moving.
- 8.30 s before the matched collision, A came to a stop.
- 5.00 s before the matched collision, C's camera established a YIELD sign detection (unidentified object C:sign-1) (the detector judged it not relevant to its path).
- 4.50 s before the matched collision, C's camera stopped detecting YIELD sign unidentified object C:sign-1.
- 3.15 s before the matched collision, A released the brake.
- 2.95 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 2.95 s before the matched collision, A's radar started tracking C, which appeared on its left.
- 2.70 s before the matched collision, A left its stop.
- 2.70 s before the matched collision, A started moving.
- 2.35 s before the matched collision, A observed C start closing in.
- 2.30 s before the matched collision, A observed unidentified object A:track_001 start closing in.
- 2.20 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 2.15 s before the matched collision, C left its stop.
- 2.15 s before the matched collision, C started moving.
- 2.00 s before the matched collision, A observed C enter its forward path corridor.
- 1.45 s before the matched collision, A's time-to-contact with C became critical.
- 0.30 s before the matched collision, C's camera established a STOP sign detection (unidentified object C:sign-3) (the detector judged it not relevant to its path).
- 0.30 s before the matched collision, C's camera stopped detecting STOP sign unidentified object C:sign-3.
- At the matched collision, A and C both recorded this same collision (peak impulses A: 9096, C: 9096 N*s).
- At the matched collision, C started braking.
- 0.20 s after the matched collision, A observed C stop closing in.
- 0.25 s after the matched collision, A's radar lost C (its states are UNKNOWN from then on, not ended).
- 0.55 s after the matched collision, A stopped moving.
- 0.55 s after the matched collision, C stopped moving.
- 0.55 s after the matched collision, A came to a stop.
- 0.55 s after the matched collision, C came to a stop.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.00 s) B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- (unaligned, B local time 0.70 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 0.75 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 1.40 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 1.40 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 4.45 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 4.75 s) B started braking.
- (unaligned, B local time 5.15 s) B's collision sensor recorded a contact (peak impulse 6074 N*s).
- (unaligned, B local time 5.20 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.20 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.60 s) B stopped moving.
- (unaligned, B local time 5.60 s) B came to a stop.
- (unaligned, B local time 13.45 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 13.55 s) B's radar started tracking unidentified object B:track_002, which appeared on its left.
- (unaligned, B local time 13.55 s) B's radar started tracking unidentified object B:track_003, which appeared on its left.
- (unaligned, B local time 14.00 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 14.50 s) B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
