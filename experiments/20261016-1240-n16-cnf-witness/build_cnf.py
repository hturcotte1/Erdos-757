"""CNF / CDCL (CaDiCaL) variant of experiments/20261016-0850-n16-deletion-cpsat/model16.py.

Base class O' encoding = e757.sat_indep.Encoding (linear, injective midpoints, K30, K31, alpha<=T eager,
cores v<=7 eager / v=8 lazy, F7 lazy, exactly m edges; GL colouring LR when m = n-2) + reflection lex-leader
+ deletion constraints (b),(c) of model16.add_deletion_constraints encoded with witness vectors.

Usage:
  python3 build_cnf.py enctest                      # the 145-case encoding test (no long run)
  python3 build_cnf.py solve N T M TAG [solver]     # CEGAR solve (CaDiCaL), writes result_TAG.json at the end
  python3 build_cnf.py stats N T M                  # variable / clause counts only
"""
import itertools, json, os, sys, time, random, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from e757 import sat_indep as SI


# ------------------------------------------------------------------ cardinality helpers (guarded)
def card_clauses(lits, bound, kind, top, guard=None):
    """CNF for  sum(lits) {<=,==} bound  (kind 'le'/'eq'), each clause extended by `guard` (a literal that,
    if true, switches the constraint off).  Returns (clauses, new_top)."""
    g = [] if guard is None else [guard]
    n = len(lits)
    if bound < 0:
        return [g[:]], top                      # impossible unless guard
    if kind == "le" and bound >= n:
        return [], top
    if kind == "eq" and bound > n:
        return [g[:]], top
    if bound == 0:
        return [[-l] + g for l in lits], top
    if kind == "eq" and bound == n:
        return [[l] + g for l in lits], top
    enc = CardEnc.atmost if kind == "le" else CardEnc.equals
    c = enc(lits=lits, bound=bound, top_id=top, encoding=EncType.seqcounter)
    return [list(cl) + g for cl in c.clauses], max(top, c.nv)


