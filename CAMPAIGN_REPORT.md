# Semantic-event redesign: full-scenario campaign report (2026-09-29)

Updated 2026-10-01: every run now has the 200 deg radar (S01-S05 re-recorded in `7f8d00f`, S06-S16 in
`e2153e1`), S02 `critical_before_cut_in` was added (33 runs), and every reconstruction was regenerated after
the close-multiple-collision fix (section 9). The section 3 table, the section 7 sequences,
`traces/campaign_summary.json` and `traces/radar_visibility_audit.json` come from the current
reconstructions. Sections 1, 2 and 4-6 describe the campaign as of 2026-09-29, section 8 the first
world-model version (120 deg radar).

Canonical dataset: `traces/<Sxx>/run_0_<variant>` (the 33 runs of this campaign); each run has
`reconstruction/` (local, global, evaluation). Campaign-level files: `traces/campaign_runs.json` (the
recording log of the 32 runs of 2026-09-29),
`traces/campaign_summary.json`, `traces/stop_sign_audit.json`, `traces/vocabulary_comparison.json`,
`traces/radar_visibility_audit.json` (privileged).

## 1. What was done

- Event layer redesigned as START/END state transitions (facts stay in the 10 Hz trace), speed limit supplied
  as explicit incident context (50 km/h for every scenario: all are ordinary urban roads/junctions; none is
  declared a 30 zone or a motorway), sparse PRECEDES (never between equal times), rendering/docs updated.
- Fresh CARLA campaign: all 32 configured scenario variants, seed 0, recorded under `-quality-level=Epic`
  (see section 2); every run recorded on its first attempt. Every run reconstructed, then evaluated.
- Validation found and fixed 4 issues (commits `dac9c43`, `8496cbe`, `96ec862`, `fa51001`), and the
  CARLA crashes (`609ee98`).

Commits (oldest first): `19a6572` state transitions + tests · `2cf26c6` incident context · `9445243` rendering/docs ·
`b94f36c` per-scenario context · `dac9c43` zero-length state order, sign ids · `8496cbe` final trace frame ·
`609ee98` CARLA Epic + unattended · `96ec862` TRACK_LOST last, open-state reporting · `fa51001` CRITICAL_TTC nests in CLOSING.

Tests: 85 passed on Python 3.8.20 (carla env) and 3.14.

## 2. CARLA "fatal error" crashes

- Root cause (CARLA 0.9.15 bug): use-after-free on the render thread. A camera scene capture renders a
  vehicle skeletal mesh whose mesh object was already freed:
  `FSkeletalMeshSceneProxy::GetMeshElementsConditionallySelectable` <- `GetDynamicMeshElements` <-
  `FSceneRenderer::GatherDynamicMeshElements` <- ... <- `FDeferredShadingSceneRenderer::Render_CARLA` <-
  `UpdateSceneCaptureContent_RenderThread`, resolved with the PDB shipped with CARLA. About 60 crash reports
  since 2026-09-16 share this stack.
- Deterministic under `-quality-level=Low` (with or without `-RenderOffScreen`): S05 crash at tick 66
  (3 of 3 attempts), S13 accelerates_into_gap at tick 127 (2 of 2), S08 before its first tick (2 of 2).
- Under `-quality-level=Epic` the same three runs complete. Vehicle physics is bit-identical between Low and
  Epic (ego poses, controls, collisions). Radar returns differ slightly (+1-3 %: Low removes foliage) and
  camera images differ. Reconstructions of the 19 runs recorded under both: identical event graphs apart from
  STOP-sign windows in 17 runs; S02 crash differs only because that Low run was itself a one-off divergent
  recording (below); S12 near_simultaneous differs only in clutter tracks after 9.4 s; identity associations
  identical in all 19.
- Fix: CARLA now starts with `-quality-level=Epic -unattended` (`simulation.quality_level`,
  `simulation.unattended`). `-unattended` makes a crashed engine exit instead of showing a blocking dialog.
- The 19 runs recorded under Low before the fix were used only for this comparison and have been removed
  from the workspace (they are not part of the canonical dataset).

Determinism: S01, S02 (both variants) and S03 are bit-identical across CARLA sessions and quality levels,
and the Epic S02 crash equals the S02 crash committed in `a4a71ca` (previously at `traces/S02/run_0_crash`,
now replaced there by the Epic run). Only the Low partial S02 crash diverged
(B from t = 0, max 0.42 m): a one-off in that CARLA session, not reproduced.

## 3. Run matrix and per-run table

33 runs = S01 {avoided, crash}, S02 {avoided, crash, critical_before_cut_in}, S03 crash, S04 yield, S05 crash, S06 {a_front_pushed,
b_rear_first}, S07 {full_view, occluded}, S08 crash, S09 merge_conflict (Town03_Opt), S10 / S11 {rolls_through,
stops_safely, stops_then_proceeds}, S12 {a_arrives_first, b_arrives_first, b_fails_to_stop, near_simultaneous},
S13 {accelerates_into_gap, cut_in, safe_lane_change}, S15 {b_stops, deflected_into_c, single_impact},
S16 {avoided, consequential, independent}; Town05 except S09. Seed 0, speed limit 50 km/h in every run.

Transition counts are START/END over the global graph (all recorders). BR brake, TL / TR turn left /
right, MOV moving, STOP stop, SPD speed limit exceeded, CLS closing, TTC critical TTC, CUTL / CUTR cut-in from
the left / right, STOPSIGN STOP sign detected, TRACK appeared (FRONT/LEFT/RIGHT) / lost, PATH ego-path
entry/exit, COLL collision nodes (a contact matched across recorders is one node). "ok via collision_00x":
aligned through a chain of matched collisions (multi-hop, section 9). No YIELD sign was detected in any run
(the two maps contain no yield-sign actors), so YIELD_SIGN_DETECTED never occurs.

| Run | Limit | Local A/B/C nodes:edges | Global nodes:edges | Collision reconstructed | Alignment | Identity associations | Transitions (START/END) |
|---|---:|---|---|---|---|---|---|
| S01/run_0_avoided | 50 | A 11:16 B 7:7 | 18:6 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 2/1, MOV 3/2, STOP 2/1, CLS 2/2, TTC 1/1, TRACK 1/0, PATH 0/0, COLL 0 |
| S01/run_0_crash | 50 | A 12:21 B 5:5 | 16:26 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.99) | BR 2/0, MOV 2/2, STOP 2/0, CLS 2/2, TTC 1/1, TRACK 1/0, PATH 0/0, COLL 1 |
| S02/run_0_avoided | 50 | A 9:13 B 3:2 | 12:5 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 2/2, MOV 2/0, CLS 1/1, CUTL 1/1, TRACK 1/0, PATH 1/0, COLL 0 |
| S02/run_0_crash | 50 | A 13:23 B 7:8 | 19:33 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.95) | BR 3/1, MOV 2/2, STOP 2/0, CLS 1/1, TTC 1/1, CUTL 1/1, TRACK 1/0, PATH 1/0, COLL 1 |
| S02/run_0_critical_before_cut_in | 50 | A 15:21 B 7:6 | 21:32 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.67) | BR 4/2, MOV 2/2, STOP 2/0, CLS 1/0, TTC 2/1, CUTL 1/0, TRACK 1/1, PATH 1/0, COLL 1 |
| S03/run_0_crash | 50 | A 9:12 B 12:21 | 20:37 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.96); B:track_001→A (0.75) | BR 2/0, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, TRACK 2/1, PATH 1/1, COLL 1 |
| S04/run_0_yield | 50 | A 41:146 B 15:22 | 56:27 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 16 | BR 2/2, TL 1/0, MOV 3/1, STOP 1/1, CLS 14/2, TTC 2/1, STOPSIGN 1/1, TRACK 16/6, PATH 1/1, COLL 0 |
| S05/run_0_crash | 50 | A 13:22 B 81:409 | 93:488 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.90); B:track_001→A (0.73); anonymous 18 | BR 2/0, TL 1/1, MOV 2/2, STOP 2/0, CLS 15/14, TTC 3/2, TRACK 20/8, PATH 11/9, COLL 1 |
| S06/run_0_a_front_pushed | 50 | A 12:17 B 20:33 C 7:7 | 37:63 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | A:track_001→B (0.67); B:track_001→C (0.99) | BR 3/1, MOV 4/4, STOP 4/1, SPD 1/1, CLS 4/4, TTC 3/2, TRACK 2/1, PATH 0/0, COLL 2 |
| S06/run_0_b_rear_first | 50 | A 9:11 B 13:23 C 7:7 | 27:41 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | B:track_001→C (0.97); anonymous 1 (A:track_001) | BR 3/0, MOV 3/3, STOP 3/0, SPD 1/1, CLS 3/3, TTC 1/1, TRACK 2/1, PATH 0/0, COLL 2 |
| S07/run_0_full_view | 50 | A 12:19 B 12:19 C 9:9 | 32:45 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_001→B (0.98); anonymous 1 (B:track_001) | BR 3/1, MOV 4/3, STOP 3/1, SPD 1/1, CLS 4/4, TTC 2/2, TRACK 2/0, PATH 0/0, COLL 1 |
| S07/run_0_occluded | 50 | A 12:19 B 12:19 C 9:9 | 32:45 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_001→B (0.98); anonymous 1 (B:track_001) | BR 3/1, MOV 4/3, STOP 3/1, SPD 1/1, CLS 4/4, TTC 2/2, TRACK 2/0, PATH 0/0, COLL 1 |
| S08/run_0_crash | 50 | A 16:27 B 17:33 C 15:27 | 47:77 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_002→B (0.96); B:track_002→A (0.75); anonymous 4 | BR 3/1, MOV 3/3, STOP 3/0, CLS 6/5, TTC 7/6, TRACK 6/1, PATH 1/1, COLL 1 |
| S09/run_0_merge_conflict | 50 | A 51:194 B 46:195 | 96:749 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.68); anonymous 27 | BR 2/0, TL 2/2, TR 1/1, MOV 2/2, STOP 2/0, CLS 18/8, TTC 2/1, CUTR 1/1, TRACK 28/21, PATH 1/0, COLL 1 |
| S10/run_0_rolls_through | 50 | A 16:26 B 11:18 | 26:51 | yes (1/1 vehicle contacts) | A ok B ok | B:track_001→A (0.91); anonymous 1 (A:track_001) | BR 3/1, TL 1/1, MOV 2/2, STOP 2/0, CLS 2/2, TTC 2/1, STOPSIGN 1/1, TRACK 2/1, PATH 1/0, COLL 1 |
| S10/run_0_stops_safely | 50 | A 12:18 B 8:12 | 20:9 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, MOV 2/1, STOP 1/0, CLS 2/1, TTC 1/1, STOPSIGN 2/2, TRACK 2/2, PATH 1/1, COLL 0 |
| S10/run_0_stops_then_proceeds | 50 | A 67:176 B 6:10 | 73:45 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 16 | BR 1/1, TL 1/1, MOV 3/1, STOP 1/1, CLS 16/4, TTC 4/2, CUTL 2/0, CUTR 1/0, STOPSIGN 1/1, TRACK 16/14, PATH 1/1, COLL 0 |
| S11/run_0_rolls_through | 50 | A 9:12 B 17:23 | 25:48 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.90); B:track_001→A (0.98) | BR 3/1, TL 1/1, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, STOPSIGN 1/1, TRACK 2/1, PATH 1/0, COLL 1 |
| S11/run_0_stops_safely | 50 | A 4:6 B 12:18 | 16:7 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, MOV 2/1, STOP 1/0, CLS 2/1, STOPSIGN 1/1, TRACK 2/2, PATH 1/1, COLL 0 |
| S11/run_0_stops_then_proceeds | 50 | A 4:6 B 57:205 | 61:35 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 14 | BR 1/1, TL 1/1, MOV 3/1, STOP 1/1, CLS 14/3, TTC 1/0, CUTL 1/0, CUTR 1/0, STOPSIGN 1/1, TRACK 14/13, PATH 1/1, COLL 0 |
| S12/run_0_a_arrives_first | 50 | A 66:171 B 16:26 | 82:43 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 19 | BR 2/2, TL 1/1, MOV 4/2, STOP 2/2, CLS 19/2, TTC 2/2, STOPSIGN 2/2, TRACK 19/13, PATH 3/2, COLL 0 |
| S12/run_0_b_arrives_first | 50 | A 65:178 B 14:21 | 79:39 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 20 | BR 2/2, TL 1/1, MOV 4/2, STOP 2/2, CLS 20/3, CUTR 1/0, STOPSIGN 2/2, TRACK 20/10, PATH 3/2, COLL 0 |
| S12/run_0_b_fails_to_stop | 50 | A 19:25 B 25:54 | 43:91 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.96); B:track_001→A (0.92); anonymous 3 (B:track_002, B:track_003, B:track_004) | BR 4/2, TL 1/1, MOV 3/3, STOP 3/1, CLS 5/4, TTC 2/1, STOPSIGN 2/2, TRACK 5/2, PATH 1/0, COLL 1 |
| S12/run_0_near_simultaneous | 50 | A 81:353 B 23:37 | 103:439 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.90); B:track_001→A (0.69); anonymous 18 | BR 4/2, TL 1/1, MOV 4/4, STOP 4/2, CLS 21/20, TTC 2/1, STOPSIGN 3/2, TRACK 20/8, PATH 1/2, COLL 1 |
| S13/run_0_accelerates_into_gap | 50 | A 20:35 B 153:753 | 172:998 | yes (1/1 vehicle contacts) | A ok B ok | A:track_002→B (0.93); anonymous 43 | BR 2/0, TR 1/1, MOV 2/2, STOP 2/0, SPD 1/1, CLS 44/25, TTC 4/4, CUTL 1/1, TRACK 44/30, PATH 5/1, COLL 1 |
| S13/run_0_cut_in | 50 | A 13:22 B 22:95 | 34:138 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.98); anonymous 5 | BR 2/0, TR 1/1, MOV 2/2, STOP 2/0, CLS 6/6, TTC 1/1, CUTL 1/1, TRACK 6/0, PATH 1/0, COLL 1 |
| S13/run_0_safe_lane_change | 50 | A 9:14 B 1:0 | 10:6 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 1/0, MOV 2/0, CLS 2/1, CUTL 1/1, TRACK 1/0, PATH 1/0, COLL 0 |
| S15/run_0_b_stops | 50 | A 10:21 B 24:39 C 9:17 | 43:24 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED C UNALIGNED | none; anonymous 6 | BR 1/0, TL 1/1, MOV 3/1, STOP 1/0, CLS 6/4, TTC 4/1, STOPSIGN 3/2, TRACK 6/5, PATH 2/2, COLL 0 |
| S15/run_0_deflected_into_c | 50 | A 26:43 B 40:96 C 14:23 | 78:195 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | A:track_001→C (0.94); A:track_002→B (0.85); B:track_002→A (0.88); C:track_002→A (0.92); anonymous 8 | BR 3/1, TL 2/2, MOV 3/3, STOP 3/0, CLS 12/3, TTC 5/3, STOPSIGN 6/5, TRACK 12/9, PATH 3/1, COLL 2 |
| S15/run_0_single_impact | 50 | A 20:36 B 33:74 C 10:19 | 62:137 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_002→B (0.85); B:track_001→A (0.88); anonymous 8 | BR 2/1, TL 2/2, MOV 3/2, STOP 2/0, CLS 11/2, TTC 3/1, STOPSIGN 4/3, TRACK 10/6, PATH 4/3, COLL 1 |
| S16/run_0_avoided | 50 | A 5:4 B 14:24 C 3:2 | 21:30 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | B:track_001→A (0.94) | BR 2/0, MOV 3/3, STOP 3/0, CLS 2/2, TTC 2/2, TRACK 1/0, PATH 0/0, COLL 1 |
| S16/run_0_consequential | 50 | A 27:55 B 14:24 C 9:13 | 48:121 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | B:track_001→A (0.94); anonymous 6 | BR 3/1, TL 1/1, MOV 4/4, STOP 4/1, CLS 6/6, TTC 3/3, TRACK 7/1, PATH 1/0, COLL 2 |
| S16/run_0_independent | 50 | A 20:30 B 19:34 C 13:19 | 50:85 | yes (2/2 vehicle contacts) | A ok B ok via collision_001 C ok | A:track_002→C (1.00); B:track_001→A (0.94); anonymous 3 (A:track_001, B:track_002, B:track_003) | BR 3/1, MOV 5/5, STOP 5/2, CLS 4/3, TTC 3/2, STOPSIGN 1/1, YIELDSIGN 1/1, TRACK 5/4, PATH 1/1, COLL 2 |

