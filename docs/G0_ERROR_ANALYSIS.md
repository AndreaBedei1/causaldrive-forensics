# G0 reconstruction on the 2026-10-22 canonical set: results and error analysis

The reconstruction code is unchanged in G0, and no threshold was changed.  The reconstruction changes of this branch
act only when the pose source is not the recorded stream:
* the measured pose in the local path (`d9c4d4e8`);
* the poses written for the viewer (`e0480b25`).

Sources of the numbers:
* `results/g0_scorecard_20261022/scorecard.{md,json}` (`scripts/g0_scorecard.py`);
* `results/g0_scorecard_20261022/tracking_regimes.{md,json}` (`scripts/tracking_regimes.py`);
* `docs/CANONICAL_VALIDATION.md`;
* `docs/STABILITY_AUDIT.md`.

Definitions are in the `cdf.evaluation.scorecard` docstring.

## Headline (22 runs, 95 vehicles, 27 true vehicle-vehicle contacts)

| family | result |
|---|---|
| Collisions | 27/27 detected, 27/27 with the correct participants, 0 invented, timing error 0.00 s.  All 27 contacts are between two recorders, so these numbers measure the matching of the recorders' own collision reports (next section) |
| Completeness | 50 recorders, each represented by its own pose stream.  **45/45 road users that record nothing are observable and represented**.  **20 duplicates** (a vehicle split over 2-4 road users, S14-S19), **1 recorder ghost** (S06), 0 phantoms |
| Continuity | represented time over observable time, lowest per run: 0.45 (S16), 0.63 (S17), 0.68 (S12); 0.83-0.93 elsewhere |
| Position / speed of road users | median centre error 0.05-0.42 m per run, P95 0.20-1.10 m; speed median 0.02-0.07 m/s, P95 0.09-0.58 m/s.  S06's 1.75 m belongs to its recorder ghost |
| Association | 0 wrong recorder links, 0 false merges; 1 missed recorder link (S06); 43 missed merges (S14-S19: conservative, identities left unresolved) |
| CRITICAL_TTC | 43/43 justified warnings arrive **before** the impact (lead time min 0.75 s, median 1.55 s).  "Justified" means the COVERAGE oracle also raises one about the partner within 8 s before the contact.  The other 11 of the 54 (recorder, partner) cases have neither a warning nor an oracle warning; in most of them the recorder is the struck vehicle |
| Path intrusions (EGO_PATH_ENTRY or CUT_IN, either order, 2 s) | 5 oracle intrusions not reported and 9 reported without an oracle counterpart.  After the ground-truth check below, none of the 5 misses has forensic weight; 7 of the 9 extras are real but minor reconstruction errors |
| Unconfirmed CRITICAL_TTC alarms | 2 (S14, after the contact), physically plausible (below) |

## How the collisions are identified, and what 27/27 means

* **Every true contact involves two recorders.**  All 27 true vehicle-vehicle contacts of the canonical set are
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
  * The participants of a contact are named from both participants' own collision sensors.  The 27/27 measures the
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
    (relative impulse noise 2-20 %, already implemented).  It is not among the v3 families: including it is a
    decision for the campaign.
* **Repeated contacts versus distinct incidents.**  A pause longer than `merge_gap_s` = 0.5 s always separates two
  contacts.  A weaker burst (< 1000 N s) within it continues the same contact (scraping, pushing).  The
  multi-contact runs are reconstructed with every contact detected and its pair identified:
  * S04 a_front_pushed: 3 contacts;
  * S04 b_rear_first: 2;
  * S10: 2;
  * S11: 2.

## Tracking by motion regime (diagnostic)

Fused road users with a pure true identity are compared with the truth at every state of their trajectory, and
each state is labelled by the true vehicle's motion at that instant (`scripts/tracking_regimes.py`; thresholds
are diagnostic choices).

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
  error from 0.21 m to 0.33 m and the P95 from 0.73 m to 1.02 m.  The Kalman filter and RTS smoother follow the
  manoeuvre with a bias but no breakdown.
* **Several recorders.**  A road user seen by several recorders is placed about twice as accurately as one seen
  by a single recorder (median 0.22 m against 0.47 m).
