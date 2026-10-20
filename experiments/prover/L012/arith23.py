"""(L012) Arithmetic for the 23-point record cell (exact integers):
(a) 23-point patterns with h = 13: tau = 10, m <= 21 (P3), K8 17*10 <= 5*23 + 3m  =>  m >= 19;
(b) the deletion bound: for a vertex v of degree d, H - v has 22 vertices, m - d edges and tau(H - v) in {9, 10}; I11 at n = 22 (L011)
    excludes tau(H - v) = 10 and gives 11*9 <= 66 + 2(m - d); the resulting maximum degree and the degree-sum test;
(c) the decompositions of G = H - v used in routes 4, 20 and (open) 3, by the two generators of decomp22.py (G1 slack-sum, G2
    partition-first) and by engine.decompositions;
(d) the I11-allowed record cells for n <= 40 (as in L011 Remark 5)."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp22 import gen1, slack_cells
from engine import decompositions
n, tau = 23, 10
print('(a) h = 13 => tau = 10; P3: m <= 21; K8: 170 <= 115 + 3m  <=>  m >= %d' % math.ceil((17 * tau - 5 * n) / 3))
for m in (19, 20, 21):
    s = 3 * n + 2 * m - 11 * tau
    t10 = [d for d in range(0, 10) if 110 <= 66 + 2 * (m - d)]
    dmax = max(d for d in range(0, 10) if 99 <= 66 + 2 * (m - d))
    print('(b) m = %d: I11 slack of H = %d; tau(H-v) = 10 possible for degrees %s (none); tau(H-v) = 9 and 99 <= 66 + 2(%d - d) => d <= %d;'
          ' degree sum 3m = %d vs 2n = %d, %s' % (m, s, t10, m, dmax, 3 * m, 2 * n, 'impossible' if 3 * m > dmax * n else 'max degree %d forced' % dmax if 3 * m > (dmax - 1) * n else 'ok'))
    for d in range(1, dmax + 1):
        print('      a vertex of degree %d: H - v = (22, %d, 9), slack %d' % (d, m - d, 66 + 2 * (m - d) - 99))
def gen2_any(N, M, S):
    """partition-first generator for arbitrary total slack S (parts of size 1 or >= 3; every admissible (m_i, tau_i) per part)."""
    if (3 * N + 2 * M - S) % 11: return set()
    T = (3 * N + 2 * M - S) // 11
    def types(p):
        if p == 1: return [(1, 0, 0)]
        return [(p, mm, t) for mm in range(0, p - 1) if p <= 2 * mm + 1 for t in range(1, mm + 1)
                if 0 <= 3 * p + 2 * mm - 11 * t <= S and 17 * t <= 5 * p + 3 * mm]
    def partitions(r, mx):
        if r == 0: yield []; return
        for p in range(min(r, mx), 0, -1):
            if p == 2: continue
            for rest in partitions(r - p, p): yield [p] + rest
    import itertools
    sols = set()
    for part in partitions(N, N):
        for combo in itertools.product(*[types(p) for p in part]):
            if sum(c[1] for c in combo) == M and sum(c[2] for c in combo) == T: sols.add(tuple(sorted(combo)))
    return sols
for (N, M, S, why) in [(22, 17, 1, 'routes 4 and 20: G = H - v, d(v) = 4 resp. 3'), (22, 18, 3, 'open route 3: G = H - v, d(v) = 3, m = 21'),
                       (22, 19, 5, 'm = 21, d(v) = 2 (not used)')]:
    a = set(tuple(sorted(x)) for x in gen1(N, M, S)); b = gen2_any(N, M, S); c = set(tuple(sorted(x)) for x in decompositions(N, M, S))
    print('(c) (%d,%d) slack %d [%s]: G1 %d, G2 %d, engine %d, %s' % (N, M, S, why, len(a), len(b), len(c), 'EQUAL' if a == b == c else 'DIFFERENT'))
    for x in sorted(c): print('       ', list(x))
print('(d) record cells (n, m, tau, slack) with I11 slack >= 0, n <= 40:')
for nn in range(3, 41):
    hmax = math.ceil(4 * nn / 7) - 1; tmin = nn - hmax
    cells = [(nn, mm, t, 3 * nn + 2 * mm - 11 * t) for mm in range(0, nn - 1) for t in range(tmin, mm + 1) if 17 * t <= 5 * nn + 3 * mm and 11 * t <= 3 * nn + 2 * mm]
    if cells: print('    n=%d:' % nn, cells)
