# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 12.853837836533785 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 30 (PRECEDES 21, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e05 | 2.70 | CLOSING_START | B | track_002 | radar |  |
| B:e06 | 3.65 | CUT_IN_FROM_RIGHT_START | B | track_002 | radar |  |
| B:e07 | 4.95 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 5.10 | CLOSING_END | B | track_002 | radar |  |
| B:e09 | 5.15 | CLOSING_START | B | track_001 | radar |  |
| B:e10 | 5.65 | CUT_IN_FROM_RIGHT_END | B | track_002 | radar |  |
| B:e11 | 5.75 | COLLISION | B | - | collision_sensor | peak_impulse=915.98 |
| B:e12 | 5.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e13 | 5.80 | THROTTLE_END | B | - | controls |  |
| B:e14 | 5.80 | BRAKE_START | B | - | controls |  |
| B:e15 | 5.85 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 6.70 | MOVING_END | B | - | ego |  |
| B:e17 | 6.70 | STOP_START | B | - | ego |  |
| B:e18 | 7.15 | TRACK_LOST | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e05
    B:e02 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e07
    B:e04 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e09
    B:e04 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e15
    B:e04 --SAME_TRACK--> B:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002 | ego: not yet observed | - |
| 2.70 | B:e05 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state | 2.60 |
| 3.65 | B:e06 CUT_IN_FROM_RIGHT_START track_002 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING | 3.60 |
| 4.95 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CUT_IN_FROM_RIGHT | 4.90 |
| 5.10 | B:e08 CLOSING_END track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING, CUT_IN_FROM_RIGHT | 5.00 |
| 5.15 | B:e09 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CUT_IN_FROM_RIGHT | 5.10 |
| 5.65 | B:e10 CUT_IN_FROM_RIGHT_END track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CUT_IN_FROM_RIGHT | 5.60 |
| 5.75 | B:e11 COLLISION<br>B:e12 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state | 5.70 |
| 5.80 | B:e13 THROTTLE_END<br>B:e14 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state | 5.70 |
| 5.85 | B:e15 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state | 5.80 |
| 6.70 | B:e16 MOVING_END<br>B:e17 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state | 6.60 |
| 7.15 | B:e18 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state | 7.10 |

## States still active when observation ended

- BRAKE, since B:e14 (t = 5.80 s)
- STOP, since B:e17 (t = 6.70 s)

## Tracks lost

- lost with no state active: track_002

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.95, COLLISION 5.75 (+0.80 s)
- track_002: CUT_IN_FROM_RIGHT_START 3.65, no critical TTC after it

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.50 | 231 | 3.1 m / +37 deg | 0.22 m (6.60) | 0.7 m / +68 deg | 12.1 m/s |
| track_002 | 0.00 | 7.15 | 144 | 13.5 m / +25 deg | 6.09 m (5.20) | 20.8 m / +17 deg | 15.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 2.70 s: B observed track_002 start closing in.
- t = 3.65 s: B observed track_002 cutting in from the right.
- t = 4.95 s: B's time-to-contact with track_001 became critical.
- t = 5.10 s: B observed track_002 stop closing in.
- t = 5.15 s: B observed track_001 start closing in.
- t = 5.65 s: B observed track_002's cut-in from the right settle.
- t = 5.75 s: B's collision sensor recorded a contact (peak impulse 916 N*s).
- t = 5.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.80 s: B released the accelerator.
- t = 5.80 s: B started braking.
- t = 5.85 s: B observed track_001 stop closing in.
- t = 6.70 s: B stopped moving.
- t = 6.70 s: B came to a stop.
- t = 7.15 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
