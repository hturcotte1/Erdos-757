"""Collect results/*.json into witnesses.json and table.md (HY bound, f(n) from START_HERE s.5)."""
import glob, json, os
from e757.fn_bounds import fn_bounds
here = os.path.dirname(os.path.abspath(__file__))
res = os.path.join(here, "results")
W, rows = {}, {}
for f in sorted(glob.glob(res + "/table_n*.json")):
    r = json.load(open(f)); n = r["n"]; rows[n] = r
    for key in ("f7", "nof7"):
        x = r[key]
        if x["alpha"] is not None:
            W["n%d_%s_min_alpha" % (n, key)] = {"n": n, "f7_free": key == "f7", "alpha": x["alpha"], "edges": x["edges"]}
        if x.get("min_m_edges"):
            W["n%d_%s_min_m" % (n, key)] = {"n": n, "f7_free": key == "f7", "alpha": x["alpha"], "edges": x["min_m_edges"]}
for f in sorted(glob.glob(res + "/n*_hy1.json")):
    r = json.load(open(f))
    if r["alpha"] is not None:
        W["n%d_f7_hyassisted" % r["n"]] = {"n": r["n"], "f7_free": True, "alpha": r["alpha"], "edges": r["edges"]}
for f in sorted(glob.glob(res + "/feas_*.json")):
    r = json.load(open(f))
    if r["result"] == "SAT":
        W["feas_n%d_T%d" % (r["n"], r["T"])] = {"n": r["n"], "f7_free": r["f7_free"], "alpha": max(r["T"], 0), "edges": r["edges"]}
json.dump(W, open(os.path.join(here, "witnesses.json"), "w"))
# alpha in feas witnesses is only <= T: recompute exactly
from e757.saturated import alpha_of_edges
for k, w in W.items():
    w["alpha"] = alpha_of_edges(w["n"], [tuple(e) for e in w["edges"]]) if k.startswith("feas") else w["alpha"]
json.dump(W, open(os.path.join(here, "witnesses.json"), "w"))
FB = fn_bounds(30)
out = ["| n | c_hyp (F7-free) | c_hyp (no F7) | min m (F7-free) | min m (no F7) | HY lower | f(n) known | time F7 / noF7 (s) |", "|---|---|---|---|---|---|---|---|"]
for n in sorted(rows):
    r = rows[n]
    def fmt(x, k):
        if x["alpha"] is None: return "?"
        v = str(x["alpha"]) if x["optimal"] else ">=?, <=%d" % x["alpha"]
        return v
    def mm(x):
        v = x.get("min_m")
        return "-" if v is None else (str(v) if x.get("min_m_proved_optimal") else "<=%d" % v)
    L, U = FB[n]
    fk = str(L) if L == U else "%d..%d" % (L, U)
    out.append("| %d | %s | %s | %s | %s | %d | %s | %s / %s |" % (n, fmt(r["f7"], "f7"), fmt(r["nof7"], "nof7"), mm(r["f7"]), mm(r["nof7"]), L, fk, r["f7"]["time"], r["nof7"]["time"]))
open(os.path.join(here, "table.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
