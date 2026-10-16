"""Full-CNF sanity check at n=14,T=8,m=12 (pair mode ge9): A_base and its reflection; one of them must satisfy the CNF (lex), and a
non-example (A_base with one edge removed->m=11 mismatch) must not. Also test incremental add_clause after solve for cadical195."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261016-0850-n16-deletion-cpsat"))
from build_cnf import *
from soundness import edges_of, abase
n, T, m = 14, 8, 12
E = [tuple(e) for e in edges_of(abase)]
R = sorted((n-1-k, n-1-j, n-1-i) for i, j, k in E)
enc, cl, top = build(n, T, m, pair_mode="ge9")
out = {}
for name, P in (("abase", E), ("reflected", R)):
    s = Solver(name="cadical195", bootstrap_with=cl)
    asm = [enc.var[t] if t in set(P) else -enc.var[t] for t in enc.triples]
    out[name] = bool(s.solve(assumptions=asm))
    s.delete()
print(out)
# incremental
s = Solver(name="cadical195", bootstrap_with=cl)
r1 = s.solve(); s.add_clause([-l for l in [enc.var[t] for t in enc.triples if enc.var[t] in set(x for x in s.get_model() if x > 0)]]); r2 = s.solve()
print("incremental ok", r1, r2)
out["incremental"] = [r1, r2]
out["vars"], out["clauses"] = top, len(cl)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fullcheck.json"), "w"))
