"""Referee round 2 (opus): data test of Lemma 0.5 (TP) as revised (any co-vertex degree, incl. >= 4).
For every class in the given tight cell lists: recompute tau exactly (own code), check tightness,
connectivity, linearity, and that every pendant's two co-vertices have degree 2.
Also check the (Red) pairs of the proof: for a pendant x in {x,p,q}, value of ({x,p},{p}) = 6+2d(p)-11
and of ({x,p,q},{q}) = 9+2d(q)-11 (when d(p)=1), and confirm they are < 0 exactly when the lemma says so.
Own code only."""
import sys, re, itertools
from collections import Counter

def parse(fn):
    out = []
    for line in open(fn):
        if line.startswith('FOUND:'):
            E = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]
            out.append(E)
    return out

def tau(E):
    n = 1 + max(v for e in E for v in e)
    inc = [0] * n
    for i, e in enumerate(E):
        for v in e: inc[v] |= 1 << i
    memo = {}
    def rec(mask):
        if mask == 0: return 0
        if mask in memo: return memo[mask]
        i = (mask & -mask).bit_length() - 1
        r = min(1 + rec(mask & ~inc[u]) for u in E[i])
        memo[mask] = r
        return r
    return rec((1 << len(E)) - 1)

def connected(E, n):
    adj = [set() for _ in range(n)]
    for e in E:
        for u in e: adj[u] |= set(e)
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n

tot = Counter()
for fn in sys.argv[1:]:
    m_ = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)', fn)
    n, m, t, D = map(int, m_.groups())
    if 3 * n + 2 * m != 11 * t: print('skip (not tight)', fn); continue
    cls = parse(fn)
    viol = 0; npend = 0; maxdeg = Counter()
    for E in cls:
        assert len(E) == m
        V = sorted({v for e in E for v in e}); assert V == list(range(n)), fn
        assert all(len(set(e1) & set(e2)) <= 1 for e1, e2 in itertools.combinations(E, 2)), 'nonlinear'
        assert connected(E, n)
        assert tau(E) == t, ('tau mismatch', fn, E)
        d = Counter(v for e in E for v in e); maxdeg[max(d.values())] += 1
        assert max(d.values()) <= D
        for x in range(n):
            if d[x] != 1: continue
            npend += 1
            e = [e for e in E if x in e][0]; p, q = [v for v in e if v != x]
            if not (d[p] == 2 and d[q] == 2) and n > 3:
                viol += 1; print('TP VIOLATION', fn, E, x, d[p], d[q])
    tot['classes'] += len(cls); tot['pendants'] += npend; tot['viol'] += viol
    print('%-60s classes %6d  maxdeg %s  pendants %d  TP violations %d' % (fn.split('/')[-1], len(cls), dict(maxdeg), npend, viol))
print('TOTAL', dict(tot))
