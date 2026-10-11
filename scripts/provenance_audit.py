#!/usr/bin/env python3
"""Annotate verifiable historical result provenance without rewriting execution history."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from cdf.evaluation.provenance import verify_equivalence,commit_code_hash


def main():
    verified=[]
    for path in sorted((ROOT/'results').glob('*/*.json')):
        record=json.loads(path.read_text(encoding='utf-8'))
        if 'provenance' not in record:continue
        original=dict(record['provenance'])
        record['provenance']=verify_equivalence(original,['ea0ccb1','11dbc6d'])
        assert record['provenance'].get('git_commit')==original.get('git_commit')
        assert record['provenance'].get('git_dirty')==original.get('git_dirty')
        path.write_text(json.dumps(record,indent=1)+'\n',encoding='utf-8')
        verified.append({'file':path.relative_to(ROOT).as_posix(),'original_commit':original.get('git_commit'),
                         'original_dirty':original.get('git_dirty'),'code_sha256':original.get('code_sha256'),
                         'equivalent_clean_commit':record['provenance'].get('equivalent_clean_commit')})
    out=ROOT/'docs/audit/provenance_equivalence.json'
    out.write_text(json.dumps({'algorithm':'Git path/content SHA-256; no historical git fields changed',
                               'verified_commit_sha256':{c:commit_code_hash(c) for c in ('ea0ccb1','11dbc6d')},
                               'records':verified},indent=2)+'\n',encoding='utf-8')
    print(len(verified),'historical records annotated')


if __name__=='__main__':main()
