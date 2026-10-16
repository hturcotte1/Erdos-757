"""Referee L006, Route C: independent re-implementation (no e757, no authors' code) of the per-class counters of
extend12_all.py, with h computed from the Sidon DEFINITION (not 3-AP hypergraphs):
  Px_size, n_single_45, t1_pairs, n_t1b_45, t2_isect_pts, n_max_sidon, plus: h(A u x) = 8 for every admissible single,
  h(B) = 9 for every (4,5) T1b pair (exhibit a Sidon 9-subset T u {x,y}), and for every a in A a maximum Sidon subset avoiding a.
Arithmetic: integers after scaling A by 4 (all candidates are then integers; asserted); T2 intersections as integer homogeneous points.
Usage: python3 route_C.py CENSUS_IDX,... NPROC
"""
import gzip, json, sys, itertools, time
from math import gcd
from multiprocessing import Pool
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'

def is_sidon(S):
    seen = set(); n = len(S)
    for i in range(n):
        for j in range(i, n):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True

def nd(Q):
    return len({abs(u - v) for u, v in itertools.combinations(Q, 2)})

def ap_partners(P):
    """all reals forming a 3-term AP with two distinct points of P, as exact halves: returns set of 2*value (ints)"""
    out = set()
    for u, v in itertools.permutations(P, 2):
        out.add(u + v)            # 2*midpoint
        out.add(2 * (2 * u - v))  # 2*endpoint (u is the middle term)
    return out

def run(item):
    idx, A0 = item
    t0 = time.time()
    A = sorted(4 * a for a in A0); AS = set(A); n = len(A)
    r = {'class': idx}
    assert all(nd(Q) >= 5 for Q in itertools.combinations(A, 4))
    assert not any(is_sidon(S) for S in itertools.combinations(A, 8))
    Ts = [T for T in itertools.combinations(A, 7) if is_sidon(T)]
    r['n_max_sidon'] = len(Ts)
    # T2 generic: for every a some maximum Sidon subset avoids a
    r['t2_all_a_avoidable'] = all(any(a not in T for T in Ts) for a in A)
    # Px (as doubled values -> must be even, i.e. integer candidates in x4 coordinates)
    Px2 = ap_partners(A)
    assert all(v % 2 == 0 for v in Px2)
    Px = sorted({v // 2 for v in Px2} - AS)
    r['Px_size'] = len(Px)
    tri = list(itertools.combinations(A, 3)); prs = list(itertools.combinations(A, 2))
    okc = {}
    def single45(v):
        if v not in okc: okc[v] = all(nd(q + (v,)) >= 5 for q in tri)
        return okc[v]
    singles = [x for x in Px if single45(x)]
    r['n_single_45'] = len(singles)
    # h(A u x) = 8 for each admissible x (Sidon definition: some T u {x} is Sidon; 9-subsets would contain 8 points of A)
    r['h_single_all_8'] = all(any(is_sidon(T + (x,)) for T in Ts) for x in singles)
    pairs = set()
    for x in singles:
        Y2 = ap_partners(A + [x]); assert all(v % 2 == 0 for v in Y2)
        for y in {v // 2 for v in Y2} - AS - {x}:
            pairs.add((min(x, y), max(x, y)))
    r['t1_pairs'] = len(pairs)
    good = []
    for x, y in pairs:
        if not single45(x) or not single45(y): continue
        if all(nd(q + (x, y)) >= 5 for q in prs): good.append((x, y))
    r['n_t1b_45'] = len(good)
    r['t1b_all_h9'] = all(any(is_sidon(T + (x, y)) for T in Ts) for x, y in good)
    # T2 lines in ordered (x,y): a*X + b*Y = c ; x_mid: 2x - y = a ; y_mid: -x + 2y = a ; a_mid: x + y = 2a
    lines = []
    for a in A:
        lines += [(2, -1, a), (-1, 2, a), (1, 1, 2 * a)]
    pts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0: continue
        X = c1 * b2 - c2 * b1; Y = a1 * c2 - a2 * c1
        if det < 0: det, X, Y = -det, -X, -Y
        g = gcd(gcd(abs(X), abs(Y)), det); X //= g; Y //= g; d = det // g
        if X == Y or any(X == d * v or Y == d * v for v in A): continue
        pts.add((X, Y, d))
    r['t2_isect_pts'] = len(pts)
    def b45(X, Y, d):
        AD = [d * v for v in A]
        return all(nd(q + (X,)) >= 5 and nd(q + (Y,)) >= 5 for q in itertools.combinations(AD, 3)) and all(nd(q + (X, Y)) >= 5 for q in itertools.combinations(AD, 2))
    r['t2_isect_45'] = sum(1 for p in pts if b45(*p))
    r['secs'] = round(time.time() - t0, 1)
    return r

if __name__ == '__main__':
    cen = json.load(gzip.open(CENSUS, 'rt'))
    items = [(int(i), cen[int(i)]['set']) for i in sys.argv[1].split(',')]
    with Pool(int(sys.argv[2])) as pool:
        for r in pool.imap(run, items):
            print(json.dumps(r), flush=True)
