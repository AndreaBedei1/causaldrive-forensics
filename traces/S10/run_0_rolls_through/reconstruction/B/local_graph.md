# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 245.13907996192575 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 30 (PRECEDES 25, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.20 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.80 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.65 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e05 | 2.65 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 3.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 4.90 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e08 | 5.25 | COLLISION | B | - | collision_sensor | peak_impulse=12489.77 |
| B:e09 | 5.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e10 | 5.30 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e11 | 5.30 | BRAKE_START | B | - | controls |  |
| B:e12 | 5.30 | HARD_BRAKE_START | B | - | controls |  |
| B:e13 | 5.35 | MOVING_END | B | - | ego |  |
| B:e14 | 5.35 | STOP_START | B | - | ego |  |
| B:e15 | 5.40 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e16 | 5.40 | CLOSING_END | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e07
    B:e04 --SAME_TRACK--> B:e15
    B:e04 --SAME_TRACK--> B:e16
```

## States still active when observation ended

- EGO_PATH of track_001, since B:e07 (t = 4.90 s)
- BRAKE, since B:e11 (t = 5.30 s)
- HARD_BRAKE, since B:e12 (t = 5.30 s)
- STOP, since B:e14 (t = 5.35 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.65 | 15.95 | 267 | 34.4 m / +21 deg | 0.91 m (5.45) | 1.0 m / +12 deg | 5.7 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.20 s: B started applying strong throttle.
- t = 1.80 s: B stopped applying strong throttle.
- t = 2.65 s: B's radar started tracking track_001.
- t = 2.65 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.50 s: B's time-to-contact with track_001 became critical.
- t = 4.90 s: B observed track_001 enter its forward path corridor.
- t = 5.25 s: B's collision sensor recorded a contact (peak impulse 12490 N*s).
- t = 5.25 s: B started applying strong throttle.
- t = 5.30 s: B stopped applying strong throttle.
- t = 5.30 s: B started braking.
- t = 5.30 s: B started braking hard.
- t = 5.35 s: B stopped moving.
- t = 5.35 s: B came to a stop.
- t = 5.40 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.40 s: B observed track_001 stop closing in.
