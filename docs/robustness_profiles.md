# Robustness profiles

The robustness study (`scripts/robustness.py`, perturbations in `src/cdf/robustness/perturb.py`) measures how the reconstruction degrades when the recordings are worse than CARLA's.  Each condition perturbs a copy of a run, never the canonical raw files under `traces/`, and the unchanged reconstruction then runs on the copy.  Ground truth travels into the copy untouched and is read only by the evaluation: the reconstruction never sees it.  GNSS errors are not written into any file; they enter through the pose source handed to the reconstruction and to the replay.  Clock perturbations are constant offsets only (no drift).

Below, every parameter value is given exactly as in the code, with its justification: a published source, a value derived from one, or an engineering assumption with its reason.

## Conventions

- **Source**: the value is stated in the cited document (references at the end).
- **derived**: computed from a source value (unit conversion, median, or statistic conversion assuming zero-mean Gaussian errors), never presented as a source value.  For a circular Gaussian with per-axis sigma: CEP = 1.1774 sigma, R95 = 2.4477 sigma; in one dimension 95 % = 1.96 sigma, the factor the GPS SPS Performance Standard uses to turn 95 % values into RMS [G7].
- **engineering assumption**: no source supports the value itself; the reason follows.
- Vendor "accuracy" figures are used as Gaussian 1-sigma.  No manufacturer document reviewed says whether its figures are 1-sigma, 2-sigma or hard bounds: engineering assumption, conservative if they are 2-sigma or bounds.

## Perturbed copies

- `perturbed_copy` writes a new folder (an existing target is refused: a copy is never overwritten).  Every file it does not change is a hard link to the original (a copy where links are refused); changed files are written anew.  The source's `reconstruction/` folder is not copied.  `perturbation.json` records the condition and seed for bookkeeping; the reconstruction never reads it.
- The driver refuses `traces/` as its work folder and deletes each copy after its job unless `--keep` is given.
- The recorded ego stream is both the vehicle's own motion (odometry and IMU, used by the local reconstruction) and its absolute pose (GNSS/INS, used by the common frame).  A GNSS profile is therefore a `PerturbedPoseSource` passed as `pose_factory` to the reconstruction, the replay and the fusion evaluation; the odometry stays as recorded.
- A condition perturbs one family only, except `combined` (GNSS + collision impulse noise) and `radar_gnss_combined` (GNSS + radar).  Every random quantity has its own stream, seeded by SHA-256 from the run seed and its labels (sensor, profile, recorder, radar or axis; never the family), so no stream depends on the order of drawing, and a combined job of a given run, level and seed draws exactly the errors of the corresponding single-sensor jobs.

## Radar

Applied to every sweep of the recorder's radar (`perturb_sweeps`; columns depth, azimuth, altitude and radial velocity of CARLA's detections):

1. each detection is dropped independently with probability `p_drop`;
2. the survivors get independent zero-mean Gaussian errors: range sigma_r (result clipped at 0.1 m), azimuth sigma_az and elevation sigma_el (converted from degrees to radians), radial velocity sigma_v;
3. K ~ Poisson(lambda) false returns are appended, uniform in azimuth over the horizontal field of view, in elevation over the vertical one and in range over [1 m, maximum range], all taken from the radar's metadata.  Doppler model: each false return is, with probability 0.5, a mirror-like ghost carrying the radial velocity of a randomly chosen surviving return of the same sweep; otherwise it carries the Doppler of a static point seen from the moving recorder, v_r = -s u_x, where s is the recorder's recorded speed at the sweep time and u_x the forward component of the unit line of sight in the vehicle frame (mount yaw and pitch included).  As in CARLA, negative means approaching [R11].  If no real return survives, every false return is static-world.  False returns are not noised.

`ideal` is CARLA's native output.  CARLA 0.9.15 models no measurement noise, no SNR-dependent detection and no false alarms.  Depth and angles are exactly those of the cast ray, though the ray directions themselves are random [R11].

| Parameter | ideal | low | nominal | high |
|---|--:|--:|--:|--:|
| sigma_r, range [m] | 0 | 0.10 | 0.25 | 0.50 |
| sigma_az, azimuth [deg] | 0 | 0.1 | 0.5 | 2.0 |
| sigma_el, elevation [deg] | 0 | 0.1 | 0.5 | 2.0 |
| sigma_v, radial velocity [m/s] | 0 | 0.03 | 0.10 | 0.20 |
| p_drop, per detection | 0 | 0.05 | 0.20 | 0.40 |
| lambda, false returns per sweep (Poisson mean) | 0 | 1.0 | 3.0 | 30.0 |

