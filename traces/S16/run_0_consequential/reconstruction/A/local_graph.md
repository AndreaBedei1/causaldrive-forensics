# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 196.7230779863894 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 6 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 27; edges: 55 (PRECEDES 43, SAME_TRACK 12)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e03 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e04 | 5.15 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 5.15 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e06 | 5.15 | TRACK_APPEARED_RIGHT | A | track_003 | radar |  |
| A:e07 | 5.15 | TRACK_APPEARED_RIGHT | A | track_004 | radar |  |
| A:e08 | 5.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e09 | 5.15 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e10 | 5.15 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e11 | 5.15 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e12 | 5.15 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e13 | 5.20 | BRAKE_END | A | - | controls |  |
| A:e14 | 5.40 | TURN_LEFT_START | A | - | ego |  |
| A:e15 | 5.45 | CLOSING_END | A | track_002 | radar |  |
| A:e16 | 5.45 | CLOSING_END | A | track_003 | radar |  |
| A:e17 | 5.50 | TRACK_APPEARED_RIGHT | A | track_005 | radar |  |
| A:e18 | 5.50 | TRACK_APPEARED_RIGHT | A | track_006 | radar |  |
| A:e19 | 5.70 | CLOSING_END | A | track_004 | radar |  |
| A:e20 | 5.70 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e21 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=2695.68 |
| A:e22 | 5.95 | TRACK_LOST | A | track_005 | radar |  |
| A:e23 | 6.00 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e24 | 6.00 | TURN_LEFT_END | A | - | ego |  |
| A:e25 | 6.05 | CLOSING_END | A | track_001 | radar |  |
| A:e26 | 6.05 | MOVING_END | A | - | ego |  |
| A:e27 | 6.05 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e08
    A:e02 --PRECEDES--> A:e09
    A:e02 --PRECEDES--> A:e10
    A:e02 --PRECEDES--> A:e11
    A:e02 --PRECEDES--> A:e12
    A:e03 --PRECEDES--> A:e13
    A:e04 --PRECEDES--> A:e13
    A:e05 --PRECEDES--> A:e13
    A:e06 --PRECEDES--> A:e13
    A:e07 --PRECEDES--> A:e13
    A:e08 --PRECEDES--> A:e13
    A:e09 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e04 --SAME_TRACK--> A:e08
    A:e05 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
    A:e07 --SAME_TRACK--> A:e11
    A:e04 --SAME_TRACK--> A:e12
    A:e05 --SAME_TRACK--> A:e15
    A:e06 --SAME_TRACK--> A:e16
    A:e07 --SAME_TRACK--> A:e19
    A:e04 --SAME_TRACK--> A:e20
    A:e17 --SAME_TRACK--> A:e22
    A:e04 --SAME_TRACK--> A:e23
    A:e04 --SAME_TRACK--> A:e25
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 3.95 | A:e02 BRAKE_START | ego: MOVING | 3.90 |
| 5.15 | A:e03 COLLISION<br>A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 TRACK_APPEARED_RIGHT track_002<br>A:e06 TRACK_APPEARED_RIGHT track_003<br>A:e07 TRACK_APPEARED_RIGHT track_004<br>A:e08 CLOSING_START track_001<br>A:e09 CLOSING_START track_002<br>A:e10 CLOSING_START track_003<br>A:e11 CLOSING_START track_004<br>A:e12 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE | 5.10 |
| 5.20 | A:e13 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING | 5.10 |
| 5.40 | A:e14 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING | 5.30 |
| 5.45 | A:e15 CLOSING_END track_002<br>A:e16 CLOSING_END track_003 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING | 5.40 |
| 5.50 | A:e17 TRACK_APPEARED_RIGHT track_005<br>A:e18 TRACK_APPEARED_RIGHT track_006 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING | 5.40 |
| 5.70 | A:e19 CLOSING_END track_004<br>A:e20 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING<br>track_005: no active state<br>track_006: no active state | 5.60 |
| 5.90 | A:e21 COLLISION | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state | 5.80 |
| 5.95 | A:e22 TRACK_LOST track_005 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state | 5.90 |
| 6.00 | A:e23 CRITICAL_TTC_END track_001<br>A:e24 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 | 5.90 |
| 6.05 | A:e25 CLOSING_END track_001<br>A:e26 MOVING_END<br>A:e27 STOP_START | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 | 6.00 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e20 (t = 5.70 s)
- STOP, since A:e27 (t = 6.05 s)

## Tracks lost

- lost with no state active: track_005

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.15, COLLISION 5.15 (+0.00 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.15 | 9.95 | 92 | 4.7 m / -51 deg | 0.41 m (6.15) | 1.0 m / -53 deg | 2.8 m/s |
| track_002 | 5.15 | 9.95 | 91 | 15.9 m / +56 deg | 15.25 m (9.95) | 15.2 m / +73 deg | 9.1 m/s |
| track_003 | 5.15 | 9.95 | 78 | 13.5 m / +53 deg | 13.02 m (5.40) | 13.8 m / +80 deg | 7.1 m/s |
| track_004 | 5.15 | 9.95 | 90 | 21.7 m / +26 deg | 18.93 m (9.95) | 18.9 m / +61 deg | 1.5 m/s |
| track_005 | 5.50 | 5.95 | 10 | 14.2 m / +54 deg | 14.23 m (5.50) | 15.1 m / +73 deg | 6.2 m/s |
| track_006 | 5.50 | 9.95 | 88 | 19.0 m / +54 deg | 19.02 m (5.50) | 19.3 m / +73 deg | 3.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.15 s: A's radar started tracking track_001, which appeared on its left.
- t = 5.15 s: A's radar started tracking track_002, which appeared on its right.
- t = 5.15 s: A's radar started tracking track_003, which appeared on its right.
- t = 5.15 s: A's radar started tracking track_004, which appeared on its right.
- t = 5.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 5.15 s: A observed track_002 start closing in (already the case when first observed).
- t = 5.15 s: A observed track_003 start closing in (already the case when first observed).
- t = 5.15 s: A observed track_004 start closing in (already the case when first observed).
- t = 5.15 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 5.20 s: A released the brake.
- t = 5.40 s: A started turning left.
- t = 5.45 s: A observed track_002 stop closing in.
- t = 5.45 s: A observed track_003 stop closing in.
- t = 5.50 s: A's radar started tracking track_005, which appeared on its right.
- t = 5.50 s: A's radar started tracking track_006, which appeared on its right.
- t = 5.70 s: A observed track_004 stop closing in.
- t = 5.70 s: A observed track_001 enter its forward path corridor.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 2696 N*s).
- t = 5.95 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 6.00 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.00 s: A stopped turning left.
- t = 6.05 s: A observed track_001 stop closing in.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
