# CarlaGraph / causaldrive-forensics

Offline forensic reconstruction from each vehicle's own recorded radar, odometry,
controls and collision callbacks. Local tracks and events are reconstructed first;
clock alignment, conservative recorder links and anonymous road-user fusion follow.
Ground truth is available only to privileged evaluation and never enters reconstruction,
fusion or replay. Supported/tested Python version: 3.8 only (the CARLA 0.9.15 client wheel is cp38):
one environment runs acquisition, reconstruction, evaluation, replay and the tests.

The saved campaign contains 17 canonical recordings and 240 local sweep recordings.
Current quantitative results, limitations, tests and the exact analysis freeze are in
[FINAL_VALIDATION_REPORT](docs/FINAL_VALIDATION_REPORT.md). The acquisition provenance
of every recording remains historical; the new canonical S02 does not redefine old sweeps.

## Reconstruct and evaluate saved files

```text
python scripts/reconstruct_run.py traces/S17/run_0_crash
python scripts/worked_example.py traces/S17/run_0_crash
python -m pytest -q
```

Install NumPy, Pillow, OpenCV, PyYAML, Matplotlib and pytest. Recording and interactive
replay additionally require the matching CARLA 0.9.15 Python API. The current validation
is entirely offline and needs no CARLA server or provider API.

For a complete reproducible analysis, execute `scripts/final_validation.py` from a
clean detached checkout of `ANALYSIS_FREEZE_COMMIT` (`8d7343d`), with `--original-root`, a separate
`--data-root`, `--analysis-commit` and the successive phases `stage`, `reconstruct`,
`aggregate`, `sensitivity`, `robustness`, `visual`, `figures`, `qa`. All raw files are
read or linked; only derived outputs are published. The script verifies the source
checkout is clean at that commit before and after every phase.

## Results and review

- [Results index](results/README.md): current tables and vector figures, with artifact hashes.
- [Event definitions](docs/event_definitions.md): shared body geometry, target-induced cut-in and thresholds.
- [Robustness profiles](docs/robustness_profiles.md): independent/correlated GNSS and combined impulse study.
- [Fusion regression diagnosis](docs/audit/fusion_accuracy_regression.md): identical-instant historical comparisons.
- [Acquisition and calibration](docs/campaign_acquisition.md): sensor geometry and recording prerequisites.
- [Paper positioning](docs/paper_positioning.md): framing, logging prerequisites vs regulations, related work, limitations.
- [Verified bibliography](docs/bibliography.md).
- [Manual replay checklist](docs/manual_replay_checklist.md).

Each canonical run has one current `reconstruction/evaluation/visual_audit_final` set.
Headless replay frames read reconstructed data and public map geometry. Interactive replay:

```text
python scripts/replay_run.py traces/S12/run_0_near_simultaneous --speed 0.25 --paused
```

Recorder-associated tracks are dots; each anonymous fused entity is drawn once.
Radar blindness, uncertainty, conservative unmatched contacts and missed merges remain
explicit limitations. Source nodes and source tracks are preserved in aggregated global events.

The optional `src/cdf/llm` infrastructure is parked and is outside this validated pipeline.
No provider calls are needed for any current result.
