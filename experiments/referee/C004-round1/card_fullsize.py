"""Cardinality part of the k=34 CNF at the real size n=58: random x-assignments with exactly c true are SAT iff c >= 34."""
import random, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402
n = 58
card, top = R.atmost_seqcounter([-(v + 1) for v in range(n)], n - 34, n)
rng = random.Random(5)
bad = 0; tests = 0
with Solver(name='minisat22', bootstrap_with=card) as s:
    for c in list(range(28, 41)) + [0, 58]:
        for rep in range(40):
            T = set(rng.sample(range(n), c))
            res = s.solve(assumptions=[(v + 1) if v in T else -(v + 1) for v in range(n)])
            tests += 1
            bad += (res != (c >= 34))
print('full-size cardinality tests:', tests, 'mismatches (must be 0):', bad)
