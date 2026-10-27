"""A_base sanity check for Theorem 10 / Remark 10.4: AP hypergraph, tau, minimum transversals, NC pairs (own code)."""
from hyp25 import *
from itertools import combinations
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
idx = {a: i for i, a in enumerate(A)}
S = set(A)
E = []
for x, z in combinations(A, 2):
    if (x + z) % 2 == 0 and (x + z) // 2 in S:
        E.append(tuple(sorted((idx[x], idx[(x + z) // 2], idx[z]))))
h = Hyp(E, range(14))
print('n m tau s', h.n, h.m, h.tau(), h.slack(), 'inC', h.in_C(), 'maxdeg', h.maxdeg(), '#minT', len(h.min_transversals()))
cp = h.co_pairs()
nc = [p for p in combinations(range(14), 2) if frozenset(p) not in cp]
print('NC pairs', len(nc))
