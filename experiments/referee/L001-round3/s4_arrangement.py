"""S4: independent completeness check by the line arrangement of ALL formal sum relations.
No AP theory, no T0/T1/T2 case split, no weak-Sidon reduction.

Symbols: the points of the base set and two unknowns X, Y. Every pair of distinct 2-multisets
{s1,s2} != {s3,s4} of symbols gives a relation s1+s2 = s3+s4, i.e. aX + bY + c = 0.
 * a = b = 0: constant relation (always true or always false).
 * otherwise: a line in the (x,y)-plane.
The set of relations that hold at (x,y) (its 'type') determines whether the 16 values are distinct,
whether B = base u {x,y} is a (4,5)-set (|p-q| = |r-s| iff p+s = q+r or p+r = q+s) and every Sidon
subset of B (S is Sidon iff no two distinct 2-multisets from S have equal sums), hence h(B).
The type is constant on the open 2-cells (no line), on each line minus the other lines, and at each
vertex. A valid point lies on no 'pruned' line (lines X=c / Y=c with c in base or base u {c} not (4,5),
and X=Y), because every point of a pruned line is invalid. Hence the following test points cover
every valid (x,y) in R^2:
  (i) one point on no line at all; (ii) for each kept line, one point on it and on NO other line
  (pruned lines included); (iii) every intersection point of two kept lines.
Run: python3 -I s4_arrangement.py  (from this directory)."""
import itertools, json, sys, time
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from r3lib import A_BASE, is45_np, is45_py, h_sat

EXP = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'


def arrangement(base, label, verbose=True):
    t0 = time.time()
    base = [F(v) for v in base]
    BS = set(base)
    n = len(base)
    hb = h_sat(base)[0]
    X, Y = n, n + 1
    form = [(0, 0, b) for b in base] + [(1, 0, F(0)), (0, 1, F(0))]
    msets = [(i, j) for i in range(n + 2) for j in range(i, n + 2)]
    lines = {}
    n_true = 0
    for M1, M2 in itertools.combinations(msets, 2):
        a = form[M1[0]][0] + form[M1[1]][0] - form[M2[0]][0] - form[M2[1]][0]
        b = form[M1[0]][1] + form[M1[1]][1] - form[M2[0]][1] - form[M2[1]][1]
        c = form[M1[0]][2] + form[M1[1]][2] - form[M2[0]][2] - form[M2[1]][2]
        if a == 0 and b == 0:
            n_true += (c == 0)
            continue
        # normalise a*X + b*Y + c = 0 (a, b ints; c rational)
        D = c.denominator
        ai, bi, ci = a * D, b * D, int(c * D)
        g = gcd(gcd(abs(ai), abs(bi)), abs(ci))
        ai, bi, ci = ai // g, bi // g, ci // g
        if ai < 0 or (ai == 0 and bi < 0):
            ai, bi, ci = -ai, -bi, -ci
        lines.setdefault((ai, bi, ci), []).append((M1, M2))
    L = list(lines)
    single = {}

    def single_ok(v):
        if v not in single:
            single[v] = (v not in BS) and is45_np(base + [v])
        return single[v]

    def prunable(l):
        a, b, c = l
        if b == 0:
            return not single_ok(F(-c, a))
        if a == 0:
            return not single_ok(F(-c, b))
        if a == -b and c == 0:   # X = Y
            return True
        return False

    kept = [l for l in L if not prunable(l)]
    pruned = [l for l in L if prunable(l)]

    def on(l, x, y):
        return l[0] * x + l[1] * y + l[2] == 0

    def evaluate(x, y):
        if x == y or x in BS or y in BS or not single_ok(x) or not single_ok(y):
            return None
        B = base + [x, y]
        if not is45_np(B):
            return None
        return h_sat(B, start=hb + 2)[0]

    classes = []   # (kind, descriptor, point, h or None)
    # (i) generic point
    gx, gy = F(1234567, 1000003), F(7654321, 999983)
    assert not any(on(l, gx, gy) for l in L)
    classes.append(('generic', None, (gx, gy), evaluate(gx, gy)))
    # (ii) one point per kept line, on no other line; also one per pruned line (sanity: must be invalid)
    for group, kind in ((kept, 'line'), (pruned, 'pruned-line')):
        for l in group:
            a, b, c = l
            for k in range(1, 200):
                t = F(1000 * k + 7919 * k * k, 104729) + F(k, 7)
                x, y = (t, F(-c - a * t, b)) if b != 0 else (F(-c, a), t)
                assert on(l, x, y)
                if not any(on(m, x, y) for m in L if m != l):
                    break
            else:
                raise RuntimeError('no free point on line %s' % (l,))
            classes.append((kind, l, (x, y), evaluate(x, y)))
    # (iii) vertices of the kept arrangement
    verts = set()
    for l1, l2 in itertools.combinations(kept, 2):
        det = l1[0] * l2[1] - l2[0] * l1[1]
        if det == 0:
            continue
        x = F(-l1[2] * l2[1] + l2[2] * l1[1], det)
        y = F(-l1[0] * l2[2] + l2[0] * l1[2], det)
        verts.add((x, y))
    for (x, y) in verts:
        classes.append(('vertex', None, (x, y), evaluate(x, y)))
    if verbose:
        nX = sum(1 for l in L if l[1] == 0); nY = sum(1 for l in L if l[0] == 0)
        print('[%s] n=%d h(base)=%d | constant-true relations %d | distinct lines %d (X-only %d, Y-only %d, two-variable %d)'
              % (label, n, hb, n_true, len(L), nX, nY, len(L) - nX - nY))
        print('[%s] kept lines %d, pruned %d, vertices of kept arrangement %d' % (label, len(kept), len(pruned), len(verts)))
    return dict(hb=hb, L=L, kept=kept, pruned=pruned, classes=classes, time=time.time() - t0)


