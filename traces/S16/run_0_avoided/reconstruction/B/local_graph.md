# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 239.17912420257926 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 24 (PRECEDES 16, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar |  |
| B:e03 | 0.65 | CLOSING_START | B | track_001 | radar |  |
| B:e04 | 0.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 1.40 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e06 | 1.40 | CLOSING_END | B | track_001 | radar |  |
| B:e07 | 4.25 | CLOSING_START | B | track_001 | radar |  |
| B:e08 | 4.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 4.75 | BRAKE_START | B | - | controls |  |
| B:e10 | 5.15 | COLLISION | B | - | collision_sensor | peak_impulse=6073.81 |
| B:e11 | 5.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e12 | 5.20 | CLOSING_END | B | track_001 | radar |  |
| B:e13 | 5.60 | MOVING_END | B | - | ego |  |
| B:e14 | 5.60 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
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
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e11
    B:e02 --SAME_TRACK--> B:e12
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 0.65 | B:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 0.60 |
| 0.75 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 0.70 |
| 1.40 | B:e05 CRITICAL_TTC_END track_001<br>B:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 1.30 |
| 4.25 | B:e07 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 4.20 |
| 4.40 | B:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 4.30 |
| 4.75 | B:e09 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.70 |
| 5.15 | B:e10 COLLISION | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.10 |
| 5.20 | B:e11 CRITICAL_TTC_END track_001<br>B:e12 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.10 |
| 5.60 | B:e13 MOVING_END<br>B:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 5.50 |

## States still active when observation ended

- BRAKE, since B:e09 (t = 4.75 s)
- STOP, since B:e14 (t = 5.60 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.75, COLLISION 5.15 (+4.40 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 9.95 | 196 | 6.1 m / +1 deg | 3.08 m (5.20) | 4.5 m / +2 deg | 12.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.65 s: B observed track_001 start closing in.
- t = 0.75 s: B's time-to-contact with track_001 became critical.
- t = 1.40 s: B's time-to-contact with track_001 stopped being critical.
- t = 1.40 s: B observed track_001 stop closing in.
- t = 4.25 s: B observed track_001 start closing in.
- t = 4.40 s: B's time-to-contact with track_001 became critical.
- t = 4.75 s: B started braking.
- t = 5.15 s: B's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.20 s: B observed track_001 stop closing in.
- t = 5.60 s: B stopped moving.
- t = 5.60 s: B came to a stop.
