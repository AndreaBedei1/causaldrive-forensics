# S08 — diagnosi radar di C e continuità dell'identità

HEAD iniziale: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`, working tree pulito.
La diagnosi usa GT esclusivamente nello script privilegiato separato
`scripts/debug_track_loss.py` e nell'audit `scripts/audit_radar_visibility.py`.
Nessun risultato privilegiato è input della reconstruction, fusion o replay.

## Tempi esatti prima del fix

In questo run `t_global = t_local(C) - 4.10 s`.

| momento | t_local C [s] | t_global [s] | posizione di A rispetto a C: avanti/destra [m] |
|---|---:|---:|---|
| ultimo sample del segmento nominato A; TRACK_LOST segment_1 | 3.65 | -0.45 | 20.505 / -3.928 |
| primo sample segment_2, marcato ambiguo | 3.70 | -0.40 | 20.003 / -3.909 |
| collisione A–B | 4.10 | 0.00 | 16.072 / -3.691 |
| primo cambio A→B del punto tracciato grezzo (box GT più vicino) | 4.15 | +0.05 | 15.766 / -3.482 |
| primo sample segment_3, anonimo | 5.10 | +1.00 | 13.000 / -1.842 |
| successivo passaggio B→A del punto tracciato grezzo contaminato | 6.00 | +1.90 | 13.000 / -1.842 |

Il TRACK_LOST a 3.65 non indica assenza di radar: è la fine artificiale del
segmento stabile. La track grezza continua a misurare A anche a 3.70 e fino
all'urto. Il taglio retroattivo deriva dal padding di 0.5 s di un intervallo
di supporto trasversale largo: il primo sweep largo della sequenza è a 4.20.

## RAW_SENSOR / FILTER / TRACKER / OCCLUSION / FOV

La finestra richiesta è 2.65–4.65 s locali, 1 s prima e dopo il TRACK_LOST.
I [CSV prima](s08_radar_returns_before.csv) e [dati per sweep](s08_track_loss_before.json)
riportano ogni sweep di front/left/right, per A e B: conteggio grezzo, filtro
di altezza, range e azimuth min/mediana/max, velocità radiale grezza, FOV,
occlusione della linea al centro, conteggi dopo i filtri runtime e supporto
effettivamente assegnato alle track. Il JSON arriva fino a 7.00 s per coprire
anche la seconda perdita. Le attribuzioni sono compatibilità con box GT
orientati estesi di 0.5 m; al contatto i box possono sovrapporsi e un return
può risultare compatibile con entrambi. Non sono etichette native del sensore.

Al momento della perdita:

- **RAW_SENSOR:** A ha 15 return frontali a 3.65, 27 a 3.70, 25 a 4.10;
  anche dopo il presunto TRACK_LOST il sensore continua a vederla.
- **FILTER:** 14/15 passano il filtro di altezza a 3.65; 13 sono assegnati
  alla track. A 3.70 passano 22/27 e la track ne prende 21. Nella finestra
  c'è un solo sweep senza return di A dopo il filtro, a 2.85 (2 grezzi,
  entrambi scartati); il tracker lo attraversa regolarmente e non coincide
  con la perdita. Dopo lo stop, i return statici restano utilizzabili da
  track già confermate: il limite sulla velocità riguarda la nascita.
- **FOV:** A è nel FOV frontale per tutta la finestra; nessun handoff verso
  i radar laterali e nessun return laterale di A in questi sweep.
- **OCCLUSION:** nessun veicolo blocca la linea al centro di A in questa
  finestra. La presenza effettiva dei return esclude un'occlusione totale.
- **TRACKER:** causa della perdita di identità. La priorità cronologica
  faceva prendere alla track più vecchia tutti i return nel gate di 2.5 m
  e 4 m/s, anche quelli meglio supportati dalla predizione della rivale.
  All'avvicinamento e contatto di A/B, track_001 assorbe return di B,
  mentre track_002 passa da B ad A. Quando entrambe sono ferme, la più
  vecchia torna ad assorbire A e impoverisce la rivale fino alla sua perdita.

A 3.65 il range dei return di A è 16.257–19.451 m (mediana 16.653),
azimuth -15.475–-8.919° (mediana -12.611), velocità radiale -9.972–-9.772
m/s (mediana -9.874). I return di B sono contemporaneamente presenti su
front e left: questo overlap riguarda B, non un cambio di sensore di A.
L'audit privilegiato precedente è conservato in
[s08_radar_visibility_before.json](s08_radar_visibility_before.json).

## Correzione generale e risultato

`tracking.associate_returns` predice tutte le track prima di aggiornarle.
I return contesi sono assegnati in base alla somma dei residui quadratici
di posizione e Doppler, normalizzati ai gate esistenti. Restano la priorità
confirmed/tentative e il tie-break deterministico. Clustering, conferma,
max gap, filtri di altezza e gates non cambiano.

Lo smoothing RTS non retropropaga attraverso un'innovazione Doppler oltre
3 sigma quando vi è stata competizione tra gate confermati nell'ultimo
max gap. La prima candidata senza questa protezione generava un falso
CRITICAL su C a 3.75, retroproiettando la deviazione post-urto di A. La
protezione elimina questo effetto e preserva i run senza competizione,
inclusa l'intera sequenza della variante S02 opposta.

La segmentation e il veto agli stitch anonimi attraverso boundary restano.
`anonymous.link_to_recorders` consente invece una reacquisition nominata di
un segmento successivo stabile: geometria e velocità nuove persistenti in
ogni finestra di 10 sample, mediana entro 1 sigma, continuità temporale con
un segmento già nominato e assenza di una rivale supportata. Una coda lunga
pulita non può nominare un prefisso contaminato. Segmenti ambigui restano
anonimi. Questa regola è testata su dati sintetici, senza nomi o tempi S08.

Nel run S08 corretto C mantiene `track_001 → A` da 0.00 a 15.15 e
`track_002 → B` da 2.10 a 15.15: nessun TRACK_LOST, nessuna segmentation,
nessuna entità anonima duplicata. La valutazione misura purezza 1.0 per
entrambe le track; l'allineamento osservato di C resta -4.10 s.
I [dati dopo](s08_track_loss_after.json) e [CSV dopo](s08_radar_returns_after.csv)
rendono verificabile il risultato sweep per sweep.

## Eventi semantici di C: limite residuo esplicito

Prima: nessun CUT_IN o CRITICAL su C; due EGO_PATH_ENTRY a 4.65 sulla
track_002 contaminata e 6.25 sul segment_3. Durante segment_2 le predizioni
di path/cut-in/critical erano UNKNOWN. Dopo: nessun CUT_IN o CRITICAL,
un solo EGO_PATH_ENTRY su A a 4.60. Nessuna reacquisition è necessaria in
questo run: l'identità continua.

L'EGO_PATH_ENTRY restante è ancora un **extra rispetto all'oracle COVERAGE**:
non va dichiarato un evento fisico confermato. Dipende dalla traiettoria e
dall'inviluppo nominale stimato dopo l'impatto, con identità A stabile, non
da uno scambio A/B. Gli extra path del run scendono 2→1; i CRITICAL mancati
dell'oracle restano quelli precedenti (A/C e C/B). Le definizioni semantiche
e i parametri del modello di rischio non sono stati cambiati per cancellarli.
