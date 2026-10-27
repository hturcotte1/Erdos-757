"""Referee #2 (fable), L023 round 1: own verification code.  No import of e757/, judge/ or any prover script.
Checks: Theorem 1 arithmetic; the six classes (parsed from the certificate text itself) are in C, connected, tau = 11, Delta = 4,
pairwise non-isomorphic; Q8 is in C and not realizable (two independent methods: SDR/affine normalisation as in 3.1, and the
complete generic-point method over all 3^6 midpoint assignments, which does not use K5); Q8 embeds in every X_i (explicit
embedding); the decompositions of the two top branches by brute force; the witness C25; Corollary 5 arithmetic."""
import sys, re, json, itertools, math, time
from fractions import Fraction
from itertools import combinations, permutations, product

CERT = '/home/user/Erdos-757/results/proofs/L023-f25-equals-15.md'
SIX_JSON = '/home/user/Erdos-757/experiments/prover/L023/six_classes_25_23_11_D4.json'
TOPCELL = '/home/user/Erdos-757/experiments/referee/L023-round1-fable/own/topcell_lists'
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.append(s)
def check(cond, msg):
    P(('OK   ' if cond else 'FAIL ') + msg)
    if not cond: FAILS.append(msg)
FAILS = []

# ---------------------------------------------------------------- hypergraph utilities (own)
def verts(E):
    return sorted(set(v for e in E for v in e))
def degrees(E, V):
    d = {v: 0 for v in V}
    for e in E:
        for v in e: d[v] += 1
    return d
def is_linear(E):
    for e, f in combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return False
    return True
def contains_F7(E):
    """F7 = {012,034,056,135,246} as a (not necessarily induced) subhypergraph.  Complete search: the image of vertex 0 is a
    vertex v with 3 edges (ordered choice), the images of (1,2),(3,4),(5,6) are the two other vertices of those edges in either order;
    then 135 and 246 must be edges."""
    ES = set(frozenset(e) for e in E)
    at = {}
    for e in E:
        for v in e: at.setdefault(v, []).append(e)
    for v, es in at.items():
        if len(es) < 3: continue
        for e1, e2, e3 in permutations(es, 3):
            p1 = [u for u in e1 if u != v]; p2 = [u for u in e2 if u != v]; p3 = [u for u in e3 if u != v]
            for a1, a2 in (p1, p1[::-1]):
                for a3, a4 in (p2, p2[::-1]):
                    for a5, a6 in (p3, p3[::-1]):
                        if frozenset((a1, a3, a5)) in ES and frozenset((a2, a4, a6)) in ES: return True
    return False
def hall_sdr_avoiding(E, V, forbidden):
    """Is there a system of distinct representatives of the edges avoiding the vertices in `forbidden`?  Own augmenting-path matching."""
    match = {}  # vertex -> edge index
    def try_edge(i, seen):
        for v in E[i]:
            if v in forbidden or v in seen: continue
            seen.add(v)
            if v not in match or try_edge(match[v], seen):
                match[v] = i; return True
        return False
    for i in range(len(E)):
        if not try_edge(i, set()): return False
    return True
def P3_by_matching(E, V):
    """(P3): e(S) <= |S|-2 for all |S| >= 2  <=>  for every pair {u,w} the edges have an SDR avoiding u,w (Lemma P; proof re-derived in
    the review)."""
    for u, w in combinations(V, 2):
        if not hall_sdr_avoiding(E, V, {u, w}): return False
    return True
def P3_brute(E, V):
    """(P3) directly from the definition; only for small V."""
    for k in range(2, len(V) + 1):
        for S in combinations(V, k):
            SS = set(S)
            if sum(1 for e in E if set(e) <= SS) > k - 2: return False
    return True
def connected(E, V):
    adj = {v: set() for v in V}
    for e in E:
        for a in e:
            for b in e:
                if a != b: adj[a].add(b)
    seen = {V[0]}; st = [V[0]]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(V)
