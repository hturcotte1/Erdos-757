"""Referee round 3: enumerate ALL saturated models (mode 'sat') of the CNF in sat_model.py, split into cubes:
outer loop = triple at midpoint c1 (fresh solver per value), inner loop = triple at midpoint c2 (assumptions).
Saturated: every midpoint has exactly one triple, so the cubes partition the model set and positive-literal
blocking is exact.  Usage: python3 sat_enum_cubes.py n T c1 c2 out.txt.gz [solver] [only_k1]"""
import sys, gzip, time
from pysat.solvers import Solver
from sat_model import build

n, T, c1, c2, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
sname = sys.argv[6] if len(sys.argv) > 6 else 'g4'
only = int(sys.argv[7]) if len(sys.argv) > 7 else None
triples, var, nv, clauses, bymid, aux = build(n, T, 'sat')
ntr = len(triples)
t0 = time.time(); total = 0
with gzip.open(out, 'wt') as fo:
    for idx1, t1 in enumerate(bymid[c1]):
        if only is not None and idx1 != only:
            continue
        cnt1 = 0; ts = time.time()
        with Solver(name=sname, bootstrap_with=clauses) as S:
            S.add_clause([var[t1]])
            for t2 in bymid[c2]:
                while S.solve(assumptions=[var[t2]]):
                    model = S.get_model()
                    pos = sorted(triples[v - 1] for v in model if 0 < v <= ntr)
                    fo.write(' '.join('%d,%d,%d' % t for t in pos) + '\n')
                    S.add_clause([-var[t] for t in pos])
                    cnt1 += 1
        total += cnt1
        print('cube %s: models=%d time=%.1f' % (t1, cnt1, time.time() - ts), flush=True)
print('n=%d T=%d c1=%d c2=%d total_models=%d time=%.1f' % (n, T, c1, c2, total, time.time() - t0), flush=True)
