"""MILP cross-check (HiGHS via scipy; floating point, used only as a cross-check, the decisive methods are exact):
max sum x s.t. sum_{v in F} x_v <= |F| - 1 for every definition-derived forbidden set F, x binary; then the same with
sum x >= 34 (must be infeasible)."""
import json
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402

c = R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')
A = sorted(R.as_int_list(c['set']))
n = len(A)
forb, census = R.forbidden_sets(A)
M = np.zeros((len(forb), n))
ub = np.zeros(len(forb))
for r, F in enumerate(forb):
    for v in F:
        M[r, v] = 1
    ub[r] = len(F) - 1
out = {}
t = time.time()
res = milp(c=-np.ones(n), constraints=[LinearConstraint(M, -np.inf, ub)], integrality=np.ones(n),
           bounds=Bounds(0, 1), options={'mip_rel_gap': 0, 'time_limit': 600})
x = np.round(res.x).astype(int) if res.x is not None else None
chosen = [A[i] for i in range(n) if x is not None and x[i] == 1]
out['max'] = dict(status=int(res.status), message=res.message, obj=-res.fun if res.fun is not None else None,
                  dual_bound=getattr(res, 'mip_dual_bound', None), gap=getattr(res, 'mip_gap', None),
                  size=len(chosen), sidon=R.is_sidon_sums(chosen), secs=round(time.time() - t, 2))
print('MILP max:', out['max'])
t = time.time()
M2 = np.vstack([M, np.ones((1, n))])
lo2 = np.concatenate([np.full(len(forb), -np.inf), [34]])
ub2 = np.concatenate([ub, [n]])
res2 = milp(c=np.zeros(n), constraints=[LinearConstraint(M2, lo2, ub2)], integrality=np.ones(n),
            bounds=Bounds(0, 1), options={'time_limit': 600})
out['ge34'] = dict(status=int(res2.status), message=res2.message, secs=round(time.time() - t, 2))
print('MILP feasibility of sum >= 34:', out['ge34'])
with open('/home/user/Erdos-757/experiments/referee/C004-round1/milp_c004.json', 'w') as fh:
    json.dump(out, fh, indent=1, default=str)
