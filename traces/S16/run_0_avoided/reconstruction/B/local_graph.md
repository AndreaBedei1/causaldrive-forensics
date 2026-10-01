# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 531.2718035392463 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 40 (PRECEDES 28, SAME_TRACK 12)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e03 | 0.65 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e04 | 0.70 | CLOSING_START | B | track_001 | radar |  |
| B:e05 | 0.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e06 | 1.35 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e07 | 1.40 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e08 | 1.40 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e09 | 1.40 | CLOSING_END | B | track_001 | radar |  |
| B:e10 | 2.50 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e11 | 4.20 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e12 | 4.25 | CLOSING_START | B | track_001 | radar |  |
| B:e13 | 4.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e14 | 4.75 | BRAKE_START | B | - | controls |  |
| B:e15 | 5.15 | COLLISION | B | - | collision_sensor | peak_impulse=6073.81 |
| B:e16 | 5.20 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e17 | 5.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e18 | 5.20 | CLOSING_END | B | track_001 | radar |  |
| B:e19 | 5.20 | HARD_BRAKE_START | B | - | controls |  |
| B:e20 | 5.60 | MOVING_END | B | - | ego |  |
| B:e21 | 5.60 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
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
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e11
    B:e02 --SAME_TRACK--> B:e12
    B:e02 --SAME_TRACK--> B:e13
    B:e02 --SAME_TRACK--> B:e16
    B:e02 --SAME_TRACK--> B:e17
    B:e02 --SAME_TRACK--> B:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED track_001 | ego: not yet observed | - |
| 0.65 | B:e03 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 0.60 |
| 0.70 | B:e04 CLOSING_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT | 0.60 |
| 0.75 | B:e05 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT | 0.70 |
| 1.35 | B:e06 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 1.30 |
| 1.40 | B:e07 PREDICTED_PATH_CONFLICT_END track_001<br>B:e08 CRITICAL_TTC_END track_001<br>B:e09 CLOSING_END track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 1.30 |
| 2.50 | B:e10 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH | 2.40 |
| 4.20 | B:e11 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 4.10 |
| 4.25 | B:e12 CLOSING_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT | 4.20 |
| 4.35 | B:e13 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT | 4.30 |
| 4.75 | B:e14 BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 4.70 |
| 5.15 | B:e15 COLLISION | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 5.10 |
| 5.20 | B:e16 PREDICTED_PATH_CONFLICT_END track_001<br>B:e17 CRITICAL_TTC_END track_001<br>B:e18 CLOSING_END track_001<br>B:e19 HARD_BRAKE_START | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 5.10 |
| 5.60 | B:e20 MOVING_END<br>B:e21 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 5.50 |

## States still active when observation ended

- BRAKE, since B:e14 (t = 4.75 s)
- HARD_BRAKE, since B:e19 (t = 5.20 s)
- STOP, since B:e21 (t = 5.60 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 9.95 | 200 | 3.1 m / -0 deg | 0.51 m (5.20) | 1.6 m / +0 deg | 13.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001.
- t = 0.65 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 0.70 s: B observed track_001 start closing in.
- t = 0.75 s: B's time-to-contact with track_001 became critical.
- t = 1.35 s: B started applying strong throttle.
- t = 1.40 s: B stopped predicting a path conflict with track_001.
- t = 1.40 s: B's time-to-contact with track_001 stopped being critical.
- t = 1.40 s: B observed track_001 stop closing in.
- t = 2.50 s: B stopped applying strong throttle.
- t = 4.20 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 4.25 s: B observed track_001 start closing in.
- t = 4.35 s: B's time-to-contact with track_001 became critical.
- t = 4.75 s: B started braking.
- t = 5.15 s: B's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.20 s: B stopped predicting a path conflict with track_001.
- t = 5.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.20 s: B observed track_001 stop closing in.
- t = 5.20 s: B started braking hard.
- t = 5.60 s: B stopped moving.
- t = 5.60 s: B came to a stop.
