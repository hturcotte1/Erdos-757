"""L003 round 3: own non-saturated extremal witnesses for n = 6..11 and an exact proof that each lies in an
infinite family of pairwise affinely inequivalent extremal sets. Pure Python, Fractions, no repo imports.
usage: python3 -I nonsat3.py"""
import random, math, gzip
from fractions import Fraction as Fr
from itertools import combinations
F = {4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}

def is45(X): return all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in combinations(X, 4))
def aps(X):  # index triples (i,j,k), X sorted
    pos = {v: i for i, v in enumerate(X)}
    return sorted((i, pos[(X[i] + X[k]) / 2], k) for i, k in combinations(range(len(X)), 2) if (X[i] + X[k]) / 2 in pos)
def sidon(S):
    d = [b - a for a, b in combinations(S, 2)]; return len(d) == len(set(d))
def hmax(X):
    for k in range(len(X), 0, -1):
        if any(sidon(S) for S in combinations(X, k)): return k
def to_int(X):
    X = sorted(Fr(v) for v in X); X = [v - X[0] for v in X]
    den = 1
    for v in X: den = den * v.denominator // math.gcd(den, v.denominator)
    Y = [int(v * den) for v in X]; g = 0
    for y in Y: g = math.gcd(g, y)
    return [y // g for y in Y]
def norm(X):
    X = to_int(X); R = [X[-1] - v for v in reversed(X)]; return tuple(min(X, R))

def nullspace(rows, n):
    """basis of {x : row.x = 0 for all rows}, exact"""
    M = [list(map(Fr, r)) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(n) if c not in piv]; basis = []
    for fc in free:
        v = [Fr(0)] * n; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis, len(piv)
def rank(vecs):
    return len(vecs[0]) - nullspace(vecs, len(vecs[0]))[1] and nullspace(vecs, len(vecs[0]))[1]

def family_proof(name, X0, f):
    """X0 sorted ints. Returns dict; asserts every step."""
    n = len(X0); X0 = [Fr(v) for v in X0]
    P = aps(X0); m = len(P)
    assert is45(X0) and m < n - 2 and hmax(X0) == f, (name, is45(X0), m, hmax(X0))
    rows = []
    for i, j, k in P:
        r = [0] * n; r[i] += 1; r[k] += 1; r[j] -= 2; rows.append(r)
    basis, rk = nullspace(rows, n)
    assert rk == m and len(basis) == n - m >= 3
    one = [Fr(1)] * n
    v = next(b for b in basis if nullspace([X0, one, b], n)[1] == 3)  # x0, 1, v linearly independent
    # order interval
    lo, hi = None, None
    for i in range(n - 1):
        g0, g1 = X0[i + 1] - X0[i], v[i + 1] - v[i]
        assert g0 > 0
        if g1 > 0: lo = max(lo, -g0 / g1) if lo is not None else -g0 / g1
        if g1 < 0: hi = min(hi, -g0 / g1) if hi is not None else -g0 / g1
    # coincidences of distances
    pairs = list(combinations(range(n), 2)); ident = set(); roots = set()
    for (a, b), (c, d) in combinations(pairs, 2):
        F0 = (X0[b] - X0[a]) - (X0[d] - X0[c]); F1 = (v[b] - v[a]) - (v[d] - v[c])
        if F0 == 0 and F1 == 0: ident.add(((a, b), (c, d)))
        elif F0 == 0: raise AssertionError("coincidence of x0 not identical along v")
        elif F1 != 0: roots.add(-F0 / F1)
    apco = set()
    for i, j, k in P: apco.add(tuple(sorted([(i, j), (j, k)])))
    assert {tuple(sorted(p)) for p in ident} == apco, "identical coincidences != AP coincidences of P"
    inI = lambda s: (lo is None or s > lo) and (hi is None or s < hi)
    rI = sorted(s for s in roots if inI(s))
    # spot check members of the family from the definitions
    rng = random.Random(1); members = [tuple(X0)]
    S = []
    while len(S) < 6:
        a = lo if lo is not None else Fr(-10**6); b = hi if hi is not None else Fr(10**6)
        s = a + (b - a) * Fr(rng.randint(1, 999), 1000)
        if s != 0 and s not in roots and inI(s): S.append(s)
    for s in S:
        Xs = [x + s * w for x, w in zip(X0, v)]
        assert all(Xs[i] < Xs[i + 1] for i in range(n - 1))
        assert is45(Xs) and aps(Xs) == P and hmax(Xs) == f
        members.append(tuple(Xs))
    nfs = {norm(Mb) for Mb in members}
    assert len(nfs) == len(members), "family members not pairwise inequivalent"
    return {"name": name, "n": n, "m": m, "h": f, "dimV": n - m, "I": (str(lo), str(hi)), "roots_in_I": len(rI),
            "checked_members": len(members), "distinct_classes": len(nfs)}

def load_sat(n, k=0):
    fn = {6: "sat_n6_k0_l0.txt", 8: "sat_n8_k0_l0.txt", 10: "sat_n10_k1_l1.txt"}[n]
    L = [list(map(int, l.split()[1:1 + n])) for l in open(fn) if l.startswith("S ")]
    return L[k]

def search_one_free(n, f, seed, tries=200000):
    """random maps with one interior non-midpoint j0 (K30 + linear), x_j0 random, exact solve"""
    rng = random.Random(seed)
    for t in range(tries):
        j0 = rng.randint(1, n - 2); L = {}; R = {}; ok = True
        js = [j for j in range(1, n - 1) if j != j0]; rng.shuffle(js)
        for j in js:
            cand = []
            for l in range(j):
                for r in range(j + 1, n):
                    good = True
                    for jj in L:
                        if len({l, j, r} & {L[jj], jj, R[jj]}) >= 2: good = False; break
                        if j < jj and l >= L[jj] and r >= R[jj]: good = False; break
                        if jj < j and L[jj] >= l and R[jj] >= r: good = False; break
                    if good: cand.append((l, r))
            if not cand: ok = False; break
            L[j], R[j] = rng.choice(cand)
        if not ok: continue
        edges = [(L[j], j, R[j]) for j in L]
        # alpha of the pattern (combinatorial) must be <= f
        if any(not any(set(e) <= set(Sx) for e in edges) for Sx in combinations(range(n), f + 1)): continue
        # solve: x0 = 0, x_{n-1} = 1, x_j0 = c
        c = Fr(rng.randint(1, 10**6 - 1), 10**6)
        rows = []; rhs = []
        for (l, j, r) in edges:
            row = [Fr(0)] * n; row[l] += 1; row[r] += 1; row[j] -= 2; rows.append(row); rhs.append(Fr(0))
        for idx, val in ((0, Fr(0)), (n - 1, Fr(1)), (j0, c)):
            row = [Fr(0)] * n; row[idx] = Fr(1); rows.append(row); rhs.append(val)
        A = [r + [b] for r, b in zip(rows, rhs)]; N = n; okk = True
        for col in range(N):
            p = next((i for i in range(col, N) if A[i][col] != 0), None)
            if p is None: okk = False; break
            A[col], A[p] = A[p], A[col]; pv = A[col][col]; A[col] = [x / pv for x in A[col]]
            for i in range(N):
                if i != col and A[i][col] != 0:
                    fct = A[i][col]; A[i] = [x - fct * y for x, y in zip(A[i], A[col])]
        if not okk: continue
        X = [A[i][N] for i in range(N)]
        if not all(X[i] < X[i + 1] for i in range(n - 1)): continue
        if not is45(X): continue
        if aps(X) != sorted(edges): continue
        if hmax(X) != f: continue
        return to_int(X), t + 1
    return None, tries

out = []
# n=6: generic gluing of two 3-APs
out.append(family_proof("glue {0,1,2} u (13/7*{0,1,2}+50)", to_int([0, 1, 2, 50, 50 + Fr(13, 7), 50 + Fr(26, 7)]), 4))
# n=7, 9, 11: saturated (n-1)-set + generic point
for n in (7, 9, 11):
    S = load_sat(n - 1); y = Fr(S[-1] * 3) + Fr(1, 7919)
    out.append(family_proof("sat%d %s + point %s" % (n - 1, S, y), to_int(S + [y]), F[n]))
# n=8, 10: own random search, one free interior point
for n in (8, 10):
    X, t = search_one_free(n, F[n], seed=2026)
    assert X is not None, n
    out.append(family_proof("own search (%d tries) %s" % (t, X), X, F[n]))
# n=8 record set of data/small_records.json (read as data)
import json
rec = json.load(open("/home/user/Erdos-757/data/small_records.json"))["sets"]
out.append(family_proof("record n=8 %s" % rec["8"]["set"], to_int(rec["8"]["set"]), 5))
out.append(family_proof("record n=11 %s" % rec["11"]["set"], to_int(rec["11"]["set"]), 7))
for o in out: print(o)
print("ALL_OK", len(out))
