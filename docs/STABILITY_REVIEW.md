# Tracking, identity and semantic stability review

Review of the reconstruction at `c558d031` (the baseline) for unstable local tracks, false births, repeated
TRACK_APPEARED / TRACK_LOST, oscillating EGO_PATH, premature CUT_IN, false CRITICAL_TTC and fused-trajectory
jumps, and what was changed.  The reconstruction is offline and reads only each recorder's own logs (poses,
controls, radar, collisions); ground truth is used only by the evaluation (`scripts/stability_audit.py`,
`docs/STABILITY_AUDIT.md`, per run `reconstruction/evaluation/stability.json`).  Every number below comes from
the **same audit** applied to the baseline outputs (committed at `c558d031`) and to the outputs regenerated from
the unchanged raw recordings: a change of definition cannot pass for an improvement.

## Root causes

| symptom | root cause | where | introduced |
|---|---|---|---|
| EGO_PATH_ENTRY / EXIT alternating every 0.05-0.2 s (S08 B on A: 4.50/4.55, 4.70/4.75 ...; S10 A: 10 oscillations) | the reference path was rebuilt from the lane stretches at every timestamp, so it could flip between branches; and the occupancy was a hysteresis on a nominal box with no uncertainty: noise at the boundary created events | `road.RoadFrame.path_at` (a new path per sweep), `local.active_intervals` on `body_in_corridor` | `a48dfc27` (lane-following path) |
| two simultaneous tracks of one car (S08 B: track_002 / track_003 = A; S09) and repeated TRACK_APPEARED / LOST of one body (S06, S07, S09) | new tentative tracks were born on returns of a confirmed body's far side (a car crossing the line of sight); young tracks died when their velocity was unknown at birth; a car that stopped was dropped as static scenery; a track lost its body at an abrupt braking | `tracking.associate_returns`: birth suppression by an isotropic region, no heading prior, the slowdown gate | the FINAL tracker (`eef7d543`) |
| phantom U12 in S15 (`B:track_001#segment_3`), phantoms in S11 B | the slowdown gate let a moving track take the static returns of scenery where its body was predicted (8.3 m/s to standstill in one sweep, 100-270 wall returns) | `tracking._slowdown_gate` | FINAL (`eef7d543`) |
| S04 b_rear_first: A loses B when B bounces off C | the braking-bounded gate (first fix of the phantoms) refused B's rebound (+13.8 to -3.4 m/s in one sweep) | `tracking._manoeuvre_gate` | this review (intermediate) |
| S12: B reports A's CUT_IN at 2.75 s, before A swerves (3.65 s) | the cut-in start was the moment the lateral run was established on a lateral speed of a box whose point slid along A's side; confirmation accepted any later entry | `local.cut_in_spans`, `track_events` confirmation | `a48dfc27` |
| genuine cut-ins ending in contact not reported (S13 x3, S17) | the nominal box behind the median return sits 1-2 m short of the front of a car seen from beside, so the body was never "ahead"; the cause of an entry was the largest displacement, a coin toss when both cars move | `conflict.target_box`, `local._path_cause` | `a48dfc27` |
| false CRITICAL_TTC beside the recorder on a curve (S19: A on C abreast, 0.9 m gap, TTC 0.8 s; B on C two lanes away) | the recorder's predicted path follows its yaw rate, the target's goes straight: a car keeping its lane through a 185 m bend is extrapolated along a tangent into the recorder | `conflict._Prediction.overlaps` | original model |
| fused road users jump by 1-2 m (S15: implied accelerations 100-1190 m/s^2) | the fused state of each instant is independent: box fit when two observers or two faces, else covariance intersection of points with another reference, alternating instant to instant | `anonymous.entity_trajectory` | original fusion |
| S19: A's re-acquisitions of E never stitched | the crowd test counted B's track of E (the same car) as a confusable neighbour, its overlap with A's short tracks being below the 5-instant pair minimum | `identity.confusable_neighbours`, `rival_density` | `68b9ce2f` era |

