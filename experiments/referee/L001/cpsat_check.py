"""Referee L001: h via CP-SAT on the equal-difference conflict structure (third method)."""
import json, sys, time
from fractions import Fraction as Fr
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001')
from rcore import A_BASE, to_int

def h_cpsat(S):
    T, _ = to_int(S)
    n = len(T)
    byd = {}
    for i, j in combinations(range(n), 2):
        byd.setdefault(abs(T[i] - T[j]), []).append((i, j))
    m = cp_model.CpModel()
    z = [m.NewBoolVar(f'z{i}') for i in range(n)]
    ncons = 0
    for d, prs in byd.items():
        for p, q in combinations(prs, 2):
            U = sorted(set(p) | set(q))
            m.Add(sum(z[u] for u in U) <= len(U) - 1)
            ncons += 1
    m.Maximize(sum(z))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    st = s.Solve(m)
    assert st == cp_model.OPTIMAL
    return int(round(s.ObjectiveValue())), ncons

t0 = time.time()
A = [Fr(a) for a in A_BASE]
print('A:', h_cpsat(A))
D = json.load(open('/home/user/Erdos-757/experiments/referee/L001/t1_out.json'))
hx = {}
for xs in D['P_ok']:
    hx.setdefault(h_cpsat(A + [Fr(xs)])[0], []).append(xs)
print('A u {x}, x in P_ok:', {k: len(v) for k, v in hx.items()})
hd = {}
for xs, ys, h, W in D['good']:
    hc, nc = h_cpsat(A + [Fr(xs), Fr(ys)])
    hd[(h, hc)] = hd.get((h, hc), 0) + 1
print('T1b (4,5) pairs (h_dfs, h_cpsat) counts:', hd, 'time', round(time.time() - t0, 1))
