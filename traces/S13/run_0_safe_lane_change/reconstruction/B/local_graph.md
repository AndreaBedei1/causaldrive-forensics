# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 463.0985040329397 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 3; edges: 2 (PRECEDES 2)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | STRONG_THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 1.25 | STRONG_THROTTLE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 STRONG_THROTTLE_START | ego: not yet observed | - |
| 1.25 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.20 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B started applying strong throttle (already the case when first observed).
- t = 1.25 s: B stopped applying strong throttle.
