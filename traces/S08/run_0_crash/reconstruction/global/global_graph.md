# Global graph - S08/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 4.25 | -4.25 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 4.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 20.2 m -> 10.8 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.79 m/s over 3.0 s (> 1.50)<br>range at the contact 10.85 m (beyond 3.50 m: confidence factor 0.05) |
| A:track_002 | B | ASSOCIATED | 0.96 | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 0.50 s)<br>approaching before the contact: range 18.6 m -> 3.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 2.0 s<br>range at the contact 3.78 m (beyond 3.50 m: confidence factor 1.00)<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 20.4 m -> 12.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.46 m/s over 2.2 s (> 1.50)<br>range at the contact 12.51 m (beyond 3.50 m: confidence factor 0.01) |
| B:track_002 | A | ASSOCIATED | 0.75 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.0 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.14 m/s over 2.0 s<br>range at the contact 1.07 m<br>the only track of B compatible with the contact |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.25 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.00 |  |
| g04 | -4.25 | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -2.20 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 2.05 |  |
| g06 | -2.20 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 2.05 |  |
| g07 | -2.20 | CLOSING_START | A | B | A:e05 @ 2.05 | active_at_first_observation=True |
| g08 | -2.20 | CLOSING_START | B | B:track_001 | B:e03 @ 2.05 | active_at_first_observation=True |
| g09 | -2.10 | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 2.15 |  |
| g10 | -2.05 | TRACK_APPEARED_LEFT | B | A | B:e04 @ 2.20 |  |
| g11 | -2.05 | CLOSING_START | B | A | B:e05 @ 2.20 | active_at_first_observation=True |
| g12 | -1.90 | CRITICAL_TTC_START | B | A | B:e06 @ 2.35 |  |
| g13 | -1.85 | CRITICAL_TTC_START | B | B:track_001 | B:e07 @ 2.40 |  |
| g14 | -1.80 | CRITICAL_TTC_START | A | B | A:e07 @ 2.45 |  |
| g15 | -1.50 | CRITICAL_TTC_END | A | A:track_001 | A:e08 @ 2.75 |  |
| g16 | -0.70 | CRITICAL_TTC_START | A | A:track_001 | A:e09 @ 3.55 |  |
| g17 | -0.15 | TRACK_LOST | A | B | A:e10 @ 4.10 |  |
| g18 | -0.10 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 4.15 |  |
| g19 | -0.10 | EGO_PATH_ENTRY | B | A | B:e09 @ 4.15 |  |
| g20 | 0.00 | COLLISION | - | A, B | A:e11 @ 4.25, B:e10 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g21 | 0.05 | BRAKE_START | A | - | A:e12 @ 4.30 |  |
| g22 | 0.05 | BRAKE_START | B | - | B:e11 @ 4.30 |  |
| g23 | 0.10 | CRITICAL_TTC_END | B | A | B:e12 @ 4.35 |  |
| g24 | 0.10 | CLOSING_END | B | A | B:e13 @ 4.35 |  |
| g25 | 0.30 | MOVING_END | B | - | B:e14 @ 4.55 |  |
| g26 | 0.30 | STOP_START | B | - | B:e15 @ 4.55 |  |
| g27 | 0.35 | CLOSING_END | B | B:track_001 | B:e16 @ 4.60 |  |
| g28 | 0.45 | EGO_PATH_EXIT | B | A | B:e17 @ 4.70 |  |
| g29 | 0.50 | CRITICAL_TTC_END | A | A:track_001 | A:e13 @ 4.75 |  |
| g30 | 0.65 | CLOSING_END | A | A:track_001 | A:e14 @ 4.90 |  |
| g31 | 0.65 | MOVING_END | A | - | A:e15 @ 4.90 |  |
| g32 | 0.65 | STOP_START | A | - | A:e16 @ 4.90 |  |
| g33 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g34 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e02 @ 0.00 |  |
| g35 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.00 | active_at_first_observation=True |
| g36 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e04 @ 2.05 |  |
| g37 | - | CLOSING_START | C | C:track_002 | C:e05 @ 2.05 | active_at_first_observation=True |
| g38 | - | CRITICAL_TTC_START | C | C:track_001 | C:e06 @ 2.25 |  |
| g39 | - | BRAKE_START | C | - | C:e07 @ 2.35 |  |
| g40 | - | MOVING_END | C | - | C:e08 @ 2.85 |  |
| g41 | - | STOP_START | C | - | C:e09 @ 2.85 |  |
| g42 | - | CRITICAL_TTC_START | C | C:track_002 | C:e10 @ 3.55 |  |
| g43 | - | CRITICAL_TTC_END | C | C:track_001 | C:e11 @ 3.85 |  |
| g44 | - | CRITICAL_TTC_END | C | C:track_002 | C:e12 @ 3.85 |  |
| g45 | - | CLOSING_END | C | C:track_002 | C:e13 @ 4.55 |  |
| g46 | - | CLOSING_END | C | C:track_001 | C:e14 @ 4.90 |  |
| g47 | - | BRAKE_END | C | - | C:e15 @ 14.35 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g01 --PRECEDES--> g08
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g02 --PRECEDES--> g08
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g09
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
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
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g03 --SAME_TRACK--> g04
    g05 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g15
    g03 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g29
    g03 --SAME_TRACK--> g30
    g06 --SAME_TRACK--> g08
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g18
    g10 --SAME_TRACK--> g19
    g10 --SAME_TRACK--> g23
    g10 --SAME_TRACK--> g24
    g06 --SAME_TRACK--> g27
    g10 --SAME_TRACK--> g28
    g34 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g37
    g34 --SAME_TRACK--> g38
    g36 --SAME_TRACK--> g42
    g34 --SAME_TRACK--> g43
    g36 --SAME_TRACK--> g44
    g36 --SAME_TRACK--> g45
    g34 --SAME_TRACK--> g46
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.20 | TRACK_APPEARED_RIGHT(A,B); TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(A,B); CLOSING_START(B,B:track_001) |
| -2.10 | CRITICAL_TTC_START(A,A:track_001) |
| -2.05 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.90 | CRITICAL_TTC_START(B,A) |
| -1.85 | CRITICAL_TTC_START(B,B:track_001) |
| -1.80 | CRITICAL_TTC_START(A,B) |
| -1.50 | CRITICAL_TTC_END(A,A:track_001) |
| -0.70 | CRITICAL_TTC_START(A,A:track_001) |
| -0.15 | TRACK_LOST(A,B) |
| -0.10 | CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.35 | CLOSING_END(B,B:track_001) |
| +0.45 | EGO_PATH_EXIT(B,A) |
| +0.50 | CRITICAL_TTC_END(A,A:track_001) |
| +0.65 | CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 2.15, COLLISION 4.25 (+2.10 s) [local times; t_global: critical_ttc_start -2.10, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.45, COLLISION with B 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 2.40, COLLISION 4.25 (+1.85 s) [local times; t_global: critical_ttc_start -1.85, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.35, COLLISION with A 4.25 (+1.90 s); EGO_PATH_ENTRY 4.15 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -1.90, ego_path_entry -0.10, collision +0.00]
- C's track_001 (unidentified C:track_001): CRITICAL_TTC_START 2.25 [local times]
- C's track_002 (unidentified C:track_002): CRITICAL_TTC_START 3.55 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.20 | A | g05 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g07 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.20 | B | g06 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g08 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| -2.10 | A | g09 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -2.05 | B | g10 TRACK_APPEARED_LEFT(B,A) (B:e04)<br>g11 CLOSING_START(B,A) (B:e05) | ego: MOVING<br>track_001: CLOSING |
| -1.90 | B | g12 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.85 | B | g13 CRITICAL_TTC_START(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -1.80 | A | g14 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -1.50 | A | g15 CRITICAL_TTC_END(A,A:track_001) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| -0.70 | A | g16 CRITICAL_TTC_START(A,A:track_001) (A:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.15 | A | g17 TRACK_LOST(A,B) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| -0.10 | B | g18 CRITICAL_TTC_END(B,B:track_001) (B:e08)<br>g19 EGO_PATH_ENTRY(B,A) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | A | g20 COLLISION(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g20 COLLISION(A,B) (B:e10) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g21 BRAKE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.05 | B | g22 BRAKE_START(B) (B:e11) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.10 | B | g23 CRITICAL_TTC_END(B,A) (B:e12)<br>g24 CLOSING_END(B,A) (B:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.30 | B | g25 MOVING_END(B) (B:e14)<br>g26 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH |
| +0.35 | B | g27 CLOSING_END(B,B:track_001) (B:e16) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH |
| +0.45 | B | g28 EGO_PATH_EXIT(B,A) (B:e17) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH |
| +0.50 | A | g29 CRITICAL_TTC_END(A,A:track_001) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.65 | A | g30 CLOSING_END(A,A:track_001) (A:e14)<br>g31 MOVING_END(A) (A:e15)<br>g32 STOP_START(A) (A:e16) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| - | C | g33 MOVING_START(C) (C:e01)<br>g34 TRACK_APPEARED_FRONT(C,C:track_001) (C:e02)<br>g35 CLOSING_START(C,C:track_001) (C:e03) | ego: not yet observed |
| - | C | g36 TRACK_APPEARED_LEFT(C,C:track_002) (C:e04)<br>g37 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| - | C | g38 CRITICAL_TTC_START(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g39 BRAKE_START(C) (C:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g40 MOVING_END(C) (C:e08)<br>g41 STOP_START(C) (C:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g42 CRITICAL_TTC_START(C,C:track_002) (C:e10) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g43 CRITICAL_TTC_END(C,C:track_001) (C:e11)<br>g44 CRITICAL_TTC_END(C,C:track_002) (C:e12) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g45 CLOSING_END(C,C:track_002) (C:e13) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g46 CLOSING_END(C,C:track_001) (C:e14) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| - | C | g47 BRAKE_END(C) (C:e15) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 4.25 s before the reference collision, A started moving (already the case when first observed).
- 4.25 s before the reference collision, B started moving (already the case when first observed).
- 4.25 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 4.25 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.20 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.20 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.20 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.20 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.10 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 2.05 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.05 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.90 s before the reference collision, B's time-to-contact with A became critical.
- 1.85 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.80 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.70 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.15 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.10 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.10 s before the reference collision, B observed A enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.30 s after the reference collision, B stopped moving.
- 0.30 s after the reference collision, B came to a stop.
- 0.35 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
- 0.45 s after the reference collision, B observed A leave its forward path corridor.
- 0.50 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.65 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.05 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 2.05 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.85 s) C stopped moving.
- (unaligned, C local time 2.85 s) C came to a stop.
- (unaligned, C local time 3.55 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.55 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 4.90 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 14.35 s) C released the brake.
