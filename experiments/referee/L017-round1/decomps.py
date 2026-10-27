# Referee L017 round 1: independent enumeration of the degree-3 branch decompositions at the 17 top-level violator
# cells of L013/L016 (Theorem 6(iii), C4), and of the slack-0 decompositions of (28,24) (Remark 13.4).
import json, os, math, itertools
from math import comb
HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, 'cell_inventory.json')))
def conn_cells(nmax):
    res = []
    for n in range(3, nmax + 1):
        for m in range(math.ceil((n - 1) / 2), n - 1):
            for t in range(1, m + 1):
                s = 3*n + 2*m - 11*t
                if s < 0: continue
                if 17*t > 5*n + 3*m: continue
                res.append((n, m, t, s))
    return res
def count3(n, m, t):
    key = '%d_%d_%d' % (n, m, t)
    if key not in inv: return None
    for (D, cnt, cnt3, path, ninfo) in inv[key]:
        if D >= 3: return cnt3
    return None
def decomps(N, M, S, maxparts=12):
    cells = [c for c in conn_cells(N) if c[3] <= S]
    out = []
    def rec(i, n, m, s, cur):
        if n == N and m == M and s == S:
            out.append(list(cur)); return
        if i >= len(cells) or n >= N: return
        c = cells[i]
        # use cell i k times
        k = 0
        while True:
            nn, mm, ss = n + k*c[0], m + k*c[1], s + k*c[3]
            if nn > N or mm > M or ss > S: break
            rec(i + 1, nn, mm, ss, cur + [c[:3]]*k)
            k += 1
    rec(0, 0, 0, 0, [])
    return out
def inputs(dec):
    tot = 1
    from collections import Counter
    for cell, k in Counter(dec).items():
        c = count3(*cell)
        if c is None: return None
        tot *= comb(c + k - 1, k)
    return tot
TOP = [(23,14,9),(23,20,10),(24,13,9),(24,18,10),(25,17,10),(25,22,11),(26,15,10),(26,21,11),(27,14,10),(27,19,11),(27,25,12)]
tot = {'decs': 0, 'r>=4': 0, 'r>=4 with inputs': 0, 'inputs r>=4': 0}
for (n, m, t) in TOP:
    s = 3*n + 2*m - 11*t
    S = s + 2  # degree-3 branch, t' = t - 1
    ds = decomps(n - 1, m - 3, S)
    ds = [d for d in ds if sum(c[2] for c in d) == t - 1]
    print((n, m, t, 3), 's=%d' % s, 'S\'=%d' % S, len(ds), 'decompositions of (%d,%d)' % (n - 1, m - 3))
    r3 = 0
    for d in ds:
        r = len(d); inp = inputs(d)
        print('    r=%d %s inputs=%s' % (r, d, inp))
        tot['decs'] += 1
        if r >= 4:
            tot['r>=4'] += 1
            if inp: tot['r>=4 with inputs'] += 1; tot['inputs r>=4'] += inp
        elif inp: r3 += inp
    print('    inputs from r<=3:', r3)
print(tot)
print('slack-0 decompositions of (28,24):', [d for d in decomps(28, 24, 0) if sum(c[2] for c in d) == 12])
print('slack-0/1 decompositions of (27,15) and (27,20):', decomps(27, 15, 1), decomps(27, 20, 0))
