#!/usr/bin/env python3
"""Evaluation-only body/point comparison on identical tracks and one body oracle."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from semantic_sensitivity import _reconstruction_events
from cdf.evaluation.event_oracle import compare_run,prepare_truth
from cdf.reconstruction.config import load_config
from cdf.reconstruction.local import collision_contacts,read_jsonl,reconstruct_vehicle

def compare_geometry(run,locals_=None,truth=None):
    run=Path(run);cfg=load_config();truth=truth or prepare_truth(run,cfg)
    evaluation=json.loads((run/'reconstruction/evaluation/evaluation.json').read_text(encoding='utf-8'))
    identity={r['track']:r.get('true_identity') for r in evaluation['tracks']}
    locals_=locals_ or {p.name:reconstruct_vehicle(p,cfg) for p in (run/'vehicles').iterdir() if (p/'ego.jsonl').exists()}
    contacts={owner:collision_contacts(read_jsonl(run/'vehicles'/owner/'collisions.jsonl'),r.clock_origin,cfg.collision,r.ego)
              for owner,r in locals_.items()}
    results={}
    for label,body_based in [('body',True),('point',False)]:
        events=_reconstruction_events(locals_,contacts,identity,cfg.semantics,cfg,body_based)
        results[label]=compare_run(run,cfg,truth,events)
    return results

if __name__=='__main__':
    from cdf.evaluation.event_oracle import pooled
    results=[compare_geometry(Path(p)) for p in sys.argv[1:]]
    for label in ['body','point']:
        print(label,json.dumps(pooled([r[label] for r in results],'comparison_pre_contact')['RECONSTRUCTION vs COVERAGE'],indent=1))
