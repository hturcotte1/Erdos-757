"""CP-SAT model for the abstract (n=14, alpha<=8) question with Henning-Yeo / K48 deletion constraints.

Usage:
  python3 model14.py solve M TIME_S WORKERS TAG        (n=14, T=8, m exactly M; M=11 is Q11, M=12 is the sanity cell)
Constraints added to the class-O' model (see README for derivations):
 (a) alpha(C) = 8 (eager: every 9-set contains an edge; witness: some independent 8-set)  -- implied by (b)
 (b) for each p: independent T-set avoiding p; m - deg p >= vmin (HY on C-p, tau = n-1-T)
 (c) for each pair p<q: independent T-set avoiding p and q   (K48/L006 for m=11; K47 census for m=12)
"""
import itertools, json, os, subprocess, sys, time, random, re

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, REPO)
from ortools.sat.python import cp_model
from e757.cpsat_model import build_model, load_cores, _cegar_step, _learn_core
from e757 import realizability as RZ

HERE = os.path.dirname(os.path.abspath(__file__))


def vmin_of(n, T):
    """HY on n-1 vertices with tau = n-1-T: 17(n-1-T) <= 5(n-1) + 3 m'  =>  m' >= vmin."""
    return max(0, -((5 * (n - 1) - 17 * (n - 1 - T)) // 3))


def add_constraints(mod, T, pairs=True):
    n, M, tri, e = mod.n, mod.model, mod.tri, mod.e
    deg = [sum(e[t] for t in tri if p in t) for p in range(n)]
    vm = vmin_of(n, T)
    for p in range(n):
        M.Add(mod.total - deg[p] >= vm)

    def witness(name, avoid):
        s = [M.NewBoolVar("%s_%d" % (name, v)) for v in range(n)]
        for v in avoid:
            M.Add(s[v] == 0)
        M.Add(sum(s) == T)
        for t in tri:
            M.AddBoolOr([s[t[0]].Not(), s[t[1]].Not(), s[t[2]].Not(), e[t].Not()])
        return s
    mod.sv = {p: witness("sv%d" % p, [p]) for p in range(n)}
    mod.sp = {}
    if pairs:
        for p, q in itertools.combinations(range(n), 2):
            mod.sp[(p, q)] = witness("sp%d_%d" % (p, q), [p, q])


# --------------------------------------------------------------- direct (solver-free) evaluation of the same constraints
def indep_exists(n, edges, size, avoid):
    verts = [v for v in range(n) if v not in avoid]
    by_last = {}
    for (i, j, k) in edges:
        by_last.setdefault(max(i, j, k), []).append((1 << i) | (1 << j) | (1 << k))
    found = [False]

    def rec(idx, chosen, sz):
        if found[0]:
            return
        if sz == size:
            found[0] = True
            return
        if sz + (len(verts) - idx) < size or idx == len(verts):
            return
        v = verts[idx]
        c2 = chosen | (1 << v)
        if all((m & c2) != m for m in by_last.get(v, [])):
            rec(idx + 1, c2, sz + 1)
        rec(idx + 1, chosen, sz)
    rec(0, 0, 0)
    return found[0]


def check14(n, edges, T, pairs=True):
    E = [tuple(x) for x in edges]
    m = len(E)
    deg = [sum(1 for t in E if p in t) for p in range(n)]
    vm = vmin_of(n, T)
    det = {"deg_viol": [p for p in range(n) if m - deg[p] < vm],
           "vertex_viol": [p for p in range(n) if not indep_exists(n, E, T, {p})],
           "pair_viol": []}
    if pairs:
        det["pair_viol"] = [(p, q) for p, q in itertools.combinations(range(n), 2) if not indep_exists(n, E, T, {p, q})]
    return (not det["deg_viol"] and not det["vertex_viol"] and not det["pair_viol"]), det


# --------------------------------------------------------------- solving
def solve(m, time_limit, workers, tag, n=14, T=8, seed=0):
    t0 = time.time()
    rng = random.Random(seed)
    cores = load_cores(REPO + "/data/forbidden_ordered_n7.json", REPO + "/data/forbidden_ordered_n8.json")
    mod = build_model(n, m_exact=m, forbid_f7="lazy", monotone=True, medial=True, cores=cores, core_lit_budget=2_000_000)
    mod.add_eager_alpha(T)
    add_constraints(mod, T)
    logf = open(os.path.join(HERE, "solver_%s.log" % tag), "a")

    def log(msg):
        logf.write(msg if msg.endswith("\n") else msg + "\n"); logf.flush()
    log("# model built in %.1fs; constraints %s; n=%d T=%d m=%d" % (time.time() - t0, mod.constraint_counts, n, T, m))
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "rounds": 0, "learnt": 0, "fail_kinds": {}}
    res = {"n": n, "T": T, "m": m, "workers": workers, "tag": tag, "time_limit": time_limit,
           "model_built_s": round(time.time() - t0, 1), "num_vars_hint": len(mod.model.Proto().variables),
           "num_constraints": len(mod.model.Proto().constraints)}

    def finish(status, extra=None):
        res.update(status=status, wall_s=round(time.time() - t0, 1), stats=stats, **(extra or {}))
        json.dump(res, open(os.path.join(HERE, "result_%s.json" % tag), "w"), indent=1)
        log("# FINAL " + status)
        print("DONE", tag, status, res["wall_s"], flush=True)
    keep = re.compile(r"^(#\d|#Bound|#Done|#Model|Starting|Search stats|CpSolverResponse|status|best_bound|objective|walltime|#Boolean|\s*\d+ (full|first))")
    while True:
        left = time_limit - (time.time() - t0)
        if left <= 1:
            return finish("UNKNOWN")
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = left
        s.parameters.num_workers = workers
        s.parameters.random_seed = seed + stats["solves"]
        s.parameters.log_search_progress = True
        s.parameters.log_to_stdout = False
        s.log_callback = lambda msg: (log(msg) if keep.match(msg) else None)
        st = s.Solve(mod.model)
        stats["solves"] += 1
        res["last_cpsat_status"] = s.StatusName(st)
        if st == cp_model.INFEASIBLE:
            return finish("INFEASIBLE")
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return finish("UNKNOWN")
        edges = [t for t in mod.tri if s.Value(mod.e[t])]
        kind, a = _cegar_step(mod, edges, T, rng, 40, stats)
        if kind == "cut":
            continue
        stats["rounds"] += 1
        log("# abstract solution round %d: edges=%s" % (stats["rounds"], edges))
        json.dump({"edges": edges}, open(os.path.join(HERE, "abstract_solution_%s_%d.json" % (tag, stats["rounds"])), "w"))
        ok, cert = RZ.order_feasible(n, edges)
        if ok is None:
            return finish("UNKNOWN", {"note": "order_feasible inconclusive", "edges": edges})
        if not ok:
            S, Tx, fk = RZ.iis(n, edges), None, "order"
        else:
            fr = RZ.forced_relations(n, edges)
            if fr["extra_ap"]:
                S, Tx, fk = RZ.forbidden_core(n, edges, ("extra_ap", fr["extra_ap"][0])), tuple(fr["extra_ap"][0]), "extra_ap"
            elif fr["diff"]:
                S, Tx, fk = RZ.forbidden_core(n, edges, ("diff", tuple(fr["diff"][0]))), None, "diff"
            else:
                r = RZ.realize_exact(n, edges)
                if r[0]:
                    setl = r[1]
                    json.dump({"set": setl, "edges": edges}, open(os.path.join(HERE, "CANDIDATE.json"), "w"))
                    p = subprocess.run([sys.executable, REPO + "/scripts/new_claim.py", "--slug", "n14m%d-deletion-cpsat" % m,
                                        "--set", ",".join(map(str, setl))], capture_output=True, text=True, cwd=REPO)
                    return finish("SAT_REALIZABLE", {"set": setl, "edges": edges, "new_claim": (p.stdout + p.stderr)[-2000:]})
                return finish("SAT_ABSTRACT_ONLY", {"edges": edges, "note": "realize_exact failed: %r" % (r[:2],)})
        stats["fail_kinds"][fk] = stats["fail_kinds"].get(fk, 0) + 1
        stats["learnt"] += _learn_core(mod, S, Tx)
        log("# learnt core kind=%s total learnt=%d" % (fk, stats["learnt"]))


if __name__ == "__main__":
    if sys.argv[1] == "solve":
        solve(int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