How to read the levels:
- `low`: the best stated accuracies of premium sensors near boresight.
- `nominal`: typical production accuracies over a wide field of view.  Its range, azimuth and radial-velocity sigmas equal the noise that DC-Loc injected into CARLA radar [R9].  Range sits at the median of the stated accuracies; azimuth and radial velocity sit above their medians.
- `high`: the worst stated accuracies (long-range modes, field-of-view edges), with the clutter level of a T-ITS tracker on real data [R8].

| Value | Justification |
|---|---|
| sigma_r low 0.10 m | Source: ARS 408-21 near-range accuracy +-0.10 m, the best stated value [R1]; Bosch premium 0.11 m, lower end of 0.11-0.22 m [R3]. |
| sigma_r nominal 0.25 m | Source, derived: median of nine stated range accuracies (0.10-0.50 m) [R1, R2, R3, R6]; equals the UMRR-11 medium-range "< 0.25 m" [R2] and the sigma used by DC-Loc [R9]. |
| sigma_r high 0.50 m | Source: worst stated accuracy, smartmicro long-range modes "< 0.5 m" [R2]; ARS 408-21 far range +-0.40 m [R1]. |
| sigma_az low 0.1 deg | Source: ARS 408-21 far range +-0.1 deg [R1]; Bosch 0.1 deg [R3]; AUMOVIO ARS540 +-0.1 deg [R4]. |
| sigma_az nominal 0.5 deg | Source: RadarScenes 0.5 deg at boresight [R6]; UMRR-11 medium range <= 0.5 deg [R2]; DC-Loc 0.5 deg [R9].  Choosing it over the boresight median of the stated values (0.28 deg, derived) is an engineering assumption: crash geometry (cut-ins, crossings) is off boresight, where the ARS 408-21 near range states +-1 deg at +-45 deg [R1]. |
| sigma_az high 2.0 deg | Source: RadarScenes 2 deg at the +-60 deg field-of-view border [R6]; between the ARS 408-21 near-range +-1 deg (at +-45 deg) and +-5 deg (at +-60 deg) [R1]. |
| sigma_el low 0.1 deg | Source: AUMOVIO ARS540 +-0.1 deg in azimuth and elevation [R4] (Bosch states 0.2 deg [R3]). |
| sigma_el nominal 0.5 deg | Source: UMRR-11 elevation <= 0.5 deg [R2]. |
| sigma_el high 2.0 deg | Source: UMRR-96 elevation <= 2 deg [R2]. |
| sigma_v low 0.03 m/s | Source: +-0.1 km/h = 0.028 m/s (converted) for the ARS 408-21 [R1] and RadarScenes [R6]; Bosch 0.04 m/s [R3]; AUMOVIO ARS620 and SRR52x +-0.08 and +-0.07 km/h (0.022 and 0.019 m/s, converted) [R4]. |
| sigma_v nominal 0.10 m/s | Source: UMRR-11 <= 0.1 m/s [R2]; DC-Loc 0.1 m/s [R9].  Keeping it above the median stated accuracy (0.028 m/s, derived) is an engineering assumption: data-sheet values hold for point targets without tracking [R1] and exclude the Doppler spread of extended targets; 0.10 m/s is about one Doppler resolution cell (ARS 408-21 0.37 and 0.43 km/h = 0.10 and 0.12 m/s, derived [R1]; 0.087 m/s [R7]). |
| sigma_v high 0.20 m/s | Source: UMRR-96 < 0.2 m/s [R2]; Bosch velocity separability 0.17 m/s [R3]. |
| p_drop low 0.05 | Engineering assumption: residual SNR losses only (no manufacturer document reviewed states a detection probability). |
| p_drop nominal 0.20 | Source, derived: 1 - P_D with P_D = 0.8, the detection probability of a T-ITS tracker on real radar data [R8], applied per detection.  A CARLA vehicle usually returns several rays, so this is milder per object than in [R8]. |
| p_drop high 0.40 | Engineering assumption: twice nominal, motivated by P_D lowered towards the field-of-view edges [R8] and by returns per object falling from up to about 40 at 10 m to 10 at 50 m in nuScenes [R5]. |
| lambda low 1.0 | Engineering assumption: a residual false-return level (no manufacturer document reviewed states a false-alarm rate or clutter density). |
| lambda nominal 3.0 | Source, derived: about 2.3 ghost (multipath) points per frame in the Radar Ghost Dataset (about 100 k ghost points over 42 793 frames) [R7], rounded up; consistent with the 0-4 ghost points per frame of [R10] (preprint, context only).  Its scenes were chosen next to reflective surfaces, so this is an upper-end urban rate. |
| lambda high 30.0 | Source: Poisson clutter mean lambda_C = 30 per single-sensor scan [R8]; a tracker design value for real short-range radars, not a measured specification. |
| vendor accuracy as 1-sigma | Engineering assumption (see Conventions). |
| range clip at 0.1 m | Engineering assumption: keeps every noisy range positive. |
| false-return range from 1 m | Engineering assumption: no false return at the sensor face; no source gives a minimum. |
| ghost share 0.5 | Engineering assumption: false positives can carry non-zero Doppler (mirror effects, ambiguities, sidelobes [R6]; multipath ghosts [R7]); [R10] also draws ghost velocities from the current frame. |
| fallback field of view 30 x 30 deg, range 100 m | Source: CARLA 0.9.15 radar blueprint defaults `horizontal_fov` 30.0, `vertical_fov` 30.0, `range` 100 [R11]; used only if the radar metadata lacks them. |

