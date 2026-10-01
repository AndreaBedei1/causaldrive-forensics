# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 115.46773005649447 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 23; edges: 42 (PRECEDES 35, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 1.95 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e05 | 1.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 3.15 | BRAKE_START | B | - | controls |  |
| B:e07 | 3.15 | HARD_BRAKE_START | B | - | controls |  |
| B:e08 | 3.15 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 3.90 | MOVING_END | B | - | ego |  |
| B:e10 | 3.90 | STOP_START | B | - | ego |  |
| B:e11 | 5.40 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e12 | 5.45 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e13 | 5.55 | CLOSING_END | B | track_001 | radar |  |
| B:e14 | 5.90 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e15 | 7.15 | HARD_BRAKE_END | B | - | controls |  |
| B:e16 | 7.15 | BRAKE_END | B | - | controls |  |
| B:e17 | 7.15 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e18 | 7.55 | STOP_END | B | - | ego |  |
| B:e19 | 7.55 | MOVING_START | B | - | ego |  |
| B:e20 | 8.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e21 | 8.55 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e22 | 8.75 | BRAKE_START | B | - | controls |  |
| B:e23 | 9.00 | BRAKE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e10
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e08
    B:e04 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e04 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e04 --SAME_TRACK--> B:e20
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 1.95 | B:e04 TRACK_APPEARED track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING | 1.90 |
| 3.15 | B:e06 BRAKE_START<br>B:e07 HARD_BRAKE_START<br>B:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 3.10 |
| 3.90 | B:e09 MOVING_END<br>B:e10 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 3.80 |
| 5.40 | B:e11 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 5.30 |
| 5.45 | B:e12 CRITICAL_TTC_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.40 |
| 5.55 | B:e13 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 5.50 |
| 5.90 | B:e14 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 5.80 |
| 7.15 | B:e15 HARD_BRAKE_END<br>B:e16 BRAKE_END<br>B:e17 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE | 7.10 |
| 7.55 | B:e18 STOP_END<br>B:e19 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE | 7.50 |
| 8.30 | B:e20 TRACK_LOST track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE | 8.20 |
| 8.55 | B:e21 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001 | 8.50 |
| 8.75 | B:e22 BRAKE_START | ego: MOVING<br>lost (states UNKNOWN): track_001 | 8.70 |
| 9.00 | B:e23 BRAKE_END | ego: MOVING, BRAKE<br>lost (states UNKNOWN): track_001 | 8.90 |

## States still active when observation ended

- MOVING, since B:e19 (t = 7.55 s)

## Tracks lost

- lost with no state active: track_001

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.95 | 8.30 | 128 | 38.8 m / -59 deg | 4.53 m (5.60) | 25.2 m / +80 deg | 9.7 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 1.95 s: B's radar started tracking track_001.
- t = 1.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.15 s: B started braking.
- t = 3.15 s: B started braking hard.
- t = 3.15 s: B's time-to-contact with track_001 became critical.
- t = 3.90 s: B stopped moving.
- t = 3.90 s: B came to a stop.
- t = 5.40 s: B observed track_001 enter its forward path corridor.
- t = 5.45 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.55 s: B observed track_001 stop closing in.
- t = 5.90 s: B observed track_001 leave its forward path corridor.
- t = 7.15 s: B stopped braking hard.
- t = 7.15 s: B released the brake.
- t = 7.15 s: B started applying strong throttle.
- t = 7.55 s: B left its stop.
- t = 7.55 s: B started moving.
- t = 8.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.55 s: B stopped applying strong throttle.
- t = 8.75 s: B started braking.
- t = 9.00 s: B released the brake.
