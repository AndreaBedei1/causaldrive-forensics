# Final technical hardening

Final hardening of saved data, 2026-10-11. Initial HEAD: `11dbc6d1a479d535d87b5edf42158d3e5c9788ae` (phase 7);
initial working tree clean. The requested project/context audit was completed
before edits: README, campaign/readiness reports, experiment size, definitions,
robustness profiles, result index, reconstruction/fusion/tracking, replay/QA and
evaluation/oracle code. No acquisition, scenario redesign or research campaign.

## Tests and code snapshots

| suite | initial | final |
|---|---|---|
| Python 3.14.2 | 464 passed, 17 subtests, 379.48 s | 481 passed, 17 subtests, 161.74 s |
| Python 3.8 (CARLA environment) | 464 passed, 501.80 s | 481 passed, 417.28 s |

No pre-existing failure. Seventeen regression tests were added for presentation,
persistent mixed-body support/UNKNOWN, identity-boundary stitching, lateral lane
jumps, impulse uncertainty, competing partners/chain assignments, provenance and
checker independence. Existing canonical fusion tests retain S08 alignment,
S16, S17 and negative S18 checks; privileged-file poisoning/access checks pass.
Provider tests use mocks; no test calls an LLM API. Durations are machine/load
observations, not a reconstruction speed comparison.

Runtime fix is committed as `fd8d2ba`; previous source snapshots were committed
before their analyses. Created implementation commits:

- `1fc3e8d` hardening-ui: compact anonymous labels and replay help
- `48b6826` hardening-reconstruction: segment ambiguous body support and constrain collision and fusion assignments
- `be1aaf9` hardening-provenance-oracle: verify historical code equivalence and add independent geometry check
- `bf79b92` hardening-collision: correct matching branch indentation
- `64bce83` hardening-provenance: preserve study history and record table and figure rendering snapshots
- `fd8d2ba` hardening-fusion: prevent motion stitching across detected identity boundaries

The indentation defect was caught during regeneration before output writes and
corrected. Derived data/audit and clean-render artifacts are packaged in the
subsequent local commits. Final delivery HEAD and the complete commit list are
reported with the handoff; `git log --oneline 11dbc6d..HEAD` gives the same list.
The clean rendering execution commit is recorded in
`results/artifact_provenance.json`; the later packaging commit does not rename it.

## Replay presentation

Physical anonymous boxes carry only **U1**. Sidebar rows are **U1 seen by A,B**.
Numerical uncertainty/circles, dimensions, speed, fit method and source lists
were removed from the standard anonymous display. Scientific values remain in
the entity trajectory/footprint/covariance and source structures. Member radar
points retain observer colours. Identity-ambiguous support is shown as points
without asserting a physical ghost box.

Help is two compact rows: SPACE play/pause, arrows seek, N/P event, C camera,
TAB vehicle, T tracks, G ghosts, H help, ESC quit. Other controls remain in the
README. The 143 reviewed keyframes show compact U labels: S17 has one U1 through
cut-in/swerve/contact; S18 passing has two separate anonymous bodies. Known
abreast/platoon startup fragments and post-impact S08/S15 ghosts remain WARN.
Interactive CARLA camera/controls are prepared for Andrea's final manual check;
the completed visual inspection here is of exported replay frames.

## S18 and fusion

There were **three erroneous pairs in two sweep runs**, seeds 16 and 28,
not three runs. Seed 16's C track stitched to a D successor, creating two
false pairs through a correct cross-observer link. Seed 28's local D→C
contamination made an early D overlap apply to the whole track. Exact parameters,
intervals, sources and evidence are in [s18_false_merges.md](s18_false_merges.md).

| scope | correct / false / missed before | after | entities before → after |
|---|---|---|---|
| S18 adjacent (40) | 143 / 3 / 51 | 159 / 0 / 83 | 98 → 107 |
| S18 platoon (40) | 101 / 0 / 128 | 103 / 0 / 126 | 144 → 145 |
| all saved sweeps (240) | 313 / 3 / 187 | 335 / 0 / 239 | 348 → 381 |
| canonical (17) | 15 / 0 / 10 | 23 / 0 / 16 | 14 → 19 |