Sweep density: CARLA casts int(points_per_second x dt) rays per sweep [R11].  At its default 1500 points/s and 20 Hz that is 75 rays, far below the hundreds of detections per cycle of real sensors (mean 819.91 per frame in [R7], up to 1,024 per cycle in [R3]).  With sweeps that sparse, lambda = 30 is a stress level.

## GNSS (pose source)

`PerturbedPoseSource` adds errors to the recorded pose of each recorder (`x`, `y`, `yaw`, `vx`, `vy` of `ego.jsonl`):

- position, per axis x and y: e(t) = b + g(t) + w(t).  Here b ~ N(0, sigma_b^2) is drawn once per run and recorder.  g is a stationary first-order Gauss-Markov process: g_k = phi g_(k-1) + sqrt(1 - phi^2) sigma_g n_k, with phi = exp(-dt/tau), g_0 ~ N(0, sigma_g^2) and n_k ~ N(0, 1).  w ~ N(0, sigma_w^2) is white noise, drawn once per receiver epoch;
- heading: the same three terms, with their own parameters in degrees;
- velocity, per axis vx and vy: white noise only;
- every term is drawn on epochs at the receiver output rate `rate_hz` and interpolated linearly at the recorded sample times.  Each recorder and each quantity has its own random stream;
- declared accuracy: like a receiver reporting its own estimate, the pose source declares sigma_pos = sqrt(sigma_b^2 + sigma_g^2 + sigma_w^2) per axis.  sigma_yaw is the same root sum of squares of the heading terms; sigma_vel is the velocity white-noise sigma.

In `ideal` every amplitude is zero.  The study's unperturbed baseline uses the recorded pose itself, which is CARLA's exact pose.  The `gnss_refined` family repeats the same draws with the mutual refinement of the pose sources enabled.

| Profile | sigma_b [m] | sigma_g [m] | tau [s] | sigma_w [m] | rate [Hz] | declared sigma_pos [m] | CEP / R95 [m], derived |
|---|--:|--:|--:|--:|--:|--:|--:|
| ideal | 0 | 0 | - | 0 | - | 0 | 0 / 0 |
| rtk | 0.010 | 0.015 | 60.0 | 0.003 | 10.0 | 0.0183 | 0.022 / 0.045 |
| consumer | 1.5 | 0.7 | 60.0 | 0.05 | 1.0 | 1.66 | 1.95 / 4.05 |
| degraded | 3.0 | 4.5 | 30.0 | 0.5 | 1.0 | 5.43 | 6.39 / 13.3 |

| Profile | yaw sigma_b [deg] | yaw sigma_g [deg] | yaw tau [s] | yaw sigma_w [deg] | declared sigma_yaw [deg] | yaw 95 % [deg], derived | sigma_vel [m/s] |
|---|--:|--:|--:|--:|--:|--:|--:|
| ideal | 0 | 0 | - | 0 | 0 | 0 | 0 |
| rtk | 0.10 | 0.15 | 30.0 | 0.05 | 0.187 | 0.37 | 0.02 |
| consumer | 0.3 | 0.9 | 10.0 | 0.3 | 0.995 | 1.95 | 0.10 |
| degraded | 0.5 | 2.8 | 5.0 | 1.0 | 3.01 | 5.91 | 0.30 |

