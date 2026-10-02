# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 132.83806166797876 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 12; edges: 21 (PRECEDES 17, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.55 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e03 | 0.55 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 1.65 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 3.70 | COLLISION | B | - | collision_sensor | peak_impulse=6116.26 |
| B:e06 | 3.70 | TURN_LEFT_START | B | - | ego |  |
| B:e07 | 3.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e08 | 3.75 | CLOSING_END | B | track_001 | radar |  |
| B:e09 | 3.75 | BRAKE_START | B | - | controls |  |
| B:e10 | 4.25 | TURN_LEFT_END | B | - | ego |  |
| B:e11 | 4.30 | MOVING_END | B | - | ego |  |
| B:e12 | 4.30 | STOP_START | B | - | ego |  |

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
    B:e05 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.55 | B:e02 TRACK_APPEARED_LEFT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 0.50 |
| 1.65 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 1.60 |
| 3.70 | B:e05 COLLISION<br>B:e06 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 3.60 |
| 3.75 | B:e07 CRITICAL_TTC_END track_001<br>B:e08 CLOSING_END track_001<br>B:e09 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 3.70 |
| 4.25 | B:e10 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 4.20 |
| 4.30 | B:e11 MOVING_END<br>B:e12 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.20 |

## States still active when observation ended

- BRAKE, since B:e09 (t = 3.75 s)
- STOP, since B:e12 (t = 4.30 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 1.65, COLLISION 3.70 (+2.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.55 | 14.45 | 270 | 48.0 m / -50 deg | 2.92 m (3.65) | 3.6 m / -69 deg | 11.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.55 s: B's radar started tracking track_001, which appeared on its left.
- t = 0.55 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.65 s: B's time-to-contact with track_001 became critical.
- t = 3.70 s: B's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: B started turning left.
- t = 3.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 3.75 s: B observed track_001 stop closing in.
- t = 3.75 s: B started braking.
- t = 4.25 s: B stopped turning left.
- t = 4.30 s: B stopped moving.
- t = 4.30 s: B came to a stop.
