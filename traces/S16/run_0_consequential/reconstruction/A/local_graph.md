# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 544.6900767125189 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 23; edges: 44 (PRECEDES 33, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e03 | 1.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e04 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e05 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e06 | 5.15 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e07 | 5.15 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e08 | 5.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e09 | 5.15 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e10 | 5.15 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e11 | 5.20 | BRAKE_END | A | - | controls |  |
| A:e12 | 5.50 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e13 | 5.55 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e14 | 5.60 | CLOSING_END | A | track_002 | radar |  |
| A:e15 | 5.65 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e16 | 5.65 | TRACK_LOST | A | track_002 | radar |  |
| A:e17 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=2695.68 |
| A:e18 | 6.00 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e19 | 6.00 | CLOSING_END | A | track_001 | radar |  |
| A:e20 | 6.05 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e21 | 6.05 | MOVING_END | A | - | ego |  |
| A:e22 | 6.05 | STOP_START | A | - | ego |  |
| A:e23 | 6.20 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e09
    A:e04 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e11
    A:e06 --PRECEDES--> A:e11
    A:e07 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e22
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e23
    A:e06 --SAME_TRACK--> A:e08
    A:e07 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
    A:e06 --SAME_TRACK--> A:e12
    A:e07 --SAME_TRACK--> A:e14
    A:e06 --SAME_TRACK--> A:e15
    A:e07 --SAME_TRACK--> A:e16
    A:e06 --SAME_TRACK--> A:e18
    A:e06 --SAME_TRACK--> A:e19
    A:e06 --SAME_TRACK--> A:e20
    A:e13 --SAME_TRACK--> A:e23
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.70 | A:e02 STRONG_THROTTLE_START | ego: MOVING | 0.60 |
| 1.80 | A:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.70 |
| 3.95 | A:e04 BRAKE_START | ego: MOVING | 3.90 |
| 5.15 | A:e05 COLLISION<br>A:e06 TRACK_APPEARED track_001<br>A:e07 TRACK_APPEARED track_002<br>A:e08 CLOSING_START track_001<br>A:e09 CLOSING_START track_002<br>A:e10 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE | 5.10 |
| 5.20 | A:e11 BRAKE_END | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 5.10 |
| 5.50 | A:e12 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 5.40 |
| 5.55 | A:e13 TRACK_APPEARED track_003 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING | 5.50 |
| 5.60 | A:e14 CLOSING_END track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE | 5.50 |
| 5.65 | A:e15 EGO_PATH_ENTRY track_001<br>A:e16 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>track_002: VISIBLE<br>track_003: VISIBLE | 5.60 |
| 5.90 | A:e17 COLLISION | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_002 | 5.80 |
| 6.00 | A:e18 CRITICAL_TTC_END track_001<br>A:e19 CLOSING_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_002 | 5.90 |
| 6.05 | A:e20 PREDICTED_PATH_CONFLICT_END track_001<br>A:e21 MOVING_END<br>A:e22 STOP_START | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_002 | 6.00 |
| 6.20 | A:e23 TRACK_LOST track_003 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_002 | 6.10 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e15 (t = 5.65 s)
- STOP, since A:e22 (t = 6.05 s)

## Tracks lost

- lost with no state active: track_002, track_003

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.15 | 9.95 | 91 | 5.6 m / -39 deg | 0.78 m (6.05) | 1.4 m / -14 deg | 1.9 m/s |
| track_002 | 5.15 | 5.65 | 5 | 15.6 m / +41 deg | 14.36 m (5.50) | 14.6 m / +61 deg | 6.2 m/s |
| track_003 | 5.55 | 6.20 | 8 | 19.5 m / +43 deg | 19.46 m (5.55) | 20.0 m / +60 deg | 4.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A started applying strong throttle.
- t = 1.80 s: A stopped applying strong throttle.
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.15 s: A's radar started tracking track_001.
- t = 5.15 s: A's radar started tracking track_002.
- t = 5.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 5.15 s: A observed track_002 start closing in (already the case when first observed).
- t = 5.15 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 5.20 s: A released the brake.
- t = 5.50 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 5.55 s: A's radar started tracking track_003.
- t = 5.60 s: A observed track_002 stop closing in.
- t = 5.65 s: A observed track_001 enter its forward path corridor.
- t = 5.65 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 2696 N*s).
- t = 6.00 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.00 s: A observed track_001 stop closing in.
- t = 6.05 s: A stopped predicting a path conflict with track_001.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
- t = 6.20 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
