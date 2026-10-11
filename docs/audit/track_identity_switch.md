# Track identity switches and semantic costs

GT is used only to diagnose/evaluate the saved reconstruction. Runtime detection
uses radar returns and estimated motion. Position innovations alone are weak:
at the known switches the old tracker remains close to the next body, so a
large-jump threshold would miss them. Five persistently wide transverse return
sweeps flag support inconsistent with one car/van envelope. The uncertain bout
is padded by the existing tracking gap; before/after segments are independently
smoothed, with `parent_track` and `identity_ambiguous` retained in the files.

| case | privileged switch diagnosis (t_local) | reconstruction-only handling / remaining limit |
|---|---|---|
| S08 C:track_002 | B→A at 4.50; innovation 0.353 m, returns 39→31 | Insufficient persistent wide support: remains anonymous; residual path event/ghost duplication is WARN. Related C:track_001 A→B at 4.15, then B→A at 6.00 is split into 0–3.65, ambiguous 3.70–5.05, and 5.10–15.15. Its last segment can still contain a handoff. C stays aligned. |
| S15 B:track_001 | C→A at 4.55; innovation 0.364 m, returns 20→23 | Segments 1.70–4.60, ambiguous 4.65–5.95, 6.00–13.95. The true handoff begins just before the detectable bout; detection is not complete. Early stable segment links to C, later remains anonymous. |
| S18 abreast A:track_001 | D→C at 2.55; innovation 0.270 m, returns 11→17 | Segments 0–0.25, ambiguous 0.30–3.40, 3.45–10.20. Early switch-generated cut-in/path entry disappear. |
| S18 passing A:track_001 | D→C at 3.35; innovation 2.097 m, returns 19→28 | Segments 0–1.90, ambiguous 1.95–4.25, 4.30–10.20. Early switch-generated cut-in/path entry disappear; two physical anonymous bodies remain. |

During ambiguous support, path/cut-in/hazard states are UNKNOWN; radar points
remain visible and no physical ghost box is asserted. There is no silent
association of a segment to a true vehicle. The rule can also flag uncertain
heading while a single body turns/slides after impact; it is an uncertainty test,
not proof of two bodies. Ordinary raw samples, covariance, uncertainty, dimensions,
fit method and source tracks remain available.

The table counts **CUT_IN start, EGO_PATH_ENTRY, CRITICAL_TTC start/end**, whole
recording, against COVERAGE with the unchanged 2 s one-to-one matching window.
An extra event is an operational false positive under that definition, not a
statement of physical responsibility. TRACK_APPEARED is reported separately.

| canonical case | extra core events before → after | missed core events before → after | anonymous entities before → after |
|---|---|---|---|
| S08 | 2 → 2 | 5 → 5 | 1 → 3 |
| S15 | 2 → 1 | 2 → 2 | 1 → 2 |
| S18 abreast | 2 → 1 | 7 → 8 | 3 → 4 |
| S18 passing | 3 → 0 | 7 → 6 | 3 → 3 |
| four targeted cases | 9 → 4 | 21 → 21 | 8 → 12 |

Across all 17 canonical runs, pre-contact extra path entries 5→3, cut-in starts
2→0; missed path/cut-in counts are unchanged (8 and 4). CRITICAL_TTC onsets have
extra 1→2, missed 2→3 (one delayed onset in abreast); whole-recording critical
onset matches stay 39/44. TRACK_APPEARED extras increase 23→33 because segments
are separate local tracks. This cost is retained, not omitted from the oracle.

Across 240 sweeps, pre-contact path extras 15→5 (missed 121→122), right cut-in
extras 11→5 (missed 76→76), critical onset extras 37→36 (missed 34→37).
Whole-recording TRACK_APPEARED extras 261→307; identity segmentation increases
fragmentation. Full event-by-event pre-contact/whole counts and original majority
identity mapping are in [hardening_before_after.json](hardening_before_after.json).
The overall policy reduces false semantic claims while retaining the known S08,
S15 and delayed S18 limitations; it does not assert complete identity recovery.
