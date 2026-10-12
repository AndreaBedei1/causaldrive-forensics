# Controllo manuale dei replay

Tutti i tempi sono **t_global [s]**. Eseguire i comandi nell'ambiente CARLA.
SPACE pausa; frecce seek; N/P evento; C camera; TAB recorder; T punti; G ghost; H help.
Tutti i canonical vengono rigenerati nello stesso [visual audit finale](../traces/visual_audit_final.md).
Tempi ed eventuali WARN definitivi sono nel [report finale](FINAL_VALIDATION_REPORT.md).

| Comando | Momenti da guardare | Cosa verificare |
|---|---|---|
| `python scripts/replay_run.py traces/S01/run_0_crash` | -2.35, 0, +0.50 | Avvicinamento, critical, contatto A-B; critical della coppia termina al contatto. |
| `python scripts/replay_run.py traces/S02/run_0_crash` | -3.85, -3.50, -3.40, 0 | CUT_IN prima di CRITICAL; ingresso del body nel corridor; collisione A-B. |
| `python scripts/replay_run.py traces/S02/run_0_critical_before_cut_in` | -1.50, -1.15, -0.45, 0 | Critical prima del cut-in, path entry, contatto. |
| `python scripts/replay_run.py traces/S03/run_0_crash` | -1.55, 0, +0.50 | Crossing, due recorder, critical chiuso al contatto. |
| `python scripts/replay_run.py traces/S06/run_0_a_front_pushed` | 0, +0.50, +0.65 | Sequenza A-B, B-C, nuovo A-B; nessuna confusione tra partner. |
| `python scripts/replay_run.py traces/S06/run_0_b_rear_first` | -1.55, 0, +0.50 | B-C prima di A-B; critical delle rispettive coppie termina. |
| `python scripts/replay_run.py traces/S07/run_0_crash` | -5.40, -1.55, 0 | A-B critical; B-C critical termina separatamente; recorder coerenti. |
| `python scripts/replay_run.py traces/S08/run_0_crash` | -0.45, 0, +1.00, +11.00 | C mantiene A e B distinti: nessun TRACK_LOST o duplicato anonimo. L'EGO_PATH_ENTRY a +0.50 resta extra rispetto all'oracle, senza cambio di identità. |
| `python scripts/replay_run.py traces/S09/run_0_merge_conflict` | -4.95, -3.60, 0 | Path entry, merge conflict, contatto A-B. |
| `python scripts/replay_run.py traces/S10/run_0_rolls_through` | -2.00, -0.15, 0 | Crossing/curva, path entry, critical chiuso al contatto. |
| `python scripts/replay_run.py traces/S12/run_0_near_simultaneous` | -1.25, -0.40, -0.35, 0, +0.90 | B mantiene A nei tre segmenti dello stesso parent track; nessun nuovo U tra A e A. La dinamica può restare incerta internamente. |
| `python scripts/replay_run.py traces/S15/run_0_deflected_into_c` | 0, +0.55, +0.90, +2.20 | A-B poi A-C; associazioni nominate coerenti, precedente duplicato anonimo eliminato. |
| `python scripts/replay_run.py traces/S16/run_0_consequential` | -0.40, -0.10, 0, +1.05, +1.30 | Ingresso geometrico nel path ammesso; nessun cut-in di C causato dalla rotazione di A. A-B poi A-C. |
| `python scripts/replay_run.py traces/S17/run_0_crash` | -2.20, -2.05, -0.50, 0, +0.50 | Un solo U1: vero cut-in, ingresso body, swerve di A osservata da B, A-B; niente critical A/B dopo il contatto. |
| `python scripts/replay_run.py traces/S18/run_0_abreast` | -6.20, -2.25, 0, +0.50 | Corpi anonimi distinti. Nessun falso cut-in/path entry da handoff. WARN: frammenti iniziali e cambio numero U. |
| `python scripts/replay_run.py traces/S18/run_0_passing` | -5.55, -1.40, 0, +0.50 | Due corpi distinti, nessun merge C/D; supporto ambiguo solo punti, senza ghost fisico. |
| `python scripts/replay_run.py traces/S18/run_0_platoon` | -6.20, -5.70, 0, +0.50 | Corpi in platoon distinti; una appearance e una timeline di stato per observer/entity, anche con più source track. |

In S17 accanto al ghost deve comparire solo `U1`; nel pannello `U1 seen by A,B`.
I WARN ammessi sono limiti dichiarati nel report finale. Il controllo interattivo di Andrea resta disponibile con i comandi sopra.
