# Replay and dense-scenario review (S16, S18, S19-S24)

Branch `final-uncertainty-hardening`, Python 3.14 only, no campaign run.  Ground truth appears in this document
only through privileged scenario checks (`scripts/check_scenario_run.py`, `scripts/scenario_density.py`) and the
evaluation; reconstruction and replay never read it (`tests/test_replay_standard_ui.py::NoGroundTruthTests`
replays a run copy without `ground_truth/`).

## 1. Why S19-S24 showed no reconstructed boxes and no events (diagnosis before any change)

| scenario | physical vehicles | recorders | local tracks | global entities | semantic events | boxes expected (max at once) | boxes drawable | root cause |
|---|--:|---|--:|--:|--:|--:|--:|---|
| S16 consequential | 3 | A, B, C | 7 | 1 | 63 | 1 | 1 | works; C drawn through several radar dots (section 4) |
| S18 abreast | 4 | A, B | 9 | 4 | 51 | 3 | 3 | works (one identity-ambiguous entity is not drawn by design) |
| S18 passing | 4 | A, B | 8 | 2 | 46 | 2 | 2 | works |
| S18 platoon | 4 | A, B | 9 | 4 | 48 | 3 | 3 | works |
| S19-S24 (`traces/`) | 8-10 | A, B | 0 | 0 | 0 | 0 | 0 | **F: no `reconstruction/` folder**: `ReplayRun` fell back to the source clocks with notes "no local_graph.json; no events shown" |
| S19 reconstructed | 9 | A, B | 24 | 15 | 78 | 8 | 7 | + **D**: 66 event lines pushed out of the panel |
| S20 reconstructed | 10 | A, B | 19 | 11 | 68 | 8 | 8 | + D: 64 |
| S21 reconstructed | 9 | A, B | 23 | 15 | 110 | 8 | 8 | + D: 100 |
| S22 reconstructed | 8 | A, B | 20 | 7 | 96 | 5 | 5 | + D: 50 |
| S23 reconstructed | 8 | A, B | 20 | 9 | 91 | 7 | 7 | + D: 9 |
| S24 reconstructed | 8 | A, B | 19 | 12 | 77 | 9 | 9 | + D: 47 |

* **F (data):** the dense runs were acquired and reconstructed only on copies (`scratch/review`); the canonical
  `traces/S19..S24/run_0` held raw data only.  Every layer of the replay was fine: there was nothing to load.
  Fixed by the canonical reconstruction and evaluation of S19-S24 (same default configuration and refresh as
  every other canonical run; raw files untouched).  The viewer now says so in the HUD and the log when a run
  has no reconstruction.
* **D (presentation):** the recorder panel listed the perceived state of every local track (including UNKNOWN
  ones, with '?'), then an "anonymous tracks" inventory, then a row per road user, and the events LAST; in a
  dense scene (18-25 lines per panel) the events fell beyond the truncation.  S16/S18 never exceeded the room.
* Not a cause: entity drawing (`entities_at`), camera projection, drawing order, alpha.  Entities marked
  `identity_ambiguous` are deliberately not drawn as boxes (S18 abreast 1, S19 2, S21 1, S24 1).

## 2. Standard interface (after)

* Recorder panels: recent semantic events first (newest first, named by global subject), then confirmed
  important states per global road user (CRITICAL_TTC, CUT_IN, IN_EGO_PATH; one line per road user however many
  local tracks contribute), then the recorder's braking/stop/turn; at most 8 lines (`... +N more`), at most 360 px
  wide.  Over every 0.1 s of the ten runs: at most 8 lines, no '?' and no PREDICTED text, no recent event lost.
* Removed from the standard interface: UNKNOWN '?' states, "(PREDICTED)" / "PREDICTED", the "anonymous tracks:"
  inventory, a second label on the radar dots of a recorder (its badge names it; one observer line per
  recorder).  Reconstruction files and `ReplayRun` debug data are unchanged.
* C cycles overview -> follow every recorder vehicle -> free -> overview (TAB kept); reconstructed road users are
  not part of the cycle.  No CARLA actor is created for an anonymous road user (unchanged: only `run.participants`,
  the recorders, are spawned).
* The interactive viewer needs the CARLA client library (only in the CARLA Python environment); it was validated
  headlessly here (its own methods with stubs, `tests/test_replay_standard_ui.py`) and through the headless export
  (`S20_canonical_replay_tgm000.20.png`: U1-U7 around A and B).

## 3. S24: CRITICAL_TTC after the contact

Case B (a regression, same pair), in two forms, both fixed generally:
* METHOD 3 FINAL (earlier commits `30e54a5`, `b546bcb`): a second local track of B touching A, and the partner's
  hold released while still touching.
* Canonical METHOD 1: `A:track_008` (another face of B, 1.5 m away, linked to B with same-body evidence) started
  a CRITICAL_TTC 0.45 s after the contact.  Only the fusion knows it is B, so the rule lives in the global graph
  (`fusion.post_contact_episodes`): after a matched X-Y collision, an episode X starts on a track identified as
  Y is not asserted while some track of X identified as Y is still within the touching distance.  The local
  graph keeps the event.  Only S24 changes among the canonical runs; every canonical run is checked by
  `tests/test_post_contact_global.py`.

## 4. S16: several tracks associated with C

| observer | tracks -> C (before = after) | overlap | how linked | same-body evidence | true vehicle (evaluation) |
|---|---|---|---|---|---|
| A | track_001 (0.0-11.9 s), track_002 (0.1-6.7 s) | 6.6 s | track_001 by the collision (touching), track_002 by its returns on C's footprint (median 0.00 m) | split test: 132 instants, 100 % pass | C, C |
| B | track_002 (0.0-11.9 s), track_003 (0.9-5.5 s) | 4.6 s | both by C's footprint | split test: 48 instants, 97.9 % pass | C, C |