(`-`: the code defaults have no effect at zero amplitude.)

| Value | Justification |
|---|---|
| rtk sigma_pos 0.0183 m | Source: u-blox ZED-F9P RTK 0.01 m + 1 ppm CEP with a 1 km baseline [G3], same for the ZED-F9R [G4]: sigma 0.0093 m at 1 km and 0.017 m at 10 km (derived).  The profile is thus about a ZED-F9P at 10 km, slightly conservative against reference GNSS/INS (OxTS RT3000 v4 0.010 m CEP [G6]; Septentrio mosaic-X5 0.6 cm + 0.5 ppm RMS [G5]).  Fixed RTK in open sky. |
| rtk sigma_b 0.010, sigma_g 0.015, sigma_w 0.003 m | Engineering assumption: 30 % of the variance is a run bias (base coordinates, antenna phase centre, lever arm); the rest is a slowly varying residual (differential atmosphere, multipath) plus a 3 mm per-epoch term.  The speed noise implied by 10 Hz position differences, 0.043 m/s per axis (derived), stays below the u-blox 0.05 m/s [G3]. |
| rtk rate 10 Hz | Engineering assumption: errors are drawn at a receiver output rate and interpolated, because white noise drawn at every 20 Hz tick would give speed noise far above receiver velocity specifications.  10 Hz is inside the 7-20 Hz maximum RTK output rate of the ZED-F9P [G3]. |
| rtk heading 0.187 deg (sigma_b 0.10, sigma_g 0.15, sigma_w 0.05 deg) | Source for the total: ZED-F9R dynamic heading 0.2 deg (68 % at 30 m/s) [G4].  It lies between dual-antenna moving-base RTK, 0.4 deg (ZED-F9P, 1 m baseline [G3]), and a reference INS, 0.040 deg 1-sigma (OxTS [G6]).  The split is an engineering assumption. |
| rtk sigma_vel 0.02 m/s | Engineering assumption: between OxTS 0.025 km/h RMS (0.007 m/s, derived) [G6] and mosaic-X5 3 cm/s [G5], and below ZED-F9R 0.05 m/s (68 %) [G4]. |
| consumer sigma_pos 1.66 m | Source: CEP 1.95 m (derived) matches the u-blox NEO-M9N 2.0 m CEP [G2] and the NEO-M8N with SBAS, 2.0 m CEP [G1].  R95 4.05 m (derived) is inside the C2C-CC open-sky horizontal confidence of <= 5 m (95 %) [G8]. |
| consumer sigma_b 1.5, sigma_g 0.7, sigma_w 0.05 m | Engineering assumption: 82 % of the variance is a run bias, because the dominant slow errors barely move within a run of 1-2 min.  Signal-in-space errors correlate over hours [G7], and broadcast orbit, clock and ionosphere errors change by only 5.8 cm north and 4.0 cm east RMS over 50 s [G10].  The 5 cm per-epoch term models a filtered receiver output.  The speed noise implied by 1 Hz position differences is 0.146 m/s per axis (derived), consistent with the C2C-CC 0.3 m/s (95 %) [G8]. |
| consumer heading 0.995 deg (sigma_b 0.3, sigma_g 0.9, sigma_w 0.3 deg) | Source for the total: C2C-CC heading confidence <= 2 deg (95 %) above 12.5 m/s [G8], sigma 1.02 deg (derived).  Between 1.4 and 12.5 m/s, C2C-CC allows 3 deg (sigma 1.53 deg, derived).  The u-blox 0.3 deg (50 %) holds at 30 m/s only [G1, G2].  The split is an engineering assumption. |
| consumer sigma_vel 0.10 m/s | Engineering assumption: equals the GPS SPS global average velocity accuracy, <= 0.2 m/s (95 %, any axis, signal in space) [G7], divided by 1.96 (0.102 m/s, derived).  The u-blox modules state 0.05 m/s (50 % at 30 m/s) [G1, G2]. |
| consumer and degraded rate 1 Hz | Engineering assumption: drawn at an output rate for the same reason as `rtk`; below the maximum output rates of consumer modules (NEO-M8N 5-10 Hz [G1], NEO-M9N 25 Hz [G2]). |
| degraded sigma_pos 5.43 m | Source: R95 13.3 m (derived) is at the C2C-CC city limit of <= 14 m (95 %) and above its mild-urban limit of <= 10 m [G8].  Measured urban errors can be larger: u-blox F9P single-point RMSE of 14.6-16.7 m in middle-class and deep-urban Hong Kong (2-D or 3-D not stated) [G9]. |
| degraded sigma_b 3.0, sigma_g 4.5, sigma_w 0.5 m | Engineering assumption: a larger Gauss-Markov share (69 % of the variance), because NLOS and multipath geometry changes as the vehicle moves along streets; 0.5 m per epoch. |
| degraded heading 3.01 deg (sigma_b 0.5, sigma_g 2.8, sigma_w 1.0 deg) | Source for the total: C2C-CC heading confidence 6 deg (95 %), sigma 3.06 deg (derived) [G8].  6 deg is the value of its half-open-sky, forest, mountain-valley, mild-urban and dynamic-driving scenarios.  The city and tunnel scenarios allow 12 deg (95 %), so this profile is milder than the C2C-CC city case.  The split is an engineering assumption. |
| degraded sigma_vel 0.30 m/s | Engineering assumption: about the C2C-CC city and tunnel speed confidence, 0.6 m/s (95 %), divided by 1.96 (0.31 m/s, derived) [G8]. |
| tau 60 s (rtk, consumer), 30 s (degraded) | Engineering assumption: no peer-reviewed Gauss-Markov time constant was found for the position error of a receiver on a moving road vehicle.  Static results bracket it: single-point solutions behave as first-order Gauss-Markov for cluster times of 10-400 s [G11], and static code multipath has bounding time constants of 100-1500 s [G13].  60 s is shorter than the static values, to cover moving-vehicle multipath and changes of the satellite set.  30 s because urban multipath varies with a mean period under one minute even for a static receiver [G12]. |
| yaw tau 30 s (rtk), 10 s (consumer), 5 s (degraded) | Engineering assumption: no source gives a heading-error correlation time; shorter for poorer heading sources. |

