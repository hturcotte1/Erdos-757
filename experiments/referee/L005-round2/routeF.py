"""Referee round 2 for L005, Route F: exact deficient locus over all of R^2, written from scratch (imports nothing from
e757/, judge/, the authors' folder or the round-1 referee folder).

For a 14-point (4,5)-set A with h(A)=8 and its maximum Sidon sets M (difference-definition DFS):
  B = A u {x,y} (x != y, x,y not in A) has h(B) = 10  iff  some S in M has S u {x,y} Sidon
  (a Sidon 10-subset of B meets A in at most 8 points, so it is S u {x,y} with S a Sidon 8-subset of A).
Deficient locus D = {(x,y) admissible : for all S in M, S u {x,y} is not Sidon}.
K(S) := {(x,y): S u {x,y} not Sidon} is, for admissible (x,y), the union of the lines
   x = v, y = v (v in V(S) = {q+r-p : p not in {q,r}} u {(q+r)/2 : q != r}),
   x + y = p + q (p <= q),  x - y = q - p (p != q),  2x - y = p,  2y - x = p,  x = y.
D is contained in K(S_0). For every line l of K(S_0): if l is a line of K(S) for every S, l is a whole line of D (it must
carry a symbolic 4-point witness of non-(4,5), checked with linear forms, unless it is x=a, y=a (a in A) or x=y);
otherwise D n l is contained in the finite set l n K(S*) for the first S* not containing l, and every such point is filtered
by the DEFINITION (S u {x,y} not Sidon for every S in M). Every surviving admissible point is tested exactly for (4,5);
any (4,5) one would be a counterexample (h computed by brute force on all 10-subsets).
A self-test checks the line description of K(S) against the definition on random and special points.
Usage: python3 routeF.py CENSUS.jsonl.gz OUT.jsonl IDX [IDX ...]
"""
import gzip, itertools, json, random, sys, time
from fractions import Fraction as Fr
from math import gcd

SCALE = 12


def sidon_max_all(P):
    P = sorted(P); n = len(P); best = [0]; sets = []
    def rec(i, ch, diffs):
        if len(ch) + (n - i) < best[0]:
            return
        if i == n:
            if len(ch) > best[0]:
                best[0] = len(ch); sets.clear()
            if len(ch) == best[0]:
                sets.append(tuple(ch))
            return
        v = P[i]; nd = [v - c for c in ch]
        if len(set(nd)) == len(nd) and not (set(nd) & diffs):
            rec(i + 1, ch + [v], diffs | set(nd))
        rec(i + 1, ch, diffs)
    rec(0, [], frozenset())
    return best[0], sets


def is_sidon(T):
    T = list(T)
    d = [abs(u - v) for u, v in itertools.combinations(T, 2)]
    return len(d) == len(set(d))


