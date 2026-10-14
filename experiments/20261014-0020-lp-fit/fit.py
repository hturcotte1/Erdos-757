"""Analysis of dataset.jsonl.gz. Writes analysis.json and prints tables (markdown).
LP via scipy HiGHS (floats, [heuristic]); every fitted inequality is then re-verified EXACTLY with Fractions."""
import gzip, json, os, sys, statistics, collections
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

here = os.path.dirname(os.path.abspath(__file__))
rows = []
for l in gzip.open(os.path.join(here, "dataset.jsonl.gz"), "rt"):
    r = json.loads(l)
    if r["slack"] > 5:
        del r["edges_list"]
        if r["src"].startswith("randsub"):
            del r["set"]
    rows.append(r)
out = {}
print(f"rows: {len(rows)}")
bysrc = collections.Counter(r["src"] for r in rows)
print("rows by src:", dict(bysrc))
print("rows by n:", dict(sorted(collections.Counter(r["n"] for r in rows).items())))
print("saturated rows:", sum(r["saturated"] for r in rows))

# ---- 1. Henning-Yeo
print("\n## 1. HY check")
slacks = [r["slack"] for r in rows]
print("rows with slack<0:", sum(s < 0 for s in slacks), " min slack:", min(slacks))
# sanity: tau recompute exact from edges is already in features; check D identity
bad = [r for r in rows if r["D"] != r["slack"] + 3 * (r["n"] - r["m"])]
print("rows violating D = slack + 3(n-m):", len(bad), "(expected only where HY-derived identity is invalid: none)")
hist = collections.Counter(slacks)
print("slack histogram (lowest 12):", sorted(hist.items())[:12])
out["min_slack"] = min(slacks)
out["slack_hist_low"] = sorted(hist.items())[:12]
# per-n min slack and per-n min slack among saturated
print("\nmin slack by n (all rows / saturated rows):")
tab = {}
for n in sorted({r["n"] for r in rows}):
    a = [r["slack"] for r in rows if r["n"] == n]
    b = [r["slack"] for r in rows if r["n"] == n and r["saturated"]]
    tab[n] = (min(a), len(a), min(b) if b else None, len(b))
    print(f"  n={n}: all min {min(a)} ({len(a)} rows); saturated min {min(b) if b else '-'} ({len(b)} rows)")
out["min_slack_by_n"] = tab
mn = min(slacks)
near = sorted([r for r in rows if r["slack"] == mn], key=lambda r: (-r["n"], r["set"]))
print(f"\nrows attaining min slack {mn}: {len(near)}")
# top 20: lowest slack, then largest n, prefer saturated, dedupe (already deduped by normalization)
top = sorted([r for r in rows if r["n"] >= 10 and "set" in r], key=lambda r: (r["slack"], -r["n"], not r["saturated"]))[:20]
out["top20"] = [{"n": r["n"], "m": r["m"], "tau": r["tau"], "slack": r["slack"], "D": r["D"], "src": r["src"], "set": r["set"]} for r in top]
print("top 20 among n>=10 (lowest slack, then larger n; n<10 rows listed above are trivial small cases):")
for r in top:
    print(f"  slack {r['slack']} n={r['n']} m={r['m']} tau={r['tau']} D={r['D']} src={r['src']} set={r['set']}")

# ---- 2. LP fits
# All features are ADDITIVE under disjoint union (gluing Ma-Tang Lemma 3.6 makes the AP hypergraph a disjoint union), and so are
# tau, n, m.  Hence a HOMOGENEOUS inequality (no constant) valid on the rows is automatically valid on all glued sets.
# Constant-term fits are NOT closed under gluing and carry no asymptotic information.
print("\n## 2. LP fits  tau <= a n + b m + sum c_i f_i   (homogeneous; a,b,c_i >= 0)")
FEATS = {
    "none": [],
    "non_mid": ["non_mid"],
    "deg(d2,d1)": ["d2", "d1"],
    "deg(d1,d2,d3,d4p)": ["d1", "d2", "d3", "d4p"],
    "comps": ["comps"],
    "all(non_mid,d2,d1,comps)": ["non_mid", "d2", "d1", "comps"],
    "mid_end2+parent_only": ["mid_end2", "parent_only"],
    "mid_edge_deg1": ["edges_mid_deg1"],
    "d3+d4p": ["d3", "d4p"],
}
_comp_cache = {}
def compress(feats, R):
    """Constraints depend only on (n, m, feats, tag) and tau: keep max tau per key (same feasible set); tag=extremal marks record sets."""
    key0 = (tuple(feats), id(R))
    if key0 in _comp_cache:
        return _comp_cache[key0]
    d = {}
    for r in R:
        k = (r["n"], r["m"], r["saturated"], r["extremal"]) + tuple(r[f] for f in feats)
        if d.get(k, -1) < r["tau"]:
            d[k] = r["tau"]
    out = [dict(zip(["n", "m", "saturated", "extremal"] + feats, k), tau=t) for k, t in d.items()]
    _comp_cache[key0] = out
    return out