def summarize(R, label):
    cls = R['classes']
    hb = R['hb']
    pr = [c for c in cls if c[0] == 'pruned-line']
    print('[%s] pruned-line test points that are valid (must be 0): %d' % (label, sum(c[3] is not None for c in pr)))
    g = [c for c in cls if c[0] == 'generic'][0]
    print('[%s] generic point: h = %s' % (label, g[3]))
    ln = [c for c in cls if c[0] == 'line']
    bykind = {}
    for kind, l, p, h in ln:
        a, b, c = l
        if b == 0: k = 'X=c'
        elif a == 0: k = 'Y=c'
        elif (a, b) == (1, 1): k = 'X+Y=s'
        elif (a, b) == (1, -1): k = 'X-Y=d'
        else: k = '%dX%+dY' % (a, b)
        bykind.setdefault(k, {}).setdefault(h if h is not None else 'invalid', 0)
        bykind[k][h if h is not None else 'invalid'] += 1
    print('[%s] kept-line generic points by line kind: %s' % (label, bykind))
    vs = [c for c in cls if c[0] == 'vertex']
    vh = {}
    for _, _, p, h in vs:
        vh[h if h is not None else 'invalid'] = vh.get(h if h is not None else 'invalid', 0) + 1
    print('[%s] vertices: %d, outcome counts %s' % (label, len(vs), vh))
    defic = [c for c in cls if c[3] is not None and c[3] < hb + 2]
    print('[%s] valid classes with h < h(base)+2 = %d: %d' % (label, hb + 2, len(defic)))
    return defic


if __name__ == '__main__':
    t0 = time.time()
    A = [F(a) for a in A_BASE]
    R = arrangement(A, 'A_base')
    defic = summarize(R, 'A_base')
    valid_v = {frozenset(p) for kind, l, p, h in R['classes'] if kind == 'vertex' and h is not None}
    nord = sum(1 for kind, l, p, h in R['classes'] if kind == 'vertex' and h is not None)
    Rj = json.load(open(EXP + 'results.json'))
    stored = {frozenset((F(a), F(b))) for a, b, h in Rj['stored']}
    print('[A_base] valid vertices: %d ordered, %d unordered | == results.json stored set: %s'
          % (nord, len(valid_v), valid_v == stored))
    xc = sorted(F(-l[2], l[0]) for l in R['kept'] if l[1] == 0)
    print('[A_base] values c of kept lines X=c:', len(xc), '(these are the admissible special single coordinates)')
    json.dump({'kept_X_values': [str(c) for c in xc]}, open('s4_keptX.json', 'w'))
    print('[A_base] time %.1fs' % R['time'])
    # ---- positive controls: A' = A_base minus two points; A_base itself is a deficient extension of A'
    for p, q in ((F(0), F(246)), (F(243), F(249)), (F(528), F(1056))):
        Ap = [a for a in A if a not in (p, q)]
        lab = 'control A_base-{%s,%s}' % (p, q)
        Rc = arrangement(Ap, lab)
        dc = summarize(Rc, lab)
        through = [l for l in Rc['kept'] if l[0] * p + l[1] * q + l[2] == 0]
        hit = False
        for kind, l, pt, h in dc:
            if kind == 'vertex' and set(pt) == {p, q}: hit = True
            if kind == 'line' and len(through) == 1 and l == through[0]: hit = True
            if kind == 'generic' and not through: hit = True
        print('[%s] (p,q) lies on %d kept lines; detected as deficient: %s; time %.1fs' % (lab, len(through), hit, Rc['time']))
    print('total time %.1fs' % (time.time() - t0))
