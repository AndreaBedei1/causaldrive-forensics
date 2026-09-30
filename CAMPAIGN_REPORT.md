# Semantic-event redesign: full-scenario campaign report (2026-09-29)

Canonical dataset: `traces/<Sxx>/run_0_<variant>` (the 32 runs of this campaign); each run has
`reconstruction/` (local, global, evaluation). Campaign-level files: `traces/campaign_runs.json`,
`traces/campaign_summary.json`, `traces/stop_sign_audit.json`, `traces/vocabulary_comparison.json`.

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

32 runs = S01 {avoided, crash}, S02 {avoided, crash}, S03 crash, S04 yield, S05 crash, S06 {a_front_pushed,
b_rear_first}, S07 {full_view, occluded}, S08 crash, S09 merge_conflict (Town03_Opt), S10 / S11 {rolls_through,
stops_safely, stops_then_proceeds}, S12 {a_arrives_first, b_arrives_first, b_fails_to_stop, near_simultaneous},
S13 {accelerates_into_gap, cut_in, safe_lane_change}, S15 {b_stops, deflected_into_c, single_impact},
S16 {avoided, consequential, independent}; Town05 except S09. Seed 0, speed limit 50 km/h in every run.

Transition counts are START/END over the global graph (all recorders). BR brake, HB hard brake, THR strong
throttle, MOV moving, STOP stop, SPD speed limit exceeded, CLS closing, TTC critical TTC, STOPSIGN STOP sign
detected, TRACK appeared/lost, PATH ego-path entry/exit, COLL collision nodes. No YIELD sign was detected in
any run (the two maps contain no yield-sign actors), so YIELD_SIGN_DETECTED never occurs.

