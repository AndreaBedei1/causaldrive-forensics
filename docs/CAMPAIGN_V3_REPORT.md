# Campaign v3: results

Every number below comes from `scripts/campaign_v3_report.py` run on the job records of the frozen campaign, or from
the same records where a section says so.  Tables and figures are in [`results/campaign_v3/`](../results/campaign_v3/)
(index: [`results/campaign_v3/index.md`](../results/campaign_v3/index.md)).  Design, conditions and freeze:
[CAMPAIGN_V3.md](CAMPAIGN_V3.md).  Error profiles and their sources: [robustness_profiles.md](robustness_profiles.md),
[REFERENCES.md](REFERENCES.md).

## 1. What was run

* **Code and data.**  Tag `campaign-v3` (`df12f759`), run from a separate worktree of that tag.  At each of its five
  starts the controller verified the code hash (`83713ba5...`), the configuration hash (`830087c6...`) and the
  SHA-256 of the raw data of the 22 canonical runs against the manifest.  All 1816 complete jobs carry that commit
  and code hash, from a clean tree.  The 22 baseline jobs reproduce the canonical reconstruction exactly
  (`identical_graph` in every one).
* **When.**  2026-10-23, 05:36 to 14:28.  The sum of the job wall times is 76 h.
* **Jobs.**  1816, all complete; 0 failed in the end.

| family | conditions | jobs |
|---|---|---|
| `baseline` | G0 | 22 |
| `gnss` | G1 RTK, G2 degraded | 132 |
| `radar_v3` | nominal, severe, extreme; every recorder | 242 |
| `radar_asym` | nominal, severe, extreme; each recorder alone, and with three recorders every pair | 748 |
| `radar_gnss_v3` | {G1, G2} x {nominal, severe}; every recorder | 264 |
| `radar_asym_gnss` | G2 x {nominal, severe}; radar on the subsets of `radar_asym` | 408 |

* **Attempts.**  `jobs.jsonl` holds 1826 records: the 1816 complete jobs and 10 failed attempts.  The 10 failed
  attempts are job processes terminated from outside the campaign at 10:14 and 10:20-10:21 (section 15).  Their
  nine jobs ran again from the frozen code and completed.
* **Seeds.**  Every stochastic condition has seeds 0, 1 and 2.  The seed rule added seeds 3 and 4 to two
  conditions:
  * `radar_v3` extreme: the standard error over seeds of the aligned-run rate was 0.026 at 3 seeds and 0.022 at 4,
    above its tolerance of 0.02;
  * `radar_asym` extreme: the legacy fused-centre error was 0.084 m at 3 seeds and 0.066 m at 4 (tolerance 0.05 m),
    and the aligned-run rate was 0.025 and 0.021.

  On 2026-10-23 at 14:27 Andrea decided to add no further seed.  With 5 seeds every tolerance is met, except the
  legacy fused-centre error of `radar_asym` extreme: 0.052 m against 0.05 m.  That legacy metric falls back to
  recorder ghosts when a job has no other road user ([CAMPAIGN_V3.md](CAMPAIGN_V3.md), decision 7).  The position
  errors of this report do not use it: they are the raw road-user errors without ghosts.

## 2. How to read the numbers

* **Unit of replication: the seed.**  One seed draws every random error of a condition on all 22 runs.  Per
  condition and seed the runs are pooled:
  * rates are ratios of sums;
  * counts are means per job;
  * error statistics are taken over all compared states of all runs.

  A table gives the mean over seeds and a 95 % interval with Student's t on n_seeds - 1 degrees of freedom,
  truncated to the feasible range.  The 22 scenarios are a designed set, not a sample: an interval describes the
  randomness of the perturbations on these runs, not other scenarios.
* **Paired change.**  Each job is compared with the G0 baseline job of the same run.  "Change" below is that paired
  difference, averaged over seeds, with its interval.
* **Where each quantity is measured.**
  * Collisions: all 22 runs, 26 true contacts per set of runs, 2344 contacts over the campaign.  All 26 are between
    two recorders, matched from their own impact reports.
  * Road users that record nothing: the 45 observable non-recording vehicles are in ten two-recorder runs (S12 to
    S19).  Completeness and road-user errors come from those runs only.
  * The "all but one" subsets exist only in the six three-recorder runs, which have no non-recording vehicle.  Their
    rows therefore have no road-user errors.