Evaluation (privileged, after reconstruction): each of the 27 true vehicle-vehicle contacts is one merged
COLLISION node with the right participants and no COLLISION node reproduces no contact; all 34 identity
claims are correct; aligned global times have 0.0 s error; shifting a recorder's clock by 0.73 s leaves every
global graph unchanged.

## 4. Highlights

### Unresolved identities
- Every run without a vehicle-vehicle collision has unaligned graphs and therefore only anonymous tracks,
  even when a track obviously is the other vehicle (e.g. S01 avoided A:track_001, S02 avoided A:track_001).
  This is the collision-anchored alignment by design.
- S03 crash: A:track_001 stays anonymous (regression case preserved): A lost it at 3.35 s, before the contact.
- Post-impact clutter: B in S05 (17 anonymous tracks) and B in S13 accelerates_into_gap (16) start tracks on the
  static world while spinning after the impact (all appear at or after the collision instant).
- Turning / pull-away clutter: S10 stops_then_proceeds A (8 tracks), S11 stops_then_proceeds B (5),
  S12 a_arrives_first A (12), b_arrives_first A (13), near_simultaneous A (8). Same counts under Low and in the
  old implementation, so neither the event redesign nor the quality level causes them.
- Low-confidence associations: S09 A:track_001 -> B 0.63, S06 a_front_pushed A:track_001 -> B 0.67,
  S12 near_simultaneous B:track_001 -> A 0.79 (all correct).

### Missing expected events / collisions
- Secondary collisions are not merged (evaluation "collision reconstructed: NO"): S06 a_front_pushed (B's contacts
  with A at 5.90 s and C at 6.15 s fall within the 0.5 s merge gap and become one COLLISION, so C matches
  nothing), S06 b_rear_first (C shares only the non-reference collision; multi-hop alignment not implemented),
  S15 deflected_into_c, S16 consequential, S16 independent. The third vehicle is UNALIGNED in every
  three-vehicle run.
- Unaligned (no-collision) runs have no global PRECEDES; each local graph keeps its own order. Same as the old
  implementation.
- LANE_DEPARTURE and LEFT/RIGHT_TURN_SIGNAL are never emitted: the recordings contain no lane or indicator
  evidence (names reserved, nothing fabricated).

### States active when observation ended (no END invented)
- After every collision the post-impact BRAKE, HARD_BRAKE and STOP stay open to the recording end.
- Vehicles still MOVING at the end in avoided / no-collision runs.
- Track states left open by TRACK_LOST, e.g. S03 A CLOSING and CRITICAL_TTC of track_001 (track lost at 3.35 s),
  and the EGO_PATH states in S10/S11 rolls_through and S12 b_fails_to_stop (entry in the track's last sample).
- STRONG_THROTTLE open together with BRAKE/HARD_BRAKE at the end (S01 avoided A, S10 stops_safely A,
  S11 stops_safely B, S15 b_stops B): see raw-faithful behaviour.

### Same-timestamp ambiguities (simultaneous, no PRECEDES between them)
- COLLISION with STRONG_THROTTLE_START in 14 runs (one-sample throttle spike, below).
- COLLISION with CRITICAL_TTC_END / CLOSING_END (range collapses at contact) and, in S02 crash B, with
  BRAKE_START / HARD_BRAKE_START.
- BRAKE_START with HARD_BRAKE_START (pedal jumps to >= 0.9 in one step); MOVING_END with STOP_START and STOP_END
  with MOVING_START (by definition).
- EGO_PATH_ENTRY with TRACK_LOST (S10 and S11 rolls_through, S12 b_fails_to_stop, S16 consequential).
- Zero-length sign windows (START and END at the same time: one confirmation only), e.g. S12 near_simultaneous
  A sign-4, S15 deflected_into_c A sign-0 / sign-3, S15 single_impact A sign-0.
- After alignment, simultaneous events of different recorders (e.g. S03 BRAKE_START(A), BRAKE_START(B) at +0.05 s).

### Speed-limit context
- No context problem: every scenario is an ordinary urban road or junction at 50 km/h.
- SPEED_LIMIT_EXCEEDED occurs in 5 runs: C in S06 (both variants) and S07 (both), 2.40-3.05/3.10 s, peak
  51.5-51.7 km/h. C is configured at 14.0 m/s = 50.4 km/h, i.e. above the declared limit; its controller
  overshoot crosses the 51 km/h on-threshold. In S13 accelerates_into_gap, A exceeds from 2.75 s until the
  collision at 5.65 s, peak 54.5 km/h (the END is simultaneous with COLLISION).

### Surprising but raw-faithful behaviour
- One-sample full throttle at the collision frame: the scenario speed controller reacts to the impact's speed
  drop (e.g. S03 B 12.6 -> 5.2 m/s) one tick before the post-impact brake engages.
- Full throttle in the very last control sample when a scripted brake window ends at the recording end (S01
  avoided A 13.05 s, S10 stops_safely A 9.55 s, ...): STRONG_THROTTLE_START is observed, but the 0.2 s release
  debounce cannot confirm the brake release, so BRAKE and STRONG_THROTTLE are both open at the end.
- S16 C (configured at 1 m/s) starts at 0.66 m/s and stops at 0.30 s: MOVING_START (active at first
  observation) then STOP_START.
- S16 independent B: track first seen inside the corridor, so EGO_PATH_EXIT without an ENTRY (by design).

## 5. STOP-sign audit

Question: can compliance be checked as "a STOP_START strictly inside the STOP_SIGN_DETECTED window"?
The governing sign of each approach was identified privilegedly (CARLA `traffic.stop` actors whose trigger
volume the vehicle drives through), only for this audit. "Stop vs trigger" is the distance from the camera to
the trigger centre at STOP_START (positive: stopped before it).

| Run | Recorder (STOP approach) | Window(s) t_local | Sign at window END | Relevant flag | Stopped before the junction? | STOP_START inside |
|---|---|---|---|---|---|---|
| S10 rolls_through | A | 1.85 -> 2.15 | 5.8 m ahead, 38.6 deg | False | no (rolls through; stops only after the collision) | none |
| S10 stops_safely | A | 1.90 -> 2.15 | 5.7 m, 38.9 deg | False | yes, 3.35 s (-2.4 m, at the line) | none |
| S10 stops_then_proceeds | A | 1.75 -> 2.15 | 5.7 m, 38.9 deg | False | yes, 3.35 s (-2.4 m) | none |
| S11 rolls_through | B | 2.10 -> 2.45 | 5.1 m, 41.7 deg | False | no | none |
| S11 stops_safely | B | 2.10 -> 2.35 | 5.5 m, 40.3 deg | False | yes, 3.25 s (-0.6 m) | none |
| S11 stops_then_proceeds | B | 2.10 -> 2.40 | 5.0 m, 43.0 deg | False | yes, 3.25 s (-0.6 m) | none |
| S12 a_arrives_first | A | 0.65 -> 2.25 | 8.9 m ahead | True | yes, 3.40 s (+0.8 m) | none |
| S12 a_arrives_first | B | 2.10 -> 4.00 | 5.1 m, 41.3 deg | False | yes, 4.70 s (+2.0 m) | none |
| S12 b_arrives_first | A | 1.05 -> 3.55 | 8.8 m ahead | True | yes, 4.75 s (+2.9 m) | none |
| S12 b_arrives_first | B | 2.10 -> 2.60 | 5.0 m, 42.1 deg | True | yes, 3.40 s (+0.2 m) | none |
| S12 b_fails_to_stop | A | 0.65 -> 2.25 | 8.9 m ahead | True | yes, 3.40 s (+0.8 m) | none |
| S12 b_fails_to_stop | B | 3.50 -> 5.30 | 4.8 m, 43.2 deg | False | no (fails to stop) | none |
| S12 near_simultaneous | A | 0.65 -> 2.25 | 8.9 m ahead | True | yes, 3.40 s (+0.9 m) | none |
| S12 near_simultaneous | B | 2.10 -> 2.60 | 5.0 m, 42.1 deg | True | yes, 3.50 s (-0.6 m) | none |
| S15 b_stops | B | 1.80 -> 2.10 | 5.5 m, 40.4 deg | False | yes, 3.40 s (-4.5 m, past the line) | none |
| S15 deflected_into_c / single_impact | B | 1.80 -> 2.10 | 5.5 m, 40.4 deg | False | no (rolls through) | none |

(S12 A's `traffic.stop` actor sits in the lane, so its bearing does not describe the pole; the pole-side
signs of S10/S11/S12 B/S15 sit about 4.5 m right of the lane. Later windows of other signs, detected while
already stopped or after crossing, are omitted.)

Findings:
- In none of the 17 approaches does a STOP_START fall inside a detection window, although 12 vehicles did stop
  at the line. The check returns the same answer for compliant and violating runs, so it cannot decide
  compliance.
- The window ends while the sign is still 4.8-5.8 m ahead at 38-43 deg (roadside signs), or 9 m ahead (S12 A);
  the vehicle stops 0.7-1.3 s later, when the sign is beside it and outside the 90 deg field of view.
- Detection also starts late: under Epic the roadside signs are first confirmed only 8-9 m ahead in S10/S11/S15
  (9-16 m for S12 B), so those windows last 0.25-0.5 s (S12: 0.5-2.5 s). With the sign 16-43 deg off-axis the
  relevance heuristic (centredness >= 0.35 and growing) marks the governing sign "not relevant" in 11 of 17
  approaches.
- The junction used by S03/S04/S05/S08 has STOP trigger volumes on both approaches (A and B drive through
  them), but the camera never detected those signs and the scenario descriptions call it an unsignalised /
  priority crossing (S05). Scenarios were not changed.

Diagnosis and recommendation:
1. Semantic window definition (primary): END is, as specified, the end of the tracked perception window, not the
   end of the obligation. A compliance check needs an obligation interval: from STOP_SIGN_DETECTED_START until
   the recorder passes the sign, with the sign position estimated locally from the detection geometry (bbox
   size and bearing) and ego odometry. No map is needed. This belongs to a later reasoning layer.
2. Sensor FOV (contributing): a forward 90 deg camera cannot see a roadside sign at the stop line.
3. Detector timing (contributing): late first confirmation and an image-centre relevance heuristic that rejects
   normal roadside signs.
4. Scenario geometry / timing: not the cause for S10-S12/S15 (stops are within -4.5 .. +2.9 m of the trigger
   centre); the S03-S08 junction's undetected STOP signs are a scenario/map mismatch to note.

## 6. Old vs new implementation (same raw runs, pre-change code at a4a71ca)

- Collision nodes, alignment, identity associations and radar tracks: identical in all 32 runs.
- Nodes per global graph: 5-59 old vs 10-86 new (START/END pairs instead of onsets).
- Count differences, none a regression:
  - STRONG_THROTTLE_START vs old THROTTLE_ONSET (+1 in 8 runs): the old rule needed 0.5 s below 0.8 first, so
    it missed onsets right after the recording start (e.g. S01 B at 0.40 s).
  - STOP_START vs old FULL_STOP (+1 in the three S16 runs): the old rule needed > 1 m/s before arming; S16 C
    starts at 0.66 m/s and stops at 0.30 s.
  - CRITICAL_TTC (S02 avoided, 0 -> 1) and CLOSING (S13 accelerates_into_gap, 17 -> 19): borderline 0.3 s
    minimum-duration episodes. The old rule measured duration to the last inside sample, the new one to the
    first outside sample.

## 7. Global event sequences

Aligned runs: global time, 0 = reference collision. Unaligned runs: each recorder's local sequence in its own
clock (`*` = already active at the first observation).

**S01/run_0_avoided** (global graph, unaligned nodes: 18)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.10 TRACK_APPEARED_FRONT(track_001); 0.45 CLOSING_START(track_001); 1.60 CLOSING_END(track_001); 4.25 CLOSING_START(track_001); 5.00 CRITICAL_TTC_START(track_001); 5.05 BRAKE_START; 6.25 CRITICAL_TTC_END(track_001); 6.35 CLOSING_END(track_001); 6.35 MOVING_END; 6.35 STOP_START
B: 0.00 MOVING_START*; 3.95 BRAKE_START; 5.15 MOVING_END; 5.15 STOP_START; 11.95 BRAKE_END; 12.35 STOP_END; 12.35 MOVING_START
```

**S01/run_0_crash** (global graph)

```
-6.50 MOVING_START(A); MOVING_START(B)
-6.40 TRACK_APPEARED_FRONT(A,B)
-6.05 CLOSING_START(A,B)
-4.90 CLOSING_END(A,B)
-2.55 BRAKE_START(B)
-2.25 CLOSING_START(A,B)
-1.50 CRITICAL_TTC_START(A,B)
-1.35 MOVING_END(B); STOP_START(B)
-0.95 BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 MOVING_END(A); STOP_START(A)
```

**S02/run_0_avoided** (global graph, unaligned nodes: 12)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_LEFT(track_001); 0.00 CLOSING_START(track_001)*; 2.35 CUT_IN_FROM_LEFT_START(track_001); 2.85 BRAKE_START; 3.25 EGO_PATH_ENTRY(track_001); 4.05 CLOSING_END(track_001); 4.10 BRAKE_END; 5.30 CUT_IN_FROM_LEFT_END(track_001)
B: 0.00 MOVING_START*; 3.15 BRAKE_START; 3.60 BRAKE_END
```

**S02/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-1.90 CUT_IN_FROM_LEFT_START(A,B)
-1.10 BRAKE_START(B)
-1.05 CRITICAL_TTC_START(A,B)
-0.95 EGO_PATH_ENTRY(A,B)
-0.65 BRAKE_END(B)
-0.40 BRAKE_START(A)
+0.00 COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B); BRAKE_START(B)
+0.05 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.60 MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
```

**S02/run_0_critical_before_cut_in** (global graph)

```
-3.85 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-3.10 CRITICAL_TTC_START(A,B)
-2.60 CRITICAL_TTC_END(A,B)
-2.45 BRAKE_START(B)
-2.30 BRAKE_END(B); CRITICAL_TTC_START(A,B)
-1.40 BRAKE_START(A)
-1.15 CUT_IN_FROM_LEFT_START(A,B)
-0.65 BRAKE_END(A)
-0.45 EGO_PATH_ENTRY(A,B)
-0.15 TRACK_LOST(A,B)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.50 MOVING_END(B); STOP_START(B)
+0.60 MOVING_END(A); STOP_START(A)
```

**S03/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B)
-2.20 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.05 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.90 CRITICAL_TTC_START(B,A)
-1.80 CRITICAL_TTC_START(A,B)
-0.15 TRACK_LOST(A,B)
-0.10 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.10 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.30 MOVING_END(B); STOP_START(B)
+0.45 EGO_PATH_EXIT(B,A)
+0.65 MOVING_END(A); STOP_START(A)
```

