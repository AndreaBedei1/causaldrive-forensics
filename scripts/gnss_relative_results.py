#!/usr/bin/env python3
"""Measured absolute and pairwise pose errors vs fusion quality (evaluation only)."""
import argparse,csv,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))


def analyse(jobs,out):
    from cdf.evaluation.provenance import provenance
    from cdf.evaluation.figures import DOUBLE_COLUMN_IN,paper_style
    selected=[r for r in jobs if r['status']=='complete' and r['family'] in
              ('baseline','gnss','gnss_refined','gnss_correlated') and r.get('pose_errors')]
    rows=[]
    for r in selected:
        pose=r['pose_errors'];m=r['metrics'];relative=pose['relative_position_m']['rms']
        if relative is None:continue
        rows.append(dict(run=Path(r['run']).parent.name+'/'+Path(r['run']).name,family=r['family'],level=r['level'],
                         seed=r['seed'],absolute_rms_m=pose['absolute_position_m']['rms'],relative_rms_m=relative,
                         fusion_median_m=m.get('fused_centre_error_median_m'),wrong_links=m['links_wrong'],
                         false_merges=m['merges_false'],missed_merges=m['merges_missed'],
                         aligned=m['recorders']==m['recorders_aligned']))
    limits=[]
    for upper in [.05,.1,.25,.5,1.,2.,3.,5.,10.,20.]:
        subset=[r for r in rows if r['relative_rms_m']<=upper]
        if not subset:continue
        errors=sum(r['wrong_links']+r['false_merges'] for r in subset)
        limits.append(dict(relative_rms_upper_m=upper,jobs=len(subset),identity_errors=errors,
                           fraction_aligned=sum(r['aligned'] for r in subset)/len(subset)))
    supported=[r for r in limits if r['jobs']>=20 and r['identity_errors']==0 and r['fraction_aligned']>=.95]
    record=dict(provenance=provenance(runs=sorted({r['run'] for r in rows})),
                definition='Injected input pose: run-level 2-D RMS error; fusion median per run; measured conditions and seeds only. Refined runs use the same injected input errors.',
                reliability_definition='No wrong recorder links or false merges, at least 95% of jobs fully aligned; conservative misses allowed',
                empirical_prefix_limit_m=max([r['relative_rms_upper_m'] for r in supported] or [0]),
                caveat='Conditional sensitivity bound, not a universal GNSS specification. Common translation can preserve identity while degrading absolute fusion accuracy.',
                prefix_limits=limits,rows=rows)
    out.mkdir(parents=True,exist_ok=True)
    (out/'gnss_relative.json').write_text(json.dumps(record,indent=1)+'\n',encoding='utf-8')
    with (out/'gnss_relative.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]) if rows else []);writer.writeheader();writer.writerows(rows)
    plt=paper_style();fig,axes=plt.subplots(1,2,figsize=(DOUBLE_COLUMN_IN,3.0))
    for family in ['baseline','gnss','gnss_refined','gnss_correlated']:
        subset=[r for r in rows if r['family']==family]
        for axis,xkey in zip(axes,['absolute_rms_m','relative_rms_m']):
            valid=[r for r in subset if r['fusion_median_m'] is not None]
            axis.scatter([r[xkey] for r in valid],[r['fusion_median_m'] for r in valid],s=9,alpha=.5,label=family)
            axis.set_xlabel(xkey.replace('_',' '));axis.set_ylabel('Fusion centre error median [m]');axis.grid(alpha=.3)
    axes[1].legend(fontsize=7);fig.tight_layout()
    for suffix in ['svg','pdf']:fig.savefig(str(out/('gnss_relative.'+suffix)))
    plt.close(fig)
    lines=['# Fusion quality vs measured relative pose error','',record['definition'],record['caveat'],'',
           'Empirical zero-identity-error prefix: '+str(record['empirical_prefix_limit_m'])+' m RMS (conditions above).','',
           '| relative RMS upper [m] | jobs | wrong links + false merges | fully aligned |','|--:|--:|--:|--:|']
    lines+=['| {relative_rms_upper_m} | {jobs} | {identity_errors} | {fraction_aligned:.3f} |'.format(**r) for r in limits]
    (out/'gnss_relative.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return record


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('jobs',type=Path);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();analyse([json.loads(line) for line in a.jobs.read_text(encoding='utf-8').splitlines() if line.strip()],a.out)


if __name__=='__main__':main()