| Run | Limit | Local A/B/C nodes:edges | Global nodes:edges | Collision reconstructed | Alignment | Identity associations | Transitions (START/END) |
|---|---:|---|---|---|---|---|---|
| S01/run_0_avoided | 50 | A 15:23 B 12:20 | 27:6 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 2/1, HB 2/1, THR 4/2, MOV 3/2, STOP 2/1, CLS 2/2, TTC 1/1, TRACK 1/0, PATH 0/0, COLL 0 |
| S01/run_0_crash | 50 | A 15:26 B 8:10 | 22:35 | yes | A ok B ok | A:track_001→B (0.99) | BR 2/0, HB 2/0, THR 2/2, MOV 2/2, STOP 2/0, CLS 2/2, TTC 1/1, TRACK 1/0, PATH 0/0, COLL 1 |
| S02/run_0_avoided | 50 | A 13:18 B 5:4 | 18:5 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 2/2, HB 1/1, THR 2/2, MOV 2/0, CLS 1/1, TTC 1/1, TRACK 1/0, PATH 1/0, COLL 0 |
| S02/run_0_crash | 50 | A 14:20 B 10:13 | 23:33 | yes | A ok B ok | A:track_001→B (0.97) | BR 3/1, HB 2/0, THR 2/2, MOV 2/2, STOP 2/0, CLS 1/1, TTC 1/1, TRACK 1/0, PATH 1/0, COLL 1 |
| S03/run_0_crash | 50 | A 10:15 B 17:37 | 26:59 | yes | A ok B ok | B:track_001→A (0.84); anonymous 1 (A:track_001) | BR 2/0, HB 2/0, THR 2/2, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, TRACK 2/1, PATH 1/1, COLL 1 |
| S04/run_0_yield | 50 | A 9:13 B 26:47 | 35:13 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 4 | BR 2/2, HB 1/1, THR 2/2, MOV 3/1, STOP 1/1, CLS 4/1, TTC 2/1, STOPSIGN 1/1, TRACK 4/3, PATH 1/1, COLL 0 |
| S05/run_0_crash | 50 | A 16:34 B 63:301 | 78:417 | yes | A ok B ok | A:track_001→B (0.89); anonymous 17 | BR 2/0, HB 2/0, THR 3/3, MOV 2/2, STOP 2/0, CLS 11/9, TTC 2/1, TRACK 18/9, PATH 6/5, COLL 1 |
| S06/run_0_a_front_pushed | 50 | A 17:23 B 23:54 C 10:11 | 49:71 | NO | A ok B ok C UNALIGNED | A:track_001→B (0.67); anonymous 2 (A:track_002, B:track_001) | BR 3/1, HB 3/1, THR 4/3, MOV 4/4, STOP 4/1, SPD 1/1, CLS 4/4, TTC 2/2, TRACK 3/2, PATH 0/0, COLL 2 |
| S06/run_0_b_rear_first | 50 | A 16:26 B 18:37 C 10:11 | 43:64 | NO | A ok B ok C UNALIGNED | none; anonymous 3 (A:track_001, A:track_002, B:track_001) | BR 3/0, HB 3/0, THR 5/5, MOV 3/3, STOP 3/0, SPD 1/1, CLS 3/3, TTC 1/1, TRACK 3/2, PATH 0/0, COLL 3 |
| S07/run_0_full_view | 50 | A 17:35 B 15:23 C 14:21 | 45:70 | yes | A ok B ok C UNALIGNED | A:track_001→B (0.98); anonymous 1 (B:track_001) | BR 3/1, HB 3/1, THR 5/4, MOV 4/3, STOP 3/1, SPD 1/1, CLS 4/4, TTC 2/2, TRACK 2/0, PATH 0/0, COLL 1 |
| S07/run_0_occluded | 50 | A 17:35 B 15:23 C 14:21 | 45:70 | yes | A ok B ok C UNALIGNED | A:track_001→B (0.98); anonymous 1 (B:track_001) | BR 3/1, HB 3/1, THR 5/4, MOV 4/3, STOP 3/1, SPD 1/1, CLS 4/4, TTC 2/2, TRACK 2/0, PATH 0/0, COLL 1 |
| S08/run_0_crash | 50 | A 17:29 B 20:44 C 20:34 | 56:90 | yes | A ok B ok C UNALIGNED | B:track_001→A (0.84); anonymous 5 | BR 3/1, HB 3/1, THR 3/2, MOV 3/3, STOP 3/0, CLS 6/4, TTC 7/6, TRACK 6/2, PATH 1/1, COLL 1 |
| S09/run_0_merge_conflict | 50 | A 18:44 B 15:24 | 32:108 | yes | A ok B ok | A:track_001→B (0.63); anonymous 4 | BR 2/0, HB 2/0, THR 1/1, MOV 2/2, STOP 2/0, CLS 5/3, TTC 2/1, TRACK 5/2, PATH 1/0, COLL 1 |
| S10/run_0_rolls_through | 50 | A 19:38 B 16:30 | 34:76 | yes | A ok B ok | A:track_001→B (0.96); B:track_001→A (0.91) | BR 3/1, HB 3/1, THR 3/3, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, STOPSIGN 1/1, TRACK 2/1, PATH 2/0, COLL 1 |
| S10/run_0_stops_safely | 50 | A 16:27 B 9:12 | 25:10 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, HB 1/0, THR 2/1, MOV 2/1, STOP 1/0, CLS 2/1, TTC 2/1, STOPSIGN 2/2, TRACK 2/2, PATH 1/1, COLL 0 |
| S10/run_0_stops_then_proceeds | 50 | A 41:87 B 9:12 | 50:23 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 9 | BR 1/1, HB 1/1, THR 2/2, MOV 3/1, STOP 1/1, CLS 9/1, TTC 3/1, STOPSIGN 2/2, TRACK 9/7, PATH 1/1, COLL 0 |
| S11/run_0_rolls_through | 50 | A 13:26 B 24:40 | 36:77 | yes | A ok B ok | A:track_001→B (0.94); B:track_001→A (0.95) | BR 3/1, HB 3/1, THR 4/4, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, STOPSIGN 1/1, TRACK 2/1, PATH 2/0, COLL 1 |
| S11/run_0_stops_safely | 50 | A 6:10 B 18:29 | 24:11 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, HB 1/0, THR 2/1, MOV 2/1, STOP 1/0, CLS 2/1, TTC 2/2, STOPSIGN 1/1, TRACK 2/2, PATH 1/1, COLL 0 |
| S11/run_0_stops_then_proceeds | 50 | A 6:10 B 37:76 | 43:21 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 6 | BR 1/1, HB 1/1, THR 2/2, MOV 3/1, STOP 1/1, CLS 6/1, TTC 2/2, STOPSIGN 1/1, TRACK 6/4, PATH 3/3, COLL 0 |
| S12/run_0_a_arrives_first | 50 | A 49:123 B 23:45 | 72:31 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 13 | BR 2/2, HB 2/2, THR 3/3, MOV 4/2, STOP 2/2, CLS 14/1, TTC 3/0, STOPSIGN 2/2, TRACK 13/10, PATH 2/1, COLL 0 |
| S12/run_0_b_arrives_first | 50 | A 51:132 B 20:33 | 71:29 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 14 | BR 2/2, HB 2/2, THR 3/3, MOV 4/2, STOP 2/2, CLS 16/3, TTC 1/0, STOPSIGN 2/2, TRACK 14/5, PATH 2/2, COLL 0 |
| S12/run_0_b_fails_to_stop | 50 | A 25:49 B 30:67 | 54:139 | yes | A ok B ok | A:track_001→B (0.90); B:track_001→A (0.88); anonymous 2 (B:track_002, B:track_003) | BR 4/2, HB 4/2, THR 5/5, MOV 3/3, STOP 3/1, CLS 4/3, TTC 2/1, STOPSIGN 2/2, TRACK 4/1, PATH 2/0, COLL 1 |
| S12/run_0_near_simultaneous | 50 | A 48:129 B 32:64 | 79:255 | yes | A ok B ok | B:track_001→A (0.79); anonymous 8 | BR 4/2, HB 4/2, THR 5/5, MOV 4/4, STOP 4/2, CLS 10/8, TTC 1/1, STOPSIGN 4/4, TRACK 9/3, PATH 1/1, COLL 1 |
| S13/run_0_accelerates_into_gap | 50 | A 25:53 B 62:226 | 86:307 | yes | A ok B ok | A:track_002→B (0.93); anonymous 17 | BR 2/0, HB 2/0, THR 2/2, MOV 2/2, STOP 2/0, SPD 1/1, CLS 19/10, TTC 4/4, TRACK 18/9, PATH 4/1, COLL 1 |
| S13/run_0_cut_in | 50 | A 12:20 B 6:7 | 17:29 | yes | A ok B ok | A:track_001→B (0.97) | BR 2/0, HB 2/0, MOV 2/2, STOP 2/0, CLS 1/1, TTC 1/1, TRACK 1/0, PATH 1/0, COLL 1 |
| S13/run_0_safe_lane_change | 50 | A 7:10 B 3:2 | 10:4 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 1 (A:track_001) | BR 1/0, THR 1/1, MOV 2/0, CLS 2/1, TRACK 1/0, PATH 1/0, COLL 0 |
| S15/run_0_b_stops | 50 | A 9:20 B 35:61 C 14:22 | 58:30 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED C UNALIGNED | none; anonymous 7 | BR 1/0, HB 1/0, THR 3/2, MOV 3/1, STOP 1/0, CLS 7/3, TTC 6/4, STOPSIGN 5/4, TRACK 7/6, PATH 2/2, COLL 0 |
| S15/run_0_deflected_into_c | 50 | A 26:45 B 25:47 C 21:34 | 71:109 | NO | A ok B ok C UNALIGNED | A:track_002→B (0.97); B:track_002→A (0.90); anonymous 4 | BR 3/1, HB 2/0, THR 5/5, MOV 3/3, STOP 3/0, CLS 6/3, TTC 6/5, STOPSIGN 6/5, TRACK 6/3, PATH 3/0, COLL 3 |
| S15/run_0_single_impact | 50 | A 19:37 B 22:41 C 10:21 | 50:97 | yes | A ok B ok C UNALIGNED | A:track_002→B (0.97); B:track_001→A (0.90); anonymous 3 (A:track_001, C:track_001, C:track_002) | BR 2/1, HB 1/0, THR 3/3, MOV 3/2, STOP 2/0, CLS 6/2, TTC 2/1, STOPSIGN 4/3, TRACK 5/2, PATH 4/3, COLL 1 |
| S16/run_0_avoided | 50 | A 8:7 B 17:29 C 3:2 | 27:43 | yes | A ok B ok C UNALIGNED | B:track_001→A (0.95) | BR 2/0, HB 2/0, THR 2/2, MOV 3/3, STOP 3/0, CLS 2/2, TTC 2/2, TRACK 1/0, PATH 0/0, COLL 1 |
| S16/run_0_consequential | 50 | A 21:38 B 17:29 C 10:18 | 47:88 | NO | A ok B ok C UNALIGNED | B:track_001→A (0.95); anonymous 3 (A:track_001, A:track_002, A:track_003) | BR 3/1, HB 2/0, THR 2/2, MOV 4/4, STOP 4/1, CLS 4/4, TTC 3/3, TRACK 4/2, PATH 1/0, COLL 3 |
| S16/run_0_independent | 50 | A 28:49 B 20:35 C 10:14 | 57:73 | NO | A ok B UNALIGNED C ok | A:track_001→C (1.00); anonymous 3 (A:track_002, B:track_001, B:track_002) | BR 3/1, HB 2/0, THR 4/3, MOV 5/5, STOP 5/2, CLS 4/3, TTC 4/3, TRACK 4/3, PATH 2/1, COLL 3 |

Evaluation (privileged, after reconstruction): every identity claim in every run is correct; aligned global
times have 0.0 s error; clock-shift checks pass.

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

