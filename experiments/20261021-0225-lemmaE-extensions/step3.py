"""Build Lemma-E extensions of S_K, verify exactly, compute h by DP + CP-SAT + direct SAT; test universality again."""
import json, sys, time, itertools
from collections import defaultdict
from lib import *

def extend(A, pairs):
    new = list(A)
    for a, t in pairs:
        new += [a - t, a + t]
    s = min(new)
    return sorted(v - s for v in new)   # translation only

def rel_sets(A):
    by = defaultdict(list)
    for i, a in enumerate(A):
        for b in A[i:]:
            by[a + b].append((a, b))
    rels = set()
    for s, ps in by.items():
        for p, q in itertools.combinations(ps, 2):
            rels.add(frozenset(p) | frozenset(q))
    return rels

def cpsat_alpha(A, edges, tlim=600):
    from ortools.sat.python import cp_model
    idx = {v: i for i, v in enumerate(A)}
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(A))]
    for e in edges: m.Add(sum(x[idx[v]] for v in e) <= 2)
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlim; s.parameters.num_workers = 2
    r = s.Solve(m)
    return s.StatusName(r), int(round(s.ObjectiveValue())), int(round(s.BestObjectiveBound())), round(s.WallTime(), 1)

def analyse(name, K, pairs_spec, do_sat=True, do_cp=True):
    A0, copies = family(K)
    span = max(A0) - min(A0)
    pairs = []
    for side, t in pairs_spec:
        pairs.append((min(A0) if side == "min" else max(A0), t))
    t0 = time.time()
    B = extend(A0, pairs)
    n = len(B)
    assert len(set(B)) == n
    ok, cnt, mn = own_45(B)
    r = dict(name=name, K=K, base_n=len(A0), base_h=7 + 5 * K, pairs=[(s, t) for s, t in pairs_spec], n=n,
             own_4subset_ok=ok, n4=cnt, min_distinct_diffs=mn, e757_is_45=bool(core.is_45_set(B)))
    E = aps(B)
    r["m_aps"] = len(E); r["m_aps_e757"] = len(core.ap_edges(B)); r["expected_m"] = len(aps(A0)) + len(pairs)
    # group: original points via copies (shifted), new points group 0
    shift = min(min(A0) - 0, 0)
    s0 = min([min(A0)] + [a - t for a, t in pairs])
    Aset_shift = {v - s0: v for v in A0}
    g = {}
    for v in B:
        if v in Aset_shift:
            g[v] = min(j for j, cp in enumerate(copies) if Aset_shift[v] in cp)
        else:
            g[v] = 0
    h, mf = alpha_dp(B, g)
    r.update(h_dp=h, maxfront=mf, expected_h=7 + 5 * K + len(pairs), ratio=f"{h}/{n}", beats_4_7=(7 * h < 4 * n), twice_h_check=None)
    if do_cp:
        r["cpsat_plain"] = cpsat_alpha(B, E)
    if do_sat:
        from pysat.card import CardEnc, EncType
        from pysat.solvers import Cadical153
        rels = rel_sets(B)
        idx = {v: i + 1 for i, v in enumerate(B)}
        cl = [[-idx[v] for v in sorted(rr)] for rr in rels]
        outs = {}
        for k in (h, h + 1):
            card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.totalizer)
            sv = Cadical153(bootstrap_with=cl + card.clauses); res = sv.solve()
            if res:
                mod = sv.get_model(); wit = [B[i] for i in range(n) if mod[i] > 0]
                assert cf.is_sidon_def(wit) and len(wit) >= k
            sv.delete(); outs[k] = res
        r["sat_ge_h"] = outs[h]; r["sat_ge_h_plus_1"] = outs[h + 1]
    # universality of each vertex
    uni = [v for v in B if alpha_dp(B, g, [v])[0] == h - 1]
    r["universal_vertices"] = [B.index(v) for v in uni]
    r["extremes"] = [B.index(min(B)), B.index(max(B))]
    r["min_universal"] = min(B) in uni; r["max_universal"] = max(B) in uni
    r["sec"] = round(time.time() - t0, 1)
    json.dump(B, open(f"set_{name}.json", "w"))
    print(json.dumps(r, default=str), flush=True)
    return r

if __name__ == "__main__":
    which = sys.argv[1:]
    out = {}
    for K in (3, 4, 5, 6):
        A0, _ = family(K); span = max(A0) - min(A0)
        t1 = 3 * span + 1000003; t2 = 5 * span + 7000027
        specs = {f"E1_K{K}": [("min", t1)], f"E2_K{K}": [("max", t2)], f"E12_K{K}": [("min", t1), ("max", t2)]}
        for nm, sp in specs.items():
            out[nm] = analyse(nm, K, sp)
            json.dump(out, open("step3_results.json", "w"), indent=1, default=str)