## Correlated position sensitivity and combined collision study

The verified sources [G7, G10] support slowly varying orbit, clock and atmospheric errors;
they do not establish one universal common fraction for neighbouring vehicle receivers.
`gnss_correlated` therefore sweeps rho = 0.5, 0.9, 1.0 as a declared sensitivity assumption.
For each horizontal axis:

    e_i(t) = sqrt(rho) [b_common + g_common(t)]
             + sqrt(1-rho) [b_i + g_i(t)] + w_i(t)

The bias and Gauss-Markov marginal variances stay equal to the consumer profile.
Common errors use shared absolute receiver epochs, even when recorder starts differ.
White position noise, heading and velocity remain receiver-specific and independent.
Even rho=1 retains independent white receiver noise. No universal GNSS correlation is asserted.
Heading errors still produce range-dependent relative geometry errors despite common position.

`pose_errors` measures absolute horizontal 2-D RMS error and simultaneous pairwise position-vector
error against the exact recorded pose. Common translation cancels only from the latter; it can
still displace the fused body in the absolute map. The final scatter plot relates fusion quality
to both errors. Any empirical relative-error boundary is conditional on these runs, profiles,
seeds and heading assumptions; conservative missed merges are reported separately.

`combined` runs all canonical cases at exact, RTK, consumer-independent and consumer-rho=0.9
pose quality with 10% independent impulse noise per callback, using the same seed schedule.
It reports true-contact recall, wrong pairings, unmatched true contacts and clock alignment.
Singleton unpaired collision callbacks are not wrong vehicle-vehicle matches.

## Simultaneous GNSS and radar degradation

`radar_gnss_combined` applies one GNSS profile (`rtk`, `consumer`, `degraded`, independent receivers) and one radar
profile (`low`, `nominal`, `high`) to the same perturbed copy: the radar errors are written into the copy's radar
files and the GNSS errors enter through the pose source, and the frozen reconstruction runs once on the jointly
degraded data.  All nine combinations, with the profiles above unchanged.  The radar stream of a recorder's radar
is keyed by (seed, "radar", radar profile, recorder, radar) and the GNSS streams by (seed, "gnss", GNSS profile,
recorder, axis): the same errors as the `radar` and `gnss` jobs of that run, level and seed, independent of each
other.  This pairing makes the comparison with the single-sensor conditions a paired one (per run and seed): the
report estimates the interaction I = C - R - G + B per run and gives a bootstrap interval over runs
(`scripts/campaign_report.py`).  It is kept separate from `combined`, which studies GNSS with collision impulse
noise.

