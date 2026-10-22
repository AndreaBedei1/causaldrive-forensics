# Robustness profiles

The robustness study (`scripts/robustness.py`, perturbations in `src/cdf/robustness/perturb.py`) measures how the reconstruction degrades when the recordings are worse than CARLA's.  Each condition perturbs a copy of a run, never the canonical raw files under `traces/`, and the unchanged reconstruction then runs on the copy.  Ground truth travels into the copy untouched and is read only by the evaluation: the reconstruction never sees it.  GNSS errors are not written into any file; they enter through the pose source handed to the reconstruction and to the replay.  Clock perturbations are constant offsets only (no drift).

Below, every parameter value is given exactly as in the code, with its justification: a published source, a value derived from one, or an engineering assumption with its reason.

The current GNSS protocol below is a new parametrization and is distinct from the historical 2026-10-15 campaign. The historical profile table and published campaign outputs remain documented separately and unchanged.

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

## Current GNSS protocol: RTK with correction transport over 5G

The active profiles are exactly `ideal` (G0), `rtk` (G1) and `degraded` (G2). `consumer` is retained only under `HISTORICAL_GNSS_PROFILES` for reproducibility of old analyses; it is not scheduled by the current campaign. The 5G assumption is limited to transporting RTK corrections to a GNSS/INS receiver. CARLA does not simulate 5G, and this study does not model radio behavior, correction latency or packet loss.

Errors are evaluated against the recorded CARLA pose, only after reconstruction: horizontal position is `hypot(dx, dy)` in metres; heading is the absolute wrapped difference in [-180, 180] degrees; horizontal velocity is `hypot(dvx, dvy)` in m/s. The reconstruction never reads ground truth.

| Level | Horizontal position | Heading/yaw | Horizontal velocity |
|---|---:|---:|---:|
| G0 `ideal` | exactly 0 | exactly 0 | exactly 0 |
| G1 `rtk` | P95 = 0.040 m | P95 = 0.140 deg | P95 = 0.016 m/s |
| G2 `degraded` | P99.5 = 0.500 m | P99.5 = 0.600 deg | P99.5 = 0.200 m/s |

These are percentile targets, not per-axis sigmas or hard limits; values above P99.5 are allowed. For a single independent, zero-mean isotropic 2D Gaussian sample, `R_p = sigma_axis sqrt(-2 ln(1-p))`; for absolute scalar Gaussian heading, `H_p = sigma_axis Phi^-1((1+p)/2)`. The velocity values below are equivalent single-sample sigmas implied by the targets; the implemented 20 Hz interpolated white-noise marginal is a mixture of phase variances and is calibrated directly to the target percentile.

| Level | Position sigma/axis [m] | Heading sigma [deg] | Velocity sigma/axis [m/s] |
|---|---:|---:|---:|
| G0 | 0 | 0 | 0 |
| G1 | 0.01634156 | 0.07142988 | 0.00653662 |
| G2 | 0.15359816 | 0.21374876 | 0.06143927 |

Position and heading use stationary `b + g(t) + w(t)` errors at the existing profile rates, with `g` initialized from its stationary distribution and linearly interpolated. Velocity retains the original white-noise model: independent per-axis `w` at the receiver rate, linearly interpolated to the 20 Hz reconstruction samples. Its active epoch amplitudes are calibrated against the mixture of interpolation phases at 20 Hz. The current profile components and epoch-declared one-axis sigmas are:

| Level | Position b / g / w [m] | Position tau / rate | Epoch sigma [m/axis] | Velocity b / g / w [m/s] | Velocity tau / rate | Epoch sigma [m/s/axis] |
|---|---:|---:|---:|---:|---:|---:|
| G0 | 0 / 0 / 0 | — | 0 | 0 / 0 / 0 | — | 0 |
| G1 | 0.00897324 / 0.01345986 / 0.00269197 | 60 s / 10 Hz | 0.01639920 | 0 / 0 / 0.00731787 | — / 10 Hz | 0.00731787 |
| G2 | 0.08527949 / 0.12791923 / 0.01421325 | 30 s / 1 Hz | 0.15439539 | 0 / 0 / 0.07226664 | — / 1 Hz | 0.07226664 |

| Level | Heading b / g / w [deg] | tau / rate | Epoch sigma [deg] |
|---|---:|---:|---:|
| G0 | 0 / 0 / 0 | — | 0 |
| G1 | 0.03853691 / 0.05780536 / 0.01926845 | 30 s / 10 Hz | 0.07209595 |
| G2 | 0.03713028 / 0.20792956 / 0.07426056 | 5 s / 1 Hz | 0.22389281 |

