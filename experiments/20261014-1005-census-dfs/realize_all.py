"""Realize every O' solution (K30,K31, cores<=4 edges) with realize_exact; affine classes; known-set check.
Input results/n12_m10_filtered.txt.gz (output of ./filter).  Output results/realized_n12.json + stdout summary.
Usage: python3 realize_all.py [start_index end_index]  (default all)"""
import sys, os, gzip, json, math, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from e757.core import alpha, is_45_set, ap_edges
from e757.realizability import realize_exact, _rref, _x_rows
from e757.saturated import map_of_set, edges_of_map
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastreal import realize_fast
N = 12
lo = int(sys.argv[1]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 10**12
here = os.path.dirname(os.path.abspath(__file__))
def normalize(vals):
    v = sorted(vals); l = v[0]; v = [x - l for x in v]
    g = 0
    for x in v: g = math.gcd(g, x)
    v = [x // g for x in v]
    r = sorted(v[-1] - x for x in v)
    return tuple(min(v, r))
def canon(edges):
    t = tuple(sorted(tuple(e) for e in edges))
    r = tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in t))
    return min(t, r)
pats = []
counts = {"canon": 0, "k30": 0, "k31": 0, "c4": 0, "call": 0}
for line in gzip.open(os.path.join(here, "results/n12_m10_filtered.txt.gz"), "rt"):
    f = line.split(); fl = list(map(int, f[:4]))
    counts["canon"] += 1
    counts["k30"] += fl[0]
    if fl[0] and fl[1]:
        counts["k31"] += 1
        if fl[2]:
            counts["c4"] += 1
            pats.append((tuple(tuple(map(int, t.split(","))) for t in f[4:]), fl[3]))
            if fl[3]: counts["call"] += 1
pats = pats[lo:hi]
nfallback = 0; reasons = {}; realizable = []; t0 = time.time(); rig = 0
for idx, (t, in_call) in enumerate(pats):
    fr = realize_fast(N, list(t))
    if fr is None:
        nfallback += 1; r = realize_exact(N, list(t))
    elif fr[0] == "ok":
        r = (True, fr[1])
    else:
        r = (False, fr[1])
    if not r[0]:
        reasons[r[1]] = reasons.get(r[1], 0) + 1
        if in_call == 0: reasons["(excluded by long core) " + r[1]] = reasons.get("(excluded by long core) " + r[1], 0) + 1
        continue
    vals = sorted(r[1]); h = alpha(vals, ap_edges(vals)); ok45 = is_45_set(vals)
    R, piv = _rref(_x_rows(N, list(t)), N)
    realizable.append({"edges": [list(e) for e in t], "set": vals, "h": h, "is_45": ok45, "rigid": (N - len(piv)) == 2, "in_call": in_call})
    if (idx + 1) % 20000 == 0: print(idx + 1, len(pats), len(realizable), round(time.time() - t0), flush=True)
classes = {}
for k, r in enumerate(realizable): classes.setdefault(normalize(r["set"]), []).append(k)
known = {}
data = json.load(open(os.path.join(here, "../../data/small_records.json")))["sets"]
from e757 import core as _core
cands = {("record_" + k): v["set"] for k, v in data.items() if len(v["set"]) == N}
cands.update({"core.KNOWN: " + k: v for k, v in _core.KNOWN.items() if len(v) == N})
cset = set(canon(r["edges"]) for r in realizable)
for name, A in cands.items():
    lo_, hi_, mid = map_of_set(A)
    known[name] = {"pattern_in_realizable": canon(edges_of_map(mid)) in cset, "affine_class_in_realized": normalize(A) in classes, "h": alpha(sorted(A))}
out = {"range": [lo, hi], "filter_counts": counts, "n_tested": len(pats), "n_realizable": len(realizable),
       "n_rigid": sum(r["rigid"] for r in realizable), "n_affine_classes": len(classes), "unrealizable_reasons": reasons,
       "all_h_7": all(r["h"] == 7 for r in realizable), "all_45": all(r["is_45"] for r in realizable),
       "realizable_all_in_full_core_set": all(r["in_call"] for r in realizable),
       "record_beating": sum(1 for r in realizable if 7 * r["h"] < 4 * N), "known_sets": known,
       "n_fallback_to_realize_exact": nfallback, "seconds": round(time.time() - t0)}
suffix = "" if hi >= 10**12 and lo == 0 else "_%d_%d" % (lo, hi)
json.dump(realizable, open(os.path.join(here, "results/realized_n12%s.json" % suffix), "w"))
json.dump(out, open(os.path.join(here, "results/realize_summary%s.json" % suffix), "w"), indent=1)
print(json.dumps(out, indent=1))
