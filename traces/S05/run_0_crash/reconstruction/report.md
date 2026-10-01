# Reconstruction report - S05/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.45 s | 146 | 18 | 41 | 1 | A:e07 @ 3.70 s |
| B | 14.45 s | 146 | 64 | 303 | 17 | B:e09 @ 3.70 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 3.70 | -3.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 3.70 | -3.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6116.26 vs 6116.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.89 | A and B both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.45 s before the matched collision<br>at the contact: minimum range 0.85 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.73 m/s over 2.5 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>not at the contact: last seen 0.85 s before the matched collision (window 0.50 s)<br>track speed agrees with A's own speed: RMSE 1.00 m/s over 1.7 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 30.54 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 29.63 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 19.90 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 30.38 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.15 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.10 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.15 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.20 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.15 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.25 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.25 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_017 | B:track_017 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Global graph

81 nodes, 435 edges; 1 merged node(s): g15 COLLISION(A,B) from A:e07 + B:e09.

### Event sequence (global time)

- `-3.70` MOVING_START(A); MOVING_START(B)
- `-2.85` STRONG_THROTTLE_START(B)
- `-2.50` TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
- `-2.45` TRACK_APPEARED(A,B); CLOSING_START(A,B)
- `-2.20` PREDICTED_PATH_CONFLICT_START(A,B)
- `-2.10` STRONG_THROTTLE_END(B)
- `-2.05` CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001)
- `-1.30` PREDICTED_PATH_CONFLICT_START(B,B:track_001)
- `-0.85` TRACK_LOST(B,B:track_001)
- `-0.20` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B); PREDICTED_PATH_CONFLICT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- `+0.05` STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_006); TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
- `+0.10` EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED(B,B:track_010); EGO_PATH_ENTRY(B,B:track_006)
- `+0.15` EGO_PATH_EXIT(B,B:track_006); TRACK_APPEARED(B,B:track_009); TRACK_APPEARED(B,B:track_011); TRACK_APPEARED(B,B:track_013); EGO_PATH_ENTRY(B,B:track_003)
- `+0.20` EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED(B,B:track_012)
- `+0.25` TRACK_APPEARED(B,B:track_014); TRACK_APPEARED(B,B:track_015); CLOSING_START(B,B:track_012); TRACK_LOST(A,B); TRACK_LOST(B,B:track_002)
- `+0.30` CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TRACK_APPEARED(B,B:track_016); TRACK_APPEARED(B,B:track_017); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_006)
- `+0.35` CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_008); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005)
- `+0.40` EGO_PATH_EXIT(B,B:track_013)
- `+0.50` EGO_PATH_ENTRY(B,B:track_012)
- `+0.55` CLOSING_END(B,B:track_012)
- `+0.60` CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B); TRACK_LOST(B,B:track_017)
- `+0.75` TRACK_LOST(B,B:track_008)
- `+0.85` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 3.70 s before the matched collision, A started moving (already the case when first observed).
- 3.70 s before the matched collision, B started moving (already the case when first observed).
- 2.85 s before the matched collision, B started applying strong throttle.
- 2.50 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 2.50 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.45 s before the matched collision, A's radar started tracking B.
- 2.45 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.20 s before the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 2.10 s before the matched collision, B stopped applying strong throttle.
- 2.05 s before the matched collision, A's time-to-contact with B became critical.
- 2.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.30 s before the matched collision, B predicted a path conflict with unidentified object B:track_001 (close approach ahead if both keep their motion).
- 0.85 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.20 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the matched collision, A stopped predicting a path conflict with B.
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, B's radar started tracking unidentified object B:track_002.
- At the matched collision, B's radar started tracking unidentified object B:track_003.
- At the matched collision, B's radar started tracking unidentified object B:track_004.
- At the matched collision, B's radar started tracking unidentified object B:track_005.
- At the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_006.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_007.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_008.
- 0.05 s after the matched collision, B observed unidentified object B:track_002 enter its forward path corridor.
- 0.05 s after the matched collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.05 s after the matched collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.10 s after the matched collision, B observed unidentified object B:track_002 leave its forward path corridor.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_010.
- 0.10 s after the matched collision, B observed unidentified object B:track_006 enter its forward path corridor.
- 0.15 s after the matched collision, B observed unidentified object B:track_006 leave its forward path corridor.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_009.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_011.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_013.
- 0.15 s after the matched collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 0.20 s after the matched collision, A observed B leave its forward path corridor.
- 0.20 s after the matched collision, B observed unidentified object B:track_003 leave its forward path corridor.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_012.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_014.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_015.
- 0.25 s after the matched collision, B observed unidentified object B:track_012 start closing in.
- 0.25 s after the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.25 s after the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.30 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 0.30 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 0.30 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_016.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_017.
- 0.30 s after the matched collision, B observed unidentified object B:track_014 start closing in.
- 0.30 s after the matched collision, B observed unidentified object B:track_015 start closing in.
- 0.30 s after the matched collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.30 s after the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, B observed unidentified object B:track_007 stop closing in.
- 0.35 s after the matched collision, B observed unidentified object B:track_008 stop closing in.
- 0.35 s after the matched collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 0.35 s after the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.40 s after the matched collision, B observed unidentified object B:track_013 leave its forward path corridor.
- 0.50 s after the matched collision, B observed unidentified object B:track_012 enter its forward path corridor.
- 0.55 s after the matched collision, B observed unidentified object B:track_012 stop closing in.
- 0.60 s after the matched collision, B observed unidentified object B:track_014 stop closing in.
- 0.60 s after the matched collision, B observed unidentified object B:track_015 stop closing in.
- 0.60 s after the matched collision, B stopped moving.
- 0.60 s after the matched collision, B came to a stop.
- 0.60 s after the matched collision, B's radar lost unidentified object B:track_017 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the matched collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the matched collision, A stopped moving.
- 0.85 s after the matched collision, A came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
- TRACK_APPEARED(A,B); CLOSING_START(A,B)
- CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001)
- COLLISION(A,B); PREDICTED_PATH_CONFLICT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_006); TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
- EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED(B,B:track_010); EGO_PATH_ENTRY(B,B:track_006)
- EGO_PATH_EXIT(B,B:track_006); TRACK_APPEARED(B,B:track_009); TRACK_APPEARED(B,B:track_011); TRACK_APPEARED(B,B:track_013); EGO_PATH_ENTRY(B,B:track_003)
- EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED(B,B:track_012)
- TRACK_APPEARED(B,B:track_014); TRACK_APPEARED(B,B:track_015); CLOSING_START(B,B:track_012); TRACK_LOST(A,B); TRACK_LOST(B,B:track_002)
- CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TRACK_APPEARED(B,B:track_016); TRACK_APPEARED(B,B:track_017); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_006)
- CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_008); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005)
- CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B); TRACK_LOST(B,B:track_017)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e13 (t = 3.75 s)
- HARD_BRAKE, since A:e14 (t = 3.75 s)
- STOP, since A:e18 (t = 4.55 s)
B:
- CLOSING of track_001, since B:e04 (t = 1.20 s); the track was lost at 2.85 s
- CRITICAL_TTC of track_001, since B:e06 (t = 1.65 s); the track was lost at 2.85 s
- PREDICTED_PATH_CONFLICT of track_001, since B:e07 (t = 2.40 s); the track was lost at 2.85 s
- CLOSING of track_002, since B:e15 (t = 3.70 s); the track was lost at 3.95 s
- BRAKE, since B:e20 (t = 3.75 s)
- HARD_BRAKE, since B:e21 (t = 3.75 s)
- EGO_PATH of track_012, since B:e57 (t = 4.20 s)
- STOP, since B:e62 (t = 4.30 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e07 at 3.70 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT
- B B:e09 at 3.70 s (local): ego: MOVING; lost (states UNKNOWN): track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_001
B:
- track_001 at 2.85 s (B:e08): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 3.95 s (B:e41): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 4.00 s (B:e49): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_006, track_004, track_005, track_017, track_008

## Uncertainty and limitations

- B:track_001 stays anonymous: not at the contact: last seen 0.85 s before the matched collision (window 0.50 s).
- B:track_002 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 30.54 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 29.63 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 19.90 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 30.38 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_009 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.15 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.10 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_011 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.15 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_012 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.20 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_013 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.15 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_014 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.25 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_015 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.25 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_016 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.30 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_017 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.30 s after the matched collision; speed not comparable with A's own speed before the collision.
- Global time rests on one collision anchor and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from t_global = 0.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5
  },
  "tracking": {
    "min_height_m": 0.3,
    "max_height_m": 2.5,
    "moving_speed_mps": 1.0,
    "cluster_distance_m": 2.0,
    "max_association_distance_m": 2.5,
    "max_velocity_mismatch_mps": 4.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "hard_brake_threshold": 0.9,
    "strong_throttle_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_ttc_s": 2.0,
    "path_half_width_m": 1.5,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "conflict_horizon_s": 4.0,
    "conflict_distance_m": 1.5,
    "conflict_release_horizon_s": 5.0,
    "conflict_release_distance_m": 2.5,
    "cut_in_max_heading_deg": 25.0,
    "cut_in_min_target_speed_mps": 2.0,
    "cut_in_lateral_speed_mps": 0.3,
    "cut_in_persistence_s": 0.5,
    "cut_in_outside_margin_m": 0.5,
    "cut_in_min_displacement_m": 0.5,
    "cut_in_horizon_s": 3.0,
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