G1 and G2 position and heading component ratios retain the preceding profile ratios while scaling their amplitudes to the percentile targets. The velocity target applies at the 20 Hz samples consumed by reconstruction. The earlier Gauss-Markov velocity candidate borrowed the position time constants of 60 s and 30 s; no cited velocity specification supplies those correlation times. The original white receiver-epoch process meets the required 20 Hz percentiles after calibration for the interpolation-phase mixture, so it is retained and does not add a velocity time constant. Interpolation still creates correlation between adjacent reconstruction samples. No clipping is applied.

The deterministic acceptance test samples 4,096 independent two-second runs per profile (seed 0 through 4095). It checks position and heading at 20 Hz and receiver epochs, and velocity at the 20 Hz reconstruction samples where the protocol defines its target. This is separate from the independent validation below.

Independent validation uses seeds 300000 through 302047: 2,048 independent 20-second trajectories per profile on a 20 Hz grid. The 95% intervals resample complete seed trajectories (300 bootstrap replicates), preserving temporal dependence. The bootstrap interval for a maximum describes resampled maxima and is capped at the largest observed sample; it is not an upper bound on the population maximum. Values are in metres, degrees and m/s as indicated.

| Level / measure | Target | P50 (95% CI) | P95 (95% CI) | P99 (95% CI) | P99.5 (95% CI) | RMS (95% CI) | Max (95% seed-bootstrap interval) |
|---|---:|---:|---:|---:|---:|---:|---:|
| G1 position [m] | P95 0.040 | 0.01916 [0.01878, 0.01961] | 0.04032 [0.03931, 0.04141] | 0.04953 [0.04812, 0.05106] | 0.05285 [0.05114, 0.05468] | 0.02313 [0.02270, 0.02358] | 0.07635 [0.06690, 0.07635] |
| G1 heading [deg] | P95 0.140 | 0.04868 [0.04717, 0.05037] | 0.14229 [0.13838, 0.14665] | 0.18816 [0.18101, 0.19556] | 0.20604 [0.19654, 0.21584] | 0.07264 [0.07076, 0.07445] | 0.31576 [0.30228, 0.31576] |
| G1 velocity [m/s] | P95 0.016 | 0.00719 [0.00717, 0.00720] | 0.01602 [0.01599, 0.01605] | 0.02051 [0.02046, 0.02057] | 0.02223 [0.02218, 0.02230] | 0.00897 [0.00896, 0.00898] | 0.03670 [0.03437, 0.03670] |
| G2 position [m] | P99.5 0.500 | 0.18596 [0.18218, 0.18990] | 0.38135 [0.37421, 0.38839] | 0.46805 [0.45464, 0.47941] | 0.50290 [0.48183, 0.52493] | 0.22235 [0.21864, 0.22565] | 0.71073 [0.62276, 0.71073] |
| G2 heading [deg] | P99.5 0.600 | 0.14497 [0.14261, 0.14771] | 0.41925 [0.41345, 0.42542] | 0.54870 [0.53789, 0.55870] | 0.60049 [0.58374, 0.61657] | 0.21462 [0.21156, 0.21764] | 0.98729 [0.92970, 0.98729] |
| G2 velocity [m/s] | P99.5 0.200 | 0.06801 [0.06760, 0.06844] | 0.14655 [0.14566, 0.14737] | 0.18610 [0.18452, 0.18766] | 0.20161 [0.19966, 0.20353] | 0.08338 [0.08297, 0.08378] | 0.34012 [0.30654, 0.34012] |

All six target point estimates are within 2% of their target, and each target lies inside its seed-bootstrap 95% interval. The velocity white-noise epoch amplitudes are 0.00731787 m/s (G1, 10 Hz) and 0.07226664 m/s (G2, 1 Hz). They come from the exact Rayleigh-mixture quantile over the 20 Hz interpolation phases rather than from a target change.

On the four canonical recordings, first-10-second windows were sampled at 20 Hz using 512 seed blocks per recorder: S01 and S14 had 2 recorders each, S04 had 3 and S19 had 2. Across those windows, the target percentiles were G1 P95 position 0.03956–0.04043 m, heading 0.13673–0.14270 deg and velocity 0.01597–0.01600 m/s; G2 P99.5 position 0.51761–0.51896 m, heading 0.59770–0.61808 deg and velocity 0.19900–0.19964 m/s. These short windows are descriptive and are not pooled as extra independent evidence.

The model comparison used 512 new seeds (400000–400511) and both 10- and 20-second trajectories. Temporary bias is the per-trajectory magnitude of the mean 2D velocity-error vector; intervals bootstrap those trajectory means. Lag-1 autocorrelation is averaged across both horizontal components and trajectories. P95/P99.5 and RMS pool the 20 Hz samples; maxima are the observed maximum.