The general policy adds lateral face/velocity consistency to stitching, segments
persistently incompatible transverse return support, and refuses motion-only
stitches across detected identity boundaries. No scenario branch or GT identity
is used. The first complete audit exposed two new pairs in a non-crash S17 sweep;
the endpoint veto removed both before acceptance. Final false pairs=0 everywhere.

There is a real cost: +32 adjacent missed pairs and +52 across sweeps. New
segments increase total pair trials 503→574; correct-merge recall among true
pairs is 62.6%→58.4%, and entity count rises 9.5%. Evaluated impure fused states
fall 412/23502→202/23242 (sweeps), 107/925→49/958 (canonical). This tradeoff is
retained explicitly; zero majority-pair false merges does not prove all samples
pure. S17 still has one U1, three correct pairs, zero false/missed and unchanged
events. S16's known short fragment/events are unchanged. S08's C alignment and
all true canonical contacts are preserved. Canonical recorder links: 42 correct,
0 wrong, 3 missed → 44 correct, 0 wrong, 7 missed (segmented-track units).

## Identity switches and semantics

[track_identity_switch.md](track_identity_switch.md) records original switch
times, innovations, return changes, segment limits and residual failures.
S08 C:track_002 still lacks sufficient independent switch evidence and remains
anonymous; C:track_001 is partially segmented. S15 B:track_001 is segmented around
contact, but the handoff begins just before detectable wide support. S18 early
D→C ambiguity is segmented; ambiguous state is UNKNOWN, not a cut-in/path entry.

For the four targeted cases (S08, S15, S18 abreast/passing), whole-recording extra
cut-in/path/critical-start/end events against COVERAGE fall **9→4**; missed events
remain **21→21**. S18 false cut-in/path-entry starts disappear in both variants.
Canonical pre-contact path extras 5→3, cut-in extras 2→0; their missed counts stay
8 and 4. Critical onset extras/misses change 1/2→2/3 due to one delayed abreast
onset; whole-recording onset matches remain 39/44. TRACK_APPEARED extras increase
23→33 as segments are local tracks. These costs remain in the metric.
Across sweeps, pre-contact path extras/misses 15/121→5/122; right cut-in
11/76→5/76; critical onset 37/34→36/37. The unchanged oracle window is 2 s,
and majority track identity is a privileged attribution approximation, not
an event-time proof. Complete counts: [hardening_before_after.json](hardening_before_after.json).

## Collision matching and impulse

The old fixed 10% relative gate made CARLA's symmetric contact impulses a brittle
identifier. The new geometry-supported gate uses
`abs(I1-I2)/(impulse_relative_std*hypot(I1,I2)) <= impulse_sigma_gate`, default
0.10 per report and 3 sigma. This is a configurable **engineering uncertainty
budget**, not a realistic sensor specification inferred from CARLA; no reviewed
source establishes a real collision-impulse accuracy. Without geometry the
legacy conservative gate remains. Zero/non-finite impulses provide no identity.

Candidate contact geometry, pre-contact radar/body compatibility, feasible
one-to-one assignments and clock consistency constrain pairing. Only edges
present in every maximum feasible assignment are selected; equally supported
partners remain unmatched. The bounded search is conservative on exhaustion.
Known-offset merged bursts and multi-hop collision chains remain supported.

| noise | old recall | new recall / matched true contacts | old aligned runs | new aligned runs | new false matches |
|---|---:|---|---:|---|---:|
| baseline | 100% | 100%, 22/22 | 100% | 17/17 | 0 |
| 2% | 100% | 100%, 66/66 | 100% | 51/51 | 0 |
| 5% | 98.48% | 100%, 66/66 | 100% | 51/51 | 0 |
| 10% | 41.48% | 100%, 66/66 | 86.76% | 51/51 | 0 |
| 20% | 28.98% | 98.48%, 65/66 | 83.82% | 51/51 | 0 |

