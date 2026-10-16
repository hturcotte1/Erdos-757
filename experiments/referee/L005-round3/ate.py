"""Referee round 3, independent check of my own design: ARRANGEMENT-TYPE ENUMERATION (ATE).
Imports nothing from e757/, judge/ or the authors' experiment folder.

For a class A and B = A u {X,Y}: every additive relation u1+u2 = u3+u4 between two different 2-multisets of
symbols of B that involves X or Y is a line aX+bY=c in the (x,y)-plane.  Every distance equality |p-q|=|r-s| in B
and every failure of the Sidon property of a subset of B is such a relation, so distinctness, the (4,5) property and
h(B) depend only on the TYPE of (x,y), i.e. the set of relation lines through it.
Line kinds: E (relation reduces to u=v: X=a, Y=a, X=Y; excluded points), F (some relation on the line has 4 distinct
symbols: then that 4-subset of B has <=4 distances, so no point of an F line is (4,5)), G (only 3-AP relations).
Coverage: a non-excluded point is (i) on no line -> generic-plane representative; (ii) on exactly one line ->
that line's generic representative (chosen exactly on no other line); (iii) on >=2 lines -> on an F line (not (4,5))
or an intersection point of two G lines (all enumerated).  Every representative and every G x G intersection point
is tested DIRECTLY: distinctness, (4,5) by counting distances in ALL 1820 4-subsets, and h(B) from the definition
(Sidon = all positive differences distinct): exists Sidon 10-subset among all C(16,10), no Sidon 11-subset among all
C(16,11).  h(A) is computed the same way.  F-line representatives are also tested directly (lemma check).
Usage: python3 ate.py OUT.jsonl idx[,idx...] [--control]   (--control: run on A minus one point, expect deficits)
"""
import gzip, itertools, json, os, random, sys, time
from fractions import Fraction as Fr
from math import gcd, lcm
import numpy as np

CENSUS = '/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz'

def load_classes(idxs):
    want = set(idxs); out = {}
    with gzip.open(CENSUS, 'rt') as f:
        for i, line in enumerate(f):
            if i in want: out[i] = json.loads(line)['set']
    return out

def norm_line(a, b, c):
    g = gcd(a, b); a //= g; b //= g; c = Fr(c) / g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return (a, b, c)

def build_lines(A):
    n = len(A)
    ms = list(itertools.combinations_with_replacement(range(n + 2), 2))   # 0 = X, 1 = Y, 2.. = A
    def lin(p):
        return (sum(1 for i in p if i == 0), sum(1 for i in p if i == 1), sum(A[i - 2] for i in p if i >= 2))
    L = {}
    for p, q in itertools.combinations(ms, 2):
        (xp, yp, cp), (xq, yq, cq) = lin(p), lin(q)
        a, b, c = xp - xq, yp - yq, cq - cp
        if a == 0 and b == 0: continue
        sp, sq = set(p), set(q)
        if (sp & sq) or (len(sp) == 1 and len(sq) == 1): kind = 'E'
        elif len(sp) == 2 and len(sq) == 2: kind = 'F'
        else: kind = 'G'
        L.setdefault(norm_line(a, b, c), set()).add(kind)
    return {k: ('E' if 'E' in v else 'F' if 'F' in v else 'G') for k, v in L.items()}

