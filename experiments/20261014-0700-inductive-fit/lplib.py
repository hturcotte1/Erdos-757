"""Exact small LP for the inequality  tau <= b*R + c*e2 + d*e1   (a = 1).
Constraint rows are (tau,R,e2,e1).  min_var(...) returns the exact optimum (Fraction) of one variable,
others either fixed (Fraction) or free in [0, cap].  Vertex enumeration on the scipy-tight set, exact in Fraction."""
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
NAMES = ('b', 'c', 'd')

def pareto(tuples):
    """keep tuples not dominated (a tuple t is implied by t' if tau'>=tau, R'<=R, e2'<=e2, e1'<=e1, all coefficients >= 0)."""
    T = sorted(set(tuples), key=lambda t: (t[1] + t[2] + t[3], -t[0]))
    keep = []
    for t in T:
        dom = False
        for u in keep:
            if u[0] >= t[0] and u[1] <= t[1] and u[2] <= t[2] and u[3] <= t[3]:
                dom = True; break
        if not dom: keep.append(t)
    return keep

def _solve3(rows):
    """solve 3x3 exact; rows = list of (coeffs(3), rhs). returns tuple or None"""
    M = [[F(x) for x in r[0]] + [F(r[1])] for r in rows]
    n = len(M)
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i] != 0), None)
        if p is None: return None
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]
                M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return tuple(M[i][n] / M[i][i] for i in range(n))

def min_var(tuples, target, fixed=None, cap=F(2)):
    """tuples: iterable of (tau,R,e2,e1). target in 'b','c','d'. fixed: dict name->Fraction. Returns (value Fraction, argmin dict) or (None,None) if infeasible."""
    fixed = fixed or {}
    free = [v for v in NAMES if v not in fixed]
    assert target in free
    k = len(free)
    cons = []   # (coef over free vars, rhs) meaning coef.x >= rhs
    for tau, R, e2, e1 in pareto(tuples):
        co = {'b': R, 'c': e2, 'd': e1}
        rhs = F(tau) - sum(F(co[v]) * fixed[v] for v in fixed)
        cons.append(([F(co[v]) for v in free], rhs))
    bounds = []
    for i in range(k):
        e = [F(0)] * k; e[i] = F(1); bounds.append((e, F(0))); bounds.append(([-x for x in e], -F(cap)))
    allc = cons + bounds
    # infeasible constant rows
    for co, rhs in cons:
        if all(x == 0 for x in co) and rhs > 0: return None, None
    A = np.array([[-float(x) for x in co] for co, _ in allc]); bb = np.array([-float(r) for _, r in allc])
    obj = np.zeros(k); obj[free.index(target)] = 1
    r = linprog(obj, A_ub=A, b_ub=bb, bounds=[(None, None)] * k, method='highs')
    if r.status != 0: return None, None
    x = r.x; tight = [i for i in range(len(allc)) if abs(float(sum(allc[i][0][j] * 0 for j in range(k))) + sum(float(allc[i][0][j]) * x[j] for j in range(k)) - float(allc[i][1])) < 1e-7]
    best = None
    def feas(p):
        return all(sum(co[j] * p[j] for j in range(k)) >= rhs for co, rhs in allc)
    for sub in combinations(tight, k):
        if k == 1: p = (allc[sub[0]][1] / allc[sub[0]][0][0],) if allc[sub[0]][0][0] != 0 else None
        elif k == 2:
            (a1, a2), r1 = allc[sub[0]]; (b1, b2), r2 = allc[sub[1]]
            det = a1 * b2 - a2 * b1
            p = None if det == 0 else ((r1 * b2 - a2 * r2) / det, (a1 * r2 - r1 * b1) / det)
        else:
            p = _solve3([allc[i] for i in sub])
        if p is None or not feas(p): continue
        v = p[free.index(target)]
        if best is None or v < best[0]: best = (v, p)
    assert best is not None and abs(float(best[0]) - r.fun) < 1e-6, (best, r.fun)
    out = dict(zip(free, best[1])); out.update(fixed)
    return best[0], out

def check(tuples, b, c, d):
    """exact: returns list of violated tuples"""
    return [t for t in set(tuples) if F(t[0]) > b * t[1] + c * t[2] + d * t[3]]

def min_c_given(tuples, b, d):
    """exact minimal c >= 0 with feasibility at (b,c,d), or None."""
    need = F(0)
    for tau, R, e2, e1 in set(tuples):
        r = F(tau) - b * R - d * e1
        if r <= 0: continue
        if e2 == 0: return None
        need = max(need, r / e2)
    return need
