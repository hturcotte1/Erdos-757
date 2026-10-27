"""Referee L023 round 1 (own code): number of injective midpoint labellings (systems of distinct representatives) of each X_i,
and the two non-midpoint vertices; memoised count over (edge index, set of used vertices)."""
from functools import lru_cache
import hg_checks as H
L = [H.parse(l) for l in open('six_from_certificate.txt')]
for i, E in enumerate(L):
    E = sorted(E)
    @lru_cache(maxsize=None)
    def cnt(k, used):
        if k == len(E): return 1
        return sum(cnt(k + 1, used | (1 << v)) for v in E[k] if not used >> v & 1)
    print('X_%d injective labellings %d' % (i, cnt(0, 0)))
Q = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 2, 7)]
@lru_cache(maxsize=None)
def cq(k, used):
    if k == 6: return 1
    return sum(cq(k + 1, used | (1 << v)) for v in Q[k] if not used >> v & 1)
print('Q8 injective labellings', cq(0, 0))
