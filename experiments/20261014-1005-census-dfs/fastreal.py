"""Fast exact realization of RIGID ordered patterns (AP-equation rank N-2 => unique up to x -> qx+t).
realize_fast(N, edges) -> ("ok", vals) | ("fail", reason) | None (not rigid / degenerate: caller falls back to
e757.realizability.realize_exact).  Reasons are the same labels realize_exact uses, in the same check order
(order, extra AP, repeated difference).  All arithmetic is Fraction/int."""
import math
from fractions import Fraction
from e757.core import ap_edges, is_45_set

def realize_fast(N, edges):
    rows = []
    for (i, j, k) in edges:
        r = [Fraction(0)] * (N + 1)
        r[i] += 1; r[k] += 1; r[j] -= 2
        rows.append(r)
    for idx, val in ((0, 0), (N - 1, 1)):
        r = [Fraction(0)] * (N + 1); r[idx] = Fraction(1); r[N] = Fraction(val); rows.append(r)
    # Gauss-Jordan on square system (len(rows) == len(edges)+2 == N when m = N-2)
    nr = len(rows)
    piv = []
    row = 0
    for col in range(N):
        p = None
        for r in range(row, nr):
            if rows[r][col] != 0: p = r; break
        if p is None: return None
        rows[row], rows[p] = rows[p], rows[row]
        inv = 1 / rows[row][col]
        rows[row] = [x * inv for x in rows[row]]
        for r in range(nr):
            if r != row and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[row])]
        row += 1
    if row != N: return None
    for r in range(N, nr):
        if rows[r][N] != 0: return None
    x = [rows[c][N] for c in range(N)]
    if any(x[i] >= x[i + 1] for i in range(N - 1)):
        return ("fail", "order-infeasible")
    L = 1
    for v in x: L = L * v.denominator // math.gcd(L, v.denominator)
    vals = [int(v * L) for v in x]
    g = 0
    for v in vals: g = math.gcd(g, v)
    vals = [v // g for v in vals]
    got = set()
    pos = {v: i for i, v in enumerate(vals)}
    for (a, b, c) in ap_edges(vals): got.add((pos[a], pos[b], pos[c]))
    if got != set(tuple(e) for e in edges):
        return ("fail", "forced extra AP")
    if not is_45_set(vals):
        return ("fail", "forced repeated difference")
    return ("ok", vals)