**S01/run_0_avoided** (global graph, unaligned nodes: 27)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED(track_001); 0.45 CLOSING_START(track_001); 1.15 STRONG_THROTTLE_START; 1.35 STRONG_THROTTLE_END; 1.60 CLOSING_END(track_001); 4.25 CLOSING_START(track_001); 5.00 CRITICAL_TTC_START(track_001); 5.05 BRAKE_START; 5.05 HARD_BRAKE_START; 6.25 CRITICAL_TTC_END(track_001); 6.35 CLOSING_END(track_001); 6.35 MOVING_END; 6.35 STOP_START; 13.05 STRONG_THROTTLE_START
B: 0.00 MOVING_START*; 0.40 STRONG_THROTTLE_START; 1.75 STRONG_THROTTLE_END; 3.95 BRAKE_START; 3.95 HARD_BRAKE_START; 5.15 MOVING_END; 5.15 STOP_START; 11.95 HARD_BRAKE_END; 11.95 BRAKE_END; 11.95 STRONG_THROTTLE_START; 12.35 STOP_END; 12.35 MOVING_START
```

**S01/run_0_crash** (global graph)

```
-6.50 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B)
-6.10 STRONG_THROTTLE_START(B)
-6.05 CLOSING_START(A,B)
-5.35 STRONG_THROTTLE_START(A)
-5.15 STRONG_THROTTLE_END(A)
-4.90 CLOSING_END(A,B)
-4.75 STRONG_THROTTLE_END(B)
-2.55 BRAKE_START(B); HARD_BRAKE_START(B)
-2.25 CLOSING_START(A,B)
-1.50 CRITICAL_TTC_START(A,B)
-1.35 MOVING_END(B); STOP_START(B)
-0.95 BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 MOVING_END(A); STOP_START(A); HARD_BRAKE_START(A)
```

**S02/run_0_avoided** (global graph, unaligned nodes: 18)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED(track_001); 0.00 CLOSING_START(track_001)*; 1.15 STRONG_THROTTLE_START; 1.35 STRONG_THROTTLE_END; 2.75 CRITICAL_TTC_START(track_001); 2.85 BRAKE_START; 2.85 HARD_BRAKE_START; 3.10 CRITICAL_TTC_END(track_001); 3.15 EGO_PATH_ENTRY(track_001); 3.70 HARD_BRAKE_END; 4.05 CLOSING_END(track_001); 4.10 BRAKE_END
B: 0.00 MOVING_START*; 0.35 STRONG_THROTTLE_START; 1.30 STRONG_THROTTLE_END; 3.15 BRAKE_START; 3.60 BRAKE_END
```

**S02/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B)
-3.90 STRONG_THROTTLE_START(B)
-3.10 STRONG_THROTTLE_START(A)
-2.95 STRONG_THROTTLE_END(B)
-2.90 STRONG_THROTTLE_END(A)
-1.45 CRITICAL_TTC_START(A,B)
-1.10 BRAKE_START(B)
-1.05 EGO_PATH_ENTRY(A,B)
-0.65 BRAKE_END(B)
-0.40 BRAKE_START(A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); BRAKE_START(B); HARD_BRAKE_START(B)
+0.05 HARD_BRAKE_START(A)
+0.60 MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
```

**S03/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B)
-3.10 STRONG_THROTTLE_START(B)
-2.20 TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-2.10 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-1.90 CRITICAL_TTC_START(A,A:track_001); CRITICAL_TTC_START(B,A)
-1.85 STRONG_THROTTLE_END(B)
-0.90 TRACK_LOST(A,A:track_001)
-0.15 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.30 MOVING_END(B); STOP_START(B)
+0.45 EGO_PATH_EXIT(B,A)
+0.65 MOVING_END(A); STOP_START(A)
```

**S04/run_0_yield** (global graph, unaligned nodes: 35)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.10 TRACK_APPEARED(track_001); 2.10 CLOSING_START(track_001)*; 3.00 CRITICAL_TTC_START(track_001); 4.95 TRACK_LOST(track_001); 8.15 STOP_SIGN_DETECTED_START(sign-0); 8.45 STOP_SIGN_DETECTED_END(sign-0); 9.70 TRACK_APPEARED(track_002); 9.70 CLOSING_START(track_002)*
B: 0.00 MOVING_START*; 1.25 STRONG_THROTTLE_START; 1.85 STRONG_THROTTLE_END; 2.00 TRACK_APPEARED(track_001); 2.00 CLOSING_START(track_001)*; 2.35 TRACK_LOST(track_001); 3.15 BRAKE_START; 3.15 HARD_BRAKE_START; 3.90 MOVING_END; 3.90 STOP_START; 4.35 TRACK_APPEARED(track_002); 4.35 CLOSING_START(track_002)*; 4.35 CRITICAL_TTC_START(track_002)*; 5.40 EGO_PATH_ENTRY(track_002); 5.45 CRITICAL_TTC_END(track_002); 5.55 CLOSING_END(track_002); 5.90 EGO_PATH_EXIT(track_002); 6.90 TRACK_LOST(track_002); 7.15 HARD_BRAKE_END; 7.15 BRAKE_END; 7.15 STRONG_THROTTLE_START; 7.55 STOP_END; 7.55 MOVING_START; 8.55 STRONG_THROTTLE_END; 8.75 BRAKE_START; 9.00 BRAKE_END
```

**S05/run_0_crash** (global graph)

```
-3.70 MOVING_START(A); MOVING_START(B)
-2.85 STRONG_THROTTLE_START(B)
-2.50 TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
-2.45 TRACK_APPEARED(A,B); CLOSING_START(A,B)
-2.10 STRONG_THROTTLE_END(B)
-2.05 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001)
-0.85 TRACK_LOST(B,B:track_001)
-0.20 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_006); TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
+0.10 EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED(B,B:track_010); EGO_PATH_ENTRY(B,B:track_006)
+0.15 EGO_PATH_EXIT(B,B:track_006); TRACK_APPEARED(B,B:track_009); TRACK_APPEARED(B,B:track_011); TRACK_APPEARED(B,B:track_013); EGO_PATH_ENTRY(B,B:track_003)
+0.20 EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED(B,B:track_012)
+0.25 TRACK_APPEARED(B,B:track_014); TRACK_APPEARED(B,B:track_015); CLOSING_START(B,B:track_012); TRACK_LOST(A,B); TRACK_LOST(B,B:track_002)
+0.30 CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TRACK_APPEARED(B,B:track_016); TRACK_APPEARED(B,B:track_017); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_006)
+0.35 CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_008); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005)
+0.40 EGO_PATH_EXIT(B,B:track_013)
+0.50 EGO_PATH_ENTRY(B,B:track_012)
+0.55 CLOSING_END(B,B:track_012)
+0.60 CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B); TRACK_LOST(B,B:track_017)
+0.75 TRACK_LOST(B,B:track_008)
+0.85 MOVING_END(A); STOP_START(A)
```

**S06/run_0_a_front_pushed** (global graph, unaligned nodes: 10)

```
-5.90 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); TRACK_APPEARED(B,B:track_001)
-5.55 STRONG_THROTTLE_START(B)
-5.45 CLOSING_START(A,B)
-4.80 CLOSING_START(B,B:track_001)
-4.75 STRONG_THROTTLE_START(A)
-4.55 STRONG_THROTTLE_END(A)
-4.35 TRACK_APPEARED(A,A:track_002)
-4.30 CLOSING_END(A,B)
-4.15 STRONG_THROTTLE_END(B)
-3.80 CLOSING_END(B,B:track_001)
-2.95 TRACK_LOST(A,A:track_002)
-2.70 CLOSING_START(B,B:track_001)
-2.20 BRAKE_START(B); HARD_BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001)
-1.90 CLOSING_START(A,B)
-1.20 CRITICAL_TTC_START(A,B)
-1.00 CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
-0.35 BRAKE_START(A)
-0.20 HARD_BRAKE_END(B); BRAKE_END(B); STRONG_THROTTLE_START(B)
+0.00 COLLISION(A,B); STOP_END(B); MOVING_START(B)
+0.05 HARD_BRAKE_START(A)
+0.30 TRACK_LOST(B,B:track_001)
+0.35 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); MOVING_END(A); STOP_START(A)
+0.40 MOVING_END(B); STOP_START(B)
```

**S06/run_0_b_rear_first** (global graph, unaligned nodes: 10)

```
-6.00 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(B,B:track_001)
-5.65 STRONG_THROTTLE_START(B)
-5.55 CLOSING_START(A,A:track_001)
-4.90 CLOSING_START(B,B:track_001)
-4.85 STRONG_THROTTLE_START(A)
-4.65 STRONG_THROTTLE_END(A)
-4.45 TRACK_APPEARED(A,A:track_002)
-4.40 CLOSING_END(A,A:track_001)
-4.25 STRONG_THROTTLE_END(B)
-3.90 CLOSING_END(B,B:track_001)
-3.05 TRACK_LOST(A,A:track_002)
-2.80 CLOSING_START(B,B:track_001)
-2.30 CRITICAL_TTC_START(B,B:track_001)
-1.45 TRACK_LOST(A,A:track_001)
-1.40 COLLISION(B); STRONG_THROTTLE_START(B)
-1.35 CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
-1.25 MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A)
+0.05 STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
+0.20 MOVING_END(A); STOP_START(A)
```

**S07/run_0_full_view** (global graph, unaligned nodes: 14)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); TRACK_APPEARED(B,B:track_001)
-5.25 STRONG_THROTTLE_START(B); CLOSING_START(A,B)
-4.60 CLOSING_START(B,B:track_001)
-4.55 STRONG_THROTTLE_START(A)
-4.35 STRONG_THROTTLE_END(A)
-4.10 CLOSING_END(A,B)
-3.95 STRONG_THROTTLE_END(B)
-3.60 CLOSING_END(B,B:track_001)
-2.45 CLOSING_START(B,B:track_001)
-2.05 BRAKE_START(B); HARD_BRAKE_START(B)
-1.80 CLOSING_START(A,B); CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_START(A,B)
-1.05 CRITICAL_TTC_END(B,B:track_001)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A)
+0.05 STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
```

