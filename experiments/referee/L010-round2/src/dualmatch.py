"""Dual-graph check of the Delta<=2 cells.  A connected linear 3-graph H with Delta(H)<=2, n vertices, m edges corresponds
(up to isomorphism, bijectively) to a connected simple graph D on the m edges of H, one D-edge per degree-2 vertex of H,
with Delta(D)<=3 and |E(D)| = 3m-n; and tau(H) = m - nu(D) (minimum edge cover with singletons).  Reads graph6 from geng
and reports the matching numbers.  Usage: dualmatch.py m tau0 < g6"""
import sys
def g6(s):
    s = s.strip(); n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    E = []; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: E.append((i, j))
            k += 1
    return n, E
def nu(n, E):  # exact maximum matching by branching on the lowest vertex
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    best = 0
    def rec(free, size):
        nonlocal best
        if size + len(free) // 2 <= best: return
        if not free: best = max(best, size); return
        v = min(free); f2 = free - {v}
        for u in adj[v] & f2: rec(f2 - {u}, size + 1)
        rec(f2, size)
    rec(frozenset(range(n)), 0); return best
m, t0 = int(sys.argv[1]), int(sys.argv[2])
cnt = 0; hist = {}; bad = 0
for l in sys.stdin:
    n, E = g6(l); cnt += 1; k = nu(n, E); hist[k] = hist.get(k, 0) + 1
    if m - k >= t0: bad += 1
print('graphs', cnt, 'nu histogram', dict(sorted(hist.items())), 'with tau(H)=m-nu >=', t0, ':', bad)