## Collision reports

Final hardening uses `impulse_relative_std = 0.10` per report and
`impulse_sigma_gate = 3` with body geometry: `abs(I1-I2)/(0.10*hypot(I1,I2))`.
This configurable uncertainty budget is an engineering assumption; it is not a
specification for a real crash-impulse sensor. Contact, pre-contact approach and
clock/assignment consistency constrain the pairing. Ambiguous partners remain
unmatched. The legacy 10% relative gate applies without geometry.
The symmetry Monte Carlo report is regenerated as a diagnostic of that legacy
gate. All robustness families are rerun from the final clean analysis freeze;
see the final campaign results (`results/`).

`CollisionPerturbation` rewrites each recorder's `collisions.jsonl`.  Each callback is dropped with probability `p_drop`; its impulse is multiplied by max(0, 1 + N(0, eps^2)); its timestamp is delayed by `latency_s` if the recorder is in `latency_recorders`.  The draws are made per callback, separately for each recorder.

| Family: value | Justification |
|---|---|
| `impulse`: eps = 0.02, 0.05, 0.10, 0.20 | Engineering assumption: a sweep of the relative error of the reported impulse magnitude, from small to large; no source reviewed covers the accuracy of crash-impulse reports. |
| clamp of the factor at 0 | Engineering assumption: an impulse magnitude is never negative. |
| `latency`: 0.05, 0.10, 0.25, 0.50 s | Engineering assumption: from one to ten sample periods of the 20 Hz recordings. |
| latency on one recorder: the second in name order (none in a single-recorder run) | Engineering assumption: one recorder reports late while the others stay on time. |
| `p_drop` = 0 | Default; the study does not exercise dropped callbacks. |

## Clock offsets

Every timestamp a recorder wrote moves by that recorder's constant offset.  This covers the ego, control, collision and traffic-sign streams, the radar sweep times, and the `first_timestamp` / `last_timestamp` of its sensor metadata.  There is no drift.

| Value | Justification |
|---|---|
| recorder i (0-based, name order): round(7.31 (i + 1) (-1)^i, 2) s, i.e. +7.31, -14.62, +21.93, -29.24 s, ... | Engineering assumption: arbitrary, large offsets, different for every recorder and of alternating sign.  The recorders share no clock, so the reconstruction must align them from its own data.  The expected outcome is a global graph identical to the unperturbed one.  The evaluation checks identity because shifted raw clocks invalidate the ground-truth time mapping. |

## Downsampling

Downsampling keeps every n-th record of `ego.jsonl` and `controls.jsonl` and every n-th radar sweep.  Collision and traffic-sign events are kept in full.

| Level | Value | Justification |
|---|---|---|
| 10 Hz | n = 2 | Engineering assumption: half the 20 Hz recording rate; equals the slowest radar cycle in the sources (100 ms, the Radar Ghost Dataset radars [R7]). |
| 5 Hz | n = 4 | Engineering assumption: a stress level below every radar update rate in the sources (production cycles of 50-72 ms [R1, R2, R4]). |

## Recorder dropout

The folder `vehicles/<recorder>/` is left out of the copy.

| Level | Justification |
|---|---|
| one recorder, each in turn (runs with two or more recorders) | Engineering assumption: total loss of one participant's recording.  Core events are compared on the remaining recorders. |

## Radar outage

Every sweep of one recorder's radar whose local time (seconds since its first ego record) lies in [start, end] is removed.

| Level | Value | Justification |
|---|---|---|
| 1 s outage, each recorder in turn | [t_c - 2.0, t_c - 1.0] s, where t_c is the recorder's own first collision callback.  Without a callback, the 1 s window ends at mid-recording. | Engineering assumption: a short outage in the approach phase, placed using the recorder's own files, not ground truth. |

## Seeds and metrics