**S07/run_0_occluded** (global graph, unaligned nodes: 14)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); TRACK_APPEARED(B,B:track_001)
-5.25 STRONG_THROTTLE_START(B); CLOSING_START(A,B)
-4.60 CLOSING_START(B,B:track_001)
-4.55 STRONG_THROTTLE_START(A)
-4.35 STRONG_THROTTLE_END(A)
-4.10 CLOSING_END(A,B)
-3.95 STRONG_THROTTLE_END(B)
-3.60 CLOSING_END(B,B:track_001)
-2.45 CLOSING_START(B,B:track_001)
-2.05 BRAKE_START(B); HARD_BRAKE_START(B)
-1.80 CLOSING_START(A,B); CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_START(A,B)
-1.05 CRITICAL_TTC_END(B,B:track_001)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A)
+0.05 STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
```

**S08/run_0_crash** (global graph, unaligned nodes: 20)

```
-4.25 MOVING_START(A); MOVING_START(B)
-4.20 TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-3.10 STRONG_THROTTLE_START(B)
-2.20 TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_002)
-2.15 CRITICAL_TTC_START(A,A:track_001)
-2.10 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-2.05 TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
-1.90 CRITICAL_TTC_START(A,A:track_002); CRITICAL_TTC_START(B,A)
-1.85 STRONG_THROTTLE_END(B)
-1.55 CRITICAL_TTC_END(A,A:track_001)
-0.90 TRACK_LOST(A,A:track_002)
-0.80 CRITICAL_TTC_START(A,A:track_001)
-0.20 TRACK_LOST(B,B:track_002)
-0.15 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.30 MOVING_END(B); STOP_START(B)
+0.45 EGO_PATH_EXIT(B,A)
+0.50 CRITICAL_TTC_END(A,A:track_001)
+0.65 CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)
```

**S09/run_0_merge_conflict** (global graph)

```
-1.80 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
-1.60 TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001)
-1.00 STRONG_THROTTLE_START(B)
-0.35 EGO_PATH_ENTRY(A,B)
-0.20 STRONG_THROTTLE_END(B)
-0.15 TRACK_LOST(B,B:track_001)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.10 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TRACK_LOST(B,B:track_002)
+0.70 CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003); MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
```

**S10/run_0_rolls_through** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B)
-4.05 STRONG_THROTTLE_START(B)
-3.45 STRONG_THROTTLE_END(B)
-3.40 STOP_SIGN_DETECTED_START(A,A:sign-0)
-3.30 BRAKE_START(A); HARD_BRAKE_START(A)
-3.10 STOP_SIGN_DETECTED_END(A,A:sign-0)
-3.05 HARD_BRAKE_END(A)
-2.60 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-1.75 CRITICAL_TTC_START(B,A)
-1.45 BRAKE_END(A); TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
-0.35 EGO_PATH_ENTRY(B,A)
-0.05 EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.10 MOVING_END(B); STOP_START(B)
+0.15 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
```

