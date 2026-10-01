# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 13.59220041334629 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 301 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (29.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 33 (PRECEDES 25, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar |  |
| B:e03 | 1.10 | CLOSING_START | B | track_001 | radar |  |
| B:e04 | 2.10 | CLOSING_END | B | track_001 | radar |  |
| B:e05 | 3.20 | CLOSING_START | B | track_001 | radar |  |
| B:e06 | 3.70 | BRAKE_START | B | - | controls |  |
| B:e07 | 3.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 4.90 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e09 | 4.90 | CLOSING_END | B | track_001 | radar |  |
| B:e10 | 4.90 | MOVING_END | B | - | ego |  |
| B:e11 | 4.90 | STOP_START | B | - | ego |  |
| B:e12 | 5.70 | BRAKE_END | B | - | controls |  |
| B:e13 | 5.90 | COLLISION | B | - | collision_sensor | peak_impulse=11621.71 |
| B:e14 | 5.90 | STOP_END | B | - | ego |  |
| B:e15 | 5.90 | MOVING_START | B | - | ego |  |
| B:e16 | 5.90 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e17 | 6.15 | COLLISION | B | - | collision_sensor | peak_impulse=9832.40; new_contact=break_s 0.25, peak_ratio 0.85 |
| B:e18 | 6.20 | TRACK_LOST | B | track_001 | radar |  |
| B:e19 | 6.30 | MOVING_END | B | - | ego |  |
| B:e20 | 6.30 | STOP_START | B | - | ego |  |

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
    B:e07 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e16
    B:e02 --SAME_TRACK--> B:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 1.10 | B:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 1.00 |
| 2.10 | B:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 2.00 |
| 3.20 | B:e05 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 3.10 |
| 3.70 | B:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 3.60 |
| 3.75 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH | 3.70 |
| 4.90 | B:e08 CRITICAL_TTC_END track_001<br>B:e09 CLOSING_END track_001<br>B:e10 MOVING_END<br>B:e11 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.80 |
| 5.70 | B:e12 BRAKE_END | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH | 5.60 |
| 5.90 | B:e13 COLLISION<br>B:e14 STOP_END<br>B:e15 MOVING_START<br>B:e16 CRITICAL_TTC_START track_001 | ego: STOP<br>track_001: IN_EGO_PATH | 5.80 |
| 6.15 | B:e17 COLLISION | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH | 6.10 |
| 6.20 | B:e18 TRACK_LOST track_001 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH | 6.10 |
| 6.30 | B:e19 MOVING_END<br>B:e20 STOP_START | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 6.20 |

## States still active when observation ended

- CRITICAL_TTC of track_001, since B:e16 (t = 5.90 s); the track was lost at 6.20 s
- STOP, since B:e20 (t = 6.30 s)

## Tracks lost

- track_001 at 6.20 s (B:e18): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 5.90 (+2.15 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 6.20 | 124 | 13.8 m / -0 deg | 0.08 m (6.15) | 0.1 m / -145 deg | 14.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 1.10 s: B observed track_001 start closing in.
- t = 2.10 s: B observed track_001 stop closing in.
- t = 3.20 s: B observed track_001 start closing in.
- t = 3.70 s: B started braking.
- t = 3.75 s: B's time-to-contact with track_001 became critical.
- t = 4.90 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: B observed track_001 stop closing in.
- t = 4.90 s: B stopped moving.
- t = 4.90 s: B came to a stop.
- t = 5.70 s: B released the brake.
- t = 5.90 s: B's collision sensor recorded a contact (peak impulse 11622 N*s).
- t = 5.90 s: B left its stop.
- t = 5.90 s: B started moving.
- t = 5.90 s: B's time-to-contact with track_001 became critical.
- t = 6.15 s: B's collision sensor recorded a contact (peak impulse 9832 N*s).
- t = 6.20 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: B stopped moving.
- t = 6.30 s: B came to a stop.
