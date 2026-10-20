#!/usr/bin/env python3
"""CP-SAT as a pure feasibility check: is there a conflict-free subset of size >= 38?  (expect INFEASIBLE)"""
import json, sys, time
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *
from ortools.sat.python import cp_model
A, raw = load_claim_set(); n = len(A); conf = conflicts_from_definition(A)
res = {}
for k in (38, 37):
    mdl = cp_model.CpModel()
    x = [mdl.NewBoolVar(f"x{v}") for v in range(n)]
    for c in conf:
        mdl.AddBoolOr([x[v].Not() for v in c])
    mdl.Add(sum(x) >= k)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 900; s.parameters.num_workers = 1
    t = time.time(); st = s.Solve(mdl); dt = time.time() - t
    ver = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        T = [A[v] for v in range(n) if s.Value(x[v])]
        ver = is_sidon(T) and len(T) >= k
    print(f"CP-SAT feasibility size >= {k}: {s.StatusName(st)} ({dt:.1f}s) model_verified={ver}")
    res[f"ge{k}"] = {"status": s.StatusName(st), "time_s": round(dt, 1), "model_verified": ver}
json.dump(res, open("cpsat_feas38.json", "w"), indent=1)
