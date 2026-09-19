# Reproducibility

Everything below regenerates from the repository plus a CARLA installation. The
recorded artifacts are not committed — they are hundreds of megabytes of
telemetry — but every number quoted in the documentation is derived from them by
a generator that reads files, so a reproduction can be compared line by line
against what is written here.

---

## What is pinned

| Thing | Where |
|---|---|
| CARLA version and Python | `docs/ENVIRONMENT.md` |
| Every threshold, gain and tolerance | `configs/default.yaml`, hashed into every artifact |
| The nine scenarios | `configs/scenarios/*.yaml`, SHA-256 pinned in `tests/test_scenario_freeze.py` |
| Per-run seed and clock profile | `manifest.json`, `oracle/clock_ground_truth.json` |

### The scenarios are frozen

`tests/test_scenario_freeze.py` holds the SHA-256 of each of the nine scenario
files and fails if any byte changes. The point is not tidiness. A method that
is improved by adjusting the scenario it is measured on has not been improved,
and freezing the definitions makes that impossible to do by accident. The same
test asserts there are exactly nine files and that no new one has appeared.

### The configuration travels with the run

Every artifact carries `config_hash`. Re-deriving an old recording under today's
thresholds would describe a run that was never made, so
`scripts/reprocess_runs.py` re-derives each run under **its own** recorded
configuration, filling in only the keys that did not exist when it was recorded
— which is the only way a newly added stage can be applied to an older
recording at all. `tests/integration/test_recorded_campaign_config.py` enforces
this: a key the recording carries must match exactly, and only genuinely new
namespaces may be filled from current defaults.

---

## Determinism, and its limits

CARLA in synchronous mode at a fixed 0.05 s step is deterministic given the same
map, spawn points, seeds and control sequence. The pipeline downstream is
deterministic outright: no wall-clock reads, no unseeded randomness, no
iteration over unordered sets that reaches an output. Ties in track association,
event matching and rule application break on sorted identifiers so that two runs
of the same analysis produce byte-identical artifacts.

What is **not** guaranteed is bit-identical physics, even on the same machine.
This was measured rather than assumed: running one scenario's counterfactual
suite twice, back to back, with a freshly started simulator per replay and an
identical configuration, six of seven replays reproduced exactly and one differed
in impact speed by several per cent. **No replay changed outcome class** — every
collision was still a collision, every prevention still a prevention.

So the guarantee this project actually offers is at the level of the *verdict*:
which vehicle collided with which, in what order, which behaviours are in the
ancestry of the outcome, and what the counterfactual established. Continuous
quantities — impact speed, minimum distance — carry a few per cent of run-to-run
variation, and a result that depended on the third decimal of one of them would
not be reproducible.

Across CARLA builds, GPU drivers or operating systems the variation should be
expected to be larger, and nothing here bounds it.

**Two cautions, both learned the hard way, both now checked by the code.**

*The restart must be possible.* It only happens when the session can start the
server itself, which means `$CARLA_ROOT` must point at the installation. Without
it, `fresh_world_for_map` falls back to reusing the current server.

*The restart must also take effect.* `stop()` deliberately does not kill an
engine that was already running when the session started — killing a server
somebody else is using would be indefensible — but that engine keeps the RPC
port, the newly started one cannot bind it, and the client reconnects to the old
one. Every replay then shares accumulated state while every log line reports
success. This happened during development and produced a verdict that did not
reproduce.

So the restart is now **verified rather than assumed**: a genuinely fresh engine
has been ticking for seconds, and one that has served a campaign has not. The
check is cheap, it runs on every restart, and its result is written into the
attribution report as `replay_protocol.restarts_verified_fresh`. The viewer
prints a banner above any verdict whose replays shared a session.

Before a sweep, make sure nothing is already listening on the RPC port:

```bash
# Windows
Get-NetTCPConnection -LocalPort 2000 -State Listen
```

and check `replay_protocol.effective` in the resulting report reads
`fresh_server_per_replay`.

---

## The full reproduction

### 1. Environment

```bash
# CARLA 0.9.15, Python 3.8
python -m cdf.cli env          # verifies the simulator connection and version
```

`docs/ENVIRONMENT.md` covers the CARLA startup flags this project assumes.

### 2. Record the campaign

```bash
python scripts/run_campaign.py --artifacts artifacts_v2 \
                               --seeds 0 1 2 --attempts 3 --logs artifacts_v2/logs
```

