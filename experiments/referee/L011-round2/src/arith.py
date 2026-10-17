"""Referee L011 round 2: exact integer re-derivation of Steps 0.7, 1, 2, 3 and the decomposition lists.
Written from scratch; no e757, no prover code.  Usage: python3 -I arith.py"""
from itertools import combinations_with_replacement
from fractions import Fraction

def slack(n, m, t): return 3*n + 2*m - 11*t

# ---- Step 1: window cells (connected violator: m>=1, n<=2m+1, m<=n-2, tau<=m, K8 17tau<=5n+3m)
def windows(n, useK8=True):
    out = []
    for m in range(0, n+1):
        if m < 1 or n > 2*m+1 or m > n-2: continue
        for t in range(0, m+1):
            if slack(n, m, t) >= 0: continue
            if useK8 and 17*t > 5*n + 3*m: continue
            out.append((n, m, t))
    return out

print("== window cells n=21,22 (with K8)")
allw = []
for n in range(3, 23):
    w = windows(n); allw += w
    if n >= 21: print(n, w)
print("number of window cells with n<=22:", len(allw))
# L010 had n<=20 -> 22 cells?
print("  with n<=20:", len([c for c in allw if c[0] <= 20]))

# ---- Step 2: degree bound, by testing each d directly (not the closed formula)
print("== degree bounds (I11 on H-v with N-1 vertices, m-d edges, tau(H-v) in {tau-1, tau})")
for (n, m, t) in [c for c in allw if c[0] >= 21]:
    # tau(H-v) = tau impossible?
    forced = []
    for tv in (t, t-1):
        ok_any = any(11*tv <= 3*(n-1) + 2*(m-d) for d in range(0, m+1))
        forced.append((tv, ok_any))
    # which d allow some tv in {t-1,t} with I11 on H-v
    dmax = max([d for d in range(0, m+1) if any(11*tv <= 3*(n-1)+2*(m-d) for tv in (t-1, t))], default=None)
    tv_t_possible = any(11*t <= 3*(n-1)+2*(m-d) for d in range(0, m+1))
    print((n, m, t), "s=", slack(n, m, t), "dmax=", dmax, "tau(H-v)=tau possible:", tv_t_possible,
          "  3m=", 3*m, "2n=", 2*n, "count-impossible(dmax<=2):", dmax is not None and dmax <= 2 and 3*m > 2*n,
          " dmax*n<3m:", dmax is not None and dmax*n < 3*m)

# also without K8: extra windows and their degree bounds
print("== windows without K8 at n=21,22: extra cells and their dmax")
for n in (21, 22):
    extra = [c for c in windows(n, False) if c not in windows(n, True)]
    dm = {}
    for (nn, m, t) in extra:
        dmax = max([d for d in range(0, m+1) if any(11*tv <= 3*(nn-1)+2*(m-d) for tv in (t-1, t))], default=-1)
        dm[dmax] = dm.get(dmax, 0) + 1
    print(n, "extra", len(extra), "dmax histogram", dm)

# ---- Step 0.7: slack cells (connected components, n<=21, slack 0..3)
def cells(S, nmax=21, useK8=True):
    out = []
    for n in range(2, nmax+1):
        for m in range(1, n-1):          # m <= n-2
            if n > 2*m + 1: continue
            for t in range(1, m+1):
                s = slack(n, m, t)
                if s != S: continue
                if useK8 and 17*t > 5*n + 3*m: continue
                out.append((n, m, t))
    return out
print("== slack cells (n<=21)")
for S in range(4):
    a, b = cells(S), cells(S, useK8=False)
    print(S, a, "same without K8:", a == b)

# ---- decompositions: multisets of pieces with sum n = N, sum m = M, total slack = S (pieces: cells with slack<=S, iso vertex)
def decomps(N, M, S, useK8=True):
    pieces = [('I', 1, 0, 0, 3)] if S >= 3 else []
    for s in range(S+1):
        for (n, m, t) in cells(s, nmax=N, useK8=useK8):
            pieces.append(((n, m, t), n, m, t, s))
    res = []
    def rec(i, n, m, s, cur):
        if n == N and m == M and s == S:
            res.append(tuple(cur)); return
        if i >= len(pieces): return
        # use piece i some number of times (including 0)
        name, pn, pm, pt, ps = pieces[i]
        k = 0
        while n + k*pn <= N and m + k*pm <= M and s + k*ps <= S:
            rec(i+1, n + k*pn, m + k*pm, s + k*ps, cur + [name]*k)
            k += 1
            if pn == 0: break
    rec(0, 0, 0, 0, [])
    return res

def fmt(d):
    from collections import Counter
    c = Counter(d); parts = []
    for k in sorted(c, key=lambda x: (x == 'I', x if x != 'I' else (0,))):
        nm = 'I' if k == 'I' else ('AP' if k == (3, 1, 1) else str(k))
        parts.append(nm + ('^%d' % c[k] if c[k] > 1 else ''))
    return '[' + ', '.join(parts) + ']'

print("== decompositions")
for (N, M, S, tag) in [(20, 9, 1, 'Step5.3 G=(20,9,7)'), (19, 11, 2, 'Step6.3 X-w=(19,11,7)'), (20, 14, 0, 'Step7.2 G=(20,14,8)'),
                       (20, 10, 3, 'Step9.3 X-w=(20,10,7)'), (21, 13, 1, 'Step10.2 G=(21,13,8)'),
                       (17, 9, 3, 'check L010'), (18, 12, 1, 'check'), (19, 10, 0, 'check'), (16, 10, 2, 'check'), (13, 9, 2, 'check')]:
    t = (3*N + 2*M - S)
    assert t % 11 == 0
    d1 = decomps(N, M, S); d2 = decomps(N, M, S, useK8=False)
    print(tag, (N, M, t//11), "slack", S, ":", len(d1), "decompositions; same without K8:", sorted(map(fmt, d1)) == sorted(map(fmt, d2)))
    for d in sorted(d1, key=lambda x: fmt(x)): print("    ", fmt(d))
