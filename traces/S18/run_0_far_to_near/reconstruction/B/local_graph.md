# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 534.8805473558605 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 11 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 42; edges: 95 (PRECEDES 71, SAME_TRACK 24)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 0.15 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e07 | 0.15 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e08 | 0.40 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e09 | 0.85 | TRACK_APPEARED_FRONT | B | track_006 | radar | initial_in_ego_path=False |
| B:e10 | 0.85 | TRACK_APPEARED_RIGHT | B | track_005 | radar | initial_in_ego_path=False |
| B:e11 | 0.85 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e12 | 0.85 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e13 | 2.30 | CLOSING_END | B | track_001 | radar |  |
| B:e14 | 2.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e15 | 2.55 | TRACK_LOST | B | track_004 | radar |  |
| B:e16 | 3.35 | TRACK_LOST | B | track_006 | radar |  |
| B:e17 | 3.40 | TRACK_LOST | B | track_005 | radar |  |
| B:e18 | 3.50 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e19 | 5.40 | TRACK_LOST | B | track_007 | radar |  |
| B:e20 | 5.80 | CLOSING_END | B | track_003 | radar |  |
| B:e21 | 5.80 | TRACK_LOST | B | track_003 | radar |  |
| B:e22 | 6.55 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e23 | 6.55 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e24 | 6.80 | TRACK_APPEARED_RIGHT | B | track_009 | radar | initial_in_ego_path=False |
| B:e25 | 6.80 | CLOSING_START | B | track_009 | radar | active_at_first_observation=True |
| B:e26 | 6.95 | TRACK_APPEARED_RIGHT | B | track_010 | radar | initial_in_ego_path=False |
| B:e27 | 7.70 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e28 | 7.80 | CLOSING_START | B | track_002 | radar |  |
| B:e29 | 8.30 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e30 | 8.50 | COLLISION | B | - | collision_sensor | peak_impulse=745.29 |
| B:e31 | 8.50 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e32 | 8.55 | CLOSING_END | B | track_002 | radar |  |
| B:e33 | 8.55 | THROTTLE_END | B | - | controls |  |
| B:e34 | 8.55 | BRAKE_START | B | - | controls |  |
| B:e35 | 9.20 | EGO_PATH_EXIT | B | track_002 | radar | geometry=estimated_body |
| B:e36 | 9.20 | TRACK_LOST | B | track_010 | radar |  |
| B:e37 | 9.30 | CLOSING_END | B | track_008 | radar |  |
| B:e38 | 9.30 | CLOSING_END | B | track_009 | radar |  |
| B:e39 | 9.60 | MOVING_END | B | - | ego |  |
| B:e40 | 9.60 | STOP_START | B | - | ego |  |
| B:e41 | 9.85 | TRACK_APPEARED_RIGHT | B | track_011 | radar | initial_in_ego_path=False |
| B:e42 | 9.85 | CLOSING_START | B | track_011 | radar | active_at_first_observation=True |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e01 --PRECEDES--> B:e07
    B:e02 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e09 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e33
    B:e30 --PRECEDES--> B:e34
    B:e31 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e33
    B:e31 --PRECEDES--> B:e34
    B:e32 --PRECEDES--> B:e35
    B:e32 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e35
    B:e33 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e38
    B:e36 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e37 --PRECEDES--> B:e40
    B:e38 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e41
    B:e39 --PRECEDES--> B:e42
    B:e40 --PRECEDES--> B:e41
    B:e40 --PRECEDES--> B:e42
    B:e03 --SAME_TRACK--> B:e05
    B:e06 --SAME_TRACK--> B:e07
    B:e10 --SAME_TRACK--> B:e11
    B:e09 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e13
    B:e03 --SAME_TRACK--> B:e14
    B:e08 --SAME_TRACK--> B:e15
    B:e09 --SAME_TRACK--> B:e16
    B:e10 --SAME_TRACK--> B:e17
    B:e18 --SAME_TRACK--> B:e19
    B:e06 --SAME_TRACK--> B:e20
    B:e06 --SAME_TRACK--> B:e21
    B:e22 --SAME_TRACK--> B:e23
    B:e24 --SAME_TRACK--> B:e25
    B:e04 --SAME_TRACK--> B:e27
    B:e04 --SAME_TRACK--> B:e28
    B:e04 --SAME_TRACK--> B:e29
    B:e04 --SAME_TRACK--> B:e31
    B:e04 --SAME_TRACK--> B:e32
    B:e04 --SAME_TRACK--> B:e35
    B:e26 --SAME_TRACK--> B:e36
    B:e22 --SAME_TRACK--> B:e37
    B:e24 --SAME_TRACK--> B:e38
    B:e41 --SAME_TRACK--> B:e42
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 CLOSING_START track_001 | ego: not yet observed | - |
| 0.15 | B:e06 TRACK_APPEARED_RIGHT track_003<br>B:e07 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? | 0.10 |
| 0.40 | B:e08 TRACK_APPEARED_RIGHT track_004 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC? | 0.30 |
| 0.85 | B:e09 TRACK_APPEARED_FRONT track_006<br>B:e10 TRACK_APPEARED_RIGHT track_005<br>B:e11 CLOSING_START track_005<br>B:e12 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CRITICAL_TTC? | 0.80 |
| 2.30 | B:e13 CLOSING_END track_001<br>B:e14 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005: CLOSING<br>track_006: CLOSING | 2.20 |
| 2.55 | B:e15 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001 | 2.50 |
| 3.35 | B:e16 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001, track_004 | 3.30 |
| 3.40 | B:e17 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_006 | 3.30 |
| 3.50 | B:e18 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006 | 3.40 |
| 5.40 | B:e19 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_007: no active state<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006 | 5.30 |
| 5.80 | B:e20 CLOSING_END track_003<br>B:e21 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006, track_007 | 5.70 |
| 6.55 | B:e22 TRACK_APPEARED_RIGHT track_008<br>B:e23 CLOSING_START track_008 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 6.50 |
| 6.80 | B:e24 TRACK_APPEARED_RIGHT track_009<br>B:e25 CLOSING_START track_009 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 6.70 |
| 6.95 | B:e26 TRACK_APPEARED_RIGHT track_010 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 6.90 |
| 7.70 | B:e27 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 7.60 |
| 7.80 | B:e28 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 7.70 |
| 8.30 | B:e29 EGO_PATH_ENTRY track_002 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 8.20 |
| 8.50 | B:e30 COLLISION<br>B:e31 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 8.40 |
| 8.55 | B:e32 CLOSING_END track_002<br>B:e33 THROTTLE_END<br>B:e34 BRAKE_START | ego: MOVING, THROTTLE<br>track_002: CLOSING, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 8.50 |
| 9.20 | B:e35 EGO_PATH_EXIT track_002<br>B:e36 TRACK_LOST track_010 | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 | 9.10 |
| 9.30 | B:e37 CLOSING_END track_008<br>B:e38 CLOSING_END track_009 | ego: MOVING, BRAKE<br>track_002: no active state<br>track_008: CLOSING<br>track_009: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_010 | 9.20 |
| 9.60 | B:e39 MOVING_END<br>B:e40 STOP_START | ego: MOVING, BRAKE<br>track_002: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_010 | 9.50 |
| 9.85 | B:e41 TRACK_APPEARED_RIGHT track_011<br>B:e42 CLOSING_START track_011 | ego: STOP, BRAKE<br>track_002: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_010 | 9.80 |

