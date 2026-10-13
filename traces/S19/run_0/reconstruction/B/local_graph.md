# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 142.39008847996593 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 11 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 36; edges: 74 (PRECEDES 53, SAME_TRACK 21)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_003 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e07 | 0.05 | TRACK_APPEARED_FRONT | B | track_007 | radar | initial_in_ego_path=False |
| B:e08 | 0.05 | TRACK_APPEARED_LEFT | B | track_006 | radar | initial_in_ego_path=False |
| B:e09 | 0.05 | TRACK_APPEARED_RIGHT | B | track_005 | radar | initial_in_ego_path=False |
| B:e10 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e11 | 2.20 | TRACK_LOST | B | track_007 | radar |  |
| B:e12 | 3.65 | TRACK_LOST | B | track_003 | radar |  |
| B:e13 | 3.80 | TRACK_LOST | B | track_004 | radar |  |
| B:e14 | 6.35 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e15 | 6.40 | TRACK_APPEARED_LEFT | B | track_009 | radar | initial_in_ego_path=False |
| B:e16 | 6.60 | TRACK_APPEARED_FRONT | B | track_010 | radar | initial_in_ego_path=False |
| B:e17 | 7.00 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e18 | 7.05 | CLOSING_START | B | track_002 | radar |  |
| B:e19 | 7.75 | COLLISION | B | - | collision_sensor | peak_impulse=255.03 |
| B:e20 | 7.75 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e21 | 7.75 | CLOSING_END | B | track_002 | radar |  |
| B:e22 | 7.80 | THROTTLE_END | B | - | controls |  |
| B:e23 | 7.85 | EGO_PATH_ENTRY | B | track_010 | radar | geometry=estimated_body |
| B:e24 | 8.00 | EGO_PATH_ENTRY | B | track_009 | radar | geometry=estimated_body |
| B:e25 | 8.85 | TRACK_LOST | B | track_008 | radar |  |
| B:e26 | 9.20 | EGO_PATH_ENTRY | B | track_006 | radar | geometry=estimated_body |
| B:e27 | 9.20 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e28 | 9.35 | TRACK_LOST | B | track_009 | radar |  |
| B:e29 | 9.60 | EGO_PATH_EXIT | B | track_010 | radar | geometry=estimated_body |
| B:e30 | 9.60 | CUT_IN_FROM_RIGHT_START | B | track_005 | radar | geometry=estimated_body |
| B:e31 | 10.55 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e32 | 10.55 | EGO_PATH_EXIT | B | track_006 | radar | geometry=estimated_body |
| B:e33 | 10.70 | CRITICAL_TTC_START | B | track_005 | radar |  |
| B:e34 | 11.15 | EGO_PATH_ENTRY | B | track_005 | radar | geometry=estimated_body |
| B:e35 | 11.35 | TRACK_APPEARED_LEFT | B | track_011 | radar | initial_in_ego_path=False |
| B:e36 | 11.65 | TRACK_LOST | B | track_011 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e07
    B:e01 --PRECEDES--> B:e08
    B:e01 --PRECEDES--> B:e09
    B:e02 --PRECEDES--> B:e07
    B:e02 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e10
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
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e33
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e03 --SAME_TRACK--> B:e10
    B:e07 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e06 --SAME_TRACK--> B:e13
    B:e05 --SAME_TRACK--> B:e17
    B:e05 --SAME_TRACK--> B:e18
    B:e05 --SAME_TRACK--> B:e20
    B:e05 --SAME_TRACK--> B:e21
    B:e16 --SAME_TRACK--> B:e23
    B:e15 --SAME_TRACK--> B:e24
    B:e14 --SAME_TRACK--> B:e25
    B:e08 --SAME_TRACK--> B:e26
    B:e08 --SAME_TRACK--> B:e27
    B:e15 --SAME_TRACK--> B:e28
    B:e16 --SAME_TRACK--> B:e29
    B:e09 --SAME_TRACK--> B:e30
    B:e08 --SAME_TRACK--> B:e31
    B:e08 --SAME_TRACK--> B:e32
    B:e09 --SAME_TRACK--> B:e33
    B:e09 --SAME_TRACK--> B:e34
    B:e35 --SAME_TRACK--> B:e36
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_LEFT track_003<br>B:e05 TRACK_APPEARED_RIGHT track_002<br>B:e06 TRACK_APPEARED_RIGHT track_004 | ego: not yet observed | - |
| 0.05 | B:e07 TRACK_APPEARED_FRONT track_007<br>B:e08 TRACK_APPEARED_LEFT track_006<br>B:e09 TRACK_APPEARED_RIGHT track_005 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.00 |
| 0.50 | B:e10 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? | 0.40 |
| 2.20 | B:e11 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 2.10 |
| 3.65 | B:e12 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_007 | 3.60 |
| 3.80 | B:e13 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_003, track_007 | 3.70 |
| 6.35 | B:e14 TRACK_APPEARED_RIGHT track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 6.30 |
| 6.40 | B:e15 TRACK_APPEARED_LEFT track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 6.30 |
| 6.60 | B:e16 TRACK_APPEARED_FRONT track_010 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 6.50 |
| 7.00 | B:e17 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 6.90 |
| 7.05 | B:e18 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 7.00 |
| 7.75 | B:e19 COLLISION<br>B:e20 CRITICAL_TTC_END track_002<br>B:e21 CLOSING_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 7.70 |
| 7.80 | B:e22 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 7.70 |
| 7.85 | B:e23 EGO_PATH_ENTRY track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 7.80 |
| 8.00 | B:e24 EGO_PATH_ENTRY track_009 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 7.90 |
| 8.85 | B:e25 TRACK_LOST track_008 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007 | 8.80 |
| 9.20 | B:e26 EGO_PATH_ENTRY track_006<br>B:e27 CRITICAL_TTC_START track_006 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008 | 9.10 |
| 9.35 | B:e28 TRACK_LOST track_009 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008 | 9.30 |
| 9.60 | B:e29 EGO_PATH_EXIT track_010<br>B:e30 CUT_IN_FROM_RIGHT_START track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 9.50 |
| 10.55 | B:e31 CRITICAL_TTC_END track_006<br>B:e32 EGO_PATH_EXIT track_006 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 10.50 |
| 10.70 | B:e33 CRITICAL_TTC_START track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 10.60 |
| 11.15 | B:e34 EGO_PATH_ENTRY track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 11.10 |
| 11.35 | B:e35 TRACK_APPEARED_LEFT track_011 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 11.30 |
| 11.65 | B:e36 TRACK_LOST track_011 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track_011: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 | 11.60 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)
- CRITICAL_TTC of track_001, since B:e10 (t = 0.50 s)
- EGO_PATH of track_009, since B:e24 (t = 8.00 s); the track was lost at 9.35 s
- CUT_IN_FROM_RIGHT of track_005, since B:e30 (t = 9.60 s)
- CRITICAL_TTC of track_005, since B:e33 (t = 10.70 s)
- EGO_PATH of track_005, since B:e34 (t = 11.15 s)

