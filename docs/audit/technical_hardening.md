# Final technical hardening

Initial HEAD: `11dbc6d` (phase 7); initial working tree clean. No reset or push.
Initial Python 3.14 suite: **464 passed, 17 subtests passed**, 379.48 s; no pre-existing failure.
Initial Python 3.8.20 suite: **464 passed**, 501.80 s; no pre-existing failure.

Audit completed before implementation: README, PAPER_READINESS_REPORT, CAMPAIGN_REPORT,
experiment_size, event_definitions, robustness_profiles, results index; reconstruction local
tracking/events, common-frame anonymous association/stitching, collision alignment, replay model,
top-down and CARLA HUD, visual QA, fusion evaluation and semantic oracle.

Original derived outputs for all 17 canonical and 240 recorded sweep runs are preserved locally
under `scratch/hardening_baseline/`. SHA-256 fingerprints cover 8,342 recorder/GT raw files.
No recording is being repeated. The historical reports remain records of their original phases.

The original S18 statistic is three false **track pairs in two runs**, not three runs: seed 16
contributes two pairs via one wrong stitch; seed 28 contributes one cross-observer pair.
Detailed evidence and before/after results are recorded in the accompanying audit documents.
