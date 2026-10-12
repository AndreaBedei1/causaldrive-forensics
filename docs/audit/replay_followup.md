# Follow-up locale dei replay S08 / S02

HEAD iniziale: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`, working tree pulito.
`git status` e `git log -10 --oneline` verificati prima di lavorare. Nessun reset,
remote usato come verità o push. Commit locale di codice/dati: **`568c7320de5ee9c8b23e63d5cdefb6910b469540`**
(`Preserve radar identity through competing returns and correct S02 crash order`).
Secondo commit: `Document verified replay follow-up closure`, contenente solo
questo riferimento e il [manifest di chiusura](replay_followup_closure.json).
HEAD finale e hash del secondo commit sono riportati nel messaggio finale.
Il manifest verifica il runtime e tutti i source/config/test contro gli oggetti Git
del commit pulito di codice/dati. Un commit non può incorporare il proprio hash nel suo
contenuto senza cambiarlo.

## S08: perdita artificiale, evidenza radar presente

Diagnosi completa sample-by-sample: [s08_track_loss_diagnosis.md](s08_track_loss_diagnosis.md),
[CSV prima](s08_radar_returns_before.csv), [CSV dopo](s08_radar_returns_after.csv),
[audit radar privilegiato](s08_radar_visibility_before.json).
`t_global = t_local(C) - 4.10 s`.

| Momento precedente | t_local C [s] | t_global [s] | A avanti / destra rispetto a C [m] |
|---|---:|---:|---|
| Ultimo sample nominato A e TRACK_LOST segment_1 | 3.65 | -0.45 | 20.505 / -3.928 |
| Primo segment_2 ambiguo | 3.70 | -0.40 | 20.003 / -3.909 |
| Collisione A-B | 4.10 | 0.00 | 16.072 / -3.691 |
| Primo cambio grezzo A→B, box più vicino | 4.15 | +0.05 | 15.766 / -3.482 |
| Primo segment_3 anonimo | 5.10 | +1.00 | 13.000 / -1.842 |
| Ritorno grezzo B→A | 6.00 | +1.90 | 13.000 / -1.842 |

A era ancora nei **raw return frontali**: 15 a 3.65, 27 a 3.70 e 25 a 4.10.
A 3.65, 14 passavano il filtro d'altezza e 13 erano assegnati alla track;
range mediano 16.653 m, azimuth -12.611°, velocità radiale -9.874 m/s.
Nella finestra 2.65–4.65 A resta nel FOV frontale, senza handoff laterale o
occlusione veicolare della linea al centro. L'unico sweep filtrato interamente
a 2.85 viene attraversato correttamente. I return compatibili con box GT estesi
di 0.5 m non sono etichette native: al contatto i box possono sovrapporsi.

La causa è **TRACKER**: l'associazione greedy della track più vecchia assorbiva
return meglio compatibili con la rivale. Il cambio A/B provocava segmentation;
il padding retroattivo di 0.5 s anticipava la fine nominata a 3.65, quando la
track grezza seguiva ancora A. La policy pre-contatto bloccava il successivo
segmento stabile anonimo.

Correzione generale in `tracking.py`: predizioni simultanee e competizione per
return tramite residui normalizzati posizione/Doppler entro i gate esistenti.
Lo smoothing RTS si interrompe attraverso innovazioni Doppler oltre 3σ dopo
competizione tra gate confermati, impedendo che la deviazione post-impatto
inventi una criticità precedente. Nessuna soglia semantica è cambiata.
In `anonymous.py`, una reacquisition nominata richiede continuità temporale,
geometria e velocità persistenti in ogni finestra di 10 sample e nessuna rivale
supportata. Segmenti ambigui e prefissi contaminati restano anonimi; non viene
riaperto lo stitching anonimo attraverso boundary.

Prima: `track_001#segment_1 → A`, poi segment_2 ambiguo, segment_3 anonimo;
track_002 contaminata. Dopo: **C:track_001 → A 0–15.15**, **C:track_002 → B
2.10–15.15**, purezza privilegiata 1.0 ciascuna, nessun TRACK_LOST o duplicato
anonimo. Offset C -4.10 invariato. Qui non serve reacquisition: il tracker
preserva direttamente l'identità.

