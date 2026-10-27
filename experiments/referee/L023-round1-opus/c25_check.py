"""Referee L023 round 1 (own code; no import of e757/, judge/ or any prover script).
Theorem 4: C25 from the claim file and from the certificate's two descriptions; distinct integers; (4,5) by all 4-subsets;
largest Sidon subset by BRUTE FORCE over all 2^25 subsets (numpy bitmasks): a subset is Sidon iff it contains no 3-AP {z<x<w, 2x=z+w}
and no 4-set {x,y,z,w} with x+y=z+w (these are all the ways two different pairs-with-repetition can have the same sum)."""
import json, itertools
from fractions import Fraction
import numpy as np
A_base = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
B11 = [0,2009010,2901878,3392944,3459949,3705482,3750000,3794746,3884010,4018020,7500000]
built = sorted(set(A_base) | set(10**9 + 7919 * b for b in B11))
listed = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056,1000000000,16909350190,23979971882,27868723536,28399336131,30343711958,30696250000,31050593574,31757475190,32818700380,60392500000]
claim = json.load(open('/home/user/Erdos-757/results/claims/C007-c25-witness-f25.json'))
S = claim['set']
print('claim set == certificate list:', sorted(S) == listed, '; == A_base u (1e9+7919 B11):', sorted(S) == built, '; len', len(S), 'distinct', len(set(S)), 'all int', all(isinstance(x, int) for x in S))
A = sorted(S); n = len(A)
bad45 = 0
for Q in itertools.combinations(A, 4):
    if len(set(abs(a - b) for a, b in itertools.combinations(Q, 2))) < 5: bad45 += 1
print('4-subsets', len(list(itertools.combinations(range(n), 4))), 'with < 5 distinct distances:', bad45)
idx = {x: i for i, x in enumerate(A)}
aps = [(i, idx[(A[i] + A[k]) // 2], k) for i in range(n) for k in range(i + 1, n) if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx]
sums = {}
for i, j in itertools.combinations(range(n), 2): sums.setdefault(A[i] + A[j], []).append((i, j))
quads = [(p, q) for L in sums.values() for p, q in itertools.combinations(L, 2)]
print('3-APs', len(aps), '; 4-element additive quadruples (x+y=z+w, x<y, z<w, disjoint)', len(quads), '; weak Sidon:', len(quads) == 0)
inA = sum(1 for (i, j, k) in aps if A[k] <= 1056); inB = sum(1 for (i, j, k) in aps if A[i] >= 10**9); mixed = len(aps) - inA - inB
print('APs inside A_base', inA, 'inside the scaled B11', inB, 'mixed', mixed)
masks = [sum(1 << v for v in ap) for ap in aps] + [sum(1 << v for v in p + q) for p, q in quads]
M = np.arange(1 << n, dtype=np.int64); good = np.ones(1 << n, dtype=bool)
for m in masks: good &= (M & m) != m
pc = np.zeros(1 << n, dtype=np.int8)
for v in range(n): pc += ((M >> v) & 1).astype(np.int8)
best = int(pc[good].max()); arg = int(M[good][np.argmax(pc[good])])
W = [A[v] for v in range(n) if arg >> v & 1]
sid = len(set(x + y for x, y in itertools.combinations_with_replacement(W, 2))) == len(W) * (len(W) + 1) // 2
print('largest Sidon subset (brute force over all 2^25 subsets):', best, '; number of maximum Sidon subsets:', int((pc[good] == best).sum()), '; example', W, 'is Sidon (direct sums check):', sid)
w = claim['witness_sidon_subset']
print('claimed_h', claim['claimed_h'], '; witness in set', set(w) <= set(A), 'witness size', len(w), 'witness Sidon', len(set(x + y for x, y in itertools.combinations_with_replacement(sorted(w), 2))) == len(w) * (len(w) + 1) // 2)
print('h/n =', Fraction(best, n), '; 4/7 =', Fraction(4, 7), '; h/n < 4/7:', Fraction(best, n) < Fraction(4, 7))
