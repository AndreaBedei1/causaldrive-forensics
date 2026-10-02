# Global graph - S13/run_0_accelerates_into_gap

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.65 | -5.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e05 | 5.65 | -5.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5215.85 vs 5215.85 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 2.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.3 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.40 m/s over 2.3 s<br>clearance at the contact 0.33 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 2.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.5 m -> 0.8 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 2.9 s<br>clearance at the contact 0.78 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.65 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.65 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.85 | BRAKE_START | B | - | B:e02 @ 0.80 |  |
| g04 | -2.90 | SPEED_LIMIT_EXCEEDED_START | A | - | A:e02 @ 2.75 |  |
| g05 | -2.90 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 2.75 |  |
| g06 | -2.90 | CLOSING_START | B | A | B:e04 @ 2.75 | active_at_first_observation=True |
| g07 | -2.25 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 3.40 |  |
| g08 | -2.25 | CLOSING_START | A | B | A:e04 @ 3.40 | active_at_first_observation=True |
| g09 | -1.70 | CRITICAL_TTC_START | A | B | A:e05 @ 3.95 |  |
| g10 | -1.50 | CUT_IN_FROM_LEFT_START | A | B | A:e06 @ 4.15 |  |
| g11 | -0.20 | EGO_PATH_ENTRY | A | B | A:e07 @ 5.45 |  |
| g12 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.65, B:e05 @ 5.65 | matched_event=collision_001; reference_event=True; peak_impulse=A 5215.85, B 5215.85 |
| g13 | 0.00 | CLOSING_END | B | A | B:e06 @ 5.65 |  |
| g14 | 0.00 | SPEED_LIMIT_EXCEEDED_END | A | - | A:e09 @ 5.65 |  |
| g15 | 0.05 | BRAKE_START | A | - | A:e10 @ 5.70 |  |
| g16 | 0.10 | TURN_RIGHT_START | B | - | B:e07 @ 5.75 |  |
| g17 | 0.15 | CRITICAL_TTC_END | A | B | A:e11 @ 5.80 |  |
| g18 | 0.15 | CLOSING_END | A | B | A:e12 @ 5.80 |  |
| g19 | 0.90 | CLOSING_START | A | B | A:e13 @ 6.55 |  |
| g20 | 0.90 | CLOSING_START | B | A | B:e08 @ 6.55 |  |
| g21 | 0.90 | CRITICAL_TTC_START | A | B | A:e14 @ 6.55 |  |
| g22 | 0.90 | CRITICAL_TTC_START | B | A | B:e09 @ 6.55 |  |
| g23 | 1.20 | CRITICAL_TTC_END | A | B | A:e15 @ 6.85 |  |
| g24 | 1.20 | CLOSING_END | A | B | A:e16 @ 6.85 |  |
| g25 | 1.25 | CRITICAL_TTC_END | B | A | B:e10 @ 6.90 |  |
| g26 | 1.25 | TURN_RIGHT_END | B | - | B:e11 @ 6.90 |  |
| g27 | 1.25 | MOVING_END | B | - | B:e12 @ 6.90 |  |
| g28 | 1.25 | STOP_START | B | - | B:e13 @ 6.90 |  |
| g29 | 1.30 | CLOSING_END | B | A | B:e14 @ 6.95 |  |
| g30 | 1.30 | MOVING_END | A | - | A:e17 @ 6.95 |  |
| g31 | 1.30 | STOP_START | A | - | A:e18 @ 6.95 |  |
| g32 | 1.40 | CUT_IN_FROM_LEFT_END | A | B | A:e19 @ 7.05 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g09
    g07 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g18
    g07 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g32
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g22
    g05 --SAME_TRACK--> g25
    g05 --SAME_TRACK--> g29
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.65 | MOVING_START(A); MOVING_START(B) |
| -4.85 | BRAKE_START(B) |
| -2.90 | SPEED_LIMIT_EXCEEDED_START(A); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -2.25 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.70 | CRITICAL_TTC_START(A,B) |
| -1.50 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.20 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CLOSING_END(B,A); SPEED_LIMIT_EXCEEDED_END(A) |
| +0.05 | BRAKE_START(A) |
| +0.10 | TURN_RIGHT_START(B) |
| +0.15 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.90 | CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| +1.20 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +1.25 | CRITICAL_TTC_END(B,A); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B) |
| +1.30 | CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |
| +1.40 | CUT_IN_FROM_LEFT_END(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 3.95 <= CUT_IN_FROM_LEFT_START 4.15 (+0.20 s); EGO_PATH_ENTRY 5.45 after critical TTC (+1.50 s) [local times; t_global: cut_in -1.50, critical_ttc_start -1.70, ego_path_entry -0.20, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 6.55 [local times; t_global: critical_ttc_start +0.90]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.65 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.65 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.85 | B | g03 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.90 | A | g04 SPEED_LIMIT_EXCEEDED_START(A) (A:e02) | ego: MOVING |
| -2.90 | B | g05 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g06 CLOSING_START(B,A) (B:e04) | ego: MOVING, BRAKE |
| -2.25 | A | g07 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g08 CLOSING_START(A,B) (A:e04) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| -1.70 | A | g09 CRITICAL_TTC_START(A,B) (A:e05) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING |
| -1.50 | A | g10 CUT_IN_FROM_LEFT_START(A,B) (A:e06) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC |
| -0.20 | A | g11 EGO_PATH_ENTRY(A,B) (A:e07) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | A | g12 COLLISION(A,B) (A:e08)<br>g14 SPEED_LIMIT_EXCEEDED_END(A) (A:e09) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g12 COLLISION(A,B) (B:e05)<br>g13 CLOSING_END(B,A) (B:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| +0.05 | A | g15 BRAKE_START(A) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.10 | B | g16 TURN_RIGHT_START(B) (B:e07) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.15 | A | g17 CRITICAL_TTC_END(A,B) (A:e11)<br>g18 CLOSING_END(A,B) (A:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.90 | A | g19 CLOSING_START(A,B) (A:e13)<br>g21 CRITICAL_TTC_START(A,B) (A:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.90 | B | g20 CLOSING_START(B,A) (B:e08)<br>g22 CRITICAL_TTC_START(B,A) (B:e09) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: no active state |
| +1.20 | A | g23 CRITICAL_TTC_END(A,B) (A:e15)<br>g24 CLOSING_END(A,B) (A:e16) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.25 | B | g25 CRITICAL_TTC_END(B,A) (B:e10)<br>g26 TURN_RIGHT_END(B) (B:e11)<br>g27 MOVING_END(B) (B:e12)<br>g28 STOP_START(B) (B:e13) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC |
| +1.30 | B | g29 CLOSING_END(B,A) (B:e14) | ego: STOP, BRAKE<br>track_001: CLOSING |
| +1.30 | A | g30 MOVING_END(A) (A:e17)<br>g31 STOP_START(A) (A:e18) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.40 | A | g32 CUT_IN_FROM_LEFT_END(A,B) (A:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 5.65 s before the reference collision, A started moving (already the case when first observed).
- 5.65 s before the reference collision, B started moving (already the case when first observed).
- 4.85 s before the reference collision, B started braking.
- 2.90 s before the reference collision, A began exceeding the speed limit.
- 2.90 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 2.90 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.25 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 2.25 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, A observed B cutting in from the left.
- 0.20 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 5216, B: 5216 N*s).
- At the reference collision, B observed A stop closing in.
- At the reference collision, A returned within the speed limit.
- 0.05 s after the reference collision, A started braking.
- 0.10 s after the reference collision, B started turning right.
- 0.15 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.90 s after the reference collision, A observed B start closing in.
- 0.90 s after the reference collision, B observed A start closing in.
- 0.90 s after the reference collision, A's time-to-contact with B became critical.
- 0.90 s after the reference collision, B's time-to-contact with A became critical.
- 1.20 s after the reference collision, A's time-to-contact with B stopped being critical.
- 1.20 s after the reference collision, A observed B stop closing in.
- 1.25 s after the reference collision, B's time-to-contact with A stopped being critical.
- 1.25 s after the reference collision, B stopped turning right.
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, B observed A stop closing in.
- 1.30 s after the reference collision, A stopped moving.
- 1.30 s after the reference collision, A came to a stop.
- 1.40 s after the reference collision, A observed B's cut-in from the left settle.
