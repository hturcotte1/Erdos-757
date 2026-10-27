"""Referee #5, round 3: exact check of the corrected Step 8.4 (H_1) chain of L021.
For R in C (the 32 stored pieces) and every vertex u of R, H' = R + e', e' = {u, z1, z2}
(z1, z2 new).  Checks, by enumerating ALL edge subsets (exact integers):
  (a) R satisfies (P3): |V(U)| >= |U| + 2 for every nonempty U subset E(R)  [membership in C]
  (b) H' is linear and satisfies (P3) on every nonempty edge subset (so e(S) <= |S|-2, |S|>=2)
  (c) max over S >= e' of e_{H'}(S) - |S| equals -2, attained only at S = e'
      (so '<= |S|-2' holds, and the old '<= |S|-3' fails exactly at S = e', holds for |S| >= 4).
Standard library only; reads only experiments/prover/L021/closure_results.json (edge lists).
"""
import json, sys
from itertools import combinations

P = json.load(open(sys.argv[1]))["pieces"]

def vmask(e):
    return (1 << e[0]) | (1 << e[1]) | (1 << e[2])

def popc(x):
    return bin(x).count("1")

def p3_ok(edges):
    """(P3) for all nonempty edge subsets; returns min of |V(U)| - |U| over nonempty U."""
    m = len(edges); vm = [vmask(e) for e in edges]; best = None
    # subset DP on union masks
    union = [0] * (1 << m)
    for s in range(1, 1 << m):
        low = s & -s; i = low.bit_length() - 1
        union[s] = union[s ^ low] | vm[i]
        val = popc(union[s]) - popc(s)
        if best is None or val < best:
            best = val
    return best

def linear(edges):
    for a, b in combinations(edges, 2):
        if len(set(a) & set(b)) >= 2:
            return False
    return True

tot_cases = 0; fails = 0; old_fail_only_at_eprime = 0
for pc in P:
    E = [tuple(e) for e in pc["edges"]]; n = pc["n"]; m = len(E)
    assert m == pc["m"]
    assert linear(E), pc["name"]
    assert p3_ok(E) >= 2, pc["name"]          # (a): R in C (P3)
    for u in range(n):
        z1, z2 = n, n + 1
        ep = (u, z1, z2)
        Hp = E + [ep]
        tot_cases += 1
        ok_lin = linear(Hp)
        ok_p3 = p3_ok(Hp) >= 2                  # (b)
        # (c): S >= e' ; e_{H'}(S) - |S| maximised over S = V(U) u e', U subset E(R)
        vm = [vmask(e) for e in E]; emask = (1 << u) | (1 << z1) | (1 << z2)
        best = None; argbest = []
        union = [0] * (1 << m)
        for s in range(0, 1 << m):
            if s:
                low = s & -s; i = low.bit_length() - 1
                union[s] = union[s ^ low] | vm[i]
            S = union[s] | emask
            # e_{H'}(S): count edges of H' inside S (closure: count all R-edges inside S, plus e')
            eS = 1 + sum(1 for j in range(m) if vm[j] & S == vm[j])
            val = eS - popc(S)
            if best is None or val > best:
                best = val; argbest = [S]
            elif val == best:
                argbest.append(S)
        only_eprime = (best == -2) and all(S == emask for S in argbest)
        if not (ok_lin and ok_p3 and best <= -2):
            fails += 1
            print("FAIL", pc["name"], "u=", u, ok_lin, ok_p3, best)
        if only_eprime:
            old_fail_only_at_eprime += 1
print(f"pieces={len(P)} (R,u) cases={tot_cases} failures={fails} "
      f"cases where max_(S>=e') e(S)-|S| = -2 attained only at S=e': {old_fail_only_at_eprime}")
print("ALL OK" if fails == 0 and old_fail_only_at_eprime == tot_cases else "CHECK OUTPUT")
