#!/usr/bin/env python3
"""Referee round 2 for L015: build S_K exactly (Fractions) and I_K = 269^K S_K (integers, two ways),
check Theorem 1(a) (count, copy intersections, levels), and run a relation census of I_K by
point completion: for every ordered triple (p1,p2,p3) in I_K^3 put p4 = p1+p2-p3 and test p4 in I_K.
This enumerates every ordered relation quadruple; each relation class {{p1,p2},{p3,p4}} is then
classified.  Prediction (Theorem 1(b),(c)): exactly 9(K+1) classes, each a 3-AP class whose point set
is phi^J(e) for some J<=K, e in E(O); hence 4*9(K+1) ordered quadruples and no 4-point relation.
Usage: python3 r2_family.py K1 K2 ...   Own code; standard library only.
"""
import sys, json
from fractions import Fraction as Fr

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
OI = [x for x in O if x not in (0, 269)]
E = [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121), (75, 117, 159),
     (83, 101, 119), (83, 121, 159), (117, 119, 121)]
r = Fr(18, 269)
def phi(x):
    return 101 + r * x
def phij(x, j):
    v = Fr(x)
    for _ in range(j):
        v = phi(v)
    return v

def build(K):
    copies = [[phij(x, j) for x in O] for j in range(K + 1)]
    S = sorted(set(v for c in copies for v in c))
    scale = 269 ** K
    I = []
    for v in S:
        w = v * scale
        assert w.denominator == 1
        I.append(int(w))
    # second, integer-only construction: N_j(x) = 101*269^j + 18*N_{j-1}(x), N_0(x) = x; I_K = 269^(K-j) N_j(x)
    I2 = set()
    for x in O:
        N = x
        I2.add(269 ** K * N)
        for j in range(1, K + 1):
            N = 101 * 269 ** j + 18 * N
            I2.add(269 ** (K - j) * N)
    assert sorted(I2) == I, "integer recursion disagrees with Fractions"
    return copies, S, I

def main(Ks):
    out = {}
    for K in Ks:
        copies, S, I = build(K)
        n = len(I)
        res = {"n": n, "n_ok": n == 11 + 9 * K}
        # copy intersections
        cs = [set(c) for c in copies]
        inter_ok = True
        for j in range(K + 1):
            if len(cs[j]) != 11:
                inter_ok = False
            for jp in range(j + 1, K + 1):
                X = cs[j] & cs[jp]
                if jp == j + 1:
                    want = {phij(101, j), phij(119, j)}
                    want2 = {phij(0, j + 1), phij(269, j + 1)}
                    if not (X == want == want2):
                        inter_ok = False
                elif X:
                    inter_ok = False
        # no point in three copies
        mult = {}
        for c in cs:
            for v in c:
                mult[v] = mult.get(v, 0) + 1
        res["copies_ok"] = inter_ok and max(mult.values()) <= 2
        # levels: points of level 0 = O, of level j>=1 = phi^j(O interior)
        lev = {}
        for j in range(K + 1):
            for v in cs[j]:
                lev.setdefault(v, j)
        lev_ok = all(set(v for v in lev if lev[v] == 0) == set(Fr(x) for x in O) for _ in [0])
        for j in range(1, K + 1):
            if set(v for v in lev if lev[v] == j) != set(phij(x, j) for x in OI):
                lev_ok = False
        res["levels_ok"] = lev_ok
        # predicted edges (integer form)
        scale = 269 ** K
        pred = set()
        for J in range(K + 1):
            for e in E:
                pred.add(tuple(sorted(int(phij(x, J) * scale) for x in e)))
        res["pred_edges"] = len(pred)
        # census by point completion
        Iset = set(I)
        nquad = 0
        classes = set()
        for p1 in I:
            for p2 in I:
                s = p1 + p2
                for p3 in I:
                    p4 = s - p3
                    if p4 in Iset:
                        if (p1 == p3 and p2 == p4) or (p1 == p4 and p2 == p3):
                            continue
                        nquad += 1
                        a = (p1, p2) if p1 <= p2 else (p2, p1)
                        b = (p3, p4) if p3 <= p4 else (p4, p3)
                        classes.add((a, b) if a <= b else (b, a))
        four = 0
        three_sets = set()
        bad = 0
        for a, b in classes:
            pts = set(a) | set(b)
            if len(pts) == 4:
                four += 1
            elif len(pts) == 3:
                # must be (u,u) vs (v,w), v<u<w
                dbl = [t for t in (a, b) if t[0] == t[1]]
                other = [t for t in (a, b) if t[0] != t[1]]
                if len(dbl) != 1 or not (other[0][0] < dbl[0][0] < other[0][1]):
                    bad += 1
                three_sets.add(tuple(sorted(pts)))
            else:
                bad += 1
        res.update({"ordered_quads": nquad, "classes": len(classes), "four_point": four, "bad": bad,
                    "ap_sets_eq_pred": three_sets == pred})
        # linearity: no pair of points in two APs
        pairs = {}
        lin = True
        for e in pred:
            for i in range(3):
                for k in range(i + 1, 3):
                    pr = (e[i], e[k])
                    if pr in pairs:
                        lin = False
                    pairs[pr] = 1
        res["linear"] = lin
        # midpoints = non-extreme points, each once
        mids = sorted(e[1] for e in pred)
        res["saturated"] = mids == sorted(I[1:-1])
        # degree profile
        deg = {}
        for e in pred:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        res["maxdeg"] = max(deg.values())
        ok = (res["n_ok"] and res["copies_ok"] and res["levels_ok"] and nquad == 36 * (K + 1)
              and len(classes) == 9 * (K + 1) and four == 0 and bad == 0 and res["ap_sets_eq_pred"]
              and res["pred_edges"] == 9 * (K + 1) and lin and res["saturated"] and res["maxdeg"] == 4)
        res["ok"] = ok
        out[K] = res
        print("K=%d n=%d copies_ok=%s levels_ok=%s ordered_quads=%d classes=%d four_point=%d bad=%d "
              "AP_sets==pred=%s edges=%d linear=%s saturated=%s maxdeg=%d -> %s"
              % (K, n, res["copies_ok"], res["levels_ok"], nquad, len(classes), four, bad, res["ap_sets_eq_pred"],
                 res["pred_edges"], lin, res["saturated"], res["maxdeg"], "OK" if ok else "FAIL"), flush=True)
    allok = all(v["ok"] for v in out.values())
    print("ALL R2 CENSUS OK" if allok else "R2 CENSUS FAILED")
    json.dump({str(k): v for k, v in out.items()}, open("r2_family_results.json", "w"), indent=1)

if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
