"""Referee round 3: as sat_cubes.py, but runs only the listed outer options (indices into the option list of
midpoint c1: 0..len-1 = its triples in lexicographic order, len = 'empty'), one fresh solver per outer option,
and logs each outer option's completion.  Usage: python3 sat_cubes2.py n T mode c1 c2 solver idx,idx,..."""
import sys, time
from pysat.solvers import Solver
from sat_model import build

n, T, mode, c1, c2, sname = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
idxs = [int(x) for x in sys.argv[7].split(',')]
triples, var, nv, clauses, bymid, aux = build(n, T, mode)
opts1 = [var[t] for t in bymid[c1]] + [None]
opts2 = [var[t] for t in bymid[c2]] + [None]
for ix in idxs:
    a = opts1[ix]; t0 = time.time(); nsat = 0
    with Solver(name=sname, bootstrap_with=clauses) as S:
        for b in opts2:
            ass = ([a] if a else [-var[t] for t in bymid[c1]]) + ([b] if b else [-var[t] for t in bymid[c2]])
            if S.solve(assumptions=ass):
                nsat += 1
                m = S.get_model()
                print('SAT cube', a, b, 'model', ' '.join('%d,%d,%d' % triples[v - 1] for v in m if 0 < v <= len(triples)), flush=True)
    print('OUTER idx=%d c1-option=%s (%s) inner_cubes=%d sat=%d result=%s time=%.1f' % (
        ix, a, triples[a - 1] if a else 'empty', len(opts2), nsat, 'SAT' if nsat else 'UNSAT', time.time() - t0), flush=True)
