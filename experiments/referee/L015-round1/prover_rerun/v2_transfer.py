#!/usr/bin/env python3
"""L015 / C2: the 4-state max-plus transfer matrix of Step 4, computed in two independent ways.
  (A) all 2^11 subsets U of O as bitmasks; U admissible iff it contains none of the nine 3-APs of O
      (the APs re-derived here from the triples a<u<c, a+c=2u);
  (B) all subsets U of O by itertools.combinations; U admissible iff U is Sidon BY DEFINITION
      (all sums x+y, x<=y, distinct) -- no AP list used.  (A) and (B) must agree because the
      only relations a+b=c+d in O are the nine APs (v1_facts_O.py, F4).
States: s = a(U) = ([0 in U],[269 in U]) (anchor state), s' = b(U) = ([101 in U],[119 in U]) (inner state),
ordered (0,0),(1,0),(0,1),(1,1).  best[s][s'] = max |U|;  M[s][s'] = best[s][s'] - |s|;  R0[s'] = max_s best[s][s'].
Run:  python3 -I v2_transfer.py
"""
from itertools import combinations

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
ST = [(0, 0), (1, 0), (0, 1), (1, 1)]
NEG = None


def ok(cond, label):
    if not cond:
        raise SystemExit("FAILED: " + label)
    print("OK  ", label)


def states(U):
    U = set(U)
    return (int(0 in U), int(269 in U)), (int(101 in U), int(119 in U))


# (A) bitmask enumeration with the AP list
E = sorted((a, u, c) for a in O for u in O for c in O if a < u < c and a + c == 2 * u)
assert len(E) == 9
idx = {v: i for i, v in enumerate(O)}
emask = [sum(1 << idx[v] for v in e) for e in E]
bestA = {}
cntA = {}
for T in range(1 << 11):
    if any(T & m == m for m in emask):
        continue
    U = [O[i] for i in range(11) if T >> i & 1]
    s, sp = states(U)
    k = len(U)
    if k > bestA.get((s, sp), -1):
        bestA[(s, sp)] = k
        cntA[(s, sp)] = 0
    if k == bestA[(s, sp)]:
        cntA[(s, sp)] += 1

# (B) Sidon-by-definition enumeration, no AP list
def is_sidon(U):
    sums = [x + y for i, x in enumerate(U) for y in U[i:]]
    return len(sums) == len(set(sums))

bestB = {}
nsid = 0
for k in range(12):
    for U in combinations(O, k):
        if is_sidon(U):
            nsid += 1
            s, sp = states(U)
            bestB[(s, sp)] = max(bestB.get((s, sp), -1), k)

ok(bestA == bestB and len(bestA) == 16, "best[s][s'] identical by (A) AP-free bitmasks and (B) Sidon-by-definition; all 16 entries finite")
print("     number of Sidon (= AP-free) subsets of O, including the empty set:", nsid)
best = [[bestA[(s, sp)] for sp in ST] for s in ST]
M = [[best[i][k] - sum(ST[i]) for k in range(4)] for i in range(4)]
R0 = [max(best[i][k] for i in range(4)) for k in range(4)]
print("     states (order):", ST)
print("     best[s][s'] (rows s = anchor state, columns s' = inner state):")
for i in range(4):
    print("      ", ST[i], best[i], "  #maximisers:", [cntA[(ST[i], ST[k])] for k in range(4)])
print("     M =", M)
print("     R0 =", R0)
ok(M == [[5, 6, 6, 6], [4, 5, 5, 5], [4, 5, 5, 5], [4, 5, 5, 5]], "M = [[5,6,6,6],[4,5,5,5],[4,5,5,5],[4,5,5,5]] (the agent's matrix)")
ok(R0 == [6, 7, 7, 7], "R0 = [6,7,7,7] (the page's vector)")
ok(max(R0) == 7, "h(O) = max R0 = 7")


def mp(R, M):
    return [max(R[i] + M[i][k] for i in range(4)) for k in range(4)]


R1 = mp(R0, M)
print("     R0 (x) M =", R1)
ok(R1 == [r + 5 for r in R0], "R0 (x) M = R0 + 5 = [11,12,12,12] (max-plus eigenvector, eigenvalue 5)")
# the termwise maxima (which i attains the max in each column) -- for the certificate's table
for k in range(4):
    att = [ST[i] for i in range(4) if R0[i] + M[i][k] == R1[k]]
    print(f"     column {ST[k]}: R0[i]+M[i][k] = {[R0[i] + M[i][k] for i in range(4)]}, max {R1[k]} attained at {att}")
# consistency: iterate (the proof uses only the one-step identity and translation equivariance)
R = list(R0)
for t in range(1, 101):
    R = mp(R, M)
    assert R == [r + 5 * t for r in R0], t
ok(True, "iteration check: R_t = R0 + 5t for t = 1..100 (consistency only)")
# explicit admissible U* with both anchors and both inner points, |U*| = 7
Ustar = [0, 98, 101, 117, 119, 159, 269]
ok(is_sidon(Ustar) and not any(set(e) <= set(Ustar) for e in E) and states(Ustar) == ((1, 1), (1, 1)) and len(Ustar) == 7,
   "U* = {0,98,101,117,119,159,269}: Sidon, AP-free, a(U*) = b(U*) = (1,1), |U*| = 7 = best[(1,1)][(1,1)]")
for e in E:
    print("     AP", e, "misses", sorted(set(e) - set(Ustar)))
# the upper-bound inequalities actually used in Step 4 (each is an entry of the table above)
need = {"alpha(O) <= 7": max(max(r) for r in best) <= 7,
        "best[s][(0,0)] <= 6 for all s": all(best[i][0] <= 6 for i in range(4)),
        "best[(0,0)][s'] <= 6 for all s'": all(best[0][k] <= 6 for k in range(4)),
        "best[(0,0)][(0,0)] <= 5": best[0][0] <= 5,
        "best[s][s'] <= 5 + |s| for |s| = 1": all(best[i][k] <= 6 for i in (1, 2) for k in range(4)),
        "best[s][(0,0)] <= 4 + |s| for s != (0,0)": all(best[i][0] <= 4 + sum(ST[i]) for i in (1, 2, 3))}
for k, v in need.items():
    ok(v, "used bound: " + k)
print("ALL TRANSFER CHECKS OK")
