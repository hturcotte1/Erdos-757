"""L027 sanity checks (own code, exact): (1) the triangle (6,3,2) with its pendant triple (slack 2,
outside Theorem B): hub and fold arithmetic of Lemmas A1, A2 and the gadget Lemma A11 on T - {0,1,2};
(2) A_base (Ma-Tang 14-point set): AP hypergraph in C, tight, and no pairwise-NC non-edge triple
(Theorem B with (H_16), which holds by L016)."""
from itertools import combinations
from hyp27 import tau, min_transversals, in_C, slack, degrees, popc

# (1) triangle
T = [(0, 3, 4), (1, 3, 5), (2, 4, 5)]
t, Ts = min_transversals(6, T)
print('triangle: n,m,tau,s =', 6, 3, t, slack(6, 3, t), 'in C', in_C(6, T))
nc = all(not ((M >> p & 1) and (M >> q & 1)) for M in Ts for (p, q) in combinations((0, 1, 2), 2))
print('  {0,1,2}: degrees', [degrees(6, T)[u] for u in (0, 1, 2)], 'pairwise NC', nc)
v, x, y, z = 6, 7, 8, 9
Hh = T + [(x, y, z), (0, v, x), (1, v, y), (2, v, z)]
th = tau(10, Hh)
print('  hub T+(0,1,2): n,m,tau,s =', 10, 7, th, slack(10, 7, th), 'in C', in_C(10, Hh), '(Lemma A1: s-2 =', slack(6, 3, t) - 2, ')')
Fo = T + [(0, 1, 6), (2, 6, 7)]
tf = tau(8, Fo)
print('  fold T+(0,1|2): n,m,tau,s =', 8, 5, tf, slack(8, 5, tf), 'in C', in_C(8, Fo), '(Lemma A2: s-1 =', slack(6, 3, t) - 1, ')')
# T'' = T - {0,1,2}: three isolated vertices 3,4,5 (relabelled 0,1,2), s = 9; pairs A={3,4},B={3,5},C={4,5}
print('  T-{0,1,2}: three isolated vertices, s =', slack(3, 0, 0), '(= s(T)+13-2*3 = 9, Lemma A9 with drop 2)')

# (2) A_base
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
idx = {a: i for i, a in enumerate(A)}
S = set(A)
E = []
for i, a in enumerate(A):
    for c in A[i + 1:]:
        if (a + c) % 2 == 0 and (a + c) // 2 in S:
            E.append(tuple(sorted((idx[a], idx[(a + c) // 2], idx[c]))))
n, m = len(A), len(E)
t, Ts = min_transversals(n, E)
print('A_base: n,m,tau,s =', n, m, t, slack(n, m, t), 'in C', in_C(n, E), 'min transversals', len(Ts),
      'max degree', max(degrees(n, E)))
co = set()
for M in Ts:
    co.update(combinations([u for u in range(n) if M >> u & 1], 2))
ncpairs = [p for p in combinations(range(n), 2) if p not in co]
es = set(E)
trip = [tr for tr in combinations(range(n), 3) if tr not in es and all(p not in co for p in combinations(tr, 2))]
print('  NC pairs', len(ncpairs), ' pairwise-NC non-edge triples', len(trip))
