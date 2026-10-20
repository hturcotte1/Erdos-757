"""Checks of the certificate's hand statements (F-facts, Step 5.6 bounds, Step 5.3 bijection, size formula, sanity numbers). Own code."""
import json, random
from fractions import Fraction
from lib import *
res = {}
O = O0; Oi = O[1:-1]
# F1/F3
res["269_prime"] = all(269 % q for q in range(2, 17))
res["27169=101*269"] = 27169 == 101*269
res["251*108<27169<251*109"] = 251*108 < 27169 < 251*109
res["y(0),y(269)"] = (251*0-27169, 251*269-27169, (251*269-27169) == 150*269)
res["y(x)_div_269_only_endpoints"] = [x for x in O if (251*x-27169) % 269 == 0]
res["269^2_divides_y_endpoints"] = [ (251*x-27169) % 269**2 == 0 for x in (0, 269)]
# F2
L = Fraction(27169, 251); phi = lambda x: 101 + Fraction(18, 269)*x
res["phi(L)=L"] = phi(L) == L; res["phi(0),phi(269)"] = (phi(0), phi(269))
# F4: doubled sums
from collections import defaultdict
d = defaultdict(list)
for i in range(11):
    for j in range(i, 11): d[O[i]+O[j]].append((O[i], O[j]))
rep = {s: v for s, v in d.items() if len(v) > 1}
res["F4_repeated_sums"] = {s: v for s, v in sorted(rep.items())}
res["F4_num_repeated=9_each_twice"] = len(rep) == 9 and all(len(v) == 2 for v in rep.values())
E = apsO(O); res["E(O)"] = E
# F5 sum list
res["F5ii_sums<=159"] = sorted(x+y for x in Oi for y in Oi if x <= y and x+y <= 159)
res["F5_269-x"] = [269-x for x in Oi]
sol = [(x,y,z) for x in Oi for y in Oi for z in Oi if (x+y-z) % 269 == 0]
res["F5iv_solutions"] = sol
# Lemma 1.2 up to d=60 (exact Fractions)
hits = set()
for x in O:
    y = Fraction(x)
    for dd in range(1, 61):
        y = phi(y)
        if y.denominator == 1 and int(y) in O: hits.add((dd, x, int(y)))
res["lemma12_hits_d<=60"] = sorted(hits)
# Step 5.6 bounds
def maxU(excl=(), force_out=()):
    best = 0
    for U in range(1 << 11):
        S = {O[i] for i in range(11) if (U >> i) & 1}
        if S & set(excl): continue
        if any(set(e) <= S for e in E): continue
        best = max(best, len(S))
    return best
res["5.6a_max_adm"] = maxU()
res["5.6b_no101_119"] = maxU([101, 119])
res["5.6c_no0"] = maxU([0]); res["5.6c'_no269"] = maxU([269])
res["5.6d_no101_119_0"] = maxU([101, 119, 0]); res["5.6d'_no101_119_269"] = maxU([101, 119, 269])
res["5.4_no_edge_in_{0,101,119,269}_except_e7"] = [e for e in E if len(set(e) & {0,101,119,269}) >= 2]
n_sidon = sum(1 for U in range(1 << 11) if not any(all((U >> O.index(v)) & 1 for v in e) for e in E))
res["num_admissible_subsets_incl_empty"] = n_sidon
# degrees in 5.6(b): W=O\{101,119}
W = [x for x in O if x not in (101,119)]; EW = [e for e in E if set(e) <= set(W)]
res["5.6b_edges"] = EW; res["5.6b_deg"] = {x: sum(x in e for e in EW) for x in W}
# 6.1
Ustar = {0,98,101,117,119,159,269}
res["U*_admissible"] = not any(set(e) <= Ustar for e in E)
# Step 5.3 bijection and size formula on random Sidon subsets of S_K
random.seed(7); bijfail = 0; sizefail = 0; trials = 0
for K in (3, 5, 8):
    copies, ic, den = build(O, 101, 18, K); pts = points(ic); idx = {p: i for i, p in enumerate(pts)}
    groups, _ = relation_groups(pts); ps = [sorted(p) for p in relation_pointsets(groups)]
    byp = defaultdict(list)
    for t, P in enumerate(ps):
        for v in P: byp[v].append(t)
    for _ in range(300):
        order = list(range(len(pts))); random.shuffle(order)
        T = set()
        for v in order:
            T.add(v)
            if any(set(ps[t]) <= T for t in byp[v]): T.discard(v)
        # random maximal Sidon subset T (index set)
        Tp = {pts[v] for v in T}
        assert sums_distinct_subset(Tp)
        trials += 1
        U = [frozenset(x for x in O if ic[j][O.index(x)] in Tp) for j in range(K+1)]
        # admissible
        assert all(not any(set(e) <= u for e in E) for u in U)
        # consistency
        cons = all(((101 in U[j]), (119 in U[j])) == ((0 in U[j+1]), (269 in U[j+1])) for j in range(K))
        rebuilt = {ic[j][O.index(x)] for j in range(K+1) for x in U[j]}
        if not cons or rebuilt != Tp: bijfail += 1
        size = len(U[0]) + sum(len(U[j]) - (0 in U[j]) - (269 in U[j]) for j in range(1, K+1))
        if size != len(Tp): sizefail += 1
res["bijection_trials"] = trials; res["bijection_failures"] = bijfail; res["size_formula_failures"] = sizefail
# record numbers & HY sanity for K
rows = []
for K in range(0, 12):
    n = 11+9*K; h = 7+5*K; m = 9*(K+1); tau = n-h
    rows.append((K, n, h, Fraction(h, n) < Fraction(4, 7), 17*tau <= 5*n+3*m, 5*n+3*m-17*tau == 14+4*K, 11*tau <= 3*n+2*m))
res["K_n_h_below47_HYok_slackformula_I11ok"] = [tuple(map(str, r)) for r in rows]
res["first_K_below_4/7"] = next(r[0] for r in rows if r[3])
print(json.dumps(res, indent=1, default=str)[:6000])
json.dump(res, open("t7_hand.json", "w"), indent=1, default=str)
