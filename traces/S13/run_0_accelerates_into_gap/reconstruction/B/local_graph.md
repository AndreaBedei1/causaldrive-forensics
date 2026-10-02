# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 138.9119843505323 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 29 (PRECEDES 23, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.80 | BRAKE_START | B | - | controls |  |
| B:e03 | 2.75 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e04 | 2.75 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 5.65 | COLLISION | B | - | collision_sensor | peak_impulse=5215.85 |
| B:e06 | 5.65 | CLOSING_END | B | track_001 | radar |  |
| B:e07 | 5.75 | TURN_RIGHT_START | B | - | ego |  |
| B:e08 | 6.55 | CLOSING_START | B | track_001 | radar |  |
| B:e09 | 6.55 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e10 | 6.90 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e11 | 6.90 | TURN_RIGHT_END | B | - | ego |  |
| B:e12 | 6.90 | MOVING_END | B | - | ego |  |
| B:e13 | 6.90 | STOP_START | B | - | ego |  |
| B:e14 | 6.95 | CLOSING_END | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    B:e08 --PRECEDES--> B:e13
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | B:e02 BRAKE_START | ego: MOVING | 0.70 |
| 2.75 | B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, BRAKE | 2.70 |
| 5.65 | B:e05 COLLISION<br>B:e06 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING | 5.60 |
| 5.75 | B:e07 TURN_RIGHT_START | ego: MOVING, BRAKE<br>track_001: no active state | 5.70 |
| 6.55 | B:e08 CLOSING_START track_001<br>B:e09 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: no active state | 6.50 |
| 6.90 | B:e10 CRITICAL_TTC_END track_001<br>B:e11 TURN_RIGHT_END<br>B:e12 MOVING_END<br>B:e13 STOP_START | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC | 6.80 |
| 6.95 | B:e14 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING | 6.90 |

## States still active when observation ended

- BRAKE, since B:e02 (t = 0.80 s)
- STOP, since B:e13 (t = 6.90 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 6.55

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.75 | 9.95 | 136 | 25.0 m / +172 deg | 3.03 m (7.05) | 3.1 m / +119 deg | 15.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.80 s: B started braking.
- t = 2.75 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.75 s: B observed track_001 start closing in (already the case when first observed).
- t = 5.65 s: B's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.65 s: B observed track_001 stop closing in.
- t = 5.75 s: B started turning right.
- t = 6.55 s: B observed track_001 start closing in.
- t = 6.55 s: B's time-to-contact with track_001 became critical.
- t = 6.90 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.90 s: B stopped turning right.
- t = 6.90 s: B stopped moving.
- t = 6.90 s: B came to a stop.
- t = 6.95 s: B observed track_001 stop closing in.
