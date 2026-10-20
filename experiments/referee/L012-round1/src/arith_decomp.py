"""Referee: arithmetic of Steps 0.3/1/2 and an independent brute force of all slack decompositions used by the prover's engine.
Decomposition of (N, M) with total slack S: a multiset of component types, each either the isolated vertex (1,0,0) (slack 3) or a
connected type (n,m,t) with n >= 3, ceil((n-1)/2) <= m <= n-2, 1 <= t <= m, slack 3n+2m-11t >= 0; sum n = N, sum m = M,
sum of slacks = S.  Version W ('weak') uses only these constraints; version HY adds 17t <= 5n+3m (Henning-Yeo, published)."""
import json, glob, os, re, math, sys
from functools import lru_cache
# ---- Steps 0.3, 1, 2
n, tau = 23, 10
ms = [m for m in range(0, n - 1) if 17 * tau <= 5 * n + 3 * m]       # P3: m <= n-2
print('Step 1: m with P3 and HY at (23, tau=10):', ms)
for m in ms:
    s = 3 * n + 2 * m - 11 * tau
    dmax = None
    for d in range(0, m + 1):
        ok10 = 11 * 10 <= 3 * 22 + 2 * (m - d)          # tau(H-v)=10 allowed by I11 at n=22?
        ok9 = 11 * 9 <= 3 * 22 + 2 * (m - d)
        if ok10: print('  tau(H-v)=10 possible at m=%d d=%d' % (m, d))
        if ok9: dmax = d
    print('  m=%d: H slack %d, max degree %d, degree sum %d vs 2n=%d -> %s' % (m, s, dmax, 3 * m, dmax * n,
          'impossible' if 3 * m > dmax * n else 'ok'))
    for d in range(1, dmax + 1):
        print('     degree %d: H-v = (22,%d,9) slack %d' % (d, m - d, 66 + 2 * (m - d) - 99))
# Theorem 1 degree count
sols = [(n1, n2, n3) for n1 in range(24) for n2 in range(24) for n3 in range(24) if n1 + n2 + n3 == 23 and n1 + 2 * n2 + 3 * n3 == 63]
print('degree patterns (n1,n2,n3) with max degree 3, no isolated:', len(sols), 'min n3 =', min(s[2] for s in sols))
# ---- decompositions
def types(nn, smax, hy):
    out = []
    if nn == 1: return [(1, 0, 0)] if 3 <= smax else []
    if nn == 2: return []
    for mm in range(math.ceil((nn - 1) / 2), nn - 1):
        for t in range(1, mm + 1):
            s = 3 * nn + 2 * mm - 11 * t
            if 0 <= s <= smax and (not hy or 17 * t <= 5 * nn + 3 * mm): out.append((nn, mm, t))
    return out
def decomps(N, M, S, hy):
    res = set()
    def rec(remN, remM, remS, maxpart, cur):
        if remN == 0:
            if remM == 0 and remS == 0: res.add(tuple(sorted(cur)))
            return
        for part in range(min(remN, maxpart), 0, -1):
            for ty in types(part, remS, hy):
                s = 3 * ty[0] + 2 * ty[1] - 11 * ty[2]
                if ty[1] <= remM and s <= remS:
                    if cur and part == maxpart and ty > max(c for c in cur if c[0] == part): continue  # canonical order within equal sizes
                    rec(remN - part, remM - ty[1], remS - s, part, cur + [ty])
    rec(N, M, S, N, [])
    return res
for (N, M, S) in [(22, 17, 1), (22, 18, 3), (22, 19, 5)]:
    a, b = decomps(N, M, S, False), decomps(N, M, S, True)
    print('(%d,%d) slack %d: weak %d, HY %d' % (N, M, S, len(a), len(b)), sorted(b), 'extra in weak:', sorted(a - b))
# ---- compare with every branch recorded by the prover's engine
cells = sorted(glob.glob('/home/user/Erdos-757/experiments/prover/L012/out/cells/cell_*.txt'))
nb = 0; bad = 0; extra_weak = 0
for fn in cells:
    info = None
    for l in open(fn):
        if l.startswith('INFO '): info = json.loads(l[5:])
    if not info or info.get('route') != 'recurse': continue
    key = tuple(map(int, re.findall(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)', fn)[0]))
    for br in info['branches']:
        N, M, S = key[0] - 1, key[1] - br['d'], br['Sp']
        theirs = {tuple(sorted(tuple(x) for x in dd[0])) for dd in br['dec']}
        mine = decomps(N, M, S, True); weak = decomps(N, M, S, False)
        nb += 1
        if mine != theirs: bad += 1; print('MISMATCH', key, br['d'], br['tp'], S, sorted(mine ^ theirs))
        if weak != mine: extra_weak += 1
    # also check that every (d, tp) with S' >= 0 is present
    n_, m_, t_, D_ = key
    want = [(d, tp) for d in range(max(1, math.ceil(3 * m_ / n_)), D_ + 1) for tp in (t_ - 1, t_) if tp >= 0 and 3 * (n_ - 1) + 2 * (m_ - d) - 11 * tp >= 0]
    have = [(br['d'], br['tp']) for br in info['branches']]
    if want != have: print('BRANCH SET MISMATCH', key, want, have); bad += 1
print('engine branches compared: %d, mismatches: %d, branches where the weak (no-HY) list is larger: %d' % (nb, bad, extra_weak))
