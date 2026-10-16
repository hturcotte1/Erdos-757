"""Referee round 3: enumerate ALL saturated models (mode 'sat') of the CNF in sat_model.py; one fresh solver per
cube (triple at midpoint c1, triple at midpoint c2).  Saturated: each midpoint has exactly one triple, so the cubes
partition the model set, and blocking by positive literals is exact.
Usage: python3 sat_enum_cubes2.py n T c1 c2 solver idx out.txt.gz   (idx = index of the c1 triple)"""
import sys, gzip, time
from pysat.solvers import Solver
from sat_model import build

n, T, c1, c2, sname, idx, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), sys.argv[7]
triples, var, nv, clauses, bymid, aux = build(n, T, 'sat')
ntr = len(triples)
t1 = bymid[c1][idx]
t0 = time.time(); total = 0; per = []
with gzip.open(out, 'wt') as fo:
    for t2 in bymid[c2]:
        cnt = 0
        with Solver(name=sname, bootstrap_with=clauses) as S:
            S.add_clause([var[t1]]); S.add_clause([var[t2]])
            while S.solve():
                model = S.get_model()
                pos = sorted(triples[v - 1] for v in model if 0 < v <= ntr)
                assert len(pos) == n - 2 and t1 in pos and t2 in pos
                fo.write(' '.join('%d,%d,%d' % t for t in pos) + '\n')
                S.add_clause([-var[t] for t in pos])
                cnt += 1
        per.append(cnt); total += cnt
print('split %s: per-%d-cube=%s models=%d time=%.1f' % (t1, c2, per, total, time.time() - t0), flush=True)
