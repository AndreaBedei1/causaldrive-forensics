# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 48.17277328297496 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 13; edges: 23 (PRECEDES 17, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar |  |
| B:e03 | 1.10 | CLOSING_START | B | track_001 | radar |  |
| B:e04 | 2.10 | CLOSING_END | B | track_001 | radar |  |
| B:e05 | 3.20 | CLOSING_START | B | track_001 | radar |  |
| B:e06 | 3.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 4.60 | COLLISION | B | - | collision_sensor | peak_impulse=21812.15 |
| B:e08 | 4.65 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e09 | 4.65 | CLOSING_END | B | track_001 | radar |  |
| B:e10 | 4.65 | BRAKE_START | B | - | controls |  |
| B:e11 | 4.75 | MOVING_END | B | - | ego |  |
| B:e12 | 4.75 | STOP_START | B | - | ego |  |
| B:e13 | 6.00 | COLLISION | B | - | collision_sensor | peak_impulse=31488.29 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 1.10 | B:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 1.00 |
| 2.10 | B:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 2.00 |
| 3.20 | B:e05 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 3.10 |
| 3.75 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 3.70 |
| 4.60 | B:e07 COLLISION | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.50 |
| 4.65 | B:e08 CRITICAL_TTC_END track_001<br>B:e09 CLOSING_END track_001<br>B:e10 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.60 |
| 4.75 | B:e11 MOVING_END<br>B:e12 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 4.70 |
| 6.00 | B:e13 COLLISION | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH | 5.90 |

## States still active when observation ended

- BRAKE, since B:e10 (t = 4.65 s)
- STOP, since B:e12 (t = 4.75 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 4.60 (+0.85 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.15 | 284 | 13.8 m / -0 deg | 0.08 m (4.65) | 0.3 m / +2 deg | 14.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 1.10 s: B observed track_001 start closing in.
- t = 2.10 s: B observed track_001 stop closing in.
- t = 3.20 s: B observed track_001 start closing in.
- t = 3.75 s: B's time-to-contact with track_001 became critical.
- t = 4.60 s: B's collision sensor recorded a contact (peak impulse 21812 N*s).
- t = 4.65 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.65 s: B observed track_001 stop closing in.
- t = 4.65 s: B started braking.
- t = 4.75 s: B stopped moving.
- t = 4.75 s: B came to a stop.
- t = 6.00 s: B's collision sensor recorded a contact (peak impulse 31488 N*s).
