# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 269.6633632183075 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 22 (PRECEDES 19, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.85 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 1.95 | BRAKE_START | A | - | controls |  |
| A:e04 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e05 | 2.70 | TURN_LEFT_START | A | - | ego |  |
| A:e06 | 2.75 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e07 | 2.75 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e08 | 3.80 | BRAKE_END | A | - | controls |  |
| A:e09 | 3.80 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e10 | 5.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e11 | 5.25 | COLLISION | A | - | collision_sensor | peak_impulse=12489.77 |
| A:e12 | 5.30 | TURN_LEFT_END | A | - | ego |  |
| A:e13 | 5.30 | BRAKE_START | A | - | controls |  |
| A:e14 | 5.40 | MOVING_END | A | - | ego |  |
| A:e15 | 5.40 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e06 --SAME_TRACK--> A:e07
    A:e06 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.85 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.80 |
| 1.95 | A:e03 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known | 1.90 |
| 2.15 | A:e04 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING, BRAKE<br>sign-0: STOP sign known | 2.10 |
| 2.70 | A:e05 TURN_LEFT_START | ego: MOVING, BRAKE<br>sign-0: STOP sign known | 2.60 |
| 2.75 | A:e06 TRACK_APPEARED_LEFT track_001<br>A:e07 CLOSING_START track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>sign-0: STOP sign known | 2.70 |
| 3.80 | A:e08 BRAKE_END<br>A:e09 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known | 3.70 |
| 5.20 | A:e10 TRACK_LOST track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 5.10 |
| 5.25 | A:e11 COLLISION | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 5.20 |
| 5.30 | A:e12 TURN_LEFT_END<br>A:e13 BRAKE_START | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 5.20 |
| 5.40 | A:e14 MOVING_END<br>A:e15 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 5.30 |

## States still active when observation ended

- CLOSING of track_001, since A:e07 (t = 2.75 s); the track was lost at 5.20 s
- CRITICAL_TTC of track_001, since A:e09 (t = 3.80 s); the track was lost at 5.20 s
- BRAKE, since A:e13 (t = 5.30 s)
- STOP, since A:e15 (t = 5.40 s)

## Tracks lost

- track_001 at 5.20 s (A:e10): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.80, COLLISION 5.25 (+1.45 s)

## Sign detection windows

- STOP sign sign-0: detected 1.85 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.75 | 5.20 | 50 | 34.9 m / -67 deg | 3.70 m (5.20) | 3.7 m / -28 deg | 10.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.85 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: A started braking.
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.70 s: A started turning left.
- t = 2.75 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.75 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.80 s: A released the brake.
- t = 3.80 s: A's time-to-contact with track_001 became critical.
- t = 5.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.25 s: A's collision sensor recorded a contact (peak impulse 12490 N*s).
- t = 5.30 s: A stopped turning left.
- t = 5.30 s: A started braking.
- t = 5.40 s: A stopped moving.
- t = 5.40 s: A came to a stop.
