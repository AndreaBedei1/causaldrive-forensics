# Global graph - S07/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 22183.35 vs 22183.35 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 22183.35 vs 22183.35 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 22183.35 vs 22183.35 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.2 m -> 14.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.87 m/s over 3.0 s (> 1.50)<br>clearance at the contact 14.08 m (beyond 3.50 m: confidence factor 0.00) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.90 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -5.90 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -5.90 | TRACK_APPEARED_FRONT | A | B | A:e03 @ 0.00 |  |
| g06 | -5.90 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e03 @ 0.00 |  |
| g07 | -5.40 | CRITICAL_TTC_START | A | B | A:e04 @ 0.50 |  |
| g08 | -2.70 | CLOSING_START | B | B:track_001 | B:e04 @ 3.20 |  |
| g09 | -2.50 | CRITICAL_TTC_START | B | B:track_001 | B:e05 @ 3.40 |  |
| g10 | -2.25 | THROTTLE_END | B | - | B:e06 @ 3.65 |  |
| g11 | -2.25 | BRAKE_START | B | - | B:e07 @ 3.65 |  |
| g12 | -2.05 | CLOSING_START | A | B | A:e05 @ 3.85 |  |
| g13 | -1.55 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 4.35 |  |
| g14 | -1.05 | CLOSING_END | B | B:track_001 | B:e09 @ 4.85 |  |
| g15 | -1.05 | MOVING_END | B | - | B:e10 @ 4.85 |  |
| g16 | -1.05 | STOP_START | B | - | B:e11 @ 4.85 |  |
| g17 | -0.65 | THROTTLE_END | A | - | A:e06 @ 5.25 |  |
| g18 | -0.65 | BRAKE_START | A | - | A:e07 @ 5.25 |  |
| g19 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.90, B:e12 @ 5.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 22183.35, B 22183.35 |
| g20 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 5.90 |  |
| g21 | 0.00 | CLOSING_END | A | B | A:e10 @ 5.90 |  |
| g22 | 0.10 | MOVING_END | A | - | A:e11 @ 6.00 |  |
| g23 | 0.10 | STOP_START | A | - | A:e12 @ 6.00 |  |
| g24 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g25 | - | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g26 | - | THROTTLE_END | C | - | C:e03 @ 2.95 |  |
| g27 | - | BRAKE_START | C | - | C:e04 @ 2.95 |  |
| g28 | - | MOVING_END | C | - | C:e05 @ 4.35 |  |
| g29 | - | STOP_START | C | - | C:e06 @ 4.35 |  |

## Edges

```
    g01 --PRECEDES--> g07
    g02 --PRECEDES--> g07
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g05 --SAME_TRACK--> g07
    g05 --SAME_TRACK--> g12
    g05 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g21
    g06 --SAME_TRACK--> g08
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.90 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001) |
| -5.40 | CRITICAL_TTC_START(A,B) |
| -2.70 | CLOSING_START(B,B:track_001) |
| -2.50 | CRITICAL_TTC_START(B,B:track_001) |
| -2.25 | THROTTLE_END(B); BRAKE_START(B) |
| -2.05 | CLOSING_START(A,B) |
| -1.55 | CRITICAL_TTC_END(B,B:track_001) |
| -1.05 | CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| -0.65 | THROTTLE_END(A); BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.10 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 0.50, COLLISION with B 5.90 (+5.40 s) [local times; t_global: critical_ttc_start -5.40, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.40, COLLISION 5.90 (+2.50 s) [local times; t_global: critical_ttc_start -2.50, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.90 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,B) (A:e03) | ego: not yet observed |
| -5.90 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,B:track_001) (B:e03) | ego: not yet observed |
| -5.40 | A | g07 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC? |
| -2.70 | B | g08 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH |
| -2.50 | B | g09 CRITICAL_TTC_START(B,B:track_001) (B:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH |
| -2.25 | B | g10 THROTTLE_END(B) (B:e06)<br>g11 BRAKE_START(B) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -2.05 | A | g12 CLOSING_START(A,B) (A:e05) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH |
| -1.55 | B | g13 CRITICAL_TTC_END(B,B:track_001) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.05 | B | g14 CLOSING_END(B,B:track_001) (B:e09)<br>g15 MOVING_END(B) (B:e10)<br>g16 STOP_START(B) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| -0.65 | A | g17 THROTTLE_END(A) (A:e06)<br>g18 BRAKE_START(A) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g19 COLLISION(A,B) (A:e08)<br>g20 CRITICAL_TTC_END(A,B) (A:e09)<br>g21 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g19 COLLISION(A,B) (B:e12) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.10 | A | g22 MOVING_END(A) (A:e11)<br>g23 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| - | C | g24 MOVING_START(C) (C:e01)<br>g25 THROTTLE_START(C) (C:e02) | ego: not yet observed |
| - | C | g26 THROTTLE_END(C) (C:e03)<br>g27 BRAKE_START(C) (C:e04) | ego: MOVING, THROTTLE |
| - | C | g28 MOVING_END(C) (C:e05)<br>g29 STOP_START(C) (C:e06) | ego: MOVING, BRAKE |

## Plain-language reading

- 5.90 s before the reference collision, A started moving (already the case when first observed).
- 5.90 s before the reference collision, B started moving (already the case when first observed).
- 5.90 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.90 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.90 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.40 s before the reference collision, A's time-to-contact with B became critical.
- 2.70 s before the reference collision, B observed unidentified object B:track_001 start closing in.
- 2.50 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 2.25 s before the reference collision, B released the accelerator.
- 2.25 s before the reference collision, B started braking.
- 2.05 s before the reference collision, A observed B start closing in.
- 1.55 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.05 s before the reference collision, B observed unidentified object B:track_001 stop closing in.
- 1.05 s before the reference collision, B stopped moving.
- 1.05 s before the reference collision, B came to a stop.
- 0.65 s before the reference collision, A released the accelerator.
- 0.65 s before the reference collision, A started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 22183, B: 22183 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.10 s after the reference collision, A stopped moving.
- 0.10 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C pressed the accelerator (already the case when first observed).
- (unaligned, C local time 2.95 s) C released the accelerator.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 4.35 s) C stopped moving.
- (unaligned, C local time 4.35 s) C came to a stop.
