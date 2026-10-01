# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 126.0048761293292 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 18 (PRECEDES 13, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.60 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 2.60 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 3.55 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 4.95 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e06 | 5.25 | COLLISION | B | - | collision_sensor | peak_impulse=12489.77 |
| B:e07 | 5.30 | BRAKE_START | B | - | controls |  |
| B:e08 | 5.35 | MOVING_END | B | - | ego |  |
| B:e09 | 5.35 | STOP_START | B | - | ego |  |
| B:e10 | 5.40 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e11 | 5.40 | CLOSING_END | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e10
    B:e02 --SAME_TRACK--> B:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.60 | B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 2.50 |
| 3.55 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 3.50 |
| 4.95 | B:e05 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 4.90 |
| 5.25 | B:e06 COLLISION | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.20 |
| 5.30 | B:e07 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.20 |
| 5.35 | B:e08 MOVING_END<br>B:e09 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.30 |
| 5.40 | B:e10 CRITICAL_TTC_END track_001<br>B:e11 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.30 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e05 (t = 4.95 s)
- BRAKE, since B:e07 (t = 5.30 s)
- STOP, since B:e09 (t = 5.35 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.55, COLLISION 5.25 (+1.70 s); EGO_PATH_ENTRY 4.95 after critical TTC (+1.40 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 15.95 | 265 | 35.0 m / +21 deg | 0.88 m (5.50) | 1.0 m / +21 deg | 6.0 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.60 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.60 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.55 s: B's time-to-contact with track_001 became critical.
- t = 4.95 s: B observed track_001 enter its forward path corridor.
- t = 5.25 s: B's collision sensor recorded a contact (peak impulse 12490 N*s).
- t = 5.30 s: B started braking.
- t = 5.35 s: B stopped moving.
- t = 5.35 s: B came to a stop.
- t = 5.40 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.40 s: B observed track_001 stop closing in.
