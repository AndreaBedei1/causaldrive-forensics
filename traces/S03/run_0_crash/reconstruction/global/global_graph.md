# Global graph - S03/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.10 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.15 |  |
| g04 | -2.20 | TRACK_APPEARED | A | A:track_001 | A:e02 @ 2.05 |  |
| g05 | -2.20 | CLOSING_START | A | A:track_001 | A:e03 @ 2.05 | active_at_first_observation=True |
| g06 | -2.10 | TRACK_APPEARED | B | A | B:e03 @ 2.15 |  |
| g07 | -2.10 | CLOSING_START | B | A | B:e04 @ 2.15 | active_at_first_observation=True |
| g08 | -1.90 | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 2.35 |  |
| g09 | -1.90 | CRITICAL_TTC_START | B | A | B:e05 @ 2.35 |  |
| g10 | -1.85 | STRONG_THROTTLE_END | B | - | B:e06 @ 2.40 |  |
| g11 | -1.70 | PREDICTED_PATH_CONFLICT_START | A | A:track_001 | A:e05 @ 2.55 |  |
| g12 | -1.40 | PREDICTED_PATH_CONFLICT_START | B | A | B:e07 @ 2.85 |  |
| g13 | -0.90 | TRACK_LOST | A | A:track_001 | A:e06 @ 3.35 |  |
| g14 | -0.15 | EGO_PATH_ENTRY | B | A | B:e08 @ 4.10 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e07 @ 4.25, B:e09 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g16 | 0.00 | STRONG_THROTTLE_START | B | - | B:e10 @ 4.25 |  |
| g17 | 0.05 | PREDICTED_PATH_CONFLICT_END | B | A | B:e11 @ 4.30 |  |
| g18 | 0.05 | CRITICAL_TTC_END | B | A | B:e12 @ 4.30 |  |
| g19 | 0.05 | CLOSING_END | B | A | B:e13 @ 4.30 |  |
| g20 | 0.05 | STRONG_THROTTLE_END | B | - | B:e14 @ 4.30 |  |
| g21 | 0.05 | BRAKE_START | A | - | A:e08 @ 4.30 |  |
| g22 | 0.05 | BRAKE_START | B | - | B:e15 @ 4.30 |  |
| g23 | 0.05 | HARD_BRAKE_START | A | - | A:e09 @ 4.30 |  |
| g24 | 0.05 | HARD_BRAKE_START | B | - | B:e16 @ 4.30 |  |
| g25 | 0.30 | MOVING_END | B | - | B:e17 @ 4.55 |  |
| g26 | 0.30 | STOP_START | B | - | B:e18 @ 4.55 |  |
| g27 | 0.45 | EGO_PATH_EXIT | B | A | B:e19 @ 4.70 |  |
| g28 | 0.65 | MOVING_END | A | - | A:e10 @ 4.90 |  |
| g29 | 0.65 | STOP_START | A | - | A:e11 @ 4.90 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g15 --PRECEDES--> g22
    g15 --PRECEDES--> g23
    g15 --PRECEDES--> g24
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g16 --PRECEDES--> g22
    g16 --PRECEDES--> g23
    g16 --PRECEDES--> g24
    g17 --PRECEDES--> g25
    g17 --PRECEDES--> g26
    g18 --PRECEDES--> g25
    g18 --PRECEDES--> g26
    g19 --PRECEDES--> g25
    g19 --PRECEDES--> g26
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g11
    g04 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g14
    g06 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g19
    g06 --SAME_TRACK--> g27
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B) |
| -3.10 | STRONG_THROTTLE_START(B) |
| -2.20 | TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.10 | TRACK_APPEARED(B,A); CLOSING_START(B,A) |
| -1.90 | CRITICAL_TTC_START(A,A:track_001); CRITICAL_TTC_START(B,A) |
| -1.85 | STRONG_THROTTLE_END(B) |
| -1.70 | PREDICTED_PATH_CONFLICT_START(A,A:track_001) |
| -1.40 | PREDICTED_PATH_CONFLICT_START(B,A) |
| -0.90 | TRACK_LOST(A,A:track_001) |
| -0.15 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(B) |
| +0.05 | PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.45 | EGO_PATH_EXIT(B,A) |
| +0.65 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.10 | B | g03 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -2.20 | A | g04 TRACK_APPEARED(A,A:track_001) (A:e02)<br>g05 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -2.10 | B | g06 TRACK_APPEARED(B,A) (B:e03)<br>g07 CLOSING_START(B,A) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| -1.90 | A | g08 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| -1.90 | B | g09 CRITICAL_TTC_START(B,A) (B:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING |
| -1.85 | B | g10 STRONG_THROTTLE_END(B) (B:e06) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| -1.70 | A | g11 PREDICTED_PATH_CONFLICT_START(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| -1.40 | B | g12 PREDICTED_PATH_CONFLICT_START(B,A) (B:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| -0.90 | A | g13 TRACK_LOST(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| -0.15 | B | g14 EGO_PATH_ENTRY(B,A) (B:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| +0.00 | A | g15 COLLISION(A,B) (A:e07) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| +0.00 | B | g15 COLLISION(A,B) (B:e09)<br>g16 STRONG_THROTTLE_START(B) (B:e10) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT |
| +0.05 | B | g17 PREDICTED_PATH_CONFLICT_END(B,A) (B:e11)<br>g18 CRITICAL_TTC_END(B,A) (B:e12)<br>g19 CLOSING_END(B,A) (B:e13)<br>g20 STRONG_THROTTLE_END(B) (B:e14)<br>g22 BRAKE_START(B) (B:e15)<br>g24 HARD_BRAKE_START(B) (B:e16) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT |
| +0.05 | A | g21 BRAKE_START(A) (A:e08)<br>g23 HARD_BRAKE_START(A) (A:e09) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| +0.30 | B | g25 MOVING_END(B) (B:e17)<br>g26 STOP_START(B) (B:e18) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.45 | B | g27 EGO_PATH_EXIT(B,A) (B:e19) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.65 | A | g28 MOVING_END(A) (A:e10)<br>g29 STOP_START(A) (A:e11) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 3.10 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 2.20 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.10 s before the matched collision, B's radar started tracking A.
- 2.10 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.90 s before the matched collision, B's time-to-contact with A became critical.
- 1.85 s before the matched collision, B stopped applying strong throttle.
- 1.70 s before the matched collision, A predicted a path conflict with unidentified object A:track_001 (close approach ahead if both keep their motion).
- 1.40 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 0.90 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, B stopped predicting a path conflict with A.
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.30 s after the matched collision, B stopped moving.
- 0.30 s after the matched collision, B came to a stop.
- 0.45 s after the matched collision, B observed A leave its forward path corridor.
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.
