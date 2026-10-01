# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 559.752460680902 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 29; edges: 51 (PRECEDES 40, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e03 | 1.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e04 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e05 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e06 | 5.80 | MOVING_END | A | - | ego |  |
| A:e07 | 5.80 | STOP_START | A | - | ego |  |
| A:e08 | 10.95 | BRAKE_END | A | - | controls |  |
| A:e09 | 10.95 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e10 | 11.15 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e11 | 11.15 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e12 | 11.40 | STOP_END | A | - | ego |  |
| A:e13 | 11.40 | MOVING_START | A | - | ego |  |
| A:e14 | 11.80 | CLOSING_START | A | track_001 | radar |  |
| A:e15 | 11.80 | CLOSING_START | A | track_002 | radar |  |
| A:e16 | 12.00 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e17 | 12.15 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e18 | 12.20 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e19 | 12.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e20 | 12.70 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e21 | 12.75 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e22 | 13.50 | TRACK_LOST | A | track_002 | radar |  |
| A:e23 | 14.10 | COLLISION | A | - | collision_sensor | peak_impulse=9089.81 |
| A:e24 | 14.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e25 | 14.10 | CLOSING_END | A | track_001 | radar |  |
| A:e26 | 14.10 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e27 | 14.35 | TRACK_LOST | A | track_001 | radar |  |
| A:e28 | 14.65 | MOVING_END | A | - | ego |  |
| A:e29 | 14.65 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e10 --SAME_TRACK--> A:e14
    A:e11 --SAME_TRACK--> A:e15
    A:e11 --SAME_TRACK--> A:e16
    A:e10 --SAME_TRACK--> A:e17
    A:e10 --SAME_TRACK--> A:e18
    A:e10 --SAME_TRACK--> A:e19
    A:e11 --SAME_TRACK--> A:e21
    A:e11 --SAME_TRACK--> A:e22
    A:e10 --SAME_TRACK--> A:e24
    A:e10 --SAME_TRACK--> A:e25
    A:e10 --SAME_TRACK--> A:e27
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.70 | A:e02 STRONG_THROTTLE_START | ego: MOVING | 0.60 |
| 1.80 | A:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.70 |
| 3.95 | A:e04 BRAKE_START | ego: MOVING | 3.90 |
| 5.15 | A:e05 COLLISION | ego: MOVING, BRAKE | 5.10 |
| 5.80 | A:e06 MOVING_END<br>A:e07 STOP_START | ego: MOVING, BRAKE | 5.70 |
| 10.95 | A:e08 BRAKE_END<br>A:e09 STRONG_THROTTLE_START | ego: STOP, BRAKE | 10.90 |
| 11.15 | A:e10 TRACK_APPEARED track_001<br>A:e11 TRACK_APPEARED track_002 | ego: STOP, STRONG_THROTTLE | 11.10 |
| 11.40 | A:e12 STOP_END<br>A:e13 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE<br>track_002: VISIBLE | 11.30 |
| 11.80 | A:e14 CLOSING_START track_001<br>A:e15 CLOSING_START track_002 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE<br>track_002: VISIBLE | 11.70 |
| 12.00 | A:e16 EGO_PATH_ENTRY track_002 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 11.90 |
| 12.15 | A:e17 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH | 12.10 |
| 12.20 | A:e18 EGO_PATH_ENTRY track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH | 12.10 |
| 12.55 | A:e19 CRITICAL_TTC_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH | 12.50 |
| 12.70 | A:e20 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH | 12.60 |
| 12.75 | A:e21 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH | 12.70 |
| 13.50 | A:e22 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH | 13.40 |
| 14.10 | A:e23 COLLISION<br>A:e24 CRITICAL_TTC_END track_001<br>A:e25 CLOSING_END track_001<br>A:e26 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 14.00 |
| 14.35 | A:e27 TRACK_LOST track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 14.30 |
| 14.65 | A:e28 MOVING_END<br>A:e29 STOP_START | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 | 14.60 |

## States still active when observation ended

- CLOSING of track_002, since A:e15 (t = 11.80 s); the track was lost at 13.50 s
- EGO_PATH of track_002, since A:e16 (t = 12.00 s); the track was lost at 13.50 s
- PREDICTED_PATH_CONFLICT of track_001, since A:e17 (t = 12.15 s); the track was lost at 14.35 s
- EGO_PATH of track_001, since A:e18 (t = 12.20 s); the track was lost at 14.35 s
- CRITICAL_TTC of track_002, since A:e21 (t = 12.75 s); the track was lost at 13.50 s
- STRONG_THROTTLE, since A:e26 (t = 14.10 s)
- STOP, since A:e29 (t = 14.65 s)

## Tracks lost

- track_002 at 13.50 s (A:e22): CLOSING, CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 14.35 s (A:e27): IN_EGO_PATH, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 11.15 | 14.35 | 59 | 14.8 m / -13 deg | 0.01 m (14.25) | 0.1 m / +174 deg | 3.1 m/s |
| track_002 | 11.15 | 13.50 | 41 | 18.2 m / -8 deg | 8.22 m (13.50) | 8.2 m / +12 deg | 1.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A started applying strong throttle.
- t = 1.80 s: A stopped applying strong throttle.
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.80 s: A stopped moving.
- t = 5.80 s: A came to a stop.
- t = 10.95 s: A released the brake.
- t = 10.95 s: A started applying strong throttle.
- t = 11.15 s: A's radar started tracking track_001.
- t = 11.15 s: A's radar started tracking track_002.
- t = 11.40 s: A left its stop.
- t = 11.40 s: A started moving.
- t = 11.80 s: A observed track_001 start closing in.
- t = 11.80 s: A observed track_002 start closing in.
- t = 12.00 s: A observed track_002 enter its forward path corridor.
- t = 12.15 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 12.20 s: A observed track_001 enter its forward path corridor.
- t = 12.55 s: A's time-to-contact with track_001 became critical.
- t = 12.70 s: A stopped applying strong throttle.
- t = 12.75 s: A's time-to-contact with track_002 became critical.
- t = 13.50 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 14.10 s: A's collision sensor recorded a contact (peak impulse 9090 N*s).
- t = 14.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 14.10 s: A observed track_001 stop closing in.
- t = 14.10 s: A started applying strong throttle.
- t = 14.35 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 14.65 s: A stopped moving.
- t = 14.65 s: A came to a stop.