Eventi di C prima: nessun CUT_IN/CRITICAL, EGO_PATH_ENTRY a 4.65 sulla track_002
contaminata e a 6.25 sul segment_3; stato UNKNOWN durante segment_2.
Dopo: nessun CUT_IN/CRITICAL, un EGO_PATH_ENTRY su A a **4.60 locale / +0.50
globale**. Questo evento resta **extra rispetto all'oracle COVERAGE**, dovuto
all'inviluppo nominale stimato dopo l'urto con identità stabile; non è un cambio
A/B. Gli extra path scendono 2→1. I critical mancati A/C e C/B restano un limite.

## S02: scenario crash anticipato e riregistrato

Modifica confinata agli override `crash` in `configs/scenarios/s02_cut_in.yaml`.
Partecipanti base e variante `critical_before_cut_in` invariati.

| Parametro crash | Prima | Dopo |
|---|---:|---:|
| B_cut_in t_start [s] | 1.0 | 0.2 |
| B_cut_in duration [s] | 2.2 | 2.2 |
| B distanza iniziale forward [m] | 30 | 35 |
| A late_brake t_start [s] | 3.9 | 4.5 |

L'anticipo di B è stato provato prima, da 0.8 fino a 0.0: da solo non bastava.
Distanze 31–34 m e durate 2.0–1.4 s non soddisfacevano ordine e collisione
insieme. A 35 m e start 0.2, gli start meno anticipati 0.4/0.6/0.8 non
raggiungevano l'ordine desiderato. La frenata originale evitava il contatto;
4.4 s produceva ancora near miss, 4.5 s ripristina il contatto posteriore A-B.
È una scelta misurata sulla griglia esplorata, non una prova di minimo continuo
globale. [24 tentativi e configurazioni effettive](s02_crash_trials.json).

| Evento ricostruito | Vecchio t_local [s] | Nuovo t_local [s] | Vecchio t_global [s] | Nuovo t_global [s] |
|---|---:|---:|---:|---:|
| CUT_IN_FROM_LEFT_START | 2.10 | **1.65** | -2.55 | **-3.65** |
| CRITICAL_TTC_START | 1.80 | **1.90** | -2.85 | **-3.40** |
| EGO_PATH_ENTRY | 3.25 | 2.45 | -1.40 | -2.85 |
| Collisione A-B | 4.65 | **5.30** | 0.00 | 0.00 |

**CUT_IN < CRITICAL con 0.25 s di separazione**, poi path entry e collisione.
L'oracle PERFECT, solo evaluation, conferma l'ordine fisico CUT_IN 1.75 <
CRITICAL 1.80: il margine fisico è 0.05 s, mentre quello ricostruito/replay è
0.25 s. Non confondere i due. La frenata di A precede l'urto di 0.8 s (prima
0.75 s), con dinamica dello stesso tipo e partner A-B.

Riregistrato soltanto S02/crash in scratch, poi sostituzione controllata.
Backup **integrale** precedente: `scratch/followup_s02_original_complete/S02/run_0_crash`.
Ogni suo SHA256 è verificato contro l'inventario salvato in
[acquisition_provenance.json](../../traces/S02/run_0_crash/acquisition_provenance.json).
ScenarioSpec effettivo del trial selezionato e YAML finale identici.
Il backup locale è escluso dal Git; la revisione precedente conserva inoltre
i vecchi dati versionati. Le acquisizioni esplorative restano in scratch.

La variante opposta conserva raw e config: **CRITICAL 2.60 < CUT_IN 2.95 <
EGO_PATH_ENTRY 3.65 < collisione 4.10**. Ricostruzione fresca verificata contro
la baseline: clock, associazioni, sample e nodi identici.

## Regressioni, scope e test

