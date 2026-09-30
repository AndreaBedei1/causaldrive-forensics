# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 349.14128875359893 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 23; edges: 45 (PRECEDES 38, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.65 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 2.10 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e05 | 3.00 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e06 | 3.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 4.00 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e08 | 4.35 | BRAKE_START | B | - | controls |  |
| B:e09 | 4.35 | HARD_BRAKE_START | B | - | controls |  |
| B:e10 | 4.70 | CLOSING_END | B | track_001 | radar |  |
| B:e11 | 4.70 | MOVING_END | B | - | ego |  |
| B:e12 | 4.70 | STOP_START | B | - | ego |  |
| B:e13 | 6.95 | CLOSING_START | B | track_001 | radar |  |
| B:e14 | 8.50 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e15 | 9.05 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e16 | 9.55 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e17 | 10.45 | HARD_BRAKE_END | B | - | controls |  |
| B:e18 | 10.45 | BRAKE_END | B | - | controls |  |
| B:e19 | 10.45 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e20 | 10.85 | STOP_END | B | - | ego |  |
| B:e21 | 10.85 | MOVING_START | B | - | ego |  |
| B:e22 | 10.85 | TRACK_LOST | B | track_001 | radar |  |
| B:e23 | 11.95 | STRONG_THROTTLE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
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
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e23
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e10
    B:e05 --SAME_TRACK--> B:e13
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e16
    B:e05 --SAME_TRACK--> B:e22
```

## States still active when observation ended

- CLOSING of track_001, since B:e13 (t = 6.95 s); the track was lost at 10.85 s
- CRITICAL_TTC of track_001, since B:e16 (t = 9.55 s); the track was lost at 10.85 s
- MOVING, since B:e21 (t = 10.85 s)

## Sign detection windows

- STOP sign sign-0: detected 2.10 s -> 4.00 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.00 | 10.85 | 158 | 30.1 m / +21 deg | 5.26 m (10.85) | 5.3 m / -62 deg | 8.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.65 s: B started applying strong throttle.
- t = 2.10 s: B stopped applying strong throttle.
- t = 2.10 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 3.00 s: B's radar started tracking track_001.
- t = 3.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.00 s: B's camera stopped detecting STOP sign sign-0.
- t = 4.35 s: B started braking.
- t = 4.35 s: B started braking hard.
- t = 4.70 s: B observed track_001 stop closing in.
- t = 4.70 s: B stopped moving.
- t = 4.70 s: B came to a stop.
- t = 6.95 s: B observed track_001 start closing in.
- t = 8.50 s: B observed track_001 enter its forward path corridor.
- t = 9.05 s: B observed track_001 leave its forward path corridor.
- t = 9.55 s: B's time-to-contact with track_001 became critical.
- t = 10.45 s: B stopped braking hard.
- t = 10.45 s: B released the brake.
- t = 10.45 s: B started applying strong throttle.
- t = 10.85 s: B left its stop.
- t = 10.85 s: B started moving.
- t = 10.85 s: B's radar lost track_001.
- t = 11.95 s: B stopped applying strong throttle.
