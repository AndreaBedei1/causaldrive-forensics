# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 305.1153160445392 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 15 (PRECEDES 10, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.60 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 2.60 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 4.25 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 5.95 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e06 | 6.15 | CLOSING_END | B | track_001 | radar |  |
| B:e07 | 7.70 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e08 | 7.70 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e09 | 11.95 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.60 | B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 2.50 |
| 4.25 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 4.20 |
| 5.95 | B:e05 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 5.90 |
| 6.15 | B:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 6.10 |
| 7.70 | B:e07 STOP_SIGN_DETECTED_START sign-0<br>B:e08 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: no active state | 7.60 |
| 11.95 | B:e09 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known | 11.90 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.25

## Sign detection windows

- STOP sign sign-0: detected 7.70 s -> 7.70 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 11.95 | 166 | 36.8 m / +17 deg | 7.38 m (6.15) | 90.1 m / -178 deg | 9.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.60 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.60 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.25 s: B's time-to-contact with track_001 became critical.
- t = 5.95 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.15 s: B observed track_001 stop closing in.
- t = 7.70 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 7.70 s: B's camera stopped detecting STOP sign sign-0.
- t = 11.95 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
