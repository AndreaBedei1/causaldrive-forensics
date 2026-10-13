# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 568.7781397588551 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 7 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 29; edges: 53 (PRECEDES 38, SAME_TRACK 15)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_002 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_001 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_LEFT | B | track_003 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_LEFT | B | track_004 | radar | initial_in_ego_path=False |
| B:e07 | 0.00 | TRACK_APPEARED_RIGHT | B | track_005 | radar | initial_in_ego_path=False |
| B:e08 | 0.50 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e09 | 7.75 | COLLISION | B | - | collision_sensor | peak_impulse=1897.70 |
| B:e10 | 7.75 | THROTTLE_END | B | - | controls |  |
| B:e11 | 7.80 | BRAKE_START | B | - | controls |  |
| B:e12 | 8.25 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e13 | 9.00 | MOVING_END | B | - | ego |  |
| B:e14 | 9.00 | STOP_START | B | - | ego |  |
| B:e15 | 9.40 | TRACK_APPEARED_LEFT | B | track_006 | radar | initial_in_ego_path=False |
| B:e16 | 9.40 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e17 | 9.50 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e18 | 9.50 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e19 | 9.90 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e20 | 10.00 | CRITICAL_TTC_START | B | track_007 | radar |  |
| B:e21 | 10.25 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e22 | 10.25 | TRACK_LOST | B | track_003 | radar |  |
| B:e23 | 10.30 | CRITICAL_TTC_END | B | track_007 | radar |  |
| B:e24 | 10.30 | CLOSING_END | B | track_006 | radar |  |
| B:e25 | 10.35 | CLOSING_END | B | track_007 | radar |  |
| B:e26 | 10.65 | EGO_PATH_EXIT | B | track_002 | radar | geometry=estimated_body |
| B:e27 | 10.65 | CUT_IN_FROM_RIGHT_START | B | track_005 | radar | geometry=estimated_body |
| B:e28 | 11.00 | EGO_PATH_ENTRY | B | track_005 | radar | geometry=estimated_body |
| B:e29 | 11.25 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e03 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e12
    B:e15 --SAME_TRACK--> B:e16
    B:e17 --SAME_TRACK--> B:e18
    B:e15 --SAME_TRACK--> B:e19
    B:e17 --SAME_TRACK--> B:e20
    B:e15 --SAME_TRACK--> B:e21
    B:e05 --SAME_TRACK--> B:e22
    B:e17 --SAME_TRACK--> B:e23
    B:e15 --SAME_TRACK--> B:e24
    B:e17 --SAME_TRACK--> B:e25
    B:e03 --SAME_TRACK--> B:e26
    B:e07 --SAME_TRACK--> B:e27
    B:e07 --SAME_TRACK--> B:e28
    B:e04 --SAME_TRACK--> B:e29
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_002<br>B:e04 TRACK_APPEARED_LEFT track_001<br>B:e05 TRACK_APPEARED_LEFT track_003<br>B:e06 TRACK_APPEARED_LEFT track_004<br>B:e07 TRACK_APPEARED_RIGHT track_005 | ego: not yet observed | - |
| 0.50 | B:e08 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.40 |
| 7.75 | B:e09 COLLISION<br>B:e10 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 7.70 |
| 7.80 | B:e11 BRAKE_START | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 7.70 |
| 8.25 | B:e12 CRITICAL_TTC_END track_002 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 8.20 |
| 9.00 | B:e13 MOVING_END<br>B:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 8.90 |
| 9.40 | B:e15 TRACK_APPEARED_LEFT track_006<br>B:e16 CLOSING_START track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 9.30 |
| 9.50 | B:e17 TRACK_APPEARED_RIGHT track_007<br>B:e18 CLOSING_START track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC? | 9.40 |
| 9.90 | B:e19 CRITICAL_TTC_START track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC?<br>track_007: CLOSING, CRITICAL_TTC? | 9.80 |
| 10.00 | B:e20 CRITICAL_TTC_START track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC? | 9.90 |
| 10.25 | B:e21 CRITICAL_TTC_END track_006<br>B:e22 TRACK_LOST track_003 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC | 10.20 |
| 10.30 | B:e23 CRITICAL_TTC_END track_007<br>B:e24 CLOSING_END track_006 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_003 | 10.20 |
| 10.35 | B:e25 CLOSING_END track_007 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003 | 10.30 |
| 10.65 | B:e26 EGO_PATH_EXIT track_002<br>B:e27 CUT_IN_FROM_RIGHT_START track_005 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 | 10.60 |
| 11.00 | B:e28 EGO_PATH_ENTRY track_005 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 | 10.90 |
| 11.25 | B:e29 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 | 11.20 |

