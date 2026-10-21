# Revisione preflight RTK/5G

**Data:** 2026-10-21. **Ambiente della suite:** `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe`, Python 3.8.20. **Ricostruzione:** invariata. Nessuna delle 22 registrazioni canoniche, soglie o risultati della campagna congelata è stata modificata.

## Esito sintetico

- Suite completa: **613 passed, 5 failed, 3 warnings**. I cinque failure sono riproducibili anche al commit originale `1d596c1e499097e5cead7c1214a2588afd4ac3ba`; sono mismatch preesistenti tra output rigenerati e golden/report salvati.
- I sei test che prima avevano errori di setup pygame passano in Conda. pygame 2.1.3 era già installato ed è compatibile; non è servita una reinstallazione.
- Il rumore bianco interpolato della velocità raggiunge i target 20 Hz sui seed indipendenti. È il modello mantenuto; il Gauss-Markov aggiunge correlazione e bias temporaneo senza evidenza temporale specifica per la velocità.
- Il controller rifiuta l'avvio della campagna: manifest `PRELIMINARY`, tag/versione di freeze assente, **0 job** registrati dal controller. Nessun tag o campagna completa è stato avviato.

## Suite e test problematici

Comando della suite completa: `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe -m pytest -q --tb=short`. Esito: **613 passed, 5 failed, 3 warnings in 1738.98 s**. I cinque node ID sono stati eseguiti sia nel working tree sia nel worktree temporaneo detached e sparse `C:\Users\andrea.bedei3\AppData\Local\Temp\CarlaGraph_original_1d596c1` del commit originale; `traces` era una junction ai dati canonici condivisi, senza copia dei dati. Entrambi hanno dato 5 failure. Run di confronto: 111.68 s sull'originale e 130.22 s sul working tree.

