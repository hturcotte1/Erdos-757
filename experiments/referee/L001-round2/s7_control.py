"""Step 7: positive control for the line-arrangement check of step 4.
Same algorithm as s4_arrangement.py, packaged as a function of the base set A0.  For A0 = A_base minus {p,q},
A_base itself is a 2-point extension with h(A_base)=8 < h(A0)+2, so the check MUST report the pair (p,q)."""
import itertools, sys, time, random
from math import gcd
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *


def arrangement(A0, seed=1):
    A0 = sorted(A0)
    n0 = len(A0)
    NS = n0 + 2
    ms = [(i, j) for i in range(NS) for j in range(i, NS)]
    lines = set()
    for m1, m2 in itertools.combinations(ms, 2):
        c = [0] * NS
        for s in m1: c[s] += 1
        for s in m2: c[s] -= 1
        al, be = c[n0], c[n0 + 1]
        ga = -sum(c[i] * A0[i] for i in range(n0))
        if al == 0 and be == 0:
            continue
        g = gcd(gcd(abs(al), abs(be)), abs(ga))
        al, be, ga = al // g, be // g, ga // g
        if al < 0 or (al == 0 and be < 0):
            al, be, ga = -al, -be, -ga
        lines.add((al, be, ga))
    L = list(lines)
    AF = [F(a) for a in A0]
    Aset = set(AF)
    CX = {F(l[2], l[0]) for l in L if l[1] == 0}
    CY = {F(l[2], l[1]) for l in L if l[0] == 0}
    validX = {c for c in CX if c not in Aset and is45(AF + [c])}
    validY = {c for c in CY if c not in Aset and is45(AF + [c])}
    badX, badY = CX - validX, CY - validY
    VL = [l for l in L if l[0] != 0 and l[1] != 0 and l != (1, -1, 0)] + \
         [l for l in L if l[1] == 0 and F(l[2], l[0]) in validX] + [l for l in L if l[0] == 0 and F(l[2], l[1]) in validY]
    on = lambda l, x, y: l[0] * x + l[1] * y == l[2]
    adm = lambda x, y: x != y and x not in Aset and y not in Aset and x not in badX and y not in badY
    h0 = hmax_brute(AF, 1)[0]
    rng = random.Random(seed)
    results = []   # (kind, x, y, h)
    for _ in range(3):
        while True:
            x = F(rng.randrange(-10 ** 10, 10 ** 10), 1000003); y = F(rng.randrange(-10 ** 10, 10 ** 10), 999983)
            if not any(on(l, x, y) for l in L): break
        if adm(x, y) and is45(AF + [x, y]):
            results.append(('plane', x, y, hmax_brute(AF + [x, y], h0 + 2)[0]))
    for l in VL:
        while True:
            t = F(rng.randrange(-10 ** 10, 10 ** 10), 1000003)
            if l[1] != 0: x = t; y = (l[2] - l[0] * x) / l[1]
            else: y = t; x = F(l[2], l[0])
            if not any(on(m, x, y) for m in L if m != l): break
        if adm(x, y) and is45(AF + [x, y]):
            results.append(('line%s' % str(l), x, y, hmax_brute(AF + [x, y], h0 + 2)[0]))
    verts = set()
    for l1, l2 in itertools.combinations(VL, 2):
        det = l1[0] * l2[1] - l2[0] * l1[1]
        if det == 0: continue
        verts.add((F(l1[2] * l2[1] - l2[2] * l1[1], det), F(l1[0] * l2[2] - l2[0] * l1[2], det)))
    seen = set()
    for x, y in verts:
        if not adm(x, y) or frozenset((x, y)) in seen: continue
        seen.add(frozenset((x, y)))
        if is45(AF + [x, y]):
            results.append(('vertex', x, y, hmax_brute(AF + [x, y], h0 + 2)[0]))
    return h0, len(L), len(VL), len(verts), results


t0 = time.time()
for p, q in [(0, 246), (243, 249), (528, 1056)]:
    A0 = [a for a in ABASE if a not in (p, q)]
    h0, nl, nvl, nv, res = arrangement(A0)
    bad = [(k, x, y, h) for k, x, y, h in res if h < h0 + 2]
    hit = [r for r in bad if {r[1], r[2]} == {F(p), F(q)}]
    print('A0 = A_base - {%d,%d}: h(A0)=%d lines=%d valid=%d vertices=%d (4,5)-classes=%d | classes with h<h0+2: %d | '
          'pair (%d,%d) reported: %s %s | t=%.0fs' % (p, q, h0, nl, nvl, nv, len(res), len(bad), p, q, bool(hit),
                                                      [(r[0], r[3]) for r in hit], time.time() - t0), flush=True)
