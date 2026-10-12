#!/usr/bin/env python3
"""Offline validation from a clean, immutable analysis checkout into a separate data directory.

Never invokes CARLA acquisition or providers. Raw files are read or hard-linked;
mutable manifests are copied. Publish only derived outputs after the audit.
"""
import argparse
import csv
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/'src'), str(SOURCE/'scripts')]


def read(path):
    record=json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(record,dict) and 'checkpoint_paths' in record:
        return [read(p) for p in record['checkpoint_paths']]
    return record


def write(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=1)+'\n',encoding='utf-8')


def runs(data):
    return sorted((data/'traces').glob('S*/run_*'))+sorted((data/'sweeps').glob('*/S*/run_*'))


def clean_proof(commit):
    def git(*args):
        return subprocess.check_output(['git',*args],cwd=str(SOURCE),text=True).strip()
    if git('rev-parse','HEAD')!=commit or git('status','--porcelain'):
        raise RuntimeError('Analysis source checkout must be clean at the named freeze commit')
    os.environ['CDF_ANALYSIS_FREEZE_COMMIT']=commit
    from cdf.evaluation.provenance import provenance
    from cdf.reconstruction.config import load_config
    return provenance(load_config().to_dict(),extra={'clean_status_output':'','source_checkout':str(SOURCE)})


def stage(original,data,proof):
    if data==original or data==SOURCE or original in data.parents and 'scratch' not in data.relative_to(original).parts:
        raise ValueError('Use a dedicated scratch data directory outside the source checkout')
    selected=sorted((original/'traces').glob('S*/run_*'))+sorted((original/'sweeps').glob('*/S*/run_*'))
    assert len(selected)==257
    raw_hashes={}
    for run in selected:
        dest=data/run.relative_to(original)
        for file in run.rglob('*'):
            if not file.is_file() or 'reconstruction' in file.relative_to(run).parts:continue
            relative=file.relative_to(original);target=data/relative
            raw_hashes[relative.as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():continue
            if file.name=='sweep_manifest.json':shutil.copy2(str(file),str(target))
            else:os.link(str(file),str(target))
    for folder in ['configs','scripts']:
        shutil.copytree(str(SOURCE/folder),str(data/folder),dirs_exist_ok=True)
    write(data/'results/clean_start.json',dict(proof,raw_sha256=raw_hashes,canonical_runs=17,sweep_runs=240))
    print('Staged 17 canonical + 240 sweeps; raw files retained',flush=True)


def refresh(run_name):
    from cdf.reconstruction.pipeline import reconstruct_run
    from cdf.reconstruction.config import load_config
    from cdf.evaluation.reconstruction import evaluate_run
    from cdf.evaluation.fusion_metrics import evaluate_fusion
    from cdf.evaluation.event_oracle import compare_run,prepare_truth
    from cdf.evaluation.run_metrics import run_metrics
    from cdf.evaluation.provenance import provenance
    from body_event_ablation import compare_geometry
    run=Path(run_name);start=time.monotonic();cfg=load_config()
    rec=reconstruct_run(run);rec_time=time.monotonic()-start
    canonical=run.parts[-3]=='traces'
    evaluation=evaluate_run(run,clock_shift_check=canonical)
    fusion=evaluate_fusion(run)
    paired=fusion['_raw']['paired_states'];fusion.pop('_raw')
    truth=prepare_truth(run,cfg)
    semantic=compare_run(run,cfg,truth)
    ablation=compare_geometry(run,{r.owner:r for r in rec.locals},truth)
    prov=provenance(cfg.to_dict(),[str(run)])
    metrics=run_metrics(run,evaluation,fusion)
    out=run/'reconstruction/evaluation'
    write(out/'event_oracle.json',dict(semantic,provenance=prov))
    write(out/'fusion_paired_states.json',dict(provenance=prov,states=paired))
    write(out/'analysis_manifest.json',dict(provenance=prov,metrics=metrics))
    for filename in ['evaluation.json','fusion_metrics.json']:
        result=read(out/filename);result['provenance']=prov;write(out/filename,result)
    manifest=run/'sweep_manifest.json'
    if manifest.exists():
        from run_sweep import classify_outcome
        m=read(manifest)
        m['reconstruction']=dict(prov,wall_s=round(rec_time,2))
        m['evaluation']=dict(provenance=prov,wall_s=round(time.monotonic()-start-rec_time,2),headline=evaluation['headline'])
        m['metrics']=metrics;m['outcome']=classify_outcome(run);m['status']='complete'
        write(manifest,m) # staged copy only; historical recording member unchanged
    return dict(run=str(run),metrics=metrics,fusion=fusion,semantic=semantic,
                ablation=ablation,provenance=prov,wall_s=round(time.monotonic()-start,2))


def parallel(function,items,workers,out):
    complete={r['run']:r for r in read(out)} if Path(out).exists() else {}
    checkpoint_dir=Path(out).with_suffix('')
    def checkpoint(run):
        return checkpoint_dir/(hashlib.sha256(run.encode('utf-8')).hexdigest()+'.json')
    todo=[str(p) for p in items if str(p) not in complete]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(function,p) for p in todo]
        for future in as_completed(futures):
            row=future.result()
            if 'error' in row:raise RuntimeError(str(row))
            complete[row['run']]=row
            write(checkpoint(row['run']),row)
            write(out,dict(checkpoint_paths=[str(checkpoint(name)) for name in sorted(complete)]))
            print(len(complete),'/',len(items),row['run'],row.get('wall_s',''),flush=True)
    return list(complete.values())


