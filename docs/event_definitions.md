# Core event definitions

The paper's core events (`PAPER_CORE_EVENTS`, `src/cdf/reconstruction/models.py`) describe, per recorder and on
its own clock, what its own sensors established and what it did: when another road user became perceivable,
entered its path or cut in, when a conflict became critical, when it braked, when it collided.  Everything is
local to one recorder: its own odometry (`ego.jsonl`), pedals (`controls.jsonl`), collision sensor
(`collisions.jsonl`) and radar tracks.  The global trace only places these events on t_global and names their
subjects (recorders, or anonymous road users U1, U2, ...).

Every threshold is listed with its value (`configs/reconstruction.yaml`, section `semantics` unless stated)
and its justification: a published source [references at the end], or **engineering assumption** with the
reason.  A source that only gives context (a related quantity, a regulation written for another purpose) is
marked as such.  The definitions are validated in two ways (section 8): against a ground-truth event oracle
that applies them to true kinematics, and by varying each threshold one at a time.

None of these events states that a collision was avoidable, nor who is responsible: they are inputs to an
expert's analysis.  "Perceivable" always means perceivable by the vehicle's sensors, never by a driver.

## 1. COLLISION

Source: the recorder's own collision sensor (one callback per simulator step of a contact, with the impulse
magnitude; `local.collision_contacts`).  Callbacks without a missing step form a burst; a contact is one or
more bursts; one COLLISION per contact, at its first callback.

| Parameter (section `collision`) | Value | Justification |
|---|--:|---|
| `merge_gap_s` | 0.5 s | Engineering assumption: a longer pause always separates two contacts. |
| `new_impact_ratio` | 0.75 | Engineering assumption calibrated on the campaign's own recordings: a burst within the gap at >= 0.75 of the current peak is a new impact (rebounds measured <= 0.52 of the first peak, second bodies 0.85-0.93). |
| `min_impact_ratio` | 0.25 | Engineering assumption (same calibration): below, the same contact (persistent contact <= 0.25). |
| `min_new_impact_impulse` | 1000 N s | Engineering assumption: a weaker burst within the gap continues the contact (scraping, pushing). |
| `impact_acceleration_mps2` | 20 m/s^2 | Engineering assumption (about 2 g): the recorder's own velocity jump that makes a burst impact-like. |
| `reversal_angle_deg` | 90 deg | Engineering assumption: impact-like jumps further apart than this mean a strike from the other side (new contact), otherwise a rebound. |
| `undirected_impact_ratio` | 0.5 | Engineering assumption: without that evidence, a new contact from this ratio. |

Context: a regulated EDR is triggered by a velocity change of more than 8 km/h within 150 ms (UN R160
section 5.3.1) [R160]; the collision sensor here reports every contact, with an impulse magnitude.  CARLA
reports the same impulse magnitude to both bodies of a contact (`results/robustness/impulse_symmetry.md`), which
the collision-anchored alignment uses within `fusion.impulse_tolerance` = 0.10 (engineering assumption; its
robustness to impulse noise is in `results/robustness/summary.md`).  Two reports are one contact only if the two
bodies also touch at them, each from its own pose stream (`fusion.contact_consistency_m` = 1.0 m plus 3 sigma of
the declared pose accuracy; engineering assumption, against 0.06 m at most for every genuine match of the
campaign and 54 m at least for the single-vehicle contacts it rejects).

## 2. BRAKE_START / BRAKE_END

From the recorder's own brake pedal command (0-1, `local.control_events`): BRAKE_START when it reaches
`brake_onset_threshold`, BRAKE_END when it stays below it longer than the release debounce.

| Parameter | Value | Justification |
|---|--:|---|
| `brake_onset_threshold` | 0.1 | Engineering assumption: a deliberate brake application, above pedal noise. |
| release debounce (`PEDAL_RELEASE_DEBOUNCE_S`, code) | 0.2 s | Engineering assumption: a shorter release does not end the braking. |

Context: UN R160 records the service brake status in its pre-crash data (-5.0 to 0 s at 2 Hz, sample timing
accuracy -0.1/+1.0 s) [R160]; the recorders here log the pedal at the simulation rate.

## 3. TRACK_APPEARED_FRONT / _LEFT / _RIGHT and TRACK_LOST

A radar track (`tracking.build_local_tracks`) is reported once it has `tracking.min_track_frames` = 5 sweeps
with moving returns and is dated from its first measurement; TRACK_APPEARED_* is its first sample, the side
from its first bearing; TRACK_LOST its last sample when that is before the end of the recording (a track is
ended after `tracking.max_track_gap_s` = 0.5 s without a measurement).  Only moving returns (own radial
speed >= `tracking.moving_speed_mps` = 1 m/s) start tracks: a standing vehicle is not tracked.

