"""Encoding test: fix the edge variables of the CP-SAT model to a given pattern and compare feasibility of
(b)+(c) constraints with the direct computation check_conditions.  Several (T, pair-mode) settings and random
16-vertex class-O patterns (from the plain model), plus A_base at n=14."""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model16 import *
from soundness import edges_of, abase

def model_feasible(n, T, edges, mode, const):
    mod = build_model(n, forbid_f7="none", symmetry=False)
    add_deletion_constraints(mod, T, mode, const)
    Es = {tuple(e) for e in edges}
    for t in mod.tri:
        mod.model.Add(mod.e[t] == (1 if t in Es else 0))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 60
    st = s.Solve(mod.model)
    assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE), st
    return st != cp_model.INFEASIBLE

def vmin(n, T): return max(0, -((5 * (n - 1) - 17 * (n - 1 - T)) // 3))

rows = []
def compare(n, T, edges, mode, const):
    a = model_feasible(n, T, edges, mode, const)
    b, det = check_conditions(n, edges, T, mode, const)
    rows.append((n, T, mode, const, a, b))
    assert a == b, (n, T, mode, const, a, b, det)
    return a

compare(14, 8, edges_of(abase), "ge9", None)
# random 16-vertex patterns: alpha<=10 hypergraphs from the plain model with random seeds
rng = random.Random(5)
pats = []
for seed in range(12):
    mod = build_model(16, m_min=12 + seed % 3, m_max=14, forbid_f7="lazy", symmetry=False, monotone=True, medial=True)
    mod.add_eager_alpha(10 + seed % 2)
    # random hint/objective to diversify
    for t in mod.tri:
        mod.model.AddHint(mod.e[t], rng.randint(0, 1))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.random_seed = seed; s.parameters.max_time_in_seconds = 60
    s.parameters.randomize_search = True
    st = s.Solve(mod.model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        pats.append([t for t in mod.tri if s.Value(mod.e[t])])
print("patterns", len(pats))
nsat = 0
for P in pats:
    m = len(P)
    for T in (9, 10):
        for mode, const in (("eq11", None), ("ge", 9), ("ge", 10), ("eq", 11), ("eq", 12), ("none", None)):
            nsat += compare(16, T, P, mode, const)
print("compared", len(rows), "all agree; feasible cases:", nsat)
# distribution of the feasible/infeasible combos
from collections import Counter
print(Counter((r[1], r[2], r[3], r[4]) for r in rows))
json.dump({"compared": len(rows), "feasible": nsat, "all_agree": True,
           "breakdown": [[*k, v] for k, v in Counter((r[1], r[2], r[3], r[4]) for r in rows).items()]},
          open(os.path.join(HERE, "encoding_test.json"), "w"), indent=1)
