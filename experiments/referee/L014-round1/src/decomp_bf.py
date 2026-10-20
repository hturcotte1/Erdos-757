"""Referee L014 r1: own brute force of the branches and decompositions of every recursion cell of the run, compared with the
branch data recorded in the INFO lines of the prover's cell files (no import of engine.py / decomp22.py).
Component types: isolated vertex (1,0,0) (slack 3), or connected (n,m,t): n >= 3, n <= 2m+1, m <= n-2 (P3), 1 <= t <= m,
I11 slack 3n+2m-11t >= 0 (L011, n <= 22).  K8 (17t <= 5n+3m) is applied separately so that its effect is visible.
Usage: python3 decomp_bf.py CELLDIR tree_keys.txt"""
import sys, json, math, glob, os
CD = sys.argv[1]
def types(N, S, k8):
    out = [((1, 0, 0), 3)] if S >= 3 else []
    for n in range(3, N + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            for t in range(1, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= S and (not k8 or 17 * t <= 5 * n + 3 * m): out.append(((n, m, t), s))
    return out
def decs(N, M, S, k8=True):
    P = types(N, S, k8); res = []
    def rec(i, n, m, s, ch):
        if n == N and m == M and s == S: res.append(tuple(sorted(ch))); return
        if i == len(P) or n >= N: return
        (pn, pm, pt), ps = P[i]
        k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, ch + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(set(res))
def size(n, m, t, D):
    if (n, m, t) == (1, 0, 0): return 1
    fn = '%s/cell_%d_%d_%d_D%d.txt' % (CD, n, m, t, D)
    if not os.path.exists(fn): return None
    return sum(1 for l in open(fn) if l.startswith('FOUND'))
from math import comb
from collections import Counter
nb = nd = ndiff = 0; extra_noK8 = 0; inp_bad = 0
for fn in sorted(glob.glob(CD + '/cell_*.txt')):
    info = None
    for l in open(fn):
        if l.startswith('INFO '): info = json.loads(l[5:])
    if info is None or info.get('route') != 'recurse': continue
    n, m, t, D = map(int, os.path.basename(fn)[5:-4].replace('D', '').split('_'))
    mine_br = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp >= 0 and tp >= 0: mine_br.append((d, tp, Sp))
    theirs_br = [(b['d'], b['tp'], b['Sp']) for b in info['branches']]
    if mine_br != theirs_br: print('BRANCH DIFF', (n, m, t, D), mine_br, theirs_br); ndiff += 1
    for b in info['branches']:
        nb += 1
        d, tp, Sp = b['d'], b['tp'], b['Sp']
        mine = decs(n - 1, m - d, Sp); mine_nok8 = decs(n - 1, m - d, Sp, k8=False)
        theirs = sorted(tuple(sorted(tuple(x) for x in dec)) for dec, sz in b['dec'])
        nd += len(mine)
        if mine != theirs: print('DEC DIFF', (n, m, t, D), (d, tp, Sp), set(mine) ^ set(theirs)); ndiff += 1
        ex = set(mine_nok8) - set(mine)
        if ex:
            extra_noK8 += len(ex)
            print('  without K8 also:', (n, m, t, D), (d, tp, Sp), sorted(ex))
        # input counts recomputed from list sizes (multisets for repeated types)
        tot = 0
        for dec, sz in b['dec']:
            c = Counter(tuple(x) for x in dec); s = 1
            for typ, k in c.items():
                L = size(typ[0], typ[1], typ[2], d)
                if L is None: s = None; break
                s *= comb(L + k - 1, k)
            if s != sz: print('INPUT COUNT DIFF', (n, m, t, D), dec, s, sz); inp_bad += 1
            tot += sz if s is None else s
        if tot != b['inputs']: print('TOTAL INPUT DIFF', (n, m, t, D), tot, b['inputs']); inp_bad += 1
print('SUMMARY recursion branches', nb, 'decompositions', nd, 'differences', ndiff, 'extra decompositions without K8', extra_noK8, 'input-count differences', inp_bad)
