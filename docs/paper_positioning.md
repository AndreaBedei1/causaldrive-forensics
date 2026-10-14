# Paper positioning

Framing, logging prerequisites against the regulations, related work, limitations and the STOP / YIELD and
depth-camera decision.  Quantitative claims come from the final experimental campaign (not yet run); the 23
canonical runs S01-S18 are the development set.  Citations: [bibliography](bibliography.md).

## Framing

The work reconstructs a multi-vehicle accident from the partial onboard recordings of the vehicles involved.
Each recording vehicle contributes its own pose stream, controls, collision reports and radars, on its own
clock; a vehicle that recorded nothing is reconstructed only from what the recorders' radars saw of it.  The
method aligns the recorders in time on the collisions they share (without one, on what they observed of each
other), associates identities between recorders, fuses the observations of road users that recorded nothing
into anonymous entities (U1, U2, ...), builds a global semantic event trace and a replay from the
reconstruction alone, and shows per vehicle when a hazard became perceivable from its onboard sensors and when
the vehicle responded (an observed vehicle response delay).  These are inputs to an expert's avoidability
analysis: the method decides neither avoidability nor liability, and a hazard perceivable by a vehicle's
sensors is not a hazard perceived by its driver.  Every quantitative claim comes from CARLA simulations (the canonical
development runs S01-S18 and the final held-out campaign) whose ground truth is used for evaluation only.

## Logging prerequisites

What each recording vehicle must log for the method, against what the regulations require (sources:
`docs/bibliography.md`, Regulatory facts, instruments R1-R9).

| Data (per vehicle, own clock) | Used for | Required by regulation? |
|---|---|---|
| Absolute pose (GNSS/INS position and heading) with a declared accuracy | common frame, recorder links, fusion of road users that recorded nothing, replay | No.  GSR Art. 6(4)(a) names the vehicle's position and tilt on the road among the EDR data, but the technical acts it relies on exclude location/positioning data (UN R160 / R169 section 1.3); the R157 DSSAD has no position; only the ADS log of fully automated vehicles stores a GPS position, per occurrence (Reg. (EU) 2022/1426, Annex II section 9.3) |
| Own motion (speed, accelerations, yaw rate) | local motion events, the conflict model | Partly: R160 pre-crash speed, longitudinal and lateral acceleration, yaw rate, -5 to 0 s at 2 Hz |
| Controls (accelerator, brake, steering) | BRAKE events, observed vehicle response delays | Partly: R160 pre-crash accelerator, service brake and steering input, -5 to 0 s at 2 Hz; R169 service brake and accelerator at 10 Hz (-20 to +10 s); US Part 563 accelerator and service brake -20 to 0 s at 10 Hz after its phase-in, only if an EDR is fitted |
| Collision reports with impulse magnitude and time | collision-anchored alignment, contact gate | Partly: R160 delta-V at 100 Hz over 0-250 ms from the event's time zero; the R157 DSSAD flags an "involvement in a detected collision" with a timestamp accurate to +-1.0 s |
| Radar detections or tracks, with mounts and fields of view | perceivability, road users that recorded nothing | No instrument requires raw or tracked perception data (Regulatory facts G.1); R157 01 series logs distances and relative speeds of other vehicles only during type-approval public-road testing (Annex 6) |
| Own footprint (bounding box) | clearances, recorder links, contact gate | Indirectly: the EDR data identify the exact type, variant and version (GSR Art. 6(4); Reg. (EU) 2022/545 Art. 4(3)), from which the dimensions follow |
| Clock | nothing common: each vehicle's own | EDR timestamps are relative to the event's time zero (pre-crash sample timing -0.1 / +1.0 s); R157 01 series section 8.4.5.3 (where national or regional law requires it) and Reg. (EU) 2022/1426 Annex II section 9.7.3 replace the DSSAD / ADS timestamps by the time difference to the EDR trigger: a regulatory precedent for anchoring time on the crash |

Rates and accuracies, from the robustness study: the campaign logs poses, controls and radar at 20 Hz;
downsampling all of them to 10 Hz costs little (core events 0.97 found again, identities 0.977), to 5 Hz
costs identities (0.975), collisions (0.864) and core events (0.90).  Production-grade radar noise (the nominal
profile) keeps every identity, collision and alignment (fused centre error 0.48 m against 0.40 m, core events
0.97); an RTK-grade pose changes nothing (0.43 m, no identity error); a consumer-grade pose (1.66 m per axis)
raises the fused centre error to 2.83 m (1.94 m with the mutual refinement), keeps 0.985 of the identities but
lets road users 1.4 m apart merge (the declared accuracy widens the gates) and, with 10 % impulse noise, matches
0.77 of the collisions with about one wrong pairing in ten draws.  With exact or RTK poses a 10 % impulse error
per report keeps every collision match (geometry-supported matching).  Recorders like the campaign's therefore go beyond
today's regulated content, in line with proposals for richer automated-vehicle data ([B19], SAE J3197 [B21],
IEEE 1616.1 [B22]).

## Related work (verified sources, `docs/bibliography.md`)

- **Accident reconstruction.**  Physics- and simulation-based reconstruction from scene evidence (PC-Crash
  [B1], Brach [B2], the Burg-Moser handbook with its avoidability chapter [B3]), EDR-based checks [B4], video
  reconstruction from a single dashcam [B6, B7], counterfactual re-simulation of reconstructed crashes [B8, B15,
  B17].  The closest precedent [B5] stores in each EDR the states of its neighbours received over V2V
  cooperative collision warning; the NTSB Tempe report [B9] built a perceivable-versus-reacted timeline from one
  vehicle's perception record.  Here the recordings of several vehicles are combined after the fact, without
  V2V, and road users that recorded nothing are reconstructed from the recorders' own perception.
