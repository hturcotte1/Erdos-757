"""Step 1: A_base facts used by the certificate, recomputed from the definitions.
 - distinct, (4,5), its 3-APs (count, midpoints)
 - h(A)=8 (brute force + ILP), number of maximum Sidon subsets
 - for every a in A: h(A minus a) = 8   (=> T2-generic: S u {x,y} 3-AP-free with a notin S)
 - the abstract 16-vertex hypergraph H(A)+{a,X,Y}: alpha = 10 for each a (brute force over 10/11-subsets)
"""
import itertools, sys, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *

t0 = time.time()
A = ABASE
assert len(set(A)) == 14
print('A distinct, n=14; is45:', is45(A))
aps = three_aps(A)
print('3-APs of A:', len(aps), aps)
mids = sorted(t[1] for t in aps)
print('midpoints:', mids, '| distinct:', len(set(mids)), '| non-extreme points:', sorted(A)[1:-1] == mids)
hb, w = hmax_brute(A, 8)
print('h(A) brute =', hb, 'witness', w, '| ILP =', hmax_ilp(A))
nmax = sum(1 for c in itertools.combinations(A, 8) if is_sidon(c))
print('number of maximum Sidon 8-subsets:', nmax)
print('Sidon 9-subsets:', sum(1 for c in itertools.combinations(A, 9) if is_sidon(c)))
for a in A:
    R = [v for v in A if v != a]
    hb, w = hmax_brute(R, 8)
    print('  h(A - {%d}) brute=%d ILP=%d' % (a, hb, hmax_ilp(R)))
# abstract hypergraph check (vertices 0..13 = A, 14 = X, 15 = Y)
idx = {v: i for i, v in enumerate(A)}
E = [frozenset(idx[v] for v in t) for t in aps]
for a in A:
    EE = E + [frozenset((idx[a], 14, 15))]
    def indep(c):
        s = set(c)
        return not any(e <= s for e in EE)
    a10 = any(indep(c) for c in itertools.combinations(range(16), 10))
    a11 = any(indep(c) for c in itertools.combinations(range(16), 11))
    print('  abstract H(A)+{%d,X,Y}: has indep 10-set: %s, has indep 11-set: %s' % (a, a10, a11))
print('time %.1fs' % (time.time() - t0))
