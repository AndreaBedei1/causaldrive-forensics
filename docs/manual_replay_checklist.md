# Controllo manuale dei replay

Tutti i tempi sono **t_global [s]**. Eseguire i comandi nell'ambiente CARLA.
SPACE pausa; frecce seek; N/P evento; C camera; TAB recorder; T punti; G ghost; H help.
Dettagli e keyframe aggiornati dei sette run toccati: [follow-up](../traces/visual_audit_replay_followup.md).
Gli altri run conservano il [visual audit precedente](../traces/visual_audit_final.md).

| Comando | Momenti da guardare | Cosa verificare |
|---|---|---|
| `python scripts/replay_run.py traces/S01/run_0_crash` | -2.35, 0, +0.50 | Avvicinamento, critical, contatto A-B; critical della coppia termina al contatto. |
| `python scripts/replay_run.py traces/S02/run_0_crash` | -3.65, -3.55, -3.40, -2.85, 0 | CUT_IN prima di CRITICAL (gap 0.25 s); a -3.55 solo CUT_IN; poi path entry e collisione A-B. |
| `python scripts/replay_run.py traces/S02/run_0_critical_before_cut_in` | -1.50, -1.15, -0.45, 0 | Critical prima del cut-in, path entry, contatto. |
| `python scripts/replay_run.py traces/S03/run_0_crash` | -1.55, 0, +0.50 | Crossing, due recorder, critical chiuso al contatto. |
| `python scripts/replay_run.py traces/S06/run_0_a_front_pushed` | 0, +0.50, +0.65 | Sequenza A-B, B-C, nuovo A-B; nessuna confusione tra partner. |
| `python scripts/replay_run.py traces/S06/run_0_b_rear_first` | -1.55, 0, +0.50 | B-C prima di A-B; critical delle rispettive coppie termina. |
| `python scripts/replay_run.py traces/S07/run_0_crash` | -5.40, -1.55, 0 | A-B critical; B-C critical termina separatamente; recorder coerenti. |
| `python scripts/replay_run.py traces/S08/run_0_crash` | -0.45, 0, +1.00, +11.00 | C mantiene A e B distinti: nessun TRACK_LOST o duplicato anonimo. L'EGO_PATH_ENTRY a +0.50 resta extra rispetto all'oracle, senza cambio di identità. |
| `python scripts/replay_run.py traces/S09/run_0_merge_conflict` | -4.95, -3.60, 0 | Path entry, merge conflict, contatto A-B. |
| `python scripts/replay_run.py traces/S10/run_0_rolls_through` | -2.00, -0.15, 0 | Crossing/curva, path entry, critical chiuso al contatto. |
| `python scripts/replay_run.py traces/S12/run_0_near_simultaneous` | -1.25, -0.40, 0 | Critical, path entry; supporto ambiguo UNKNOWN prima del contatto. |
| `python scripts/replay_run.py traces/S15/run_0_deflected_into_c` | 0, +0.55, +0.90, +2.20 | A-B poi A-C; associazioni nominate coerenti, precedente duplicato anonimo eliminato. |
| `python scripts/replay_run.py traces/S16/run_0_consequential` | -0.10, 0, +1.05, +1.30 | Cut-in, A-B poi A-C. WARN: breve frammento van e perdita di A da C. |
| `python scripts/replay_run.py traces/S17/run_0_crash` | -2.20, -1.60, 0, +0.50 | Un solo U1: cut-in, path entry, swerve di A, A-B; niente critical A/B dopo il contatto. |
| `python scripts/replay_run.py traces/S18/run_0_abreast` | -6.20, -2.25, 0, +0.50 | Corpi anonimi distinti. Nessun falso cut-in/path entry da handoff. WARN: frammenti iniziali e cambio numero U. |
| `python scripts/replay_run.py traces/S18/run_0_passing` | -5.55, -1.40, 0, +0.50 | Due corpi distinti, nessun merge C/D; supporto ambiguo solo punti, senza ghost fisico. |
| `python scripts/replay_run.py traces/S18/run_0_platoon` | -6.20, -5.70, 0, +0.50 | Corpi in platoon distinti. WARN: duplicazione iniziale di frammenti, già documentata. |

In S17 accanto al ghost deve comparire solo `U1`; nel pannello `U1 seen by A,B`.
I WARN sono limiti dichiarati. Tutti i 79 keyframe finali dei sette run aggiornati sono stati ispezionati; il controllo interattivo di Andrea resta disponibile con i comandi sopra.