## What changed

* **Tracker** (`tracking.py`): a heading-aware body region (velocity heading combined with the map's lane
  direction, `lane_heading_std_deg`) for birth suppression and confirmation; a lane velocity prior for new
  tracks (their Doppler along their lane); rigid-body Doppler velocity profiles; a braking-bounded manoeuvre gate
  (`max_braking_mps2`); an **impact gate** for a target hit or hitting something (moving returns on its own body,
  the measured velocity change carried as an impulse and an RTS boundary; static returns never); a stopped body
  keeps its track, scenery by history excluded; an impact kick only for a body that can touch the recorder;
  an entanglement split of two tracks that exchanged returns at a contact; survival by coasting growth.
* **Road model** (`road.py`, `common/opendrive.py`): OpenDRIVE lane pieces and a lane graph; the recorder's whole
  trajectory map-matched at once (Viterbi); one reference path per lane episode; at a junction the branch the
  recorder's own later positions take.
* **EGO_PATH** (`local.path_occupancy`): definite in / out at 1.645 sigma, two consecutive definite sweeps,
  dated at the boundary crossing; no entry at first observation, no exit for a lost track; the body bounded from
  below by its own returns (`_on_body_returns`, `_returns_bounds`); the cause of a change by counterfactuals
  (TARGET_LATERAL / RECORDER_LATERAL / MUTUAL_LATERAL / LONGITUDINAL).
* **CUT_IN**: started at the onset of the uninterrupted lateral approach (also when it began beside the
  recorder); confirmed only by an entry the target's own manoeuvre was needed for.
* **CRITICAL_TTC**: the target's prediction follows the curvature of the lane it keeps (`road.lane_curvature`).
* **Fusion**: an RTS smoother over the fused states of every road user (no smoothing across gaps, observer
  impacts or a target impact); another observer's track that agreed with a body at every shared instant under a
  separating uncertainty is that body, not a crowd or a rival.
* **Replay**: a recorder's panel in two sections, its current states and its 15 latest events newest first
  (PgUp / PgDn), each event with its age and, for a path change, its cause.

## Before / after (22 runs present in both; the same audit)

| quantity | before | after |
|---|--:|--:|
| tracks / births | 163 / 163 | 153 / 153 |
| TRACK_LOST | 90 | 75 |
| ... visibility loss (no returns on the body) | 63 | 68 |
| ... sparse returns | 5 | 4 |
| ... fragmentation (the radar kept measuring the body) | 20 | 3 |
| phantom tracks | 4 | 0 |
| duplicate tracks (seconds) | 3 (1.90 s) | 0 |
| EGO_PATH_ENTRY / EXIT | 72 / 40 | 34 / 4 |
| EGO_PATH oscillations (undone within 0.15 s) | 25 | 0 |
| CRITICAL_TTC episodes | 63 | 61 |
| closure violations (a same-pair episode during contact) | 0 | 0 |
| CUT_IN true positives / without a true cut-in / missed (10 true) | 4 / 0 / 6 | 8 / 0 / 2 |
| merges correct / false / missed (track pairs) | 59 / 0 / 31 | 58 / 0 / 32 |
| recorder links wrong / missed | 0 / 0 | 0 / 1 |
| implausible track steps (> 40 m/s^2 away from own impacts) | 3 | 2 |

The baseline's CUT_IN onset errors were +0.7 s (S02, both runs), +0.45 s and -1.2 s (S12: B's cut-in of A
1.2 s before A's swerve); after: -0.3 to +0.05 s (the earliest, S02 critical_before_cut_in at 2.00 s, lies in the
ground-truth interval in which B leaves its lane line, 1.8-2.2 s).  The two "implausible steps" left are real third-party
impacts the tracker now follows (S04: B rebounding off C; S06: A hit by B), kept sharp by the impulse boundary.

TRACK_APPEARED / TRACK_LOST, S06-S09 (tracks, losses):

