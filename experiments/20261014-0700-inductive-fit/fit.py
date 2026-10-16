"""Analysis: feasible region of  tau(K) <= b|R| + c e2 + d e1  (a=1) on abstract vs realizable datasets.
Run after build_realizable.py, build_abstract.py {census,census_all500,witnesses,fresh}, classify_census.py."""
import sys, os, json, gzip, glob, itertools
from fractions import Fraction as F
from collections import Counter, defaultdict
from common import *
from lplib import min_var, min_c_given, check, pareto
sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/q8-abstract')
HERE = os.path.dirname(os.path.abspath(__file__))
def load(path):
    p = os.path.join(HERE, path)
    return [json.loads(l) for l in gzip.open(p, 'rt')] if os.path.exists(p) else []
real = load('realizable_tuples.jsonl.gz')
cen = load('abstract_census_tuples.jsonl.gz'); cen500 = load('abstract_census_all500_tuples.jsonl.gz')
wit = load('abstract_witness_tuples.jsonl.gz'); fresh = load('abstract_fresh_tuples.jsonl.gz')
hascore = json.load(open(os.path.join(HERE, 'census_has_core.json'))) if os.path.exists(os.path.join(HERE, 'census_has_core.json')) else None
# census 500 random sample -> index into census to know core status
cen_idx = {r['name']: i for i, r in enumerate(cen)}
def tup(rows): return {(t['tau'], t['R'], t['e2'], t['e1']) for r in rows for t in r['tuples']}
DS = {}
DS['REAL records (7 sets, all 3^n states)'] = tup([r for r in real if r['src'] == 'record'])
DS['REAL random n=12 (300, |D|<=2)'] = tup([r for r in real if r['src'] == 'rand12'])
DS['REAL random n=14 (300, |D|<=2)'] = tup([r for r in real if r['src'] == 'rand14'])
DS['REAL all'] = tup(real)
DS['ABS census n12m10 (|D|<=2, all)'] = tup(cen)
DS['ABS census 500 random, ALL D'] = tup(cen500)
DS['ABS witnesses (103)'] = tup(wit)
DS['ABS fresh class O (10,8,6),(11,9,7),(13,11,8)'] = tup([r for r in fresh if r['src'] == 'fresh_O'])
DS["ABS fresh class O' (K30,K31,cores)"] = tup([r for r in fresh if r['src'] == 'fresh_Op'])
absall = cen + cen500 + wit + fresh
DS['ABS all'] = tup(absall)
if hascore is not None:
    smp = [r for i, r in enumerate(cen) if str(i) in hascore]
    ok = [r for i, r in enumerate(cen) if hascore.get(str(i)) is False]
    ok500 = [r for r in cen500 if hascore.get(str(cen_idx[r['name']])) is False]
    DS["ABS census sample (%d hyp., |D|<=2), NO core filter" % len(smp)] = tup(smp)
    DS["ABS census sample passing FULL cores (%d hyp., |D|<=2)" % len(ok)] = tup(ok)
    DS["ABS census500 passing FULL cores (%d hyp.), ALL D" % len(ok500)] = tup(ok500)
    DS["ABS O'-like: core-passing census + witnesses(op) + fresh O'"] = tup(ok + ok500 + [r for r in wit if r['name'].startswith('op:')] + [r for r in fresh if r['src'] == 'fresh_Op'])