| Parameter | Value | Justification |
|---|--:|---|
| `track_appeared_front_deg` | 5 deg | Engineering assumption: FRONT within this first bearing, else LEFT/RIGHT (no rear radar). |
| `tracking.min_track_frames` | 5 sweeps (0.25 s) | Engineering assumption (tracker design): confirmation before a track is reported. |
| `tracking.max_track_gap_s` | 0.5 s | Engineering assumption (tracker design). |
| `tracking.moving_speed_mps` | 1.0 m/s | Engineering assumption (moving-target radar tracker). |

TRACK_APPEARED is when a road user became perceivable to the recorder's radar tracker: not when it entered
the field of view (the visibility audit, `scripts/audit_radar_visibility.py`, gives both).

## 4. EGO_PATH_ENTRY / EGO_PATH_EXIT

A track is in the recorder's path when its estimated target body intersects the forward corridor beyond
the recorder's front edge. It leaves only when the whole body is outside the corridor enlarged laterally
and backward by the hysteresis (`local.track_events`, `conflict.body_in_corridor`).
A track first seen inside the corridor has no observed entry.

| Parameter | Value | Justification |
|---|--:|---|
| `path_half_width_m` | 1.5 m | Engineering assumption: half of a 3 m lane, straight ahead (no lane geometry is perceived). |
| `path_hysteresis_m` | 0.5 m | Engineering assumption: out of the path only this far beyond it. |

PATH, CUT_IN and CRITICAL_TTC use the same estimated box (`conflict.target_box`): tracked position,
velocity heading and nominal footprint. The runtime never uses the true target dimensions or pose.
The body-vs-point ablation holds tracks, target-motion semantics and reference body constant.

## 5. CUT_IN_FROM_LEFT / _RIGHT (START, END)

A target moving within `cut_in_max_heading_deg` of the path heading frozen at its first observation, at least `cut_in_min_target_speed_mps`
fast, approaching the corridor laterally at `cut_in_lateral_speed_mps` or more (beyond its velocity uncertainty)
without interruption for `cut_in_persistence_s`, having started at least `cut_in_outside_margin_m` outside the
corridor and closed at least `cut_in_min_displacement_m`, due to reach it within `cut_in_horizon_s` and with its
nominal body already within `cut_in_preentry_margin_m` of it (`local.cut_in_spans`).  The side is the side it
comes from.  END: lateral approach below `cut_in_settle_speed_mps` for `cut_in_settle_s`.  Claimed only on a
precise estimate (`max_position_std_m` = 1.0 m, `max_velocity_std_mps` = 1.0 m/s, engineering assumptions);
a sample seen past another tracked vehicle gives no evidence. Absolute target velocity is projected
into that fixed path frame; ego translation and yaw alone cannot establish a target manoeuvre.
Distance, displacement and pre-entry are estimated body-to-corridor gaps in the same fixed frame.
This is a straight-path operational definition: renewed or curved manoeuvres need a separate future model.

| Parameter | Value | Justification |
|---|--:|---|
| `cut_in_max_heading_deg` | 25 deg | Engineering assumption: same direction of travel. |
| `cut_in_min_target_speed_mps` | 2.0 m/s | Engineering assumption: a slow or standing object does not cut in. |
| `cut_in_lateral_speed_mps` | 0.3 m/s | Engineering assumption. |
| `cut_in_persistence_s` | 0.5 s | Engineering assumption.  Context: UN R157 asks an ALKS to avoid a cut-in only if the lateral movement was visible for at least 0.72 s before the lane intrusion reference point (section 5.2.5.2) [R157]; the event here is declared once the motion is established, which can be earlier. |
| `cut_in_outside_margin_m` | 0.5 m | Engineering assumption. |
| `cut_in_min_displacement_m` | 0.5 m | Engineering assumption.  Context: UN R157's performance model 1 starts risk perception when the cutting-in vehicle's centre deviates more than 0.375 m from its lane centre [R157]. |
| `cut_in_horizon_s` | 3.0 s | Engineering assumption. |
| `cut_in_preentry_margin_m` | 1.0 m | Engineering assumption: not a vehicle two lanes away. |
| `cut_in_settle_speed_mps`, `cut_in_settle_s` | 0.2 m/s, 0.3 s | Engineering assumption. |

## 6. CRITICAL_TTC_START / CRITICAL_TTC_END

`conflict.py` (module docstring) has the full model.  CRITICAL_TTC is the event's historical name; it is true
for either of two reasons, per track sample:

* PREDICTED_OVERLAP: the recorder's safety envelope (its footprint grown by the margins) and the target's box,
  both predicted over the horizon (recorder: constant speed and yaw rate; target: its velocity, its measured
  deceleration when braking), overlap, and avoiding the overlap by braking after a reaction time needs at least
  the available deceleration.  The time of the first overlap is the TTC in Hayward's sense [B65].
