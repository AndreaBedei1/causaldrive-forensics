# Experiment size

How many runs each sweep needs, chosen from data (`scripts/experiment_size.py`), not by habit.  Each sweep first recorded a pilot of 5 runs (`scripts/run_sweep.py --runs 5`).  For every paper metric with a value per run, the pilot values were resampled with replacement (2000 times) at sizes N; N is the smallest size whose 95 % bootstrap interval of the campaign statistic (median of a per-run error, mean of a per-run share) is within +- the tolerance below.  Errors never seen (a wrong link, a false merge) cannot be sized by a bootstrap: after n independent trials without one, 3/n bounds their probability at 95 % (rule of three), so a 5 % bound needs 60 trials.  The chosen N is the largest over the metrics, capped at 40 runs per sweep (recording budget: about 35 s per run); where the cap binds, the interval reached is stated.  A bootstrap from a five-run pilot is crude (it cannot see values the pilot missed): the settling tables below, computed on every run recorded, check the choice after the fact.

Tolerances: association_accuracy +-0.05 share (identity association (contribution 2): share of decided tracks named correctly); fused_centre_error +-0.05 m or 10% of the pilot value (fusion of road users that recorded nothing (contribution 3)); alignment_error +-0.025 s (temporal alignment (contribution 1): half a radar period); event_time_error +-0.025 s (global event times (contribution 4): half a radar period).

Provenance: commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), code `b5cbbff6ceb04c12`, 2026-10-11T03:48:00Z.

Over all 240 runs of the sweeps: wrong links 0 in 464 trials (95 % upper bound 0.0065); false merges 3 in 503 trials.

| sweep | pilot outcomes c/b/n | runs recorded | outcomes c/b/n | N chosen | capped |
|---|---|--:|---|--:|---|
| anonymous_pair_adjacent | 5/0/0 | 40 | 40/0/0 | 40 | yes |
| anonymous_pair_platoon | 5/0/0 | 40 | 40/0/0 | 40 | yes |
| crossing | 2/1/2 | 40 | 18/7/15 | 40 | yes |
| cut_in | 2/0/3 | 40 | 17/2/21 | 30 | no |
| rear_end | 1/1/3 | 40 | 8/4/28 | 40 | yes |
| unobserved_cut_in | 4/0/1 | 40 | 32/0/8 | 34 | no |

## anonymous_pair_adjacent

- association_accuracy (mean of per-run values, share): pilot mean = 1.0, tolerance +-0.05; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 1.0, IQR 0.0, p95 1.0; n=10: median 1.0, IQR 0.0, p95 1.0; n=15: median 1.0, IQR 0.0, p95 1.0; n=20: median 1.0, IQR 0.0, p95 1.0; n=25: median 1.0, IQR 0.0, p95 1.0; n=30: median 1.0, IQR 0.0, p95 1.0; n=40: median 1.0, IQR 0.0, p95 1.0.
- fused_centre_error (median of per-run values, m): pilot median = 0.3667, tolerance +-0.05; 95 % half-width N=5: +-0.1103, N=10: +-0.0847, N=15: +-0.0591, N=20: +-0.0591, N=25: +-0.0591, N=30: +-0.0591, N=40: +-0.0591, N=50: +-0.0591, N=60: +-0.0591; needs N = 80.
  Settling: n=5: median 0.3667, IQR 0.1182, p95 0.4152; n=10: median 0.3529, IQR 0.1266, p95 0.4151; n=15: median 0.339, IQR 0.1079, p95 0.4086; n=20: median 0.3207, IQR 0.0964, p95 0.4149; n=25: median 0.3149, IQR 0.0965, p95 0.4116; n=30: median 0.3207, IQR 0.111, p95 0.4173; n=40: median 0.3236, IQR 0.1063, p95 0.418.
- alignment_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- event_time_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- wrong links: 0 in 80 trials (95 % upper bound 0.0375); 2.0 trials per run in the pilot -> 30 runs for a 5 % bound.
- false merges: 3 in 197 trials; 4.8 trials per run in the pilot -> 13 runs for a 5 % bound.

## anonymous_pair_platoon

