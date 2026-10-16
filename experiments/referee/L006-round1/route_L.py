"""Referee L006, Route L: exact deficient locus over R^2, Sidon DEFINITION only (no 3-APs, no case analysis, no e757/authors' code).

For a finite integer set A with h(A)=k (computed by brute force from the Sidon definition), and the list Ts of ALL Sidon k-subsets:
  h(A u {x,y}) <= k+1  <=>  for every T in Ts, T u {x,y} is not Sidon      (every (k+2)-subset with >= k+1 points of A is non-Sidon).
On Omega = {x != y, x,y not in A}, "T u {x,y} non-Sidon" <=> (x,y) lies on one of the lines where two of the 45 formal sums
s_i + s_j (i <= j) of T u {x,y} coincide.  So the deficient locus D = (intersection over T of union of lines) cap Omega
= (union of common lines) u (finite point set P), computed exactly (integer line triples, integer homogeneous points).
Claim to test: no point of D gives a (4,5)-set B = A u {x,y}.  Common lines: decided symbolically (affine functions of the
line parameter; ndist <= 4 generically on a line implies ndist <= 4 at every point).  Points: (4,5) tested directly.
Usage: python3 route_L.py CENSUS_IDX,... | python3 route_L.py control
"""
import gzip, json, sys, itertools, time, os
from math import gcd
from multiprocessing import Pool
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'

def is_sidon(S):
    seen = set(); n = len(S)
    for i in range(n):
        si = S[i]
        for j in range(i, n):
            s = si + S[j]
            if s in seen: return False
            seen.add(s)
    return True

def max_sidon(A):
    for k in range(len(A), 0, -1):
        Ts = [T for T in itertools.combinations(A, k) if is_sidon(T)]
        if Ts: return k, Ts

def ndist(Q):
    return len({abs(u - v) for u, v in itertools.combinations(Q, 2)})

def is_45(S):
    return all(ndist(Q) >= 5 for Q in itertools.combinations(S, 4))

