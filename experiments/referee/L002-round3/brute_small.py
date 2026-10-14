"""Referee round 3: plain brute force over ALL ordered midpoint maps for small n (validation of the CNF model).
Each interior j gets None or a pair (i,k), i<j<k.  Keep: linearity (no pair of vertices in two triples) and
K30 (no j<j' with i>=i', k>=k').  alpha by full subset scan; F7 via f7split.has_f7.  Prints counts by
(m, alpha, f7)."""
import sys
from itertools import combinations, product
from collections import Counter
from f7split import has_f7

n = int(sys.argv[1])
choices = []
for j in range(1, n - 1):
    choices.append([None] + [(i, j, k) for i in range(j) for k in range(j + 1, n)])
subsets_by_size = sorted(range(1 << n), key=lambda s: -bin(s).count('1'))
cnt = Counter()
for pick in product(*choices):
    es = [e for e in pick if e is not None]
    ok = True
    pairs = set()
    for (i, j, k) in es:
        for p in ((i, j), (i, k), (j, k)):
            if p in pairs:
                ok = False; break
            pairs.add(p)
        if not ok:
            break
    if not ok:
        continue
    for a, b in combinations(es, 2):
        if a[1] > b[1]:
            a, b = b, a
        if a[0] >= b[0] and a[2] >= b[2]:
            ok = False; break
    if not ok:
        continue
    masks = [(1 << i) | (1 << j) | (1 << k) for (i, j, k) in es]
    al = 0
    for s in subsets_by_size:
        if all((s & mk) != mk for mk in masks):
            al = bin(s).count('1'); break
    cnt[(len(es), al, has_f7(es))] += 1
for k in sorted(cnt):
    print('n=%d m=%d alpha=%d f7=%d count=%d' % (n, k[0], k[1], k[2], cnt[k]))