- association_accuracy (mean of per-run values, share): pilot mean = 1.0, tolerance +-0.05; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 1.0, IQR 0.0, p95 1.0; n=10: median 1.0, IQR 0.0, p95 1.0; n=15: median 1.0, IQR 0.0, p95 1.0; n=20: median 1.0, IQR 0.0, p95 1.0; n=25: median 1.0, IQR 0.0, p95 1.0; n=30: median 1.0, IQR 0.0, p95 1.0; n=40: median 1.0, IQR 0.0, p95 1.0.
- fused_centre_error (median of per-run values, m): pilot median = 0.3462, tolerance +-0.05; 95 % half-width N=5: +-0.1316, N=10: +-0.1033, N=15: +-0.0751, N=20: +-0.0751, N=25: +-0.0751, N=30: +-0.0751, N=40: +-0.0751, N=50: +-0.0751, N=60: +-0.0751; needs N = 80.
  Settling: n=5: median 0.3462, IQR 0.1502, p95 0.5258; n=10: median 0.3539, IQR 0.1794, p95 0.7446; n=15: median 0.3666, IQR 0.1507, p95 0.6548; n=20: median 0.4183, IQR 0.1648, p95 0.565; n=25: median 0.4233, IQR 0.1581, p95 0.693; n=30: median 0.4305, IQR 0.1559, p95 0.673; n=40: median 0.4395, IQR 0.1638, p95 0.73.
- alignment_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- event_time_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- wrong links: 0 in 80 trials (95 % upper bound 0.0375); 2.0 trials per run in the pilot -> 30 runs for a 5 % bound.
- false merges: 0 in 229 trials (95 % upper bound 0.0131); 6.4 trials per run in the pilot -> 10 runs for a 5 % bound.

## crossing

- association_accuracy: fewer than 3 pilot values: not used to size the sweep.
- fused_centre_error (median of per-run values, m): pilot median = 0.6078, tolerance +-0.0608; 95 % half-width N=5: +-0.0572, N=10: +-0.0572, N=15: +-0.0572, N=20: +-0.0572, N=25: +-0.0572, N=30: +-0.0286, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.6078, IQR 0.1023, p95 0.6414; n=10: median 0.5305, IQR 0.1776, p95 0.6356; n=15: median 0.5405, IQR 0.1251, p95 0.6499; n=20: median 0.5503, IQR 0.1344, p95 0.708; n=23: median 0.5405, IQR 0.1373, p95 0.6584.
- alignment_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.05, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.025, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- event_time_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.05, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.025, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- wrong links: 0 in 93 trials (95 % upper bound 0.0323); 2.4 trials per run in the pilot -> 26 runs for a 5 % bound.
- false merges: 0 in 12 trials (95 % upper bound 0.25); 0.4 trials per run in the pilot -> 150 runs for a 5 % bound.

## cut_in

- association_accuracy (mean of per-run values, share): pilot mean = 1.0, tolerance +-0.05; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 1.0, IQR 0.0, p95 1.0; n=10: median 1.0, IQR 0.0, p95 1.0; n=15: median 1.0, IQR 0.0, p95 1.0; n=20: median 1.0, IQR 0.0, p95 1.0; n=25: median 1.0, IQR 0.0, p95 1.0; n=30: median 1.0, IQR 0.0, p95 1.0; n=40: median 1.0, IQR 0.0, p95 1.0.
- fused_centre_error: fewer than 3 pilot values: not used to size the sweep.
- alignment_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.05, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.05, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- event_time_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.05, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.05, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- wrong links: 0 in 87 trials (95 % upper bound 0.0345); 2.0 trials per run in the pilot -> 30 runs for a 5 % bound.
- false merges: 0 in 0 trials; 0.0 trials per run in the pilot -> - runs for a 5 % bound.

## rear_end