def has_cover(E, k):
    """Is there a vertex set of size <= k meeting every edge?  Branch on the first uncovered edge (3 choices), depth <= k."""
    def rec(cov, k):
        for e in E:
            if not (cov & set(e)):
                if k == 0: return None
                for v in e:
                    r = rec(cov | {v}, k - 1)
                    if r is not None: return r
                return None
        return cov
    return rec(frozenset(), k)
def tau(E):
    k = 0
    while True:
        c = has_cover(E, k)
        if c is not None: return k, sorted(c)
        k += 1
def isomorphic(E1, E2):
    """Own backtracking isomorphism test for 3-graphs (vertices = all vertices appearing; isolated vertices irrelevant here)."""
    V1, V2 = verts(E1), verts(E2)
    if len(V1) != len(V2) or len(E1) != len(E2): return None
    d1, d2 = degrees(E1, V1), degrees(E2, V2)
    if sorted(d1.values()) != sorted(d2.values()): return None
    S1 = set(frozenset(e) for e in E1); S2 = set(frozenset(e) for e in E2)
    at1 = {v: [e for e in E1 if v in e] for v in V1}
    # order V1 by BFS so that constraints appear early
    order = []; seen = set()
    for s in sorted(V1, key=lambda v: -d1[v]):
        if s in seen: continue
        seen.add(s); q = [s]
        while q:
            x = q.pop(0); order.append(x)
            for e in at1[x]:
                for y in e:
                    if y not in seen: seen.add(y); q.append(y)
    f = {}; used = set()
    def ok(x, y):
        # every edge of E1 through x with all vertices mapped must map to an edge of E2
        for e in at1[x]:
            if all(u in f or u == x for u in e):
                img = frozenset(f[u] if u != x else y for u in e)
                if img not in S2: return False
        return True
    def rec(i):
        if i == len(order): return True
        x = order[i]
        for y in V2:
            if y in used or d2[y] != d1[x]: continue
            if ok(x, y):
                f[x] = y; used.add(y)
                if rec(i + 1): return True
                del f[x]; used.discard(y)
        return False
    if rec(0):
        # verify edge count preserved (injective map sending edges to edges, equal counts => bijection on edges)
        assert set(frozenset(f[u] for u in e) for e in E1) == S2
        return dict(f)
    return None

# ---------------------------------------------------------------- exact linear algebra (own)
def solve_square(rows, rhs, nvar):
    """Gauss-Jordan over Q.  rows: list of dict var->coef.  Returns (None if singular) or solution list."""
    M = [dict(r) for r in rows]; b = list(rhs)
    piv_of = {}
    for col in range(nvar):
        pr = None
        for i in range(len(M)):
            if i in piv_of.values(): continue
            if M[i].get(col, 0) != 0: pr = i; break
        if pr is None: return None
        piv_of[col] = pr
        inv = Fraction(1) / M[pr][col]
        M[pr] = {k: v * inv for k, v in M[pr].items()}; b[pr] *= inv
        for i in range(len(M)):
            if i == pr: continue
            c = M[i].get(col, 0)
            if c:
                for k, v in M[pr].items():
                    nv = M[i].get(k, 0) - c * v
                    if nv: M[i][k] = nv
                    else: M[i].pop(k, None)
                b[i] -= c * b[pr]
    x = [None] * nvar
    for col, pr in piv_of.items(): x[col] = b[pr]
    return x
