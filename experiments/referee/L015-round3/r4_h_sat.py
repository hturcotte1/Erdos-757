#!/usr/bin/env python3
"""Referee round 3, L015: h(I_K) for K <= KMAX by solvers that do NOT use the AP
structure or the transfer matrix.  The Sidon constraint is generated directly from
pair-sum collisions of the integer set: for every two distinct pairs (a<=b), (c<=d)
with a+b = c+d, the subset cannot contain all of {a,b,c,d}.
(1) pysat / CaDiCaL 1.5.3 + totalizer cardinality: size >= 7+5K SAT (model re-verified
    Sidon by definition), size >= 8+5K UNSAT.
(2) pysat / Glucose 4 + sequential-counter cardinality: the same two bounds
    (second solver, second encoding).
(3) OR-tools CP-SAT maximise (OPTIMAL) as a cross-check for K <= 3 only (slow beyond).
(4) K <= 1: my own exhaustive DFS over all Sidon subsets (no solver).
Usage: r4_h_sat.py KMAX"""
from itertools import combinations
import sys, time
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from ortools.sat.python import cp_model

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]

def integer_set(K):
    pts = set()
    Nj = {x: x for x in O}
    pts |= {269 ** K * v for v in Nj.values()}
    for j in range(1, K + 1):
        Nj = {x: 101 * 269 ** j + 18 * Nj[x] for x in O}
        pts |= {269 ** (K - j) * v for v in Nj.values()}
    return sorted(pts)

def is_sidon(S):
    seen = set()
    for a, b in combinations(sorted(S), 2):
        if a + b in seen:
            return False
        seen.add(a + b)
    for a in S:
        if 2 * a in seen:
            return False
        seen.add(2 * a)
    return True

def collision_clauses(A):
    """forbidden point sets: unions of two distinct pairs with equal sum (1-based variable ids)."""
    idx = {p: i + 1 for i, p in enumerate(A)}
    sums = {}
    for a, b in combinations(A, 2):
        sums.setdefault(a + b, []).append((a, b))
    for a in A:
        sums.setdefault(2 * a, []).append((a, a))
    forb = set()
    for s, v in sums.items():
        if len(v) >= 2:
            for P, Q in combinations(v, 2):
                forb.add(frozenset(idx[p] for p in P + Q))
    return idx, sorted(forb, key=sorted)

def dfs_max_sidon(A):
    best = [0]
    n = len(A)
    def rec(i, chosen, sums):
        if len(chosen) + (n - i) <= best[0]:
            return
        if i == n:
            best[0] = max(best[0], len(chosen)); return
        p = A[i]
        new = [p + q for q in chosen] + [2 * p]
        if len(set(new)) == len(new) and not (set(new) & sums):
            chosen.append(p)
            rec(i + 1, chosen, sums | set(new))
            chosen.pop()
        rec(i + 1, chosen, sums)
    rec(0, [], frozenset())
    return best[0]

def sat_pair(A, forb, target, solver_name, enc):
    n = len(A)
    out = {}
    for bound in (target, target + 1):
        cnf = [[-v for v in f] for f in forb]
        card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=bound, top_id=n, encoding=enc)
        with Solver(name=solver_name, bootstrap_with=cnf + card.clauses) as s:
            sat = s.solve()
            model = s.get_model() if sat else None
        if sat:
            chosen = [A[v - 1] for v in model if 0 < v <= n]
            out[bound] = ("SAT", len(chosen), len(chosen) >= bound and is_sidon(chosen))
        else:
            out[bound] = ("UNSAT", None, None)
    ok = out[target][0] == "SAT" and out[target][2] and out[target + 1][0] == "UNSAT"
    return ok, out

fails = []
for K in range(0, KMAX + 1):
    A = integer_set(K)
    n = len(A)
    idx, forb = collision_clauses(A)
    sizes = sorted({len(f) for f in forb})
    target = 7 + 5 * K
    t0 = time.time()
    ok1, r1 = sat_pair(A, forb, target, "cadical153", EncType.totalizer)
    t1 = time.time()
    ok2, r2 = sat_pair(A, forb, target, "glucose4", EncType.seqcounter)
    t2 = time.time()
    if K <= 3:
        m = cp_model.CpModel()
        x = [m.NewBoolVar("x%d" % i) for i in range(n)]
        for f in forb:
            m.AddBoolOr([x[v - 1].Not() for v in f])
        m.Maximize(sum(x))
        solver = cp_model.CpSolver()
        solver.parameters.num_workers = 1
        solver.parameters.max_time_in_seconds = 90
        st = solver.Solve(m)
        cp_val = int(round(solver.ObjectiveValue())) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
        cp_sol = [A[i] for i in range(n) if solver.Value(x[i])] if cp_val is not None else []
        cp_ok = (st == cp_model.OPTIMAL) and cp_val == target and is_sidon(cp_sol) and len(cp_sol) == target
        cp_name = solver.StatusName(st)
    else:
        cp_ok, cp_val, cp_name = True, None, "skipped"
    t3 = time.time()
    bf = dfs_max_sidon(A) if K <= 1 else None
    bf_ok = (bf == target) if K <= 1 else True
    line = ("K=%d n=%d forbidden sets=%d (sizes %s) | cadical/totalizer >=%d: %s(size %s, sidon %s), >=%d: %s [%.1fs] | "
            "glucose/seqcounter >=%d: %s(sidon %s), >=%d: %s [%.1fs] | CP-SAT: %s value=%s [%.1fs] | DFS=%s"
            % (K, n, len(forb), sizes, target, r1[target][0], r1[target][1], r1[target][2], target + 1, r1[target + 1][0], t1 - t0,
               target, r2[target][0], r2[target][2], target + 1, r2[target + 1][0], t2 - t1, cp_name, cp_val, t3 - t2, bf))
    print(line, flush=True)
    if not (ok1 and ok2 and cp_ok and bf_ok):
        fails.append(line)
print("ALL h CHECKS OK: h(I_K) = 7+5K for K<=%d" % KMAX if not fails else "FAILURES:\n" + "\n".join(fails))
sys.exit(1 if fails else 0)
