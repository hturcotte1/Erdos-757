"""Referee round 3: decide the CNF of sat_model.py by cube-and-conquer.
Cubes = joint choice at midpoints c1, c2 (each: one of its triples, or 'empty'); the cubes partition the space
(midpoints are at most one triple each), so all cubes UNSAT <=> formula UNSAT.  One incremental solver.
Usage: python3 sat_cubes.py n T mode c1 c2 [solver]"""
import sys, time
from pysat.solvers import Solver
from sat_model import build

n, T, mode, c1, c2 = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
sname = sys.argv[6] if len(sys.argv) > 6 else 'cd15'
triples, var, nv, clauses, bymid, aux = build(n, T, mode)
opts1 = [var[t] for t in bymid[c1]] + [None]
opts2 = [var[t] for t in bymid[c2]] + [None]
t0 = time.time(); nsat = 0; ncube = 0
with Solver(name=sname, bootstrap_with=clauses) as S:
    for a in opts1:
        for b in opts2:
            ass = []
            ass += [a] if a else [-var[t] for t in bymid[c1]]
            ass += [b] if b else [-var[t] for t in bymid[c2]]
            t1 = time.time()
            r = S.solve(assumptions=ass)
            ncube += 1
            if r:
                nsat += 1
                m = S.get_model()
                print('SAT cube', a, b, 'model', ' '.join('%d,%d,%d' % triples[v - 1] for v in m if 0 < v <= len(triples)), flush=True)
            if time.time() - t1 > 20:
                print('slow cube %s %s %.1fs' % (a, b, time.time() - t1), flush=True)
print('n=%d T=%d mode=%s cubes=%d (midpoints %d,%d) sat_cubes=%d result=%s time=%.1f' % (
    n, T, mode, ncube, c1, c2, nsat, 'SAT' if nsat else 'UNSAT', time.time() - t0), flush=True)
