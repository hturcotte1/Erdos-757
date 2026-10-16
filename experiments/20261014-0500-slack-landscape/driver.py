"""Slack landscape. usage: driver.py CLASS(op|real) NMIN NMAX [tl]
For each (n,m): smallest T with alpha<=T feasible (=> tau_max = n-T); T starts at the HY / trivial lower bound.
Results appended to results_<class>.jsonl (one json per (n,m))."""
import sys, json, time, os
repo = "/home/user/Erdos-757"
sys.path.insert(0, repo)
from e757.cpsat_model import feasible_alpha_le, solve_realizable, load_cores
cls, nmin, nmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
MOFF = int(os.environ.get('MOFF', '99'))
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_%s.jsonl" % cls)
done = set()
if os.path.exists(out):
    for l in open(out):
        r = json.loads(l); done.add((r["n"], r["m"]))
op_lb = {}
if cls == "real":
    for l in open(os.path.join(os.path.dirname(out), "results_op.jsonl")):
        r = json.loads(l)
        if r["status"] in ("optimal", "range"): op_lb[(r["n"], r["m"])] = r["alpha"] if r["status"] == "optimal" else r["alpha_ge"]
opts = dict(monotone=True, medial=True, cores=cores, core_lit_budget=(int(os.environ.get('BUDGET','500000')) or None))
for n in range(nmin, nmax + 1):
    for m in range(max(1, n - 2 - MOFF), n - 1):
        if (n, m) in done: continue
        t0 = time.time()
        T = max(n - ((5 * n + 3 * m) // 17), n - m, 1)
        if cls == "real":
            T = max(T, op_lb.get((n, m), T))
        rec = dict(n=n, m=m, status="unknown", trace=[])
        while T <= n:
            if cls == "op":
                st, edges, stats = feasible_alpha_le(n, T, m_exact=m, time_limit=tl, **opts)
                info = None
            else:
                st, info = solve_realizable(n, T, m_exact=m, time_limit=tl, **opts)
                edges = info.get("edges") if st == "SAT" else None
            rec["trace"].append([T, st, round(time.time() - t0, 1)])
            if st == "SAT":
                rec.update(status=("optimal" if rec["status"] != "timeout" else "range"), alpha=T, edges=[list(e) for e in edges])
                if info and "set" in info: rec["set"] = info["set"]
                break
            if st == "UNKNOWN":
                rec["alpha_ge"] = rec.get("alpha_ge", T)
                rec["status"] = "timeout"
            T += 1
        rec["time"] = round(time.time() - t0, 1)
        with open(out, "a") as f: f.write(json.dumps(rec) + "\n")
        print(n, m, rec["status"], rec.get("alpha"), rec["trace"], flush=True)
