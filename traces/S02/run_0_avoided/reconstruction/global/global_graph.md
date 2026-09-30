# Global graph - S02/run_0_avoided

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
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g05 | - | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g06 | - | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 2.75 |  |
| g07 | - | BRAKE_START | A | - | A:e07 @ 2.85 |  |
| g08 | - | HARD_BRAKE_START | A | - | A:e08 @ 2.85 |  |
| g09 | - | CRITICAL_TTC_END | A | A:track_001 | A:e09 @ 3.10 |  |
| g10 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e10 @ 3.15 |  |
| g11 | - | HARD_BRAKE_END | A | - | A:e11 @ 3.70 |  |
| g12 | - | CLOSING_END | A | A:track_001 | A:e12 @ 4.05 |  |
| g13 | - | BRAKE_END | A | - | A:e13 @ 4.10 |  |
| g14 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g15 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 0.35 |  |
| g16 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.30 |  |
| g17 | - | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g18 | - | BRAKE_END | B | - | B:e05 @ 3.60 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g09
    g02 --SAME_TRACK--> g10
    g02 --SAME_TRACK--> g12
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 1.15 s) A started applying strong throttle.
- (unaligned, A local time 1.35 s) A stopped applying strong throttle.
- (unaligned, A local time 2.75 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 2.85 s) A started braking.
- (unaligned, A local time 2.85 s) A started braking hard.
- (unaligned, A local time 3.10 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 3.15 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 3.70 s) A stopped braking hard.
- (unaligned, A local time 4.05 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.10 s) A released the brake.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.35 s) B started applying strong throttle.
- (unaligned, B local time 1.30 s) B stopped applying strong throttle.
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.60 s) B released the brake.
