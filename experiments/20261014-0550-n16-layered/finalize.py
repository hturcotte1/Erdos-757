"""Merge extension shards: dedupe under reflection, run realize_exact, new_claim for any set beating 4/7.
Usage: python3 finalize.py N M NSHARDS   -> results/n{N}_m{M}_solutions.jsonl (+ summary json)"""
import sys as _s, os as _o; _s.path.insert(0, _o.path.abspath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..")))
import glob, json, os, subprocess, sys
from e757.realizability import realize_exact
N, M, NSH = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
T = int(sys.argv[4]) if len(sys.argv) > 4 else None
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
res = os.path.join(here, "results")
allsol, tot = set(), 0
for sh in range(NSH):
    r = json.load(open(os.path.join(res, "n%d_m%d_ext_shard%d.json" % (N, M, sh))))
    T = r["T"]
    for s in r["solutions"]:
        t = tuple(sorted(tuple(e) for e in s)); tot += 1
        refl = tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in t))
        allsol.add(min(t, refl))
summary = {"N": N, "M": M, "T": T, "n_solutions_total": tot, "n_up_to_reflection": len(allsol), "realizable": []}
reasons = {}
with open(os.path.join(res, "n%d_m%d_solutions.jsonl" % (N, M)), "w") as fh:
    for t in sorted(allsol):
        fh.write(json.dumps([list(e) for e in t]) + "\n")
        r = realize_exact(N, list(t))
        if r[0]:
            rec = {"edges": [list(e) for e in t], "set": r[1]}
            if 7 * T < 4 * N:   # alpha/N < 4/7: this would beat the record
                p = subprocess.run([sys.executable, repo + "/scripts/new_claim.py", "--slug", "layered-n%d-m%d" % (N, M),
                                    "--set", ",".join(map(str, r[1]))], capture_output=True, text=True, cwd=repo)
                rec["new_claim"] = p.stdout[-1500:]
            summary["realizable"].append(rec)
        else:
            reasons[r[1]] = reasons.get(r[1], 0) + 1
summary["unrealizable_reasons"] = reasons
json.dump(summary, open(os.path.join(res, "n%d_m%d_summary.json" % (N, M)), "w"))
print({k: v for k, v in summary.items() if k != "realizable"}, "realizable:", len(summary["realizable"]))