**S04/run_0_yield** (global graph, unaligned nodes: 56)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.00 TRACK_APPEARED_RIGHT(track_001); 2.00 CLOSING_START(track_001)*; 3.15 CRITICAL_TTC_START(track_001); 4.95 CRITICAL_TTC_END(track_001); 5.25 TRACK_LOST(track_001); 8.20 STOP_SIGN_DETECTED_START(sign-0); 8.45 STOP_SIGN_DETECTED_END(sign-0); 8.65 TURN_LEFT_START; 9.35 TRACK_APPEARED_LEFT(track_002); 9.35 TRACK_APPEARED_LEFT(track_003); 9.35 TRACK_APPEARED_LEFT(track_004); 9.35 TRACK_APPEARED_LEFT(track_005); 9.35 TRACK_APPEARED_LEFT(track_006); 9.35 TRACK_APPEARED_LEFT(track_010); 9.35 CLOSING_START(track_002)*; 9.35 CLOSING_START(track_003)*; 9.35 CLOSING_START(track_004)*; 9.35 CLOSING_START(track_005)*; 9.35 CLOSING_START(track_006)*; 9.35 CLOSING_START(track_010)*; 9.45 TRACK_APPEARED_LEFT(track_007); 9.45 TRACK_APPEARED_LEFT(track_011); 9.45 CLOSING_START(track_007)*; 9.45 CLOSING_START(track_011)*; 9.50 TRACK_APPEARED_LEFT(track_012); 9.50 TRACK_APPEARED_LEFT(track_014); 9.50 TRACK_APPEARED_LEFT(track_015); 9.50 TRACK_APPEARED_RIGHT(track_008); 9.50 TRACK_APPEARED_RIGHT(track_009); 9.50 CLOSING_START(track_009)*; 9.50 CLOSING_START(track_012)*; 9.50 CLOSING_START(track_014)*; 9.50 CLOSING_START(track_015)*; 9.70 TRACK_APPEARED_RIGHT(track_013); 9.75 TRACK_LOST(track_008); 9.85 CLOSING_END(track_009); 9.85 TRACK_LOST(track_011); 9.85 TRACK_LOST(track_012); 9.90 CRITICAL_TTC_START(track_006); 9.90 TRACK_LOST(track_009)
B: 0.00 MOVING_START*; 1.95 TRACK_APPEARED_LEFT(track_001); 1.95 CLOSING_START(track_001)*; 3.15 BRAKE_START; 3.90 MOVING_END; 3.90 STOP_START; 5.40 EGO_PATH_ENTRY(track_001); 5.55 CLOSING_END(track_001); 5.90 EGO_PATH_EXIT(track_001); 7.15 BRAKE_END; 7.55 STOP_END; 7.55 MOVING_START; 8.30 TRACK_LOST(track_001); 8.75 BRAKE_START; 9.00 BRAKE_END
```

**S05/run_0_crash** (global graph)

```
-3.70 MOVING_START(A); MOVING_START(B)
-2.50 TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A)
-2.05 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.35 TRACK_LOST(B,A)
-0.25 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018)
+0.05 BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_006); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012)
+0.10 EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_RIGHT(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009)
+0.15 EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_LEFT(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008)
+0.20 EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015)
+0.25 EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006)
+0.30 CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_LOST(B,B:track_011)
+0.35 CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_012); EGO_PATH_ENTRY(B,B:track_009); TRACK_LOST(A,B); TRACK_LOST(B,B:track_003)
+0.40 CLOSING_END(B,B:track_009); CLOSING_END(B,B:track_018); EGO_PATH_EXIT(B,B:track_009); EGO_PATH_ENTRY(B,B:track_010)
+0.45 CLOSING_END(B,B:track_008); EGO_PATH_EXIT(B,B:track_010); EGO_PATH_ENTRY(B,B:track_008); TRACK_LOST(B,B:track_005)
+0.50 CRITICAL_TTC_END(B,B:track_015)
+0.55 CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_015); EGO_PATH_EXIT(B,B:track_008); TURN_LEFT_END(B); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_018)
+0.60 CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_016); CLOSING_END(B,B:track_017); MOVING_END(B); STOP_START(B)
+0.85 MOVING_END(A); STOP_START(A)
+1.25 EGO_PATH_ENTRY(B,B:track_008)
+1.40 EGO_PATH_EXIT(B,B:track_013)
+3.75 EGO_PATH_ENTRY(B,B:track_013)
+10.70 TRACK_LOST(B,B:track_004)
```

**S06/run_0_a_front_pushed** (global graph)

```
-5.90 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,C)
-5.85 TRACK_APPEARED_FRONT(A,B)
-5.45 CLOSING_START(A,B)
-4.80 CLOSING_START(B,C)
-4.30 CLOSING_END(A,B)
-3.80 CLOSING_END(B,C)
-3.50 SPEED_LIMIT_EXCEEDED_START(C)
-2.95 BRAKE_START(C)
-2.85 SPEED_LIMIT_EXCEEDED_END(C)
-2.70 CLOSING_START(B,C)
-2.20 BRAKE_START(B)
-2.15 CRITICAL_TTC_START(B,C)
-1.90 CLOSING_START(A,B)
-1.85 MOVING_END(C); STOP_START(C)
-1.20 CRITICAL_TTC_START(A,B)
-1.00 CRITICAL_TTC_END(B,C); CLOSING_END(B,C); MOVING_END(B); STOP_START(B)
-0.35 BRAKE_START(A)
-0.20 BRAKE_END(B)
+0.00 COLLISION(A,B); STOP_END(B); MOVING_START(B); CRITICAL_TTC_START(B,C)
+0.25 COLLISION(B,C)
+0.30 TRACK_LOST(B,C)
+0.35 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); MOVING_END(A); STOP_START(A)
+0.40 MOVING_END(B); STOP_START(B)
```

**S06/run_0_b_rear_first** (global graph)

```
-6.00 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,C)
-5.95 TRACK_APPEARED_FRONT(A,A:track_001)
-5.55 CLOSING_START(A,A:track_001)
-4.90 CLOSING_START(B,C)
-4.40 CLOSING_END(A,A:track_001)
-3.90 CLOSING_END(B,C)
-3.60 SPEED_LIMIT_EXCEEDED_START(C)
-3.05 BRAKE_START(C)
-2.95 SPEED_LIMIT_EXCEEDED_END(C)
-2.80 CLOSING_START(B,C)
-2.25 CRITICAL_TTC_START(B,C)
-1.95 MOVING_END(C); STOP_START(C)
-1.45 TRACK_LOST(A,A:track_001)
-1.40 COLLISION(B,C)
-1.35 CRITICAL_TTC_END(B,C); CLOSING_END(B,C); BRAKE_START(B)
-1.25 MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A)
+0.20 MOVING_END(A); STOP_START(A)
```

**S07/run_0_full_view** (global graph, unaligned nodes: 9)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001)
-5.65 TRACK_APPEARED_FRONT(A,B)
-5.25 CLOSING_START(A,B)
-4.60 CLOSING_START(B,B:track_001)
-4.10 CLOSING_END(A,B)
-3.60 CLOSING_END(B,B:track_001)
-2.45 CLOSING_START(B,B:track_001)
-2.05 BRAKE_START(B)
-1.80 CLOSING_START(A,B)
-1.75 CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
```

**S07/run_0_occluded** (global graph, unaligned nodes: 9)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001)
-5.65 TRACK_APPEARED_FRONT(A,B)
-5.25 CLOSING_START(A,B)
-4.60 CLOSING_START(B,B:track_001)
-4.10 CLOSING_END(A,B)
-3.60 CLOSING_END(B,B:track_001)
-2.45 CLOSING_START(B,B:track_001)
-2.05 BRAKE_START(B)
-1.80 CLOSING_START(A,B)
-1.75 CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
```

**S08/run_0_crash** (global graph, unaligned nodes: 15)

```
-4.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
-2.20 TRACK_APPEARED_RIGHT(A,B); TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(A,B); CLOSING_START(B,B:track_001)
-2.10 CRITICAL_TTC_START(A,A:track_001)
-2.05 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.90 CRITICAL_TTC_START(B,A)
-1.85 CRITICAL_TTC_START(B,B:track_001)
-1.80 CRITICAL_TTC_START(A,B)
-1.50 CRITICAL_TTC_END(A,A:track_001)
-0.70 CRITICAL_TTC_START(A,A:track_001)
-0.15 TRACK_LOST(A,B)
-0.10 CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.10 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.30 MOVING_END(B); STOP_START(B)
+0.35 CLOSING_END(B,B:track_001)
+0.45 EGO_PATH_EXIT(B,A)
+0.50 CRITICAL_TTC_END(A,A:track_001)
+0.65 CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)
```

**S09/run_0_merge_conflict** (global graph)

```
-1.80 MOVING_START(A); MOVING_START(B); TURN_LEFT_START(A); TURN_RIGHT_START(B); TRACK_APPEARED_LEFT(B,B:track_001); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,B:track_001); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001)
-1.60 TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_009); TRACK_APPEARED_LEFT(A,A:track_010); TRACK_APPEARED_LEFT(A,A:track_012); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_RIGHT(A,A:track_011); TRACK_APPEARED_RIGHT(A,A:track_013); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_009); CLOSING_START(A,A:track_010); CLOSING_START(A,A:track_012); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
-1.55 TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_RIGHT(A,A:track_014); CLOSING_START(B,B:track_009); TRACK_LOST(B,B:track_001)
-1.50 TRACK_APPEARED_LEFT(B,B:track_014); CLOSING_START(B,B:track_014)
-1.40 TRACK_LOST(A,A:track_007); TRACK_LOST(A,A:track_011); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007)
-1.35 TRACK_LOST(A,A:track_013); TRACK_LOST(B,B:track_008)
-1.30 TRACK_LOST(B,B:track_011)
-1.25 TRACK_LOST(B,B:track_012)
-1.20 TRACK_LOST(A,A:track_014); TRACK_LOST(B,B:track_013)
-1.15 TRACK_LOST(B,B:track_010)
-1.00 CLOSING_END(B,B:track_009)
-0.90 TRACK_LOST(B,B:track_009)
-0.60 TURN_RIGHT_END(B)
-0.35 TRACK_LOST(A,A:track_002)
-0.30 TRACK_LOST(B,B:track_006)
-0.25 TRACK_LOST(A,A:track_009)
-0.20 EGO_PATH_ENTRY(A,B)
-0.15 CUT_IN_FROM_RIGHT_START(A,B); TRACK_LOST(A,A:track_005)
-0.05 CRITICAL_TTC_END(A,B)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B); TRACK_LOST(A,A:track_012); TRACK_LOST(B,B:track_003)
+0.10 CLOSING_END(A,B); TRACK_LOST(B,B:track_005)
+0.15 CUT_IN_FROM_RIGHT_END(A,B); TRACK_LOST(B,B:track_004)
+0.35 CLOSING_END(B,B:track_014)
+0.65 CLOSING_END(A,A:track_010); TURN_LEFT_END(A)
+0.70 CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_008); TURN_LEFT_END(B); MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
```

**S10/run_0_rolls_through** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B)
-3.45 STOP_SIGN_DETECTED_START(A,A:sign-0)
-3.30 BRAKE_START(A)
-3.10 STOP_SIGN_DETECTED_END(A,A:sign-0)
-2.80 TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
-2.65 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-2.55 TURN_LEFT_START(A)
-1.70 CRITICAL_TTC_START(B,A)
-1.45 BRAKE_END(A)
-1.40 CRITICAL_TTC_START(A,A:track_001)
-0.30 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B); CLOSING_END(A,A:track_001); TRACK_LOST(A,A:track_001)
+0.05 TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B)
+0.10 MOVING_END(B); STOP_START(B)
+0.15 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
```