def oracle_tables(rows,data,label):
    from cdf.evaluation.event_oracle import CORE_TYPES,MATCH_WINDOW_S,pooled
    from cdf.evaluation.provenance import provenance
    from cdf.reconstruction.config import load_config
    import event_oracle as module
    results=[r['semantic'] for r in rows]
    record=dict(definition='Privileged estimated-body event validation',label=label,runs=len(rows),failed=[],
                event_types=list(CORE_TYPES),match_window_s=MATCH_WINDOW_S,
                provenance=provenance(load_config().to_dict(),[r['run'] for r in rows]),
                pooled=pooled(results),pooled_pre_contact=pooled(results,'comparison_pre_contact'))
    base=data/'results/semantics'/('event_oracle_'+label)
    write(base.with_suffix('.json'),record)
    base.with_suffix('.md').write_text(module.markdown(record),encoding='utf-8')
    with base.with_suffix('.csv').open('w',newline='',encoding='utf-8') as handle:
        fields=['window','comparison','event','found','expected','matched','precision','recall','delta_median_s',
                'delta_p05_s','delta_p95_s','abs_delta_median_s']
        writer=csv.DictWriter(handle,fieldnames=fields);writer.writeheader()
        for window in ['pooled_pre_contact','pooled']:
            for comparison,types in record[window].items():
                for event,row in types.items():
                    writer.writerow(dict(window=window,comparison=comparison,event=event,
                                        **{key:row[key] for key in fields[3:]}))
    module.figure(record,results,data/'results/semantics/figures'/('event_oracle_'+label),'comparison_pre_contact')
    ablation=dict(provenance=record['provenance'],definition='Same tracks, stable target frame and true-body oracle; body vs point geometry only',
                  runs=len(rows),rows={label:pooled([r['ablation'][label] for r in rows],'comparison_pre_contact') for label in ['body','point']})
    write(data/'results/semantics'/('body_point_'+record['label']+'.json'),ablation)


def call_module(name,argv,data_root=None):
    module=importlib.import_module(name)
    if data_root is not None:module.ROOT=data_root
    original=sys.argv;sys.argv=[name]+[str(p) for p in argv]
    try:
        code=module.main()
        if code not in (None,0):raise RuntimeError(name+' failed: '+str(code))
    finally:sys.argv=original


def aggregate(data,rows):
    canonical=[r for r in rows if Path(r['run']).parts[-3]=='traces']
    sweeps=[r for r in rows if Path(r['run']).parts[-3]!='traces']
    oracle_tables(canonical,data,'canonical');oracle_tables(sweeps,data,'sweeps')
    import campaign_summary
    write(data/'traces/campaign_summary.json',[campaign_summary.summarize(Path(r['run'])) for r in canonical])
    from cdf.evaluation.provenance import provenance
    write(data/'traces/campaign_provenance.json',provenance(runs=[r['run'] for r in canonical]))
    import run_sweep
    for path in sorted((SOURCE/'configs/sweeps').glob('*.yaml')):
        run_sweep.summarize(run_sweep.load_sweep(path),data/'sweeps',data/'results/sweeps')
    call_module('fusion_metrics',[*[r['run'] for r in canonical],'--out',data/'traces/fusion_metrics'])
    call_module('fusion_metrics',[*[r['run'] for r in sweeps],'--out',data/'results/sweeps/fusion_metrics'])
    call_module('gt_audit',[*[r['run'] for r in canonical],'--name','gt_audit_final','--index',data/'traces'])
    call_module('worked_example',[data/'traces/S17/run_0_crash'])
    call_module('impulse_symmetry',[*[r['run'] for r in canonical],'--out',data/'results/robustness/impulse_symmetry'])
    selected=[Path(r['run']) for r in canonical]
    for folder in sorted((data/'sweeps').iterdir()):selected+=sorted(folder.glob('S*/run_*'))[:2]
    call_module('event_oracle_independent_check',[*selected,'--output',data/'results/semantics/independent_check.json'],data)