# extremal rows: the full record sets (A_base, three 12-pt sets, n=10, n=11, n=8 records)
EXT = {tuple(v) for v in [[0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]]}
for r in rows:
    r["extremal"] = (r["src"] in ("sub_A_base", "sub_rec12", "sub_rec12b", "sub_rec12c", "sub_rec10", "sub_rec11", "sub_rec8")
                     and r.get("set") is not None and False)
FULL = {"sub_A_base": 14, "sub_rec12": 12, "sub_rec12b": 12, "sub_rec12c": 12, "sub_rec10": 10, "sub_rec11": 11, "sub_rec8": 8}
for r in rows:
    r["extremal"] = (r["src"] in FULL and r["n"] == FULL[r["src"]])

def fit(feats, const=False, objective="ab"):
    R = compress(feats, rows)
    X = np.array([[r["n"], r["m"]] + [r[f] for f in feats] + ([1] if const else []) for r in R], float)
    tau = np.array([r["tau"] for r in R], float)
    k = X.shape[1]
    if objective == "ab":
        c = np.zeros(k); c[0] = c[1] = 1
    else:  # "ext": tightest inequality = minimise the total slack (RHS - tau) over the full extremal record sets
        sel = [i for i, r in enumerate(R) if r["extremal"]]
        c = X[sel].sum(axis=0)
    bnds = [(0, None), (0, None)] + [(0, None)] * len(feats) + ([(None, None)] if const else [])
    res = linprog(c, A_ub=-X, b_ub=-tau, bounds=bnds, method="highs")
    return res, X, tau, R

def exact_check(coef, feats, const, R, tol_den=1000):
    co = [Fraction(x).limit_denominator(tol_den) for x in coef]
    viol = None
    for r in R:
        rhs = co[0] * r["n"] + co[1] * r["m"] + sum(co[2 + i] * r[f] for i, f in enumerate(feats)) + (co[2 + len(feats)] if const else 0)
        v = r["tau"] - rhs
        if viol is None or v > viol: viol = v
    return co, viol

results = []
def run(name, feats, const=False, objective="ab"):
    res, X, tau, R = fit(feats, const, objective)
    if res.status != 0:
        print(f"- {name} const={const} obj={objective}: LP status {res.status}"); return
    co, viol = exact_check(res.x, feats, const, R)
    slack = X @ res.x - tau
    ntight = int((slack < 1e-7).sum())
    names = ["a", "b"] + feats + (["const"] if const else [])
    cs = ", ".join(f"{n}={x:.4f}" for n, x in zip(names, res.x))
    ext_tight = sum(1 for i, r in enumerate(R) if r["extremal"] and slack[i] < 1e-7)
    ext_n = sum(1 for r in R if r["extremal"])
    print(f"- **{name}** obj={objective}: {cs}; tight distinct-feature-keys {ntight}; tight extremal sets {ext_tight}/{ext_n}; "
          f"exact max violation after rounding (den<=1000): {viol}")
    results.append({"name": name, "const": const, "objective": objective, "coef": dict(zip(names, map(float, res.x))),
                    "tight_keys": ntight, "tight_extremal": f"{ext_tight}/{ext_n}", "exact_max_violation": str(viol)})

print("\n### 2a. objective min a+b (literal spec), homogeneous")
for name, feats in FEATS.items():
    run(name, feats, False, "ab")
print("\n### 2b. objective = total slack on the 7 full extremal record sets (tightest valid inequality), homogeneous")
for name, feats in FEATS.items():
    run(name, feats, False, "ext")
print("\n### 2c. (non-homogeneous, NOT closed under gluing: shown for completeness) objective min a+b with free constant")
for name in ("none", "non_mid", "comps"):
    run(name, FEATS[name], True, "ab")
