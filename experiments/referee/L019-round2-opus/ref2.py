"""Referee #3 (round 2, opus) independent library for spot checks of L019.
Imports nothing from e757/, judge/, experiments/prover/*, pyverify.py or the round-1 referee folders.
Methods deliberately different from the prover's hg.py:
  - tau and all minimum transversals: brute force over vertex combinations of increasing size;
  - F7 copies: brute force over 5-edge subsets (union of 7 vertices, pairwise intersections <= 1,
    degree multiset {3,2,2,2,2,2,2}; this characterises F7, see review);
  - (P3): zeta transform over all vertex subsets (e(S) for every S), then e(S) <= |S|-2 for |S| >= 2.
Everything exact (ints, frozensets)."""
import itertools


def read_cell(path, K=None):
    out = []
    with open(path) as fh:
        for line in fh:
            a = line.split()
            if not a:
                continue
            a = list(map(int, a))
            n, m, t = a[0], a[1], a[2]
            E = [frozenset(a[3 + 3 * i:6 + 3 * i]) for i in range(m)]
            out.append((n, E, t))
            if K is not None and len(out) >= K:
                break
    return out


def is_linear(E):
    seen = set()
    for e in E:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen:
                return False
            seen.add(p)
    return True


def f7_copies(E):
    El = list(set(E))
    res = []
    for five in itertools.combinations(El, 5):
        U = set().union(*five)
        if len(U) != 7:
            continue
        if any(len(a & b) > 1 for a, b in itertools.combinations(five, 2)):
            continue
        deg = {}
        for e in five:
            for x in e:
                deg[x] = deg.get(x, 0) + 1
        if sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]:
            res.append(five)
    return res


def edge_counts(V, E):
    """f[S] = number of edges inside S, for every subset S of V (bitmask over sorted V)."""
    V = sorted(V)
    idx = {v: i for i, v in enumerate(V)}
    N = len(V)
    f = [0] * (1 << N)
    for e in E:
        f[sum(1 << idx[x] for x in e)] += 1
    for i in range(N):
        b = 1 << i
        for S in range(1 << N):
            if S & b:
                f[S] += f[S ^ b]
    return V, idx, f


def p3_ok(V, E):
    V, idx, f = edge_counts(V, E)
    for S in range(1 << len(V)):
        k = bin(S).count('1')
        if k >= 2 and f[S] > k - 2:
            return False
    return True


def in_C(V, E):
    return is_linear(E) and not f7_copies(E) and p3_ok(V, E)


def all_min_T(V, E):
    V = sorted(V)
    idx = {v: i for i, v in enumerate(V)}
    EM = [sum(1 << idx[x] for x in e) for e in E]
    if not EM:
        return 0, [frozenset()]
    for t in range(0, len(V) + 1):
        res = []
        for T in itertools.combinations(range(len(V)), t):
            msk = 0
            for i in T:
                msk |= 1 << i
            if all(em & msk for em in EM):
                res.append(frozenset(V[i] for i in T))
        if res:
            return t, res
    raise RuntimeError


def slack(nv, m, t):
    return 3 * nv + 2 * m - 11 * t


def degrees(V, E):
    d = {v: 0 for v in V}
    for e in E:
        for x in e:
            d[x] += 1
    return d


def adjacent(E, a, b):
    return any(a in e and b in e for e in E)


def fold(V, E, x, y, z):
    zeta = max(V) + 1
    V2 = [v for v in V if v not in (x, y, z)] + [zeta]
    E2 = [frozenset(zeta if a in (y, z) else a for a in e) for e in E if x not in e]
    return V2, E2, zeta


def ap_hypergraph(A):
    A = sorted(A)
    S = set(A)
    E = []
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            c = 2 * A[j] - A[i]
            if c in S and c > A[j]:
                E.append(frozenset((A[i], A[j], c)))
    return E


def is_45(A):
    for B in itertools.combinations(sorted(A), 4):
        if len({abs(a - b) for a, b in itertools.combinations(B, 2)}) < 5:
            return False
    return True
