# Global graph - S01/run_0_avoided

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.45 |  |
| g04 | - | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g05 | - | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g06 | - | CLOSING_END | A | A:track_001 | A:e06 @ 1.60 |  |
| g07 | - | CLOSING_START | A | A:track_001 | A:e07 @ 4.25 |  |
| g08 | - | CRITICAL_TTC_START | A | A:track_001 | A:e08 @ 5.00 |  |
| g09 | - | BRAKE_START | A | - | A:e09 @ 5.05 |  |
| g10 | - | HARD_BRAKE_START | A | - | A:e10 @ 5.05 |  |
| g11 | - | CRITICAL_TTC_END | A | A:track_001 | A:e11 @ 6.25 |  |
| g12 | - | CLOSING_END | A | A:track_001 | A:e12 @ 6.35 |  |
| g13 | - | MOVING_END | A | - | A:e13 @ 6.35 |  |
| g14 | - | STOP_START | A | - | A:e14 @ 6.35 |  |
| g15 | - | STRONG_THROTTLE_START | A | - | A:e15 @ 13.05 |  |
| g16 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g17 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 0.40 |  |
| g18 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.75 |  |
| g19 | - | BRAKE_START | B | - | B:e04 @ 3.95 |  |
| g20 | - | HARD_BRAKE_START | B | - | B:e05 @ 3.95 |  |
| g21 | - | MOVING_END | B | - | B:e06 @ 5.15 |  |
| g22 | - | STOP_START | B | - | B:e07 @ 5.15 |  |
| g23 | - | HARD_BRAKE_END | B | - | B:e08 @ 11.95 |  |
| g24 | - | BRAKE_END | B | - | B:e09 @ 11.95 |  |
| g25 | - | STRONG_THROTTLE_START | B | - | B:e10 @ 11.95 |  |
| g26 | - | STOP_END | B | - | B:e11 @ 12.35 |  |
| g27 | - | MOVING_START | B | - | B:e12 @ 12.35 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g02 --SAME_TRACK--> g08
    g02 --SAME_TRACK--> g11
    g02 --SAME_TRACK--> g12
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 0.45 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 1.15 s) A started applying strong throttle.
- (unaligned, A local time 1.35 s) A stopped applying strong throttle.
- (unaligned, A local time 1.60 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.25 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 5.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.05 s) A started braking.
- (unaligned, A local time 5.05 s) A started braking hard.
- (unaligned, A local time 6.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.35 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.35 s) A stopped moving.
- (unaligned, A local time 6.35 s) A came to a stop.
- (unaligned, A local time 13.05 s) A started applying strong throttle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.40 s) B started applying strong throttle.
- (unaligned, B local time 1.75 s) B stopped applying strong throttle.
- (unaligned, B local time 3.95 s) B started braking.
- (unaligned, B local time 3.95 s) B started braking hard.
- (unaligned, B local time 5.15 s) B stopped moving.
- (unaligned, B local time 5.15 s) B came to a stop.
- (unaligned, B local time 11.95 s) B stopped braking hard.
- (unaligned, B local time 11.95 s) B released the brake.
- (unaligned, B local time 11.95 s) B started applying strong throttle.
- (unaligned, B local time 12.35 s) B left its stop.
- (unaligned, B local time 12.35 s) B started moving.