**S10/run_0_stops_safely** (global graph, unaligned nodes: 25)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.90 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.55 BRAKE_START; 2.55 HARD_BRAKE_START; 3.35 MOVING_END; 3.35 STOP_START; 3.70 TRACK_APPEARED(track_001); 3.70 CLOSING_START(track_001)*; 4.25 CRITICAL_TTC_START(track_001); 5.80 EGO_PATH_ENTRY(track_001); 5.95 CRITICAL_TTC_END(track_001); 6.10 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 7.00 TRACK_LOST(track_001); 9.55 STRONG_THROTTLE_START
B: 0.00 MOVING_START*; 1.20 STRONG_THROTTLE_START; 1.80 STRONG_THROTTLE_END; 2.55 TRACK_APPEARED(track_001); 2.55 CLOSING_START(track_001)*; 4.30 CRITICAL_TTC_START(track_001); 5.50 TRACK_LOST(track_001); 7.55 STOP_SIGN_DETECTED_START(sign-1); 7.75 STOP_SIGN_DETECTED_END(sign-1)
```

**S10/run_0_stops_then_proceeds** (global graph, unaligned nodes: 50)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.75 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.55 BRAKE_START; 2.55 HARD_BRAKE_START; 3.35 MOVING_END; 3.35 STOP_START; 3.70 TRACK_APPEARED(track_001); 3.70 CLOSING_START(track_001)*; 4.25 CRITICAL_TTC_START(track_001); 5.80 EGO_PATH_ENTRY(track_001); 5.95 CRITICAL_TTC_END(track_001); 6.10 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 6.75 HARD_BRAKE_END; 6.75 BRAKE_END; 6.75 STRONG_THROTTLE_START; 7.00 TRACK_LOST(track_001); 7.10 STOP_END; 7.10 MOVING_START; 8.20 TRACK_APPEARED(track_002); 8.20 CLOSING_START(track_002)*; 8.25 STRONG_THROTTLE_END; 8.25 TRACK_APPEARED(track_003); 8.25 CLOSING_START(track_003)*; 8.30 TRACK_APPEARED(track_004); 8.30 CLOSING_START(track_004)*; 8.35 TRACK_APPEARED(track_005); 8.35 CLOSING_START(track_005)*; 8.40 TRACK_APPEARED(track_006); 8.40 CLOSING_START(track_006)*; 8.45 TRACK_APPEARED(track_007); 8.45 TRACK_APPEARED(track_008); 8.45 CLOSING_START(track_007)*; 8.45 CLOSING_START(track_008)*; 9.00 CRITICAL_TTC_START(track_003); 9.25 TRACK_LOST(track_003); 9.50 TRACK_LOST(track_002); 10.75 TRACK_LOST(track_006); 11.60 TRACK_LOST(track_007); 12.45 TRACK_LOST(track_005)
B: 0.00 MOVING_START*; 1.20 STRONG_THROTTLE_START; 1.80 STRONG_THROTTLE_END; 2.55 TRACK_APPEARED(track_001); 2.55 CLOSING_START(track_001)*; 4.30 CRITICAL_TTC_START(track_001); 5.50 TRACK_LOST(track_001); 7.60 STOP_SIGN_DETECTED_START(sign-1); 7.70 STOP_SIGN_DETECTED_END(sign-1)
```

**S11/run_0_rolls_through** (global graph)

```
-5.50 MOVING_START(A); MOVING_START(B)
-4.25 STRONG_THROTTLE_START(B)
-3.65 STRONG_THROTTLE_END(B)
-3.55 BRAKE_START(B); HARD_BRAKE_START(B)
-3.40 STOP_SIGN_DETECTED_START(B,B:sign-1)
-3.30 HARD_BRAKE_END(B)
-3.05 STOP_SIGN_DETECTED_END(B,B:sign-1)
-2.85 BRAKE_END(B)
-2.75 TRACK_APPEARED(A,B); CLOSING_START(A,B)
-2.50 STRONG_THROTTLE_START(B)
-2.25 STRONG_THROTTLE_END(B)
-1.80 CRITICAL_TTC_START(A,B)
-1.55 TRACK_APPEARED(B,A); CLOSING_START(B,A); CRITICAL_TTC_START(B,A)
-0.20 EGO_PATH_ENTRY(B,A)
-0.05 EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.25 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.55 MOVING_END(A); STOP_START(A)
```

**S11/run_0_stops_safely** (global graph, unaligned nodes: 24)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.60 TRACK_APPEARED(track_001); 2.60 CLOSING_START(track_001)*; 4.65 CRITICAL_TTC_START(track_001); 5.25 CRITICAL_TTC_END(track_001); 5.35 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 1.25 STRONG_THROTTLE_START; 1.85 STRONG_THROTTLE_END; 2.10 STOP_SIGN_DETECTED_START(sign-1); 2.35 STOP_SIGN_DETECTED_END(sign-1); 2.55 BRAKE_START; 2.55 HARD_BRAKE_START; 3.25 MOVING_END; 3.25 STOP_START; 3.50 TRACK_APPEARED(track_001); 3.50 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.75 CRITICAL_TTC_END(track_001); 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001); 7.30 TRACK_LOST(track_001); 9.55 STRONG_THROTTLE_START
```

**S11/run_0_stops_then_proceeds** (global graph, unaligned nodes: 43)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.60 TRACK_APPEARED(track_001); 2.60 CLOSING_START(track_001)*; 4.65 CRITICAL_TTC_START(track_001); 5.25 CRITICAL_TTC_END(track_001); 5.35 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 1.25 STRONG_THROTTLE_START; 1.85 STRONG_THROTTLE_END; 2.10 STOP_SIGN_DETECTED_START(sign-1); 2.40 STOP_SIGN_DETECTED_END(sign-1); 2.55 BRAKE_START; 2.55 HARD_BRAKE_START; 3.25 MOVING_END; 3.25 STOP_START; 3.50 TRACK_APPEARED(track_001); 3.50 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.75 CRITICAL_TTC_END(track_001); 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001); 6.75 HARD_BRAKE_END; 6.75 BRAKE_END; 6.75 STRONG_THROTTLE_START; 7.20 STOP_END; 7.20 MOVING_START; 7.30 TRACK_LOST(track_001); 8.40 STRONG_THROTTLE_END; 8.40 TRACK_APPEARED(track_002); 8.40 TRACK_APPEARED(track_003); 8.40 TRACK_APPEARED(track_004); 8.40 CLOSING_START(track_002)*; 8.40 CLOSING_START(track_003)*; 8.40 CLOSING_START(track_004)*; 8.45 TRACK_APPEARED(track_005); 8.45 CLOSING_START(track_005)*; 8.65 TRACK_LOST(track_005); 9.60 EGO_PATH_ENTRY(track_004); 9.70 EGO_PATH_ENTRY(track_003); 9.85 EGO_PATH_EXIT(track_004); 9.90 EGO_PATH_EXIT(track_003); 9.90 TRACK_LOST(track_002)
```

