"""Referee L009 round 3: independent exact arithmetic for Steps 1, 2.2, 2.4, 3.2, 4.2, 4.4, 5.1-5.3.
Written from the definitions only (not from decomp18.py / cells.py of earlier rounds)."""
from itertools import product

def is_conn_cell(n, m):
    # connected 3-graph with n>=3 vertices and m>=1 edges: n <= 2m+1; class C: m <= n-2
    return n >= 3 and m >= 1 and n <= 2 * m + 1 and m <= n - 2

def window_cells(nmax, use_hy=True):
    out = []
    for n in range(3, nmax + 1):
        for m in range(1, n):
            if not is_conn_cell(n, m): continue
            taus = []
            for t in range(0, m + 1):
                if 11 * t > 3 * n + 2 * m and (not use_hy or 17 * t <= 5 * n + 3 * m):
                    taus.append(t)
            if taus: out.append((n, m, taus, 3 * n + 2 * m - 11 * taus[0]))
    return out

def slack_cells(nmax, smax, use_hy=True):
    out = []
    for n in range(3, nmax + 1):
        for m in range(1, n):
            if not is_conn_cell(n, m): continue
            for t in range(0, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= smax and (not use_hy or 17 * t <= 5 * n + 3 * m):
                    out.append((n, m, t, s))
    return out

def decompositions(N, M, S, pieces):
    """all multisets of pieces (n,m,t,s) [including the isolated vertex (1,0,0,3)] with sum (N,M,S)."""
    sols = []
    def rec(i, n, m, s, chosen):
        if (n, m, s) == (N, M, S): sols.append(tuple(chosen)); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt, ps = pieces[i]
        k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [pieces[i][:3]] * k)
            k += 1
    rec(0, 0, 0, 0, [])
    return sols

for hy in (True, False):
    print("=== window cells n<=18, Henning-Yeo %s ===" % ("imposed" if hy else "NOT imposed"))
    for w in window_cells(18, hy):
        if w[0] >= 17 or not hy: print("  ", w)
    print("   n<=16:", [(w[0], w[1], w[2]) for w in window_cells(16, hy)])

for hy in (True, False):
    sc = slack_cells(17, 2, hy)
    for s in (0, 1, 2):
        print("slack %d cells n<=17 (HY %s):" % (s, hy), [c[:3] for c in sc if c[3] == s])
    pieces = sc + [(1, 0, 0, 3)]
    for (N, M, S, why) in [(16, 9, 0, "G=H-v, H in (17,12,7)"), (17, 13, 0, "G=H-v, H in (18,16,8)"),
                           (16, 10, 2, "T-w, T in (17,13,7)"), (13, 9, 2, "T-w, T in (14,12,6)")]:
        print("  decomp (%d,%d) slack %d [%s]:" % (N, M, S, why), decompositions(N, M, S, pieces))

# degree bounds from I11 at n-1 together with tau(H-v) >= tau(H)-1 and tau(H-v) <= tau(H)
def degree_bound(n, m, tau):
    """largest d such that some tau' in [tau-1, tau] satisfies 11 tau' <= 3(n-1) + 2(m-d); also which tau' are possible."""
    res = {}
    for d in range(0, m + 1):
        ok = [t for t in (tau - 1, tau) if 11 * t <= 3 * (n - 1) + 2 * (m - d)]
        if ok: res[d] = ok
    return res
for cell in [(17, 12, 7), (18, 11, 7), (18, 16, 8), (17, 13, 7), (14, 12, 6)]:
    db = degree_bound(*cell)
    n, m, t = cell
    dmax = max(db)
    d3_min = 3 * m - 2 * n if dmax == 3 else None   # sum d = 3m <= 3 d3 + 2 (n - d3)
    print("cell", cell, "admissible (d: tau(H-v) values)", db, "=> Delta <=", dmax, "; min #deg-3 vertices", d3_min)
    if dmax == 3:
        print("   H-v for d(v)=3: (n,m,tau)=", (n - 1, m - 3, t - 1), "slack", 3 * (n - 1) + 2 * (m - 3) - 11 * (t - 1))
