"""Referee round 3: single satisfiability decision of the CNF in sat_model.py.
Usage: python3 sat_decide.py n T mode [solver] [empty_j]
  empty_j (optional, mode nonsat): additionally force midpoint empty_j to be empty (case split)."""
import sys, time
from pysat.solvers import Solver
from sat_model import build

n, T, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
sname = sys.argv[4] if len(sys.argv) > 4 else 'cd15'
ej = int(sys.argv[5]) if len(sys.argv) > 5 else None
triples, var, nv, clauses, bymid, aux = build(n, T, mode)
t0 = time.time()
with Solver(name=sname, bootstrap_with=clauses) as S:
    assum = [aux[ej]] if ej is not None else []
    r = S.solve(assumptions=assum)
    st = S.accum_stats()
    out = 'n=%d T=%d mode=%s empty_j=%s solver=%s result=%s time=%.1f stats=%s' % (n, T, mode, ej, sname, 'SAT' if r else 'UNSAT', time.time() - t0, st)
    if r:
        m = S.get_model()
        out += ' model=' + ' '.join('%d,%d,%d' % triples[v - 1] for v in m if 0 < v <= len(triples))
    print(out, flush=True)
