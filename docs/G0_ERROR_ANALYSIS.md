# G0 reconstruction on the 2026-10-22 canonical set: results and error analysis

Reconstruction code unchanged in G0 (the only reconstruction change of this branch affects perturbed GNSS only);
no threshold was changed.  Numbers: `results/g0_scorecard_20261022/scorecard.{md,json}` (`scripts/g0_scorecard.py`),
`docs/CANONICAL_VALIDATION.md`, `docs/STABILITY_AUDIT.md`.  Definitions: `cdf.evaluation.scorecard` docstring.

## Headline (22 runs, 95 vehicles, 27 true vehicle-vehicle contacts)

| family | result |
|---|---|
| Collisions | 27/27 detected, **27/27 with the correct participants**, 0 invented, timing error 0.00 s (all recorders aligned on collisions) |
| Completeness | 95/95 observable vehicles represented (every vehicle of the set is observable by the definition); **20 duplicates** (a vehicle split over 2-4 road users) in S14-S19, **1 recorder ghost** (S06), 0 phantoms |
| Position / speed of road users | median centre error 0.05-0.42 m per run, P95 0.20-1.10 m; speed median 0.02-0.07 m/s, P95 0.09-0.58 m/s (S06's 1.75 m is the recorder ghost, see below) |
| Association | 0 wrong recorder links, 0 false merges; 1 missed recorder link (S06); 43 missed merges (S14-S19, conservative: identities left unresolved) |
| CRITICAL_TTC | 43/43 justified warnings (the COVERAGE oracle also raises one about the partner within 8 s before the contact) arrive **before** the impact; lead time min 0.75 s, median 1.55 s.  The other 11 of the 54 (recorder, partner) cases have no warning and no oracle warning either (in most of them the recorder is the struck vehicle; to be confirmed in the viewers) |
| Path intrusions (EGO_PATH_ENTRY or CUT_IN, any order, 2 s) | 5 oracle intrusions not reported, 9 reported intrusions without oracle counterpart (list below) |
| Unconfirmed CRITICAL_TTC alarms | 2 (S14), candidates for visual review |

## How the collisions are identified, and what 27/27 means

* **Every true contact involves two recorders.**  All 27 true vehicle-vehicle contacts of the canonical set are
  between two recording vehicles: 16 runs have two recorders, 6 have three, and no contact involves a vehicle
  that records nothing.  Each participant's own collision sensor reports the contact with its time and impulse
  magnitude, and no partner identity.  `test_sensor_ground_truth_separation` checks this on all 50 recorder files.
* **Matching** (`cdf.reconstruction.alignment`).  Two reports from different recorders count as one contact when
  three conditions hold:
  * their peak impulses agree within 10 % (equal and opposite impulses, `impulse_tolerance`);
  * the two bodies touch in their own pose streams: within `contact_consistency_m` = 1.0 m, plus 3 sigma of the
    declared pose accuracy;
  * each recorder's radar view before the contact does not contradict the candidate partner's own speed.

  Each match fixes the clock offset between the two recorders, and t_global = 0 is the strongest matched contact.
  A later contact must agree with the offsets already fixed, within `clock_tolerance_s` = 0.1 s.
* **Consequences.**
  * The participants of a contact are named from both participants' own collision sensors.  The 27/27 measures the
    matching of collision reports across recorders, not the recognition of a non-recording partner by radar.
  * The timing error of 0.00 s holds by construction, because the clocks are aligned on the matched contacts
    themselves.  The later contacts of S04, S10 and S11 must agree with the fixed offsets, and in G0 they do exactly.
  * **Limit of the dataset.**  The set does not test a contact with a vehicle that records nothing, whether one
    recorder hits a non-recorder or two non-recorders hit each other.  Such a contact has at most one collision
    report, and whether the reconstruction would attribute it from radar is not measured here.  The paper must
    state this, or new scenarios must cover it.
  * **The campaign.**  Its GNSS and radar degradations leave the collision reports unchanged.  They can act on the
    matching only through the pose-consistency gate (GNSS) and the radar approach check, and the smoke test kept
    100 % identification at every level.  The condition that tests the matching itself is the `impulse` family
    (relative impulse noise 2-20 %, already implemented).  It is not among the v3 families: including it is a
    decision for the campaign.
* **Repeated contacts versus distinct incidents.**  A pause longer than `merge_gap_s` = 0.5 s always separates two
  contacts.  A weaker burst (< 1000 N s) within it continues the same contact (scraping, pushing).  The
  multi-contact runs are reconstructed with every contact detected and its pair identified:
  * S04 a_front_pushed: 3 contacts;
  * S04 b_rear_first: 2;
  * S10: 2;
  * S11: 2.

## Main errors, by importance

1. **Duplicated road users in dense traffic (S14, S15, S16, S17, S18, S19; 20 extra road users).**  A non-recording
   vehicle seen in separate track segments, or by both recorders without a confident merge, stays as two to four
   anonymous road users (`fragmented_vehicles` in the scorecard: e.g. S14 H = U6, U8, U10, U12).  The fusion refuses
   uncertain merges by design (0 false merges): the cost is completeness, not correctness.  This is the largest
   remaining G0 error with respect to "the correct number of vehicles".  It is the subject of the local experiment
   branch `experiment/robust-offline-association` (v2: 679 -> 761 of 1512 merges on its development set, safeguard
   policy left open); it was not merged here because it changes the reconstruction and requires its own validation.
2. **S06: recorder A drawn twice.**  C's track `track_002#segment_2` of A was not linked to recorder A ("missed
   link"), so A also appears as anonymous road user U1, 1.7-1.8 m from A's true centre.  Not a position error: an
   association miss in a multidirectional crossing.  Visible in the RECONSTRUCTION viewer.
3. **Path intrusions.**  Missed: S09 A/B 7.05 s, S10 A/B 3.60 s, S16 A/I 6.45 s, S17 A/E 6.30 s and B/E 6.35 s.
   Extra: S06 C/B 4.60, S13 (three variants) A/B 6.30, S14 A/G 11.35 and A/J 7.50, S16 A/I 9.20 and A/G 6.50.  The
   oracle is itself an idealisation (true nearest surface, true box): several of these are side views where the
   radar point slides along the body, or entries a few tenths of a second before a contact.  They need the visual
   check before being counted as reconstruction errors.
4. **S14 true cut-in not reported** (validation WARN: B by A at 6.5 s) and two unconfirmed CRITICAL_TTC starts
   (A/E 10.15 s, A/P 10.45 s, after the contact phase).

## Re-interpreting the earlier 84.8 % event figure

A single pooled event-match percentage mixes event types of very different forensic weight (frequent types such
as track appearances weigh as much as a collision warning), counts an oracle disagreement as a reconstruction error, and penalises a correct manoeuvre reported with
a different but equivalent event (CUT_IN versus EGO_PATH_ENTRY) or a few tenths of a second off.  It is no longer
reported as an accuracy.  The scorecard reports instead what the forensic question needs: whether every observable
critical situation was warned before the impact (43/43), whether intrusions are recognised in either form, and the
list of disagreements for visual review.

## What must be checked visually (both viewers)

S06 (recorder ghost U1), S14-S19 (duplicates), the intrusion disagreements above, S14 (cut-in and the two
unconfirmed alarms), S10 (new reproducible post-impact contact sequence A-C), S04 b_rear_first.
