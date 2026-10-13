# Recording and sensor calibration notes

Acquisition/calibration information retained from the historical campaign report at `c706e025`.
The sensor laboratory measurements are historical acquisition data, not newly simulated results.
Per-run recording metadata and acquisition_provenance.json are authoritative; in particular
the replacement canonical S02 has its own provenance, distinct from the old saved sweeps.

## 2. Sensors

### 2.1 Three body-mounted radars (no rear radar)

CARLA traces a radar's rays in a cone of half-width tan(hfov/2) x range around its axis: a horizontal FOV of 180 deg or more folds back (measured: 200 deg -> +-80 deg, 360 deg -> a vertical slice).  The 360-degree logical sensor (six co-located roof radars) is gone; each vehicle carries three physical radars on its own body, every one recorded as its own stream (vehicles/X/radar/<id>/) with its resolved mount in its metadata (``sensor_transform``).

| radar | mount (from the vehicle's own bounding box) | yaw | H FOV | V FOV | range | points/s | tick | height |
|---|---|---|---|---|---|---|---|---|
| front | front face centre, 0.05 m beyond x_max, y = box centre | 0 | 150 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |
| left | left side, mid-length (x = box centre), 0.05 m beyond y_min | -90 | 140 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |
| right | right side, mirrored | +90 | 140 deg | 20 deg | 90 m | 12000 | 0.05 s | 0.6 m |

Resolved mounts (vehicle frame, x forward, y right, metres):

| blueprint | box L x W | front | left | right |
|---|---|---|---|---|
| model3 | 4.79 x 2.16 | (2.475, 0.000) | (0.029, -1.132) | (0.029, 1.132) |
| tt | 4.18 x 1.99 | (2.140, 0.000) | (-0.000, -1.047) | (-0.000, 1.047) |
| patrol | 4.60 x 1.93 | (2.295, 0.000) | (-0.057, -1.016) | (-0.057, 1.016) |
| sprinter | 5.92 x 1.99 | (2.997, 0.004) | (-0.011, -1.040) | (-0.011, 1.048) |

Measured with a car target on the private engine (returns per sweep at 10 / 25 / 40 / 60 m, all three radars together; bearing from the recorder, + = right):

| bearing | 10 m | 25 m | 40 m | 60 m |
|---|---|---|---|---|
| 0 deg | 76 | 19 | 11 | 7 |
| 30 deg | 149 | 28 | 11 | 4 |
| 60 deg | 150 | 42 | 15 | 6 |
| 90 deg | 112 | 42 | 24 | 16 |
| 120 deg | 67 | 11 | 5 | 3 |
| 140 deg | 91 | 14 | 5 | 2 |
| -90 deg | 116 | 39 | 24 | 17 |

- Field of view, geometric (tests/test_three_radars.py): front +-46 deg at 5 m, +-61 at 10 m, +-69 at 25 m, +-73 at 80 m; sides from 33 deg (5 m) / 27 (10 m) / 22 (40 m) to 147 / 153 / 158 deg.  Bearings 30-55 deg are seen by the front radar and a side radar together from 10 m on: no gap and no discontinuity at the front -> side transition (a target passing from one to the other stays one track, tested synthetically and seen in the campaign).
- Rear blind zone (measured): a car directly behind is not seen within +-12 deg at 5 m and +-16 deg from 10 to 40 m (total 24-32 deg); for a point target the blind cone is 41-53 deg wide from 10 m on, up to 65 deg at 5 m.  A follower in the same lane is invisible to the car it follows (S01, S04, S05: B never tracks A; S11: A never tracks B).
- The radars never see their own vehicle (0 own-body returns; returns inside the footprint are dropped anyway).  Vertical FOV 20 deg: 10 deg halves the returns on cars at 40-60 m, 30 deg adds mostly road and sky returns.  12000 points/s per radar: 6000 left 4-7 returns on a car at 60 m, 24000 doubled the scenery returns without changing first detections.

### 2.2 Occlusion A -> B -> C

Lab (private engine, 864 configurations: observer A in {model3, audi.tt, sprinter}, B and C in {model3, audi.tt, nissan.patrol, sprinter}, gaps A-B 5 / 10 m, B-C 5 / 15 m, C lateral offset 0 / 0.5 / 1.0 m): body returns on C per sweep, mean over the gaps:

| B (middle) | C (hidden) | C aligned | C 0.5 m aside | C 1.0 m aside |
|---|---|---|---|---|
| model3 | model3 | 0.00 | 0.02 | 0.46 |
| model3 | tt | 0.00 | 0.02 | 0.53 |
| model3 | patrol | 0.00 | 0.02 | 0.58 |
| model3 | sprinter | 0.20 | 0.26 | 1.04 |
| tt | model3 | 0.00 | 0.06 | 0.71 |
| tt | tt | 0.00 | 0.04 | 0.59 |
| tt | patrol | 0.03 | 0.12 | 0.72 |
| tt | sprinter | 0.38 | 0.42 | 1.28 |
| patrol | model3 | 0.00 | 0.03 | 0.71 |
| patrol | tt | 0.00 | 0.01 | 0.57 |
| patrol | patrol | 0.00 | 0.07 | 0.62 |
| patrol | sprinter | 0.02 | 0.12 | 0.88 |
| sprinter | model3 | 0.00 | 0.00 | 0.26 |
| sprinter | tt | 0.00 | 0.00 | 0.30 |
| sprinter | patrol | 0.00 | 0.00 | 0.23 |
| sprinter | sprinter | 0.00 | 0.00 | 0.49 |

- Aligned behind a car or SUV, a car or SUV C returns nothing: the radar 0.6 m above the road does not look over a low car (B sedan, C sedan: 0.00).  Only a van taller than B shows its upper body (sprinter behind a model3 / audi.tt: 0.2-0.4 returns per sweep), as it physically should.
- In the recorded S05 (A model3 -> B audi.tt -> C model3): A tracks B from 0.00 s to the end and never has a track on C (tests/test_campaign_perception.py).  A received 13 returns on C's body in 4 of 274 sweeps: 3 single returns under B's floor (the ray crosses B's rear plane 0.12-0.15 m above the road) and 10 at the impact instant, A's bumper radar pressed against B.  None over B's roof, none through B; no rule hides C: occlusion is CARLA's ray casting.

### 2.3 Camera

One RGB camera per vehicle, 1280x720, 10 Hz, behind the windscreen at its top centre in front of the interior mirror, per blueprint (checked visually on every campaign blueprint with physics on; a mount further back sees the windscreen header across the horizon):

| blueprint | x | z |
|---|---|---|
| model3 | 0.50 | 1.30 |
| tt | 0.40 | 1.18 |
| patrol | 0.60 | 1.62 |
| sprinter | 1.80 | 2.10 |

FOV chosen 110 deg (tested 100 / 110 / 120 on GT replays of the campaign with the new mounts): first STOP detection at 24.1 / 24.1 / 22.4 m (S08 A), 31.2 / 30.4 / 29.5 m (S09 A), 25.6 m each (Town10HD STOP), YIELD 20.7 / 15.9 / 10.5 m; at 100 deg the plate leaves the image 0.4-0.7 m earlier than at 110 deg (lost before the stop line at the S09 junction), at 120 deg it is smaller (later first detection).  110 deg is the smallest FOV that keeps the sign until the stop.  Images are not persisted; signs are detected on board (section 4.7).

### 2.4 Recording health

- Every recorder of every run (verify_campaign): the three radars with the expected ids, FOVs, range, points/s and mounts at the box faces (+0.05 m); one sweep per tick for every radar, 0 queue drops, 0 frames without measurement, 0 missing frames; the RGB camera complete (frames = ticks / 2), 0 drops, 0 duplicates; ego.jsonl and controls.jsonl one record per tick; the recorders' collision callbacks equal the ground-truth callbacks; metadata (footprint, mounts, camera) present.  Problems: none.
- The depth camera (800x600, 20 Hz, not used by the reconstruction) misses frames on the second and third vehicle when three cameras render per tick (as in the earlier campaigns): this does not affect any output.

## 3. Scenarios

- Recording start (all runs).  CARLA spawns a vehicle in neutral; given its initial velocity directly, the automatic gearbox engaged first gear at cruising speed after the recording had started and the over-revving engine braked the car at 10-20 m/s^2 for about 0.5 s under full throttle (every non-Tesla vehicle of the 360-degree campaign: e.g. S04 C -15.8 m/s^2 at 0.75 s).  That was read as a braking target.  Now each moving vehicle is launched over 12 ticks in the gear its gearbox would hold at that speed, at a nominal cruising throttle, and its speed controller starts from that throttle; it is spawned 0.6 s x its speed back along its lane, so the recording starts with it at its scenario spawn point.  Measured: |acceleration| <= 0.45 m/s^2 in the first second for every campaign blueprint (simulation.launch_ticks / launch_throttle).
- post_impact_mode coast (A in S11, B in S04 a_front_pushed): no pedals, no steering, gearbox in neutral, and the brake held once at rest.  With the clutch engaged CARLA's zero-throttle engine braking decelerates a car at 4-7 m/s^2, several times a real car rolling off the pedals; in neutral a shunted car is carried on as it should be.
- S04 a_front_pushed: B's brake action used to expire at 5.75 s and its post-impact mode was 'drive': B drove into C under full throttle and kept pushing it for 24 s.  Now B stops 3 m short of C and holds its brake; A, following 4.5 m behind at 14 m/s, strikes it while it is still slowing (3.2 m/s) and pushes it into C.  A stationary braked car cannot be pushed in CARLA (measured: it stops the striking car dead), hence the closer following.
- S05 occluded_chain_stop (new single variant crash): A -> B -> C in one lane; C stops hard at 3.0 s (permanent stop), B stops 13.7 m short of C, A brakes late (5.3 s) and runs into B at 5.90 s.  One collision, A-B.
- S05 C and S06 C: their stop is now a permanent stop (the brake action used to expire near the end of the recording and they drove off).
- S07: both vehicles start 67-68 m (8.4 s at 8 m/s) further back along their own routes (A still on the circulating lane; the routes contain the original ones exactly), B's acceleration moved by the same time.  Collision at 10.25 s (was 1.8 s), same place and pair; first CRITICAL_TTC at 6.65 s.
- S09 near_simultaneous: braking 0.3 instead of 0.95, started earlier so that both stop at their stop lines; brake released at 4.87 / 4.73 s.  Stops (STOP_START -> STOP_END) 1.50 s (A) and 1.55 s (B); both pull away within 0.05 s; collision at 7.15 s.
- S11 consequential (rebuilt): three lanes; C, a van, drives in the left lane at 9 m/s; A moves over into the left lane behind C and slows to its speed; B follows A too closely, reacts late and runs into A at 5.55 s while A is angled across the lane line; the shunt (A from 8.2 to 11.3 m/s, coasting in neutral) carries A into the back of C at 6.60 s.  No scripted deflection; without B, A's merge ends 2.0 m behind C (checked).  A sideways knock is not used because CARLA does not carry a struck car sideways (measured: a rear-corner impact turned A by at most 7 deg and moved it 0.8 m; a sideswipe 0.3 m).
- S10 deflected_into_c keeps its scripted post-impact deflection (unchanged on request; documented in section 7).
- The two reference links were studied for geometry: their patterns (rear-end chains, junction crossings, roundabout merge, cut-in, multi-vehicle pile-up) are covered by S01-S11; the remaining elements (a lane-change dispute, removed on request; hit-and-run; weather) are not new geometries.  No scenario was added in the three-radar campaign.
- S12 unobserved_causal_vehicle (2026-10-07, re-recorded 2026-10-08, section 8): a close cut-in by a vehicle that records nothing (record: false) makes A swerve into B; A's swerve is a reactive action fired when C's box is inside A's corridor within 3 m of its front (privileged corridor_clearance trigger, ground_truth/triggers.jsonl only); without the swerve A runs into C.


### 8.1 Dynamics

- A (audi.tt, recorder) drives the middle lane at 11.8 m/s; B (nissan.patrol, recorder) drives the left lane at 12.9 m/s, starting 7.2 m behind A and catching up; C (tesla.model3, record: false) drives the right lane at 10.8 m/s, 10.4 m ahead of A (centres): A is about to pass it.
- 2.0 s: C cuts into A's lane without braking (lane shift -3.5 m commanded over 1.0 s): its lateral motion starts at 2.45 s, its left side crosses into A's lane at 2.85 s and it is centred in A's lane by 4.45 s; peak lateral acceleration 3.9 m/s^2, heading at most 13 deg off A's.
- 3.30 s: C's box is inside A's corridor (A's width + 0.3 m a side) within 3 m of A's front face (measured 2.48 m in the corridor, 2.32 m box to box): privileged corridor_clearance trigger, logged only in ground_truth/triggers.jsonl.  3.65 s: after a 0.35 s reaction A swerves left (lane shift -3.5 m over 1.0 s; 1.96 m box to box when it starts, lateral motion from 4.10 s, peak lateral acceleration 3.8 m/s^2) into B's lane.
- 4.95 s: A-B collision (A's left side against B's right front; peak impulse 1577 N*s, contact until 5.75 s); both brake to a stop side by side.  C touches nobody: closest 0.59 m to A (5.20 s), 3.13 m to B.
- 7.0 s: C accelerates to 16 m/s (speeding up from 7.15 s) and drives away in the middle lane.

### 8.2 Scene

```
          direction of travel ------------------------------------------------------>
 left   | B==>  B catches up (13 m/s) ........................ [A][B] contact 4.95 s
 middle | A==>  A swerves left from 3.65 s .............../
        |             C==> in A's lane ~2 m ahead from ~3.3 s ...... C==> 16 m/s from 7.0 s, away
 right  |      C==> (11 m/s) cuts left at 2.0 s __/
```

True positions (ground truth; forward / right of A's first pose, metres; centre of each vehicle):

| t s | moment | A forward / right @ m/s | B | C |
|---|---|---|---|---|
| 0.00 | start | -0.0 / +0.0 @ 11.9 | -7.2 / -3.5 @ 12.9 | 10.4 / +3.5 @ 10.7 |
| 2.00 | C starts its cut-in | 23.6 / +0.0 @ 11.8 | 18.6 / -3.5 @ 12.8 | 32.0 / +3.5 @ 10.8 |
| 2.85 | C's left side in A's lane | 33.7 / +0.0 @ 11.8 | 29.4 / -3.5 @ 12.8 | 41.2 / +2.8 @ 10.8 |
| 3.30 | trigger: C within 3 m in A's corridor | 39.0 / +0.0 @ 11.8 | 35.2 / -3.5 @ 12.8 | 45.9 / +1.8 @ 10.8 |
| 3.65 | A starts swerving | 43.1 / +0.0 @ 11.8 | 39.6 / -3.5 @ 12.8 | 49.7 / +1.2 @ 10.8 |
| 4.95 | A-B contact | 58.3 / -1.6 @ 12.5 | 56.3 / -3.5 @ 12.4 | 63.7 / +0.3 @ 10.9 |
| 5.20 | C closest to A | 61.4 / -1.9 @ 11.7 | 59.3 / -3.6 @ 11.5 | 66.4 / +0.2 @ 10.9 |
| 7.00 | C speeds up | 67.6 / -2.7 @ 0.0 | 64.5 / -4.2 @ 0.0 | 86.2 / +0.0 @ 11.1 |

Clearance A-C: box to box, inside A's corridor, longitudinal (C's rear - A's front, along A's initial heading) and as A's radar track of C reports it (``clearance_m`` of A:track_001, biased high: section 5.6):

| t s | moment | box gap m | in A's corridor m | longitudinal m | radar m |
|---|---|---|---|---|---|
| 1.10 | box gap first <= 5 m | 4.98 | - | 4.78 | 5.17 |
| 2.90 | box gap first <= 3 m | 3.00 | 6.82 | 2.95 | 3.15 |
| 3.30 | trigger | 2.32 | 2.31 | 2.47 | 2.51 |
| 3.65 | A's reaction starts | 1.96 | 1.96 | 2.08 | 2.20 |
| 3.65 | box gap first <= 2 m | 1.96 | 1.96 | 2.08 | 2.20 |
| 4.10 | A starts moving left | 1.54 | 1.54 | 1.62 | 1.77 |
| 4.95 | A-B contact | 0.78 | - | 0.91 | 1.06 |
| 5.20 | minimum | 0.59 | - | 0.58 | 0.85 |

### 8.3 Recorders and the non-recorder

| participant | role | data |
|---|---|---|
| A | recorder | vehicles/A: 3 radars, camera, ego, controls, collisions, signs |
| B | recorder | vehicles/B: same |
| C | record: false | no vehicles/C; the run's metadata.json lists A, B only; C is in ground_truth/ (states, controls, its collision sensor: no contact) and in ground_truth/metadata.json with record: false |

Radar visibility of C (privileged audit): A first raw return 0.00, track track_001 0.00-7.45 s; B first raw return 0.00, track track_002 0.00-5.70 s, track_003 6.40-7.00 s.  B's view of C is partly behind A (B loses it after the contact and picks it up again briefly as track_003); both see it from the first sweep.

### 8.4 Privileged counterfactuals (ground_truth/counterfactuals.json)

Same configuration on the same private engine, cameras on, into a scratch directory; only the ground-truth summary is kept in the run.  Never read by the reconstruction, never given to a model.

| run | collisions | min gap A-B m | min gap A-C m | A's swerve | A's max left departure m |
|---|---|---|---|---|---|
| factual (S12 as recorded) | A-B 4.95 s (1577 N*s) | 0.0 | 0.59 | A_evasive_swerve_left at 3.30 s | 2.71 |
| without C (--without-participant C) | none | 1.54 | - | none | 0.0 |
| C present, swerve disabled (--disable-action A_evasive_swerve_left) | A-C 5.95 s (478 N*s) | 1.51 | 0.0 | none | 0.01 |

Without C there is no swerve and no collision: C's presence is causally relevant although C touches nobody.  With C but no swerve, A runs into the back of C at 5.95 s (closing at 0.96 m/s, 478 N*s) and never touches B: A's evasion answered a real conflict, and turned a rear-end collision with C into a sideswipe with B.  C starts 10.36 m ahead of A in every run (the same launch).


## Additional recording prerequisites

## Recording start and post-impact behaviour

- Launch.  A moving vehicle is spawned `launch_ticks x dt x its speed` (0.6 s) back along its
  lane and launched over 12 ticks at its scripted initial velocity, in the gear its automatic
  gearbox would hold at that speed and at a nominal cruising throttle (0.5); its speed
  controller then starts from that throttle.  The recording starts with the vehicle at its
  scenario spawn point, cruising (|acceleration| <= 0.45 m/s^2 in the first second, every
  blueprint).  Without it CARLA engaged first gear at speed after the recording had started:
  10-20 m/s^2 of engine braking under full throttle for about 0.5 s, which looked like a
  braking target.
- `post_impact_mode: coast`: no pedals, no steering, gearbox in neutral, the brake held once
  the vehicle has come to rest.  With the clutch engaged CARLA's zero-throttle engine braking
  decelerates a car at 4-7 m/s^2, several times what a real car loses rolling off the pedals.
  `stop` (the default) brakes hard; `deflect` coasts and steers the vehicle off its line by a
  scripted offset (S10 only); `drive` keeps following the route.
- CARLA physics to keep in mind: a stationary braked vehicle that is struck does not move (it
  stops the striking car dead), so a chain push needs the struck car still rolling; a rear
  impact on a corner turns the struck car by a few degrees at most, a forward shunt carries it.

## Participants that do not record; reactive actions

- `record: false` on a participant makes it a physical vehicle that is not a recorder: it is
  spawned, drives its script, is seen by the others' radars and cameras and is in
  `ground_truth/` (states, controls, collisions; `ground_truth/metadata.json` lists every
  participant with its `record` flag), but it carries no sensor and writes nothing under
  `vehicles/`.  The run's `metadata.json` lists the recorders only.  The reconstruction can
  therefore know it only as an anonymous radar track of a recorder.
- A scripted action may have a `trigger` instead of a `t_start`: it stays armed until a
  condition on the simulator's true state holds (within `window_s`), then starts `reaction_s`
  later.  Kinds: `envelope_entry`, the target participant's box enters a corridor `ahead_m` long
  ahead of the owner's front face, as wide as the owner plus `lateral_margin_m` a side;
  `corridor_clearance`, the target's box is inside that corridor (any length) within
  `clearance_m` of the owner's front face, measured exactly box to box on the part inside the
  corridor (a close cut-in; the firing record carries the measured clearance).  This is
  scenario construction with privileged information: firings go to
  `ground_truth/triggers.jsonl` only, never to `vehicles/`.  A trigger whose target is not in
  the run never fires.
- Privileged counterfactuals of a scenario (into a scratch `--output`, never into the campaign):
  `--without-participant C` removes a participant, `--disable-action <action_id>` never plays an
  action.

```text
python scripts/run_scenario.py --scenario S12 --variant crash --output <scratch> --without-participant C
python scripts/run_scenario.py --scenario S12 --variant crash --output <scratch> --disable-action A_evasive_swerve_left
```

S12 `unobserved_causal_vehicle` (crash) uses both.  Three lanes, one direction: A (audi.tt,
12 m/s) in the middle lane, B (nissan.patrol, 13 m/s) in the left lane 7 m behind and catching
up, C (model3, `record: false`) in the right lane 10 m ahead of A and 1 m/s slower.  At 2.0 s C
cuts into A's lane without braking (lane shift -3.5 m over 1.0 s, its left side in A's lane at
2.85 s); at 3.30 s C's box is inside A's corridor 2.3 m ahead box to box (`corridor_clearance`,
3 m) and after a 0.35 s reaction A swerves left (lane shift -3.5 m over 1.0 s; 2.0 m of
clearance when it starts) into B: A-B collision at 4.95 s (peak impulse 1577 N*s).  C touches
nobody (closest 0.59 m to A, 3.1 m to B) and speeds up to 16 m/s from 7.0 s.  Without C A
never swerves and A and B never touch (closest 1.5 m); with C but the swerve disabled A runs
into the back of C at 5.95 s and never touches B: `ground_truth/counterfactuals.json`,
privileged.  
