"""Own minimal 3-graph toolkit for L028 (exact integer / bitmask arithmetic only).

Independent of e757/, judge/ and all other L0xx code.
A graph is (n, edges): vertices 0..n-1, edges a list of 3-tuples (sorted).
"""
import os
import re
from itertools import combinations


# ---------------------------------------------------------------- reading
def read_cell(path):
    """Read 'FOUND: (a,b,c) ...' lines (engine format) or 'n m tau e1 e2 ...' lines."""
    base = os.path.basename(path)
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)', base)
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('INFO'):
                continue
            if line.startswith('FOUND:'):
                n, m, tau = map(int, mm.groups())
                tri = re.findall(r'\((\d+),(\d+),(\d+)\)', line)
                edges = [tuple(sorted(map(int, t))) for t in tri]
                assert len(edges) == m, (path, len(edges), m)
                out.append((n, edges, tau))
            else:
                t = list(map(int, line.split()))
                n, m, tau = t[0], t[1], t[2]
                e = t[3:]
                edges = [tuple(sorted(e[3 * i:3 * i + 3])) for i in range(m)]
                out.append((n, edges, tau))
    return out


# ---------------------------------------------------------------- basics
def masks(edges):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]


def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for u in e:
            d[u] += 1
    return d


def popcount(x):
    return bin(x).count('1')


def tau(n, edges):
    """Exact transversal number by branching on an uncovered edge."""
    em = masks(edges)
    best = [len(em)]

    def rec(T, k):
        if k >= best[0]:
            return
        for e in em:
            if not (e & T):
                break
        else:
            best[0] = k
            return
        x = e
        while x:
            low = x & -x
            rec(T | low, k + 1)
            x ^= low

    rec(0, 0)
    return best[0]


def transversals_upto(n, edges, k):
    """All transversals (bitmasks) of size <= k, by brute force over subsets.
    Only for small n."""
    em = masks(edges)
    res = []
    for size in range(0, k + 1):
        for S in combinations(range(n), size):
            T = 0
            for u in S:
                T |= 1 << u
            ok = True
            for e in em:
                if not (e & T):
                    ok = False
                    break
            if ok:
                res.append(T)
    return res


def min_transversals(n, edges, t=None):
    if t is None:
        t = tau(n, edges)
    return [T for T in transversals_upto(n, edges, t) if popcount(T) == t]


def slack(n, edges, t=None):
    if t is None:
        t = tau(n, edges)
    return 3 * n + 2 * len(edges) - 11 * t


def is_linear(edges):
    em = masks(edges)
    for i in range(len(em)):
        for j in range(i + 1, len(em)):
            if popcount(em[i] & em[j]) >= 2:
                return False
    return True


def has_F7(n, edges):
    """F7 = {012,034,056,135,246}: a centre o with three edges covering six
    further vertices, plus two edges avoiding o, each meeting each centre edge once,
    the two being disjoint."""
    inc = [[] for _ in range(n)]
    for e in edges:
        for u in e:
            inc[u].append(e)
    eset = set(edges)
    for o in range(n):
        if len(inc[o]) < 3:
            continue
        for e1, e2, e3 in combinations(inc[o], 3):
            P = [tuple(x for x in e if x != o) for e in (e1, e2, e3)]
            allv = set(P[0]) | set(P[1]) | set(P[2])
            if len(allv) != 6:
                continue
            # choose one from each pair for the first transversal edge
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        f = tuple(sorted((P[0][i], P[1][j], P[2][k])))
                        g = tuple(sorted((P[0][1 - i], P[1][1 - j], P[2][1 - k])))
                        if f in eset and g in eset:
                            return True
    return False


def p3_ok(n, edges):
    """(P3): e(S) <= |S|-2 for all |S|>=2.  Brute force over subsets via
    a max-closure-free check: for each subset S of the vertex set spanned by edges."""
    em = masks(edges)
    # brute force over all subsets: fine for n <= 16
    for S in range(1, 1 << n):
        k = popcount(S)
        if k < 2:
            continue
        cnt = 0
        for e in em:
            if e & S == e:
                cnt += 1
        if cnt > k - 2:
            return False
    return True


def in_C(n, edges):
    return is_linear(edges) and (not has_F7(n, edges)) and p3_ok(n, edges)


def saturated_sets(n, edges):
    """All S with |S|>=3 and e(S) = |S|-2 (brute force)."""
    em = masks(edges)
    res = []
    for S in range(1, 1 << n):
        k = popcount(S)
        if k < 3:
            continue
        cnt = sum(1 for e in em if e & S == e)
        if cnt == k - 2:
            res.append(S)
    return res


def delete_vertices(n, edges, Z):
    """Induced subgraph on V \\ Z, relabelled; returns (n', edges', old->new map)."""
    keep = [u for u in range(n) if u not in Z]
    mp = {u: i for i, u in enumerate(keep)}
    ne = [tuple(sorted(mp[x] for x in e)) for e in edges if not (set(e) & set(Z))]
    return len(keep), ne, mp


def adjacent(edges, u, w):
    return any(u in e and w in e for e in edges)