* **Definitions** (`cdf.evaluation.scorecard`, module docstring):
  * a collision is *identified* when a node names exactly its participants, *misattributed* when it is found with
    other participants, and *missed* when no node matches it; a node with no true collision is *invented*;
  * an observable vehicle is *represented* when a road user follows it; *coverage* is its represented time over
    its observable time (mean over vehicles);
  * *duplicates* are extra road users on one vehicle;
  * a *phantom* is a road user that follows no true vehicle: *near* when its track lies within 3 m of a true
    vehicle box (a displaced estimate), *far* otherwise (clutter);
  * a *recorder ghost* is a recorder also drawn as an anonymous road user: a missed recorder link;
  * *wrong links* join a track to the wrong recorder; *false merges* join two vehicles; *missed merges* leave one
    vehicle split;
  * *all aligned*: every recorder of the run aligned in time and space;
  * CRITICAL_TTC *in time*: a justified warning raised before the contact;
  * a *path intrusion* (lane entry or cut-in) is found when the reconstruction reports it for the same recorder and
    subject within the match window; reported intrusions with no true counterpart are *extra*;
  * *unconfirmed* CRITICAL_TTC alarms have no counterpart in the ideal-track oracle;
  * *recorder pose P95*: the 95th percentile of a recorder's own position error.

## 3. G0 baseline

The 22 baseline jobs give the G0 results of [G0_ERROR_ANALYSIS.md](G0_ERROR_ANALYSIS.md).  With the campaign's
pooled definitions:

* collisions: 26/26 identified, 0 misattributed, 0 missed, 0 invented, timing error 0.00 s;
* road users: 45/45 observable vehicles represented, coverage 0.933, 0.91 duplicates per job (20 in all), 0.05
  recorder ghosts per job (1, in S06), 0 phantoms;
* road-user errors, pooled over all compared states: position median 0.242 m, P95 0.817 m, RMSE 0.444 m; speed
  median 0.036 m/s, P95 0.308 m/s, RMSE 0.133 m/s;
* associations: 0 wrong links, 0 false merges, 1.95 missed merges per job;
* semantics: 42/42 justified CRITICAL_TTC warnings in time (lead time median 1.52 s, minimum 0.75 s); 26 of 33
  path intrusions found (0.788), 7 extra; 0.09 unconfirmed CRITICAL_TTC alarms per job.

## 4. GNSS: G1 RTK and G2 degraded

GNSS degradation alone changes neither the collisions nor the road users:

| quantity | G0 | G1 RTK | G2 degraded |
|---|---|---|---|
| recorder pose P95 [m] | 0.000 | 0.033 [0.009, 0.057] | 0.311 [0.124, 0.497] |
| collisions identified | 1.000 | 1.000 | 1.000 |
| observable road users represented | 1.000 | 1.000 | 1.000 |
| coverage | 0.933 | 0.933 (change 0.001 [-0.001, 0.002]) | 0.926 (change -0.006 [-0.024, 0.012]) |
| position median [m] | 0.242 | 0.239 (change -0.003 [-0.017, 0.012]) | 0.253 (change 0.011 [-0.095, 0.117]) |
| position P95 [m] | 0.817 | 0.848 (change 0.031 [-0.027, 0.089]) | 0.867 (change 0.050 [-0.075, 0.175]) |
| speed median [m/s] | 0.036 | 0.039 (change 0.003 [0.002, 0.004]) | 0.048 (change 0.012 [0.011, 0.012]) |
| CRITICAL_TTC in time | 1.000 | 1.000 | 1.000 |
| unconfirmed CRITICAL_TTC alarms per job | 0.09 | 0.20 (change 0.11 [0.04, 0.17]) | 0.21 (change 0.12 [0.06, 0.19]) |

* 0 phantoms and 0 wrong links in both.
* Two changes have intervals that exclude zero, and both are small:
  * the speed error, by 0.003 m/s (G1) and 0.012 m/s (G2);
  * the unconfirmed CRITICAL_TTC alarms, which roughly double, from 0.09 to 0.20-0.21 per job.
* The recorder pose errors (P95 up to 0.31 m under G2) are small next to the radar's lateral error at range (about
  1.4 m at 40 m for a 2 degree azimuth sigma, [CAMPAIGN_V3.md](CAMPAIGN_V3.md)).  This is consistent with the absence
  of effects on association and completeness.

