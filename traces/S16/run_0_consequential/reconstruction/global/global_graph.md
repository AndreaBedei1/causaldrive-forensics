# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001, C:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock ALIGNED; observed by others as: - |
| C:track_002 | anonymous_track | seen only by C; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | ALIGNED | C:e10 | 5.90 | -5.15 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.3 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 0.20 m<br>the only track of A compatible with the contact<br>collision_002 with C at 5.90 s: not compatible (not approaching before the contact: clearance 1.1 m -> 2.1 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 10.63 m/s over 3.0 s (> 1.50)) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 0.66 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.84 | C and A both reported collision_002 (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.75 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.0 m -> 5.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 2.2 s<br>clearance at the contact 4.97 m (beyond 3.50 m: confidence factor 0.89)<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.0 m -> 6.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.66 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.05 m (beyond 3.50 m: confidence factor 0.70) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g05 | -5.15 | TRACK_APPEARED_REAR | A | B | A:e02 @ 0.00 |  |
| g06 | -5.15 | TRACK_APPEARED_REAR | C | A | C:e02 @ 0.00 |  |
| g07 | -5.15 | CLOSING_START | C | A | C:e03 @ 0.00 | active_at_first_observation=True |
| g08 | -5.00 | TRACK_APPEARED_REAR | C | C:track_002 | C:e04 @ 0.15 |  |
| g09 | -5.00 | CLOSING_START | C | C:track_002 | C:e05 @ 0.15 | active_at_first_observation=True |
| g10 | -4.85 | MOVING_END | C | - | C:e06 @ 0.30 |  |
| g11 | -4.85 | STOP_START | C | - | C:e07 @ 0.30 |  |
| g12 | -4.50 | CLOSING_START | B | A | B:e03 @ 0.65 |  |
| g13 | -4.45 | CLOSING_START | A | B | A:e03 @ 0.70 |  |
| g14 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g15 | -3.75 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g16 | -3.75 | CLOSING_END | A | B | A:e04 @ 1.40 |  |
| g17 | -3.75 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g18 | -1.20 | BRAKE_START | A | - | A:e05 @ 3.95 |  |
| g19 | -0.95 | CLOSING_START | A | B | A:e06 @ 4.20 |  |
| g20 | -0.90 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g21 | -0.75 | CRITICAL_TTC_START | B | A | B:e08 @ 4.40 |  |
| g22 | -0.40 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g23 | 0.00 | COLLISION | - | A, B | A:e07 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g24 | 0.00 | CLOSING_END | A | B | A:e08 @ 5.15 |  |
| g25 | 0.00 | TRACK_LOST | C | A | C:e08 @ 5.15 |  |
| g26 | 0.05 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g27 | 0.05 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g28 | 0.05 | BRAKE_END | A | - | A:e09 @ 5.20 |  |
| g29 | 0.25 | TURN_LEFT_START | A | - | A:e10 @ 5.40 |  |
| g30 | 0.45 | CLOSING_END | C | C:track_002 | C:e09 @ 5.60 |  |
| g31 | 0.45 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g32 | 0.45 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g33 | 0.75 | COLLISION | - | A, C | A:e11 @ 5.90, C:e10 @ 5.90 | matched_event=collision_002; reference_event=False; peak_impulse=A 2695.68, C 2695.68 |
| g34 | 0.75 | STOP_END | C | - | C:e11 @ 5.90 |  |
| g35 | 0.75 | MOVING_START | C | - | C:e12 @ 5.90 |  |
| g36 | 0.80 | BRAKE_START | C | - | C:e13 @ 5.95 |  |
| g37 | 0.85 | TURN_LEFT_END | A | - | A:e12 @ 6.00 |  |
| g38 | 0.90 | MOVING_END | A | - | A:e13 @ 6.05 |  |
| g39 | 0.90 | MOVING_END | C | - | C:e14 @ 6.05 |  |
| g40 | 0.90 | STOP_START | A | - | A:e14 @ 6.05 |  |
| g41 | 0.90 | STOP_START | C | - | C:e15 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g08
    g01 --PRECEDES--> g09
    g02 --PRECEDES--> g08
    g02 --PRECEDES--> g09
    g03 --PRECEDES--> g08
    g03 --PRECEDES--> g09
    g04 --PRECEDES--> g08
    g04 --PRECEDES--> g09
    g05 --PRECEDES--> g08
    g05 --PRECEDES--> g09
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g05 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g24
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g14
    g04 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g17
    g04 --SAME_TRACK--> g20
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g26
    g04 --SAME_TRACK--> g27
    g06 --SAME_TRACK--> g07
    g08 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g25
    g08 --SAME_TRACK--> g30
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B); TRACK_APPEARED_REAR(C,A); CLOSING_START(C,A) |
| -5.00 | TRACK_APPEARED_REAR(C,C:track_002); CLOSING_START(C,C:track_002) |
| -4.85 | MOVING_END(C); STOP_START(C) |
| -4.50 | CLOSING_START(B,A) |
| -4.45 | CLOSING_START(A,B) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| -1.20 | BRAKE_START(A) |
| -0.95 | CLOSING_START(A,B) |
| -0.90 | CLOSING_START(B,A) |
| -0.75 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,B); TRACK_LOST(C,A) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A) |
| +0.25 | TURN_LEFT_START(A) |
| +0.45 | CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B) |
| +0.75 | COLLISION(A,C); STOP_END(C); MOVING_START(C) |
| +0.80 | BRAKE_START(C) |
| +0.85 | TURN_LEFT_END(A) |
| +0.90 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01)<br>g05 TRACK_APPEARED_REAR(A,B) (A:e02) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -5.15 | C | g03 MOVING_START(C) (C:e01)<br>g06 TRACK_APPEARED_REAR(C,A) (C:e02)<br>g07 CLOSING_START(C,A) (C:e03) | ego: not yet observed |
| -5.00 | C | g08 TRACK_APPEARED_REAR(C,C:track_002) (C:e04)<br>g09 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| -4.85 | C | g10 MOVING_END(C) (C:e06)<br>g11 STOP_START(C) (C:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -4.50 | B | g12 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.45 | A | g13 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: no active state |
| -4.40 | B | g14 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.75 | B | g15 CRITICAL_TTC_END(B,A) (B:e05)<br>g17 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -3.75 | A | g16 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.20 | A | g18 BRAKE_START(A) (A:e05) | ego: MOVING<br>track_001: no active state |
| -0.95 | A | g19 CLOSING_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: no active state |
| -0.90 | B | g20 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.75 | B | g21 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g22 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g23 COLLISION(A,B) (A:e07)<br>g24 CLOSING_END(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| +0.00 | B | g23 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | C | g25 TRACK_LOST(C,A) (C:e08) | ego: STOP<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.05 | B | g26 CRITICAL_TTC_END(B,A) (B:e11)<br>g27 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g28 BRAKE_END(A) (A:e09) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.25 | A | g29 TURN_LEFT_START(A) (A:e10) | ego: MOVING<br>track_001: no active state |
| +0.45 | C | g30 CLOSING_END(C,C:track_002) (C:e09) | ego: STOP<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.45 | B | g31 MOVING_END(B) (B:e13)<br>g32 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.75 | A | g33 COLLISION(A,C) (A:e11) | ego: MOVING, TURN_LEFT<br>track_001: no active state |
| +0.75 | C | g33 COLLISION(A,C) (C:e10)<br>g34 STOP_END(C) (C:e11)<br>g35 MOVING_START(C) (C:e12) | ego: STOP<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.80 | C | g36 BRAKE_START(C) (C:e13) | ego: MOVING<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.85 | A | g37 TURN_LEFT_END(A) (A:e12) | ego: MOVING, TURN_LEFT<br>track_001: no active state |
| +0.90 | A | g38 MOVING_END(A) (A:e13)<br>g40 STOP_START(A) (A:e14) | ego: MOVING<br>track_001: no active state |
| +0.90 | C | g39 MOVING_END(C) (C:e14)<br>g41 STOP_START(C) (C:e15) | ego: MOVING, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.15 s before the reference collision, A started moving (already the case when first observed).
- 5.15 s before the reference collision, B started moving (already the case when first observed).
- 5.15 s before the reference collision, C started moving (already the case when first observed).
- 5.15 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.15 s before the reference collision, A's radar started tracking B, which appeared behind it.
- 5.15 s before the reference collision, C's radar started tracking A, which appeared behind it.
- 5.15 s before the reference collision, C observed A start closing in (already the case when first observed).
- 5.00 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared behind it.
- 5.00 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 4.85 s before the reference collision, C stopped moving.
- 4.85 s before the reference collision, C came to a stop.
- 4.50 s before the reference collision, B observed A start closing in.
- 4.45 s before the reference collision, A observed B start closing in.
- 4.40 s before the reference collision, B's time-to-contact with A became critical.
- 3.75 s before the reference collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the reference collision, A observed B stop closing in.
- 3.75 s before the reference collision, B observed A stop closing in.
- 1.20 s before the reference collision, A started braking.
- 0.95 s before the reference collision, A observed B start closing in.
- 0.90 s before the reference collision, B observed A start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.40 s before the reference collision, B started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the brake.
- 0.25 s after the reference collision, A started turning left.
- 0.45 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.75 s after the reference collision, A and C both recorded this same collision (peak impulses A: 2696, C: 2696 N*s).
- 0.75 s after the reference collision, C left its stop.
- 0.75 s after the reference collision, C started moving.
- 0.80 s after the reference collision, C started braking.
- 0.85 s after the reference collision, A stopped turning left.
- 0.90 s after the reference collision, A stopped moving.
- 0.90 s after the reference collision, C stopped moving.
- 0.90 s after the reference collision, A came to a stop.
- 0.90 s after the reference collision, C came to a stop.
