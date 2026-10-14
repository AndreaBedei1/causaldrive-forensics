# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 184.6674646884203 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 10 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 42; edges: 68 (PRECEDES 45, SAME_TRACK 23)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_002 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_005 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | TRACK_APPEARED_RIGHT | A | track_003 | radar | initial_in_ego_path=False |
| A:e08 | 0.00 | TRACK_APPEARED_RIGHT | A | track_004 | radar | initial_in_ego_path=False |
| A:e09 | 0.00 | TRACK_APPEARED_RIGHT | A | track_007 | radar | initial_in_ego_path=False |
| A:e10 | 0.50 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e11 | 5.95 | THROTTLE_END | A | - | controls |  |
| A:e12 | 5.95 | BRAKE_START | A | - | controls |  |
| A:e13 | 6.25 | CLOSING_START | A | track_006 | radar |  |
| A:e14 | 6.35 | CLOSING_START | A | track_007 | radar |  |
| A:e15 | 6.55 | CRITICAL_TTC_START | A | track_006 | radar |  |
| A:e16 | 6.55 | CRITICAL_TTC_START | A | track_007 | radar |  |
| A:e17 | 6.80 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e18 | 7.05 | CRITICAL_TTC_END | A | track_007 | radar |  |
| A:e19 | 7.10 | CLOSING_END | A | track_007 | radar |  |
| A:e20 | 7.15 | MOVING_END | A | - | ego |  |
| A:e21 | 7.15 | STOP_START | A | - | ego |  |
| A:e22 | 7.20 | CRITICAL_TTC_END | A | track_006 | radar |  |
| A:e23 | 7.25 | CLOSING_END | A | track_006 | radar |  |
| A:e24 | 7.45 | COLLISION | A | - | collision_sensor | peak_impulse=34836.87 |
| A:e25 | 7.50 | BRAKE_END | A | - | controls |  |
| A:e26 | 7.90 | TRACK_APPEARED_FRONT | A | track_008 | radar | initial_in_ego_path=True |
| A:e27 | 8.00 | BRAKE_START | A | - | controls |  |
| A:e28 | 8.25 | EGO_PATH_ENTRY | A | track_004 | radar | geometry=estimated_body |
| A:e29 | 8.95 | TRACK_LOST | A | track_005 | radar |  |
| A:e30 | 9.25 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e31 | 9.50 | EGO_PATH_ENTRY | A | track_003 | radar | geometry=estimated_body |
| A:e32 | 9.55 | TRACK_LOST | A | track_001 | radar |  |
| A:e33 | 10.25 | TRACK_LOST | A | track_008 | radar |  |
| A:e34 | 10.50 | EGO_PATH_ENTRY | A | track_007 | radar | geometry=estimated_body |
| A:e35 | 10.55 | EGO_PATH_EXIT | A | track_002 | radar | geometry=estimated_body |
| A:e36 | 10.70 | TRACK_APPEARED_LEFT | A | track_009 | radar | initial_in_ego_path=False |
| A:e37 | 10.95 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e38 | 10.95 | TRACK_LOST | A | track_009 | radar |  |
| A:e39 | 11.00 | EGO_PATH_EXIT | A | track_004 | radar | geometry=estimated_body |
| A:e40 | 11.85 | TRACK_LOST | A | track_002 | radar |  |
| A:e41 | 11.90 | EGO_PATH_EXIT | A | track_003 | radar | geometry=estimated_body |
| A:e42 | 11.90 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e10
    A:e02 --PRECEDES--> A:e10
    A:e03 --PRECEDES--> A:e10
    A:e04 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e10
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e31 --PRECEDES--> A:e32
    A:e32 --PRECEDES--> A:e33
    A:e33 --PRECEDES--> A:e34
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e03 --SAME_TRACK--> A:e10
    A:e06 --SAME_TRACK--> A:e13
    A:e09 --SAME_TRACK--> A:e14
    A:e06 --SAME_TRACK--> A:e15
    A:e09 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e17
    A:e09 --SAME_TRACK--> A:e18
    A:e09 --SAME_TRACK--> A:e19
    A:e06 --SAME_TRACK--> A:e22
    A:e06 --SAME_TRACK--> A:e23
    A:e08 --SAME_TRACK--> A:e28
    A:e05 --SAME_TRACK--> A:e29
    A:e26 --SAME_TRACK--> A:e30
    A:e07 --SAME_TRACK--> A:e31
    A:e04 --SAME_TRACK--> A:e32
    A:e26 --SAME_TRACK--> A:e33
    A:e09 --SAME_TRACK--> A:e34
    A:e03 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e38
    A:e08 --SAME_TRACK--> A:e39
    A:e03 --SAME_TRACK--> A:e40
    A:e07 --SAME_TRACK--> A:e41
    A:e07 --SAME_TRACK--> A:e42
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_002<br>A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 TRACK_APPEARED_LEFT track_005<br>A:e06 TRACK_APPEARED_LEFT track_006<br>A:e07 TRACK_APPEARED_RIGHT track_003<br>A:e08 TRACK_APPEARED_RIGHT track_004<br>A:e09 TRACK_APPEARED_RIGHT track_007 | ego: not yet observed | - |
| 0.50 | A:e10 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? | 0.40 |
| 5.95 | A:e11 THROTTLE_END<br>A:e12 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 5.90 |
| 6.25 | A:e13 CLOSING_START track_006 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 6.20 |
| 6.35 | A:e14 CLOSING_START track_007 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: no active state | 6.30 |
| 6.55 | A:e15 CRITICAL_TTC_START track_006<br>A:e16 CRITICAL_TTC_START track_007 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING | 6.50 |
| 6.80 | A:e17 CRITICAL_TTC_END track_002 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC | 6.70 |
| 7.05 | A:e18 CRITICAL_TTC_END track_007 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC | 7.00 |
| 7.10 | A:e19 CLOSING_END track_007 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING | 7.00 |
| 7.15 | A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: no active state | 7.10 |
| 7.20 | A:e22 CRITICAL_TTC_END track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: no active state | 7.10 |
| 7.25 | A:e23 CLOSING_END track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: no active state | 7.20 |
| 7.45 | A:e24 COLLISION | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 7.40 |
| 7.50 | A:e25 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 7.40 |
| 7.90 | A:e26 TRACK_APPEARED_FRONT track_008 | ego: STOP<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state | 7.80 |
| 8.00 | A:e27 BRAKE_START | ego: STOP<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC? | 7.90 |
| 8.25 | A:e28 EGO_PATH_ENTRY track_004 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC? | 8.20 |
| 8.95 | A:e29 TRACK_LOST track_005 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: IN_EGO_PATH<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH | 8.90 |
| 9.25 | A:e30 EGO_PATH_EXIT track_008 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 | 9.20 |
| 9.50 | A:e31 EGO_PATH_ENTRY track_003 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_005 | 9.40 |
| 9.55 | A:e32 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_005 | 9.50 |
| 10.25 | A:e33 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_005 | 10.20 |
| 10.50 | A:e34 EGO_PATH_ENTRY track_007 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_001, track_005, track_008 | 10.40 |
| 10.55 | A:e35 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005, track_008 | 10.50 |
| 10.70 | A:e36 TRACK_APPEARED_LEFT track_009 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005, track_008 | 10.60 |
| 10.95 | A:e37 TRACK_APPEARED_LEFT track_010<br>A:e38 TRACK_LOST track_009 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_009: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_005, track_008 | 10.90 |
| 11.00 | A:e39 EGO_PATH_EXIT track_004 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_005, track_008, track_009 | 10.90 |
| 11.85 | A:e40 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_005, track_008, track_009 | 11.80 |
| 11.90 | A:e41 EGO_PATH_EXIT track_003<br>A:e42 TRACK_LOST track_003 | ego: STOP, BRAKE<br>track_003: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_005, track_008, track_009 | 11.80 |

