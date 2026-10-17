# Referee round 2: pure-Python exact (Fraction) solver, edge-driven enumeration of injective midpoint maps; compares the multiset of
# exact solution vectors with rz's (dump build) for one class, and the counts (assignments, distinct, realizations).
import sys, re, subprocess
from fractions import Fraction
from collections import Counter
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
idx = int(sys.argv[1]); L = open('out/r4_699.txt').read().splitlines(); E = parse(L[idx]); n = 23; m = len(E)
def solve(mu):
    used = set(mu); un = [w for w in range(n) if w not in used]; u, v = un
    var = [w for w in range(n) if w not in (u, v)]; col = {w: i for i, w in enumerate(var)}; N = len(var)
    rows = []
    for e, j in zip(E, mu):
        r = [Fraction(0)] * (N + 1); r[col[j]] += 2
        for a in e:
            if a == j: continue
            if a == v: r[N] += 1
            elif a != u: r[col[a]] -= 1
        rows.append(r)
    for c in range(N):   # Gauss-Jordan with first-nonzero pivoting, exact
        p = next(i for i in range(c, N) if rows[i][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        pc = rows[c][c]; rows[c] = [x / pc for x in rows[c]]
        for i in range(N):
            if i != c and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[c])]
    x = [Fraction(0)] * n; x[v] = Fraction(1)
    for w in var: x[w] = rows[col[w]][N]
    for e, j in zip(E, mu):
        a, c = [t for t in e if t != j]; assert 2 * x[j] == x[a] + x[c]
    return u, v, tuple(x)
sols = Counter(); dist = real = 0
mu = []
def rec(k, used):
    global dist, real
    if k == m:
        u, v, x = solve(mu); sols[(u, v, x)] += 1
        if len(set(x)) == n:
            dist_ok = True; S = set(x)
            aps = sum(1 for i in range(n) for j in range(i + 1, n) if (x[i] + x[j]) / 2 in S)
            dist += 1; real += (aps == m)
        return
    for w in E[k]:
        if w in used: continue
        mu.append(w); used.add(w); rec(k + 1, used); used.discard(w); mu.pop()
rec(0, set())
out = subprocess.run(['./out/rz_dump', '23'], input=L[idx] + '\n', capture_output=True, text=True).stdout.splitlines()
rzs = Counter()
for l in out:
    if l.startswith('S '):
        a = list(map(int, l.split()[1:])); u, v, y = a[0], a[1], a[2:]; D = y[v]
        rzs[(u, v, tuple(Fraction(t, D) for t in y))] += 1
G = [l for l in out if l.startswith('G ')][0]
print('class %d: python assignments %d distinct %d realizations %d | rz: %s | solution multisets equal: %s'
      % (idx, sum(sols.values()), dist, real, G, sols == rzs))
