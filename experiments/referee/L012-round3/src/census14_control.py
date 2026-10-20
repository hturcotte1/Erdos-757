"""Referee L012 round 3: two-sided control of bareal on the 2,910 saturated extremal 14-point classes (data/census_n14_m12_classes.jsonl.gz).
For every census set A (14 points, 12 APs): its AP pattern is computed here (independently of the 'edges' field, which is checked to
agree), bareal is run on the pattern with 'print', and we check that A normalised to [0,1] (or its reflection) is among the printed
realizations.  Every k-th printed realization (k = 97) is re-verified with Fractions: distinct values, AP set == edge set.
Also reports: total assignments, singular, realizations; the (4,5) property of A is re-checked."""
import sys, json, gzip, subprocess
from fractions import Fraction as F
from itertools import combinations
fn = sys.argv[1]; BIN = sys.argv[2]
def aps(x):
    n = len(x); S = set()
    for i, j, k in combinations(range(n), 3):
        a, b, c = sorted((x[i], x[j], x[k]))
        if a + c == 2 * b: S.add((i, j, k))
    return S
def is45(x):
    for Q in combinations(x, 4):
        if len(set(abs(a - b) for a, b in combinations(Q, 2))) < 5: return False
    return True
rows = [json.loads(l) for l in gzip.open(fn, 'rt')]
print('census rows:', len(rows))
lines = []; targets = []
for r in rows:
    A = sorted(r['set']); n = len(A); assert n == 14
    E = aps(A); assert E == set(tuple(sorted(e)) for e in r['edges']), 'edges field disagrees with AP pattern'
    assert len(E) == 12 and is45(A)
    lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in sorted(E)))
    lo, hi = A[0], A[-1]
    t = tuple(F(a - lo, hi - lo) for a in A); targets.append((t, tuple(1 - x for x in t), E))
out = subprocess.run([BIN, '14', 'print'], input='\n'.join(lines) + '\n', capture_output=True, text=True)
assert out.returncode == 0, out.stderr
gi = -1; found = [False] * len(rows); nreal = 0; nver = 0; tot = {}
for l in out.stdout.splitlines():
    if l.startswith('REALIZATION'):
        gi_cur = gi + 1
        h, vals = l.split(':'); D = int(h.split()[1].split('=')[1]); y = [int(v) for v in vals.split()]
        x = tuple(F(v, D) for v in y)
        t, rt, E = targets[gi_cur]
        if x == t or x == rt: found[gi_cur] = True
        nreal += 1
        if nreal % 97 == 0:
            assert len(set(x)) == 14 and aps(list(x)) == E, 'printed realization fails exact re-check'
            nver += 1
    elif l.startswith('STAT'):
        gi += 1
        for kv in l.split()[2:]:
            k, v = kv.split('='); tot[k] = tot.get(k, 0) + int(v)
    elif l.startswith('TOTAL'):
        print(l)
print('graphs processed:', gi + 1, 'own set found for', sum(found), 'of', len(rows), '; realizations printed', nreal, '; re-verified with Fractions', nver)
print('totals:', tot)
