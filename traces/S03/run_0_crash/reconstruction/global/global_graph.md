# Global graph - S03/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.96 | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 0.50 s)<br>approaching before the contact: range 18.6 m -> 3.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 2.0 s<br>range at the contact 3.78 m (beyond 3.50 m: confidence factor 1.00)<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.75 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.0 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.14 m/s over 2.0 s<br>range at the contact 1.07 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -2.20 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 2.05 |  |
| g04 | -2.20 | CLOSING_START | A | B | A:e03 @ 2.05 | active_at_first_observation=True |
| g05 | -2.05 | TRACK_APPEARED_LEFT | B | A | B:e02 @ 2.20 |  |
| g06 | -2.05 | CLOSING_START | B | A | B:e03 @ 2.20 | active_at_first_observation=True |
| g07 | -1.90 | CRITICAL_TTC_START | B | A | B:e04 @ 2.35 |  |
| g08 | -1.80 | CRITICAL_TTC_START | A | B | A:e04 @ 2.45 |  |
| g09 | -0.15 | TRACK_LOST | A | B | A:e05 @ 4.10 |  |
| g10 | -0.10 | EGO_PATH_ENTRY | B | A | B:e05 @ 4.15 |  |
| g11 | 0.00 | COLLISION | - | A, B | A:e06 @ 4.25, B:e06 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g12 | 0.05 | BRAKE_START | A | - | A:e07 @ 4.30 |  |
| g13 | 0.05 | BRAKE_START | B | - | B:e07 @ 4.30 |  |
| g14 | 0.10 | CRITICAL_TTC_END | B | A | B:e08 @ 4.35 |  |
| g15 | 0.10 | CLOSING_END | B | A | B:e09 @ 4.35 |  |
| g16 | 0.30 | MOVING_END | B | - | B:e10 @ 4.55 |  |
| g17 | 0.30 | STOP_START | B | - | B:e11 @ 4.55 |  |
| g18 | 0.45 | EGO_PATH_EXIT | B | A | B:e12 @ 4.70 |  |
| g19 | 0.65 | MOVING_END | A | - | A:e08 @ 4.90 |  |
| g20 | 0.65 | STOP_START | A | - | A:e09 @ 4.90 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
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
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g07
    g05 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g18
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B) |
| -2.20 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.05 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.90 | CRITICAL_TTC_START(B,A) |
| -1.80 | CRITICAL_TTC_START(A,B) |
| -0.15 | TRACK_LOST(A,B) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.45 | EGO_PATH_EXIT(B,A) |
| +0.65 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 2.45, COLLISION 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.35, COLLISION 4.25 (+1.90 s); EGO_PATH_ENTRY 4.15 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -1.90, ego_path_entry -0.10, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.20 | A | g03 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.05 | B | g05 TRACK_APPEARED_LEFT(B,A) (B:e02)<br>g06 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -1.90 | B | g07 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.80 | A | g08 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -0.15 | A | g09 TRACK_LOST(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.10 | B | g10 EGO_PATH_ENTRY(B,A) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g11 COLLISION(A,B) (A:e06) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g11 COLLISION(A,B) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g12 BRAKE_START(A) (A:e07) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | B | g13 BRAKE_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.10 | B | g14 CRITICAL_TTC_END(B,A) (B:e08)<br>g15 CLOSING_END(B,A) (B:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.30 | B | g16 MOVING_END(B) (B:e10)<br>g17 STOP_START(B) (B:e11) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.45 | B | g18 EGO_PATH_EXIT(B,A) (B:e12) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.65 | A | g19 MOVING_END(A) (A:e08)<br>g20 STOP_START(A) (A:e09) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 2.20 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 2.20 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.05 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 2.05 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.90 s before the matched collision, B's time-to-contact with A became critical.
- 1.80 s before the matched collision, A's time-to-contact with B became critical.
- 0.15 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.10 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.10 s after the matched collision, B observed A stop closing in.
- 0.30 s after the matched collision, B stopped moving.
- 0.30 s after the matched collision, B came to a stop.
- 0.45 s after the matched collision, B observed A leave its forward path corridor.
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.
