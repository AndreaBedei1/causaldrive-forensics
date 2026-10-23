# G0 reconstruction of the canonical set (final, 2026-10-23): results and error analysis

The numbers below are those of the frozen code of campaign v3.  Compared with the analysis of 2026-10-22, five
changes act in G0 (no threshold was tuned):
* **Recontact** (`c884c288`): a contact of the same pair within 2 s, the bodies never more than 1 m apart, belongs
  to the collision it follows.  S04 `a_front_pushed` now has 2 collisions, one with its recontact, instead of 3.
* **Map as supplied incident context** (`41d19dfb`): S06 recorder C used Town01's lanes and S10 recorder B none;
  both now use Town05, which changes their tracking and some of their events (below).
* **Inherited identities** (`f3fef365`): an observer's track of its own collision partner passes no identity on to
  a track lying on the observer itself after their contact (S06, below).
* **Evaluation** (`6e3883cd`, `d7e7cfc4`): wrong recorder links are counted (the verdict was never matched), and a
  collision named with the wrong participants counts as detected, not missed.  Neither changes a G0 number.
* **Scorecard definitions** (`5b8e0753`): recall over reportable collisions, recorder ghosts out of the road-user
  errors, RMSE, phantoms near and far.

Sources of the numbers:
* `results/g0_final/scorecard.{md,json}` (`scripts/g0_scorecard.py`);
* `results/g0_final/tracking_regimes.{md,json}` (`scripts/tracking_regimes.py`);
* `docs/CANONICAL_VALIDATION.md` (14 PASS, 8 WARN, 0 FAIL);
* `docs/STABILITY_AUDIT.md`.

Definitions are in the `cdf.evaluation.scorecard` docstring.

## Headline (22 runs, 95 vehicles, 26 true vehicle-vehicle collisions)