Classification: **1, legitimate simultaneous split tracks of one physical C** (two faces, two tracks), shown
in the replay as several dots and labels "→ C" (presentation duplication).  But the code had no protection:
`link_to_recorders` accepted each track alone, so two simultaneous tracks of one observer could both have been
asserted as C without any evidence of being one body.  Generic fix (`anonymous.exclusive_recorder_links`, all
association methods): two overlapping tracks of one observer may both carry recorder R only with explicit
same-body evidence (the split test, or both on R's outline at the same instants with 3 sigma no wider than a
body); otherwise a collision decision keeps R, a dominating footprint link keeps R, ambiguous links are both
refused; a re-acquisition after a gap never competes.  S16 associations are byte-identical before and after
(the evidence is there); every canonical METHOD 1 output and METHOD 3 FINAL on the 23 runs (exact) are
unchanged.  The replay now shows C once (its badge), one line per observer.

## 5. S18

The standard panels are global-subject oriented (one line per road user), so the several local tracks of one
road user no longer appear as several rows; distinct road users (separate entities) are kept.  Two boxes for one
physical car remain when the reconstruction itself did not merge two tracks (a missed merge, visible on
purpose, not hidden).

## 6. Are S19-S24 physically dense? (`results/final_hardening/replay_review/scenario_density.md`)

| scenario | non-recorders within 15 m (mean / max) | within 30 m | closest | around the recorders | case |
|---|---|---|--:|---|---|
| S19 | 0.87 / 1 | 3.35 / 4 | 14.4 m | all ahead | **2: sparse near A and B** |
| S20 | 4.92 / 5 | 7.98 / 8 | 3.5 m | ahead, alongside, behind | 1 |
| S21 | 1.59 / 2 | 4.26 / 5 | 5.3 m | ahead 75 %, behind 18 %, alongside 7 % | 1 (moderate) |
| S22 | 1.41 / 3 | 5.0 / 5 | 3.5 m | ahead 47 %, behind 40 % | 1 |
| S23 | 1.3 / 3 | 2.7 / 4 | 3.5 m | C, D, E go far -> near | 1 (H never within 50 m) |
| S24 | 3.98 / 4 | 6.0 / 6 | 3.5 m | alongside 46 % | 1 |

S20-S24 were dense already (case 1: only the pipeline/viewer was fixed, geometry unchanged).  S19 is case 2: its
three abreast rows are all ahead and nothing else comes within 14 m of the recorders.  Its improved geometry is
prepared as a new variant (`configs/scenarios/s19_dense_abreast.yaml`, variant `surrounded`: a car diagonally
ahead-left of B and a braking row of three cars 12-14 m behind) but NOT acquired: acquisition needs the CARLA
client library (the CARLA Python environment), outside the Python 3.14-only rule of this phase.
`traces/S19/run_0` stays as it is.

## 7. Semantic events per recorder (canonical reconstruction)

| scenario | rec | APPEARED F/L/R | LOST | CLOSING S/E | EGO_PATH in/out | CUT_IN L/R | CRITICAL S/E | BRAKE S/E | THROTTLE S/E | TURN L/R | COLLISION | STOP |
|---|---|---|--:|---|---|---|---|---|---|---|--:|--:|
| S19 | A | 6/6/1 | 7 | 1/1 | 4/4 | 0/1 | 5/2 | 0/0 | 1/1 | 0/0 | 1 | 0 |
| S19 | B | 3/4/4 | 6 | 1/1 | 4/2 | 0/1 | 4/2 | 0/0 | 1/1 | 0/0 | 1 | 0 |
| S20 | A | 2/5/3 | 6 | 2/2 | 3/4 | 0/1 | 3/3 | 2/1 | 1/1 | 0/0 | 1 | 1 |
| S20 | B | 1/4/4 | 8 | 1/1 | 0/0 | 0/0 | 1/1 | 0/0 | 1/1 | 0/0 | 1 | 0 |
| S21 | A | 4/4/5 | 8 | 5/4 | 5/7 | 0/0 | 4/2 | 1/0 | 1/1 | 0/0 | 1 | 1 |
| S21 | B | 2/1/7 | 6 | 7/6 | 5/4 | 0/3 | 3/3 | 1/0 | 1/1 | 0/0 | 1 | 1 |
| S22 | A | 2/6/2 | 6 | 4/3 | 4/3 | 1/0 | 4/3 | 1/0 | 1/1 | 1/0 | 1 | 1 |
| S22 | B | 3/0/7 | 8 | 4/3 | 4/2 | 0/1 | 4/2 | 1/0 | 1/1 | 1/0 | 1 | 1 |
| S23 | A | 3/1/5 | 5 | 8/5 | 1/0 | 0/2 | 5/5 | 1/0 | 1/1 | 0/0 | 1 | 1 |
| S23 | B | 1/0/10 | 7 | 8/5 | 1/1 | 0/0 | 1/1 | 1/0 | 1/1 | 0/0 | 1 | 1 |
| S24 | A | 4/5/3 | 11 | 7/5 | 0/1 | 0/1 | 2/1 (global 1/1) | 1/0 | 1/1 | 0/0 | 1 | 1 |
| S24 | B | 1/4/2 | 2 | 2/2 | 1/1 | 0/1 | 3/3 | 1/0 | 1/1 | 0/0 | 1 | 1 |

Counts from the local graphs.  S24 A: the local graph keeps the post-contact start on track_008 (2/1); the global
graph asserts one pre-impact episode (start -5.9 s, end 0.0 s at the contact).
Straight three-lane road: TURN only where a recorder changes lane enough (S22).  Nothing was added to raise counts.