**S10/run_0_stops_safely** (global graph, unaligned nodes: 20)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.85 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.40 TRACK_APPEARED_LEFT(track_001); 2.40 CLOSING_START(track_001)*; 2.55 BRAKE_START; 3.35 MOVING_END; 3.35 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 7.90 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.60 TRACK_APPEARED_RIGHT(track_001); 2.60 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.60 CRITICAL_TTC_END(track_001); 5.85 TRACK_LOST(track_001); 7.70 STOP_SIGN_DETECTED_START(sign-1); 7.80 STOP_SIGN_DETECTED_END(sign-1)
```

**S10/run_0_stops_then_proceeds** (global graph, unaligned nodes: 73)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.85 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.40 TRACK_APPEARED_LEFT(track_001); 2.40 CLOSING_START(track_001)*; 2.55 BRAKE_START; 3.35 MOVING_END; 3.35 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 6.75 BRAKE_END; 7.10 STOP_END; 7.10 MOVING_START; 7.50 TRACK_LOST(track_001); 7.65 TURN_LEFT_START; 8.20 TRACK_APPEARED_LEFT(track_002); 8.20 TRACK_APPEARED_LEFT(track_003); 8.20 TRACK_APPEARED_LEFT(track_005); 8.20 TRACK_APPEARED_LEFT(track_006); 8.20 TRACK_APPEARED_LEFT(track_007); 8.20 TRACK_APPEARED_LEFT(track_008); 8.20 TRACK_APPEARED_LEFT(track_012); 8.20 TRACK_APPEARED_LEFT(track_013); 8.20 TRACK_APPEARED_RIGHT(track_004); 8.20 CLOSING_START(track_002)*; 8.20 CLOSING_START(track_003)*; 8.20 CLOSING_START(track_005)*; 8.20 CLOSING_START(track_006)*; 8.20 CLOSING_START(track_007)*; 8.20 CLOSING_START(track_008)*; 8.20 CLOSING_START(track_012)*; 8.20 CLOSING_START(track_013)*; 8.25 TRACK_APPEARED_RIGHT(track_009); 8.25 TRACK_APPEARED_RIGHT(track_010); 8.25 CLOSING_START(track_010)*; 8.30 TRACK_APPEARED_RIGHT(track_011); 8.30 CLOSING_START(track_011)*; 8.45 TRACK_APPEARED_LEFT(track_014); 8.45 CLOSING_START(track_014)*; 8.50 TRACK_APPEARED_RIGHT(track_015); 8.50 CLOSING_START(track_015)*; 8.50 CRITICAL_TTC_START(track_006); 8.55 CLOSING_END(track_010); 8.55 TRACK_LOST(track_010); 8.60 TRACK_LOST(track_004); 8.60 TRACK_LOST(track_008); 8.65 TRACK_LOST(track_009); 8.70 CLOSING_END(track_011); 9.10 TRACK_LOST(track_006); 9.15 TRACK_LOST(track_015); 9.30 CLOSING_START(track_011); 10.20 TRACK_LOST(track_014); 10.30 TURN_LEFT_END; 11.00 CUT_IN_FROM_LEFT_START(track_002); 11.20 TRACK_LOST(track_002); 11.65 CLOSING_END(track_011); 11.75 CRITICAL_TTC_START(track_003); 11.75 TRACK_LOST(track_007); 11.95 CLOSING_START(track_011); 12.00 TRACK_LOST(track_012); 12.15 CRITICAL_TTC_START(track_011); 12.20 CRITICAL_TTC_END(track_003); 12.20 CUT_IN_FROM_LEFT_START(track_003); 12.45 CUT_IN_FROM_RIGHT_START(track_011); 12.50 TRACK_LOST(track_003); 13.15 TRACK_LOST(track_013)
B: 0.00 MOVING_START*; 2.60 TRACK_APPEARED_RIGHT(track_001); 2.60 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.60 CRITICAL_TTC_END(track_001); 5.85 TRACK_LOST(track_001)
```

**S11/run_0_rolls_through** (global graph)

```
-5.50 MOVING_START(A); MOVING_START(B)
-3.55 BRAKE_START(B)
-3.40 STOP_SIGN_DETECTED_START(B,B:sign-1)
-3.00 STOP_SIGN_DETECTED_END(B,B:sign-1)
-2.90 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-2.85 BRAKE_END(B)
-2.75 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-1.70 TURN_LEFT_START(B); CRITICAL_TTC_START(A,B)
-1.40 CRITICAL_TTC_START(B,A)
-0.15 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); TURN_LEFT_END(B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.20 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
+0.55 MOVING_END(A); STOP_START(A)
```

**S11/run_0_stops_safely** (global graph, unaligned nodes: 16)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.70 TRACK_APPEARED_RIGHT(track_001); 2.70 CLOSING_START(track_001)*; 5.75 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.00 STOP_SIGN_DETECTED_START(sign-1); 2.40 STOP_SIGN_DETECTED_END(sign-1); 2.50 TRACK_APPEARED_LEFT(track_001); 2.50 CLOSING_START(track_001)*; 2.55 BRAKE_START; 3.25 MOVING_END; 3.25 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001); 8.75 TRACK_LOST(track_001)
```

**S11/run_0_stops_then_proceeds** (global graph, unaligned nodes: 61)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.70 TRACK_APPEARED_RIGHT(track_001); 2.70 CLOSING_START(track_001)*; 5.75 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.05 STOP_SIGN_DETECTED_START(sign-1); 2.40 STOP_SIGN_DETECTED_END(sign-1); 2.50 TRACK_APPEARED_LEFT(track_001); 2.50 CLOSING_START(track_001)*; 2.55 BRAKE_START; 3.25 MOVING_END; 3.25 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001); 6.75 BRAKE_END; 7.20 STOP_END; 7.20 MOVING_START; 7.95 TURN_LEFT_START; 7.95 TRACK_LOST(track_001); 8.40 TRACK_APPEARED_LEFT(track_003); 8.40 TRACK_APPEARED_LEFT(track_004); 8.40 TRACK_APPEARED_LEFT(track_005); 8.40 TRACK_APPEARED_LEFT(track_006); 8.40 TRACK_APPEARED_LEFT(track_007); 8.40 TRACK_APPEARED_LEFT(track_008); 8.40 TRACK_APPEARED_RIGHT(track_002); 8.40 CLOSING_START(track_003)*; 8.40 CLOSING_START(track_004)*; 8.40 CLOSING_START(track_005)*; 8.40 CLOSING_START(track_006)*; 8.40 CLOSING_START(track_007)*; 8.40 CLOSING_START(track_008)*; 8.45 TRACK_APPEARED_LEFT(track_010); 8.45 TRACK_APPEARED_RIGHT(track_009); 8.45 TRACK_APPEARED_RIGHT(track_011); 8.45 CLOSING_START(track_009)*; 8.45 CLOSING_START(track_010)*; 8.45 CLOSING_START(track_011)*; 8.60 TRACK_APPEARED_RIGHT(track_012); 8.60 TRACK_APPEARED_RIGHT(track_013); 8.60 CLOSING_START(track_012)*; 8.60 CLOSING_START(track_013)*; 8.65 TRACK_LOST(track_005); 8.80 TRACK_LOST(track_002); 8.80 TRACK_LOST(track_011); 8.90 CLOSING_END(track_009); 8.90 CRITICAL_TTC_START(track_004); 8.95 TRACK_LOST(track_013); 9.00 TRACK_LOST(track_009); 9.50 TRACK_LOST(track_004); 9.70 TRACK_LOST(track_010); 10.70 TURN_LEFT_END; 10.70 TRACK_LOST(track_003); 12.05 CLOSING_END(track_012); 12.20 TRACK_LOST(track_008); 12.30 CLOSING_START(track_012); 12.55 CUT_IN_FROM_LEFT_START(track_007); 12.75 CUT_IN_FROM_RIGHT_START(track_012); 12.90 TRACK_LOST(track_007); 13.05 TRACK_LOST(track_012)
```

**S12/run_0_a_arrives_first** (global graph, unaligned nodes: 82)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.65 STOP_SIGN_DETECTED_START(sign-0); 2.25 STOP_SIGN_DETECTED_END(sign-0); 2.65 BRAKE_START; 2.95 TRACK_APPEARED_LEFT(track_001); 2.95 CLOSING_START(track_001)*; 3.40 MOVING_END; 3.40 STOP_START; 4.70 CLOSING_END(track_001); 6.45 BRAKE_END; 6.80 STOP_END; 6.80 MOVING_START; 7.15 CLOSING_START(track_001); 7.80 TURN_LEFT_START; 8.25 TRACK_APPEARED_LEFT(track_002); 8.25 TRACK_APPEARED_LEFT(track_003); 8.25 TRACK_APPEARED_LEFT(track_005); 8.25 TRACK_APPEARED_LEFT(track_008); 8.25 CLOSING_START(track_002)*; 8.25 CLOSING_START(track_003)*; 8.25 CLOSING_START(track_005)*; 8.25 CLOSING_START(track_008)*; 8.30 TRACK_APPEARED_LEFT(track_004); 8.30 CLOSING_START(track_004)*; 8.80 TRACK_APPEARED_LEFT(track_006); 8.80 TRACK_APPEARED_RIGHT(track_007); 8.80 CLOSING_START(track_006)*; 8.85 TRACK_APPEARED_LEFT(track_010); 8.85 TRACK_APPEARED_LEFT(track_011); 8.85 TRACK_APPEARED_RIGHT(track_009); 8.85 CLOSING_START(track_010)*; 8.85 CLOSING_START(track_011)*; 8.90 TRACK_APPEARED_LEFT(track_012); 8.90 TRACK_APPEARED_LEFT(track_017); 8.90 CLOSING_START(track_012)*; 8.90 CLOSING_START(track_017)*; 9.00 TRACK_APPEARED_LEFT(track_014); 9.00 TRACK_APPEARED_RIGHT(track_013); 9.00 CLOSING_START(track_014)*; 9.00 TRACK_LOST(track_007); 9.05 TRACK_APPEARED_LEFT(track_015); 9.05 CLOSING_START(track_015)*; 9.10 TRACK_APPEARED_RIGHT(track_016); 9.10 CLOSING_START(track_016)*; 9.20 TRACK_LOST(track_009); 9.25 TRACK_APPEARED_RIGHT(track_018); 9.25 CLOSING_START(track_018)*; 9.40 CLOSING_END(track_016); 9.60 CLOSING_START(track_016); 9.75 CRITICAL_TTC_START(track_001); 9.80 CLOSING_START(track_013); 10.10 TRACK_LOST(track_018); 10.40 TRACK_LOST(track_016); 10.45 TRACK_LOST(track_015); 10.60 EGO_PATH_ENTRY(track_014); 10.65 CRITICAL_TTC_END(track_001); 10.70 TRACK_LOST(track_010); 11.00 TRACK_LOST(track_001); 11.05 TURN_LEFT_END; 11.20 EGO_PATH_EXIT(track_014); 11.90 EGO_PATH_ENTRY(track_008); 12.30 TRACK_LOST(track_006); 13.50 TRACK_LOST(track_013); 14.30 TRACK_LOST(track_017); 14.35 TRACK_LOST(track_012); 14.50 TRACK_LOST(track_004)
B: 0.00 MOVING_START*; 2.10 STOP_SIGN_DETECTED_START(sign-0); 4.00 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.70 MOVING_END; 4.70 STOP_START; 6.90 TRACK_APPEARED_RIGHT(track_001); 6.90 CLOSING_START(track_001)*; 8.50 EGO_PATH_ENTRY(track_001); 9.05 EGO_PATH_EXIT(track_001); 10.45 BRAKE_END; 10.55 CRITICAL_TTC_START(track_001); 10.85 CRITICAL_TTC_END(track_001); 10.85 STOP_END; 10.85 MOVING_START; 11.15 TRACK_LOST(track_001)
```

**S12/run_0_b_arrives_first** (global graph, unaligned nodes: 79)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.95 STOP_SIGN_DETECTED_START(sign-0); 3.10 TRACK_APPEARED_LEFT(track_001); 3.10 CLOSING_START(track_001)*; 3.60 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.70 CLOSING_END(track_001); 4.75 MOVING_END; 4.75 STOP_START; 6.95 CLOSING_START(track_001); 9.75 EGO_PATH_ENTRY(track_001); 9.90 CLOSING_END(track_001); 10.20 EGO_PATH_EXIT(track_001); 10.45 BRAKE_END; 10.80 STOP_END; 10.80 MOVING_START; 12.10 TURN_LEFT_START; 12.10 TRACK_LOST(track_001); 12.55 TRACK_APPEARED_LEFT(track_006); 12.55 TRACK_APPEARED_LEFT(track_007); 12.55 CLOSING_START(track_006)*; 12.55 CLOSING_START(track_007)*; 12.60 TRACK_APPEARED_LEFT(track_002); 12.60 TRACK_APPEARED_LEFT(track_003); 12.60 TRACK_APPEARED_LEFT(track_004); 12.60 CLOSING_START(track_002)*; 12.60 CLOSING_START(track_003)*; 12.60 CLOSING_START(track_004)*; 12.65 TRACK_APPEARED_LEFT(track_005); 12.65 CLOSING_START(track_005)*; 13.05 TRACK_APPEARED_LEFT(track_009); 13.05 TRACK_APPEARED_LEFT(track_013); 13.05 TRACK_APPEARED_RIGHT(track_008); 13.05 CLOSING_START(track_009)*; 13.05 CLOSING_START(track_013)*; 13.10 TRACK_APPEARED_LEFT(track_011); 13.10 TRACK_APPEARED_LEFT(track_015); 13.10 TRACK_APPEARED_RIGHT(track_010); 13.10 CLOSING_START(track_011)*; 13.10 CLOSING_START(track_015)*; 13.15 TRACK_APPEARED_LEFT(track_012); 13.15 CLOSING_START(track_012)*; 13.20 TRACK_APPEARED_LEFT(track_014); 13.20 CLOSING_START(track_014)*; 13.25 TRACK_APPEARED_LEFT(track_017); 13.25 TRACK_APPEARED_RIGHT(track_016); 13.25 CLOSING_START(track_017)*; 13.30 TRACK_LOST(track_008); 13.35 TRACK_APPEARED_RIGHT(track_018); 13.35 CLOSING_START(track_018)*; 13.40 TRACK_APPEARED_LEFT(track_019); 13.40 CLOSING_START(track_019)*; 13.50 TRACK_LOST(track_010); 14.00 CLOSING_START(track_016); 14.45 TRACK_LOST(track_019); 14.60 TRACK_LOST(track_018); 14.90 EGO_PATH_ENTRY(track_017); 15.15 TRACK_LOST(track_014); 15.30 TURN_LEFT_END; 15.35 EGO_PATH_ENTRY(track_006); 15.55 EGO_PATH_EXIT(track_017); 15.90 CUT_IN_FROM_RIGHT_START(track_016); 16.05 TRACK_LOST(track_012); 16.35 TRACK_LOST(track_009); 16.40 TRACK_LOST(track_004)
B: 0.00 MOVING_START*; 1.80 STOP_SIGN_DETECTED_START(sign-0); 2.60 STOP_SIGN_DETECTED_END(sign-0); 2.65 BRAKE_START; 3.05 TRACK_APPEARED_RIGHT(track_001); 3.05 CLOSING_START(track_001)*; 3.40 MOVING_END; 3.40 STOP_START; 4.70 CLOSING_END(track_001); 6.45 BRAKE_END; 6.85 STOP_END; 6.85 MOVING_START; 7.00 CLOSING_START(track_001); 9.45 TRACK_LOST(track_001)
```

