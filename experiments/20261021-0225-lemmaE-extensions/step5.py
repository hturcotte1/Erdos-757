"""Beam search over iterated Lemma-E/Remark extensions (a, a+t, a+2t) at any vertex a (universal or not).
Score = 7h - 4n (negative <=> beats 4/7).  Each node: exact DP for h and the universal vertices.
Moves: every universal vertex, plus up to 4 spread non-universal vertices.  Beam width W, depth D.
The best chain is re-verified at the end: own (4,5) test, e757.is_45_set, exact DP h, m."""
import json, random, sys, time
from lib2 import *
random.seed(757)
W, DEPTH, TLIM = 4, 8, 1500
T0 = time.time()
out = []
for K, which in ((5, "S"), (5, "E12")):
    B, g = build(K, which)
    E, h, uni = state(B, g)
    beam = [(7 * h - 4 * len(B), B, g, h, uni, [])]
    best = beam[0]
    for depth in range(DEPTH):
        cand = []
        for sc, B, g, h, uni, hist in beam:
            nonuni = [a for a in B if a not in set(uni)]
            moves = list(uni) + nonuni[:: max(1, len(nonuni) // 4)][:4]
            seen = set()
            for a in moves:
                nb, ng = ext(B, g, a)
                E2, h2, uni2 = state(nb, ng)
                key = (len(nb), h2, len(uni2), a in uni)
                if key in seen: continue
                seen.add(key)
                cand.append((7 * h2 - 4 * len(nb), nb, ng, h2, uni2, hist + [(B.index(a), a in uni, h2 - h, len(E2) - len(E))]))
        cand.sort(key=lambda c: (c[0], -len(c[4])))
        beam = cand[:W]
        if beam and beam[0][0] < best[0]: best = beam[0]
        print(K, which, "depth", depth + 1, "best score", beam[0][0], "n", len(beam[0][1]), "h", beam[0][3], "n_universal", len(beam[0][4]), "hist", beam[0][5], flush=True)
        if time.time() - T0 > TLIM: break
    sc, B, g, h, uni, hist = best
    ok, cnt, mn = own_45(B)
    row = dict(K=K, start=which, best_score=sc, n=len(B), h=h, ratio=f"{h}/{len(B)}", hist=hist, own_45=ok, e757_45=bool(core.is_45_set(B)), m=len(aps(B)))
    out.append(row); print(json.dumps(row), flush=True)
    json.dump(out, open("step5_results.json", "w"), indent=1)
