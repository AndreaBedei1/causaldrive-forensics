# Global graph - S02/run_0_critical_before_cut_in

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 3.85 | -3.85 | reported the reference collision collision_001 |
| B | ALIGNED | B:e04 | 3.85 | -3.85 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 241.17 vs 241.17 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.67 | A and B both reported collision_001 (peak impulse 241.17 vs 241.17 N*s)<br>tracked for 3.85 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 0.50 s)<br>approaching before the contact: range 3.3 m -> 0.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.34 m/s over 2.9 s<br>range at the contact 0.92 m<br>the only track of A compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.85 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.85 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.85 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -3.85 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -3.10 | CRITICAL_TTC_START | A | B | A:e04 @ 0.75 |  |
| g06 | -2.60 | CRITICAL_TTC_END | A | B | A:e05 @ 1.25 |  |
| g07 | -2.45 | BRAKE_START | B | - | B:e02 @ 1.40 |  |
| g08 | -2.30 | BRAKE_END | B | - | B:e03 @ 1.55 |  |
| g09 | -2.30 | CRITICAL_TTC_START | A | B | A:e06 @ 1.55 |  |
| g10 | -1.40 | BRAKE_START | A | - | A:e07 @ 2.45 |  |
| g11 | -1.15 | CUT_IN_FROM_LEFT_START | A | B | A:e08 @ 2.70 |  |
| g12 | -0.65 | BRAKE_END | A | - | A:e09 @ 3.20 |  |
| g13 | -0.45 | EGO_PATH_ENTRY | A | B | A:e10 @ 3.40 |  |
| g14 | -0.15 | TRACK_LOST | A | B | A:e11 @ 3.70 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e12 @ 3.85, B:e04 @ 3.85 | matched_event=collision_001; reference_event=True; peak_impulse=A 241.17, B 241.17 |
| g16 | 0.05 | BRAKE_START | A | - | A:e13 @ 3.90 |  |
| g17 | 0.05 | BRAKE_START | B | - | B:e05 @ 3.90 |  |
| g18 | 0.50 | MOVING_END | B | - | B:e06 @ 4.35 |  |
| g19 | 0.50 | STOP_START | B | - | B:e07 @ 4.35 |  |
| g20 | 0.60 | MOVING_END | A | - | A:e14 @ 4.45 |  |
| g21 | 0.60 | STOP_START | A | - | A:e15 @ 4.45 |  |

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
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
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
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.85 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -3.10 | CRITICAL_TTC_START(A,B) |
| -2.60 | CRITICAL_TTC_END(A,B) |
| -2.45 | BRAKE_START(B) |
| -2.30 | BRAKE_END(B); CRITICAL_TTC_START(A,B) |
| -1.40 | BRAKE_START(A) |
| -1.15 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.65 | BRAKE_END(A) |
| -0.45 | EGO_PATH_ENTRY(A,B) |
| -0.15 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B) |
| +0.50 | MOVING_END(B); STOP_START(B) |
| +0.60 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 1.55 <= CUT_IN_FROM_LEFT_START 2.70 (+1.15 s); EGO_PATH_ENTRY 3.40 after critical TTC (+1.85 s) [local times; t_global: cut_in -1.15, critical_ttc_start -2.30, ego_path_entry -0.45, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.85 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -3.85 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.10 | A | g05 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.60 | A | g06 CRITICAL_TTC_END(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -2.45 | B | g07 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.30 | B | g08 BRAKE_END(B) (B:e03) | ego: MOVING, BRAKE |
| -2.30 | A | g09 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.40 | A | g10 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -1.15 | A | g11 CUT_IN_FROM_LEFT_START(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.65 | A | g12 BRAKE_END(A) (A:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.45 | A | g13 EGO_PATH_ENTRY(A,B) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.15 | A | g14 TRACK_LOST(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g15 COLLISION(A,B) (A:e12) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g15 COLLISION(A,B) (B:e04) | ego: MOVING |
| +0.05 | A | g16 BRAKE_START(A) (A:e13) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | B | g17 BRAKE_START(B) (B:e05) | ego: MOVING |
| +0.50 | B | g18 MOVING_END(B) (B:e06)<br>g19 STOP_START(B) (B:e07) | ego: MOVING, BRAKE |
| +0.60 | A | g20 MOVING_END(A) (A:e14)<br>g21 STOP_START(A) (A:e15) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 3.85 s before the reference collision, A started moving (already the case when first observed).
- 3.85 s before the reference collision, B started moving (already the case when first observed).
- 3.85 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 3.85 s before the reference collision, A observed B start closing in (already the case when first observed).
- 3.10 s before the reference collision, A's time-to-contact with B became critical.
- 2.60 s before the reference collision, A's time-to-contact with B stopped being critical.
- 2.45 s before the reference collision, B started braking.
- 2.30 s before the reference collision, B released the brake.
- 2.30 s before the reference collision, A's time-to-contact with B became critical.
- 1.40 s before the reference collision, A started braking.
- 1.15 s before the reference collision, A observed B cutting in from the left.
- 0.65 s before the reference collision, A released the brake.
- 0.45 s before the reference collision, A observed B enter its forward path corridor.
- 0.15 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 241, B: 241 N*s).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.60 s after the reference collision, A stopped moving.
- 0.60 s after the reference collision, A came to a stop.