def vmin_of(n, T):
    return max(0, -((5 * (n - 1) - 17 * (n - 1 - T)) // 3))


def deletion_clauses(n, T, m, var, top, pair_mode="eq11", pair_const=None):
    """Deletion constraints (b),(c) of model16, total number of edges fixed to m.
    var: dict triple -> SAT variable.  Returns (clauses, top, witness_tables)."""
    tri = list(itertools.combinations(range(n), 3))
    cl = []
    vm = vmin_of(n, T)
    # m - deg p >= vmin
    for p in range(n):
        lits = [var[t] for t in tri if p in t]
        c, top = card_clauses(lits, m - vm, "le", top)
        cl += c

    def witness(avoid, guard_b=None):
        """s-vector; if guard_b given, zero/sum constraints hold when guard_b is true."""
        nonlocal top
        s = []
        for _ in range(n):
            top += 1
            s.append(top)
        off = [] if guard_b is None else [-guard_b]
        for v in avoid:
            cl.append([-s[v]] + off)
        c, top = card_clauses(s, T, "eq", top, guard=(None if guard_b is None else -guard_b))
        cl.extend(c)
        for t in tri:
            cl.append([-s[t[0]], -s[t[1]], -s[t[2]], -var[t]])
        return s

    sv = {p: witness([p]) for p in range(n)}
    sp, b = {}, {}
    for p, q in itertools.combinations(range(n), 2):
        top += 1
        bpq = top
        b[(p, q)] = bpq
        sp[(p, q)] = witness([p, q], guard_b=bpq)
        touch = [var[t] for t in tri if p in t or q in t]      # |edges meeting {p,q}| = deg p + deg q - eps_pq
        # mprime = m - touch
        if pair_mode == "eq11":
            c, top = card_clauses(touch, m - 11, "eq", top, guard=bpq)
        elif pair_mode == "ge9":
            c, top = card_clauses(touch, m - 9, "le", top, guard=bpq)
        elif pair_mode == "ge":
            c, top = card_clauses(touch, m - pair_const, "le", top, guard=bpq)
        elif pair_mode == "eq":
            c, top = card_clauses(touch, m - pair_const, "eq", top, guard=bpq)
        elif pair_mode == "none":
            c = []
        else:
            raise ValueError(pair_mode)
        cl += c
    return cl, top, (sv, sp, b)


def lex_clauses(n, var, top):
    """e-vector <=_lex reflected e-vector (same idea as cpsat_model._add_lex)."""
    tri = list(itertools.combinations(range(n), 3))
    refl = lambda t: (n - 1 - t[2], n - 1 - t[1], n - 1 - t[0])
    pairs, used = [], set()
    for t in tri:
        r = refl(t)
        if r == t or r in used:
            continue
        used.add(t)
        pairs.append((var[t], var[r]))
    cl = []
    eq_prev = None
    for idx, (a, b) in enumerate(pairs):
        pre = [] if eq_prev is None else [-eq_prev]
        cl.append(pre + [-a, b])                   # prefix equal -> a <= b
        if idx < len(pairs) - 1:
            top += 1
            eq = top
            cl.append(pre + [a, b, eq])
            cl.append(pre + [-a, -b, eq])
            eq_prev = eq
    return cl, top


def build(n, T, m, pair_mode="eq11", gl=None, symmetry=True):
    gl = ("LR" if m == n - 2 else False) if gl is None else gl
    enc = SI.Encoding(n, T, m, cores="hybrid", eager_max_v=7, forbid_f7=True, gl_constraints=gl)
    cl = list(enc.clauses)
    top = enc.nv_total
    c, top, tabs = deletion_clauses(n, T, m, enc.var, top, pair_mode)
    cl += c
    if symmetry:
        c, top = lex_clauses(n, enc.var, top)
        cl += c
    return enc, cl, top


# ------------------------------------------------------------------ CEGAR solve
def cegar_solve(n, T, m, tag, solver_name="cadical195", seed=0):
    from e757 import realizability as RZ
    t0 = time.time()
    enc, cl, top = build(n, T, m)
    logf = open(os.path.join(HERE, "solver_%s.log" % tag), "a")
    def log(s):
        logf.write("[%7.1fs] %s\n" % (time.time() - t0, s)); logf.flush()
    log("built: vars=%d clauses=%d lazy_cores=%d" % (top, len(cl), len(enc.lazy_cores)))
    res = {"n": n, "T": T, "m": m, "tag": tag, "solver": solver_name, "vars": top, "clauses": len(cl)}
    json.dump(dict(res, status="RUNNING"), open(os.path.join(HERE, "result_%s.json" % tag), "w"), indent=1)
    S = Solver(name=solver_name, bootstrap_with=cl)
    stats = {"iterations": 0, "lazy_nogoods": 0, "rz_nogoods": 0, "abstract_solutions": 0}
    rng = random.Random(seed)
    def finish(status, extra=None):
        res.update(status=status, wall_s=round(time.time() - t0, 1), stats=stats, **(extra or {}))
        json.dump(res, open(os.path.join(HERE, "result_%s.json" % tag), "w"), indent=1)
        log("FINAL " + status)
        print("DONE", tag, status, flush=True)
    while True:
        stats["iterations"] += 1
        r = S.solve()
        if not r:
            return finish("UNSAT")
        model = S.get_model()
        pos = set(l for l in model if 0 < l <= enc.nv)
        edges = sorted(t for t in enc.triples if enc.var[t] in pos)
        ng = SI._lazy_nogoods(enc, edges)
        if ng:
            for kind, c in ng:
                S.add_clause(c)
            stats["lazy_nogoods"] += len(ng)
            if stats["iterations"] % 10 == 1:
                log("iter %d lazy nogoods total %d" % (stats["iterations"], stats["lazy_nogoods"]))
            continue
        # abstract solution: check all constraints independently, then realizability
        stats["abstract_solutions"] += 1
        log("abstract solution %d: %s" % (stats["abstract_solutions"], edges))
        json.dump({"edges": edges}, open(os.path.join(HERE, "abstract_solution_%s_%d.json" % (tag, stats["abstract_solutions"])), "w"))
        ok, cert = RZ.order_feasible(n, edges)
        if ok is None:
            return finish("UNKNOWN_ORDER_INCONCLUSIVE", {"edges": edges})
        if not ok:
            core = RZ.iis(n, edges)
            S.add_clause([-enc.var[tuple(e)] for e in core]); stats["rz_nogoods"] += 1
            continue
        fr = RZ.forced_relations(n, edges)
        if fr["extra_ap"]:
            T3 = tuple(fr["extra_ap"][0])
            core = RZ.forbidden_core(n, edges, ("extra_ap", T3))
            S.add_clause([-enc.var[tuple(e)] for e in core] + [enc.var[T3]]); stats["rz_nogoods"] += 1
            continue
        if fr["diff"]:
            core = RZ.forbidden_core(n, edges, ("diff", tuple(fr["diff"][0])))
            S.add_clause([-enc.var[tuple(e)] for e in core]); stats["rz_nogoods"] += 1
            continue
        rr = RZ.realize_exact(n, edges)
        if rr[0]:
            setl = rr[1]
            json.dump({"set": setl, "edges": edges}, open(os.path.join(HERE, "RECORD_CANDIDATE_%s.json" % tag), "w"))
            p = subprocess.run([sys.executable, REPO + "/scripts/new_claim.py", "--slug", "n16-cnf-witness-" + tag,
                                "--set", ",".join(map(str, setl))], capture_output=True, text=True, cwd=REPO)
            return finish("SAT_REALIZABLE", {"set": setl, "edges": edges, "new_claim": (p.stdout + p.stderr)[-2000:]})
        return finish("SAT_ABSTRACT_ONLY", {"edges": edges, "note": "realize_exact failed: %r" % (rr[:2],)})


# ------------------------------------------------------------------ encoding test
def enctest():
    sys.path.insert(0, os.path.join(REPO, "experiments", "20261016-0850-n16-deletion-cpsat"))
    from model16 import check_conditions, build_model, cp_model
    from soundness import edges_of, abase
    def cnf_feasible(n, T, edges, mode, const):
        tri = list(itertools.combinations(range(n), 3))
        var = {t: i + 1 for i, t in enumerate(tri)}
        m = len(edges)
        cl, top, _ = deletion_clauses(n, T, m, var, len(tri), mode, const)
        Es = {tuple(e) for e in edges}
        cl = cl + [[var[t] if t in Es else -var[t]] for t in tri]
        s = Solver(name="cadical195", bootstrap_with=cl)
        r = s.solve(); s.delete()
        return r
    rows = []
    def compare(n, T, edges, mode, const):
        a = cnf_feasible(n, T, edges, mode, const)
        b, det = check_conditions(n, edges, T, mode, const)
        rows.append((n, T, mode, const, a, b))
        assert a == b, (n, T, mode, const, a, b, det)
        return a
    compare(14, 8, edges_of(abase), "ge9", None)
    rng = random.Random(5)
    pats = []
    for seed in range(12):
        mod = build_model(16, m_min=12 + seed % 3, m_max=14, forbid_f7="lazy", symmetry=False, monotone=True, medial=True)
        mod.add_eager_alpha(10 + seed % 2)
        for t in mod.tri:
            mod.model.AddHint(mod.e[t], rng.randint(0, 1))
        s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.random_seed = seed
        s.parameters.max_time_in_seconds = 60; s.parameters.randomize_search = True
        st = s.Solve(mod.model)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            pats.append([t for t in mod.tri if s.Value(mod.e[t])])
    print("patterns", len(pats))
    nsat = 0
    for P in pats:
        for T in (9, 10):
            for mode, const in (("eq11", None), ("ge", 9), ("ge", 10), ("eq", 11), ("eq", 12), ("none", None)):
                nsat += compare(16, T, P, mode, const)
    from collections import Counter
    br = Counter((r[1], r[2], r[3], r[4]) for r in rows)
    print("compared", len(rows), "all agree; feasible", nsat)
    json.dump({"compared": len(rows), "all_agree": True, "feasible": nsat, "infeasible": len(rows) - nsat,
               "patterns": len(pats), "breakdown": [[*k, v] for k, v in br.items()]},
              open(os.path.join(HERE, "encoding_test.json"), "w"), indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "enctest":
        enctest()
    elif cmd == "stats":
        n, T, m = map(int, sys.argv[2:5])
        t0 = time.time()
        enc, cl, top = build(n, T, m)
        print(json.dumps({"n": n, "T": T, "m": m, "vars": top, "clauses": len(cl), "lazy_cores": len(enc.lazy_cores),
                          "build_s": round(time.time() - t0, 1)}))
    elif cmd == "solve":
        n, T, m = map(int, sys.argv[2:5])
        cegar_solve(n, T, m, sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else "cadical195")
