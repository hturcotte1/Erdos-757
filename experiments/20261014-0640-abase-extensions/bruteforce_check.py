"""Independent completeness sanity check: all integer pairs in [-60,1120] (and half-integers in a narrower window)."""
import json, itertools, sys
from fractions import Fraction as F
sys.path.insert(0,'.')
from extend import *
R = json.load(open('results.json'))
stored = {frozenset((F(a),F(b))) for a,b,h in R['stored']}
Pxset = candidates(AF)
vals = [F(v,2) for v in range(-120, 2241)]   # half-integers in [-60,1120]
vals = [v for v in vals if v not in Aset and single_ok(v)]
print('valid singles', len(vals), flush=True)
cnt = bad = 0; ap_pairs = 0
for x, y in itertools.combinations(vals, 2):
    # cheap AP pre-test: does the pair create any AP with some new point?
    pts = AF + [x, y]
    s = set(pts)
    new = False
    for a in AF:
        if (a+x)/2 == y or (a+y)/2 == x or (x+y)/2 == a: new = True; break
    if not new:
        # AP with one new point and two A points (x or y in Px)
        if x in Pxset or y in Pxset: new = True
    if not new: continue
    ap_pairs += 1
    if not pair_ok(x, y): continue
    cnt += 1
    if frozenset((x, y)) not in stored:
        # may be x in Px_ok with y generic?? no: that has new AP only if y creates AP; check
        bad += 1; print('NOT STORED', x, y)
print('pairs with new AP', ap_pairs, 'of which 45', cnt, 'missing', bad)
