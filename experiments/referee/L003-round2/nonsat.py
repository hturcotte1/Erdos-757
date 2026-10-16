"""Referee L003 round 2: non-saturated extremal sets for n = 6..11 and the infinite-family argument, done exactly.
No imports from e757/ or judge/; census files are read as DATA only.

For every witness x0 (an n-point set):
  1. from the definitions: distinct points, (4,5) on every 4-subset, the 3-AP set P, m = |P| < n-2,
     h = largest Sidon subset by exhaustive subset search on the DEFINITION (all positive differences distinct) = f(n).
  2. V = solution space of the AP equations of P (exact Fractions); rank must be m, so dim V = n-m >= 3.
  3. v in V outside span(x0, 1)  (x0, v, 1 linearly independent, checked exactly).
  4. Family x(s) = x0 + s v:  order holds on an explicit open interval I containing 0; every linear form
     (x_b - x_a) - (x_d - x_c) (pairs a<b, c<d, {a,b} != {c,d}) that is nonzero at s=0 has at most one root;
     the forms vanishing at s=0 must be exactly the AP coincidences of P (2 per AP: x_j-x_l = x_r-x_j and its
     mirror, as an unordered pair of pairs counted once) and then they vanish identically (v in V).
     Hence for every s in I minus the finite root set, x(s) has exactly the same distance coincidences as x0:
     it is a (4,5)-set with AP set P, so h = alpha(P) = f(n).  Distinct s give affinely inequivalent
     orientation-preserving sets (x0, v, 1 independent), reflection identifies at most pairs: infinitely many classes.
  5. Spot check: 12 rational s in I \\ roots, each re-verified from the definitions (no reliance on step 4),
     canonical forms pairwise distinct.
"""
import sys, os, json, gzip, glob, random, math, itertools
from fractions import Fraction as Fr

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CENSUS = os.path.join(ROOT, "experiments", "20261014-1430-small-counts", "results")
F = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}


def is45(x):
    for q in itertools.combinations(sorted(x), 4):
        if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5:
            return False
    return True


def aps(x):
    x = sorted(x); pos = {v: i for i, v in enumerate(x)}
    out = []
    for a, c in itertools.combinations(range(len(x)), 2):
        mid = (x[a] + x[c]) / 2
        if mid in pos:
            out.append((a, pos[mid], c))
    return sorted(out)


def is_sidon(s):
    d = [b - a for a, b in itertools.combinations(sorted(s), 2)]
    return len(d) == len(set(d))


def h_def(x):
    x = sorted(x)
    for k in range(len(x), 0, -1):
        for s in itertools.combinations(x, k):
            if is_sidon(s):
                return k
    return 0


