"""Independent falsifier library for L015 (own code; nothing imported from the repo)."""
from fractions import Fraction
from itertools import combinations
from math import lcm
import numpy as np

O0 = [0,49,75,83,98,101,117,119,121,159,269]
P61 = (1 << 61) - 1

def build(O, c=101, a=18, K=3):
    """phi(x)=c+a*x/M, M=max(O).  Returns (copies as lists of Fractions aligned to O, scaled int copies, scale)."""
    M = max(O)
    copies = [[Fraction(x) for x in O]]
    for j in range(K):
        copies.append([Fraction(c) + Fraction(a, M) * x for x in copies[-1]])
    den = 1
    for cp in copies:
        for x in cp:
            den = lcm(den, x.denominator)
    ic = [[int(x * den) for x in cp] for cp in copies]
    for cp, icp in zip(copies, ic):
        assert all(Fraction(i, den) == x for i, x in zip(icp, cp))
    return copies, ic, den

def points(ic):
    return sorted(set(x for cp in ic for x in cp))

def relation_groups(pts):
    """group pairs (i<=j, indices into sorted pts) by exact sum; hash via mod 2^61-1 then exact verify.
    returns (groups: list of lists of pairs with equal exact sum, size>=2 ; n_false_hash_groups)"""
    n = len(pts)
    r = np.array([p % P61 for p in pts], dtype=np.uint64)
    I, J = np.triu_indices(n)
    s = (r[I] + r[J]) % np.uint64(P61)
    order = np.argsort(s, kind='stable')
    ss = s[order]
    brk = np.flatnonzero(ss[1:] != ss[:-1]) + 1
    starts = np.concatenate(([0], brk)); ends = np.concatenate((brk, [len(ss)]))
    big = np.flatnonzero(ends - starts >= 2)
    groups = []; false = 0
    for g in big:
        idx = order[starts[g]:ends[g]]
        d = {}
        for t in idx:
            i, j = int(I[t]), int(J[t])
            d.setdefault(pts[i] + pts[j], []).append((i, j))
        if len(d) > 1: false += 1
        for v in d.values():
            if len(v) >= 2: groups.append(v)
    return groups, false

def relation_pointsets(groups):
    """each pair of distinct pairs with equal sum gives a relation; return set of frozenset(point indices)."""
    out = set()
    for g in groups:
        for (p, q) in combinations(g, 2):
            out.add(frozenset(p + q))
    return out

def sums_distinct_subset(vals):
    """Sidon by definition (all x<=y sums distinct)"""
    seen = set()
    v = sorted(vals)
    for i in range(len(v)):
        for j in range(i, len(v)):
            s = v[i] + v[j]
            if s in seen: return False
            seen.add(s)
    return True

def min_distinct_diffs(pts):
    """exhaustive over all 4-subsets: minimum number of distinct positive differences"""
    best = 6
    for a, b, c, d in combinations(pts, 4):
        k = len({b-a, c-a, d-a, c-b, d-b, d-c})
        if k < best:
            best = k
            if best < 5: return best
    return best

def apsO(O):
    """E(O) computed by own triple enumeration"""
    S = set(O); E = []
    for a, b, c in combinations(sorted(O), 3):
        if a + c == 2 * b: E.append((a, b, c))
    return E

# ---------- exact independence number, two independent solvers ----------
def alpha_cpsat(n, ptsets, tl=120):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(n)]
    for P in ptsets:
        m.Add(sum(x[i] for i in P) <= len(P) - 1)
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = tl
    st = s.Solve(m)
    return s.StatusName(st), int(round(s.ObjectiveValue())), int(round(s.BestObjectiveBound())), [i for i in range(n) if s.Value(x[i])]

def sat_atleast(n, ptsets, k):
    from pysat.solvers import Cadical153
    from pysat.card import CardEnc, EncType
    cl = [[-(i+1) for i in P] for P in ptsets]
    enc = CardEnc.atleast(lits=list(range(1, n+1)), bound=k, top_id=n, encoding=EncType.totalizer)
    s = Cadical153(bootstrap_with=cl + enc.clauses)
    r = s.solve(); s.delete()
    return r

# ---------- transfer matrix, own implementation ----------
def transfer(O, c=101, a=18):
    """anchor = (min,max) states; exit = (phi(min),phi(max)) must lie in O. returns (best, M, R0) or None"""
    O = sorted(O); M = max(O); lo = min(O)
    e0 = Fraction(c) + Fraction(a, M) * lo; e1 = Fraction(c) + Fraction(a, M) * M
    if e0.denominator != 1 or e1.denominator != 1 or int(e0) not in O or int(e1) not in O: return None
    e0, e1 = int(e0), int(e1)
    n = len(O)
    edges = apsO(O)
    em = []
    for e in edges:
        mk = 0
        for v in e: mk |= 1 << O.index(v)
        em.append(mk)
    NEG = -10**9
    best = [[NEG]*4 for _ in range(4)]
    st = lambda U, p, q: (1 if (U >> O.index(p)) & 1 else 0) + 2 * (1 if (U >> O.index(q)) & 1 else 0)
    for U in range(1 << n):
        if any((U & m) == m for m in em): continue
        s = st(U, lo, M); t = st(U, e0, e1)
        best[s][t] = max(best[s][t], bin(U).count('1'))
    pc = lambda s: (s & 1) + (s >> 1)
    Mx = [[best[s][t] - pc(s) if best[s][t] > NEG//2 else NEG for t in range(4)] for s in range(4)]
    R0 = [max(best[s][t] for s in range(4)) for t in range(4)]
    return best, Mx, R0

def maxplus(R, Mx):
    return [max(R[s] + Mx[s][t] for s in range(4)) for t in range(4)]

def predict_h(O, K, c=101, a=18):
    tr = transfer(O, c, a)
    if tr is None: return None
    best, Mx, R0 = tr
    R = R0
    for _ in range(K): R = maxplus(R, Mx)
    return max(R)

# ---------- generic exact frontier DP (order only affects speed, not correctness) ----------
def alpha_frontier_dp(n, ptsets, order=None, return_width=False):
    """max |T| with no relation point-set contained in T; exact for any hypergraph and any vertex order."""
    from collections import deque
    adj = [set() for _ in range(n)]
    for P in ptsets:
        for u in P:
            adj[u] |= set(P)
    if order is None:
        seen = set(); order = []
        for s in range(n):
            if s in seen: continue
            dq = deque([s]); seen.add(s)
            while dq:
                u = dq.popleft(); order.append(u)
                for w in sorted(adj[u]):
                    if w not in seen: seen.add(w); dq.append(w)
    pos = {v: i for i, v in enumerate(order)}
    edges_at = [[] for _ in range(n)]
    lastpos = [pos[v] for v in range(n)]
    for P in ptsets:
        L = max(pos[v] for v in P)
        edges_at[L].append(tuple(P))
        for v in P: lastpos[v] = max(lastpos[v], L)
    states = {frozenset(): 0}; width = 0
    for i, v in enumerate(order):
        new = {}
        for S, val in states.items():
            for take in (0, 1):
                if take:
                    S2 = S | {v}
                    if any(all(u in S2 for u in P) for P in edges_at[i]): continue
                else:
                    S2 = S
                S3 = frozenset(u for u in S2 if lastpos[u] > i)
                nv = val + take
                if new.get(S3, -1) < nv: new[S3] = nv
        states = new; width = max(width, len(states))
    res = max(states.values())
    return (res, width) if return_width else res
