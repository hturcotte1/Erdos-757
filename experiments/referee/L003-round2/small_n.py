"""Referee L003 round 2: n <= 5.
(1) n = 1, 2, 3: number of affine classes of extremal sets (h = f(n)) in a box [0, 40] (sanity; the proof is one line).
(2) n = 4, 5: the families {0,1,2,x} and {0,1,2,x,3x}: exact root analysis of every linear distance-coincidence form in x,
    giving an explicit x0 such that for EVERY real x > x0 the set is a (4,5)-set whose only 3-AP is (0,1,2), hence
    h = n-1 = f(n); plus a check of the affine invariant (distinct x -> distinct classes) and an exact check for x = x0+1..x0+60.
(3) f(4) = 3, f(5) = 4 from the definitions: exhaustive search of 4- and 5-subsets of [0, 24] for the minimum h over (4,5)-sets.
No imports from e757/ or judge/.
"""
import itertools, math
from fractions import Fraction as Fr


def is45(x):
    return all(len({abs(a - b) for a, b in itertools.combinations(q, 2)}) >= 5 for q in itertools.combinations(sorted(x), 4))


def is_sidon(s):
    d = [b - a for a, b in itertools.combinations(sorted(s), 2)]
    return len(d) == len(set(d))


def h_def(x):
    for k in range(len(x), 0, -1):
        if any(is_sidon(s) for s in itertools.combinations(sorted(x), k)):
            return k


def aps(x):
    x = sorted(x); S = set(x)
    return [(a, c) for a, c in itertools.combinations(x, 2) if Fr(a + c, 2) in S]


def canon(vals):
    v = sorted(Fr(t) for t in vals); lo = v[0]; v = [t - lo for t in v]
    den = 1
    for t in v: den = den * t.denominator // math.gcd(den, t.denominator)
    w = [int(t * den) for t in v]; g = 0
    for t in w: g = math.gcd(g, t)
    w = [t // g for t in w] if g else w
    return tuple(min(w, sorted(w[-1] - t for t in w)))


# (1) n = 1, 2, 3 in a box
F = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4}
for n in (1, 2, 3):
    cl = set()
    for s in itertools.combinations(range(41), n):
        if h_def(s) == F[n]:
            cl.add(canon(s))
    print("n=%d: extremal classes in [0,40]: %d %s" % (n, len(cl), sorted(cl)[:3]))

# (2) families: x(t) = a + t b, ranks fixed for t > max(a)
fams = {4: ([0, 1, 2, 0], [0, 0, 0, 1]), 5: ([0, 1, 2, 0, 0], [0, 0, 0, 1, 3])}
for n, (a, b) in fams.items():
    pairs = list(itertools.combinations(range(n), 2))
    roots, ident = set(), []
    for p, q in itertools.combinations(pairs, 2):
        # for t > 2 the points are in the listed order, so x_j - x_i (i<j) is the distance
        c0 = (a[p[1]] - a[p[0]]) - (a[q[1]] - a[q[0]]); c1 = (b[p[1]] - b[p[0]]) - (b[q[1]] - b[q[0]])
        if c0 == 0 and c1 == 0:
            ident.append((p, q))
        elif c1 != 0:
            roots.add(Fr(-c0, c1))
    # order: need 2 < t (and for n=5, t < 3t, true for t > 0)
    x0 = max([Fr(2)] + [r for r in roots])
    print("n=%d family %s + t*%s: identically-equal distance pairs %s; roots %s; good for all t > %s"
          % (n, a, b, ident, sorted(roots), x0))
    # the only identical coincidence must be the AP (0,1,2): pairs (0,1),(1,2)
    assert ident == [((0, 1), (1, 2))]
    # => for t > x0: exactly one distance coincidence, so every 4-subset has >= 5 distinct distances, the only 3-AP is
    #    {0,1,2}, and h = alpha = n-1 = f(n).  Exact check for 60 values:
    cls = set()
    for t in range(int(x0) + 1, int(x0) + 61):
        x = [ai + t * bi for ai, bi in zip(a, b)]
        assert is45(x) and len(aps(x)) == 1 and h_def(x) == F[n], (n, t)
        cls.add(canon(x))
    print("   exact check t = %d..%d: all (4,5), one AP, h = %d; %d distinct affine classes" % (int(x0) + 1, int(x0) + 60, F[n], len(cls)))
    # affine invariant: (largest gap)/(smallest gap) ... use the ratio (x_3 - x_2)/(x_1 - x_0) = t - 2 together with reflection:
    # canonical form of {0,1,2,t} is (0,1,2,t) or reflection (0,t-2,t-1,t); these differ for different t > 3, so the map t -> class
    # is injective on t > x0 (checked above on 60 values; in general two sets with the same normal form have the same gap ratios).

# (3) f(4), f(5) by exhaustive search in a box (upper bound side is the families above; the lower bound is the
#     argument in the review: a (4,5)-set on 4 or 5 points has pairwise intersecting APs and no triangle, so tau <= 1)
for n in (4, 5):
    best = None
    for s in itertools.combinations(range(25), n):
        if s[0] != 0: break
        if is45(s):
            h = h_def(s); best = h if best is None or h < best else best
    print("n=%d: min h over (4,5)-subsets of [0,24] containing 0: %d (f(n) = %d)" % (n, best, F[n]))
