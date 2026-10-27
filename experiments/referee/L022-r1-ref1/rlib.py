# Referee #1 (round 1) of L022: independent helper library.
# Does NOT import e757, judge/, or any experiments/prover code.
# Exact arithmetic only (int / Fraction).
from fractions import Fraction
from itertools import combinations, product
import random

# ---------------------------------------------------------------- hypergraphs
def norm_edges(edges):
    return sorted(tuple(sorted(e)) for e in edges)

def vertices_of(edges, extra=()):
    s = set(extra)
    for e in edges:
        s.update(e)
    return sorted(s)

def is_linear(edges):
    E = [frozenset(e) for e in edges]
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            if len(E[i] & E[j]) > 1:
                return False
    return True

def degrees(V, edges):
    d = {v: 0 for v in V}
    for e in edges:
        for x in e:
            d[x] += 1
    return d

def components(V, edges):
    par = {v: v for v in V}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for e in edges:
        a = f(e[0])
        for x in e[1:]:
            b = f(x)
            if a != b:
                par[b] = a
    comp = {}
    for v in V:
        comp.setdefault(f(v), []).append(v)
    return sorted(comp.values(), key=lambda c: min(c))

def induced(edges, Y):
    Y = set(Y)
    return [e for e in edges if set(e) <= Y]

def tau(edges):
    """exact transversal number by branch and bound"""
    edges = [tuple(e) for e in edges]
    best = [len(edges)]
    def rec(rem, k):
        if k >= best[0]:
            return
        if not rem:
            best[0] = k
            return
        # lower bound: greedy disjoint edges
        used = set(); lb = 0
        for e in rem:
            if not (used & set(e)):
                used |= set(e); lb += 1
        if k + lb >= best[0]:
            return
        # branch on edge with highest degree vertices first
        e = rem[0]
        for x in e:
            rec([f for f in rem if x not in f], k + 1)
    rec(edges, 0)
    return best[0]

def min_transversals(edges):
    """all minimum transversals (as frozensets)"""
    t = tau(edges)
    out = set()
    edges = [tuple(e) for e in edges]
    def rec(rem, chosen):
        if len(chosen) > t:
            return
        if not rem:
            if len(chosen) == t:
                out.add(frozenset(chosen))
            return
        if len(chosen) == t:
            return
        e = rem[0]
        for x in e:
            rec([f for f in rem if x not in f], chosen | {x})
    rec(edges, frozenset())
    return t, out

def slack(n, edges, t=None):
    if t is None:
        t = tau(edges)
    return 3 * n + 2 * len(edges) - 11 * t

def is_F7_free(edges):
    # F7 = centre c with three edges, and two more edges each taking one vertex of each pair, disjoint
    E = [frozenset(e) for e in edges]
    Eset = set(E)
    V = vertices_of(edges)
    inc = {v: [e for e in E if v in e] for v in V}
    for c in V:
        if len(inc[c]) < 3:
            continue
        for t3 in combinations(inc[c], 3):
            pairs = [tuple(e - {c}) for e in t3]
            for choice in product((0, 1), repeat=3):
                g = frozenset(pairs[i][choice[i]] for i in range(3))
                h = frozenset(pairs[i][1 - choice[i]] for i in range(3))
                if g in Eset and h in Eset:
                    return False
    return True

def p3_ok(V, edges):
    # e(S) <= |S|-2 for all S with |S|>=2 ; only need connected-ish check but do brute force for small n
    n = len(V)
    E = [frozenset(e) for e in edges]
    idx = {v: i for i, v in enumerate(V)}
    masks = [sum(1 << idx[x] for x in e) for e in E]
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2:
            continue
        cnt = sum(1 for mk in masks if mk & S == mk)
        if cnt > k - 2:
            return False
    return True

# ---------------------------------------------------------------- exact linear algebra
def nullspace(rows, n):
    """rows: list of dict {col: Fraction}; returns basis of nullspace as list of length-n vectors (Fractions)"""
    M = [[Fraction(r.get(j, 0)) for j in range(n)] for r in rows]
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i; break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fcol in free:
        v = [Fraction(0)] * n
        v[fcol] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fcol]
        basis.append(v)
    return basis, len(piv)

def rank(rows, n):
    return nullspace(rows, n)[1]

# ---------------------------------------------------------------- sets of reals
def is_45_bruteforce(xs):
    xs = list(xs)
    if len(set(xs)) != len(xs):
        return False
    for B in combinations(xs, 4):
        d = set(abs(a - b) for a, b in combinations(B, 2))
        if len(d) < 5:
            return False
    return True

