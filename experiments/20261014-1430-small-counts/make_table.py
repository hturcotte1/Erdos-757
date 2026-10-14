"""Aggregate results/*.json into results/summary.json and print a markdown table."""
import json, glob, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
rows = {}
for f in glob.glob(R + "/n*_m*.json"):
    if f.endswith("_real.json"): continue
    d = json.load(open(f)); rows[(d["n"], d["m"], bool(d.get("sample_size")))] = d
dfs = {}
for f in glob.glob(R + "/dfs_n*_m*.json"):
    d = json.load(open(f)); dfs[(d["n"], d["m"])] = d
out = {"exact": {}, "dfs_counts": {}}
for (n, m, smp), d in sorted(rows.items()):
    out["exact" if not smp else "sample"] = out.get("exact" if not smp else "sample", {})
    out["exact" if not smp else "sample"]["n%d_m%d" % (n, m)] = {k: d[k] for k in
        ("n", "f", "m", "saturated", "labelled_patterns", "patterns_up_to_reflection", "realizable_patterns", "free_dims_minus2", "reasons", "all_h_eq_f", "all_45", "t_enum", "t_realize", "sample_size") if k in d}
for (n, m), d in sorted(dfs.items()):
    out["dfs_counts"]["n%d_m%d" % (n, m)] = d
json.dump(out, open(R + "/summary.json", "w"), indent=1)
print("| n | m | sat | labelled | sym | up to refl | realizable | free params | tag |")
for (n, m, smp), d in sorted(rows.items()):
    print("| %d | %d | %s | %d | %d | %d | %d | %s | %s |" % (n, m, "yes" if d["saturated"] else "no", d["labelled_patterns"], d["reflection_symmetric"],
          d["patterns_up_to_reflection"], d["realizable_patterns"], d["free_dims_minus2"], "sample first %d" % d["sample_size"] if smp else "all"))
for (n, m), d in sorted(dfs.items()):
    print("DFS", n, m, d["labelled"], d["reflection_symmetric"], d["up_to_reflection"], d["nodes"], d["t"])