| family | result |
|---|---|
| Collisions | 26/26 detected and 26/26 with the correct participants (0 missed, 0 misattributed), 0 invented, timing error 0.00 s; one collision (S04 `a_front_pushed`, A-B) carries its recontact 0.65 s later.  All 26 are between two recorders, so these numbers measure the matching of the recorders' own collision reports (next section) |
| Completeness | 50 recorders, each represented by its own pose stream.  **45/45 road users that record nothing are observable and represented**.  **20 duplicates** (a vehicle split over 2-4 road users, S14-S19), **1 recorder ghost** (S06: C's track that slides from B onto A at their collision, left unresolved), 0 phantoms |
| Continuity | represented time over observable time, lowest per run: 0.45 (S16), 0.63 (S17), 0.68 (S12); 0.83-0.93 elsewhere |
| Position / speed of road users | median centre error 0.05-0.42 m per run, P95 0.20-1.10 m; speed median 0.02-0.07 m/s, P95 0.09-0.58 m/s.  Pooled over the runs: median 0.21 m in steady motion, 0.33 m in turns (definition below).  Recorder ghosts are not road-user estimates and are left out (S06 has no other road user) |
| Association | 0 wrong recorder links, 0 false merges; 1 missed recorder link (S06, the same track); 43 missed merges (S14-S19: conservative, identities left unresolved) |
| CRITICAL_TTC | 42/42 justified warnings arrive **before** the impact (lead time min 0.75 s, median 1.53 s).  "Justified" means the COVERAGE oracle also raises one about the partner within 8 s before the collision.  In the other (recorder, partner) cases neither the reconstruction nor the oracle warns; in most of them the recorder is the struck vehicle |
| Path intrusions (manoeuvres: EGO_PATH_ENTRY and CUT_IN starts less than 2 s apart are one manoeuvre, matched in either order and kind within 2 s) | 26 of 33 oracle manoeuvres found; 7 missed and 7 reported without an oracle counterpart.  After the ground-truth check below, none of the 7 misses is a missed hazard; 6 of the 7 extras are real but minor reconstruction errors, and the seventh is a real manoeuvre the oracle misses |
| Unconfirmed CRITICAL_TTC alarms | 2 (S14, after the contact), physically plausible (below) |

## Two different things: a detected collision and a reconstructed identity

| | what produces it | what the G0 numbers say |
|---|---|---|
| **Collision detected** | each recorder's own **impact (collision) sensor**: the time and impulse magnitude of a contact it felt, with no partner identity | 26/26 collisions detected; all are between two recorders, so both felt them |
| **Participants of a collision** | the matching of the two recorders' **impact reports** (equal and opposite impulses, bodies touching in their own pose streams).  Radar only vetoes a pairing its pre-contact view contradicts | 26/26 pairs correct, 0 invented |
| **Identity of a radar track** | the **radar** association: which track of a recorder is which other recorder (recorder link), or an anonymous road user U1, U2, ... for a vehicle that records nothing | recorder links: 0 wrong, 1 missed (S06); road users: 45/45 represented, 20 duplicates, 0 false merges |

A correct collision pair therefore does not show that radar recognised the partner.  The radar identities are judged
on their own lines of the scorecard.

## How the collisions are identified, and what 26/26 means

* **Every true contact involves two recorders.**  All 26 true vehicle-vehicle collisions of the canonical set are
  between two recording vehicles: 16 runs have two recorders, 6 have three, and no contact involves a vehicle
  that records nothing.  Each participant's own collision sensor reports the contact with its time and impulse
  magnitude, and no partner identity.  `test_sensor_ground_truth_separation` checks this on all 50 recorder files.
* **Matching** (`cdf.reconstruction.alignment`).  Two reports from different recorders count as one contact when
  three conditions hold:
  * their peak impulses agree within 10 % (equal and opposite impulses, `impulse_tolerance`);
  * the two bodies touch in their own pose streams: within `contact_consistency_m` = 1.0 m, plus 3 sigma of the
    declared pose accuracy;
  * each recorder's radar view before the contact does not contradict the candidate partner's own speed.

  Each match fixes the clock offset between the two recorders, and t_global = 0 is the strongest matched contact.
  A later contact must agree with the offsets already fixed, within `clock_tolerance_s` = 0.1 s.
* **Consequences.**
  * The participants of a contact are named from both participants' own collision sensors.  The 26/26 measures the
    matching of collision reports across recorders, not the recognition of a non-recording partner by radar.
  * The timing error of 0.00 s holds by construction, because the clocks are aligned on the matched contacts
    themselves.  The later contacts of S04, S10 and S11 must agree with the fixed offsets, and in G0 they do exactly.
  * **Limit of the dataset.**  The set does not test a contact with a vehicle that records nothing, whether one
    recorder hits a non-recorder or two non-recorders hit each other.  Such a contact has at most one collision
    report, and whether the reconstruction would attribute it from radar is not measured here.  The paper must
    state this, or new scenarios must cover it.
  * **The campaign.**  Its GNSS and radar degradations leave the collision reports unchanged.  They can act on the
    matching only through the pose-consistency gate (GNSS) and the radar approach check, and the smoke test kept
    100 % identification at every level.  The condition that tests the matching itself is the `impulse` family
    (relative impulse noise 2-20 %, already implemented).  It is not among the v3 families (decision of the
    freeze: the requested degradations are GNSS and radar; the earlier campaign studied impulse noise).
* **Repeated contacts versus distinct incidents.**  Within one recorder, a pause longer than `merge_gap_s` = 0.5 s
  separates two contact reports, and a weaker burst (< 1000 N s) within it continues the same contact (scraping,
  pushing).  Across the global graph, a contact of the same pair within 2 s, the bodies never more than 1 m apart
  in between, is a recontact of the collision it follows (`recontact_max_pause_s`, `recontact_max_separation_m`).  The
  multi-contact runs are reconstructed with every contact detected and its pair identified:
  * S04 a_front_pushed: 2 collisions, the first with a recontact (A hits B, the bodies rebound by 0.15 m, A touches
    B again 0.65 s later and pushes it; B hits C in between);
  * S04 b_rear_first: 2;
  * S10: 2;
  * S11: 2.

## Tracking by motion regime (diagnostic)

**Definition of the position error.**  For each fused road user whose true identity is pure (every track sample it
was built from lies on one true vehicle), and for every state of its fused trajectory, the error is the planar
distance between the estimated box centre and the true vehicle's position at the same simulator time.  The
simulator time is t_global mapped through the reference recorder's own clock, as in `cdf.evaluation.fusion_metrics`.
* **The true position** is CARLA's actor origin.  For the five vehicle models of the set it lies within 0.06 m of
  the bounding-box centre (Tesla Model 3 +0.029 m, Nissan Patrol -0.057 m, the others below 0.012 m; read from
  CARLA 0.9.15).  This is negligible against the errors reported.
* **The 0.21 m and 0.33 m** are medians over all such states of the 22 runs, labelled by the true vehicle's motion
  (`scripts/tracking_regimes.py`; the thresholds are diagnostic choices).
* **Recorders are excluded:** they are represented by their own pose stream.  Recorder ghosts are excluded too:
  they are association errors.

| regime | states | centre median [m] | centre P95 [m] | centre RMSE [m] | speed median [m/s] | speed P95 [m/s] |
|---|---:|---:|---:|---:|---:|---:|
| steady | 3259 | 0.205 | 0.734 | 0.416 | 0.032 | 0.308 |
| turning (yaw rate >= 5 deg/s) | 1127 | 0.325 | 1.023 | 0.514 | 0.055 | 0.314 |
| braking (>= 2 m/s2) | 1 | - | - | - | - | - |
| after the vehicle's first contact | 0 | - | - | - | - | - |
| fused from one recorder | 641 | 0.465 | 1.650 | 0.804 | 0.110 | 0.394 |
| fused from several recorders | 3746 | 0.220 | 0.671 | 0.346 | 0.032 | 0.246 |

* **Turning.**  Turning states come mostly from the S19 highway curve (404 of 1127) and from lane changes and
  swerves in S12-S17.  The S07 roundabout has no road user that records nothing.  Turning raises the median centre
  error from 0.21 m to 0.33 m and the P95 from 0.73 m to 1.02 m: larger errors, no breakdown.
* **One recorder versus several.**  Road users fused from several recorders have a median error of 0.22 m, against
  0.47 m for those seen by a single recorder.  The two groups also differ in range and geometry, so this is an
  association, not a measured effect of the number of recorders.
* **Braking and contact.**  No vehicle that records nothing brakes hard (1 state) or collides (0 states).  The
  vehicles that brake and collide are the recorders.  They are radar-tracked by the other recorders, and those
  tracks are assessed below: distance from the track point to the tracked recorder's true body (0 on or inside it),
  and speed error.

| tracked recorder's motion | samples | measured | body distance median / P95 [m] | speed error median / P95 [m/s] |
|---|---:|---:|---:|---:|
| steady | 2270 | 0.99 | 0.00 / 0.00 | 0.06 / 0.55 |
| braking (>= 2 m/s2) | 134 | 0.99 | 0.00 / 0.00 | 0.11 / 1.25 |
| turning | 355 | 0.99 | 0.00 / 0.11 | 0.13 / 0.70 |
| after its first contact, 0-3 s | 1320 | 0.99 | 0.00 / 0.00 | 0.07 / 0.48 |
| after its first contact, > 3 s | 1927 | 1.00 | 0.00 / 0.00 | 0.01 / 0.08 |

* **Through braking, turns and the collision itself** the track point stays on the tracked vehicle's body (P95
  0.11 m in turns, 0 otherwise).