* UNSAFE_FORWARD_GAP: a leader (same direction, ahead, in the corridor or entering it) is closer than
  d_min = max(v_ego x t_front(v_ego), 2 m).  A time gap is not a TTC [B67]: an unsafe gap alone has no TTC.

CRITICAL_TTC_END after 0.2 s of clearly resolved samples (no collision course, or one avoided with less than
`critical_release_ratio` of the available deceleration; no imminent line-of-sight contact; the target outside
the envelope; a leader of the episode clearly gone), or at the recorder's collision with the track.

| Parameter | Value | Justification |
|---|--:|---|
| `critical_reaction_time_s` | 1.0 s | Source-informed engineering assumption: within the range of measured driver brake reaction times (on-road median about 0.9 s, 25 % above 1.2 s [B10]; about 0.70-0.75 s when expected, about 1.25 s for unexpected but common signals, about 1.5 s for surprise [B12]).  It defines the braking model of the event, not a person's reaction. |
| `critical_deceleration_mps2` | 6.0 m/s^2 | Engineering assumption: hard braking.  Context: UN R157 counts any longitudinal deceleration demand above 5.0 m/s^2 as an emergency manoeuvre of an ALKS (section 5.3.1.1) [R157]. |
| `critical_standstill_margin_m` | 1.0 m | Engineering assumption: stopping at least this far from the target. |
| `critical_lateral_margin_m` | 0.3 m | Engineering assumption: a car passing closer than this is a threat. |
| `critical_release_ratio` | 0.75 | Engineering assumption (hysteresis of the release). |
| `prediction_horizon_s`, `prediction_time_step_s` | 6.0 s, 0.05 s | Engineering assumption; the step is the radar sweep period. |
| `target_length_m` x `target_width_m` | 4.6 x 1.9 m | Engineering assumption: the radar measures no size; a mid-size car (campaign cars 4.2-5.9 x 1.8-2.2 m). |
| `target_braking_min_mps2` | 1.0 m/s^2 | Engineering assumption: a target braking at least this is predicted to keep braking to a stop. |
| `critical_min_track_age_s` | 0.5 s | Engineering assumption: a younger track's velocity is not known yet. |
| `critical_time_gap_table` | 1.0 s at 7.2 km/h ... 1.6 s at 60 km/h | Source: UN R157 minimum following time gap for M1/N1, linear between the tabulated speeds (section 5.2.3.3) [R157].  The table applies up to 60 km/h; above it the last value is held here (R157 defers to national rules).  Used as a technical reference for automated lane keeping, not as a law of human driving; the safe-distance idea follows art. 149 of the Italian Highway Code and Directive 2006/126/EC, which give no numbers. |
| `critical_min_following_distance_m` | 2.0 m | Source: UN R157, d_min never below 2 m below 2 m/s (section 5.2.3.3) [R157]. |
| `critical_forward_min_speed_mps` | 1.0 m/s | Engineering assumption: the recorder must be moving (the MOVING threshold). |
| `critical_front_lateral_margin_m`, `critical_front_lateral_speed_mps` | 1.0 m, 0.3 m/s | Engineering assumption: a leader entering the corridor from just beside it. |
| `critical_forward_release_factor` | 1.10 | Engineering assumption (hysteresis of the release). |
| `occlusion_margin_m` | 0.5 m | Engineering assumption: a track seen past another track's box grown by this gives no forward-gap evidence. |

Criticality metrics are reviewed in [B68]; responsibility-sensitive safety [B64] and the R157 performance models
[R157, B16] are alternative safe-distance and avoidance criteria that an expert could apply to the same
reconstructed kinematics.

## 7. Derived quantity: observed vehicle response delay

The worked example (`cdf.evaluation.worked_example`, S12) measures, on the recorder's own clock, the delay from
a hazard its sensors established (CUT_IN_*_START, EGO_PATH_ENTRY, CRITICAL_TTC_START) to its own first
steering command (|steer| >= 0.001 held 0.2 s) and to its heading response (|yaw rate| >= 0.5 deg/s), and BRAKE_START
plays the same role for braking.  These are **observed vehicle response delays**, never human reaction times:

* the sensors say when the hazard was perceivable by the vehicle, not when a driver perceived it.  A driver can
  perceive cues the radar does not measure (indicators, another driver's gaze, a drift that announces a lane
  change) and miss what it measures (inattention, blind spots); an automated driving system perceives through its
  own sensors and adds processing and planning time;
* in the simulated campaign the responses are scripted (S12: a trigger on the corridor clearance plus a
  scripted latency), so the delays describe the scenario logic, not a driver;
* an expert would compare such delays with perception-reaction time distributions chosen for the expectation
  level and the kinematic context [B12, B13, B11]; braking onset follows kinematic urgency rather than a fixed
  delay after a "hazard onset" [B13].  The NTSB report on the Tempe crash [B9] is the reference case of a
  perceivable-versus-reacted timeline built from a vehicle's own perception record.