- **Cooperative perception** (OPV2V [B23], V2X-Sim [B24], DAIR-V2X with its time-compensated late fusion [B25],
  V2X-ViT [B26], Where2comm [B27], CoBEVT [B28], track-level Car2X fusion [B29], alignment of shared tracks
  [B30], cooperative tracking [B31], ETSI collective perception [B32]) shares perception online, over
  communication, with synchronised or compensated clocks.  Here the fusion is offline and post hoc, without
  communication or a shared clock.
- **Track-to-track association and fusion** (correlation test [B33], common process noise [B34], estimation
  [B35], covariance intersection [B36], fusion architectures [B37], extended objects [B38, B41], asynchronous
  automotive fusion [B40], assignment [B39], CLEAR MOT [B42]): the cross-observer test here explains the faces
  both observers see with one rigid box, refuses ambiguous links, and falls back on covariance intersection.
- **Common frame and relative pose** (Umeyama [B43], ICP [B44], decentralised fusion [B45], VANET relative
  positioning [B46], consistent cooperative localisation [B47], learned pose-error correction [B48]): the
  optional mutual refinement is a point-to-face registration with the pose sources' declared accuracies as
  priors, which leaves unobservable directions alone.
- **Time synchronisation** (reference broadcasts [B49], PTP [B50], gPTP [B51], intra-vehicle timestamping
  [B52, B53], sequence alignment [B54], flashes [B55], event-based synchronisation [B56]): here the common event
  is the collision itself, with the observed trajectories as a fallback.
- **Data recorders** (EDR and DSSAD regulations R1-R9, [B18-B22]); **criticality and reaction** (TTC [B65],
  headway against TTC [B67], extended TTC [B66], a review of criticality metrics [B68], RSS [B64], the R157
  driver models [B16, B69]; reaction and response times [B10-B14]); **simulation and digital twins** (CARLA
  [B63]; digital twins for the replay [B57-B59]).

## Limitations (consolidated)

- Simulation only, no real multi-vehicle recordings: CARLA vehicle dynamics and contacts; CARLA 0.9.15's radar
  models no measurement noise, no false alarms and no range, angle or Doppler resolution, and the poses are
  exact (`docs/robustness_profiles.md`).  The robustness study quantifies noisier sensors one perturbation
  family at a time, except the combined GNSS + impulse study.  CARLA reports one impulse magnitude to both bodies of a contact, which
  makes collision matching easier than with real recorders.
- Alignment: it needs a shared collision, or observed trajectories that fix one clock offset (otherwise the
  recorder stays UNALIGNED).  Collision matching relies on the touching geometry from the pose streams and on
  the recorder's own radar view of the arriving body; with consumer-grade poses matches are lost (left
  unmatched rather than guessed); a collision-report latency costs matches; clock offsets are constant within a
  recording (no drift modelled or tested).
- Radar-only perception of road users that recorded nothing: their size is fitted only where the recorders see
  different faces (otherwise a nominal box); standing vehicles are not tracked; two cars 1.4 m apart side by
  side must be kept apart, and a merge needs evidence that discriminates them at the declared pose accuracy
  (otherwise the identities stay unresolved: false merges are worse than unresolved identities); the same car
  can be drawn as two anonymous users until the cross-observer evidence suffices; identity switches at
  contacts and short fragments leave some tracks anonymous; heavy clutter creates spurious tracks and events.
- Recorder links: a recorder's identity is exclusive per observer at each instant (two simultaneous tracks
  carry it only with same-body evidence); tracks of a recorder can stay anonymous, notably crossing targets
  whose tracked tangential velocity is poorly observed by Doppler.
- Pose errors: the mutual refinement estimates translations only (heading errors remain) and does not reduce
  the false merges of the degraded GNSS profile; the part of the pose errors common to all recorders stays in
  every absolute position.
- Event semantics: thresholds with sources where they exist and engineering assumptions elsewhere
  (`docs/event_definitions.md`); path entries and cut-ins are tested on the estimated body (recall is lower in
  the last 0.5 s before a contact, when the body enters alongside the observer at contact range); the oracle validates perception
  against the definitions, not the definitions against human judgement; the sensitivity varies one threshold
  at a time.
- Responses in the campaign are scripted: observed vehicle response delays describe the scenario logic, not
  drivers; sensor perceivability is not driver perception.
- Scope: motor vehicles only (cars and one van; no pedestrians, cyclists, motorcycles or infrastructure
  sensors); 19 canonical scenarios (23 development runs) on two CARLA maps; no LLM in the pipeline.

## STOP / YIELD and the depth camera

Out of the main paper (the default).  The camera-based STOP / YIELD detector runs on board and gives
STOP_SIGN_DETECTED / YIELD events, but the campaign has four confirmed STOP tracks, all on real signs (S08 A,
S09 A, S09 B, S10 B), and no YIELD sign on its routes (the YIELD detector is validated on the Town10HD yield
sign only): too little to evaluate rule-related events, and rule compliance is not one of the contributions.
The depth camera is recorded but used by nothing in the reconstruction (it also misses frames on the second
and third vehicle when three cameras render per tick).  Both stay in the repository, documented, as future
work.
