# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 201.56119414046407 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 12; edges: 18 (PRECEDES 13, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.00 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e03 | 2.40 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e04 | 2.50 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e05 | 2.50 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e07 | 3.25 | MOVING_END | B | - | ego |  |
| B:e08 | 3.25 | STOP_START | B | - | ego |  |
| B:e09 | 5.80 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e10 | 6.10 | CLOSING_END | B | track_001 | radar |  |
| B:e11 | 6.20 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e12 | 8.75 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e09
    B:e04 --SAME_TRACK--> B:e10
    B:e04 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.00 | B:e02 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 1.90 |
| 2.40 | B:e03 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign known | 2.30 |
| 2.50 | B:e04 TRACK_APPEARED_LEFT track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING<br>sign-1: STOP sign known | 2.40 |
| 2.55 | B:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known | 2.50 |
| 3.25 | B:e07 MOVING_END<br>B:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 3.20 |
| 5.80 | B:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 5.70 |
| 6.10 | B:e10 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known | 6.00 |
| 6.20 | B:e11 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known | 6.10 |
| 8.75 | B:e12 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>sign-1: STOP sign known | 8.70 |

## States still active when observation ended

- BRAKE, since B:e06 (t = 2.55 s)
- STOP, since B:e08 (t = 3.25 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.80, no critical TTC

## Sign detection windows

- STOP sign sign-1: detected 2.00 s -> 2.40 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.50 | 8.75 | 126 | 36.2 m / -68 deg | 6.84 m (6.10) | 25.7 m / +80 deg | 10.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.00 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.40 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.50 s: B's radar started tracking track_001, which appeared on its left.
- t = 2.50 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.55 s: B started braking.
- t = 3.25 s: B stopped moving.
- t = 3.25 s: B came to a stop.
- t = 5.80 s: B observed track_001 enter its forward path corridor.
- t = 6.10 s: B observed track_001 stop closing in.
- t = 6.20 s: B observed track_001 leave its forward path corridor.
- t = 8.75 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