## 5. Radar: nominal, severe, extreme (every recorder degraded)

| quantity | G0 | nominal | severe | extreme (5 seeds) |
|---|---|---|---|---|
| collisions identified | 1.000 | 1.000 | 0.987 [0.932, 1.000] | 0.954 [0.902, 1.000] |
| invented collisions per job | 0.00 | 0.00 | 0.02 [0.00, 0.08] | 0.05 [0.00, 0.12] |
| phantoms per job (far) | 0.0 | 0.6 (0.5) | 68.7 [65.7, 71.7] (67.2) | 102.4 [99.5, 105.3] (99.4) |
| near phantoms per job | 0.00 | 0.06 | 1.52 [0.76, 2.27] | 3.05 [2.72, 3.37] |
| recorder ghosts per job | 0.05 | 0.06 | 0.50 [0.27, 0.73] | 1.79 [1.24, 2.34] |
| duplicates per job | 0.91 | 1.17 | 1.85 [1.59, 2.11] | 2.45 [2.08, 2.83] |
| coverage | 0.933 | 0.927 | 0.874 [0.857, 0.891] | 0.887 [0.877, 0.897] |
| position median / P95 / RMSE [m] | 0.242 / 0.817 / 0.444 | 0.256 / 0.971 / 0.507 | 0.317 / 1.335 / 0.645 | 0.325 / 1.556 / 0.749 |
| speed median / P95 / RMSE [m/s] | 0.036 / 0.308 / 0.133 | 0.045 / 0.332 / 0.211 | 0.068 / 0.442 / 0.246 | 0.068 / 0.491 / 0.630 |
| wrong links per job | 0.00 | 0.00 | 0.03 [0.00, 0.10] | 0.12 [0.04, 0.19] |
| false merges per job | 0.00 | 0.00 | 0.68 [0.29, 1.07] | 0.91 [0.56, 1.26] |
| all recorders aligned | 1.000 | 1.000 | 1.000 | 0.964 [0.916, 1.000] |
| CRITICAL_TTC in time | 1.000 | 1.000 | 0.984 [0.950, 1.000] | 0.919 [0.865, 0.973] |

* **Nominal radar** (typical production accuracy) is close to G0.  It adds 0.6 phantoms per job and raises the
  position P95 by 0.155 m [0.145, 0.164] and the RMSE by 0.063 m [0.037, 0.089].  Collisions, associations and
  warnings are unchanged.
* **Severe radar** leaves every observable vehicle represented but adds 68.7 phantoms per job, 98 % of them far from
  any vehicle.  The paired changes are:
  * coverage -0.059 [-0.076, -0.042];
  * duplicates +0.94 [0.68, 1.20] per job;
  * recorder ghosts +0.45 [0.23, 0.68] per job;
  * position P95 +0.518 m [0.420, 0.615], RMSE +0.201 m [0.163, 0.240].

  One collision is misattributed in 66 jobs (S12 `crash`, section 8).
* **Extreme radar** (severe with dense clutter, a stress test) adds 102.4 phantoms per job (97 % far).  Its paired
  changes are:
  * recorder ghosts +1.75 [1.19, 2.30] per job;
  * position P95 +0.740 m [0.505, 0.974], RMSE +0.305 m [0.245, 0.366];
  * speed RMSE +0.497 m/s [0.406, 0.588], driven by few large errors;
  * justified CRITICAL_TTC warnings in time -0.081 [-0.135, -0.027]: the only collision or warning measure whose
    interval excludes zero.

  The identified rate falls to 0.954 [0.902, 1.000], and 3.6 % of the jobs do not align every recorder.
* Coverage under severe and extreme radar is not distinguishable: the intervals overlap.

## 6. One, several or all radars degraded

Phantoms per job, by the number of recorders and of degraded radars (G0 GNSS):

| recorders | radar level | one degraded | two degraded | all degraded |
|---|---|---|---|---|
| 2 | severe | 32.5 [31.0, 33.9] | - | 64.6 [61.8, 67.3] |
| 2 | extreme | 49.4 [48.6, 50.2] | - | 98.3 [96.8, 99.8] |
| 3 | severe | 27.0 [23.2, 30.7] | 53.6 [46.2, 61.0] | 79.8 [68.7, 91.0] |
| 3 | extreme | 38.8 [36.9, 40.7] | 76.6 [72.1, 81.0] | 113.3 [105.4, 121.3] |