def canon(vals):
    v = sorted(Fr(t) for t in vals); lo = v[0]; v = [t - lo for t in v]
    den = 1
    for t in v: den = den * t.denominator // math.gcd(den, t.denominator)
    w = [int(t * den) for t in v]; g = 0
    for t in w: g = math.gcd(g, t)
    w = [t // g for t in w]
    return tuple(min(w, sorted(w[-1] - t for t in w)))


def rref(rows, ncol):
    rows = [list(r) for r in rows]; piv = []; r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        inv = 1 / rows[r][c]; rows[r] = [t * inv for t in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
        if r == len(rows): break
    return rows[:r], piv


def nullspace(rows, ncol):
    R, piv = rref(rows, ncol)
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * ncol; v[f] = Fr(1)
        for i, c in enumerate(piv): v[c] = -R[i][f]
        basis.append(v)
    return basis, len(piv)


def rank(vecs, ncol):
    return len(rref([list(map(Fr, v)) for v in vecs], ncol)[1])


def analyse(name, x0, n_expected=None, verbose=True):
    x0 = sorted(Fr(t) for t in x0); n = len(x0)
    assert n_expected is None or n == n_expected
    assert len(set(x0)) == n
    rep = {"name": name, "n": n}
    rep["is45"] = is45(x0)
    P = aps(x0); m = len(P); rep["m"] = m
    rep["h"] = h_def(x0); rep["f"] = F[n]
    ok = rep["is45"] and m < n - 2 and rep["h"] == F[n]
    rows = []
    for (l, j, r) in P:
        row = [Fr(0)] * n; row[l] += 1; row[r] += 1; row[j] -= 2; rows.append(row)
    basis, rk = nullspace(rows, n) if rows else ([[Fr(int(i == k)) for i in range(n)] for k in range(n)], 0)
    rep["rank"] = rk; rep["dimV"] = len(basis)
    ok = ok and rk == m and len(basis) == n - m >= 3
    one = [Fr(1)] * n
    v = next(b for b in basis if rank([x0, one, b], n) == 3)
    # sanity: v solves the AP equations
    assert all(sum(a * b for a, b in zip(row, v)) == 0 for row in rows)
    # order interval
    lo, hi = None, None
    for i in range(n - 1):
        g = x0[i + 1] - x0[i]; d = v[i + 1] - v[i]
        assert g > 0
        if d > 0:
            t = -g / d; lo = t if lo is None or t > lo else lo
        elif d < 0:
            t = -g / d; hi = t if hi is None or t < hi else hi
    rep["interval"] = [str(lo) if lo is not None else "-inf", str(hi) if hi is not None else "+inf"]
    # coincidence analysis
    pairs = list(itertools.combinations(range(n), 2))
    apco = set()
    for (l, j, r) in P:
        apco.add(frozenset([(l, j), (j, r)]))
    roots, zero_at_0 = set(), set()
    for p1, p2 in itertools.combinations(pairs, 2):
        a0 = (x0[p1[1]] - x0[p1[0]]) - (x0[p2[1]] - x0[p2[0]])
        a1 = (v[p1[1]] - v[p1[0]]) - (v[p2[1]] - v[p2[0]])
        if a0 == 0:
            zero_at_0.add(frozenset([p1, p2]))
            ok = ok and a1 == 0
        elif a1 != 0:
            roots.add(-a0 / a1)
    rep["coincidences_at_0_equal_AP_coincidences"] = (zero_at_0 == apco)
    ok = ok and zero_at_0 == apco
    rin = sorted(t for t in roots if (lo is None or t > lo) and (hi is None or t < hi))
    rep["n_roots_total"] = len(roots); rep["n_roots_in_interval"] = len(rin)
    # spot check: 12 rational s in the interval avoiding roots, verified from the definitions
    a = lo if lo is not None else Fr(-1); b = hi if hi is not None else Fr(1)
    a = max(a, Fr(-1)); b = min(b, Fr(1))
    cands, k = [], 1
    while len(cands) < 12:
        s = a + (b - a) * Fr(k, 29); k += 1
        if s != 0 and s not in roots and a < s < b: cands.append(s)
    cl = set(); spot_ok = True
    for s in cands:
        xs = [p + s * q for p, q in zip(x0, v)]
        good = (sorted(xs) == xs and len(set(xs)) == n and is45(xs) and aps(xs) == P and h_def(xs) == F[n])
        spot_ok = spot_ok and good
        cl.add(canon(xs))
    cl.add(canon(x0))
    rep["spot_all_ok"] = spot_ok; rep["spot_distinct_classes"] = len(cl)
    ok = ok and spot_ok and len(cl) == len(cands) + 1
    rep["OK"] = ok
    if verbose:
        print(json.dumps(rep), flush=True)
    return ok


def glue(A, B, q, t):
    return sorted([Fr(a) for a in A] + [Fr(q) * b + t for b in B])


def find_glue(A, B, n):
    """first (q, t) on a fixed grid that gives an n-point (4,5)-set with AP set = APs(A) + APs(B) (no cross AP)."""
    for q in [Fr(7, 3), Fr(11, 5), Fr(13, 4), Fr(17, 7), Fr(19, 6), Fr(23, 9)]:
        for t in range(50, 2000, 37):
            C = glue(A, B, q, t)
            if len(set(C)) == n and is45(C) and len(aps(C)) == len(aps(A)) + len(aps(B)):
                return C, q, t
    raise RuntimeError("no gluing found")


if __name__ == "__main__":
    random.seed(20261014)
    allok = True
    # (a) census non-saturated witnesses: first and one random record of every non-saturated cell (data only)
    for n in range(6, 12):
        files = sorted(glob.glob(os.path.join(CENSUS, "n%d_m*_real.json.gz" % n)))
        for fn in files:
            m = int(os.path.basename(fn).split("_")[1][1:])
            if m >= n - 2: continue
            recs = json.load(gzip.open(fn, "rt"))
            if not recs: continue
            for tag, r in (("first", recs[0]), ("random", random.choice(recs))):
                allok &= analyse("census %s %s" % (os.path.basename(fn), tag), r["set"], n)
    # (b) record sets of data/small_records.json that are non-saturated (n=8: m=5, n=11: m=8)
    rec = json.load(open(os.path.join(ROOT, "data", "small_records.json")))["sets"]
    for key in ("8", "11"):
        allok &= analyse("record %s" % key, rec[key]["set"], int(key))
    # (c) own gluing constructions: 3-AP {0,1,2} glued to a generic copy of B
    S6 = None
    for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sat_n6_k0_l0.txt")):
        if line.startswith("S "): S6 = [int(t) for t in line.split()[2:]]
    gl = {6: [0, 1, 2], 7: [0, 1, 2, 5], 9: S6, 11: rec["8"]["set"]}
    for n, B in sorted(gl.items()):
        C, q, t = find_glue([0, 1, 2], B, n)
        allok &= analyse("glue {0,1,2} + %s*B+%s, B=%s" % (q, t, B), C, n)
    print("ALL_OK", allok)
