"""S1: A_base facts and sanity checks of the round-3 primitives.
Run: python3 -I s1_base.py   (from this directory)"""
import itertools, json, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
import numpy as np
from r3lib import A_BASE, is45_py, is45_np, is_sidon, h_sat, h_brute, ap_triples, collision_sets

t0 = time.time()
A = [F(a) for a in A_BASE]
print('A_base n =', len(A), 'distinct =', len(set(A)) == len(A))
print('(4,5): py', is45_py(A), 'np', is45_np(A))
aps = ap_triples(A)
print('3-APs:', len(aps), '; midpoints == interior points:', sorted(m for _, m, _ in aps) == sorted(A)[1:-1])
deg = {a: sum(a in t for t in aps) for a in A}
print('AP degrees:', sorted(deg.values(), reverse=True))
# sum collisions of A: for a weak Sidon set they are exactly the 12 3-APs
coll = collision_sets(A)
print('sum-collision sets in A:', len(coll), 'all of size 3:', all(len(U) == 3 for U in coll))

# h(A)
hs, W = h_sat(A, start=8)
hb, cnt = h_brute(A)
n9 = sum(1 for c in itertools.combinations(A, 9) if is_sidon(c))
n8 = sum(1 for c in itertools.combinations(A, 8) if is_sidon(c))
print('h(A): sat', hs, 'brute', hb, '#max', cnt, '| pure-python: Sidon 9-subsets', n9, ', Sidon 8-subsets', n8)
assert hs == hb == 8 and n9 == 0 and n8 == cnt == 143

# for each a: a Sidon 8-subset of A avoiding a  <=>  alpha(H(A) + {a,X,Y}) = 10
S8 = [c for c in itertools.combinations(A, 8) if is_sidon(c)]
avoid = {a: next((c for c in S8 if a not in c), None) for a in A}
print('every a avoided by some max Sidon set:', all(v is not None for v in avoid.values()))
print('points in all 143 max Sidon sets:', [a for a in A if all(a in c for c in S8)])
# abstract 16-vertex hypergraph H(A) + {a,X,Y}: brute force over all 2^16 vertex subsets
idx = {a: i for i, a in enumerate(A)}
emask = [sum(1 << idx[v] for v in t) for t in aps]
m = np.arange(1 << 16, dtype=np.int64)
pc = sum((m >> i) & 1 for i in range(16))
base_bad = np.zeros(1 << 16, dtype=bool)
for e in emask:
    base_bad |= (m & e) == e
alph = {}
for a in A:
    e = (1 << idx[a]) | (1 << 14) | (1 << 15)
    bad = base_bad | ((m & e) == e)
    alph[a] = int(pc[~bad].max())
print('alpha(H(A)+{a,X,Y}) over a:', sorted(set(alph.values())), {str(k): v for k, v in alph.items()})
assert set(alph.values()) == {10}

# K3 examples and Fibonacci
print('{1,2,3,5} (4,5)?', is45_py([1, 2, 3, 5]), '| {2,3,5,8} (4,5)?', is45_py([2, 3, 5, 8]),
      '| {1,2,3,6} (4,5)?', is45_py([1, 2, 3, 6]), 'Sidon?', is_sidon([1, 2, 3, 6]))
fib = [2, 3]
while len(fib) < 18:
    fib.append(fib[-1] + fib[-2])
for k in (5, 8, 10, 12, 15, 18):
    S = fib[:k]
    print('Fibonacci n=%d: (4,5) %s, h_sat %d, h_brute %d' % (k, is45_np(S), h_sat(S)[0], h_brute(S)[0]))

# data/small_records.json
D = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
for k, rec in D.items():
    S = [F(v) for v in rec['set']]
    print('small_records %s: n=%d (4,5) %s, h_sat %d, h_brute %d, recorded h %s' %
          (k, len(S), is45_np(S), h_sat(S)[0], h_brute(S)[0], rec.get('h')))

# Lemma K4 on all 2^14 induced subsets of A_base: Sidon (definition) == 3-AP-free
sid = np.ones(1 << 14, dtype=bool)
for U in coll:
    u = sum(1 << i for i in U)
    sid &= ~((m[:1 << 14] & u) == u)
apf = np.ones(1 << 14, dtype=bool)
for e in emask:
    apf &= ~((m[:1 << 14] & e) == e)
print('induced subsets of A_base: Sidon==3-AP-free on all 16384:', bool((sid == apf).all()))
print('time %.1fs' % (time.time() - t0))