def nullspace(rows, nvar):
    """Basis of {x : row . x = 0 for all rows}, exact.  rows: list of dicts."""
    M = [dict(r) for r in rows]
    pivots = []; r = 0
    M = [m for m in M if m]
    rowsL = [[Fraction(m.get(c, 0)) for c in range(nvar)] for m in M]
    nr = len(rowsL)
    pivcols = []
    for c in range(nvar):
        pr = next((i for i in range(r, nr) if rowsL[i][c] != 0), None)
        if pr is None: continue
        rowsL[r], rowsL[pr] = rowsL[pr], rowsL[r]
        inv = 1 / rowsL[r][c]; rowsL[r] = [v * inv for v in rowsL[r]]
        for i in range(nr):
            if i != r and rowsL[i][c] != 0:
                f = rowsL[i][c]; rowsL[i] = [a - f * bb for a, bb in zip(rowsL[i], rowsL[r])]
        pivcols.append(c); r += 1
        if r == nr: break
    free = [c for c in range(nvar) if c not in pivcols]
    basis = []
    for fc in free:
        v = [Fraction(0)] * nvar; v[fc] = Fraction(1)
        for i, pc in enumerate(pivcols): v[pc] = -rowsL[i][fc]
        basis.append(v)
    return basis

# ---------------------------------------------------------------- realizability deciders (own)
def classify_point(x, E):
    """x: dict vertex -> Fraction.  Returns the first failure among NONINJ, NOTWS, NONLIN, or 'REAL' (AP set may exceed E:
    reported separately)."""
    V = sorted(x)
    vals = [x[v] for v in V]
    if len(set(vals)) < len(vals): return 'NONINJ'
    sums = {}
    for a, b in combinations(V, 2):
        s = x[a] + x[b]
        if s in sums: return 'NOTWS'
        sums[s] = (a, b)
    aps = set()
    for a, b, c in combinations(V, 3):
        xs = sorted((x[a], x[b], x[c]))
        if xs[0] + xs[2] == 2 * xs[1]: aps.add(frozenset((a, b, c)))
    if not is_linear([tuple(e) for e in aps]): return 'NONLIN'
    if aps != set(frozenset(e) for e in E): return 'APSET'
    return 'REAL'
def sdr_labellings(E):
    """All injective lambda: E -> V with lambda(e) in e (depth-first over edges; each map exactly once)."""
    res = []
    def rec(i, used, lam):
        if i == len(E): res.append(list(lam)); return
        for v in E[i]:
            if v not in used:
                used.add(v); lam.append(v); rec(i + 1, used, lam); lam.pop(); used.discard(v)
    rec(0, set(), []); return res
def realize_sdr(E, verbose=False):
    """Method 1 (certificate 3.1): for every injective midpoint labelling, u<w = the two unlabelled vertices, x_u=0, x_w=1, solve exactly."""
    V = verts(E); n = len(V); assert len(E) == n - 2
    cnt = {'labellings': 0, 'SINGULAR': 0, 'NONINJ': 0, 'NOTWS': 0, 'NONLIN': 0, 'APSET': 0, 'REAL': 0}
    reals = []
    for lam in sdr_labellings(E):
        cnt['labellings'] += 1
        u, w = sorted(set(V) - set(lam))
        unk = [v for v in V if v not in (u, w)]; idx = {v: i for i, v in enumerate(unk)}
        rows = []; rhs = []
        for e, mid in zip(E, lam):
            a, c = [v for v in e if v != mid]
            row = {}; r = Fraction(0)
            for v, coef in ((mid, 2), (a, -1), (c, -1)):
                if v == u: pass
                elif v == w: r -= coef
                else: row[idx[v]] = row.get(idx[v], 0) + coef
            rows.append(row); rhs.append(r)
        sol = solve_square(rows, rhs, len(unk))
        if sol is None: cnt['SINGULAR'] += 1; continue
        x = {u: Fraction(0), w: Fraction(1)}
        for v in unk: x[v] = sol[idx[v]]
        c = classify_point(x, E); cnt[c] += 1
        if c == 'REAL': reals.append((lam, x))
    return cnt, reals
