"""Exact (Fraction) tools for self-similar families S_K = O u phi(O) u ... u phi^K(O)."""
import sys, itertools
from fractions import Fraction as F
from collections import defaultdict
sys.path.insert(0, '/home/user/Erdos-757')
from e757 import core

NEG = None

def make_phi(O, a, b, ap, bp):
    """phi(x) = O[ap] + (O[bp]-O[ap])/(O[b]-O[a]) * (x - O[a]); indices into sorted O."""
    r = F(O[bp] - O[ap], O[b] - O[a])
    return (lambda x: O[ap] + r * (F(x) - O[a])), r

def copies(O, phi, K):
    cs = [[F(x) for x in O]]
    for _ in range(K):
        cs.append([phi(x) for x in cs[-1]])
    return cs

def aps_of(A):
    A = sorted(A); S = set(A); out = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            m = (A[i] + A[j]) / 2
            if m in S and m != A[i] and m != A[j]:
                out.add((A[i], m, A[j]))
    return out

def structure_check(O, phi, K, literal=False):
    """Returns dict of exact checks for S_K."""
    cs = copies(O, phi, K)
    S = sorted(set(x for c in cs for x in c))
    n0 = len(O)
    res = {'K': K, 'n': len(S), 'n_expected': n0 + (n0 - 2) * K}
    res['count_ok'] = res['n'] == res['n_expected']
    sums = defaultdict(int)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            sums[S[i] + S[j]] += 1
    res['weak_sidon'] = all(v == 1 for v in sums.values())
    ap_all = aps_of(S)
    ap_cop = set()
    c0 = aps_of([F(x) for x in O])
    for c in cs:
        # image of AP(O) under phi^j: reconstruct via copy lists (same index order)
        pass
    cs_idx = [dict(zip([F(x) for x in O], c)) for c in cs]
    for d in cs_idx:
        for (u, m, w) in c0:
            t = tuple(sorted((d[u], d[m], d[w])))
            ap_cop.add(t)
    res['ap_equal'] = (ap_all == ap_cop)
    res['n_ap'] = len(ap_all)
    pairs = defaultdict(int)
    lin = True
    for t in ap_all:
        for p in itertools.combinations(t, 2):
            pairs[p] += 1
            if pairs[p] > 1: lin = False
    res['linear'] = lin
    res['is_45_fast'] = res['weak_sidon'] and lin
    if literal:
        res['is_45_literal'] = core.is_45_set(S)
    return res

def transfer(O, a, b, ap, bp):
    """exact best[s][s'] (None = infeasible), M, R0, and slope via max-plus iteration."""
    n = len(O)
    Ofr = [F(x) for x in O]
    aps = aps_of(Ofr)
    idx = {x: i for i, x in enumerate(Ofr)}
    apm = [(1 << idx[u]) | (1 << idx[m]) | (1 << idx[w]) for (u, m, w) in aps]
    best = [[None] * 4 for _ in range(4)]
    for mk in range(1 << n):
        if any((mk & t) == t for t in apm): continue
        sa = ((mk >> a) & 1) | (((mk >> b) & 1) << 1)
        sb = ((mk >> ap) & 1) | (((mk >> bp) & 1) << 1)
        sz = bin(mk).count('1')
        if best[sa][sb] is None or sz > best[sa][sb]: best[sa][sb] = sz
    pc = [0, 1, 1, 2]
    M = [[None if best[i][j] is None else best[i][j] - pc[i] for j in range(4)] for i in range(4)]
    R0 = [max([best[i][j] for i in range(4) if best[i][j] is not None], default=None) for j in range(4)]
    return best, M, R0

def maxplus_iter(M, R0, steps):
    R = list(R0); hist = [list(R)]
    for _ in range(steps):
        T = [None] * 4
        for j in range(4):
            c = [R[i] + M[i][j] for i in range(4) if R[i] is not None and M[i][j] is not None]
            T[j] = max(c) if c else None
        R = T; hist.append(list(R))
    return hist

def slope(M, R0):
    h = maxplus_iter(M, R0, 240)
    mx = lambda R: max(x for x in R if x is not None)
    return F(mx(h[240]) - mx(h[120]), 120), h

def hseq(M, R0, Kmax):
    h = maxplus_iter(M, R0, Kmax)
    return [max(x for x in R if x is not None) for R in h]

def alpha_exact(points, aps, tl=60):
    """max 3-AP-free subset via CP-SAT (OPTIMAL asserted)."""
    from ortools.sat.python import cp_model
    m = cp_model.CpModel(); idx = {p: i for i, p in enumerate(points)}
    x = [m.NewBoolVar(f"x{i}") for i in range(len(points))]
    for (u, mm, w) in aps: m.Add(x[idx[u]] + x[idx[mm]] + x[idx[w]] <= 2)
    m.Maximize(sum(x))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 1
    st = sv.Solve(m); assert st == cp_model.OPTIMAL, st
    return int(round(sv.ObjectiveValue()))
