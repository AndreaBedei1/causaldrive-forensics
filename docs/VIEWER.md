# The incident viewer

A static page, opened from a run directory, that answers *what happened and why*.
No framework, no bundler, no CDN, no web font, no network request of any kind:
the page is designed to open from an offline copy of the evidence.

```bash
python scripts/serve_viewer.py --run artifacts_v2/S10_single_stop_a/seed_000_rolls_through
```

That builds the bundle, serves the run directory and opens a browser. Add
`--port N` to choose the port (`--port 0` picks a free one) or `--no-browser` to
just serve it. `python -m cdf.cli viewer --run ...` is the same command; the
script is a thin wrapper.

The stage writes `run_data.json` and copies `index.html`, `app.js` and
`styles.css` next to it, because the page fetches its data *relative to itself*.
A browser refuses that fetch over `file://`, which is why the run is served
rather than opened as a file; the page says so itself if you try. To serve a run
that already has a bundle, any static server will do:

```bash
cd artifacts_v2/S10_single_stop_a/seed_000_rolls_through/viewer
python -m http.server 8000
```

---

## Four sections, because there are four questions

The V1 viewer had nine tabs and a perspective switcher that recoloured the whole
page. It could show anything and answered nothing at a glance. This one has four
sections, one per question the pipeline exists to answer:

| Section | Question |
|---|---|
| **Reconstruction** | what did each vehicle record, and what does the merged account say? |
| **Graph** | what contributed to what, and how much of that was recovered? |
| **Responsibility** | which behaviours contributed, and which rules were broken? |
| **Video** | what did the forward camera actually see? |

Two rules govern the whole page.

**It renders what the artifacts say and computes nothing it could get wrong.** A
viewer that re-derived a metric could disagree with the run it is displaying, and
then a reader would have no way to tell which was right. Every number on screen
was read from `run_data.json`.

**Absence is shown, never filled in.** A run with no camera, no merged timeline
or no responsibility layer says so in the place the content would have been. A
blank panel looks identical whether nothing was found or nothing was run, and
those are very different findings.

---

## Perspective badges

The V1 perspective *switcher* is gone; the distinction it protected is not. Each
section carries a badge naming whose account is on screen:

- **LOCAL RECONSTRUCTION** — one vehicle, its own sensors, its own clock;
- **FUSED RECONSTRUCTION** — the merged account, built only from what the
  vehicles recorded;
- **PRIVILEGED GROUND TRUTH – EVALUATION ONLY** — read from exact simulator
  state, never available to inference.

Mistaking a privileged fact for a reconstructed one is the worst error a reader
of this tool can make, and the badge text is byte-identical to the string the
bundle stamps on its oracle block — a test asserts that, so the two cannot drift.

---

## Reconstruction

**Each vehicle's own log.** A vehicle switch (A / B / C) and a table:

| Time | Event | Subject | Evidence | Value | Conf. |

There is no common-time column, by construction: one vehicle has no way to know
what another recorder's clock said. Outcome events are red, non-actions amber,
road and traffic-control events blue. Clicking a row seeks the video to that
instant where a clip exists.

**The merged log.** The same table with common time and a `Who` column, in strict
chronological order.

Where no shared contact tied the recorders together, the table is replaced by a
notice naming the recorders that stayed on their own clocks, and an unaligned row
renders as a dash — never as `0.00`, which would be a fabricated timestamp.
Simulator time is never substituted. A recorder the alignment excluded usually
contributes no rows at all, so the log names it explicitly rather than reporting
a clean timeline that silently omits a vehicle.

---

## Graph

Time runs left to right, one horizontal band per vehicle, collisions drawn larger
and in red. Labels are shortened to stay readable at that density and the full
type is in the tooltip.

Three modes:

- **Reconstructed** — the fused physical causal graph;
- **Ground truth** — the *observable* ground truth, not the scenario template.
  The template asserts scripted actions no reconstruction can emit, so a diff
  against it would be a wall of unmatchable nodes that told a reader nothing;
- **Difference** — the ground-truth graph coloured by what the reconstruction
  recovered: green matched, red missed, with the count of invented nodes beside
  it.

The counts line under the graph quotes recall and edge F1 straight from the
comparison artifact. It also reports how many nodes the reconstruction invented,
which is the figure a careless implementation most easily reports as zero.

---

## Responsibility

A card per participant, with the eight findings the responsibility layer
produces: physical contributor, but-for, rules broken, properties failed,
non-actions, mitigating actions, prevention opportunities, and the summary
evidence class — **supported**, **partial** or **insufficient**.

The right-of-way verdict sits above the cards with the reason it was reached,
including when that reason is that priority could not be decided.

Below the cards, every temporal property with its verdict — PASS, FAIL, UNKNOWN
or **vacuous** — the formula that was evaluated, and the reason. Vacuous is
shown as its own state: a property whose trigger never fired has not passed.

**A banner appears above the cards when the replay protocol was degraded**, in
three states rather than two. A report predating the protocol record carries no
block at all, and reading that as "it was fine" is exactly the mistake the record
was added to prevent, so it gets its own message.

No legal-fault language appears anywhere. A test walks every string of real
output and permits *fault*, *guilt*, *liability* and *blame* only inside the
disclaimers that say what this layer is not.

---

## Video

A camera switch per vehicle, the 20 s + 5 s clip, and event markers on a
timeline below it — outcome, non-action and road events only, since marking every
event would produce an unreadable comb. Clicking a marker seeks; so does clicking
a row in the Reconstruction table.

A run recorded without a camera says so. That is a supported configuration: the
V1 scenarios have no camera at all.

---

## What the bundle contains

`run_data.json`, built by `cdf.viewer.bundle`. Blocks whose source artifacts are
absent are omitted and listed under `notes`, which the footer link shows.

| Block | Source |
|---|---|
| `run` | the manifest |
| `participants` | telemetry, controls, tracks, decimated |
| `logs` | `vehicle_*/local_log.json`, `fusion/global_log.json` |
| `fusion` | the fused graphs, association, clock, reconstruction |
| `formal` | `formal/properties.json`, `formal/results.json` |
| `responsibility` | `fusion/responsibility_{graph,report}.json` |
| `video` | per-vehicle frame index and clip path |
| `oracle` | privileged, including the observable ground truth |
| `evaluation` | metrics, matches, `graph_diff` |
| `counterfactual` | replay results and the protocol they ran under |

The video itself stays on disk and is referenced by relative path; a bundle
embedding 20 MB of frames per vehicle would be unopenable for no benefit.

---

## Tests

`tests/unit/test_viewer_bundle.py` covers both directions of the page/bundle
contract: every field the page reads must be produced by some writer, and every
field a writer declares the page reads must actually be read. It also asserts
that the four sections exist, that each absence notice exists, that no privileged
key appears outside the oracle block, and that map facts inside it appear only
under a `map_context` key — present as context for interpreting a claim, never as
the claim itself.

---

## Related

- `docs/EVENTS.md` — the vocabulary the tables and graph display
- `docs/CLOCKS.md` — why a row can have no common time
- `docs/FORMAL_METHODS.md` — what PASS, FAIL, UNKNOWN and vacuous mean
- `docs/RESPONSIBILITY.md` — what the cards are and are not claiming
