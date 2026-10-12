> **Snapshot storico.** Per i sette run aggiornati vedere [follow-up](visual_audit_replay_followup.md); gli altri run non sono stati rigenerati.

# Visual audit (visual_audit_final)

One row per run: the reviewer's verdict on the reconstruction-only replay frames (details and frames in each run's reconstruction/evaluation/visual_audit_final.md).

| scenario | run | verdict | frames | automatic flags | summary |
|---|---|---|---|---|---|
| S01 | run_0_crash | PASS | 5 | 0 | Reconstruction-only QA: no anomaly. |
| S02 | run_0_crash | PASS | 7 | 0 | Reconstruction-only QA: no anomaly. |
| S02 | run_0_critical_before_cut_in | PASS | 9 | 0 | Reconstruction-only QA: no anomaly. |
| S03 | run_0_crash | PASS | 6 | 0 | Reconstruction-only QA: no anomaly. |
| S06 | run_0_a_front_pushed | PASS | 10 | 0 | Reconstruction-only QA: no anomaly. |
| S06 | run_0_b_rear_first | PASS | 8 | 0 | Reconstruction-only QA: no anomaly. |
| S07 | run_0_crash | PASS | 7 | 0 | Reconstruction-only QA: no anomaly. |
| S08 | run_0_crash | WARN | 8 | 5 | Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |
| S09 | run_0_merge_conflict | PASS | 7 | 0 | Reconstruction-only QA: no anomaly. |
| S10 | run_0_rolls_through | PASS | 8 | 0 | Reconstruction-only QA: no anomaly. |
| S12 | run_0_near_simultaneous | PASS | 7 | 0 | Reconstruction-only QA: no anomaly. |
| S15 | run_0_deflected_into_c | WARN | 11 | 2 | Contact handoff may begin before wide support is confirmed; post-impact fragments remain anonymous. |
| S16 | run_0_consequential | WARN | 14 | 0 | Short post-contact van fragment and C losing A before their contact remain documented limitations. |
| S17 | run_0_crash | PASS | 11 | 0 | Reconstruction-only QA: no anomaly. |
| S18 | run_0_abreast | WARN | 8 | 4 | Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |
| S18 | run_0_passing | WARN | 9 | 0 | Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |
| S18 | run_0_platoon | WARN | 8 | 1 | Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |

All 143 exported keyframes inspected. Verdicts: 11 PASS, 6 WARN, 0 FAIL.
Known WARN diagnoses: [track contamination](../docs/audit/track_identity_switch.md); [S18 fusion](../docs/audit/s18_false_merges.md).
Andrea interactive replay: [checklist](../docs/manual_replay_checklist.md).