Thirty-five scenario/variant combinations x three seeds = **105 runs**. One
subprocess per run with a fresh simulator connection, because a long-lived engine
accumulates state that silently changes later runs. Completed runs are skipped on
a re-invocation, so an interrupted campaign resumes.

### The simulator process, and one deviation

The default protocol restarts the engine for each run. On the machine the V2
campaign was recorded on, that was losing the engine part way through a scenario:
the client then spun on a refused streaming port, the campaign retried the same
run three times, and the whole campaign stalled with 15 of 105 recorded.

So the V2 campaign was driven by a supervisor that keeps **one** served engine
alive, passes `--keep-stray-engines` so the campaign does not kill it, and
restarts the engine only when it actually dies, relaunching the campaign from
whatever is already on disk. The deviation is recorded here rather than left
implicit. It changes only how the simulator process is kept alive around the
experiment: each run still records its own configuration, its own seed and its
own fate, so the campaign remains one experiment.

Two things made the default protocol fragile and are fixed rather than worked
around. `connect_with_retry` probed `get_server_version`, which answers while the
engine is still bringing a map up, so the caller's first `get_map` blocked for
sixty seconds and raised; it now asks for the world as well. And running a second
engine alongside the campaign's own, easy to do by accident, leaves two processes
contending for port 2000 and neither can serve.

The tree is stamped `campaign.json` with `clock_protocol:
independent_local_clocks`. A run recorded under a different protocol is reported
as **foreign** by the aggregation rather than averaged in — two campaigns
averaged together answer no question anyone asked.

### 3. Replay the counterfactuals

```bash
export CARLA_ROOT=/path/to/CARLA_0.9.15/WindowsNoEditor   # required, see below
python scripts/run_counterfactuals.py --artifacts artifacts_v2 --seeds 0
```

One seed per variant by default: a replay sweep costs a full simulator run per
intervention, and the verdict is a property of the scenario rather than of the
seed. `--fresh` re-records every replay instead of reusing one already on disk;
`--force` re-runs a suite that already carries an attribution.

`$CARLA_ROOT` is not optional here. Without it the session cannot restart the
simulator between replays, and the comparison the whole stage rests on is
quietly degraded — see the caution above.

### 4. Score, ablate, and build the viewer bundles

```bash
python scripts/reprocess_runs.py --artifacts artifacts_v2 \
                                 --stages evaluate ablate viewer
```

Offline; no simulator needed. `ablate` re-derives fusion twice per run — with
and without post-fusion causal reasoning — and scores both against the same
reference.

### 5. Generate the results

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.final_results import write_final_results; \
           write_final_results('artifacts_v2')"
```

Writes `summary/final_results.{json,csv,md}`. The markdown is what
[RESULTS.md](RESULTS.md) quotes.

---

## The tests

```bash
python -m pytest tests/ --ignore=tests/integration      # offline, ~3 minutes
python -m pytest tests/integration                      # needs a running CARLA
```

Four groups matter for trusting a reproduction:

**Scenario freeze** — the nine definitions are byte-identical to the ones the
results were produced from.

**Anti-leakage, statically** (`tests/test_no_privileged_leakage.py`) — no
inference module imports `cdf.oracle`, `cdf.simulation`, `cdf.common.clocks` or
`carla`; no privileged field name appears in a local or fused artifact; the
whole recorded campaign is walked, not a sample.

**Anti-leakage, dynamically** (`tests/test_inference_is_blind.py`) — delete the
oracle subtree, relabel the scenario as a different one, strip the designed
causal template out of the configuration, re-run the real pipeline over the same
recordings, and require every node, edge, confidence, chain and named
contributor to come back *identical*. They do. This is the strongest available
evidence that a reported number was not produced with knowledge of the answer.

**Configuration provenance** — a re-derivation cannot silently retune what the
campaign was recorded under.

---

## Reading someone else's artifacts

A run directory is self-describing. `manifest.json` names the scenario, variant,
seed, map and clock protocol; `evidence_manifest.json` lists every file with its
size and hash; and `viewer/index.html` opens the whole thing without any part of
this repository being installed:

```bash
cd <run_dir>/viewer && python -m http.server 8000
```

## Related

- [ENVIRONMENT.md](ENVIRONMENT.md) — CARLA setup
- [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) — what the campaign measures and why
- [RESULTS.md](RESULTS.md) — what it found