def ap_triples(xs):
    """list of (i, mid, j) index triples of 3-APs of the integer list xs"""
    pos = {x: i for i, x in enumerate(xs)}
    out = []
    n = len(xs)
    for i in range(n):
        for j in range(i + 1, n):
            s = xs[i] + xs[j]
            if s % 2:
                continue
            m = s // 2
            if m in pos and pos[m] not in (i, j):
                out.append((i, pos[m], j))
    return out

def ap_triples_frac(xs):
    pos = {Fraction(x): i for i, x in enumerate(xs)}
    out = []
    n = len(xs)
    for i in range(n):
        for j in range(i + 1, n):
            m = (Fraction(xs[i]) + Fraction(xs[j])) / 2
            if m in pos:
                out.append((i, pos[m], j))
    return out

def ap_forms_rank(xs):
    aps = ap_triples_frac(xs)
    rows = []
    for (a, b, c) in aps:
        rows.append({a: 1, c: 1, b: -2} if a != c else {})
    return len(aps), rank(rows, len(xs))

# ---------------------------------------------------------------- realizability
def labelings(edges):
    for choice in product(range(3), repeat=len(edges)):
        lab = []
        for e, k in zip(edges, choice):
            e = tuple(e)
            mid = e[k]
            others = [x for x in e if x != mid]
            lab.append((others[0], mid, others[1]))
        yield lab

def analyse_labeling(n, lab):
    """n vertices 0..n-1, lab list of (a,mid,c). Returns (status, basis, forced_aps)
    status in {'bad','ok'}; forced_aps = set of frozenset triples with forced midpoint"""
    rows = [{a: 1, c: 1, b: -2} for (a, b, c) in lab]
    # merge rows where a==c impossible
    basis, rk = nullspace(rows, n)
    d = len(basis)
    R = [tuple(basis[k][i] for k in range(d)) for i in range(n)]  # row i = coefficients of X_i
    # equal coordinates
    if len(set(R)) < n:
        return 'bad-equal', basis, None
    # parallelograms / pair-sum coincidences
    sums = {}
    for i in range(n):
        for j in range(i + 1, n):
            s = tuple(a + b for a, b in zip(R[i], R[j]))
            if s in sums:
                return 'bad-parallelogram', basis, None
            sums[s] = (i, j)
    # forced APs: R_i + R_k == 2 R_j
    twice = {tuple(2 * a for a in R[j]): j for j in range(n)}
    forced = []
    for (i, k), s in [((v[0], v[1]), key) for key, v in sums.items()]:
        if s in twice:
            j = twice[s]
            if j != i and j != k:
                forced.append((i, j, k))
    F = [frozenset(t) for t in forced]
    for x in range(len(F)):
        for y in range(x + 1, len(F)):
            if len(F[x] & F[y]) > 1:
                return 'bad-nonlinear', basis, forced
    return 'ok', basis, forced

def realize(n, edges, want_exact=True, rng=None, tries=50, all_labelings=False):
    """returns dict with keys realizable (bool), exact (bool), labeling, point (ints)"""
    edges = [tuple(e) for e in edges]
    Eset = set(frozenset(e) for e in edges)
    rng = rng or random.Random(12345)
    found_sub = None
    nlab = 0; nok = 0
    for lab in labelings(edges):
        mids = [b for (_, b, _) in lab]
        if len(set(mids)) < len(mids):
            continue
        nlab += 1
        st, basis, forced = analyse_labeling(n, lab)
        if st != 'ok':
            continue
        nok += 1
        Fset = set(frozenset(t) for t in forced)
        assert Eset <= Fset
        exact = (Fset == Eset)
        res = {'realizable': True, 'exact': exact, 'labeling': lab, 'forced': sorted(tuple(sorted(t)) for t in Fset)}
        # explicit point
        pt = explicit_point(n, basis, Fset, rng, tries)
        res['point'] = pt
        if exact or not want_exact:
            if not all_labelings:
                res['n_injective_labelings_scanned'] = nlab
                return res
        if found_sub is None:
            found_sub = res
    if found_sub is not None:
        found_sub['n_injective_labelings_scanned'] = nlab
        found_sub['n_ok'] = nok
        return found_sub
    return {'realizable': False, 'n_injective_labelings_scanned': nlab}

def explicit_point(n, basis, Fset, rng, tries):
    from math import lcm
    d = len(basis)
    for _ in range(tries):
        t = [rng.randint(-10**6, 10**6) for _ in range(d)]
        x = [sum(basis[k][i] * t[k] for k in range(d)) for i in range(n)]
        L = 1
        for v in x:
            L = lcm(L, v.denominator)
        xi = [int(v * L) for v in x]
        if len(set(xi)) < n:
            continue
        aps = ap_triples(xi)
        A = set(frozenset(t) for t in aps)
        if A == Fset and is_45_bruteforce(xi):
            return xi
    return None
