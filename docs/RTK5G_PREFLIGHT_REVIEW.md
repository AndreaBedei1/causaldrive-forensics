# Revisione preflight RTK/5G

**Data:** 2026-10-21. **Ambiente della suite:** `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe`, Python 3.8.20. **Ricostruzione:** invariata. Nessuna delle 22 registrazioni canoniche, soglie o risultati della campagna congelata è stata modificata.

## Esito sintetico

- Suite completa (prima dell'aggiornamento protocollo depth): **619 passed, 5 failed, 3 warnings**. I cinque failure sono riproducibili anche al commit originale `1d596c1e499097e5cead7c1214a2588afd4ac3ba`; sono mismatch preesistenti tra output rigenerati e golden/report salvati.
- I sei test che prima avevano errori di setup pygame passano in Conda. pygame 2.1.3 era già installato ed è compatibile; non è servita una reinstallazione.
- Il rumore bianco interpolato della velocità raggiunge i target 20 Hz sui seed indipendenti. È il modello mantenuto; il Gauss-Markov aggiunge correlazione e bias temporaneo senza evidenza temporale specifica per la velocità.
- Il controller rifiuta l'avvio della campagna: manifest `PRELIMINARY`, tag/versione di freeze assente, **0 job** registrati dal controller. Nessun tag o campagna completa è stato avviato.

## Suite e test problematici

Comando della suite completa: `C:\Users\andrea.bedei3\.conda\envs\carla\python.exe -m pytest -q --tb=short`. Esito: **619 passed, 5 failed, 3 warnings in 1347.26 s**. I cinque node ID sono stati eseguiti sia nel working tree sia nel worktree temporaneo detached e sparse `C:\Users\andrea.bedei3\AppData\Local\Temp\CarlaGraph_original_1d596c1` del commit originale; `traces` era una junction ai dati canonici condivisi, senza copia dei dati. Entrambi hanno dato 5 failure. Run di confronto: 111.68 s sull'originale e 130.22 s sul working tree. Dopo le modifiche al protocollo depth, i test mirati sono stati rieseguiti separatamente: vedi la sezione finale; il run completo qui riportato precede quell'aggiornamento.

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

Il [`manifest.json`](../results/robustness/rtk5g_current/manifest.json) è **PRELIMINARY**: `version_tag_commit=null`, HEAD fotografato `1d596c1e499097e5cead7c1214a2588afd4ac3ba`, working tree dirty al momento della generazione. Il controller sul percorso corrente `rtk5g_current` non è attivo e registra 0 job; `verify_freeze()` rifiuta l'avvio se il manifest è preliminare o il checkout non corrisponde al commit congelato. Il comando `campaign_controller.py status` senza override legge invece lo storico `results/robustness/frozen_campaign`: 3.775 record, 3.774 risultati unici completi all'ultimo tentativo, 0 fallimenti correnti; quel dataset ha timestamp 2026-10-16 ed è preesistente, non è stato avviato o modificato in questo incarico. Il commit di revisione non rappresenta un freeze e il manifest `rtk5g_current` non abilita una campagna.

Hash dei 22 input canonici verificati contro il manifest: invariati. La hash delle sorgenti di ricostruzione coincide con quella del freeze storico. Nessun output della campagna congelata è stato rigenerato o aggiunto. In questo incarico non è stata avviata una nuova campagna massiva e non è stato creato un tag di freeze.

## Fonti e assunzioni

I target G1/G2 combinano percentili sperimentali e assunzioni ingegneristiche, non descrivono un singolo ricevitore o una prestazione 5G misurata. Volckaert et al. riportano percentili RTK di posizione/velocità in una presentazione tecnica ([Septentrio, 2019](https://gnss-imu.com/down/upload/20240402/1712021876.pdf)); la prova SBG riporta heading real-time ([vendor test](https://www.sbg-systems.com/test-reports/automotive-tests/)); lo studio peer-reviewed di Lesjak et al. fornisce percentili C-ITS/4G, non 5G ([Springer, 2025](https://doi.org/10.1007/978-3-032-06763-0_81)). La scheda u-blox riporta specifiche a 68%, non i target G2 di coda ([ZED-F9R-02B](https://content.u-blox.com/sites/default/files/ZED-F9R-02B_DataSheet_UBX-21017486.pdf)).

La letteratura Gauss-Markov descrive un modello di errore di localizzazione ([Hoffmann et al., EURASIP, 2020](https://doi.org/10.1186/s13638-020-1641-8)), ma non determina i tau della velocità usati nel candidato. La fattibilità del trasporto correzioni via 5G è documentata da una dimostrazione peer-reviewed ([Elgarhy et al., IEEE FNWF](https://doi.org/10.1109/FNWF63303.2024.11028789)) e da un testbed report ([FrontierSI, 2024](https://frontiersi.com.au/wp-content/uploads/2023/04/5G-Testbed-Technical-Report.pdf)); nessuna delle due fonti stabilisce i percentili qui usati. Riferimenti, limiti e assunzioni estese sono in [`robustness_profiles.md`](robustness_profiles.md).

## File di questo branch

Modifiche codice/test/documentazione GNSS già presenti nel checkout: `docs/robustness_profiles.md`; `scripts/campaign_controller.py`, `scripts/campaign_manifest.py`, `scripts/campaign_report.py`, `scripts/robustness.py`; `src/cdf/evaluation/pose_errors.py`, `src/cdf/robustness/perturb.py`; `tests/test_final_hardening.py`, `tests/test_frozen_campaign.py`, `tests/test_robustness.py`.

Nuovi artefatti leggeri di preflight: questo report, `results/robustness/rtk5g_current/manifest.json`, i report smoke e i CSV statistici GNSS. La sezione seguente aggiunge solo report CSV/JSON/Markdown e 22 overlay compressi; nessun dato grezzo riacquisito, dato canonico o output della campagna congelata è pubblicato.

## Gate obbligatorio OLD/NEW delle 22 riacquisizioni

### Esito del gate

Tutti i 22 nuovi run sono stati acquisiti con CARLA client/server 0.9.15, Python Conda 3.8.20, seed 0 e `fixed_delta_seconds=0.05`; il controllo post-run ha confermato il ripristino asincrono, la mappa prevista e l'assenza di veicoli/sensori residui. Le 22 coppie storiche/nuove sono state confrontate; non manca alcun run. I dati storici sono rimasti in `traces/` e nella copia verificata `F:\CarlaGraph_RTK5G_archive_20261021\OLD_ARCHIVED\traces`; i nuovi raw sono separati in `F:\CarlaGraph_RTK5G_archive_20261021\NEW_REACQUIRED\traces`. Nessun raw è stato eliminato o aggiunto al repository.

Il gate fisico passa per **21/22** run. **S10/deflected_into_c** non passa: mantiene i contatti iniziali A–B e A–C negli stessi tempi, ma la durata e la continuità del contatto A–C cambiano sostanzialmente. Il gate sensori passa per **0/22**: 49 dei 50 canali depth nuovi hanno frame mancanti (anche se 50/50 depth storici erano già incompleti). Tutti i canali radar e RGB risultano presenti e senza frame mancanti o drop registrati. Poiché la richiesta definisce i sensori incompleti come condizione di stop, **la campagna massiva resta bloccata**. Non ho modificato soglie, scenari, ricostruzione, target GNSS o risultati canonici e non ho avviato la campagna.

Gli artefatti di confronto sono in [`reacquisition/comparison/`](../results/robustness/rtk5g_current/reacquisition/comparison/): [indice dei 22 run e overlay](../results/robustness/rtk5g_current/reacquisition/comparison/comparison_index.md), [tabelle dettagliate OLD/NEW per ciascun run](../results/robustness/rtk5g_current/reacquisition/comparison/comparison_details.md), [metriche traiettorie per partecipante](../results/robustness/rtk5g_current/reacquisition/comparison/trajectory_metrics.csv), [sensori](../results/robustness/rtk5g_current/reacquisition/comparison/sensor_comparison.csv), [callback collisione grezzi](../results/robustness/rtk5g_current/reacquisition/comparison/collision_events.csv), [burst di contatto fisico](../results/robustness/rtk5g_current/reacquisition/comparison/collision_episodes.csv), [trigger](../results/robustness/rtk5g_current/reacquisition/comparison/trigger_events.csv), [distanze minime OBB](../results/robustness/rtk5g_current/reacquisition/comparison/minimum_gap_comparison.csv), [manovre/frenate/accelerazioni](../results/robustness/rtk5g_current/reacquisition/comparison/maneuver_comparison.csv) e [configurazione veicoli/sensori](../results/robustness/rtk5g_current/reacquisition/comparison/vehicle_config_comparison.csv). La [manifest dei run acquisiti](../results/robustness/rtk5g_current/reacquisition/reacquisition_run_manifest.csv) e gli [hash SHA-256 per run](../results/robustness/rtk5g_current/reacquisition/reacquisition_integrity.csv) identificano anche i due alberi raw locali. Gli hash non sostituiscono l'accesso ai raw: i nuovi raw non sono pubblicati per rispettare il limite sui dati pesanti.

Il comparatore allinea le ground truth a 20 Hz dal primo stato dello scenario e riporta, per ogni partecipante, P50/P95/P99/P99,5/massimo/RMS di errore posizione in coordinate mondo e rispetto allo spostamento iniziale, velocità 2D e heading assoluto avvolto. Timestamp assoluti, actor ID e frame assoluti sono run-local: gli abbinamenti usano ID partecipante, tempo relativo e offset di frame. I callback reciproci sono deduplicati solo entro lo stesso frame e coppia. Per distinguere i contatti persistenti dai callback per tick, il report raggruppa i callback della stessa coppia quando la distanza temporale è al massimo 2,5 tick; confronta separatamente inizio/fine con tolleranza descrittiva di 0,10 s. Il file dei callback grezzi conserva comunque ogni frame. Questa regola serve solo alla classificazione del confronto e non tocca la ricostruzione né le sue soglie.

### Sensori, traiettorie e contatti

Il confronto contiene 250 canali: 150 radar, 50 RGB e 50 depth. I radar hanno tick configurato e cadenza misurata di 0,05 s/20 Hz: 150/150 completi sia OLD sia NEW, zero drop e zero frame mancanti. RGB ha tick configurato 0,10 s/10 Hz, callback/frame contati 6.956 OLD e 6.958 NEW, zero drop e zero frame mancanti nei metadata; i frame immagine/timestamp RGB non sono salvati come array, quindi la cadenza effettiva RGB non è misurabile indipendentemente dai contatori registrati. Depth è configurato a 0,05 s/20 Hz: OLD 9.904 frame, 3.915 mancanti e 3.963 callback duplicati; NEW 10.493 frame, 3.326 mancanti e 3.376 duplicati. I drop di coda sono zero; i canali depth nuovi incompleti sono 49/50, uno in meno rispetto allo storico. La frequenza misurata nei canali depth nuovi è 10 o 20 Hz, coerente con la presenza di frame saltati; tutti i tick/configurazioni statiche corrispondono. Ogni run ha comunque almeno un canale depth incompleto.

Tutti i 22 run hanno mappa, variante, seed, partecipanti/ruoli, registratori, metadati/configurazione veicolo e durata corrispondenti; la differenza durata è 0,000 s e i conteggi di stato sono uguali. Trigger e relativi tempi coincidono; le distanze minime fra OBB e le statistiche di frenata, throttle, sterzo e accelerazione sono nelle tabelle collegate. Gli errori completi posizione/velocità/heading sono nel CSV per partecipante; l'indice contiene una riga per ciascuna delle 22 coppie e un overlay per ciascun run.

S03 aveva 7 OLD contro 6 NEW tick-callback A–B, ma due burst fisici in entrambi: 4,15 s e 4,40–4,65 s OLD / 4,40–4,60 s NEW, differenza finale 0,05 s. S16 aveva 40 contro 39 callback A–B, ma un singolo burst 6,80–8,80 s OLD / 6,80–8,75 s NEW; impulso totale 1.672,4 contro 1.669,0 N·s. Queste differenze di callback non sono collisioni fisiche aggiuntive o perse.

**S10 è una differenza fisica reale:** entrambi i run hanno A–B a 3,85 s e il primo A–C a 4,75 s. OLD registra A–C in un burst continuo fino a 14,00 s (186 tick, impulso totale 10.527,5 N·s). NEW registra il burst iniziale fino a 6,30 s (31 tick, 8.082,2 N·s), poi tre ricontatti deboli separati a 6,50–6,75 s (6 tick), 7,00–7,15 s (4) e 7,55–7,60 s (2), per 43 tick totali e 8.120,5 N·s. Non manca la coppia A–C né nasce una coppia nuova, ma la persistenza del contatto cessa 7,70 s prima e la traiettoria diverge fino a 0,301 m per A e 0,206 m per C. Il cambiamento della dinamica successiva all'impatto è materiale; insieme ai sensori depth incompleti blocca il gate.

### Differenze G0 smoke/canonico per S14 e S19

I due job G0 mirati, riprodotti con Python Conda e un seed deterministico, replicano esattamente i valori dello smoke: S14 5 merge mancati e S19 10; `identical_graph=false` in entrambi. Il dettaglio OLD/canonico contro G0 rigenerato è in [`g0_merge_pair_diff.csv`](../results/robustness/rtk5g_current/reacquisition/g0_merge_pair_diff.csv). Il conteggio è sui pair di tracce dello stesso veicolo rimasti separati.

- **S14: 8 canonici contro 5 G0.** Cinque coppie mancate coincidono; i tre mancanti aggiuntivi nel grafo canonico sono `H: B:track_007–B:track_014`, `B:track_011–B:track_014` e `B:track_012–B:track_014`. `B:track_014` non esiste nel G0 rigenerato. Entrambi hanno 11 merge corretti; il grafo canonico ha 23 decisioni di traccia contro 22 nel G0. Il delta 3 è quindi un track in più che crea tre coppie dello stesso veicolo rimaste separate, non una perdita di tre merge corretti.
- **S19: 11 canonici contro 10 G0.** Cinque coppie mancate coincidono. Sei sono solo nel canonico (`A:track_004–A:track_010`, `A:track_005–A:track_011`, `A:track_006–A:track_008`, `A:track_006–A:track_009`, `A:track_010–B:track_001`, `A:track_010–B:track_006`); cinque solo nel G0 (`A:track_004–A:track_008`, `A:track_005–A:track_009`, `A:track_007–B:track_002`, `A:track_008–B:track_001`, `A:track_008–B:track_006`). Il G0 sostituisce la frammentazione/indicizzazione delle tracce osservata nel grafo salvato. Il saldo netto è +1 merge mancato nel canonico; il confronto non autorizza a cambiare le soglie o a sovrascrivere i risultati canonici.

### S04 radar high

Le due combinazioni radar high dello smoke riportano 7 `CRITICAL_TTC_START` rispetto ai 2 eventi coverage attesi; entrambi gli eventi attesi sono abbinati, mentre i 5 start residui non lo sono. Sono 4 istanze anonime distinte e una ripetizione: `B/anonymous @ −4,30 s`, `C/anonymous @ −3,15 s` due volte, `B/anonymous @ −2,85 s`, `C/anonymous @ −1,05 s`. Si tratta quindi di falsi start dell'oracolo, non di collisioni fisiche nuove: il radar high degrada associazione e continuità delle tracce (un link mancato e 123 entità anonime per ciascuna combinazione). Le altre quattro combinazioni radar low/nominal hanno 2/2 start. Le soglie e la logica restano invariate. Il dettaglio e i limiti del vecchio smoke sono nella sezione S04 sopra.

## Aggiornamento protocollo: depth camera

Dal 2026-10-21 le acquisizioni RTK/5G future disabilitano `sensors.depth_camera.enabled` in `configs/default.yaml`. `RawVehicleAgent` riceve quindi una specifica depth nulla: non costruisce `CameraSensor` depth, executor o stimatore temporale. `VehicleLogger` crea `depth/observations.npz` solo quando i metadati attestano una camera depth configurata; per le acquisizioni nuove il campo resta `null` e non viene creato un flusso depth. Radar e RGB restano configurati. Il test mirato istanzia l'agente con le dipendenze CARLA isolate, verifica che il solo `CameraSensor` istanziato sia RGB, scrive un frame radar e processa RGB in memoria, poi controlla che metadata RGB e NPZ radar esistano e la directory depth no.

L'audit delle dipendenze trova lettura depth soltanto nei tool diagnostici separati (`scripts/validate_observations.py` e audit radar/depth). Il percorso di ricostruzione/fusione non chiama il loader di osservazioni `source="depth"`; carica radar e pose GNSS/ego. I callback collisione arrivano dai sensori CARLA `sensor.other.collision` e dalla ground truth privilegiata. Le metriche campagna consumano valutazione/ricostruzione, ground truth e collisioni, senza leggere file depth. Le variabili `depth` in `tracking.py`, `anonymous.py` ed `event_oracle.py` sono distanze geometriche/range radar, non il flusso della camera. Il comparatore ora fa bloccare il gate solo a canali radar/RGB assenti o incompleti; segnala depth assente/incompleta come dato advisory. La tabella sensori mantiene i conteggi di tutte le sorgenti.

L'aggiornamento non riscrive la valutazione storica né i raw: tutti i 22 run NEW già acquisiti avevano depth attiva, come indicano i loro `vehicles/*/metadata.json`; i relativi file sono conservati. In precedenza solo 1/50 canali depth NEW era completo, mentre 50/50 radar e 50/50 RGB erano completi. Il precedente valore del gate depth **0/22** riportato nella sezione del confronto è una valutazione pre-aggiornamento; con il protocollo attuale il gate richiesto radar/RGB è **22/22**, senza cambiare i dati o le statistiche archiviate. Non ho riacquisito quei 22 run per rimuovere depth.

Test dopo la modifica: **25 passed** tra `test_depth_camera_protocol.py`, `test_reacquisition_comparison.py`, `test_radial_velocity_sign.py`, `test_rgb_jpeg.py` e `test_depth_observations.py`. La suite completa sopra è stata eseguita prima di questa modifica; la riesecuzione mirata copre configurazione, istanziazione, logger, completezza e compatibilità del supporto storico depth.

### Manifest, controller e gate residui

Il manifest `results/robustness/rtk5g_current/manifest.json` resta **PRELIMINARY** con `version_tag_commit=null`. Il controller sul percorso `rtk5g_current` non e attivo e registra 0 job. Il controller predefinito riporta i 3.775 record della campagna congelata storica (3.774 latest complete, 0 latest failed); quei dati sono anteriori a questo lavoro e non sono stati modificati. Non e stato creato alcun tag di freeze e la campagna massiva non e stata avviata.

#### Riproducibilita G0 sulle 22 baseline

Il rerun offline ha completato **22/22 job G0, 0 falliti** e ha eliminato ogni copia di lavoro temporanea dopo il job. Solo **2/22 grafi** sono identici al grafo canonico salvato (le due varianti S04); le firme degli eventi coincidono in **8/22**. Le metriche aggregate sono associazione 1,0, collision recall 1,0, tutti i recorder allineati 1,0, event recall 0,9194, 28 eventi aggiuntivi, un link mancato, zero merge falsi e p95 della differenza temporale eventi 0,50 s. La riproducibilita G0 completa **non passa**; nessun raw o risultato canonico e stato sovrascritto. Dati riproducibili: [`jobs.jsonl`](../results/robustness/rtk5g_current/g0_baseline_22/jobs.jsonl), [`summary.json`](../results/robustness/rtk5g_current/g0_baseline_22/summary.json), [`summary.csv`](../results/robustness/rtk5g_current/g0_baseline_22/summary.csv), [`summary.md`](../results/robustness/rtk5g_current/g0_baseline_22/summary.md). I due run identici sono `S04/run_0_a_front_pushed` e `S04/run_0_b_rear_first`; i run con firma eventi identica sono enumerati nei job JSON.

#### Smoke GNSS G1/G2 con il modello bianco finale

Sono stati eseguiti **14 job, 14 complete, 0 failed**, con seed smoke 0: profili GNSS RTK e degradato su S01, S04, S14 e S19 (8 job), piu 6 combinazioni radar low/nominal/high e GNSS RTK/degradato su S04. Lo smoke e un controllo mirato a un seed e non sostituisce gli intervalli indipendenti della sezione GNSS. Tutti i 6 job combinati hanno collision recall 3/3 e recorder alignment 3/3. I job di profilo sono in [`jobs.jsonl`](../results/robustness/rtk5g_current/final_white_g1_g2_smoke/jobs.jsonl); riepiloghi [`summary.json`](../results/robustness/rtk5g_current/final_white_g1_g2_smoke/summary.json), [`summary.csv`](../results/robustness/rtk5g_current/final_white_g1_g2_smoke/summary.csv) e [`summary.md`](../results/robustness/rtk5g_current/final_white_g1_g2_smoke/summary.md).

S04 high riproduce l'anomalia anche con il profilo bianco finale: G1 e G2 trovano **7 `CRITICAL_TTC_START`, 2 attesi, 2 abbinati**. I riepiloghi finali confermano conteggi e abbinamenti, ma `jobs.jsonl` non conserva l'identita dei singoli eventi. Il dettaglio del precedente smoke riportato sopra attribuiva i 5 start non abbinati a quattro istanze anonime distinte piu una duplicazione (`C/anonymous @ -3,15 s` due volte; inoltre `B/anonymous @ -4,30 s`, `B/anonymous @ -2,85 s`, `C/anonymous @ -1,05 s`); questa attribuzione non e stata ri-verificata nel run finale a rumore bianco. I cinque sono falsi start rispetto all'oracolo nei dati del precedente smoke, non collisioni ground-truth nuove. Entrambi gli eventi fisici attesi risultano abbinati anche nel run finale; permane un link mancato e 123 track anonimi, 122 senza veicolo. Fusion-centre median: 2,685 m con GNSS RTK e 2,285 m con GNSS degradato. Low e nominale mantengono 2/2 start e nessun link mancato. Soglie e ricostruzione restano intatte.

#### S10 ripetuto con la configurazione sensori originale

Il repeat S10 usa seed 0, variante `deflected_into_c`, la stessa mappa e gli stessi sensori dei 22 run: radar baseline, RGB a 10 Hz e depth a 20 Hz. L'unica override sensore e stata `sensors.depth_camera.enabled=true`; `simulation.port=2000` collega il server CARLA 0.9.15 gia attivo e non modifica la configurazione sensori. I metadati depth sono presenti per A/B/C e il comparatore conferma che la configurazione statica di ogni canale radar/RGB/depth coincide con la riacquisizione NEW. E un singolo run diagnostico in `F:/CarlaGraph_RTK5G_archive_20261021/S10_REPEAT_DEPTH_ON/traces/S10/run_0_deflected_into_c`, separato dai 22 run. Raw: 51 file, 22.856.756 byte, SHA-256 tree `f2ff096574811c6fcbd9cb879ac30178f7ad4e11870468e6a6a9ff20c657ee49`. Non e stato scritto alcun output di ricostruzione ne alterato alcun raw storico.

A-B ricompare a 3,85 s e il primo contatto A-C a 4,75 s; i trigger e la durata coincidono. Il repeat non replica la persistenza OLD ne quella NEW. OLD ha un burst A-C continuo 4,75-14,00 s (186 tick, 10.527,5 N*s). NEW ha 4 episodi A-C, 4,75-7,60 s complessivi (43 tick, 8.120,5 N*s). Il repeat ha 18 episodi A-C tra 4,75 e 13,95 s (132 tick, 7.975,8 N*s): il primo dura fino a 6,80 s (39 tick, 7.809,7 N*s), poi sono ricontatti intermittenti a basso impulso. Non compaiono nuove coppie veicolari, ma la continuita del contatto cambia e il gate fisico fallisce sia contro OLD sia contro NEW. Errore massimo di percorso dal punto iniziale: repeat vs OLD A 0,369 m / C 0,289 m; repeat vs NEW A 0,089 m / C 0,084 m (B 0,022 m). Dati per riga e overlays: [`s10_repeat_comparison.json`](../results/robustness/rtk5g_current/reacquisition/s10_repeat/s10_repeat_comparison.json), [OLD vs repeat](../results/robustness/rtk5g_current/reacquisition/s10_repeat/old_vs_repeat.png), [NEW vs repeat](../results/robustness/rtk5g_current/reacquisition/s10_repeat/new_vs_repeat.png). L'indice d'acquisizione NEW resta [`reacquisition_run_manifest.csv`](../results/robustness/rtk5g_current/reacquisition/reacquisition_run_manifest.csv); il repeat e separato e non sostituisce nessuna acquisizione.

### Decisione sul protocollo e blocchi prima della campagna

La depth camera e disattivata per le **future** acquisizioni e il suo flusso non e piu una condizione di completezza; il gate di completezza radar/RGB risulta **22/22 PASS**. I 22 run NEW gia raccolti conservano la loro depth attiva, i metadati reali e tutti i raw. La validazione mirata dopo la modifica ha **25 passed**. La suite completa immediatamente precedente alla modifica ha **619 passed, 5 failed, 3 warnings**; i cinque failure storici sono gli stessi del commit originale, come confrontato nella sezione iniziale.

La campagna resta bloccata da due gate scientifici non superati: (1) G0 non riproduce in modo identico i grafi canonici (2/22 identici; 8/22 firme eventi); (2) S10 mostra contatti A-C fisicamente diversi tra OLD, NEW e repeat anche usando la stessa configurazione sensori. S04 radar high conserva inoltre falsi start di evento e forte frammentazione d'associazione, da tenere esplicitamente nel giudizio. Il limite diagnostico RGB resta che i raw conservano contatori e non sequenze di frame/timestamp; i metadata non mostrano drop, ma non permettono una stima indipendente della cadenza effettiva. Nessuna ricostruzione, soglia, traiettoria canonica, campagna storica o metrica GNSS e stata cambiata.
