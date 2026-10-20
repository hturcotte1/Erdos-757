#!/usr/bin/env python3
"""SAT (CaDiCaL + totalizer; also Glucose4 + seqcounter) and frontier-DP routes for h(C003)."""
import json
import sys
import time
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *

A, raw = load_claim_set()
n = len(A)
conf = conflicts_from_definition(A)
print(f"n={n}, minimal conflicts from the definition: {len(conf)}, sizes {sorted(set(map(len,conf)))}")
res = {"n": n, "num_conflicts": len(conf)}

# ---- SAT -------------------------------------------------------------------------------------
for k in (37, 38):
    for solver, enc in (("cadical195", "totalizer"), ("glucose4", "seqcounter"), ("cadical195", "kmtotalizer")):
        t = time.time()
        sat, chosen = sat_atleast(n, conf, k, solver, enc)
        dt = time.time() - t
        ver = None
        if sat:
            T = [A[v] for v in chosen]
            ver = is_sidon(T) and len(T) >= k
        print(f"SAT  >= {k:2d}  {solver:10s} {enc:11s}: {'SAT' if sat else 'UNSAT'}  ({dt:.1f}s)" + (f"  model size {len(chosen)} Sidon-verified={ver}" if sat else ""))
        res[f"sat_ge{k}_{solver}_{enc}"] = {"sat": sat, "time_s": round(dt, 2), "model_verified": ver, "model_size": (len(chosen) if sat else None)}
        if sat:
            assert ver

# ---- frontier DP, several orders --------------------------------------------------------------
ints, levels, is_anchor = rebuild_family(6)
assert ints == A
orders = {
    "copy_order": sorted(range(n), key=lambda v: (levels[v], is_anchor[v], A[v])),
    "level_then_value": sorted(range(n), key=lambda v: (levels[v], A[v])),
    "reverse_copy_order": sorted(range(n), key=lambda v: (-levels[v], not is_anchor[v], A[v])),
    "sorted_by_value": list(range(n)),
}
for name, order in orders.items():
    t = time.time()
    cap = 3_000_000 if name == "sorted_by_value" else None
    best, mask, peak = frontier_dp(n, conf, order, max_states=cap)
    dt = time.time() - t
    if best is None:
        print(f"DP   {name:20s}: ABORTED, state count exceeded {cap} (peak {peak}) ({dt:.1f}s)")
        res[f"dp_{name}"] = {"best": None, "peak_states": peak, "time_s": round(dt, 2)}
        continue
    T = [A[v] for v in range(n) if mask >> v & 1]
    ok = is_sidon(T) and len(T) == best
    print(f"DP   {name:20s}: h = {best}, peak states {peak}, witness Sidon-verified={ok} ({dt:.1f}s)")
    res[f"dp_{name}"] = {"best": best, "peak_states": peak, "time_s": round(dt, 2), "witness_verified": ok}
    assert ok
json.dump(res, open("/home/user/Erdos-757/experiments/referee/C003-round2/solve_sat_dp.json", "w"), indent=1)
