"""Summarise data/ext15_sets.jsonl and data/attempts.jsonl -> results.json (+ prints tables). Run from repo root."""
import json, collections, os, sys
H = os.path.dirname(os.path.abspath(__file__))
R = [json.loads(l) for l in open(os.path.join(H, "data/ext15_sets.jsonl"))]
A = [json.loads(l) for l in open(os.path.join(H, "data/attempts.jsonl"))]
out = {"n_sets": len(R)}
out["by_m"] = dict(collections.Counter(r["m"] for r in R))
out["attempt_patterns_by_m"] = {}
for m in (9, 10, 11, 12):
    x = [a for a in A if a["m"] == m]
    fails = collections.Counter()
    for a in x:
        for k, v in a["fail"].items(): fails[k] += v
    out["attempt_patterns_by_m"][m] = {"files": len(x), "patterns_tested": sum(a["new"] for a in x),
                                       "realizable": sum(a["realizable"] for a in x), "fail": dict(fails)}
out["prefix_files_with_found_by_m"] = {m: sum(1 for a in A if a["m"] == m and a["found"] > 0) for m in (9, 10, 11, 12)}
for m in (11, 12):
    x = [r for r in R if r["m"] == m]
    if not x: continue
    d = {}
    d["deg_seq"] = collections.Counter(tuple(r["deg_seq"]) for r in x).most_common(8)
    d["max_deg"] = dict(collections.Counter(r["deg_seq"][0] for r in x))
    d["n_max_sidon_min_med_max"] = [min(r["n_max_sidon"] for r in x), sorted(r["n_max_sidon"] for r in x)[len(x) // 2], max(r["n_max_sidon"] for r in x)]
    d["universal_any"] = sum(1 for r in x if r["universal"])
    d["n_ext_admissible_min_med_max"] = [min(r["n_ext_admissible"] for r in x), sorted(r["n_ext_admissible"] for r in x)[len(x) // 2], max(r["n_ext_admissible"] for r in x)]
    d["min_h_ext"] = dict(collections.Counter(r["min_h_ext"] for r in x))
    d["ext_degx"] = dict(collections.Counter(k for r in x for k in r["ext_degx_dist"]))
    d["cover_min"] = dict(collections.Counter(r["cover_min"] for r in x))
    d["n_min_covers"] = dict(collections.Counter(r["n_min_covers"] for r in x))
    ce = [r["cover_ext"] for r in x if "cover_ext" in r]
    d["cover_ext_sets_with_cover"] = len(ce)
    d["cover_ext_patterns"] = sum(c["patterns"] for c in ce)
    d["cover_ext_prefiltered_ok"] = sum(c["prefiltered"] for c in ce)
    d["cover_ext_realizable"] = sum(c["realizable"] for c in ce)
    d["records"] = sum(r["n_record_ext"] for r in x)
    out["m%d" % m] = d
json.dump(out, open(os.path.join(H, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
