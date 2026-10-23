# RTK/5G preflight smoke report

Seed 0; recorded traces only; no CARLA server. status=complete means the job finished; quality metrics remain descriptive. Collision column is detected/true contacts and wrong participants. Link and merge columns are wrong/missed. Centre is fused trajectory median/P95 in metres (n/a means no fused centre samples). TTC is CRITICAL_TTC starts found/expected; CUT_IN is true positives/ground-truth positives. COLLISION is shown in the first metric column.

Jobs: 18 total, 18 complete, 0 failed.

## Baseline G0 and GNSS G1/G2

| Run | Profile | Status / s | Collisions; wrong participants | False collision matches | Links wrong/missed | Merges false/missed | Fragments | Centre median/P95 m | CRITICAL_TTC found/expected | CUT_IN TP/true |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S01/run_0_crash | G1 RTK | complete / 6.2400 | 1/1; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 1/1 | 0/0 |
| S01/run_0_crash | G2 degraded | complete / 6.2300 | 1/1; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 1/1 | 0/0 |
| S01/run_0_crash | G0 exact | complete / 9.4400 | 1/1; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 1/1 | 0/0 |
| S04/run_0_a_front_pushed | G1 RTK | complete / 12.2600 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| S04/run_0_a_front_pushed | G2 degraded | complete / 12.3700 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| S04/run_0_a_front_pushed | G0 exact | complete / 15.4800 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| S14/run_0_surrounded | G1 RTK | complete / 167.7700 | 1/1; wrong participants 0 | 0 | 0/0 | 0/5 | 0 | 0.1705/0.7708 | 9/8 | 0/0 |
| S14/run_0_surrounded | G2 degraded | complete / 165.0200 | 1/1; wrong participants 0 | 0 | 0/0 | 0/5 | 0 | 0.1855/0.7080 | 9/8 | 0/0 |
| S14/run_0_surrounded | G0 exact | complete / 94.9300 | 1/1; wrong participants 0 | 0 | 0/0 | 0/5 | 0 | 0.1483/0.7405 | 9/8 | 0/0 |
| S19/run_0_highway_curve | G1 RTK | complete / 42.6700 | 1/1; wrong participants 0 | 0 | 0/0 | 0/10 | 0 | 0.2481/0.7306 | 3/3 | 0/0 |
| S19/run_0_highway_curve | G2 degraded | complete / 42.4700 | 1/1; wrong participants 0 | 0 | 0/0 | 0/10 | 0 | 0.3094/0.7952 | 3/3 | 0/0 |
| S19/run_0_highway_curve | G0 exact | complete / 29.2500 | 1/1; wrong participants 0 | 0 | 0/0 | 0/10 | 0 | 0.2729/0.7278 | 3/3 | 0/0 |

G0 pose errors are exactly zero for position, heading and velocity. For each GNSS row below the five values are P50/P95/P99/P99.5/max. Units: position m, heading degrees, velocity m/s.

| Run | Profile | Position P50/P95/P99/P99.5/max | Heading P50/P95/P99/P99.5/max | Velocity P50/P95/P99/P99.5/max |
|---|---|---|---|---|
| S01/run_0_crash | G1 RTK | 0.0300/0.0499/0.0517/0.0518/0.0536 | 0.0279/0.0770/0.0903/0.1005/0.1183 | 0.0086/0.0233/0.0237/0.0238/0.0240 |
| S01/run_0_crash | G2 degraded | 0.2024/0.3267/0.3318/0.3326/0.3337 | 0.1409/0.4174/0.4549/0.4782/0.5016 | 0.0762/0.1218/0.1310/0.1327/0.1349 |
| S04/run_0_a_front_pushed | G1 RTK | 0.0133/0.0358/0.0398/0.0410/0.0452 | 0.0877/0.1508/0.1739/0.1765/0.1982 | 0.0150/0.0231/0.0236/0.0237/0.0240 |
| S04/run_0_a_front_pushed | G2 degraded | 0.2456/0.4914/0.5061/0.5101/0.5155 | 0.2230/0.4677/0.5223/0.5264/0.5388 | 0.0779/0.1219/0.1288/0.1311/0.1349 |
| S14/run_0_surrounded | G1 RTK | 0.0300/0.0499/0.0517/0.0518/0.0536 | 0.0279/0.0770/0.0903/0.1005/0.1183 | 0.0086/0.0233/0.0237/0.0238/0.0240 |
| S14/run_0_surrounded | G2 degraded | 0.2024/0.3267/0.3318/0.3326/0.3337 | 0.1409/0.4174/0.4549/0.4782/0.5016 | 0.0762/0.1218/0.1310/0.1327/0.1349 |
| S19/run_0_highway_curve | G1 RTK | 0.0300/0.0499/0.0517/0.0518/0.0536 | 0.0279/0.0770/0.0903/0.1005/0.1183 | 0.0086/0.0233/0.0237/0.0238/0.0240 |
| S19/run_0_highway_curve | G2 degraded | 0.2024/0.3267/0.3318/0.3326/0.3337 | 0.1409/0.4174/0.4549/0.4782/0.5016 | 0.0762/0.1218/0.1310/0.1327/0.1349 |

