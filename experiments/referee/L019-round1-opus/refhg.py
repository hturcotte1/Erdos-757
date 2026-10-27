"""Referee L019 round 1 (opus): independent 3-graph routines. Shares no code with experiments/prover/L019/hg.py or
experiments/20261027-0300-transversal-richness/pyverify.py.

- tau_bb: transversal number by branch and bound on a vertex of maximum degree (include / forbid), with a greedy
  disjoint-edge (packing) lower bound. Cross-checked against brute force over vertex subsets (tau_brute).
- edge_table: e(S) for all S subset of V by a subset-sum (zeta) transform in numpy (exact int16), for n <= 23.
- p3_ok_table / saturated_sets: (P3) and saturated sets from the table (brute force over all subsets).
- p3_ok_flow: (P3) for larger n by an independent criterion: for every pair {a,b}, the edges admit a system of distinct
  representatives avoiding a and b (Hall). Implemented with a simple augmenting-path (Kuhn) matching written here.
- f7_copies: all copies of F7 = {012,034,056,135,246}: two disjoint edges g1,g2, a centre c outside both, and a bijection
  sigma: g1 -> g2 with {c,a,sigma(a)} an edge for every a in g1.
- linear, degrees, common neighbours, folds (own relabelling), AP hypergraphs of integer sets.
Exact integer arithmetic throughout."""
import itertools
from collections import defaultdict

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None


def read_cell(path, K=None):
    out = []
    with open(path) as fh:
        for line in fh:
            a = line.split()
            if not a:
                continue
            a = list(map(int, a))
            n, m, t = a[0], a[1], a[2]
            assert len(a) == 3 + 3 * m, (path, len(a), m)
            E = [tuple(sorted(a[3 + 3 * i:6 + 3 * i])) for i in range(m)]
            out.append((n, m, t, E))
            if K is not None and len(out) >= K:
                break
    return out


def masks_of(E):
    return [sum(1 << x for x in g) for g in E]


def tau_bb(E):
    """minimum transversal size of the 3-graph with edge list E (vertex labels arbitrary ints >= 0)."""
    ms = list(set(masks_of(E)))
    if not ms:
        return 0
    best = [len(ms)]

    def packing(ms):
        used = 0
        c = 0
        for e in sorted(ms, key=lambda e: bin(e).count('1')):
            if not e & used:
                used |= e
                c += 1
        return c

    def rec(ms, k):
        if not ms:
            if k < best[0]:
                best[0] = k
            return
        for e in ms:
            if e == 0:
                return
        if k + packing(ms) >= best[0]:
            return
        cnt = defaultdict(int)
        for e in ms:
            x = e
            while x:
                b = x & -x
                cnt[b] += 1
                x ^= b
        b = max(cnt, key=lambda bb: (cnt[bb], -bb))
        rec([e for e in ms if not e & b], k + 1)
        rec([e & ~b for e in ms], k)

    rec(ms, 0)
    return best[0]


def tau_brute(n, E):
    ms = masks_of(E)
    for k in range(0, n + 1):
        for T in itertools.combinations(range(n), k):
            tm = sum(1 << x for x in T)
            if all(e & tm for e in ms):
                return k
    raise AssertionError


def slack(n, E, t=None):
    if t is None:
        t = tau_bb(E)
    return 3 * n + 2 * len(E) - 11 * t


def degrees(n, E):
    d = [0] * n
    for g in E:
        for x in g:
            d[x] += 1
    return d


def linear(E):
    S = [frozenset(g) for g in E]
    if any(len(g) != 3 for g in S) or len(set(S)) != len(S):
        return False
    seen = set()
    for g in S:
        for p in itertools.combinations(sorted(g), 2):
            if p in seen:
                return False
            seen.add(p)
    return True


def f7_copies(E):
    Es = set(frozenset(g) for g in E)
    El = sorted(Es, key=lambda g: tuple(sorted(g)))
    at = defaultdict(int)
    for g in Es:
        for x in g:
            at[x] += 1
    verts = sorted(at)
    res = []
    for g1, g2 in itertools.combinations(El, 2):
        if g1 & g2:
            continue
        A = sorted(g1)
        for c in verts:
            if c in g1 or c in g2 or at[c] < 3:
                continue
            for perm in itertools.permutations(sorted(g2)):
                if all(frozenset((c, a, b)) in Es for a, b in zip(A, perm)):
                    res.append((c, tuple(A), perm))
    return res


