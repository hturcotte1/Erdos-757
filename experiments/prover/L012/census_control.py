"""(L012) Positive control for realize.c on known realizable saturated patterns: for every class of a census file (set + edges with
vertex i = i-th smallest element), run realize (print mode) and check (a) at least one realization, (b) the true set, normalised
to [0,1] (or its reflection), is among the realizations (exact Fractions), (c) every printed realization re-checked in Python:
distinct values whose 3-AP set (exact) is exactly the edge set.  Usage: census_control.py FILE NV LIMIT"""
import sys, json, gzip, subprocess, itertools
from fractions import Fraction as F
f, NV, LIMIT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
op = gzip.open if f.endswith('.gz') else open
if f.endswith('.jsonl.gz'): recs = [json.loads(l) for l in op(f, 'rt')]
else: recs = json.load(op(f, 'rt'))
recs = recs[:LIMIT] if LIMIT > 0 else recs
lines = ['FOUND: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in r['edges']) for r in recs]
out = subprocess.run(['./bin/realize', str(NV), 'print'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
per = []; cur = []
for l in out:
    if l.startswith('REALIZATION'): cur.append(l)
    elif l.startswith('STAT'): per.append((l, cur)); cur = []
assert len(per) == len(recs)
ok_a = ok_b = ok_c = 0; nreal = 0
def aps(x):
    s = sorted(range(len(x)), key=lambda i: x[i]); res = set(); pos = {x[i]: i for i in range(len(x))}
    for a, c in itertools.combinations(range(len(x)), 2):
        mid = (x[a] + x[c]) / 2
        if mid in pos and pos[mid] not in (a, c): res.add(tuple(sorted((a, pos[mid], c))))
    return res
for r, (stat, reals) in zip(recs, per):
    S = r['set']; lo, hi = min(S), max(S); tx = [F(v - lo, hi - lo) for v in S]; rx = [1 - t for t in tx]
    E = set(tuple(sorted(e)) for e in r['edges'])
    if reals: ok_a += 1
    found = False; allok = True
    for l in reals:
        h, vals = l.split(':'); D = int(h.split('=')[1]); x = [F(int(v), D) for v in vals.split()]
        nreal += 1
        if x == tx or x == rx: found = True
        if len(set(x)) != len(x) or aps(x) != E: allok = False
    ok_b += found; ok_c += allok
print(f, 'classes', len(recs), '| with >=1 realization', ok_a, '| true set found', ok_b, '| all printed realizations re-verified', ok_c, '| realizations', nreal)