## Tracks lost

- track_009 at 9.35 s (B:e28): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_007, track_003, track_004, track_008, track_011

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s)
- track_002: CRITICAL_TTC_START 7.00, COLLISION 7.75 (+0.75 s)
- track_005: cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 9.60 < CRITICAL_TTC_START 10.70 (+1.10 s); EGO_PATH_ENTRY 11.15 after critical TTC (+0.45 s)
- track_006: CRITICAL_TTC_START 9.20; EGO_PATH_ENTRY 9.20 together with critical TTC (+0.00 s)
- track_009: EGO_PATH_ENTRY 8.00, no critical TTC
- track_010: EGO_PATH_ENTRY 7.85, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 14.4 m / +1 deg | 9.12 m (11.45) | 9.2 m / -11 deg | 12.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 2.9 m / +38 deg | 1.04 m (7.70) | 1.7 m / +72 deg | 14.1 m/s |
| track_003 | 0.00 | 3.65 | 70 | 30.1 m / -5 deg | 28.54 m (3.65) | 28.5 m / -6 deg | 12.2 m/s |
| track_004 | 0.00 | 3.80 | 75 | 30.4 m / +6 deg | 28.04 m (3.80) | 28.0 m / +6 deg | 11.9 m/s |
| track_005 | 0.05 | 11.95 | 239 | 15.4 m / +10 deg | 9.63 m (11.95) | 9.6 m / +3 deg | 12.1 m/s |
| track_006 | 0.05 | 11.95 | 239 | 14.6 m / -12 deg | 10.09 m (10.10) | 11.1 m / -28 deg | 12.1 m/s |
| track_007 | 0.05 | 2.20 | 37 | 45.2 m / -4 deg | 44.26 m (2.20) | 44.3 m / -4 deg | 11.9 m/s |
| track_008 | 6.35 | 8.85 | 49 | 27.1 m / +7 deg | 25.92 m (8.85) | 25.9 m / +10 deg | 12.2 m/s |
| track_009 | 6.40 | 9.35 | 58 | 27.6 m / -6 deg | 26.42 m (9.35) | 26.4 m / -5 deg | 12.1 m/s |
| track_010 | 6.60 | 11.95 | 75 | 42.6 m / -5 deg | 40.73 m (11.05) | 41.0 m / -21 deg | 12.3 m/s |
| track_011 | 11.35 | 11.65 | 5 | 44.3 m / -22 deg | 44.30 m (11.35) | 44.5 m / -24 deg | 12.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.05 s: B's radar started tracking track_007, which appeared in front of it.
- t = 0.05 s: B's radar started tracking track_006, which appeared on its left.
- t = 0.05 s: B's radar started tracking track_005, which appeared on its right.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 2.20 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 3.65 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 6.35 s: B's radar started tracking track_008, which appeared on its right.
- t = 6.40 s: B's radar started tracking track_009, which appeared on its left.
- t = 6.60 s: B's radar started tracking track_010, which appeared in front of it.
- t = 7.00 s: B's time-to-contact with track_002 became critical.
- t = 7.05 s: B observed track_002 start closing in.
- t = 7.75 s: B's collision sensor recorded a contact (peak impulse 255 N*s).
- t = 7.75 s: B's time-to-contact with track_002 stopped being critical.
- t = 7.75 s: B observed track_002 stop closing in.
- t = 7.80 s: B released the accelerator.
- t = 7.85 s: B observed track_010 enter its forward path corridor.
- t = 8.00 s: B observed track_009 enter its forward path corridor.
- t = 8.85 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 9.20 s: B observed track_006 enter its forward path corridor.
- t = 9.20 s: B's time-to-contact with track_006 became critical.
- t = 9.35 s: B's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 9.60 s: B observed track_010 leave its forward path corridor.
- t = 9.60 s: B observed track_005 cutting in from the right.
- t = 10.55 s: B's time-to-contact with track_006 stopped being critical.
- t = 10.55 s: B observed track_006 leave its forward path corridor.
- t = 10.70 s: B's time-to-contact with track_005 became critical.
- t = 11.15 s: B observed track_005 enter its forward path corridor.
- t = 11.35 s: B's radar started tracking track_011, which appeared on its left.
- t = 11.65 s: B's radar lost track_011 (its states are UNKNOWN from then on, not ended).
