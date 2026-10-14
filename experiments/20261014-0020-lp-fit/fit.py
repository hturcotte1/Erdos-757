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
    if r["slack"] > 2:
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
print("\n## 2. LP fits  tau <= a n + b m + sum c_i f_i   (min a+b ; then variants)")
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
    """Constraints depend only on (n, m, feats, saturated) and tau: keep the max tau per key (identical LP feasible set)."""
    key0 = (tuple(feats), id(R))
    if key0 in _comp_cache:
        return _comp_cache[key0]
    d = {}
    for r in R:
        k = (r["n"], r["m"], r["saturated"]) + tuple(r[f] for f in feats)
        if d.get(k, -1) < r["tau"]:
            d[k] = r["tau"]
    out = [dict(zip(["n", "m", "saturated"] + feats, k), tau=t) for k, t in d.items()]
    _comp_cache[key0] = out
    return out

def fit(feats, const=False, objective="ab", cbounds=(0, None), subset=None):
    R = compress(feats, rows if subset is None else subset)
    X = np.array([[r["n"], r["m"]] + [r[f] for f in feats] + ([1] if const else []) for r in R], float)
    tau = np.array([r["tau"] for r in R], float)
    k = X.shape[1]
    if objective == "ab":
        c = np.zeros(k); c[0] = c[1] = 1
    else:  # mean (RHS/n) over saturated rows with n>=14: the per-vertex bound at realistic feature densities
        sel = [i for i, r in enumerate(R) if r["saturated"] and r["n"] >= 14]
        c = (X[sel] / X[sel][:, [0]]).mean(axis=0)
    bnds = [(0, None), (0, None)] + [cbounds] * len(feats) + ([(None, None)] if const else [])
    res = linprog(c, A_ub=-X, b_ub=-tau, bounds=bnds, method="highs")
    return res, X, tau

def exact_check(coef, feats, const, tol_den=1000, subset=None):
    """round coefficients to Fractions, report max exact violation tau - RHS over all rows and the tight rows."""
    R = compress(feats, rows if subset is None else subset)
    co = [Fraction(x).limit_denominator(tol_den) for x in coef]
    viol = None; tight = 0
    for r in R:
        rhs = co[0] * r["n"] + co[1] * r["m"] + sum(co[2 + i] * r[f] for i, f in enumerate(feats)) + (co[2 + len(feats)] if const else 0)
        v = r["tau"] - rhs
        if viol is None or v > viol: viol = v
    return co, viol

results = []
def run(name, feats, const=False, objective="ab", cbounds=(0, None)):
    res, X, tau = fit(feats, const, objective, cbounds)
    if res.status != 0:
        print(f"- {name} const={const} obj={objective}: LP status {res.status}")
        return
    co, viol = exact_check(res.x, feats, const)
    slack = X @ res.x - tau
    ntight = int((slack < 1e-7).sum())
    ab = res.x[0] + res.x[1]
    ratio = 1 - ab
    names = ["a", "b"] + feats + (["const"] if const else [])
    cs = ", ".join(f"{n}={x:.4f}" for n, x in zip(names, res.x))
    print(f"- **{name}** const={const} obj={objective}: {cs}; a+b={ab:.4f} -> alpha/n >= 1-a-b = {ratio:.4f} (naive); "
          f"tight rows {ntight}; exact max violation after rounding (den<=1000): {float(viol):+.5f} ({viol})")
    results.append({"name": name, "const": const, "objective": objective, "coef": dict(zip(names, map(float, res.x))),
                    "a_plus_b": float(ab), "tight_rows": ntight, "exact_max_violation": str(viol)})
    return res

for const in (False, True):
    for name, feats in FEATS.items():
        run(name, feats, const, "ab")
print("\nvariant objective = mean RHS/n over saturated rows n>=14 (realistic densities):")
for name, feats in FEATS.items():
    if feats:
        run(name, feats, False, "mean")
        run(name, feats, True, "mean")
out["fits"] = results

# HY reference: exact violation of 5/17 n + 3/17 m
print("\nreference HY (5/17,3/17): max violation", max(Fraction(r['tau']) - Fraction(5 * r['n'] + 3 * r['m'], 17) for r in rows))
# restricted fits: saturated only, and saturated n>=12
print("\nsaturated rows only, no features (a n + b m + const):")
sat = [r for r in rows if r["saturated"]]
res, X, tau = fit([], True, "ab", subset=sat)
print(res.x, "a+b =", res.x[0] + res.x[1], "tight", int(((X @ res.x - tau) < 1e-7).sum()))
co, viol = exact_check(res.x, [], True, subset=sat); print("exact:", co, "viol", viol)
# saturated: simplest form tau <= s*n + t  (m = n-2)
best = None
for r in sat:
    pass
lo = max(Fraction(r["tau"] - 0, 1) / r["n"] for r in sat)  # ignoring constant: max tau/n
print("max tau/n over saturated rows:", lo, float(lo), "(argmax n:", [r['n'] for r in sat if Fraction(r['tau'], r['n']) == lo][:3], ")")
for n in sorted({r['n'] for r in sat}):
    mt = max(r['tau'] for r in sat if r['n'] == n)
    print(f"  saturated n={n}: max tau = {mt}  (min h = {n-mt}, 4n/7 = {4*n/7:.2f})")

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
print("\n## 4. Local structure around degree>=3 vertices in HY-near-tight rows (slack<=2)")
def vertex_types(r):
    n = r["n"]; edges = r["edges_list"]
    inc = collections.defaultdict(list)
    for (i, j, k) in edges:
        inc[i].append("L"); inc[j].append("M"); inc[k].append("R")
    return inc
nt = [r for r in rows if r["slack"] <= 2]
print("near-tight rows (slack<=2):", len(nt), " by slack:", dict(collections.Counter(r["slack"] for r in nt)), " by n:", dict(sorted(collections.Counter(r["n"] for r in nt).items())))
sig = collections.Counter(); sigdeg = collections.defaultdict(collections.Counter)
roles = collections.Counter()
for r in nt:
    inc = vertex_types(r)
    for v, lst in inc.items():
        if len(lst) >= 3:
            s = "".join(sorted(lst))
            sig[(len(lst), s)] += 1
            roles[s.count("M")] += 1
print("signature of incident edges (sorted roles: L=left endpoint, M=midpoint, R=right endpoint) for deg>=3 vertices:")
for (d, s), c in sorted(sig.items()):
    print(f"  deg {d} {s}: {c}")
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
for s_max in (0, 1):
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
json.dump(out, open(os.path.join(here, "analysis.json"), "w"), indent=1, default=str)
