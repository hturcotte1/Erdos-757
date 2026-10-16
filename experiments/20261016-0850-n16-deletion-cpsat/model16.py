"""CP-SAT model for the abstract n=16 (alpha<=9) question with Henning-Yeo deletion constraints.

Usage:
  python3 model16.py solve N T M_MIN M_MAX TIME_S WORKERS TAG [pair_mode]
     pair_mode: 'eq11' (n=16 default: NOT b_pq => m - deg p - deg q + eps == 11) or 'ge9' (n=14 test)
  python3 model16.py checks    (direct, solver-free soundness checks; see README)

Implied constraints for the AP hypergraph H of an n-point (4,5)-set C with h(C)=T=f(n-1)... (see README):
 (b) for every p: an independent T-set avoids p;   deg p <= m - T
 (c) for every pair p<q: b_pq => independent T-set avoids p,q;  NOT b_pq => m(C-p-q) = const / >= const.
"""
import itertools, json, os, subprocess, sys, time, random

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, REPO)
from ortools.sat.python import cp_model
from e757.cpsat_model import (build_model, load_cores, _cegar_step, _learn_core, independent_sets)
from e757 import realizability as RZ

HERE = os.path.dirname(os.path.abspath(__file__))


def add_deletion_constraints(mod, T, pair_mode="eq11", pair_const=None):
    """Add (b), (c) to a cpsat_model.Model.  Returns dict of variable tables."""
    n, M = mod.n, mod.model
    tri = mod.tri
    e = mod.e
    deg = [sum(e[t] for t in tri if p in t) for p in range(n)]
    total = mod.total
    vmin = max(0, -((5 * (n - 1) - 17 * (n - 1 - T)) // 3))   # HY on n-1 vertices, tau=n-1-T: m' >= vmin
    mod.vmin = vmin
    for p in range(n):
        M.Add(total - deg[p] >= vmin)         # n=16,T=9: vmin=9 (Lemma Delta); n=14,T=8: vmin=7
    # witness vectors
    def witness(name, avoid, cond=None):
        s = [M.NewBoolVar("%s_%d" % (name, v)) for v in range(n)]
        for v in avoid:
            M.Add(s[v] == 0) if cond is None else M.Add(s[v] == 0).OnlyEnforceIf(cond)
        if cond is None:
            M.Add(sum(s) == T)
        else:
            M.Add(sum(s) == T).OnlyEnforceIf(cond)
        for t in tri:
            M.AddBoolOr([s[t[0]].Not(), s[t[1]].Not(), s[t[2]].Not(), e[t].Not()])
        return s
    sv = {p: witness("sv%d" % p, [p]) for p in range(n)}
    sp, b = {}, {}
    for p, q in itertools.combinations(range(n), 2):
        bpq = M.NewBoolVar("b_%d_%d" % (p, q))
        b[(p, q)] = bpq
        sp[(p, q)] = witness("sp%d_%d" % (p, q), [p, q], cond=bpq)
        eps = sum(e[t] for t in tri if p in t and q in t)
        mprime = total - deg[p] - deg[q] + eps
        if pair_mode == "eq11":
            M.Add(mprime == 11).OnlyEnforceIf(bpq.Not())
        elif pair_mode == "ge9":
            M.Add(mprime >= 9).OnlyEnforceIf(bpq.Not())
        elif pair_mode == "ge":
            M.Add(mprime >= pair_const).OnlyEnforceIf(bpq.Not())
        elif pair_mode == "eq":
            M.Add(mprime == pair_const).OnlyEnforceIf(bpq.Not())
        elif pair_mode == "none":
            pass
        else:
            raise ValueError(pair_mode)
    mod.sv, mod.sp, mod.b = sv, sp, b
    return sv, sp, b


# ---------------------------------------------------------------- direct (solver-free) checks of the conditions
def indep_exists(n, edges, size, avoid):
    """Is there an independent (edge-free) set of exactly `size` vertices avoiding `avoid`?  (exact DFS)"""
    verts = [v for v in range(n) if v not in avoid]
    emask = [(1 << i) | (1 << j) | (1 << k) for i, j, k in edges]
    by_last = {}
    for (i, j, k), m in zip(edges, emask):
        by_last.setdefault(max(i, j, k), []).append(m)
    best = [False]

    def rec(idx, chosen, sz):
        if best[0]:
            return
        if sz == size:
            best[0] = True
            return
        if sz + (len(verts) - idx) < size:
            return
        if idx == len(verts):
            return
        v = verts[idx]
        c2 = chosen | (1 << v)
        if all((m & c2) != m for m in by_last.get(v, [])):
            rec(idx + 1, c2, sz + 1)
        rec(idx + 1, chosen, sz)
    rec(0, 0, 0)
    return best[0]


def check_conditions(n, edges, T, pair_mode, pair_const=None):
    """Evaluate (b),(c) directly on a pattern.  Returns (ok, details)."""
    E = [tuple(x) for x in edges]
    m = len(E)
    deg = [sum(1 for t in E if p in t) for p in range(n)]
    det = {"deg_bound_viol": [], "vertex_viol": [], "pair_viol": [], "npairs_witness": 0, "npairs_via_m": 0,
           "mprime_when_no_witness": []}
    for p in range(n):
        if m - deg[p] < max(0, -((5 * (n - 1) - 17 * (n - 1 - T)) // 3)):
            det["deg_bound_viol"].append(p)
        if not indep_exists(n, E, T, {p}):
            det["vertex_viol"].append(p)
    for p, q in itertools.combinations(range(n), 2):
        if indep_exists(n, E, T, {p, q}):
            det["npairs_witness"] += 1
            continue
        eps = sum(1 for t in E if p in t and q in t)
        mp = m - deg[p] - deg[q] + eps
        det["mprime_when_no_witness"].append(mp)
        good = {"eq11": mp == 11, "ge9": mp >= 9, "ge": pair_const is not None and mp >= pair_const,
                "eq": mp == pair_const, "none": True}[pair_mode]
        if good:
            det["npairs_via_m"] += 1
        else:
            det["pair_viol"].append((p, q, mp))
    ok = not det["deg_bound_viol"] and not det["vertex_viol"] and not det["pair_viol"]
    return ok, det


# ---------------------------------------------------------------- solving
def solve(n, T, m_min, m_max, time_limit, workers, tag, pair_mode, seed=0, log_every=300):
    t0 = time.time()
    rng = random.Random(seed)
    cores = load_cores(REPO + "/data/forbidden_ordered_n7.json", REPO + "/data/forbidden_ordered_n8.json")
    mod = build_model(n, m_min=m_min, m_max=m_max, forbid_f7="lazy", monotone=True, medial=True,
                      cores=cores, core_lit_budget=1_000_000)
    mod.add_eager_alpha(T)
    add_deletion_constraints(mod, T, pair_mode)
    logf = open(os.path.join(HERE, "solver_%s.log" % tag), "a")
    def log(msg):
        logf.write(msg if msg.endswith("\n") else msg + "\n"); logf.flush()
    log("# model built in %.1fs; constraints %s" % (time.time() - t0, mod.constraint_counts))
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0, "rounds": 0, "learnt": 0, "fail_kinds": {}}
    res = {"n": n, "T": T, "m_min": m_min, "m_max": m_max, "pair_mode": pair_mode, "workers": workers,
           "tag": tag, "time_limit": time_limit, "model_built_s": round(time.time() - t0, 1)}
    def finish(status, extra=None):
        res.update(status=status, wall_s=round(time.time() - t0, 1), stats=stats, **(extra or {}))
        json.dump(res, open(os.path.join(HERE, "result_%s.json" % tag), "w"), indent=1)
        log("# FINAL " + status)
        print("DONE", tag, status, res["wall_s"], flush=True)
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
        import re as _re
        keep = _re.compile(r"^(#\d|#Bound|#Done|#Model|Starting|Search stats|CpSolverResponse|status|best_bound|objective|walltime|#Boolean|\s*\d+ (full|first))")
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
                    json.dump({"set": setl, "edges": edges}, open(os.path.join(HERE, "RECORD_CANDIDATE.json"), "w"))
                    p = subprocess.run([sys.executable, REPO + "/scripts/new_claim.py", "--slug", "n16-deletion-cpsat",
                                        "--set", ",".join(map(str, setl))], capture_output=True, text=True, cwd=REPO)
                    return finish("SAT_REALIZABLE", {"set": setl, "edges": edges, "new_claim": (p.stdout + p.stderr)[-2000:]})
                return finish("SAT_ABSTRACT_ONLY", {"edges": edges, "note": "realize_exact failed: %r" % (r[:2],)})
        stats["fail_kinds"][fk] = stats["fail_kinds"].get(fk, 0) + 1
        stats["learnt"] += _learn_core(mod, S, Tx)
        log("# learnt core kind=%s total learnt=%d" % (fk, stats["learnt"]))


if __name__ == "__main__":
    if sys.argv[1] == "solve":
        n, T, mmin, mmax = map(int, sys.argv[2:6])
        solve(n, T, mmin, mmax, float(sys.argv[6]), int(sys.argv[7]), sys.argv[8],
              sys.argv[9] if len(sys.argv) > 9 else "eq11")
