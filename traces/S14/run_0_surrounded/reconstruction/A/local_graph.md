# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 63.627261225134134 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 11 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 37; edges: 61 (PRECEDES 39, SAME_TRACK 22)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 | radar | initial_in_ego_path=True |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_LEFT | A | track_003 | radar | initial_in_ego_path=False |
| A:e06 | 0.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 4.45 | TRACK_APPEARED_LEFT | A | track_004 | radar | initial_in_ego_path=False |
| A:e08 | 6.35 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e09 | 6.75 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=False |
| A:e10 | 6.85 | TRACK_APPEARED_LEFT | A | track_005 | radar | initial_in_ego_path=True |
| A:e11 | 6.95 | CLOSING_START | A | track_003 | radar |  |
| A:e12 | 7.05 | TRACK_APPEARED_FRONT | A | track_007 | radar | initial_in_ego_path=True |
| A:e13 | 7.25 | TRACK_LOST | A | track_004 | radar |  |
| A:e14 | 7.35 | CRITICAL_TTC_START | A | track_005 | radar |  |
| A:e15 | 7.40 | TRACK_APPEARED_RIGHT | A | track_008 | radar | initial_in_ego_path=False |
| A:e16 | 7.45 | TRACK_LOST | A | track_006 | radar |  |
| A:e17 | 7.60 | EGO_PATH_EXIT | A | track_007 | radar | geometry=estimated_body |
| A:e18 | 7.60 | TRACK_APPEARED_RIGHT | A | track_009 | radar | initial_in_ego_path=True |
| A:e19 | 7.70 | TRACK_LOST | A | track_007 | radar |  |
| A:e20 | 7.75 | COLLISION | A | - | collision_sensor | peak_impulse=254.40 |
| A:e21 | 7.75 | CRITICAL_TTC_END | A | track_003 | radar |  |
| A:e22 | 7.80 | THROTTLE_END | A | - | controls |  |
| A:e23 | 7.85 | EGO_PATH_ENTRY | A | track_003 | radar | geometry=estimated_body |
| A:e24 | 7.90 | CLOSING_END | A | track_003 | radar |  |
| A:e25 | 8.45 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e26 | 9.05 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e27 | 9.05 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e28 | 9.10 | EGO_PATH_ENTRY | A | track_008 | radar | geometry=estimated_body |
| A:e29 | 9.15 | EGO_PATH_EXIT | A | track_009 | radar | geometry=estimated_body |
| A:e30 | 9.50 | TRACK_APPEARED_LEFT | A | track_011 | radar | initial_in_ego_path=False |
| A:e31 | 10.15 | CRITICAL_TTC_START | A | track_009 | radar |  |
| A:e32 | 10.25 | EGO_PATH_ENTRY | A | track_009 | radar | geometry=estimated_body |
| A:e33 | 10.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e34 | 11.00 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e35 | 11.15 | TRACK_LOST | A | track_011 | radar |  |
| A:e36 | 11.55 | EGO_PATH_EXIT | A | track_008 | radar | geometry=estimated_body |
| A:e37 | 11.60 | EGO_PATH_EXIT | A | track_005 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
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
    A:e03 --SAME_TRACK--> A:e06
    A:e05 --SAME_TRACK--> A:e08
    A:e05 --SAME_TRACK--> A:e11
    A:e07 --SAME_TRACK--> A:e13
    A:e10 --SAME_TRACK--> A:e14
    A:e09 --SAME_TRACK--> A:e16
    A:e12 --SAME_TRACK--> A:e17
    A:e12 --SAME_TRACK--> A:e19
    A:e05 --SAME_TRACK--> A:e21
    A:e05 --SAME_TRACK--> A:e23
    A:e05 --SAME_TRACK--> A:e24
    A:e03 --SAME_TRACK--> A:e26
    A:e03 --SAME_TRACK--> A:e27
    A:e15 --SAME_TRACK--> A:e28
    A:e18 --SAME_TRACK--> A:e29
    A:e18 --SAME_TRACK--> A:e31
    A:e18 --SAME_TRACK--> A:e32
    A:e03 --SAME_TRACK--> A:e33
    A:e03 --SAME_TRACK--> A:e34
    A:e30 --SAME_TRACK--> A:e35
    A:e15 --SAME_TRACK--> A:e36
    A:e10 --SAME_TRACK--> A:e37
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_FRONT track_001<br>A:e04 TRACK_APPEARED_LEFT track_002<br>A:e05 TRACK_APPEARED_LEFT track_003 | ego: not yet observed | - |
| 0.50 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.40 |
| 4.45 | A:e07 TRACK_APPEARED_LEFT track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state | 4.40 |
| 6.35 | A:e08 CRITICAL_TTC_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 6.30 |
| 6.75 | A:e09 TRACK_APPEARED_LEFT track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state | 6.70 |
| 6.85 | A:e10 TRACK_APPEARED_LEFT track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state<br>track_006: CRITICAL_TTC? | 6.80 |
| 6.95 | A:e11 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? | 6.90 |
| 7.05 | A:e12 TRACK_APPEARED_FRONT track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? | 7.00 |
| 7.25 | A:e13 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: IN_EGO_PATH, CRITICAL_TTC? | 7.20 |
| 7.35 | A:e14 CRITICAL_TTC_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 | 7.30 |
| 7.40 | A:e15 TRACK_APPEARED_RIGHT track_008 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 | 7.30 |
| 7.45 | A:e16 TRACK_LOST track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 | 7.40 |
| 7.60 | A:e17 EGO_PATH_EXIT track_007<br>A:e18 TRACK_APPEARED_RIGHT track_009 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006 | 7.50 |
| 7.70 | A:e19 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006 | 7.60 |
| 7.75 | A:e20 COLLISION<br>A:e21 CRITICAL_TTC_END track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 7.70 |
| 7.80 | A:e22 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 7.70 |
| 7.85 | A:e23 EGO_PATH_ENTRY track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 7.80 |
| 7.90 | A:e24 CLOSING_END track_003 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 7.80 |
| 8.45 | A:e25 TRACK_APPEARED_LEFT track_010 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 8.40 |
| 9.05 | A:e26 CRITICAL_TTC_END track_001<br>A:e27 EGO_PATH_EXIT track_001 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 9.00 |
| 9.10 | A:e28 EGO_PATH_ENTRY track_008 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 9.00 |
| 9.15 | A:e29 EGO_PATH_EXIT track_009 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 9.10 |
| 9.50 | A:e30 TRACK_APPEARED_LEFT track_011 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 9.40 |
| 10.15 | A:e31 CRITICAL_TTC_START track_009 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 10.10 |
| 10.25 | A:e32 EGO_PATH_ENTRY track_009 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 10.20 |
| 10.50 | A:e33 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 10.40 |
| 11.00 | A:e34 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CRITICAL_TTC<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 10.90 |
| 11.15 | A:e35 TRACK_LOST track_011 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 | 11.10 |
| 11.55 | A:e36 EGO_PATH_EXIT track_008 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007, track_011 | 11.50 |
| 11.60 | A:e37 EGO_PATH_EXIT track_005 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007, track_011 | 11.50 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CRITICAL_TTC of track_005, since A:e14 (t = 7.35 s)
- EGO_PATH of track_003, since A:e23 (t = 7.85 s)
- CRITICAL_TTC of track_009, since A:e31 (t = 10.15 s)
- EGO_PATH of track_009, since A:e32 (t = 10.25 s)
- CRITICAL_TTC of track_001, since A:e33 (t = 10.50 s)
- EGO_PATH of track_001, since A:e34 (t = 11.00 s)

