"""Referee #1 (L021): report of the full check1.py 24 run from check1_pieces.json (its stdout tail was lost when the
shared repository was committed/rewritten at 08:13:34 UTC while the run was in progress; the JSON is written at the very
end of the run), plus the piece table recomputed by brute force, plus comparison with the prover's closure_results.json."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'check1_pieces.json')))
tot = 0
print('cell summary (cell, graphs, irreducible, reducible with A+DEF=0, reducible with A+DEF>0):')
for row in d['summary']:
    print(' ', row); 
    if isinstance(row[1], int): tot += row[1]
print('graphs in all candidate cells with n<=24:', tot, ' non-empty cells:', sum(1 for r in d['summary'] if isinstance(r[1], int) and r[1] > 0))
print('irreducible pieces:', len(d['pieces']))
bad = 0
for p in d['pieces']:
    e = [tuple(x) for x in p['edges']]; n = p['n']; m = len(e)
    t, T = min_transversals_bf(n, e)
    U = 0
    for x in T: U |= x
    L1 = U == (1 << n) - 1; s = 3*n + 2*m - 11*t; W = -A_val(n, m, t)
    ok = L1 and W == p['W'] and W <= 16 and 66*t <= 19*n + 12*m and W <= 11*(n - m)
    bad += not ok
    print(' ', p['name'], 'n,m,tau', (n, m, t), '#minT', len(T), 'L1', L1, 'W', W, 's', s, 'maxdeg', max(degrees(n, e)), 'ok', ok)
print('piece failures:', bad)
pr = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
same = [(a['name'] == b['name'] and [tuple(x) for x in a['edges']] == [tuple(x) for x in b['edges']]) for a, b in zip(d['pieces'], pr)]
print('identical to prover closure_results.json (names and edge lists):', len(pr) == len(d['pieces']) and all(same))
