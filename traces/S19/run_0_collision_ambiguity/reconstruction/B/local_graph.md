# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 568.7781397588551 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 6 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 47 (PRECEDES 34, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e06 | 0.10 | TRACK_APPEARED_LEFT | B | track_004 | radar | initial_in_ego_path=False |
| B:e07 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 7.75 | COLLISION | B | - | collision_sensor | peak_impulse=1897.70 |
| B:e09 | 7.75 | THROTTLE_END | B | - | controls |  |
| B:e10 | 7.80 | BRAKE_START | B | - | controls |  |
| B:e11 | 8.25 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e12 | 9.00 | MOVING_END | B | - | ego |  |
| B:e13 | 9.00 | STOP_START | B | - | ego |  |
| B:e14 | 9.40 | TRACK_APPEARED_LEFT | B | track_005 | radar | initial_in_ego_path=False |
| B:e15 | 9.40 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e16 | 9.50 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e17 | 9.50 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e18 | 9.90 | CRITICAL_TTC_START | B | track_005 | radar |  |
| B:e19 | 10.00 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e20 | 10.25 | CRITICAL_TTC_END | B | track_005 | radar |  |
| B:e21 | 10.25 | TRACK_LOST | B | track_004 | radar |  |
| B:e22 | 10.30 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e23 | 10.30 | CLOSING_END | B | track_005 | radar |  |
| B:e24 | 10.40 | CLOSING_END | B | track_006 | radar |  |
| B:e25 | 10.65 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e26 | 10.90 | EGO_PATH_ENTRY | B | track_003 | radar | geometry=estimated_body |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e03 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e11
    B:e14 --SAME_TRACK--> B:e15
    B:e16 --SAME_TRACK--> B:e17
    B:e14 --SAME_TRACK--> B:e18
    B:e16 --SAME_TRACK--> B:e19
    B:e14 --SAME_TRACK--> B:e20
    B:e06 --SAME_TRACK--> B:e21
    B:e16 --SAME_TRACK--> B:e22
    B:e14 --SAME_TRACK--> B:e23
    B:e16 --SAME_TRACK--> B:e24
    B:e03 --SAME_TRACK--> B:e25
    B:e05 --SAME_TRACK--> B:e26
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_LEFT track_002<br>B:e05 TRACK_APPEARED_RIGHT track_003 | ego: not yet observed | - |
| 0.10 | B:e06 TRACK_APPEARED_LEFT track_004 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.00 |
| 0.50 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.40 |
| 7.75 | B:e08 COLLISION<br>B:e09 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 7.70 |
| 7.80 | B:e10 BRAKE_START | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 7.70 |
| 8.25 | B:e11 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 8.20 |
| 9.00 | B:e12 MOVING_END<br>B:e13 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 8.90 |
| 9.40 | B:e14 TRACK_APPEARED_LEFT track_005<br>B:e15 CLOSING_START track_005 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 9.30 |
| 9.50 | B:e16 TRACK_APPEARED_RIGHT track_006<br>B:e17 CLOSING_START track_006 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? | 9.40 |
| 9.90 | B:e18 CRITICAL_TTC_START track_005 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? | 9.80 |
| 10.00 | B:e19 CRITICAL_TTC_START track_006 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING, CRITICAL_TTC? | 9.90 |
| 10.25 | B:e20 CRITICAL_TTC_END track_005<br>B:e21 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING, CRITICAL_TTC | 10.20 |
| 10.30 | B:e22 CRITICAL_TTC_END track_006<br>B:e23 CLOSING_END track_005 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_004 | 10.20 |
| 10.40 | B:e24 CLOSING_END track_006 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_004 | 10.30 |
| 10.65 | B:e25 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004 | 10.60 |
| 10.90 | B:e26 EGO_PATH_ENTRY track_003 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004 | 10.80 |

## States still active when observation ended

- BRAKE, since B:e10 (t = 7.80 s)
- STOP, since B:e13 (t = 9.00 s)
- EGO_PATH of track_003, since B:e26 (t = 10.90 s)

## Tracks lost

- lost with no state active: track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s)
- track_003: EGO_PATH_ENTRY 10.90, no critical TTC
- track_005: CRITICAL_TTC_START 9.90
- track_006: CRITICAL_TTC_START 10.00

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 13.6 m / +0 deg | 13.16 m (3.30) | 49.7 m / -8 deg | 11.1 m/s |
| track_002 | 0.00 | 11.95 | 240 | 1.5 m / -80 deg | 1.31 m (8.05) | 33.3 m / -9 deg | 11.1 m/s |
| track_003 | 0.00 | 11.95 | 240 | 1.4 m / +99 deg | 1.28 m (8.70) | 30.8 m / +1 deg | 11.2 m/s |
| track_004 | 0.10 | 10.25 | 198 | 16.2 m / -10 deg | 15.99 m (8.00) | 33.9 m / -9 deg | 11.1 m/s |
| track_005 | 9.40 | 11.95 | 52 | 9.2 m / -152 deg | 1.07 m (10.35) | 14.0 m / -12 deg | 11.1 m/s |
| track_006 | 9.50 | 11.95 | 50 | 8.9 m / +151 deg | 1.13 m (10.45) | 13.2 m / +12 deg | 10.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.10 s: B's radar started tracking track_004, which appeared on its left.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 7.75 s: B's collision sensor recorded a contact (peak impulse 1898 N*s).
- t = 7.75 s: B released the accelerator.
- t = 7.80 s: B started braking.
- t = 8.25 s: B's time-to-contact with track_001 stopped being critical.
- t = 9.00 s: B stopped moving.
- t = 9.00 s: B came to a stop.
- t = 9.40 s: B's radar started tracking track_005, which appeared on its left.
- t = 9.40 s: B observed track_005 start closing in (already the case when first observed).
- t = 9.50 s: B's radar started tracking track_006, which appeared on its right.
- t = 9.50 s: B observed track_006 start closing in (already the case when first observed).
- t = 9.90 s: B's time-to-contact with track_005 became critical.
- t = 10.00 s: B's time-to-contact with track_006 became critical.
- t = 10.25 s: B's time-to-contact with track_005 stopped being critical.
- t = 10.25 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 10.30 s: B's time-to-contact with track_006 stopped being critical.
- t = 10.30 s: B observed track_005 stop closing in.
- t = 10.40 s: B observed track_006 stop closing in.
- t = 10.65 s: B observed track_001 leave its forward path corridor.
- t = 10.90 s: B observed track_003 enter its forward path corridor.