**S12/run_0_a_arrives_first** (global graph, unaligned nodes: 72)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.65 STOP_SIGN_DETECTED_START(sign-0); 2.25 STOP_SIGN_DETECTED_END(sign-0); 2.65 BRAKE_START; 2.65 HARD_BRAKE_START; 3.40 MOVING_END; 3.40 STOP_START; 6.45 HARD_BRAKE_END; 6.45 BRAKE_END; 6.45 STRONG_THROTTLE_START; 6.80 STOP_END; 6.80 MOVING_START; 7.80 STRONG_THROTTLE_END; 8.85 TRACK_APPEARED(track_001); 8.85 TRACK_APPEARED(track_002); 8.85 CLOSING_START(track_001)*; 8.85 CLOSING_START(track_002)*; 8.95 TRACK_APPEARED(track_003); 8.95 CLOSING_START(track_003)*; 9.00 TRACK_APPEARED(track_004); 9.00 CLOSING_START(track_004)*; 9.05 TRACK_APPEARED(track_005); 9.05 TRACK_APPEARED(track_007); 9.05 CLOSING_START(track_005)*; 9.05 CLOSING_START(track_007)*; 9.10 TRACK_APPEARED(track_006); 9.10 TRACK_APPEARED(track_008); 9.10 CLOSING_START(track_006)*; 9.10 CLOSING_START(track_008)*; 9.15 TRACK_APPEARED(track_009); 9.15 CLOSING_START(track_009)*; 9.20 TRACK_APPEARED(track_010); 9.20 TRACK_APPEARED(track_011); 9.20 CLOSING_START(track_010)*; 9.20 CLOSING_START(track_011)*; 9.25 TRACK_APPEARED(track_012); 9.25 CLOSING_START(track_012)*; 9.45 CRITICAL_TTC_START(track_009); 10.05 CRITICAL_TTC_START(track_004); 10.25 TRACK_LOST(track_004); 10.70 TRACK_LOST(track_009); 12.00 EGO_PATH_ENTRY(track_001); 12.25 TRACK_LOST(track_012); 12.75 TRACK_LOST(track_011); 13.35 TRACK_LOST(track_006); 14.50 TRACK_LOST(track_008); 14.65 TRACK_LOST(track_010); 15.75 TRACK_LOST(track_005); 16.30 TRACK_LOST(track_007)
B: 0.00 MOVING_START*; 1.65 STRONG_THROTTLE_START; 2.10 STRONG_THROTTLE_END; 2.10 STOP_SIGN_DETECTED_START(sign-0); 3.00 TRACK_APPEARED(track_001); 3.00 CLOSING_START(track_001)*; 4.00 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.35 HARD_BRAKE_START; 4.70 CLOSING_END(track_001); 4.70 MOVING_END; 4.70 STOP_START; 6.95 CLOSING_START(track_001); 8.50 EGO_PATH_ENTRY(track_001); 9.05 EGO_PATH_EXIT(track_001); 9.55 CRITICAL_TTC_START(track_001); 10.45 HARD_BRAKE_END; 10.45 BRAKE_END; 10.45 STRONG_THROTTLE_START; 10.85 STOP_END; 10.85 MOVING_START; 10.85 TRACK_LOST(track_001); 11.95 STRONG_THROTTLE_END
```

**S12/run_0_b_arrives_first** (global graph, unaligned nodes: 71)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.05 STOP_SIGN_DETECTED_START(sign-0); 3.00 TRACK_APPEARED(track_001); 3.00 CLOSING_START(track_001)*; 3.55 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.35 HARD_BRAKE_START; 4.70 CLOSING_END(track_001); 4.75 MOVING_END; 4.75 STOP_START; 7.00 CLOSING_START(track_001); 9.70 EGO_PATH_ENTRY(track_001); 9.85 CLOSING_END(track_001); 10.20 EGO_PATH_EXIT(track_001); 10.45 HARD_BRAKE_END; 10.45 BRAKE_END; 10.45 STRONG_THROTTLE_START; 10.80 STOP_END; 10.80 MOVING_START; 11.65 TRACK_LOST(track_001); 11.80 STRONG_THROTTLE_END; 13.10 TRACK_APPEARED(track_002); 13.10 TRACK_APPEARED(track_003); 13.10 TRACK_APPEARED(track_004); 13.10 TRACK_APPEARED(track_006); 13.10 CLOSING_START(track_002)*; 13.10 CLOSING_START(track_003)*; 13.10 CLOSING_START(track_004)*; 13.10 CLOSING_START(track_006)*; 13.25 TRACK_APPEARED(track_005); 13.25 CLOSING_START(track_005)*; 13.30 TRACK_APPEARED(track_007); 13.30 TRACK_APPEARED(track_009); 13.30 CLOSING_START(track_007)*; 13.30 CLOSING_START(track_009)*; 13.35 TRACK_APPEARED(track_008); 13.35 TRACK_APPEARED(track_010); 13.35 CLOSING_START(track_008)*; 13.35 CLOSING_START(track_010)*; 13.45 TRACK_APPEARED(track_011); 13.45 TRACK_APPEARED(track_012); 13.45 CLOSING_START(track_011)*; 13.45 CLOSING_START(track_012)*; 13.50 TRACK_APPEARED(track_013); 13.50 CLOSING_START(track_013)*; 13.80 CRITICAL_TTC_START(track_007); 14.00 TRACK_LOST(track_007); 14.40 TRACK_LOST(track_003); 15.00 EGO_PATH_ENTRY(track_006); 15.60 TRACK_LOST(track_013); 15.95 EGO_PATH_EXIT(track_006)
B: 0.00 MOVING_START*; 1.25 STRONG_THROTTLE_START; 1.85 STRONG_THROTTLE_END; 2.10 STOP_SIGN_DETECTED_START(sign-1); 2.60 STOP_SIGN_DETECTED_END(sign-1); 2.65 BRAKE_START; 2.65 HARD_BRAKE_START; 3.00 TRACK_APPEARED(track_001); 3.00 CLOSING_START(track_001)*; 3.40 MOVING_END; 3.40 STOP_START; 4.70 CLOSING_END(track_001); 6.45 HARD_BRAKE_END; 6.45 BRAKE_END; 6.45 STRONG_THROTTLE_START; 6.85 STOP_END; 6.85 MOVING_START; 7.00 CLOSING_START(track_001); 7.90 STRONG_THROTTLE_END; 8.75 TRACK_LOST(track_001)
```

**S12/run_0_b_fails_to_stop** (global graph)

```
-9.70 MOVING_START(A); MOVING_START(B)
-9.05 STOP_SIGN_DETECTED_START(A,A:sign-0)
-8.45 STRONG_THROTTLE_START(B)
-7.85 STRONG_THROTTLE_END(B)
-7.75 BRAKE_START(B); HARD_BRAKE_START(B)
-7.45 STOP_SIGN_DETECTED_END(A,A:sign-0)
-7.40 HARD_BRAKE_END(B)
-7.05 BRAKE_END(B); BRAKE_START(A); HARD_BRAKE_START(A)
-6.45 STRONG_THROTTLE_START(B)
-6.40 STRONG_THROTTLE_END(B)
-6.30 MOVING_END(A); STOP_START(A)
-6.20 STOP_SIGN_DETECTED_START(B,B:sign-1)
-4.40 STOP_SIGN_DETECTED_END(B,B:sign-1)
-2.95 TRACK_APPEARED(A,B); CLOSING_START(A,B)
-1.95 HARD_BRAKE_END(A); BRAKE_END(A); STRONG_THROTTLE_START(A)
-1.60 STOP_END(A); MOVING_START(A)
-1.55 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-1.20 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.60 STRONG_THROTTLE_END(A)
-0.10 EGO_PATH_ENTRY(B,A)
-0.05 EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_003); CLOSING_START(B,B:track_003)
+0.35 MOVING_END(B); STOP_START(B)
+0.40 CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003)
+0.45 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.50 MOVING_END(A); STOP_START(A)
```

