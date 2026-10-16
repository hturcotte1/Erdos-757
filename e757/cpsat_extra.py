"""CP-SAT wrapper: class O' feasibility (n, T, m) with the optional empirical invariants of
e757.sat_indep (`extra` dict, same keys).  Does not modify e757/cpsat_model.py.

The invariants are reflection symmetric, so the lex-leader symmetry breaking of cpsat_model stays sound.
An UNSAT answer is conditional on `extra` (they are empirical, not proved).
"""
import random
import time

from ortools.sat.python import cp_model

from . import cpsat_model as cm


def add_extra(mod, extra):
    n, M, e = mod.n, mod.model, mod.e
    through = {v: [e[t] for t in mod.tri if v in t] for v in range(n)}
    deg = {v: sum(through[v]) for v in range(n)}
    if not extra:
        return
    if "maxdeg" in extra:
        for v in range(n):
            M.Add(deg[v] <= extra["maxdeg"])
    for key, vs in (("deg_ends", (0, n - 1)), ("deg_near_ends", (1, n - 2))):
        if key in extra:
            lo, hi = extra[key]
            for v in vs:
                M.Add(deg[v] <= hi)
                M.Add(deg[v] >= lo)
    if "ends_sum_min" in extra:
        M.Add(deg[0] + deg[n - 1] >= extra["ends_sum_min"])
    if "n_deg1_max" in extra:
        u = {v: M.NewBoolVar("u%d" % v) for v in range(n)}
        for v in range(n):
            M.Add(deg[v] + u[v] >= 2)       # saturated: deg >= 1 always, so u_v=1 iff deg 1 is allowed
        M.Add(sum(u.values()) <= extra["n_deg1_max"])


def feasible(n, T, m, extra=None, time_limit=3600, workers=4, seed=0, ncuts_per_iter=40, cores=True, log=None):
    """('SAT'|'UNSAT'|'UNKNOWN', edges, stats) for class O' (K30, K31, cores with <=4 edges, F7-free, alpha<=T)."""
    t0 = time.time()
    rng = random.Random(seed)
    mods = {}
    if cores:
        mods["cores"] = cm.load_cores("data/forbidden_ordered_n7.json", "data/forbidden_ordered_n8.json")
        mods["core_max_edges"] = 4
    mod = cm.build_model(n, m_exact=m, forbid_f7="lazy", monotone=True, medial=True, **mods)
    add_extra(mod, extra)
    mod.add_eager_alpha(T)
    stats = {"alpha_cuts": 0, "f7_cuts": 0, "solves": 0}
    while True:
        left = time_limit - (time.time() - t0)
        if left <= 0:
            stats["time"] = round(time.time() - t0, 1)
            return "UNKNOWN", None, stats
        r, edges = cm._solve(mod, left, workers=workers, seed=seed)
        stats["solves"] += 1
        if r != "SAT":
            stats["time"] = round(time.time() - t0, 1)
            return r, None, stats
        kind, a = cm._cegar_step(mod, edges, T, rng, ncuts_per_iter, stats)
        if log:
            log("solve %d: %s" % (stats["solves"], kind))
        if kind == "ok":
            stats["time"] = round(time.time() - t0, 1)
            return "SAT", edges, stats
