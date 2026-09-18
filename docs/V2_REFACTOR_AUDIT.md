# V2 refactor audit

Written before anything was deleted, as the V2 brief requires. It records what
the repository contained at the start of the refactor, what each part is for,
and what V2 does with it.

**Starting HEAD:** `ae7f4cbbfa3b69624bf7b0ceffece19a31fca207`
("Make the observable comparison the primary metric, and fix a timeline bug in it")

## What V2 changes, in one paragraph

V1 answered one question -- *how much of the incident graph can distributed logs
reconstruct?* -- and answered it well. V2 splits that into four questions that
have to stay separate: what each vehicle observed, what happened globally, which
temporal properties were violated, and which behaviours contributed to
responsibility. Three consequences drive every entry below. A **camera** and
**traffic-control perception** are new inputs, so signs and road markings become
observable rather than privileged. **Contact replaces radar** as the primary
clock anchor, which makes the synchronisation story explainable in two lines and
makes the no-collision case an honest failure instead of a hidden fallback. And a
**global log** now exists before any graph, because a reader can check a table of
timestamps and cannot check a DAG.

## Classification

### KEEP -- unchanged, still correct under V2

| Component | Why it stays |
|---|---|
| `common/{config,io,layout,schemas,evidence,geometry}.py` | The artifact and schema substrate. `layout.py` grows V2 paths; nothing existing breaks. |
| `common/clocks.py` | Independent per-recorder clocks. V2 changes how offsets are *estimated*, not that clocks are independent. |
| `local/{recorder,radar,tracking,own_state,indicators}.py` | Honest onboard sensing and local tracks. Untouched by V2. |
| `causal/{counterfactuals,interventions,scm,attribution,combinations}.py` | The counterfactual engine, including the but-for/prevention-opportunity distinction §22 says not to regress. |
| `oracle/{observable,observable_graph,ground_truth_package}.py` | The observable ground truth. V2 extends it with traffic-control and responsibility references; the concept is exactly what §27 asks for. |
| `graph/ontology.py` | The comparable-vocabulary contract. V2 adds road/non-action types to it. |
| `evaluation/{graph_comparison,knowledge_gain}.py` | Node/edge matching that ignores event ids. Reused verbatim for V2 metrics. |
| `simulation/{carla_client,world,runner,controllers,vehicle_agent}.py` | Simulator lifecycle, including the fresh-engine verification. V2 adds sensors to it. |
| `tests/test_no_privileged_leakage.py`, `tests/test_inference_is_blind.py` | Anti-leakage. §4 explicitly forbids removing these. |

### REPLACE -- the concept survives, the implementation does not

| Component | Replaced by | Why |
|---|---|---|
| `fusion/clock_alignment.py` (radar-primary, `soft_l1` global fit, drift in ppm) | `fusion/contact_alignment.py` | §12. One collision cannot estimate drift over a 25 s window; claiming a ppm rate from it overstates what the evidence supports. V2 anchors on contact, fixes `scale = 1.0`, and reports drift as *unestimated, assumed negligible*. |
| `checking/properties.py` (1517 lines of hand-written P1--P4/O1--O2 evaluators) | `formal/` (syntax, trace, evaluator, properties, report) | §17. The current layer computes verdicts but has no logic to read: the properties are Python, not formulae. V2 uses executable MTL over a finite trace so a property is a term a reader can check. |
| Graph-first pipeline (local graph -> fused graph) | Log-first (`local_log.json` -> `global_log.json` -> graph) | §15. |
| `evaluation/graph_metrics.py` as primary scoring | `evaluation/graph_comparison.py` | Already demoted at HEAD; V2 removes the template path from the primary result entirely. |

### REMOVE -- obsolete under V2, archived under `legacy/`

| Component | Why it goes |
|---|---|
| `graph/canonical.py` | This module exists only to paper over the vocabulary gap between the scripted-action oracle and a physical reconstruction. The observable ground truth closed that gap at the source, so a "canonical recall ceiling" now measures nothing. §4 names it. |
| Template-based scoring as a headline metric | Superseded; retained only as `legacy_template_reference`. |
| `FINAL_STATUS.md` | A V1 status report. Keeping it next to V2 results would mix campaigns, which §47 forbids. |
| `scratch/` | Untracked working files from the V1 campaign. |
| Radar-primary alignment as the documented method | Moves to `legacy/`; §12 requires it out of the primary story. |

### MIGRATE -- moves or is extended rather than rewritten

| Component | Change |
|---|---|
| `local/event_extractor.py` | Gains road/traffic-control and non-action events; emits `local_log.json` alongside its graph. |
| `simulation/sensors.py` | Gains `CameraSensor` (rolling 20 s + 5 s buffer) and `LaneInvasionSensor`. |
| `oracle/events.py`, `oracle/graph.py` | Demoted to the scenario-design reference they always were; the primary reference is the observable package. |
| `viewer/` (2 993 lines) | Rewritten around four sections (§28). |
| `evaluation/final_results.py` | Rewritten to lead with the per-scenario supervisor table (§42) rather than aggregate ablations. |

