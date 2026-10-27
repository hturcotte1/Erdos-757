"""Bookkeeping tests for Theorems 1, 2(iv), (Pair) lemma, (Red), on stored class-C lists (all n <= 26, so I11 holds for
every induced subgraph by L016).
For each stored graph K:
 - identity 0.5: s(K-x) = s(K) - 3 - 2 d(x) + 11 (tau(K) - tau(K-x)); x co-transversal <=> tau(K-x) = tau(K)-1;
   for co-transversal x: s(K-x) = s(K) + 8 - 2 d(x)  (Theorem 1 bookkeeping)
 - (Pair): for every pair {y,z} not co-transversal: 2|boundary({y,z})| <= s(K) + 5
 - Theorem 2(iv) with N = 27 >= n(K): tau(K \\ D) <= tau(K) - ceil((2|D| - s(K))/11) for all single edges and a sample of
   edge sets D with |D| in {2,3,4}; for s(K) <= 1 every edge is critical.
 - (Red) with random Z, T: s(K-Z) <= s(K) + 11|T| - 3|Z| - 2|boundary(Z)|.
usage: test_slack.py <path> <K> <seed>"""
import sys, random, itertools, collections, math
from ref import *

path, K, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
st = collections.Counter()
for (n, m, t0, E) in read_cell(path, K):
    V = set(range(n))
    t, Ts, co = cotransversal_vertices(E)
    assert t == t0
    s = 3 * n + 2 * m - 11 * t
    d = degrees(V, E)
    st['graphs'] += 1
    for x in range(n):
        Ex = [e for e in E if x not in e]
        tx = tau(Ex)
        sx = 3 * (n - 1) + 2 * len(Ex) - 11 * tx
        if sx != s - 3 - 2 * d[x] + 11 * (t - tx): st['id05_fail'] += 1
        if (x in co) != (tx == t - 1): st['cotrans_fail'] += 1
        if x in co and sx != s + 8 - 2 * d[x]: st['thm1_fail'] += 1
        if sx < 0: st['I11_fail_sub'] += 1
    # (Pair)
    for y, z in itertools.combinations(range(n), 2):
        if any(y in T and z in T for T in Ts):
            continue
        st['noncotrans_pairs'] += 1
        bd = sum(1 for e in E if y in e or z in e)
        if 2 * bd > s + 5: st['pair_fail'] += 1
    # Theorem 2(iv)
    for g in E:
        Eg = [e for e in E if e != g]
        tg = tau(Eg)
        bound = t - math.ceil((2 - s) / 11)
        if tg > bound: st['iv_single_fail'] += 1
        if s <= 1 and tg != t - 1: st['critical_fail'] += 1
    for _ in range(6):
        k = rng.randint(2, min(4, m))
        D = set(rng.sample(E, k))
        ED = [e for e in E if e not in D]
        tD = tau(ED)
        if tD > t - math.ceil((2 * k - s) / 11): st['iv_multi_fail'] += 1
        st['iv_multi'] += 1
    # (Red)
    for _ in range(6):
        zs = rng.randint(1, max(1, n // 3))
        Z = set(rng.sample(range(n), zs))
        bdZ = [e for e in E if e & Z]
        # T: random transversal of the boundary edges (greedy with random order), then possibly more
        T = set()
        for e in rng.sample(bdZ, len(bdZ)):
            if not (e & T): T.add(rng.choice(sorted(e)))
        EZ = [e for e in E if not (e & Z)]
        tZ = tau(EZ)
        sZ = 3 * (n - zs) + 2 * len(EZ) - 11 * tZ
        if sZ > s + 11 * len(T) - 3 * zs - 2 * len(bdZ): st['red_fail'] += 1
        st['red'] += 1
print(path.split('/')[-1], K, dict(st))
