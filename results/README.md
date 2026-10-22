# Results

## Current: the canonical set re-acquired on 2026-10-22

- `g0_scorecard_20261022/`: the G0 scorecard of the 22 runs (`scorecard.md|json`, `scripts/g0_scorecard.py`) and
  the tracking diagnostic by motion regime (`tracking_regimes.md|json`, `scripts/tracking_regimes.py`).
  Analysis: `docs/G0_ERROR_ANALYSIS.md`.
- `reproducibility_20261022/`: integrity and reproducibility summaries of the two acquisitions:
  - set A, installed in `traces/`;
  - set B, the repeat, kept with the lab runs on `F:\CarlaGraph_repro_20261022`;
  - the S10 repeats.

  Protocol and causes: `docs/REPRODUCIBILITY.md`.

The 22 canonical runs keep their reconstruction and evaluation next to the raw data in
`traces/<scenario>/<run>/reconstruction/`.  Campaign v3 (`docs/CAMPAIGN_V3.md`) has not been run.  Its results will
go to `results/robustness/campaign_v3/`.

## Historical: the previous recordings (before commit `34162ca7`)

These numbers do not refer to the current `traces/`.

- `robustness_campaign_manifest.json`: the manifest of the robustness campaign of 2026-10-15/16.  It holds the
  frozen reconstruction, hashes, the raw-data hashes of the previous recordings, profiles, the 35-condition matrix,
  the seed schedule and the software versions.  It was written by `scripts/campaign_manifest.py` and is checked by
  `scripts/campaign_controller.py` (run from tag `robustness-campaign-final`).
- `robustness/frozen_campaign/`: that campaign:
  - every job (`jobs.jsonl.gz`);
  - the driver's summary (`summary.json|csv|md`, `figures/`);
  - the report (`report/`).

  Regenerate them with `python scripts/campaign_report.py robustness`.
- `robustness/frozen_campaign_smoke/`: its smoke test.
- `robustness/rtk5g_current/`: the RTK/5G GNSS preflight of 2026-10-21 on the previous recordings
  (`docs/archive/RTK5G_PREFLIGHT_REVIEW.md`).

Report: `docs/archive/ROBUSTNESS_CAMPAIGN.md`; protocol: `docs/archive/FROZEN_CAMPAIGN.md`.
