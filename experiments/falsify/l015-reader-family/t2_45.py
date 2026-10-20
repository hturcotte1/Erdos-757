import json, time
from lib import *
out = {}
for K in range(0, 13):
    t = time.time()
    copies, ic, den = build(O0, 101, 18, K)
    pts = points(ic)
    m = min_distinct_diffs(pts)
    # count of 4-subsets with exactly 5 distinct diffs (tight) for information
    out[K] = {"n": len(pts), "n4subsets": __import__('math').comb(len(pts), 4), "min_distinct_positive_diffs": m, "sec": round(time.time()-t, 1)}
    print(K, out[K], flush=True)
json.dump(out, open("t2_45.json", "w"), indent=1)
print("ALL_(4,5)_OK", all(v["min_distinct_positive_diffs"] >= 5 for v in out.values()))