**S12/run_0_b_fails_to_stop** (global graph)

```
-9.70 MOVING_START(A); MOVING_START(B)
-9.00 STOP_SIGN_DETECTED_START(A,A:sign-0)
-7.75 BRAKE_START(B)
-7.45 STOP_SIGN_DETECTED_END(A,A:sign-0)
-7.05 BRAKE_END(B); BRAKE_START(A)
-6.55 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-6.30 MOVING_END(A); STOP_START(A)
-6.20 STOP_SIGN_DETECTED_START(B,B:sign-1)
-4.40 STOP_SIGN_DETECTED_END(B,B:sign-1)
-1.95 BRAKE_END(A)
-1.60 STOP_END(A); MOVING_START(A)
-1.55 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-1.05 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.60 TURN_LEFT_START(A)
-0.10 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(B,B:track_002)
+0.05 BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004)
+0.10 TURN_LEFT_END(A)
+0.15 CRITICAL_TTC_END(B,A)
+0.25 CLOSING_END(B,A)
+0.35 MOVING_END(B); STOP_START(B)
+0.40 CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_004)
+0.50 MOVING_END(A); STOP_START(A); TRACK_LOST(B,B:track_004)
+0.55 CLOSING_END(B,B:track_003)
```

**S12/run_0_near_simultaneous** (global graph)

```
-9.50 MOVING_START(A); MOVING_START(B)
-8.80 STOP_SIGN_DETECTED_START(A,A:sign-0)
-7.70 STOP_SIGN_DETECTED_START(B,B:sign-0)
-7.20 STOP_SIGN_DETECTED_END(A,A:sign-0)
-7.05 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-6.95 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-6.90 STOP_SIGN_DETECTED_END(B,B:sign-0)
-6.85 BRAKE_START(A)
-6.75 BRAKE_START(B)
-6.10 MOVING_END(A); STOP_START(A)
-6.00 CLOSING_END(A,B); CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
-2.55 BRAKE_END(A); BRAKE_END(B)
-2.20 STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
-2.15 STOP_END(B); MOVING_START(B)
-1.20 TURN_LEFT_START(A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.70 TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_010); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_010)
-0.65 TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_013); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_013)
-0.60 TRACK_APPEARED_LEFT(A,A:track_009); CLOSING_START(A,A:track_009)
-0.55 EGO_PATH_ENTRY(B,A)
-0.35 TRACK_LOST(A,B)
-0.20 TRACK_APPEARED_LEFT(A,A:track_011); CLOSING_START(A,A:track_011)
-0.15 TRACK_APPEARED_RIGHT(A,A:track_012)
-0.10 TRACK_APPEARED_LEFT(A,A:track_014); CLOSING_START(A,A:track_014)
-0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); TRACK_APPEARED_LEFT(A,A:track_016); CLOSING_START(A,A:track_016)
+0.00 COLLISION(A,B); TRACK_APPEARED_FRONT(A,A:track_017); TRACK_APPEARED_RIGHT(A,A:track_015); CLOSING_START(A,A:track_017)
+0.05 EGO_PATH_EXIT(A,A:track_017); EGO_PATH_EXIT(B,A); BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(A,A:track_018); TRACK_APPEARED_RIGHT(A,A:track_019); CLOSING_START(A,A:track_018); CLOSING_START(A,A:track_019); TRACK_LOST(A,A:track_012)
+0.20 CLOSING_START(A,A:track_015)
+0.25 TRACK_LOST(B,A)
+0.45 MOVING_END(B); STOP_START(B)
+0.50 CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_005); CLOSING_END(A,A:track_008); CLOSING_END(A,A:track_015); CLOSING_END(A,A:track_017); CLOSING_END(A,A:track_018); CLOSING_END(A,A:track_019); TURN_LEFT_END(A); MOVING_END(A); STOP_START(A); TRACK_LOST(A,A:track_019)
+0.55 CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_009); CLOSING_END(A,A:track_010); CLOSING_END(A,A:track_011); CLOSING_END(A,A:track_013); CLOSING_END(A,A:track_014); CLOSING_END(A,A:track_016)
+0.60 CLOSING_END(A,A:track_006)
+1.50 STOP_SIGN_DETECTED_START(A,A:sign-1)
+3.10 TRACK_LOST(A,A:track_006)
+4.85 TRACK_LOST(A,A:track_018)
+5.35 TRACK_LOST(A,A:track_005)
+5.40 TRACK_LOST(A,A:track_008)
```

**S13/run_0_accelerates_into_gap** (global graph)

```
-5.65 MOVING_START(A); MOVING_START(B)
-5.50 TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
-4.90 TRACK_LOST(A,A:track_001)
-4.85 BRAKE_START(B)
-2.90 SPEED_LIMIT_EXCEEDED_START(A)
-2.30 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-1.80 CUT_IN_FROM_LEFT_START(A,B)
-1.65 CRITICAL_TTC_START(A,B)
-0.20 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A)
+0.05 BRAKE_START(A)
+0.10 TURN_RIGHT_START(B)
+0.20 CRITICAL_TTC_END(A,B)
+0.25 TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_022); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_022)
+0.30 TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
+0.40 TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008); CLOSING_START(B,B:track_009)
+0.45 TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_RIGHT(B,B:track_020); TRACK_APPEARED_RIGHT(B,B:track_029); CLOSING_START(B,B:track_010); CLOSING_START(B,B:track_011); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_020); CLOSING_START(B,B:track_029)
+0.50 TRACK_APPEARED_LEFT(B,B:track_014); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_021); TRACK_APPEARED_RIGHT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_013); CLOSING_START(B,B:track_012); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_021); CRITICAL_TTC_START(B,B:track_012); CRITICAL_TTC_START(B,B:track_013)
+0.55 TRACK_APPEARED_LEFT(B,B:track_017); TRACK_APPEARED_LEFT(B,B:track_018); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_APPEARED_LEFT(B,B:track_026); CLOSING_START(B,B:track_017); CLOSING_START(B,B:track_018); CLOSING_START(B,B:track_019); CLOSING_START(B,B:track_026)
+0.60 TRACK_LOST(B,B:track_004)
+0.65 TRACK_APPEARED_LEFT(B,B:track_023); TRACK_APPEARED_LEFT(B,B:track_024); TRACK_APPEARED_LEFT(B,B:track_025); TRACK_APPEARED_LEFT(B,B:track_027); TRACK_APPEARED_LEFT(B,B:track_030); TRACK_APPEARED_LEFT(B,B:track_031); CLOSING_START(B,B:track_023); CLOSING_START(B,B:track_024); CLOSING_START(B,B:track_025); CLOSING_START(B,B:track_027); CLOSING_START(B,B:track_030); CLOSING_START(B,B:track_031); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_008); TRACK_LOST(B,B:track_009)
+0.70 TRACK_APPEARED_LEFT(B,B:track_028); CLOSING_START(B,B:track_028)
+0.75 TRACK_APPEARED_LEFT(B,B:track_032); TRACK_APPEARED_LEFT(B,B:track_033); TRACK_APPEARED_LEFT(B,B:track_034); TRACK_APPEARED_LEFT(B,B:track_036); TRACK_APPEARED_LEFT(B,B:track_037); TRACK_APPEARED_LEFT(B,B:track_040); TRACK_APPEARED_RIGHT(B,B:track_035); CLOSING_START(B,B:track_032); CLOSING_START(B,B:track_033); CLOSING_START(B,B:track_034); CLOSING_START(B,B:track_035); CLOSING_START(B,B:track_036); CLOSING_START(B,B:track_037); CLOSING_START(B,B:track_040); CRITICAL_TTC_START(A,B); TRACK_LOST(B,B:track_010); TRACK_LOST(B,B:track_011)
+0.80 TRACK_APPEARED_LEFT(B,B:track_041); CLOSING_START(B,B:track_041); TRACK_LOST(B,B:track_014); TRACK_LOST(B,B:track_015); TRACK_LOST(B,B:track_021)
+0.85 TRACK_APPEARED_LEFT(B,B:track_038); TRACK_APPEARED_LEFT(B,B:track_039); TRACK_APPEARED_LEFT(B,B:track_042); CLOSING_START(B,B:track_038); CLOSING_START(B,B:track_039); CLOSING_START(B,B:track_042); TRACK_LOST(B,B:track_016); TRACK_LOST(B,B:track_018)
+0.90 TRACK_LOST(B,B:track_019); TRACK_LOST(B,B:track_026)
+0.95 TRACK_LOST(B,B:track_017); TRACK_LOST(B,B:track_023); TRACK_LOST(B,B:track_027)
+1.00 CRITICAL_TTC_END(B,B:track_013); EGO_PATH_ENTRY(B,B:track_012); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_033)
+1.05 CLOSING_END(B,B:track_024); CLOSING_END(B,B:track_031); CLOSING_END(B,B:track_034); TRACK_LOST(B,B:track_024); TRACK_LOST(B,B:track_031); TRACK_LOST(B,B:track_034)
+1.10 CRITICAL_TTC_END(B,B:track_012); CLOSING_END(B,B:track_030)
+1.15 CUT_IN_FROM_LEFT_END(A,B); CLOSING_END(B,B:track_028); CLOSING_END(B,B:track_032); CLOSING_END(B,B:track_036); CLOSING_END(B,B:track_040); CLOSING_END(B,B:track_041); EGO_PATH_ENTRY(B,B:track_005); TRACK_LOST(B,B:track_028)
+1.20 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_025); CLOSING_END(B,B:track_037); CLOSING_END(B,B:track_038); CLOSING_END(B,B:track_039); CLOSING_END(B,B:track_042); TRACK_LOST(B,B:track_041)
+1.25 CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_006); CLOSING_END(B,B:track_012); CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_020); CLOSING_END(B,B:track_029); CLOSING_END(B,B:track_035); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
+1.30 MOVING_END(A); STOP_START(A)
+1.35 CLOSING_END(B,B:track_022)
+1.70 TRACK_LOST(B,B:track_022)
+2.00 TRACK_LOST(B,B:track_025)
+2.05 EGO_PATH_ENTRY(B,B:track_006)
+2.70 EGO_PATH_EXIT(B,B:track_013)
+3.00 TRACK_LOST(B,B:track_029)
+4.05 TRACK_LOST(B,B:track_037)
+4.25 TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_035)
```

**S13/run_0_cut_in** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-4.45 BRAKE_START(B)
-2.40 BRAKE_START(A)
-1.70 CUT_IN_FROM_LEFT_START(A,B)
-1.30 CRITICAL_TTC_START(A,B)
-0.35 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B)
+0.05 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.20 TURN_RIGHT_START(B)
+0.70 TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
+1.15 CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A)
+1.20 MOVING_END(B); STOP_START(B)
+1.40 CUT_IN_FROM_LEFT_END(A,B)
```

**S13/run_0_safe_lane_change** (global graph, unaligned nodes: 10)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_LEFT(track_001); 0.00 CLOSING_START(track_001)*; 1.50 CLOSING_END(track_001); 2.45 CLOSING_START(track_001); 2.85 BRAKE_START; 4.00 CUT_IN_FROM_LEFT_START(track_001); 5.30 EGO_PATH_ENTRY(track_001); 8.00 CUT_IN_FROM_LEFT_END(track_001)
B: 0.00 MOVING_START*
```