## Radar + GNSS on S04/run_0_a_front_pushed

GNSS error percentiles match the S04 G1/G2 rows above; radar does not alter the pose stream.

| GNSS + radar | Status / s | Collisions; wrong participants | False collision matches | Links wrong/missed | Merges false/missed | Fragments | Centre median/P95 m | CRITICAL_TTC found/expected | CUT_IN TP/true |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gnss rtk + radar low | complete / 16.3500 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| gnss rtk + radar nominal | complete / 15.6100 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| gnss rtk + radar high | complete / 268.3800 | 3/3; wrong participants 0 | 0 | 0/1 | 0/0 | 0 | 2.6852/3.2357 | 7/2 | 0/0 |
| gnss degraded + radar low | complete / 13.5400 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| gnss degraded + radar nominal | complete / 12.5400 | 3/3; wrong participants 0 | 0 | 0/0 | 0/0 | 0 | n/a/n/a | 2/2 | 0/0 |
| gnss degraded + radar high | complete / 265.8500 | 3/3; wrong participants 0 | 0 | 0/1 | 0/0 | 0 | 2.2848/3.0487 | 7/2 | 0/0 |

## Observations

- S14 reports one extra CRITICAL_TTC start (9 found / 8 expected) and 5 missed merges in G0/G1/G2; collision participants remain correct.
- S19 reports 10 missed merges in G0/G1/G2; collision participants remain correct.
- On S04, both high-radar combinations miss one link and report 7 CRITICAL_TTC starts against 2 expected. Fused centre median/P95 is 2.6852/3.2357 m for RTK+high and 2.2848/3.0487 m for G2+high.
- All six radar+GNSS jobs and all twelve baseline/GNSS jobs completed. These smoke observations do not replace multi-seed campaign estimates.

## Audit complementare

Data: 2026-10-21. Nessuna ricostruzione, soglia, registrazione canonica o risultato della campagna congelata  è stata modificata.

### 1. Failure dei test e confronto col commit originale

Checkout temporaneo detached al commit `1d596c1e499097e5cead7c1214a2588afd4ac3ba`, con checkout sparse di codice/test e una junction `traces` verso i dati canonici condivisi. Gli stessi cinque node ID sono stati eseguiti con Python Conda del progetto sia dal checkout originale sia dal working tree. Tutti e cinque falliscono in entrambi nello stesso confronto/assertion; sono quindi preesistenti e non regressioni GNSS.

