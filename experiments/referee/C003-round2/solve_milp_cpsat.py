#!/usr/bin/env python3
"""Third family of methods: HiGHS MILP (scipy.optimize.milp) and OR-tools CP-SAT, each with a time limit.
Model: maximize sum x_v, x binary, sum_{v in c} x_v <= |c|-1 for every minimal conflict c (from the definition).
Usage: solve_milp_cpsat.py milp|cpsat <time_limit_s>"""
import json
import sys
import time
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *

which, tl = sys.argv[1], float(sys.argv[2])
A, raw = load_claim_set()
n = len(A)
conf = conflicts_from_definition(A)
res = {"method": which, "time_limit_s": tl}
t = time.time()
if which == "milp":
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    Amat = np.zeros((len(conf), n))
    for r, c in enumerate(conf):
        for v in c:
            Amat[r, v] = 1
    ub = np.array([len(c) - 1 for c in conf], dtype=float)
    r = milp(c=-np.ones(n), constraints=LinearConstraint(Amat, -np.inf, ub), integrality=np.ones(n),
             bounds=Bounds(0, 1), options={"time_limit": tl, "disp": False, "mip_rel_gap": 0.0})
    dt = time.time() - t
    chosen = [v for v in range(n) if r.x is not None and r.x[v] > 0.5]
    T = [A[v] for v in chosen]
    res.update(status=int(r.status), message=str(r.message), objective=(-r.fun if r.fun is not None else None),
               mip_gap=(float(r.mip_gap) if hasattr(r, "mip_gap") and r.mip_gap is not None else None),
               mip_dual_bound=(float(r.mip_dual_bound) if hasattr(r, "mip_dual_bound") and r.mip_dual_bound is not None else None),
               witness_size=len(T), witness_sidon=is_sidon(T), time_s=round(dt, 1))
else:
    from ortools.sat.python import cp_model
    mdl = cp_model.CpModel()
    x = [mdl.NewBoolVar(f"x{v}") for v in range(n)]
    for c in conf:
        mdl.Add(sum(x[v] for v in c) <= len(c) - 1)
    mdl.Maximize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 1
    st = s.Solve(mdl)
    dt = time.time() - t
    chosen = [v for v in range(n) if s.Value(x[v])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else []
    T = [A[v] for v in chosen]
    res.update(status=s.StatusName(st), objective=s.ObjectiveValue(), best_bound=s.BestObjectiveBound(),
               witness_size=len(T), witness_sidon=is_sidon(T), time_s=round(dt, 1))
print(json.dumps(res, indent=1))
json.dump(res, open(f"/home/user/Erdos-757/experiments/referee/C003-round2/solve_{which}.json", "w"), indent=1)