* **Braking and contact.**  These regimes cannot be assessed on radar-tracked vehicles in this dataset.  No vehicle
  that records nothing brakes hard (1 state) or collides (0 states).  The vehicles that brake and collide are the
  recorders, placed by their own pose streams.  Their radar tracks seen by other recorders enter the evaluation as
  recorder links (0 wrong, 1 missed), not as position errors.  This is a limit of the scenario design.

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
| S06 C/B 4.60 (+0.45) | extra intrusion | after its crash B stops 7.7 m ahead of C, centre 4.3 m to C's left, rotated 122 deg; its nearest corner is about 1 m outside C's width | borderline geometry: the reconstructed box sits up to about 1 m closer than the truth; minor reconstruction error |
| S13 abreast, platoon, passing A/B 6.30 (+0.10) | extra intrusion (same in the three variants) | B is abreast of A (0.6 m behind A's centre); A swerves into B's lane (yaw rate -15 then +29 deg/s) for the side contact | false intrusion of an abreast car at the moment of contact (side view of B); minor, at the contact |
| S14 A/G 11.35 (+3.60) | extra intrusion | G crosses A's lane 25 m ahead from right to left (lateral speed up to 4.8 m/s); the body enters A's corridor about 1.5-2 s earlier | real manoeuvre the oracle does not report (likely occluded in dense traffic); the reconstruction reports it 1.5-2 s late |
| S14 A/J 7.50 (-0.25) | extra intrusion | J keeps its lane 46 m ahead; A swerves before the contact (yaw rate -8 deg/s), so J sweeps across A's heading line | reconstruction false intrusion caused by the recorder's own rotation at long range |
| S16 A/G 6.50 (-0.25) | extra intrusion | G keeps its lane 32 m ahead; A swerves (-4 then +13 deg/s); the G fragment U8 is drawn about 1.5 m towards A's lane (frame checked) | as S14 A/J |
| S16 A/I 9.20 (+2.45) | extra intrusion | after its crash A is nearly stationary; I drives away 35-69 m ahead, turning left | post-contact report without forensic meaning |
| S14 A/E 10.15 (+2.40), A/P 10.45 (+2.70) | unconfirmed CRITICAL_TTC | E (10 m bumper gap) and P (1.5 m bumper gap) drift into A's lane at 1-2 m/s after the contact | physically plausible warnings; P's body reaches A's corridor about 1 s after the alarm, so the oracle does not confirm it within 2 s |
| S14 A/B 6.5 (validator WARN "true cut-in not reported") | missed CUT_IN | B is abreast of A (-1.7 to +0.1 m longitudinal offset) and steers into A's lane for the side contact | correct: no CUT_IN for cars abreast (rule of 2026-10-14); the validator's heuristic counts the side-swipe |

**Summary.**
* **Missed intrusions.**  None of the 5 is a missed hazard:
  * 2 come a few tenths of a second before a reconstructed collision;
  * 3 are oracle artefacts.  The recorder's own swerve puts a target that keeps its lane into the recorder's
    predicted path.  This is the situation where "a vehicle that follows the road geometry must not be read as
    the author of a cut-in".
* **Extra intrusions.**  7 of the 9 are real but minor reconstruction errors, all at or around the contacts:
  * 3 are the abreast side contact of S13, one per variant;
  * 2 come from the recorder's own rotation with targets 32-46 m ahead (S14 A/J, S16 A/G);
  * 1 is post-contact (S16 A/I);
  * 1 is borderline geometry (S06).

  The eighth (S14 A/G) is a real manoeuvre that the oracle misses.  The reconstruction reports it late.

## Main errors, by importance

1. **Duplicated road users in dense traffic.**  Runs S14, S15, S16, S17, S18 and S19 have 20 extra road users.
   * **What happens.**  A non-recording vehicle seen in separate track segments, or by two recorders without a
     confident merge, stays as two to four anonymous road users.  An example from the scorecard's
     `fragmented_vehicles`: in S14, H = U6, U8, U10, U12.
   * **Why.**  The fusion refuses uncertain merges by design (0 false merges).  The cost is completeness, not
     correctness.
   * **Weight.**  This is the largest remaining G0 error against "the correct number of vehicles".
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
* whether every observable critical situation was warned before the impact (43/43);
* whether intrusions are recognised in either form;
* the list of disagreements, each checked against the ground truth.

## What to check visually (both viewers)

* **S06**: recorder ghost U1.
* **S14-S19**: duplicates and continuity gaps.
* **The disagreements in the table above**: frames in `F:\CarlaGraph_repro_20261022\semantic_cases\`.
* **S10**: the reproducible post-impact contact sequence A-C.
* **S04 b_rear_first**: the only run with a residual between repetitions (3e-5 m).

Frames of both viewers at -2, -1, 0, +1 and +3 s around the first contact of every run are in
`F:\CarlaGraph_repro_20261022\viewer_review\`.
