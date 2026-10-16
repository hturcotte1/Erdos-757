"""Falsify Lemma Delta' (deletion version). Exact integer arithmetic. usage: python3 run.py"""
import sys, os, json, gzip, itertools
from collections import Counter
from fractions import Fraction
import numpy as np
ROOT = "/home/user/Erdos-757"
F = {4:3,5:4,6:4,7:5,8:5,9:6,10:6,11:7,12:7,13:8,14:8}

def aps(vals):
    n = len(vals); s = set(vals); out = []
    idx = {v: i for i, v in enumerate(vals)}
    for i in range(n):
        for k in range(i+1, n):
            t = vals[i] + vals[k]
            if t % 2 == 0 and t//2 in idx and i < idx[t//2] < k:
                out.append((i, idx[t//2], k))
    return out

def alpha_table(n, edges):
    """alpha[S] for all subsets S (bitmask), numpy"""
    N = 1 << n
    S = np.arange(N, dtype=np.int64)
    bad = np.zeros(N, dtype=bool)
    for e in edges:
        em = sum(1 << v for v in e)
        bad |= (S & em) == em
    pc = np.zeros(N, dtype=np.int64)
    for i in range(n): pc += (S >> i) & 1
    g = np.where(bad, 0, pc)
    for i in range(n):
        g2 = g.reshape(-1, 2, 1 << i)
        g2[:, 1, :] = np.maximum(g2[:, 1, :], g2[:, 0, :])
    return g

def bound(n, m, tau):
    # d <= m - (17 tau - 5 n - 7)/3 ; return Fraction
    return m - Fraction(17*tau - 5*n - 7, 3)

def analyse(sets, n, label, fn_target=None):
    """for each set: all pairs; classify by h(A-p-q)"""
    fA = F[n]; fB = F[n-2]
    dist = {"ext": Counter(), "other": Counter()}   # h(A-p-q)==h(A)-1 (and ==f(n-2)) vs rest
    hsub = Counter(); viol = []; nsets_with = 0; bnd_seen = Counter()
    adj_deg2 = Counter()
    nsets = 0
    for vals in sets:
        nsets += 1
        edges = aps(vals); m = len(edges)
        al = alpha_table(n, edges)
        h = int(al[(1 << n) - 1])
        tau = n - h
        deg = [0]*n; E = [set(e) for e in edges]
        for e in edges:
            for v in e: deg[v] += 1
        b = bound(n, m, tau)
        bnd_seen[(m, h, str(b))] += 1
        has = False
        for p, q in itertools.combinations(range(n), 2):
            eps = 1 if any(p in e and q in e for e in E) else 0
            d = deg[p] + deg[q] - eps
            hs = int(al[((1 << n) - 1) ^ (1 << p) ^ (1 << q)])
            hsub[(h, hs)] += 1
            if h == fA and hs == fB:  # extremal subset, f(n-2) = f(n)-1 needed
                assert fB == fA - 1
                dist["ext"][d] += 1; has = True
                if d > b: viol.append((vals, p, q, d, str(b)))
            else:
                dist["other"][(d, hs)] += 1
            if hs == h - 1 and h != fA: pass
        nsets_with += has
    return {"label": label, "n": n, "sets": nsets, "sets_with_extremal_pair": nsets_with,
            "dist_ext_pairs_d": dict(sorted(dist["ext"].items())),
            "dist_other_pairs_(d,hsub)": {str(k): v for k, v in sorted(dist["other"].items())},
            "h_vs_hsub": {str(k): v for k, v in sorted(hsub.items())},
            "bounds_seen_(m,h,bound)": {str(k): v for k, v in bnd_seen.items()},
            "violations": len(viol), "first_violation": viol[:1]}

def load_real(path):
    return [r["set"] for r in json.load(gzip.open(path, "rt")) if r["h"] == F[len(r["set"])]]

if __name__ == "__main__":
    out = []
    # 1
    d12 = json.load(gzip.open(ROOT + "/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz"))
    sets12 = [r["set"] for r in d12 if r["h"] == 7 and r["is_45"]]
    out.append(analyse(sets12, 12, "T1 n=12 all 54243 classes"))
    print("T1 done", flush=True)
    # 2
    R = ROOT + "/experiments/20261014-1430-small-counts/results/"
    for n, m in [(10, 8), (8, 6), (10, 7), (8, 5), (9, 7), (9, 6)]:
        sets = load_real(R + "n%d_m%d_real.json.gz" % (n, m))
        out.append(analyse(sets, n, "T2 n=%d m=%d (%d sets)" % (n, m, len(sets))))
        print("T2", n, m, flush=True)
    # 3
    sets14 = []
    for line in gzip.open(ROOT + "/data/census_n14_m12_classes.jsonl.gz", "rt"):
        r = json.loads(line); sets14.append(r["set"])
    r14 = analyse(sets14, 14, "T3 n=14 2910 classes")
    # adjacent degree-2 pairs distribution
    cnt = Counter(); allpairs = Counter()
    for vals in sets14:
        edges = aps(vals); deg = [0]*14
        for e in edges:
            for v in e: deg[v] += 1
        for p, q in itertools.combinations(range(14), 2):
            adj = any(p in e and q in e for e in edges)
            d = deg[p] + deg[q] - (1 if adj else 0)
            allpairs[d] += 1
            if adj and deg[p] == 2 and deg[q] == 2: cnt[d] += 1
    r14["adjacent_deg2_pairs_d"] = dict(cnt); r14["all_pairs_d"] = dict(sorted(allpairs.items()))
    out.append(r14)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w"), indent=1)
    for r in out:
        print(r["label"], "sets", r["sets"], "with ext pair", r["sets_with_extremal_pair"], "dist", r["dist_ext_pairs_d"], "viol", r["violations"], "bounds", r["bounds_seen_(m,h,bound)"])
    print("T3 adjacent deg-2 pairs", r14["adjacent_deg2_pairs_d"], "all", r14["all_pairs_d"])