**S12/run_0_near_simultaneous** (global graph)

```
-9.50 MOVING_START(A); MOVING_START(B)
-8.85 STOP_SIGN_DETECTED_START(A,A:sign-0)
-8.25 STRONG_THROTTLE_START(B)
-7.65 STRONG_THROTTLE_END(B)
-7.40 STOP_SIGN_DETECTED_START(B,B:sign-1)
-7.25 STOP_SIGN_DETECTED_END(A,A:sign-0)
-7.00 TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-6.95 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-6.90 STOP_SIGN_DETECTED_END(B,B:sign-1)
-6.85 BRAKE_START(A); HARD_BRAKE_START(A)
-6.75 BRAKE_START(B); HARD_BRAKE_START(B)
-6.70 TRACK_LOST(A,A:track_001)
-6.10 MOVING_END(A); STOP_START(A)
-6.00 CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
-2.55 HARD_BRAKE_END(A); HARD_BRAKE_END(B); BRAKE_END(A); BRAKE_END(B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
-2.20 STOP_END(A); MOVING_START(A); CLOSING_START(B,A)
-2.15 STOP_END(B); MOVING_START(B)
-1.25 CRITICAL_TTC_START(B,A)
-1.20 STRONG_THROTTLE_END(A)
-0.85 STRONG_THROTTLE_END(B)
-0.55 EGO_PATH_ENTRY(B,A)
-0.10 TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003)
-0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.00 COLLISION(A,B); EGO_PATH_EXIT(B,A); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(A,A:track_004)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(A,A:track_005); TRACK_APPEARED(A,A:track_006); TRACK_APPEARED(A,A:track_007); TRACK_APPEARED(A,A:track_008); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008)
+0.10 CLOSING_START(A,A:track_004); TRACK_LOST(B,A)
+0.30 TRACK_LOST(A,A:track_002)
+0.45 MOVING_END(B); STOP_START(B)
+0.50 CLOSING_END(A,A:track_005); MOVING_END(A); STOP_START(A)
+0.55 CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_008)
+2.20 STOP_SIGN_DETECTED_START(A,A:sign-1)
+2.30 STOP_SIGN_DETECTED_END(A,A:sign-1)
+4.45 STOP_SIGN_DETECTED_START(A,A:sign-4); STOP_SIGN_DETECTED_END(A,A:sign-4)
```

**S13/run_0_accelerates_into_gap** (global graph)

```
-5.65 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-4.85 BRAKE_START(B)
-4.65 TRACK_LOST(A,A:track_001)
-3.70 STRONG_THROTTLE_START(A)
-2.90 STRONG_THROTTLE_END(A); SPEED_LIMIT_EXCEEDED_START(A)
-2.30 TRACK_APPEARED(A,B); CLOSING_START(A,B)
-1.85 CRITICAL_TTC_START(A,B)
-0.40 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A); STRONG_THROTTLE_START(A); HARD_BRAKE_START(B)
+0.05 CRITICAL_TTC_END(A,B); STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
+0.15 CLOSING_END(A,B)
+0.30 TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001); CRITICAL_TTC_START(B,B:track_002)
+0.35 TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004)
+0.55 TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_005)
+0.60 TRACK_APPEARED(B,B:track_006); CLOSING_START(B,B:track_006)
+0.65 TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
+0.70 TRACK_APPEARED(B,B:track_009); CLOSING_START(B,B:track_009)
+0.75 TRACK_APPEARED(B,B:track_010); CLOSING_START(A,B); CLOSING_START(B,B:track_010); CRITICAL_TTC_START(A,B)
+0.80 TRACK_APPEARED(B,B:track_011); CLOSING_START(B,B:track_011); TRACK_LOST(B,B:track_006)
+0.85 TRACK_APPEARED(B,B:track_012); CLOSING_START(B,B:track_012)
+0.90 TRACK_APPEARED(B,B:track_013); TRACK_APPEARED(B,B:track_014); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); TRACK_LOST(B,B:track_008)
+0.95 TRACK_APPEARED(B,B:track_015); TRACK_APPEARED(B,B:track_016); EGO_PATH_ENTRY(B,B:track_001); EGO_PATH_ENTRY(B,B:track_004); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_016); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_009)
+1.00 TRACK_LOST(B,B:track_010)
+1.05 EGO_PATH_EXIT(B,B:track_004); TRACK_LOST(B,B:track_011)
+1.10 CRITICAL_TTC_END(B,B:track_002); TRACK_LOST(B,B:track_012)
+1.15 CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,B:track_003); TRACK_LOST(B,B:track_013)
+1.25 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B)
+1.30 CLOSING_END(B,B:track_016); MOVING_END(A); STOP_START(A)
+1.35 CLOSING_END(B,B:track_002)
```

**S13/run_0_cut_in** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B)
-4.45 BRAKE_START(B)
-2.40 BRAKE_START(A)
-1.60 CRITICAL_TTC_START(A,B)
-0.45 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); HARD_BRAKE_START(B)
+0.05 CLOSING_END(A,B); HARD_BRAKE_START(A)
+1.15 MOVING_END(A); STOP_START(A)
+1.20 MOVING_END(B); STOP_START(B)
```

**S13/run_0_safe_lane_change** (global graph, unaligned nodes: 10)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED(track_001); 0.00 CLOSING_START(track_001)*; 1.40 CLOSING_END(track_001); 2.55 CLOSING_START(track_001); 2.85 BRAKE_START; 5.35 EGO_PATH_ENTRY(track_001)
B: 0.00 MOVING_START*; 0.00 STRONG_THROTTLE_START*; 1.25 STRONG_THROTTLE_END
```

