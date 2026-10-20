"""(L013, prover) Compare arith13.py's violator cells for n = 23..27 with the worker's arith_results.json files (Step 10.1)."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arith13 import violator_cells
mine = {}
for n in range(23, 28):
    for c in violator_cells(n): mine[(n, c['m'], c['tau'])] = (c['s'], c['dmax'], c['status'].split(' ')[0])
W = {}
for fn in [os.path.join(HERE, '../../20261017-1645-i11-n23-n24/arith_results.json'), os.path.join(HERE, '../../20261017-1720-i11-n26/arith_results.json')]:
    r = json.load(open(fn))
    for n, lst in r.items():
        if not str(n).isdigit(): continue
        for c in lst: W[(c['n'], c['m'], c['tau'])] = (c['slack'], c['dmax'], 'OPEN' if c['status'].startswith('OPEN') else 'EMPTY')
common = sorted(set(mine) & set(W))
print('violator cells n=23..27: mine %d, worker %d, common %d' % (len(mine), len(W), len(common)))
print('only mine:', sorted(set(mine) - set(W)), 'only worker:', sorted(set(W) - set(mine)))
print('differences in (slack, dmax, open/empty):', [(k, mine[k], W[k]) for k in common if mine[k] != W[k]])