* **Phantoms add up over the degraded radars.**  Per degraded radar the count stays almost constant:
  * two recorders: 32.5 for one radar, 32.3 for each of two (severe); 49.4 and 49.2 (extreme);
  * three recorders: 27.0, 26.8 and 26.6 (severe); 38.8, 38.3 and 37.8 (extreme).

  A phantom from one recorder's radar is therefore not removed by the other recorders, which do not see it.
* **Other effects grow with the number of degraded radars, and collisions suffer mainly under extreme radar.**
  With three recorders under extreme radar (one, two, all degraded):
  * collisions identified: 0.973, 0.947, 0.920;
  * recorder ghosts per job: 0.87, 1.54, 2.20;
  * wrong links per job: 0.06, 0.12, 0.20.

  With two recorders the identified rate is 0.988 (one) and 0.975 (both) under extreme radar, 0.990 and 0.979 under
  severe radar (the S12 case of section 8); with three recorders it stays 1.000 under severe radar.
* **Road-user errors grow likewise** (two-recorder runs, position P95): severe 1.079 m (one) and 1.335 m (both);
  extreme 1.186 m and 1.556 m.

## 7. GNSS x radar

* **Mostly additive effects.**  For each seed the interaction is the combined change minus the sum of the GNSS-only
  and radar-only changes.  Over the four combinations and every metric of `interaction.csv`, four intervals
  exclude zero:
  * unconfirmed CRITICAL_TTC alarms, G1 with nominal radar: -0.11 [-0.17, -0.04] per job;
  * unconfirmed CRITICAL_TTC alarms, G2 with nominal radar: -0.12 [-0.19, -0.06] per job;
  * position median, G2 with nominal radar: +0.006 m [0.002, 0.011];
  * near phantoms, G2 with severe radar: +0.42 [0.06, 0.79] per job.

  The first two mean that the alarms GNSS degradation adds on its own (section 4) do not appear when the radar is
  perturbed too.  The other two are small next to the single-sensor effects.  Collisions, coverage, duplicates,
  all phantoms, recorder ghosts, the position P95 and RMSE, the speed errors and the warnings in time show no
  interaction.  Examples (G2 with severe radar):
  * phantoms: 69.6 per job combined, against 68.7 for the sum; interaction 0.9 [-5.0, 6.7];
  * coverage: interaction 0.003 [-0.013, 0.019];
  * position P95: interaction -0.052 m [-0.245, 0.140].
* **Asymmetric radar under G2 GNSS** (`radar_asym_gnss`) repeats `radar_asym`:
  * severe radar alone: 31.1 phantoms per job against 30.5;
  * severe radar on all but one: 55.4 against 53.6;
  * identified collisions: 1.000 in every subset under G2, against 0.995 and 1.000 without it.

  The single misattributed collision of `radar_asym` severe does not recur there.  The interval of `radar_asym` severe
  alone (0.995 [0.971, 1.000]) includes 1.

## 8. Collisions: identified, missed, misattributed, invented

* **None missed.**  Of 2344 true contacts in 1816 jobs, none was missed, and the report time of every detected
  contact matches the truth (timing error 0.00 s).
* **22 misattributed, 22 invented.**  All occur under severe or extreme radar, in four scenarios:

| scenario | condition | jobs | contacts | misattributed | invented |
|---|---|---|---|---|---|
| S04 `b_rear_first` | `radar_v3` extreme | 5 | 10 | 4 | 4 |
| S04 `b_rear_first` | `radar_asym` extreme | 30 | 60 | 12 | 12 |
| S07 `merge_conflict` | `radar_v3` extreme | 5 | 5 | 1 | 1 |
| S07 `merge_conflict` | `radar_asym` extreme | 10 | 10 | 1 | 1 |
| S12 `crash` | `radar_v3` severe | 3 | 3 | 1 | 1 |
| S12 `crash` | `radar_asym` severe | 6 | 6 | 1 | 1 |
| S13 `passing` | `radar_v3` extreme | 5 | 5 | 1 | 1 |
| S13 `passing` | `radar_asym` extreme | 10 | 10 | 1 | 1 |

