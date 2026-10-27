"""Cost model [heuristic] for the missing cells of the I11 recursion (n=28, n=29 record / full, record cell (25,23,11,4)).
Exact class counts where a cell list exists (2150 folder, this folder's out/cells, and the concurrent tight-cells-d4 folder, read only);
elsewhere classes ~ inputs * yield(n,s,D) (log-linear fit on the recursed cells with >=20 inputs and >=5 classes), cost ~ inputs * nodes/input / rate."""
import json, math, sys, os
import numpy as np
import plan2
rows = json.load(open('harvest.json'))
KNOWN = {tuple(r['key']): r['count'] for r in rows}
plan2.exists = lambda k: k in KNOWN
plan2.count = lambda k: KNOWN.get(k)
from plan2 import build, tops_for
# ---- yield fit (D=3)
X = []; y = []
for r in rows:
    n, m, t, D = r['key']
    if D == 3 and (r['route'] or '').startswith('recurse') and r['inputs'] >= 20 and r['count'] >= 5:
        s = r['s']; X.append([1, n, s, s * s]); y.append(math.log(r['count'] / r['inputs']))
X = np.array(X, float); y = np.array(y); coef = np.linalg.lstsq(X, y, rcond=None)[0]; resid = y - X @ coef
RMS = float(np.sqrt((resid ** 2).mean()))
def yield_(n, s, D):
    f = math.exp(coef[0] + coef[1] * n + coef[2] * s + coef[3] * s * s)
    if D == 4: f *= 3
    if D == 2: f = min(f, 0.5)
    return min(f, 50.0)
NPI = {2: 300.0, 3: 1.0e4, 4: 3.0e4}      # ext_d search nodes per input (central); measured 4e2-1e5, median-ish 1e4 for D=3
DIRECT_EST = {(18, 10, 6, 3): (5000, 1500)}   # (classes, core-seconds) [heuristic]
def ncomb(c, kk):
    r = 1.0
    for i in range(kk): r *= (c + i) / (i + 1)
    return r
def evaluate(seen, mult_y=1.0, mult_npi=1.0, rate=1.0e6, d2_sec=0.05):
    est = {}; cost = {}
    def cls(k):
        if k in KNOWN: return KNOWN[k]
        if k in est: return est[k]
        n, m, t, D = k; v = seen[k]; s = 3 * n + 2 * m - 11 * t
        if k in DIRECT_EST: est[k] = DIRECT_EST[k][0]; cost[k] = DIRECT_EST[k][1]; return est[k]
        inputs = 0.0
        for b in v['branches']:
            for dec in b['decs']:
                if dec['comps'] is None: continue
                sz = 1.0
                for ck, kk in dec['comps']: sz *= ncomb(cls(ck), kk)
                inputs += sz
        if D == 2: cost[k] = inputs * d2_sec
        else: cost[k] = inputs * NPI[D] * mult_npi / rate * 1.2
        est[k] = 0.0 if s < 0 else inputs * yield_(n, s, D) * mult_y
        return est[k]
    for k in seen:
        if k not in KNOWN: cls(k)
    return est, cost
def run_target(name, **kw):
    seen = build(tops_for(name)); est, cost = evaluate(seen, **kw)
    return seen, est, cost
if __name__ == '__main__':
    print('yield fit coef', np.round(coef, 3), 'rms ln resid', round(RMS, 2), 'N', len(y))
    out = {}
    scen = {'central': dict(mult_y=1, mult_npi=1, rate=1e6), 'low': dict(mult_y=1 / 2.7, mult_npi=1 / 3, rate=3e6), 'high': dict(mult_y=2.7, mult_npi=3, rate=1e6)}
    allcost = {}
    for name in ('n28', 'n29rec', 'n29full', 'rec25'):
        out[name] = {}
        for sc, kw in scen.items():
            seen, est, cost = run_target(name, **kw)
            tot = sum(cost.values()); out[name][sc] = dict(core_hours=tot / 3600, cells_new=len(cost))
            if sc == 'central':
                top = sorted(cost.items(), key=lambda kv: -kv[1])[:8]
                out[name]['top_cells'] = [dict(cell=list(k), est_classes=round(est[k], 1), core_hours=round(c / 3600, 3)) for k, c in top]
                allcost[name] = {k: (est[k], cost[k]) for k in cost}
    # union cost (shared cells counted once) for n28 + n29rec etc.
    def union(names, sc):
        u = {}
        for nm in names:
            seen, est, cost = run_target(nm, **scen[sc])
            for k, c in cost.items(): u[k] = c
        return sum(u.values()) / 3600
    out['union'] = {'n28+n29rec': {sc: union(['n28', 'n29rec'], sc) for sc in scen},
                    'n28+n29full': {sc: union(['n28', 'n29full'], sc) for sc in scen},
                    'n28+n29rec+rec25': {sc: union(['n28', 'n29rec', 'rec25'], sc) for sc in scen}}
    json.dump(out, open('model_results.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
