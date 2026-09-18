# The incident viewer

A static page, opened from a run directory, that answers *what happened and
why*. No framework, no bundler, no CDN, no web font, no network request of any
kind: the page is designed to open from an offline copy of the evidence.

```bash
python -m cdf.cli viewer --scenario S06 --variant a_front_pushed --seed 0
# or, for a run that already has a bundle:
cd artifacts_independent_clocks/S06_chain_collision/seed_000_a_front_pushed/viewer
python -m http.server 8000
# then open http://localhost:8000/index.html
```

The `viewer` stage writes `run_data.json` and copies `index.html`, `app.js` and
`styles.css` next to it, because the page fetches its data *relative to itself*.
A browser refuses that fetch over `file://`, which is why the instruction above
serves the directory rather than double-clicking the file; the page says so
itself if you try.

---

## Perspective and tab are different questions

Two controls, deliberately orthogonal.

**Perspective** (header, top right) selects *whose account you are reading*:

- **A**, **B**, **C** — one vehicle's own log. It can reach that participant's
  telemetry, its own radar tracks and its own graph, and nothing else.
- **FUSED** — the merged reconstruction. The participants' exchanged logs, the
  resolved identities, the common timeline, the fused causal graph.
- **ORACLE** — privileged ground truth. Red hazard border, because it is not
  something any vehicle knew.

The colour of the page changes with the perspective and a badge names it, because
mistaking a privileged fact for a reconstructed one is the single worst error a
reader of this tool can make. There is no code path that mixes them: the
bundle's privileged material lives under one key and only the oracle perspective
reads it, which a test verifies by walking the whole document.

A panel that shows a *fused* conclusion says so plainly when a local perspective
is selected, rather than displaying the merge's answer under one vehicle's name.

**Tabs** select *which question you are asking*, in the order an investigation
works through them.

---

## The tabs

### Overview

The answer, first, in words:

> A and B collided at t = 6.51 s on the common clock.
>
> Because:
> 1. B braking contributed to B slowing
> 2. B slowing led to A closing rapidly on B
> 3. A closing rapidly on B contributed to A's time-to-collision with B becoming critical
> 4. A's time-to-collision with B becoming critical resulted in the impact between A and B

Every one of those sentences is a field of `fusion/incident_reconstruction.json`.
The viewer puts them in reading order; it writes none of them and it has no
language model. Beneath it sits the verdict — the counterfactual replay's when
one has been run, the graph's hypothesis when it has not, always labelled with
which — and the disclaimer that travels with every attribution.

Also here: **At a glance** (scenario, map, seed, recorded outcome, clock gauge)
and **What the evidence does not settle**, which exists so that an honest
non-answer has somewhere to go other than silence.

### Reconstruction

Bird's-eye replay on canvas: trajectories, radar tracks, conflict regions, event
markers, the impact. Transport with play/pause, a scrub bar, frame stepping, and
a speed control from 0.1× to 4×. At 0.1× a 50 ms simulator step takes half a
second of wall time, which is what it takes to actually watch an impact happen.

Below it, the signals — speed, longitudinal acceleration, throttle, brake, range
and TTC per tracked target — with a cursor locked to the transport.

### Causal graph

The DAG, laid out left to right in time and banded by vehicle.

The distinction the whole method rests on is drawn rather than buried: an edge a
vehicle claimed **inside its own log** is solid and grey; an edge that exists
**only because the logs were merged** is dashed and accented. A filter isolates
the latter, which is the quickest way to see what the reasoning stage
contributed.

Drag to pan, wheel to zoom about the pointer. Filters on confidence and on
vehicle *hide* rather than delete — selecting a node still traces its real
ancestry through parts that are filtered out of view, because a highlight that
changed with the filter would be lying about the structure.

Click any node: its path to the outcome is highlighted and the detail panel
names the rule, the confidence, the evidence and — for an inferred edge — the
supporting participants and the clock slack the inference was allowed.

### Timeline

