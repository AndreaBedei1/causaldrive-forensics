# Global graph - S08/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 4.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.0 m -> 10.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.95 m/s over 3.0 s (> 1.50)<br>clearance at the contact 10.47 m (beyond 3.50 m: confidence factor 0.07) |
| A:track_002 | B | ASSOCIATED | 0.88 | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 3.00 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.3 m -> 1.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 1.46 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.4 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.3 m -> 11.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.99 m/s over 2.1 s (> 1.50)<br>clearance at the contact 11.74 m (beyond 3.50 m: confidence factor 0.02) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.20 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.05 |  |
| g04 | -4.20 | CLOSING_START | A | A:track_001 | A:e03 @ 0.05 | active_at_first_observation=True |
| g05 | -3.00 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 1.25 |  |
| g06 | -3.00 | CLOSING_START | A | B | A:e05 @ 1.25 | active_at_first_observation=True |
| g07 | -2.95 | TRACK_APPEARED_LEFT | B | A | B:e02 @ 1.30 |  |
| g08 | -2.95 | CLOSING_START | B | A | B:e03 @ 1.30 | active_at_first_observation=True |
| g09 | -2.10 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e04 @ 2.15 |  |
| g10 | -2.10 | CLOSING_START | B | B:track_002 | B:e05 @ 2.15 | active_at_first_observation=True |
| g11 | -2.05 | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 2.20 |  |
| g12 | -1.90 | CRITICAL_TTC_START | B | A | B:e06 @ 2.35 |  |
| g13 | -1.80 | CRITICAL_TTC_START | A | B | A:e07 @ 2.45 |  |
| g14 | -1.80 | CRITICAL_TTC_START | B | B:track_002 | B:e07 @ 2.45 |  |
| g15 | -1.50 | CRITICAL_TTC_END | A | A:track_001 | A:e08 @ 2.75 |  |
| g16 | -0.75 | CRITICAL_TTC_START | A | A:track_001 | A:e09 @ 3.50 |  |
| g17 | -0.05 | TRACK_LOST | A | B | A:e10 @ 4.20 |  |
| g18 | 0.00 | COLLISION | - | A, B | A:e11 @ 4.25, B:e08 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g19 | 0.00 | CRITICAL_TTC_END | B | B:track_002 | B:e09 @ 4.25 |  |
| g20 | 0.00 | EGO_PATH_ENTRY | B | A | B:e10 @ 4.25 |  |
| g21 | 0.05 | BRAKE_START | A | - | A:e12 @ 4.30 |  |
| g22 | 0.05 | BRAKE_START | B | - | B:e11 @ 4.30 |  |
| g23 | 0.25 | CRITICAL_TTC_END | B | A | B:e12 @ 4.50 |  |
| g24 | 0.25 | CLOSING_END | B | A | B:e13 @ 4.50 |  |
| g25 | 0.30 | CLOSING_END | B | B:track_002 | B:e14 @ 4.55 |  |
| g26 | 0.30 | MOVING_END | B | - | B:e15 @ 4.55 |  |
| g27 | 0.30 | STOP_START | B | - | B:e16 @ 4.55 |  |
| g28 | 0.50 | CRITICAL_TTC_END | A | A:track_001 | A:e13 @ 4.75 |  |
| g29 | 0.65 | CLOSING_END | A | A:track_001 | A:e14 @ 4.90 |  |
| g30 | 0.65 | MOVING_END | A | - | A:e15 @ 4.90 |  |
| g31 | 0.65 | STOP_START | A | - | A:e16 @ 4.90 |  |
| g32 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g33 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e02 @ 0.00 |  |
| g34 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.00 | active_at_first_observation=True |
| g35 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e04 @ 2.25 |  |
| g36 | - | CLOSING_START | C | C:track_002 | C:e05 @ 2.25 | active_at_first_observation=True |
| g37 | - | CRITICAL_TTC_START | C | C:track_001 | C:e06 @ 2.25 |  |
| g38 | - | BRAKE_START | C | - | C:e07 @ 2.35 |  |
| g39 | - | CRITICAL_TTC_START | C | C:track_002 | C:e08 @ 2.80 |  |
| g40 | - | MOVING_END | C | - | C:e09 @ 2.85 |  |
| g41 | - | STOP_START | C | - | C:e10 @ 2.85 |  |
| g42 | - | CRITICAL_TTC_END | C | C:track_002 | C:e11 @ 3.20 |  |
| g43 | - | CRITICAL_TTC_START | C | C:track_002 | C:e12 @ 3.55 |  |
| g44 | - | CRITICAL_TTC_END | C | C:track_001 | C:e13 @ 3.85 |  |
| g45 | - | CRITICAL_TTC_END | C | C:track_002 | C:e14 @ 3.85 |  |
| g46 | - | CLOSING_END | C | C:track_002 | C:e15 @ 4.55 |  |
| g47 | - | CLOSING_END | C | C:track_001 | C:e16 @ 4.90 |  |
| g48 | - | BRAKE_END | C | - | C:e17 @ 14.35 |  |

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
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g03 --SAME_TRACK--> g04
    g05 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g15
    g03 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g28
    g03 --SAME_TRACK--> g29
    g07 --SAME_TRACK--> g08
    g09 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g14
    g09 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g20
    g07 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g24
    g09 --SAME_TRACK--> g25
    g33 --SAME_TRACK--> g34
    g35 --SAME_TRACK--> g36
    g33 --SAME_TRACK--> g37
    g35 --SAME_TRACK--> g39
    g35 --SAME_TRACK--> g42
    g35 --SAME_TRACK--> g43
    g33 --SAME_TRACK--> g44
    g35 --SAME_TRACK--> g45
    g35 --SAME_TRACK--> g46
    g33 --SAME_TRACK--> g47
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B) |
| -4.20 | TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -3.00 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.95 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -2.10 | TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_002) |
| -2.05 | CRITICAL_TTC_START(A,A:track_001) |
| -1.90 | CRITICAL_TTC_START(B,A) |
| -1.80 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_002) |
| -1.50 | CRITICAL_TTC_END(A,A:track_001) |
| -0.75 | CRITICAL_TTC_START(A,A:track_001) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(B,B:track_002); EGO_PATH_ENTRY(B,A) |
| +0.05 | BRAKE_START(A); BRAKE_START(B) |
| +0.25 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.30 | CLOSING_END(B,B:track_002); MOVING_END(B); STOP_START(B) |
| +0.50 | CRITICAL_TTC_END(A,A:track_001) |
| +0.65 | CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 2.20, COLLISION 4.25 (+2.05 s) [local times; t_global: critical_ttc_start -2.05, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.45, COLLISION with B 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.35, COLLISION with A 4.25 (+1.90 s); EGO_PATH_ENTRY 4.25 after critical TTC (+1.90 s) [local times; t_global: critical_ttc_start -1.90, ego_path_entry +0.00, collision +0.00]
- B's track_002 (unidentified B:track_002): CRITICAL_TTC_START 2.45, COLLISION 4.25 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- C's track_001 (unidentified C:track_001): CRITICAL_TTC_START 2.25 [local times]
- C's track_002 (unidentified C:track_002): CRITICAL_TTC_START 2.80 [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.20 | A | g03 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -3.00 | A | g05 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g06 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.95 | B | g07 TRACK_APPEARED_LEFT(B,A) (B:e02)<br>g08 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -2.10 | B | g09 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e04)<br>g10 CLOSING_START(B,B:track_002) (B:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.05 | A | g11 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.90 | B | g12 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.80 | A | g13 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -1.80 | B | g14 CRITICAL_TTC_START(B,B:track_002) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -1.50 | A | g15 CRITICAL_TTC_END(A,A:track_001) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| -0.75 | A | g16 CRITICAL_TTC_START(A,A:track_001) (A:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | A | g17 TRACK_LOST(A,B) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | A | g18 COLLISION(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g18 COLLISION(A,B) (B:e08)<br>g19 CRITICAL_TTC_END(B,B:track_002) (B:e09)<br>g20 EGO_PATH_ENTRY(B,A) (B:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.05 | A | g21 BRAKE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.05 | B | g22 BRAKE_START(B) (B:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| +0.25 | B | g23 CRITICAL_TTC_END(B,A) (B:e12)<br>g24 CLOSING_END(B,A) (B:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| +0.30 | B | g25 CLOSING_END(B,B:track_002) (B:e14)<br>g26 MOVING_END(B) (B:e15)<br>g27 STOP_START(B) (B:e16) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| +0.50 | A | g28 CRITICAL_TTC_END(A,A:track_001) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.65 | A | g29 CLOSING_END(A,A:track_001) (A:e14)<br>g30 MOVING_END(A) (A:e15)<br>g31 STOP_START(A) (A:e16) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| - | C | g32 MOVING_START(C) (C:e01)<br>g33 TRACK_APPEARED_FRONT(C,C:track_001) (C:e02)<br>g34 CLOSING_START(C,C:track_001) (C:e03) | ego: not yet observed |
| - | C | g35 TRACK_APPEARED_LEFT(C,C:track_002) (C:e04)<br>g36 CLOSING_START(C,C:track_002) (C:e05)<br>g37 CRITICAL_TTC_START(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING |
| - | C | g38 BRAKE_START(C) (C:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g39 CRITICAL_TTC_START(C,C:track_002) (C:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g40 MOVING_END(C) (C:e09)<br>g41 STOP_START(C) (C:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g42 CRITICAL_TTC_END(C,C:track_002) (C:e11) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g43 CRITICAL_TTC_START(C,C:track_002) (C:e12) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g44 CRITICAL_TTC_END(C,C:track_001) (C:e13)<br>g45 CRITICAL_TTC_END(C,C:track_002) (C:e14) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g46 CLOSING_END(C,C:track_002) (C:e15) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g47 CLOSING_END(C,C:track_001) (C:e16) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| - | C | g48 BRAKE_END(C) (C:e17) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 4.25 s before the reference collision, A started moving (already the case when first observed).
- 4.25 s before the reference collision, B started moving (already the case when first observed).
- 4.20 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 4.20 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 3.00 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 3.00 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.95 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.95 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.10 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 2.10 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.90 s before the reference collision, B's time-to-contact with A became critical.
- 1.80 s before the reference collision, A's time-to-contact with B became critical.
- 1.80 s before the reference collision, B's time-to-contact with unidentified object B:track_002 became critical.
- 1.50 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.75 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the reference collision, B's time-to-contact with unidentified object B:track_002 stopped being critical.
- At the reference collision, B observed A enter its forward path corridor.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.25 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the reference collision, B observed A stop closing in.
- 0.30 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.30 s after the reference collision, B stopped moving.
- 0.30 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.65 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 2.25 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.80 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.85 s) C stopped moving.
- (unaligned, C local time 2.85 s) C came to a stop.
- (unaligned, C local time 3.20 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 3.55 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 3.85 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.55 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 4.90 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 14.35 s) C released the brake.
