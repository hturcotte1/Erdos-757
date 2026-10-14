"""Independent completeness sanity check: all integer pairs in [-60,1120] (and half-integers in a narrower window)."""
import json, itertools, sys
from fractions import Fraction as F
sys.path.insert(0,'.')
from extend import *
R = json.load(open('results.json'))
stored = {frozenset((F(a),F(b))) for a,b,h in R['stored']}
Pxset = candidates(AF); nA = len(ap_edges(AF)); nline = 0
vals = [F(v,2) for v in range(-120, 2241)]   # half-integers in [-60,1120]
vals = [v for v in vals if v not in Aset and single_ok(v)]
print('valid singles', len(vals), flush=True)
cnt = bad = 0; ap_pairs = 0
for x, y in itertools.combinations(vals, 2):
    if not pair_ok(x, y): continue
    E = ap_edges(AF + [x, y])
    inap = set()
    for e in E:
        inap.update(e)
    if x not in inap or y not in inap: continue   # one new point in no AP: generic case (h = h(A+other)+1)
    if x not in Pxset and y not in Pxset and len(E) == nA + 1:
        nline += 1                                  # generic point of a type-2 line: handled abstractly
        if nline % 500 == 1 and witness10(AF + [x, y]) is None: print('LINE-GENERIC WITNESS FAIL', x, y)
        continue
    ap_pairs += 1
    if frozenset((x, y)) not in stored:
        bad += 1
        if bad < 10: print('NOT STORED', x, y)
print('(4,5) pairs with both points in APs, non-line-generic:', ap_pairs, 'missing from stored', bad, 'line-generic (4,5) pairs', nline, 'stored total', len(stored))