def norm(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return (a, b, c)


def V_of(S):
    Ss = set(S); out = set()
    for q, r in itertools.combinations_with_replacement(S, 2):
        for p in S:
            if p != q and p != r:
                out.add(q + r - p)
    for q, r in itertools.combinations(S, 2):
        assert (q + r) % 2 == 0
        out.add((q + r) // 2)
    return out - Ss


def lines_of(S):
    L = set()
    for v in V_of(S):
        L.add(norm(1, 0, v)); L.add(norm(0, 1, v))
    for p, q in itertools.combinations_with_replacement(S, 2):
        L.add(norm(1, 1, p + q))
    for p, q in itertools.permutations(S, 2):
        L.add(norm(1, -1, q - p))
    for p in S:
        L.add(norm(2, -1, p)); L.add(norm(-1, 2, p))
    L.add(norm(1, -1, 0))
    return L


def on_some_line(x, y, L):
    return any(a * x + b * y == c for a, b, c in L)


def isect(l1, l2):
    a1, b1, c1 = l1; a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    xn = c1 * b2 - c2 * b1; yn = a1 * c2 - a2 * c1
    x = xn // det if xn % det == 0 else Fr(xn, det)
    y = yn // det if yn % det == 0 else Fr(yn, det)
    return (x, y)


def nd4(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})


def is45_ext(A, x, y):
    for q in itertools.combinations(A, 3):
        if nd4((x,) + q) < 5 or nd4((y,) + q) < 5:
            return False
    for q in itertools.combinations(A, 2):
        if nd4((x, y) + q) < 5:
            return False
    return True


def h_brute(B):
    B = sorted(B)
    for k in range(len(B), 0, -1):
        for T in itertools.combinations(B, k):
            if is_sidon(T):
                return k
    return 0


def line_param(l):
    """return (x0,y0,dx,dy) with (x0+t dx, y0+t dy) running over l (rational x0,y0)."""
    a, b, c = l
    if b != 0:
        return (Fr(0), Fr(c, b), Fr(b), Fr(-a))   # x = b t, y = (c - a b t)/b
    return (Fr(c, a), Fr(0), Fr(0), Fr(1))


def symbolic_witness(A, l):
    """find a 4-subset of A u {X(t),Y(t)} containing X or Y with <= 4 distinct |differences| identically in t."""
    x0, y0, dx, dy = line_param(l)
    X = (dx, x0); Y = (dy, y0)                  # linear forms (slope, const)
    pts = [('X', X), ('Y', Y)] + [(a, (Fr(0), Fr(a))) for a in A]
    def canon(f):
        s, c = f
        if s < 0 or (s == 0 and c < 0):
            return (-s, -c)
        return (s, c)
    for q in itertools.combinations(pts, 4):
        names = [p[0] for p in q]
        if 'X' not in names and 'Y' not in names:
            continue
        ds = set()
        for (_, f), (_, g) in itertools.combinations(q, 2):
            ds.add(canon((f[0] - g[0], f[1] - g[1])))
        if (Fr(0), Fr(0)) in ds:
            continue   # degenerate identically (cannot happen for distinct names unless X == a identically)
        if len(ds) <= 4:
            return [str(n) for n in names]
    return None


def analyse(A0, idx, rng):
    t0 = time.time()
    A = sorted(SCALE * a for a in A0); Aset = set(A)
    h, M = sidon_max_all(A)
    assert h == 8
    LS = [lines_of(S) for S in M]
    DS = [set(abs(u - v) for u, v in itertools.combinations(S, 2)) for S in M]
    # ---- self-test of the line description against the definition
    st_n = 0; st_bad = 0
    for _ in range(4):
        j = rng.randrange(len(M)); S = M[j]; L = LS[j]
        Ll = list(L)
        pts = []
        for _ in range(300):
            pts.append((rng.randint(A[0] - 200, A[-1] + 200), rng.randint(A[0] - 200, A[-1] + 200)))
        for _ in range(600):
            p = isect(rng.choice(Ll), rng.choice(Ll))
            if p is not None: pts.append(p)
        for _ in range(300):
            a, b, c = rng.choice(Ll)
            if b != 0:
                xx = rng.randint(A[0] - 200, A[-1] + 200); yy = Fr(c - a * xx, b)
                if yy.denominator == 1: yy = int(yy)
            else:
                yy = rng.randint(A[0] - 200, A[-1] + 200); xx = Fr(c, a)
                if xx.denominator == 1: xx = int(xx)
            pts.append((xx, yy))
        for x, y in pts:
            if x == y or x in S or y in S:
                continue
            st_n += 1
            if (not is_sidon(list(S) + [x, y])) != on_some_line(x, y, L):
                st_bad += 1
    # ---- locus
    L0 = LS[0]
    excluded = set()
    for a in A:
        excluded.add(norm(1, 0, a)); excluded.add(norm(0, 1, a))
    excluded.add(norm(1, -1, 0))
    whole = []; Dpts = set(); ncand = 0; nfrac = 0
    for l in sorted(L0):
        jstar = None
        for j in range(1, len(M)):
            if l not in LS[j]:
                jstar = j; break
        if jstar is None:
            whole.append(l); continue
        if l in excluded:
            # every admissible point of an excluded line is excluded
            continue
        cands = set()
        for l2 in LS[jstar]:
            p = isect(l, l2)
            if p is not None:
                cands.add(p)
        for (x, y) in cands:
            ncand += 1
            if x == y or x in Aset or y in Aset:
                continue
            if isinstance(x, Fr) or isinstance(y, Fr):
                nfrac += 1
            ok_def = True
            for j, S in enumerate(M):
                dx = [abs(x - s) for s in S]; dy = [abs(y - s) for s in S]
                allv = dx + dy + [abs(x - y)]
                sx = set(allv)
                if len(sx) == 17 and not (sx & DS[j]):
                    ok_def = False; break   # S u {x,y} Sidon -> not deficient
            if ok_def:
                Dpts.add((x, y))
    # whole lines
    wl = {'excluded': 0, 'witnessed': 0, 'flagged': []}; wex = []
    for l in whole:
        if l in excluded:
            wl['excluded'] += 1; continue
        w = symbolic_witness(A, l)
        if w is None:
            wl['flagged'].append(list(l))
        else:
            wl['witnessed'] += 1; wex.append([list(l), w])
    on_whole = lambda x, y: any(a * x + b * y == c for a, b, c in whole if (a, b, c) not in excluded)
    iso = [(x, y) for (x, y) in Dpts if not on_whole(x, y)]
    p45 = []
    for (x, y) in Dpts:
        if is45_ext(A, x, y):
            p45.append((str(x), str(y), h_brute(A + [x, y])))
    return {'class': idx, 'h': h, 'nS': len(M), 'selftest_points': st_n, 'selftest_bad': st_bad,
            'n_lines_K_S0': len(L0), 'n_whole': len(whole), 'whole': wl, 'whole_examples': wex[:4],
            'n_candidates': ncand, 'n_fraction_candidates': nfrac, 'n_D_points': len(Dpts),
            'n_isolated_not_on_whole': len(iso), 'n_D_points_45': len(p45), 'D_points_45': p45[:10],
            'secs': round(time.time() - t0, 1)}


def main():
    census, outp = sys.argv[1], sys.argv[2]
    idxs = [int(a) for a in sys.argv[3:]]
    sets = [json.loads(l)['set'] for l in gzip.open(census, 'rt')]
    with open(outp, 'a') as fo:
        for idx in idxs:
            r = analyse(sets[idx], idx, random.Random(1000 + idx))
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