* **How these errors arise.**
  * Every misattributed collision comes with an invented node that names a single recorder (`['A']` or `['B']`).
  * Every job with such a pair also has at least one missed recorder link and no wrong link.
  * The impact, reported by both recorders, ends up in single-recorder nodes instead of one node with both
    participants.  One node is matched to the true collision with incomplete participants (misattributed); the
    other counts as invented.
  * None of the 22 invented nodes is a true recontact.
* **Recontacts.**  S04 `a_front_pushed` (one A-B collision with a recontact 0.65 s later) has 0 invented collisions
  and 0 recontact splits in all its 132 jobs.  The recontact rule holds under every degradation, and the case left
  open at the freeze (a recontact reported by one recorder only, [CAMPAIGN_V3.md](CAMPAIGN_V3.md), decision 7) does
  not occur.

## 9. Completeness and continuity of the road users that record nothing

* **Represented.**  All 45 observable vehicles are represented in every job of every condition (1.000).
* **Continuity: coverage.**  Coverage drops by:
  * up to 0.007 under GNSS degradation and nominal radar;
  * 0.023-0.030 when one radar is severe or extreme;
  * 0.046-0.062 when every radar is severe or extreme, with or without degraded GNSS.
* **Continuity: fragmentation.**  Duplicates per job rise from 0.91 (G0) to 1.85 (severe) and 2.45 (extreme), and
  missed merges from 1.95 to 4.61 and 7.35.  Degraded radar therefore splits a vehicle into more road users rather
  than losing it.
* **Recorder ghosts** (a recorder also drawn as an anonymous road user) rise from 0.05 per job to 0.50 (severe) and
  1.79 (extreme).

## 10. Position and speed errors

Road-user errors pooled over all compared states (mean over seeds [95 % interval]):

| condition | position median [m] | position P95 [m] | position RMSE [m] | speed median [m/s] | speed P95 [m/s] |
|---|---|---|---|---|---|
| G0 | 0.242 | 0.817 | 0.444 | 0.036 | 0.308 |
| G1 RTK | 0.239 [0.225, 0.254] | 0.848 [0.790, 0.905] | 0.447 [0.432, 0.462] | 0.039 [0.038, 0.040] | 0.309 [0.299, 0.319] |
| G2 degraded | 0.253 [0.147, 0.359] | 0.867 [0.742, 0.992] | 0.463 [0.390, 0.536] | 0.048 [0.047, 0.048] | 0.316 [0.297, 0.335] |
| radar nominal | 0.256 [0.245, 0.268] | 0.971 [0.962, 0.981] | 0.507 [0.481, 0.533] | 0.045 [0.039, 0.050] | 0.332 [0.291, 0.374] |
| radar severe | 0.317 [0.295, 0.338] | 1.335 [1.237, 1.432] | 0.645 [0.606, 0.683] | 0.068 [0.063, 0.072] | 0.442 [0.383, 0.500] |
| radar extreme | 0.325 [0.319, 0.332] | 1.556 [1.322, 1.791] | 0.749 [0.688, 0.810] | 0.068 [0.067, 0.070] | 0.491 [0.467, 0.515] |
| G1 + severe | 0.313 [0.290, 0.336] | 1.386 [1.256, 1.517] | 0.654 [0.598, 0.710] | 0.069 [0.066, 0.073] | 0.437 [0.362, 0.512] |
| G2 + severe | 0.330 [0.252, 0.408] | 1.332 [1.223, 1.442] | 0.676 [0.644, 0.708] | 0.074 [0.063, 0.084] | 0.448 [0.433, 0.464] |
| one radar severe | 0.259 [0.255, 0.262] | 1.079 [1.026, 1.131] | 0.550 [0.532, 0.567] | 0.050 [0.047, 0.053] | 0.363 [0.344, 0.383] |
| one radar extreme | 0.266 [0.261, 0.271] | 1.186 [1.069, 1.302] | 0.619 [0.579, 0.660] | 0.050 [0.049, 0.052] | 0.394 [0.386, 0.402] |

* **The tail moves more than the median.**  With every radar severe or extreme, alone or with degraded GNSS, the
  median grows by 0.071-0.088 m and the P95 by 0.52-0.74 m.
