"""C1 (L019): exact check of the folding lemma.
For a linear 3-graph H, a vertex x of degree 2 with edges {x,u,u'}, {x,w,w'} and u,w not in a common edge,
H° = (H - x)/(u~w).  Claims: (a) H° has n-2 vertices and m-2 distinct 3-edges and is linear;
(b) tau(H) <= tau(H°) + 1 always; (c) if x lies in a minimum transversal of H then tau(H°) = tau(H) - 1.
Data: random connected linear 3-graphs (seeded) and the stored class-C lists (slack <= 2).
usage: check_folding.py random N seed | cell path K"""
import sys, random, itertools
from hg import *

def fold(n, E, x, u, w):
    """delete x, merge w into u; relabel to range(n-2)."""
    E2 = [e for e in E if x not in e]
    E3 = []
    for e in E2:
        f = tuple(sorted(u if y == w else y for y in e))
        E3.append(f)
    V = sorted(set(range(n)) - {x, w})
    idx = {y: i for i, y in enumerate(V)}
    E4 = [tuple(sorted(idx[y] for y in e)) for e in E3]
    return len(V), E4

def check_graph(n, E, stats, need_C=False):
    t, Ts = all_min_transversals(n, E)
    co = set()
    for T in Ts:
        for y in range(n):
            if T >> y & 1: co.add(y)
    d = degrees(n, E)
    inE = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): inE.add((a, b))
    for x in range(n):
        if d[x] != 2: continue
        e1, e2 = [e for e in E if x in e]
        A = [y for y in e1 if y != x]; B = [y for y in e2 if y != x]
        for u in A:
            for w in B:
                if (u, w) in inE: continue
                n2, E2 = fold(n, E, x, u, w)
                ok_shape = all(len(set(e)) == 3 for e in E2) and len(set(E2)) == len(E2) == len(E) - 2
                if not ok_shape: stats['shape_fail'] += 1; continue
                t2 = tau(n2, E2)
                stats['folds'] += 1
                if not (t <= t2 + 1): stats['ub_fail'] += 1
                if x in co:
                    stats['folds_cotrans'] += 1
                    if t2 != t - 1: stats['exact_fail'] += 1
                else:
                    stats['folds_noncotrans'] += 1
                    if t2 not in (t - 1, t): stats['range_fail'] += 1
                if need_C:
                    inC = in_C(E2)
                    stats['fold_inC'] += int(inC)
                    if inC:
                        s2 = 3*n2 + 2*len(E2) - 11*t2
                        s = 3*n + 2*len(E) - 11*t
                        if x in co and s2 != s + 1: stats['slack_fail'] += 1
                        if s2 < 0: stats['I11_fail_inC'] += 1

def random_linear(n, m, rng):
    E = []; pairs = set()
    tries = 0
    while len(E) < m and tries < 5000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        ps = [(e[0], e[1]), (e[0], e[2]), (e[1], e[2])]
        if any(p in pairs for p in ps): continue
        E.append(e); pairs.update(ps)
    return E

if __name__ == '__main__':
    stats = dict(folds=0, folds_cotrans=0, folds_noncotrans=0, shape_fail=0, ub_fail=0, exact_fail=0, range_fail=0,
                 fold_inC=0, slack_fail=0, I11_fail_inC=0, graphs=0)
    if sys.argv[1] == 'random':
        N, seed = int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(seed)
        for _ in range(N):
            n = rng.randint(6, 13); m = rng.randint(2, n)
            E = random_linear(n, m, rng)
            V = set(y for e in E for y in e)
            if len(V) < n: continue
            stats['graphs'] += 1
            check_graph(n, E, stats)
    else:
        path, K = sys.argv[2], int(sys.argv[3])
        for (n, m, t, E) in read_cell(path, K):
            stats['graphs'] += 1
            check_graph(n, E, stats, need_C=True)
    print(sys.argv[1:], stats)