out["fits"] = results

# 2d. Pareto frontier of tau <= a n + b m  (a(b) = max_rows (tau - b m)/n, exact)
print("\n### 2d. exact frontier  a(b) = max over rows (tau - b m)/n  for tau <= a n + b m")
R0 = compress([], rows)
print("| b | a(b) | a+b | alpha/n >= 1-a-b (using m<=n-2) | rows attaining (n,m,tau) |")
print("|---|---|---|---|---|")
front = []
for b in [Fraction(0), Fraction(1, 17), Fraction(2, 17), Fraction(3, 17), Fraction(1, 4), Fraction(1, 3), Fraction(3, 8), Fraction(1, 2)]:
    best = max(Fraction(r["tau"]) - b * r["m"] for r in R0 for _ in [0]) if False else None
    vals = [((Fraction(r["tau"]) - b * r["m"]) / r["n"], r) for r in R0]
    a = max(v for v, _ in vals)
    att = sorted({(r["n"], r["m"], r["tau"]) for v, r in vals if v == a})[:4]
    print(f"| {b} | {a} = {float(a):.4f} | {float(a+b):.4f} | {float(1-a-b):.4f} | {att} |")
    front.append((str(b), str(a)))
out["frontier_ab"] = front
print("HY reference: b=3/17 needs a>=?; HY says a=5/17=%.4f valid" % (5/17))
# 2e. non_mid family, implied worst-case ratio: bound per vertex g(x)=a+b(1-x)+c x, x=non_mid/n, also tau<=m => per-vertex <= 1-x
print("\n### 2e. tau <= a n + b m + c*non_mid ; a(b,c)=max_rows (tau-b m-c nm)/n exact grid; implied worst-case per-vertex bound W=max_x min(g(x),1-x)")
R1 = compress(["non_mid"], rows)
best = []
grid_b = [Fraction(i, 34) for i in range(0, 18)]
grid_c = [Fraction(i, 8) for i in range(0, 25)]
for b in grid_b:
    for c in grid_c:
        a = max((Fraction(r["tau"]) - b * r["m"] - c * r["non_mid"]) / r["n"] for r in R1)
        a = max(a, Fraction(0))
        # W = max over x in [0,1] of min(g(x),1-x), g(x) = a+b+(c-b)x  (float eval ok for ranking; exact recheck below)
        g0 = a + b
        if c <= b:
            W = min(g0, Fraction(1))
        else:
            xs = (1 - a - b) / (1 + c - b)
            W = 1 - xs if xs >= 0 else Fraction(0)
        best.append((W, a, b, c))
best.sort()
for W, a, b, c in best[:8]:
    print(f"  W={float(W):.4f} (alpha/n >= {float(1-W):.4f}) with a={a} b={b} c={c}")
out["nonmid_best"] = [(str(W), str(a), str(b), str(c)) for W, a, b, c in best[:8]]

# ---- 3. D distribution on random saturated sets
print("\n## 3. D = 17h-9n distribution on random saturated (4,5)-sets (src randN, full sets)")
print("| n | #sets | D min | D median | D max | min h | #D/n<5/7 | #h<4n/7 |")
print("|---|---|---|---|---|---|---|---|")
dist = {}
records = []
for n in sorted({r["n"] for r in rows if r["src"].startswith("rand") and not r["src"].startswith("randsub")}):
    R = [r for r in rows if r["src"] == f"rand{n}"]
    Ds = [r["D"] for r in R]
    below = [r for r in R if Fraction(r["D"], n) < Fraction(5, 7)]
    hb = [r for r in R if 7 * r["alpha"] < 4 * n]
    dist[n] = {"count": len(R), "Dmin": min(Ds), "Dmed": statistics.median(Ds), "Dmax": max(Ds), "min_h": min(r["alpha"] for r in R),
               "below_5_7": len(below), "h_below_4n_7": len(hb)}
    records += below
    d = dist[n]
    print(f"| {n} | {d['count']} | {d['Dmin']} | {d['Dmed']} | {d['Dmax']} | {d['min_h']} | {d['below_5_7']} | {d['h_below_4n_7']} |")
