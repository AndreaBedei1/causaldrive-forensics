# Global graph - S09/run_0_merge_conflict

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| B:track_002 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 1.80 | -1.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 1.80 | -1.80 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1247.19 vs 1247.19 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.63 | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.01 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 1.45 m/s over 1.8 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 36.18 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 6.69 m/s (> 1.50) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 38.37 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 6.74 m/s (> 1.50) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>at the contact: minimum range 2.22 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed disagrees with A's own speed: RMSE 4.97 m/s (> 1.50) |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 14.50 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with A's own speed: RMSE 6.98 m/s (> 1.50) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -1.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -1.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -1.80 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 0.00 |  |
| g04 | -1.80 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -1.80 | CRITICAL_TTC_START | A | B | A:e04 @ 0.00 | active_at_first_observation=True |
| g06 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_002 | A:e05 @ 0.20 |  |
| g07 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_003 | A:e06 @ 0.20 |  |
| g08 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 0.20 |  |
| g09 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e03 @ 0.20 |  |
| g10 | -1.60 | CLOSING_START | A | A:track_002 | A:e07 @ 0.20 | active_at_first_observation=True |
| g11 | -1.60 | CLOSING_START | A | A:track_003 | A:e08 @ 0.20 | active_at_first_observation=True |
| g12 | -1.60 | CLOSING_START | B | B:track_001 | B:e04 @ 0.20 | active_at_first_observation=True |
| g13 | -1.60 | CLOSING_START | B | B:track_002 | B:e05 @ 0.20 | active_at_first_observation=True |
| g14 | -1.60 | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 0.20 | active_at_first_observation=True |
| g15 | -1.00 | STRONG_THROTTLE_START | B | - | B:e07 @ 0.80 |  |
| g16 | -0.35 | EGO_PATH_ENTRY | A | B | A:e09 @ 1.45 |  |
| g17 | -0.20 | STRONG_THROTTLE_END | B | - | B:e08 @ 1.60 |  |
| g18 | -0.15 | TRACK_LOST | B | B:track_001 | B:e09 @ 1.65 |  |
| g19 | 0.00 | COLLISION | - | A, B | A:e10 @ 1.80, B:e10 @ 1.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 1247.19, B 1247.19 |
| g20 | 0.05 | BRAKE_START | A | - | A:e11 @ 1.85 |  |
| g21 | 0.05 | BRAKE_START | B | - | B:e11 @ 1.85 |  |
| g22 | 0.05 | HARD_BRAKE_START | A | - | A:e12 @ 1.85 |  |
| g23 | 0.05 | HARD_BRAKE_START | B | - | B:e12 @ 1.85 |  |
| g24 | 0.10 | CRITICAL_TTC_END | A | B | A:e13 @ 1.90 |  |
| g25 | 0.10 | CLOSING_END | A | B | A:e14 @ 1.90 |  |
| g26 | 0.10 | TRACK_LOST | B | B:track_002 | B:e13 @ 1.90 |  |
| g27 | 0.70 | CLOSING_END | A | A:track_002 | A:e15 @ 2.50 |  |
| g28 | 0.70 | CLOSING_END | A | A:track_003 | A:e16 @ 2.50 |  |
| g29 | 0.70 | MOVING_END | A | - | A:e17 @ 2.50 |  |
| g30 | 0.70 | STOP_START | A | - | A:e18 @ 2.50 |  |
| g31 | 0.75 | MOVING_END | B | - | B:e14 @ 2.55 |  |
| g32 | 0.75 | STOP_START | B | - | B:e15 @ 2.55 |  |

## Edges

