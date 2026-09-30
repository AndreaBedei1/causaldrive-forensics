# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 225.90415861457586 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 34 (PRECEDES 24, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.05 | TRACK_APPEARED | C | track_001 | radar |  |
| C:e03 | 0.05 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 2.15 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e05 | 2.35 | BRAKE_START | C | - | controls |  |
| C:e06 | 2.35 | HARD_BRAKE_START | C | - | controls |  |
| C:e07 | 2.75 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e08 | 2.85 | MOVING_END | C | - | ego |  |
| C:e09 | 2.85 | STOP_START | C | - | ego |  |
| C:e10 | 3.00 | TRACK_APPEARED | C | track_002 | radar |  |
| C:e11 | 3.00 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e12 | 3.35 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e13 | 3.55 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e14 | 4.20 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e15 | 4.55 | CLOSING_END | C | track_002 | radar |  |
| C:e16 | 4.70 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e17 | 4.90 | CLOSING_END | C | track_001 | radar |  |
| C:e18 | 14.35 | HARD_BRAKE_END | C | - | controls |  |
| C:e19 | 14.35 | BRAKE_END | C | - | controls |  |
| C:e20 | 14.35 | STRONG_THROTTLE_START | C | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e04
    C:e04 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e08 --PRECEDES--> C:e11
    C:e09 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e12
    C:e12 --PRECEDES--> C:e13
    C:e13 --PRECEDES--> C:e14
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e16 --PRECEDES--> C:e17
    C:e17 --PRECEDES--> C:e18
    C:e17 --PRECEDES--> C:e19
    C:e17 --PRECEDES--> C:e20
    C:e02 --SAME_TRACK--> C:e03
    C:e02 --SAME_TRACK--> C:e04
    C:e02 --SAME_TRACK--> C:e07
    C:e10 --SAME_TRACK--> C:e11
    C:e10 --SAME_TRACK--> C:e12
    C:e02 --SAME_TRACK--> C:e13
    C:e10 --SAME_TRACK--> C:e14
    C:e10 --SAME_TRACK--> C:e15
    C:e02 --SAME_TRACK--> C:e16
    C:e02 --SAME_TRACK--> C:e17
```

## States still active when observation ended

- STOP, since C:e09 (t = 2.85 s)
- STRONG_THROTTLE, since C:e20 (t = 14.35 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 15.15 | 301 | 74.4 m / -3 deg | 8.36 m (5.00) | 8.4 m / -16 deg | 9.9 m/s |
| track_002 | 3.00 | 15.15 | 244 | 24.1 m / -60 deg | 11.81 m (4.60) | 12.0 m / -30 deg | 11.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.05 s: C's radar started tracking track_001.
- t = 0.05 s: C observed track_001 start closing in (already the case when first observed).
- t = 2.15 s: C's time-to-contact with track_001 became critical.
- t = 2.35 s: C started braking.
- t = 2.35 s: C started braking hard.
- t = 2.75 s: C's time-to-contact with track_001 stopped being critical.
- t = 2.85 s: C stopped moving.
- t = 2.85 s: C came to a stop.
- t = 3.00 s: C's radar started tracking track_002.
- t = 3.00 s: C observed track_002 start closing in (already the case when first observed).
- t = 3.35 s: C's time-to-contact with track_002 became critical.
- t = 3.55 s: C's time-to-contact with track_001 became critical.
- t = 4.20 s: C's time-to-contact with track_002 stopped being critical.
- t = 4.55 s: C observed track_002 stop closing in.
- t = 4.70 s: C's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: C observed track_001 stop closing in.
- t = 14.35 s: C stopped braking hard.
- t = 14.35 s: C released the brake.
- t = 14.35 s: C started applying strong throttle.