class Tester:
    def __init__(self, N):
        self.N = N
        self.Q4 = np.array(list(itertools.combinations(range(N), 4)), dtype=np.int64)
        self.P4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
        self.sub = {}
    def _subs(self, k):
        if k not in self.sub:
            idx = np.array(list(itertools.combinations(range(self.N), k)), dtype=np.int64)
            I, J = np.triu_indices(k, 1)
            self.sub[k] = (idx, I, J)
        return self.sub[k]
    def is45(self, Bv):
        V = Bv[self.Q4]
        D = np.stack([np.abs(V[:, j] - V[:, i]) for i, j in self.P4], axis=1)
        D.sort(axis=1)
        nd = 1 + (D[:, 1:] != D[:, :-1]).sum(axis=1)
        return bool((nd >= 5).all())
    def n_sidon(self, Bv, k):
        idx, I, J = self._subs(k)
        V = np.sort(Bv)[idx]
        D = V[:, J] - V[:, I]
        D.sort(axis=1)
        dup = (D[:, 1:] == D[:, :-1]).any(axis=1)
        return int((~dup).sum())
    def h(self, Bv, lo):
        """exact h for |B| = N assuming h >= lo is to be tested: returns largest k in [lo-1 .. ] with a Sidon k-subset"""
        k = lo
        if self.n_sidon(Bv, k) == 0:
            while k > 1 and self.n_sidon(Bv, k - 1) == 0: k -= 1
            return k - 1
        while k < self.N and self.n_sidon(Bv, k + 1) > 0: k += 1
        return k

def to_int(A, pts):
    D = 1
    for p in pts: D = lcm(D, p.denominator)
    return np.array(sorted([a * D for a in A] + [int(p * D) for p in pts]), dtype=np.int64)

def run_class(idx, A, control=False):
    t0 = time.time()
    A = sorted(A)
    assert len(A) == len(set(A))
    n = len(A)
    rng = random.Random(1000003 * (idx + 1) + n)
    TA = Tester(n); TB = Tester(n + 2)
    Av = np.array(A, dtype=np.int64)
    A45 = TA.is45(Av)
    hA = TA.h(Av, 8 if n == 14 else 7)
    target = hA + 2
    L = build_lines(A)
    kinds = {}
    for k, v in L.items(): kinds[v] = kinds.get(v, 0) + 1
    E_lines = sorted(k for k, v in L.items() if v == 'E')
    expectE = {(1, 0, Fr(a)) for a in A} | {(0, 1, Fr(a)) for a in A} | {(1, -1, Fr(0))}
    assert set(E_lines) == expectE, 'unexpected E lines'
    bydir = {}
    for (a, b, c), v in L.items(): bydir.setdefault((a, b), {})[c] = v
    dirs = list(bydir)
    def through(x, y):
        out = []
        for (a, b) in dirs:
            c = a * x + b * y
            v = bydir[(a, b)].get(c)
            if v is not None: out.append(((a, b, c), v))
        return out
    span = A[-1] - A[0]
    def rnd():
        return Fr(rng.randrange(A[0] - span, A[-1] + span), 1) + Fr(rng.randrange(1, 6), 7)
    res = {'class': idx, 'n': n, 'A45': A45, 'hA': hA, 'lines': kinds, 'control': control}
    deficits = []
    # (0) generic plane point
    while True:
        x, y = rnd(), rnd()
        if not through(x, y): break
    Bv = to_int(A, [x, y]); assert len(set(Bv.tolist())) == n + 2
    g45 = TB.is45(Bv); gh = TB.h(Bv, target)
    res['generic'] = {'is45': g45, 'h': gh}
    if g45 and gh < target: deficits.append(('generic', str(x), str(y), gh))
    # (1) generic representative of every non-E line
    rep_stats = {}
    for (a, b, c), v in L.items():
        if v == 'E': continue
        for _ in range(200):
            t = rnd()
            if b == 0: x, y = c / a, t
            else: x, y = t, (c - a * t) / b
            th = through(x, y)
            if len(th) == 1 and th[0][0] == (a, b, c): break
        else:
            raise RuntimeError('no generic point found on line')
        Bv = to_int(A, [x, y]); assert len(set(Bv.tolist())) == n + 2
        is45 = TB.is45(Bv)
        key = (v, 'vert' if b == 0 else 'hor' if a == 0 else 'slant')
        st = rep_stats.setdefault('%s-%s' % key, {'lines': 0, 'is45': 0, 'h_hist': {}})
        st['lines'] += 1
        if is45:
            if v == 'F': deficits.append(('LEMMA-VIOLATION F line (4,5)', str((a, b, c))))
            st['is45'] += 1
            hh = TB.h(Bv, target)
            st['h_hist'][str(hh)] = st['h_hist'].get(str(hh), 0) + 1
            if hh < target: deficits.append(('line', str((a, b, c)), str(x), str(y), hh))
    res['line_reps'] = rep_stats
    # (2) all intersection points of two G lines
    G = [k for k, v in L.items() if v == 'G']
    pts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(G, 2):
        det = a1 * b2 - a2 * b1
        if det == 0: continue
        x = (c1 * b2 - c2 * b1) / det; y = (a1 * c2 - a2 * c1) / det
        pts.add((x, y))
    n_excl = n_onF = n_test = 0; n45 = 0; lemma_viol = 0; hh_hist = {}; pairs45 = set(); asym = 0
    for (x, y) in pts:
        th = through(x, y)
        ks = {v for _, v in th}
        assert len(th) >= 2 and 'G' in ks
        if 'E' in ks: n_excl += 1; continue
        Bv = to_int(A, [x, y]); assert len(set(Bv.tolist())) == n + 2
        is45 = TB.is45(Bv)          # tested directly for every non-excluded intersection point
        if 'F' in ks:
            n_onF += 1
            if is45: lemma_viol += 1
            continue
        n_test += 1
        if not is45: continue
        n45 += 1
        if (y, x) not in pts: asym += 1
        key = (min(x, y), max(x, y))
        if key in pairs45: continue
        pairs45.add(key)
        hh = TB.h(Bv, target)
        hh_hist[str(hh)] = hh_hist.get(str(hh), 0) + 1
        if hh < target: deficits.append(('point', str(x), str(y), hh))
    res.update({'G_lines': len(G), 'GxG_points': len(pts), 'GxG_excluded': n_excl, 'GxG_onF': n_onF,
                'GxG_onF_but_45 (lemma violations)': lemma_viol, 'GxG_onlyG': n_test, 'GxG_45_ordered': n45,
                'GxG_45_unordered': len(pairs45), 'asymmetric': asym, 'GxG_h_hist': hh_hist,
                'deficits': deficits[:50], 'n_deficits': len(deficits), 'target': target,
                'secs': round(time.time() - t0, 1)})
    res['pairs45'] = sorted([str(p), str(q)] for p, q in pairs45)
    return res

