# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 170.45841221511364 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 44 (PRECEDES 36, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e03 | 0.35 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e04 | 1.10 | CLOSING_START | B | track_001 | radar |  |
| B:e05 | 1.75 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e06 | 2.10 | CLOSING_END | B | track_001 | radar |  |
| B:e07 | 3.20 | CLOSING_START | B | track_001 | radar |  |
| B:e08 | 3.45 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e09 | 3.70 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e10 | 4.60 | COLLISION | B | - | collision_sensor | peak_impulse=21812.15 |
| B:e11 | 4.60 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e12 | 4.65 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e13 | 4.65 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e14 | 4.65 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 4.65 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e16 | 4.65 | BRAKE_START | B | - | controls |  |
| B:e17 | 4.65 | HARD_BRAKE_START | B | - | controls |  |
| B:e18 | 4.75 | MOVING_END | B | - | ego |  |
| B:e19 | 4.75 | STOP_START | B | - | ego |  |
| B:e20 | 6.00 | COLLISION | B | - | collision_sensor | peak_impulse=31488.29 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e15
    B:e10 --PRECEDES--> B:e16
    B:e10 --PRECEDES--> B:e17
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e11 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e12 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e19
    B:e15 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e20
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e12
    B:e02 --SAME_TRACK--> B:e13
    B:e02 --SAME_TRACK--> B:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED track_001 | ego: not yet observed | - |
| 0.35 | B:e03 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 0.30 |
| 1.10 | B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH | 1.00 |
| 1.75 | B:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 1.70 |
| 2.10 | B:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 2.00 |
| 3.20 | B:e07 CLOSING_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 3.10 |
| 3.45 | B:e08 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 3.40 |
| 3.70 | B:e09 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT | 3.60 |
| 4.60 | B:e10 COLLISION<br>B:e11 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 4.50 |
| 4.65 | B:e12 PREDICTED_PATH_CONFLICT_END track_001<br>B:e13 CRITICAL_TTC_END track_001<br>B:e14 CLOSING_END track_001<br>B:e15 STRONG_THROTTLE_END<br>B:e16 BRAKE_START<br>B:e17 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 4.60 |
| 4.75 | B:e18 MOVING_END<br>B:e19 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 4.70 |
| 6.00 | B:e20 COLLISION | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 5.90 |

## States still active when observation ended

- BRAKE, since B:e16 (t = 4.65 s)
- HARD_BRAKE, since B:e17 (t = 4.65 s)
- STOP, since B:e19 (t = 4.75 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.15 | 283 | 13.7 m / +0 deg | 0.05 m (4.65) | 0.3 m / +0 deg | 14.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001.
- t = 0.35 s: B started applying strong throttle.
- t = 1.10 s: B observed track_001 start closing in.
- t = 1.75 s: B stopped applying strong throttle.
- t = 2.10 s: B observed track_001 stop closing in.
- t = 3.20 s: B observed track_001 start closing in.
- t = 3.45 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 3.70 s: B's time-to-contact with track_001 became critical.
- t = 4.60 s: B's collision sensor recorded a contact (peak impulse 21812 N*s).
- t = 4.60 s: B started applying strong throttle.
- t = 4.65 s: B stopped predicting a path conflict with track_001.
- t = 4.65 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.65 s: B observed track_001 stop closing in.
- t = 4.65 s: B stopped applying strong throttle.
- t = 4.65 s: B started braking.
- t = 4.65 s: B started braking hard.
- t = 4.75 s: B stopped moving.
- t = 4.75 s: B came to a stop.
- t = 6.00 s: B's collision sensor recorded a contact (peak impulse 31488 N*s).
