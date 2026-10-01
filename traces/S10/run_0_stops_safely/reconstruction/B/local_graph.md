# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 147.96782859042287 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 8; edges: 12 (PRECEDES 8, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.60 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 2.60 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 4.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e05 | 5.60 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e06 | 5.85 | TRACK_LOST | B | track_001 | radar |  |
| B:e07 | 7.70 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e08 | 7.80 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |

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
    B:e07 --PRECEDES--> B:e08
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.60 | B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 2.50 |
| 4.40 | B:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 4.30 |
| 5.60 | B:e05 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 5.50 |
| 5.85 | B:e06 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING | 5.80 |
| 7.70 | B:e07 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 7.60 |
| 7.80 | B:e08 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 7.70 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)
- CLOSING of track_001, since B:e03 (t = 2.60 s); the track was lost at 5.85 s

## Tracks lost

- track_001 at 5.85 s (B:e06): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.40

## Sign detection windows

- STOP sign sign-1: detected 7.70 s -> 7.80 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 5.85 | 66 | 34.7 m / +20 deg | 7.40 m (5.85) | 7.4 m / +83 deg | 6.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.60 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.60 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.40 s: B's time-to-contact with track_001 became critical.
- t = 5.60 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.85 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 7.70 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 7.80 s: B's camera stopped detecting STOP sign sign-1.
