"""Encoding test: fix the edge variables to a pattern; CP-SAT feasibility of constraints (b),(c) must equal check14."""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model14 import *
from soundness import edges_of, abase  # noqa (soundness re-runs and rewrites soundness.json; harmless)

def model_feasible(n, T, edges):
    mod = build_model(n, forbid_f7="none", symmetry=False)
    add_constraints(mod, T)
    Es = {tuple(e) for e in edges}
    for t in mod.tri:
        mod.model.Add(mod.e[t] == (1 if t in Es else 0))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 120
    st = s.Solve(mod.model)
    assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE), st
    return st != cp_model.INFEASIBLE

rows = []
def compare(n, T, edges):
    a = model_feasible(n, T, edges); b, det = check14(n, edges, T)
    rows.append((n, T, a, b)); assert a == b, (n, T, a, b, det); return a
pats = [edges_of(abase)]
rng = random.Random(11)
for seed in range(24):
    m = 9 + seed % 4
    mod = build_model(14, m_exact=m, forbid_f7="lazy", symmetry=False, monotone=True, medial=True)
    mod.add_eager_alpha(8 + seed % 3)
    for t in mod.tri: mod.model.AddHint(mod.e[t], rng.randint(0, 1))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 40; s.parameters.randomize_search = True
    st = s.Solve(mod.model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        pats.append([t for t in mod.tri if s.Value(mod.e[t])])
print("patterns", len(pats), flush=True)
for P in pats:
    for T in (7, 8, 9):
        compare(14, T, P)
from collections import Counter
cnt = Counter((r[1], r[2]) for r in rows)
print("compared", len(rows), "all agree", dict(cnt))
json.dump({"compared": len(rows), "all_agree": True, "breakdown": [[T, feas, c] for (T, feas), c in cnt.items()],
           "patterns": len(pats), "note": "breakdown rows are [T, model_feasible, count]"},
          open(os.path.join(HERE, "encoding_test.json"), "w"), indent=1)