Q8 = (F(3, 7), F(2, 7), F(4, 7))
out = {}
def q8slack(t): return 3 * t[1] + 2 * t[2] + 4 * t[3] - 7 * t[0]
lines = []
P = lambda s='': lines.append(s)
P('| dataset | #distinct tuples | #Pareto | min Q8 slack | #Q8-violating | min b (c,d free in [0,2]) | argmin (b,c,d) | min b at c=2/7,d=4/7 | min b at c=2b/3,d=4b/3 |')
P('|---|---|---|---|---|---|---|---|---|')
for name, T in DS.items():
    if not T: continue
    ms = min(q8slack(t) for t in T); nv = sum(1 for t in T if q8slack(t) < 0)
    b1, a1 = min_var(T, 'b')
    # fixed (c,d) = (2/7,4/7): closed form
    need = max(((F(t[0]) - Q8[1] * t[2] - Q8[2] * t[3]) / t[1] for t in T if t[1] > 0), default=F(0))
    b2 = need if all(not (t[1] == 0 and F(t[0]) > Q8[1] * t[2] + Q8[2] * t[3]) for t in T) else None
    # c=2b/3, d=4b/3 : tau <= b (R + 2e2/3 + 4e1/3)
    b3 = max((F(t[0]) / (t[1] + F(2, 3) * t[2] + F(4, 3) * t[3]) for t in T if t[0] > 0), default=F(0))
    # verify exactly
    assert not check(T, b1, a1['c'], a1['d']) and not check(T, b2, Q8[1], Q8[2]) and not check(T, b3, F(2, 3) * b3, F(4, 3) * b3)
    out[name] = dict(n_tuples=len(T), n_pareto=len(pareto(T)), min_q8_slack=ms, n_q8_viol=nv, min_b_free=str(b1), argmin={k: str(v) for k, v in a1.items()}, min_b_fixed_cd=str(b2), min_b_ratio=str(b3))
    P(f'| {name} | {len(T)} | {len(pareto(T))} | {ms} | {nv} | {b1} = {float(b1):.4f} | ({a1["b"]},{a1["c"]},{a1["d"]}) | {b2} = {float(b2):.4f} | {b3} = {float(b3):.4f} |')
tab1 = '\n'.join(lines); lines.clear()
# min c, d needed at b=3/7
P('| dataset | min c (b=3/7, d free<=2) | min d (b=3/7, c free<=2) | min c at d=4/7 | min d at c=2/7 | min c+d (b=3/7) |')
P('|---|---|---|---|---|---|')
b0 = F(3, 7)
def fm(x): return 'infeasible' if x is None else f'{x} = {float(x):.4f}'
for name, T in DS.items():
    if not T: continue
    c1, _ = min_var(T, 'c', fixed={'b': b0}); d1, _ = min_var(T, 'd', fixed={'b': b0})
    c2 = min_c_given(T, b0, F(4, 7))
    d2, _ = min_var(T, 'd', fixed={'b': b0, 'c': F(2, 7)})
    # min c+d: 2D vertex search on exact via small LP using scipy then check
    from scipy.optimize import linprog
    import numpy as np
    TT = pareto(T); A = [[-t[2], -t[3]] for t in TT]; bb = [-(t[0] - float(b0) * t[1]) for t in TT]
    r = linprog([1, 1], A_ub=A, b_ub=bb, bounds=[(0, 2), (0, 2)], method='highs')
    cd = None if r.status else r.fun
    out[name].update(minc_b37=str(c1) if c1 is not None else None, mind_b37=str(d1) if d1 is not None else None, minc_d47=str(c2) if c2 is not None else None, mind_c27=str(d2) if d2 is not None else None, mincd_b37_float=cd)
    P(f'| {name} | {fm(c1)} | {fm(d1)} | {fm(c2)} | {fm(d2)} | {"infeasible" if cd is None else f"{cd:.4f} [heuristic, float LP]"} |')
tab2 = '\n'.join(lines); lines.clear()
grid = [F(3, 7), F(44, 100), F(45, 100), F(46, 100), F(8, 17)]
P('| dataset | ' + ' | '.join(f'b={g} ({float(g):.4f})' for g in grid) + ' |')
P('|---|' + '---|' * len(grid))
for name, T in DS.items():
    if not T: continue
    cells = []; cur = {}
    for g in grid:
        c = min_c_given(T, g, F(4, 7)); cur[str(g)] = None if c is None else str(c)
        cells.append('infeasible' if c is None else f'{c} = {float(c):.4f}')
    out[name]['curve_d47'] = cur
    P(f'| {name} | ' + ' | '.join(cells) + ' |')
tab3 = '\n'.join(lines); lines.clear()
json.dump(out, open(os.path.join(HERE, 'fit_results.json'), 'w'), indent=1)
open(os.path.join(HERE, 'tables_fit.md'), 'w').write('## Table 1: minimal b\n\n' + tab1 + '\n\n## Table 2: minimal c,d at b=3/7\n\n' + tab2 + '\n\n## Table 3: minimal c at d=4/7 vs b\n\n' + tab3 + '\n')
print(tab1); print(); print(tab2); print(); print(tab3)
