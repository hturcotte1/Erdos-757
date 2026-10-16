"""Exact counts of extremal (4,5)-sets (h = f(n)) for small n.
usage: python3 counts.py N [M ...]   (run from repo root; one process; results -> results/n<N>_m<M>.json(.gz))
For each m: C DFS (class O, exactly m edges, alpha <= f(n)) -> all patterns; every pattern realized exactly
(fastreal for saturated/rigid, e757.realizability.realize_exact otherwise); each realization re-checked with
e757.core.is_45_set / alpha (h must equal f(n))."""
import sys, os, json, gzip, math, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "experiments", "20261014-1005-census-dfs"))
from e757.core import alpha, is_45_set, ap_edges
from e757.realizability import realize_exact, _rref, _x_rows
from e757.ordered_dfs_c import BIN
from fastreal import realize_fast

F = {6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8}
OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)

def m_min_hy(n):
    t = n - F[n]
    return max(1, -(-(17 * t - 5 * n) // 3))

def refl_of(n, edges):
    return tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in edges))

def canon(n, edges):
    t = tuple(sorted(tuple(e) for e in edges))
    return min(t, refl_of(n, t))

def normalize(vals):
    v = sorted(vals); lo = v[0]; v = [x - lo for x in v]
    g = 0
    for x in v: g = math.gcd(g, x)
    v = [x // g for x in v]
    return tuple(min(v, sorted(v[-1] - x for x in v)))

def enum(n, m, extra=()):
    T = F[n]; t0 = time.time()
    cmd = ["nice", "-n", "10", BIN, "n=%d" % n, "T=%d" % T, "m_min=%d" % m, "m_exact=%d" % m, "f7=1", "progress=0", "mode=enum"] + list(extra)
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    pats, stats = [], {}
    for line in out.splitlines():
        if line.startswith("SOL"):
            pats.append(tuple(sorted(tuple(int(x) for x in p.split(",")) for p in line.split()[2:])))
        elif line.startswith("DONE"):
            stats = dict(kv.split("=") for kv in line.split()[1:])
    assert int(stats["timed_out"]) == 0 and int(stats["solutions"]) == len(pats), stats
    return pats, stats, time.time() - t0

def realize_all(n, m, canons):
    reasons, real, fallback = {}, [], 0
    for c in canons:
        edges = list(c)
        fr = realize_fast(n, edges) if m == n - 2 else None
        if fr is None:
            if m == n - 2: fallback += 1
            r = realize_exact(n, edges)
            ok, payload = r[0], r[1]
        else:
            ok, payload = fr[0] == "ok", fr[1]
        if not ok:
            reasons[payload] = reasons.get(payload, 0) + 1
            continue
        vals = sorted(payload)
        h = alpha(vals, ap_edges(vals)); ok45 = is_45_set(vals)
        R, piv = _rref(_x_rows(n, edges), n)
        real.append({"edges": [list(e) for e in edges], "set": vals, "h": h, "is_45": ok45, "dim": n - len(piv)})
    return real, reasons, fallback

def run(n, m, sample=0):
    T = F[n]
    pats, stats, tenum = enum(n, m, ["limit=%d" % sample] if sample else [])  # sample mode = FIRST `sample` patterns in DFS order
    assert len(set(pats)) == len(pats)
    cs = sorted(set(canon(n, p) for p in pats))
    ncs = len(cs)
    t1 = time.time()
    real, reasons, fallback = realize_all(n, m, cs)
    classes = {}
    for r in real: classes.setdefault(normalize(r["set"]), []).append(r)
    res = {"n": n, "f": T, "m": m, "saturated": m == n - 2, "labelled_patterns": len(pats), "patterns_up_to_reflection": ncs, "sample_size": sample or None,
           "reflection_symmetric": sum(1 for p in pats if refl_of(n, p) == p),
           "realizable_patterns": len(real), "reasons": reasons, "all_h_eq_f": all(r["h"] == T for r in real),
           "all_45": all(r["is_45"] for r in real), "free_dims_minus2": sorted(set(r["dim"] - 2 for r in real)),
           "affine_classes_distinct_samples": len(classes), "dfs_nodes": int(stats["nodes"]), "t_enum": round(tenum, 1),
           "t_realize": round(time.time() - t1, 1), "fallback": fallback}
    tag = "n%d_m%d%s" % (n, m, "_sample" if sample else "")
    json.dump(res, open(os.path.join(OUT, tag + ".json"), "w"), indent=1)
    with gzip.open(os.path.join(OUT, tag + "_real.json.gz"), "wt") as g:
        json.dump(real, g)
    print(json.dumps(res), flush=True)

if __name__ == "__main__":
    args = sys.argv[1:]
    sample = 0
    if "--sample" in args:
        i = args.index("--sample"); sample = int(args[i + 1]); del args[i:i + 2]
    n = int(args[0])
    ms = [int(x) for x in args[1:]] or list(range(m_min_hy(n), n - 1))
    for m in ms: run(n, m, sample)
