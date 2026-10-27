"""cross-check p3_fast against the slow SDR test of hyp25 on random sub-hypergraphs and gadget graphs"""
import random
from hyp25 import *
from lemmas25 import p3_fast, NEAR, SLACK2
rnd = random.Random(5); cnt = 0; mism = 0
for c in NEAR + SLACK2[:5]:
    for (n0, m0, t0, E) in load_cell(*c)[:40]:
        V = list(range(n0))
        for trial in range(6):
            E2 = list(E)
            # add 1-3 random edges among existing / new vertices
            for _ in range(rnd.randint(0, 3)):
                N = max(V) + 1
                cand = V + [N]
                e = tuple(sorted(rnd.sample(cand, 3)))
                if e not in E2:
                    E2.append(e)
            V2 = sorted(set(V) | set(v for e in E2 for v in e))
            a = p3(E2, V2); b = p3_fast(E2, V2); cnt += 1; nfalse = globals().get("nfalse", 0) + (not a); globals()["nfalse"] = nfalse
            if a != b: mism += 1
print('p3 cross-check graphs', cnt, 'P3-violating', globals().get('nfalse', 0), 'mismatches', mism)
