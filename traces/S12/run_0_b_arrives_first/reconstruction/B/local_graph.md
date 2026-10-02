# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 76.44139377772808 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 23 (PRECEDES 18, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=True |
| B:e03 | 2.60 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e04 | 2.65 | BRAKE_START | B | - | controls |  |
| B:e05 | 3.35 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e06 | 3.35 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 3.40 | MOVING_END | B | - | ego |  |
| B:e08 | 3.40 | STOP_START | B | - | ego |  |
| B:e09 | 4.70 | CLOSING_END | B | track_001 | radar |  |
| B:e10 | 6.45 | BRAKE_END | B | - | controls |  |
| B:e11 | 6.85 | STOP_END | B | - | ego |  |
| B:e12 | 6.85 | MOVING_START | B | - | ego |  |
| B:e13 | 6.90 | CLOSING_START | B | track_001 | radar |  |
| B:e14 | 9.85 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 15.85 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e09
    B:e05 --SAME_TRACK--> B:e13
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.80 | B:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.70 |
| 2.60 | B:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.50 |
| 2.65 | B:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 3.35 | B:e05 TRACK_APPEARED_RIGHT track_001<br>B:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 3.40 | B:e07 MOVING_END<br>B:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 4.70 | B:e09 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.60 |
| 6.45 | B:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.40 |
| 6.85 | B:e11 STOP_END<br>B:e12 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.80 |
| 6.90 | B:e13 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.80 |
| 9.85 | B:e14 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 9.80 |
| 15.85 | B:e15 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 15.80 |

## States still active when observation ended

- MOVING, since B:e12 (t = 6.85 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.35 | 15.85 | 229 | 27.4 m / +43 deg | 12.08 m (9.95) | 70.3 m / -175 deg | 8.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.80 s: B's camera established a STOP sign detection (sign-0).
- t = 2.60 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: B started braking.
- t = 3.35 s: B's radar started tracking track_001, which appeared on its right.
- t = 3.35 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.40 s: B stopped moving.
- t = 3.40 s: B came to a stop.
- t = 4.70 s: B observed track_001 stop closing in.
- t = 6.45 s: B released the brake.
- t = 6.85 s: B left its stop.
- t = 6.85 s: B started moving.
- t = 6.90 s: B observed track_001 start closing in.
- t = 9.85 s: B observed track_001 stop closing in.
- t = 15.85 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
