# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 54.60816580802202 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 29 (PRECEDES 22, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e05 | 3.20 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e06 | 3.20 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e07 | 3.40 | MOVING_END | A | - | ego |  |
| A:e08 | 3.40 | STOP_START | A | - | ego |  |
| A:e09 | 4.70 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 6.45 | BRAKE_END | A | - | controls |  |
| A:e11 | 6.80 | STOP_END | A | - | ego |  |
| A:e12 | 6.80 | MOVING_START | A | - | ego |  |
| A:e13 | 6.95 | CLOSING_START | A | track_001 | radar |  |
| A:e14 | 7.80 | TURN_LEFT_START | A | - | ego |  |
| A:e15 | 9.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e16 | 11.05 | TURN_LEFT_END | A | - | ego |  |
| A:e17 | 11.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e18 | 11.25 | CLOSING_END | A | track_001 | radar |  |
| A:e19 | 15.55 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e05 --SAME_TRACK--> A:e06
    A:e05 --SAME_TRACK--> A:e09
    A:e05 --SAME_TRACK--> A:e13
    A:e05 --SAME_TRACK--> A:e15
    A:e05 --SAME_TRACK--> A:e17
    A:e05 --SAME_TRACK--> A:e18
    A:e05 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.65 | A:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 3.20 | A:e05 TRACK_APPEARED_LEFT track_001<br>A:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 3.10 |
| 3.40 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 4.70 | A:e09 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.60 |
| 6.45 | A:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.40 |
| 6.80 | A:e11 STOP_END<br>A:e12 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.70 |
| 6.95 | A:e13 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 7.80 | A:e14 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 7.70 |
| 9.60 | A:e15 CRITICAL_TTC_START track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 11.05 | A:e16 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 11.00 |
| 11.10 | A:e17 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 11.00 |
| 11.25 | A:e18 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 11.20 |
| 15.55 | A:e19 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 15.50 |

## States still active when observation ended

- MOVING, since A:e12 (t = 6.80 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 9.60

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.20 | 15.55 | 207 | 30.3 m / -66 deg | 5.58 m (11.25) | 65.9 m / -174 deg | 8.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: A started braking.
- t = 3.20 s: A's radar started tracking track_001, which appeared on its left.
- t = 3.20 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 4.70 s: A observed track_001 stop closing in.
- t = 6.45 s: A released the brake.
- t = 6.80 s: A left its stop.
- t = 6.80 s: A started moving.
- t = 6.95 s: A observed track_001 start closing in.
- t = 7.80 s: A started turning left.
- t = 9.60 s: A's time-to-contact with track_001 became critical.
- t = 11.05 s: A stopped turning left.
- t = 11.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 11.25 s: A observed track_001 stop closing in.
- t = 15.55 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
