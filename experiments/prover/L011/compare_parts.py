"""(L011) Compare the falsifier's decomposition lists (F/results_parts_check.json, after its isolated-vertex correction) with the
prover's generator G1 of decomp22.py, as sets of multisets of component types (n, m, tau)."""
import json
from decomp22 import gen1, gen2
R = json.load(open('/home/user/Erdos-757/experiments/20261017-0825-n21-n22-via-i11/results_parts_check.json'))
for r in R:
    mine = set(tuple(sorted(tuple(c) for c in x)) for x in gen1(r['N'], r['M'], r['k']))
    mine2 = set(tuple(sorted(tuple(c) for c in x)) for x in gen2(r['N'], r['M'], r['k']))
    theirs = set(tuple(sorted(tuple(c[:3]) for c in x)) for x in r['lists'])
    print((r['N'], r['M'], r['T'], 'slack', r['k']), 'prover G1', len(mine), 'G2', len(mine2), 'falsifier', len(theirs),
          'ALL EQUAL' if mine == mine2 == theirs else 'DIFFERENT')
