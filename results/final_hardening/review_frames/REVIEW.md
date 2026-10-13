# S19-S24 review before the definitive campaign

Reconstruction: METHOD 3 FINAL (uncertainty-normalised tracker), exact poses, nominal radar, one clean run per
scenario.  Raw recordings untouched (reconstructed on copies).  Frames: `<S>/pair_*.png` (left: reconstruction-only
replay; right: ground truth, evaluation only) and `<S>/SHEET.png`; event-driven audit frames and flags in
`../visual_audit_review/`; per-car local tracks and entities in `IDENTITY_REPORT.md`; model-only gates in
`../uncertainty_tables.md`.  NO perturbation campaign was run.

## Structure (configs + privileged scenario check `scripts/check_scenario_run.py`)

| scenario | physical vehicles | recorders | record:false | lanes | manoeuvre | intended collision | contacts (ground truth) | other collisions | purpose |
|---|--:|---|--:|---|---|---|---|---|---|
| S19 dense_abreast | 9 | A (right), B (middle) | 7 | 3, one way | three abreast rows at 12 m/s, ~15 m headway; A drifts left 2 s from 6.0 s | A-B sideswipe | A-B at 7.75 s | none | abreast pairs kept apart, one partner |
| S20 dense_platoon | 10 | A, B (middle column) | 8 | 3 | column C, D, A, B at 12 m headway + 3 staggered cars per side lane; A brakes hard at 6 s | B rear-ends A | A-B at 7.45 s | none | occlusions in a column, no same/adjacent-lane merge |
| S21 dense_overtaking | 9 | A (middle), B (left) | 7 | 3 at 10 / 12 / 14 m/s | B overtakes A; A drifts left over 3 s from 4.5 s | A-B sideswipe while passing | A-B at 6.75 s | none | identity through passes |
| S22 occlusion_reappearance | 8 | A (right), B (left) | 6 (incl. van V) | 3 | V hides B from A, accelerates at 3 s; A and B both move into the middle at 4.8 s; F, G brake at 8 s | A-B merging | A-B at 7.3 s | none | same identity of B before/after occlusion |
| S23 far_to_near | 8 | A (middle), B (left) | 6 | 3 (right lane 6 m/s) | C, D abreast 70 m ahead at 6 m/s; A, B close at 13 m/s; A swerves left at 6.8 s | A-B after A avoids C | A-B at 8.5 s | none | far identities unresolved, resolved when near |
| S24 collision_ambiguity | 8 | A, B (middle) | 6 | 3 at 11 m/s | B between C and D (1.6 m gaps); A 2 m/s faster behind B | A rear-ends B | A-B at 7.75 s | none | partner B, not C or D |

Every run: exactly one vehicle contact (A-B), no contact with the road edge, no car standing without a crash.
Closest other approaches 1.3-1.5 m (abreast pairs in adjacent lanes).  Observations for the review:
* S21: the other cars stay 20-40 m from the recorders at the contact: the overtaking traffic is mostly ahead,
  less dense around A and B than the description suggests.
* S23: the far pair C/D is visible to the recorders only intermittently at 50-70 m.
* S24: after the impact A yaws towards D (U7), which starts a new CRITICAL_TTC of a different pair.

## Reconstruction (one clean run each)

| scenario | verdict | collision | local tracks | global anonymous entities | single-track entities | tracks resolved retrospectively | false merges | missed merges | duplicate entities | cars fragmented INSIDE relevance | cars fragmented outside only | wrong samples |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|---|---|--:|
| S19 | WARN | A-B correct | 24 | 17 | 12 | 10 | 0 | 21 | 10 | C, E, F, G, H | J | 5 / 1258 |
| S20 | WARN | A-B correct | 20 | 14 | 9 | 10 | 0 | 8 | 4 | E, G | F | 0 / 1280 |
| S21 | WARN | A-B correct | 21 | 14 | 10 | 7 | 0 | 14 | 7 | E, G | I | 16 / 1117 |
| S22 | WARN | A-B correct | 17 | 9 | 6 | 9 | 0 | 4 | 3 | G | E | 0 / 924 |
| S23 | FAIL | A-B correct | 24 | 11 | 5 | 17 | 0 | 22 | 6 | C, D | - | 2 / 802 |
| S24 | WARN | A-B correct | 21 | 15 | 11 | 8 | 0 | 14 | 8 | B, C, D, E, F, H | - | 4 / 1010 |

Fragmentation outside the relevance envelope (a car that never matters split into several entities) is
acceptable by design.  Fragmentation INSIDE it is not, and remains: S23 (C and D, which A swerves around, 4
entities each), S24 (A's view of B, the partner, 3 entities; D, E, F likewise), S19 (relevant row cars).  The
cause seen in S10: a crossing or closely interacting target's track ends after a few missing sweeps (its
prediction uncertainty exceeds a car width), and the next track of the same car is not stitched to it.

## Known cases

| case | result |
|---|---|
| S06 seed 0, seed 3 (consumer + 10 % impulse) | no wrong collision pairing (recorded-run tests) |
| S06 a_front_pushed / b_rear_first (exact) | PASS: all contacts named, correct links |
| S10 rolls_through | collision matched, no wrong collision, recorder links kept (3 correct, 1 early fragment missed) |
| S18 abreast / passing / platoon (exact and consumer, dev seed 200) | 0 false merges, 0 wrong samples, 2 correct links each |
| S24 post-contact CRITICAL_TTC A->B | cause: a second track of B touching A was not in the post-impact hold (and, in S18 platoon, the partner's hold was released while still touching); fixed generally, no same-pair episode after the contact |
