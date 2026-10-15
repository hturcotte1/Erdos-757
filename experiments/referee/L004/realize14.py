"""Referee L004: independent exact realizer for saturated ordered midpoint patterns (own code; no e757/judge imports).
For a pattern with triples (l, j, r), one per interior j, solve 2 x_j - x_l - x_r = 0 (j = 1..N-2), x_0 = 0, x_{N-1} = 1
exactly: integer Bareiss forward elimination on the (N-2)x(N-2) system + Fraction back-substitution, then an exact
residual check of every equation. Classification (in this order):
  singular   : determinant 0 (pattern not rigid)
  order      : solution not strictly increasing in rank order (x_0 < x_1 < ... < x_{N-1} fails)
  extraAP    : the solved set has a 3-AP that is not a pattern triple
  not45      : some 4 points determine <= 4 distinct distances
  ok         : realizable; then h (largest Sidon subset, by exhaustive search from the definition) and alpha of the
               AP hypergraph are computed, and the affine normal form (translate to 0, divide by gcd, min with
               reflection) is returned.
usage: python3 realize14.py N < patterns (lines 'tag i,j,k i,j,k ...' or 'i,j,k ...')  > out (tsv)
out: tag status h alpha det normal_form(comma list or -) pattern"""
import sys, itertools
from fractions import Fraction
from math import gcd


def solve(N, edges):
    n = N - 2  # unknowns x_1..x_{N-2}
    A = [[0] * (n + 1) for _ in range(n)]
    for (l, j, r) in edges:
        row = A[j - 1]
        row[j - 1] += 2
        for v in (l, r):
            if v == 0:
                pass  # x_0 = 0
            elif v == N - 1:
                row[n] += 1  # x_{N-1} = 1 moves to the right-hand side
            else:
                row[v - 1] -= 1
    # Bareiss
    M = [row[:] for row in A]
    prev = 1
    sign = 1
    for k in range(n):
        if M[k][k] == 0:
            sw = next((q for q in range(k + 1, n) if M[q][k] != 0), None)
            if sw is None:
                return None, 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k + 1, n):
            for c in range(k + 1, n + 1):
                M[i][c] = (M[i][c] * M[k][k] - M[i][k] * M[k][c]) // prev
            M[i][k] = 0
        prev = M[k][k]
    det = sign * M[n - 1][n - 1]
    if det == 0:
        return None, 0
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        s = Fraction(M[i][n]) - sum(M[i][c] * x[c] for c in range(i + 1, n))
        x[i] = s / M[i][i]
    X = [Fraction(0)] + x + [Fraction(1)]
    # exact residual check against the ORIGINAL equations
    for (l, j, r) in edges:
        if 2 * X[j] - X[l] - X[r] != 0:
            raise AssertionError("residual")
    return X, det


def three_aps(vals):
    s = set(vals); pos = {v: q for q, v in enumerate(vals)}; out = set()
    for a, c in itertools.combinations(vals, 2):
        if (a + c) % 2 == 0 and (a + c) // 2 in s:
            out.add((pos[a], pos[(a + c) // 2], pos[c]))
    return out


def is45(vals):
    for q in itertools.combinations(vals, 4):
        d = set(abs(a - b) for a, b in itertools.combinations(q, 2))
        if len(d) < 5:
            return False
    return True


def sidon_max(vals):
    vals = sorted(vals); n = len(vals); best = [0]

    def rec(i, chosen, diffs):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
        if len(chosen) + (n - i) <= best[0]:
            return
        for t in range(i, n):
            if len(chosen) + (n - t) <= best[0]:
                return
            v = vals[t]; nd = [v - c for c in chosen]
            if len(set(nd)) == len(nd) and not (set(nd) & diffs):
                rec(t + 1, chosen + [v], diffs | set(nd))
    rec(0, [], frozenset())
    return best[0]


def alpha_ap(N, aps):
    masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in aps]
    best = 0
    for S in range(1 << N):
        pc = bin(S).count("1")
        if pc <= best:
            continue
        if all((m & S) != m for m in masks):
            best = pc
    return best


def normal_form(vals):
    v = sorted(vals); lo = v[0]; v = [x - lo for x in v]
    g = 0
    for x in v:
        g = gcd(g, x)
    v = [x // g for x in v]
    w = sorted(v[-1] - x for x in v)
    return min(tuple(v), tuple(w))


def realize(N, edges):
    X, det = solve(N, edges)
    if X is None:
        return "singular", None, det
    if any(X[q] >= X[q + 1] for q in range(N - 1)):
        return "order", None, det
    L = 1
    for f in X:
        L = L * f.denominator // gcd(L, f.denominator)
    vals = [int(f * L) for f in X]
    g = 0
    for v in vals:
        g = gcd(g, v)
    vals = [v // g for v in vals]
    if three_aps(vals) != set(tuple(e) for e in edges):
        return "extraAP", vals, det
    if not is45(vals):
        return "not45", vals, det
    return "ok", vals, det


if __name__ == "__main__":
    N = int(sys.argv[1])
    for line in sys.stdin:
        w = line.split()
        if not w or w[0].startswith("#"):
            continue
        tag = "-"
        if "," not in w[0]:
            tag, w = w[0], w[1:]
        es = sorted(tuple(map(int, t.split(","))) for t in w)
        st, vals, det = realize(N, es)
        h = al = -1; nf = "-"
        if st == "ok":
            h = sidon_max(vals); al = alpha_ap(N, three_aps(vals)); nf = ",".join(map(str, normal_form(vals)))
        print("%s\t%s\t%d\t%d\t%d\t%s\t%s" % (tag, st, h, al, det, nf, " ".join("%d,%d,%d" % e for e in es)))
