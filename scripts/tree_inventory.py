#!/usr/bin/env python3
"""Classify tracked paths and optionally remove explicitly superseded generated artifacts."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def category(name,replace_final_audit=False):
    p=Path(name);parts=p.parts
    if name.startswith(('src/','scripts/')) or name in ('pyproject.toml','requirements.txt','.gitignore','.env.example','pytest.ini'):
        return 'SOURCE'
    if name.startswith('configs/'):return 'CONFIG'
    if name.startswith('tests/'):return 'TEST_FIXTURE'
    if name.startswith('traces/') and 'reconstruction' not in parts and len(parts)>=4:
        return 'RAW_CANONICAL'
    if 'visual_audit_final' in name and not replace_final_audit:return 'CURRENT_RESULT'
    if any(part in ['visual_audit_baseline','visual_audit_phase2','visual_audit_phase6',
                    'visual_audit_final','visual_audit_replay_followup','llm'] for part in parts) or any(
                    token in name for token in ['visual_audit_baseline.','visual_audit_phase2.','visual_audit_phase6.',
                    'visual_audit_final.','visual_audit_replay_followup.','gt_audit_baseline.','gt_audit_phase2.',
                    'gt_audit_phase6.','gt_audit_final.','gt_audit_replay_followup.']):
        return 'STALE_GENERATED'
    if name.startswith('docs/audit/') and not p.name.startswith(('fusion_accuracy_', 'final_')):
        return 'HISTORICAL_DEBUG'
    if '/reconstruction/' in name:return 'CURRENT_RECONSTRUCTION'
    if name.startswith(('traces/','results/')):return 'CURRENT_RESULT'
    return 'FINAL_DOCUMENTATION'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--remove-superseded',action='store_true')
    p.add_argument('--rebuild-final-audit',action='store_true',help='explicitly retire the final audit before regenerating it')
    a=p.parse_args()
    paths=subprocess.check_output(['git','ls-files'],cwd=str(ROOT),text=True).splitlines()
    rows=[]
    for name in paths:
        target=(ROOT/name).resolve()
        if ROOT.resolve() not in target.parents:raise ValueError('Path outside repository: '+name)
        kind=category(name,a.rebuild_final_audit);exists=target.is_file()
        remove=a.remove_superseded and kind in ('STALE_GENERATED','HISTORICAL_DEBUG')
        rows.append(dict(path=name,category=kind,bytes=target.stat().st_size if exists else 0,
                         action='removed superseded artifact; retained in Git history' if remove else 'retained'))
        if remove and exists:target.unlink()
    record=dict(definition='Tracked-file classification before the final freeze cleanup',
                tracked_files=len(rows),tracked_bytes=sum(r['bytes'] for r in rows),
                removed_files=sum(r['action'].startswith('removed') for r in rows),
                removed_bytes=sum(r['bytes'] for r in rows if r['action'].startswith('removed')),files=rows)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(record,indent=1)+'\n',encoding='utf-8')
    print(record['tracked_files'],'classified;',record['removed_files'],'superseded files removed')


if __name__=='__main__':main()
