import json, os, sys, collections
repo = "/home/user/Erdos-757"; sys.path.insert(0, repo)
here = os.path.dirname(os.path.abspath(__file__))
def load(f):
    p = here + "/" + f
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
R = {"op": load("results_op.jsonl"), "real": load("results_real.jsonl")}
W = {"op": {}, "real": {}}; status = {"op": {}, "real": {}}
for c in R:
    for r in R[c]:
        status[c][(r["n"], r["m"])] = r
        if r["status"] == "optimal":
            n, m, a = r["n"], r["m"], r["alpha"]
            W[c]["%d,%d" % (n, m)] = dict(n=n, m=m, alpha=a, tau=n - a, slack=5*n+3*m-17*(n-a), edges=r["edges"],
                                          **({"set": r["set"]} if "set" in r else {}))
json.dump(W, open(here + "/witnesses.json", "w"))
def cell(c, n, m):
    r = status[c].get((n, m))
    if r is None: return "."
    if r["status"] != "optimal": return "?>=%d" % (n - r["alpha_ge"] + 0) if False else "t/o"
    tau = n - r["alpha"]; s = 5*n+3*m-17*tau
    return "%d/%d" % (tau, s)
ns = sorted({n for c in R for (n, m) in status[c]})
out = []
minslack = {}
for c, title in (("op", "O' (abstract ordered class)"), ("real", "Realizable class")):
    out.append("\n### %s: tau_max/slack for each (n, m)\n" % title)
    mmax = max([n - 2 for n in ns] or [0])
    out.append("| n \\ m | " + " | ".join(str(m) for m in range(1, mmax + 1)) + " | min slack (m) |")
    out.append("|" + "---|" * (mmax + 2))
    for n in ns:
        row = []; best = None
        for m in range(1, mmax + 1):
            if m > n - 2: row.append(""); continue
            cs = cell(c, n, m)
            r = status[c].get((n, m))
            if r and r["status"] == "optimal":
                s = 5*n+3*m-17*(n-r["alpha"])
                if best is None or s < best[0]: best = (s, [m])
                elif s == best[0]: best[1].append(m)
            row.append(cs)
        minslack[(c, n)] = best
        row = [("**%s**" % x if best and x and x != "t/o" and x.endswith("/%d" % best[0]) else x) for x in row]
        out.append("| %d | " % n + " | ".join(row) + " | %s |" % ("%d (m=%s)" % (best[0], ",".join(map(str, best[1]))) if best else "-"))
out.append("\n### Gaps: (n,m) with strictly smaller tau_max in the realizable class\n")
gaps = []
for (n, m), r in sorted(status["real"].items()):
    o = status["op"].get((n, m))
    if r["status"] == "optimal" and o and o["status"] == "optimal" and r["alpha"] > o["alpha"]:
        gaps.append((n, m, n - o["alpha"], n - r["alpha"], 5*n+3*m-17*(n-o["alpha"]), 5*n+3*m-17*(n-r["alpha"])))
out.append("| n | m | tau_max O' | tau_max real | slack O' | slack real |\n|---|---|---|---|---|---|")
for g in gaps: out.append("| " + " | ".join(map(str, g)) + " |")
if not gaps: out.append("(none)")
open(here + "/tables.md", "w").write("\n".join(out))
print("\n".join(out))
# structures
from e757.realizability import realize_exact
S = []
for c in ("op", "real"):
    for key, w in sorted(W[c].items(), key=lambda kv: tuple(map(int, kv[0].split(",")))):
        if w["slack"] > 3: continue
        n, edges = w["n"], [tuple(e) for e in w["edges"]]
        roles = {v: [] for v in range(n)}
        for i, j, k in edges:
            roles[i].append("L"); roles[j].append("M"); roles[k].append("R")
        rp = {v: "".join(sorted(roles[v], key="LMR".index)) or "-" for v in roles}
        deg = sorted((len(roles[v]) for v in roles), reverse=True)
        par = list(range(n))
        def find(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for e in edges:
            for v in e[1:]: par[find(v)] = find(e[0])
        comps = collections.defaultdict(list)
        for v in range(n): comps[find(v)].append(v)
        comp_sizes = sorted((len(x) for x in comps.values()), reverse=True)
        ok = bool(realize_exact(n, edges)[0])
        S.append(dict(cls=c, n=n, m=w["m"], tau=w["tau"], slack=w["slack"], degree_seq=deg,
                      nonmidpoints=n - w["m"], role_pattern=[rp[v] for v in range(n)],
                      role_multiset=dict(collections.Counter(rp.values())), component_sizes=comp_sizes,
                      realizable=ok, edges=w["edges"]))
json.dump(S, open(here + "/structures.json", "w"), indent=1)
print("\nstructures:")
for s in S:
    print(s["cls"], s["n"], s["m"], "tau", s["tau"], "s", s["slack"], "deg", "".join(map(str, s["degree_seq"])), "nonmid", s["nonmidpoints"],
          "comps", s["component_sizes"], "real", s["realizable"], s["role_multiset"])