[Evidenze machine-readable](replay_followup_regressions.json): ricostruiti in
scratch **98 run già salvati** (17 canonical, 80 sweep S18 adjacent/platoon,
S17 seed27). **Zero false merge e zero wrong recorder link**. Nessuna nuova
acquisizione di sweep. Gli otto raw protetti diversi da S02/crash conservano
gli SHA256 iniziali; il diff raw versionato riguarda esclusivamente S02/crash.

- S07: observed alignment di C -5.95; A/B -5.90, link B:track_001→C invariato.
- S10: offset -5.40, recorder association e sample invariati.
- S17: U1 conserva esattamente source A:track_001, B:track_002, B:track_003 e
  l'intera traiettoria x/y/vx/vy; aggiornati solo i due file con metadati della
  nuova configurazione (global_graph.json e report.md).
- S18: zero false merge su tutti gli 80 sweep verificati e tre canonical.

Rigenerati reconstruction/evaluation, GT audit separati ed export deterministici
dei fatti per i soli sette run con cambiamenti fisici/semantici: S02/crash,
S08, S15, S16, tre S18. Aggiornati campaign_summary e fusion_metrics canonical.
Le tabelle e figure di pubblicazione restano il loro snapshot storico,
esplicitamente indicato in results/README.md; nessuna nuova campagna di studi.
In S07/S10 le strutture scientifiche coincidono; il nuovo campo descrittivo
`reacquired:false` viene normalizzato nel confronto delle associazioni salvate.

Sette test nuovi in `tests/test_replay_followup.py`: nomi S02 richiesti, due test
generali di competizione/smoothing, tre di reacquisition inclusi rivale
indistinguibile e prefisso contaminato. Aspettativa di continuità S08 aggiornata
in `tests/test_road_user_fusion.py`. I test generali non dipendono da GT.

| Suite completa | Baseline | Finale |
|---|---|---|
| Python 3.8 | 481 passed, 723.02 s | **488 passed, 509.25 s** |
| Python 3.14 | 481 passed + 17 subtests, 206.80 s | **488 passed + 17 subtests, 158.87 s** |

La prima full suite 3.14 finale ha rilevato due confronti di metadati S17;
corretti i metadati, il targeted worked example passa (7 test) e la full suite
successiva passa come sopra. Baseline in [replay_followup_baseline.json](replay_followup_baseline.json).
Nessun cambiamento runtime dopo queste full suite.

## Controllo visivo e replay

[Indice nuovo](../../traces/visual_audit_replay_followup.md): **79 keyframe** con
corsie OpenDRIVE, tutti ispezionati, per i soli sette run toccati. Quattro PASS
visivi (S02, S08, S15, S18 passing), tre WARN (S16, S18 abreast/platoon), zero
FAIL. Restano brevi frammenti duplicati/anonimi in S16 e nei due S18; sono
documentati per timestamp e immagine nei rispettivi audit. Il PASS visivo S08
non annulla l'extra semantico dichiarato sopra. I vecchi audit restano storici.

Nell'ambiente Python 3.8 con CARLA:

```console
python scripts/replay_run.py traces/S02/run_0_crash
python scripts/replay_run.py traces/S08/run_0_crash
```

S02: fermarsi a -3.55/-3.45 e verificare CUT_IN già iniziato, CRITICAL ancora
assente. S08: osservare C a -0.45, al contatto, +1 e +11; A/B restano nominati
e distinti. [Checklist aggiornata](../manual_replay_checklist.md).

## Provenienza e vincoli

Gli audit conservano l'HEAD reale di esecuzione `a095...` e **git_dirty=true**:
i dati sono stati prodotti durante il lavoro locale. Il manifest di chiusura
attesta separatamente l'equivalenza con il commit contenente il runtime finale,
senza riscrivere la storia di esecuzione. GT solo negli evaluator/debug esterni,
mai passato al runtime/replay. Export dei fatti deterministico senza provider.

**GT runtime: NO. LLM/provider API calls del repository: ZERO. Push: NO.**
Le acquisizioni e gli audit usano solo CARLA locale e codice del repository.
Lavoro concluso: nessuna ulteriore modifica o campagna prevista.
