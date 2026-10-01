# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 115.46773005649447 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 22 (PRECEDES 17, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.95 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e03 | 1.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 3.15 | BRAKE_START | B | - | controls |  |
| B:e05 | 3.90 | MOVING_END | B | - | ego |  |
| B:e06 | 3.90 | STOP_START | B | - | ego |  |
| B:e07 | 5.40 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e08 | 5.55 | CLOSING_END | B | track_001 | radar |  |
| B:e09 | 5.90 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e10 | 7.15 | BRAKE_END | B | - | controls |  |
| B:e11 | 7.55 | STOP_END | B | - | ego |  |
| B:e12 | 7.55 | MOVING_START | B | - | ego |  |
| B:e13 | 8.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e14 | 8.75 | BRAKE_START | B | - | controls |  |
| B:e15 | 9.00 | BRAKE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.95 | B:e02 TRACK_APPEARED_LEFT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 1.90 |
| 3.15 | B:e04 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 3.10 |
| 3.90 | B:e05 MOVING_END<br>B:e06 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING | 3.80 |
| 5.40 | B:e07 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING | 5.30 |
| 5.55 | B:e08 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH | 5.50 |
| 5.90 | B:e09 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH | 5.80 |
| 7.15 | B:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state | 7.10 |
| 7.55 | B:e11 STOP_END<br>B:e12 MOVING_START | ego: STOP<br>track_001: no active state | 7.50 |
| 8.30 | B:e13 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state | 8.20 |
| 8.75 | B:e14 BRAKE_START | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 8.70 |
| 9.00 | B:e15 BRAKE_END | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 | 8.90 |

## States still active when observation ended

- MOVING, since B:e12 (t = 7.55 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.40, no critical TTC

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
- t = 1.95 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.15 s: B started braking.
- t = 3.90 s: B stopped moving.
- t = 3.90 s: B came to a stop.
- t = 5.40 s: B observed track_001 enter its forward path corridor.
- t = 5.55 s: B observed track_001 stop closing in.
- t = 5.90 s: B observed track_001 leave its forward path corridor.
- t = 7.15 s: B released the brake.
- t = 7.55 s: B left its stop.
- t = 7.55 s: B started moving.
- t = 8.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.75 s: B started braking.
- t = 9.00 s: B released the brake.
