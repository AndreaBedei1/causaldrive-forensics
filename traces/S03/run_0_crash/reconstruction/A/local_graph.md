# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 94.55838460847735 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 15 (PRECEDES 12, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.05 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.40 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 4.10 | TRACK_LOST | A | track_001 | radar |  |
| A:e06 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22 |
| A:e07 | 4.30 | BRAKE_START | A | - | controls |  |
| A:e08 | 4.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e09 | 4.90 | MOVING_END | A | - | ego |  |
| A:e10 | 4.90 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.05 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 2.00 |
| 2.40 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 2.30 |
| 4.10 | A:e05 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 4.00 |
| 4.25 | A:e06 COLLISION | ego: MOVING<br>lost (states UNKNOWN): track_001 | 4.20 |
| 4.30 | A:e07 BRAKE_START<br>A:e08 HARD_BRAKE_START | ego: MOVING<br>lost (states UNKNOWN): track_001 | 4.20 |
| 4.90 | A:e09 MOVING_END<br>A:e10 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 | 4.80 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 2.05 s); the track was lost at 4.10 s
- CRITICAL_TTC of track_001, since A:e04 (t = 2.40 s); the track was lost at 4.10 s
- BRAKE, since A:e07 (t = 4.30 s)
- HARD_BRAKE, since A:e08 (t = 4.30 s)
- STOP, since A:e10 (t = 4.90 s)

## Tracks lost

- track_001 at 4.10 s (A:e05): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.05 | 4.10 | 42 | 34.5 m / +56 deg | 3.78 m (4.10) | 3.8 m / +84 deg | 13.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.05 s: A's radar started tracking track_001.
- t = 2.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.40 s: A's time-to-contact with track_001 became critical.
- t = 4.10 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.30 s: A started braking.
- t = 4.30 s: A started braking hard.
- t = 4.90 s: A stopped moving.
- t = 4.90 s: A came to a stop.
