"""Privileged diagnostic (evaluation only). Usage: python scripts/diagnose_body_event_misses.py <data root with traces/ and sweeps/>.

Diagnosis of the missed body-based EGO_PATH_ENTRY onsets (pre-contact, reconstruction vs COVERAGE)."""
import json, sys
from collections import Counter
from pathlib import Path

DATA = Path(sys.argv[1])
cause = Counter(); total = 0; examples = {}
for label, runs in (('sweeps', sorted(DATA.glob('sweeps/*/S*/run_*'))), ('canonical', sorted(DATA.glob('traces/S*/run_*')))):
    cause = Counter(); total = 0
    for run in runs:
        o = json.loads((run / 'reconstruction/evaluation/event_oracle.json').read_text(encoding='utf-8'))
        comp = o['comparison_pre_contact']['RECONSTRUCTION vs COVERAGE']['EGO_PATH_ENTRY']
        total += comp['expected']
        rec = o['events']['RECONSTRUCTION']
        for item in comp['missed']:
            pair, t = item.split('@'); obs, subject = pair.split('/'); t = float(t)
            mine = [e for e in rec.get(obs, []) if e.get('subject') == subject]
            appeared = [e['t_local'] for e in mine if e['type'].startswith('TRACK_APPEARED')]
            entries = [e['t_local'] for e in mine if e['type'] == 'EGO_PATH_ENTRY']
            if not mine:
                c = 'subject never tracked by this observer (identity unknown / not detected)'
            elif entries and min(abs(x - t) for x in entries) > 2.0:
                c = 'entry reconstructed, but more than 2 s from the oracle'
            elif min(e['t_local'] for e in mine) >= t - 0.25:
                c = 'first reconstructed event of the subject at or after the true entry (late identity/track)'
            elif any(e['type'] == 'EGO_PATH_ENTRY' for e in o['events']['COVERAGE'].get(obs, []) if e.get('subject') == subject and e['t_local'] < t - 0.01) or not appeared and min(e['t_local'] for e in mine) < 0.3:
                c = 'subject tracked from the first sweep (already-inside handling / first-seen state)'
            else:
                c = 'tracked before the entry, body entry not detected'
            cause[c] += 1
            examples.setdefault(c, []).append(f'{run.relative_to(DATA).as_posix()} {item}')
    print(label, 'expected', total, 'missed', sum(cause.values()))
    for c, n in cause.most_common():
        print(f'  {n:4d}  {c}')
json.dump({k: v[:10] for k, v in examples.items()}, open(Path('docs/audit/body_event_misses_examples.json'), 'w'), indent=1)
