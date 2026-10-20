#!/usr/bin/env python3
"""Referee L015 round 1, script r4: h(S_K) by SAT (pysat, CaDiCaL 1.9.5), a method independent of the
frontier DP of r3.  Forbidden sets come from the Sidon definition (pairs (a<=b) != (c<=d), a+b = c+d) of the
integer set I_K built from scratch; clause NOT(all of f) for each forbidden f; cardinality sum x >= k by a
totalizer encoding.  k = 7+5K must be SAT (the model is re-checked Sidon by definition), k = 8+5K UNSAT.
Usage: python3 -I r4_sat.py K [K ...]
"""
import sys
import time
from fractions import Fraction as F
from itertools import combinations

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
r = F(18, 269)


def IK(K):
    pts = set()
    for x in O:
        v = F(x)
        for j in range(K + 1):
            pts.add(v)
            v = 101 + r * v
    sc = 269 ** K
    out = []
    for v in pts:
        w = v * sc
        assert w.denominator == 1
        out.append(int(w))
    return sorted(out)


def forbidden(I):
    n = len(I)
    bysum = {}
    for i in range(n):
        for k in range(i, n):
            bysum.setdefault(I[i] + I[k], []).append((i, k))
    Fs = set()
    for L in bysum.values():
        for p, q in combinations(L, 2):
            Fs.add(tuple(sorted(set(p) | set(q))))
    return sorted(Fs)


def solve(I, Fs, k):
    n = len(I)
    clauses = [[-(v + 1) for v in f] for f in Fs]
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.totalizer)
    with Solver(name="cadical195", bootstrap_with=clauses + card.clauses) as s:
        res = s.solve()
        model = s.get_model() if res else None
    if res:
        T = [I[v] for v in range(n) if model[v] > 0]
        sm = [a + b for i, a in enumerate(T) for b in T[i:]]
        return True, (len(T) >= k and len(sm) == len(set(sm))), len(T)
    return False, None, None


allok = True
for K in map(int, sys.argv[1:]):
    t0 = time.time()
    I = IK(K)
    Fs = forbidden(I)
    h = 7 + 5 * K
    s1, okm, sz = solve(I, Fs, h)
    t1 = time.time()
    s2, _, _ = solve(I, Fs, h + 1)
    t2 = time.time()
    ok = s1 and okm and not s2
    allok &= ok
    print("%s SAT K=%d n=%d: >=%d %s (model size %s, Sidon by definition: %s; %.1fs), >=%d %s (%.1fs)" %
          ("PASS" if ok else "FAIL", K, len(I), h, "SAT" if s1 else "UNSAT", sz, okm, t1 - t0, h + 1,
           "SAT" if s2 else "UNSAT", t2 - t1), flush=True)
print("SAT SUMMARY:", "ALL OK" if allok else "FAILURE")
