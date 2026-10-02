# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 248.77736597135663 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 32 (PRECEDES 23, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.30 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e03 | 1.30 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 2.15 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e05 | 2.15 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e06 | 2.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 2.45 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e08 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=12077.22 |
| B:e09 | 4.25 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e10 | 4.25 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e11 | 4.30 | BRAKE_START | B | - | controls |  |
| B:e12 | 4.50 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e13 | 4.50 | CLOSING_END | B | track_001 | radar |  |
| B:e14 | 4.55 | CLOSING_END | B | track_002 | radar |  |
| B:e15 | 4.55 | MOVING_END | B | - | ego |  |
| B:e16 | 4.55 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e02 --SAME_TRACK--> B:e03
    B:e04 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e07
    B:e04 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e10
    B:e02 --SAME_TRACK--> B:e12
    B:e02 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.30 | B:e02 TRACK_APPEARED_LEFT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 1.20 |
| 2.15 | B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 2.10 |
| 2.35 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.30 |
| 2.45 | B:e07 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 2.40 |
| 4.25 | B:e08 COLLISION<br>B:e09 CRITICAL_TTC_END track_002<br>B:e10 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 4.20 |
| 4.30 | B:e11 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING | 4.20 |
| 4.50 | B:e12 CRITICAL_TTC_END track_001<br>B:e13 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING | 4.40 |
| 4.55 | B:e14 CLOSING_END track_002<br>B:e15 MOVING_END<br>B:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING | 4.50 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e10 (t = 4.25 s)
- BRAKE, since B:e11 (t = 4.30 s)
- STOP, since B:e16 (t = 4.55 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.35, COLLISION 4.25 (+1.90 s); EGO_PATH_ENTRY 4.25 after critical TTC (+1.90 s)
- track_002: CRITICAL_TTC_START 2.45, COLLISION 4.25 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.30 | 15.15 | 267 | 45.2 m / -40 deg | 2.11 m (4.50) | 2.6 m / +20 deg | 9.9 m/s |
| track_002 | 2.15 | 15.15 | 258 | 36.5 m / +25 deg | 13.57 m (4.55) | 13.6 m / +60 deg | 4.5 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.30 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.30 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.15 s: B's radar started tracking track_002, which appeared on its right.
- t = 2.15 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.35 s: B's time-to-contact with track_001 became critical.
- t = 2.45 s: B's time-to-contact with track_002 became critical.
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.25 s: B's time-to-contact with track_002 stopped being critical.
- t = 4.25 s: B observed track_001 enter its forward path corridor.
- t = 4.30 s: B started braking.
- t = 4.50 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.50 s: B observed track_001 stop closing in.
- t = 4.55 s: B observed track_002 stop closing in.
- t = 4.55 s: B stopped moving.
- t = 4.55 s: B came to a stop.