def sensitivity(data,workers):
    import semantic_sensitivity as module
    from cdf.evaluation.provenance import provenance
    from cdf.reconstruction.config import load_config
    rows=parallel(module.one_run,runs(data),workers,data/'checkpoints/sensitivity_runs.json')
    for label in ['canonical','sweeps']:
        subset=[r for r in rows if (Path(r['run']).parts[-3]=='traces')==(label=='canonical')]
        record=dict(definition='One-at-a-time body-event semantic sensitivity; privileged evaluation',label=label,
                    variants_tested=module.VARIANTS,provenance=provenance(load_config().to_dict(),[r['run'] for r in subset]),
                    runs=len(subset),failed=[],variants=module.summarize(subset))
        base=data/'results/semantics'/('sensitivity_'+label);write(base.with_suffix('.json'),record)
        base.with_suffix('.md').write_text(module.markdown(record),encoding='utf-8')
        with base.with_suffix('.csv').open('w',newline='',encoding='utf-8') as handle:
            writer=csv.writer(handle);writer.writerow(['setting','event','recall','precision','delta_median_s','oracle_varied','oracle_nominal','oracle_shift_median_s','oracle_shift_abs_max_s'])
            for key,row in record['variants'].items():
                for event,a in row['agreement'].items():
                    s=row['oracle_shift'][event];writer.writerow([key,event,a['recall'],a['precision'],a['delta_median_s'],s['varied'],s['nominal'],s['delta_median_s'],s['abs_delta_max_s']])


def visual(data):
    import visual_audit
    from cdf.evaluation.provenance import provenance
    viewer=visual_audit._viewer()
    for run in sorted((data/'traces').glob('S*/run_*')):
        record=visual_audit.audit_run(viewer,run,'visual_audit_final')
        record['provenance']=provenance(runs=[str(run)])
        write(run/'reconstruction/evaluation/visual_audit_final/audit.json',record)
        visual_audit.write_markdown(run,'visual_audit_final',record,{})
        print(record['run'],len(record['frames']),'frames',len(record['flags']),'flags',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-root',type=Path,required=True)
    parser.add_argument('--data-root',type=Path,required=True)
    parser.add_argument('--analysis-commit',required=True)
    parser.add_argument('--phase',choices=['stage','reconstruct','aggregate','sensitivity','robustness','visual','figures','qa'],required=True)
    parser.add_argument('--workers',type=int,default=6)
    args=parser.parse_args();data=args.data_root.resolve()
    proof=clean_proof(args.analysis_commit)
    if args.phase=='stage':stage(args.original_root.resolve(),data,proof)
    elif args.phase=='reconstruct':
        rows=parallel(refresh,runs(data),args.workers,data/'checkpoints/validation_runs.json')
        write(data/'results/validation_manifest.json',dict(provenance=proof,
              canonical_runs=sum(Path(r['run']).parts[-3]=='traces' for r in rows),
              sweep_runs=sum(Path(r['run']).parts[-3]!='traces' for r in rows),
              rows=[dict(run=Path(r['run']).relative_to(data).as_posix(),metrics=r['metrics'],provenance=r['provenance']) for r in rows]))
    elif args.phase=='aggregate':aggregate(data,read(data/'checkpoints/validation_runs.json'))
    elif args.phase=='sensitivity':sensitivity(data,args.workers)
    elif args.phase=='robustness':
        import robustness
        robustness.main([*[str(p) for p in sorted((data/'traces').glob('S*/run_*'))],
                         '--work',str(data/'perturbations'),'--results',str(data/'results/robustness'),
                         '--workers',str(args.workers),'--min-seeds','3','--max-seeds','8'])
    elif args.phase=='visual':visual(data)
    elif args.phase=='figures':
        call_module('gnss_relative_results',[data/'results/robustness/jobs.jsonl','--out',data/'results/robustness/figures'])
        call_module('paper_results',['--out',data/'results'],data)
    elif args.phase=='qa':call_module('results_qa',['--results',data/'results'])
    clean_proof(args.analysis_commit)


if __name__=='__main__':main()