| Test | Stato originale | Stato corrente | Assertion fallita |
|---|---|---|---|
| `test_retrospective.py::RealRunRegressions::test_reconstruction_matches_the_committed_one` | FAIL | FAIL | `assertEqual(committed["nodes"], mine["nodes"])`; prima differenza al nodo 7 (`track_002`/`track_003`). |
| `test_robustness.py::ReconstructionUnderPerturbationTests::test_constant_clock_offsets_leave_the_global_graph_unchanged` | FAIL | FAIL | `assertEqual(graph_signature(new), graph_signature(base))`; la firma contiene un `EGO_PATH_EXIT` in più e non coincide con la lista di eventi canonica. |
| `test_robustness.py::MutualRefinementTests::test_exact_pose_sources_are_not_refined` | FAIL | FAIL | La stessa uguaglianza di `graph_signature`; stesso tipo di discrepanza di eventi. |
| `test_worked_example.py::S12WorkedExampleTests::test_privileged_checks_pass_and_the_committed_report_is_current` | FAIL | FAIL | `assertEqual(committed.read_text(), fresh)`; il report rigenerato elenca file `DIFFERENT` rispetto al testo committed. |
| `test_worked_example.py::S12WorkedExampleTests::test_privileged_files_do_not_reach_the_reconstruction` | FAIL | FAIL | `assertTrue(result["identical"], result["different_files"])`; elenco: `A/local_graph.dot`, `A/local_graph.json`, `A/local_graph.md`, `A/local_trace.jsonl`, `B/local_graph.json`, `B/local_trace.jsonl`, `global/alignment.json`, `global/global_graph.dot`, `global/global_graph.json`, `global/global_graph.md`, `global/global_trace.jsonl`, `report.md`. |

Riproduzione: `python -m pytest -q --tb=short <i cinque node ID sopra>` eseguito una volta dalla root del checkout temporaneo e una dalla root del working tree, usando `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe`. Nel checkout originale il run è terminato con 5 failed in 111.68 s; nel working tree con 5 failed in 130.22 s. Nessuna assertion o baseline canonica  è stata alterata per nascondere questi failure.

### 2. pygame e ambiente

L'interprete usato in precedenza per la suite era il Python di sistema 3.14, privo di pygame. L'interprete del progetto è `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe`, Python 3.8.20, pygame 2.1.3, SDL 2.0.22; `pyproject.toml` ammette `pygame>=2.1,<2.7`. Non è servita alcuna reinstallazione o modifica dell'ambiente. Le sei prove che prima terminavano in errore di setup sono passate:

- `test_replay_focus_panel.py::FocusLayoutTests::test_focus_gives_the_selected_recorder_the_column_and_every_event`
- `test_replay_focus_panel.py::FocusLayoutTests::test_long_history_scrolls_through_every_event`
- `test_replay_focus_panel.py::FocusLayoutTests::test_others_collapsed_in_focus_and_restored_without_it`
- `test_replay_focus_panel.py::FocusLayoutTests::test_collision_banner_keeps_every_pair_clear_of_the_focused_panel`
- `test_replay_focus_panel.py::FocusLayoutTests::test_keys_f_toggles_and_tab_shows_the_new_recorder_newest_events`
- `test_replay_focus_panel.py::FocusLayoutTests::test_help_names_the_focus_key`

L'intero file `tests/test_replay_focus_panel.py` ha dato 13 passed e 3 warning di deprecazione.

### 3. Rumore della velocità

Il modello white interpolato originale è stato confrontato con il candidato Gauss-Markov su 512 seed nuovi (`400000–400511`) e traiettorie indipendenti di 10 e 20 secondi a 20 Hz. Il modello white è scalato analiticamente per la miscela delle fasi di interpolazione e poi validato con altri seed. Il bias temporaneo è la norma della media vettoriale 2D per traiettoria; intervalli al 95% con bootstrap delle traiettorie. Autocorrelazione lag-1 mediata su assi e traiettorie.

