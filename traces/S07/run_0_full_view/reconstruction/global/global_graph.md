# Global graph - S07/run_0_full_view

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 5.70 | -5.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e17 | 5.70 | -5.70 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31406.82 vs 31406.82 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 0.20 m<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 4.65 s before the matched collision<br>lost 2.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 41.4 m -> 41.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.58 m/s over 0.8 s (> 1.50) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 8.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.0 m -> 11.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 10.27 m/s over 3.0 s (> 1.50)<br>clearance at the contact 10.71 m (beyond 3.50 m: confidence factor 0.06) |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.0 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.06 m/s over 3.0 s<br>clearance at the contact 0.59 m<br>the only track of B compatible with the contact |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.70 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.00 |  |
| g04 | -5.70 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g05 | -5.70 | TRACK_APPEARED_REAR | B | A | B:e03 @ 0.00 |  |
| g06 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g07 | -5.20 | CLOSING_START | B | A | B:e04 @ 0.50 |  |
| g08 | -4.65 | TRACK_APPEARED_FRONT | A | A:track_002 | A:e04 @ 1.05 |  |
| g09 | -4.65 | CLOSING_START | A | A:track_002 | A:e05 @ 1.05 | active_at_first_observation=True |
| g10 | -4.60 | CLOSING_START | B | B:track_001 | B:e05 @ 1.10 |  |
| g11 | -4.05 | CLOSING_END | A | B | A:e06 @ 1.65 |  |
| g12 | -4.05 | CLOSING_END | B | A | B:e06 @ 1.65 |  |
| g13 | -3.70 | CLOSING_END | A | A:track_002 | A:e07 @ 2.00 |  |
| g14 | -3.60 | CLOSING_END | B | B:track_001 | B:e07 @ 2.10 |  |
| g15 | -2.50 | CLOSING_START | B | B:track_001 | B:e08 @ 3.20 |  |
| g16 | -2.45 | CLOSING_START | A | A:track_002 | A:e08 @ 3.25 |  |
| g17 | -2.15 | TRACK_LOST | A | A:track_002 | A:e09 @ 3.55 |  |
| g18 | -2.05 | BRAKE_START | B | - | B:e09 @ 3.65 |  |
| g19 | -1.80 | CLOSING_START | A | B | A:e10 @ 3.90 |  |
| g20 | -1.80 | CLOSING_START | B | A | B:e10 @ 3.90 |  |
| g21 | -1.75 | CRITICAL_TTC_START | B | B:track_001 | B:e11 @ 3.95 |  |
| g22 | -1.10 | CRITICAL_TTC_END | B | B:track_001 | B:e12 @ 4.60 |  |
| g23 | -1.10 | CRITICAL_TTC_START | A | B | A:e11 @ 4.60 |  |
| g24 | -0.85 | CLOSING_END | B | B:track_001 | B:e13 @ 4.85 |  |
| g25 | -0.85 | MOVING_END | B | - | B:e14 @ 4.85 |  |
| g26 | -0.85 | STOP_START | B | - | B:e15 @ 4.85 |  |
| g27 | -0.05 | TRACK_LOST | B | A | B:e16 @ 5.65 |  |
| g28 | 0.00 | COLLISION | - | A, B | A:e12 @ 5.70, B:e17 @ 5.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 31406.82, B 31406.82 |
| g29 | 0.00 | CRITICAL_TTC_END | A | B | A:e13 @ 5.70 |  |
| g30 | 0.00 | CLOSING_END | A | B | A:e14 @ 5.70 |  |
| g31 | 0.05 | BRAKE_START | A | - | A:e15 @ 5.75 |  |
| g32 | 0.15 | MOVING_END | A | - | A:e16 @ 5.85 |  |
| g33 | 0.15 | STOP_START | A | - | A:e17 @ 5.85 |  |
| g34 | 8.05 | TRACK_APPEARED_FRONT | A | A:track_003 | A:e18 @ 13.75 |  |
| g35 | 8.40 | TRACK_LOST | A | A:track_003 | A:e19 @ 14.10 |  |
| g36 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g37 | - | TRACK_APPEARED_REAR | C | C:track_001 | C:e02 @ 0.00 |  |
| g38 | - | TRACK_APPEARED_REAR | C | C:track_002 | C:e03 @ 0.00 |  |
| g39 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.80 |  |
| g40 | - | CLOSING_START | C | C:track_002 | C:e05 @ 1.05 |  |
| g41 | - | CLOSING_END | C | C:track_001 | C:e06 @ 2.00 |  |
| g42 | - | CLOSING_END | C | C:track_002 | C:e07 @ 2.10 |  |
| g43 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e08 @ 2.40 |  |
| g44 | - | TRACK_LOST | C | C:track_001 | C:e09 @ 2.50 |  |
| g45 | - | TRACK_LOST | C | C:track_002 | C:e10 @ 2.85 |  |
| g46 | - | BRAKE_START | C | - | C:e11 @ 2.95 |  |
| g47 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e12 @ 3.10 |  |
| g48 | - | MOVING_END | C | - | C:e13 @ 4.05 |  |
| g49 | - | STOP_START | C | - | C:e14 @ 4.05 |  |
| g50 | - | BRAKE_END | C | - | C:e15 @ 12.95 |  |
| g51 | - | STOP_END | C | - | C:e16 @ 13.75 |  |
| g52 | - | MOVING_START | C | - | C:e17 @ 13.75 |  |

