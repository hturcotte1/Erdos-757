"""Referee L008 round 3: own re-derivation of all arithmetic steps (Steps 1, 3, 4 of the proof), written from scratch.
Everything exact integers.  Prints window cells, the degree argument, slack-0/1 component cells (with and without HY),
and all decompositions of (15,11) into components with total slack 1."""
from math import ceil
from itertools import product

def lo(n, m): return (3*n + 2*m)//11 + 1          # least tau with 3n+2m-11tau < 0
def hy(n, m): return (5*n + 3*m)//17              # largest tau allowed by Henning-Yeo

def conn_cells(nmax):
    for n in range(3, nmax+1):
        for m in range(ceil((n-1)/2), n-1):       # n <= 2m+1 and m <= n-2
            yield n, m

# ---- Step 1: window cells
win = []
for n, m in conn_cells(16):
    if lo(n, m) <= min(hy(n, m), m):
        win.append((n, m, lo(n, m), min(hy(n, m), m)))
print("window cells (n,m,lo,hi):", win)
assert all(l == h for _, _, l, h in win), "some window cell admits more than one tau"
assert [(n, m) for n, m, _, _ in win] == [(5,3),(8,4),(10,6),(11,5),(12,9),(13,7),(14,11),(15,9),(15,10),(16,8),(16,13),(16,14)]
# window cells WITHOUT Henning-Yeo (what would have to be checked if K8 were dropped): lo <= m
win_nohy = [(n, m, lo(n, m), m) for n, m in conn_cells(15) if lo(n, m) <= m]
print("window cells n<=15 without HY (n,m,lo,m):", win_nohy)

# ---- Step 3: degree argument at n=16 (brute force over m and degree sequences, using only: P3 => m<=14, K8, Lemma A' on H-v)
feasible = []
for m in range(1, 15):
    for tau in range(7, m+1):
        if 17*tau > 5*16 + 3*m: continue                     # K8
        # for every vertex: tau(H-v) >= tau-1 and Lemma A': 11 tau(H-v) <= 3*15 + 2(m-d)
        dmax = None
        for d in range(0, m+1):
            ok = any(11*t <= 45 + 2*(m-d) for t in range(tau-1, tau+1))
            if ok: dmax = d
        if dmax is None: continue
        if 3*m > 16*dmax: continue                           # sum of degrees = 3m
        feasible.append((m, tau, dmax))
print("feasible (m, tau, max degree) at n=16 with tau>=7:", feasible)
assert feasible == [(14, 7, 3)]
# tau(H-v) for m=14, d=3: 11 t <= 45+22 = 67 -> t <= 6 ; and t >= 6
assert [t for t in range(0, 15) if 11*t <= 67 and t >= 6] == [6]
# minimum number of degree-3 vertices: 42 <= 3 d3 + 2 (16-d3)
print("min d3:", min(d3 for d3 in range(0, 17) if 3*d3 + 2*(16-d3) >= 42))

# ---- Step 4: slack cells for components (n<=15), with and without HY
def slack_cells(use_hy):
    out = []
    for n, m in conn_cells(15):
        for t in range(0, m+1):
            s = 3*n + 2*m - 11*t
            if s in (0, 1) and (not use_hy or 17*t <= 5*n + 3*m):
                out.append((n, m, t, s))
    return out
for use_hy in (True, False):
    sc = slack_cells(use_hy)
    print("HY" if use_hy else "noHY", "slack0:", [c[:3] for c in sc if c[3] == 0], "slack1:", [c[:3] for c in sc if c[3] == 1])
sc = slack_cells(False)
pieces = sc + [(1, 0, 0, 3)]     # isolated vertex has slack 3
# all multisets of pieces summing to (15 vertices, 11 edges) with total slack exactly 1 (no restriction on count of slack-1 pieces)
sols = []
def rec(i, n, m, s, chosen):
    if (n, m, s) == (15, 11, 1): sols.append(sorted(chosen)); return
    if i == len(pieces) or n > 15 or m > 11 or s > 1: return
    pn, pm, pt, ps = pieces[i]
    k = 0
    while n + k*pn <= 15 and m + k*pm <= 11 and s + k*ps <= 1:
        rec(i+1, n + k*pn, m + k*pm, s + k*ps, chosen + [pieces[i][:3]]*k)
        k += 1
rec(0, 0, 0, 0, [])
print("decompositions of (15,11) with total slack 1:", sols)
assert sorted(sols) == sorted([[(15,11,6)], sorted([(12,10,5),(3,1,1)])])
# cross-check: (13,8) with slack 0 (L007)
sols2 = []
def rec2(i, n, m, s, chosen):
    if (n, m, s) == (13, 8, 0): sols2.append(sorted(chosen)); return
    if i == len(pieces) or n > 13 or m > 8 or s > 0: return
    pn, pm, pt, ps = pieces[i]
    k = 0
    while n + k*pn <= 13 and m + k*pm <= 8 and s + k*ps <= 0:
        rec2(i+1, n + k*pn, m + k*pm, s + k*ps, chosen + [pieces[i][:3]]*k)
        k += 1
rec2(0, 0, 0, 0, [])
print("decompositions of (13,8) with total slack 0:", sols2)
# ---- Corollary 4: sizes n<=30 where beating 4/7 is arithmetically possible (HY + m<=n-2)
poss = []
for n in range(4, 31):
    h = -(-4*n//7) - 1; tau = n - h
    if any(17*tau <= 5*n + 3*m for m in range(0, n-1)) and tau <= n-2:
        poss.append(n)
print("sizes n<=30 where h<=ceil(4n/7)-1 is HY-feasible:", poss)
# ---- Step 7: C16 slack
n, m, t = 16, 13, 6
print("C16 slack:", 3*n + 2*m - 11*t, "HY ok:", 17*t <= 5*n + 3*m)
print("ALL ARITHMETIC CHECKS PASSED")
