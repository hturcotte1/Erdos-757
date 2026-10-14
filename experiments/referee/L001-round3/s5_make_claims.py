"""S5a: write frozen-judge input files (scratch only) for A_base, all 50 A u {x}, and all 1,743 (4,5) T1b sets,
with claimed_h and a witness from my SAT computation (s2_t1_out.json)."""
import json, os, sys
from fractions import Fraction as F
sys.path.insert(0, '.')
from r3lib import A_BASE, h_sat

os.makedirs('jin', exist_ok=True)
A = [F(a) for a in A_BASE]
D = json.load(open('s2_t1_out.json'))


def write(cid, S, h, W):
    json.dump({'id': cid, 'type': 'construction', 'set': [str(v) for v in sorted(S)], 'claimed_h': h,
               'witness_sidon_subset': [str(w) for w in sorted(W)], 'notes': 'L001 round-3 referee scratch'},
              open('jin/%s.json' % cid, 'w'))


h, W = h_sat(A, start=8)
write('r3-abase', A, h, W)
for i, xs in enumerate(D['Pok']):
    S = A + [F(xs)]
    h, W = h_sat(S, start=9)
    write('r3-ax-%02d' % i, S, h, W)
for i, p in enumerate(D['pairs']):
    write('r3-b-%04d' % i, A + [F(p['x']), F(p['y'])], p['h'], [F(w) for w in p['W']])
print('written', 1 + len(D['Pok']) + len(D['pairs']))