| Profilo / durata | Modello | Autocorr. lag-1 | Bias temporaneo medio [95% CI], m/s | RMS, m/s | P95, m/s | P99, m/s | P99.5, m/s | Massimo, m/s |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| G1 / 10 s | white interpolato | 0.6620 [0.6594, 0.6646] | 0.00096 [0.00092, 0.00100] | 0.00901 | 0.01611 | 0.02073 | 0.02249 | 0.03842 |
| G1 / 10 s | Gauss-Markov | 0.9863 [0.9857, 0.9868] | 0.00805 [0.00768, 0.00839] | 0.00929 | 0.01588 | 0.01994 | 0.02109 | 0.02557 |
| G1 / 20 s | white interpolato | 0.6635 [0.6617, 0.6654] | 0.00066 [0.00063, 0.00068] | 0.00899 | 0.01603 | 0.02061 | 0.02229 | 0.03444 |
| G1 / 20 s | Gauss-Markov | 0.9930 [0.9927, 0.9934] | 0.00796 [0.00760, 0.00830] | 0.00941 | 0.01596 | 0.01947 | 0.02078 | 0.02557 |
| G2 / 10 s | white interpolato | 0.9954 [0.9953, 0.9956] | 0.02755 [0.02640, 0.02883] | 0.08327 | 0.14556 | 0.17904 | 0.19293 | 0.31215 |
| G2 / 10 s | Gauss-Markov | 0.9987 [0.9986, 0.9987] | 0.07498 [0.07150, 0.07852] | 0.08931 | 0.15477 | 0.18818 | 0.20192 | 0.25347 |
| G2 / 20 s | white interpolato | 0.9959 [0.9958, 0.9960] | 0.01985 [0.01897, 0.02080] | 0.08363 | 0.14557 | 0.18526 | 0.20074 | 0.30029 |
| G2 / 20 s | Gauss-Markov | 0.9993 [0.9992, 0.9993] | 0.07126 [0.06839, 0.07430] | 0.08868 | 0.15259 | 0.18495 | 0.19602 | 0.25347 |

Il white interpolato soddisfa P95 G1 0.016 m/s e P99.5 G2 0.200 m/s sul campionamento 20 Hz, con ampiezze per asse ai receiver epochs di 0.00731787 e 0.07226664 m/s. Nei run da 10–20 s il bias temporaneo medio è da 3 a 12 volte inferiore al Gauss-Markov; la correlazione residua del modello white deriva dall'interpolazione già prevista. Scelta: mantenere il modello originale; il tau della posizione non costituisce evidenza per un tau della velocità.

### 4. Validazione indipendente dei sei target

Nuovi seed `300000–302047`, 2.048 traiettorie da 20 s per profilo, 20 Hz. Gli intervalli al 95% sono bootstrap per traiettoria/seed (300 repliche), non sui singoli campioni correlati. Gli intervalli per il massimo sono intervalli bootstrap dei massimi osservati e non bound superiori della distribuzione.

| Target | P50 [95% CI] | P95 [95% CI] | P99 [95% CI] | P99.5 [95% CI] | RMS [95% CI] | Max osservato [CI bootstrap] |
|---|---|---|---|---|---|---|
| G1 posizione, target P95 0.040 m | 0.01916 [0.01878, 0.01961] | 0.04032 [0.03931, 0.04141] | 0.04953 [0.04812, 0.05106] | 0.05285 [0.05114, 0.05468] | 0.02313 [0.02270, 0.02358] | 0.07635 [0.06690, 0.07635] |
| G1 heading, target P95 0.140 deg | 0.04868 [0.04717, 0.05037] | 0.14229 [0.13838, 0.14665] | 0.18816 [0.18101, 0.19556] | 0.20604 [0.19654, 0.21584] | 0.07264 [0.07076, 0.07445] | 0.31576 [0.30228, 0.31576] |
| G1 velocità 2D, target P95 0.016 m/s | 0.00719 [0.00717, 0.00720] | 0.01602 [0.01599, 0.01605] | 0.02051 [0.02046, 0.02057] | 0.02223 [0.02218, 0.02230] | 0.00897 [0.00896, 0.00898] | 0.03670 [0.03437, 0.03670] |
| G2 posizione, target P99.5 0.500 m | 0.18596 [0.18218, 0.18990] | 0.38135 [0.37421, 0.38839] | 0.46805 [0.45464, 0.47941] | 0.50290 [0.48183, 0.52493] | 0.22235 [0.21864, 0.22565] | 0.71073 [0.62276, 0.71073] |
| G2 heading, target P99.5 0.600 deg | 0.14497 [0.14261, 0.14771] | 0.41925 [0.41345, 0.42542] | 0.54870 [0.53789, 0.55870] | 0.60049 [0.58374, 0.61657] | 0.21462 [0.21156, 0.21764] | 0.98729 [0.92970, 0.98729] |
| G2 velocità 2D, target P99.5 0.200 m/s | 0.06801 [0.06760, 0.06844] | 0.14655 [0.14566, 0.14737] | 0.18610 [0.18452, 0.18766] | 0.20161 [0.19966, 0.20353] | 0.08338 [0.08297, 0.08378] | 0.34012 [0.30654, 0.34012] |