Baseline plus impulse only: 221 jobs, plus 13 targeted passing jobs after the
final stitch veto. The adaptive rule stopped the refreshed stochastic levels
at three seeds; old 10%/20% used eight. These are study aggregates, not paired
eight-seed significance claims. One conservative unmatched contact remains at
20%; false collision matches do not increase. Canonical baseline preserves all
22/22 true contacts. Other robustness families were not rerun.

## Provenance and scope

Original `c80eab4` + `git_dirty: true` records are retained, including recording
objects. The historical SHA-256 `b5cbbff6...` is verified against committed Git
path/content objects at `ea0ccb1` and `11dbc6d`: `src/cdf/**/*.py` and root config
YAML, with newline normalization. Thirteen historical records gain
`analysis_code_sha256` and `equivalent_clean_commit`; dirty is never changed to
false. This scope proves runtime/config equivalence, not arbitrary untracked
files or every driver script. Evidence: [provenance_equivalence.json](provenance_equivalence.json).

Reanalysis histories retain old metrics/provenance. Current aggregate records
preserve their actual source snapshots; final patch scope is in
[final_patch_scope.json](final_patch_scope.json). All 257 saved reconstructions
were refreshed; the nine outputs eligible for the final stitch-only change were
refreshed again. Robustness `family_provenance` and analysis history distinguish
baseline/impulse from historical families; sensitivity, sample-size and legacy
impulse-symmetry studies keep original execution provenance. Historical families'
job records remain unchanged. No new 240-run acquisition or 1389-job rerun.

Final tables and every figure are rendered from a clean committed HEAD into an
ignored staging directory, verified, then copied into `results/` and committed.
`artifact_provenance.json` records `git_dirty: false`, source/config/script hashes,
rendering commit and input-study provenance. Clean rendering does not relabel the
historical scientific executions. Tables explicitly identify mixed/historical
studies; the old impulse-survival table is labelled legacy.

## Independent oracle subset

Separate direct GT oriented-body geometry, outline sampling, SAT and explicit
braking/cut-in/path predicates; no reconstruction/oracle event-generator import.
Six stratified runs: S01 rear-end, S02 cut-in, S03 crossing, S17, S18 passing,
non-crash crossing sweep seed 0. Of 23 first onsets, 17 are exact; one path
entry differs 0.05 s; five critical onsets differ 0.10–0.50 s. All first onsets
are found. Evaluation-only ablations diagnose yaw-rate vs straight forecast,
surface placement and braking conventions; no definition is tuned to agree.
See [event_oracle_independent_check.md](event_oracle_independent_check.md).
This small check detects no obvious implementation error, but does not validate
all definitions, post-impact ends or real-world avoidance/causality claims.

## Visual handoff and integrity

All 17 canonical replay outputs and keyframes refreshed; every exported PNG
inspected in 33 contact sheets: **143 frames; 11 PASS, 6 WARN, 0 FAIL**.
WARN only S08, S15, S16 and three S18 variants, for the documented handoff,
post-impact heading/fragment and startup duplication modes. Each finding links
to a frame. [Final visual audit](../../traces/visual_audit_final.md) and
[Andrea's short checklist](../manual_replay_checklist.md) give all commands and
2–4 t_global moments per run. Andrea's interactive check remains pending.

SHA-256 verification covers **8,342 raw files**, unchanged; all **240 recording
manifest objects** unchanged. Initial/final raw manifest digests are identical.
Evidence: [raw_integrity.json](raw_integrity.json). Working tree is left clean
after final local packaging commits. No reset or push; no existing edits lost.

Reconstruction GT access: **NO**. Fusion GT access: **NO**. Replay GT access:
**NO**. GT evaluation only: **YES**. LLM API calls: **ZERO**. Push: **NO**.
No paper, related work, clock-drift, combined perturbation or real-world study.
Work stops at this handoff.
