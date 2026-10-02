# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 33.096214424818754 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 14 (PRECEDES 10, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_REAR | B | track_001 | radar |  |
| B:e03 | 0.50 | CLOSING_START | B | track_001 | radar |  |
| B:e04 | 1.65 | CLOSING_END | B | track_001 | radar |  |
| B:e05 | 3.95 | BRAKE_START | B | - | controls |  |
| B:e06 | 4.25 | CLOSING_START | B | track_001 | radar |  |
| B:e07 | 5.15 | MOVING_END | B | - | ego |  |
| B:e08 | 5.15 | STOP_START | B | - | ego |  |
| B:e09 | 6.45 | TRACK_LOST | B | track_001 | radar |  |
| B:e10 | 6.50 | COLLISION | B | - | collision_sensor | peak_impulse=17663.06 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_REAR track_001 | ego: not yet observed | - |
| 0.50 | B:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state | 0.40 |
| 1.65 | B:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 1.60 |
| 3.95 | B:e05 BRAKE_START | ego: MOVING<br>track_001: no active state | 3.90 |
| 4.25 | B:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>track_001: no active state | 4.20 |
| 5.15 | B:e07 MOVING_END<br>B:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING | 5.10 |
| 6.45 | B:e09 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: CLOSING | 6.40 |
| 6.50 | B:e10 COLLISION | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001 | 6.40 |

## States still active when observation ended

- BRAKE, since B:e05 (t = 3.95 s)
- CLOSING of track_001, since B:e06 (t = 4.25 s); the track was lost at 6.45 s
- STOP, since B:e08 (t = 5.15 s)

## Tracks lost

- track_001 at 6.45 s (B:e09): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 6.45 | 113 | 26.2 m / +180 deg | 3.26 m (6.45) | 3.3 m / -179 deg | 13.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared behind it.
- t = 0.50 s: B observed track_001 start closing in.
- t = 1.65 s: B observed track_001 stop closing in.
- t = 3.95 s: B started braking.
- t = 4.25 s: B observed track_001 start closing in.
- t = 5.15 s: B stopped moving.
- t = 5.15 s: B came to a stop.
- t = 6.45 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 6.50 s: B's collision sensor recorded a contact (peak impulse 17663 N*s).