Tutti i punti target sono entro il 2% dai rispettivi valori e i target sono compresi nei relativi intervalli. Nei primi 10 s delle registrazioni canoniche S01, S04, S14 e S19, gli intervalli P95 G1 sono: posizione 0.03956–0.04043 m, heading 0.13673–0.14270 deg, velocità 0.01597–0.01600 m/s; P99.5 G2: posizione 0.51761–0.51896 m, heading 0.59770–0.61808 deg, velocità 0.19900–0.19964 m/s. Campioni descrittivi, non aggiunti al campione indipendente sintetico.

### 5. Anomalie smoke

- **S14:** G0 smoke ha 5 merge mancati, mentre la ricostruzione canonica salvata riporta 8 (`fusion_metrics.json`); `identical_graph=false`. I risultati G1 e G2 mantengono 5. Quindi i merge mancati non sono identici al risultato canonico.
- **S19:** G0 smoke ha 10 merge mancati, la ricostruzione canonica salvata 11; `identical_graph=false`. G1 e G2 mantengono 10. Anche qui non sono identici.
- **S04 con radar high:** entrambi i job RTK+high e degraded+high riportano 7 `CRITICAL_TTC_START` contro 2 attesi dalla coverage; RTK/G2 con radar low o nominale restano 2/2. Nei due job high gli eventi extra rispetto a G0 sono `B/anonymous @ -4.30`, `C/anonymous @ -3.15` (due righe identiche), `B/anonymous @ -2.85` e `C/anonymous @ -1.05` in tempo globale riallineato. Sono 5 istanze ma 4 eventi unici: una partizione/duplicazione produce il doppio start C a -3.15. L'oracolo conferma 2/2 eventi coverage visibili abbinati; nessuno dei 5 start eccedenti è abbinato a coverage o all'oracolo perfetto, perciò sono falsi positivi associati al radar degradato (quattro start distinti, uno duplicato). Non sono state cambiate soglie o logica.

### 6. Manifest e controller

Manifest `results/robustness/rtk5g_current/manifest.json`: `PRELIMINARY`, `version_tag_commit=null`, ricreato con Python 3.8.20 e hash del codice corrente. `campaign_controller.py status` restituisce controller fermo e 0 job; `verify_freeze()` rifiuta per manifest preliminare, HEAD non congelato e working tree tracciato modificato. Il controller della campagna completa non è stato avviato. I risultati smoke restano 18 job su 18 completati, a fini descrittivi.

### 7. Suite completa

Run completo nell'ambiente Conda `carla` (Python 3.8.20, comando `python -m pytest -q --tb=short`): **613 passed, 5 failed, 0 errori, 3 warning in 1738.98 s (28:58)**. I cinque failure sono gli stessi già riprodotti sul commit originale; nessun nuovo failure è stato introdotto dal modello white interpolato. I 6 test pygame falliti solo sotto Python di sistema sono passati; la suite completa non ha errori di setup.


### 8. File modificati

File tracciati modificati nell'attuale protocollo: `docs/robustness_profiles.md`, `scripts/campaign_controller.py`, `scripts/campaign_manifest.py`, `scripts/campaign_report.py`, `scripts/robustness.py`, `src/cdf/evaluation/pose_errors.py`, `src/cdf/robustness/perturb.py`, `tests/test_final_hardening.py`, `tests/test_frozen_campaign.py`, `tests/test_robustness.py`. La correzione di scelta del rumore è limitata a `src/cdf/robustness/perturb.py`, alla relativa descrizione statistica in `docs/robustness_profiles.md` e all'assertion di campionamento velocità in `tests/test_robustness.py`.

Nuovi risultati sotto `results/robustness/rtk5g_current/`: `manifest.json`, `preflight_smoke/jobs.jsonl`, `preflight_smoke/preflight_report.md`, `preflight_smoke/summary.md`, `summary.json`, `summary.csv` e `figures/gnss.svg` / `figures/gnss.pdf`. Nessun file pygame/Conda, dato canonico o output della campagna congelata è stato modificato.