| Profile / duration | Model | Lag-1 autocorrelation | Mean temporary bias (95% CI) | RMS [m/s] | P95 [m/s] | P99 [m/s] | P99.5 [m/s] | Max [m/s] |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| G1 / 10 s | white interpolated | 0.6620 [0.6594, 0.6646] | 0.00096 [0.00092, 0.00100] | 0.00901 | 0.01611 | 0.02073 | 0.02249 | 0.03842 |
| G1 / 10 s | Gauss-Markov | 0.9863 [0.9857, 0.9868] | 0.00805 [0.00768, 0.00839] | 0.00929 | 0.01588 | 0.01994 | 0.02109 | 0.02557 |
| G1 / 20 s | white interpolated | 0.6635 [0.6617, 0.6654] | 0.00066 [0.00063, 0.00068] | 0.00899 | 0.01603 | 0.02061 | 0.02229 | 0.03444 |
| G1 / 20 s | Gauss-Markov | 0.9930 [0.9927, 0.9934] | 0.00796 [0.00760, 0.00830] | 0.00941 | 0.01596 | 0.01947 | 0.02078 | 0.02557 |
| G2 / 10 s | white interpolated | 0.9954 [0.9953, 0.9956] | 0.02755 [0.02640, 0.02883] | 0.08327 | 0.14556 | 0.17904 | 0.19293 | 0.31215 |
| G2 / 10 s | Gauss-Markov | 0.9987 [0.9986, 0.9987] | 0.07498 [0.07150, 0.07852] | 0.08931 | 0.15477 | 0.18818 | 0.20192 | 0.25347 |
| G2 / 20 s | white interpolated | 0.9959 [0.9958, 0.9960] | 0.01985 [0.01897, 0.02080] | 0.08363 | 0.14557 | 0.18526 | 0.20074 | 0.30029 |
| G2 / 20 s | Gauss-Markov | 0.9993 [0.9992, 0.9993] | 0.07126 [0.06839, 0.07430] | 0.08868 | 0.15259 | 0.18495 | 0.19602 | 0.25347 |

At the required 20 Hz grid, the white-interpolated model reaches both target percentiles on independent validation. Its higher adjacent-sample correlation in G2 is the linear interpolation already present in the original model; the Gauss-Markov model adds still stronger correlation and a longer-lived velocity offset. The measured mean temporary bias is 3–12 times smaller with white noise over 10–20 seconds, while RMS and target percentiles remain comparable. The position time constants are not evidence for velocity correlation, so the white model is the better-supported engineering choice for this protocol.

Position correlation is a sensitivity assumption, not a 5G property. The `gnss_correlated` family applies rho = 0.5, 0.9 and 1.0 to G2 slow position components; combined GNSS/radar and GNSS/impulse levels use G1/G2 or exact/G1/G2 as specified by the driver. For rho=1, white position noise remains recorder-specific. Heading and velocity streams remain recorder-specific and independent. The paired-family tests verify stream reuse across family names and decreasing simultaneous relative position error as rho increases.

**Experimental results.** Volckaert et al.'s Septentrio presentation reports horizontal RTK-epoch position P95=4.0 cm and P99=5.3 cm, and horizontal velocity over all epochs P95=1.6 cm/s and P99=2.9 cm/s. SSR corrections are converted to OSR in that test; it does not demonstrate a 5G link. SBG's EUT#1 RTK+odometer urban report gives real-time yaw P95=0.140 deg and 2D position P95=0.246 m. Lesjak et al.'s Table 1 reports overall 2D errors for C-ITS of P95=3.1 cm/P99.5=43.4 cm and for 4G P95=2.4 cm/P99.5=37.9 cm. RTK-fixed positions were 98.90% with C-ITS and 98.78% with 4G; C-ITS also had 0.39% no-fix, 0.45% SPP and 0.25% RTK-float, while 4G had 0.42% no-fix, 0.44% SPP and 0.35% RTK-float. The C-ITS link is not 5G. SBG's Ellipse-D RTK+odometer report gives yaw P99.7=0.444 deg in light urban and 0.477 deg in forest, and position P99.7=0.600 m and 0.838 m respectively. Thus 0.50 m is not the worst observed position error.

**Manufacturer specification.** The u-blox ZED-F9R-02B data sheet states velocity accuracy 0.05 m/s and dynamic heading accuracy 0.2 deg at 68% for dynamic operation at 30 m/s. It does not publish the G2 P99.5 speed or heading targets.

**Engineering assumptions.** G2 position 0.50 m is a conservative rounded stress target informed by the C-ITS P99.5 of 0.434 m, not a measured P99.5 of 0.50 m. G2 yaw P99.5=0.60 deg and speed P99.5=0.20 m/s are stress assumptions, not source percentiles. G2 combines evidence from different products and trials; it is neither one receiver's measured distribution nor the worst physically observable error. The Gaussian stationary model covers horizontal position, heading and horizontal velocity. It does not model RTK float/no-fix modes, NLOS jumps, outages, vertical errors, changing receiver modes, correction-age effects, or 5G network performance.