- association_accuracy (mean of per-run values, share): pilot mean = 1.0, tolerance +-0.05; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 1.0, IQR 0.0, p95 1.0; n=10: median 1.0, IQR 0.0, p95 1.0; n=15: median 1.0, IQR 0.0, p95 1.0; n=20: median 1.0, IQR 0.0, p95 1.0; n=25: median 1.0, IQR 0.0, p95 1.0; n=30: median 1.0, IQR 0.0, p95 1.0; n=40: median 1.0, IQR 0.0, p95 1.0.
- fused_centre_error: fewer than 3 pilot values: not used to size the sweep.
- alignment_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.025, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.05, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- event_time_error (median of per-run values, s): pilot median = 0.05, tolerance +-0.025; 95 % half-width N=5: +-0.025, N=10: +-0.025, N=15: +-0.025, N=20: +-0.025, N=25: +-0.025, N=30: +-0.025, N=40: +-0.025, N=50: +-0.025, N=60: +-0.025; needs N = 5.
  Settling: n=5: median 0.05, IQR 0.05, p95 0.05; n=10: median 0.025, IQR 0.05, p95 0.05; n=15: median 0.05, IQR 0.05, p95 0.05; n=20: median 0.05, IQR 0.05, p95 0.05; n=25: median 0.05, IQR 0.05, p95 0.05; n=30: median 0.05, IQR 0.05, p95 0.05; n=40: median 0.05, IQR 0.05, p95 0.05.
- wrong links: 0 in 43 trials (95 % upper bound 0.0698); 1.2 trials per run in the pilot -> 51 runs for a 5 % bound.
- false merges: 0 in 0 trials; 0.0 trials per run in the pilot -> - runs for a 5 % bound.

## unobserved_cut_in

- association_accuracy (mean of per-run values, share): pilot mean = 1.0, tolerance +-0.05; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 1.0, IQR 0.0, p95 1.0; n=10: median 1.0, IQR 0.0, p95 1.0; n=15: median 1.0, IQR 0.0, p95 1.0; n=20: median 1.0, IQR 0.0, p95 1.0; n=25: median 1.0, IQR 0.0, p95 1.0; n=30: median 1.0, IQR 0.0, p95 1.0; n=40: median 1.0, IQR 0.0, p95 1.0.
- fused_centre_error (median of per-run values, m): pilot median = 0.101, tolerance +-0.05; 95 % half-width N=5: +-0.0268, N=10: +-0.0214, N=15: +-0.0163, N=20: +-0.0163, N=25: +-0.0163, N=30: +-0.0163, N=40: +-0.0163, N=50: +-0.0163, N=60: +-0.0163; needs N = 5.
  Settling: n=5: median 0.101, IQR 0.0325, p95 0.1374; n=10: median 0.1155, IQR 0.0178, p95 0.1999; n=15: median 0.1172, IQR 0.0314, p95 0.1924; n=20: median 0.1201, IQR 0.0359, p95 0.1727; n=25: median 0.1191, IQR 0.0346, p95 0.1668; n=30: median 0.1167, IQR 0.0398, p95 0.2121; n=40: median 0.1167, IQR 0.0378, p95 0.3882.
- alignment_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- event_time_error (median of per-run values, s): pilot median = 0.0, tolerance +-0.025; 95 % half-width N=5: +-0.0, N=10: +-0.0, N=15: +-0.0, N=20: +-0.0, N=25: +-0.0, N=30: +-0.0, N=40: +-0.0, N=50: +-0.0, N=60: +-0.0; needs N = 5.
  Settling: n=5: median 0.0, IQR 0.0, p95 0.0; n=10: median 0.0, IQR 0.0, p95 0.0; n=15: median 0.0, IQR 0.0, p95 0.0; n=20: median 0.0, IQR 0.0, p95 0.0; n=25: median 0.0, IQR 0.0, p95 0.0; n=30: median 0.0, IQR 0.0, p95 0.0; n=40: median 0.0, IQR 0.0, p95 0.0.
- wrong links: 0 in 81 trials (95 % upper bound 0.037); 2.0 trials per run in the pilot -> 30 runs for a 5 % bound.
- false merges: 0 in 65 trials (95 % upper bound 0.0462); 1.8 trials per run in the pilot -> 34 runs for a 5 % bound.

Final hardening reanalyses the same saved 240 recordings. The original sample-size study and its execution provenance are retained; segmentation changes pair-trial denominators. Pilot record: `docs/audit/experiment_size_pilot.json`; final per-sweep results: [FINAL_VALIDATION_REPORT](FINAL_VALIDATION_REPORT.md).
