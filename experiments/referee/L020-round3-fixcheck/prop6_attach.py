"""Round-3 fix check of L020 Step 5.2 (own code, imports nothing from the repo).
For the ten slack<=1 stored lists (Delta<=3, connected classes only): find all NC pairs
(two vertices of degree<=2 not co-transversal, i.e. tau(K-x-y) != tau(K)-2), histogram of
types (dmin,dmax,sigma), and for type (2,2,1) the number of vertices other than x,y lying
in edges that meet {x,y} (the step says 'at most 1+2+2=5'; the parenthetical says 21 of 95 have 4)."""
import sys, itertools
from collections import Counter
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
CELLS = ['3_1_1','10_7_4','14_12_6','17_13_7','8_5_3','12_10_5','15_11_6','19_16_8','22_17_9','26_22_11']
sys.setrecursionlimit(10000)
def parse(path):
    out = []
    for line in open(path):
        a = list(map(int, line.split()))
        if not a: continue
        n, m, t = a[:3]; E = [tuple(a[3+3*i:6+3*i]) for i in range(m)]
        assert len(E) == m and all(len(set(e)) == 3 for e in E)
        out.append((n, m, t, E))
    return out
def connected(n, E):
    adj = {u: set() for u in range(n)}
    for e in E:
        for u in e: adj[u] |= set(e) - {u}
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n
tot_graphs = 0; types = Counter(); att = Counter(); fails = 0
for c in CELLS:
    for (n, m, t, E) in parse(I + 'cell_' + c + '.txt'):
        deg = Counter(u for e in E for u in e)
        if max(deg.values()) > 3 or not connected(n, E): continue
        tot_graphs += 1
        inc = [0] * n
        for i, e in enumerate(E):
            for u in e: inc[u] |= 1 << i
        memo = {}
        def tau(mask):
            if mask == 0: return 0
            r = memo.get(mask)
            if r is not None: return r
            i = (mask & -mask).bit_length() - 1
            r = 1 + min(tau(mask & ~inc[u]) for u in E[i])
            memo[mask] = r; return r
        full = (1 << m) - 1; T = tau(full)
        if T != t: fails += 1; print('TAU MISMATCH', c, T, t)
        low = [u for u in range(n) if deg[u] <= 2]
        for x, y in itertools.combinations(low, 2):
            if tau(full & ~inc[x] & ~inc[y]) == T - 2: continue   # co-transversal
            sig = 1 if (inc[x] & inc[y]) else 0
            dx, dy = sorted((deg[x], deg[y]))
            types[(dx, dy, sig)] += 1
            if (dx, dy, sig) == (2, 2, 1):
                others = set(u for e in E if x in e or y in e for u in e) - {x, y}
                att[len(others)] += 1
print('graphs', tot_graphs, 'NC pairs', sum(types.values()), 'types', dict(sorted(types.items())))
print('type (2,2,1): number of vertices other than x,y in edges meeting {x,y}:', dict(sorted(att.items())))
print('tau mismatches', fails)
