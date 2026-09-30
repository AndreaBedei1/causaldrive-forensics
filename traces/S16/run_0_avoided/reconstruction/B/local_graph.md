# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 531.2718035392463 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 29 (PRECEDES 21, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e03 | 0.70 | CLOSING_START | B | track_001 | radar |  |
| B:e04 | 0.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 1.35 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e06 | 1.40 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e07 | 1.40 | CLOSING_END | B | track_001 | radar |  |
| B:e08 | 2.50 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e09 | 4.25 | CLOSING_START | B | track_001 | radar |  |
| B:e10 | 4.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e11 | 4.75 | BRAKE_START | B | - | controls |  |
| B:e12 | 5.15 | COLLISION | B | - | collision_sensor | peak_impulse=6073.81 |
| B:e13 | 5.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e14 | 5.20 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 5.20 | HARD_BRAKE_START | B | - | controls |  |
| B:e16 | 5.60 | MOVING_END | B | - | ego |  |
| B:e17 | 5.60 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e10
    B:e02 --SAME_TRACK--> B:e13
    B:e02 --SAME_TRACK--> B:e14
```

## States still active when observation ended

- BRAKE, since B:e11 (t = 4.75 s)
- HARD_BRAKE, since B:e15 (t = 5.20 s)
- STOP, since B:e17 (t = 5.60 s)

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
- t = 0.70 s: B observed track_001 start closing in.
- t = 0.75 s: B's time-to-contact with track_001 became critical.
- t = 1.35 s: B started applying strong throttle.
- t = 1.40 s: B's time-to-contact with track_001 stopped being critical.
- t = 1.40 s: B observed track_001 stop closing in.
- t = 2.50 s: B stopped applying strong throttle.
- t = 4.25 s: B observed track_001 start closing in.
- t = 4.35 s: B's time-to-contact with track_001 became critical.
- t = 4.75 s: B started braking.
- t = 5.15 s: B's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.20 s: B observed track_001 stop closing in.
- t = 5.20 s: B started braking hard.
- t = 5.60 s: B stopped moving.
- t = 5.60 s: B came to a stop.
