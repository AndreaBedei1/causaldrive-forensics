# Global graph - S10/run_0_stops_then_proceeds

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| A:track_003 | anonymous_track | seen only by A; candidate: - |
| A:track_004 | anonymous_track | seen only by A; candidate: - |
| A:track_005 | anonymous_track | seen only by A; candidate: - |
| A:track_006 | anonymous_track | seen only by A; candidate: - |
| A:track_007 | anonymous_track | seen only by A; candidate: - |
| A:track_008 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |

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
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_003 | A:track_003 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_004 | A:track_004 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_005 | A:track_005 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_006 | A:track_006 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_007 | A:track_007 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_008 | A:track_008 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.75 | relevant_to_ego_path=False |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.15 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.55 |  |
| g05 | - | HARD_BRAKE_START | A | - | A:e05 @ 2.55 |  |
| g06 | - | MOVING_END | A | - | A:e06 @ 3.35 |  |
| g07 | - | STOP_START | A | - | A:e07 @ 3.35 |  |
| g08 | - | TRACK_APPEARED | A | A:track_001 | A:e08 @ 3.70 |  |
| g09 | - | CLOSING_START | A | A:track_001 | A:e09 @ 3.70 | active_at_first_observation=True |
| g10 | - | CRITICAL_TTC_START | A | A:track_001 | A:e10 @ 4.25 |  |
| g11 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e11 @ 5.80 |  |
| g12 | - | CRITICAL_TTC_END | A | A:track_001 | A:e12 @ 5.95 |  |
| g13 | - | CLOSING_END | A | A:track_001 | A:e13 @ 6.10 |  |
| g14 | - | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 6.25 |  |
| g15 | - | HARD_BRAKE_END | A | - | A:e15 @ 6.75 |  |
| g16 | - | BRAKE_END | A | - | A:e16 @ 6.75 |  |
| g17 | - | STRONG_THROTTLE_START | A | - | A:e17 @ 6.75 |  |
| g18 | - | TRACK_LOST | A | A:track_001 | A:e18 @ 7.00 |  |
| g19 | - | STOP_END | A | - | A:e19 @ 7.10 |  |
| g20 | - | MOVING_START | A | - | A:e20 @ 7.10 |  |
| g21 | - | TRACK_APPEARED | A | A:track_002 | A:e21 @ 8.20 |  |
| g22 | - | CLOSING_START | A | A:track_002 | A:e22 @ 8.20 | active_at_first_observation=True |
| g23 | - | STRONG_THROTTLE_END | A | - | A:e23 @ 8.25 |  |
| g24 | - | TRACK_APPEARED | A | A:track_003 | A:e24 @ 8.25 |  |
| g25 | - | CLOSING_START | A | A:track_003 | A:e25 @ 8.25 | active_at_first_observation=True |
| g26 | - | TRACK_APPEARED | A | A:track_004 | A:e26 @ 8.30 |  |
| g27 | - | CLOSING_START | A | A:track_004 | A:e27 @ 8.30 | active_at_first_observation=True |
| g28 | - | TRACK_APPEARED | A | A:track_005 | A:e28 @ 8.35 |  |
| g29 | - | CLOSING_START | A | A:track_005 | A:e29 @ 8.35 | active_at_first_observation=True |
| g30 | - | TRACK_APPEARED | A | A:track_006 | A:e30 @ 8.40 |  |
| g31 | - | CLOSING_START | A | A:track_006 | A:e31 @ 8.40 | active_at_first_observation=True |
| g32 | - | TRACK_APPEARED | A | A:track_007 | A:e32 @ 8.45 |  |
| g33 | - | TRACK_APPEARED | A | A:track_008 | A:e33 @ 8.45 |  |
| g34 | - | CLOSING_START | A | A:track_007 | A:e34 @ 8.45 | active_at_first_observation=True |
| g35 | - | CLOSING_START | A | A:track_008 | A:e35 @ 8.45 | active_at_first_observation=True |
| g36 | - | CRITICAL_TTC_START | A | A:track_003 | A:e36 @ 9.00 |  |
| g37 | - | TRACK_LOST | A | A:track_003 | A:e37 @ 9.25 |  |
| g38 | - | TRACK_LOST | A | A:track_002 | A:e38 @ 9.50 |  |
| g39 | - | TRACK_LOST | A | A:track_006 | A:e39 @ 10.75 |  |
| g40 | - | TRACK_LOST | A | A:track_007 | A:e40 @ 11.60 |  |
| g41 | - | TRACK_LOST | A | A:track_005 | A:e41 @ 12.45 |  |
| g42 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g43 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g44 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.80 |  |
| g45 | - | TRACK_APPEARED | B | B:track_001 | B:e04 @ 2.55 |  |
| g46 | - | CLOSING_START | B | B:track_001 | B:e05 @ 2.55 | active_at_first_observation=True |
| g47 | - | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 4.30 |  |
| g48 | - | TRACK_LOST | B | B:track_001 | B:e07 @ 5.50 |  |
| g49 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e08 @ 7.60 | relevant_to_ego_path=False |
| g50 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e09 @ 7.70 |  |

