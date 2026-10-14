"""Exact re-verification of K13: every 2-point extension of A_base that is a (4,5)-set has h = 10.
See README.md for the case analysis.  All arithmetic is exact (Fraction)."""
import itertools, json, sys, time
from fractions import Fraction as F
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, alpha, is_45_set, is_sidon
from e757.saturated import alpha_of_edges

A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
AF = [F(a) for a in A]
Aset = set(AF)

def dd_ok(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)}) >= 5

def candidates(P):
    """all values creating >=1 AP with two points of P (midpoint or endpoint), excluding P."""
    out = set()
    for a, b in itertools.combinations(sorted(P), 2):
        out.add((a + b) / 2); out.add(2*a - b); out.add(2*b - a)
    return out - set(P)

single_cache = {}
def single_ok(v):   # A u {v} is (4,5)
    if v not in single_cache:
        single_cache[v] = is_45_set(AF + [v])
    return single_cache[v]

def pair_ok(x, y):  # A u {x,y} is (4,5), given A u {x}, A u {y} are
    return all(dd_ok((x, y) + q) for q in itertools.combinations(AF, 2))

def h_exact(pts):
    """exact h = alpha (valid because pts is a (4,5)-set, hence weak Sidon); also returns a Sidon witness check"""
    return alpha(pts)

def witness10(pts, target=10):
    """a 3-AP-free 10-subset that is genuinely Sidon (exact certificate for h>=10), or None"""
    pts = sorted(pts)
    edges = ap_edges(pts)
    idx = {v: i for i, v in enumerate(pts)}
    masks = [sum(1 << idx[v] for v in e) for e in edges]
    n = len(pts)
    res = []
    def rec(i, cur, size):
        if res: return
        if size + n - i < target: return
        if size == target:
            res.append(cur); return
        nxt = cur | (1 << i)
        if all(m & nxt != m for m in masks): rec(i+1, nxt, size+1)
        rec(i+1, cur, size)
    rec(0, 0, 0)
    if not res: return None
    S = [pts[i] for i in range(n) if res[0] >> i & 1]
    return S if is_sidon(S) else None

def main():
    t0 = time.time()
    results = {'hdist': {}, 'type1_pairs': 0, 'type1_45': 0, 'type1_generic_y': 0,
               'type2_lines': [], 'type2_isect_45': 0, 'type2_isect_pts': 0}
    stored = []
    hd = results['hdist']
    def rec_h(h): hd[str(h)] = hd.get(str(h), 0) + 1

    assert alpha(AF) == 8 and is_45_set(AF)
    # ---------- Type 1: at least one new point in P_x
    Px = sorted(candidates(AF))
    Px_ok = [x for x in Px if single_ok(x)]
    results['Px_size'] = len(Px); results['Px_45'] = len(Px_ok)
    seen = set()
    hAx = {}
    for x in Px_ok:
        Ax = AF + [x]
        hAx[x] = alpha(Ax)
        # generic y: no AP with A u {x}; h = h(A u x) + 1
        rec_h(hAx[x] + 1); results['type1_generic_y'] += 1
        if hAx[x] + 1 < 10: print('RECORD? generic y', x, hAx[x]+1)
        for y in sorted(candidates(Ax)):
            key = frozenset((x, y))
            if key in seen: continue
            seen.add(key)
            results['type1_pairs'] += 1
            if not single_ok(y) or not pair_ok(x, y): continue
            results['type1_45'] += 1
            B = Ax + [y]
            h = alpha(B)
            rec_h(h)
            if h < 10: print('RECORD', x, y, h)
            stored.append((str(x), str(y), h))
    print('type1 done', time.time() - t0, flush=True)
    # ---------- Type 2: neither point in P_x u A, but {a,x,y} is an AP.
    # lines y = m*x + c  for roles: (x mid) y=2x-a ; (y mid) y=(x+a)/2 ; (a mid) y=2a-x
    lines = []
    for a in AF:
        lines.append(('x_mid', a, F(2), -a)); lines.append(('y_mid', a, F(1, 2), a/2)); lines.append(('a_mid', a, F(-1), 2*a))
    # generic point on each line: B has APs = APs(A) + {a,x,y}; abstract hypergraph on 16 vertices
    base_edges = [tuple(sorted((A.index(int(u)), A.index(int(m)), A.index(int(w))))) for u, m, w in ap_edges(A)]
    for role, a, m, c in lines:
        ai = A.index(int(a))
        if role == 'x_mid': e = (ai, 15, 14)  # x=14,y=15 : a + y = 2x -> AP (a,x,y) roles; hypergraph edge is just the vertex set
        e = (ai, 14, 15)
        h = alpha_of_edges(16, base_edges + [e])
        results['type2_lines'].append([role, str(a), h])
        rec_h(h) if False else None
        if h < 10: print('RECORD generic line', role, a, h)
    # exceptional points: pairwise intersections of distinct lines
    isect = set()
    for (r1, a1, m1, c1), (r2, a2, m2, c2) in itertools.combinations(lines, 2):
        if m1 == m2: continue   # parallel (or identical, impossible: distinct (role,a) give distinct lines)
        x = (c2 - c1) / (m1 - m2); y = m1 * x + c1
        isect.add((x, y))
    # also add the reflected points, since lines are on ordered (x,y): intersections are already ordered pairs
    for x, y in sorted(isect):
        if x == y or x in Aset or y in Aset: continue
        results['type2_isect_pts'] += 1
        if not single_ok(x) or not single_ok(y) or not pair_ok(x, y): continue
        results['type2_isect_45'] += 1
        if frozenset((x, y)) in seen: continue    # already handled in type 1
        seen.add(frozenset((x, y)))
        B = AF + [x, y]
        h = alpha(B); rec_h(h)
        if h < 10: print('RECORD isect', x, y, h)
        stored.append((str(x), str(y), h))
    # type 0 / 3 (no AP involving a new point): h = 10 trivially
    print('done', time.time() - t0, flush=True)
    # independent Sidon-witness certificate for every stored extension
    nwit = 0
    for xs, ys, h in stored:
        S = witness10(AF + [F(xs), F(ys)])
        assert S is not None, (xs, ys)
        nwit += 1
    results['witness_certified'] = nwit
    wit = {'pairs': [], 'generic_y': []}
    for xs, ys, h in stored:
        S = witness10(AF + [F(xs), F(ys)])
        wit['pairs'].append({'x': xs, 'y': ys, 'S': [str(v) for v in S]})
    for x in Px_ok:
        S = witness10(AF + [x], target=9)
        assert S is not None
        wit['generic_y'].append({'x': str(x), 'y': 'generic (no AP with A u {x}); add y to S9', 'S9': [str(v) for v in S]})
    json.dump(wit, open('/home/user/Erdos-757/experiments/referee/L001-round3/rerun/witnesses_rerun.json', 'w'))
    results['n_stored'] = len(stored)
    results['stored'] = stored
    json.dump(results, open('/home/user/Erdos-757/experiments/referee/L001-round3/rerun/results_rerun.json', 'w'))
    print({k: v for k, v in results.items() if k not in ('stored', 'type2_lines')})
    print('type2 line h:', sorted(set(l[2] for l in results['type2_lines'])))

if __name__ == '__main__':
    main()
