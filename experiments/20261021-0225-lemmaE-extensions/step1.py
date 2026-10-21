import sys, json, time
from lib import *
res = {}
for K in (3, 4, 5, 6):
    t0 = time.time()
    A, copies = family(K)
    g = groups_for(A, copies)
    h, mf = alpha_dp(A, g)
    lo, hi = min(A), max(A)
    hlo, _ = alpha_dp(A, g, [lo]); hhi, _ = alpha_dp(A, g, [hi])
    res[K] = dict(n=len(A), m=len(aps(A)), h=h, maxfront=mf, alpha_minus_min=hlo, alpha_minus_max=hhi,
                  min_universal=(hlo == h - 1), max_universal=(hhi == h - 1), sec=round(time.time() - t0, 1))
    print(K, res[K], flush=True)
json.dump(res, open("step1_universality_dp.json", "w"), indent=1)