out["D_dist"] = dist
# also across ALL rows incl. subsets: min D/n
allmin = min(rows, key=lambda r: Fraction(r["D"], r["n"]))
print("min D/n over ALL rows:", Fraction(allmin["D"], allmin["n"]), "n=", allmin["n"], "src", allmin["src"], allmin["set"])
print("rows with D/n < 5/7:", sum(Fraction(r["D"], r["n"]) < Fraction(5, 7) for r in rows))
out["records_below_5_7"] = [r["set"] for r in records]
hist = collections.Counter((r['n'], r['D']) for r in rows if r['src'].startswith('rand') and not r['src'].startswith('randsub') and r['n'] >= 14)
print("D histograms n>=14 (full random sets):", sorted(hist.items()))

# ---- 4. local structure of near-tight rows
print("\n## 4. Local structure around degree>=3 vertices in HY-near-tight rows (slack<=5, n>=10; smaller n are trivially tight)")
def vertex_types(r):
    n = r["n"]; edges = r["edges_list"]
    inc = collections.defaultdict(list)
    for (i, j, k) in edges:
        inc[i].append("L"); inc[j].append("M"); inc[k].append("R")
    return inc
nt = [r for r in rows if r["slack"] <= 5 and r["n"] >= 10]
print("near-tight rows (slack<=5, n>=10; smaller n are trivially tight):", len(nt), " by slack:", dict(collections.Counter(r["slack"] for r in nt)), " by n:", dict(sorted(collections.Counter(r["n"] for r in nt).items())))
sigslack = collections.Counter(); sig = collections.Counter(); sigdeg = collections.defaultdict(collections.Counter)
roles = collections.Counter()
for r in nt:
    inc = vertex_types(r)
    for v, lst in inc.items():
        if len(lst) >= 3:
            s = "".join(sorted(lst))
            sig[(len(lst), s)] += 1
            sigslack[(r["slack"], len(lst), s)] += 1
            roles[s.count("M")] += 1
print("signature of incident edges (sorted roles: L=left endpoint, M=midpoint, R=right endpoint) for deg>=3 vertices:")
for (d, s), c in sorted(sig.items()):
    print(f"  deg {d} {s}: {c}")
print("same, split by HY slack (slack, deg, roles): count")
for k, c in sorted(sigslack.items()):
    print("  ", k, c)
# structure: number of M roles at deg>=3 vertices; neighbourhood: how many neighbours also deg>=3; vertex deg multiset
adjh = collections.Counter(); degseq = collections.Counter(); sat_nt = 0
for r in nt:
    inc = vertex_types(r)
    deg = {v: len(l) for v, l in inc.items()}
    for v in deg:
        if deg[v] >= 3:
            nb = set()
            for (i, j, k) in r["edges_list"]:
                if v in (i, j, k):
                    nb |= {i, j, k} - {v}
            adjh[sum(1 for u in nb if deg.get(u, 0) >= 3)] += 1
    degseq[(r["d0"], r["d1"], r["d2"], r["d3"], r["d4p"])] += 1
print("# of deg>=3 neighbours of a deg>=3 vertex (primal graph) :", dict(sorted(adjh.items())))
print("most common degree profiles (d0,d1,d2,d3,d4p) in near-tight rows:", degseq.most_common(8))
# which rows slack<=2 are saturated
print("near-tight rows saturated:", sum(r["saturated"] for r in nt))
# per-slack signature for slack<=1 rows if any
for s_max in (3, 4):
    sub = [r for r in nt if r["slack"] <= s_max]
    print(f"slack<={s_max}: rows {len(sub)}; ", [(r['n'], r['m'], r['tau'], r['set']) for r in sub[:5]])
out["near_tight"] = {"rows": len(nt), "signatures": {f"{d}:{s}": c for (d, s), c in sig.items()},
                     "deg3plus_neighbours_deg3plus": dict(adjh), "profiles": degseq.most_common(8)}
# example: A_base
Ab = [r for r in rows if r.get("set") == [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]]
if Ab:
    r = Ab[0]; inc = vertex_types(r)
    print("\nA_base: slack", r["slack"], "D", r["D"], "; deg>=3 vertices:")
    for v, l in sorted(inc.items()):
        if len(l) >= 3:
            print("  value", r["set"][v], "roles", "".join(sorted(l)))
    print("  A_base APs (left,mid,right):", [tuple(r["set"][x] for x in e) for e in r["edges_list"]])
json.dump(out, open(os.path.join(here, "analysis.json"), "w"), indent=1, default=str)