| run | recorder | before | after |
|---|---|---|---|
| S06 | A | 2, fragmentation 1 | 2, none |
| S06 | B | 2, none | 2, none |
| S06 | C | 3, fragmentation 2 | 3, fragmentation 2 (the A-B crash it observes) |
| S07 | B | 2, fragmentation 1 | 1, none |
| S08 | B | 3, fragmentation 3 | 1, none |
| S09 | A | 2, fragmentation 1 | 1, none |
| S09 | B | 3, fragmentation 2 | 1, none |

EGO_PATH entries / exits / oscillations of the most affected runs: S08 8/7/12 -> 2/0/0, S10 18/16/10 -> 2/1/0,
S06 6/3/1 -> 4/0/0, S16 8/3/2 -> 4/0/0, S12 4/2/0 -> 2/0/0.

## Focused cases

* **S06** - A keeps C through its stop (a car that stops brings its echoes with it; scenery by history).  C,
  observing the A-B crash, loses both at the contact (5.15 s): the bodies touch and exchange returns; its track
  of A after the contact is split from B's (entanglement split) and left anonymous (1 missed recorder link)
  rather than asserting an identity across the contact.
* **S07** - B keeps one track of A (2 before).  The audit's ground truth counts A's merge into the roundabout as a
  cut-in (B, A, 9.25 s); A follows its own entry connector, with no lateral change relative to its lane, so by
  the definition (a lateral position change relative to the target's own lane) it is a merge: B reports A's
  EGO_PATH_ENTRY (both moving sideways) 0.15 s before the contact and CRITICAL_TTC from 6.75 s.
* **S08** - B tracks A with **one** track (three before, two of them simultaneous); one entry, no exit, no
  oscillation (12 before).
* **S09** - one track per recorder (2 and 3 before); B's entry of A (6.45 s, A crossing into B's path; ground
  truth 6.4 s) precedes their contact at 7.15 s; the exit at 7.35 s is the separation after the impact.
* **S11** - C's EGO_PATH_ENTRY into A's path is caused by A's own lateral motion after its collision with B at
  5.55 s (A deflected toward C, cause RECORDER_LATERAL; no CUT_IN): A's CRITICAL_TTC on C starts at 5.55 s and
  ends at their contact at 6.60 s.
* **S12** - B's CUT_IN of A now starts at 3.95 s (the onset of A's swerve; ground truth: lateral motion from about
  3.85 s), confirmed by A's entry into B's path at 4.55 s (ground truth 4.62 s), contact at 4.95 s.  A's CUT_IN of
  C starts at 2.30 s (ground truth 2.3 s).
* **S13 (x3)** - B's CUT_IN of A (A drifting into B's lane ahead of it) is found in every variant at its onset
  (5.30 s) with A's entry at 5.95 s (ground truth 5.87 s), before the contact at 6.20 s.  A's track of D at
  birth mixed C's returns (C is in A's lane): those returns lie a lane off D's body and no longer prove an
  occupancy (no exit / entry pair at 0.1 s).
* **S14** - the audit's "missed" cut-in (B, A, 6.5) is a sideswipe: A's front protrudes 0.05-0.17 m past B's
  front edge while overlapping B's corridor and is level with it at the contact; within the occupancy uncertainty
  no entry is definite.  B's CRITICAL_TTC on A from 7.00 s ends at the contact.  P's shallow excursion out of A's
  corridor (at most 0.38 m by ground truth, 0.30 m reconstructed) stays inside the uncertainty band: no exit /
  re-entry pair.
* **S15** - U12 is gone: no phantom (the slowdown gate is replaced; static returns are never an impact).  The
  fused trajectories no longer jump (implied accelerations mostly below 35 m/s^2), except at the recorders' own
  collision (below).  7 missed merges: re-acquisitions in the dense platoon whose true predecessor fails the
  lateral test while a neighbour passes it; the rival posterior keeps them apart rather than risk false merges.
