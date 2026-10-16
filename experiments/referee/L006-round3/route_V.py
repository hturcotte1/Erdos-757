"""Referee round 3, L006 -- Route V (own design; imports nothing from the repo).
Exact computation, for a finite A with h(A)=k, of every (x,y) in Omega={x!=y, x,y notin A} with h(A u {x,y}) <= k+1 ("deficient"),
and of which of them give a (4,5)-set.  Uses ONLY the Sidon definition (no 3-AP hypergraph, no T0/T1/T2 case split).
Fact used: a Sidon (k+2)-subset of B=A u{x,y} must be T u {x,y} with T a maximum (size-k) Sidon subset of A, so
  (x,y) deficient  <=>  for every maximum Sidon T of A, T u {x,y} is not Sidon  <=>  (x,y) in  cap_T  U_T,
U_T = union of the lines {alpha x + beta y = gamma} on which two distinct formal sums of T u {X,Y} coincide.
Algorithm (line by line): every deficient point lies on some line l of U_{T1} (T1 fixed).  If l is in U_T for all T it is a
"common line" (all its points deficient): decided symbolically for generic (4,5) along l.  Otherwise pick T' with l notin U_{T'};
every deficient point of l lies in the finite set l cap U_{T'}; each such point is re-tested numerically (exact ints) with the Sidon
definition against ALL maximum T, and every deficient point is tested for (4,5) directly.
Usage: python3 route_V.py census ID,ID,...   |  python3 route_V.py control"""
import itertools, json, gzip, sys, time
from fractions import Fraction as F
from math import gcd, lcm

def is_sidon(S):
    seen = set(); S = list(S)
    for i in range(len(S)):
        for j in range(i, len(S)):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True

def max_sidon(A):
    for k in range(len(A), 0, -1):
        Ts = [T for T in itertools.combinations(A, k) if is_sidon(T)]
        if Ts: return k, Ts

def nd(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})

def is45_int(P):
    return all(nd(q) >= 5 for q in itertools.combinations(P, 4))

def norm(a, b, c):
    g = gcd(gcd(a, b), c)
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return (a, b, c)

def lines_of(T, excl):
    E = [(0, 0, t) for t in T] + [(1, 0, 0), (0, 1, 0)]
    sums = [(E[i][0] + E[j][0], E[i][1] + E[j][1], E[i][2] + E[j][2]) for i in range(len(E)) for j in range(i, len(E))]
    L = set()
    for s1, s2 in itertools.combinations(sums, 2):
        a, b, c = s1[0] - s2[0], s1[1] - s2[1], s2[2] - s1[2]   # a x + b y = c
        if a == 0 and b == 0:
            assert c != 0, 'T not Sidon?'
            continue
        l = norm(a, b, c)
        if l in excl: continue
        L.add(l)
    return L

def deficient_pt(px, py, Ts):
    D = lcm(px.denominator, py.denominator)
    xi, yi = int(px * D), int(py * D)
    for T in Ts:
        if is_sidon([t * D for t in T] + [xi, yi]): return False
    return True

def is45_ext(A, px, py):
    D = lcm(px.denominator, py.denominator)
    AD = [a * D for a in A]; xi, yi = int(px * D), int(py * D)
    for q in itertools.combinations(AD, 3):
        if nd((xi,) + q) < 5 or nd((yi,) + q) < 5: return False
    for q in itertools.combinations(AD, 2):
        if nd((xi, yi) + q) < 5: return False
    return True

def generic45_on_line(A, l):
    """min over 4-subsets containing X or Y of the generic number of distinct distances along line l (exact, symbolic)."""
    a, b, c = l
    if b != 0: X = (F(1), F(0)); Y = (F(-a, b), F(c, b))
    else: X = (F(0), F(c, a)); Y = (F(1), F(0))
    P = [(F(0), F(t)) for t in A] + [X, Y]
    n = len(A)
    def canon(u, v):
        d = (u[0] - v[0], u[1] - v[1])
        assert d != (0, 0), 'identically coinciding points on line %s' % (l,)
        if d < (0, 0): d = (-d[0], -d[1])
        return d
    best = 99
    idxs = range(n + 2)
    for q in itertools.combinations(idxs, 4):
        if n not in q and n + 1 not in q: continue
        k = len({canon(P[i], P[j]) for i, j in itertools.combinations(q, 2)})
        best = min(best, k)
    return best

def h_brute(B):
    for k in range(len(B), 0, -1):
        if any(is_sidon(S) for S in itertools.combinations(B, k)): return k

def route_V(A, tag):
    t0 = time.time()
    A = sorted(A); Aset = set(A)
    assert is45_int(A)
    k, Ts = max_sidon(A)
    excl = {(1, -1, 0)} | {(1, 0, a) for a in A} | {(0, 1, a) for a in A}
    U = [lines_of(T, excl) for T in Ts]
    order = sorted(range(len(Ts)), key=lambda i: len(U[i]))
    i1 = order[0]
    common = []; cand = set(); n_noncommon = 0
    for l in U[i1]:
        miss = [i for i in order if l not in U[i]]
        if not miss: common.append(l); continue
        n_noncommon += 1
        a1, b1, g1 = l
        for (a2, b2, g2) in U[miss[0]]:
            det = a1 * b2 - a2 * b1
            if det == 0: continue
            px = F(g1 * b2 - g2 * b1, det); py = F(a1 * g2 - a2 * g1, det)
            if px == py or px in Aset or py in Aset: continue
            cand.add((px, py))
    # numeric re-test with the Sidon definition (T1 and the chosen T' are on the lines by construction; all T are tested)
    defic = [p for p in cand if deficient_pt(p[0], p[1], Ts)]
    defic45 = [p for p in defic if is45_ext(A, p[0], p[1])]
    out = {'tag': tag, 'n': len(A), 'k': k, 'n_maxT': len(Ts), 'lines_T_min_max': [min(map(len, U)), max(map(len, U))],
           'lines_T1': len(U[i1]), 'noncommon_lines_T1': n_noncommon, 'cand_points': len(cand), 'deficient_points': len(defic),
           'deficient_45_points': [[str(p[0]), str(p[1])] for p in defic45]}
    cl = []
    for l in common:
        g = generic45_on_line(A, l)
        cl.append({'line': l, 'generic_min_ndist': g, 'generic_45': g >= 5})
    out['common_lines'] = cl
    out['common_lines_generic45'] = [c['line'] for c in cl if c['generic_45']]
    # confirm any hit by brute-force h
    hits = []
    for p in defic45:
        D = lcm(p[0].denominator, p[1].denominator)
        B = sorted([a * D for a in A] + [int(p[0] * D), int(p[1] * D)])
        hits.append(h_brute(B))
    out['h_of_deficient_45'] = hits
    out['secs'] = round(time.time() - t0, 1)
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'census':
        cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
        for i in [int(v) for v in sys.argv[2].split(',')]:
            r = route_V(cen[i]['set'], i); print(json.dumps(r), flush=True)
    elif mode == 'set':
        r = route_V(json.loads(sys.argv[2]), 'set'); print(json.dumps(r), flush=True)