def realize_generic(E):
    """Method 2 (complete, no use of K5): for EVERY assignment mu of a midpoint to each edge (3^m), compute the solution space W of
    the equations 2x_mu(e) = x_a + x_c and test whether some bad linear form vanishes identically on W: x_a - x_b (a != b),
    x_a + x_b - x_c - x_d (distinct pairs), or two AP forms on triples sharing two vertices both vanish (non-linear forced AP set).
    If for some mu none does, the generic point of W is a (4,5)-set realizing E (plus possibly further APs, forming a linear set);
    if every mu fails, no (4,5)-set contains E as APs with any midpoints."""
    V = verts(E); n = len(V); idx = {v: i for i, v in enumerate(V)}
    def vanishes(form, basis):  # form: dict var->coef
        return all(sum(c * b[i] for i, c in form.items()) == 0 for b in basis)
    res = {'assignments': 0, 'NONINJ': 0, 'NOTWS': 0, 'NONLIN': 0, 'REAL': 0}
    for mu in product(*[list(e) for e in E]):
        res['assignments'] += 1
        rows = []
        for e, mid in zip(E, mu):
            a, c = [v for v in e if v != mid]
            rows.append({idx[mid]: 2, idx[a]: -1, idx[c]: -1})
        B = nullspace(rows, n)
        bad = None
        for a, b in combinations(range(n), 2):
            if vanishes({a: 1, b: -1}, B): bad = 'NONINJ'; break
        if bad is None:
            for (a, b), (c, d) in combinations(list(combinations(range(n), 2)), 2):
                if len({a, b, c, d}) == 4 and vanishes({a: 1, b: 1, c: -1, d: -1}, B):
                    bad = 'NOTWS'; break
        if bad is None:
            forced = set()
            for T in combinations(range(n), 3):
                for mid in T:
                    a, c = [v for v in T if v != mid]
                    if vanishes({mid: 2, a: -1, c: -1}, B): forced.add(frozenset(T))
            if not is_linear([tuple(t) for t in forced]): bad = 'NONLIN'
        res[bad or 'REAL'] += 1
    return res

# ================================================================ A. Theorem 1 arithmetic
P('=== A. Theorem 1 arithmetic (own re-derivation)')
n = 25; h = 14; t = n - h
check(t == 11, 'tau = 25 - 14 = 11 (K4)')
ms = [m for m in range(0, 24) if 11 * t <= 3 * n + 2 * m]      # I11 at n = 25 (L013 Thm 1) and (P3): m <= 23
check(ms == [23], 'I11 + (P3) force m = 23 exactly (allowed m: %s)' % ms)
check(17 * t <= 5 * n + 3 * 23, 'K8 consistent at (25,23,11): 187 <= 194')
allowed = {}
for d in range(0, 24):
    for tp in (10, 11):
        if 11 * tp <= 3 * 24 + 2 * (23 - d): allowed.setdefault(d, []).append(tp)
check(sorted(allowed) == [0, 1, 2, 3, 4] and all(allowed[d] == [10] for d in allowed), 'I11 on H-v: tau(H-v)=10 and d <= 4 exactly (allowed: %s)' % allowed)
# top key branches
for d in (3, 4):
    for tp in (10, 11):
        Sp = 3 * 24 + 2 * (23 - d) - 11 * tp
        P('   d=%d tp=%d S\'=%d' % (d, tp, Sp))
check(math.ceil(69 / 25) == 3, 'Delta >= ceil(69/25) = 3')

# ================================================================ B. parse the six classes from the certificate text
P('=== B. the six classes, parsed from the certificate text')
txt = open(CERT).read()
X = []
for line in txt.splitlines():
    m = re.match(r'^X_(\d) FOUND: (.*)$', line.strip())
    if m:
        E = [tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', m.group(2))]
        X.append(E)
check(len(X) == 6, 'six X_i lines found')
sj = json.load(open(SIX_JSON))['classes']
check([[list(e) for e in E] for E in X] == sj, 'certificate text == six_classes JSON')
stored = [tuple(map(int, g)) for g in []]
# compare with the stored engine list of the top cell (topcell archive does not contain it; use the prover's copy)
try:
    L = [l for l in open('/home/user/Erdos-757/experiments/prover/L023/cell_25_23_11_D4.txt') if l.startswith('FOUND:')]
    LS = [sorted(tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)) for l in L]
    check(sorted(LS) == sorted(sorted(E) for E in X), 'certificate text == prover copy of cell_25_23_11_D4.txt (as edge sets)')
