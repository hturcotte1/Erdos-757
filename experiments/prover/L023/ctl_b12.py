"""(L023) Positive control: the third 12-point record B12 (kb/00_START_HERE.md section 6) is REALIZABLE for realize_sdr, with its true labelling."""
import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import decide, solve, classify
from e757.core import ap_edges
A = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
idx = {x: i for i, x in enumerate(A)}
aps = ap_edges(A); E = [tuple(sorted((idx[a], idx[b], idx[c]))) for a, b, c in aps]; mids = {tuple(sorted((idx[a], idx[b], idx[c]))): idx[b] for a, b, c in aps}
st, ex = decide(E, 12); x = solve(E, 12, tuple(mids[e] for e in E))
print('SET B12 n=12 m=%d' % len(E), 'REALIZABLE' if st['REAL'] else 'NOT', json.dumps(st), 'true_labelling', classify(x, E, 12), 'solution_equals_normalized_set', x == [Fr(a, 575) for a in A])