## Tracks lost

- lost with no state active: track_004, track_006, track_007, track_011

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 11.00 after critical TTC (+10.50 s)
- track_003: CRITICAL_TTC_START 6.35, COLLISION 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s)
- track_005: CRITICAL_TTC_START 7.35, COLLISION 7.75 (+0.40 s)
- track_008: EGO_PATH_ENTRY 9.10, no critical TTC
- track_009: CRITICAL_TTC_START 10.15; EGO_PATH_ENTRY 10.25 after critical TTC (+0.10 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 3.1 m / +0 deg | 1.42 m (11.95) | 1.4 m / +6 deg | 12.2 m/s |
| track_002 | 0.00 | 11.95 | 240 | 12.3 m / -27 deg | 10.85 m (9.85) | 12.4 m / -31 deg | 12.4 m/s |
| track_003 | 0.00 | 11.95 | 240 | 2.9 m / -129 deg | 0.00 m (11.65) | 0.0 m / -90 deg | 12.4 m/s |
| track_004 | 4.45 | 7.25 | 55 | 12.9 m / -154 deg | 12.50 m (7.25) | 12.5 m / -149 deg | 12.2 m/s |
| track_005 | 6.85 | 11.95 | 103 | 10.5 m / -8 deg | 9.56 m (10.65) | 10.0 m / -18 deg | 12.1 m/s |
| track_006 | 6.75 | 7.45 | 10 | 20.9 m / -157 deg | 20.60 m (7.45) | 20.6 m / -156 deg | 11.8 m/s |
| track_007 | 7.05 | 7.70 | 14 | 42.0 m / -1 deg | 41.97 m (7.70) | 42.0 m / +5 deg | 12.4 m/s |
| track_008 | 7.40 | 11.95 | 89 | 26.4 m / +8 deg | 24.86 m (11.75) | 24.9 m / -11 deg | 12.1 m/s |
| track_009 | 7.60 | 11.95 | 88 | 11.3 m / +8 deg | 9.84 m (11.95) | 9.8 m / -5 deg | 12.0 m/s |
| track_010 | 8.45 | 11.95 | 66 | 27.0 m / -9 deg | 26.93 m (9.20) | 28.4 m / -26 deg | 12.1 m/s |
| track_011 | 9.50 | 11.15 | 26 | 41.9 m / -7 deg | 41.70 m (10.50) | 41.8 m / -16 deg | 12.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its left.
- t = 0.50 s: A's time-to-contact with track_001 became critical.
- t = 4.45 s: A's radar started tracking track_004, which appeared on its left.
- t = 6.35 s: A's time-to-contact with track_003 became critical.
- t = 6.75 s: A's radar started tracking track_006, which appeared on its left.
- t = 6.85 s: A's radar started tracking track_005, which appeared on its left.
- t = 6.95 s: A observed track_003 start closing in.
- t = 7.05 s: A's radar started tracking track_007, which appeared in front of it.
- t = 7.25 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 7.35 s: A's time-to-contact with track_005 became critical.
- t = 7.40 s: A's radar started tracking track_008, which appeared on its right.
- t = 7.45 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 7.60 s: A observed track_007 leave its forward path corridor.
- t = 7.60 s: A's radar started tracking track_009, which appeared on its right.
- t = 7.70 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 7.75 s: A's collision sensor recorded a contact (peak impulse 254 N*s).
- t = 7.75 s: A's time-to-contact with track_003 stopped being critical.
- t = 7.80 s: A released the accelerator.
- t = 7.85 s: A observed track_003 enter its forward path corridor.
- t = 7.90 s: A observed track_003 stop closing in.
- t = 8.45 s: A's radar started tracking track_010, which appeared on its left.
- t = 9.05 s: A's time-to-contact with track_001 stopped being critical.
- t = 9.05 s: A observed track_001 leave its forward path corridor.
- t = 9.10 s: A observed track_008 enter its forward path corridor.
- t = 9.15 s: A observed track_009 leave its forward path corridor.
- t = 9.50 s: A's radar started tracking track_011, which appeared on its left.
- t = 10.15 s: A's time-to-contact with track_009 became critical.
- t = 10.25 s: A observed track_009 enter its forward path corridor.
- t = 10.50 s: A's time-to-contact with track_001 became critical.
- t = 11.00 s: A observed track_001 enter its forward path corridor.
- t = 11.15 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 11.55 s: A observed track_008 leave its forward path corridor.
- t = 11.60 s: A observed track_005 leave its forward path corridor.