## States still active when observation ended

- STOP, since A:e21 (t = 7.15 s)
- BRAKE, since A:e27 (t = 8.00 s)
- EGO_PATH of track_007, since A:e34 (t = 10.50 s)

## Tracks lost

- track_003 at 11.90 s (A:e42): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_001, track_008, track_009, track_002

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 0.50, COLLISION 7.45 (+6.95 s)
- track_003: EGO_PATH_ENTRY 9.50, no critical TTC
- track_004: EGO_PATH_ENTRY 8.25, no critical TTC
- track_006: CRITICAL_TTC_START 6.55, COLLISION 7.45 (+0.90 s)
- track_007: CRITICAL_TTC_START 6.55, COLLISION 7.45 (+0.90 s); EGO_PATH_ENTRY 10.50 after critical TTC (+3.95 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 9.55 | 190 | 3.3 m / -34 deg | 3.02 m (4.80) | 35.2 m / -5 deg | 12.2 m/s |
| track_002 | 0.00 | 11.85 | 229 | 7.8 m / +0 deg | 7.20 m (4.10) | 68.2 m / -6 deg | 12.1 m/s |
| track_003 | 0.00 | 11.90 | 239 | 5.1 m / +28 deg | 5.08 m (0.00) | 65.4 m / -3 deg | 12.3 m/s |
| track_004 | 0.00 | 11.95 | 229 | 16.1 m / +10 deg | 16.13 m (0.35) | 76.8 m / -6 deg | 12.2 m/s |
| track_005 | 0.00 | 8.95 | 173 | 14.1 m / -10 deg | 14.11 m (0.35) | 40.5 m / -5 deg | 12.1 m/s |
| track_006 | 0.00 | 11.95 | 240 | 4.6 m / -141 deg | 0.92 m (7.25) | 53.0 m / -8 deg | 12.1 m/s |
| track_007 | 0.00 | 11.95 | 240 | 2.6 m / +128 deg | 0.90 m (7.15) | 53.3 m / -0 deg | 12.1 m/s |
| track_008 | 7.90 | 10.25 | 46 | 34.3 m / -2 deg | 34.34 m (7.90) | 61.9 m / -5 deg | 11.9 m/s |
| track_009 | 10.70 | 10.95 | 6 | 61.9 m / -10 deg | 61.91 m (10.70) | 64.8 m / -9 deg | 11.9 m/s |
| track_010 | 10.95 | 11.95 | 17 | 52.5 m / -8 deg | 52.45 m (10.95) | 64.3 m / -9 deg | 12.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_005, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_007, which appeared on its right.
- t = 0.50 s: A's time-to-contact with track_002 became critical.
- t = 5.95 s: A released the accelerator.
- t = 5.95 s: A started braking.
- t = 6.25 s: A observed track_006 start closing in.
- t = 6.35 s: A observed track_007 start closing in.
- t = 6.55 s: A's time-to-contact with track_006 became critical.
- t = 6.55 s: A's time-to-contact with track_007 became critical.
- t = 6.80 s: A's time-to-contact with track_002 stopped being critical.
- t = 7.05 s: A's time-to-contact with track_007 stopped being critical.
- t = 7.10 s: A observed track_007 stop closing in.
- t = 7.15 s: A stopped moving.
- t = 7.15 s: A came to a stop.
- t = 7.20 s: A's time-to-contact with track_006 stopped being critical.
- t = 7.25 s: A observed track_006 stop closing in.
- t = 7.45 s: A's collision sensor recorded a contact (peak impulse 34837 N*s).
- t = 7.50 s: A released the brake.
- t = 7.90 s: A's radar started tracking track_008, which appeared in front of it.
- t = 8.00 s: A started braking.
- t = 8.25 s: A observed track_004 enter its forward path corridor.
- t = 8.95 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 9.25 s: A observed track_008 leave its forward path corridor.
- t = 9.50 s: A observed track_003 enter its forward path corridor.
- t = 9.55 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 10.25 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 10.50 s: A observed track_007 enter its forward path corridor.
- t = 10.55 s: A observed track_002 leave its forward path corridor.
- t = 10.70 s: A's radar started tracking track_009, which appeared on its left.
- t = 10.95 s: A's radar started tracking track_010, which appeared on its left.
- t = 10.95 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 11.00 s: A observed track_004 leave its forward path corridor.
- t = 11.85 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 11.90 s: A observed track_003 leave its forward path corridor.
- t = 11.90 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