Comando di confronto riproducibile, dalla root di ciascun checkout (con l'interprete Conda sopra):

```powershell
python -m pytest -q --tb=short `
  tests/test_retrospective.py::RealRunRegressions::test_reconstruction_matches_the_committed_one `
  tests/test_robustness.py::ReconstructionUnderPerturbationTests::test_constant_clock_offsets_leave_the_global_graph_unchanged `
  tests/test_robustness.py::MutualRefinementTests::test_exact_pose_sources_are_not_refined `
  tests/test_worked_example.py::S12WorkedExampleTests::test_privileged_checks_pass_and_the_committed_report_is_current `
  tests/test_worked_example.py::S12WorkedExampleTests::test_privileged_files_do_not_reach_the_reconstruction
```

| Test | Esito attuale | Esito `1d596c1e499097e5cead7c1214a2588afd4ac3ba` | Assertion e causa osservata |
|---|---|---|---|
| [`test_retrospective.py::RealRunRegressions::test_reconstruction_matches_the_committed_one`](../tests/test_retrospective.py) | FAIL | FAIL | `assertEqual(committed["nodes"], mine["nodes"])`; prima differenza al nodo 7: `track_002` contro `track_003`. La ricostruzione rigenerata non coincide col grafo salvato. |
| [`test_robustness.py::ReconstructionUnderPerturbationTests::test_constant_clock_offsets_leave_the_global_graph_unchanged`](../tests/test_robustness.py) | FAIL | FAIL | `assertEqual(graph_signature(new), graph_signature(base))`; la firma nuova contiene un `EGO_PATH_EXIT` aggiuntivo. |
| [`test_robustness.py::MutualRefinementTests::test_exact_pose_sources_are_not_refined`](../tests/test_robustness.py) | FAIL | FAIL | La stessa uguaglianza di `graph_signature`; con pose esatte compare lo stesso tipo di evento aggiuntivo. |
| [`test_worked_example.py::S12WorkedExampleTests::test_privileged_checks_pass_and_the_committed_report_is_current`](../tests/test_worked_example.py) | FAIL | FAIL | `assertEqual(committed.read_text(), fresh)`; la rigenerazione del report marca file come `DIFFERENT`. |
| [`test_worked_example.py::S12WorkedExampleTests::test_privileged_files_do_not_reach_the_reconstruction`](../tests/test_worked_example.py) | FAIL | FAIL | `assertTrue(result["identical"], result["different_files"])`; divergono `A/local_graph.dot`, `A/local_graph.json`, `A/local_graph.md`, `A/local_trace.jsonl`, `B/local_graph.json`, `B/local_trace.jsonl`, `global/alignment.json`, `global/global_graph.dot`, `global/global_graph.json`, `global/global_graph.md`, `global/global_trace.jsonl` e `report.md`. |

I cinque failure sono preesistenti, non introdotti dalla modifica GNSS: l'identica assertion fallisce sul commit originale. Non sono state cambiate ricostruzione, soglie o golden output per farli passare.

### pygame: i sei test di setup

L'ambiente usato per questa suite è Conda Python 3.8.20 con pygame 2.1.3 e SDL 2.0.22; `pyproject.toml` ammette `pygame>=2.1,<2.7`. I sei test risultano **PASS**; l'intero `tests/test_replay_focus_panel.py` ha dato **13 passed, 3 deprecation warnings**.

| Test | Esito |
|---|---|
| `FocusLayoutTests::test_focus_gives_the_selected_recorder_the_column_and_every_event` | PASS |
| `FocusLayoutTests::test_long_history_scrolls_through_every_event` | PASS |
| `FocusLayoutTests::test_others_collapsed_in_focus_and_restored_without_it` | PASS |
| `FocusLayoutTests::test_collision_banner_keeps_every_pair_clear_of_the_focused_panel` | PASS |
| `FocusLayoutTests::test_keys_f_toggles_and_tab_shows_the_new_recorder_newest_events` | PASS |
| `FocusLayoutTests::test_help_names_the_focus_key` | PASS |

pygame era già presente nella Conda usata dai test: non è stato necessario installare o aggiornare dipendenze.

## Modello del rumore sulla velocità

Il confronto usa 512 seed nuovi (`400000–400511`), traiettorie indipendenti di 10 e 20 s, campionamento a 20 Hz. Gli intervalli al 95% per autocorrelazione lag-1 e bias temporaneo ricampionano traiettorie intere. Il bias è la norma della media vettoriale 2D dell'errore velocità per traiettoria; RMS, percentili e massimo sono misure sui campioni 20 Hz. I dettagli numerici sono anche in [`velocity_model_comparison.csv`](../results/robustness/rtk5g_current/velocity_model_comparison.csv).

| Profilo/durata | Modello | Autocorr. lag-1 [95% CI] | Bias temporaneo medio m/s [95% CI] | RMS m/s | P95 | P99 | P99.5 | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| G1 / 10 s | Bianco interpolato | 0.6620 [0.6594, 0.6646] | 0.00096 [0.00092, 0.00100] | 0.00901 | 0.01611 | 0.02073 | 0.02249 | 0.03842 |
| G1 / 10 s | Gauss-Markov | 0.9863 [0.9857, 0.9868] | 0.00805 [0.00768, 0.00839] | 0.00929 | 0.01588 | 0.01994 | 0.02109 | 0.02557 |
| G1 / 20 s | Bianco interpolato | 0.6635 [0.6617, 0.6654] | 0.00066 [0.00063, 0.00068] | 0.00899 | 0.01603 | 0.02061 | 0.02229 | 0.03444 |
| G1 / 20 s | Gauss-Markov | 0.9930 [0.9927, 0.9934] | 0.00796 [0.00760, 0.00830] | 0.00941 | 0.01596 | 0.01947 | 0.02078 | 0.02557 |
| G2 / 10 s | Bianco interpolato | 0.9954 [0.9953, 0.9956] | 0.02755 [0.02640, 0.02883] | 0.08327 | 0.14556 | 0.17904 | 0.19293 | 0.31215 |
| G2 / 10 s | Gauss-Markov | 0.9987 [0.9986, 0.9987] | 0.07498 [0.07150, 0.07852] | 0.08931 | 0.15477 | 0.18818 | 0.20192 | 0.25347 |
| G2 / 20 s | Bianco interpolato | 0.9959 [0.9958, 0.9960] | 0.01985 [0.01897, 0.02080] | 0.08363 | 0.14557 | 0.18526 | 0.20074 | 0.30029 |
| G2 / 20 s | Gauss-Markov | 0.9993 [0.9992, 0.9993] | 0.07126 [0.06839, 0.07430] | 0.08868 | 0.15259 | 0.18495 | 0.19602 | 0.25347 |

Il bianco supera i target richiesti a 20 Hz senza un nuovo parametro temporale: G1 P95 0.01611 m/s contro 0.016; G2 P99.5 0.20074 m/s contro 0.200. Le ampiezze per asse agli epoch ricevitore sono 0.00731787 m/s per G1 a 10 Hz e 0.07226664 m/s per G2 a 1 Hz, calibrate per la miscela delle fasi dell'interpolazione lineare. La sua autocorrelazione residua deriva da quell'interpolazione già prevista. Il candidato Gauss-Markov usa ampiezze 0.00653798 e 0.06177689 m/s e tau copiati dalla posizione (60 e 30 s): il bias medio su traiettorie brevi è circa 3–12 volte maggiore, con RMS e percentili simili. Le fonti bibliografiche citate non forniscono questi tau per la velocità. Scelta: mantenere il rumore bianco interpolato.

## Validazione GNSS indipendente

Seed nuovi `300000–302047`: 2.048 traiettorie indipendenti da 20 s per profilo, griglia 20 Hz, 300 repliche bootstrap per seed/traiettoria. Gli intervalli preservano la dipendenza temporale. Posizione e velocità sono errori orizzontali 2D; heading è errore assoluto avvolto. Tutti i sei target sono dentro il rispettivo intervallo al 95%; i sei valori puntuali target sono entro il 2% dal valore richiesto. CSV riproducibile: [`gnss_validation.csv`](../results/robustness/rtk5g_current/gnss_validation.csv).

| Target | P50 [95% CI] | P95 [95% CI] | P99 [95% CI] | P99.5 [95% CI] | RMS [95% CI] | Max osservato [CI bootstrap] |
|---|---:|---:|---:|---:|---:|---:|
| G1 posizione, P95 0.040 m | 0.01916 [0.01878, 0.01961] | 0.04032 [0.03931, 0.04141] | 0.04953 [0.04812, 0.05106] | 0.05285 [0.05114, 0.05468] | 0.02313 [0.02270, 0.02358] | 0.07635 [0.06690, 0.07635] |
| G1 heading, P95 0.140 deg | 0.04868 [0.04717, 0.05037] | 0.14229 [0.13838, 0.14665] | 0.18816 [0.18101, 0.19556] | 0.20604 [0.19654, 0.21584] | 0.07264 [0.07076, 0.07445] | 0.31576 [0.30228, 0.31576] |
| G1 velocità 2D, P95 0.016 m/s | 0.00719 [0.00717, 0.00720] | 0.01602 [0.01599, 0.01605] | 0.02051 [0.02046, 0.02057] | 0.02223 [0.02218, 0.02230] | 0.00897 [0.00896, 0.00898] | 0.03670 [0.03437, 0.03670] |
| G2 posizione, P99.5 0.500 m | 0.18596 [0.18218, 0.18990] | 0.38135 [0.37421, 0.38839] | 0.46805 [0.45464, 0.47941] | 0.50290 [0.48183, 0.52493] | 0.22235 [0.21864, 0.22565] | 0.71073 [0.62276, 0.71073] |
| G2 heading, P99.5 0.600 deg | 0.14497 [0.14261, 0.14771] | 0.41925 [0.41345, 0.42542] | 0.54870 [0.53789, 0.55870] | 0.60049 [0.58374, 0.61657] | 0.21462 [0.21156, 0.21764] | 0.98729 [0.92970, 0.98729] |
| G2 velocità 2D, P99.5 0.200 m/s | 0.06801 [0.06760, 0.06844] | 0.14655 [0.14566, 0.14737] | 0.18610 [0.18452, 0.18766] | 0.20161 [0.19966, 0.20353] | 0.08338 [0.08297, 0.08378] | 0.34012 [0.30654, 0.34012] |

Gli intervalli del massimo descrivono i massimi osservati nelle traiettorie ricampionate e sono limitati dal massimo del campione; non sono bound superiori della distribuzione. Su finestre da 10 s dei quattro scenari canonici S01, S04, S14 e S19, 512 seed per registratore: G1 P95 varia fra 0.03956–0.04043 m (posizione), 0.13673–0.14270 deg (heading) e 0.01597–0.01600 m/s (velocità); G2 P99.5 varia fra 0.51761–0.51896 m, 0.59770–0.61808 deg e 0.19900–0.19964 m/s. I range sono disponibili in [`gnss_short_canonical.csv`](../results/robustness/rtk5g_current/gnss_short_canonical.csv). Sono intervalli descrittivi su traiettorie brevi, non ulteriori campioni pooled indipendenti.

## Anomalie smoke S04, S14 e S19

I 18 job dello smoke hanno terminato (18 complete, 0 failed); dettagli: [`jobs.jsonl`](../results/robustness/rtk5g_current/preflight_smoke/jobs.jsonl), [`summary.json`](../results/robustness/rtk5g_current/preflight_smoke/summary.json), [`summary.csv`](../results/robustness/rtk5g_current/preflight_smoke/summary.csv). Gli output GNSS G1/G2 dello smoke sono stati prodotti prima del passaggio finale al rumore bianco e non verificano il nuovo modello; G0 non usa rumore GNSS.

### S04: radar high

Con radar low o nominale sono stati trovati 2 avvii `CRITICAL_TTC` attesi su 2. Entrambe le combinazioni radar high, sia RTK sia degraded, ne riportano 7; l'oracolo ne abbina 2/2 e nessuno dei cinque avvii extra coincide con gli eventi attesi. I cinque extra sono `B/anonymous @ -4.30 s`, `C/anonymous @ -3.15 s` (duplicato due volte), `B/anonymous @ -2.85 s`, `C/anonymous @ -1.05 s`: quattro istanze uniche e una ripetizione compatibile con uno split/duplicazione di traccia. Entrambi gli high hanno inoltre un link mancato e 123 entità anonime. I cinque avvii sono falsi positivi rispetto agli oracoli coverage/perfect, non nuovi eventi corretti causati dalla scena. Non sono state cambiate soglie o logica. Il conteggio G1/G2 è però del run smoke precedente al rumore bianco: va confermato con un breve smoke mirato prima del freeze.

### S14 e S19: G0 smoke contro ricostruzione canonica salvata

Nota sul perimetro S04: le combinazioni G1/G2 con radar high provengono dallo smoke pre-rumore bianco e sono state registrate da Python 3.14.2. Il confronto G0 in Conda non convalida quei job; prima del freeze serve un breve rerun mirato in Conda Python 3.8.20 con il profilo bianco finale.

| Scenario | G0 smoke ricalcolato: merge mancati / entità | Output canonico salvato: merge mancati / entità | Confronto |
|---|---:|---:|---|
| S14 | 5 / 11 | 8 / 12 | grafo non identico |
| S19 | 10 / 10 | 11 / 9 | grafo non identico |

Il conteggio G0 è stato riprodotto con due soli job mirati in Conda Python 3.8.20: S14 5 merge mancati e 11 entità; S19 10 e 10. I file canonici salvati riportano rispettivamente 8/12 e 11/9 ([S14 fusion metrics](../traces/S14/run_0_surrounded/reconstruction/evaluation/fusion_metrics.json), [S19 fusion metrics](../traces/S19/run_0_highway_curve/reconstruction/evaluation/fusion_metrics.json)). Il mismatch non è dovuto al modello GNSS né alla versione Python: `identical_graph=false` anche nel confronto Conda. Il numero dei merge mancati dipende dalle coppie di tracce anonime formate dal grafo; le ricostruzioni salvate e quelle appena ricalcolate hanno insiemi di entità diversi. I test storici di riproducibilità falliscono già sul commit originale. La riconciliazione puntuale dei singoli abbinamenti di entità resta aperta: i risultati aggregati non consentono di assegnare i 3 merge (S14) e 1 merge (S19) a specifiche coppie senza un diff dedicato dei grafi completi.

Il log smoke riporta Python 3.14.2, mentre la suite, il manifest e il confronto mirato sono in Conda Python 3.8.20. Il confronto Conda appena eseguito esclude che questa differenza spieghi i conteggi G0. Non sono stati inclusi nel commit i grafi rigenerati né altri output canonici.

## Manifest, controller e integrità

Il [`manifest.json`](../results/robustness/rtk5g_current/manifest.json) è **PRELIMINARY**: `version_tag_commit=null`, HEAD fotografato `1d596c1e499097e5cead7c1214a2588afd4ac3ba`, working tree dirty al momento della generazione. Il controller è **non pronto** e registra 0 job; `verify_freeze()` rifiuta l'avvio se il manifest è preliminare o il checkout non corrisponde al commit congelato. Il commit di revisione non rappresenta un freeze e il manifest non abilita una campagna.

Hash dei 22 input canonici verificati contro il manifest: invariati. La hash delle sorgenti di ricostruzione coincide con quella del freeze storico. Nessun output della campagna congelata è stato rigenerato o aggiunto. Nessuna campagna completa o tag di freeze è stato creato.

## Fonti e assunzioni

I target G1/G2 combinano percentili sperimentali e assunzioni ingegneristiche, non descrivono un singolo ricevitore o una prestazione 5G misurata. Volckaert et al. riportano percentili RTK di posizione/velocità in una presentazione tecnica ([Septentrio, 2019](https://gnss-imu.com/down/upload/20240402/1712021876.pdf)); la prova SBG riporta heading real-time ([vendor test](https://www.sbg-systems.com/test-reports/automotive-tests/)); lo studio peer-reviewed di Lesjak et al. fornisce percentili C-ITS/4G, non 5G ([Springer, 2025](https://doi.org/10.1007/978-3-032-06763-0_81)). La scheda u-blox riporta specifiche a 68%, non i target G2 di coda ([ZED-F9R-02B](https://content.u-blox.com/sites/default/files/ZED-F9R-02B_DataSheet_UBX-21017486.pdf)).

La letteratura Gauss-Markov descrive un modello di errore di localizzazione ([Hoffmann et al., EURASIP, 2020](https://doi.org/10.1186/s13638-020-1641-8)), ma non determina i tau della velocità usati nel candidato. La fattibilità del trasporto correzioni via 5G è documentata da una dimostrazione peer-reviewed ([Elgarhy et al., IEEE FNWF](https://doi.org/10.1109/FNWF63303.2024.11028789)) e da un testbed report ([FrontierSI, 2024](https://frontiersi.com.au/wp-content/uploads/2023/04/5G-Testbed-Technical-Report.pdf)); nessuna delle due fonti stabilisce i percentili qui usati. Riferimenti, limiti e assunzioni estese sono in [`robustness_profiles.md`](robustness_profiles.md).

## File di questo branch

Modifiche codice/test/documentazione GNSS già presenti nel checkout: `docs/robustness_profiles.md`; `scripts/campaign_controller.py`, `scripts/campaign_manifest.py`, `scripts/campaign_report.py`, `scripts/robustness.py`; `src/cdf/evaluation/pose_errors.py`, `src/cdf/robustness/perturb.py`; `tests/test_final_hardening.py`, `tests/test_frozen_campaign.py`, `tests/test_robustness.py`.

Nuovi artefatti leggeri di revisione: questo report, `results/robustness/rtk5g_current/manifest.json`, `results/robustness/rtk5g_current/preflight_smoke/jobs.jsonl`, `summary.json`, `summary.csv`, `velocity_model_comparison.csv`, `gnss_validation.csv` e `gnss_short_canonical.csv`. Nessun dato canonico, output congelato o figura è incluso come modifica.