except Exception as ex:
    P('   (prover copy not compared: %s)' % ex)

# ================================================================ C. properties of each X_i
P('=== C. each X_i: in C, connected, tau = 11, Delta = 4, tau(X-v) = 10, component types of X - w')
types_seen = []
for i, E in enumerate(X):
    V = verts(E)
    ok_basic = V == list(range(25)) and len(E) == 23 and len(set(frozenset(e) for e in E)) == 23 and all(len(set(e)) == 3 for e in E)
    lin = is_linear(E); f7 = contains_F7(E); p3 = P3_by_matching(E, V); con = connected(E, V)
    tv, cov = tau(E)
    d = degrees(E, V); ds = {k: list(d.values()).count(k) for k in sorted(set(d.values()))}
    check(ok_basic and lin and not f7 and p3 and con and tv == 11 and max(d.values()) == 4,
          'X_%d: 25 vertices, 23 edges, linear=%s, F7-free=%s, (P3)=%s, connected=%s, tau=%d (cover %s), degrees %s' % (i, lin, not f7, p3, con, tv, cov, ds))
    # tau(X - v) = 10 for all v, and component types for degree-4 vertices
    allten = True; comp_types = {}
    for v in V:
        Ev = [e for e in E if v not in e]
        if has_cover(Ev, 9) is not None or has_cover(Ev, 10) is None: allten = False
        if d[v] == 4:
            Vv = [u for u in V if u != v]
            # components
            adj = {u: set() for u in Vv}
            for e in Ev:
                for a in e:
                    for b in e:
                        if a != b: adj[a].add(b)
            seen = set(); comps = []
            for s in Vv:
                if s in seen: continue
                st = [s]; seen.add(s); comp = {s}
                while st:
                    x = st.pop()
                    for y in adj[x]:
                        if y not in seen: seen.add(y); comp.add(y); st.append(y)
                comps.append(comp)
            typ = tuple(sorted(((len(c), sum(1 for e in Ev if set(e) <= c), tau([e for e in Ev if set(e) <= c])[0] if any(set(e) <= c for e in Ev) else 0) for c in comps), reverse=True))
            comp_types[v] = typ
    check(allten, 'X_%d: tau(X - v) = 10 for all 25 vertices' % i)
    P('   X_%d: components of X - w for the degree-4 vertices: %s' % (i, comp_types))
    types_seen.append(comp_types)
P('--- pairwise non-isomorphism (own backtracking)')
for i, j in combinations(range(6), 2):
    check(isomorphic(X[i], X[j]) is None, 'X_%d and X_%d are non-isomorphic' % (i, j))

# ================================================================ D. Q8
P('=== D. Q8 = {a,c1c2},{a,c3c4},{a,c5c6},{b,c2c3},{b,c4c5},{b,c6c1}, a=0,b=1,c_i=i+1')
Q8 = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 7, 2)]
VQ = verts(Q8)
check(is_linear(Q8) and not contains_F7(Q8) and P3_brute(Q8, VQ) and P3_by_matching(Q8, VQ) and connected(Q8, VQ), 'Q8 is linear, F7-free, (P3) [brute force AND matching agree], connected: in C')
check(P3_brute(F7, list(range(7))) == P3_by_matching(F7, list(range(7))), 'Lemma P matching test agrees with brute force on F7 (value %s)' % P3_brute(F7, list(range(7))))
fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
check(P3_brute(fano, list(range(7))) is False and P3_by_matching(fano, list(range(7))) is False, 'Fano plane violates (P3) by both tests')
# random cross-validation of Lemma P on small linear graphs
import random
random.seed(7); agree = 0; viol = 0
for _ in range(200):
    Vr = list(range(8)); Er = []
    while len(Er) < random.randint(3, 7):
        e = tuple(sorted(random.sample(Vr, 3)))
        if all(len(set(e) & set(f)) <= 1 for f in Er): Er.append(e)
    a, b = P3_brute(Er, Vr), P3_by_matching(Er, Vr); agree += (a == b); viol += (not a)
