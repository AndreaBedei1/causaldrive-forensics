# Reconstruction report - S05/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.45 s | 146 | 13 | 22 | 1 | A:e06 @ 3.70 s |
| B | 14.45 s | 146 | 81 | 409 | 19 | B:e06 @ 3.70 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 3.70 | -3.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 3.70 | -3.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6116.26 vs 6116.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.5 m -> 1.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.70 m/s over 2.5 s<br>range at the contact 0.90 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.73 | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.35 s before it (window 0.50 s)<br>approaching before the contact: range 19.9 m -> 5.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.58 m/s over 2.2 s<br>range at the contact 5.59 m (beyond 3.50 m: confidence factor 0.78)<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 18.91 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 32.42 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 37.27 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 22.75 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 29.98 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_017 | B:track_017 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_018 | B:track_018 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 27.37 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_019 | B:track_019 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Global graph

93 nodes, 488 edges; 1 merged node(s): g11 COLLISION(A,B) from A:e06 + B:e06.

### Event sequence (global time)

- `-3.70` MOVING_START(A); MOVING_START(B)
- `-2.50` TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A)
- `-2.05` CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-0.35` TRACK_LOST(B,A)
- `-0.25` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018)
- `+0.05` BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_006); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012)
- `+0.10` EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_RIGHT(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009)
- `+0.15` EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_LEFT(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008)
- `+0.20` EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015)
- `+0.25` EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006)
- `+0.30` CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_LOST(B,B:track_011)
- `+0.35` CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_012); EGO_PATH_ENTRY(B,B:track_009); TRACK_LOST(A,B); TRACK_LOST(B,B:track_003)
- `+0.40` CLOSING_END(B,B:track_009); CLOSING_END(B,B:track_018); EGO_PATH_EXIT(B,B:track_009); EGO_PATH_ENTRY(B,B:track_010)
- `+0.45` CLOSING_END(B,B:track_008); EGO_PATH_EXIT(B,B:track_010); EGO_PATH_ENTRY(B,B:track_008); TRACK_LOST(B,B:track_005)
- `+0.50` CRITICAL_TTC_END(B,B:track_015)
- `+0.55` CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_015); EGO_PATH_EXIT(B,B:track_008); TURN_LEFT_END(B); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_018)
- `+0.60` CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_016); CLOSING_END(B,B:track_017); MOVING_END(B); STOP_START(B)
- `+0.85` MOVING_END(A); STOP_START(A)
- `+1.25` EGO_PATH_ENTRY(B,B:track_008)
- `+1.40` EGO_PATH_EXIT(B,B:track_013)
- `+3.75` EGO_PATH_ENTRY(B,B:track_013)
- `+10.70` TRACK_LOST(B,B:track_004)

### What happened, in plain language

- 3.70 s before the reference collision, A started moving (already the case when first observed).
- 3.70 s before the reference collision, B started moving (already the case when first observed).
- 2.50 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.50 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.50 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's time-to-contact with B became critical.
- 2.05 s before the reference collision, B's time-to-contact with A became critical.
- 0.35 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.25 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B started turning left.
- At the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- At the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- At the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- At the reference collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- At the reference collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- At the reference collision, B's radar started tracking unidentified object B:track_018, which appeared on its left.
- At the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- At the reference collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- At the reference collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- At the reference collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- At the reference collision, B observed unidentified object B:track_018 start closing in (already the case when first observed).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_012, which appeared on its left.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_006, which appeared on its right.
- 0.05 s after the reference collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 0.05 s after the reference collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.10 s after the reference collision, B observed unidentified object B:track_003 leave its forward path corridor.
- 0.10 s after the reference collision, B's radar started tracking unidentified object B:track_008, which appeared on its left.
- 0.10 s after the reference collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 0.10 s after the reference collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 0.10 s after the reference collision, B's radar started tracking unidentified object B:track_011, which appeared on its right.
- 0.10 s after the reference collision, B observed unidentified object B:track_005 enter its forward path corridor.
- 0.10 s after the reference collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.15 s after the reference collision, B observed unidentified object B:track_005 leave its forward path corridor.
- 0.15 s after the reference collision, B's radar started tracking unidentified object B:track_013, which appeared on its left.
- 0.15 s after the reference collision, B's radar started tracking unidentified object B:track_014, which appeared on its left.
- 0.15 s after the reference collision, B observed unidentified object B:track_002 enter its forward path corridor.
- 0.15 s after the reference collision, B observed unidentified object B:track_008 start closing in.
- 0.20 s after the reference collision, A observed B leave its forward path corridor.
- 0.20 s after the reference collision, B observed unidentified object B:track_002 leave its forward path corridor.
- 0.20 s after the reference collision, B's radar started tracking unidentified object B:track_015, which appeared on its left.
- 0.20 s after the reference collision, B's radar started tracking unidentified object B:track_016, which appeared on its left.
- 0.20 s after the reference collision, B's radar started tracking unidentified object B:track_017, which appeared on its left.
- 0.20 s after the reference collision, B observed unidentified object B:track_018 enter its forward path corridor.
- 0.20 s after the reference collision, B observed unidentified object B:track_013 start closing in.
- 0.20 s after the reference collision, B observed unidentified object B:track_014 start closing in.
- 0.20 s after the reference collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.20 s after the reference collision, B's time-to-contact with unidentified object B:track_015 became critical (already the case when first observed).
- 0.25 s after the reference collision, B observed unidentified object B:track_018 leave its forward path corridor.
- 0.25 s after the reference collision, B observed unidentified object B:track_016 start closing in.
- 0.25 s after the reference collision, B observed unidentified object B:track_017 start closing in.
- 0.25 s after the reference collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.30 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.30 s after the reference collision, B observed unidentified object B:track_005 stop closing in.
- 0.30 s after the reference collision, B's radar started tracking unidentified object B:track_019, which appeared on its left.
- 0.30 s after the reference collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, B observed unidentified object B:track_004 stop closing in.
- 0.35 s after the reference collision, B observed unidentified object B:track_007 stop closing in.
- 0.35 s after the reference collision, B observed unidentified object B:track_012 stop closing in.
- 0.35 s after the reference collision, B observed unidentified object B:track_009 enter its forward path corridor.
- 0.35 s after the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.40 s after the reference collision, B observed unidentified object B:track_009 stop closing in.
- 0.40 s after the reference collision, B observed unidentified object B:track_018 stop closing in.
- 0.40 s after the reference collision, B observed unidentified object B:track_009 leave its forward path corridor.
- 0.40 s after the reference collision, B observed unidentified object B:track_010 enter its forward path corridor.
- 0.45 s after the reference collision, B observed unidentified object B:track_008 stop closing in.
- 0.45 s after the reference collision, B observed unidentified object B:track_010 leave its forward path corridor.
- 0.45 s after the reference collision, B observed unidentified object B:track_008 enter its forward path corridor.
- 0.45 s after the reference collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.50 s after the reference collision, B's time-to-contact with unidentified object B:track_015 stopped being critical.
- 0.55 s after the reference collision, B observed unidentified object B:track_013 stop closing in.
- 0.55 s after the reference collision, B observed unidentified object B:track_015 stop closing in.
- 0.55 s after the reference collision, B observed unidentified object B:track_008 leave its forward path corridor.
- 0.55 s after the reference collision, B stopped turning left.
- 0.55 s after the reference collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 0.55 s after the reference collision, B's radar lost unidentified object B:track_018 (its states are UNKNOWN from then on, not ended).
- 0.60 s after the reference collision, B observed unidentified object B:track_014 stop closing in.
- 0.60 s after the reference collision, B observed unidentified object B:track_016 stop closing in.
- 0.60 s after the reference collision, B observed unidentified object B:track_017 stop closing in.
- 0.60 s after the reference collision, B stopped moving.
- 0.60 s after the reference collision, B came to a stop.
- 0.85 s after the reference collision, A stopped moving.
- 0.85 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, B observed unidentified object B:track_008 enter its forward path corridor.
- 1.40 s after the reference collision, B observed unidentified object B:track_013 leave its forward path corridor.
- 3.75 s after the reference collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 10.70 s after the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 1.65, COLLISION with B 3.70 (+2.05 s); EGO_PATH_ENTRY 3.45 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -2.05, ego_path_entry -0.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 1.65, COLLISION with A 3.70 (+2.05 s) [local times; t_global: critical_ttc_start -2.05, collision +0.00]
- B's track_002 (unidentified B:track_002): EGO_PATH_ENTRY 3.85, no critical TTC [local times; t_global: ego_path_entry +0.15]
- B's track_003 (unidentified B:track_003): EGO_PATH_ENTRY 3.75, no critical TTC [local times; t_global: ego_path_entry +0.05]
- B's track_005 (unidentified B:track_005): EGO_PATH_ENTRY 3.80, no critical TTC [local times; t_global: ego_path_entry +0.10]
- B's track_008 (unidentified B:track_008): EGO_PATH_ENTRY 4.15, no critical TTC [local times; t_global: ego_path_entry +0.45]
- B's track_009 (unidentified B:track_009): EGO_PATH_ENTRY 4.05, no critical TTC [local times; t_global: ego_path_entry +0.35]
- B's track_010 (unidentified B:track_010): EGO_PATH_ENTRY 4.10, no critical TTC [local times; t_global: ego_path_entry +0.40]
- B's track_013 (unidentified B:track_013): EGO_PATH_ENTRY 4.25, no critical TTC [local times; t_global: ego_path_entry +0.55]
- B's track_015 (unidentified B:track_015): CRITICAL_TTC_START 3.90 [local times; t_global: critical_ttc_start +0.20]
- B's track_018 (unidentified B:track_018): EGO_PATH_ENTRY 3.90, no critical TTC [local times; t_global: ego_path_entry +0.20]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A)
- CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018)
- BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_006); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012)
- EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_RIGHT(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009)
- EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_LEFT(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008)
- EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015)
- EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006)
- CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_LOST(B,B:track_011)
- CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_012); EGO_PATH_ENTRY(B,B:track_009); TRACK_LOST(A,B); TRACK_LOST(B,B:track_003)
- CLOSING_END(B,B:track_009); CLOSING_END(B,B:track_018); EGO_PATH_EXIT(B,B:track_009); EGO_PATH_ENTRY(B,B:track_010)
- CLOSING_END(B,B:track_008); EGO_PATH_EXIT(B,B:track_010); EGO_PATH_ENTRY(B,B:track_008); TRACK_LOST(B,B:track_005)
- CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_015); EGO_PATH_EXIT(B,B:track_008); TURN_LEFT_END(B); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_018)
- CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_016); CLOSING_END(B,B:track_017); MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e09 (t = 3.75 s)
- STOP, since A:e13 (t = 4.55 s)
B:
- CLOSING of track_001, since B:e03 (t = 1.20 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_001, since B:e04 (t = 1.65 s); the track was lost at 3.35 s
- BRAKE, since B:e19 (t = 3.75 s)
- STOP, since B:e77 (t = 4.30 s)
- EGO_PATH of track_008, since B:e78 (t = 4.95 s)
- EGO_PATH of track_013, since B:e80 (t = 7.45 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e06 at 3.70 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH
- B B:e06 at 3.70 s (local): ego: MOVING; track lost, states UNKNOWN: track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_001
B:
- track_001 at 3.35 s (B:e05): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_006, track_011, track_003, track_005, track_018, track_004

## Uncertainty and limitations

- B:track_002 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_009 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_011 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_012 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_013 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.15 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_014 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.15 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_015 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.20 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_016 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.20 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_017 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.20 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_018 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_019 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.30 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- Global time rests on matched collisions (t_global = 0 at the reference one) and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from the collisions that align each recorder.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5,
    "new_impact_ratio": 0.5,
    "reversal_impact_ratio": 0.25,
    "impact_acceleration_mps2": 20.0,
    "reversal_angle_deg": 90.0
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
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_release_ratio": 0.75,
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
    "track_appeared_front_deg": 5.0,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
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
    "clock_tolerance_s": 0.1,
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