## States still active when observation ended

- CLOSING of track_005, since B:e11 (t = 0.85 s); the track was lost at 3.40 s
- CLOSING of track_006, since B:e12 (t = 0.85 s); the track was lost at 3.35 s
- BRAKE, since B:e34 (t = 8.55 s)
- STOP, since B:e40 (t = 9.60 s)
- CLOSING of track_011, since B:e42 (t = 9.85 s)

## Tracks lost

- track_001 at 2.30 s (B:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.35 s (B:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 3.40 s (B:e17): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 5.80 s (B:e21): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_007, track_010

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 7.70, COLLISION 8.50 (+0.80 s); EGO_PATH_ENTRY 8.30 after critical TTC (+0.60 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 2.30 | 47 | 16.2 m / +22 deg | 5.56 m (2.30) | 5.6 m / +69 deg | 7.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 1.5 m / +98 deg | 0.64 m (8.85) | 1.7 m / +73 deg | 14.6 m/s |
| track_003 | 0.15 | 5.80 | 109 | 38.2 m / +10 deg | 5.51 m (5.80) | 5.5 m / +70 deg | 7.4 m/s |
| track_004 | 0.40 | 2.55 | 44 | 6.8 m / +138 deg | 6.79 m (0.40) | 19.7 m / +157 deg | 7.7 m/s |
| track_005 | 0.85 | 3.40 | 35 | 59.9 m / +6 deg | 42.75 m (3.40) | 42.8 m / +8 deg | 6.1 m/s |
| track_006 | 0.85 | 3.35 | 34 | 59.9 m / +3 deg | 42.39 m (3.35) | 42.4 m / +4 deg | 6.0 m/s |
| track_007 | 3.50 | 5.40 | 39 | 7.3 m / +139 deg | 7.30 m (3.50) | 19.1 m / +156 deg | 7.1 m/s |
| track_008 | 6.55 | 11.95 | 108 | 21.7 m / +16 deg | 7.35 m (9.30) | 19.1 m / +21 deg | 6.4 m/s |
| track_009 | 6.80 | 11.95 | 104 | 18.5 m / +9 deg | 4.04 m (9.30) | 17.5 m / +12 deg | 6.2 m/s |
| track_010 | 6.95 | 9.20 | 38 | 7.6 m / +139 deg | 7.59 m (6.95) | 20.0 m / +156 deg | 8.4 m/s |
| track_011 | 9.85 | 11.95 | 43 | 17.5 m / +156 deg | 6.66 m (11.95) | 6.7 m / +128 deg | 5.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.15 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.15 s: B observed track_003 start closing in (already the case when first observed).
- t = 0.40 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.85 s: B's radar started tracking track_006, which appeared in front of it.
- t = 0.85 s: B's radar started tracking track_005, which appeared on its right.
- t = 0.85 s: B observed track_005 start closing in (already the case when first observed).
- t = 0.85 s: B observed track_006 start closing in (already the case when first observed).
- t = 2.30 s: B observed track_001 stop closing in.
- t = 2.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.55 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.35 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 3.40 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.50 s: B's radar started tracking track_007, which appeared on its right.
- t = 5.40 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 5.80 s: B observed track_003 stop closing in.
- t = 5.80 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 6.55 s: B's radar started tracking track_008, which appeared on its right.
- t = 6.55 s: B observed track_008 start closing in (already the case when first observed).
- t = 6.80 s: B's radar started tracking track_009, which appeared on its right.
- t = 6.80 s: B observed track_009 start closing in (already the case when first observed).
- t = 6.95 s: B's radar started tracking track_010, which appeared on its right.
- t = 7.70 s: B's time-to-contact with track_002 became critical.
- t = 7.80 s: B observed track_002 start closing in.
- t = 8.30 s: B observed track_002 enter its forward path corridor.
- t = 8.50 s: B's collision sensor recorded a contact (peak impulse 745 N*s).
- t = 8.50 s: B's time-to-contact with track_002 stopped being critical.
- t = 8.55 s: B observed track_002 stop closing in.
- t = 8.55 s: B released the accelerator.
- t = 8.55 s: B started braking.
- t = 9.20 s: B observed track_002 leave its forward path corridor.
- t = 9.20 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 9.30 s: B observed track_008 stop closing in.
- t = 9.30 s: B observed track_009 stop closing in.
- t = 9.60 s: B stopped moving.
- t = 9.60 s: B came to a stop.
- t = 9.85 s: B's radar started tracking track_011, which appeared on its right.
- t = 9.85 s: B observed track_011 start closing in (already the case when first observed).