## States still active when observation ended

- BRAKE, since B:e11 (t = 7.80 s)
- STOP, since B:e14 (t = 9.00 s)
- CUT_IN_FROM_RIGHT of track_005, since B:e27 (t = 10.65 s)
- EGO_PATH of track_005, since B:e28 (t = 11.00 s)

## Tracks lost

- lost with no state active: track_003, track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s)
- track_005: CUT_IN_FROM_RIGHT_START 10.65, no critical TTC after it; EGO_PATH_ENTRY 11.00, no critical TTC
- track_006: CRITICAL_TTC_START 9.90
- track_007: CRITICAL_TTC_START 10.00

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.25 | 175 | 17.7 m / -7 deg | 17.18 m (8.00) | 45.2 m / -8 deg | 11.4 m/s |
| track_002 | 0.00 | 11.95 | 240 | 13.6 m / +0 deg | 13.16 m (3.30) | 49.7 m / -8 deg | 11.1 m/s |
| track_003 | 0.00 | 10.25 | 192 | 16.1 m / -10 deg | 15.92 m (8.00) | 33.9 m / -9 deg | 11.2 m/s |
| track_004 | 0.00 | 11.95 | 240 | 1.5 m / -78 deg | 1.32 m (8.05) | 33.3 m / -9 deg | 11.1 m/s |
| track_005 | 0.00 | 11.95 | 240 | 1.4 m / +101 deg | 1.29 m (8.70) | 30.7 m / +2 deg | 11.2 m/s |
| track_006 | 9.40 | 11.95 | 52 | 9.2 m / -152 deg | 1.03 m (10.35) | 14.0 m / -12 deg | 11.1 m/s |
| track_007 | 9.50 | 11.95 | 50 | 8.8 m / +151 deg | 1.10 m (10.45) | 13.2 m / +12 deg | 10.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_002, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_005, which appeared on its right.
- t = 0.50 s: B's time-to-contact with track_002 became critical.
- t = 7.75 s: B's collision sensor recorded a contact (peak impulse 1898 N*s).
- t = 7.75 s: B released the accelerator.
- t = 7.80 s: B started braking.
- t = 8.25 s: B's time-to-contact with track_002 stopped being critical.
- t = 9.00 s: B stopped moving.
- t = 9.00 s: B came to a stop.
- t = 9.40 s: B's radar started tracking track_006, which appeared on its left.
- t = 9.40 s: B observed track_006 start closing in (already the case when first observed).
- t = 9.50 s: B's radar started tracking track_007, which appeared on its right.
- t = 9.50 s: B observed track_007 start closing in (already the case when first observed).
- t = 9.90 s: B's time-to-contact with track_006 became critical.
- t = 10.00 s: B's time-to-contact with track_007 became critical.
- t = 10.25 s: B's time-to-contact with track_006 stopped being critical.
- t = 10.25 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 10.30 s: B's time-to-contact with track_007 stopped being critical.
- t = 10.30 s: B observed track_006 stop closing in.
- t = 10.35 s: B observed track_007 stop closing in.
- t = 10.65 s: B observed track_002 leave its forward path corridor.
- t = 10.65 s: B observed track_005 cutting in from the right.
- t = 11.00 s: B observed track_005 enter its forward path corridor.
- t = 11.25 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
