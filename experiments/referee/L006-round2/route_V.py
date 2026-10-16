"""Referee round 2, Route V: complete type enumeration of the (x,y)-plane by the arrangement of ALL sum relations.
Own code: imports neither e757 nor the authors' scripts nor the judge.

For B = A u {X, Y}, every property in question (distinctness, (4,5), the Sidon property of each subset) depends only on
which relations p+q = r+s (p,q,r,s in B, multisets {p,q} != {r,s}) hold.  A relation involving X or Y non-trivially is a
line c_x x + c_y y + c_0 = 0.  Types: DEG (reduces to u = v), AP (2u = v + w, u,v,w distinct), PAR (u+v = w+z, 4 distinct;
then {u,v,w,z} has |u-w| = |z-v| and |u-z| = |w-v|, i.e. at most 4 distances, so no point of a PAR line is (4,5)).
A point (x,y) with B distinct and (4,5) lies on no DEG/PAR line, so either on no line (generic type), or on exactly one
line, which is then a pure-AP line (its type = the generic type of that line), or on >= 2 pure-AP lines (a vertex).
We evaluate one point of every such type from scratch: (4,5) by counting distances, h by an exact maximum-Sidon search
(distinct positive differences).  Output per class: counts, min h, all (4,5) vertex pairs, deficient points.
Usage: python3 route_V.py IDS_JSON_OR_CSV OUT.jsonl NPROCS [--control]"""
import gzip, json, sys, os, time
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
from multiprocessing import Pool

ROOT = '/home/user/Erdos-757'

def ndist(q):
    return len({abs(u - v) for u, v in combinations(q, 2)})

def max_sidon(vals):
    """exact max size of a subset of vals (distinct ints) with all positive differences distinct"""
    vals = sorted(vals); n = len(vals)
    best = [0]
    def rec(i, chosen, used, size):
        if size > best[0]: best[0] = size
        for k in range(i, n):
            if size + (n - k) <= best[0]: return
            v = vals[k]
            nd = {v - c for c in chosen}
            if not (nd & used):
                chosen.append(v)
                rec(k + 1, chosen, used | nd, size + 1)
                chosen.pop()
    rec(0, [], frozenset(), 0)
    return best[0]

def norm(L):
    cx, cy, c0 = L
    g = gcd(gcd(abs(cx), abs(cy)), abs(c0))
    cx, cy, c0 = cx // g, cy // g, c0 // g
    if cx < 0 or (cx == 0 and cy < 0): cx, cy, c0 = -cx, -cy, -c0
    return (cx, cy, c0)

def classify(m1, m2):
    a = list(m1); b = list(m2)
    for u in list(a):
        if u in b: a.remove(u); b.remove(u)
    if len(a) == 1: return 'DEG'
    if a[0] == a[1] and b[0] == b[1]: return 'DEG'
    if a[0] == a[1] or b[0] == b[1]: return 'AP'
    return 'PAR'

def arrangement(A):
    """A: sorted list of ints.  Returns dict line -> set of relation types (only lines involving X or Y)."""
    pts = [(0, 0, a) for a in A] + [(1, 0, 0), (0, 1, 0)]
    N = len(pts)
    ms = [(i, j) for i in range(N) for j in range(i, N)]
    lines = {}
    for (i, j), (k, l) in combinations(ms, 2):
        L = tuple(pts[i][t] + pts[j][t] - pts[k][t] - pts[l][t] for t in range(3))
        if L[0] == 0 and L[1] == 0:
            # constant relation: must never hold among A except APs of A (checked separately)
            continue
        typ = classify((i, j), (k, l))
        lines.setdefault(norm(L), set()).add(typ)
    return lines

def on_line(L, x, y):
    return L[0] * x + L[1] * y + L[2] == 0

def evaluate(A, x, y):
    """returns (status, h) ; status in 'nondistinct', 'not45', 'ok'"""
    if x == y or x in A or y in A: return 'nondistinct', None
    D = lcm(F(x).denominator, F(y).denominator)
    AD = [a * D for a in A]; xi = int(x * D); yi = int(y * D)
    assert xi == x * D and yi == y * D
    for q in combinations(AD, 3):
        if ndist((xi,) + q) < 5 or ndist((yi,) + q) < 5: return 'not45', None
    for q in combinations(AD, 2):
        if ndist((xi, yi) + q) < 5: return 'not45', None
    return 'ok', max_sidon(AD + [xi, yi])

def generic_point_on(L, all_lines, big):
    """a point of line L on no other line of all_lines"""
    cx, cy, c0 = L
    for t0 in (F(big) + F(1, 7), F(big) * 3 + F(2, 11), F(big) * 7 + F(5, 13)):
        if cy != 0:
            x = t0; y = -(cx * x + c0) / F(cy)
        else:
            y = t0; x = F(-c0, cx)
        if all(M == L or not on_line(M, x, y) for M in all_lines):
            assert on_line(L, x, y)
            return x, y
    raise RuntimeError('no generic point found')

