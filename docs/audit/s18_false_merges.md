# S18: the three original false merge pairs

The original count is **three erroneous track pairs in two runs**, not three
runs. All use `anonymous_pair_adjacent`, scenario S18, base `abreast`;
C and D do not record. The pair-based evaluator labels tracks by majority GT
identity after reconstruction. GT below is privileged diagnosis only.

| false pair | run / seed | source tracks and interval (local seconds) | original evidence / cause |
|---|---|---|---|
| 1 | `run_16_anonymous_pair_adjacent_016`, seed 16 | A:track_003=C, 0.25–9.40; A:track_004=D, 10.40–11.95 | Same-observer stitch: gap 1.00 s, predicted centre miss 3.410 m, position chi2 1.156, velocity chi2 0.319. Isotropic acceleration uncertainty admitted a lateral body jump. |
| 2 | same run / seed 16 | B:track_002=C, 0–8.95; A:track_004=D, 10.40–11.95 | Transitive consequence of pair 1: correct cross-observer A:track_003–B:track_002 joined the wrong successor into their entity. No direct evidence for this pair. |
| 3 | `run_28_anonymous_pair_adjacent_028`, seed 28 | A:track_001, 0–10.20, D until 2.55 then C; B:track_004=D, 0.30–1.65 | Cross-observer match: 25 shared samples, passed 1.000, box chi2 0.216, velocity chi2 1.089, centre gap 0.288 m. Early overlap correctly resembled D, but a contaminated full local track was treated as one persistent body (majority C, purity 0.732). |

Parameters: seed 16 D forward=38.39 m, initial/target speed=12.29 m/s,
B forward=11.30 m; seed 28 D forward=40.64 m, initial/target speed=11.80 m/s,
B forward=12.50 m. Other parameters follow the unchanged sweep definition.
Original entity U2 in seed 16 contained C and D; original U1 in seed 28 did too.
These were not clock-alignment failures or evidence of C/D sharing one body.

The general fix checks lateral stitch displacement with face/velocity covariance,
without the gap's isotropic acceleration allowance. Seed 16 now has lateral
chi2=10.948, above the existing 99% 2-dof gate 9.210: the stitch is refused.
Persistent transverse radar support outside the declared car/van envelope
segments the mixed track in seed 28; ambiguous support cannot associate or
generate path/hazard claims. Stable D and C portions use actual shared samples.
Detected segment endpoints cannot motion-stitch to siblings or other local IDs.
There is no scenario ID or true identity in these rules; engineering choices are
in [hardening_assumptions.md](hardening_assumptions.md).

| scope | correct / false / missed before | correct / false / missed after | anonymous entities before → after |
|---|---|---|---|
| seed 16 | 2 / 2 / 2 | 4 / 0 / 7 | pair trial counts change after segmentation |
| seed 28 | 2 / 1 / 4 | 6 / 0 / 7 | pair trial counts change after segmentation |
| adjacent, 40 runs | 143 / 3 / 51 | 159 / 0 / 83 | 98 → 107 |
| platoon, 40 runs | 101 / 0 / 128 | 103 / 0 / 126 | 144 → 145 |
| all six sweeps, 240 runs | 313 / 3 / 187 | 335 / 0 / 239 | 348 → 381 |
| all 17 canonical | 15 / 0 / 10 | 23 / 0 / 16 | 14 → 19 |

The missed count is not hidden: adjacent +32, all sweeps +52. New segments add
same-identity pairs to the denominator (503 → 574 total sweep trials).
Correct-merge recall among true pairs changes from 62.6% to 58.4%; entity count
increases 9.5%. The fix is retained for explicit identity uncertainty and reduced
contamination, not as a claim of universal recall improvement. Evaluated impure
fused states fall from 412/23502 to 202/23242 in sweeps, and 107/925 to 49/958 in
canonical runs. Majority-pair false merges=0 does **not** mean all track samples
have pure identity; seed 16's later stable segment still has purity 0.652.

S17 remains one U1, three correct merged pairs, zero false/missed; its semantic
events are unchanged. S16 has the same events and one short anonymous fragment.
S08 preserves C alignment but remains WARN for residual contact handoffs.
All canonical S18 remain at zero false pairs; abreast/platoon still have known
startup fragmentation, and passing has two simultaneous physical bodies.

The first full reanalysis exposed two new erroneous pairs in one S17 cut-in sweep
(`run_27_unobserved_cut_in_027`): a motion-only stitch from a newly segmented
endpoint. The final endpoint veto removed both. The final patch affected only
nine saved runs (one canonical, eight sweeps), which were refreshed; 13 affected
baseline/impulse jobs for canonical passing were refreshed too. No recording was
repeated. Full metric snapshots: [hardening_before_after.json](hardening_before_after.json).
