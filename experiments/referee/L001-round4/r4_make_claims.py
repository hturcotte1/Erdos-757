"""Write judge input files (in this scratch folder only) for A_base, the 50 sets A u {x} (x in P_ok) and the
1,743 stored pairs, each with claimed_h and a Sidon witness found by the M-criterion (S u new Sidon)."""
import json, sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
from r4_lib import A_BASE, is45_full, is_sidon, sidon_subsets
EXP = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
A = [Fr(a) for a in A_BASE]
Aset = set(A)
M = sidon_subsets(A, 8)
P = set()
for a, b in itertools.combinations(A, 2):
    P |= {(a + b) / 2, 2 * a - b, 2 * b - a}
P -= Aset
P_ok = sorted(x for x in P if is45_full(A + [x]))
R = json.load(open(EXP + 'results.json'))
D = '/home/user/Erdos-757/experiments/referee/L001-round4/jin/'


def write(cid, pts, new):
    W = next(list(S) + list(new) for S in M if is_sidon(list(S) + list(new)))
    with open(D + cid + '.json', 'w') as f:
        json.dump({'id': cid, 'type': 'construction', 'set': [str(p) for p in pts], 'claimed_h': len(W),
                   'witness_sidon_subset': [str(w) for w in W]}, f)


write('r4-abase', A, [])
for i, x in enumerate(P_ok):
    write('r4-ax-%02d' % i, A + [x], [x])
for i, (xs, ys, h) in enumerate(R['stored']):
    write('r4-pair-%04d' % i, A + [Fr(xs), Fr(ys)], [Fr(xs), Fr(ys)])
print('written', 1 + len(P_ok) + len(R['stored']))
