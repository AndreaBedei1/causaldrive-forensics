# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 14.000380951911211 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 12 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 33; edges: 56 (PRECEDES 39, SAME_TRACK 17)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_004 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e07 | 0.05 | TRACK_APPEARED_LEFT | B | track_005 | radar | initial_in_ego_path=False |
| B:e08 | 0.05 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e09 | 0.15 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e10 | 0.20 | TRACK_APPEARED_FRONT | B | track_008 | radar | initial_in_ego_path=False |
| B:e11 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e12 | 2.20 | TRACK_LOST | B | track_008 | radar |  |
| B:e13 | 3.65 | TRACK_LOST | B | track_004 | radar |  |
| B:e14 | 3.80 | TRACK_LOST | B | track_007 | radar |  |
| B:e15 | 6.40 | TRACK_APPEARED_LEFT | B | track_009 | radar | initial_in_ego_path=False |
| B:e16 | 6.50 | TRACK_APPEARED_RIGHT | B | track_010 | radar | initial_in_ego_path=False |
| B:e17 | 6.60 | TRACK_APPEARED_FRONT | B | track_011 | radar | initial_in_ego_path=False |
| B:e18 | 7.00 | TRACK_LOST | B | track_011 | radar |  |
| B:e19 | 7.05 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e20 | 7.15 | CLOSING_START | B | track_002 | radar |  |
| B:e21 | 7.75 | COLLISION | B | - | collision_sensor | peak_impulse=497.63 |
| B:e22 | 7.75 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e23 | 7.80 | THROTTLE_END | B | - | controls |  |
| B:e24 | 7.85 | CLOSING_END | B | track_002 | radar |  |
| B:e25 | 8.15 | TRACK_APPEARED_FRONT | B | track_012 | radar | initial_in_ego_path=True |
| B:e26 | 8.75 | TRACK_LOST | B | track_010 | radar |  |
| B:e27 | 9.00 | EGO_PATH_ENTRY | B | track_009 | radar | geometry=estimated_body |
| B:e28 | 9.35 | TRACK_LOST | B | track_009 | radar |  |
| B:e29 | 9.95 | EGO_PATH_ENTRY | B | track_005 | radar | geometry=estimated_body |
| B:e30 | 11.05 | CLOSING_START | B | track_003 | radar |  |
| B:e31 | 11.40 | EGO_PATH_EXIT | B | track_005 | radar | geometry=estimated_body |
| B:e32 | 11.55 | CLOSING_START | B | track_002 | radar |  |
| B:e33 | 11.60 | CRITICAL_TTC_START | B | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e07
    B:e01 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e07
    B:e02 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e03 --SAME_TRACK--> B:e11
    B:e10 --SAME_TRACK--> B:e12
    B:e04 --SAME_TRACK--> B:e13
    B:e09 --SAME_TRACK--> B:e14
    B:e17 --SAME_TRACK--> B:e18
    B:e05 --SAME_TRACK--> B:e19
    B:e05 --SAME_TRACK--> B:e20
    B:e05 --SAME_TRACK--> B:e22
    B:e05 --SAME_TRACK--> B:e24
    B:e16 --SAME_TRACK--> B:e26
    B:e15 --SAME_TRACK--> B:e27
    B:e15 --SAME_TRACK--> B:e28
    B:e07 --SAME_TRACK--> B:e29
    B:e06 --SAME_TRACK--> B:e30
    B:e07 --SAME_TRACK--> B:e31
    B:e05 --SAME_TRACK--> B:e32
    B:e06 --SAME_TRACK--> B:e33
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_LEFT track_004<br>B:e05 TRACK_APPEARED_RIGHT track_002<br>B:e06 TRACK_APPEARED_RIGHT track_003 | ego: not yet observed | - |
| 0.05 | B:e07 TRACK_APPEARED_LEFT track_005<br>B:e08 TRACK_APPEARED_RIGHT track_006 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.00 |
| 0.15 | B:e09 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC? | 0.10 |
| 0.20 | B:e10 TRACK_APPEARED_FRONT track_008 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? | 0.10 |
| 0.50 | B:e11 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC? | 0.40 |
| 2.20 | B:e12 TRACK_LOST track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state | 2.10 |
| 3.65 | B:e13 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_008 | 3.60 |
| 3.80 | B:e14 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_008 | 3.70 |
| 6.40 | B:e15 TRACK_APPEARED_LEFT track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008 | 6.30 |
| 6.50 | B:e16 TRACK_APPEARED_RIGHT track_010 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 | 6.40 |
| 6.60 | B:e17 TRACK_APPEARED_FRONT track_011 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 | 6.50 |
| 7.00 | B:e18 TRACK_LOST track_011 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track_011: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_007, track_008 | 6.90 |
| 7.05 | B:e19 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 7.00 |
| 7.15 | B:e20 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 7.10 |
| 7.75 | B:e21 COLLISION<br>B:e22 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 7.70 |
| 7.80 | B:e23 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 7.70 |
| 7.85 | B:e24 CLOSING_END track_002 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 7.80 |
| 8.15 | B:e25 TRACK_APPEARED_FRONT track_012 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 8.10 |
| 8.75 | B:e26 TRACK_LOST track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 | 8.70 |
| 9.00 | B:e27 EGO_PATH_ENTRY track_009 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_010, track_011 | 8.90 |
| 9.35 | B:e28 TRACK_LOST track_009 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_010, track_011 | 9.30 |
| 9.95 | B:e29 EGO_PATH_ENTRY track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 | 9.90 |
| 11.05 | B:e30 CLOSING_START track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 | 11.00 |
| 11.40 | B:e31 EGO_PATH_EXIT track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 | 11.30 |
| 11.55 | B:e32 CLOSING_START track_002 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 | 11.50 |
| 11.60 | B:e33 CRITICAL_TTC_START track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 | 11.50 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)
- CRITICAL_TTC of track_001, since B:e11 (t = 0.50 s)
- EGO_PATH of track_009, since B:e27 (t = 9.00 s); the track was lost at 9.35 s
- CLOSING of track_003, since B:e30 (t = 11.05 s)
- CLOSING of track_002, since B:e32 (t = 11.55 s)
- CRITICAL_TTC of track_003, since B:e33 (t = 11.60 s)