Every event, ordered, with its type, subject, confidence and provenance. Click
one to seek the reconstruction to it.

### Attribution

Three panels:

1. **Causal contribution** — the verdict class, its rationale, the per-action
   contribution scores with their but-for flags, and what each replay actually
   showed. Below it, the hypothesis the graph produced *before* any replay, so
   a reader can see what reasoning alone concluded and whether the simulator
   agreed.
2. **What would have prevented it** — the minimal prevention sets, each marked
   `minimal` or `minimal_within_tested`, with the untested subsets named.
3. **Counterfactual replays** — every replay including the factual one, with
   impact speed, minimum distance, minimum TTC and validation status.

### Model checking

Per property, per participant: PASS, FAIL or UNKNOWN, with counterexample
witnesses. `UNKNOWN` is a first-class verdict — a finite trace that never
exhibits a property's premise can neither satisfy nor violate it — and is
displayed as such rather than folded into a pass rate.

### Evidence

**Recorder clocks** — the estimated transform for each recorder onto the common
timeline, with the residual of the fit beside it, the evidence families it was
fitted from, and the drift status. Every timestamp elsewhere on the page has been
through one of these transforms, so the table is not an appendix.

**Reconstructed identity** — which radar track was resolved to which vehicle, the
trajectory RMSE behind each claim, the margin over the runner-up, and the
verdicts the association refused to make.

### Evaluation

Scored against the reference. Graph agreement for the best single vehicle and
the merged account; the scene reconstruction errors; the causal chain metrics;
the named contributors against the designed ones.

Then the **method ablation**: the same recording re-fused under one changed key,
scored three ways, with the strict edge-recall ceiling called out beside the
achieved recall — because a large fraction of the reference's edges leave
scripted-action nodes that no reconstruction can emit, and a strict recall
number read without that context says something untrue.

Everything on this tab is evaluation-only. None of it is ever an input to the
reconstruction, and the bundle keeps it structurally separate.

---

## Cross-linking

Clicking a step of a causal chain on the Overview tab opens that node in the
Causal graph tab, selected and highlighted. The sentence and the structure
behind it stay connected, which is the difference between a narrative you can
check and one you have to trust.

---

## What the bundle contains

`cdf.viewer.bundle` assembles one JSON document per run. Blocks whose source
artifacts are absent are **omitted and listed in `notes`**, so every panel
renders "not available for this run, because —" rather than an empty chart.

| Key | Source |
|---|---|
| `run`, `params` | manifest and configuration |
| `participants.<id>` | that vehicle's telemetry, controls, tracks, events, graphs |
| `fusion` | fused graphs, association, clock alignment, reconstruction, graph attribution |
| `counterfactual` | replay manifest and the contribution verdict |
| `checking` | property results and counterexamples |
| `evaluation` | metrics and the method ablation |
| `oracle` | **privileged**; badged, and the only place privileged data appears |

Series longer than `output.viewer_max_samples` are stride-decimated, never
interpolated: every point the page draws was recorded. What was decimated, and
at what stride, is printed in the footer.

## Tests

`tests/unit/test_viewer_bundle.py` asserts that the bundle carries the fields
the page reads, that privileged material appears nowhere outside the oracle
block — walked recursively rather than trusted — and that no key outside that
block is even *named* for the oracle.

One test pins every field name the page dereferences against the writers that
produce them. It exists because of a real defect: the attribution panel used to
probe a list of plausible field names and fall through to INSUFFICIENT EVIDENCE
when none matched. The artifact writes `contribution_score`, which was not on the
list, so every run with a perfectly good attribution rendered as though it had
none — and the bug was invisible, because its output was identical to the honest
answer.

## Related

- [DATA_BOUNDARY.md](DATA_BOUNDARY.md) — the split the perspectives render
- [GRAPH_FUSION.md](GRAPH_FUSION.md) — what the fused perspective shows
- [COUNTERFACTUALS.md](COUNTERFACTUALS.md) — what the attribution tab reports