## Edges

```
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g12
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g14
    g08 --SAME_TRACK--> g18
    g21 --SAME_TRACK--> g22
    g24 --SAME_TRACK--> g25
    g26 --SAME_TRACK--> g27
    g28 --SAME_TRACK--> g29
    g30 --SAME_TRACK--> g31
    g32 --SAME_TRACK--> g34
    g33 --SAME_TRACK--> g35
    g24 --SAME_TRACK--> g36
    g24 --SAME_TRACK--> g37
    g21 --SAME_TRACK--> g38
    g30 --SAME_TRACK--> g39
    g32 --SAME_TRACK--> g40
    g28 --SAME_TRACK--> g41
    g45 --SAME_TRACK--> g46
    g45 --SAME_TRACK--> g47
    g45 --SAME_TRACK--> g48
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.75 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 2.15 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.55 s) A started braking.
- (unaligned, A local time 2.55 s) A started braking hard.
- (unaligned, A local time 3.35 s) A stopped moving.
- (unaligned, A local time 3.35 s) A came to a stop.
- (unaligned, A local time 3.70 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 3.70 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.25 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.80 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 5.95 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.10 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.25 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 6.75 s) A stopped braking hard.
- (unaligned, A local time 6.75 s) A released the brake.
- (unaligned, A local time 6.75 s) A started applying strong throttle.
- (unaligned, A local time 7.00 s) A's radar lost unidentified object A:track_001.
- (unaligned, A local time 7.10 s) A left its stop.
- (unaligned, A local time 7.10 s) A started moving.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A stopped applying strong throttle.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_003.
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 8.30 s) A's radar started tracking unidentified object A:track_004.
- (unaligned, A local time 8.30 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 8.35 s) A's radar started tracking unidentified object A:track_005.
- (unaligned, A local time 8.35 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 8.40 s) A's radar started tracking unidentified object A:track_006.
- (unaligned, A local time 8.40 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 8.45 s) A's radar started tracking unidentified object A:track_007.
- (unaligned, A local time 8.45 s) A's radar started tracking unidentified object A:track_008.
- (unaligned, A local time 8.45 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 8.45 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 9.00 s) A's time-to-contact with unidentified object A:track_003 became critical.
- (unaligned, A local time 9.25 s) A's radar lost unidentified object A:track_003.
- (unaligned, A local time 9.50 s) A's radar lost unidentified object A:track_002.
- (unaligned, A local time 10.75 s) A's radar lost unidentified object A:track_006.
- (unaligned, A local time 11.60 s) A's radar lost unidentified object A:track_007.
- (unaligned, A local time 12.45 s) A's radar lost unidentified object A:track_005.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 2.55 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 2.55 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.30 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.50 s) B's radar lost unidentified object B:track_001.
- (unaligned, B local time 7.60 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 7.70 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