* **Per scenario** the G0 median ranges from 0.05 m (S12) to 0.42 m (one S13 run); under extreme radar it ranges
  from 0.10 m to 0.49 m (`results/campaign_v3/scenarios.csv`, figure `scenarios_position`).
* **Speed RMSE intervals are wide** in some conditions, for instance nominal radar 0.211 [0.000, 0.519] m/s.  The
  RMSE reacts to a few large speed errors, and the median and P95 are the stable summaries there.

## 11. Associations and critical cases

* **Recorder links.**
  * Wrong links appear only under severe and extreme radar: at most 0.12 per job with every radar degraded, and
    0.20 in three-recorder runs under extreme radar.
  * Missed links equal the recorder ghosts (section 9).
* **Merges.**  False merges rise from 0 to 0.68 (severe) and 0.91 (extreme) per job.
* **CRITICAL_TTC.**
  * Every justified warning not given in time was never given; none came late.
  * S11 `consequential` (warning of C about A) is the most sensitive case:
    * 2 of 3 jobs miss it under severe radar, and 3 of 5 under extreme;
    * 6 of 18 miss it under one or two severe radars, and 9 of 30 under extreme;
    * 2 of 3 miss it when G1 or G2 GNSS is added to severe radar, and 6 of 18 with asymmetric severe radar under
      G2.
  * S10 `deflected_into_c` (C about A) misses under G2 with severe radar: 1 of 3 jobs, and 3 of 18 with asymmetric
    radar.
  * Under extreme radar single warnings are also missed in S12, S13 (`abreast`, `passing`, `platoon`), S14, S16
    and S17, each in one of 5 jobs (radar on every recorder) or one of 10 (asymmetric).  S19 misses in two of 5 and
    two of 10.
  * The median lead time of the warnings in time stays at 1.45-1.52 s in every condition.  The shortest lead is
    0.75 s in G0, 0.70-0.75 s under GNSS degradation, 0.15-0.20 s with nominal radar, 0.75-0.80 s with severe radar,
    and 0.00 s (a warning in the frame of the contact) with extreme radar.
  * Unconfirmed alarms per job: 0.09 (G0), 0.20-0.21 (GNSS), 0.05 (nominal radar), 0.12 (severe), 0.18 (extreme).
* **Path intrusions.**
  * The found share stays between 0.71 and 0.85 across conditions and recorder strata (G0 0.788 over all runs).
  * Extra intrusions grow with radar degradation: 0.32 per job in G0, 0.53 under severe and 1.56 under extreme
    radar on every recorder.
  * In the three-recorder runs the found share rises with degraded radar (for instance 0.847 against 0.625 of G0
    on the same runs, severe radar on all but one).  It rises together with the extra intrusions.  This is
    consistent with noise pushing estimates across the lane corridor more often, not with better detection.

## 12. Scenarios and seed variability

* **Per scenario** (`results/campaign_v3/scenarios.csv`: mean, minimum and maximum over seeds; figures
  `scenarios_phantoms` and `scenarios_position`):
  * phantoms per job under extreme radar range from 49 (S09 `near_simultaneous`) to 187 (S19 `highway_curve`);
  * under severe radar they range from 17 (S07, S09) to 157 (S19).
* **Seed variability is small next to the effects.**  Standard deviations over seeds, severe and extreme radar on
  every recorder:
  * phantoms per job: 1.2 and 2.3;
  * identified collisions: 0.022 and 0.042;
  * position P95: 0.039 m and 0.189 m;
  * coverage: 0.007 and 0.008.
* **Seed rule.**  Its standard errors are given in section 1.

## 13. What degrades the reconstruction most, and why

1. **Radar clutter produces phantoms.**  97-98 % of the phantoms under severe and extreme radar lie more than 3 m
   from any vehicle.  Their number is proportional to the number of degraded radars (section 6).  The tracker is not
   re-tuned to the degraded radar (CAMPAIGN_V3.md, "Reconstruction configuration frozen"), so it confirms clutter
   tracks that last long enough.  Phantoms do not hide real vehicles: every observable vehicle stays represented.
2. **Radar noise and misses fragment the road users and break recorder links.**  Duplicates, missed merges and
   recorder ghosts grow with the radar level.  Every misattributed collision coincides with a missed recorder link
   (section 8).  The missed CRITICAL_TTC warnings are of the same kind: a warning about the partner is never raised.
