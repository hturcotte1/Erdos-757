"""Referee L009 round 2: Lemma R checked directly on the tight graphs: for every class representative T (6 of (17,13,7), 2 of (14,12,6)),
every vertex u has tau(T-u) = tau(T)-1; for every degree-3 vertex w, T-w has slack 2 and its component types (n_c,m_c,tau_c) form one of
the multisets listed in Lemma R; the three edges at w have pairwise disjoint pairs, none inside an edge of T-w, endpoints of degree <= 2."""
import re, sys, itertools, collections
def tau(es, verts):
    vs = sorted(verts)
    for k in range(len(vs) + 1):
        for T in itertools.combinations(vs, k):
            T = set(T)
            if all(T & set(e) for e in es): return k
def comps(es, verts):
    par = {v: v for v in verts}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    C = collections.defaultdict(set)
    for v in verts: C[f(v)].add(v)
    out = []
    for c in C.values():
        ce = [e for e in es if set(e) <= c]
        out.append((len(c), len(ce), tau(ce, c)))
    return tuple(sorted(out))
L17 = {((16, 10, 6),), ((3, 1, 1), (13, 9, 5)), ((3, 1, 1), (3, 1, 1), (10, 8, 4)), ((6, 3, 2), (10, 7, 4)), ((8, 5, 3), (8, 5, 3))}
L14 = {((13, 9, 5),), ((3, 1, 1), (10, 8, 4))}
for fn, N, t0, allowed in [(sys.argv[1], 17, 7, L17), (sys.argv[2], 14, 6, L14)]:
    seen = collections.Counter()
    for line in open(fn):
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]
        es = [e for e in es if max(e) < N]          # drop the appended edge (14,15,16) of the T14 inputs
        V = set(range(N)); assert {v for e in es for v in e} == V
        assert tau(es, V) == t0
        deg = collections.Counter(v for e in es for v in e)
        for u in V:
            assert tau([e for e in es if u not in e], V - {u}) == t0 - 1, (fn, u)
        for w in [v for v in V if deg[v] == 3]:
            rest = [e for e in es if w not in e]; at = [tuple(x for x in e if x != w) for e in es if w in e]
            ct = comps(rest, V - {w}); assert ct in allowed, (fn, w, ct)
            assert 3 * (N - 1) + 2 * len(rest) - 11 * (t0 - 1) == 2
            assert all(not set(p) & set(q) for p, q in itertools.combinations(at, 2))
            assert all(not set(p) <= set(e) for p in at for e in rest)
            dr = collections.Counter(v for e in rest for v in e)
            assert all(dr[x] <= 2 for p in at for x in p)
            seen[ct] += 1
    print(fn.split('/')[-1], ': all checks pass; component types of T-w over all degree-3 vertices w:', dict(seen))
