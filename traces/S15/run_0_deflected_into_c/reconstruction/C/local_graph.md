# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 493.54037738218904 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 25; edges: 46 (PRECEDES 33, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED | C | track_001 | radar |  |
| C:e03 | 0.00 | TRACK_APPEARED | C | track_002 | radar |  |
| C:e04 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.00 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 0.45 | PREDICTED_PATH_CONFLICT_START | C | track_002 | radar |  |
| C:e07 | 1.65 | PREDICTED_PATH_CONFLICT_END | C | track_002 | radar |  |
| C:e08 | 1.65 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e09 | 2.10 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e10 | 2.25 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e11 | 2.50 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e12 | 3.15 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e13 | 4.45 | TRACK_LOST | C | track_002 | radar |  |
| C:e14 | 4.75 | COLLISION | C | - | collision_sensor | peak_impulse=1637.56 |
| C:e15 | 4.75 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e16 | 4.80 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e17 | 4.80 | BRAKE_START | C | - | controls |  |
| C:e18 | 4.80 | HARD_BRAKE_START | C | - | controls |  |
| C:e19 | 4.85 | PREDICTED_PATH_CONFLICT_START | C | track_001 | radar |  |
| C:e20 | 5.00 | EGO_PATH_ENTRY | C | track_001 | radar |  |
| C:e21 | 5.05 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e22 | 5.05 | CLOSING_END | C | track_001 | radar |  |
| C:e23 | 5.05 | MOVING_END | C | - | ego |  |
| C:e24 | 5.05 | STOP_START | C | - | ego |  |
| C:e25 | 5.20 | PREDICTED_PATH_CONFLICT_END | C | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e12 --PRECEDES--> C:e13
    C:e13 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e15
    C:e14 --PRECEDES--> C:e16
    C:e14 --PRECEDES--> C:e17
    C:e14 --PRECEDES--> C:e18
    C:e15 --PRECEDES--> C:e16
    C:e15 --PRECEDES--> C:e17
    C:e15 --PRECEDES--> C:e18
    C:e16 --PRECEDES--> C:e19
    C:e17 --PRECEDES--> C:e19
    C:e18 --PRECEDES--> C:e19
    C:e19 --PRECEDES--> C:e20
    C:e20 --PRECEDES--> C:e21
    C:e20 --PRECEDES--> C:e22
    C:e20 --PRECEDES--> C:e23
    C:e20 --PRECEDES--> C:e24
    C:e21 --PRECEDES--> C:e25
    C:e22 --PRECEDES--> C:e25
    C:e23 --PRECEDES--> C:e25
    C:e24 --PRECEDES--> C:e25
    C:e02 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e03 --SAME_TRACK--> C:e06
    C:e03 --SAME_TRACK--> C:e07
    C:e03 --SAME_TRACK--> C:e10
    C:e02 --SAME_TRACK--> C:e11
    C:e03 --SAME_TRACK--> C:e12
    C:e03 --SAME_TRACK--> C:e13
    C:e02 --SAME_TRACK--> C:e19
    C:e02 --SAME_TRACK--> C:e20
    C:e02 --SAME_TRACK--> C:e21
    C:e02 --SAME_TRACK--> C:e22
    C:e02 --SAME_TRACK--> C:e25
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED track_001<br>C:e03 TRACK_APPEARED track_002<br>C:e04 CLOSING_START track_001<br>C:e05 CLOSING_START track_002 | ego: not yet observed | - |
| 0.45 | C:e06 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 0.40 |
| 1.65 | C:e07 PREDICTED_PATH_CONFLICT_END track_002<br>C:e08 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT | 1.60 |
| 2.10 | C:e09 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.00 |
| 2.25 | C:e10 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.20 |
| 2.50 | C:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.40 |
| 3.15 | C:e12 CRITICAL_TTC_END track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 3.10 |
| 4.45 | C:e13 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 4.40 |
| 4.75 | C:e14 COLLISION<br>C:e15 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.70 |
| 4.80 | C:e16 STRONG_THROTTLE_END<br>C:e17 BRAKE_START<br>C:e18 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.70 |
| 4.85 | C:e19 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.80 |
| 5.00 | C:e20 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 4.90 |
| 5.05 | C:e21 CRITICAL_TTC_END track_001<br>C:e22 CLOSING_END track_001<br>C:e23 MOVING_END<br>C:e24 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 5.00 |
| 5.20 | C:e25 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 5.10 |

## States still active when observation ended

- CLOSING of track_002, since C:e05 (t = 0.00 s); the track was lost at 4.45 s
- BRAKE, since C:e17 (t = 4.80 s)
- HARD_BRAKE, since C:e18 (t = 4.80 s)
- EGO_PATH of track_001, since C:e20 (t = 5.00 s)
- STOP, since C:e24 (t = 5.05 s)

## Tracks lost

- track_002 at 4.45 s (C:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 13.95 | 279 | 70.8 m / -2 deg | 1.46 m (5.20) | 2.1 m / -49 deg | 10.7 m/s |
| track_002 | 0.00 | 4.45 | 88 | 45.2 m / -57 deg | 7.51 m (4.45) | 7.5 m / -52 deg | 9.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001.
- t = 0.00 s: C's radar started tracking track_002.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: C observed track_002 start closing in (already the case when first observed).
- t = 0.45 s: C predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 1.65 s: C stopped predicting a path conflict with track_002.
- t = 1.65 s: C started applying strong throttle.
- t = 2.10 s: C stopped applying strong throttle.
- t = 2.25 s: C's time-to-contact with track_002 became critical.
- t = 2.50 s: C's time-to-contact with track_001 became critical.
- t = 3.15 s: C's time-to-contact with track_002 stopped being critical.
- t = 4.45 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.75 s: C's collision sensor recorded a contact (peak impulse 1638 N*s).
- t = 4.75 s: C started applying strong throttle.
- t = 4.80 s: C stopped applying strong throttle.
- t = 4.80 s: C started braking.
- t = 4.80 s: C started braking hard.
- t = 4.85 s: C predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 5.00 s: C observed track_001 enter its forward path corridor.
- t = 5.05 s: C's time-to-contact with track_001 stopped being critical.
- t = 5.05 s: C observed track_001 stop closing in.
- t = 5.05 s: C stopped moving.
- t = 5.05 s: C came to a stop.
- t = 5.20 s: C stopped predicting a path conflict with track_001.
