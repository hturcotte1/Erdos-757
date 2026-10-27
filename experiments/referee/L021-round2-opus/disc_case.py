"""Brute force of the disconnected case of L021 Theorem 7(v) (all three co-vertex
pairs of the hub v inside one piece F): for every piece F of L* and every set of
three pairwise disjoint pairs of vertices of F-degree <= 2, no pair inside an edge of
F, build B = F + v + {v}uP_1 + {v}uP_2 + {v}uP_3 and test
  (1) tau(B) = tau(F) + 1  (computed directly by branching, independent of the
      transversal-meeting criterion, on every configuration),
  (2) for tau-raising B: s(B) = s(F) - 2 < 0 and B is NOT in C (F7 or (P3) fails),
as L016 predicts. Usage: disc_case.py [max_piece_n]"""
import json, sys, time
from itertools import combinations
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rlib import tau, min_transversals, degrees, is_linear, p3_ok_hall, iso, F7, s_of, masks

ROOT = "/home/user/Erdos-757/"
maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 17
pieces = json.load(open(ROOT + "experiments/prover/L021/closure_results.json"))["pieces"]
t0 = time.time()


def has_F7_new(edges, new_idx):
    """F7 copies in B must use >= 2 of the three new edges (F is F7-free and v has degree 3)."""
    m = len(edges)
    old = [i for i in range(m) if i not in new_idx]
    for k in (2, 3):
        for N in combinations(sorted(new_idx), k):
            for O in combinations(old, 5 - k):
                F = [edges[i] for i in N + O]
                vs = set()
                for e in F:
                    vs |= set(e)
                if len(vs) == 7 and iso(F, F7):
                    return True
    return False


tot_conf = tot_raise = tot_inC = 0
mismatch = 0
for p in pieces:
    if p["n"] > maxn:
        continue
    E = [tuple(e) for e in p["edges"]]
    n, m = p["n"], len(E)
    t = tau(n, E)
    MT = min_transversals(n, E, t)
    d = degrees(n, E)
    att = [x for x in range(n) if d[x] <= 2]
    inside = set()
    for e in E:
        for a, b in combinations(sorted(e), 2):
            inside.add((a, b))
    pairs = [pr for pr in combinations(att, 2) if pr not in inside]
    conf = raise_ = inC = 0
    v = n
    for P1, P2, P3 in combinations(pairs, 3):
        if len(set(P1) | set(P2) | set(P3)) != 6:
            continue
        conf += 1
        pm = [(1 << a) | (1 << b) for (a, b) in (P1, P2, P3)]
        covered = any(all(T & q for q in pm) for T in MT)
        Bedges = E + [(v,) + P1, (v,) + P2, (v,) + P3]
        tB = tau(n + 1, Bedges)
        if (tB == t + 1) != (not covered):
            mismatch += 1
        if tB == t + 1:
            raise_ += 1
            assert s_of(n + 1, m + 3, tB) == s_of(n, m, t) - 2 < 0
            assert is_linear(Bedges)
            new_idx = {m, m + 1, m + 2}
            if (not has_F7_new(Bedges, new_idx)) and p3_ok_hall(n + 1, Bedges):
                inC += 1
    tot_conf += conf; tot_raise += raise_; tot_inC += inC
    print(f"{p['name']:12s} n={n:2d} |MT|={len(MT):4d} attachable={len(att):2d} configs={conf:6d} "
          f"tau-raising={raise_:5d} tau-raising in C={inC} [{time.time()-t0:.0f}s]", flush=True)
print(f"TOTAL configs={tot_conf} tau-raising={tot_raise} tau-raising in C={tot_inC} "
      f"criterion/direct-tau mismatches={mismatch}")
print("ALL OK" if tot_inC == 0 and mismatch == 0 else "SOME FAILURE")
