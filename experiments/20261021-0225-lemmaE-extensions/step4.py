"""Iteration test: from S_K, E1, E12 apply the Lemma-E / Remark extension (a, a+t, a+2t) at EVERY vertex a
(universal or not) up to depth 2, recording (n, h, D=17h-9n, #universal vertices); then greedy DFS using universal vertices only
up to depth 6 from the sets with universal vertices.  Exact DP for h; (4,5) re-verified on the best chain."""
import json, random, sys, time
from lib import *

random.seed(757)

def state(B, g):
    E = aps(B)
    h, _ = alpha_dp(B, g)
    uni = [v for v in B if alpha_dp(B, g, [v])[0] == h - 1]
    return E, h, uni

def ext(B, g, a):
    span = max(B) - min(B)
    t = 3 * span + random.randrange(10**6, 10**7)
    nb = sorted(B + [a + t, a + 2 * t]); ng = dict(g); ng[a + t] = g[a]; ng[a + 2 * t] = g[a]
    return nb, ng

def load(name, K):
    B = sorted(json.load(open(f"set_{name}.json")))
    A0, copies = family(K)
    # recover group via the same construction as step3: groups by copy of original points; new points -> 0
    return B

# rebuild groups for step3 sets: original points are those of S_K shifted
from step3 import extend
def build(K, which):
    A0, copies = family(K); span = max(A0) - min(A0)
    t1 = 3 * span + 1000003; t2 = 5 * span + 7000027
    pairs = {"S": [], "E1": [(min(A0), t1)], "E2": [(max(A0), t2)], "E12": [(min(A0), t1), (max(A0), t2)]}[which]
    B = extend(A0, pairs)
    s0 = min([min(A0)] + [a - t for a, t in pairs])
    sh = {v - s0: v for v in A0}
    g = {v: (min(j for j, cp in enumerate(copies) if sh[v] in cp) if v in sh else 0) for v in B}
    return B, g

# the groups: sh[v] maps shifted point -> original; copies hold original ints
res = []
T0 = time.time()
for K in (4, 5, 6):
    for which in ("S", "E1", "E12"):
        B, g = build(K, which)
        E, h, uni = state(B, g)
        row = dict(K=K, start=which, n=len(B), h=h, D=17 * h - 9 * len(B), n_universal=len(uni))
        # depth-1 moves at every vertex
        d1 = {}
        for a in B:
            nb, ng = ext(B, g, a)
            E2, h2, uni2 = state(nb, ng)
            key = (h2 - h, len(E2) - len(E), len(uni2))
            d1.setdefault(key, []).append(B.index(a))
        row["depth1_(dh,dm,n_universal_after)->vertex_indices"] = {str(k): v for k, v in sorted(d1.items())}
        res.append(row); print(json.dumps(row), flush=True)
        if time.time() - T0 > 900: break
json.dump(res, open("step4_results.json", "w"), indent=1)