* **S16 / S18** - no oscillation, no phantom; missed merges 10 / 5 (re-acquisitions among similar cars).
* **S17** - B's CUT_IN of A (both changing into the middle lane, A arriving ahead) from 5.35 s (ground truth
  5.3 s), the entry "both moving sideways"; terrain-occlusion losses remain visibility losses.
* **S19** - see the scenario section of the README; A reports B's cut-in on the curve from 5.50 s (ground
  truth +0.05 s), the entry at 6.30 s, CRITICAL_TTC from the cut-in to the contact at 7.50 s; no CUT_IN and no
  CRITICAL_TTC from curve following (the two false episodes of the straight target prediction removed).

## CRITICAL_TTC (S02, S03, S08, S11, S12, S13, S19)

Every episode of a colliding pair ends at that pair's first contact (S02 5.30 / 4.10, S03 4.10, S08 5.40,
S11 5.55 and 6.60, S12 4.95, S13 6.20, S19 7.50), and no same-pair episode starts during a contact (0 closure
violations).  UNSAFE_FORWARD_GAP appears only for a leader (in the path, or in a confirmed cut-in: S02, S11 B
following A, S12 A behind C after C's cut-in, S13 A following C / D, S19 A behind B after its cut-in) and stays
distinct from a collision course.  The lane-keeping null hypothesis does not delay a genuine lateral conflict:
its confirmation is offline (an entry now or later), so S12 B on A starts at 4.05 s and S13 B on A at 5.45 s,
both shortly after the onset of the target's lateral manoeuvre and before its entry.  Two episodes end with the
track lost before the contact (S11 C on A, S19 B on A going into B's rear blind zone): the state becomes
UNKNOWN, not ended.

## Known limitations

* **Missed merges** (dense S14-S19): re-acquisitions among similar cars are left as separate road users when the
  evidence does not single out the predecessor (crowd within two car widths, rival posterior below 0.95): a
  conservative choice, 0 false merges.  The replay shows each fused road user once; two boxes for one car means
  the fusion did not merge them.
* **Observer impacts**: at a recorder's own collision its recorded pose lags the jolt for about one sweep; the
  positions it measures of other road users step by up to ~1.5 m there.  The fused smoother does not smooth across
  an observer's impact, so that step stays visible (S15, S16, S19, at the contact instant).
* **Shallow intrusions**: a body whose overlap with the corridor stays within its uncertainty (about 0.4 m at
  1.645 sigma) is never definitely inside; a cut-in ending in a sideswipe with that little overlap is reported as
  CRITICAL_TTC and COLLISION, not as an entry or a cut-in.
* **A body stopped dead within one sweep** by a collision is not followed by the impact gate (static returns are
  indistinguishable from the road surface in that sweep); its track ends.
* The ground-truth CUT_IN heuristic of the audit (lane-relative lateral motion, 45 deg) counts a roundabout
  merge (S07) and a level sideswipe (S14) as cut-ins; the reconstruction's definition does not.

## Turn indicators

Recorded since this review: each recorder logs its own light state every frame (`lights.jsonl`, CARLA's
`VehicleLightState` read back, `LeftBlinker` / `RightBlinker` decoded), and the reconstruction reports
INDICATOR_LEFT / INDICATOR_RIGHT states and their START / END events at the logged frames (event definitions,
section 6b).  Three runs were re-recorded with the light log (their trajectories identical to the earlier
recordings within 0.08 m, the collisions at the same instants): S02 critical_before_cut_in (B signals its cut-in
from 0.55 s to 3.95 s; A signals left from 0.25 s to 1.45 s without changing lane), S17 (A signals from 3.95 s,
before its lane change at 4.8 s, and leaves the indicator on to the end; B changes lane unsignalled), S07 (the
roundabout driven without any signal).  The other runs have no light log: their indicator states are UNKNOWN,
never off.  Indicators are never inferred from motion, and other road users' indicators are not observable.
