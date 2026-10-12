"""Privileged diagnostic (evaluation only; not part of the frozen tables): which part of the consumer GNSS model makes S18's C and D merge.

Variants on the three S18 canonical runs, seeds 0-2, reconstruction code of the main checkout:
  ref        consumer, common fraction 1.0 (position error shared, heading/velocity independent)
  no_heading ref with heading and velocity errors removed (pure common translation)
  no_head_rtk_declared  no_heading, but the pose sources declare RTK accuracy (gates as with RTK)
  heading_only  no position error, consumer heading and velocity errors (independent)
"""
import dataclasses, json, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'scripts')]
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'traces'
WORK = ROOT / 'robustness' / 'diag_gnss_work'


def variant(name):
    from cdf.robustness.perturb import GNSS_PROFILES
    c = dataclasses.replace(GNSS_PROFILES['consumer'], common_fraction=1.0)
    nohead = dict(yaw_bias_deg=0.0, yaw_markov_deg=0.0, yaw_white_deg=0.0, velocity_white_mps=0.0)
    if name == 'ref': return c, None
    if name == 'no_heading': return dataclasses.replace(c, **nohead), None
    if name == 'no_head_rtk_declared': return dataclasses.replace(c, **nohead), GNSS_PROFILES['rtk']
    if name == 'heading_only':
        return dataclasses.replace(c, bias_m=0.0, markov_m=0.0, white_m=0.0, common_fraction=0.0), None
    raise ValueError(name)


def one(args):
    run, name, seed = args
    import robustness
    from cdf.robustness.perturb import Perturbation, PerturbedPoseSource
    profile, declared = variant(name)
    factory = PerturbedPoseSource.factory(profile, seed)
    def pose(*a, **k):
        source = factory(*a, **k)
        if declared is not None:
            source.position_std_m = declared.position_std_m
            source.yaw_std_rad = __import__('math').radians(declared.yaw_std_deg)
            source.velocity_std_mps = declared.velocity_white_mps
        return source
    robustness.build = lambda job: (Perturbation('diag_' + name, gnss=profile), pose)
    job = dict(run=str(run), family='gnss_correlated', level=name, parameter=None, seed=seed)
    r = robustness.run_job(job, str(WORK), keep=False)
    m = r.get('metrics', {})
    return dict(run=run.name, variant=name, seed=seed, status=r['status'], error=r.get('error'),
                false_merges=m.get('merges_false'), wrong_links=m.get('links_wrong'),
                centre=m.get('fused_centre_error_median_m'),
                rel=r.get('pose_errors', {}).get('relative_position_m', {}).get('rms'),
                head=r.get('pose_errors', {}).get('heading_deg', {}).get('rms'))


if __name__ == '__main__':
    runs = sorted(DATA.glob('S18/run_*'))
    tasks = [(run, v, s) for run in runs for v in ('ref', 'no_heading', 'no_head_rtk_declared', 'heading_only') for s in range(3)]
    with ProcessPoolExecutor(4) as pool:
        rows = list(pool.map(one, tasks))
    out = ROOT / 'docs/audit/gnss_false_merge_mechanism.json'
    out.write_text(json.dumps(rows, indent=1), encoding='utf-8')
    from collections import defaultdict
    agg = defaultdict(list)
    for r in rows: agg[r['variant']].append(r)
    for v, rs in agg.items():
        print(v, 'false merges per draw (3 runs)', sum(r['false_merges'] or 0 for r in rs) / 3,
              'wrong', sum(r['wrong_links'] or 0 for r in rs) / 3,
              'rel', round(sum(r['rel'] or 0 for r in rs) / len(rs), 3), 'head', round(sum(r['head'] or 0 for r in rs) / len(rs), 2),
              [r['error'] for r in rs if r['status'] != 'complete'][:1])