## Tracks lost

- track_009 at 9.35 s (B:e28): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_008, track_004, track_007, track_011, track_010

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s)
- track_002: CRITICAL_TTC_START 7.05, COLLISION 7.75 (+0.70 s)
- track_003: CRITICAL_TTC_START 11.60
- track_005: EGO_PATH_ENTRY 9.95, no critical TTC
- track_009: EGO_PATH_ENTRY 9.00, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 14.4 m / +1 deg | 9.11 m (11.45) | 9.2 m / -12 deg | 12.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 2.6 m / +38 deg | 1.25 m (7.50) | 1.6 m / +68 deg | 14.3 m/s |
| track_003 | 0.00 | 11.95 | 240 | 7.5 m / +17 deg | 2.44 m (11.95) | 2.4 m / +29 deg | 12.3 m/s |
| track_004 | 0.00 | 3.65 | 70 | 30.2 m / -5 deg | 28.57 m (3.65) | 28.6 m / -6 deg | 12.1 m/s |
| track_005 | 0.05 | 11.95 | 239 | 14.6 m / -11 deg | 10.11 m (10.10) | 11.2 m / -28 deg | 12.1 m/s |
| track_006 | 0.05 | 11.95 | 239 | 15.4 m / +10 deg | 9.77 m (11.95) | 9.8 m / +2 deg | 12.1 m/s |
| track_007 | 0.15 | 3.80 | 73 | 30.2 m / +6 deg | 28.03 m (3.80) | 28.0 m / +6 deg | 11.8 m/s |
| track_008 | 0.20 | 2.20 | 35 | 45.2 m / -4 deg | 44.27 m (2.20) | 44.3 m / -4 deg | 11.9 m/s |
| track_009 | 6.40 | 9.35 | 58 | 27.6 m / -6 deg | 26.39 m (9.35) | 26.4 m / -5 deg | 12.1 m/s |
| track_010 | 6.50 | 8.75 | 46 | 27.0 m / +7 deg | 25.90 m (8.75) | 25.9 m / +10 deg | 12.1 m/s |
| track_011 | 6.60 | 7.00 | 7 | 42.8 m / -5 deg | 42.58 m (7.00) | 42.6 m / -4 deg | 12.1 m/s |
| track_012 | 8.15 | 11.95 | 62 | 41.7 m / -1 deg | 40.69 m (11.05) | 41.0 m / -21 deg | 12.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.05 s: B's radar started tracking track_005, which appeared on its left.
- t = 0.05 s: B's radar started tracking track_006, which appeared on its right.
- t = 0.15 s: B's radar started tracking track_007, which appeared on its right.
- t = 0.20 s: B's radar started tracking track_008, which appeared in front of it.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 2.20 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 3.65 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 6.40 s: B's radar started tracking track_009, which appeared on its left.
- t = 6.50 s: B's radar started tracking track_010, which appeared on its right.
- t = 6.60 s: B's radar started tracking track_011, which appeared in front of it.
- t = 7.00 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 7.05 s: B's time-to-contact with track_002 became critical.
- t = 7.15 s: B observed track_002 start closing in.
- t = 7.75 s: B's collision sensor recorded a contact (peak impulse 498 N*s).
- t = 7.75 s: B's time-to-contact with track_002 stopped being critical.
- t = 7.80 s: B released the accelerator.
- t = 7.85 s: B observed track_002 stop closing in.
- t = 8.15 s: B's radar started tracking track_012, which appeared in front of it.
- t = 8.75 s: B's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 9.00 s: B observed track_009 enter its forward path corridor.
- t = 9.35 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 9.95 s: B observed track_005 enter its forward path corridor.
- t = 11.05 s: B observed track_003 start closing in.
- t = 11.40 s: B observed track_005 leave its forward path corridor.
- t = 11.55 s: B observed track_002 start closing in.
- t = 11.60 s: B's time-to-contact with track_003 became critical.