## 8. Validation

**Ground-truth event oracle** (`cdf.evaluation.event_oracle`, `scripts/event_oracle.py`, privileged).  For every
recorder and every other vehicle an ideal radar track is built from ground truth (true near surface, velocity,
acceleration and size) at the recorder's sweep times and passed through the same event functions: PERFECT
(all-seeing) and COVERAGE (only where the vehicle is within one of the recorder's radar fields of view and range
with a clear line of sight), and COVERAGE_TRACKED (the same, testing the point a radar track reports -- the
median of the body's visible faces). All three ideal oracles supply the same true oriented body.
COVERAGE against PERFECT measures FOV, range and occlusion loss; reconstruction against COVERAGE
measures sensing and estimation loss. COVERAGE_TRACKED now isolates the return-point effects on
kinematic quantities, without replacing the true body by that point. The explicit point ablation is
`results/semantics/body_point_*.json`. Current precision, recall and timing are in
`results/semantics/event_oracle_*.md`, interpreted in `docs/FINAL_VALIDATION_REPORT.md`.

**One-at-a-time sensitivity** (`scripts/semantic_sensitivity.py`): each threshold of section 4-6 varied to two
alternative values, the oracle under the same definition; it reports the reconstruction's agreement with the
oracle under each value and how far the oracle's own events move (what the choice of threshold alone does to
the reference events): `results/semantics/sensitivity_*.md`.

## References

Verified against Crossref or the official texts (see the bibliography of the paper-readiness report).

- [B9] National Transportation Safety Board, "Collision Between Vehicle Controlled by Developmental Automated Driving System and Pedestrian, Tempe, Arizona, March 18, 2018," Highway Accident Report NTSB/HAR-19/03, 2019. https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf
- [B10] G. Johansson, K. Rumar, "Drivers' Brake Reaction Times," Human Factors 13(1):23-27, 1971, DOI 10.1177/001872087101300104.
- [B11] P. L. Olson, M. Sivak, "Perception-Response Time to Unexpected Roadway Hazards," Human Factors 28(1):91-96, 1986, DOI 10.1177/001872088602800110.
- [B12] M. Green, "'How Long Does It Take to Stop?' Methodological Analysis of Driver Perception-Brake Times," Transportation Human Factors 2(3):195-216, 2000, DOI 10.1207/STHF0203_1.
- [B13] G. Markkula et al., "A farewell to brake reaction times? Kinematics-dependent brake response in naturalistic rear-end emergencies," Accident Analysis & Prevention 95:209-226, 2016, DOI 10.1016/j.aap.2016.07.007.
- [B16] K. Mattas et al., "Driver models for the definition of safety requirements of automated vehicles in international regulations. Application to motorway driving conditions," Accident Analysis & Prevention 174:106743, 2022, DOI 10.1016/j.aap.2022.106743.
- [B64] S. Shalev-Shwartz, S. Shammah, A. Shashua, "On a Formal Model of Safe and Scalable Self-driving Cars," arXiv:1708.06374, 2017.
- [B65] J. C. Hayward, "Near-Miss Determination Through Use of a Scale of Danger," Highway Research Record 384, pp. 24-34, 1972. https://onlinepubs.trb.org/Onlinepubs/hrr/1972/384/384-004.pdf
- [B67] K. Vogel, "A comparison of headway and time to collision as safety indicators," Accident Analysis & Prevention 35(3):427-433, 2003, DOI 10.1016/S0001-4575(02)00022-2.
- [B68] L. Westhofen et al., "Criticality Metrics for Automated Driving: A Review and Suitability Analysis of the State of the Art," Archives of Computational Methods in Engineering 30(1):1-35, 2023, DOI 10.1007/s11831-022-09788-7.
- [R157] UN Regulation No. 157, Automated Lane Keeping Systems: original version, OJ L 82, 9.3.2021, p. 75 (ECE/TRANS/WP.29/2020/81); 01 series of amendments, ECE/TRANS/WP.29/2022/59/Rev.1.  Sections 5.2.3.3 (minimum following distance), 5.2.5.2 (cut-in), 5.3.1.1 (emergency manoeuvre), Annex 4 Appendix 3 / 01 series Annex 3 (performance models).
- [R160] UN Regulation No. 160, Event Data Recorder, 01 series, OJ L 265, 26.7.2021, p. 3 (ECE/TRANS/WP.29/2021/58).  Sections 5.3.1 (triggers), Annex 4 Table 1 (data elements and timing).
- Directive 2006/126/EC of the European Parliament and of the Council on driving licences (recast), OJ L 403, 30.12.2006; Italian Highway Code (D.Lgs. 285/1992), art. 149.
