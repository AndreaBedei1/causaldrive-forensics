# Global graph - S16/run_0_avoided

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 0.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.38 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 3.0 s<br>clearance at the contact 0.57 m<br>the only track of B compatible with the contact |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g04 | -5.15 | TRACK_APPEARED_REAR | A | B | A:e02 @ 0.00 |  |
| g05 | -4.50 | CLOSING_START | B | A | B:e03 @ 0.65 |  |
| g06 | -4.45 | CLOSING_START | A | B | A:e03 @ 0.70 |  |
| g07 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g08 | -3.75 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g09 | -3.75 | CLOSING_END | A | B | A:e04 @ 1.40 |  |
| g10 | -3.75 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g11 | -1.20 | BRAKE_START | A | - | A:e05 @ 3.95 |  |
| g12 | -0.95 | CLOSING_START | A | B | A:e06 @ 4.20 |  |
| g13 | -0.90 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g14 | -0.75 | CRITICAL_TTC_START | B | A | B:e08 @ 4.40 |  |
| g15 | -0.40 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e07 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g17 | 0.00 | CLOSING_END | A | B | A:e08 @ 5.15 |  |
| g18 | 0.05 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g19 | 0.05 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g20 | 0.45 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g21 | 0.45 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g22 | 0.60 | MOVING_END | A | - | A:e09 @ 5.75 |  |
| g23 | 0.60 | STOP_START | A | - | A:e10 @ 5.75 |  |
| g24 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g25 | - | TRACK_APPEARED_REAR | C | C:track_001 | C:e02 @ 0.00 |  |
| g26 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.00 | active_at_first_observation=True |
| g27 | - | TRACK_APPEARED_REAR | C | C:track_002 | C:e04 @ 0.15 |  |
| g28 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.15 | active_at_first_observation=True |
| g29 | - | MOVING_END | C | - | C:e06 @ 0.30 |  |
| g30 | - | STOP_START | C | - | C:e07 @ 0.30 |  |
| g31 | - | TRACK_LOST | C | C:track_001 | C:e08 @ 5.15 |  |
| g32 | - | CLOSING_END | C | C:track_002 | C:e09 @ 5.60 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g19
    g25 --SAME_TRACK--> g26
    g27 --SAME_TRACK--> g28
    g25 --SAME_TRACK--> g31
    g27 --SAME_TRACK--> g32
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B) |
| -4.50 | CLOSING_START(B,A) |
| -4.45 | CLOSING_START(A,B) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| -1.20 | BRAKE_START(A) |
| -0.95 | CLOSING_START(A,B) |
| -0.90 | CLOSING_START(B,A) |
| -0.75 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,B) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.60 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01)<br>g04 TRACK_APPEARED_REAR(A,B) (A:e02) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -4.50 | B | g05 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.45 | A | g06 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: no active state |
| -4.40 | B | g07 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.75 | B | g08 CRITICAL_TTC_END(B,A) (B:e05)<br>g10 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -3.75 | A | g09 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.20 | A | g11 BRAKE_START(A) (A:e05) | ego: MOVING<br>track_001: no active state |
| -0.95 | A | g12 CLOSING_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: no active state |
| -0.90 | B | g13 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.75 | B | g14 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g15 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g16 COLLISION(A,B) (A:e07)<br>g17 CLOSING_END(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| +0.00 | B | g16 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g18 CRITICAL_TTC_END(B,A) (B:e11)<br>g19 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.45 | B | g20 MOVING_END(B) (B:e13)<br>g21 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.60 | A | g22 MOVING_END(A) (A:e09)<br>g23 STOP_START(A) (A:e10) | ego: MOVING, BRAKE<br>track_001: no active state |
| - | C | g24 MOVING_START(C) (C:e01)<br>g25 TRACK_APPEARED_REAR(C,C:track_001) (C:e02)<br>g26 CLOSING_START(C,C:track_001) (C:e03) | ego: not yet observed |
| - | C | g27 TRACK_APPEARED_REAR(C,C:track_002) (C:e04)<br>g28 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| - | C | g29 MOVING_END(C) (C:e06)<br>g30 STOP_START(C) (C:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g31 TRACK_LOST(C,C:track_001) (C:e08) | ego: STOP<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g32 CLOSING_END(C,C:track_002) (C:e09) | ego: STOP<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.15 s before the reference collision, A started moving (already the case when first observed).
- 5.15 s before the reference collision, B started moving (already the case when first observed).
- 5.15 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.15 s before the reference collision, A's radar started tracking B, which appeared behind it.
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
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.60 s after the reference collision, A stopped moving.
- 0.60 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared behind it.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.15 s) C's radar started tracking unidentified object C:track_002, which appeared behind it.
- (unaligned, C local time 0.15 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
- (unaligned, C local time 5.15 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 5.60 s) C observed unidentified object C:track_002 stop closing in.