3. **GNSS at the G1 and G2 levels has small effects.**  It slightly raises speed errors and unconfirmed alarms.  Its
   effects add to the radar's; the alarms it adds alone do not appear when the radar is perturbed too (section 7).

The reconstruction degrades gradually.  Collisions are never missed and observable vehicles never lost.  The cost
appears as false road users, split road users, wider error tails and, under extreme radar, a few misattributed
collisions and missed warnings.

## 14. Limits of the study

* **Simulation.**  The accidents are simulated.  CARLA's radar casts rays and adds no noise.  The degradation
  profiles add Gaussian per-detection errors, independent misses and uniform clutter.  Real clutter is structured
  (guardrails, multipath), and real misses depend on the target.
* **GNSS model.**  The GNSS profiles are stationary Gaussian processes, with no RTK float or no-fix episodes and no
  outages.  5G is only the transport of the RTK corrections; no network behaviour is simulated.
* **Collisions.**  Every collision of the dataset is between two recorders.  The identification of a collision with
  a vehicle that records nothing is not tested.
* **Scope of the intervals.**  The 22 scenarios are a designed set; the intervals cover the random perturbations on
  these runs.  Three seeds (five for the two extreme conditions) give wide t intervals for rare events such as
  misattributed collisions.
* **Seeds closed by decision.**  The seed rule was stopped at 5 seeds; one legacy tolerance is missed by 0.002 m
  (section 1).
* **No re-tuning.**  The method was not re-tuned to any degraded sensor.
* **Wall times not comparable.**  Job wall times depend on the machine's load and on the priority changes of
  section 15, so they are not compared across conditions.

## 15. Execution notes

These events changed neither the code nor any job's result: every complete job carries the frozen commit and code
hash.  Details are in [PROJECT_STATUS.md](PROJECT_STATUS.md).

* **External terminations** (10:14, 10:20-10:21).  Ten job processes were terminated from outside the campaign
  (exit code 1, no traceback).  A concurrent session on the machine was the likely source; no record ties it to
  these processes.  The failed attempts stay in `jobs.jsonl`.  A pause and resume (10:31-10:32) re-queued the jobs:
  the controller does not count an attempt without provenance.
* **Priority** (12:19).  At Andrea's request the campaign received the 22 cores ahead of another project's load:
  fixed concurrency 22 and above-normal priority, inherited by every job and child through a Windows job object.
  From 13:25 to 13:43 it ran at the frozen default (below normal).
* **Hidden launch** (13:43).  `campaign_v3.bat` starts the controller without a console, so Windows opened a visible
  console for every job.  From 13:43 the same controller command ran with a hidden console.
* **Interrupted runs.**  Two `stop-now` commands (13:24 and 13:43) interrupted 18 and 21 running jobs.  Those
  attempts were not recorded, and the jobs ran again.
* **Closing.**  The campaign was paused at 14:27 and closed at 14:28 by a controller started with `--max-seeds 5`,
  which reached COMPLETE with nothing left to run.

## 16. Files

| path | content |
|---|---|
| `results/campaign_v3/conditions.csv`, `conditions.md` | one row per condition and stratum: values, SD and interval over seeds, paired changes |
| `results/campaign_v3/interaction.csv` | GNSS x radar interaction per metric |
| `results/campaign_v3/asymmetry.csv` | phantoms, completeness, errors and links by number of degraded radars |
| `results/campaign_v3/scenarios.csv` | per scenario and condition: mean, minimum and maximum over seeds |
| `results/campaign_v3/failures.csv` | jobs failed in the end (none) |
| `results/campaign_v3/report_data.json` | all of the above in one file |
| `results/campaign_v3/figures/` | collisions, completeness, errors, asymmetry, interaction and scenario figures (SVG, PDF, PNG) |
| `results/robustness/campaign_v3/jobs.jsonl.gz` | every attempt (1826 records), compressed; SHA-256 of the uncompressed file in the index |
| `results/robustness/campaign_v3/manifest.json` | the frozen manifest |
| `results/robustness/campaign_v3/` (other files) | the controller's own summary and its log |

Regenerate the tables and figures:

```bat
python scripts\campaign_v3_report.py --jobs results\robustness\campaign_v3\jobs.jsonl --out results\campaign_v3
```

(after decompressing `jobs.jsonl.gz`).