def edge_table(n, E):
    assert n <= 23
    f = np.zeros(1 << n, dtype=np.int16)
    for g in E:
        f[sum(1 << x for x in g)] += 1
    for i in range(n):
        bit = 1 << i
        v = f.reshape(-1, 2 * bit)
        v[:, bit:] += v[:, :bit]
    return f


_pc_cache = {}


def popcounts(n):
    if n not in _pc_cache:
        pc = np.zeros(1 << n, dtype=np.int16)
        for i in range(n):
            bit = 1 << i
            v = pc.reshape(-1, 2 * bit)
            v[:, bit:] += 1
        _pc_cache[n] = pc
    return _pc_cache[n]


def p3_ok_table(n, E):
    f = edge_table(n, E)
    pc = popcounts(n)
    bad = (pc >= 2) & (f > pc - 2)
    return not bool(bad.any())


def saturated_sets(n, E, f=None):
    """all S (as bitmasks) with |S| >= 3 and e(S) = |S| - 2."""
    if f is None:
        f = edge_table(n, E)
    pc = popcounts(n)
    idx = np.nonzero((pc >= 3) & (f == pc - 2))[0]
    return [int(i) for i in idx]


def _sdr_avoid(E, a, b):
    """True iff the edges of E have distinct representatives, none equal to a or b (Kuhn's algorithm)."""
    owner = {}

    def try_edge(i, visited):
        for x in E[i]:
            if x == a or x == b or x in visited:
                continue
            visited.add(x)
            if x not in owner or try_edge(owner[x], visited):
                owner[x] = i
                return True
        return False

    for i in range(len(E)):
        if not try_edge(i, set()):
            return False
    return True


def p3_ok_flow(E):
    V = sorted(set(x for g in E for x in g))
    E = [tuple(g) for g in E]
    if len(E) > max(len(V) - 2, 0) and len(V) >= 2:
        return False
    for a, b in itertools.combinations(V, 2):
        if not _sdr_avoid(E, a, b):
            return False
    return True


def in_C(n, E, use_table=True):
    if not linear(E):
        return False
    if f7_copies(E):
        return False
    if use_table and n <= 22:
        return p3_ok_table(n, E)
    return p3_ok_flow(E)


def adjacent(E, y, z, avoid=None):
    return any(y in g and z in g for g in E if avoid is None or avoid not in g)


def common_neighbours(E, y, z, avoid):
    Ny = set(); Nz = set()
    for g in E:
        if avoid in g:
            continue
        if y in g:
            Ny |= set(g) - {y}
        if z in g:
            Nz |= set(g) - {z}
    return (Ny & Nz) - {y, z, avoid}


def fold(n, E, x, y, z):
    """K-degree-2 vertex x deleted, y and z identified into a NEW vertex zeta. Returns (n2, E2, zeta_label, raw_images)
    where E2 is relabelled to range(n2) (zeta gets label n2-1) and raw_images are the images as tuples (possibly
    degenerate / repeated: no dedup, no sorting of duplicates away)."""
    keep = [u for u in range(n) if u not in (x, y, z)]
    lab = {u: i for i, u in enumerate(keep)}
    zeta = len(keep)
    lab[y] = zeta
    lab[z] = zeta
    imgs = []
    for g in E:
        if x in g:
            continue
        imgs.append(tuple(lab[u] for u in g))
    return len(keep) + 1, imgs, zeta


def ap_edges(A):
    A = sorted(A)
    S = set(A)
    idx = {a: i for i, a in enumerate(A)}
    E = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and s // 2 in S and A[i] < s // 2 < A[k]:
                E.append((i, idx[s // 2], k))
    return E


def components(n, E):
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for g in E:
        for u in g[1:]:
            ra, rb = find(g[0]), find(u)
            if ra != rb:
                par[ra] = rb
    comps = defaultdict(list)
    for v in range(n):
        comps[find(v)].append(v)
    return list(comps.values())


def induced(n, E, keep):
    keep = sorted(keep)
    lab = {u: i for i, u in enumerate(keep)}
    ks = set(keep)
    return len(keep), [tuple(lab[u] for u in g) for g in E if set(g) <= ks]