- Stochastic families (`radar`, `gnss`, `gnss_refined`, `gnss_correlated`, `combined`, `radar_gnss_combined`, `impulse`) draw seeds 0, 1, 2, ..., at least 3 and at most 8.  Seeds are added while the standard error over seeds of any pooled metric exceeds its tolerance: 0.02 for association accuracy, collision recall, event recall and the share of runs aligned; 0.05 m for the fused centre error.  These counts and tolerances are settings of the driver: engineering assumptions.
- Deterministic families (`latency`, `clock`, `downsample`, `dropout`, `outage`) run once with seed 0.  The `baseline` copy, left unchanged, must reproduce the canonical reconstruction.
- For each condition and seed, the metrics are pooled over the runs.  The summary (`results/robustness/summary.{json,md,csv}`, `figures/`) gives the mean and SD over seeds.  The metrics are:
  - association accuracy of the decided tracks;
  - true vehicle-vehicle collisions reconstructed;
  - share of runs with every recorder on the global clock;
  - core events of the unperturbed reconstruction found again, events added, and their time differences;
  - fused centre error of the anonymous road users;
  - wrong or missed recorder links, and false merges;
  - anonymous entities that are not vehicles.

## Limitations

- Radar errors are Gaussian and independent per detection.  There is no correlation between the detections of one target or between sweeps, no angle- or SNR-dependent sigma, and no heavy tail.  Misses are drawn per detection, not per object.
- There is no multipath or ghost geometry beyond the clutter model.  False returns are uniform in the field of view rather than mirror images of real targets; only their Doppler may copy a real return.  CARLA models no range, angle or Doppler resolution, so close targets never merge [R11].  lambda is fixed per sweep and does not scale with the number of rays.
- The static-world Doppler of clutter uses only the recorder's speed along its own x axis: there is no yaw-rate, lever-arm or sideslip term.
- GNSS errors are a horizontal translation and a heading error, plus an independent velocity noise.  There is no vertical error and no correlation between vehicles: each recorder has its own streams, the worst case for relative geometry.  There are no NLOS jumps, no RTK float episodes or outages, and no heading latching at low speed.  The errors are Gaussian and stationary over a run.
- The odometry and IMU used by the local reconstruction stay exact; only the absolute pose of the common frame is perturbed.
- Errors are drawn on receiver epochs and interpolated linearly, so between epochs the white terms have less variance than declared.
- The velocity noise is independent of the position error.  Differentiating the `degraded` position errors at 1 Hz would imply 1.35 m/s per axis (derived), far above the C2C-CC city speed confidence for fused states (0.6 m/s, 95 % [G8]).
- Clock offsets are constant: there is no drift and no jitter.
- The impulse noise is applied independently to each recorder's report.
- Combined degradations are limited to GNSS with collision impulse noise (`combined`) and GNSS with radar (`radar_gnss_combined`); timing, sampling and data-loss perturbations are studied one at a time.

## References

URLs accessed 2026-10-10; the titles of [G9] and [G12] from their DOIs (Crossref, 2026-10-11).

Radar:
- [R1] Continental Engineering Services, "ARS 408-21 Long Range Radar Sensor 77 GHz - Data Sheet", print ID 091018_FS_ARS_408_21_EN_HS (PDF created 2018, modified 2020; AutonomouStuff copy), https://platformselect.autonomoustuff.com/wp-content/uploads/2020/08/ARS-408-21-whitelabel.pdf
- [R2] smartmicro, "High Performance Automotive Radar" flyer, UMRR-11 Type 132 and UMRR-96 Type 153 (PDF 2020; Level Five Supplies copy), https://levelfivesupplies.com/wp-content/uploads/2019/11/smartmicro-High-Performance-Automotive-Radar-PDF.pdf
- [R3] Bosch Engineering, "Radar off-highway premium" data sheet, (c) 2024, https://www.bosch-engineering.com/media/industries/construction/bosch_engineering_ohw_premiumradar_datasheet_en_1125.pdf
- [R4] AUMOVIO (former Continental automotive business), product pages "Technical data" of the ARS540, ARS620, ARS51x and SRR52x, https://www.aumovio.com/en/solutions/driver-assistance/automated-assisted-driving/radar-technology/ars540.html (same path with ars620.html, ars51x.html, srr52x.html)
- [R5] H. Caesar et al., "nuScenes: A Multimodal Dataset for Autonomous Driving," CVPR 2020, pp. 11618-11628, DOI 10.1109/CVPR42600.2020.01164.
- [R6] O. Schumann et al., "RadarScenes: A Real-World Radar Point Cloud Data Set for Automotive Applications," IEEE FUSION 2021, pp. 1-8, DOI 10.23919/FUSION49465.2021.9627037.
- [R7] F. Kraus, N. Scheiner, W. Ritter, K. Dietmayer, "The Radar Ghost Dataset - An Evaluation of Ghost Objects in Automotive Radar Data," IEEE/RSJ IROS 2021, pp. 8570-8577, DOI 10.1109/IROS51168.2021.9636338.
- [R8] A. Scheel, K. Dietmayer, "Tracking Multiple Vehicles Using a Variational Radar Model," IEEE T-ITS 20(10):3721-3736, 2019, DOI 10.1109/TITS.2018.2879041.
- [R9] P. Gao, S. Zhang, W. Wang, C. X. Lu, "DC-Loc: Accurate Automotive Radar Based Metric Localization with Explicit Doppler Compensation," ICRA 2022, pp. 4128-4134, DOI 10.1109/ICRA46639.2022.9811561.
- [R10] M. Morales, G. Habibi, "Synthesizing and Identifying Noise Levels in Autonomous Vehicle Camera-Radar Datasets," arXiv:2505.00584, 2025 (preprint, not peer reviewed; context only), https://arxiv.org/abs/2505.00584
- [R11] CARLA 0.9.15, sensors reference (radar) and source at tag 0.9.15, https://carla.readthedocs.io/en/0.9.15/ref_sensors/#radar-sensor ; https://github.com/carla-simulator/carla/blob/0.9.15/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/Radar.cpp