### INVESTIGATE -- unresolved at audit time

| Question | Where it lands |
|---|---|
| Does CARLA 0.9.15 place physical STOP/YIELD sign props at the junctions the scenarios use? | §25. If not, spawn sign props and define oracle control zones in scenario config -- but local inference must still detect them by camera. |
| Is `sensor.other.lane_invasion` reliable enough to be treated as an onboard ADAS signal? | §9. If it reports the crossed marking type, it is usable; if it only reports "a marking was crossed", `SOLID_LINE_CROSSED` has to come from perception or be documented as unavailable. |
| Live MP4 encoding cost in synchronous mode | §6 allows buffering compressed frames and encoding after the run. Measured during Phase 3. |
| Is a sign classifier trainable without labelled data? | §7 requires a reproducible image-based method and forbids privileged labels. Falls back to a documented geometric/colour detector with measured precision/recall rather than a fabricated one. |

## Scenarios

S01--S09 are kept and **not retuned** (§24, §47). V2 changes sensors and timing
semantics, so the V1 recordings under `artifacts_independent_clocks/` are *not*
V2 results and are not mixed with them (§47); V2 records into `artifacts_v2/`.

S10--S16 are new (§23). Note that an earlier, unrelated scenario also called S10
was removed from this repository for a different reason; the V2 S10 is a fresh
single-stop scenario and shares nothing with it but the number.

## Known state at audit time

- 630 offline unit tests, plus scenario-freeze, blind-inference and
  leakage suites.
- V1 campaign: 39 runs under `artifacts_independent_clocks/`, 9 scenarios.
- Primary V1 result (observable ground truth): best local 0.400/0.153,
  simple fusion 0.613/0.301, fusion + global reasoning 0.613/0.358 (node/edge F1).
- No camera, no sign perception, no lane/line events, no non-action nodes,
  no executable temporal logic, no responsibility layer. All are V2 work.

## Deviations from the brief, and why

Three places where what was built differs from what §1--§49 asked for. Each is a
judgement, not an oversight, and each is recorded here so a reader can disagree
with it.

### The physical graph keeps its filename

§34 asks for `fusion/physical_causal_graph.json`. The file on disk is still
`fusion/fused_causal_graph.json`, with `physical_causal_graph` as an alias
property pointing at it.

Renaming it would touch 53 call sites across 18 files and -- the reason that
decided it -- would stop the V1 campaign from being re-read, which is how the two
generations are compared. The substantive requirement in §34 is "avoid multiple
redundant graph files with overlapping meanings", and that is met either way:
there is exactly one fused causal graph, plus the deliberately separate union
baseline. The alias makes the V2 vocabulary usable in new code.

### The legacy template scoring stays in `src/`, not `legacy/`

§4 lists "old template-based graph scoring as the primary metric" among the
things to remove or archive. It is no longer the primary metric -- the observable
comparison is -- but the earlier brief required retaining it as
`legacy_template_reference`, and the clock and method ablations still read it.

Moving it under `legacy/` would mean either breaking those ablations or importing
from `legacy/` in the active path, which is worse than leaving it where it is and
labelling it. It is labelled: in `layout.py`, in `suite.py`, and in the artifact
filename `legacy_template_edge_matches.csv`.

### The V1 docs are pointers, not deletions

§43 says to delete stale duplicates. `EVENT_TAXONOMY.md`,
`CLOCK_SYNCHRONIZATION.md` and `MODEL_CHECKING.md` are superseded by `EVENTS.md`,
`CLOCKS.md` and `FORMAL_METHODS.md`, but they are referenced from dozens of code
docstrings. Deleting them would leave those references dangling, which §4 forbids
in the same breath ("no broken docs"). Each now opens by naming its successor.

## What real recordings corrected

Offline reprocessing of the V1 campaign found four defects that no synthetic test
had, all in contact alignment, and they are worth recording because they are the
argument for validating against recordings rather than fixtures alone.

1. **Resting contact is reported as impacts.** After a pile-up the collision
   sensor fires roughly twice a second for the rest of the run at a hundredth of
   the impact impulse -- 43 such reports beside one real impact of 11 569 N*s.
2. **Averaging disagreeing pairings produces a number neither supports.** A true
   impact implied +0.267 s, a spurious pairing -0.083 s, and the median +0.092.
3. **Greedy matching cannot separate two similar impacts.** The impulses are
   uninformative; only the joint consistency of the assignment decides.
4. **The middle vehicle of a chain registers one impact, not two**, so one anchor
   relates both neighbours and the second offset inherits an error the recordings
   do not bound. The bound this audit originally reported was computed by
   subtracting two timestamps from two different clocks; it read 13 ms where the
   true error was 200 ms, and has been removed rather than corrected.

## Test count

677 at the starting HEAD; 922 offline at the time of writing, plus the
leakage, freeze and blind-inference suites.
