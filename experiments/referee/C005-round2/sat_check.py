#!/usr/bin/env python3
"""Second and third independent exact methods for h(A):
  (a) SAT (python-sat, CaDiCaL): conflict clauses straight from the Sidon DEFINITION (two distinct
      pairs with equal difference cannot both lie in S) + cardinality 'at least k'.
      k = h  -> expect SAT, model re-verified as Sidon by definition;  k = h+1 -> expect UNSAT.
  (b) CP-SAT (ortools), 1 worker, maximise |S| subject to the same conflict constraints; accept
      only status OPTIMAL.
  (c) scipy.optimize.milp (HiGHS) with mip_rel_gap = 0 (optional, may be slow).
No e757, no judge.  Usage: python3 sat_check.py claim.json h [time_limit_s] [methods]
"""
import itertools
import json
import sys
import time
from fractions import Fraction
from math import lcm


def load(path):
    raw = json.load(open(path))["set"]
    vals = sorted(Fraction(str(x)) for x in raw)
    assert len(set(vals)) == len(vals)
    den = 1
    for v in vals:
        den = lcm(den, v.denominator)
    return [int(v * den) for v in vals]


def conflicts(A):
    n = len(A)
    by_diff = {}
    for i, j in itertools.combinations(range(n), 2):
        by_diff.setdefault(A[j] - A[i], []).append((i, j))
    out = set()
    for pairs in by_diff.values():
        for p, q in itertools.combinations(pairs, 2):
            out.add(frozenset(p) | frozenset(q))
    return [tuple(sorted(c)) for c in out]


def is_sidon(S):
    S = sorted(S)
    d = [y - x for x, y in itertools.combinations(S, 2)]
    return len(d) == len(set(d))


def sat_method(A, cons, k, solver_name="cadical153"):
    from pysat.card import CardEnc, EncType
    from pysat.formula import CNF
    from pysat.solvers import Solver
    n = len(A)
    cnf = CNF()
    for c in cons:
        cnf.append([-(v + 1) for v in c])
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.totalizer)
    cnf.extend(card.clauses)
    t0 = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as s:
        res = s.solve()
        model = s.get_model() if res else None
    dt = time.time() - t0
    chosen = None
    if res:
        chosen = [v for v in range(n) if model[v] > 0]
        assert len(chosen) >= k
        assert is_sidon([A[v] for v in chosen]), "SAT model is not Sidon!"
    return res, chosen, dt


def cpsat_method(A, cons, time_limit):
    from ortools.sat.python import cp_model
    n = len(A)
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(n)]
    for c in cons:
        m.Add(sum(x[v] for v in c) <= len(c) - 1)
    m.Maximize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 1
    s.parameters.max_time_in_seconds = time_limit
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = s.StatusName(st)
    val = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [i for i in range(n) if s.Value(x[i])]
        assert is_sidon([A[i] for i in chosen])
        val = len(chosen)
    return name, val, s.BestObjectiveBound(), dt


def milp_method(A, cons, time_limit):
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    n = len(A)
    M = lil_matrix((len(cons), n))
    ub = np.zeros(len(cons))
    for r, c in enumerate(cons):
        for v in c:
            M[r, v] = 1
        ub[r] = len(c) - 1
    t0 = time.time()
    res = milp(c=-np.ones(n), constraints=LinearConstraint(M.tocsr(), -np.inf, ub),
               integrality=np.ones(n), bounds=Bounds(0, 1),
               options={"time_limit": time_limit, "mip_rel_gap": 0.0, "disp": False})
    dt = time.time() - t0
    val = None
    if res.x is not None:
        chosen = [i for i in range(n) if res.x[i] > 0.5]
        assert is_sidon([A[i] for i in chosen])
        val = len(chosen)
    return res.status, res.message, val, getattr(res, "mip_dual_bound", None), dt


def main():
    A = load(sys.argv[1])
    h = int(sys.argv[2])
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600.0
    methods = sys.argv[4] if len(sys.argv) > 4 else "sat,cpsat,milp"
    n = len(A)
    cons = conflicts(A)
    print(f"n = {n}; conflicts (from the Sidon definition) = {len(cons)}; sizes {sorted(set(len(c) for c in cons))}")
    if "sat" in methods.split(","):
        res, chosen, dt = sat_method(A, cons, h)
        print(f"SAT  atleast {h}: {'SAT' if res else 'UNSAT'} in {dt:.1f}s" + (f"; model size {len(chosen)} verified Sidon by definition" if res else ""))
        sys.stdout.flush()
        res2, chosen2, dt2 = sat_method(A, cons, h + 1)
        print(f"SAT  atleast {h+1}: {'SAT' if res2 else 'UNSAT'} in {dt2:.1f}s" + (f"; model size {len(chosen2)} (!!)" if res2 else ""))
        sys.stdout.flush()
    if "cpsat" in methods.split(","):
        name, val, bound, dt = cpsat_method(A, cons, tl)
        print(f"CP-SAT (1 worker, limit {tl}s): status {name}, objective {val}, bound {bound}, {dt:.1f}s")
        sys.stdout.flush()
    if "milp" in methods.split(","):
        st, msg, val, bnd, dt = milp_method(A, cons, tl)
        print(f"MILP (HiGHS, gap 0, limit {tl}s): status {st} ({msg}), objective {val}, dual bound {bnd}, {dt:.1f}s")


if __name__ == "__main__":
    main()
