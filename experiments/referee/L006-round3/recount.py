"""Independent recount (own code, no repo imports) of the case-analysis counters of extend12_all for chosen classes, with h from the
Sidon definition: h(A u x) >= 8 via some max Sidon T with T u {x} Sidon; h(B) >= 9 via some T with T u {x,y} Sidon."""
import gzip, json, itertools, sys
from fractions import Fraction as F
from multiprocessing import Pool
def is_sidon(S):
    seen = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True
def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})
def third_points(P):
    out = set()
    for a, b in itertools.combinations(P, 2):
        if (a + b) % 2 == 0: out.add((a + b) // 2)
        out.add(2 * a - b); out.add(2 * b - a)
    return out - set(P)
cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
def count(c):
    A = sorted(4 * a for a in cen[c]['set']); n = len(A)
    Ts = [T for T in itertools.combinations(A, 7) if is_sidon(T)]
    assert Ts and not any(is_sidon(S) for S in itertools.combinations(A, 8))
    tri = list(itertools.combinations(A, 3)); prs = list(itertools.combinations(A, 2))
    ok1 = {}
    def single(v):
        if v not in ok1: ok1[v] = all(nd((v,) + t) >= 5 for t in tri)
        return ok1[v]
    Px = third_points(A); singles = sorted(v for v in Px if single(v))
    h_single_ok = all(any(is_sidon(list(T) + [x]) for T in Ts) for x in singles)
    pairs = set()
    for x in singles:
        for y in third_points(A + [x]): pairs.add(frozenset((x, y)))
    p45 = [p for p in pairs if all(single(v) for v in p) and all(nd(tuple(p) + q) >= 5 for q in prs)]
    h_pair_ok = all(any(is_sidon(list(T) + list(p)) for T in Ts) for p in p45)
    # T2 lines a x + b y = g (x mid: 2x - y = a; y mid: -x + 2y = a; a mid: x + y = 2a); distinct pairwise intersections
    L = [(2, -1, a) for a in A] + [(-1, 2, a) for a in A] + [(1, 1, 2 * a) for a in A]
    pts = set()
    for (a1, b1, g1), (a2, b2, g2) in itertools.combinations(L, 2):
        d = a1 * b2 - a2 * b1
        if d == 0: continue
        pts.add((F(g1 * b2 - g2 * b1, d), F(a1 * g2 - a2 * g1, d)))
    S = set(A)
    pts = [p for p in pts if p[0] != p[1] and p[0] not in S and p[1] not in S]
    def ext45(p):
        from math import lcm
        D = lcm(p[0].denominator, p[1].denominator); AD = [a * D for a in A]; x, y = int(p[0] * D), int(p[1] * D)
        return all(nd((x,) + q) >= 5 and nd((y,) + q) >= 5 for q in itertools.combinations(AD, 3)) and all(nd((x, y) + q) >= 5 for q in itertools.combinations(AD, 2))
    return {'class': c, 'n_max_sidon': len(Ts), 'Px_size': len(Px), 'n_single_45': len(singles), 't1_pairs': len(pairs), 'n_t1b_45': len(p45),
            't2_isect_pts': len(pts), 't2_isect_45': sum(1 for p in pts if ext45(p)), 'h_single_all_8': h_single_ok, 'h_pair_all_9': h_pair_ok}
if __name__ == '__main__':
    ids = json.load(open('rerun_ids.json'))[::2]
    st = {}
    for l in gzip.open('/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz', 'rt'):
        r = json.loads(l); st[r['class']] = r
    with Pool(2) as pool: res = pool.map(count, ids, chunksize=1)
    keys = ('n_max_sidon', 'Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_isect_pts', 't2_isect_45')
    mism = [(r['class'], k, r[k], st[r['class']][k]) for r in res for k in keys if r[k] != st[r['class']][k]]
    print('classes', len(res), 'counter mismatches vs stored rows:', mism)
    print('all singles h=8 (Sidon 8-subset exhibited):', all(r['h_single_all_8'] for r in res), '; all T1b (4,5) pairs h=9 (Sidon 9-subset exhibited):', all(r['h_pair_all_9'] for r in res))
    print('totals: singles', sum(r['n_single_45'] for r in res), 'T1b (4,5) pairs', sum(r['n_t1b_45'] for r in res), 'isect pts', sum(r['t2_isect_pts'] for r in res), 'isect (4,5)', sum(r['t2_isect_45'] for r in res))
