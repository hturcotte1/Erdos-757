"""(L023) Independent exact realizability test for SATURATED 3-graphs (m = n - 2) as AP hypergraphs of (4,5)-sets.

No code is shared with experiments/20261027-0400-realize-21-18-9/rexact.py or rexact.c.

Mathematics (proved in results/proofs/L023-f25-equals-15.md, Theorem 3):
 A (4,5)-set A with |A| = n whose AP hypergraph contains the n-2 edges of X (via a bijection V(X) -> A) has
 (i)  AP set exactly E(X) (a (4,5)-set has at most n-2 APs, K5), so its midpoint map lam: E -> V, lam(e) in e, is injective (K3);
 (ii) the two vertices u, w not in lam(E) are min A and max A (K3: the midpoint map never hits min or max);
 (iii) after an affine map (and possibly the reflection x -> -x) x_u = 0, x_w = 1, and the 23 midpoint values solve
       2 x_lam(e) - x_a - x_c = 0 (e = {a, lam(e), c});
 (iv) this square system (unknowns: the n-2 midpoints) is non-singular (maximum principle), so x is its unique solution.
 Hence: X is realizable  <=>  for some injective labelling lam the system is non-singular and its solution is a (4,5)-set.
Algorithm: enumerate ALL injective labellings lam (DFS over the edges, each edge picks an unused vertex of itself);
 for each, solve the system EXACTLY with Fractions (sparse Gauss-Jordan); classify:
   SINGULAR | NONINJ (two equal values) | NOTWS (x_a + x_b = x_c + x_d, {a,b} and {c,d} disjoint) | NONLIN (two APs share 2 points)
   | REAL (a (4,5)-set; its AP set is then re-checked to equal E(X) and is_45_set from e757.core is applied as a cross-check).
usage: python3 realize_sdr.py FILE [maxgraphs]   (FILE: lines 'FOUND: (a,b,c) ...' or JSON list of edge lists via --json)
"""
import sys, re, json, time, itertools
from fractions import Fraction as Fr

def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]

def labellings(E, n):
    """all injective lam with lam(e) in e; yields tuples mids[i] for edge i (in input order)."""
    m = len(E)
    order = []; rem = list(range(m)); cov = set()
    while rem:   # order: most overlap with already chosen vertices first (efficiency only)
        b = max(rem, key=lambda i: (len(cov & set(E[i])), -i)); order.append(b); rem.remove(b); cov |= set(E[b])
    mids = [None] * m
    def rec(k, used):
        if k == m:
            yield tuple(mids); return
        i = order[k]
        for v in E[i]:
            if not (used >> v) & 1:
                mids[i] = v
                yield from rec(k + 1, used | (1 << v))
        mids[i] = None
    yield from rec(0, 0)

def solve(E, n, mids):
    """exact solution with x_u = 0, x_w = 1 (u < w the two vertices that are not midpoints), or None if singular."""
    M = set(mids); bd = [v for v in range(n) if v not in M]
    assert len(bd) == 2
    u, w = bd
    known = {u: Fr(0), w: Fr(1)}
    rows = []
    for e, b in zip(E, mids):
        a, c = [v for v in e if v != b]
        r = {b: Fr(2)}; rhs = Fr(0)
        for v in (a, c):
            if v in known: rhs += known[v]
            else: r[v] = r.get(v, Fr(0)) - 1
        rows.append([r, rhs])
    # Gauss-Jordan on sparse rows; unknowns = mids
    piv = {}   # col -> row index
    for i in range(len(rows)):
        r, rhs = rows[i]
        # eliminate the existing pivot columns from r (pivot rows are fully reduced: Gauss-Jordan)
        for col, j in list(piv.items()):
            if col in r and r[col] != 0:
                f = r[col]; rj, rhsj = rows[j]
                for cc, val in rj.items():
                    nv = r.get(cc, Fr(0)) - f * val
                    if nv: r[cc] = nv
                    else: r.pop(cc, None)
                rhs -= f * rhsj
        r = {cc: val for cc, val in r.items() if val}
        if not r:
            return None   # dependent row: the square system is singular
        col = min(r)      # pivot: the smallest column with a non-zero entry
        f = r[col]
        r = {cc: val / f for cc, val in r.items()}; rhs = rhs / f
        # eliminate col from previous pivot rows
        for c2, j in piv.items():
            rj, rhsj = rows[j]
            if col in rj:
                g = rj[col]
                for cc, val in r.items():
                    nv = rj.get(cc, Fr(0)) - g * val
                    if nv: rj[cc] = nv
                    else: rj.pop(cc, None)
                rows[j][1] = rhsj - g * rhs
        rows[i] = [r, rhs]; piv[col] = i
    if len(piv) != n - 2: return None
    x = dict(known)
    for col, j in piv.items():
        r, rhs = rows[j]
        assert set(r) == {col} and r[col] == 1
        x[col] = rhs
    return [x[v] for v in range(n)]

def classify(x, E, n):
    if x is None: return 'SINGULAR'
    if len(set(x)) < n: return 'NONINJ'
    sums = {}
    for a in range(n):
        for b in range(a + 1, n):
            s = x[a] + x[b]
            if s in sums: return 'NOTWS'
            sums[s] = (a, b)
    # 3-APs of x (as vertex triples): x_a + x_c = 2 x_b
    aps = []
    for b in range(n):
        p = sums.get(2 * x[b])
        if p is not None: aps.append(frozenset((p[0], b, p[1])))
    for e1, e2 in itertools.combinations(aps, 2):
        if len(e1 & e2) >= 2: return 'NONLIN'
    if set(aps) != set(frozenset(e) for e in E): return 'APSET'   # cannot happen for a (4,5)-set (K5), recorded if it does
    return 'REAL'

def decide(E, n, keep=3):
    st = {'labellings': 0, 'SINGULAR': 0, 'NONINJ': 0, 'NOTWS': 0, 'NONLIN': 0, 'APSET': 0, 'REAL': 0}
    ex = []
    for mids in labellings(E, n):
        st['labellings'] += 1
        x = solve(E, n, mids)
        k = classify(x, E, n); st[k] += 1
        if k == 'REAL' and len(ex) < keep: ex.append((mids, x))
    return st, ex

def to_int_set(x):
    from math import lcm
    den = 1
    for v in x: den = lcm(den, v.denominator)
    return [int(v * den) for v in x]

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fn = args[0]; mx = int(args[1]) if len(args) > 1 else 10**9
    if '--json' in sys.argv:
        graphs = [ [tuple(e) for e in g] for g in json.load(open(fn)) ]
    else:
        graphs = [parse(l) for l in open(fn) if l.startswith('FOUND:')]
    sys.path.insert(0, '/home/user/Erdos-757')
    from e757.core import is_45_set, ap_edges
    tot = {}
    for gi, E in enumerate(graphs[:mx]):
        n = 1 + max(max(e) for e in E); assert len(E) == n - 2, 'not saturated'
        t0 = time.time(); st, ex = decide(E, n)
        line = 'GRAPH %d n=%d m=%d %s %s' % (gi, n, len(E), 'REALIZABLE' if st['REAL'] else 'NOT-REALIZABLE', json.dumps(st))
        if ex:
            iv = to_int_set(ex[0][1]); s = sorted(iv)
            line += ' example=%s is_45_set=%s num_aps=%d' % (s, is_45_set(s), len(ap_edges(s)))
        print(line, 'secs=%.1f' % (time.time() - t0), flush=True)