Correction transport over 5G is a system integration assumption, supported as feasible by published 5G/GNSS-RTK demonstrations and the FrontierSI testbed report. Those sources support feasibility only, not these percentile targets.

The cited Springer chapter, IEEE conference paper and EURASIP journal article are peer-reviewed scientific publications used as experimental context, integration-feasibility evidence and a Gauss-Markov modeling reference respectively. The Septentrio presentation and SBG reports are not treated as peer-reviewed papers; the u-blox sheet is a manufacturer specification; the FrontierSI document is a technical report. All b/g/w splits, interpolation adjustment, correlation fractions and G2 targets are engineering assumptions.

## Historical GNSS profile (frozen 2026 campaign)

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

## Historical: correlated position sensitivity and combined collision study

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

## Historical: simultaneous GNSS and radar degradation

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

`CollisionPerturbation` rewrites each recorder's `collisions.jsonl`.  Each callback is dropped with probability `p_drop`; its impulse is multiplied by max(0, 1 + N(0, eps^2)).  The draws are made per callback, separately for each recorder.

| Family: value | Justification |
|---|---|
| `impulse`: eps = 0.02, 0.05, 0.10, 0.20 | Engineering assumption: a sweep of the relative error of the reported impulse magnitude, from small to large; no source reviewed covers the accuracy of crash-impulse reports. |
| clamp of the factor at 0 | Engineering assumption: an impulse magnitude is never negative. |
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
- Deterministic families (`clock`, `downsample`, `dropout`, `outage`) run once with seed 0.  The `baseline` copy, left unchanged, must reproduce the canonical reconstruction.
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

The full entries of every source cited here ([R1]-[R11] radar, [G1]-[G13] GNSS, [N1]-[N8] RTK and its transport over 5G, and Kopp et al. [K1]), with the values each one supports and the kind of evidence, are in [`docs/REFERENCES.md`](REFERENCES.md), Part A.  Their DOIs were resolved again against Crossref on 2026-10-23.

## Radar levels v3 (campaign v3, 2026-10-22)

Re-examined against the sources: the four radar DOIs [R6]-[R9] resolve to the cited papers and their numbers were
checked in the papers.  Few peer-reviewed sources report *measured* per-detection errors against ground truth; most
numbers below are specifications or tracker/simulation design values, and the labels say so.  Values are 1-sigma.

| parameter | nominal | severe | extreme (stress test) |
|---|---|---|---|
| sigma_range | 0.25 m — assumption of [R9] (CARLA noise); specification 0.15 m [R6] | 0.50 m — engineering assumption | 0.50 m — engineering assumption |
| sigma_azimuth | 0.5 deg — specification at boresight [R6]; [R9] | 2.0 deg — specification at the +-60 deg FOV edge [R6] | 2.0 deg — as severe |
| sigma_elevation | 0.5 deg — engineering assumption (the cited sensors are 2-D) | 2.0 deg — engineering assumption | 2.0 deg — engineering assumption |
| sigma_radial_velocity | 0.10 m/s — assumption of [R9]; specification 0.028 m/s [R6] is tighter | 0.20 m/s — engineering assumption | 0.20 m/s — engineering assumption |
| p_drop (per detection) | 0.20 — 1 - P_D, P_D = 0.8 a tracker design value [R8] | 0.40 — engineering assumption ([R8] lowers P_D toward the FOV edges without a value) | 0.40 — engineering assumption |
| false returns per sweep (Poisson mean) | 3 — derived from measured counts: ~2.3 ghost points per frame [R7] (reflective staged scenes) | 3 — as nominal | 30 — tracker design value lambda_C [R8], **not measured**; possibly per multi-sensor scan |

* **nominal** = the profile of the frozen campaign (unchanged).  **severe** = measurement quality at the edges of
  the field of view / long range, twice the misses, realistic ghost rate: the degradation of the measurements
  themselves.  **extreme** = severe plus dense clutter: equal to the historical `high` profile, kept for
  comparability, and explicitly a stress test beyond the characteristics of typical automotive radar.
* Limitation of the clutter model: real clutter is spatially structured (multipath at guardrails and walls,
  underbody reflections) and often carries non-zero Doppler; Kopp et al. [K1] measured ~90 % clutter among *moving*
  detections of a production mid-range radar in extra-urban traffic.
  Uniform clutter is a simplification; the nominal rate is optimistic for moving clutter.
* Not modelled: weather attenuation, mutual interference (no measured numbers could be verified in accessible
  peer-reviewed full texts; candidate sources with DOI only: Hasirlioglu et al. ITSC 2016, 10.1109/ITSC.2016.7795918;
  Norouzian et al. IEEE TAP 2020, 10.1109/TAP.2019.2938735; Holder et al. ITSC 2018, 10.1109/ITSC.2018.8569423).