check(agree == 200, 'Lemma P agrees with brute force on 200 random linear 3-graphs on 8 vertices (%d violate (P3))' % viol)
t0 = time.time(); cnt, reals = realize_sdr(Q8)
check(cnt['labellings'] == 95 and cnt['REAL'] == 0 and cnt['SINGULAR'] == 0, 'Q8 SDR method: %s (%.1fs)' % (cnt, time.time() - t0))
t0 = time.time(); res = realize_generic(Q8)
check(res['assignments'] == 729 and res['REAL'] == 0, 'Q8 generic-point method over all 3^6 assignments (no K5): %s (%.1fs)' % (res, time.time() - t0))
# positive control for both methods: the 11-point record B11 and A_base
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
def ap_edges(A):
    S = set(A); return [tuple(sorted((a, b, c))) for a, b, c in combinations(sorted(A), 3) if a + c == 2 * b]
EA = ap_edges(A_BASE); idxA = {a: i for i, a in enumerate(A_BASE)}; EAi = [tuple(idxA[v] for v in e) for e in EA]
cntA, realsA = realize_sdr(EAi)
true_lam = [idxA[sorted(e)[1]] for e in EA]
found_true = any(l == true_lam and all(x[idxA[a]] == Fraction(a, 1056) for a in A_BASE) for l, x in realsA)
check(cntA['REAL'] > 0 and found_true, 'positive control A_base (14 pts, 12 APs): SDR method %s, true labelling REAL with solution A_base/1056: %s' % (cntA, found_true))
small = [0, 1, 3, 7, 12, 20]  # 6 points: check generic method on a small realizable pattern
Es = ap_edges([0, 2, 3, 5, 8, 13]) ; P('   APs of {0,2,3,5,8,13}: %s' % Es)
if Es:
    idxs = {a: i for i, a in enumerate([0, 2, 3, 5, 8, 13])}
    rg = realize_generic([tuple(idxs[v] for v in e) for e in Es]); check(rg['REAL'] > 0, 'positive control generic method on APs of {0,2,3,5,8,13}: %s' % rg)

# ================================================================ E. Q8 embeddings in each X_i
P('=== E. Q8 in every X_i: pairs (a,b) with three edges each covering the same six other vertices')
for i, E in enumerate(X):
    V = verts(E); at = {v: [e for e in E if v in e] for v in V}
    occ = []
    for a in V:
        for b in V:
            if a == b: continue
            for ea in combinations(at[a], 3):
                Sa = set(v for e in ea for v in e if v != a)
                if len(Sa) != 6 or b in Sa: continue
                for eb in combinations(at[b], 3):
                    Sb = set(v for e in eb for v in e if v != b)
                    if Sb == Sa and a not in Sb:
                        sub = list(ea) + list(eb)
                        f = isomorphic(Q8, sub)
                        occ.append((a, b, sub, f))
    check(len(occ) > 0 and all(o[3] is not None for o in occ), 'X_%d contains Q8: %d ordered occurrences, all isomorphic to Q8 by explicit map' % (i, len(occ)))
    a, b, sub, f = occ[0]
    P('   X_%d: a=%d, b=%d, edges %s; embedding Q8->X_%d: %s' % (i, a, b, sub, i, f))