**S15/run_0_b_stops** (global graph, unaligned nodes: 58)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED(track_001); 0.00 CLOSING_START(track_001)*; 2.00 TRACK_APPEARED(track_002); 2.00 CLOSING_START(track_002)*; 2.00 CRITICAL_TTC_START(track_002)*; 2.45 CRITICAL_TTC_START(track_001); 3.80 TRACK_LOST(track_002); 4.45 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 1.20 STRONG_THROTTLE_START; 1.45 TRACK_APPEARED(track_001); 1.45 CLOSING_START(track_001)*; 1.80 STRONG_THROTTLE_END; 1.80 STOP_SIGN_DETECTED_START(sign-0); 1.95 TRACK_APPEARED(track_002); 1.95 CLOSING_START(track_002)*; 2.00 CRITICAL_TTC_START(track_002); 2.10 STOP_SIGN_DETECTED_END(sign-0); 2.35 CRITICAL_TTC_START(track_001); 2.55 BRAKE_START; 2.55 HARD_BRAKE_START; 2.70 CRITICAL_TTC_END(track_001); 2.85 TRACK_LOST(track_001); 3.40 MOVING_END; 3.40 STOP_START; 3.40 STOP_SIGN_DETECTED_START(sign-1); 3.70 STOP_SIGN_DETECTED_END(sign-1); 3.90 EGO_PATH_ENTRY(track_002); 3.95 TRACK_APPEARED(track_003); 3.95 CLOSING_START(track_003)*; 4.20 CRITICAL_TTC_END(track_002); 4.25 CLOSING_END(track_002); 4.40 EGO_PATH_EXIT(track_002); 4.80 STOP_SIGN_DETECTED_START(sign-2); 4.80 TRACK_LOST(track_002); 4.80 STOP_SIGN_DETECTED_END(sign-2); 5.35 CLOSING_END(track_003); 5.60 STOP_SIGN_DETECTED_START(sign-3); 5.60 STOP_SIGN_DETECTED_END(sign-3); 5.65 EGO_PATH_ENTRY(track_003); 6.45 EGO_PATH_EXIT(track_003); 6.70 STOP_SIGN_DETECTED_START(sign-4); 10.55 STRONG_THROTTLE_START
C: 0.00 MOVING_START*; 0.00 TRACK_APPEARED(track_001); 0.00 TRACK_APPEARED(track_002); 0.00 CLOSING_START(track_001)*; 0.00 CLOSING_START(track_002)*; 1.65 STRONG_THROTTLE_START; 2.10 STRONG_THROTTLE_END; 2.25 CRITICAL_TTC_START(track_002); 2.45 CRITICAL_TTC_START(track_001); 2.95 CRITICAL_TTC_END(track_002); 4.00 TRACK_LOST(track_002); 4.50 CRITICAL_TTC_END(track_001); 4.50 CLOSING_END(track_001); 4.50 TRACK_LOST(track_001)
```

**S15/run_0_deflected_into_c** (global graph, unaligned nodes: 21)

```
-3.80 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-2.60 STRONG_THROTTLE_START(B)
-2.35 TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001)
-2.00 STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.85 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-1.80 TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-1.70 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.45 CRITICAL_TTC_START(B,B:track_001)
-1.30 CRITICAL_TTC_START(A,A:track_001)
-1.05 CRITICAL_TTC_END(B,B:track_001)
-1.00 TRACK_LOST(B,B:track_001)
-0.85 BRAKE_START(B)
-0.30 BRAKE_END(B)
-0.20 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
+0.05 STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.25 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.75 STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
+0.80 EGO_PATH_ENTRY(A,A:track_001)
+0.95 COLLISION(A)
+1.15 CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
+1.25 MOVING_END(A); STOP_START(A)
+1.50 STOP_SIGN_DETECTED_START(A,A:sign-2)
+4.00 STOP_SIGN_DETECTED_END(A,A:sign-2)
+4.90 STOP_SIGN_DETECTED_START(A,A:sign-3); STOP_SIGN_DETECTED_END(A,A:sign-3)
+5.95 STOP_SIGN_DETECTED_START(A,A:sign-4)
+6.10 STOP_SIGN_DETECTED_END(A,A:sign-4)
+7.10 STOP_SIGN_DETECTED_START(A,A:sign-5)
```

**S15/run_0_single_impact** (global graph, unaligned nodes: 10)

```
-3.80 MOVING_START(A); MOVING_START(B)
-3.00 TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
-2.60 STRONG_THROTTLE_START(B)
-2.00 STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.85 TRACK_APPEARED(B,A); CLOSING_START(B,A)
-1.80 TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-1.70 STOP_SIGN_DETECTED_END(B,B:sign-0)
-0.85 BRAKE_START(B)
-0.30 BRAKE_END(B)
-0.20 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); EGO_PATH_ENTRY(A,A:track_001)
+0.05 EGO_PATH_EXIT(A,A:track_001); STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.25 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.30 EGO_PATH_ENTRY(A,A:track_001)
+0.50 EGO_PATH_EXIT(A,A:track_001)
+0.80 STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
+1.05 EGO_PATH_EXIT(B,A)
+1.70 TRACK_LOST(B,A)
+6.75 STOP_SIGN_DETECTED_START(A,A:sign-1)
+7.75 MOVING_END(A); STOP_START(A)
```

**S16/run_0_avoided** (global graph, unaligned nodes: 3)

```
-5.15 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
-4.45 STRONG_THROTTLE_START(A); CLOSING_START(B,A)
-4.40 CRITICAL_TTC_START(B,A)
-3.80 STRONG_THROTTLE_START(B)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-3.35 STRONG_THROTTLE_END(A)
-2.65 STRONG_THROTTLE_END(B)
-1.20 BRAKE_START(A)
-0.90 CLOSING_START(B,A)
-0.80 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
+0.45 MOVING_END(B); STOP_START(B)
+0.60 MOVING_END(A); STOP_START(A)
```

**S16/run_0_consequential** (global graph, unaligned nodes: 10)

```
-5.15 MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
-4.45 STRONG_THROTTLE_START(A); CLOSING_START(B,A)
-4.40 CRITICAL_TTC_START(B,A)
-3.80 STRONG_THROTTLE_START(B)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-3.35 STRONG_THROTTLE_END(A)
-2.65 STRONG_THROTTLE_END(B)
-1.20 BRAKE_START(A)
-0.90 CLOSING_START(B,A)
-0.75 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_001)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A); HARD_BRAKE_START(B)
+0.40 TRACK_APPEARED(A,A:track_003)
+0.45 CLOSING_END(A,A:track_002); MOVING_END(B); STOP_START(B)
+0.50 EGO_PATH_ENTRY(A,A:track_001); TRACK_LOST(A,A:track_002)
+0.75 COLLISION(A)
+0.85 CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001)
+0.90 MOVING_END(A); STOP_START(A)
+1.05 TRACK_LOST(A,A:track_003)
```

**S16/run_0_independent** (global graph, unaligned nodes: 20)

```
-14.10 MOVING_START(A); MOVING_START(C)
-13.60 MOVING_END(C); STOP_START(C)
-13.40 STRONG_THROTTLE_START(A)
-12.30 STRONG_THROTTLE_END(A)
-10.15 BRAKE_START(A)
-8.95 COLLISION(A)
-8.30 MOVING_END(A); STOP_START(A)
-3.15 BRAKE_END(A); STRONG_THROTTLE_START(A)
-2.95 TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,C)
-2.70 STOP_END(A); MOVING_START(A)
-2.30 CLOSING_START(A,A:track_002); CLOSING_START(A,C)
-2.15 STOP_END(C); MOVING_START(C)
-2.10 EGO_PATH_ENTRY(A,A:track_002)
-1.90 EGO_PATH_ENTRY(A,C)
-1.55 CRITICAL_TTC_START(A,C)
-1.40 STRONG_THROTTLE_END(A)
-1.35 CRITICAL_TTC_START(A,A:track_002)
-0.60 TRACK_LOST(A,A:track_002)
+0.00 COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,C); STRONG_THROTTLE_START(A); BRAKE_START(C)
+0.05 HARD_BRAKE_START(C)
+0.25 TRACK_LOST(A,C)
+0.55 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
```

