"""Step 4: independent COMPLETENESS check by a line arrangement (no AP theory, no T0/T1/T2 split).

Symbols: A (14 integers), X, Y.  For each unordered pair of distinct 2-multisets {u1,u2} != {u3,u4} of symbols, the
formal relation u1+u2 = u3+u4 is linear in (X,Y): al*X + be*Y = ga.  If al = be = 0 it is constant (independent of x,y).
Otherwise it defines a line in R^2.  The 'type' of (x,y) = set of formal relations that hold; distinctness of the 16
points, the (4,5) property (|u1-u2|=|u3-u4| <=> u1+u4=u2+u3 or u1+u3=u2+u4) and the Sidon property of every subset are
functions of the type.  The type is constant on: the complement of all lines; the points of a line lying on no other
line.  So it suffices to check
  R0: a point on no line;   R1: for every line, a point on it and on no other line;   R3: every vertex.
Pruning (justified): a line X = c with A u {c} not (4,5) or c in A carries no admissible point (A u {c} subset of B);
same for Y = c; the line X = Y carries no admissible point.  Vertices on such a line are skipped for the same reason.
"""
import itertools, sys, time, random, json
from math import gcd
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *

t0 = time.time()
A = ABASE
NS = 16  # 0..13 = A, 14 = X, 15 = Y
ms = [(i, j) for i in range(NS) for j in range(i, NS)]
lines = {}
nconst_true = 0
for m1, m2 in itertools.combinations(ms, 2):
    c = [0] * NS
    for s in m1: c[s] += 1
    for s in m2: c[s] -= 1
    al, be = c[14], c[15]
    ga = -sum(c[i] * A[i] for i in range(14))
    if al == 0 and be == 0:
        if ga == 0:
            nconst_true += 1
        continue
    g = gcd(gcd(abs(al), abs(be)), abs(ga))
    al, be, ga = al // g, be // g, ga // g
    if al < 0 or (al == 0 and be < 0):
        al, be, ga = -al, -be, -ga
    lines.setdefault((al, be, ga), []).append((m1, m2))
print('formal relations constant & true (pure-A relations, i.e. A\'s own coincidences):', nconst_true)
L = list(lines)
Xonly = [l for l in L if l[1] == 0]
Yonly = [l for l in L if l[0] == 0]
two = [l for l in L if l[0] != 0 and l[1] != 0]
print('lines:', len(L), '| X-only:', len(Xonly), '| Y-only:', len(Yonly), '| two-variable:', len(two))
print('two-variable coefficient patterns:', sorted({(l[0], l[1]) for l in two}))
CX = {F(l[2], l[0]) for l in Xonly}
CY = {F(l[2], l[1]) for l in Yonly}
print('CX == CY:', CX == CY, '| |CX| =', len(CX))
Aset = {F(a) for a in A}
validX = sorted(c for c in CX if c not in Aset and is45([F(a) for a in A] + [c]))
validY = sorted(c for c in CY if c not in Aset and is45([F(a) for a in A] + [c]))
print('valid special single values: |validX| =', len(validX), '| validX == validY:', validX == validY)
s2 = json.load(open('s2_t1_out.json'))
print('validX == P_ok of step 2 (scaled back):', validX == sorted(F(v, s2['scale']) for v in s2['Pok']))
badX = CX - set(validX)
badY = CY - set(validY)

valid_lines = [l for l in two if l != (1, -1, 0)] + [l for l in Xonly if F(l[2], l[0]) in set(validX)] + \
              [l for l in Yonly if F(l[2], l[1]) in set(validY)]
print('valid lines:', len(valid_lines))


def on(l, x, y):
    return l[0] * x + l[1] * y == l[2]


def admissible(x, y):
    return x != y and x not in Aset and y not in Aset and x not in badX and y not in badY


rng = random.Random(99)
stats = {}
hvals = {}


def judge_point(tag, x, y):
    B = [F(a) for a in A] + [x, y]
    ok = admissible(x, y) and is45(B)
    if not ok:
        stats[(tag, 'not45')] = stats.get((tag, 'not45'), 0) + 1
        return None
    h = hmax_brute(B, 10)[0]
    stats[(tag, 'h=%d' % h)] = stats.get((tag, 'h=%d' % h), 0) + 1
    return h


# R0
for _ in range(5):
    while True:
        x = F(rng.randrange(-10 ** 10, 10 ** 10), 1000003)
        y = F(rng.randrange(-10 ** 10, 10 ** 10), 999983)
        if not any(on(l, x, y) for l in L):
            break
    judge_point('R0-generic-plane', x, y)
# R1: every valid line (invalid lines carry no admissible points)
for l in valid_lines:
    for _ in range(2):
        while True:
            t = F(rng.randrange(-10 ** 10, 10 ** 10), 1000003)
            if l[1] != 0:
                x = t; y = (l[2] - l[0] * x) / l[1]
            else:
                y = t; x = F(l[2], l[0])
            if not any(on(m, x, y) for m in L if m != l):
                break
        assert on(l, x, y)
        kind = 'X-only' if l[1] == 0 else ('Y-only' if l[0] == 0 else 'two%s' % str((l[0], l[1])))
        judge_point('R1-' + kind, x, y)
print('R0/R1 done t=%.1f' % (time.time() - t0), flush=True)
# R3: vertices of the arrangement of valid lines
verts = set()
for l1, l2 in itertools.combinations(valid_lines, 2):
    det = l1[0] * l2[1] - l2[0] * l1[1]
    if det == 0:
        continue
    x = F(l1[2] * l2[1] - l2[2] * l1[1], det)
    y = F(l1[0] * l2[2] - l2[0] * l1[2], det)
    verts.add((x, y))
print('vertices of the valid-line arrangement:', len(verts), flush=True)
adm = [(x, y) for x, y in verts if admissible(x, y)]
print('admissible vertices (coordinates distinct, not in A, not on an invalid single line):', len(adm), flush=True)
v45 = [(x, y) for x, y in adm if is45([F(a) for a in A] + [x, y])]
print('(4,5) vertices (ordered):', len(v45), ' t=%.1f' % (time.time() - t0), flush=True)
unordered = {frozenset(p) for p in v45}
print('(4,5) vertices (unordered):', len(unordered))
hd = {}
for pr in unordered:
    x, y = sorted(pr)
    h = hmax_brute([F(a) for a in A] + [x, y], 10)[0]
    hd[h] = hd.get(h, 0) + 1
print('h distribution over (4,5) vertices:', hd)
st = {frozenset((F(p[0], s2['scale']), F(p[1], s2['scale']))) for p in s2['good']}
print('(4,5) vertex set == step-2 T1b (4,5) set:', unordered == st, '| sizes', len(unordered), len(st))
for k in sorted(stats):
    print('  ', k, stats[k])
print('time %.1fs' % (time.time() - t0))