# ================================================================ F. decompositions of the top branches, brute force
P('=== F. decompositions (24, 20, S\'=2) and (24, 19, S\'=0), own brute force')
def types_for(nk):
    T = []
    if nk == 1: return [(1, 0, 0)]
    if nk < 3: return []
    for mk in range(math.ceil((nk - 1) / 2), nk - 1):
        for tk in range(1, mk + 1):
            if 17 * tk <= 5 * nk + 3 * mk and 3 * nk + 2 * mk - 11 * tk >= 0: T.append((nk, mk, tk))
    return T
def decomps(N, M, S):
    res = set()
    def rec(nleft, mleft, sleft, minpart, cur):
        if nleft == 0:
            if mleft == 0 and sleft == 0: res.add(tuple(sorted(cur)))
            return
        for nk in range(minpart, nleft + 1):
            for typ in types_for(nk):
                sl = 3 * typ[0] + 2 * typ[1] - 11 * typ[2]
                if typ[1] <= mleft and sl <= sleft: rec(nleft - nk, mleft - typ[1], sleft - sl, nk, cur + [typ])
    rec(N, M, S, 1, []); return sorted(res)
D3 = decomps(24, 20, 2); D4 = decomps(24, 19, 0)
P('   d=3: %s' % D3); P('   d=4: %s' % D4)
check(set(D3) == {((24, 20, 10),), ((12, 10, 5), (12, 10, 5)), ((10, 8, 4), (14, 12, 6)), ((3, 1, 1), (21, 19, 9))}, 'd=3 decompositions as in 2.2')
check(set(D4) == {((24, 19, 10),), ((10, 7, 4), (14, 12, 6)), ((3, 1, 1), (21, 18, 9))}, 'd=4 decompositions as in 2.2')
sizes = {}
import glob, os
for p in glob.glob(TOPCELL + '/**/cell_*.txt', recursive=True):
    m = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', p); sizes[tuple(map(int, m.groups()))] = sum(1 for l in open(p) if l.startswith('FOUND:'))
P('   archived top-level component lists: %s' % sizes)
n3 = sizes[(24, 20, 10, 3)] + math.comb(sizes[(12, 10, 5, 3)] + 1, 2) + sizes[(10, 8, 4, 3)] * sizes[(14, 12, 6, 3)] + sizes[(21, 19, 9, 3)] * sizes[(3, 1, 1, 3)]
n4 = sizes[(24, 19, 10, 4)] + sizes[(10, 7, 4, 4)] * sizes[(14, 12, 6, 4)] + sizes[(21, 18, 9, 4)] * sizes[(3, 1, 1, 4)]
check(n3 == 15429 and n4 == 67, 'input counts: d=3 %d (15,429), d=4 %d (67)' % (n3, n4))

# ================================================================ G. the witness C25
P('=== G. witness C25')
B11 = [0, 2009010, 2901878, 3392944, 3459949, 3705482, 3750000, 3794746, 3884010, 4018020, 7500000]
C25 = sorted(A_BASE + [10 ** 9 + 7919 * x for x in B11])
claim = json.load(open('/home/user/Erdos-757/results/claims/C007-c25-witness-f25.json'))
check(claim['set'] == C25 and claim['claimed_h'] == 15, 'claim C007 set == A_base u (10^9 + 7919 B11), claimed_h 15')
rec11 = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['11']
check(rec11['set'] == B11 and rec11['h'] == 7, 'B11 is the stored 11-point record with h = 7')
check(len(set(C25)) == 25, '25 distinct integers')
bad4 = sum(1 for B in combinations(C25, 4) if len({abs(x - y) for x, y in combinations(B, 2)}) < 5)
check(bad4 == 0, 'all 12,650 four-point subsets have >= 5 distinct differences (violations %d)' % bad4)
sums = [a + b for a, b in combinations(C25, 2)]; check(len(set(sums)) == len(sums), 'weak Sidon')
E25 = ap_edges(C25); check(len(E25) == 20, '%d three-term APs' % len(E25))
cross = sum(1 for e in E25 if any(v < 10 ** 9 for v in e) and any(v >= 10 ** 9 for v in e)); check(cross == 0, 'no AP uses both parts')
# h by two own methods: (1) n - tau of the AP hypergraph (valid: in a weak Sidon set, Sidon <=> 3-AP-free); (2) direct maximum Sidon subset
idx25 = {a: i for i, a in enumerate(C25)}; E25i = [tuple(idx25[v] for v in e) for e in E25]
t25, cov25 = tau(E25i); check(t25 == 10, 'tau(H(C25)) = %d (cover %s)' % (t25, cov25))
def is_sidon(S):
    d = set()
    for a, b in combinations(sorted(S), 2):
        if b - a in d: return False
        d.add(b - a)
    return True
