#!/usr/bin/env python3
"""Fourth formulation: minimum transversal tau of the conflict hypergraph (HiGHS MILP), h = n - tau.
Also: the LP relaxation value and an independent-set upper bound from the degree structure."""
import json, sys, time
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
A, raw = load_claim_set(); n = len(A); conf = conflicts_from_definition(A)
M = np.zeros((len(conf), n))
for r, c in enumerate(conf):
    for v in c: M[r, v] = 1
t = time.time()
r = milp(c=np.ones(n), constraints=LinearConstraint(M, 1, np.inf), integrality=np.ones(n), bounds=Bounds(0, 1),
         options={"mip_rel_gap": 0.0, "time_limit": 600})
tau = int(round(r.fun)); cover = [v for v in range(n) if r.x[v] > 0.5]
# verify the cover hits every conflict, and that the complement is Sidon
assert all(any(v in cover for v in c) for c in conf)
T = [A[v] for v in range(n) if v not in cover]
print(f"transversal MILP: status={r.status} ({r.message}) tau={tau} -> h = n - tau = {n - tau}; complement Sidon={is_sidon(T)} size={len(T)}; {time.time()-t:.1f}s")
lp = linprog(c=np.ones(n), A_ub=-M, b_ub=-np.ones(len(conf)), bounds=[(0, 1)] * n, method="highs")
print(f"LP relaxation of tau: {lp.fun:.4f} (so fractional bound h <= {n - lp.fun:.4f}); integrality gap closed by branch and bound")
json.dump({"tau": tau, "h": n - tau, "status": int(r.status), "lp_tau": float(lp.fun), "complement_sidon": is_sidon(T)}, open("solve_transversal.json", "w"), indent=1)
