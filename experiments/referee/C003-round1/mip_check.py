#!/usr/bin/env python3
"""MIP route for h(C003): HiGHS (scipy.optimize.milp) and SCIP (OR-tools pywraplp).

Constraints come straight from the Sidon definition: for every relation a+b = c+d between
distinct multisets of A, the union {a,b,c,d} may not be fully chosen
(sum_{v in union} x_v <= |union| - 1).  Does not import e757 or judge.
Floating-point solvers: this is a numerical cross-check, the exact route is verify_c003.py.

usage: mip_check.py CLAIM.json SOLVER(highs|scip) MODE(max|ge38) TIME_LIMIT
"""
import itertools
import json
import resource
import sys
import time
from collections import defaultdict

resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 ** 3, 4 * 1024 ** 3))


def load(path):
    claim = json.load(open(path), parse_float=lambda s: (_ for _ in ()).throw(ValueError(s)))
    A = sorted(int(x) for x in claim["set"])
    assert len(set(A)) == len(A)
    return A


def forbidden(A):
    n = len(A)
    by_sum = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            by_sum[A[i] + A[j]].append((i, j))
    forb = set()
    for lst in by_sum.values():
        for p, q in itertools.combinations(lst, 2):
            forb.add(tuple(sorted(set(p) | set(q))))
    return sorted(forb)


def run_highs(n, F, mode, tl):
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    rows = np.zeros((len(F), n))
    for k, e in enumerate(F):
        for v in e:
            rows[k, v] = 1
    cons = [LinearConstraint(rows, -np.inf, np.array([len(e) - 1 for e in F], dtype=float))]
    if mode == "ge38":
        cons.append(LinearConstraint(np.ones((1, n)), 38, np.inf))
    res = milp(-np.ones(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(0, 1),
               options={"time_limit": tl, "disp": False, "mip_rel_gap": 0.0})
    out = {"status": int(res.status), "message": res.message}
    if res.x is not None:
        out["obj"] = -res.fun
        out["x"] = [int(round(v)) for v in res.x]
    out["dual_bound"] = getattr(res, "mip_dual_bound", None)
    return out


def run_scip(n, F, mode, tl):
    from ortools.linear_solver import pywraplp
    s = pywraplp.Solver.CreateSolver("SCIP")
    if s is None:
        return {"status": "SCIP unavailable"}
    x = [s.BoolVar(f"x{i}") for i in range(n)]
    for e in F:
        s.Add(sum(x[v] for v in e) <= len(e) - 1)
    if mode == "ge38":
        s.Add(sum(x) >= 38)
    s.Maximize(sum(x))
    s.SetTimeLimit(int(tl * 1000))
    st = s.Solve()
    names = {pywraplp.Solver.OPTIMAL: "OPTIMAL", pywraplp.Solver.FEASIBLE: "FEASIBLE",
             pywraplp.Solver.INFEASIBLE: "INFEASIBLE", pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
             pywraplp.Solver.ABNORMAL: "ABNORMAL"}
    out = {"status": names.get(st, st)}
    if st in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        out["obj"] = s.Objective().Value()
        out["bound"] = s.Objective().BestBound()
        out["x"] = [int(round(v.solution_value())) for v in x]
    return out


def main():
    path, solver, mode, tl = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    A = load(path)
    n = len(A)
    F = forbidden(A)
    print(f"n={n} forbidden unions={len(F)} sizes={sorted(set(len(e) for e in F))} solver={solver} mode={mode}",
          flush=True)
    t = time.time()
    out = run_highs(n, F, mode, tl) if solver == "highs" else run_scip(n, F, mode, tl)
    out["seconds"] = round(time.time() - t, 1)
    if "x" in out:
        T = [A[i] for i in range(n) if out["x"][i]]
        sums = [T[i] + T[j] for i in range(len(T)) for j in range(i, len(T))]
        out["solution_size"] = len(T)
        out["solution_is_sidon"] = len(sums) == len(set(sums))
        del out["x"]
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