## Edges

```
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g03 --SAME_TRACK--> g06
    g08 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g16
    g08 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g19
    g03 --SAME_TRACK--> g23
    g03 --SAME_TRACK--> g29
    g03 --SAME_TRACK--> g30
    g34 --SAME_TRACK--> g35
    g05 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g14
    g04 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g20
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g27
    g37 --SAME_TRACK--> g39
    g38 --SAME_TRACK--> g40
    g37 --SAME_TRACK--> g41
    g38 --SAME_TRACK--> g42
    g37 --SAME_TRACK--> g44
    g38 --SAME_TRACK--> g45
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.70 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001); TRACK_APPEARED_REAR(B,A) |
| -5.25 | CLOSING_START(A,B) |
| -5.20 | CLOSING_START(B,A) |
| -4.65 | TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002) |
| -4.60 | CLOSING_START(B,B:track_001) |
| -4.05 | CLOSING_END(A,B); CLOSING_END(B,A) |
| -3.70 | CLOSING_END(A,A:track_002) |
| -3.60 | CLOSING_END(B,B:track_001) |
| -2.50 | CLOSING_START(B,B:track_001) |
| -2.45 | CLOSING_START(A,A:track_002) |
| -2.15 | TRACK_LOST(A,A:track_002) |
| -2.05 | BRAKE_START(B) |
| -1.80 | CLOSING_START(A,B); CLOSING_START(B,A) |
| -1.75 | CRITICAL_TTC_START(B,B:track_001) |
| -1.10 | CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B) |
| -0.85 | CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| -0.05 | TRACK_LOST(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | BRAKE_START(A) |
| +0.15 | MOVING_END(A); STOP_START(A) |
| +8.05 | TRACK_APPEARED_FRONT(A,A:track_003) |
| +8.40 | TRACK_LOST(A,A:track_003) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.60, COLLISION with B 5.70 (+1.10 s) [local times; t_global: critical_ttc_start -1.10, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.95, COLLISION 5.70 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.70 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: not yet observed |
| -5.70 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02)<br>g05 TRACK_APPEARED_REAR(B,A) (B:e03) | ego: not yet observed |
| -5.25 | A | g06 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -5.20 | B | g07 CLOSING_START(B,A) (B:e04) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -4.65 | A | g08 TRACK_APPEARED_FRONT(A,A:track_002) (A:e04)<br>g09 CLOSING_START(A,A:track_002) (A:e05) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -4.60 | B | g10 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -4.05 | A | g11 CLOSING_END(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -4.05 | B | g12 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING |
| -3.70 | A | g13 CLOSING_END(A,A:track_002) (A:e07) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -3.60 | B | g14 CLOSING_END(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -2.50 | B | g15 CLOSING_START(B,B:track_001) (B:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -2.45 | A | g16 CLOSING_START(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH |
| -2.15 | A | g17 TRACK_LOST(A,A:track_002) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -2.05 | B | g18 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -1.80 | A | g19 CLOSING_START(A,B) (A:e10) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| -1.80 | B | g20 CLOSING_START(B,A) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -1.75 | B | g21 CRITICAL_TTC_START(B,B:track_001) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING |
| -1.10 | B | g22 CRITICAL_TTC_END(B,B:track_001) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| -1.10 | A | g23 CRITICAL_TTC_START(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| -0.85 | B | g24 CLOSING_END(B,B:track_001) (B:e13)<br>g25 MOVING_END(B) (B:e14)<br>g26 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING |
| -0.05 | B | g27 TRACK_LOST(B,A) (B:e16) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| +0.00 | A | g28 COLLISION(A,B) (A:e12)<br>g29 CRITICAL_TTC_END(A,B) (A:e13)<br>g30 CLOSING_END(A,B) (A:e14) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g28 COLLISION(A,B) (B:e17) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | A | g31 BRAKE_START(A) (A:e15) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.15 | A | g32 MOVING_END(A) (A:e16)<br>g33 STOP_START(A) (A:e17) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +8.05 | A | g34 TRACK_APPEARED_FRONT(A,A:track_003) (A:e18) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +8.40 | A | g35 TRACK_LOST(A,A:track_003) (A:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002 |
| - | C | g36 MOVING_START(C) (C:e01)<br>g37 TRACK_APPEARED_REAR(C,C:track_001) (C:e02)<br>g38 TRACK_APPEARED_REAR(C,C:track_002) (C:e03) | ego: not yet observed |
| - | C | g39 CLOSING_START(C,C:track_001) (C:e04) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| - | C | g40 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state |
| - | C | g41 CLOSING_END(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g42 CLOSING_END(C,C:track_002) (C:e07) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| - | C | g43 SPEED_LIMIT_EXCEEDED_START(C) (C:e08) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| - | C | g44 TRACK_LOST(C,C:track_001) (C:e09) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: no active state<br>track_002: no active state |
| - | C | g45 TRACK_LOST(C,C:track_002) (C:e10) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| - | C | g46 BRAKE_START(C) (C:e11) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001, track_002 |
| - | C | g47 SPEED_LIMIT_EXCEEDED_END(C) (C:e12) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001, track_002 |
| - | C | g48 MOVING_END(C) (C:e13)<br>g49 STOP_START(C) (C:e14) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 |
| - | C | g50 BRAKE_END(C) (C:e15) | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 |
| - | C | g51 STOP_END(C) (C:e16)<br>g52 MOVING_START(C) (C:e17) | ego: STOP<br>track lost, states UNKNOWN: track_001, track_002 |

## Plain-language reading

- 5.70 s before the reference collision, A started moving (already the case when first observed).
- 5.70 s before the reference collision, B started moving (already the case when first observed).
- 5.70 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.70 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.70 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 5.25 s before the reference collision, A observed B start closing in.
- 5.20 s before the reference collision, B observed A start closing in.
- 4.65 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 4.65 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.60 s before the reference collision, B observed unidentified object B:track_001 start closing in.
- 4.05 s before the reference collision, A observed B stop closing in.
- 4.05 s before the reference collision, B observed A stop closing in.
- 3.70 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 3.60 s before the reference collision, B observed unidentified object B:track_001 stop closing in.
- 2.50 s before the reference collision, B observed unidentified object B:track_001 start closing in.
- 2.45 s before the reference collision, A observed unidentified object A:track_002 start closing in.
- 2.15 s before the reference collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 2.05 s before the reference collision, B started braking.
- 1.80 s before the reference collision, A observed B start closing in.
- 1.80 s before the reference collision, B observed A start closing in.
- 1.75 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.10 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.10 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, B observed unidentified object B:track_001 stop closing in.
- 0.85 s before the reference collision, B stopped moving.
- 0.85 s before the reference collision, B came to a stop.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 31407, B: 31407 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.15 s after the reference collision, A stopped moving.
- 0.15 s after the reference collision, A came to a stop.
- 8.05 s after the reference collision, A's radar started tracking unidentified object A:track_003, which appeared in front of it.
- 8.40 s after the reference collision, A's radar lost unidentified object A:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared behind it.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002, which appeared behind it.
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_001 start closing in.
- (unaligned, C local time 1.05 s) C observed unidentified object C:track_002 start closing in.
- (unaligned, C local time 2.00 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 2.10 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.50 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 2.85 s) C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 3.10 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 12.95 s) C released the brake.
- (unaligned, C local time 13.75 s) C left its stop.
- (unaligned, C local time 13.75 s) C started moving.
