"""Collect all result json files into results.json (counts per case)."""
import json, glob, os
base = '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2/'
R = {}
for f in sorted(glob.glob(base + 'w1_k*_p*of*_n*.json')):
    D = json.load(open(f))
    name = os.path.basename(f)
    R[name] = dict(k=D['k'], nmin=D['nmin'], done_types=D['done_types'], of=D['of'], totals=D['totals'],
                   survivors=[c for c in D['configs'] if c.get('P', 0) < 0])
    R[name]['configs_inC3'] = len(D['configs'])
if os.path.exists(base + 'w2_beta_results.json'):
    D = json.load(open(base + 'w2_beta_results.json'))
    R['w2_beta'] = dict(stats=D['stats'], by_n=D['by_n'], survivors=[c for c in D['configs'] if c.get('P', 0) < 0],
                        A_neg_configs=[c for c in D['configs'] if c.get('A', 0) < 0])
dl = sorted(glob.glob(base + 'w2_delta_results_*.json'))
if dl:
    agg = {}; by = {}; surv = []; Aneg = []
    for f in dl:
        D = json.load(open(f))
        for k, v in D['stats'].items(): agg[k] = agg.get(k, 0) + v
        for k, v in D['by_n'].items(): by[k] = by.get(k, 0) + v
        surv += [c for c in D['configs'] if c.get('P', 0) < 0]
        Aneg += [c for c in D['configs'] if c.get('A', 0) < 0]
    R['w2_delta'] = dict(files=[os.path.basename(f) for f in dl], stats=agg, by_n=by, survivors=surv, A_neg_configs=Aneg)
json.dump(R, open(base + 'results.json', 'w'), indent=1, default=str)
for k, v in R.items():
    print(k, v.get('totals') or v.get('stats'), 'survivors', len(v['survivors']))
