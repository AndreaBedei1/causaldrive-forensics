# Results

## Current: the canonical set of 2026-10-22, final code of campaign v3 (2026-10-23)

- `g0_final/`: the G0 scorecard of the 22 runs with the final code (`scorecard.md|json`, `scripts/g0_scorecard.py`)
  and the tracking diagnostic by motion regime (`tracking_regimes.md|json`, `scripts/tracking_regimes.py`).
  Analysis: `docs/G0_ERROR_ANALYSIS.md`.
- `campaign_v3/`: the tables, figures and index of the robustness campaign v3 (`scripts/campaign_v3_report.py`;
  report `docs/CAMPAIGN_V3_REPORT.md`).
- `robustness/campaign_v3/`: that campaign's records:
  - every attempt (`jobs.jsonl.gz`, 1826 records; SHA-256 in `campaign_v3/index.md`);
  - the frozen manifest (`manifest.json`);
  - the controller's own summary (`summary.*`, `campaign_v3_*`, `figures/`);
  - its log and final state (`control/`).

  `campaign_v3/` regenerates from `jobs.jsonl.gz` byte for byte.
- `reproducibility_20261022/`: integrity and reproducibility summaries of the two acquisitions:
  - set A, installed in `traces/`;
  - set B, the repeat, kept with the lab runs on `F:\CarlaGraph_repro_20261022`;
  - the S10 repeats;
  - the amendment of 2026-10-23: the road map added to the 22 incident contexts (old and new SHA-256).

  Protocol and causes: `docs/REPRODUCIBILITY.md`.

The 22 canonical runs keep their reconstruction and evaluation next to the raw data in
`traces/<scenario>/<run>/reconstruction/`.

## Superseded on the same recordings

- `g0_scorecard_20261022/`: the G0 scorecard of 2026-10-22, before the recontact rule, the supplied map, the
  inherited-identity guard and the final scorecard definitions (`docs/G0_ERROR_ANALYSIS.md` lists the changes).
  Kept for traceability; `g0_final/` replaces it.

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