**S15/run_0_b_stops** (global graph, unaligned nodes: 43)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.05 TRACK_APPEARED_FRONT(track_001); 0.05 CLOSING_START(track_001)*; 2.00 TRACK_APPEARED_RIGHT(track_002); 2.00 CLOSING_START(track_002)*; 2.00 CRITICAL_TTC_START(track_002)*; 2.55 CRITICAL_TTC_START(track_001); 4.05 TRACK_LOST(track_002); 4.50 CLOSING_END(track_001); 4.55 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 1.45 TRACK_APPEARED_RIGHT(track_001); 1.45 CLOSING_START(track_001)*; 1.80 STOP_SIGN_DETECTED_START(sign-0); 1.95 TRACK_APPEARED_LEFT(track_002); 1.95 CLOSING_START(track_002)*; 2.10 STOP_SIGN_DETECTED_END(sign-0); 2.10 CRITICAL_TTC_START(track_002); 2.25 TURN_LEFT_START; 2.55 BRAKE_START; 3.35 TURN_LEFT_END; 3.40 MOVING_END; 3.40 STOP_START; 3.55 CRITICAL_TTC_END(track_002); 3.90 EGO_PATH_ENTRY(track_002); 4.00 STOP_SIGN_DETECTED_START(sign-1); 4.25 CLOSING_END(track_002); 4.35 EGO_PATH_EXIT(track_002); 5.25 TRACK_LOST(track_002); 5.35 CLOSING_END(track_001); 5.65 EGO_PATH_ENTRY(track_001); 6.40 EGO_PATH_EXIT(track_001); 6.90 STOP_SIGN_DETECTED_END(sign-1); 8.90 STOP_SIGN_DETECTED_START(sign-1)
C: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_LEFT(track_001); 0.00 CLOSING_START(track_001)*; 0.05 TRACK_APPEARED_FRONT(track_002); 0.05 CLOSING_START(track_002)*; 2.90 CRITICAL_TTC_START(track_002); 4.50 CLOSING_END(track_002); 4.55 TRACK_LOST(track_002); 4.75 TRACK_LOST(track_001)
```

**S15/run_0_deflected_into_c** (global graph)

```
-3.80 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_LEFT(C,C:track_001); CLOSING_START(C,C:track_001)
-3.75 TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
-2.35 TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
-2.30 STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.85 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.80 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
-1.70 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.65 CRITICAL_TTC_START(B,A)
-1.55 TURN_LEFT_START(B)
-1.25 CRITICAL_TTC_START(A,C)
-0.90 CRITICAL_TTC_START(C,A)
-0.85 BRAKE_START(B)
-0.75 TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
-0.70 TRACK_APPEARED_LEFT(B,B:track_007); CLOSING_START(B,B:track_007)
-0.65 TRACK_LOST(B,B:track_001)
-0.30 BRAKE_END(B)
-0.10 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006); TRACK_LOST(B,B:track_007)
+0.00 COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
+0.05 BRAKE_START(B); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_008); CRITICAL_TTC_START(B,B:track_008)
+0.20 MOVING_END(B); STOP_START(B)
+0.30 CRITICAL_TTC_END(B,A)
+0.35 TRACK_LOST(B,B:track_008)
+0.50 CLOSING_END(B,A)
+0.65 TRACK_LOST(C,C:track_001)
+0.70 EGO_PATH_ENTRY(A,C)
+0.80 STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
+0.95 COLLISION(A,C)
+1.00 CRITICAL_TTC_END(A,C); CLOSING_END(A,C); EGO_PATH_EXIT(B,A); BRAKE_START(C)
+1.15 TURN_LEFT_END(A); EGO_PATH_ENTRY(C,A)
+1.20 CRITICAL_TTC_END(C,A)
+1.25 CLOSING_END(C,A); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
+1.50 STOP_SIGN_DETECTED_START(A,A:sign-2)
+4.00 STOP_SIGN_DETECTED_END(A,A:sign-2)
+4.90 STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)
+5.80 STOP_SIGN_DETECTED_START(A,A:sign-2)
+6.10 STOP_SIGN_DETECTED_END(A,A:sign-2)
+7.10 STOP_SIGN_DETECTED_START(A,A:sign-2)
```

**S15/run_0_single_impact** (global graph, unaligned nodes: 10)

```
-3.80 MOVING_START(A); MOVING_START(B)
-2.90 TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
-2.00 STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.85 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.80 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
-1.70 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.65 CRITICAL_TTC_START(B,A)
-1.55 TURN_LEFT_START(B)
-0.85 BRAKE_START(B)
-0.75 TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
-0.70 TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_006)
-0.30 BRAKE_END(B)
-0.10 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006)
+0.00 COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001)
+0.05 EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.30 CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,A:track_001)
+0.50 CLOSING_END(B,A); EGO_PATH_EXIT(A,A:track_001)
+0.80 STOP_SIGN_DETECTED_START(A,A:sign-0)
+1.00 EGO_PATH_EXIT(B,A)
+1.30 STOP_SIGN_DETECTED_END(A,A:sign-0)
+1.40 TURN_LEFT_END(A)
+6.80 STOP_SIGN_DETECTED_START(A,A:sign-1)
+7.75 MOVING_END(A); STOP_START(A)
+9.65 CRITICAL_TTC_START(A,A:track_001)
```

**S16/run_0_avoided** (global graph, unaligned nodes: 3)

```
-5.15 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A)
-4.45 CLOSING_START(B,A)
-4.40 CRITICAL_TTC_START(B,A)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-1.20 BRAKE_START(A)
-0.90 CLOSING_START(B,A)
-0.70 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.45 MOVING_END(B); STOP_START(B)
+0.60 MOVING_END(A); STOP_START(A)
```

**S16/run_0_consequential** (global graph)

```
-5.15 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
-4.85 MOVING_END(C); STOP_START(C)
-4.45 CLOSING_START(B,A)
-4.40 CRITICAL_TTC_START(B,A)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-1.20 BRAKE_START(A)
-0.90 CLOSING_START(B,A)
-0.70 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B); TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_RIGHT(A,A:track_002); TRACK_APPEARED_RIGHT(A,A:track_003); TRACK_APPEARED_RIGHT(A,A:track_004); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CRITICAL_TTC_START(A,A:track_001)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
+0.25 TURN_LEFT_START(A)
+0.30 CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003)
+0.35 TRACK_APPEARED_RIGHT(A,A:track_005); TRACK_APPEARED_RIGHT(A,A:track_006)
+0.45 MOVING_END(B); STOP_START(B)
+0.55 CLOSING_END(A,A:track_004); EGO_PATH_ENTRY(A,A:track_001)
+0.75 COLLISION(A,C); STOP_END(C); MOVING_START(C)
+0.80 BRAKE_START(C); TRACK_LOST(A,A:track_005)
+0.85 CRITICAL_TTC_END(A,A:track_001); TURN_LEFT_END(A)
+0.90 CLOSING_END(A,A:track_001); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
```

**S16/run_0_independent** (global graph)

```
-14.10 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A)
-13.60 MOVING_END(C); STOP_START(C)
-13.40 CLOSING_START(B,A)
-13.35 CRITICAL_TTC_START(B,A)
-12.70 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-10.15 BRAKE_START(A)
-9.85 CLOSING_START(B,A)
-9.65 CRITICAL_TTC_START(B,A)
-9.35 BRAKE_START(B)
-8.95 COLLISION(A,B)
-8.90 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-8.50 MOVING_END(B); STOP_START(B)
-8.30 MOVING_END(A); STOP_START(A)
-5.00 YIELD_SIGN_DETECTED_START(C,C:sign-1)
-4.50 YIELD_SIGN_DETECTED_END(C,C:sign-1)
-3.15 BRAKE_END(A)
-2.95 TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_LEFT(A,C)
-2.70 STOP_END(A); MOVING_START(A)
-2.35 CLOSING_START(A,C)
-2.30 CLOSING_START(A,A:track_001)
-2.20 TRACK_LOST(A,A:track_001)
-2.15 STOP_END(C); MOVING_START(C)
-2.00 EGO_PATH_ENTRY(A,C)
-1.45 CRITICAL_TTC_START(A,C)
-0.65 EGO_PATH_EXIT(B,A)
-0.55 TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003)
-0.30 STOP_SIGN_DETECTED_START(C,C:sign-3); STOP_SIGN_DETECTED_END(C,C:sign-3)
-0.10 TRACK_LOST(B,A)
+0.00 COLLISION(A,C); BRAKE_START(C)
+0.20 CLOSING_END(A,C)
+0.25 TRACK_LOST(A,C)
+0.40 TRACK_LOST(B,B:track_003)
+0.55 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
```

## 8. Local semantic world model (2026-10-01)

_Historical: the first world-model version (120 deg radar, 32 runs). HARD_BRAKE, STRONG_THROTTLE, PREDICTED_PATH_CONFLICT and VISIBLE have been removed since, TURN_LEFT/RIGHT, TRACK_APPEARED_FRONT/LEFT/RIGHT and the braking-based CRITICAL_TTC added; the numbers below were not regenerated. Current per-run data: section 3, `traces/campaign_summary.json`, `traces/radar_visibility_audit.json`._

Reconstruction only: the 32 raw recordings were not touched and CARLA was not rerun (no sensor change).
Every run was reconstructed and evaluated again; the evaluation headlines (collisions, alignment, identity
decisions) are identical to before in all 32 runs, and every pre-existing event (type, time, subject) is
unchanged in all 75 local graphs; only reacquired sign windows now carry the first sign's id. The additions
are below.

What is new:

- `perceived_state_before` on every event node: the recorder's own state just before the event, true / false /
  UNKNOWN (ego: MOVING, STOP, BRAKE, HARD_BRAKE, STRONG_THROTTLE, SPEED_LIMIT_EXCEEDED; per local track:
  visible, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PREDICTED_PATH_CONFLICT, CUT_IN_FROM_LEFT/RIGHT; per sign:
  class, visible, known, relevant_to_ego_path). Events at one timestamp share it; trace frames carry the state
  at the frame. TRACK_LOST sets visible false and every state of the track UNKNOWN; no END is invented. The
  global graph keeps each observing recorder's belief under its own local names.
- TRACK_STATE facts gain vx/vy, velocity std, relative longitudinal/lateral speed, relative motion angle,
  `motion_relation`, `t_cpa_s` and `d_cpa_m`.
- PREDICTED_PATH_CONFLICT_START/END (closest point of approach within 4 s and 1.5 m; release beyond 5 s or
  2.5 m, or once past) and CUT_IN_FROM_LEFT/RIGHT_START/END (kinematic lateral merge of a car ahead moving
  within 25 deg of the recorder's heading). Global thresholds only.
- Uncertainty: 142 of 159 tracks are precise enough (position std <= 1 m, velocity std <= 1 m/s) from their
  first sample. 17 short tracks (5-9 samples, mostly post-impact clutter in S05 B and S13 accelerates_into_gap
  B) never are, so their PATH_CONFLICT and CUT_IN states stay UNKNOWN.
- Local sign continuity: a STOP track restarting within 5 s at the same image place while the recorder stood
  still keeps the earlier sign's id.
- Privileged `scripts/audit_radar_visibility.py`, output in `traces/radar_visibility_audit.json`.

### Cut-in (S02, S13)

CUT_IN occurs only in S02 and S13, always from the left (B starts in the lane to A's left). It never occurs
in crossing or merging traffic: S09's merge converges at about -80 deg and fails the heading criterion.

| Run | A's track | PATH_CONFLICT | CUT_IN_FROM_LEFT | EGO_PATH_ENTRY | Collision |
|---|---|---|---|---|---|
| S02 crash | track_001 (B) | 1.65 -> 4.30 | 2.20 -> 4.25 | 3.20 | 4.25 |
| S02 avoided | track_001 | 1.65 -> 3.70 | 2.20 -> 5.25 | 3.15 | - |
| S13 cut_in | track_001 (B) | 3.60 -> 6.35 | 3.90 -> 6.65 | 4.80 | 5.25 |
| S13 accelerates_into_gap | track_002 (B) | 3.35* -> 6.90 | 4.05 -> 6.90 | 5.25 | 5.65 |
| S13 safe_lane_change | track_001 | none (closest approach 2.57 m) | 4.05 -> 7.25 | 5.35 | - |

(* active when the track was first observed.) The cut-in ENDs come from the lateral approach settling. In
S13 cut_in and accelerates_into_gap they follow the collision; in S02 crash the lateral motion stops at the
contact, so the END coincides with COLLISION (it is not caused by it). The safe lane change is a cut-in
without a predicted conflict, which is the intended distinction.

### Predicted path conflicts

Where a recorder tracked its collision partner beforehand, the conflict with that track started 0.55-2.6 s
before the contact in these runs (S01 1.80, S02 2.60, S03 A 1.70 / B 1.40, S05 A 2.20 / B 1.30, S08 A 1.70 / B 1.40, S09 A 1.15,
S10 rolls_through A 0.55 / B 1.25, S11 rolls_through A 2.15 / B 1.10, S12 b_fails_to_stop A 1.40 / B 1.55,
S13 cut_in 1.65, S15 A 1.15 / B 0.70). Oncoming traffic in the adjacent lane gives none: in S08 the predicted
miss distance between A and C stays at 2.3-2.7 m during the pass. It drops below 1.5 m only from 4.1 s, as A
veers toward C's lane just before its collision with B, so C's conflict starts at 4.15 s. In S04 yield, A's
conflict ends at 3.75 s when B yields. Post-impact conflicts (S06 B, S09 A at 2.35 s) come from vehicles still
moving in contact. S09 B's conflict at 0.40 s concerns its track_001, which is not A: the privileged check
keeps it 12-18 m from A, so it is a clutter or ghost track (it already carried CLOSING and CRITICAL_TTC).

### Tracks lost while a state was active (those states are UNKNOWN afterwards)

Partner tracks lost before the collision: S03 A track_001 at 3.35 (CLOSING, CRITICAL_TTC, PATH_CONFLICT;
collision 4.25), S08 A track_002 at 3.35 (same), S05 B track_001 at 2.85 (same; collision 3.70),
S10 rolls_through A at 5.20 (collision 5.25), S11 rolls_through A at 5.45 (5.50), S12 b_fails_to_stop A at
9.65 (9.70), S15 deflected_into_c / single_impact A track_002 at 3.75 (3.80). At the loss the partner was at
the field-of-view edge or outside it in S03, S05, S08, S11 and S15. In S10 rolls_through A the tracker
dropped it although usable returns remained, and in S12 b_fails_to_stop A only static or filtered returns
remained. S09 B lost its ghost track_001 at 1.65 s. Other losses happen after the collision or concern
clutter (table below).

### Radar visibility (privileged audit; S03, S08, S15 in detail)

- S03: B is inside A's 120 deg field of view from t = 0, but for 2.0 s every return along its bearing comes
  from the corner buildings (static occlusion). A's track is born at 2.05 s and confirmed at 2.25 s; B's track
  of A at 2.15 / 2.35 s. A loses B at 3.35 s, 0.9 s before contact: on the collision course B's bearing stays
  at about 56-60 deg, at the edge of the +-60 deg field of view.
- S08 (same junction): A first sees B at 2.05 s and loses it at 3.35 s at the FOV edge. B sees A at 2.15 s and
  C at 2.20 s (static occlusion); C sees B only at 3.00 s. A and C see each other at 0.05 s, confirmed 0.20 s
  later (the confirmation latency).
- S15: static occlusion again (A sees B at 2.00 s; B sees A at 1.95 s and C at 1.45 s). In single_impact B
  never gets a return from C while C is in its field of view. C's first track of B waits 1.15 s for the
  5-sweep confirmation: usable returns on B were intermittent (11 of 24 sweeps, at most 4 in a row). A loses
  B at 3.75 s, outside the field of view, 0.05 s before the contact.
- Elsewhere: static occlusion dominates S04, S05 and S10-S12 (first track 1.2-3.0 s; S12 a_arrives_first
  A->B 9.15 s; S12 b_fails_to_stop A->B 6.75 s); in S10 A->B and S11 B->A the first returns wait for the
  field-of-view edge (RAW_SENSOR edge, 3.5-3.95 s). S09 B never sees A (FOV edge). In S12 b_fails_to_stop, B's
  first track of A waits 5.1 s because A creeps at 0-4.3 m/s and only 6 of 103 sweeps hold moving returns. S16's
  C (about 1 m/s) is barely "moving" for the tracker (FILTER/TRACKER). A's first returns on C in S06 and S07
  fail the tracker's filters (FILTER; in S07 the height filter, below).
- Decision: no sensor change. Static occlusion by buildings is the dominant cause and no FOV or extra radar
  removes it. The FOV edge matters only in the last 0.05-0.9 s before perpendicular impacts and for S09 B. A
  wider or corner radar would close those gaps but changes the experimental sensor setup, so it is reported,
  not made. The profile stays the single 120 deg forward radar; CARLA was not rerun.

### S07 full_view vs occluded

Both variants give the same evidence about C. A gets returns on C in both (4 in full_view, 27 with the denser
narrow-FOV rays), but all are 3.3-4.9 m above the road (C is uphill on the 7 deg slope), so the 2.5 m height
filter rejects them (audit: FILTER in both). C is straight ahead, inside both fields of view, and occluded
by B in both. The narrower FOV therefore removes nothing that the wide one used. S07 was not redesigned.

### STOP signs (S10-S12, S15)

- STOP_SIGN_DETECTED windows are unchanged pure perception (section 5 still holds: no STOP_START lies inside a
  window).
- New: the sign stays KNOWN after it leaves view. Before every stop at a junction, the stopping recorder's
  state holds the STOP sign as known and not visible. This holds for S10/S11 stops_safely and
  stops_then_proceeds, every S12 approach except B in b_fails_to_stop, and S15 b_stops B. In
  the violating runs (S10/S11 rolls_through, S12 b_fails_to_stop B, S15 deflected_into_c / single_impact B),
  the recorder's only STOP_START comes after its collision. No compliance is derived: knowledge is never
  cleared (no admissible local criterion for passing the sign), and the detector's relevance flag is False
  for most roadside signs.
- Fragmentation: the camera tracker split a sign while the recorder stood still in S15 b_stops B (sign-1..4:
  5 camera tracks -> 2 signs, 3 reacquired windows), S15 deflected_into_c A (sign-2..5 -> 1 sign) and S12
  near_simultaneous A (sign-1 / sign-4, after the collision). Continuity now keeps one id per sign there.
  Nothing else merged.

### Per-run audit

CUT-IN L/R and PATH_CONFLICT count START events per recorder. "Tracks lost while" lists the states that were
true at the loss (CLS closing, TTC critical TTC, CONFL path conflict, PATH in the ego path). STOP sign tracks
are given as camera tracker ids / local signs / reacquired windows, and which signs are visible vs known at
the end. Radar tracks counts TRACK_APPEARED. The last column is the privileged audit's first confirmed track
of each other vehicle and the dominant delay stage.

| Run | Rec | CUT-IN L/R | PATH_CONFLICT | Tracks lost while (states then UNKNOWN) | STOP sign tracks: camera / local / reacquired; at end visible vs known | Radar tracks | First detection of each other vehicle (privileged audit) |
|---|---|---|---:|---|---|---:|---|
| S01/run_0_avoided | A | 0/0 | 1 | - | - | 1 | B: conf 0.25, none (prompt) |
| S01/run_0_avoided | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S01/run_0_crash | A | 0/0 | 1 | - | - | 1 | B: conf 0.25, none (prompt) |
| S01/run_0_crash | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S02/run_0_avoided | A | 1/0 | 1 | - | - | 1 | B: conf 0.20, none (prompt) |
| S02/run_0_avoided | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S02/run_0_crash | A | 1/0 | 1 | - | - | 1 | B: conf 0.20, none (prompt) |
| S02/run_0_crash | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S03/run_0_crash | A | 0/0 | 1 | track_001@3.35: CLS+TTC+CONFL | - | 1 | B: conf 2.25, OCCLUSION(static) (+2.05 s) |
| S03/run_0_crash | B | 0/0 | 1 | - | - | 1 | A: conf 2.35, OCCLUSION(static) (+2.15 s) |
| S04/run_0_yield | A | 0/0 | 1 | track_001@4.95: CLS+TTC | 1 / 1 / 0; visible none vs known sign-0 | 2 | B: conf 2.30, OCCLUSION(static) (+2.10 s) |
| S04/run_0_yield | B | 0/0 | 0 | track_001@2.35: CLS (+1 lost idle) | - | 2 | A: conf 2.30, OCCLUSION(static) (+2.00 s) |
| S05/run_0_crash | A | 0/0 | 1 | - (+1 lost idle) | - | 1 | B: conf 1.45, OCCLUSION(static) (+1.25 s) |
| S05/run_0_crash | B | 0/0 | 1 | track_001@2.85: CLS+TTC+CONFL; track_002@3.95: CLS; track_003@4.00: CLS (+5 lost idle) | - | 17 | A: conf 1.40, OCCLUSION(static) (+1.20 s) |
| S06/run_0_a_front_pushed | A | 0/0 | 1 | - (+1 lost idle) | - | 2 | B: conf 0.25, none (prompt)<br>C: conf 2.65, FILTER (+1.45 s) |
| S06/run_0_a_front_pushed | B | 0/0 | 2 | track_001@6.20: CONFL+PATH | - | 1 | A: FOV never<br>C: conf 0.20, none (prompt) |
| S06/run_0_a_front_pushed | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S06/run_0_b_rear_first | A | 0/0 | 0 | - (+2 lost idle) | - | 2 | B: conf 0.25, none (prompt)<br>C: conf 2.65, FILTER (+1.45 s) |
| S06/run_0_b_rear_first | B | 0/0 | 1 | - | - | 1 | A: FOV never<br>C: conf 0.20, none (prompt) |
| S06/run_0_b_rear_first | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S07/run_0_full_view | A | 0/0 | 1 | - | - | 1 | B: conf 0.20, none (prompt)<br>C: FILTER (returns, none moving/usable) |
| S07/run_0_full_view | B | 0/0 | 1 | - | - | 1 | A: FOV never<br>C: conf 0.20, none (prompt) |
| S07/run_0_full_view | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S07/run_0_occluded | A | 0/0 | 1 | - | - | 1 | B: conf 0.20, none (prompt)<br>C: FILTER (returns, none moving/usable) |
| S07/run_0_occluded | B | 0/0 | 1 | - | - | 1 | A: FOV never<br>C: conf 0.20, none (prompt) |
| S07/run_0_occluded | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S08/run_0_crash | A | 0/0 | 1 | track_002@3.35: CLS+TTC+CONFL | - | 2 | B: conf 2.25, OCCLUSION(static) (+2.05 s)<br>C: conf 0.25, TRACKER (+0.20 s) |
| S08/run_0_crash | B | 0/0 | 1 | track_002@4.05: CLS | - | 2 | A: conf 2.35, OCCLUSION(static) (+2.15 s)<br>C: conf 2.40, OCCLUSION(static) (+2.20 s) |
| S08/run_0_crash | C | 0/0 | 1 | - | - | 2 | A: conf 0.25, TRACKER (+0.20 s)<br>B: conf 3.20, OCCLUSION(static) (+3.00 s) |
| S09/run_0_merge_conflict | A | 0/0 | 2 | - | - | 3 | B: conf 0.20, none (prompt) |
| S09/run_0_merge_conflict | B | 0/0 | 1 | track_001@1.65: CLS+TTC+CONFL; track_002@1.90: CLS | - | 2 | A: RAW_SENSOR(edge) (no return while in FOV) |
| S10/run_0_rolls_through | A | 0/0 | 1 | track_001@5.20: CLS+TTC+CONFL | 1 / 1 / 0; visible none vs known sign-0 | 1 | B: conf 4.00, RAW_SENSOR(edge) (+3.80 s) |
| S10/run_0_rolls_through | B | 0/0 | 2 | - | - | 1 | A: conf 2.85, OCCLUSION(static) (+2.65 s) |
| S10/run_0_stops_safely | A | 0/0 | 0 | - (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-0 | 1 | B: conf 4.05, RAW_SENSOR(edge) (+3.70 s) |
| S10/run_0_stops_safely | B | 0/0 | 1 | track_001@5.50: CLS+TTC | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 2.80, OCCLUSION(static) (+2.55 s) |
| S10/run_0_stops_then_proceeds | A | 0/0 | 0 | track_003@9.25: CLS+TTC; track_002@9.50: CLS; track_006@10.75: CLS; track_007@11.60: CLS; track_005@12.45: CLS (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-0 | 8 | B: conf 4.05, RAW_SENSOR(edge) (+3.70 s) |
| S10/run_0_stops_then_proceeds | B | 0/0 | 1 | track_001@5.50: CLS+TTC | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 2.80, OCCLUSION(static) (+2.55 s) |
| S11/run_0_rolls_through | A | 0/0 | 1 | track_001@5.45: CLS+TTC+CONFL | - | 1 | B: conf 3.00, OCCLUSION(static) (+2.70 s) |
| S11/run_0_rolls_through | B | 0/0 | 2 | - | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 4.15, RAW_SENSOR(edge) (+3.95 s) |
| S11/run_0_stops_safely | A | 0/0 | 0 | track_001@5.35: CLS | - | 1 | B: conf 2.80, OCCLUSION(static) (+2.60 s) |
| S11/run_0_stops_safely | B | 0/0 | 0 | - (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 3.80, RAW_SENSOR(edge) (+3.50 s) |
| S11/run_0_stops_then_proceeds | A | 0/0 | 0 | track_001@5.35: CLS | - | 1 | B: conf 2.80, OCCLUSION(static) (+2.60 s) |
| S11/run_0_stops_then_proceeds | B | 0/0 | 0 | track_005@8.65: CLS; track_002@9.90: CLS (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-1 | 5 | A: conf 3.80, RAW_SENSOR(edge) (+3.50 s) |
| S12/run_0_a_arrives_first | A | 0/0 | 1 | track_004@10.25: CLS+TTC; track_009@10.70: CLS+TTC; track_012@12.25: CLS; track_011@12.75: CLS; track_006@13.35: CLS; track_008@14.50: CLS; track_010@14.65: CLS; track_005@15.75: CLS; track_007@16.30: CLS | 1 / 1 / 0; visible none vs known sign-0 | 12 | B: conf 9.35, OCCLUSION(static) (+9.15 s) |
| S12/run_0_a_arrives_first | B | 0/0 | 0 | track_001@10.85: CLS+TTC | 1 / 1 / 0; visible none vs known sign-0 | 1 | A: conf 3.20, OCCLUSION(static) (+3.00 s) |
| S12/run_0_b_arrives_first | A | 0/0 | 0 | track_007@14.00: CLS+TTC; track_003@14.40: CLS; track_013@15.60: CLS (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-0 | 13 | B: conf 3.25, OCCLUSION(static) (+3.00 s) |
| S12/run_0_b_arrives_first | B | 0/0 | 0 | track_001@8.75: CLS | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 3.25, OCCLUSION(static) (+3.00 s) |
| S12/run_0_b_fails_to_stop | A | 0/0 | 1 | track_001@9.65: CLS+TTC+CONFL | 1 / 1 / 0; visible none vs known sign-0 | 1 | B: conf 7.10, OCCLUSION(static) (+6.75 s) |
| S12/run_0_b_fails_to_stop | B | 0/0 | 2 | - | 1 / 1 / 0; visible none vs known sign-1 | 3 | A: conf 8.35, TRACKER (+5.10 s) |
| S12/run_0_near_simultaneous | A | 0/0 | 0 | track_001@2.80: CLS; track_002@9.80: CLS | 3 / 2 / 1; visible none vs known sign-0,sign-1 | 8 | B: conf 2.80, OCCLUSION(static) (+2.50 s) |
| S12/run_0_near_simultaneous | B | 0/0 | 1 | track_001@9.60: CONFL | 1 / 1 / 0; visible none vs known sign-1 | 1 | A: conf 2.75, OCCLUSION(static) (+2.55 s) |
| S13/run_0_accelerates_into_gap | A | 1/0 | 1 | track_001@1.00: CLS | - | 2 | B: conf 0.20, none (prompt) |
| S13/run_0_accelerates_into_gap | B | 0/0 | 1 | track_006@6.45: CLS; track_008@6.55: CLS; track_007@6.60: CLS; track_009@6.60: CLS; track_010@6.65: CLS; track_011@6.70: CLS; track_012@6.75: CLS; track_013@6.80: CLS | - | 16 | A: FOV never |
| S13/run_0_cut_in | A | 1/0 | 1 | - | - | 1 | B: conf 0.25, none (prompt) |
| S13/run_0_cut_in | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S13/run_0_safe_lane_change | A | 1/0 | 0 | - | - | 1 | B: conf 0.25, none (prompt) |
| S13/run_0_safe_lane_change | B | 0/0 | 0 | - | - | 0 | A: FOV never |
| S15/run_0_b_stops | A | 0/0 | 1 | track_002@3.80: CLS+TTC; track_001@4.45: CLS+TTC | - | 2 | B: conf 2.20, OCCLUSION(static) (+2.00 s)<br>C: conf 0.20, none (prompt) |
| S15/run_0_b_stops | B | 0/0 | 1 | track_001@2.85: CLS (+1 lost idle) | 5 / 2 / 3; visible sign-1 vs known sign-0,sign-1 | 3 | A: conf 2.15, OCCLUSION(static) (+1.95 s)<br>C: conf 1.75, OCCLUSION(static) (+1.45 s) |
| S15/run_0_b_stops | C | 0/0 | 2 | track_002@4.00: CLS; track_001@4.50: CLS+TTC | - | 2 | A: conf 0.20, none (prompt)<br>B: conf 0.25, none (prompt) |
| S15/run_0_deflected_into_c | A | 0/0 | 2 | track_002@3.75: CLS+TTC+CONFL | 5 / 2 / 3; visible sign-2 vs known sign-0,sign-2 | 2 | B: conf 2.20, OCCLUSION(static) (+2.00 s)<br>C: conf 0.20, none (prompt) |
| S15/run_0_deflected_into_c | B | 0/0 | 1 | track_001@2.80: CLS | 1 / 1 / 0; visible none vs known sign-0 | 2 | A: conf 2.15, OCCLUSION(static) (+1.95 s)<br>C: conf 1.75, OCCLUSION(static) (+1.45 s) |
| S15/run_0_deflected_into_c | C | 0/0 | 2 | track_002@4.45: CLS | - | 2 | A: conf 0.20, none (prompt)<br>B: conf 0.25, none (prompt) |
| S15/run_0_single_impact | A | 0/0 | 1 | track_002@3.75: CLS+TTC+CONFL | 2 / 2 / 0; visible sign-1 vs known sign-0,sign-1 | 2 | B: conf 2.20, OCCLUSION(static) (+2.00 s)<br>C: conf 1.00, TRACKER (+0.20 s) |
| S15/run_0_single_impact | B | 0/0 | 1 | - (+1 lost idle) | 1 / 1 / 0; visible none vs known sign-0 | 1 | A: conf 2.15, OCCLUSION(static) (+1.95 s)<br>C: OCCLUSION(static) (no return while in FOV) |
| S15/run_0_single_impact | C | 0/0 | 0 | - | 1 / 1 / 0; visible none vs known sign-0 | 2 | A: conf 1.00, TRACKER (+0.20 s)<br>B: conf 1.30, TRACKER (+1.15 s) |
| S16/run_0_avoided | A | 0/0 | 0 | - | - | 0 | B: FOV never<br>C: TRACKER (usable returns, no confirmed track) |
| S16/run_0_avoided | B | 0/0 | 2 | - | - | 1 | A: conf 0.20, none (prompt)<br>C: FILTER (returns, none moving/usable) |
| S16/run_0_avoided | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S16/run_0_consequential | A | 0/0 | 1 | - (+2 lost idle) | - | 3 | B: FOV never<br>C: conf 5.65, FILTER (+5.15 s) |
| S16/run_0_consequential | B | 0/0 | 2 | - | - | 1 | A: conf 0.20, none (prompt)<br>C: TRACKER (usable returns, no confirmed track) |
| S16/run_0_consequential | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |
| S16/run_0_independent | A | 0/0 | 1 | track_002@13.50: CLS+TTC+PATH; track_001@14.35: CONFL+PATH | - | 2 | B: FOV never<br>C: conf 11.55, TRACKER (+6.40 s) |
| S16/run_0_independent | B | 0/0 | 2 | - (+1 lost idle) | - | 2 | A: conf 0.20, none (prompt)<br>C: conf 13.75, FILTER (+8.40 s) |
| S16/run_0_independent | C | 0/0 | 0 | - | - | 0 | A: FOV never<br>B: FOV never |

## 9. Close multiple collisions (2026-10-01)

Reconstruction only: CARLA was not rerun and no raw file changed (checksums of all 971 raw files identical
before and after). All 33 runs were reconstructed and evaluated again. The graph vocabulary is unchanged:
every contact is a plain `COLLISION` node, in local and global graphs.

**Problem.** In S06 `a_front_pushed` B is struck from behind by A at 5.90 s (11622 N*s) and pushed into C
0.25 s later (9832 N*s), then stays in contact with C for 24 s (~470 small callbacks). The single 0.5 s merge
gap fused B's two impacts into one COLLISION, so C's report matched no other report, C stayed UNALIGNED and
the global graph had no COLLISION(B,C). Besides, only the reference collision aligned graphs (no multi-hop)
and identity association looked only at the reference partner.

**Segmentation rule** (`local.collision_events`, recorder-local data only). The collision sensor calls back
once per sample (0.05 s) while the bodies touch and reports only the impulse magnitude. Callbacks without a
missing sample (gap <= 1.5 x the recorder's own sample period) form a burst. A burst starts a new COLLISION
when

1. the pause since the previous callback exceeds `merge_gap_s` = 0.5 s, or
2. it follows a break (at least one sample without a callback) and its peak impulse is at least
   `new_impact_ratio` = 0.5 x the current contact's peak: a rebound of the same two bodies returns with about
   the restitution coefficient times the first impulse (below 0.5 between vehicles) and persistent contact
   with far less, or
3. (supplementary evidence, never decisive alone) it follows a break, peaks at `reversal_impact_ratio` = 0.25
   x the contact's peak or more, and the recorder's own velocity jumps like an impact, a mean acceleration of
   at least `impact_acceleration_mps2` = 20 m/s^2 (twice what tyres can produce) from the sample before to
   the sample after, both at the contact's start and at the burst's, in directions more than
   `reversal_angle_deg` = 90 deg apart: a rebound pushes the recorder the same way again.

Any other burst continues the contact. A contact opened within 0.5 s of the previous one carries
`new_contact` (`break_s`, `peak_ratio`, `reversal_deg` when rule 3 fired). Thresholds are global.

Every burst of the campaign that follows a break within 0.5 s (true partner from `ground_truth/`, offline
validation only):

| Run, recorder | Burst t_local [s] | Break [s] | Burst peak / contact peak [N*s] | Own jump at contact / burst [m/s^2] | Angle [deg] | True partner (offline) | Rule |
|---|---:|---:|---|---|---:|---|---|
| S06/a_front_pushed B | 6.15 | 0.25 | 9832 / 11622 = 0.85 | 78.6 / 56.1 | 180 | A -> C | **new COLLISION** |
| S06/a_front_pushed B | 6.25 | 0.10 | 1157 / 9832 = 0.12 | 56.1 / 6.8 | 1 | C -> C | same contact |
| S06/a_front_pushed C | 6.25 | 0.10 | 1157 / 9832 = 0.12 | 0.1 / 0.0 | 112 | B -> B | same contact |
| S12/b_fails_to_stop A | 9.80 | 0.10 | 1789 / 7340 = 0.24 | 33.0 / 9.4 | 25 | B -> B | same contact |
| S12/b_fails_to_stop B | 9.80 | 0.10 | 1789 / 7340 = 0.24 | 45.8 / 3.8 | 73 | A -> A | same contact |
| S13/accelerates_into_gap A | 5.80 | 0.15 | 548 / 5216 = 0.10 | 29.9 / 6.5 | 7 | B -> B | same contact |
| S13/accelerates_into_gap B | 5.80 | 0.15 | 548 / 5216 = 0.10 | 45.8 / 3.7 | 65 | A -> A | same contact |
| S16/independent A | 14.45 | 0.35 | 3883 / 9096 = 0.43 | 66.2 / 20.6 | 3 | C -> C | same contact |
| S16/independent A | 14.55 | 0.10 | 1407 / 9096 = 0.15 | 66.2 / 16.9 | 5 | C -> C | same contact |
| S16/independent A | 14.85 | 0.15 | 204 / 9096 = 0.02 | 66.2 / 0.5 | 174 | C -> C | same contact |
| S16/independent C | 14.45 | 0.35 | 3883 / 9096 = 0.43 | 28.9 / 9.6 | 177 | A -> A | same contact |
| S16/independent C | 14.55 | 0.10 | 1407 / 9096 = 0.15 | 28.9 / 7.6 | 175 | A -> A | same contact |
| S16/independent C | 14.85 | 0.15 | 204 / 9096 = 0.02 | 28.9 / 0.1 | 76 | A -> A | same contact |

Margins: the strongest rebound is 0.43 (S16), the new partner 0.85 (S06). Rule 3 never fires in the
campaign; its closest calls are S16 independent C at 14.45 s (reversed direction, but a 9.6 m/s^2 jump:
braking, not an impact) and A at 14.45 s (impact-like 20.6 m/s^2, but the same direction as the first
impact). Partner changes after a pause above 0.5 s were already separated (S06 b_rear_first B 1.40 s, S15
deflected_into_c A 0.95 s, S16 consequential A 0.75 s, S16 independent A 8.95 s).

**Matching and alignment** (`alignment.py`). Reports are matched by impulse (within 10 %), best first; a match
also fixes the clock offset between its two graphs, and a match between graphs already linked (directly or
through other graphs) must agree with that offset within `clock_tolerance_s` = 0.1 s, or it is rejected
(`rejected_matches`; none in the campaign). The strongest matched collision only defines t_global = 0; any
graph sharing a matched collision with an aligned graph is aligned through it (breadth first, `chain` in
`alignment.json`).

**Identity association** (`fusion.py`). Every matched collision of a recorder names a partner; the
hierarchical checks run per collision. A track is named only if it is the recorder's only compatible track
for a collision with that partner and compatible with no other partner (conflict) - otherwise it stays
anonymous. `associations.json` records the collision each decision rests on.

**Temporal safety relations.** A recorder can now have several COLLISIONs: a track's relation uses the first
one at or after its critical TTC start (without one, after its cut-in or path entry), and in the global graph,
once the track is identified, the first such collision with that entity (`collision_with`).

S06 `a_front_pushed`, before -> after:

| | Before (`e2153e1`) | After |
|---|---|---|
| Local COLLISIONs | A 5.90; B 5.90 (peak 11622, both impacts fused); C 6.15 | A 5.90; B 5.90 (11622) and 6.15 (9832, `new_contact` break 0.25 s, ratio 0.85); C 6.15 |
| Matches | A-B only (C's report matched nothing) | collision_001 A-B, collision_002 B-C |
| Alignment | A, B ALIGNED; C UNALIGNED | A, B ALIGNED; C ALIGNED via collision_001 -> collision_002 |
| Global COLLISION nodes | (A,B) at 0.00; C alone, unaligned | (A,B) at 0.00 (reference), (B,C) at +0.25 |
| Identity | A:track_001 -> B; B:track_001 anonymous (tested against A only) | A:track_001 -> B (0.67); B:track_001 -> C (0.99) |
| B:track_001 relation | CRITICAL_TTC 3.75, COLLISION 5.90 (impact by A) | CRITICAL_TTC 3.75, COLLISION with C 6.15 (+2.40 s) |
| Evaluation | collision reconstructed: NO | yes (2/2 vehicle contacts), 2/2 claims correct |

Other runs that changed:

| Run | Change |
|---|---|
| S06 b_rear_first | C ALIGNED via collision_002; (B,C) at -1.40 merged (was B alone + unaligned C); B:track_001 -> C |
| S15 deflected_into_c | C ALIGNED via collision_002; (A,C) at +0.95 merged; A:track_001 -> C, C:track_002 -> A; A:track_001's relation now ends at its collision with C (4.75) |
| S16 consequential | C ALIGNED via collision_002; (A,C) at +0.75 merged |
| S16 independent | B ALIGNED via collision_001 (the reference is A-C); (A,B) at -8.95 merged; B:track_001 -> A; A:track_002's relation now ends at COLLISION 14.10 with C (+1.45 s) instead of the earlier collision with B (-7.50 s) |
| S05 crash B, S13 accelerates_into_gap B, S15 single_impact A, S15 deflected_into_c B | relations only: post-impact tracks are no longer paired with a collision that preceded them |

All other runs keep the same COLLISIONs, alignment and identities (only new output fields). Campaign
totals before -> after: vehicle-vehicle contacts reproduced 22/27 -> 27/27, with no extra COLLISION node;
aligned graphs 44 -> 49 (the 5 still UNALIGNED are uninvolved vehicles that recorded no collision: S07 C x2,
S08 C, S15 single_impact C, S16 avoided C); identity claims correct 29/29 -> 34/34; max |t_global error|
0.0 s; the clock-shift check (0.73 s) leaves every global graph unchanged, including C in S06, aligned by two
hops.

Tests: `tests/test_multi_collision.py` (segmentation, time-consistent matching, multi-hop alignment, conflict,
S06 regression, and a campaign-wide check of every run against the true contacts); 168 tests pass on Python
3.8.20 and 3.14.
