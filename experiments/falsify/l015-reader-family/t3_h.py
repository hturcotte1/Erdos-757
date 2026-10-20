import json, time, sys
from lib import *
tr = transfer(O0); best, Mx, R0 = tr
print("best", best); print("M", Mx); print("R0", R0); print("R0(x)M", maxplus(R0, Mx), "R0+5", [x+5 for x in R0], flush=True)
out = {}
Ks = list(range(0, 21)) + [30, 61, 100]
for K in Ks:
    copies, ic, den = build(O0, 101, 18, K)
    pts = points(ic); n = len(pts)
    groups, _ = relation_groups(pts)
    ps = [sorted(p) for p in relation_pointsets(groups)]
    t = time.time()
    dp, width = alpha_frontier_dp(n, ps, return_width=True)
    r = {"K": K, "n": n, "relations": len(ps), "dp_alpha": dp, "dp_width": width, "claimed": 7 + 5*K, "dp_sec": round(time.time()-t, 2)}
    if K <= 3:
        t = time.time(); st, obj, bound, sol = alpha_cpsat(n, ps, tl=600)
        r.update(cpsat_status=st, cpsat_obj=obj, cpsat_bound=bound, cpsat_sec=round(time.time()-t, 1),
                 witness_sidon_by_definition=sums_distinct_subset([pts[i] for i in sol]))
    if K <= 14:
        t = time.time(); r["sat_ge_h"] = sat_atleast(n, ps, 7+5*K); r["sat_ge_h_plus_1"] = sat_atleast(n, ps, 8+5*K); r["sat_sec"] = round(time.time()-t, 1)
    print(r, flush=True); out[K] = r
def good(r):
    c1 = ("cpsat_obj" not in r) or (r["cpsat_status"] == "OPTIMAL" and r["cpsat_obj"] == r["claimed"] and r["witness_sidon_by_definition"])
    c2 = ("sat_ge_h" not in r) or (r["sat_ge_h"] and not r["sat_ge_h_plus_1"])
    return r["dp_alpha"] == r["claimed"] and c1 and c2
print("ALL_h_OK", all(good(r) for r in out.values()))