def norm(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a //= g; b //= g; c //= g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return (a, b, c)

def lines_of(T, excl):
    el = [(0, 0, t) for t in T] + [(1, 0, 0), (0, 1, 0)]          # (coef_x, coef_y, const)
    sums = [(e[0] + f[0], e[1] + f[1], e[2] + f[2]) for i, e in enumerate(el) for f in el[i:]]
    mm = len(el); assert len(sums) == mm * (mm + 1) // 2 and len(set(sums)) == len(sums)
    L = set()
    for p, q in itertools.combinations(sums, 2):
        a = p[0] - q[0]; b = p[1] - q[1]; c = q[2] - p[2]
        if a == 0 and b == 0:
            assert c != 0          # T is Sidon: no identically-true relation
            continue
        L.add(norm(a, b, c))
    return L - excl

def inter(l1, l2):
    a1, b1, c1 = l1; a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if det == 0: return None
    X = c1 * b2 - c2 * b1; Y = a1 * c2 - a2 * c1
    if det < 0: det, X, Y = -det, -X, -Y
    g = gcd(gcd(abs(X), abs(Y)), det)
    return (X // g, Y // g, det // g)

def in_omega(p, A):
    X, Y, d = p
    if X == Y: return False
    for a in A:
        if X == d * a or Y == d * a: return False
    return True

def nonsidon_at(T, p):
    X, Y, d = p
    return not is_sidon([d * t for t in T] + [X, Y])

def B45_at(A, p):
    X, Y, d = p
    AD = [d * a for a in A]
    for Q in itertools.combinations(AD, 3):
        if ndist(Q + (X,)) < 5 or ndist(Q + (Y,)) < 5: return False
    for Q in itertools.combinations(AD, 2):
        if ndist(Q + (X, Y)) < 5: return False
    return True

def line_generic_45(A, l):
    """True iff the GENERIC point of line l gives a (4,5)-set A u {x,y} (symbolic, exact)."""
    a, b, c = l
    if b != 0: pts = [(b * v, 0) for v in A] + [(0, b), (c, -a)]
    else:      pts = [(a * v, 0) for v in A] + [(c, 0), (0, a)]
    n = len(A)
    def cls(Q):
        s = set()
        for (p0, p1), (q0, q1) in itertools.combinations(Q, 2):
            d0, d1 = p0 - q0, p1 - q1
            assert (d0, d1) != (0, 0)
            if d1 < 0 or (d1 == 0 and d0 < 0): d0, d1 = -d0, -d1
            s.add((d0, d1))
        return len(s)
    for Q in itertools.combinations(range(n + 2), 4):
        if n in Q or n + 1 in Q:
            if cls([pts[i] for i in Q]) <= 4: return False
    return True

def points_on_line(l, A, m=3):
    a, b, c = l; out = []; t = 10**6 + 7
    while len(out) < m:
        t += 9973
        p = (t * b, c - a * t, b) if b != 0 else (c, t * a, a)   # b != 0: x = t, y = (c - a t)/b ; b == 0: x = c/a, y = t
        X, Y, d = p
        if d < 0: X, Y, d = -X, -Y, -d
        g = gcd(gcd(abs(X), abs(Y)), d); p = (X // g, Y // g, d // g)
        if in_omega(p, A): out.append(p)
    return out

def deficient_locus(A, Ts):
    excl = {norm(1, 0, v) for v in A} | {norm(0, 1, v) for v in A} | {norm(1, -1, 0)}
    U = [lines_of(T, excl) for T in Ts]
    order = list(range(len(Ts)))
    # greedy order: next T shares fewest lines with the current common set (any order is exact; this is only for speed)
    L = set(U[0]); P = set(); used = [0]; rest = set(range(1, len(Ts)))
    while rest:
        k = min(rest, key=lambda j: (len(L & U[j]), j)); rest.discard(k); used.append(k)
        T = Ts[k]; Uk = U[k]; Ul = list(Uk)
        P = {p for p in P if nonsidon_at(T, p)}
        for l in L - Uk:
            for m in Ul:
                p = inter(l, m)
                if p is not None and in_omega(p, A): P.add(p)
        L &= Uk
    return L, P, U

def run(item):
    tag, A = item
    t0 = time.time()
    A = sorted(A)
    assert len(set(A)) == len(A)
    out = {'tag': tag, 'n': len(A)}
    out['A_is_45'] = is_45(A)
    k, Ts = max_sidon(A)
    out['h'] = k; out['n_max_sidon'] = len(Ts)
    L, P, U = deficient_locus(A, Ts)
    out['lines_per_T_min_max'] = [min(map(len, U)), max(map(len, U))]
    # re-verify every point of P against every T by the Sidon definition, and Omega
    assert all(in_omega(p, A) for p in P)
    assert all(nonsidon_at(T, p) for p in P for T in Ts), 'point not deficient'
    for l in L:
        for p in points_on_line(l, A):
            assert all(nonsidon_at(T, p) for T in Ts), ('common line not deficient', l)
    out['n_common_lines'] = len(L)
    gen45 = [l for l in L if line_generic_45(A, l)]
    out['common_lines_generic_45'] = [list(l) for l in gen45]
    out['common_lines'] = sorted(list(l) for l in L)
    out['n_points'] = len(P)
    p45 = sorted(p for p in P if B45_at(A, p))
    out['points_45'] = [list(p) for p in p45]
    out['n_points_45'] = len(p45)
    # for any (4,5) deficient point, confirm h(B) <= k+1 by brute force over (k+2)-subsets (Sidon definition)
    conf = []
    for X, Y, d in p45[:20]:
        Bs = [d * a for a in A] + [X, Y]
        conf.append(max(len(S) for r in range(len(Bs), 0, -1) for S in itertools.combinations(Bs, r) if is_sidon(S)) if False else
                    next(r for r in range(len(Bs), 0, -1) if any(is_sidon(S) for S in itertools.combinations(Bs, r))))
    out['h_B_at_45_points'] = conf
    out['secs'] = round(time.time() - t0, 1)
    return out

if __name__ == '__main__':
    try: os.nice(5)
    except Exception: pass
    arg = sys.argv[1]
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if arg == 'control':
        Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
        items = []
        for (u, v) in [(0, 1056), (243, 249), (136, 596), (286, 400)]:
            items.append((f'Abase-minus-{u},{v}', [a for a in Ab if a not in (u, v)]))
    else:
        cen = json.load(gzip.open(CENSUS, 'rt'))
        items = [(int(i), cen[int(i)]['set']) for i in arg.split(',')]
    with Pool(nproc) as pool:
        for r in pool.imap(run, items):
            print(json.dumps(r), flush=True)
