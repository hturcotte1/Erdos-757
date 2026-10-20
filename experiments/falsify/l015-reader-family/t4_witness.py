import json
from lib import *
Ustar = [0, 98, 101, 117, 119, 159, 269]
out = {}
for K in list(range(0, 31)) + [50, 61, 100, 150]:
    copies, ic, den = build(O0, 101, 18, K)
    pts = set(points(ic))
    T = set()
    for j in range(K+1):
        for x in Ustar: T.add(ic[j][O0.index(x)])
    r = {"K": K, "size": len(T), "claimed": 7 + 5*K, "subset_of_S_K": T <= pts, "sidon_by_definition": sums_distinct_subset(T)}
    # independent: no 3-AP by direct triple test via set lookup
    Ts = sorted(T); S = set(Ts)
    r["no_3AP"] = not any((Ts[i] + Ts[k]) % 2 == 0 and (Ts[i] + Ts[k]) // 2 in S for i in range(len(Ts)) for k in range(i+2, len(Ts)))
    r["ok"] = r["size"] == r["claimed"] and r["subset_of_S_K"] and r["sidon_by_definition"] and r["no_3AP"]
    out[K] = r
    if K % 10 == 0 or K > 30: print(r, flush=True)
json.dump(out, open("t4_witness.json", "w"), indent=1)
print("ALL_WITNESS_OK", all(r["ok"] for r in out.values()))