* **The speed estimate lags under hard braking**: P95 1.25 m/s, against 0.55 m/s in steady motion.  This is a lag
  of the tracker's motion model during strong deceleration.  Smoothing on versus off was not compared here.
* **A point on the body is not the centre.**  The track point lies on the near side of the body, so these
  distances do not measure the centre error of the recorders' tracks.

## Semantic disagreements, checked against the ground truth

**Method.**  For each disagreement, the true geometry of the target relative to the recorder was taken from
`ground_truth/states.jsonl`, from 2 s before to 1 s after.  It comprises:
* the longitudinal and lateral offset, in the recorder's frame;
* the bumper gap;
* the lateral relative speed;
* the relative heading;
* the recorder's yaw rate.

Frames of both viewers were exported at the instant (`F:\CarlaGraph_repro_20261022\semantic_cases\`); a frame of
the S16 case was checked visually.  Times are the recorder's local time and the global time.

| run, recorder/target, time | disagreement | ground truth | verdict |
|---|---|---|---|
| S09 A/B 7.05 (t_global -0.10) | missed intrusion | B crosses A's path 0.1 s before the A-B contact | subsumed by the reconstructed collision and its warning; no forensic weight |
| S10 A/B 3.60 (-0.20) | missed intrusion | B enters A's path 0.2 s before the A-B contact | as S09 |
| S16 A/I 6.45 (-0.30) | missed intrusion | I keeps its lane 30-35 m ahead; A swerves (yaw rate -4 then +17 deg/s), so I falls in A's predicted path | oracle artefact: the recorder moves, not the target; not reporting a target manoeuvre is correct |
| S17 A/E 6.30 (-1.00), B/E 6.35 (-0.95) | missed intrusions | E keeps its lane 42 m ahead; A and B swerve in opposite directions (yaw rates up to 8 deg/s) | oracle artefacts, as S16 A/I |
| S06 C/B 3.75 (t_local) | missed intrusion | C's radar track follows B until the A-B collision (4.1 s), then slides onto A (0.2 m away) and stays on A; the reconstruction reports the entry at 4.20 s on that track | scored against the track's majority identity A it matches the oracle's C/A 4.40; B's entry therefore counts as missed.  A consequence of the track changing body at the contact, which the identity association now leaves unresolved |
| S10 B/A 2.85 (t_local) | missed intrusion | A crosses B's left-turn path from the left at 11 m/s; with B's lane-following corridor through the turn, A enters it at about 2.85 s | the reconstruction warns CRITICAL_TTC about A at 2.50 s, 1.3 s before the 3.80 s impact, and marks A in B's path only implicitly (EGO_PATH_EXIT at 4.85 s); no missed hazard |
| S13 abreast, platoon, passing A/B 6.30 (+0.10) | extra intrusion (same in the three variants) | B is abreast of A (0.6 m behind A's centre); A swerves into B's lane (yaw rate -15 then +29 deg/s) for the side contact | false intrusion of an abreast car at the moment of contact (side view of B); minor, at the contact |
| S14 A/G 11.35 (+3.60) | extra intrusion | G crosses A's lane 25 m ahead from right to left (lateral speed up to 4.8 m/s); the body enters A's corridor about 1.5-2 s earlier | real manoeuvre the oracle does not report (likely occluded in dense traffic); the reconstruction reports it 1.5-2 s late |
| S14 A/J 7.50 (-0.25) | extra intrusion | J keeps its lane 46 m ahead; A swerves before the contact (yaw rate -8 deg/s), so J sweeps across A's heading line | reconstruction false intrusion caused by the recorder's own rotation at long range |
| S16 A/G 6.50 (-0.25) | extra intrusion | G keeps its lane 32 m ahead; A swerves (-4 then +13 deg/s); the G fragment U8 is drawn about 1.5 m towards A's lane (frame checked) | as S14 A/J |
| S16 A/I 9.20 (+2.45) | extra intrusion | after its crash A is nearly stationary; I drives away 35-69 m ahead, turning left | post-contact report without forensic meaning |
| S14 A/E 10.15 (+2.40), A/P 10.45 (+2.70) | unconfirmed CRITICAL_TTC | E (10 m bumper gap) and P (1.5 m bumper gap) drift into A's lane at 1-2 m/s after the contact | physically plausible warnings; P's body reaches A's corridor about 1 s after the alarm, so the oracle does not confirm it within 2 s |
| S14 A/B 6.5 (validator WARN "true cut-in not reported") | missed CUT_IN | B is abreast of A (-1.7 to +0.1 m longitudinal offset) and steers into A's lane for the side contact | correct: no CUT_IN for cars abreast (rule of 2026-10-14); the validator's heuristic counts the side-swipe |

**Summary.**
* **Missed intrusions.**  None of the 7 is a missed hazard:
  * 2 come a few tenths of a second before a reconstructed collision;
  * 1 (S10 B/A) comes after a CRITICAL_TTC warning about the same vehicle 1.3 s before the impact;
  * 1 (S06 C/B) is the entry of B on a track that later follows A;
  * 3 are oracle artefacts.  The recorder's own swerve puts a target that keeps its lane into the recorder's
    predicted path.  This is the situation where "a vehicle that follows the road geometry must not be read as
    the author of a cut-in".
* **Extra intrusions.**  6 of the 7 are real but minor reconstruction errors, all at or around the contacts:
  * 3 are the abreast side contact of S13, one per variant;
  * 2 come from the recorder's own rotation with targets 32-46 m ahead (S14 A/J, S16 A/G);
  * 1 is post-contact (S16 A/I).

  The seventh (S14 A/G) is a real manoeuvre that the oracle misses.  The reconstruction reports it late.  The
  borderline S06 C/B extra of 2026-10-22 disappeared with the correct map.

## Main errors, by importance

1. **Duplicated road users in dense traffic.**  Runs S14, S15, S16, S17, S18 and S19 have 20 extra road users.
   * **What happens.**  A non-recording vehicle seen in separate track segments, or by two recorders without a
     confident merge, stays as two to four anonymous road users.  An example from the scorecard's
     `fragmented_vehicles`: in S14, H = U6, U8, U10, U12.
   * **Why.**  The fusion refuses uncertain merges by design (0 false merges).  The cost is completeness, not
     correctness.
   * **Weight.**  This is the largest remaining G0 error against "the correct number of vehicles".
   * **What it looks like in the viewer.**  The trajectories are split, not doubled.  The fragments of one vehicle
     follow one another in time, so the vehicle's fused box disappears and reappears under another name, e.g. S14
     H: U6, then U8, U10, U12, with gaps between them.  Two fragments of the same vehicle are shown together for
     only 2.5 s out of the 155 s these vehicles are in view:
     * S16 E: 0.4 s, 2.9 m apart;
     * S18 F: 1.4 s, 0.4 m apart;
     * S19 E: 0.5 s, 0.5 m apart;
     * S15 H: 0.2 s, 0.4 m apart.

     Each fragment is placed as accurately as any other road user.
   * **Candidate fix.**  The local experiment branch `experiment/robust-offline-association` targets it (v2: 679 ->
     761 of 1512 merges on its development set; safeguard policy left open).  It was not merged here because it
     changes the reconstruction and needs its own validation on the new canonical set.
2. **Continuity gaps.**  In S16 one road user is represented for only 45 % of its observable time; S17 and S12 are
   at 63-68 %.  These are the same fragmentations, seen as time not covered.
3. **S06: recorder A drawn twice.**  C's track `track_002#segment_2` of A was not linked to recorder A (a missed
   link).  A therefore also appears as anonymous road user U1, 1.7-1.8 m from A's true centre.  This is an
   association miss in a multidirectional crossing, not a position error, and it is visible in the RECONSTRUCTION
   viewer.
