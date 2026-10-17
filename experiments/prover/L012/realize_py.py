"""(L012) Second, independent exact implementation of the realization test (pure Python, Fractions), for cross-checking realize.c on
selected graphs: enumerates the injective midpoint assignments in a different order (vertices -> edge whose midpoint they are), solves
the system with Fraction Gaussian elimination, and counts (assignments, distinct-valued solutions, realizations = distinct values with
exactly m three-term APs).  Usage: realize_py.py NV < FOUND lines"""
import sys, re, itertools
from fractions import Fraction as F
NV = int(sys.argv[1])
def solve(edges, n, mu, u, v):
    idx = [w for w in range(n) if w not in (u, v)]; pos = {w: i for i, w in enumerate(idx)}; N = len(idx)
    A = [[F(0)] * (N + 1) for _ in range(N)]
    for r, (e, j) in enumerate(zip(edges, mu)):
        A[r][pos[j]] += 2
        for w in e:
            if w == j: continue
            if w == v: A[r][N] += 1
            elif w != u: A[r][pos[w]] -= 1
    for c in range(N):
        p = next((r for r in range(c, N) if A[r][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; iv = 1 / A[c][c]; A[c] = [a * iv for a in A[c]]
        for r in range(N):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    x = [F(0)] * n; x[v] = F(1)
    for w, i in pos.items(): x[w] = A[i][N]
    return x
for line in sys.stdin:
    edges = [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)]
    if not edges: continue
    n = NV; m = len(edges); assert m == n - 2
    inc = {w: [i for i, e in enumerate(edges) if w in e] for w in range(n)}
    # enumerate injective maps edge -> midpoint as: choose the 2 unmatched vertices, then a perfect matching vertices <-> edges
    na = nd = nr = nsing = 0
    for u, v in itertools.combinations(range(n), 2):
        rest = [w for w in range(n) if w not in (u, v)]
        def match(k, used_e, assign):
            global na, nd, nr, nsing
            if k == len(rest):
                mu = [None] * m
                for w, e in assign.items(): mu[e] = w
                na += 1; x = solve(edges, n, mu, u, v)
                if x is None: nsing += 1; return
                if len(set(x)) < n: return
                nd += 1; vals = set(x)
                aps = sum(1 for a, c in itertools.combinations(range(n), 2) if (x[a] + x[c]) / 2 in vals and (x[a] + x[c]) / 2 not in (x[a], x[c]))
                if aps == m: nr += 1
                return
            w = rest[k]
            for e in inc[w]:
                if not used_e[e]:
                    used_e[e] = True; assign[w] = e; match(k + 1, used_e, assign); del assign[w]; used_e[e] = False
        match(0, [False] * m, {})
    print('PY assignments=%d singular=%d distinct=%d realizations=%d' % (na, nsing, nd, nr), flush=True)
