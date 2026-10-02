# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 111.08191861957312 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 19 (PRECEDES 14, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.30 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e03 | 1.30 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 2.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=12077.22 |
| B:e06 | 4.25 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e07 | 4.30 | BRAKE_START | B | - | controls |  |
| B:e08 | 4.50 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e09 | 4.50 | CLOSING_END | B | track_001 | radar |  |
| B:e10 | 4.55 | MOVING_END | B | - | ego |  |
| B:e11 | 4.55 | STOP_START | B | - | ego |  |

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
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.30 | B:e02 TRACK_APPEARED_LEFT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 1.20 |
| 2.35 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 2.30 |
| 4.25 | B:e05 COLLISION<br>B:e06 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 4.20 |
| 4.30 | B:e07 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.20 |
| 4.50 | B:e08 CRITICAL_TTC_END track_001<br>B:e09 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.40 |
| 4.55 | B:e10 MOVING_END<br>B:e11 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 4.50 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e06 (t = 4.25 s)
- BRAKE, since B:e07 (t = 4.30 s)
- STOP, since B:e11 (t = 4.55 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.35, COLLISION 4.25 (+1.90 s); EGO_PATH_ENTRY 4.25 after critical TTC (+1.90 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.30 | 15.15 | 267 | 45.2 m / -40 deg | 2.11 m (4.50) | 2.6 m / +20 deg | 9.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.30 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.30 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.35 s: B's time-to-contact with track_001 became critical.
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.25 s: B observed track_001 enter its forward path corridor.
- t = 4.30 s: B started braking.
- t = 4.50 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.50 s: B observed track_001 stop closing in.
- t = 4.55 s: B stopped moving.
- t = 4.55 s: B came to a stop.