```
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g01 --PRECEDES--> g08
    g01 --PRECEDES--> g09
    g01 --PRECEDES--> g10
    g01 --PRECEDES--> g11
    g01 --PRECEDES--> g12
    g01 --PRECEDES--> g13
    g01 --PRECEDES--> g14
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g02 --PRECEDES--> g08
    g02 --PRECEDES--> g09
    g02 --PRECEDES--> g10
    g02 --PRECEDES--> g11
    g02 --PRECEDES--> g12
    g02 --PRECEDES--> g13
    g02 --PRECEDES--> g14
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g03 --PRECEDES--> g09
    g03 --PRECEDES--> g10
    g03 --PRECEDES--> g11
    g03 --PRECEDES--> g12
    g03 --PRECEDES--> g13
    g03 --PRECEDES--> g14
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g04 --PRECEDES--> g09
    g04 --PRECEDES--> g10
    g04 --PRECEDES--> g11
    g04 --PRECEDES--> g12
    g04 --PRECEDES--> g13
    g04 --PRECEDES--> g14
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g05 --PRECEDES--> g09
    g05 --PRECEDES--> g10
    g05 --PRECEDES--> g11
    g05 --PRECEDES--> g12
    g05 --PRECEDES--> g13
    g05 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g07 --PRECEDES--> g15
    g08 --PRECEDES--> g15
    g09 --PRECEDES--> g15
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g06 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g16
    g03 --SAME_TRACK--> g24
    g03 --SAME_TRACK--> g25
    g06 --SAME_TRACK--> g27
    g07 --SAME_TRACK--> g28
    g08 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g14
    g08 --SAME_TRACK--> g18
    g09 --SAME_TRACK--> g26
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -1.80 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B) |
| -1.60 | TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001) |
| -1.00 | STRONG_THROTTLE_START(B) |
| -0.35 | EGO_PATH_ENTRY(A,B) |
| -0.20 | STRONG_THROTTLE_END(B) |
| -0.15 | TRACK_LOST(B,B:track_001) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.10 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TRACK_LOST(B,B:track_002) |
| +0.70 | CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003); MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -1.80 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03)<br>g05 CRITICAL_TTC_START(A,B) (A:e04) | ego: not yet observed |
| -1.80 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -1.60 | A | g06 TRACK_APPEARED_LEFT(A,A:track_002) (A:e05)<br>g07 TRACK_APPEARED_LEFT(A,A:track_003) (A:e06)<br>g10 CLOSING_START(A,A:track_002) (A:e07)<br>g11 CLOSING_START(A,A:track_003) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -1.60 | B | g08 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g09 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e03)<br>g12 CLOSING_START(B,B:track_001) (B:e04)<br>g13 CLOSING_START(B,B:track_002) (B:e05)<br>g14 CRITICAL_TTC_START(B,B:track_001) (B:e06) | ego: MOVING |
| -1.00 | B | g15 STRONG_THROTTLE_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -0.35 | A | g16 EGO_PATH_ENTRY(A,B) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.20 | B | g17 STRONG_THROTTLE_END(B) (B:e08) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -0.15 | B | g18 TRACK_LOST(B,B:track_001) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +0.00 | A | g19 COLLISION(A,B) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.00 | B | g19 COLLISION(A,B) (B:e10) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g20 BRAKE_START(A) (A:e11)<br>g22 HARD_BRAKE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.05 | B | g21 BRAKE_START(B) (B:e11)<br>g23 HARD_BRAKE_START(B) (B:e12) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.10 | A | g24 CRITICAL_TTC_END(A,B) (A:e13)<br>g25 CLOSING_END(A,B) (A:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.10 | B | g26 TRACK_LOST(B,B:track_002) (B:e13) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.70 | A | g27 CLOSING_END(A,A:track_002) (A:e15)<br>g28 CLOSING_END(A,A:track_003) (A:e16)<br>g29 MOVING_END(A) (A:e17)<br>g30 STOP_START(A) (A:e18) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.75 | B | g31 MOVING_END(B) (B:e14)<br>g32 STOP_START(B) (B:e15) | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001, track_002 |

## Plain-language reading

- 1.80 s before the matched collision, A started moving (already the case when first observed).
- 1.80 s before the matched collision, B started moving (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_003, which appeared on its left.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 1.60 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical (already the case when first observed).
- 1.00 s before the matched collision, B started applying strong throttle.
- 0.35 s before the matched collision, A observed B enter its forward path corridor.
- 0.20 s before the matched collision, B stopped applying strong throttle.
- 0.15 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 1247, B: 1247 N*s).
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.10 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.10 s after the matched collision, A observed B stop closing in.
- 0.10 s after the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.70 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.70 s after the matched collision, A stopped moving.
- 0.70 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.