def process(item):
    idx, A = item
    t0 = time.time()
    A = sorted(A); n = len(A)
    out = {'class': idx}
    # A itself: distinct, (4,5), h(A) by Sidon search
    assert len(set(A)) == n
    assert all(ndist(q) >= 5 for q in combinations(A, 4)), 'A not (4,5)'
    hA = max_sidon(A); out['hA'] = hA; target = hA + 2
    lines = arrangement(A)
    all_lines = list(lines)
    out['n_lines'] = len(all_lines)
    pure = [L for L, ts in lines.items() if ts == {'AP'}]
    out['n_pure_AP_lines'] = len(pure)
    kind = lambda L: 'V' if L[1] == 0 else ('H' if L[0] == 0 else 'D')
    out['pure_by_kind'] = {k: sum(1 for L in pure if kind(L) == k) for k in 'VHD'}
    big = 10 ** 6 * (max(abs(a) for a in A) + 1)
    res_h = {}
    deficient = []
    # (a) the 2-cell: generic point of the plane
    gx, gy = F(big) + F(1, 7), F(big) * 1000 + F(1, 11)
    assert not any(on_line(M, gx, gy) for M in all_lines)
    st, h = evaluate(A, gx, gy)
    out['cell'] = [st, h]
    if st == 'ok' and h < target: deficient.append(('cell', str(gx), str(gy), h))
    # (b) generic points of pure-AP lines
    gen45 = {'V': 0, 'H': 0, 'D': 0}; genV45 = []
    for L in pure:
        x, y = generic_point_on(L, all_lines, big)
        st, h = evaluate(A, x, y)
        if st == 'ok':
            gen45[kind(L)] += 1
            res_h[h] = res_h.get(h, 0) + 1
            if kind(L) == 'V': genV45.append(str(F(-L[2], L[0])))
            if h < target: deficient.append(('line', list(L), str(x), str(y), h))
    out['generic45_by_kind'] = gen45
    out['genV45'] = sorted(genV45, key=F)
    # (c) vertices: intersections of two distinct non-parallel pure-AP lines
    verts = set()
    for L1, L2 in combinations(pure, 2):
        det = L1[0] * L2[1] - L2[0] * L1[1]
        if det == 0: continue
        x = F(-L1[2] * L2[1] + L2[2] * L1[1], det)
        y = F(-L1[0] * L2[2] + L2[0] * L1[2], det)
        assert on_line(L1, x, y) and on_line(L2, x, y)
        verts.add((x, y))
    out['n_vertices'] = len(verts)
    pairs45 = set(); st_cnt = {}
    for x, y in verts:
        st, h = evaluate(A, x, y)
        st_cnt[st] = st_cnt.get(st, 0) + 1
        if st == 'ok':
            res_h[h] = res_h.get(h, 0) + 1
            pairs45.add(frozenset((x, y)))
            if h < target: deficient.append(('vertex', str(x), str(y), h))
    out['vertex_status'] = st_cnt
    out['n_vertex45_ordered'] = st_cnt.get('ok', 0)
    out['n_vertex45_unordered'] = len(pairs45)
    out['h_hist'] = {str(k): v for k, v in sorted(res_h.items())}
    out['min_h'] = min(res_h) if res_h else None
    out['target'] = target
    out['deficient'] = deficient; out['n_deficient'] = len(deficient)
    # store the unordered (4,5) vertex pairs (sorted, as strings) for exact comparison
    out['pairs45'] = sorted([sorted(map(str, sorted(p))) for p in pairs45])
    out['secs'] = round(time.time() - t0, 1)
    return out

def main():
    spec, outp, nprocs = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if '--control' in sys.argv:
        Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
        items = []
        for u, v in json.loads(spec):
            items.append(('Abase-minus-%d-%d' % (u, v), [a for a in Ab if a not in (u, v)]))
    else:
        cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
        ids = json.load(open(spec)) if spec.endswith('.json') else [int(t) for t in spec.split(',')]
        items = [(c, cen[c]['set']) for c in ids]
    t0 = time.time()
    with Pool(nprocs) as pool, open(outp, 'w') as fo:
        for r in pool.imap_unordered(process, items):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print(r['class'], 'hA', r['hA'], 'lines', r['n_lines'], 'pure', r['pure_by_kind'], 'gen45', r['generic45_by_kind'],
                  'verts', r['n_vertices'], 'v45', r['n_vertex45_unordered'], 'min_h', r['min_h'], 'target', r['target'],
                  'deficient', r['n_deficient'], 'secs', r['secs'], flush=True)
    print('total secs', round(time.time() - t0, 1))

if __name__ == '__main__':
    try: os.nice(5)
    except Exception: pass
    main()
