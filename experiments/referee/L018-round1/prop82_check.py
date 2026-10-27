"""prop82_check.py -- referee's partial check of L018 Proposition 8.2 (own code).
From the census list redk5_free_graphs.txt.gz (unrefereed) select 9 <= n <= 14 with slack <= 5; for each: re-check by brute
force that no (Red) pair has |Z| <= 5; compute the minimum |Z| of a (Red) pair, and for every (Red) Z of minimum size the
structure of H - Z (edges, isolated vertices) and the gap g = tau(H-Z) + tau(E_Z) - tau(H)."""
import gzip, itertools
from collections import Counter

def tau_bb(E):
    if not E:
        return 0
    best = [len(E)]
    def rec(es, k):
        if k >= best[0]:
            return
        if not es:
            best[0] = k; return
        e = es[0]
        for v in e:
            rec([f for f in es if v not in f], k + 1)
    rec([frozenset(e) for e in E], 0)
    return best[0]

def main():
    sel = []
    with gzip.open('/home/user/Erdos-757/experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz', 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            p = line.split()
            E = [tuple(int(x) for x in q.split('.')) for q in p[1:]]
            n = 1 + max(v for e in E for v in e)
            m = len(E)
            if not (9 <= n <= 14):
                continue
            t = tau_bb(E)
            s = 3 * n + 2 * m - 11 * t
            if s <= 5:
                sel.append((n, m, t, s, E))
    print('selected (9<=n<=14, slack<=5):', len(sel), Counter((a[0], a[1], a[2], a[3]) for a in sel))
    summary = Counter()
    for (n, m, t, s, E) in sel:
        vm = [0] * n
        for j, e in enumerate(E):
            for v in e:
                vm[v] |= 1 << j
        memo = {}
        def val(Z):
            F = 0
            for z in Z:
                F |= vm[z]
            if F not in memo:
                memo[F] = tau_bb([E[j] for j in range(m) if (F >> j) & 1])
            return 3 * len(Z) + 2 * bin(F).count('1') - 11 * memo[F], F
        minZ = None; minsets = []
        for k in range(1, n):
            for Z in itertools.combinations(range(n), k):
                v, F = val(Z)
                if v >= 0:
                    minsets.append((Z, v, F))
            if minsets:
                minZ = k
                break
        assert minZ is not None and minZ >= 6, ('Red pair with |Z|<=5 found', E)
        structs = Counter()
        exact = True
        for Z, v, F in minsets:
            rest = [w for w in range(n) if w not in Z]
            ER = [e for e in E if not (set(e) & set(Z))]
            tR = tau_bb(ER)
            iso = sum(1 for w in rest if not any(w in e for e in ER))
            # gap
            g = tR + memo[F] - t
            sR = 3 * len(rest) + 2 * len(ER) - 11 * tR
            if g != 0 or v != s - sR:
                exact = False
            # describe H - Z: number of edges, isolated vertices, components with an edge
            structs[(len(ER), iso, len(rest))] += 1
        summary[(n, m, s, minZ)] += 1
        print('n=%d m=%d tau=%d slack=%d min|Z|=%d #minRedZ=%d H-Z structures (edges, isolated, vertices): %s exact(g=0)=%s'
              % (n, m, t, s, minZ, len(minsets), dict(structs), exact))
    print('summary (n, m, slack, min|Z|):', sorted(summary.items()))

if __name__ == '__main__':
    main()
