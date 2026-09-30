# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 170.45841221511364 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 37 (PRECEDES 31, SAME_TRACK 6)

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
| B:e08 | 3.70 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 4.60 | COLLISION | B | - | collision_sensor | peak_impulse=21812.15 |
| B:e10 | 4.60 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e11 | 4.65 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e12 | 4.65 | CLOSING_END | B | track_001 | radar |  |
| B:e13 | 4.65 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e14 | 4.65 | BRAKE_START | B | - | controls |  |
| B:e15 | 4.65 | HARD_BRAKE_START | B | - | controls |  |
| B:e16 | 4.75 | MOVING_END | B | - | ego |  |
| B:e17 | 4.75 | STOP_START | B | - | ego |  |
| B:e18 | 6.00 | COLLISION | B | - | collision_sensor | peak_impulse=31488.29 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

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
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e09 --PRECEDES--> B:e14
    B:e09 --PRECEDES--> B:e15
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e11 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e11
    B:e02 --SAME_TRACK--> B:e12
```

## States still active when observation ended

- BRAKE, since B:e14 (t = 4.65 s)
- HARD_BRAKE, since B:e15 (t = 4.65 s)
- STOP, since B:e17 (t = 4.75 s)

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
- t = 3.70 s: B's time-to-contact with track_001 became critical.
- t = 4.60 s: B's collision sensor recorded a contact (peak impulse 21812 N*s).
- t = 4.60 s: B started applying strong throttle.
- t = 4.65 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.65 s: B observed track_001 stop closing in.
- t = 4.65 s: B stopped applying strong throttle.
- t = 4.65 s: B started braking.
- t = 4.65 s: B started braking hard.
- t = 4.75 s: B stopped moving.
- t = 4.75 s: B came to a stop.
- t = 6.00 s: B's collision sensor recorded a contact (peak impulse 31488 N*s).