GNSS:
- [G1] u-blox, "NEO-M8 - u-blox M8 concurrent GNSS modules - Data sheet", UBX-15031086, R14, 2025, https://content.u-blox.com/sites/default/files/NEO-M8-FW3_DataSheet_UBX-15031086.pdf
- [G2] u-blox, "NEO-M9N-00B - Standard precision GNSS module - Data sheet", UBX-19014285, R08, 2025, https://content.u-blox.com/sites/default/files/NEO-M9N-00B_DataSheet_UBX-19014285.pdf
- [G3] u-blox, "ZED-F9P-04B - High precision GNSS module - Data sheet", UBX-21044850, R05, 2024, https://content.u-blox.com/sites/default/files/ZED-F9P-04B_DataSheet_UBX-21044850.pdf
- [G4] u-blox, "ZED-F9R-01B - High precision sensor fusion GNSS receiver - Data sheet", UBX-19054459, R06, 2023, https://cdn.sparkfun.com/assets/d/4/3/f/4/ZED-F9R-01B_Datasheet_UBX-19054459.pdf
- [G5] Septentrio, "mosaic-X5 - Compact, multi-constellation GNSS receiver", product brochure, 2019 (third-party mirror), https://components101.com/sites/default/files/2020-09/Mosaic-X5-Datasheet.pdf
- [G6] OxTS, "RT3000 v4 DATASHEET" (no version or date printed; distributor copy), https://positics.fr/wp-content/uploads/2024/02/RT3000-v4-datasheet-1.pdf ; product page https://www.oxts.com/products/rt3000v4/
- [G7] US DoD, "GPS Standard Positioning Service Performance Standard," 5th Edition, April 2020, https://archive.gps.gov/technical/ps/2020-SPS-performance-standard.pdf
- [G8] CAR 2 CAR Communication Consortium, "Vehicle C-ITS station profile," RS_2037, Release 1.6.10, 2026, https://www.car-2-car.org/fileadmin/documents/Basic_System_Profile/Release_1.6.10/C2CCC_RS_2037_Profile_R1610.pdf
- [G9] L.-T. Hsu, F. Huang, H.-F. Ng, G. Zhang, Y. Zhong, X. Bai, W. Wen, "Hong Kong UrbanNav: An Open-Source Multisensory Dataset for Benchmarking Urban Navigation Algorithms," NAVIGATION 70(4), navi.602, 2023, DOI 10.33012/navi.602.
- [G10] Olynik, Petovello, Cannon, Lachapelle, "Temporal impact of selected GPS errors on point positioning," GPS Solutions 6:47-57, 2002, DOI 10.1007/s10291-002-0011-9.
- [G11] Niu, Chen, Zhang et al., "Using Allan variance to analyze the error characteristics of GNSS positioning," GPS Solutions 18:231-242, 2014, DOI 10.1007/s10291-013-0324-x.
- [G12] Y. Wang, X. Chen, P. Liu, "Statistical Multipath Model Based on Experimental GNSS Data in Static Urban Canyon Environment," Sensors 18(4):1149, 2018, DOI 10.3390/s18041149.
- [G13] Jada, Joerger, "Measurement error time-correlation modeling for safety-critical navigation," NAVIGATION 72(4), 2025, DOI 10.33012/navi.721.
