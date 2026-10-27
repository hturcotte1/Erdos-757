"""Exact generic realizability of a 3-uniform hypergraph as the AP hypergraph (up to extra forced APs) of a (4,5)-set.
Method: backtracking over injective midpoint labellings; at each node the solution space V of the AP equations is computed
EXACTLY over Q (incremental RREF with Fractions).  Rows r_v in Q^k are the coordinates of the 'generic point' x_v.
A relation is forced on V iff the corresponding combination of the r_v is the zero vector (exact).  Forced events (all necessary
conditions for a (4,5)-set, hence sound pruning for any subspace of V):
  EQ   r_a = r_b (a != b);   SIDON  r_a + r_b = r_c + r_d, {a,b} != {c,d}, a != b, c != d;   NONLIN  two forced 3-APs sharing 2 points.
A leaf (all edges labelled) is realizable iff none of these is forced: then a generic point of V is a (4,5)-set whose AP hypergraph
contains the given edges (and exactly the forced APs F).  (4,5) <=> distinct, weak Sidon, AP-hypergraph linear.
For output a random integer point of V is chosen and verified with e757.core.is_45_set.
"""
import sys, random, itertools, time
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import is_45_set, ap_edges

class Space:
    """RREF of AP equation rows over Q on n columns."""
    def __init__(self, n, rows=None, piv=None):
        self.n = n; self.rows = [] if rows is None else rows; self.piv = [] if piv is None else piv
    def add(self, row):
        """row: list of Fractions. returns new Space (or self if row dependent)."""
        n = self.n; row = list(row)
        for r, c in zip(self.rows, self.piv):
            f = row[c]
            if f:
                row = [x - f * y for x, y in zip(row, r)]
        c = next((j for j in range(n) if row[j]), None)
        if c is None: return self
        inv = 1 / row[c]; row = [x * inv for x in row]
        rows = []
        for r in self.rows:
            f = r[c]
            rows.append([x - f * y for x, y in zip(r, row)] if f else r)
        rows.append(row)
        return Space(n, rows, self.piv + [c])
    def coords(self):
        """rows r_v in Q^k (tuples) of the generic point, k = n - rank."""
        n = self.n; ps = set(self.piv); free = [j for j in range(n) if j not in ps]
        fidx = {f: i for i, f in enumerate(free)}; k = len(free)
        R = [None] * n
        for f in free:
            t = [Fr(0)] * k; t[fidx[f]] = Fr(1); R[f] = tuple(t)
        for r, c in zip(self.rows, self.piv):
            R[c] = tuple(-r[f] for f in free)
        return R, k

def forced_events(R, n):
    """returns (kind, detail, forcedAPs) ; kind None if no violation"""
    if len(set(R)) < n:
        d = {}
        for v in range(n):
            if R[v] in d: return 'EQ', (d[R[v]], v), None
            d[R[v]] = v
    sums = {}
    k = len(R[0])
    for a in range(n):
        for c in range(a + 1, n):
            s = tuple(x + y for x, y in zip(R[a], R[c]))
            if s in sums: return 'SIDON', (sums[s], (a, c)), None
            sums[s] = (a, c)
    F = []
    for b in range(n):
        s = tuple(2 * x for x in R[b])
        if s in sums:
            a, c = sums[s]; F.append((a, b, c))
    # linearity
    for e1, e2 in itertools.combinations(F, 2):
        if len(set(e1) & set(e2)) >= 2: return 'NONLIN', (e1, e2), None
    return None, None, F

def order_edges(E):
    m = len(E); order = []; rem = list(range(m)); cov = set()
    while rem:
        best = max(rem, key=lambda i: (len(cov & set(E[i])), -i)); order.append(best); rem.remove(best); cov |= set(E[best])
    return order

def decide(E, n, find_all=False, seed=1, tlimit=3600):
    E = [tuple(e) for e in E]; m = len(E); order = order_edges(E)
    st = dict(nodes=0, leaves=0, prunes={'EQ': 0, 'SIDON': 0, 'NONLIN': 0}, prune_depth={}, realizations=0, timeout=False)
    t0 = time.time(); lab = [None] * m; used = set(); sols = []
    rnd = random.Random(seed)
    def rec(k, sp):
        if time.time() - t0 > tlimit: st['timeout'] = True; return True
        if k == m:
            R, kk = sp.coords()
            kind, det, F = forced_events(R, n)
            assert kind is None
            st['leaves'] += 1; st['realizations'] += 1
            sols.append((list(lab), kk - 2, R, sp))
            return not find_all
        e = E[order[k]]
        for mid in e:
            if mid in used: continue
            a, c = [v for v in e if v != mid]
            row = [Fr(0)] * n; row[a] += 1; row[c] += 1; row[mid] -= 2
            sp2 = sp.add(row)
            st['nodes'] += 1
            R, kk = sp2.coords()
            kind, det, F = forced_events(R, n)
            if kind:
                st['prunes'][kind] += 1; st['prune_depth'][k + 1] = st['prune_depth'].get(k + 1, 0) + 1
                continue
            lab[order[k]] = (a, mid, c); used.add(mid)
            if rec(k + 1, sp2): return True
            used.discard(mid); lab[order[k]] = None
        return False
    rec(0, Space(n))
    st['secs'] = round(time.time() - t0, 1)
    return sols, st

def explicit_point(sol, n, rnd, bound=10**6, tries=50):
    """choose random integer parameters in V; verify exactly. returns sorted list of ints or None"""
    lab, dim, R, sp = sol
    k = len(R[0])
    for _ in range(tries):
        p = [rnd.randint(-bound, bound) for _ in range(k)]
        vals = [sum(x * y for x, y in zip(R[v], p)) for v in range(n)]
        from math import lcm
        den = 1
        for x in vals: den = lcm(den, Fr(x).denominator)
        iv = [int(x * den) for x in vals]
        if len(set(iv)) < n: continue
        if is_45_set(iv): return iv
    return None
