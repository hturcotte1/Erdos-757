"""Referee round 3 (L002): enumerate all models of the CNF in sat_model.py with a CDCL solver (pysat).
Usage:
  python3 sat_enum.py n T mode out.txt.gz [solver] [split]
    mode = sat     : saturated patterns; block each model by its positive literals (exact, since a saturated
                     pattern has no proper superpattern inside the model class)
    mode = nonsat  : >=1 empty interior midpoint; block each model by the full assignment of triple variables
    mode = any     : <=1 triple per midpoint, any m; full-assignment blocking
    split (optional, mode sat only): 'k' fixes the triple at midpoint 1 to (0,1,k)
Writes one line per model: 'm i,j,k i,j,k ...' (triples sorted), and prints the count."""
import sys, gzip, time
from pysat.solvers import Solver
from sat_model import build

n, T, mode, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
sname = sys.argv[5] if len(sys.argv) > 5 else 'g4'
split = int(sys.argv[6]) if len(sys.argv) > 6 else None
triples, var, nv, clauses, bymid, aux = build(n, T, mode)
t0 = time.time()
cnt = 0
with Solver(name=sname, bootstrap_with=clauses) as S, gzip.open(out, 'wt') as fo:
    if split is not None:
        S.add_clause([var[(0, 1, split)]])
    ntr = len(triples)
    while S.solve():
        model = S.get_model()
        pos = [triples[v - 1] for v in model if 0 < v <= ntr]
        cnt += 1
        fo.write('%d %s\n' % (len(pos), ' '.join('%d,%d,%d' % t for t in sorted(pos))))
        if mode == 'sat':
            S.add_clause([-var[t] for t in pos])
        else:
            S.add_clause([-l for l in model if abs(l) <= ntr])
    print('n=%d T=%d mode=%s split=%s solver=%s models=%d time=%.1f' % (n, T, mode, split, sname, cnt, time.time() - t0),
          flush=True)