best = [0]
def mis(i, chosen, n):
    if len(chosen) + (n - i) <= best[0]: return
    if i == n:
        best[0] = max(best[0], len(chosen)); return
    # try include i
    if all(not set(e) <= set(chosen) | {i} for e in E25i if i in e):
        mis(i + 1, chosen + [i], n)
    mis(i + 1, chosen, n)
mis(0, [], 25); check(best[0] == 15, 'largest 3-AP-free subset (own DFS) = %d' % best[0])
S15 = [C25[i] for i in range(25) if i not in cov25]; check(len(S15) == 15 and is_sidon(S15), 'complement of the 10-cover is a Sidon set of size 15 (checked by the definition)')
check(is_sidon(claim['witness_sidon_subset']) and len(claim['witness_sidon_subset']) == 15 and set(claim['witness_sidon_subset']) <= set(C25), 'claim witness Sidon subset is Sidon, size 15, inside C25')
# any Sidon 16-subset?  Sidon <=> 3-AP-free (weak Sidon) so no; direct check on a sample is unnecessary: the DFS above is exact.
hA = 14 - tau([tuple(idxA[v] for v in e) for e in EA])[0]; idxB = {a: i for i, a in enumerate(B11)}; hB = 11 - tau([tuple(idxB[v] for v in e) for e in ap_edges(B11)])[0]
check(hA == 8 and hB == 7, 'h(A_base) = %d, h(B11) = %d (so the gluing has h <= 15 by K1 and = 15 here)' % (hA, hB))

# ================================================================ H. Corollary 5 arithmetic
P('=== H. Corollary 5 arithmetic for n = 23..30')
for nn in range(23, 31):
    need = math.ceil(4 * nn / 7) - 1
    hy = nn - (8 * nn - 6) // 17
    P('   n=%d: record needs h <= %d; HY gives h >= %d; excluded by HY alone: %s; ceil(n/2)+2 = %d' % (nn, need, hy, hy > need, math.ceil(nn / 2) + 2))
check([nn for nn in range(23, 31) if nn - (8 * nn - 6) // 17 > math.ceil(4 * nn / 7) - 1] == [24, 26, 28], 'HY alone excludes exactly n = 24, 26, 28 in 23..30')
check(25 - (8 * 25 - 6) // 17 == 14 and math.ceil(25 / 2) + 2 == 15, 'HY bound at 25 is 14; ceil(25/2)+2 = 15')
# K8 at n=25: which (m, tau) allow h <= 14
cells = [(m, 11) for m in range(0, 24) if 17 * 11 <= 5 * 25 + 3 * m]
check(cells == [(21, 11), (22, 11), (23, 11)], 'K8 allows tau = 11 at n = 25 only for m in {21,22,23} (I11 slacks %s)' % [75 + 2 * m - 121 for m, _ in cells])

P('=== SUMMARY: %d failures' % len(FAILS))
for f in FAILS: P('   FAIL: ' + f)
open('/home/user/Erdos-757/experiments/referee/L023-round1-fable/own/verify_main_output.txt', 'w').write('\n'.join(out) + '\n')