4. **Minor semantic errors at the contacts.**  These are the 7 extra intrusions above: the abreast side contact,
   the recorder's own rotation, and post-contact reports.  No missed hazard was found.

## Re-interpreting the earlier 84.8 % event figure

A single pooled event-match percentage has three flaws:
* it mixes event types of very different forensic weight: frequent types such as track appearances weigh as much
  as a collision warning;
* it counts an oracle disagreement as a reconstruction error;
* it penalises a correct manoeuvre reported with a different but equivalent event (CUT_IN versus EGO_PATH_ENTRY),
  or a few tenths of a second off.

It is no longer reported as an accuracy.  The ground-truth check above shows why: 3 of the 5 "misses" are oracle
artefacts.  The scorecard reports instead what the forensic question needs:
* whether every observable critical situation was warned before the impact (42/42);
* whether intrusions are recognised in either form;
* the list of disagreements, each checked against the ground truth.

## What to check visually (both viewers)

* **S06**: recorder ghost U1, C's track that slides from B onto A at their collision.
* **S14-S19**: duplicates and continuity gaps.
* **The disagreements in the table above**: frames in `F:\CarlaGraph_repro_20261022\semantic_cases\`.
* **S10**: the reproducible post-impact contact sequence A-C.
* **S04 b_rear_first**: the only run with a residual between repetitions (3e-5 m).

Frames of both viewers at -2, -1, 0, +1 and +3 s around the first contact of every run are in
`F:\CarlaGraph_repro_20261022\viewer_review\`.
