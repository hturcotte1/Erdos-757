# Referee round 2: positive control for rz on A_base (pattern derived here from the set itself).
import subprocess, sys
from fractions import Fraction
A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
n = len(A); pos = {a: i for i, a in enumerate(A)}
edges = []
for i in range(n):
    for k in range(i + 1, n):
        s = A[i] + A[k]
        if s % 2 == 0 and s // 2 in pos: edges.append((i, pos[s // 2], k))
print('A_base: n=%d APs=%d' % (n, len(edges)))
line = 'X: ' + ' '.join('(%d,%d,%d)' % e for e in edges) + '\n'
out = subprocess.run(['./out/rz', str(n), 'print'], input=line, capture_output=True, text=True).stdout
reals = [l for l in out.splitlines() if l.startswith('REAL')]
print(out.splitlines()[-2])
E = set(frozenset(e) for e in edges)
def apset(vals):
    idx = {v: i for i, v in enumerate(vals)}; res = set()
    for i in range(len(vals)):
        for k in range(i + 1, len(vals)):
            mid = (vals[i] + vals[k]) / 2
            if mid in idx: res.add(frozenset((i, idx[mid], k)))
    return res
target = set()
for sgn in (1, -1):
    vals = [Fraction(sgn * a) for a in A]; lo = min(vals); hi = max(vals)
    target.add(tuple((v - lo) / (hi - lo) for v in vals))
ok = 0; found_self = 0; normsets = set()
for l in reals:
    head, vals = l.split(':'); u, v = [int(t.split('=')[1]) for t in head.split()[1:]]
    y = [int(t) for t in vals.split()]; D = y[v]
    x = [Fraction(t, D) for t in y]
    assert x[u] == 0 and x[v] == 1
    assert len(set(x)) == n, 'not distinct'
    assert apset(x) == E, 'AP set differs'
    ok += 1
    lo, hi = min(x), max(x); nx = tuple((t - lo) / (hi - lo) for t in x)
    normsets.add(tuple(sorted(nx)))
    if nx in target: found_self += 1
tsets = set(tuple(sorted(t)) for t in target)
print('realizations re-verified with Fractions: %d; labelled copies equal to A_base (or reflection): %d; distinct normalised sets: %d; A_base among them: %s'
      % (ok, found_self, len(normsets), any(t in normsets for t in tsets)))
