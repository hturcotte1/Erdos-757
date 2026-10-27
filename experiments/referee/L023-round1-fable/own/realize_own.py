"""Referee #2 (fable), L023: own exact realizability decision for the six classes X_0..X_5 (parsed from the certificate text).
Method (certificate 3.1, re-derived in the review): every realization has an injective midpoint labelling lambda: E -> V with
lambda(e) in e (K5), the two unlabelled vertices u < w are the extreme points; normalising x_u = 0, x_w = 1 (affine map), x solves the
square system 2 x_lambda(e) = x_a + x_c, which is non-singular (maximum principle).  So: enumerate every injective lambda (DFS over
the edges, each edge choosing an unused vertex: each lambda exactly once), solve exactly over Q, classify.  No code shared with the
prover or the worker.  Usage: python3 realize_own.py [class indices, default all]"""
import sys, re, time, json
from fractions import Fraction
from itertools import combinations
CERT = '/home/user/Erdos-757/results/proofs/L023-f25-equals-15.md'
def verts(E): return sorted(set(v for e in E for v in e))
def is_linear(E):
    for e, f in combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return False
    return True
def solve_square(rows, rhs, nvar):
    M = [dict(r) for r in rows]; b = list(rhs); piv_rows = set(); piv_of = {}
    for col in range(nvar):
        pr = None
        for i in range(len(M)):
            if i not in piv_rows and M[i].get(col, 0) != 0: pr = i; break
        if pr is None: return None
        piv_of[col] = pr; piv_rows.add(pr)
        inv = Fraction(1) / M[pr][col]
        M[pr] = {k: v * inv for k, v in M[pr].items()}; b[pr] *= inv
        prow = M[pr]; bp = b[pr]
        for i in range(len(M)):
            if i == pr: continue
            c = M[i].get(col, 0)
            if c:
                Mi = M[i]
                for k, v in prow.items():
                    nv = Mi.get(k, 0) - c * v
                    if nv: Mi[k] = nv
                    else: Mi.pop(k, None)
                b[i] -= c * bp
    x = [None] * nvar
    for col, pr in piv_of.items(): x[col] = b[pr]
    return x
def classify_point(x, E):
    V = sorted(x); vals = [x[v] for v in V]
    if len(set(vals)) < len(vals): return 'NONINJ'
    sums = set()
    for a, b in combinations(V, 2):
        s = x[a] + x[b]
        if s in sums: return 'NOTWS'
        sums.add(s)
    aps = set()
    for a, b, c in combinations(V, 3):
        xs = sorted((x[a], x[b], x[c]))
        if xs[0] + xs[2] == 2 * xs[1]: aps.add(frozenset((a, b, c)))
    if not is_linear([tuple(e) for e in aps]): return 'NONLIN'
    if aps != set(frozenset(e) for e in E): return 'APSET'
    return 'REAL'
def sdr_labellings(E):
    def rec(i, used, lam):
        if i == len(E): yield list(lam); return
        for v in E[i]:
            if v not in used:
                used.add(v); lam.append(v)
                yield from rec(i + 1, used, lam)
                lam.pop(); used.discard(v)
    yield from rec(0, set(), [])
def realize_sdr(E):
    V = verts(E); n = len(V); assert len(E) == n - 2
    cnt = {'labellings': 0, 'SINGULAR': 0, 'NONINJ': 0, 'NOTWS': 0, 'NONLIN': 0, 'APSET': 0, 'REAL': 0}; reals = []
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
        if c == 'REAL': reals.append((lam, {v: str(x[v]) for v in V}))
    return cnt, reals
if __name__ == '__main__':
    txt = open(CERT).read(); X = []
    for line in txt.splitlines():
        m = re.match(r'^X_(\d) FOUND: (.*)$', line.strip())
        if m: X.append([tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', m.group(2))])
    assert len(X) == 6
    which = [int(a) for a in sys.argv[1:]] or list(range(6))
    for i in which:
        t0 = time.time(); cnt, reals = realize_sdr(X[i])
        verdict = 'REALIZABLE' if cnt['REAL'] else 'NOT-REALIZABLE'
        print('X_%d %s %s %.1fs' % (i, verdict, json.dumps(cnt), time.time() - t0), flush=True)
        for lam, x in reals[:3]: print('   REAL labelling', lam, x, flush=True)
