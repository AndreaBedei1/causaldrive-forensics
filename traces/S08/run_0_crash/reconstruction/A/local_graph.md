# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 225.90415861457586 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 31 (PRECEDES 21, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.05 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.05 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e05 | 2.05 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.10 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 2.35 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e08 | 2.55 | PREDICTED_PATH_CONFLICT_START | A | track_002 | radar |  |
| A:e09 | 2.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e10 | 3.35 | TRACK_LOST | A | track_002 | radar |  |
| A:e11 | 3.45 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e12 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22 |
| A:e13 | 4.30 | BRAKE_START | A | - | controls |  |
| A:e14 | 4.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e15 | 4.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e16 | 4.90 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 4.90 | MOVING_END | A | - | ego |  |
| A:e18 | 4.90 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.05 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.00 |
| 2.05 | A:e04 TRACK_APPEARED track_002<br>A:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 2.00 |
| 2.10 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.00 |
| 2.35 | A:e07 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 2.30 |
| 2.55 | A:e08 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.50 |
| 2.70 | A:e09 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 2.60 |
| 3.35 | A:e10 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 3.30 |
| 3.45 | A:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002 | 3.40 |
| 4.25 | A:e12 COLLISION | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.20 |
| 4.30 | A:e13 BRAKE_START<br>A:e14 HARD_BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.20 |
| 4.75 | A:e15 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.70 |
| 4.90 | A:e16 CLOSING_END track_001<br>A:e17 MOVING_END<br>A:e18 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002 | 4.80 |

## States still active when observation ended

- CLOSING of track_002, since A:e05 (t = 2.05 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_002, since A:e07 (t = 2.35 s); the track was lost at 3.35 s
- PREDICTED_PATH_CONFLICT of track_002, since A:e08 (t = 2.55 s); the track was lost at 3.35 s
- BRAKE, since A:e13 (t = 4.30 s)
- HARD_BRAKE, since A:e14 (t = 4.30 s)
- STOP, since A:e18 (t = 4.90 s)

## Tracks lost

- track_002 at 3.35 s (A:e10): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 15.15 | 303 | 74.1 m / -3 deg | 7.62 m (15.15) | 7.6 m / -23 deg | 8.9 m/s |
| track_002 | 2.05 | 3.35 | 26 | 34.2 m / +56 deg | 14.40 m (3.35) | 14.4 m / +59 deg | 13.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_001.
- t = 0.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.05 s: A's radar started tracking track_002.
- t = 2.05 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: A's time-to-contact with track_001 became critical.
- t = 2.35 s: A's time-to-contact with track_002 became critical.
- t = 2.55 s: A predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 2.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.35 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.45 s: A's time-to-contact with track_001 became critical.
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.30 s: A started braking.
- t = 4.30 s: A started braking hard.
- t = 4.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: A observed track_001 stop closing in.
- t = 4.90 s: A stopped moving.
- t = 4.90 s: A came to a stop.
