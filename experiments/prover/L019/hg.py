"""L019 helper: exact transversal routines on small 3-graphs (bitmask), class-C tests.
Edges are tuples of ints in range(n). Everything exact (ints)."""
import itertools, sys, os
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness')
import pyverify as PV

def read_cell(path, K=None):
    out = []
    with open(path) as fh:
        for line in fh:
            a = list(map(int, line.split()))
            if not a: continue
            n, m, t = a[:3]
            E = [tuple(a[3+3*i:6+3*i]) for i in range(m)]
            out.append((n, m, t, E))
            if K is not None and len(out) >= K: break
    return out

def emask(E):
    return [sum(1 << x for x in e) for e in E]

def all_min_transversals(n, E, t=None):
    """all transversals of size tau (bitmasks); returns (tau, list)."""
    M = emask(E)
    if t is None:
        t = 0
        while not _cover_le(M, t): t += 1
    out = set()
    def rec(rem, chosen, k):
        if not rem:
            out.add(chosen); return
        if k == 0: return
        e = rem[0]
        for x in range(n):
            if e >> x & 1:
                b = 1 << x
                rec([f for f in rem if not f & b], chosen | b, k - 1)
    rec(M, 0, t)
    # keep only size exactly t (all are size<=t; if tau==t they are all size t)
    res = [T for T in out if bin(T).count('1') == t]
    return t, res

def _cover_le(M, k):
    if not M: return True
    if k == 0: return False
    e = M[0]
    x = 0
    while e:
        if e & 1:
            b = 1 << x
            if _cover_le([f for f in M if not f & b], k - 1): return True
        e >>= 1; x += 1
    return False

def tau(n, E):
    M = emask(E); t = 0
    while not _cover_le(M, t): t += 1
    return t

def slack(n, E):
    return 3*n + 2*len(E) - 11*tau(n, E)

def degrees(n, E):
    d = [0]*n
    for e in E:
        for x in e: d[x] += 1
    return d

def in_C(E):
    return PV.in_C(E)

def has_f7(E):
    return PV.has_f7(E)

def linear(E):
    return PV.linear(E)

def p3(E):
    return PV.p3(E)

def f7_copies(E):
    S = set(frozenset(e) for e in E); at = {}
    for e in E:
        for x in e: at.setdefault(x, []).append(e)
    res = set()
    for c, es in at.items():
        for e1, e2, e3 in itertools.combinations(es, 3):
            p = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]; a1, b1 = p[0]
            for x2, y2 in (p[1], p[1][::-1]):
                for x3, y3 in (p[2], p[2][::-1]):
                    if len({c, a1, b1, x2, y2, x3, y3}) == 7 and frozenset((a1, x2, x3)) in S and frozenset((b1, y2, y3)) in S:
                        res.add(frozenset([frozenset(e1), frozenset(e2), frozenset(e3), frozenset((a1, x2, x3)), frozenset((b1, y2, y3))]))
    return res

def p3_violations(E, V):
    """all minimal-size sets S (|S|>=2) with e(S) >= |S|-1 (brute force; small n only)."""
    V = sorted(V); bad = []
    for k in range(2, len(V)+1):
        for S in itertools.combinations(V, k):
            Ss = set(S); e = sum(1 for g in E if set(g) <= Ss)
            if e >= k - 1: bad.append((k, S, e))
        if bad: return bad
    return bad

def tight_set_exists(n, E, x, u, w):
    """smallest |S| of a set S with u,w in S, x not in S, |S| >= 3 and e(S) = |S|-2 (brute force), or None.
    (Lemma 5.3 of L019: the fold (H-x)/(u~w) violates (P3) iff such S exists, for H in C.)"""
    V = [y for y in range(n) if y not in (x, u, w)]
    for k in range(1, len(V)+1):
        for X in itertools.combinations(V, k):
            S = set(X) | {u, w}
            if sum(1 for e in E if set(e) <= S) == len(S) - 2: return len(S)
    return None