def main():
    try: os.nice(10)
    except Exception: pass
    out = sys.argv[1]
    idxs = [int(s) for s in sys.argv[2].split(',')]
    control = '--control' in sys.argv
    sets = load_classes(idxs)
    with open(out, 'a') as fo:
        for i in idxs:
            A = sets[i]
            if control:
                for p in (A[0], sorted(A)[5]):
                    Ac = [a for a in A if a != p]
                    r = run_class(i, Ac, control=True); r['removed'] = p
                    fo.write(json.dumps(r) + '\n'); fo.flush()
                    print('CONTROL class', i, 'minus', p, 'hA', r['hA'], 'n_deficits', r['n_deficits'],
                          'first', r['deficits'][:3], r['secs'], 's', flush=True)
            else:
                r = run_class(i, A)
                fo.write(json.dumps(r) + '\n'); fo.flush()
                print('class', i, {k: r[k] for k in ('A45', 'hA', 'lines', 'G_lines', 'GxG_points', 'GxG_excluded', 'GxG_onF',
                      'GxG_onF_but_45 (lemma violations)', 'GxG_onlyG', 'GxG_45_ordered', 'GxG_45_unordered', 'asymmetric',
                      'GxG_h_hist', 'n_deficits', 'secs')}, flush=True)
                print('   generic', r['generic'], 'line_reps', r['line_reps'], flush=True)

if __name__ == '__main__':
    main()
